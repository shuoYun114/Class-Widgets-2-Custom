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

    // 监听子组件尺寸与状态变化 (仅关键物理尺寸与状态变更时通知，避免 hover 中途反复触发 setMask)
    Connections {
        target: dailyBar
        function onHeightChanged() { sidebarRoot.geometryChanged(); }
        function onBarHoveredChanged() {
            if (dailyBar.barHovered) {
                hoverButtons.requestShow();
            } else if (!hoverButtons.isHovered) {
                hoverButtons.requestHideWithBuffer();
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

        // NORMAL 竖条态：合并竖条与按钮/详情气泡预留区
        // 一次性分配好交互区域，避免在鼠标悬停、按钮滑出、气泡淡入期间频繁调用 Win32 SetWindowRgn 造成 DWM 动画掉帧
        var rects = [];
        if (dailyBar.visible && dailyBar.opacity > 0.05) {
            var extraSpace = 210; // 覆盖悬浮按钮(44px)与气泡卡片(190px)
            if (isLeftEdge) {
                // 靠左贴边：按钮和气泡在竖条右侧
                var areaX = dailyBar.x;
                var areaW = dailyBar.width + extraSpace;
                rects.push([areaX, dailyBar.y, areaW, dailyBar.height]);
            } else {
                // 靠右贴边：按钮和气泡在竖条左侧
                var areaX = Math.max(0, dailyBar.x - extraSpace);
                var areaW = (dailyBar.x + dailyBar.width) - areaX;
                rects.push([areaX, dailyBar.y, areaW, dailyBar.height]);
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
    // R4: 贴边呼出微胶囊
    // ==========================================
    EdgeRestoreCapsule {
        id: edgeCapsule
        anchors.right: sidebarRoot.isLeftEdge ? undefined : parent.right
        anchors.left: sidebarRoot.isLeftEdge ? parent.left : undefined
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: sidebarRoot.sidebarOffsetY
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
    // R1: 当天课表竖条胶囊主体
    // ==========================================
    DailyScheduleBar {
        id: dailyBar
        anchors.right: sidebarRoot.isLeftEdge ? undefined : parent.right
        anchors.rightMargin: sidebarRoot.isLeftEdge ? 0 : 8
        anchors.left: sidebarRoot.isLeftEdge ? parent.left : undefined
        anchors.leftMargin: sidebarRoot.isLeftEdge ? 8 : 0
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: sidebarRoot.sidebarOffsetY
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
        anchors.right: sidebarRoot.isLeftEdge ? undefined : dailyBar.left
        anchors.left: sidebarRoot.isLeftEdge ? dailyBar.right : undefined
        anchors.verticalCenter: dailyBar.verticalCenter
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
    // R2: 悬浮双按钮交互组件
    // ==========================================
    SidebarHoverButtons {
        id: hoverButtons
        anchors.right: sidebarRoot.isLeftEdge ? undefined : dailyBar.left
        anchors.rightMargin: sidebarRoot.isLeftEdge ? 0 : 10
        anchors.left: sidebarRoot.isLeftEdge ? dailyBar.right : undefined
        anchors.leftMargin: sidebarRoot.isLeftEdge ? 10 : 0
        anchors.verticalCenter: dailyBar.verticalCenter
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
    // R3: 全周课表网格大面板
    // ==========================================
    WeeklySchedulePanel {
        id: weeklyPanel
        anchors.right: sidebarRoot.isLeftEdge ? undefined : parent.right
        anchors.rightMargin: sidebarRoot.isLeftEdge ? 0 : 24
        anchors.left: sidebarRoot.isLeftEdge ? parent.left : undefined
        anchors.leftMargin: sidebarRoot.isLeftEdge ? 24 : 0
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: sidebarRoot.sidebarOffsetY
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
