# PyInstaller + PySide6 Windows 平台插件初始化失败深度防御机制

## 故障现象
运行打包后的 Windows 可执行程序时弹出：
This application failed to start because no Qt platform plugin could be initialized.
Available platform plugins are: direct2d, minimal, offscreen, windows.

## 根因深剖 (Root Cause)
1. os.add_dll_directory 句柄瞬时析构：未持久引用导致垃圾回收自动触发 RemoveDllDirectory；
2. 缺失 qt.conf 与根目录 platforms 平台插件镜像；
3. 依赖裁剪误删 opengl32sw.dll 导致缺少软件 OpenGL 驱动保底。

## 永久防御规范 (Defense Rules)
1. 全局持久保留 os.add_dll_directory 引用 (_DLL_HANDLES)；
2. 系统 PATH 与 QT_PLUGIN_PATH 三位一体显式设置；
3. 打包脚本生成 qt.conf 并镜像根目录 platforms/；
4. 保留 opengl32sw.dll 兜底显卡渲染。
