# PyInstaller + PySide6 Windows 平台插件初始化失败深度防御机制

## 故障现象
目标电脑（特别是全新系统、机房电脑、未安装开发环境的纯净 Windows）解压运行或用 cmd 打开时弹出：
```
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
Available platform plugins are: direct2d, minimal, offscreen, windows.
```
或者双击 exe 毫无反应/闪退。

## 根因深剖 (Deep Root Causes)
1. **纯净环境缺少 VC++ 运行时，且 PyInstaller 依赖未平铺在根目录**：
   - 纯净机器的 `C:\Windows\System32` 没有 `MSVCP140.dll` 等 Visual C++ 2015-2022 运行时库；
   - PyInstaller 默认将 `MSVCP140*.dll`、`Qt6Core.dll`、`Qt6Gui.dll` 收集在 `PySide6\` 子文件夹内，而未放置在应用根目录；
   - 当 Windows 系统装载器加载 `platforms\qwindows.dll` 平台插件时，系统按标准搜索顺序（只在 `platforms/`、应用根目录和 `System32` 中）查找导入项（`MSVCP140.dll`、`Qt6Core.dll`、`Qt6Gui.dll`），因它们全在 `PySide6\` 子目录中而直接报 **WinError 126 (ERROR_MOD_NOT_FOUND)**。
2. **`os.add_dll_directory` 的局限性**：
   - Python 3.8+ 的 `os.add_dll_directory` 只对显式包含 `LOAD_LIBRARY_SEARCH_USER_DIRS` 标志的 `LoadLibraryEx` 生效；
   - Qt 底层 C++ 运行时解析平台插件时并不传递该标志，导致操作系统完全忽略 `os.add_dll_directory` 注册的目录。
3. **工作目录 (CWD) 偏移问题**：
   - 用户在 cmd 下从其他路径（如 `C:\Users\xxx>`）执行 exe 时，CWD 仍然是终端路径，导致基于相对路径的资源检索失效。
4. **双击静默闪退假象**：
   - 程序配置了 `--noconsole` 模式，纯净机早期发生依赖错误或 Python 顶层异常时，无控制台接管，Windows 会静默终止进程，让用户以为“双击打不开”。

## 永久防御规范 (Defense Rules)
1. **底层 Win32 API `SetDllDirectoryW` 注入**：
   - 在 `src/app.py` 最顶端调用 `ctypes.windll.kernel32.SetDllDirectoryW(pyside_candidate)`，全局生效，让 Windows 装载器在解析所有后续 DLL 依赖时无条件强制搜索 `PySide6` 目录。
2. **工作目录强制重置**：
   - 启动初期若处于冻结环境，立即执行 `os.chdir(base_dir)`，确保无论从哪个路径或终端启动，当前工作目录始终为应用根目录。
3. **依赖完全自包含（Self-contained）镜像**：
   - 打包脚本自动将 `PySide6/` 下全部关键 VC++ 运行时（`MSVCP140*.dll`、`VCRUNTIME140*.dll`）、图形渲染库（`opengl32sw.dll`、`d3dcompiler_47.dll`）以及 Qt 核心库（`Qt6Core.dll`、`Qt6Gui.dll`）同步镜像至应用根目录及 `platforms/` 目录。
4. **全局异常原生对话框拦截**：
   - 在 `__main__` 顶层包裹 `try...except`，发生任何未捕获致命错误时，调用 `MessageBoxW` 弹出完整堆栈对话框，杜绝静默退出。
5. **配套便携安全启动器与诊断启动器**：
   - 打包产物根目录同时生成 `启动 Class Widgets.bat`（一键带环境拉起）与 `启动并排查故障(显示控制台).bat`（开启 `QT_DEBUG_PLUGINS=1` 并保留错误提示暂停）。
