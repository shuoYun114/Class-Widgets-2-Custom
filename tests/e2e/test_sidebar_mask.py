# -*- coding: utf-8 -*-
"""
Class-Widgets-2 侧边栏交互遮罩与屏幕穿透测试 (Tier 1 & Tier 2)

覆盖范围:
- Tier 1: NORMAL 状态竖条遮罩合并、悬浮双按钮遮罩合并、COLLAPSED 贴边小胶囊微遮罩、
          EXPANDED 全周大面板外部点击全屏捕获遮罩、桌面小组件与侧边栏共存遮罩、浮窗共存遮罩、不可见侧边栏过滤
- Tier 2: 空遮罩 1x1 安全防御、零与负尺寸过滤、多显示器负坐标支持、编辑模式与菜单全屏覆盖、
          各种分辨率自适应坐标穿透验证（1080p, 2K, 4K, 笔记本, 超宽屏）
"""
import sys
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QCoreApplication, QRect, QObject, QPoint, Signal, Property
from PySide6.QtGui import QRegion

from src.core.widgets.core import WidgetsWindow


@pytest.fixture(scope="session")
def qapp():
    """提供 PySide6 QCoreApplication 单例"""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app


@pytest.fixture
def mock_central(qapp):
    central = MagicMock()
    central.configs.interactions.hover_fade = False
    central.theme_manager.currentTheme = "com.classwidgets.default"
    return central


class DummyRootWindow(QObject):
    """模拟 WidgetsWindow 的 root_window QQuickWindow 实例"""
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


class MockScheduleSidebar(QObject):
    """模拟 QML 中 ScheduleSidebar 组件的接口与属性"""
    geometryChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("scheduleSidebar")
        self._visible = True
        self._sidebar_state = "NORMAL"
        self._interactive_rects = []
        self._is_full_week_expanded = False

    def isVisible(self) -> bool:
        return self._visible

    def set_visible(self, val: bool):
        self._visible = val

    def set_sidebar_state(self, state: str):
        self._sidebar_state = state

    def set_interactive_rects(self, rects: list[list[int]]):
        self._interactive_rects = rects

    def set_full_week_expanded(self, val: bool):
        self._is_full_week_expanded = val

    @Property(str)
    def sidebarState(self) -> str:
        return self._sidebar_state

    @Property(list)
    def interactiveRects(self) -> list:
        return self._interactive_rects

    @Property(bool)
    def isFullWeekExpanded(self) -> bool:
        return self._is_full_week_expanded


class MockWidgetsLoader(QObject):
    """模拟桌面 widgetsLoader"""
    geometryChanged = Signal()
    contentGeometryChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("widgetsLoader")
        self._menu_visible = False
        self._edit_mode = False
        self._x = 100
        self._y = 50

    def property(self, name: str):
        if name == "menuVisible":
            return self._menu_visible
        if name == "editMode":
            return self._edit_mode
        return None

    def x(self):
        return self._x

    def y(self):
        return self._y


@pytest.fixture
def mock_widgets_env(mock_central):
    """构建用于测试 update_mask 的 WidgetsWindow 运行环境"""
    win = WidgetsWindow(mock_central)
    root = DummyRootWindow()
    win.root_window = root

    loader = MockWidgetsLoader(root)
    root.add_child(loader)

    sidebar = MockScheduleSidebar(root)
    root.add_child(sidebar)

    yield win, root, loader, sidebar
    win.release()


# ============================================================================
# Tier 1: 基础遮罩合并与状态穿透计算
# ============================================================================


