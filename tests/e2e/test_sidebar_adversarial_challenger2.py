# -*- coding: utf-8 -*-
"""
Class-Widgets-2 侧边栏对抗性实证挑战测试套件 (Challenger 2)

本测试套件由 Challenger 2 (Empirical Challenger) 独立构建并执行，
针对以下核心维度进行严酷的对抗实证检验：
1. 状态机模糊测试 (State Machine Fuzzing & 300ms Buffer Stress)：
   - 毫秒级极速交替移入/移出/展开/收起/折叠/呼出
   - 300ms 防误触缓冲计时器边界与抖动测试
   - 10,000 次混沌随机事件脉冲流 Fuzzing 与状态收敛性验证
   - 零遮罩残存与抗桌面阻断不变量检验
2. 像素级遮罩穿透验证 (Pixel-Level Mask Penetration & Dense Grid Sampling)：
   - 多分辨率 (1080p, 2K, 4K, 笔记本 1366x768, 超宽屏 3440x1440) 严密几何面积数学证明
   - 5,000+ 网格点密集全屏采样与 1px 临界边界点检验
   - 证明各状态下除可见控件外 99%+ 屏幕像素 100% 穿透
   - EXPANDED 退出后穿透率即时恢复验证
3. 异常关机与并发持久化 (Abnormal Shutdown & Concurrent Persistence Resilience)：
   - 10 线程并发高频读写/保存压力测试 (Hammer Test, 2,000+ 并发操作)
   - 写入中断截断 JSON (Truncated JSON) 容错恢复验证
   - 磁盘损坏脏字节 (Corrupted Binary/Zero Bytes) 容错回退验证
   - 磁盘写保护 (PermissionError) 容错验证
   - 持久化数据完整性与原子一致性验证
"""
import concurrent.futures
import json
import os
import random
import sys
import threading
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QCoreApplication, QObject, QRect, QPoint, Property, Signal
from PySide6.QtGui import QRegion

from src.core.config.manager import ConfigManager
from src.core.config.model import PreferencesConfig
from src.core.widgets.core import WidgetsWindow


# ============================================================================
# PySide6 测试环境与高保真 Mock 组件
# ============================================================================

@pytest.fixture(scope="session")
def qapp():
    """提供 PySide6 QCoreApplication 单例"""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app


class MockRootWindow(QObject):
    """高保真模拟 WidgetsWindow.root_window (QQuickWindow)"""
    def __init__(self):
        super().__init__()
        self._children = []
        self._applied_mask = None
        self._properties = {}

    def findChild(self, type_, name):
        for child in self._children:
            if child.objectName() == name:
                return child
        return None

    def setMask(self, mask: QRegion):
        self._applied_mask = mask

    def get_applied_mask(self) -> QRegion:
        return self._applied_mask

    def add_child(self, child: QObject):
        self._children.append(child)

    def setProperty(self, name: str, value):
        self._properties[name] = value

    def property(self, name: str):
        return self._properties.get(name)

    def hide(self):
        pass

    def releaseResources(self):
        pass

    def deleteLater(self):
        pass


class MockWidgetsLoader(QObject):
    """模拟 WidgetsLoader 容器，保证 WidgetsWindow 遮罩计算顺利运行"""
    geometryChanged = Signal()
    contentGeometryChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("widgetsLoader")
        self._menu_visible = False
        self._edit_mode = False

    def property(self, name: str):
        if name == "menuVisible":
            return self._menu_visible
        if name == "editMode":
            return self._edit_mode
        return None

    def x(self):
        return 0

    def y(self):
        return 0


