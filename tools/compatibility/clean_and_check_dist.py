import os

dist_dir = r"D:\PYTHON\classwiget\dist\Class Widgets 2"

# 1. 查找并删除无用或乱码文件
for fname in os.listdir(dist_dir):
    fpath = os.path.join(dist_dir, fname)
    if fname.endswith(".bat"):
        os.remove(fpath)
        print(f"Removed bat: {fname}")
    elif fname in ["qwindows_test.dll", "qt_debug_log.txt"]:
        os.remove(fpath)
        print(f"Removed temp file: {fname}")

# 2. 检查关键文件
critical_files = [
    "ClassWidgets.exe",
    "Class Widgets 2.exe",
    "diag.exe",
    "cwuiauto.dll",
    "platforms/qwindows.dll",
    "platforms/cwuiauto.dll",
    "PySide6/plugins/platforms/qwindows.dll",
    "PySide6/plugins/platforms/cwuiauto.dll",
    "plugins/com.classwidgets.sidebar/cwplugin.json",
    "vc_redist.x64.exe"
]

print("\n=== Checking Critical Files ===")
all_ok = True
for cf in critical_files:
    p = os.path.join(dist_dir, cf)
    if os.path.exists(p):
        print(f"  [OK] {cf} ({os.path.getsize(p)} bytes)")
    else:
        print(f"  [MISSING] {cf}")
        all_ok = False

print(f"\nAll Critical Files Ready: {all_ok}")
