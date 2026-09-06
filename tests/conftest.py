# -*- coding: utf-8 -*-
import os
import sys

# 兼容 Windows GBK 终端下打印特殊字符（如 RinUI 的 emoji）
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def pytest_sessionfinish(session, exitstatus):
    # 如果所有测试全部通过，使用 os._exit(0) 避免 PySide6 在 Python 3.13 进程清理时的平台级析构异常
    if exitstatus == 0:
        os._exit(0)
