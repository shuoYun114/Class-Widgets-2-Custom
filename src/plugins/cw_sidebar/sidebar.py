"""
侧边课表栏插件核心入口 (Schedule Sidebar Plugin)
继承自 CW2Plugin，负责侧边栏的生命周期、配置模型、设置页注册与全局动作注册。
"""

from pathlib import Path
from typing import Optional
from PySide6.QtCore import Slot, Signal, QCoreApplication, QObject
from loguru import logger

from src.core.plugin import CW2Plugin, PluginAPI


META = {
    "id": "builtin.classwidgets.sidebar",
    "name": QCoreApplication.translate("Plugins", "Schedule Sidebar"),
    "author": "Class Widgets Official",
    "version": "1.0.0",
    "api_version": "*",
    "entry": "sidebar.py",
    "description": QCoreApplication.translate(
        "Plugins", "Desktop edge schedule capsule with full-week matrix panel"
    ),
    "tags": ["schedule", "sidebar", "desktop", "capsule"]
}


class Plugin(CW2Plugin):
    """侧边栏插件主逻辑类"""

    # 供 QML 端监听的状态变更信号
    collapseChanged = Signal(bool)
    expandWeeklyRequested = Signal()

    def __init__(self, plugin_api: PluginAPI):
        super().__init__(plugin_api)
        self.settings_page_path = Path(__file__).parent / "pages" / "SidebarSettings.qml"
        self._action_toggle = None
        self._action_expand_weekly = None

    def on_load(self):
        """插件加载初始化"""
        super().on_load()
        logger.info("[SidebarPlugin] Loading Schedule Sidebar plugin...")

        # 1. 注册插件设置页面到主程序设置中心 (Plugins 分类下)
        try:
            if self.settings_page_path.exists():
                self.api.ui.register_settings_page(
                    qml_path=self.settings_page_path,
                    title=QCoreApplication.translate("Plugins", "Schedule Sidebar"),
                    icon="ic_fluent_panel_right_20_regular"
                )
                logger.debug(f"[SidebarPlugin] Registered settings page: {self.settings_page_path}")
        except Exception as err:
            logger.warning(f"[SidebarPlugin] Failed to register settings page: {err}")

        # 2. 注册进程内全局 Action 信号，支持跨模块或快捷键调用
        try:
            self._action_toggle = self.api.actions.register("classwidgets.sidebar.toggle")
            self._action_toggle.connect(self.toggleCollapse)
            self._action_expand_weekly = self.api.actions.register("classwidgets.sidebar.expand_weekly")
            self._action_expand_weekly.connect(self.expandWeekly)
            logger.debug("[SidebarPlugin] Registered sidebar actions (toggle, expand_weekly)")
        except Exception as err:
            logger.warning(f"[SidebarPlugin] Failed to register actions: {err}")

        # 3. 注册托盘快捷操作项
        try:
            self.api.ui.register_shortcut(
                shortcut_id="toggle",
                name=QCoreApplication.translate("Plugins", "Toggle Sidebar"),
                icon="ic_fluent_panel_right_20_regular",
                action=self.toggleCollapse
            )
            logger.debug("[SidebarPlugin] Registered tray shortcut: toggle")
        except Exception as err:
            logger.warning(f"[SidebarPlugin] Failed to register tray shortcut: {err}")

        logger.info("[SidebarPlugin] Schedule Sidebar plugin loaded successfully.")

    def on_unload(self):
        """插件卸载清理"""
        logger.info("[SidebarPlugin] Unloading Schedule Sidebar plugin...")

        # 注销设置页
        try:
            self.api.ui.unregister_settings_page(self.settings_page_path)
        except Exception as err:
            logger.warning(f"[SidebarPlugin] Failed to unregister settings page: {err}")

        # 注销托盘快捷项
        try:
            if self.pid:
                self.api.ui.unregister_plugin_shortcuts(self.pid)
        except Exception as err:
            logger.warning(f"[SidebarPlugin] Failed to unregister shortcuts: {err}")

        logger.info("[SidebarPlugin] Schedule Sidebar plugin unloaded.")

    # =========================================================================
    # QML / 外部调用的公共 Slots
    # =========================================================================

    @Slot(result=bool)
    def isSidebarEnabled(self) -> bool:
        """检查侧边栏在偏好设置中是否开启"""
        try:
            configs = self.api._app.configs
            return bool(getattr(configs.preferences, "schedule_sidebar_enabled", True))
        except Exception:
            return True

    @Slot(bool)
    def setSidebarEnabled(self, enabled: bool):
        """设置侧边栏启用状态"""
        try:
            self.api._app.configs.set("preferences.schedule_sidebar_enabled", enabled)
        except Exception as err:
            logger.error(f"[SidebarPlugin] Failed to set schedule_sidebar_enabled: {err}")

    @Slot(result=bool)
    def isCollapsed(self) -> bool:
        """获取侧边栏当前是否贴边折叠"""
        try:
            configs = self.api._app.configs
            return bool(getattr(configs.preferences, "schedule_sidebar_collapsed", False))
        except Exception:
            return False

    @Slot()
    def toggleCollapse(self):
        """切换贴边折叠与展开状态"""
        new_state = not self.isCollapsed()
        try:
            self.api._app.configs.set("preferences.schedule_sidebar_collapsed", new_state)
            self.collapseChanged.emit(new_state)
            logger.debug(f"[SidebarPlugin] Toggled sidebar collapse state: {new_state}")
        except Exception as err:
            logger.error(f"[SidebarPlugin] Failed to toggle collapse: {err}")

    @Slot()
    def expandWeekly(self):
        """请求展开全周课表面板"""
        self.expandWeeklyRequested.emit()
        logger.debug("[SidebarPlugin] Requested full week matrix expansion")
