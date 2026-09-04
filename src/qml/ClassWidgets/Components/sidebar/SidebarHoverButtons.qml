import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects
import RinUI
import ClassWidgets.Theme 1.0
import ClassWidgets.Easing

Item {
    id: hoverButtonsRoot

    // 默认尺寸与布局
    width: 44
    height: 106

    // 状态控制
    property bool isHovered: buttonsMouseArea.containsMouse || btn1Area.containsMouse || btn2Area.containsMouse
    property bool activeState: false
    property bool buttonsVisible: opacity > 0.05

    // 信号
    signal expandWeeklyClicked()
    signal collapseSidebarClicked()

    // 外部调用：光标移入相关触发区时保持显示
    function requestShow() {
        bufferTimer.stop();
        activeState = true;
    }

    // 外部调用：光标移出后开始 300ms 防误触倒计时
    function requestHideWithBuffer() {
        bufferTimer.restart();
    }

    // 立即收回 (无缓冲)
    function hideImmediately() {
        bufferTimer.stop();
        activeState = false;
    }

    // 提供给遮罩计算
    function getInteractiveRect() {
        if (!buttonsVisible) return [0, 0, 0, 0];
        return [x, y, width, height];
    }

    // 300ms 防误触缓冲计时器 (R2 核心)
    Timer {
        id: bufferTimer
        interval: 300
        repeat: false
        onTriggered: {
            if (!hoverButtonsRoot.isHovered) {
                hoverButtonsRoot.activeState = false;
            }
        }
    }

    // 进出平滑动画
    opacity: activeState ? 1.0 : 0.0
    scale: activeState ? 1.0 : 0.88
    visible: opacity > 0.01

    Behavior on opacity {
        NumberAnimation { duration: 240; easing.type: Easing.OutQuad }
    }
    Behavior on scale {
        NumberAnimation {
            duration: 280
            easing.type: Easing.Bezier
            easing.bezierCurve: BezierCurve.liquidBack
        }
    }

    // 背景全区域防误触捕获
    MouseArea {
        id: buttonsMouseArea
        anchors.fill: parent
        hoverEnabled: true
        onEntered: bufferTimer.stop()
        onExited: bufferTimer.restart()
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 12

        // =====================================
        // 按钮 1: 展开全周大面板
        // =====================================
        Item {
            Layout.preferredWidth: 42
            Layout.preferredHeight: 42
            Layout.alignment: Qt.AlignHCenter

            // 阴影
            DropShadow {
                anchors.fill: btn1Bg
                horizontalOffset: -2
                verticalOffset: 4
                radius: 12
                samples: 16
                color: Theme.isDark() ? Qt.alpha("#000000", 0.50) : Qt.alpha("#000000", 0.16)
                source: btn1Bg
            }

            Rectangle {
                id: btn1Bg
                anchors.fill: parent
                radius: 21
                color: {
                    if (btn1Area.pressed) {
                        return Theme.isDark() ? Qt.alpha("#3A3840", 0.95) : Qt.alpha("#E5E5EA", 0.95);
                    }
                    if (btn1Area.containsMouse) {
                        return Theme.isDark() ? Qt.alpha("#2E2D34", 0.92) : Qt.alpha("#F2F2F7", 0.95);
                    }
                    return Theme.isDark() ? Qt.alpha("#212026", 0.85) : Qt.alpha("#FCFBFF", 0.90);
                }
                border.width: 1
                border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.22) : Qt.alpha("#000000", 0.10)

                Behavior on color { ColorAnimation { duration: 150 } }

                // 网格/全周图标
                Text {
                    anchors.centerIn: parent
                    text: "▦"
                    font.pixelSize: 18
                    color: btn1Area.containsMouse ? (Theme.accentColor || "#4A90E2") : (Theme.isDark() ? "#EDEDED" : "#333333")
                    Behavior on color { ColorAnimation { duration: 150 } }
                }
            }

            MouseArea {
                id: btn1Area
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onEntered: bufferTimer.stop()
                onExited: bufferTimer.restart()
                onClicked: {
                    hoverButtonsRoot.expandWeeklyClicked();
                }
            }

            // 悬停提示 Tooltip
            Rectangle {
                id: tooltip1
                anchors.right: parent.left
                anchors.rightMargin: 8
                anchors.verticalCenter: parent.verticalCenter
                width: tipText1.implicitWidth + 14
                height: 24
                radius: 6
                color: Theme.isDark() ? "#2D2C33" : "#F7F7F7"
                border.width: 1
                border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.15) : Qt.alpha("#000000", 0.08)
                opacity: btn1Area.containsMouse ? 1.0 : 0.0
                visible: opacity > 0.01

                Behavior on opacity { NumberAnimation { duration: 160 } }

                Text {
                    id: tipText1
                    anchors.centerIn: parent
                    text: "展开全周课表"
                    font.pixelSize: 11
                    color: Theme.isDark() ? "#EDEDED" : "#222222"
                }
            }
        }

        // =====================================
        // 按钮 2: 收起隐藏竖条
        // =====================================
        Item {
            Layout.preferredWidth: 42
            Layout.preferredHeight: 42
            Layout.alignment: Qt.AlignHCenter

            // 阴影
            DropShadow {
                anchors.fill: btn2Bg
                horizontalOffset: -2
                verticalOffset: 4
                radius: 12
                samples: 16
                color: Theme.isDark() ? Qt.alpha("#000000", 0.50) : Qt.alpha("#000000", 0.16)
                source: btn2Bg
            }

            Rectangle {
                id: btn2Bg
                anchors.fill: parent
                radius: 21
                color: {
                    if (btn2Area.pressed) {
                        return Theme.isDark() ? Qt.alpha("#3A3840", 0.95) : Qt.alpha("#E5E5EA", 0.95);
                    }
                    if (btn2Area.containsMouse) {
                        return Theme.isDark() ? Qt.alpha("#2E2D34", 0.92) : Qt.alpha("#F2F2F7", 0.95);
                    }
                    return Theme.isDark() ? Qt.alpha("#212026", 0.85) : Qt.alpha("#FCFBFF", 0.90);
                }
                border.width: 1
                border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.22) : Qt.alpha("#000000", 0.10)

                Behavior on color { ColorAnimation { duration: 150 } }

                // 收缩隐藏图标
                Text {
                    anchors.centerIn: parent
                    text: "⇥"
                    font.pixelSize: 18
                    color: btn2Area.containsMouse ? (Theme.accentColor || "#4A90E2") : (Theme.isDark() ? "#EDEDED" : "#333333")
                    Behavior on color { ColorAnimation { duration: 150 } }
                }
            }

            MouseArea {
                id: btn2Area
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onEntered: bufferTimer.stop()
                onExited: bufferTimer.restart()
                onClicked: {
                    hoverButtonsRoot.collapseSidebarClicked();
                }
            }

            // 悬停提示 Tooltip
            Rectangle {
                id: tooltip2
                anchors.right: parent.left
                anchors.rightMargin: 8
                anchors.verticalCenter: parent.verticalCenter
                width: tipText2.implicitWidth + 14
                height: 24
                radius: 6
                color: Theme.isDark() ? "#2D2C33" : "#F7F7F7"
                border.width: 1
                border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.15) : Qt.alpha("#000000", 0.08)
                opacity: btn2Area.containsMouse ? 1.0 : 0.0
                visible: opacity > 0.01

                Behavior on opacity { NumberAnimation { duration: 160 } }

                Text {
                    id: tipText2
                    anchors.centerIn: parent
                    text: "收起隐藏竖条"
                    font.pixelSize: 11
                    color: Theme.isDark() ? "#EDEDED" : "#222222"
                }
            }
        }
    }
}
