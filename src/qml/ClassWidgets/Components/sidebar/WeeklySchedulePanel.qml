import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects
import RinUI
import ClassWidgets.Theme 1.0
import ClassWidgets.Easing

Item {
    id: weeklyPanelRoot

    // 尺寸设定 (适配屏幕分辨率 1366~3840，提供充裕纵向空间以实现全天课程无滚动全览)
    width: Math.min(parent ? parent.width * 0.90 : 920, 920)
    height: Math.min(parent ? parent.height * 0.88 : 720, 720)

    // 展开状态与控制
    property bool isExpanded: false
    property var weekData: (AppCentral.scheduleRuntime && AppCentral.scheduleRuntime.sidebarWeekSchedule)
        ? AppCentral.scheduleRuntime.sidebarWeekSchedule
        : { "currentDayOfWeek": 1, "days": {} }

    // 自定义外观与定位属性 (由父级 ScheduleSidebar 传入)
    property bool isLeftEdge: false
    property real cornerRadius: 22
    property real bgOpacity: 1.0

    signal requestClose()

    // 进出平滑动画 (根据贴边方向镜像 Translate 矩阵位移与淡入)
    opacity: isExpanded ? 1.0 : 0.0
    visible: opacity > 0.01

    Behavior on opacity {
        NumberAnimation { duration: 220; easing.type: Easing.OutQuad }
    }

    transform: Translate {
        x: weeklyPanelRoot.isExpanded ? 0 : (weeklyPanelRoot.isLeftEdge ? -36 : 36)
        Behavior on x {
            NumberAnimation {
                duration: 240
                easing.type: Easing.OutCubic
            }
        }
    }

    // 提供给遮罩计算
    function getPanelRect() {
        if (!isExpanded) return [0, 0, 0, 0];
        return [x, y, width, height];
    }

    function getRetractButtonRect() {
        if (!isExpanded) return [0, 0, 0, 0];
        return [retractBtnItem.x, retractBtnItem.y, retractBtnItem.width, retractBtnItem.height];
    }

    // ==========================================
    // 苹果液态玻璃大面板质感 (对齐主程序 Widget.qml 与 DailyScheduleBar)
    // 68% 高透光率 + FastBlur 内部柔和流光漫反射 + 对角线渐变物理微高光边框
    // ==========================================
    Rectangle {
        id: panelBackground
        anchors.fill: parent
        radius: weeklyPanelRoot.cornerRadius
        color: Theme.isDark()
            ? Qt.alpha("#1E1D22", 0.68 * weeklyPanelRoot.bgOpacity)
            : Qt.alpha("#FBFAFF", 0.72 * weeklyPanelRoot.bgOpacity)
    }

    // 内部流光微发光层 (Lighting Effect - FastBlur 内部弥散漫反射，营造温润通透感)
    Item {
        anchors.fill: parent
        clip: true

        Rectangle {
            id: ambientGlowLeft
            x: parent.width * 0.15 - width / 2
            y: parent.height * 0.25 - height / 2
            width: 340
            height: 340
            radius: 170
            color: Theme.accentColor || "#4099b2"
            opacity: (Configs.data && Configs.data.preferences && Configs.data.preferences.lighting_effect !== false) ? 0.25 : 0.0
            visible: opacity > 0.01

            layer.enabled: true
            layer.effect: FastBlur {
                anchors.fill: ambientGlowLeft
                radius: 64
                transparentBorder: true
            }
        }

        Rectangle {
            id: ambientGlowRight
            x: parent.width * 0.85 - width / 2
            y: parent.height * 0.75 - height / 2
            width: 320
            height: 320
            radius: 160
            color: Theme.accentColor || "#4099b2"
            opacity: (Configs.data && Configs.data.preferences && Configs.data.preferences.lighting_effect !== false) ? 0.20 : 0.0
            visible: opacity > 0.01

            layer.enabled: true
            layer.effect: FastBlur {
                anchors.fill: ambientGlowRight
                radius: 64
                transparentBorder: true
            }
        }
    }

    // 渐变微高光边框 (完全复刻主程序 Widget.qml 的 LinearGradient + OpacityMask 规范)
    Item {
        anchors.fill: parent
        Rectangle {
            id: borderRect
            anchors.fill: parent
            radius: panelBackground.radius
            layer.enabled: true
            layer.effect: LinearGradient {
                start: Qt.point(0, 0)
                end: Qt.point(width, height)
                gradient: Gradient {
                    GradientStop { position: 0.0; color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.45) : Qt.alpha("#FFFFFF", 0.95) }
                    GradientStop { position: 0.4; color: Qt.alpha("#FFFFFF", 0.05) }
                    GradientStop { position: 0.6; color: Qt.alpha("#FFFFFF", 0.05) }
                    GradientStop { position: 1.0; color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.35) : Qt.alpha("#FFFFFF", 0.75) }
                }
            }
        }
        layer.enabled: true
        layer.effect: OpacityMask {
            maskSource: Rectangle {
                width: borderRect.width
                height: borderRect.height
                radius: borderRect.radius
                color: "transparent"
                border.width: 1
            }
        }
        z: 10
    }

    // 拦截点击避免穿透到背景外部收回区域
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
    }

    // 面板内部主布局
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 10

        // ==========================================
        // 顶部极简标题栏
        // ==========================================
        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 32
            spacing: 10

            // 极简微光小点
            Rectangle {
                width: 4
                height: 4
                radius: 2
                color: Theme.accentColor || "#007AFF"
            }

            Text {
                text: "全周课表"
                font.pixelSize: 15
                font.bold: true
                color: Theme.isDark() ? "#F5F5F7" : "#1D1D1F"
            }

            // 极简周数微胶囊
            Rectangle {
                radius: 9
                height: 18
                width: weekBadgeText.implicitWidth + 14
                color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.07) : Qt.alpha("#000000", 0.05)

                Text {
                    id: weekBadgeText
                    anchors.centerIn: parent
                    text: {
                        var w = AppCentral.scheduleRuntime ? AppCentral.scheduleRuntime.currentWeek : 1;
                        return "第 " + w + " 周";
                    }
                    font.pixelSize: 10
                    color: Theme.isDark() ? "#9898A0" : "#6E6E73"
                }
            }

            Item { Layout.fillWidth: true }

            // 顶部关闭微按钮 (极细矢量叉叉，替代生硬字符 ✕)
            Rectangle {
                width: 26
                height: 26
                radius: 13
                color: closeHoverArea.containsMouse
                    ? (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.12) : Qt.alpha("#000000", 0.08))
                    : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.05) : Qt.alpha("#000000", 0.04))

                Canvas {
                    anchors.centerIn: parent
                    width: 10
                    height: 10
                    onPaint: {
                        var ctx = getContext("2d");
                        ctx.clearRect(0, 0, width, height);
                        ctx.strokeStyle = closeHoverArea.containsMouse
                            ? (Theme.isDark() ? "#FFFFFF" : "#1D1D1F")
                            : (Theme.isDark() ? "#A0A0A6" : "#6E6E73");
                        ctx.lineWidth = 1.4;
                        ctx.lineCap = "round";
                        ctx.beginPath();
                        ctx.moveTo(1, 1);
                        ctx.lineTo(9, 9);
                        ctx.moveTo(9, 1);
                        ctx.lineTo(1, 9);
                        ctx.stroke();
                    }

                    Connections {
                        target: closeHoverArea
                        function onContainsMouseChanged() { parent.children[0].requestPaint(); }
                    }
                }

                MouseArea {
                    id: closeHoverArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: weeklyPanelRoot.requestClose()
                }
            }
        }


        // ==========================================
        // 周一至周日 7 列网格
        // ==========================================
        RowLayout {
            id: weekColumnsRow
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 8

            Repeater {
                model: 7

                // 单天纵向列容器
                Rectangle {
                    id: dayColumnRect
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    radius: 10

                    readonly property int dayIndex: index + 1 // 1 到 7
                    readonly property bool isToday: {
                        var curr = weeklyPanelRoot.weekData ? weeklyPanelRoot.weekData.currentDayOfWeek : 1;
                        return dayIndex === curr;
                    }
                    readonly property var dayEntries: {
                        if (weeklyPanelRoot.weekData && weeklyPanelRoot.weekData.days) {
                            return weeklyPanelRoot.weekData.days[dayIndex.toString()] || [];
                        }
                        return [];
                    }

                    // 柔和微底色与边框 (今天采用低饱和微光染色，绝不涂大面积纯色块)
                    color: isToday
                        ? (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.05) : Qt.alpha(Theme.accentColor || "#007AFF", 0.05))
                        : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.02) : Qt.alpha("#000000", 0.02))
                    border.width: 1
                    border.color: isToday
                        ? Qt.alpha(Theme.accentColor || "#007AFF", 0.35)
                        : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.06) : Qt.alpha("#000000", 0.05))

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 4
                        spacing: 4

                        // 星期标头微胶囊
                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 24
                            radius: 6
                            color: dayColumnRect.isToday
                                ? (Theme.isDark() ? Qt.alpha(Theme.accentColor || "#007AFF", 0.28) : Qt.alpha(Theme.accentColor || "#007AFF", 0.16))
                                : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.04) : Qt.alpha("#000000", 0.03))

                            RowLayout {
                                anchors.centerIn: parent
                                spacing: 4

                                Text {
                                    text: ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][index]
                                    font.pixelSize: 11
                                    font.bold: dayColumnRect.isToday
                                    color: dayColumnRect.isToday
                                        ? (Theme.isDark() ? "#FFFFFF" : (Theme.accentColor || "#007AFF"))
                                        : (Theme.isDark() ? "#C0C0C6" : "#48484A")
                                }

                                Rectangle {
                                    visible: dayColumnRect.isToday
                                    width: 3
                                    height: 3
                                    radius: 1.5
                                    color: Theme.isDark() ? "#FFFFFF" : (Theme.accentColor || "#007AFF")
                                }
                            }
                        }

                        // 该天课程列表 (单卡紧凑38px设计，全天9~12节课无需滚动直接完全显示)
                        ListView {
                            id: dayEntriesList
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true
                            spacing: 4
                            boundsBehavior: Flickable.StopAtBounds

                            model: dayColumnRect.dayEntries

                            // 无课提示
                            Item {
                                anchors.centerIn: parent
                                width: parent.width
                                height: 60
                                visible: dayEntriesList.count === 0

                                Text {
                                    anchors.centerIn: parent
                                    text: "无课"
                                    font.pixelSize: 11
                                    color: Theme.isDark() ? "#666666" : "#A0A0A0"
                                }
                            }

                            delegate: Rectangle {
                                width: dayEntriesList.width
                                height: 38
                                radius: 7

                                readonly property bool isCurrent: modelData.isCurrent || false
                                readonly property color itemColor: modelData.color || "#007AFF"

                                color: {
                                    if (isCurrent) {
                                        return Theme.isDark() ? Qt.alpha(itemColor, 0.18) : Qt.alpha(itemColor, 0.12);
                                    }
                                    if (cellMouseArea.containsMouse) {
                                        return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.08) : Qt.alpha("#000000", 0.05);
                                    }
                                    return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.03) : Qt.alpha("#000000", 0.02);
                                }
                                border.width: 1
                                border.color: {
                                    if (isCurrent) {
                                        return Qt.alpha(itemColor, 0.38);
                                    }
                                    if (cellMouseArea.containsMouse) {
                                        return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.15) : Qt.alpha("#000000", 0.10);
                                    }
                                    return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.05) : Qt.alpha("#000000", 0.03);
                                }

                                Behavior on color { ColorAnimation { duration: 150 } }
                                Behavior on border.color { ColorAnimation { duration: 150 } }

                                MouseArea {
                                    id: cellMouseArea
                                    anchors.fill: parent
                                    hoverEnabled: true
                                }

                                // 左侧色彩标记条
                                Rectangle {
                                    anchors.left: parent.left
                                    anchors.leftMargin: 3
                                    anchors.verticalCenter: parent.verticalCenter
                                    width: 2.5
                                    height: 18
                                    radius: 1.25
                                    color: itemColor
                                }

                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.leftMargin: 9
                                    anchors.rightMargin: 4
                                    anchors.topMargin: 2
                                    anchors.bottomMargin: 2
                                    spacing: 1

                                    Text {
                                        Layout.fillWidth: true
                                        text: modelData.subjectName || modelData.title || ""
                                        font.pixelSize: 11
                                        font.bold: isCurrent
                                        elide: Text.ElideRight
                                        color: isCurrent
                                            ? (Theme.isDark() ? "#FFFFFF" : itemColor)
                                            : (Theme.isDark() ? "#EDEDED" : "#1D1D1F")
                                    }

                                    Text {
                                        Layout.fillWidth: true
                                        text: modelData.timeRange + ((modelData.location && modelData.location !== "") ? (" · " + modelData.location) : "")
                                        font.pixelSize: 9
                                        elide: Text.ElideRight
                                        color: isCurrent
                                            ? (Theme.isDark() ? "#C4C4C8" : "#48484A")
                                            : (Theme.isDark() ? "#8E8E93" : "#6E6E73")
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    // ==========================================
    // 左侧单一收回操作按钮 (苹果液态玻璃材质 + 极细 Chevron 矢量折叠微图标)
    // ==========================================
    Item {
        id: retractBtnItem
        width: 42
        height: 42
        x: -width - 12
        anchors.verticalCenter: parent.verticalCenter
        z: 999

        Rectangle {
            id: retractBtnBg
            anchors.fill: parent
            radius: 21

            color: {
                if (retractMouseArea.pressed) return Theme.isDark() ? Qt.alpha("#2E2D36", 0.90) : Qt.alpha("#E0E0E6", 0.90);
                if (retractMouseArea.containsMouse) return Theme.isDark() ? Qt.alpha("#26252C", 0.82) : Qt.alpha("#ECECF2", 0.85);
                return Theme.isDark() ? Qt.alpha("#1E1D22", 0.65 * weeklyPanelRoot.bgOpacity) : Qt.alpha("#FBFAFF", 0.70 * weeklyPanelRoot.bgOpacity);
            }

            border.width: 1
            border.color: retractMouseArea.containsMouse
                ? (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.45) : Qt.alpha("#FFFFFF", 0.95))
                : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.20) : Qt.alpha("#FFFFFF", 0.70))

            Behavior on color { ColorAnimation { duration: 150 } }
            Behavior on border.color { ColorAnimation { duration: 150 } }

            // 极细 Chevron 矢量收回微图标 (替代字符 ❯)
            Item {
                anchors.centerIn: parent
                width: 14
                height: 14

                readonly property color iconColor: retractMouseArea.containsMouse ? (Theme.accentColor || "#007AFF") : (Theme.isDark() ? "#EDEDED" : "#1D1D1F")

                Canvas {
                    id: retractIconCanvas
                    anchors.fill: parent
                    onPaint: {
                        var ctx = getContext("2d");
                        ctx.clearRect(0, 0, width, height);
                        ctx.strokeStyle = parent.iconColor;
                        ctx.lineWidth = 1.6;
                        ctx.lineCap = "round";
                        ctx.lineJoin = "round";
                        ctx.beginPath();
                        ctx.moveTo(5, 3);
                        ctx.lineTo(10, 7);
                        ctx.lineTo(5, 11);
                        ctx.stroke();
                    }

                    Connections {
                        target: retractMouseArea
                        function onContainsMouseChanged() { retractIconCanvas.requestPaint(); }
                    }
                }
            }
        }

        MouseArea {
            id: retractMouseArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: weeklyPanelRoot.requestClose()
        }

        // 提示卡 (苹果半透明胶囊气泡)
        Rectangle {
            anchors.right: parent.left
            anchors.rightMargin: 8
            anchors.verticalCenter: parent.verticalCenter
            width: retractTipText.implicitWidth + 16
            height: 24
            radius: 8
            color: Theme.isDark() ? Qt.alpha("#1E1D22", 0.85) : Qt.alpha("#FBFAFF", 0.88)
            border.width: 1
            border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.22) : Qt.alpha("#FFFFFF", 0.75)
            opacity: retractMouseArea.containsMouse ? 1.0 : 0.0
            visible: opacity > 0.01

            Behavior on opacity { NumberAnimation { duration: 160 } }

            Text {
                id: retractTipText
                anchors.centerIn: parent
                text: "收回全周大面板"
                font.pixelSize: 11
                color: Theme.isDark() ? "#EDEDED" : "#1D1D1F"
            }
        }
    }
}
