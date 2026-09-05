# Learning: PySide6 + QML 桌面应用 Windows EXE 打包与路径解析最佳实践

## 1. 核心要点
- **问题**：在源码中直接使用 `Path(__file__).parents[1]` 计算应用程序根目录。
- **后果**：通过 PyInstaller 打包为 EXE 后，Python 源码可能被归档或放在虚拟运行环境，导致 `__file__` 解析出非预期路径，造成静态资源（QML、素材、主题、配置文件）找不到而闪退。
- **防御机制 (One-Strike Permanent Defense)**：
  在路径管理模块（如 `src/core/directories.py`）中必须使用 `sys.frozen` 分支判定：
  ```python
  if getattr(sys, "frozen", False):
      ROOT_PATH = Path(sys.executable).parent
      SRC_PATH = ROOT_PATH / "src"
  else:
      SRC_PATH = Path(__file__).parents[1]
      ROOT_PATH = SRC_PATH.parent
  ```
  这样打包后的 EXE 无论移动到任何机器或目录，均能精准寻址自身同级的资源文件。

## 2. 打包规格与体积优化
- **目录模式（Onedir）优于单文件模式（Onefile）**：
  GUI 桌面小组件资源丰富（包含几十个 QML、大量图片、音效与 Qt 插件动态库）。单文件模式每次双击启动都需要将近百兆文件解压到用户临时目录（`AppData\Local\Temp\_MEIxxxx`），导致启动严重卡顿（5~10秒），且退出时残留临时垃圾。
  目录模式支持秒开（直接就地加载 DLL 与 QML），用户体验极佳。
- **动态库安全清理**：
  依据官方裁剪表清理 PySide6 中未使用的 3D、WebEngine、PDF 等冗余动态库，可减少数十兆体积。
