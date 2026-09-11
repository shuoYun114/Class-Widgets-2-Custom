import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI
import ClassWidgets.Theme 1.0
import ClassWidgets.Easing

Item {
    id: sidebarRoot
    objectName: "scheduleSidebar"

    // 填充父级窗口 (全屏)
    anchors.fill: parent
    z: 1100

    // 是否启用开关
    readonly property bool enabledConfig: (Configs && Configs.data && Configs.data.preferences)
        ? (Configs.data.preferences.schedule_sidebar_enabled !== false)
        : true

    // 贴靠屏幕边缘: "right" (默认) | "left"
    readonly property string sidebarEdge: (Configs && Configs.data && Configs.data.preferences && Configs.data.preferences.schedule_sidebar_edge)
        ? Configs.data.preferences.schedule_sidebar_edge
        : "right"
    readonly property bool isLeftEdge: (sidebarEdge === "left")

    // 垂直中心偏移量 (微调上下高度)
    readonly property int sidebarOffsetY: (Configs && Configs.data && Configs.data.preferences && Configs.data.preferences.schedule_sidebar_offset_y !== undefined)
        ? Configs.data.preferences.schedule_sidebar_offset_y
        : 0

    // 是否启用侧边栏独立外观
    readonly property bool customAppearance: (Configs && Configs.data && Configs.data.preferences)
        ? (Configs.data.preferences.schedule_sidebar_custom_appearance === true)
        : false

    // 生效圆角大小 (像素): 默认跟随主程序全局外观 widget_corner_radius，自定义时使用专属值
    readonly property real effectiveCornerRadius: {
        if (customAppearance) {
            return (Configs && Configs.data && Configs.data.preferences && Configs.data.preferences.schedule_sidebar_corner_radius !== undefined)
                ? Configs.data.preferences.schedule_sidebar_corner_radius
                : 22.0;
        }
        return (Configs && Configs.data && Configs.data.preferences && Configs.data.preferences.widget_corner_radius !== undefined)
            ? Configs.data.preferences.widget_corner_radius
            : 22.0;
    }

    // 生效背景不透明度 (0.0 ~ 1.0): 默认跟随主程序全局外观 opacity，自定义时使用专属值
    readonly property real effectiveOpacity: {
        if (customAppearance) {
            return (Configs && Configs.data && Configs.data.preferences && Configs.data.preferences.schedule_sidebar_opacity !== undefined)
                ? Configs.data.preferences.schedule_sidebar_opacity
                : 1.0;
        }
        return (Configs && Configs.data && Configs.data.preferences && Configs.data.preferences.opacity !== undefined)
            ? Configs.data.preferences.opacity
            : 1.0;
    }

    // 初始折叠配置
    readonly property bool initialCollapsed: (Configs && Configs.data && Configs.data.preferences)
        ? (Configs.data.preferences.schedule_sidebar_collapsed === true)
        : false

    // 状态机: "NORMAL" | "EXPANDED" | "COLLAPSED"
    property string sidebarState: initialCollapsed ? "COLLAPSED" : "NORMAL"

    // 是否处于全周展开态 (供 Python 遮罩全屏临时捕获)
    readonly property bool isFullWeekExpanded: (sidebarState === "EXPANDED")

    // 交互矩形列表属性 (方便 Python 端 property 读取)
    readonly property var interactiveRects: getInteractiveRects()

    // 组件整体可见性
    visible: enabledConfig

    // 对外通知几何与遮罩改变信号 (触发 Python WidgetsWindow.schedule_mask_update)
    signal geometryChanged()

    onSidebarStateChanged: {
        sidebarRoot.geometryChanged();
    }

    onVisibleChanged: {
        sidebarRoot.geometryChanged();
    }

    onSidebarEdgeChanged: {
        sidebarRoot.geometryChanged();
    }

    onSidebarOffsetYChanged: {
        sidebarRoot.geometryChanged();
    }

    // 监听子组件尺寸与状态变化，实现遮罩精准动态联动
    Connections {
        target: dailyBar
        function onHeightChanged() { sidebarRoot.geometryChanged(); }
        function onHasActiveBubbleChanged() { sidebarRoot.geometryChanged(); }
        function onBubbleCardYChanged() { sidebarRoot.geometryChanged(); }
        function onBarHoveredChanged() {
            if (dailyBar.barHovered) {
                hoverButtons.requestShow();
            } else if (!hoverButtons.isHovered) {
                hoverButtons.requestHideWithBuffer();
            }
        }
    }

    // 监听悬浮双按钮状态，滑出或隐藏时更新遮罩
    Connections {
        target: hoverButtons
        function onVisibleChanged() { sidebarRoot.geometryChanged(); }
        function onOpacityChanged() {
            if (hoverButtons.opacity > 0.05 || hoverButtons.opacity < 0.01) {
                sidebarRoot.geometryChanged();
            }
        }
    }

    // 监听贴边微胶囊状态变化，确保折叠态遮罩及时同步
    Connections {
        target: edgeCapsule
        function onVisibleChanged() { sidebarRoot.geometryChanged(); }
        function onIsActiveChanged() { sidebarRoot.geometryChanged(); }
    }

    // ==========================================
    // 计算并返回当前所有有效交互矩形 [ [x, y, w, h], ... ]
    // ==========================================
    function getInteractiveRects() {
        if (!visible || !enabledConfig) {
            return [];
        }

        // 全周展开时返回全屏以支持外部点击透明区域收回
        if (sidebarState === "EXPANDED") {
            return [[0, 0, width, height]];
        }

        // 折叠态：仅贴边小胶囊（无条件立即保留遮罩区域，杜绝淡入动画期间 DWM 裁剪导致不可见与穿透失效）
        if (sidebarState === "COLLAPSED") {
            return [[edgeCapsule.x, edgeCapsule.y, edgeCapsule.width, edgeCapsule.height]];
        }

        // NORMAL 竖条态：精准多矩形按需分配，杜绝占用左右多余空白桌面空间
        var rects = [];
        if (dailyBar.visible && dailyBar.opacity > 0.05) {
            // 1. 竖条胶囊主体 (绝对贴边，仅160px宽)
            rects.push([dailyBar.x, dailyBar.y, dailyBar.width, dailyBar.height]);

            // 2. 悬浮双按钮 (仅在滑出可见时加入遮罩，紧靠竖条，44px宽)
            if (hoverButtons.visible && hoverButtons.opacity > 0.05) {
                rects.push([hoverButtons.x, hoverButtons.y, hoverButtons.width, hoverButtons.height]);
            }

            // 3. 课程详情气泡卡片 (仅在用户点击课程弹出详情时加入遮罩，卡片关闭后桌面右键立即穿透)
            if (dailyBar.hasActiveBubble) {
                var bubbleAbsX = dailyBar.x + dailyBar.bubbleCardX;
                var bubbleAbsY = dailyBar.y + dailyBar.bubbleCardY;
                rects.push([bubbleAbsX, bubbleAbsY, dailyBar.bubbleCardW, dailyBar.bubbleCardH]);
            }
        }

        return rects;
    }

    // ==========================================
    // 外部透明区域点击捕获 (全周面板展开时点击外部自动收回)
    // ==========================================
    MouseArea {
        id: outsideCatchArea
        anchors.fill: parent
        enabled: sidebarRoot.isFullWeekExpanded
        visible: sidebarRoot.isFullWeekExpanded
        hoverEnabled: false
        z: 900
        onClicked: {
            sidebarRoot.retractWeeklyPanel();
        }
    }

    // 状态切换方法
    function expandWeeklyPanel() {
        sidebarState = "EXPANDED";
        hoverButtons.hideImmediately();
    }

    function retractWeeklyPanel() {
        sidebarState = "NORMAL";
    }

    function collapseToEdge() {
        sidebarState = "COLLAPSED";
        hoverButtons.hideImmediately();
        if (Configs && Configs.set) {
            Configs.set("preferences.schedule_sidebar_collapsed", true);
        }
        sidebarRoot.geometryChanged();
    }

    function restoreFromEdge() {
        sidebarState = "NORMAL";
        if (Configs && Configs.set) {
            Configs.set("preferences.schedule_sidebar_collapsed", false);
        }
        sidebarRoot.geometryChanged();
    }

    // ==========================================
    // R4: 贴边呼出微胶囊 (显式坐标定位，彻底杜绝动态锚点冲突拉伸)
    // ==========================================
    EdgeRestoreCapsule {
        id: edgeCapsule
        x: sidebarRoot.isLeftEdge ? 0 : Math.max(0, sidebarRoot.width - width)
        y: Math.max(0, (sidebarRoot.height - height) / 2 + sidebarRoot.sidebarOffsetY)
        isLeftEdge: sidebarRoot.isLeftEdge
        cornerRadius: Math.min(12, sidebarRoot.effectiveCornerRadius / 2)
        bgOpacity: sidebarRoot.effectiveOpacity
        isActive: (sidebarRoot.sidebarState === "COLLAPSED")
        z: 1000

        onRestoreClicked: {
            sidebarRoot.restoreFromEdge();
        }
    }

    // ==========================================
    // R1: 当天课表竖条胶囊主体 (显式坐标定位，绝对宽度160px，绝不拉伸为横条)
    // ==========================================
    DailyScheduleBar {
        id: dailyBar
        x: sidebarRoot.isLeftEdge ? 8 : Math.max(0, sidebarRoot.width - width - 8)
        y: Math.max(0, (sidebarRoot.height - height) / 2 + sidebarRoot.sidebarOffsetY)
        isLeftEdge: sidebarRoot.isLeftEdge
        cornerRadius: sidebarRoot.effectiveCornerRadius
        bgOpacity: sidebarRoot.effectiveOpacity
        z: 1000

        opacity: (sidebarRoot.sidebarState === "NORMAL") ? 1.0 : 0.0
        visible: opacity > 0.01

        Behavior on opacity {
            NumberAnimation { duration: 240; easing.type: Easing.OutQuad }
        }
    }

    // 靠近竖条一侧时的鼠标感应扩展区 (触发双按钮滑出)
    MouseArea {
        id: hoverTriggerArea
        x: sidebarRoot.isLeftEdge ? (dailyBar.x + dailyBar.width) : Math.max(0, dailyBar.x - width)
        y: dailyBar.y
        width: 32
        height: dailyBar.height
        hoverEnabled: true
        enabled: (sidebarRoot.sidebarState === "NORMAL")
        z: 950

        onEntered: {
            hoverButtons.requestShow();
        }
        onExited: {
            if (!hoverButtons.isHovered && !dailyBar.barHovered) {
                hoverButtons.requestHideWithBuffer();
            }
        }
    }

    // ==========================================
    // R2: 悬浮双按钮交互组件 (显式坐标跟随 dailyBar)
    // ==========================================
    SidebarHoverButtons {
        id: hoverButtons
        x: sidebarRoot.isLeftEdge ? (dailyBar.x + dailyBar.width + 10) : Math.max(0, dailyBar.x - width - 10)
        y: dailyBar.y + (dailyBar.height - height) / 2
        isLeftEdge: sidebarRoot.isLeftEdge
        cornerRadius: Math.min(21, sidebarRoot.effectiveCornerRadius)
        bgOpacity: sidebarRoot.effectiveOpacity
        z: 1010
        enabled: (sidebarRoot.sidebarState === "NORMAL")

        onExpandWeeklyClicked: {
            sidebarRoot.expandWeeklyPanel();
        }

        onCollapseSidebarClicked: {
            sidebarRoot.collapseToEdge();
        }
    }

    // ==========================================
    // R3: 全周课表网格大面板 (显式坐标定位)
    // ==========================================
    WeeklySchedulePanel {
        id: weeklyPanel
        x: sidebarRoot.isLeftEdge ? 24 : Math.max(0, sidebarRoot.width - width - 24)
        y: Math.max(0, (sidebarRoot.height - height) / 2 + sidebarRoot.sidebarOffsetY)
        isLeftEdge: sidebarRoot.isLeftEdge
        cornerRadius: sidebarRoot.effectiveCornerRadius
        bgOpacity: sidebarRoot.effectiveOpacity
        z: 1050

        isExpanded: (sidebarRoot.sidebarState === "EXPANDED")

        onRequestClose: {
            sidebarRoot.retractWeeklyPanel();
        }
    }
}
