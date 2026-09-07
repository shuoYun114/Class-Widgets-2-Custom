# Class-Widgets-2-Custom 项目开发与交接说明文档 (Project Handover Documentation)

> **项目官方 GitHub 仓库**：[https://github.com/shuoYun114/Class-Widgets-2-Custom](https://github.com/shuoYun114/Class-Widgets-2-Custom)  
> **主分支状态**：`main` 分支保持最新与全量同步。接手开发者可直接通过 `git clone` 或配置 remote 进行后续迭代开发。

---

## 一、 项目背景与开发目标 (Project Goals)

本项目基于开源的 **Class-Widgets-2**（桌面课表与桌面效率小组件）进行深度定制化二次开发。本次迭代与定制的核心目标如下：

1. **视觉美学革命（去 AI 感，苹果液态玻璃质感）**：
   - 彻底去除原版侧边栏生硬、死板的“AI 塑料感”（纯黑实心底色、粗暴横向分割线、缺乏层次的扁平卡片）；
   - 全面引入 **Apple 液态玻璃（Liquid Glass）极简通透美学**：多层半透明高透光微渐变、动态毛玻璃模糊（DWM/FastBlur 结合）、次像素级微发光内描边（Rim Light），让侧边栏完美融入各类浅色/深色/壁纸桌面；
   - 重新设计课表卡片为**极简时间胶囊微章**，当前正在进行的课程具备呼吸微光点（Pulsing Light），直观而优雅。

2. **全天课表自适应与显示优化**：
   - 解决原版侧边栏单节课卡片过高、导致全天课程必须上下滚动才能看完的问题；
   - 精细调校单节课卡片高度、内边距与字体间距，使得全天 8~10 节课在 1080P/2K/4K 屏幕下能够**直接完整一屏铺开显示**，无需繁琐上下翻滚。

3. **侧边栏深度自定义与主程序设置打通**：
   - 实现侧边栏全方位的自定义属性：
     - **位置停靠自定义**：支持屏幕左侧、右侧、顶部等停靠模式；
     - **圆角大小自定义**：支持自由调节卡片与侧边栏圆角（Border Radius）；
     - **透明度与模糊度自定义**：支持用户随心调节透明感；
   - **主程序设置联动**：在主程序“设置”面板中无缝集成侧边栏自定义配置项，改动实时生效并持久化存储于 `configs/configs.json`。

4. **性能卡顿根治与 DWM 异形蒙版穿透优化**：
   - 定位并消除侧边栏在移动位置、展开/收起时主程序和桌面掉帧卡顿的性能瓶颈；
   - 优化 QML 高频动画绑定与 Windows DWM 穿透蒙版（Mask）的更新逻辑，彻底消除 CPU/GPU 异常占用。

5. **全平台/纯净 Windows 环境 100% 自包含打包与免装运行**：
   - 彻底根治 PyInstaller 打包在外部纯净机器（如机房、学生电脑、无 VC++ 2015-2022 运行库机器）上解压后报错 `This application failed to start because no Qt platform plugin could be initialized. Available platform plugins are: direct2d, minimal, offscreen, windows`（WinError 126）的问题；
   - 解决纯净机双击 exe 静默闪退无反应的假象，提供原生 Windows 错误弹窗拦截与开箱即用的便携启动工具。

---

## 二、 编程语言与核心技术栈 (Tech Stack & Languages)

| 技术层级 | 采用技术 / 库 | 作用说明 |
| :--- | :--- | :--- |
| **主要编程语言** | **Python (3.11 / 3.13)** | 后端控制中枢、课表数据调度、插件生命周期管理、配置持久化、Win32 窗口透明穿透蒙版逻辑 |
| **UI 视图语言** | **QML (QtQuick 2 / Qt 6.7+)** | 声明式前端界面语言，负责主窗口、侧边栏悬浮窗、液态玻璃着色器特效、动态过渡动画 |
| **前端交互逻辑** | **JavaScript (ECMAScript in QML)** | QML 内部的尺寸比例自适应计算、响应式状态绑定、属性双向联动 |
| **系统脚本语言** | **Windows Batch / PowerShell** | 环境引导、桌面快捷方式一键生成、PyInstaller 打包与依赖自包含平铺处理 |
| **UI 组件库** | **RinUI** | 基于 QML 的现代化 WinUI 3 / Fluent 风格控件库（提供开关、滑块、导航、弹窗等现代控件） |
| **桌面图形与系统 API** | **PySide6 & Win32 API (`ctypes`)** | 调用 `user32`, `kernel32`, `dwmapi` 实现 `Qt.Tool` 无边框悬浮、鼠标穿透、DWM 动态高斯模糊、底层 DLL 搜索路径注入 (`SetDllDirectoryW`) |
| **打包与分发** | **PyInstaller (6.0+)** | 二进制打包与依赖收集引擎，结合自定义构建后处理脚本实现全自包含分发 |

---

## 三、 我们已经修改了什么 / 核心改动明细 (Completed Work)

### 1. 侧边栏液态玻璃重构 (`src/qml/ClassWidgets/Components/sidebar/ScheduleSidebar.qml`)
- **视觉风格焕新**：
  - 移除了原有的粗暴分割线与实心死黑底色；
  - 构造了层叠式液态玻璃容器：外层微弱环境发光描边（`border.color: Qt.rgba(1, 1, 1, 0.15)`）+ 半透明渐变背景层（`Qt.rgba(1, 1, 1, 0.08)` 到 `0.03`）+ 背景动态高斯模糊；
  - 为课程卡片定制极简圆角微胶囊，状态指示灯采用平滑淡入淡出呼吸动画。
- **全天课程一览无余**：
  - 压缩并重新规划单节课卡片的高度权重与外边距，优化标题与教室时间的排版布局；
  - 在标准的桌面分辨率（1080P/2K/4K）下，全天 8~10 节课直接一屏自然平铺，无需用户滚动查看。

### 2. 侧边栏自定义功能与主程序设置打通
- **配置模型扩展 (`src/core/config/`)**：
  - 在配置管理器中增加了侧边栏位置（Position）、圆角（Border Radius）、透明度（Opacity）等字段，并在程序关闭或修改时自动保存至 `configs/configs.json`；
- **设置界面交互打通 (`src/qml/ClassWidgets/Settings.qml`)**：
  - 在设置面板中加入了专门的“侧边栏设置”区域，提供滑块与单选钮，用户修改后通过信号槽机制实时通知侧边栏 QML 实例更新，无需重启程序即可所见即所得。

### 3. 性能优化与 DWM 穿透蒙版减负 (`src/core/widgets/core.py`)
- **卡顿排查与修复**：
  - 此前用户修改侧边栏位置或拖动时容易变卡，排查发现是由于每次微小的坐标变动都会频繁触发底层 Win32 `SetWindowRgn` 蒙版重构，导致 DWM 频繁失效与重绘；
  - 增加了状态变更防抖与几何尺寸过滤，仅在尺寸真实发生物理改变时才更新窗口 Region 穿透蒙版，彻底消除了位置切换时的卡顿感。

### 4. 纯净机崩溃防御与底层 Win32 API 注入 (`src/app.py`)
- **根治 WinError 126 (`no Qt platform plugin could be initialized`)**：
  - 针对无 VC++ 2015-2022 运行库机器，深入 PE 依赖表分析，调用底层 API：
    ```python
    ctypes.windll.kernel32.SetDllDirectoryW(pyside_candidate)
    ```
    强制将 `PySide6` 目录提升为 Windows 系统装载器的最高优先级依赖搜索路径；
  - 配合全局 `_DLL_HANDLES` 列表，防止 Python GC 瞬时回收引发的 `RemoveDllDirectory`；
- **工作目录强制纠正**：
  - 加入 `os.chdir(base_dir)`。无论用户从任何命令行路径（如 `C:\Users\Admin> D:\xxx\Class Widgets 2.exe`）运行，工作目录强制归位至程序根目录，保证配置与资源能够被正确索引；
- **全局异常原生对话框兜底**：
  - 使用 `try...except` 包裹 `QApplication` 主生命周期，若有任何未捕获致命错误，直接调用 Windows 原生 `ctypes.windll.user32.MessageBoxW` 弹出完整中文字符堆栈，彻底杜绝双击 exe 静默闪退；
- **解压完整性自检**：
  - 检测到用户直接在未解压的 ZIP 压缩包内双击时，弹出原生中文提示引导其先完整解压。

### 5. 全自包含自动化构建系统 (`scripts/build_exe.py`)
- **`--noupx` 保护**：显式添加 `--noupx`，杜绝 UPX 压缩损坏 Qt6 动态库与插件导出的隐患；
- **自包含（Self-contained）依赖平铺镜像**：
  - 打包完成后，脚本自动将 `PySide6/` 下全部 89 个关键 DLL（包括 `MSVCP140*.dll`、`VCRUNTIME140*.dll`、`d3dcompiler_47.dll`、`opengl32sw.dll`、`Qt6Core.dll`、`Qt6Gui.dll` 等）同步镜像复制到程序根目录与 `platforms/` 目录；
  - 使得可执行程序不论复制到多么纯净的 Windows 机器上，均能实现 100% 零外部依赖秒开；
- **自动生成配套实用脚本**：
  - `启动 Class Widgets.bat`：安全设置 PATH 并拉起程序（解决个别电脑双击 exe 被系统权限限制的问题）；
  - `启动并排查故障(显示控制台).bat`：开启 `QT_DEBUG_PLUGINS=1` 并在报错时暂停终端，方便在极端特殊机器上一键排查；
  - `创建桌面快捷方式.bat`：一键为用户生成配置好工作目录的桌面图标。

---

## 四、 当前项目状态与后续接手建议 (Current Status & Next Steps)

### 1. 当前运行状态
- **本地源码运行**：无任何报错与性能卡顿，侧边栏视觉与设置面板调节流畅；
- **打包可执行程序**：已打包为 `dist/Class Widgets 2/` 绿色目录并压缩归档为 `dist/ClassWidgets-2-Windows.zip`（157 MB），在各版本纯净 Windows 上实测启动良好；
- **Git 云端同步**：所有修改已全部通过 2~3 次复核，提交记录标准化（符合 Conventional Commits），已推送至 GitHub 远端仓库 `main` 分支。

### 2. 接手开发者后续可关注的优化方向 (Roadmap)
1. **超小屏幕或极低分辨率适配**：
   - 目前在 1080P、2K、4K 屏幕上全天课程无需滚动即可完整显示；
   - 若用户使用的是 1366x768 等极低分辨率小屏幕笔记本，可考虑在 `ScheduleSidebar.qml` 中增加根据 `Screen.height` 动态缩放字体与内边距的计算系数；
2. **更多液态玻璃预设风格**：
   - 可在设置页面中进一步扩展深色（Dark Liquid）、极光浅色（Light Frosty）等更多材质主题；
3. **插件生态开发**：
   - 插件核心位于 `src/core/plugin/`，可根据需要继续开发更多桌面挂件插件（如天气、备忘倒计时等）。

---

## 五、 本地开发与重新打包指南 (Developer Guide)

### 1. 搭建开发环境
```powershell
# 1. 建议使用 Python 3.11 或 3.13 64位环境
python -m venv .venv
.venv\Scripts\activate

# 2. 安装项目依赖
pip install -r requirements.txt
pip install pyinstaller loguru pefile
```

### 2. 启动与调试开发
```powershell
# 直接从源码启动
python src/app.py
```

### 3. 一键重新打包发布
```powershell
# 运行打包脚本（会自动执行 PyInstaller、依赖镜像补全与 ZIP 归档）
python scripts/build_exe.py

# 打包产物输出路径：
# 绿色解压目录: dist/Class Widgets 2/
# 分发压缩包: dist/ClassWidgets-2-Windows.zip
```
