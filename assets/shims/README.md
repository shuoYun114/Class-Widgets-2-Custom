# Windows 兼容性垫片与原生启动器 (Windows Compatibility Shims & Launcher)

## 1. 包含文件说明

- **`api-ms-win-shcore-scaling-l1-1-1.dll`**:
  - **作用**：Qt 6.8 的 `platforms/qwindows.dll` 链接了 `api-ms-win-shcore-scaling-l1-1-1.dll`（导入 `GetDpiForMonitor`）。Windows 10 1703 (Build 15063) 及更早版本仅包含 `SHCore.dll`，无此 API Set。此 DLL 是纯静态（`/MT`）编译的转发垫片，将调用安全路由至系统的 `SHCore.dll`，彻底根治 Win10 1703 下 Qt 抛出 `no Qt platform plugin could be initialized` 错误。
  - **依赖**：纯静态，仅链接底层 `KERNEL32.dll`，无需任何 VC++ 动态运行库。
  - **源码**：`shim.c`、`shim.def`。

- **`ClassWidgets.exe`**:
  - **作用**：基于 C 语言编写的轻量级原生桌面启动器，内嵌应用图标。支持智能环境变量净化、PATH 注入，并在老旧 Windows 版本（如 Win10 1703）下自动配置 `-platform windows:fontengine=gdi` 以防止字体渲染丢失。
  - **依赖**：纯静态，仅链接系统基础 API，无需任何外部运行库。
  - **源码**：`launcher.c`。

## 2. 编译指南（如需重新编译）

在安装有 Visual Studio（MSVC x64 环境）的终端下执行：

```cmd
:: 1. 编译兼容垫片 DLL
cl.exe /O2 /MT /LD shim.c /link /OUT:"api-ms-win-shcore-scaling-l1-1-1.dll" user32.lib kernel32.lib

:: 2. 编译原生启动器 EXE（需配合 rc.exe 编译应用图标）
rc.exe /fo launcher.res launcher.rc
cl.exe /utf-8 /O2 /MT /Fe:"ClassWidgets.exe" launcher.c launcher.res /link /SUBSYSTEM:WINDOWS shlwapi.lib user32.lib shell32.lib
```
