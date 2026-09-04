# -*- coding: utf-8 -*-
"""
Class-Widgets-2 侧边课表栏场景集成与状态机时序测试 (Tier 3 & Tier 4)

覆盖范围:
- Tier 3: 跨状态与配置成对组合测试（Pairwise Combination Tests: Pair 1 ~ Pair 11）
- Tier 4: 真实端到端应用行为时序场景（Real-World Application Scenarios: Scenario 1 ~ Scenario 6）
"""
import json
import sys
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QCoreApplication, QObject, QRect, QPoint, Property, Signal
from PySide6.QtGui import QRegion

from src.core.config.manager import ConfigManager
from src.core.schedule.model import (
    ScheduleData,
    MetaInfo,
    Subject,
    Timeline,
    Entry,
    EntryType,
)
from src.core.schedule.runtime import ScheduleRuntime
from src.core.widgets.core import WidgetsWindow
from tests.e2e.test_sidebar_model import setup_runtime


@pytest.fixture(scope="session")
def qapp():
    """提供 PySide6 QCoreApplication 单例"""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app


class MockSidebarComponent(QObject):
    """用于场景与状态机测试的高仿真 ScheduleSidebar 组件"""
    geometryChanged = Signal()
    sidebarStateChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("scheduleSidebar")
        self._visible = True
        self._sidebar_state = "NORMAL"  # NORMAL, EXPANDED, COLLAPSED
        self._interactive_rects = [[1740, 200, 180, 680]]
        self._is_full_week_expanded = False
        self._hover_buttons_visible = False
        self._buffer_timer_running = False

    def isVisible(self) -> bool:
        return self._visible

    def set_visible(self, val: bool):
        self._visible = val
        self.geometryChanged.emit()

    @Property(str, notify=sidebarStateChanged)
    def sidebarState(self) -> str:
        return self._sidebar_state

    @Property(list, notify=geometryChanged)
    def interactiveRects(self) -> list:
        return self._interactive_rects

    @Property(bool, notify=geometryChanged)
    def isFullWeekExpanded(self) -> bool:
        return self._is_full_week_expanded

    def to_normal_state(self):
        self._sidebar_state = "NORMAL"
        self._is_full_week_expanded = False
        self._interactive_rects = [[1740, 200, 180, 680]]
        self.sidebarStateChanged.emit("NORMAL")
        self.geometryChanged.emit()

    def show_hover_buttons(self):
        self._hover_buttons_visible = True
        self._buffer_timer_running = False
        self._interactive_rects = [
            [1740, 200, 180, 680],  # 竖条
            [1690, 300, 40, 90],    # 悬浮双按钮
        ]
        self.geometryChanged.emit()

    def start_hover_leave_buffer(self):
        """鼠标移出，启动 300ms 延时缓冲"""
        self._buffer_timer_running = True

    def cancel_hover_leave_buffer(self):
        """300ms 内鼠标快速移回，取消缓冲，保持按钮显示"""
        self._buffer_timer_running = False

    def trigger_hover_buffer_timeout(self):
        """300ms 缓冲超时，收回按钮"""
        if self._buffer_timer_running:
            self._buffer_timer_running = False
            self._hover_buttons_visible = False
            self._interactive_rects = [[1740, 200, 180, 680]]
            self.geometryChanged.emit()

    def expand_full_week(self):
        self._sidebar_state = "EXPANDED"
        self._is_full_week_expanded = True
        self._interactive_rects = [[1200, 150, 720, 780]]
        self.sidebarStateChanged.emit("EXPANDED")
        self.geometryChanged.emit()

    def collapse_to_edge(self):
        self._sidebar_state = "COLLAPSED"
        self._is_full_week_expanded = False
        self._hover_buttons_visible = False
        self._buffer_timer_running = False
        # 微型贴边小胶囊
        self._interactive_rects = [[1900, 500, 20, 60]]
        self.sidebarStateChanged.emit("COLLAPSED")
        self.geometryChanged.emit()