def test_sidebar_normal_state_mask(mock_widgets_env):
    """Tier 1: NORMAL 竖条态下，侧边栏矩形正确合入 mask"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_sidebar_state("NORMAL")
    sidebar.set_interactive_rects([
        [1750, 200, 160, 500],
        [1696, 397, 44, 106]
    ])

    win.update_mask()

    applied = root.get_applied_mask()
    assert not applied.isEmpty()
    assert applied.contains(QRect(1760, 250, 10, 10))
    assert applied.contains(QRect(1700, 400, 10, 10))
    assert not applied.contains(QRect(500, 500, 10, 10))


def test_sidebar_normal_with_hover_buttons(mock_widgets_env):
    """Tier 1: 鼠标移入滑出悬浮双按钮时，竖条与双按钮两个交互矩形同时被包含在遮罩内"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_sidebar_state("NORMAL")
    capsule_rect = [1740, 200, 180, 680]
    buttons_rect = [1690, 300, 40, 90]
    sidebar.set_interactive_rects([capsule_rect, buttons_rect])

    win.update_mask()

    applied = root.get_applied_mask()
    assert applied.contains(QRect(1740, 200, 180, 680))
    assert applied.contains(QRect(1690, 300, 40, 90))
    assert not applied.contains(QRect(1000, 300, 10, 10))


def test_sidebar_collapsed_state_mask(mock_widgets_env):
    """Tier 1: COLLAPSED 折叠态下，仅贴边小胶囊在 mask 内，其余 100% 穿透"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_sidebar_state("COLLAPSED")
    sidebar.set_interactive_rects([[1900, 450, 20, 64]])

    win.update_mask()

    applied = root.get_applied_mask()
    assert applied.contains(QRect(1905, 460, 5, 5))
    assert applied.boundingRect() == QRect(1900, 450, 20, 64)
    assert not applied.contains(QPoint(1760, 250))
    assert not applied.contains(QPoint(500, 500))


def test_sidebar_expanded_state_mask(mock_widgets_env):
    """Tier 1: EXPANDED 全周大面板展开时，触发全屏透明遮罩支持外部点击收回"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_sidebar_state("EXPANDED")
    sidebar.set_full_week_expanded(True)

    win.update_mask()

    applied = root.get_applied_mask()
    assert applied.isEmpty()
    assert win.interactive_rect.isEmpty()