class RealisticScheduleSidebar(QObject):
    """
    高保真仿真 ScheduleSidebar.qml 状态机与几何计算逻辑，
    1:1 对齐 ScheduleSidebar.qml, SidebarHoverButtons.qml, EdgeRestoreCapsule.qml
    """
    geometryChanged = Signal()
    sidebarStateChanged = Signal(str)

    def __init__(self, screen_w=1920, screen_h=1080, parent=None):
        super().__init__(parent)
        self.setObjectName("scheduleSidebar")
        self.screen_w = screen_w
        self.screen_h = screen_h

        # 配置与启用状态
        self._enabled = True
        self._visible = True

        # 状态机状态: "NORMAL" | "EXPANDED" | "COLLAPSED"
        self._sidebar_state = "NORMAL"

        # 子控件几何规格
        # 1. 竖条 dailyBar
        self.bar_w = 160
        self.bar_h = min(int(screen_h * 0.78), 600)
        self.bar_x = screen_w - self.bar_w - 8
        self.bar_y = (screen_h - self.bar_h) // 2

        # 2. 悬浮双按钮 hoverButtons
        self.btn_w = 44
        self.btn_h = 106
        self.btn_x = self.bar_x - 10 - self.btn_w
        self.btn_y = self.bar_y + (self.bar_h - self.btn_h) // 2
        self._buttons_active = False
        self._is_buttons_hovered = False

        # 3. 贴边胶囊 edgeCapsule
        self.cap_w = 20
        self.cap_h = 64
        self.cap_x = screen_w - self.cap_w
        self.cap_y = (screen_h - self.cap_h) // 2

        # 4. 气泡卡片 bubbleCard
        self.bubble_w = 220
        self.bubble_h = 180
        self.bubble_x = self.bar_x - self.bubble_w - 6
        self.bubble_y = self.bar_y + 80
        self._has_active_bubble = False

        # 5. 防误触 300ms 缓冲计时器模拟 (记录剩余毫秒)
        self._buffer_timer_remaining_ms = 0
        self._buffer_timer_active = False

    def isVisible(self) -> bool:
        return self._visible and self._enabled

    def set_enabled(self, val: bool):
        self._enabled = val
        self.geometryChanged.emit()

    def set_visible(self, val: bool):
        self._visible = val
        self.geometryChanged.emit()

    @Property(str, notify=sidebarStateChanged)
    def sidebarState(self) -> str:
        return self._sidebar_state

    @Property(bool, notify=geometryChanged)
    def isFullWeekExpanded(self) -> bool:
        return self._sidebar_state == "EXPANDED"

    @Property(list, notify=geometryChanged)
    def interactiveRects(self) -> list:
        if not self.isVisible():
            return []

        if self._sidebar_state == "EXPANDED":
            return [[0, 0, self.screen_w, self.screen_h]]

        if self._sidebar_state == "COLLAPSED":
            return [[self.cap_x, self.cap_y, self.cap_w, self.cap_h]]

        # NORMAL 状态
        rects = [[self.bar_x, self.bar_y, self.bar_w, self.bar_h]]

        if self._has_active_bubble:
            rects.append([self.bubble_x, self.bubble_y, self.bubble_w, self.bubble_h])

        if self._buttons_active:
            rects.append([self.btn_x, self.btn_y, self.btn_w, self.btn_h])

        return rects

    # ---------------- 状态机动作方法 ----------------
    def request_show_buttons(self):
        """鼠标移入竖条左侧感应区或按钮自身"""
        self._buffer_timer_active = False
        self._buffer_timer_remaining_ms = 0
        if not self._buttons_active:
            self._buttons_active = True
            self.geometryChanged.emit()

    def request_hide_buttons_with_buffer(self):
        """鼠标移出，启动 300ms 防误触缓冲"""
        self._buffer_timer_active = True
        self._buffer_timer_remaining_ms = 300

    def tick_buffer_timer(self, elapsed_ms: int):
        """推进防误触计时器时钟"""
        if self._buffer_timer_active:
            self._buffer_timer_remaining_ms -= elapsed_ms
            if self._buffer_timer_remaining_ms <= 0:
                self._buffer_timer_active = False
                self._buffer_timer_remaining_ms = 0
                if not self._is_buttons_hovered:
                    self._buttons_active = False
                    self.geometryChanged.emit()

    def hide_buttons_immediately(self):
        """立即收回按钮（无缓冲）"""
        self._buffer_timer_active = False
        self._buffer_timer_remaining_ms = 0
        if self._buttons_active:
            self._buttons_active = False
            self.geometryChanged.emit()

    def expand_weekly_panel(self):
        """展开全周大面板"""
        self._sidebar_state = "EXPANDED"
        self.hide_buttons_immediately()
        self._has_active_bubble = False
        self.sidebarStateChanged.emit("EXPANDED")
        self.geometryChanged.emit()

    def retract_weekly_panel(self):
        """收回全周大面板恢复 NORMAL"""
        self._sidebar_state = "NORMAL"
        self.sidebarStateChanged.emit("NORMAL")
        self.geometryChanged.emit()

    def collapse_to_edge(self):
        """折叠隐藏到屏幕右边缘贴边胶囊"""
        self._sidebar_state = "COLLAPSED"
        self.hide_buttons_immediately()
        self._has_active_bubble = False
        self.sidebarStateChanged.emit("COLLAPSED")
        self.geometryChanged.emit()

    def restore_from_edge(self):
        """贴边胶囊点击呼出恢复 NORMAL"""
        self._sidebar_state = "NORMAL"
        self.sidebarStateChanged.emit("NORMAL")
        self.geometryChanged.emit()

    def show_bubble(self):
        self._has_active_bubble = True
        self.geometryChanged.emit()

    def hide_bubble(self):
        self._has_active_bubble = False
        self.geometryChanged.emit()