class DummyWindow(QObject):
    """模拟顶层窗口对象"""
    def __init__(self):
        super().__init__()
        self._children = []
        self._mask = None

    def findChild(self, type_, name):
        for c in self._children:
            if c.objectName() == name:
                return c
        return None

    def setMask(self, mask: QRegion):
        self._mask = mask

    def get_mask(self) -> QRegion:
        return self._mask


@pytest.fixture
def full_integration_env(tmp_path, qapp):
    """集成测试环境：包含完整的 ConfigManager、ScheduleRuntime、WidgetsWindow 与 ScheduleSidebar"""
    # 1. 配置管理器
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    cfg_file = "app_config.json"
    cfg_mgr = ConfigManager(config_dir, cfg_file)

    # 2. AppCentral Mock
    central = MagicMock()
    central.configs = cfg_mgr
    central.notification = MagicMock()
    central.theme_manager.currentTheme = "default"

    # 3. ScheduleRuntime
    runtime = ScheduleRuntime(central)

    # 4. WidgetsWindow & Mock ScheduleSidebar
    win = WidgetsWindow(central)
    root = DummyWindow()
    win.root_window = root

    loader = QObject(root)
    loader.setObjectName("widgetsLoader")
    loader.property = lambda n: False
    loader.x = lambda: 0
    loader.y = lambda: 0
    root._children.append(loader)

    sidebar = MockSidebarComponent(root)
    root._children.append(sidebar)

    # 连接 geometryChanged
    sidebar.geometryChanged.connect(win.update_mask)

    # 5. 标准全天课表数据
    subjects = [
        Subject(id="s_math", name="高等数学", teacher="张教授", location="教三 101", color="#4A90E2"),
        Subject(id="s_eng", name="大学英语", teacher="李老师", location="外语楼 201", color="#50E3C2"),
        Subject(id="s_phy", name="大学物理", teacher="王教授", location="物理馆 305", color="#F5A623"),
    ]
    entries_mon = [
        Entry(id="e_m1", type=EntryType.CLASS, startTime="08:00", endTime="08:45", subjectId="s_math"),
        Entry(id="e_m2", type=EntryType.CLASS, startTime="09:00", endTime="09:45", subjectId="s_eng"),
        Entry(id="e_m3", type=EntryType.CLASS, startTime="10:00", endTime="10:45", subjectId="s_phy"),
    ]
    days = [
        Timeline(id="tl_mon", dayOfWeek=[1], weeks="all", entries=entries_mon),
        Timeline(id="tl_tue", dayOfWeek=[2], weeks="all", entries=[
            Entry(id="e_t1", type=EntryType.CLASS, startTime="14:00", endTime="15:40", subjectId="s_math")
        ]),
    ]
    schedule = ScheduleData(
        meta=MetaInfo(id="m1", startDate="2026-09-07", maxWeekCycle=1),
        subjects=subjects,
        days=days,
        overrides=[],
    )

    return cfg_mgr, runtime, win, sidebar, root, schedule


# ============================================================================
# Tier 3: 跨状态成对组合测试（Pairwise Combination Tests）
# ============================================================================


def test_pair_1_expanded_sidebar_disabled_in_settings(full_integration_env):
    """Pair 1: 全周大面板展开中在设置中心关闭侧边栏开关 (EXPANDED + Config Disable)"""
    cfg_mgr, _, win, sidebar, root, _ = full_integration_env
    # 展开全周大面板
    sidebar.expand_full_week()
    win.update_mask()
    # 展开时遮罩为空（全屏透明捕获外部点击）
    assert root.get_mask().isEmpty()

    # 设置中心关闭侧边栏
    cfg_mgr.set("preferences.schedule_sidebar_enabled", False)
    sidebar.set_visible(False)
    win.update_mask()

    # 验证：遮罩立即移除全屏捕获，退化为安全最小空遮罩 1x1
    mask = root.get_mask()
    assert not mask.isEmpty()
    assert mask.boundingRect() == QRect(0, 0, 1, 1)


