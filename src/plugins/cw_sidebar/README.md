# 课表侧边栏插件 (Schedule Sidebar Plugin)

适用于 **Class Widgets 2** 的桌面边缘极简课表侧边栏扩展插件。

## 功能特性
1. **全天课程一屏平铺**：常驻屏幕边缘垂直居中，深色液态玻璃拟物材质，当前进行课程呼吸高亮。
2. **悬浮双按钮交互**：光标靠近时平滑滑出“展开全周大面板”与“收起隐藏竖条”按钮，具备 300ms 防误触缓冲。
3. **全周课表矩阵大面板**：一键平滑展开周一至周日全周课表矩阵，支持点击外部空白区域自动收回。
4. **边缘贴边极简胶囊**：收起折叠状态下仅在屏幕边缘显示微型胶囊按钮，靠近高亮，点击唤回。
5. **独立外观与全套配置**：支持停靠边缘（左/右切换）、垂直居中偏移、独立圆角弧度与背景不透明度调节。
6. **无缝鼠标穿透遮罩**：基于 PySide6 与 Win32 遮罩机制，除交互部件外全屏背景 100% 鼠标点击穿透。

## 目录结构
```
com.classwidgets.sidebar/
├── cwplugin.json          # 插件元信息清单
├── sidebar.py             # 插件 Python 入口逻辑
├── icon.png               # 插件图标
├── README.md              # 插件说明文档
├── pages/
│   └── SidebarSettings.qml # 插件专属设置界面
└── qml/                   # 侧边栏 QML 完整套件
    ├── ScheduleSidebar.qml
    ├── DailyScheduleBar.qml
    ├── WeeklySchedulePanel.qml
    ├── EdgeRestoreCapsule.qml
    ├── SidebarHoverButtons.qml
    └── qmldir
```

## 安装方式
1. 打开 Class Widgets 2 设置中心 -> **插件** 页面。
2. 点击右上角 **导入** 按钮，选择本插件压缩包（`.zip` 或 `.cwplugin`）即可完成安装。
3. 也可直接将解压后的文件夹复制到软件根目录下的 `plugins/` 目录中。
