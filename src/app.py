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

# 持久保留 DLL 目录句柄，防止被 Python 垃圾回收导致 RemoveDllDirectory 被自动触发
_DLL_HANDLES = []

# 在 Windows (Python 3.8+) 下，将 PySide6 及关键目录加入 DLL 搜索路径并设置插件环境变量
if sys.platform == "win32":
    candidate_dirs = []
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
        candidate_dirs.extend([
            base_dir,
            os.path.join(base_dir, "PySide6"),
            os.path.join(base_dir, "shiboken6"),
        ])
    else:
        try:
            import PySide6
            pyside_base = os.path.dirname(PySide6.__file__)
            candidate_dirs.append(pyside_base)
            shiboken_base = os.path.join(os.path.dirname(pyside_base), "shiboken6")
            if os.path.isdir(shiboken_base):
                candidate_dirs.append(shiboken_base)
        except Exception:
            pass

    # 1. 注册至 Windows AddDllDirectory (保持全局句柄引用，严防垃圾回收)
    if hasattr(os, "add_dll_directory"):
        for d in candidate_dirs:
            if os.path.isdir(d):
                try:
                    handle = os.add_dll_directory(d)
                    _DLL_HANDLES.append(handle)
                except Exception:
                    pass

    # 2. 注入至系统 PATH 前端，供 LoadLibrary 标准回退搜索
    existing_path = os.environ.get("PATH", "")
    new_dirs = [d for d in candidate_dirs if os.path.isdir(d) and d not in existing_path]
    if new_dirs:
        os.environ["PATH"] = os.pathsep.join(new_dirs) + os.pathsep + existing_path

    # 3. 显式设置 Qt 插件与平台插件搜索路径
    for d in candidate_dirs:
        plugins_candidate = os.path.join(d, "plugins")
        if os.path.isdir(plugins_candidate):
            os.environ.setdefault("QT_PLUGIN_PATH", plugins_candidate)
            platforms_candidate = os.path.join(plugins_candidate, "platforms")
            if os.path.isdir(platforms_candidate):
                os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", platforms_candidate)
            break


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