def test_pair_2_collapsed_sidebar_day_rollover(full_integration_env):
    """Pair 2: 贴边折叠中跨天跨周时间跳变 (COLLAPSED + Day Rollover)"""
    _, runtime, win, sidebar, root, schedule = full_integration_env
    sidebar.collapse_to_edge()
    win.update_mask()

    # 周一晚上 23:59:50
    mon_night = datetime(2026, 9, 7, 23, 59, 50)
    setup_runtime(runtime, schedule, mon_night)
    assert len(runtime.sidebarDaySchedule) == 3
    assert sidebar.sidebarState == "COLLAPSED"

    # 时钟跳变至周二 08:30
    tue_morning = datetime(2026, 9, 8, 8, 30)
    setup_runtime(runtime, schedule, tue_morning)
    # 周二排课自动刷新为 1 节
    assert len(runtime.sidebarDaySchedule) == 1
    assert runtime.sidebarDaySchedule[0]["subjectName"] == "高等数学"
    # 小胶囊依然保持折叠状态
    assert sidebar.sidebarState == "COLLAPSED"
    assert root.get_mask().contains(QRect(1900, 500, 20, 60))


def test_pair_3_hover_buttons_directly_collapsed(full_integration_env):
    """Pair 3: 悬浮双按钮展示中直接点击折叠 (Buttons Hovering + Collapse)"""
    _, _, win, sidebar, root, _ = full_integration_env
    sidebar.show_hover_buttons()
    win.update_mask()
    mask = root.get_mask()
    assert mask.contains(QRect(1740, 200, 180, 680))
    assert mask.contains(QRect(1690, 300, 40, 90))

    # 用户点击折叠按钮
    sidebar.collapse_to_edge()
    win.update_mask()
    new_mask = root.get_mask()
    # 双按钮和竖条区域全部被释放
    assert not new_mask.contains(QPoint(1695, 310))
    assert not new_mask.contains(QPoint(1750, 250))
    assert new_mask.contains(QRect(1900, 500, 20, 60))


def test_pair_4_collapsed_persistence_across_sessions(full_integration_env):
    """Pair 4: 折叠状态持久化并跨会话加载保持 (COLLAPSED + Persistence)"""
    cfg_mgr, _, _, sidebar, _, _ = full_integration_env
    sidebar.collapse_to_edge()
    cfg_mgr.set("preferences.schedule_sidebar_collapsed", True)
    cfg_mgr.save()

    # 重新从磁盘加载
    new_cfg = ConfigManager(cfg_mgr.path, cfg_mgr.filename)
    new_cfg.load_config()
    assert new_cfg.preferences.schedule_sidebar_collapsed is True


def test_pair_5_expanded_panel_resize_geometry_update(full_integration_env):
    """Pair 5: 全周大面板展开中窗口尺寸自适应重新计算 (EXPANDED + Resize)"""
    _, _, win, sidebar, root, _ = full_integration_env
    sidebar.expand_full_week()
    win.update_mask()
    assert root.get_mask().isEmpty()

    # 模拟外部尺寸调整
    sidebar._interactive_rects = [[1000, 100, 920, 880]]
    sidebar.geometryChanged.emit()
    assert root.get_mask().isEmpty()


def test_pair_6_break_to_class_transition_highlight(full_integration_env):
    """Pair 6: 课间休息过渡到上课瞬间高亮无缝迁移 (Break -> Class Highlight Transition)"""
    _, runtime, _, _, _, schedule = full_integration_env
    # 08:50:00 (课间: 第一节课已结束，第二节课未开始)
    break_time = datetime(2026, 9, 7, 8, 50, 0)
    setup_runtime(runtime, schedule, break_time)
    sched = runtime.sidebarDaySchedule
    assert sched[0]["isCurrent"] is False
    assert sched[0]["progress"] == 1.0
    assert sched[1]["isCurrent"] is False
    assert sched[1]["progress"] == 0.0

    # 09:00:00 (第二节课刚好开始)
    class_start = datetime(2026, 9, 7, 9, 0, 0)
    setup_runtime(runtime, schedule, class_start)
    sched2 = runtime.sidebarDaySchedule
    assert sched2[0]["isCurrent"] is False
    assert sched2[0]["progress"] == 1.0
    assert sched2[1]["isCurrent"] is True
    assert sched2[1]["progress"] == 0.0


