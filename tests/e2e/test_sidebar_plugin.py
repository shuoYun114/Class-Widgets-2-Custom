# -*- coding: utf-8 -*-
"""
Class-Widgets-2 侧边课表栏插件化自动化测试 (Sidebar Plugin Tests)

覆盖范围:
1. 插件元数据与 cwplugin.json 配置合规性验证
2. 插件生命周期：on_load 注册（设置页、Action、托盘快捷方式）与 on_unload 清理
3. 插件公用槽函数与信号响应：isSidebarEnabled, setSidebarEnabled, isCollapsed, toggleCollapse, expandWeekly
4. 内置插件列表 (BUILTIN_PLUGINS) 与 PluginLoader 扫描验证
5. Loader 动态挂载机制与穿透遮罩计算兼容性验证
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import QCoreApplication, QObject, QRect, QPoint, Signal
from PySide6.QtGui import QRegion

from src.core.config.manager import ConfigManager
from src.core.plugin.api import PluginAPI
from src.core.plugin.bridge import PluginBackendBridge
from src.core.plugin.loader import PluginLoader
from src.core.widgets.core import WidgetsWindow
from src.plugins import BUILTIN_PLUGINS
from src.plugins.cw_sidebar.sidebar import META, Plugin as SidebarPlugin


@pytest.fixture(scope="session")
def qapp():
    """提供 PySide6 QCoreApplication 单例"""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app


@pytest.fixture
def mock_app_central(tmp_path):
    """构建包含 ConfigManager 与 PluginAPI 的测试 AppCentral"""
    cfg = ConfigManager(tmp_path, "configs.json")

    app = MagicMock()
    app.configs = cfg
    app.themeManager = MagicMock()
    app.themeManager.currentTheme = "com.classwidgets.default"
    app.runtime = MagicMock()
    app.notification = MagicMock()
    app.automation_manager = MagicMock()

    api = PluginAPI(app)
    app.plugin_api = api
    return app


# =========================================================================
# 1. 元数据与配置文件规范测试
# =========================================================================

def test_sidebar_plugin_meta():
    """验证 META 字典的规范性"""
    assert META["id"] == "builtin.classwidgets.sidebar"
    assert META["entry"] == "sidebar.py"
    assert META["version"] == "1.0.0"
    assert "author" in META
    assert "description" in META


def test_sidebar_plugin_json():
    """验证 cwplugin.json 存在且与 META 匹配"""
    json_path = Path(__file__).parents[2] / "src" / "plugins" / "cw_sidebar" / "cwplugin.json"
    assert json_path.exists(), "cwplugin.json 文件必须存在"

    data = json.loads(json_path.read_text(encoding="utf-8"))
    assert data["id"] == META["id"]
    assert data["version"] == META["version"]
    assert data["entry"] == META["entry"]


def test_builtin_plugins_registration():
    """验证 BUILTIN_PLUGINS 中已注册侧边栏插件"""
    sidebar_entry = next((p for p in BUILTIN_PLUGINS if p["meta"]["id"] == "builtin.classwidgets.sidebar"), None)
    assert sidebar_entry is not None, "BUILTIN_PLUGINS 必须包含 builtin.classwidgets.sidebar"
    assert sidebar_entry["class"] is SidebarPlugin


# =========================================================================
# 2. 插件生命周期与 API 注册测试
# =========================================================================

def test_sidebar_plugin_lifecycle(qapp, mock_app_central):
    """验证插件 on_load 与 on_unload 的完整生命周期行为"""
    api = mock_app_central.plugin_api
    plugin = SidebarPlugin(api)
    plugin.meta = META

    # 执行加载
    plugin.on_load()

    # 1. 验证在 PluginBackendBridge 中完成注册
    backend = PluginBackendBridge._registry.get("builtin.classwidgets.sidebar")
    assert backend is plugin

    # 2. 验证设置页注册
    registered_pages = api.ui.pages
    sidebar_page = next((p for p in registered_pages if p["id"] == "builtin.classwidgets.sidebar"), None)
    assert sidebar_page is not None, "侧边栏设置页必须成功注册到 api.ui"
    assert "SidebarSettings.qml" in sidebar_page["page"]

    # 3. 验证 Action 注册
    action_toggle = api.actions.get("classwidgets.sidebar.toggle")
    assert action_toggle is not None
    action_expand = api.actions.get("classwidgets.sidebar.expand_weekly")
    assert action_expand is not None

    # 4. 验证托盘快捷方式注册
    shortcuts = api.ui.shortcuts
    toggle_shortcut = next((s for s in shortcuts if s["owner"] == "builtin.classwidgets.sidebar"), None)
    assert toggle_shortcut is not None

    # 执行卸载
    plugin.on_unload()

    # 验证设置页已被注销
    remaining_pages = [p for p in api.ui.pages if p["id"] == "builtin.classwidgets.sidebar"]
    assert len(remaining_pages) == 0, "卸载后侧边栏设置页必须被注销"

    # 验证快捷方式已被注销
    remaining_shortcuts = [s for s in api.ui.shortcuts if s["owner"] == "builtin.classwidgets.sidebar"]
    assert len(remaining_shortcuts) == 0, "卸载后侧边栏快捷方式必须被注销"


# =========================================================================
# 3. 插件 Slots 与信号测试
# =========================================================================

def test_sidebar_plugin_slots_and_signals(qapp, mock_app_central):
    """验证侧边栏插件暴露的槽函数读写与信号触发"""
    api = mock_app_central.plugin_api
    plugin = SidebarPlugin(api)
    plugin.meta = META
    plugin.on_load()

    # 1. 启用状态读写
    assert plugin.isSidebarEnabled() is True
    plugin.setSidebarEnabled(False)
    assert plugin.isSidebarEnabled() is False
    plugin.setSidebarEnabled(True)
    assert plugin.isSidebarEnabled() is True

    # 2. 折叠状态切换与信号
    collapse_states = []
    plugin.collapseChanged.connect(lambda s: collapse_states.append(s))

    assert plugin.isCollapsed() is False
    plugin.toggleCollapse()
    assert plugin.isCollapsed() is True
    assert collapse_states == [True]

    plugin.toggleCollapse()
    assert plugin.isCollapsed() is False
    assert collapse_states == [True, False]

    # 3. 全周展开信号
    expand_triggered = []
    plugin.expandWeeklyRequested.connect(lambda: expand_triggered.append(True))
    plugin.expandWeekly()
    assert expand_triggered == [True]

    plugin.on_unload()


# =========================================================================
# 4. Loader 动态挂载与鼠标穿透遮罩兼容性测试
# =========================================================================

from tests.e2e.test_sidebar_mask import DummyRootWindow, MockScheduleSidebar, MockWidgetsLoader


def test_sidebar_plugin_mask_computation(qapp, mock_app_central):
    """验证动态加载与卸载侧边栏时的鼠标穿透遮罩计算"""
    # 构建 Mock 主窗口与基础小组件容器
    root = DummyRootWindow()
    root.setProperty("width", 1920)
    root.setProperty("height", 1080)
    loader = MockWidgetsLoader(root)
    root.add_child(loader)

    # 初始状态：未载入侧边栏组件（例如插件禁用状态）
    win = WidgetsWindow(mock_app_central)
    win.root_window = root

    win.update_mask()
    # 遮罩正常设置，且当前无侧边栏区域
    applied_mask = root.get_applied_mask()
    assert applied_mask is not None
    assert not applied_mask.contains(QPoint(1750, 250))

    # 模拟侧边栏插件启用：Loader 挂载 ScheduleSidebar 实例
    sidebar = MockScheduleSidebar(root)
    sidebar.set_interactive_rects([[1740, 200, 180, 680]])
    root.add_child(sidebar)

    win.update_mask()
    applied_mask = root.get_applied_mask()
    # 验证遮罩成功融入侧边栏矩形 (1740, 200, 180, 680)
    assert applied_mask.contains(QPoint(1750, 250))

    # 模拟侧边栏插件禁用：Loader 销毁/卸载侧边栏组件
    root._children.remove(sidebar)

    win.update_mask()
    applied_mask = root.get_applied_mask()
    # 移除侧边栏后，原区域重新变回完全穿透
    assert not applied_mask.contains(QPoint(1750, 250))

    win.release()

