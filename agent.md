# Class Widgets 2 (Custom 定制版) Agent 核心指引规范

本文档为本项目（Class-Widgets-2-Custom）的核心开发与维护基准，任何参与本项目的 AI Agent 必须严格遵守以下原则与目标体系。

---

## 🎯 核心使命与最高优先级目标

本项目作为 Class-Widgets-2 的专属定制分支，核心使命明确划分为两大优先级目标，且**第一目标始终高于一切次要功能开发**：

### 🥇 第一目标（最高优先级）：确保软件在 Windows 10 1703 上无障碍稳定运行

> [!IMPORTANT]
> **无论进行任何代码修改、库升级或重新打包，绝对不能破坏 Windows 10 1703 (Build 15063) 及老版本 Windows 系统的兼容性！**

#### 1.1 Qt 平台插件崩溃防御 (No Qt platform plugin could be initialized)
- **双重故障根因（经过二进制实证深度剖析）**：
  1. **API Set 缺失**：Qt 6.8 默认编译的 Windows 平台插件 `platforms/qwindows.dll` 显式静态链接了动态缩放虚拟模块 `api-ms-win-shcore-scaling-l1-1-1.dll` 并导入 `GetDpiForMonitor`。Windows 10 1703 (Build 15063) 系统中仅有经典 `SHCore.dll`，不存在该 API Set 模块；
  2. **UIAutomationCore 接口缺失**：Win10 1703 系统的 `UIAutomationCore.dll` 缺少高版本 Windows 才引入的 `UiaRaiseNotificationEvent` 接口，而未修补的原版 `qwindows.dll` 导入了该函数，直接导致找不到过程入口点而加载失败。
- **防御机制与标准架构**：
  1. **双重兼容垫片固化**：
     - `api-ms-win-shcore-scaling-l1-1-1.dll`（`/MT` 纯静态编译，安全转发给 `SHCore.dll`）；
     - `cwuiauto.dll`（`/MT` 纯静态编译，拦截并安全响应 `UiaRaiseNotificationEvent`，转发有效接口给系统原生 `UIAutomationCore.dll`）；
     - 修补版平台插件 `qwindows-win10-1703-patched.dll`（将 `UIAutomationCore.dll` 重定向链接至 `cwuiauto.dll`）；
  2. **绝对基线铁律**：严禁追随 GitHub 官方上游更新重新打包覆写二进制库！必须以在虚拟机 Win10 1703 实测通过的黄金基线（包含修补版 qwindows.dll 与 cwuiauto.dll）为基准，仅在应用层/QML 层进行增量功能演进；
  3. **VC++ 运行库加固**：分发包中必须将所有关键 VC++ 运行时（`MSVCP140*.dll`, `VCRUNTIME140*.dll`）和 Qt 核心 DLL 镜像至根目录与 `platforms/`，彻底达成完全自包含，杜绝纯净虚拟机环境崩溃。

#### 1.2 低版本 DirectWrite 缺失与文字隐形防御
- **故障根因**：
  Windows 10 1709 (Build 16299) 之前版本缺失 DirectWrite `IDWriteFactory6` 接口，Qt 6.8 默认的 DirectWrite 字体引擎在 Win10 1703 初始化异常，导致 QML/Qt 文本无法渲染（文字透明或发虚）。
- **防御机制与标准架构**：
  1. **代码级自动降级**：`src/app.py` 入口在检测到 `win_ver.build < 16299` 时，自动强制追加 `-platform windows:fontengine=gdi` 参数并注入环境变量；
  2. **原生启动器双保险**：分发包提供 C 语言原生编写的 `ClassWidgets.exe`（`assets/shims/launcher.c`），在拉起主程序前净化环境并确保注入 GDI 字体引擎；
  3. **便捷批处理兜底**：提供 `启动 Class Widgets.bat` 与 `启动并排查故障(显示控制台).bat`，确保任意环境下均能安全拉起并输出诊断日志。

---

### 🥈 第二目标：定制与维护屏幕右侧边缘侧边课表栏 (Sidebar Schedule)

在保证 Win10 1703 绝对兼容的前提下，实现并持续打磨贴合教室大屏与日常桌面使用的屏幕右侧边缘侧边课表系统。

