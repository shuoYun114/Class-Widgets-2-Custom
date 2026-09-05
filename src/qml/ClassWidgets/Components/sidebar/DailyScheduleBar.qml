import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects
import RinUI
import ClassWidgets.Theme 1.0
import ClassWidgets.Easing

Item {
    id: dailyBarRoot

    // 默认宽度与外层约束
    width: 160
    height: Math.min(parent ? parent.height * 0.78 : 600, Math.max(280, contentLayout.implicitHeight + 36))

    // 状态与向外暴露属性
    property bool barHovered: barMouseArea.containsMouse || bubbleMouseArea.containsMouse
    property bool hasActiveBubble: bubbleCard.opacity > 0.05
    property var activeEntry: null

    // 暴露有效交互区域 (相对于当前组件) 给遮罩计算
    function getBarRect() {
        return [x, y, width, height];
    }

    function getBubbleRect() {
        if (!hasActiveBubble) return [0, 0, 0, 0];
        return [bubbleCard.x, bubbleCard.y, bubbleCard.width, bubbleCard.height];
    }

    // 主体阴影 (轻量级硬件缓存快速渲染)
    DropShadow {
        anchors.fill: capsuleBackground
        horizontalOffset: -2
        verticalOffset: 4
        radius: 10
        samples: 8
        cached: true
        fast: true
        color: Theme.isDark() ? Qt.alpha("#000000", 0.45) : Qt.alpha("#000000", 0.15)
        source: capsuleBackground
    }

    // 竖条胶囊背景
    Rectangle {
        id: capsuleBackground
        anchors.fill: parent
        radius: 20
        color: Theme.isDark() ? Qt.alpha("#1C1B20", 0.82) : Qt.alpha("#FCFBFF", 0.90)

        // 渐变高光边框 (Fluent 规范)
        Rectangle {
            id: borderHighlight
            anchors.fill: parent
            radius: parent.radius
            color: "transparent"
            border.width: 1
            border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.22) : Qt.alpha("#000000", 0.08)
        }
    }

    // 整体鼠标悬浮监听
    MouseArea {
        id: barMouseArea
        anchors.fill: parent
        hoverEnabled: true
        acceptedButtons: Qt.NoButton
    }

    // 内部垂直流
    ColumnLayout {
        id: contentLayout
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        // 顶部小标题栏
        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: 32

            RowLayout {
                anchors.fill: parent
                spacing: 6

                Rectangle {
                    width: 6
                    height: 14
                    radius: 3
                    color: Theme.accentColor || "#4A90E2"
                }

                Text {
                    text: {
                        var days = ["", "周一", "周二", "周三", "周四", "周五", "周六", "周日"];
                        var weekday = AppCentral.scheduleRuntime ? AppCentral.scheduleRuntime.currentDayOfWeek : 1;
                        var dayStr = (weekday >= 1 && weekday <= 7) ? days[weekday] : "今日";
                        return dayStr + " 课表";
                    }
                    font.pixelSize: 12
                    font.bold: true
                    color: Theme.isDark() ? "#F3F3F3" : "#1F1F1F"
                }

                Item { Layout.fillWidth: true }

                Text {
                    text: {
                        var scheduleList = AppCentral.scheduleRuntime ? AppCentral.scheduleRuntime.sidebarDaySchedule : [];
                        return scheduleList.length > 0 ? (scheduleList.length + " 节") : "";
                    }
                    font.pixelSize: 10
                    color: Theme.isDark() ? "#8C8C8C" : "#767676"
                }
            }
        }

        // 分隔微线
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
            color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.08) : Qt.alpha("#000000", 0.06)
        }

        // 课程平滑滚动列表
        ListView {
            id: scheduleListView
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true
            spacing: 6
            boundsBehavior: Flickable.StopAtBounds

            model: AppCentral.scheduleRuntime ? AppCentral.scheduleRuntime.sidebarDaySchedule : []

            // 空课表占位提示
            Item {
                anchors.centerIn: parent
                width: parent.width - 16
                height: 100
                visible: scheduleListView.count === 0

                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 6

                    Text {
                        Layout.alignment: Qt.AlignHCenter
                        text: "☕"
                        font.pixelSize: 22
                    }

                    Text {
                        Layout.alignment: Qt.AlignHCenter
                        text: "今日暂无课程"
                        font.pixelSize: 11
                        color: Theme.isDark() ? "#8C8C8C" : "#767676"
                    }
                }
            }

            delegate: Item {
                id: entryDelegate
                width: scheduleListView.width
                height: 52

                readonly property bool isCurrent: modelData.isCurrent || false
                readonly property color itemColor: modelData.color || "#4A90E2"

                // 悬浮交互
                MouseArea {
                    id: itemHoverArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor

                    onEntered: {
                        dailyBarRoot.activeEntry = modelData;
                        // 计算气泡在 dailyBarRoot 上的相对 y 坐标
                        var mapPos = entryDelegate.mapToItem(dailyBarRoot, 0, 0);
                        bubbleCard.targetY = Math.max(10, Math.min(dailyBarRoot.height - bubbleCard.height - 10, mapPos.y - 8));
                        bubbleHideTimer.stop();
                        bubbleCard.showBubble = true;
                    }

                    onExited: {
                        bubbleHideTimer.restart();
                    }
                }

                // 卡片本体背景
                Rectangle {
                    anchors.fill: parent
                    radius: 10
                    color: {
                        if (isCurrent) {
                            return Theme.isDark() ? Qt.alpha(itemColor, 0.24) : Qt.alpha(itemColor, 0.16);
                        }
                        if (itemHoverArea.containsMouse) {
                            return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.08) : Qt.alpha("#000000", 0.05);
                        }
                        return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.03) : Qt.alpha("#000000", 0.02);
                    }
                    border.width: isCurrent ? 1.5 : (itemHoverArea.containsMouse ? 1 : 0)
                    border.color: isCurrent ? itemColor : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.2) : Qt.alpha("#000000", 0.1))

                    Behavior on color {
                        ColorAnimation { duration: 180 }
                    }

                    // 左侧色彩标记条
                    Rectangle {
                        anchors.left: parent.left
                        anchors.leftMargin: 4
                        anchors.verticalCenter: parent.verticalCenter
                        width: 3.5
                        height: 24
                        radius: 2
                        color: itemColor
                    }

                    // 文本内容
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 14
                        anchors.rightMargin: 8
                        anchors.topMargin: 6
                        anchors.bottomMargin: 6
                        spacing: 2

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 4

                            Text {
                                Layout.fillWidth: true
                                text: modelData.subjectName || modelData.title || "课程"
                                font.pixelSize: 12
                                font.bold: isCurrent
                                elide: Text.ElideRight
                                color: isCurrent ? (Theme.isDark() ? "#FFFFFF" : itemColor) : (Theme.isDark() ? "#EDEDED" : "#1A1A1A")
                            }

                            // 当前课程指示小红点或徽标
                            Rectangle {
                                visible: isCurrent
                                width: 6
                                height: 6
                                radius: 3
                                color: itemColor
                            }
                        }

                        Text {
                            text: modelData.timeRange || (modelData.startTime + " - " + modelData.endTime)
                            font.pixelSize: 10
                            color: isCurrent ? (Theme.isDark() ? "#D0D0D0" : "#444444") : (Theme.isDark() ? "#8C8C8C" : "#767676")
                        }
                    }

                    // 当前课程底部细进度条
                    Rectangle {
                        visible: isCurrent
                        anchors.bottom: parent.bottom
                        anchors.left: parent.left
                        anchors.leftMargin: 4
                        height: 2
                        radius: 1
                        width: Math.max(0, (parent.width - 8) * Math.min(1.0, Math.max(0.0, modelData.progress || 0.0)))
                        color: itemColor

                        Behavior on width {
                            NumberAnimation { duration: 300 }
                        }
                    }
                }
            }
        }
    }

    // 气泡延时消失计时器 (150ms 缓冲防抖)
    Timer {
        id: bubbleHideTimer
        interval: 150
        repeat: false
        onTriggered: {
            if (!bubbleMouseArea.containsMouse) {
                bubbleCard.showBubble = false;
            }
        }
    }

    // ==========================================
    // 课程详情悬浮气泡卡片 (Bubble Popover)
    // ==========================================
    Item {
        id: bubbleCard
        property real targetY: 20
        property bool showBubble: false

        width: 190
        height: bubbleInnerLayout.implicitHeight + 24
        x: -width - 12
        y: targetY
        z: 999

        // 进出平滑动画 (使用纯 GPU Translate 矩阵位移与淡入，消除文字重采样与模糊卡顿)
        opacity: showBubble ? 1.0 : 0.0
        visible: opacity > 0.01

        Behavior on opacity {
            NumberAnimation { duration: 180; easing.type: Easing.OutQuad }
        }

        transform: Translate {
            x: bubbleCard.showBubble ? 0 : 8
            Behavior on x {
                NumberAnimation { duration: 180; easing.type: Easing.OutCubic }
            }
        }

        Behavior on y {
            NumberAnimation { duration: 180; easing.type: Easing.OutCubic }
        }

        // 气泡卡片阴影 (轻量级硬件缓存快速渲染)
        DropShadow {
            anchors.fill: bubbleBg
            horizontalOffset: -2
            verticalOffset: 4
            radius: 10
            samples: 8
            cached: true
            fast: true
            color: Theme.isDark() ? Qt.alpha("#000000", 0.50) : Qt.alpha("#000000", 0.18)
            source: bubbleBg
        }

        // 气泡卡片背景
        Rectangle {
            id: bubbleBg
            anchors.fill: parent
            radius: 16
            color: Theme.isDark() ? Qt.alpha("#212026", 0.94) : Qt.alpha("#FFFFFF", 0.96)
            border.width: 1
            border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.20) : Qt.alpha("#000000", 0.10)
        }

        MouseArea {
            id: bubbleMouseArea
            anchors.fill: parent
            hoverEnabled: true
            onEntered: bubbleHideTimer.stop()
            onExited: bubbleHideTimer.restart()
        }

        ColumnLayout {
            id: bubbleInnerLayout
            anchors.fill: parent
            anchors.margins: 12
            spacing: 8

            // 标题行
            RowLayout {
                Layout.fillWidth: true
                spacing: 6

                Rectangle {
                    width: 8
                    height: 8
                    radius: 4
                    color: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.color || "#4A90E2") : "#4A90E2"
                }

                Text {
                    Layout.fillWidth: true
                    text: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.subjectName || dailyBarRoot.activeEntry.title || "课程详情") : ""
                    font.pixelSize: 13
                    font.bold: true
                    elide: Text.ElideRight
                    color: Theme.isDark() ? "#FFFFFF" : "#111111"
                }
            }

            // 分割线
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.08) : Qt.alpha("#000000", 0.06)
            }

            // 时间范围
            RowLayout {
                Layout.fillWidth: true
                spacing: 6

                Text {
                    text: "🕒"
                    font.pixelSize: 11
                }
                Text {
                    Layout.fillWidth: true
                    text: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.timeRange || "") : ""
                    font.pixelSize: 11
                    color: Theme.isDark() ? "#CCCCCC" : "#444444"
                }
            }

            // 教室地点
            RowLayout {
                Layout.fillWidth: true
                spacing: 6

                Text {
                    text: "📍"
                    font.pixelSize: 11
                }
                Text {
                    Layout.fillWidth: true
                    text: (dailyBarRoot.activeEntry && dailyBarRoot.activeEntry.location) ? dailyBarRoot.activeEntry.location : "无固定教室"
                    font.pixelSize: 11
                    elide: Text.ElideRight
                    color: Theme.isDark() ? "#CCCCCC" : "#444444"
                }
            }

            // 授课教师
            RowLayout {
                Layout.fillWidth: true
                spacing: 6

                Text {
                    text: "👤"
                    font.pixelSize: 11
                }
                Text {
                    Layout.fillWidth: true
                    text: (dailyBarRoot.activeEntry && dailyBarRoot.activeEntry.teacher) ? dailyBarRoot.activeEntry.teacher : "任课老师"
                    font.pixelSize: 11
                    elide: Text.ElideRight
                    color: Theme.isDark() ? "#CCCCCC" : "#444444"
                }
            }

            // 当前状态标签
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 22
                radius: 6
                visible: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.isCurrent || false) : false
                color: Qt.alpha(dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.color || "#4A90E2") : "#4A90E2", 0.20)

                RowLayout {
                    anchors.centerIn: parent
                    spacing: 4

                    Text {
                        text: "正在进行中 (" + Math.round((dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.progress || 0) : 0) * 100) + "%)"
                        font.pixelSize: 10
                        font.bold: true
                        color: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.color || "#4A90E2") : "#4A90E2"
                    }
                }
            }
        }
    }
}
