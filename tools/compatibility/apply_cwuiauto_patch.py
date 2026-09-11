import os
import shutil
from dump_imports_json import get_all_imports

base_dir = r"D:\PYTHON\classwiget\dist\Class Widgets 2"
scratch_dir = r"C:\Users\Admin\.gemini\antigravity\brain\6c70c508-e368-4292-82e0-7ab3441ff35a\scratch"
cwuiauto_dll = os.path.join(scratch_dir, "cwuiauto.dll")

# 1. 拷贝 cwuiauto.dll 到相关目录
target_dirs = [
    base_dir,
    os.path.join(base_dir, "platforms"),
    os.path.join(base_dir, "PySide6", "plugins", "platforms")
]

for d in target_dirs:
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, "cwuiauto.dll")
    shutil.copy2(cwuiauto_dll, dst)
    print(f"Copied cwuiauto.dll -> {dst}")

# 2. 查找所有包含 UIAutomationCore.DLL 的 DLL 并原地修补
target_files = [
    os.path.join(base_dir, "platforms", "qwindows.dll"),
    os.path.join(base_dir, "PySide6", "plugins", "platforms", "qwindows.dll"),
    os.path.join(base_dir, "platforms", "qdirect2d.dll"),
    os.path.join(base_dir, "PySide6", "plugins", "platforms", "qdirect2d.dll"),
    os.path.join(base_dir, "platforms", "qwindows_test.dll")
]

src_bytes = b"UIAutomationCore.DLL"  # 20 bytes: 18 chars + null or 20 chars
replacement = b"cwuiauto.dll\x00\x00\x00\x00\x00\x00\x00\x00"  # 20 bytes total

for fpath in target_files:
    if not os.path.exists(fpath):
        continue
    with open(fpath, "rb") as f:
        data = f.read()

    pos = data.find(b"UIAutomationCore.DLL")
    if pos == -1:
        # 可能是小写
        pos = data.lower().find(b"uiautomationcore.dll")
        if pos != -1:
            raw = data[pos:pos+20]
            print(f"Found lowercase/mixed {raw} in {fpath} at {hex(pos)}")
    
    if pos != -1:
        old_slice = data[pos:pos+20]
        # 确保替换长度精确一致
        new_data = data[:pos] + replacement[:len(old_slice)] + data[pos+len(old_slice):]
        with open(fpath, "wb") as f:
            f.write(new_data)
        print(f"Patched {fpath}: replaced {old_slice} with {replacement[:len(old_slice)]}")
    else:
        print(f"Pattern not found in {fpath}")

# 3. 验证修补后的导入表
print("\n=== Verifying imports of patched qwindows.dll ===")
qwin = os.path.join(base_dir, "platforms", "qwindows.dll")
imps = get_all_imports(qwin)
for dll, fns in imps.items():
    if "cwuiauto" in dll.lower() or "uiauto" in dll.lower():
        print(f"Imported DLL: {dll} ({len(fns)} functions)")
        for fn in fns:
            print(f"   {fn}")
