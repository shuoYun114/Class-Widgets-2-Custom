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
    property var scheduleList: (AppCentral.scheduleRuntime && AppCentral.scheduleRuntime.sidebarDaySchedule)
        ? AppCentral.scheduleRuntime.sidebarDaySchedule
        : []
    readonly property int courseCount: scheduleList ? scheduleList.length : 0
    readonly property real listTotalHeight: Math.max(1, courseCount) * 42 + Math.max(0, courseCount - 1) * 4
    readonly property real headerTotalHeight: 72 // 顶部栏(32)+分割线(1)+外边距(24)+间距(15)
    readonly property real idealTotalHeight: courseCount === 0 ? 180 : (headerTotalHeight + listTotalHeight)
    height: Math.min(parent ? parent.height * 0.85 : 680, Math.max(200, idealTotalHeight))

    // 状态与向外暴露属性
    property bool barHovered: barMouseArea.containsMouse || bubbleMouseArea.containsMouse
    property bool hasActiveBubble: bubbleCard.opacity > 0.05
    property var activeEntry: null

    // 自定义外观与定位属性 (由父级 ScheduleSidebar 传入)
    property bool isLeftEdge: false
    property real cornerRadius: 22
    property real bgOpacity: 1.0

    // 暴露有效交互区域 (相对于当前组件) 给遮罩计算
    function getBarRect() {
        return [x, y, width, height];
    }

    function getBubbleRect() {
        if (!hasActiveBubble) return [0, 0, 0, 0];
        return [bubbleCard.x, bubbleCard.y, bubbleCard.width, bubbleCard.height];
    }

    // ==========================================
    // 苹果液态玻璃质感背景 (Liquid Glass Material)
    // 渐变光影 + 1px Specular Rim 物理微高光边框 + 顶层微折射反光
    // ==========================================
    Rectangle {
        id: capsuleBackground
        anchors.fill: parent
        radius: dailyBarRoot.cornerRadius

        gradient: Gradient {
            GradientStop {
                position: 0.0
                color: Theme.isDark()
                    ? Qt.alpha("#26252E", 0.88 * dailyBarRoot.bgOpacity)
                    : Qt.alpha("#FFFFFF", 0.88 * dailyBarRoot.bgOpacity)
            }
            GradientStop {
                position: 1.0
                color: Theme.isDark()
                    ? Qt.alpha("#17161D", 0.82 * dailyBarRoot.bgOpacity)
                    : Qt.alpha("#ECECF2", 0.84 * dailyBarRoot.bgOpacity)
            }
        }

        // 物理微高光边缘折射 (Specular Rim Light)
        border.width: 1
        border.color: Theme.isDark()
            ? Qt.alpha("#FFFFFF", 0.16)
            : Qt.alpha("#FFFFFF", 0.70)

        // 顶层微弱反光线 (模拟玻璃受光面倒角)
        Rectangle {
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: 1
            height: 1
            radius: dailyBarRoot.cornerRadius
            color: Theme.isDark()
                ? Qt.alpha("#FFFFFF", 0.12)
                : Qt.alpha("#FFFFFF", 0.90)
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

        // 顶部极简标题栏
        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: 28

            RowLayout {
                anchors.fill: parent
                spacing: 6

                // 极简微光小点
                Rectangle {
                    width: 4
                    height: 4
                    radius: 2
                    color: Theme.accentColor || "#007AFF"
                }

                Text {
                    text: {
                        var days = ["", "周一", "周二", "周三", "周四", "周五", "周六", "周日"];
                        var weekday = AppCentral.scheduleRuntime ? AppCentral.scheduleRuntime.currentDayOfWeek : 1;
                        var dayStr = (weekday >= 1 && weekday <= 7) ? days[weekday] : "今日";
                        return dayStr + "日程";
                    }
                    font.pixelSize: 12
                    font.bold: true
                    color: Theme.isDark() ? "#F5F5F7" : "#1D1D1F"
                }

                Item { Layout.fillWidth: true }

                // 极简微胶囊：课程节数
                Rectangle {
                    visible: dailyBarRoot.courseCount > 0
                    height: 18
                    width: countBadgeText.implicitWidth + 12
                    radius: 9
                    color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.07) : Qt.alpha("#000000", 0.05)

                    Text {
                        id: countBadgeText
                        anchors.centerIn: parent
                        text: dailyBarRoot.courseCount + " 节"
                        font.pixelSize: 10
                        color: Theme.isDark() ? "#9898A0" : "#6E6E73"
                    }
                }
            }
        }

        // 分隔微线 (极细半透明)
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
            spacing: 4
            boundsBehavior: Flickable.StopAtBounds

            model: dailyBarRoot.scheduleList

            // 空课表占位提示 (去除 emoji，采用极简现代排版)
            Item {
                anchors.centerIn: parent
                width: parent.width - 16
                height: 100
                visible: dailyBarRoot.courseCount === 0

                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 6

                    Rectangle {
                        Layout.alignment: Qt.AlignHCenter
                        width: 16
                        height: 2
                        radius: 1
                        color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.20) : Qt.alpha("#000000", 0.15)
                    }

                    Text {
                        Layout.alignment: Qt.AlignHCenter
                        text: "今日暂无课程安排"
                        font.pixelSize: 11
                        color: Theme.isDark() ? "#707078" : "#8E8E93"
                    }
                }
            }

            delegate: Item {
                id: entryDelegate
                width: scheduleListView.width
                height: 42

                readonly property bool isCurrent: modelData.isCurrent || false
                readonly property color itemColor: modelData.color || "#007AFF"

                // 悬浮交互
                MouseArea {
                    id: itemHoverArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor

                    onEntered: {
                        dailyBarRoot.activeEntry = modelData;
                        var mapPos = entryDelegate.mapToItem(dailyBarRoot, 0, 0);
                        bubbleCard.targetY = Math.max(10, Math.min(dailyBarRoot.height - bubbleCard.height - 10, mapPos.y - 8));
                        bubbleHideTimer.stop();
                        bubbleCard.showBubble = true;
                    }

                    onExited: {
                        bubbleHideTimer.restart();
                    }
                }

                // 卡片本体背景 (苹果内嵌毛玻璃卡片质感)
                Rectangle {
                    anchors.fill: parent
                    radius: 7
                    color: {
                        if (isCurrent) {
                            return Theme.isDark() ? Qt.alpha(itemColor, 0.18) : Qt.alpha(itemColor, 0.12);
                        }
                        if (itemHoverArea.containsMouse) {
                            return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.08) : Qt.alpha("#000000", 0.06);
                        }
                        return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.04) : Qt.alpha("#000000", 0.03);
                    }
                    border.width: 1
                    border.color: {
                        if (isCurrent) {
                            return Qt.alpha(itemColor, 0.38);
                        }
                        if (itemHoverArea.containsMouse) {
                            return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.16) : Qt.alpha("#000000", 0.12);
                        }
                        return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.06) : Qt.alpha("#000000", 0.04);
                    }

                    Behavior on color {
                        ColorAnimation { duration: 160 }
                    }
                    Behavior on border.color {
                        ColorAnimation { duration: 160 }
                    }

                    // 左侧色彩轻标记微条
                    Rectangle {
                        anchors.left: parent.left
                        anchors.leftMargin: 3.5
                        anchors.verticalCenter: parent.verticalCenter
                        width: 2.5
                        height: 18
                        radius: 1.25
                        color: itemColor
                    }

                    // 文本内容
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 11
                        anchors.rightMargin: 6
                        anchors.topMargin: 4
                        anchors.bottomMargin: 4
                        spacing: 1

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 4

                            Text {
                                Layout.fillWidth: true
                                text: modelData.subjectName || modelData.title || "课程"
                                font.pixelSize: 11
                                font.bold: isCurrent
                                elide: Text.ElideRight
                                color: isCurrent
                                    ? (Theme.isDark() ? "#FFFFFF" : itemColor)
                                    : (Theme.isDark() ? "#EDEDED" : "#1D1D1F")
                            }

                            // 正在进行课程极简微光小点
                            Rectangle {
                                visible: isCurrent
                                width: 4
                                height: 4
                                radius: 2
                                color: itemColor
                            }
                        }

                        Text {
                            text: modelData.timeRange || (modelData.startTime + " - " + modelData.endTime)
                            font.pixelSize: 10
                            color: isCurrent
                                ? (Theme.isDark() ? "#C4C4C8" : "#48484A")
                                : (Theme.isDark() ? "#8E8E93" : "#6E6E73")
                        }
                    }

                    // 当前课程底部细微进度条 (1.5px 极简线条)
                    Rectangle {
                        visible: isCurrent
                        anchors.bottom: parent.bottom
                        anchors.left: parent.left
                        anchors.leftMargin: 4
                        anchors.rightMargin: 4
                        height: 1.5
                        radius: 1
                        width: Math.max(0, (parent.width - 8) * Math.min(1.0, Math.max(0.0, modelData.progress || 0.0)))
                        color: itemColor

                        Behavior on width {
                            NumberAnimation { duration: 250 }
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
    // 课程详情悬浮气泡卡片 (Apple Liquid Glass Popover)
    // 彻底去除 Emoji，采用锁屏通知/动态岛级极简排版
    // ==========================================
    Item {
        id: bubbleCard
        property real targetY: 20
        property bool showBubble: false

        width: 196
        height: bubbleInnerLayout.implicitHeight + 24
        x: dailyBarRoot.isLeftEdge ? (dailyBarRoot.width + 10) : (-width - 10)
        y: targetY
        z: 999

        // 进出平滑动画 (纯 GPU Translate 位移与淡入)
        opacity: showBubble ? 1.0 : 0.0
        visible: opacity > 0.01

        Behavior on opacity {
            NumberAnimation { duration: 160; easing.type: Easing.OutQuad }
        }

        transform: Translate {
            x: bubbleCard.showBubble ? 0 : (dailyBarRoot.isLeftEdge ? -6 : 6)
            Behavior on x {
                NumberAnimation { duration: 160; easing.type: Easing.OutCubic }
            }
        }

        Behavior on y {
            NumberAnimation { duration: 160; easing.type: Easing.OutCubic }
        }

        // 气泡卡片背景 (苹果液态毛玻璃大卡片)
        Rectangle {
            id: bubbleBg
            anchors.fill: parent
            radius: Math.max(10, dailyBarRoot.cornerRadius - 4)

            gradient: Gradient {
                GradientStop {
                    position: 0.0
                    color: Theme.isDark()
                        ? Qt.alpha("#2A2933", 0.94 * dailyBarRoot.bgOpacity)
                        : Qt.alpha("#FFFFFF", 0.96 * dailyBarRoot.bgOpacity)
                }
                GradientStop {
                    position: 1.0
                    color: Theme.isDark()
                        ? Qt.alpha("#1D1C24", 0.92 * dailyBarRoot.bgOpacity)
                        : Qt.alpha("#F5F5FA", 0.94 * dailyBarRoot.bgOpacity)
                }
            }

            border.width: 1
            border.color: Theme.isDark()
                ? Qt.alpha("#FFFFFF", 0.20)
                : Qt.alpha("#FFFFFF", 0.75)

            // 顶层微光折射
            Rectangle {
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.margins: 1
                height: 1
                radius: parent.radius
                color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.15) : Qt.alpha("#FFFFFF", 0.95)
            }
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

            // 标题行与状态胶囊
            RowLayout {
                Layout.fillWidth: true
                spacing: 6

                Rectangle {
                    width: 6
                    height: 6
                    radius: 3
                    color: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.color || "#007AFF") : "#007AFF"
                }

                Text {
                    Layout.fillWidth: true
                    text: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.subjectName || dailyBarRoot.activeEntry.title || "课程详情") : ""
                    font.pixelSize: 12
                    font.bold: true
                    elide: Text.ElideRight
                    color: Theme.isDark() ? "#FFFFFF" : "#1D1D1F"
                }

                // 正在进行中小徽标
                Rectangle {
                    visible: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.isCurrent || false) : false
                    height: 16
                    width: statusTagText.implicitWidth + 10
                    radius: 8
                    color: Qt.alpha(dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.color || "#007AFF") : "#007AFF", 0.18)

                    Text {
                        id: statusTagText
                        anchors.centerIn: parent
                        text: "进行中"
                        font.pixelSize: 9
                        font.bold: true
                        color: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.color || "#007AFF") : "#007AFF"
                    }
                }
            }

            // 分割微线
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.08) : Qt.alpha("#000000", 0.06)
            }

            // 时间信息 (无 Emoji，极简两列)
            RowLayout {
                Layout.fillWidth: true
                spacing: 8

                Text {
                    text: "时间"
                    font.pixelSize: 10
                    color: Theme.isDark() ? "#707078" : "#8E8E93"
                }

                Text {
                    Layout.fillWidth: true
                    text: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.timeRange || "") : ""
                    font.pixelSize: 11
                    color: Theme.isDark() ? "#D0D0D4" : "#3A3A3C"
                }
            }

            // 地点信息 (无 Emoji)
            RowLayout {
                Layout.fillWidth: true
                spacing: 8

                Text {
                    text: "教室"
                    font.pixelSize: 10
                    color: Theme.isDark() ? "#707078" : "#8E8E93"
                }

                Text {
                    Layout.fillWidth: true
                    text: (dailyBarRoot.activeEntry && dailyBarRoot.activeEntry.location) ? dailyBarRoot.activeEntry.location : "未指定"
                    font.pixelSize: 11
                    elide: Text.ElideRight
                    color: Theme.isDark() ? "#D0D0D4" : "#3A3A3C"
                }
            }

            // 教师信息 (无 Emoji)
            RowLayout {
                Layout.fillWidth: true
                spacing: 8

                Text {
                    text: "教师"
                    font.pixelSize: 10
                    color: Theme.isDark() ? "#707078" : "#8E8E93"
                }

                Text {
                    Layout.fillWidth: true
                    text: (dailyBarRoot.activeEntry && dailyBarRoot.activeEntry.teacher) ? dailyBarRoot.activeEntry.teacher : "未指定"
                    font.pixelSize: 11
                    elide: Text.ElideRight
                    color: Theme.isDark() ? "#D0D0D4" : "#3A3A3C"
                }
            }

            // 正在进行时显示进度条 (极简细腻)
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 4
                visible: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.isCurrent || false) : false

                RowLayout {
                    Layout.fillWidth: true

                    Text {
                        text: "已进行"
                        font.pixelSize: 10
                        color: Theme.isDark() ? "#707078" : "#8E8E93"
                    }

                    Item { Layout.fillWidth: true }

                    Text {
                        text: Math.round((dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.progress || 0) : 0) * 100) + "%"
                        font.pixelSize: 10
                        font.bold: true
                        color: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.color || "#007AFF") : "#007AFF"
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    height: 3
                    radius: 1.5
                    color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.08) : Qt.alpha("#000000", 0.06)

                    Rectangle {
                        anchors.left: parent.left
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        radius: 1.5
                        width: Math.max(0, parent.width * Math.min(1.0, Math.max(0.0, (dailyBarRoot.activeEntry ? dailyBarRoot.activeEntry.progress : 0) || 0.0)))
                        color: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.color || "#007AFF") : "#007AFF"
                    }
                }
            }
        }
    }
}