def test_pair_7_bubble_active_then_expand_full_week(full_integration_env):
    """Pair 7: 悬浮气泡激活时切换至全周大面板 (Bubble Active + Expand)"""
    _, _, win, sidebar, root, _ = full_integration_env
    sidebar.to_normal_state()
    # 模拟气泡展开产生额外的交互矩形
    sidebar._interactive_rects = [
        [1740, 200, 180, 680],  # 竖条
        [1500, 250, 220, 120],  # 悬浮气泡
    ]
    win.update_mask()
    assert root.get_mask().contains(QRect(1500, 250, 220, 120))

    # 点击展开大面板
    sidebar.expand_full_week()
    win.update_mask()
    assert root.get_mask().isEmpty()


def test_pair_8_reschedule_day_matrix_consistency(full_integration_env):
    """Pair 8: 调休机制下当天与整周排课一致性 (Reschedule + Matrix)"""
    cfg_mgr, runtime, _, _, _, schedule = full_integration_env
    cfg_mgr.schedule.reschedule_day = {"2026-09-12": 1}  # 周六上周一的课
    sat_now = datetime(2026, 9, 12, 8, 30)
    setup_runtime(runtime, schedule, sat_now)

    # 当天课表为周一排课
    day_sched = runtime.sidebarDaySchedule
    assert len(day_sched) == 3
    assert day_sched[0]["subjectName"] == "高等数学"


def test_pair_9_class_swap_collapse_and_restore(full_integration_env):
    """Pair 9: 临时换课生效时折叠后再展开 (Class Swap + Collapse/Restore)"""
    cfg_mgr, runtime, _, sidebar, _, schedule = full_integration_env
    cfg_mgr.schedule.class_swap = {
        "date": "2026-09-07",
        "day_of_week": 2,
        "week_of_cycle": 1,
    }
    mon_now = datetime(2026, 9, 7, 14, 10)
    setup_runtime(runtime, schedule, mon_now)
    assert len(runtime.sidebarDaySchedule) == 1

    # 折叠再恢复
    sidebar.collapse_to_edge()
    assert sidebar.sidebarState == "COLLAPSED"
    sidebar.to_normal_state()
    assert sidebar.sidebarState == "NORMAL"
    assert len(runtime.sidebarDaySchedule) == 1


def test_pair_10_desktop_edit_mode_coexistence(full_integration_env):
    """Pair 10: 桌面小组件编辑模式下遮罩全屏放开，退出后恢复精准合并 (Desktop Edit Mode + Sidebar)"""
    _, _, win, sidebar, root, _ = full_integration_env
    loader = root.findChild(QObject, "widgetsLoader")
    sidebar.to_normal_state()
    win.update_mask()
    assert not root.get_mask().isEmpty()

    # 进入编辑模式
    loader.property = lambda n: True if n == "editMode" else False
    win.update_mask()
    assert root.get_mask().isEmpty()

    # 退出编辑模式
    loader.property = lambda n: False
    win.update_mask()
    assert not root.get_mask().isEmpty()
    assert root.get_mask().contains(QRect(1740, 200, 180, 680))


def test_pair_11_rapid_state_machine_racing(full_integration_env):
    """Pair 11: 极速交替折叠与全周展开并发竞态 (Rapid State Machine Racing)"""
    _, _, win, sidebar, root, _ = full_integration_env

    # 模拟 30 次高频状态交替切换
    for i in range(30):
        if i % 3 == 0:
            sidebar.to_normal_state()
        elif i % 3 == 1:
            sidebar.expand_full_week()
        else:
            sidebar.collapse_to_edge()
        win.update_mask()

    # 最终回到 NORMAL 状态，状态与遮罩必须准确收敛
    sidebar.to_normal_state()
    win.update_mask()
    assert sidebar.sidebarState == "NORMAL"
    assert root.get_mask().contains(QRect(1740, 200, 180, 680))


