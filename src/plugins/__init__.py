from .cw_widgets.widgets import META as CW_META, Plugin as CW_Plugin
from .cw_sidebar.sidebar import META as SIDEBAR_META, Plugin as SidebarPlugin

BUILTIN_PLUGINS = [
    {
        "meta": CW_META,
        "class": CW_Plugin,
    },
    {
        "meta": SIDEBAR_META,
        "class": SidebarPlugin,
    },
]