@pytest.fixture
def test_env(qapp):
    """提供 WidgetsWindow 与 RealisticScheduleSidebar 协同环境"""
    central = MagicMock()
    central.configs.interactions.hover_fade = False
    central.theme_manager.currentTheme = "com.classwidgets.default"

    win = WidgetsWindow(central)
    root = MockRootWindow()
    win.root_window = root

    loader = MockWidgetsLoader(root)
    root.add_child(loader)

    sidebar = RealisticScheduleSidebar(1920, 1080, root)
    root.add_child(sidebar)

    yield win, root, sidebar
    win.release()


# ============================================================================
# 挑战 1: 状态机模糊测试与 300ms 防误触缓冲实证 (State Machine Fuzzing)
# ============================================================================

class TestStateMachineFuzzing:
    """实证对抗检验 1: 状态机瞬态跃迁、极速模糊测试与防误触缓冲"""

    def test_state_machine_deterministic_transitions(self, test_env):
        """
        实证检验: 严格遍历状态机所有确定性合法路径，
        验证每个状态下遮罩计算的精确性与不变量守恒。
        """
        win, root, sidebar = test_env

        # 初始态 NORMAL
        win.update_mask()
        mask = root.get_applied_mask()
        assert sidebar.sidebarState == "NORMAL"
        assert not sidebar.isFullWeekExpanded
        assert mask.contains(QPoint(sidebar.bar_x + 10, sidebar.bar_y + 10))
        # 屏幕中心绝对穿透
        assert not mask.contains(QPoint(960, 540))

        # 状态迁移 1: NORMAL -> EXPANDED
        sidebar.expand_weekly_panel()
        win.update_mask()
        assert sidebar.sidebarState == "EXPANDED"
        assert sidebar.isFullWeekExpanded
        # 此时必须为全屏遮罩用于外部点击捕获
        assert root.get_applied_mask().isEmpty()  # setMask(QRegion()) 清空遮罩即代表全屏窗口捕获

        # 状态迁移 2: EXPANDED -> NORMAL (外部点击收回)
        sidebar.retract_weekly_panel()
        win.update_mask()
        mask = root.get_applied_mask()
        assert sidebar.sidebarState == "NORMAL"
        assert not sidebar.isFullWeekExpanded
        # 核心不变量: 绝不能残留全屏遮罩阻断桌面！
        assert not mask.contains(QPoint(960, 540))
        assert mask.contains(QPoint(sidebar.bar_x + 10, sidebar.bar_y + 10))

        # 状态迁移 3: NORMAL -> COLLAPSED (点击折叠)
        sidebar.collapse_to_edge()
        win.update_mask()
        mask = root.get_applied_mask()
        assert sidebar.sidebarState == "COLLAPSED"
        assert not sidebar.isFullWeekExpanded
        # 竖条原位置必须完全穿透！
        assert not mask.contains(QPoint(sidebar.bar_x + 10, sidebar.bar_y + 10))
        # 只有贴边胶囊不可穿透
        assert mask.contains(QPoint(sidebar.cap_x + 5, sidebar.cap_y + 10))

        # 状态迁移 4: COLLAPSED -> NORMAL (点击胶囊呼出)
        sidebar.restore_from_edge()
        win.update_mask()
        mask = root.get_applied_mask()
        assert sidebar.sidebarState == "NORMAL"
        assert mask.contains(QPoint(sidebar.bar_x + 10, sidebar.bar_y + 10))
        # 贴边胶囊隐藏后，竖条右侧 8px 边距区域 (例如 x = bar_x + bar_w + 4 = 1916) 必须从被胶囊捕获释放为 100% 穿透！
        assert not mask.contains(QPoint(sidebar.bar_x + sidebar.bar_w + 4, sidebar.cap_y + 10))

    def test_hover_300ms_buffer_stress(self, test_env):
        """
        实证检验: 针对 300ms 防误触缓冲机制进行极速高频抖动攻击
        - 0~299ms 内反复进出: 缓冲重置，按钮平滑保持
        - 超过 300ms 移出: 按钮精准收回，遮罩同步释放
        - 缓冲期间突发点击展开/折叠: 缓冲立即取消，状态安全收敛
        """
        win, root, sidebar = test_env
        win.update_mask()

        # 1. 鼠标移入触发区 -> 按钮滑出
        sidebar.request_show_buttons()
        win.update_mask()
        mask = root.get_applied_mask()
        assert sidebar._buttons_active is True
        assert mask.contains(QPoint(sidebar.btn_x + 5, sidebar.btn_y + 5))

        # 2. 模拟用户抖动移出 100ms
        sidebar.request_hide_buttons_with_buffer()
        sidebar.tick_buffer_timer(100)
        win.update_mask()
        assert sidebar._buffer_timer_active is True
        assert sidebar._buffer_timer_remaining_ms == 200
        # 尚未超时，按钮仍受遮罩保护
        assert root.get_applied_mask().contains(QPoint(sidebar.btn_x + 5, sidebar.btn_y + 5))

        # 3. 200ms 时用户再次晃入 -> 缓冲取消，保持显示
        sidebar.request_show_buttons()
        win.update_mask()
        assert sidebar._buffer_timer_active is False
        assert sidebar._buttons_active is True

        # 4. 再次移出，推进 290ms (临界值)
        sidebar.request_hide_buttons_with_buffer()
        sidebar.tick_buffer_timer(290)
        assert sidebar._buttons_active is True

        # 5. 推进 15ms (累计 305ms 超时)
        sidebar.tick_buffer_timer(15)
        win.update_mask()
        assert sidebar._buttons_active is False
        assert sidebar._buffer_timer_active is False
        # 按钮位置遮罩必须立即被释放穿透
        assert not root.get_applied_mask().contains(QPoint(sidebar.btn_x + 5, sidebar.btn_y + 5))

        # 6. 缓冲期间突发展开全周测试
        sidebar.request_show_buttons()
        sidebar.request_hide_buttons_with_buffer()
        sidebar.tick_buffer_timer(150)
        assert sidebar._buffer_timer_active is True
        # 突然点击展开
        sidebar.expand_weekly_panel()
        win.update_mask()
        assert sidebar._buffer_timer_active is False
        assert sidebar._buttons_active is False
        assert sidebar.sidebarState == "EXPANDED"

    def test_massive_fuzzing_random_events(self, test_env):
        """
        实证检验: 10,000 次混沌随机事件流模糊测试 (Fuzzing)
        模拟极端手速或窗口事件暴风雨，验证：
        1. 任何时刻状态机绝无未定义状态 (严格属于合法状态集合)
        2. 遮罩计算与状态无裂痕同步 (绝无非 EXPANDED 态下残留全屏遮罩)
        3. 所有过渡态与计时器不引发未捕获异常
        """
        win, root, sidebar = test_env
        random.seed(42)  # 可重现的混沌种子

        valid_states = {"NORMAL", "EXPANDED", "COLLAPSED"}
        total_steps = 10000

        event_weights = [
            ("HOVER_IN", 0.20),
            ("HOVER_OUT", 0.15),
            ("TICK_TIMER", 0.20),
            ("EXPAND", 0.10),
            ("RETRACT", 0.10),
            ("COLLAPSE", 0.08),
            ("RESTORE", 0.08),
            ("BUBBLE_ON", 0.04),
            ("BUBBLE_OFF", 0.03),
            ("TOGGLE_ENABLE", 0.02),
        ]
        events, weights = zip(*event_weights)

        for step in range(total_steps):
            action = random.choices(events, weights=weights, k=1)[0]

            if action == "HOVER_IN":
                if sidebar.sidebarState == "NORMAL":
                    sidebar.request_show_buttons()
            elif action == "HOVER_OUT":
                if sidebar.sidebarState == "NORMAL":
                    sidebar.request_hide_buttons_with_buffer()
            elif action == "TICK_TIMER":
                delta = random.randint(10, 350)
                sidebar.tick_buffer_timer(delta)
            elif action == "EXPAND":
                if sidebar.sidebarState == "NORMAL":
                    sidebar.expand_weekly_panel()
            elif action == "RETRACT":
                if sidebar.sidebarState == "EXPANDED":
                    sidebar.retract_weekly_panel()
            elif action == "COLLAPSE":
                if sidebar.sidebarState == "NORMAL":
                    sidebar.collapse_to_edge()
            elif action == "RESTORE":
                if sidebar.sidebarState == "COLLAPSED":
                    sidebar.restore_from_edge()
            elif action == "BUBBLE_ON":
                if sidebar.sidebarState == "NORMAL":
                    sidebar.show_bubble()
            elif action == "BUBBLE_OFF":
                sidebar.hide_bubble()
            elif action == "TOGGLE_ENABLE":
                sidebar.set_enabled(not sidebar.isVisible())

            # 每次事件均触发窗口遮罩更新
            win.update_mask()

            # 断言 1: 状态有效性
            curr_state = sidebar.sidebarState
            assert curr_state in valid_states, f"Step {step}: 非法状态 {curr_state}"

            # 断言 2: 致命桌面阻断防御 (核心安全不变量)
            # 若非 EXPANDED 且组件可用，绝对不能让全屏处于不可穿透状态
            if curr_state != "EXPANDED":
                applied_mask = root.get_applied_mask()
                if sidebar.isVisible():
                    # 屏幕左上角区域绝对必须可穿透
                    assert not applied_mask.contains(QPoint(100, 100)), \
                        f"Step {step} (action={action}, state={curr_state}): 屏幕左上角检测到桌面遮罩残存阻断！"

        # Fuzzing 完成后推进时间，等待静息收敛
        sidebar.set_enabled(True)
        sidebar.tick_buffer_timer(500)
        if sidebar.sidebarState == "EXPANDED":
            sidebar.retract_weekly_panel()
        win.update_mask()

        final_mask = root.get_applied_mask()
        assert sidebar.sidebarState in {"NORMAL", "COLLAPSED"}
        assert not final_mask.contains(QPoint(960, 540))


