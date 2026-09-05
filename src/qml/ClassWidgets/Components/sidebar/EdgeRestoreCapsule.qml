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

    // 自定义外观与定位属性 (由父级 ScheduleSidebar 传入)
    property bool isLeftEdge: false
    property real cornerRadius: 10
    property real bgOpacity: 1.0

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
        x: !edgeCapsuleRoot.isActive
            ? (edgeCapsuleRoot.isLeftEdge ? -20 : 20)
            : (edgeCapsuleRoot.isHovered ? (edgeCapsuleRoot.isLeftEdge ? 3 : -3) : 0)
        Behavior on x {
            NumberAnimation { duration: 180; easing.type: Easing.OutCubic }
        }
    }

    // 柔和微投影 (轻量级硬件缓存快速渲染，提升在深浅背景上的悬浮层次)
    DropShadow {
        anchors.fill: capsuleBg
        horizontalOffset: edgeCapsuleRoot.isLeftEdge ? 2 : -2
        verticalOffset: 2
        radius: 6
        samples: 8
        cached: true
        fast: true
        color: Theme.isDark() ? Qt.alpha("#000000", 0.55) : Qt.alpha("#000000", 0.18)
        source: capsuleBg
    }

    // 贴边微药丸背景 (紧贴屏幕左/右边缘)
    Rectangle {
        id: capsuleBg
        anchors.fill: parent
        // 贴边自适应圆角 (靠右时仅左侧圆角，靠左时仅右侧圆角)
        topLeftRadius: edgeCapsuleRoot.isLeftEdge ? 0 : edgeCapsuleRoot.cornerRadius
        bottomLeftRadius: edgeCapsuleRoot.isLeftEdge ? 0 : edgeCapsuleRoot.cornerRadius
        topRightRadius: edgeCapsuleRoot.isLeftEdge ? edgeCapsuleRoot.cornerRadius : 0
        bottomRightRadius: edgeCapsuleRoot.isLeftEdge ? edgeCapsuleRoot.cornerRadius : 0

        color: {
            if (capsuleMouseArea.pressed) {
                return Theme.accentColor || "#4A90E2";
            }
            if (edgeCapsuleRoot.isHovered) {
                return Theme.isDark() ? Qt.alpha("#35343E", 0.98) : Qt.alpha("#EBEBF2", 0.98);
            }
            return Theme.isDark()
                ? Qt.alpha("#26252C", 0.95 * edgeCapsuleRoot.bgOpacity)
                : Qt.alpha("#F7F7FA", 0.98 * edgeCapsuleRoot.bgOpacity);
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

        // 胶囊内部主题色拉手条 (极具辨识度，解决深色软件背景下隐形)
        Rectangle {
            id: accentBar
            anchors.left: edgeCapsuleRoot.isLeftEdge ? undefined : parent.left
            anchors.right: edgeCapsuleRoot.isLeftEdge ? parent.right : undefined
            anchors.leftMargin: edgeCapsuleRoot.isLeftEdge ? 0 : 2.5
            anchors.rightMargin: edgeCapsuleRoot.isLeftEdge ? 2.5 : 0
            anchors.verticalCenter: parent.verticalCenter
            width: 2.5
            height: 22
            radius: 1.25
            color: Theme.accentColor || "#4A90E2"
            opacity: edgeCapsuleRoot.isHovered ? 1.0 : 0.80

            Behavior on opacity { NumberAnimation { duration: 160 } }
        }

        // "<" / ">" 图标指示符 (根据贴边方位自适应指向屏幕内侧)
        Text {
            id: arrowIcon
            anchors.centerIn: parent
            anchors.horizontalCenterOffset: edgeCapsuleRoot.isLeftEdge ? -1 : 1
            text: edgeCapsuleRoot.isLeftEdge ? "›" : "‹"
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
