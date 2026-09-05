import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects
import RinUI
import ClassWidgets.Theme 1.0
import ClassWidgets.Easing

Item {
    id: weeklyPanelRoot

    // 尺寸设定 (适配大部分屏幕分辨率 1366~2560)
    width: Math.min(parent ? parent.width * 0.85 : 840, 840)
    height: Math.min(parent ? parent.height * 0.82 : 620, 620)

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

    // 主面板轻量级柔和阴影 (开启硬件缓存与快速渲染模式)
    DropShadow {
        anchors.fill: panelBackground
        horizontalOffset: weeklyPanelRoot.isLeftEdge ? 3 : -3
        verticalOffset: 6
        radius: 14
        samples: 9
        cached: true
        fast: true
        color: Theme.isDark() ? Qt.alpha("#000000", 0.55) : Qt.alpha("#000000", 0.18)
        source: panelBackground
    }

    // 主面板背景 (Fluent 磨砂胶囊)
    Rectangle {
        id: panelBackground
        anchors.fill: parent
        radius: weeklyPanelRoot.cornerRadius
        color: Theme.isDark()
            ? Qt.alpha("#1A191E", 0.95 * weeklyPanelRoot.bgOpacity)
            : Qt.alpha("#FBFBFF", 0.96 * weeklyPanelRoot.bgOpacity)

        // 对齐主程序 Widget 的微光渐变高光边框
        Item {
            anchors.fill: parent
            Rectangle {
                id: panelBorderRect
                anchors.fill: parent
                radius: panelBackground.radius
                layer.enabled: true
                layer.effect: LinearGradient {
                    start: Qt.point(0, 0)
                    end: Qt.point(width, height)
                    gradient: Gradient {
                        GradientStop {
                            position: 0.0
                            color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.35) : Qt.alpha("#000000", 0.16)
                        }
                        GradientStop {
                            position: 0.3
                            color: Theme.isDark() ? Qt.alpha(Theme.accentColor || "#4A90E2", 0.20) : Qt.alpha("#000000", 0.04)
                        }
                        GradientStop {
                            position: 0.7
                            color: Qt.alpha("#FFFFFF", 0.0)
                        }
                        GradientStop {
                            position: 1.0
                            color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.25) : Qt.alpha("#000000", 0.10)
                        }
                    }
                }
            }
            layer.enabled: true
            layer.effect: OpacityMask {
                maskSource: Rectangle {
                    width: panelBorderRect.width
                    height: panelBorderRect.height
                    radius: panelBorderRect.radius
                    color: "transparent"
                    border.width: 1
                }
            }
            opacity: Math.min(1.0, weeklyPanelRoot.bgOpacity * 1.2)
        }
    }

    // 拦截点击避免穿透到背景外部收回区域
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
    }

    // 面板内部主布局
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 18
        spacing: 12

        // ==========================================
        // 顶部标题栏与关闭
        // ==========================================
        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 36
            spacing: 10

            Rectangle {
                width: 6
                height: 18
                radius: 3
                color: Theme.accentColor || "#4A90E2"
            }

            Text {
                text: "全周课表矩阵"
                font.pixelSize: 16
                font.bold: true
                color: Theme.isDark() ? "#FFFFFF" : "#1A1A1A"
            }

            Rectangle {
                radius: 10
                height: 20
                width: weekBadgeText.implicitWidth + 16
                color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.08) : Qt.alpha("#000000", 0.06)

                Text {
                    id: weekBadgeText
                    anchors.centerIn: parent
                    text: {
                        var w = AppCentral.scheduleRuntime ? AppCentral.scheduleRuntime.currentWeek : 1;
                        return "第 " + w + " 周";
                    }
                    font.pixelSize: 11
                    color: Theme.isDark() ? "#BBBBBB" : "#555555"
                }
            }

            Item { Layout.fillWidth: true }

            // 顶部关闭小按钮
            Rectangle {
                width: 28
                height: 28
                radius: 14
                color: closeHoverArea.containsMouse
                    ? (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.15) : Qt.alpha("#000000", 0.10))
                    : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.06) : Qt.alpha("#000000", 0.04))

                Text {
                    anchors.centerIn: parent
                    text: "✕"
                    font.pixelSize: 13
                    color: Theme.isDark() ? "#CCCCCC" : "#555555"
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

        // 分割线
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
            color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.10) : Qt.alpha("#000000", 0.08)
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

                // 单天纵向列
                Rectangle {
                    id: dayColumnRect
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    radius: 12

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

                    color: isToday
                        ? (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.06) : Qt.alpha(Theme.accentColor || "#4A90E2", 0.08))
                        : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.02) : Qt.alpha("#000000", 0.02))
                    border.width: isToday ? 1.5 : 1
                    border.color: isToday
                        ? (Theme.accentColor || "#4A90E2")
                        : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.08) : Qt.alpha("#000000", 0.06))

                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 6
                        spacing: 6

                        // 星期标头
                        Rectangle {
                            Layout.fillWidth: true
                            Layout.preferredHeight: 28
                            radius: 8
                            color: dayColumnRect.isToday
                                ? (Theme.accentColor || "#4A90E2")
                                : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.06) : Qt.alpha("#000000", 0.05))

                            RowLayout {
                                anchors.centerIn: parent
                                spacing: 4

                                Text {
                                    text: ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][index]
                                    font.pixelSize: 12
                                    font.bold: dayColumnRect.isToday
                                    color: dayColumnRect.isToday
                                        ? "#FFFFFF"
                                        : (Theme.isDark() ? "#E0E0E0" : "#333333")
                                }

                                Rectangle {
                                    visible: dayColumnRect.isToday
                                    width: 4
                                    height: 4
                                    radius: 2
                                    color: "#FFFFFF"
                                }
                            }
                        }

                        // 该天课程列表
                        ListView {
                            id: dayEntriesList
                            Layout.fillWidth: true
                            Layout.fillHeight: true
                            clip: true
                            spacing: 5
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
                                height: 50
                                radius: 8

                                readonly property bool isCurrent: modelData.isCurrent || false
                                readonly property color itemColor: modelData.color || "#4A90E2"

                                color: {
                                    if (isCurrent) {
                                        return Theme.isDark() ? Qt.alpha(itemColor, 0.30) : Qt.alpha(itemColor, 0.18);
                                    }
                                    if (cellMouseArea.containsMouse) {
                                        return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.10) : Qt.alpha("#000000", 0.06);
                                    }
                                    return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.04) : Qt.alpha("#000000", 0.03);
                                }
                                border.width: isCurrent ? 1.5 : (cellMouseArea.containsMouse ? 1 : 0)
                                border.color: isCurrent ? itemColor : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.20) : Qt.alpha("#000000", 0.10))

                                MouseArea {
                                    id: cellMouseArea
                                    anchors.fill: parent
                                    hoverEnabled: true
                                }

                                ColumnLayout {
                                    anchors.fill: parent
                                    anchors.margins: 4
                                    spacing: 1

                                    Text {
                                        Layout.fillWidth: true
                                        text: modelData.subjectName || modelData.title || ""
                                        font.pixelSize: 11
                                        font.bold: isCurrent
                                        elide: Text.ElideRight
                                        color: isCurrent
                                            ? (Theme.isDark() ? "#FFFFFF" : itemColor)
                                            : (Theme.isDark() ? "#E5E5E5" : "#222222")
                                    }

                                    Text {
                                        Layout.fillWidth: true
                                        text: modelData.timeRange || ""
                                        font.pixelSize: 9
                                        elide: Text.ElideRight
                                        color: Theme.isDark() ? "#999999" : "#666666"
                                    }

                                    Text {
                                        Layout.fillWidth: true
                                        text: modelData.location || ""
                                        font.pixelSize: 9
                                        elide: Text.ElideRight
                                        color: Theme.isDark() ? "#888888" : "#888888"
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
    // 左侧单一收回操作按钮 (R3 规范)
    // 展开状态下左侧操作按钮转为单一收回按钮
    // ==========================================
    Item {
        id: retractBtnItem
        width: 42
        height: 42
        x: -width - 12
        anchors.verticalCenter: parent.verticalCenter
        z: 999

        DropShadow {
            anchors.fill: retractBtnBg
            horizontalOffset: -2
            verticalOffset: 4
            radius: 8
            samples: 8
            cached: true
            fast: true
            color: Theme.isDark() ? Qt.alpha("#000000", 0.45) : Qt.alpha("#000000", 0.15)
            source: retractBtnBg
        }

        Rectangle {
            id: retractBtnBg
            anchors.fill: parent
            radius: 21
            color: {
                if (retractMouseArea.pressed) {
                    return Theme.isDark() ? Qt.alpha("#3A3840", 0.95) : Qt.alpha("#E5E5EA", 0.95);
                }
                if (retractMouseArea.containsMouse) {
                    return Theme.isDark() ? Qt.alpha("#2E2D34", 0.92) : Qt.alpha("#F2F2F7", 0.95);
                }
                return Theme.isDark() ? Qt.alpha("#212026", 0.88) : Qt.alpha("#FCFBFF", 0.92);
            }
            border.width: 1
            border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.22) : Qt.alpha("#000000", 0.10)

            // 向右收回图标
            Text {
                anchors.centerIn: parent
                text: "❯"
                font.pixelSize: 16
                color: retractMouseArea.containsMouse ? (Theme.accentColor || "#4A90E2") : (Theme.isDark() ? "#EDEDED" : "#333333")
            }
        }

        MouseArea {
            id: retractMouseArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: weeklyPanelRoot.requestClose()
        }

        // 提示卡
        Rectangle {
            anchors.right: parent.left
            anchors.rightMargin: 8
            anchors.verticalCenter: parent.verticalCenter
            width: retractTipText.implicitWidth + 14
            height: 24
            radius: 6
            color: Theme.isDark() ? "#2D2C33" : "#F7F7F7"
            border.width: 1
            border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.15) : Qt.alpha("#000000", 0.08)
            opacity: retractMouseArea.containsMouse ? 1.0 : 0.0
            visible: opacity > 0.01

            Behavior on opacity { NumberAnimation { duration: 160 } }

            Text {
                id: retractTipText
                anchors.centerIn: parent
                text: "收回全周大面板"
                font.pixelSize: 11
                color: Theme.isDark() ? "#EDEDED" : "#222222"
            }
        }
    }
}
