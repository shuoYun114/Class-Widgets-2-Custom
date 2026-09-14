# Windows 兼容性垫片与原生启动器 (Windows Compatibility Shims & Launcher)

## 1. 包含文件说明

- **`api-ms-win-shcore-scaling-l1-1-1.dll`**:
  - **作用**：Qt 6.8 的 `platforms/qwindows.dll` 链接了 `api-ms-win-shcore-scaling-l1-1-1.dll`（导入 `GetDpiForMonitor`）。Windows 10 1703 (Build 15063) 及更早版本仅包含 `SHCore.dll`，无此 API Set。此 DLL 是纯静态（`/MT`）编译的转发垫片，将调用安全路由至系统的 `SHCore.dll`，彻底根治 Win10 1703 下 Qt 抛出 `no Qt platform plugin could be initialized` 错误。
  - **依赖**：纯静态，仅链接底层 `KERNEL32.dll`，无需任何 VC++ 动态运行库。
  - **源码**：`shim.c`、`shim.def`。

- **`cwuiauto.dll` 与 `qwindows-win10-1703-patched.dll`**:
  - **作用**：Win10 1703 系统的 `UIAutomationCore.dll` 缺少 `UiaRaiseNotificationEvent`。修补版 `qwindows` 将 `UIAutomationCore.dll` 重定向链接至 `cwuiauto.dll`，由 `cwuiauto.dll` 拦截并安全返回，其他正常接口转发给系统原生 `UIAutomationCore.dll`。彻底根治入口点缺失导致的平台插件无法初始化。
  - **依赖**：纯静态（`/MT`），无需外部 VC++ 运行时。
  - **源码**：`cwuiauto.c`、`cwuiauto.def`。

- **`ClassWidgets.exe`**:
  - **作用**：基于 C 语言编写的轻量级原生桌面启动器，内嵌应用图标。支持智能环境变量净化、PATH 注入，并在老旧 Windows 版本（如 Win10 1703）下自动配置 `-platform windows:fontengine=gdi` 以防止字体渲染丢失。
  - **依赖**：纯静态，仅链接系统基础 API，无需任何外部运行库。
  - **源码**：`launcher.c`。
