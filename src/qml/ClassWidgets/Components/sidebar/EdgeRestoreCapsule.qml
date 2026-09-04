import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects
import RinUI
import ClassWidgets.Theme 1.0
import ClassWidgets.Easing

Item {
    id: edgeCapsuleRoot

    // 尺寸：微型贴边胶囊，宽度约 20px，高度约 64px
    width: 20
    height: 64

    // 状态与向外暴露
    property bool isHovered: capsuleMouseArea.containsMouse
    property bool isActive: false // 是否处于折叠激活态 (COLLAPSED)

    signal restoreClicked()

    function getInteractiveRect() {
        if (!visible || opacity < 0.05) return [0, 0, 0, 0];
        return [x, y, width, height];
    }

    // 贴边胶囊进出动画
    opacity: isActive ? (isHovered ? 1.0 : 0.35) : 0.0
    scale: isActive ? (isHovered ? 1.05 : 1.0) : 0.85
    visible: opacity > 0.01

    Behavior on opacity {
        NumberAnimation { duration: 220; easing.type: Easing.OutQuad }
    }
    Behavior on scale {
        NumberAnimation {
            duration: 250
            easing.type: Easing.Bezier
            easing.bezierCurve: BezierCurve.liquidBack
        }
    }

    // 柔和微投影
    DropShadow {
        anchors.fill: capsuleBg
        horizontalOffset: -2
        verticalOffset: 2
        radius: 8
        samples: 12
        color: Theme.isDark() ? Qt.alpha("#000000", 0.45) : Qt.alpha("#000000", 0.15)
        source: capsuleBg
    }

    // 贴边微药丸背景 (仅左侧圆角，紧贴屏幕右边缘)
    Rectangle {
        id: capsuleBg
        anchors.fill: parent
        // 左上与左下大圆角
        topLeftRadius: 10
        bottomLeftRadius: 10
        topRightRadius: 0
        bottomRightRadius: 0

        color: {
            if (capsuleMouseArea.pressed) {
                return Theme.accentColor || "#4A90E2";
            }
            if (edgeCapsuleRoot.isHovered) {
                return Theme.isDark() ? Qt.alpha("#2E2D34", 0.95) : Qt.alpha("#EBEBF0", 0.96);
            }
            return Theme.isDark() ? Qt.alpha("#1C1B20", 0.70) : Qt.alpha("#F2F2F7", 0.75);
        }

        border.width: 1
        border.color: edgeCapsuleRoot.isHovered
            ? (Theme.accentColor || "#4A90E2")
            : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.20) : Qt.alpha("#000000", 0.10))

        Behavior on color { ColorAnimation { duration: 180 } }
        Behavior on border.color { ColorAnimation { duration: 180 } }

        // "<" 向左图标指示符
        Text {
            anchors.centerIn: parent
            anchors.horizontalCenterOffset: -1
            text: "‹"
            font.pixelSize: 18
            font.bold: true
            color: edgeCapsuleRoot.isHovered
                ? (Theme.accentColor || "#4A90E2")
                : (Theme.isDark() ? "#D0D0D0" : "#666666")

            Behavior on color { ColorAnimation { duration: 180 } }
        }
    }

    // 鼠标点击与悬浮捕获
    MouseArea {
        id: capsuleMouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            edgeCapsuleRoot.restoreClicked();
        }
    }

    // 悬浮靠近时的提示 Tooltip
    Rectangle {
        id: capsuleTooltip
        anchors.right: parent.left
        anchors.rightMargin: 8
        anchors.verticalCenter: parent.verticalCenter
        width: tipLabel.implicitWidth + 14
        height: 24
        radius: 6
        color: Theme.isDark() ? "#2D2C33" : "#F7F7F7"
        border.width: 1
        border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.15) : Qt.alpha("#000000", 0.08)
        opacity: edgeCapsuleRoot.isHovered ? 1.0 : 0.0
        visible: opacity > 0.01

        Behavior on opacity { NumberAnimation { duration: 160 } }

        Text {
            id: tipLabel
            anchors.centerIn: parent
            text: "呼出课表竖条"
            font.pixelSize: 11
            color: Theme.isDark() ? "#EDEDED" : "#222222"
        }
    }
}
