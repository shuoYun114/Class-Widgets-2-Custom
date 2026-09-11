import os
import subprocess

work_dir = r"C:\Users\Admin\.gemini\antigravity\brain\6c70c508-e368-4292-82e0-7ab3441ff35a\scratch"
vcvars = r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
out_dll = os.path.join(work_dir, "cwuiauto.dll")

cmd = f'call "{vcvars}" && cd /d "{work_dir}" && cl.exe /utf-8 /O2 /MT /LD /Fe:"{out_dll}" cwuiauto.c /DEF:cwuiauto.def /link /MACHINE:X64 oleaut32.lib user32.lib'

res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print("Compiler STDOUT:\n", res.stdout)
print("Compiler STDERR:\n", res.stderr)

if os.path.exists(out_dll) and os.path.getsize(out_dll) > 0:
    print(f"SUCCESS! Generated {out_dll}, size: {os.path.getsize(out_dll)}")
else:
    print("FAILED!")