# ============================================================================
# Tier 4: 真实应用行为时序场景（Real-World Application Scenarios）
# ============================================================================


def test_scenario_1_full_day_flow(full_integration_env):
    """Scenario 1: 学生全天上课正常流转（课前、正在上课高亮、课间倒计时、换课）"""
    _, runtime, _, _, _, schedule = full_integration_env

    # Step 1: 07:30 (课前准备状态)
    t1 = datetime(2026, 9, 7, 7, 30)
    setup_runtime(runtime, schedule, t1)
    for c in runtime.sidebarDaySchedule:
        assert c["isCurrent"] is False
        assert c["progress"] == 0.0

    # Step 2: 08:15 (第一节高数课正上课中)
    t2 = datetime(2026, 9, 7, 8, 15)
    setup_runtime(runtime, schedule, t2)
    s2 = runtime.sidebarDaySchedule
    assert s2[0]["isCurrent"] is True
    assert 0.25 <= s2[0]["progress"] <= 0.40
    assert s2[1]["isCurrent"] is False

    # Step 3: 08:45 (第一节课下课，进入 15 分钟课间)
    t3 = datetime(2026, 9, 7, 8, 45)
    setup_runtime(runtime, schedule, t3)
    s3 = runtime.sidebarDaySchedule
    assert s3[0]["isCurrent"] is False
    assert s3[0]["progress"] == 1.0
    assert s3[1]["isCurrent"] is False
    assert s3[1]["progress"] == 0.0

    # Step 4: 09:20 (第二节英语课正在上课)
    t4 = datetime(2026, 9, 7, 9, 20)
    setup_runtime(runtime, schedule, t4)
    s4 = runtime.sidebarDaySchedule
    assert s4[0]["progress"] == 1.0
    assert s4[1]["isCurrent"] is True
    assert 0.35 <= s4[1]["progress"] <= 0.55

    # Step 5: 11:00 (上午所有课程全部结束)
    t5 = datetime(2026, 9, 7, 11, 0)
    setup_runtime(runtime, schedule, t5)
    for c in runtime.sidebarDaySchedule:
        assert c["isCurrent"] is False
        assert c["progress"] == 1.0


def test_scenario_2_view_detail_expand_and_dismiss(full_integration_env):
    """Scenario 2: 查看课程详情后临时展开全周排课并收回"""
    _, runtime, win, sidebar, root, schedule = full_integration_env
    now = datetime(2026, 9, 7, 8, 30)
    setup_runtime(runtime, schedule, now)

    # 1. 初始为 NORMAL 状态
    sidebar.to_normal_state()
    win.update_mask()
    assert root.get_mask().contains(QRect(1740, 200, 180, 680))

    # 2. 悬浮出现双按钮
    sidebar.show_hover_buttons()
    win.update_mask()
    assert root.get_mask().contains(QRect(1690, 300, 40, 90))

    # 3. 点击展开大面板
    sidebar.expand_full_week()
    win.update_mask()
    assert sidebar.sidebarState == "EXPANDED"
    assert root.get_mask().isEmpty()

    # 4. 模拟外部桌面空白区域点击，收回全周大面板
    sidebar.to_normal_state()
    win.update_mask()
    assert sidebar.sidebarState == "NORMAL"
    assert root.get_mask().contains(QRect(1740, 200, 180, 680))


