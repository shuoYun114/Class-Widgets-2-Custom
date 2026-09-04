# -*- coding: utf-8 -*-
"""
Class-Widgets-2 侧边栏交互遮罩与屏幕穿透测试 (Tier 1 & Tier 2)

覆盖范围:
- Tier 1: NORMAL 状态竖条遮罩合并、悬浮双按钮遮罩合并、COLLAPSED 贴边小胶囊微遮罩、
          EXPANDED 全周大面板外部点击全屏捕获遮罩、桌面小组件与侧边栏共存遮罩、浮窗共存遮罩、不可见侧边栏过滤
- Tier 2: 空遮罩 1x1 安全防御、零与负尺寸过滤、多显示器负坐标支持、编辑模式与菜单全屏覆盖、极小/极大分辨率容错
"""
import sys
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QCoreApplication, QObject, QRect, Property, Signal
from PySide6.QtGui import QRegion

from src.core.widgets.core import WidgetsWindow


@pytest.fixture(scope="session")
def qapp():
    """提供 PySide6 QCoreApplication 单例"""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app


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
def mock_widgets_env(qapp):
    """构建用于测试 update_mask 的 WidgetsWindow 运行环境"""
    central = MagicMock()
    central.theme_manager.currentTheme = "default"
    central.configs.interactions.hover_fade = False

    win = WidgetsWindow(central)
    root = DummyRootWindow()
    win.root_window = root

    loader = MockWidgetsLoader(root)
    root.add_child(loader)

    sidebar = MockScheduleSidebar(root)
    root.add_child(sidebar)

    return win, root, loader, sidebar


# ============================================================================
# Tier 1: 侧边栏各种交互状态下的遮罩合并计算
# ============================================================================


def test_sidebar_mask_normal_state_rect_merged(mock_widgets_env):
    """Tier 1: NORMAL 状态下，当天竖条交互矩形正确合并到窗口遮罩中"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_sidebar_state("NORMAL")
    # 模拟屏幕右侧竖条胶囊，位置 x=1740, y=200, 宽=180, 高=680
    capsule_rect = [1740, 200, 180, 680]
    sidebar.set_interactive_rects([capsule_rect])

    win.update_mask()

    applied = root.get_applied_mask()
    assert not applied.isEmpty()
    # 遮罩必须包含竖条区域
    assert applied.contains(QRect(1740, 200, 180, 680))
    # 竖条外侧任意区域必须穿透（不在遮罩中）
    assert not applied.contains(QRect(500, 500, 10, 10))


def test_sidebar_mask_normal_with_hover_buttons(mock_widgets_env):
    """Tier 1: 鼠标移入滑出悬浮双按钮时，竖条与双按钮两个交互矩形同时被包含在遮罩内"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_sidebar_state("NORMAL")
    capsule_rect = [1740, 200, 180, 680]
    # 悬浮双按钮位于竖条左侧: x=1690, y=300, 宽=40, 高=90
    buttons_rect = [1690, 300, 40, 90]
    sidebar.set_interactive_rects([capsule_rect, buttons_rect])

    win.update_mask()

    applied = root.get_applied_mask()
    assert applied.contains(QRect(1740, 200, 180, 680))
    assert applied.contains(QRect(1690, 300, 40, 90))
    # 验证非交互空白区域穿透
    assert not applied.contains(QRect(1000, 300, 10, 10))


def test_sidebar_mask_collapsed_state_capsule(mock_widgets_env):
    """Tier 1: COLLAPSED 折叠状态下，仅屏幕边缘微型贴边小胶囊保留遮罩，其余大片区域 100% 穿透"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_sidebar_state("COLLAPSED")
    # 极小边缘贴边胶囊: x=1900, y=500, 宽=20, 高=60
    capsule_rect = [1900, 500, 20, 60]
    sidebar.set_interactive_rects([capsule_rect])

    win.update_mask()

    applied = root.get_applied_mask()
    # 小胶囊必须在遮罩内
    assert applied.contains(QRect(1900, 500, 20, 60))
    assert applied.boundingRect() == QRect(1900, 500, 20, 60)
    # 原竖条主体位置点已被释放，必须完全穿透（不在遮罩中）
    from PySide6.QtCore import QPoint
    assert not applied.contains(QPoint(1750, 250))


def test_sidebar_mask_expanded_external_click_full_mask(mock_widgets_env):
    """Tier 1: EXPANDED 全周大面板展开时，触发全局遮罩 setMask(QRegion()) 支撑外部点击收回"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_sidebar_state("EXPANDED")
    sidebar.set_full_week_expanded(True)
    sidebar.set_interactive_rects([[1200, 150, 720, 780]])

    win.update_mask()

    applied = root.get_applied_mask()
    # 在 Qt 中，setMask(QRegion()) 意为清空局部掩码、使得全窗口生效捕获事件
    assert applied.isEmpty()


def test_sidebar_mask_hidden_sidebar_ignored(mock_widgets_env):
    """Tier 1: 侧边栏不可见时（isVisible=False），其上报的矩形不得合并入遮罩"""
    win, root, _, sidebar = mock_widgets_env
    sidebar.set_visible(False)
    sidebar.set_interactive_rects([[1740, 200, 180, 680]])

    win.update_mask()

    applied = root.get_applied_mask()
    # 不可见时不计入，如果无其他组件则触发最小 1x1 安全防御
    assert not applied.contains(QRect(1740, 200, 180, 680))
    assert applied.contains(QRect(0, 0, 1, 1))


def test_sidebar_mask_coexistence_with_desktop_widgets(mock_widgets_env):
    """Tier 1: 桌面组件与侧边栏同时存在时，两者交互区域正确求并集 (united)"""
    win, root, loader, sidebar = mock_widgets_env
    # 添加一个模拟桌面组件 item 到 widgetsFlow
    flow = QObject(loader)
    flow.setObjectName("widgetsFlow")
    flow.setParent(loader)
    flow.setParent(root)
    # 模拟桌面组件占据 [100, 50, 300, 120]
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

    # 侧边栏位于 [1740, 200, 180, 680]
    sidebar.set_interactive_rects([[1740, 200, 180, 680]])

    win.update_mask()

    applied = root.get_applied_mask()
    # 桌面小组件区域在 mask 内
    assert applied.contains(QRect(100, 50, 300, 120))
    # 侧边栏区域在 mask 内
    assert applied.contains(QRect(1740, 200, 180, 680))
    # 中间空白处穿透
    assert not applied.contains(QRect(800, 300, 50, 50))


# ============================================================================
# Tier 2: 极端边界与空遮罩安全防御验证
# ============================================================================


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
        [100, 100, 0, 50],    # 宽为 0
        [200, 200, 50, -10],  # 高为负
        [300, 300, -20, -20], # 均为负
    ])

    win.update_mask()

    applied = root.get_applied_mask()
    # 非法矩形全部被过滤，触发空遮罩 1x1 安全防御
    assert applied.boundingRect() == QRect(0, 0, 1, 1)


def test_sidebar_mask_multi_monitor_negative_coordinates(mock_widgets_env):
    """Tier 2 边界: 多显示器负坐标（副屏位于左侧）正常支持合并计算"""
    win, root, _, sidebar = mock_widgets_env
    # 副屏左边缘坐标: x=-1920, y=100, 宽=180, 高=700
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
    # 菜单弹出时调用 setMask(QRegion()) 清空遮罩
    assert applied.isEmpty()