#### 2.1 核心功能架构
1. **当天课表竖条常驻 (Normal State)**：
   - 极简深色磨砂半透明贴边胶囊，自适应垂直居中于屏幕最右侧；
   - 自动计算当前时间对应课程，当前课程高亮突出并展示进度与上下课时间；
   - 悬浮气泡卡片：光标悬停时弹出浮动卡片展示完整教室、教师及详细时间。
2. **悬浮双按钮交互与防误触缓冲 (Hover Buttons)**：
   - 光标靠近竖条左侧边缘时平滑滑出“展开全周大面板”与“收起隐藏竖条”两个圆形按钮；
   - 具备 300ms 计时器防误触缓冲，离开后平滑淡出。
3. **全周课表矩阵大面板 (Expanded State)**：
   - 点击上方按钮向左平滑展开周一至周日全周网格课表大面板；
   - 支持桌面空白透明区域点击自动收回，操作区切换为单一收回按钮。
4. **贴边隐藏与呼出恢复胶囊 (Collapsed State)**：
   - 点击下方收起按钮，竖条平滑缩进至屏幕右边缘，仅露出一枚微型贴边小胶囊（`<` 图标）；
   - 平时极高透明度避免遮挡屏幕，光标靠近时动态高亮，点击平滑恢复当天竖条。
5. **教室大屏侧边栏尺寸与文字大小调节 (Big Screen Usability)**：
   - 针对教室大屏后排学生看课表的需求，侧边栏整体胶囊宽度支持 140px ~ 380px 动态调节（默认 160px）；
   - 课程名称与时间字号支持 10px ~ 32px 宽范围调节（默认 12px），课程卡片高度自适应，课程名称固定采用 DemiBold 粗体加粗；
   - 设置中心（General -> 课表侧边栏）提供“尺寸与文字大小 (大屏适配)”专属卡片组，滑块拖动实时防抖联动。
6. **动态鼠标穿透遮罩 (Window Mask & Interaction)**：
   - `WidgetsWindow.update_mask` 根据侧边栏当前实际展开、折叠、气泡弹窗状态精确计算 `QRegion` 遮罩；
   - 确保未被组件占用的全屏透明区域 100% 支持鼠标穿透操作底层窗口。

---

## 🛠️ 构建、打包与发布标准

1. **本地打包流程**：
   - 执行 `uv run python scripts/build_exe.py`；
   - 脚本必须全自动完成：PyInstaller 编译 -> 部署 `qt.conf` -> 同步 `platforms` -> 裁剪冗余 Qt 库 -> 镜像核心 VC 运行时 -> **注入 Win10 1703 兼容垫片与原生启动器** -> 生成便携/排障 bat 与快捷方式脚本 -> 归档生成 `dist/ClassWidgets-2-Windows.zip`。
2. **打包验证红线**：
   - 生成的 ZIP 压缩包内必须包含：
     - `Class Widgets 2/api-ms-win-shcore-scaling-l1-1-1.dll`
     - `Class Widgets 2/platforms/api-ms-win-shcore-scaling-l1-1-1.dll`
     - `Class Widgets 2/PySide6/api-ms-win-shcore-scaling-l1-1-1.dll`
     - `Class Widgets 2/PySide6/plugins/platforms/api-ms-win-shcore-scaling-l1-1-1.dll`
     - `Class Widgets 2/ClassWidgets.exe`
3. **GitHub Releases 发布规范**：
   - 使用 `gh release upload <tag> "dist/ClassWidgets-2-Windows.zip" --clobber` 覆盖更新。

---

## 📋 Git 提交与工程纪律规范

1. **增量微提交与实时推送**：
   - 每完成一个微功能或修复一个 bug，必须立即执行标准 Git 提交（如 `feat:`, `fix:`, `refactor:`, `docs:`）；
   - 每次修改后自动将提交 `git push` 到 GitHub 远程仓库，确保进度实时云端备份，随时可回退。
2. **实证优先与零猜测**：
   - 对技术判断和兼容性问题优先以实际二进制依赖（PE 导入导出表）、测试日志和虚拟机实测为准，严禁凭空假设。
3. **语言要求**：
   - 思考过程、对外回复、代码注释与开发文档一律使用简体中文。
