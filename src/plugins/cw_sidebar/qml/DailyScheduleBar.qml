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
    readonly property bool hasActiveBubble: bubbleCard.showBubble && (bubbleCard.opacity > 0.05)
    readonly property real bubbleCardX: bubbleCard.x
    readonly property real bubbleCardY: bubbleCard.y
    readonly property real bubbleCardW: bubbleCard.width
    readonly property real bubbleCardH: bubbleCard.height
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
    // 苹果液态玻璃质感背景 (Liquid Glass Material - 对齐主程序 Widget.qml)
    // 65% 高透光率 + FastBlur 64px 内部柔和流光漫反射 + 对角线渐变物理微高光边框
    // ==========================================
    Rectangle {
        id: capsuleBackground
        anchors.fill: parent
        radius: dailyBarRoot.cornerRadius
        color: Theme.isDark()
            ? Qt.alpha("#1E1D22", 0.65 * dailyBarRoot.bgOpacity)
            : Qt.alpha("#FBFAFF", 0.70 * dailyBarRoot.bgOpacity)
    }

    // 内部流光微发光层 (Lighting Effect - FastBlur 内部弥散漫反射，营造温润通透感)
    Item {
        anchors.fill: parent
        clip: true

        Rectangle {
            id: ambientGlow
            anchors.centerIn: parent
            width: Math.min(parent.width, parent.height) * 0.75
            height: width
            radius: width / 2
            color: Theme.accentColor || "#4099b2"
            opacity: (Configs.data && Configs.data.preferences && Configs.data.preferences.lighting_effect !== false) ? 0.35 : 0.0
            visible: opacity > 0.01

            layer.enabled: true
            layer.effect: FastBlur {
                anchors.fill: ambientGlow
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
            radius: capsuleBackground.radius
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
        anchors.margins: 14
        spacing: 10

        // 顶部极简标题栏 (无生硬横分割线，依靠自然留白与字阶呼吸)
        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: 28

            RowLayout {
                anchors.fill: parent
                spacing: 8

                Text {
                    text: {
                        var days = ["", "周一", "周二", "周三", "周四", "周五", "周六", "周日"];
                        var weekday = AppCentral.scheduleRuntime ? AppCentral.scheduleRuntime.currentDayOfWeek : 1;
                        var dayStr = (weekday >= 1 && weekday <= 7) ? days[weekday] : "今日";
                        return dayStr + "日程";
                    }
                    font.pixelSize: 13
                    font.bold: true
                    color: Theme.isDark() ? "#FFFFFF" : "#1D1D1F"
                }

                Item { Layout.fillWidth: true }

                // 极简微胶囊：课程节数
                Rectangle {
                    visible: dailyBarRoot.courseCount > 0
                    height: 18
                    width: countBadgeText.implicitWidth + 12
                    radius: 9
                    color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.10) : Qt.alpha("#000000", 0.06)

                    Text {
                        id: countBadgeText
                        anchors.centerIn: parent
                        text: dailyBarRoot.courseCount + " 节"
                        font.pixelSize: 10
                        color: Theme.isDark() ? "#B0B0B8" : "#6E6E73"
                    }
                }
            }
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

            // 空课表占位提示 (完全呼应主程序 Widget【暂无日程】极简设计)
            Item {
                anchors.centerIn: parent
                width: parent.width - 16
                height: 110
                visible: dailyBarRoot.courseCount === 0

                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 8

                    // 极简圆润日程环图标
                    Canvas {
                        Layout.alignment: Qt.AlignHCenter
                        width: 24
                        height: 24
                        onPaint: {
                            var ctx = getContext("2d");
                            ctx.clearRect(0, 0, width, height);
                            ctx.strokeStyle = Theme.isDark() ? Qt.alpha("#FFFFFF", 0.50) : Qt.alpha("#000000", 0.40);
                            ctx.lineWidth = 1.8;
                            ctx.beginPath();
                            ctx.arc(12, 12, 9, 0, 2 * Math.PI);
                            ctx.stroke();
                            ctx.fillStyle = Theme.accentColor || "#4099b2";
                            ctx.beginPath();
                            ctx.arc(12, 12, 2.5, 0, 2 * Math.PI);
                            ctx.fill();
                        }
                    }

                    Text {
                        Layout.alignment: Qt.AlignHCenter
                        text: "暂无日程"
                        font.pixelSize: 13
                        font.bold: true
                        color: Theme.isDark() ? "#FFFFFF" : "#1D1D1F"
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
                        width: Math.max(0, (parent.width - 8) * Math.min(1.0, Math.max(0.0, (isCurrent ? (AppCentral.scheduleRuntime ? AppCentral.scheduleRuntime.progress : 0.0) : (modelData.progress || 0.0)))))
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

        // 气泡卡片背景 (苹果液态毛玻璃卡片，通透度与主程序 Widget 完全一致)
        Rectangle {
            id: bubbleBg
            anchors.fill: parent
            radius: Math.max(10, dailyBarRoot.cornerRadius - 4)
            color: Theme.isDark()
                ? Qt.alpha("#1E1D22", 0.72 * dailyBarRoot.bgOpacity)
                : Qt.alpha("#FBFAFF", 0.78 * dailyBarRoot.bgOpacity)
        }

        // 气泡内部柔和流光漫反射
        Item {
            anchors.fill: parent
            clip: true
            Rectangle {
                id: bubbleGlow
                anchors.centerIn: parent
                width: parent.width * 0.8
                height: parent.height * 0.6
                radius: width / 2
                color: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.color || "#4099b2") : "#4099b2"
                opacity: 0.25

                layer.enabled: true
                layer.effect: FastBlur {
                    anchors.fill: bubbleGlow
                    radius: 48
                    transparentBorder: true
                }
            }
        }

        // 气泡渐变高光边框 (复刻 Widget.qml)
        Item {
            anchors.fill: parent
            Rectangle {
                id: bubbleBorderRect
                anchors.fill: parent
                radius: bubbleBg.radius
                layer.enabled: true
                layer.effect: LinearGradient {
                    start: Qt.point(0, 0)
                    end: Qt.point(width, height)
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.50) : Qt.alpha("#FFFFFF", 0.95) }
                        GradientStop { position: 0.4; color: Qt.alpha("#FFFFFF", 0.05) }
                        GradientStop { position: 0.6; color: Qt.alpha("#FFFFFF", 0.05) }
                        GradientStop { position: 1.0; color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.35) : Qt.alpha("#FFFFFF", 0.70) }
                    }
                }
            }
            layer.enabled: true
            layer.effect: OpacityMask {
                maskSource: Rectangle {
                    width: bubbleBorderRect.width
                    height: bubbleBorderRect.height
                    radius: bubbleBorderRect.radius
                    color: "transparent"
                    border.width: 1
                }
            }
            z: 10
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
            anchors.margins: 14
            spacing: 8

            // 标题行与状态胶囊 (无分割线，优雅留白)
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
                    color: Qt.alpha(dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.color || "#007AFF") : "#007AFF", 0.22)

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
                        text: {
                            var p = 0.0;
                            if (dailyBarRoot.activeEntry && dailyBarRoot.activeEntry.isCurrent) {
                                p = (AppCentral.scheduleRuntime ? AppCentral.scheduleRuntime.progress : 0.0);
                            } else if (dailyBarRoot.activeEntry) {
                                p = dailyBarRoot.activeEntry.progress || 0.0;
                            }
                            return Math.round(Math.min(1.0, Math.max(0.0, p)) * 100) + "%";
                        }
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
                        width: {
                            var p = 0.0;
                            if (dailyBarRoot.activeEntry && dailyBarRoot.activeEntry.isCurrent) {
                                p = (AppCentral.scheduleRuntime ? AppCentral.scheduleRuntime.progress : 0.0);
                            } else if (dailyBarRoot.activeEntry) {
                                p = dailyBarRoot.activeEntry.progress || 0.0;
                            }
                            return Math.max(0, parent.width * Math.min(1.0, Math.max(0.0, p)));
                        }
                        color: dailyBarRoot.activeEntry ? (dailyBarRoot.activeEntry.color || "#007AFF") : "#007AFF"
                    }
                }
            }
        }
    }
}
