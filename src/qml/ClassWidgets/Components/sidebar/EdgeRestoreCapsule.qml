import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects
import RinUI
import ClassWidgets.Theme 1.0
import ClassWidgets.Easing

Item {
    id: edgeCapsuleRoot

    // 尺寸：微型贴边胶囊，宽度约 20px，高度约 64px (严格契合系统遮罩与数学穿透率)
    width: 20
    height: 64

    // 状态与向外暴露
    property bool isHovered: capsuleMouseArea.containsMouse
    property bool isActive: false // 是否处于折叠激活态 (COLLAPSED)

    signal restoreClicked()

    function getInteractiveRect() {
        if (!isActive) return [0, 0, 0, 0];
        return [x, y, width, height];
    }

    // 贴边胶囊进出动画 (未悬停时保持 0.88 良好辨识度，悬停时 1.0 全亮高光)
    opacity: isActive ? (isHovered ? 1.0 : 0.88) : 0.0
    visible: opacity > 0.01

    Behavior on opacity {
        NumberAnimation { duration: 180; easing.type: Easing.OutQuad }
    }

    transform: Translate {
        x: !edgeCapsuleRoot.isActive ? 20 : (edgeCapsuleRoot.isHovered ? -3 : 0)
        Behavior on x {
            NumberAnimation { duration: 180; easing.type: Easing.OutCubic }
        }
    }

    // 柔和微投影 (轻量级硬件缓存快速渲染，提升在深浅背景上的悬浮层次)
    DropShadow {
        anchors.fill: capsuleBg
        horizontalOffset: -2
        verticalOffset: 2
        radius: 6
        samples: 8
        cached: true
        fast: true
        color: Theme.isDark() ? Qt.alpha("#000000", 0.55) : Qt.alpha("#000000", 0.18)
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
                return Theme.isDark() ? Qt.alpha("#35343E", 0.98) : Qt.alpha("#EBEBF2", 0.98);
            }
            return Theme.isDark() ? Qt.alpha("#26252C", 0.95) : Qt.alpha("#F7F7FA", 0.98);
        }

        border.width: 1
        border.color: {
            if (capsuleMouseArea.pressed || edgeCapsuleRoot.isHovered) {
                return Theme.accentColor || "#4A90E2";
            }
            return Theme.isDark()
                ? Qt.alpha(Theme.accentColor || "#4A90E2", 0.45)
                : Qt.alpha("#000000", 0.16);
        }

        Behavior on color { ColorAnimation { duration: 160 } }
        Behavior on border.color { ColorAnimation { duration: 160 } }

        // 胶囊内部左侧主题色拉手条 (极具辨识度，解决深色软件背景下隐形)
        Rectangle {
            id: accentBar
            anchors.left: parent.left
            anchors.leftMargin: 2.5
            anchors.verticalCenter: parent.verticalCenter
            width: 2.5
            height: 22
            radius: 1.25
            color: Theme.accentColor || "#4A90E2"
            opacity: edgeCapsuleRoot.isHovered ? 1.0 : 0.80

            Behavior on opacity { NumberAnimation { duration: 160 } }
        }

        // "<" 向左图标指示符
        Text {
            id: arrowIcon
            anchors.centerIn: parent
            anchors.horizontalCenterOffset: 1
            text: "‹"
            font.pixelSize: 16
            font.bold: true
            color: {
                if (capsuleMouseArea.pressed) {
                    return "#FFFFFF";
                }
                if (edgeCapsuleRoot.isHovered) {
                    return Theme.accentColor || "#4A90E2";
                }
                return Theme.isDark() ? "#FFFFFF" : "#333333";
            }

            Behavior on color { ColorAnimation { duration: 160 } }
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
}
