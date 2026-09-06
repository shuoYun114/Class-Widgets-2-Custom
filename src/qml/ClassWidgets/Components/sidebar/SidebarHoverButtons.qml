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

    // 自定义外观与定位属性 (由父级 ScheduleSidebar 传入)
    property bool isLeftEdge: false
    property real cornerRadius: 21
    property real bgOpacity: 1.0

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

    // 进出平滑动画 (根据左右边缘镜像 Translate 矩阵位移与淡入)
    opacity: activeState ? 1.0 : 0.0
    visible: opacity > 0.01

    Behavior on opacity {
        NumberAnimation { duration: 180; easing.type: Easing.OutQuad }
    }

    transform: Translate {
        x: hoverButtonsRoot.activeState ? 0 : (hoverButtonsRoot.isLeftEdge ? -12 : 12)
        Behavior on x {
            NumberAnimation { duration: 200; easing.type: Easing.OutCubic }
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
        // 按钮 1: 展开全周大面板 (苹果液态玻璃圆盘 + 极简 2x2 矩阵微图标)
        // =====================================
        Item {
            Layout.preferredWidth: 42
            Layout.preferredHeight: 42
            Layout.alignment: Qt.AlignHCenter

            Rectangle {
                id: btn1Bg
                anchors.fill: parent
                radius: hoverButtonsRoot.cornerRadius

                color: {
                    if (btn1Area.pressed) return Theme.isDark() ? Qt.alpha("#2E2D36", 0.90) : Qt.alpha("#E0E0E6", 0.90);
                    if (btn1Area.containsMouse) return Theme.isDark() ? Qt.alpha("#26252C", 0.82) : Qt.alpha("#ECECF2", 0.85);
                    return Theme.isDark() ? Qt.alpha("#1E1D22", 0.65 * hoverButtonsRoot.bgOpacity) : Qt.alpha("#FBFAFF", 0.70 * hoverButtonsRoot.bgOpacity);
                }

                border.width: 1
                border.color: btn1Area.containsMouse
                    ? (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.45) : Qt.alpha("#FFFFFF", 0.95))
                    : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.20) : Qt.alpha("#FFFFFF", 0.70))

                Behavior on color { ColorAnimation { duration: 150 } }
                Behavior on border.color { ColorAnimation { duration: 150 } }

                // 精美 2x2 极简日历矩阵微图标 (替代 AI 粗糙字符 ▦)
                Item {
                    anchors.centerIn: parent
                    width: 14
                    height: 14

                    Grid {
                        anchors.centerIn: parent
                        columns: 2
                        spacing: 3

                        Repeater {
                            model: 4
                            Rectangle {
                                width: 5
                                height: 5
                                radius: 1.5
                                color: btn1Area.containsMouse ? (Theme.accentColor || "#4099b2") : (Theme.isDark() ? "#EDEDED" : "#1D1D1F")
                                Behavior on color { ColorAnimation { duration: 150 } }
                            }
                        }
                    }
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

            // 悬停提示 Tooltip (苹果半透明胶囊气泡)
            Rectangle {
                id: tooltip1
                anchors.right: hoverButtonsRoot.isLeftEdge ? undefined : parent.left
                anchors.left: hoverButtonsRoot.isLeftEdge ? parent.right : undefined
                anchors.rightMargin: hoverButtonsRoot.isLeftEdge ? 0 : 8
                anchors.leftMargin: hoverButtonsRoot.isLeftEdge ? 8 : 0
                anchors.verticalCenter: parent.verticalCenter
                width: tipText1.implicitWidth + 16
                height: 24
                radius: 8
                color: Theme.isDark() ? Qt.alpha("#1E1D22", 0.85) : Qt.alpha("#FBFAFF", 0.88)
                border.width: 1
                border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.22) : Qt.alpha("#FFFFFF", 0.75)
                opacity: btn1Area.containsMouse ? 1.0 : 0.0
                visible: opacity > 0.01

                Behavior on opacity { NumberAnimation { duration: 160 } }

                Text {
                    id: tipText1
                    anchors.centerIn: parent
                    text: "全周课表"
                    font.pixelSize: 11
                    color: Theme.isDark() ? "#EDEDED" : "#1D1D1F"
                }
            }
        }

        // =====================================
        // 按钮 2: 收起隐藏竖条 (苹果液态玻璃圆盘 + 极细 Chevron 矢量折叠微图标)
        // =====================================
        Item {
            Layout.preferredWidth: 42
            Layout.preferredHeight: 42
            Layout.alignment: Qt.AlignHCenter

            Rectangle {
                id: btn2Bg
                anchors.fill: parent
                radius: hoverButtonsRoot.cornerRadius

                color: {
                    if (btn2Area.pressed) return Theme.isDark() ? Qt.alpha("#2E2D36", 0.90) : Qt.alpha("#E0E0E6", 0.90);
                    if (btn2Area.containsMouse) return Theme.isDark() ? Qt.alpha("#26252C", 0.82) : Qt.alpha("#ECECF2", 0.85);
                    return Theme.isDark() ? Qt.alpha("#1E1D22", 0.65 * hoverButtonsRoot.bgOpacity) : Qt.alpha("#FBFAFF", 0.70 * hoverButtonsRoot.bgOpacity);
                }

                border.width: 1
                border.color: btn2Area.containsMouse
                    ? (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.45) : Qt.alpha("#FFFFFF", 0.95))
                    : (Theme.isDark() ? Qt.alpha("#FFFFFF", 0.20) : Qt.alpha("#FFFFFF", 0.70))

                Behavior on color { ColorAnimation { duration: 150 } }
                Behavior on border.color { ColorAnimation { duration: 150 } }


                // 极细 Chevron 矢量折叠微图标 (替代粗糙字符 ⇤/⇥)
                Item {
                    anchors.centerIn: parent
                    width: 14
                    height: 14

                    readonly property color iconColor: btn2Area.containsMouse ? (Theme.accentColor || "#007AFF") : (Theme.isDark() ? "#EDEDED" : "#1D1D1F")

                    Canvas {
                        id: collapseCanvas
                        anchors.fill: parent
                        onPaint: {
                            var ctx = getContext("2d");
                            ctx.clearRect(0, 0, width, height);
                            ctx.strokeStyle = parent.iconColor;
                            ctx.lineWidth = 1.6;
                            ctx.lineCap = "round";
                            ctx.lineJoin = "round";
                            ctx.beginPath();
                            if (hoverButtonsRoot.isLeftEdge) {
                                ctx.moveTo(9, 3);
                                ctx.lineTo(4, 7);
                                ctx.lineTo(9, 11);
                                ctx.moveTo(12, 3);
                                ctx.lineTo(12, 11);
                            } else {
                                ctx.moveTo(5, 3);
                                ctx.lineTo(10, 7);
                                ctx.lineTo(5, 11);
                                ctx.moveTo(2, 3);
                                ctx.lineTo(2, 11);
                            }
                            ctx.stroke();
                        }

                        Connections {
                            target: btn2Area
                            function onContainsMouseChanged() { collapseCanvas.requestPaint(); }
                        }
                        Connections {
                            target: hoverButtonsRoot
                            function onIsLeftEdgeChanged() { collapseCanvas.requestPaint(); }
                        }
                    }
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

            // 悬停提示 Tooltip (苹果半透明胶囊气泡)
            Rectangle {
                id: tooltip2
                anchors.right: hoverButtonsRoot.isLeftEdge ? undefined : parent.left
                anchors.left: hoverButtonsRoot.isLeftEdge ? parent.right : undefined
                anchors.rightMargin: hoverButtonsRoot.isLeftEdge ? 0 : 8
                anchors.leftMargin: hoverButtonsRoot.isLeftEdge ? 8 : 0
                anchors.verticalCenter: parent.verticalCenter
                width: tipText2.implicitWidth + 16
                height: 24
                radius: 8
                color: Theme.isDark() ? Qt.alpha("#26252C", 0.95) : Qt.alpha("#FFFFFF", 0.96)
                border.width: 1
                border.color: Theme.isDark() ? Qt.alpha("#FFFFFF", 0.16) : Qt.alpha("#FFFFFF", 0.70)
                opacity: btn2Area.containsMouse ? 1.0 : 0.0
                visible: opacity > 0.01

                Behavior on opacity { NumberAnimation { duration: 160 } }

                Text {
                    id: tipText2
                    anchors.centerIn: parent
                    text: "收起侧边栏"
                    font.pixelSize: 11
                    color: Theme.isDark() ? "#EDEDED" : "#1D1D1F"
                }
            }
        }
    }
}
