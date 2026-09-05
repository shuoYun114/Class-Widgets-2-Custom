import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import RinUI
import ClassWidgets.Components

FluentPage {
    id: sidebarSettingsPage
    title: qsTr("Schedule Sidebar") === "Schedule Sidebar" ? "课表侧边栏" : qsTr("Schedule Sidebar")

    // ==========================================
    // 1. 功能总开关卡片
    // ==========================================
    SettingCard {
        Layout.fillWidth: true
        icon.name: "ic_fluent_panel_right_20_regular"
        title: qsTr("Enable Schedule Sidebar") === "Enable Schedule Sidebar" ? "启用课表侧边栏" : qsTr("Enable Schedule Sidebar")
        description: qsTr("Display daily schedule capsule on the screen edge with quick actions and weekly matrix view") === "Display daily schedule capsule on the screen edge with quick actions and weekly matrix view"
            ? "在屏幕边缘以贴边胶囊形式展示今日课程，支持一键查看全周课表与课程详情"
            : qsTr("Display daily schedule capsule on the screen edge with quick actions and weekly matrix view")

        Switch {
            id: sidebarMasterSwitch
            checked: Configs.data.preferences.schedule_sidebar_enabled !== false
            enabled: !Configs.isKeyLocked("preferences.schedule_sidebar_enabled")
            onCheckedChanged: {
                if (checked !== (Configs.data.preferences.schedule_sidebar_enabled !== false)) {
                    Configs.set("preferences.schedule_sidebar_enabled", checked)
                }
            }
        }
    }

    // ==========================================
    // 2. 位置与贴靠设置
    // ==========================================
    ColumnLayout {
        Layout.fillWidth: true
        spacing: 4
        enabled: sidebarMasterSwitch.checked

        Text {
            typography: Typography.BodyStrong
            text: qsTr("Position & Edge") === "Position & Edge" ? "位置与贴靠" : qsTr("Position & Edge")
        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_align_horizontal_right_20_regular"
            title: qsTr("Screen Edge") === "Screen Edge" ? "贴靠边缘" : qsTr("Screen Edge")
            description: qsTr("Choose whether the sidebar docks to the right or left edge of the screen") === "Choose whether the sidebar docks to the right or left edge of the screen"
                ? "选择侧边课表栏停靠在屏幕左边缘还是右边缘（自动镜像对称）"
                : qsTr("Choose whether the sidebar docks to the right or left edge of the screen")

            ComboBox {
                id: edgeComboBox
                Layout.preferredWidth: 160
                model: [
                    { "text": qsTr("Right Edge") === "Right Edge" ? "靠右贴边 (默认)" : qsTr("Right Edge"), "value": "right" },
                    { "text": qsTr("Left Edge") === "Left Edge" ? "靠左贴边" : qsTr("Left Edge"), "value": "left" }
                ]
                textRole: "text"
                enabled: !Configs.isKeyLocked("preferences.schedule_sidebar_edge")
                onActivated: function(index) {
                    var val = model[index].value;
                    Configs.set("preferences.schedule_sidebar_edge", val);
                }
                Component.onCompleted: {
                    var current = Configs.data.preferences.schedule_sidebar_edge || "right";
                    currentIndex = (current === "left") ? 1 : 0;
                }
            }
        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_arrow_sort_20_regular"
            title: qsTr("Vertical Offset (Y-Axis)") === "Vertical Offset (Y-Axis)" ? "垂直居中微调 (Y轴偏移)" : qsTr("Vertical Offset (Y-Axis)")
            description: qsTr("Adjust vertical center position of the schedule sidebar (-500px to +500px)") === "Adjust vertical center position of the schedule sidebar (-500px to +500px)"
                ? "以屏幕垂直居中为基准微调上下高度偏移量（范围 -500px ~ +500px）"
                : qsTr("Adjust vertical center position of the schedule sidebar (-500px to +500px)")

            Timer {
                id: offsetYCommitTimer
                interval: 80
                repeat: false
                onTriggered: {
                    Configs.set("preferences.schedule_sidebar_offset_y", offsetYSpinBox.value);
                }
            }

            SpinBox {
                id: offsetYSpinBox
                Layout.preferredWidth: 160
                from: -500
                to: 500
                stepSize: 10
                enabled: !Configs.isKeyLocked("preferences.schedule_sidebar_offset_y")
                onValueChanged: {
                    if (focus) {
                        offsetYCommitTimer.restart();
                    }
                }
                Component.onCompleted: {
                    value = (Configs.data.preferences.schedule_sidebar_offset_y !== undefined)
                        ? Configs.data.preferences.schedule_sidebar_offset_y
                        : 0;
                }
            }
        }
    }

    // ==========================================
    // 3. 外观与主题设置
    // ==========================================
    ColumnLayout {
        Layout.fillWidth: true
        spacing: 4
        enabled: sidebarMasterSwitch.checked

        Text {
            typography: Typography.BodyStrong
            text: qsTr("Appearances & Theme") === "Appearances & Theme" ? "外观与主题" : qsTr("Appearances & Theme")
        }

        SettingCard {
            Layout.fillWidth: true
            icon.name: "ic_fluent_paint_brush_20_regular"
            title: qsTr("Custom Appearance") === "Custom Appearance" ? "独立外观设置" : qsTr("Custom Appearance")
            description: qsTr("When disabled, the sidebar inherits global widget opacity and corner radius. When enabled, custom values are used.") === "When disabled, the sidebar inherits global widget opacity and corner radius. When enabled, custom values are used."
                ? "关闭时跟随主程序全局小组件的不透明度与圆角；开启后使用下方侧边栏专属外观"
                : qsTr("When disabled, the sidebar inherits global widget opacity and corner radius. When enabled, custom values are used.")

            Switch {
                id: customAppearanceSwitch
                checked: Configs.data.preferences.schedule_sidebar_custom_appearance === true
                enabled: !Configs.isKeyLocked("preferences.schedule_sidebar_custom_appearance")
                onCheckedChanged: {
                    if (checked !== (Configs.data.preferences.schedule_sidebar_custom_appearance === true)) {
                        Configs.set("preferences.schedule_sidebar_custom_appearance", checked)
                    }
                }
            }
        }

        SettingCard {
            Layout.fillWidth: true
            visible: customAppearanceSwitch.checked
            icon.name: "ic_fluent_shape_subtract_20_regular"
            title: qsTr("Sidebar Corner Radius") === "Sidebar Corner Radius" ? "专属圆角大小" : qsTr("Sidebar Corner Radius")
            description: qsTr("Set the corner radius of the schedule sidebar (0px to 50px)") === "Set the corner radius of the schedule sidebar (0px to 50px)"
                ? "设置侧边栏及卡片的圆角弧度（范围 0 ~ 50 像素）"
                : qsTr("Set the corner radius of the schedule sidebar (0px to 50px)")

            Timer {
                id: cornerRadiusCommitTimer
                interval: 60
                repeat: false
                onTriggered: {
                    Configs.set("preferences.schedule_sidebar_corner_radius", cornerRadiusSlider.value);
                }
            }

            Slider {
                id: cornerRadiusSlider
                from: 0
                to: 50
                stepSize: 1
                tickmarks: true
                tickFrequency: 10
                toolTip.text: Math.round(value) + " px"
                toolTip.visible: pressed
                enabled: !Configs.isKeyLocked("preferences.schedule_sidebar_corner_radius")
                onValueChanged: {
                    if (pressed) {
                        cornerRadiusCommitTimer.restart();
                    }
                }
                Component.onCompleted: {
                    value = (Configs.data.preferences.schedule_sidebar_corner_radius !== undefined)
                        ? Configs.data.preferences.schedule_sidebar_corner_radius
                        : 22.0
                }
            }
        }

        SettingCard {
            Layout.fillWidth: true
            visible: customAppearanceSwitch.checked
            icon.name: "ic_fluent_transparency_square_20_regular"
            title: qsTr("Sidebar Background Opacity") === "Sidebar Background Opacity" ? "专属背景不透明度" : qsTr("Sidebar Background Opacity")
            description: qsTr("Change the background opacity of the schedule sidebar (10% to 100%)") === "Change the background opacity of the schedule sidebar (10% to 100%)"
                ? "调节侧边课表栏背景材质不透明度（范围 10% ~ 100%）"
                : qsTr("Change the background opacity of the schedule sidebar (10% to 100%)")

            Timer {
                id: opacityCommitTimer
                interval: 60
                repeat: false
                onTriggered: {
                    Configs.set("preferences.schedule_sidebar_opacity", opacitySlider.value);
                }
            }

            Slider {
                id: opacitySlider
                from: 0.1
                to: 1.0
                stepSize: 0.05
                tickmarks: true
                tickFrequency: 0.2
                toolTip.text: Math.round(value * 100) + "%"
                toolTip.visible: pressed
                enabled: !Configs.isKeyLocked("preferences.schedule_sidebar_opacity")
                onValueChanged: {
                    if (pressed) {
                        opacityCommitTimer.restart();
                    }
                }
                Component.onCompleted: {
                    value = (Configs.data.preferences.schedule_sidebar_opacity !== undefined)
                        ? Configs.data.preferences.schedule_sidebar_opacity
                        : 1.0
                }
            }
        }
    }
}
