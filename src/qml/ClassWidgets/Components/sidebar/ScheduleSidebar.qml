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

    // 监听子组件尺寸与状态变化
    Connections {
        target: dailyBar
        function onHasActiveBubbleChanged() { sidebarRoot.geometryChanged(); }
        function onBarHoveredChanged() {
            if (dailyBar.barHovered) {
                hoverButtons.requestShow();
            } else if (!hoverButtons.isHovered) {
                hoverButtons.requestHideWithBuffer();
            }
            sidebarRoot.geometryChanged();
        }
    }

    Connections {
        target: hoverButtons
        function onButtonsVisibleChanged() { sidebarRoot.geometryChanged(); }
        function onActiveStateChanged() { sidebarRoot.geometryChanged(); }
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

        // 折叠态：仅贴边小胶囊
        if (sidebarState === "COLLAPSED") {
            if (edgeCapsule.visible && edgeCapsule.opacity > 0.05) {
                return [[edgeCapsule.x, edgeCapsule.y, edgeCapsule.width, edgeCapsule.height]];
            }
            return [];
        }

        // NORMAL 竖条态
        var rects = [];
        if (dailyBar.visible && dailyBar.opacity > 0.05) {
            rects.push([dailyBar.x, dailyBar.y, dailyBar.width, dailyBar.height]);

            // 悬浮气泡卡片矩形
            if (dailyBar.hasActiveBubble) {
                var bRect = dailyBar.getBubbleRect();
                if (bRect[2] > 0 && bRect[3] > 0) {
                    rects.push([dailyBar.x + bRect[0], dailyBar.y + bRect[1], bRect[2], bRect[3]]);
                }
            }
        }

        // 悬浮双按钮矩形
        if (hoverButtons.visible && hoverButtons.opacity > 0.05) {
            rects.push([hoverButtons.x, hoverButtons.y, hoverButtons.width, hoverButtons.height]);
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
    }

    function restoreFromEdge() {
        sidebarState = "NORMAL";
        if (Configs && Configs.set) {
            Configs.set("preferences.schedule_sidebar_collapsed", false);
        }
    }

    // ==========================================
    // R4: 贴边呼出微胶囊
    // ==========================================
    EdgeRestoreCapsule {
        id: edgeCapsule
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter
        isActive: (sidebarRoot.sidebarState === "COLLAPSED")
        z: 1000

        onRestoreClicked: {
            sidebarRoot.restoreFromEdge();
        }

        onIsHoveredChanged: {
            sidebarRoot.geometryChanged();
        }
    }

    // ==========================================
    // R1: 当天课表竖条胶囊主体
    // ==========================================
    DailyScheduleBar {
        id: dailyBar
        anchors.right: parent.right
        anchors.rightMargin: 8
        anchors.verticalCenter: parent.verticalCenter
        z: 1000

        opacity: (sidebarRoot.sidebarState === "NORMAL") ? 1.0 : 0.0
        visible: opacity > 0.01

        Behavior on opacity {
            NumberAnimation { duration: 240; easing.type: Easing.OutQuad }
        }
    }

    // 靠近竖条左侧时的鼠标感应扩展区 (触发双按钮滑出)
    MouseArea {
        id: hoverTriggerArea
        anchors.right: dailyBar.left
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
        anchors.right: dailyBar.left
        anchors.rightMargin: 10
        anchors.verticalCenter: dailyBar.verticalCenter
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
        anchors.right: parent.right
        anchors.rightMargin: 24
        anchors.verticalCenter: parent.verticalCenter
        z: 1050

        isExpanded: (sidebarRoot.sidebarState === "EXPANDED")

        onRequestClose: {
            sidebarRoot.retractWeeklyPanel();
        }
    }
}