def test_sidebar_disabled_mask(mock_widgets_env):
    """Tier 1: 侧边栏被禁用（不可见）时，不贡献任何 mask 区域"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_visible(False)
    sidebar.set_interactive_rects([[1750, 200, 160, 500]])

    win.update_mask()

    applied = root.get_applied_mask()
    assert not applied.contains(QRect(1750, 200, 160, 500))
    assert applied.boundingRect() == QRect(0, 0, 1, 1)


def test_sidebar_mask_coexistence_with_desktop_widgets(mock_widgets_env):
    """Tier 1: 桌面组件与侧边栏同时存在时，两者交互区域正确求并集 (united)"""
    win, root, loader, sidebar = mock_widgets_env
    flow = QObject(loader)
    flow.setObjectName("widgetsFlow")
    flow.setParent(loader)
    flow.setParent(root)

    item = QObject()
    item.setVisible = lambda v: None
    item.isVisible = lambda: True
    item.x = lambda: 0
    item.y = lambda: 0
    item.width = lambda: 300
    item.height = lambda: 120
    flow.childItems = lambda: [item]
    flow.x = lambda: 0
    flow.y = lambda: 0
    loader.findChild = lambda t, n: flow if n == "widgetsFlow" else None

    sidebar.set_interactive_rects([[1740, 200, 180, 680]])

    win.update_mask()

    applied = root.get_applied_mask()
    assert applied.contains(QRect(100, 50, 300, 120))
    assert applied.contains(QRect(1740, 200, 180, 680))
    assert not applied.contains(QRect(800, 300, 50, 50))


def test_sidebar_mask_coexistence_with_floating_widget(mock_widgets_env):
    """Tier 1: 桌面组件、浮窗小组件与侧边栏三者同时共存时的遮罩合并"""
    win, root, _, sidebar = mock_widgets_env

    # 模拟浮窗组件
    floating = QObject(root)
    floating.setObjectName("floatingWidgetContainer")
    floating.isVisible = lambda: True
    floating.x = lambda: 400
    floating.y = lambda: 250
    floating.width = lambda: 200
    floating.height = lambda: 150
    floating.property = lambda name: 1.0 if name == "scale" else None
    root._children.append(floating)

    sidebar.set_interactive_rects([[1740, 200, 180, 680]])

    win.update_mask()

    applied = root.get_applied_mask()
    assert applied.contains(QRect(400, 250, 200, 150))
    assert applied.contains(QRect(1740, 200, 180, 680))
    assert not applied.contains(QRect(900, 500, 20, 20))


# ============================================================================
# Tier 2: 极端边界与多分辨率自适应遮罩验证
# ============================================================================


@pytest.mark.parametrize(
    "res_name,screen_w,screen_h,sidebar_x,sidebar_w",
    [
        ("1080p", 1920, 1080, 1740, 180),
        ("2K_QHD", 2560, 1440, 2380, 180),
        ("4K_UHD", 3840, 2160, 3640, 200),
        ("Laptop", 1366, 768, 1206, 160),
        ("Ultrawide", 3440, 1440, 3260, 180),
        ("Portrait", 1080, 1920, 920, 160),
    ],
)
def test_sidebar_mask_various_screen_resolutions(
    mock_widgets_env, res_name, screen_w, screen_h, sidebar_x, sidebar_w
):
    """Tier 2 边界: 不同屏幕分辨率下侧边栏交互遮罩均能准确定位，且屏幕中心 100% 穿透"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_sidebar_state("NORMAL")
    sidebar_rect = [sidebar_x, 150, sidebar_w, screen_h - 300]
    sidebar.set_interactive_rects([sidebar_rect])

    win.update_mask()

    applied = root.get_applied_mask()
    assert not applied.isEmpty()
    # 侧边栏内部
    assert applied.contains(QPoint(sidebar_x + 10, 200))
    # 屏幕正中心必须穿透
    center_point = QPoint(screen_w // 2, screen_h // 2)
    assert not applied.contains(center_point)


def test_sidebar_mask_empty_defense(mock_widgets_env):
    """Tier 2 边界: 当没有任何可见小组件与侧边栏时，自动防御为 QRect(0, 0, 1, 1) 防止全屏遮罩泄漏"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_interactive_rects([])

    win.update_mask()

    applied = root.get_applied_mask()
    assert not applied.isEmpty()
    assert applied.boundingRect() == QRect(0, 0, 1, 1)


def test_sidebar_mask_zero_and_negative_dimensions(mock_widgets_env):
    """Tier 2 边界: 上报宽度或高度 <= 0 的非法矩形时，安全过滤且不崩溃"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_interactive_rects([
        [100, 100, 0, 50],
        [200, 200, 50, -10],
        [300, 300, -20, -20],
    ])

    win.update_mask()

    applied = root.get_applied_mask()
    assert applied.boundingRect() == QRect(0, 0, 1, 1)


def test_sidebar_mask_multi_monitor_negative_coordinates(mock_widgets_env):
    """Tier 2 边界: 多显示器负坐标（副屏位于主屏左侧）正常支持合并计算"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_interactive_rects([[-1920, 100, 180, 700]])

    win.update_mask()

    applied = root.get_applied_mask()
    assert applied.contains(QRect(-1920, 100, 180, 700))


def test_sidebar_mask_menu_or_edit_mode_override(mock_widgets_env):
    """Tier 2 边界: 编辑模式或右键菜单弹出时，优先释放局部遮罩以便全局响应"""
    win, root, loader, sidebar = mock_widgets_env
    loader._menu_visible = True
    sidebar.set_interactive_rects([[1740, 200, 180, 680]])

    win.update_mask()

    applied = root.get_applied_mask()
    assert applied.isEmpty()


@pytest.mark.parametrize("px,py,expected_in_mask", [
    (1750, 250, True),    # 竖条顶部内部
    (1800, 500, True),    # 竖条中部内部
    (1910, 800, True),    # 竖条底部边缘内部
    (1739, 500, False),   # 竖条左侧 1 像素外 (必须穿透)
    (500, 500, False),    # 屏幕中心 (必须穿透)
    (0, 0, False),        # 屏幕左上角 (必须穿透)
    (100, 1000, False),   # 屏幕左下角 (必须穿透)
])
def test_sidebar_mask_pixel_level_penetration_sampling(mock_widgets_env, px, py, expected_in_mask):
    """Tier 1 [F10]: 像素级严格采样验证：只有竖条区域拦截，其余区域 100% 点击穿透"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_sidebar_state("NORMAL")
    sidebar.set_interactive_rects([[1740, 200, 180, 680]])

    win.update_mask()
    applied = root.get_applied_mask()
    assert applied.contains(QPoint(px, py)) is expected_in_mask


