import multiprocessing
import os
import sys
import time


def wait_for_process_exit(arguments: list[str]) -> list[str]:
    """Wait for the previous CW2 process before initializing Qt and plugins."""
    if "--wait-for-pid" not in arguments:
        return arguments

    index = arguments.index("--wait-for-pid")
    try:
        pid = int(arguments[index + 1])
    except (IndexError, ValueError):
        return arguments[:index] + arguments[index + 2:]

    remaining = arguments[:index] + arguments[index + 2:]
    if pid == os.getpid():
        return remaining

    while True:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return remaining
        except PermissionError:
            pass
        time.sleep(0.1)

# Add the project root to Python path (parent directory of src)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, project_root)

# 在 Windows (Python 3.8+) 下，将 PySide6 目录加入 DLL 搜索路径，确保 QML 插件能找到 Qt 核心依赖库
if sys.platform == "win32" and hasattr(os, "add_dll_directory"):
    try:
        import PySide6
        pyside6_dir = os.path.dirname(PySide6.__file__)
        if os.path.isdir(pyside6_dir):
            os.add_dll_directory(pyside6_dir)
    except Exception:
        pass

# 避免在 Windows GBK 控制台下输出 emoji (如 RinUI 的 ✨) 时触发 UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.core import AppCentral
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    multiprocessing.freeze_support()
    sys.argv[1:] = wait_for_process_exit(sys.argv[1:])
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    instance = AppCentral()
    instance.run()
    app.exec()
