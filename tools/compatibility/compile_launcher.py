import os
import subprocess

work_dir = r"C:\Users\Admin\.gemini\antigravity\brain\6c70c508-e368-4292-82e0-7ab3441ff35a\scratch"
ico_path = r"D:\PYTHON\classwiget\assets\images\logo.ico"
vcvars = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"

rc_content = f'1 ICON "{ico_path.replace(chr(92), "/")}"\n'
rc_file = os.path.join(work_dir, "launcher.rc")
with open(rc_file, "w", encoding="utf-8") as f:
    f.write(rc_content)

out_exe = os.path.join(work_dir, "ClassWidgets.exe")

cmd = f'call "{vcvars}" && cd /d "{work_dir}" && rc.exe launcher.rc && cl.exe /utf-8 /O2 /MT /Fe:"{out_exe}" launcher.c launcher.res /link /SUBSYSTEM:WINDOWS shlwapi.lib user32.lib shell32.lib'

res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print("Compiler STDOUT:", res.stdout)
print("Compiler STDERR:", res.stderr)

if os.path.exists(out_exe) and os.path.getsize(out_exe) > 0:
    print("SUCCESS! Generated:", out_exe, "Size:", os.path.getsize(out_exe))
else:
    print("FAILED!")