def test_scenario_3_hover_buffer_interaction(full_integration_env):
    """Scenario 3: 鼠标掠过竖条边缘防误触缓冲（移出后 200ms 快速移回 vs 350ms 完全收回）"""
    _, _, win, sidebar, root, _ = full_integration_env

    # 1. 鼠标移入，按钮滑出
    sidebar.show_hover_buttons()
    win.update_mask()
    assert root.get_mask().contains(QRect(1690, 300, 40, 90))

    # 2. 鼠标移出，启动 300ms 缓冲计时器
    sidebar.start_hover_leave_buffer()
    assert sidebar._buffer_timer_running is True

    # 3. 在 200ms (< 300ms) 内鼠标快速移回，缓冲取消，按钮继续保持可见
    sidebar.cancel_hover_leave_buffer()
    assert sidebar._buffer_timer_running is False
    assert sidebar._hover_buttons_visible is True
    win.update_mask()
    assert root.get_mask().contains(QRect(1690, 300, 40, 90))

    # 4. 再次移出，并在 350ms (> 300ms) 后超时触发淡出收回
    sidebar.start_hover_leave_buffer()
    sidebar.trigger_hover_buffer_timeout()
    win.update_mask()
    assert sidebar._hover_buttons_visible is False
    # 遮罩不再包含双按钮
    assert not root.get_mask().contains(QPoint(1695, 310))


def test_scenario_4_focus_mode_collapse_and_restore(full_integration_env):
    """Scenario 4: 专注模式隐藏贴边，随后点击边缘小胶囊恢复"""
    _, _, win, sidebar, root, _ = full_integration_env

    # 1. 点击收起按钮，隐藏竖条，屏幕边缘仅留微型贴边小胶囊
    sidebar.collapse_to_edge()
    win.update_mask()
    assert sidebar.sidebarState == "COLLAPSED"

    mask = root.get_mask()
    assert mask.contains(QRect(1900, 500, 20, 60))
    # 原竖条区域 100% 穿透
    assert not mask.contains(QPoint(1750, 250))

    # 2. 点击贴边小胶囊，恢复当天课表竖条
    sidebar.to_normal_state()
    win.update_mask()
    assert sidebar.sidebarState == "NORMAL"
    assert root.get_mask().contains(QRect(1740, 200, 180, 680))


def test_scenario_5_settings_toggle_and_memory_restore(full_integration_env):
    """Scenario 5: 设置中心关闭侧边栏并在下次启动时恢复记忆状态"""
    cfg_mgr, _, win, sidebar, root, _ = full_integration_env

    # 1. 设置中心关闭
    cfg_mgr.set("preferences.schedule_sidebar_enabled", False)
    cfg_mgr.set("preferences.schedule_sidebar_collapsed", True)
    cfg_mgr.save()

    sidebar.set_visible(False)
    win.update_mask()
    # 遮罩清除侧边栏
    assert not root.get_mask().contains(QRect(1740, 200, 180, 680))

    # 2. 模拟下次启动读取配置
    new_cfg = ConfigManager(cfg_mgr.path, cfg_mgr.filename)
    new_cfg.load_config()
    assert new_cfg.preferences.schedule_sidebar_enabled is False
    assert new_cfg.preferences.schedule_sidebar_collapsed is True

    # 3. 重新在设置中心开启
    new_cfg.set("preferences.schedule_sidebar_enabled", True)
    sidebar.set_visible(True)
    sidebar.to_normal_state()
    win.update_mask()
    assert root.get_mask().contains(QRect(1740, 200, 180, 680))


def test_scenario_6_high_stress_concurrent_operations(full_integration_env):
    """Scenario 6: 极限操作压力测试：快速连击展开/收回/折叠同时进行窗口遮罩穿透验证"""
    cfg_mgr, runtime, win, sidebar, root, schedule = full_integration_env

    # 连续执行 60 次跨状态交替触发
    for step in range(60):
        action = step % 4
        if action == 0:
            sidebar.to_normal_state()
        elif action == 1:
            sidebar.show_hover_buttons()
        elif action == 2:
            sidebar.expand_full_week()
        else:
            sidebar.collapse_to_edge()

        win.update_mask()
        mask = root.get_mask()
        # 无论处于哪种状态，遮罩对象必须合法存在
        assert mask is not None
        if not mask.isEmpty():
            assert mask.boundingRect().width() > 0
            assert mask.boundingRect().height() > 0

    # 压力测试后状态收敛恢复
    sidebar.to_normal_state()
    win.update_mask()
    assert sidebar.sidebarState == "NORMAL"
    assert root.get_mask().contains(QRect(1740, 200, 180, 680))
