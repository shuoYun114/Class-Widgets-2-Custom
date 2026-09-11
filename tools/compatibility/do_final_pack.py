import os
import zipfile
import shutil

src_dir = r"D:\PYTHON\classwiget\dist\Class Widgets 2"
out_zip = r"C:\Users\Admin\Desktop\ClassWidgets-2-Win10-最新终极修复版.zip"
station_zip = r"d:\PYTHON\classwiget\release_station\files\ClassWidgets-2-Win10-最新终极修复版.zip"

print("Packing into:", out_zip)
with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, src_dir)
            arcname = os.path.join("Class Widgets 2", rel_path)
            z.write(full_path, arcname)

shutil.copy2(out_zip, station_zip)
print("SUCCESS! File size:", os.path.getsize(out_zip))
