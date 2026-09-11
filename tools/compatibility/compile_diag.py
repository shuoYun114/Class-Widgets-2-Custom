import os
import subprocess

work_dir = r"C:\Users\Admin\.gemini\antigravity\brain\6c70c508-e368-4292-82e0-7ab3441ff35a\scratch"
vcvars = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
out_exe = os.path.join(work_dir, "diag.exe")

cmd = f'call "{vcvars}" && cd /d "{work_dir}" && cl.exe /utf-8 /O2 /MT /Fe:"{out_exe}" diag.c /link /SUBSYSTEM:CONSOLE shlwapi.lib user32.lib'

res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print("Compiler STDOUT:", res.stdout)
print("Compiler STDERR:", res.stderr)

if os.path.exists(out_exe) and os.path.getsize(out_exe) > 0:
    print("SUCCESS! Generated:", out_exe, "Size:", os.path.getsize(out_exe))
else:
    print("FAILED!")