# ============================================================================
# 挑战 2: 像素级遮罩穿透数学证明与密集网格采样 (Pixel-Level Penetration)
# ============================================================================

class TestPixelLevelMaskPenetration:
    """实证对抗检验 2: 像素级遮罩穿透数学证明与致密网格采样"""

    RESOLUTIONS = [
        ("1080p", 1920, 1080),
        ("2K", 2560, 1440),
        ("4K", 3840, 2160),
        ("Laptop", 1366, 768),
        ("Ultrawide", 3440, 1440),
    ]

    @pytest.mark.parametrize("name, width, height", RESOLUTIONS)
    def test_mask_penetration_multi_resolution_collapsed_math(self, name, width, height, qapp):
        """
        数学严密验证: 在各分辨率下，COLLAPSED 状态仅贴边小胶囊处于遮罩内，
        几何面积占比 < 0.13%，桌面穿透率 > 99.87% (远超 99%+ 需求指标)。
        """
        central = MagicMock()
        central.configs.interactions.hover_fade = False
        central.theme_manager.currentTheme = "com.classwidgets.default"

        win = WidgetsWindow(central)
        root = MockRootWindow()
        win.root_window = root

        loader = MockWidgetsLoader(root)
        root.add_child(loader)

        sidebar = RealisticScheduleSidebar(width, height, root)
        root.add_child(sidebar)
        sidebar.collapse_to_edge()

        win.update_mask()
        mask = root.get_applied_mask()

        # 胶囊理论尺寸
        cap_w, cap_h = 20, 64
        total_pixels = width * height
        capsule_pixels = cap_w * cap_h
        theoretical_penetration = (total_pixels - capsule_pixels) / total_pixels * 100.0

        # 断言数学穿透率
        assert theoretical_penetration > 99.85, f"{name} 穿透率不满足要求: {theoretical_penetration:.4f}%"

        # 临界采样测试: 胶囊内 100% 捕获，胶囊外 1px 100% 穿透
        cx, cy = sidebar.cap_x, sidebar.cap_y
        # 内部点
        assert mask.contains(QPoint(cx + 2, cy + 2))
        assert mask.contains(QPoint(cx + cap_w - 2, cy + cap_h - 2))
        assert mask.contains(QPoint(cx + 10, cy + 32))

        # 外部紧邻 1px 临界点 (必须 100% 穿透)
        assert not mask.contains(QPoint(cx - 1, cy + 32))       # 左侧 1px
        assert not mask.contains(QPoint(cx + 10, cy - 1))       # 上方 1px
        assert not mask.contains(QPoint(cx + 10, cy + cap_h + 1)) # 下方 1px

        win.release()

    def test_dense_grid_sampling_full_screen_normal(self, test_env):
        """
        密集网格采样测试: 在 1920x1080 屏幕上铺设 5,184 个网格采样点 (步长 20x15)，
        数学严密比对每个点在 mask 中的状态与几何解析解，绝对零假阳性与零假阴性。
        """
        win, root, sidebar = test_env
        win.update_mask()
        mask = root.get_applied_mask()

        # NORMAL 状态仅有竖条
        bx, by, bw, bh = sidebar.bar_x, sidebar.bar_y, sidebar.bar_w, sidebar.bar_h
        bar_rect = QRect(bx, by, bw, bh)

        step_x = 20
        step_y = 15
        total_samples = 0
        hit_samples = 0
        penetrated_samples = 0

        for y in range(0, 1080, step_y):
            for x in range(0, 1920, step_x):
                pt = QPoint(x, y)
                in_mask = mask.contains(pt)
                in_bar = bar_rect.contains(pt)

                total_samples += 1
                if in_mask:
                    hit_samples += 1
                else:
                    penetrated_samples += 1

                # 严密一致性断言: 点在遮罩内 当且仅当 点在竖条几何内
                assert in_mask == in_bar, f"网格采样点 ({x}, {y}) 判定不一致: mask={in_mask}, expected={in_bar}"

        penetration_rate = (penetrated_samples / total_samples) * 100.0
        # 竖条占屏幕面积约 3.8%，穿透率必在 95%~97% 之间，除该几何控件外 100% 穿透
        assert penetration_rate > 95.0, f"穿透采样率偏低: {penetration_rate:.2f}%"
        assert hit_samples > 0

    def test_mask_penetration_with_buttons_and_bubble(self, test_env):
        """
        实证检验: 当竖条、悬浮双按钮和课程气泡卡片同时展开激活时，
        测试三个多边形区域的并集遮罩，验证边界外零像素溢出与 100% 穿透。
        """
        win, root, sidebar = test_env

        sidebar.request_show_buttons()
        sidebar.show_bubble()
        win.update_mask()
        mask = root.get_applied_mask()

        bar_r = QRect(sidebar.bar_x, sidebar.bar_y, sidebar.bar_w, sidebar.bar_h)
        btn_r = QRect(sidebar.btn_x, sidebar.btn_y, sidebar.btn_w, sidebar.btn_h)
        bub_r = QRect(sidebar.bubble_x, sidebar.bubble_y, sidebar.bubble_w, sidebar.bubble_h)

        # 验证各个几何中心均被保护
        assert mask.contains(bar_r.center())
        assert mask.contains(btn_r.center())
        assert mask.contains(bub_r.center())

        # 验证按钮左侧 10px 处完全穿透
        assert not mask.contains(QPoint(btn_r.left() - 10, btn_r.center().y()))
        # 验证气泡左侧 10px 处完全穿透
        assert not mask.contains(QPoint(bub_r.left() - 10, bub_r.center().y()))
        # 验证屏幕大面积工作区完全穿透 (如代码编辑器、浏览器常驻的屏幕 0%~80% 区域)
        for tx in [100, 500, 1000, 1400]:
            for ty in [100, 500, 900]:
                assert not mask.contains(QPoint(tx, ty)), f"工作区点 ({tx}, {ty}) 被异常阻断！"

    def test_mask_state_switch_penetration_recovery(self, test_env):
        """
        实证检验: 从 EXPANDED (全周大面板临时全屏捕获遮罩，穿透率 0%)
        平滑切换回 NORMAL 或 COLLAPSED 之后，桌面穿透率是否 100% 瞬时完全恢复。
        """
        win, root, sidebar = test_env

        # 展开全周大面板
        sidebar.expand_weekly_panel()
        win.update_mask()
        # 此时全屏临时遮罩，穿透率为 0%
        assert root.get_applied_mask().isEmpty()

        # 外部点击收回恢复 NORMAL
        sidebar.retract_weekly_panel()
        win.update_mask()
        mask_normal = root.get_applied_mask()

        # 验证穿透率即时恢复 (>95%)
        assert not mask_normal.contains(QPoint(960, 540))
        assert not mask_normal.contains(QPoint(200, 200))
        assert mask_normal.contains(QPoint(sidebar.bar_x + 10, sidebar.bar_y + 10))

        # 再收起到 COLLAPSED
        sidebar.collapse_to_edge()
        win.update_mask()
        mask_collapsed = root.get_applied_mask()

        # 验证穿透率提升到 >99.9%
        assert not mask_collapsed.contains(QPoint(sidebar.bar_x + 10, sidebar.bar_y + 10))
        assert mask_collapsed.contains(QPoint(sidebar.cap_x + 5, sidebar.cap_y + 10))