@pytest.mark.parametrize("scale", [0.5, 1.0, 1.25, 1.5, 2.0])
def test_sidebar_mask_floating_scale_compatibility(mock_widgets_env, scale):
    """Tier 2 边界: 浮窗处于不同系统 DPI / 自定义缩放比例 (scale) 时与侧边栏遮罩安全合并"""
    win, root, _, sidebar = mock_widgets_env
    floating = QObject(root)
    floating.setObjectName("floatingWidgetContainer")
    floating.isVisible = lambda: True
    floating.x = lambda: 200
    floating.y = lambda: 200
    floating.width = lambda: 100
    floating.height = lambda: 100
    floating.property = lambda name: scale if name == "scale" else None
    root._children.append(floating)

    sidebar.set_interactive_rects([[1740, 200, 180, 680]])
    win.update_mask()

    applied = root.get_applied_mask()
    scaled_w = int(100 * scale)
    scaled_h = int(100 * scale)
    assert applied.contains(QRect(200, 200, scaled_w, scaled_h))
    assert applied.contains(QRect(1740, 200, 180, 680))


def test_sidebar_collapse_mask_race_condition_immunity(mock_widgets_env):
    """
    回归测试: 验证最小化/折叠瞬间小胶囊遮罩立即可用，绝不因淡入动画未结束而返回空矩形导致 DWM 裁剪消失。
    确保折叠后无需点击顶部主程序浮窗即可直接命中并唤回侧边栏。
    """
    win, root, _, sidebar = mock_widgets_env
    # 模拟进入折叠态，小胶囊初始 opacity 为 0.0
    sidebar.set_sidebar_state("COLLAPSED")
    # 修复后的规范契约：无条件保留胶囊交互矩形
    capsule_rect = [1900, 508, 20, 64]
    sidebar.set_interactive_rects([capsule_rect])

    win.update_mask()
    applied = root.get_applied_mask()

    # 遮罩必须立即可用，不允许为空
    assert not applied.isEmpty()
    assert applied.contains(QRect(1900, 508, 20, 64))
    # 严密保证胶囊外依然 100% 穿透
    assert not applied.contains(QPoint(1899, 540))
    assert not applied.contains(QPoint(1000, 540))


def test_sidebar_left_edge_mask_and_penetration(mock_widgets_env):
    """
    Tier 1: 验证侧边栏切换至「靠左贴边」模式时的遮罩合并与屏幕点击穿透：
    左边缘竖条或小胶囊被精确保护，其余区域（右边缘、屏幕中心）严格 100% 穿透。
    """
    win, root, _, sidebar = mock_widgets_env
    # 1. 靠左贴边 - NORMAL 展开态 (竖条靠左，向右扩展预留按钮区)
    sidebar.set_sidebar_state("NORMAL")
    left_bar_rect = [8, 240, 370, 600] # 包含左侧竖条与右侧按钮区
    sidebar.set_interactive_rects([left_bar_rect])

    win.update_mask()
    applied = root.get_applied_mask()
    assert applied.contains(QRect(8, 240, 370, 600))
    # 屏幕右侧与中央应当 100% 穿透
    assert not applied.contains(QPoint(1800, 500))
    assert not applied.contains(QPoint(960, 540))

    # 2. 靠左贴边 - COLLAPSED 折叠态 (仅屏幕左边缘小胶囊)
    sidebar.set_sidebar_state("COLLAPSED")
    left_capsule_rect = [0, 508, 20, 64]
    sidebar.set_interactive_rects([left_capsule_rect])

    win.update_mask()
    applied_collapsed = root.get_applied_mask()
    assert applied_collapsed.contains(QRect(0, 508, 20, 64))
    # 胶囊右侧 1 像素外必须严格穿透
    assert not applied_collapsed.contains(QPoint(21, 540))
    assert not applied_collapsed.contains(QPoint(1900, 540))



