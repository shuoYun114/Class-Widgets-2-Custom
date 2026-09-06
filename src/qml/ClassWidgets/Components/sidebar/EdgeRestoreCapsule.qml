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


    // 贴边微药丸背景 (苹果液态玻璃拉手条，通透度对齐主程序 Widget.qml)
    Rectangle {
        id: capsuleBg
        anchors.fill: parent
        topLeftRadius: edgeCapsuleRoot.isLeftEdge ? 0 : edgeCapsuleRoot.cornerRadius
        bottomLeftRadius: edgeCapsuleRoot.isLeftEdge ? 0 : edgeCapsuleRoot.cornerRadius
        topRightRadius: edgeCapsuleRoot.isLeftEdge ? edgeCapsuleRoot.cornerRadius : 0
        bottomRightRadius: edgeCapsuleRoot.isLeftEdge ? edgeCapsuleRoot.cornerRadius : 0

        color: {
            if (capsuleMouseArea.pressed) {
                return Theme.accentColor || "#4099b2";
            }
            if (edgeCapsuleRoot.isHovered) {
                return Theme.isDark() ? Qt.alpha("#2A2930", 0.80) : Qt.alpha("#ECECF2", 0.82);
            }
            return Theme.isDark()
                ? Qt.alpha("#1E1D22", 0.65 * edgeCapsuleRoot.bgOpacity)
                : Qt.alpha("#FBFAFF", 0.70 * edgeCapsuleRoot.bgOpacity);
        }

        border.width: 1
        border.color: {
            if (capsuleMouseArea.pressed) {
                return Theme.accentColor || "#4099b2";
            }
            if (edgeCapsuleRoot.isHovered) {
                return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.45) : Qt.alpha("#FFFFFF", 0.90);
            }
            return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.20) : Qt.alpha("#FFFFFF", 0.70);
        }

        Behavior on color { ColorAnimation { duration: 160 } }
        Behavior on border.color { ColorAnimation { duration: 160 } }

        // 苹果标准抽屉拉手微胶囊 (Grip Indicator Pill)
        Rectangle {
            id: gripIndicator
            anchors.centerIn: parent
            width: 3
            height: 24
            radius: 1.5
            color: {
                if (capsuleMouseArea.pressed) {
                    return "#FFFFFF";
                }
                if (edgeCapsuleRoot.isHovered) {
                    return Theme.isDark() ? "#FFFFFF" : (Theme.accentColor || "#4099b2");
                }
                return Theme.isDark() ? Qt.alpha("#FFFFFF", 0.45) : Qt.alpha("#000000", 0.30);
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