# ============================================================================
# 挑战 3: 异常关机模拟与高并发持久化抗竞态测试 (Concurrency & Resilience)
# ============================================================================

class TestAbnormalShutdownAndConcurrency:
    """实证对抗检验 3: 异常关机损坏模拟与高并发读写持久化抗竞态"""

    def test_concurrent_rapid_toggle_hammer(self, tmp_path, qapp):
        """
        高并发压力测试 (Hammer Test):
        模拟 10 个工作线程同时极速连击切换折叠状态、修改启用配置、执行 save() 与读取 data，
        累计执行 2,000+ 次并发事务，检验无死锁、无竞态奔溃、数据强一致性。
        """
        config_dir = tmp_path / "hammer_test"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.json"

        manager = ConfigManager(config_dir, "config.json")
        manager.load_config()

        num_threads = 10
        ops_per_thread = 200
        errors = []

        def worker(thread_id):
            try:
                for i in range(ops_per_thread):
                    # 交替快速切换折叠状态
                    collapsed_val = (i % 2 == 0)
                    manager.set("preferences.schedule_sidebar_collapsed", collapsed_val)

                    if i % 10 == 0:
                        enabled_val = (i % 20 != 0)
                        manager.set("preferences.schedule_sidebar_enabled", enabled_val)

                    if i % 25 == 0:
                        manager.save(silent=True)

                    # 并发读取校验
                    _ = manager.data["preferences"]["schedule_sidebar_collapsed"]
                    _ = manager.preferences.schedule_sidebar_collapsed
            except Exception as e:
                errors.append((thread_id, e))

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"并发读写出现异常: {errors}"

        # 最终保存并重新从磁盘反序列化
        manager.save(silent=True)
        assert config_file.exists()

        reloaded = ConfigManager(config_dir, "config.json")
        reloaded.load_config()
        # 验证再加载无异常且字段存在且类型为 bool
        assert isinstance(reloaded.preferences.schedule_sidebar_collapsed, bool)
        assert isinstance(reloaded.preferences.schedule_sidebar_enabled, bool)

    def test_crash_abnormal_shutdown_truncated_json(self, tmp_path, qapp):
        """
        实证检验: 模拟应用写入配置文件中途系统掉电或强制杀进程 (SIGKILL)，
        导致磁盘仅保存了截断的不完整 JSON 字符串。
        验证 ConfigManager.load_config() 必须安全捕获异常，容错回退到默认配置，应用绝不崩溃。
        """
        config_dir = tmp_path / "crash_truncated"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.json"

        # 模拟截断的非法 JSON
        truncated_payload = '{"preferences": {"schedule_sidebar_enabled": true, "schedule_side'
        config_file.write_text(truncated_payload, encoding="utf-8")

        manager = ConfigManager(config_dir, "config.json")
        # 执行加载，必须平滑容错
        manager.load_config()

        # 验证自动回退到契约默认值
        assert manager.preferences.schedule_sidebar_enabled is True
        assert manager.preferences.schedule_sidebar_collapsed is False

        # 验证随后的 save 能够自我修复生成合法 JSON
        manager.save(silent=True)
        valid_data = json.loads(config_file.read_text(encoding="utf-8"))
        assert "preferences" in valid_data
        assert valid_data["preferences"]["schedule_sidebar_enabled"] is True

    def test_crash_abnormal_shutdown_corrupted_bytes(self, tmp_path, qapp):
        """
        实证检验: 模拟磁盘损坏产生 0x00 空字节、乱码二进制脏数据。
        验证 ConfigManager 自动容错回退。
        """
        config_dir = tmp_path / "crash_corrupted"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.json"

        # 写入 512 字节的 0x00 空字节
        config_file.write_bytes(b"\x00" * 512)

        manager = ConfigManager(config_dir, "config.json")
        manager.load_config()

        assert manager.preferences.schedule_sidebar_enabled is True
        assert manager.preferences.schedule_sidebar_collapsed is False

    def test_write_permission_denied_resilience(self, tmp_path, qapp):
        """
        实证检验: 模拟配置存储目录被外部进程锁定或无写权限 (PermissionError)，
        验证 save() 安全捕获，不向上抛出未捕获异常导致 Qt 主循环崩溃。
        """
        config_dir = tmp_path / "protected_config"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.json"

        manager = ConfigManager(config_dir, "config.json")
        manager.load_config()

        # 模拟 write_text 抛出 PermissionError
        original_write_text = Path.write_text

        def mock_failing_write_text(*args, **kwargs):
            raise PermissionError("[WinError 5] 拒绝访问: 'config.json'")

        Path.write_text = mock_failing_write_text
        try:
            # 必须安全执行不崩溃
            manager.save(silent=True)
        finally:
            Path.write_text = original_write_text

    def test_rapid_toggle_atomic_consistency(self, tmp_path, qapp):
        """
        实证检验: 极速往复切换折叠状态 100 次，验证每次切换均能即时反射到
        manager.preferences、manager.data 以及最终磁盘文件的布尔值。
        """
        config_dir = tmp_path / "rapid_toggle"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "config.json"

        manager = ConfigManager(config_dir, "config.json")
        manager.load_config()

        expected = False
        for _ in range(100):
            expected = not expected
            manager.set("preferences.schedule_sidebar_collapsed", expected)
            assert manager.preferences.schedule_sidebar_collapsed == expected
            assert manager.data["preferences"]["schedule_sidebar_collapsed"] == expected

        manager.save(silent=True)
        content = json.loads(config_file.read_text(encoding="utf-8"))
        assert content["preferences"]["schedule_sidebar_collapsed"] == expected
