# -*- coding: utf-8 -*-
"""
Class-Widgets-2 自动化 Windows EXE 打包脚本
整合 PyInstaller、资源映射、动态库裁剪与归档压缩。
"""
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

# 控制台编码保护，避免 Windows GBK 终端报错
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


def run_build(skip_pyinstaller=False):
    root_dir = Path(__file__).resolve().parents[1]
    os.chdir(root_dir)
    print(f"[1/4] 当前工作目录: {root_dir}")

    dist_dir = root_dir / "dist" / "Class Widgets 2"
    exe_file = dist_dir / "Class Widgets 2.exe"

    # 自动释放被旧实例占用的 exe 与动态库
    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", "Class Widgets 2.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass

    if not skip_pyinstaller:
        # 1. 确保必要目录和数据存在
        assets_icon = root_dir / "assets" / "images" / "logo.ico"
        app_entry = root_dir / "src" / "app.py"

        if not app_entry.exists():
            print(f"错误: 入口文件不存在: {app_entry}")
            sys.exit(1)

        # 2. 组装 PyInstaller 命令参数
        sep = os.pathsep
        add_data_args = [
            f"--add-data=src/qml{sep}src/qml",
            f"--add-data=src/plugins{sep}src/plugins",
            f"--add-data=src/themes{sep}src/themes",
            f"--add-data=assets{sep}assets",
            f"--add-data=configs{sep}configs",
            f"--add-data=LICENSE{sep}.",
        ]

        cmd = [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconsole",
            "--noupx",
            f"--icon={str(assets_icon)}",
            *add_data_args,
            "--paths=.",
            "--paths=src",
            "--contents-directory=.",
            "--collect-all=RinUI",
            "--name=Class Widgets 2",
            "--noconfirm",
            "--clean",
            str(app_entry),
        ]

        print("[2/4] 开始执行 PyInstaller 打包构建...")
        print(" ".join(cmd))
        res = subprocess.run(cmd)
        if res.returncode != 0:
            print(f"错误: PyInstaller 构建失败，退出码: {res.returncode}")
            sys.exit(res.returncode)

    if not exe_file.exists():
        print(f"错误: 生成的可执行文件未找到: {exe_file}")
        sys.exit(1)
    print(f"[OK] 成功验证可执行文件: {exe_file}")

    # 2.5 写入 qt.conf 并部署根目录 platforms 平台插件镜像，保障任何纯净 Windows 环境绝对可运行
    qt_conf_file = dist_dir / "qt.conf"
    qt_conf_content = "[Paths]\nPrefix = .\nPlugins = PySide6/plugins\nImports = PySide6/qml\nQml2Imports = PySide6/qml\n"
    with open(qt_conf_file, "w", encoding="utf-8") as f:
        f.write(qt_conf_content)
    print(f"[OK] 成功生成 Qt 配置文件: {qt_conf_file}")

    # 将平台插件同时镜像至应用程序根目录 platforms，提供双保险
    src_platforms = dist_dir / "PySide6" / "plugins" / "platforms"
    dst_platforms = dist_dir / "platforms"
    if src_platforms.exists():
        if dst_platforms.exists():
            shutil.rmtree(dst_platforms)
        shutil.copytree(src_platforms, dst_platforms)
        print(f"[OK] 成功同步平台插件至根目录: {dst_platforms}")

    # 2.6 生成“创建桌面快捷方式.bat”，引导用户安全创建快捷方式，防止将 exe 单独拖离解压目录
    shortcut_bat = dist_dir / "创建桌面快捷方式.bat"
    shortcut_bat_content = (
        "@echo off\r\n"
        "chcp 65001 >nul\r\n"
        "echo 正在为 Class Widgets 2 创建桌面快捷方式...\r\n"
        "powershell -NoProfile -Command \"$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'Class Widgets 2.lnk')); $s.TargetPath = [System.IO.Path]::Combine($PSScriptRoot, 'Class Widgets 2.exe'); $s.WorkingDirectory = $PSScriptRoot; $s.Save()\"\r\n"
        "echo [成功] 桌面快捷方式已成功创建到您的桌面！\r\n"
        "ping 127.0.0.1 -n 2 >nul\r\n"
    )
    with open(shortcut_bat, "w", encoding="gbk", errors="ignore") as f:
        f.write(shortcut_bat_content)
    print(f"[OK] 成功生成桌面快捷方式助手: {shortcut_bat}")



    # 3. 冗余 Qt 动态库安全裁剪 (依据官方 scripts/qt_files_clean-Windows.json)
    clean_json = root_dir / "scripts" / "qt_files_clean-Windows.json"
    pyside_dir = dist_dir / "PySide6"
    if clean_json.exists() and pyside_dir.exists():
        print("[3/4] 清理未使用的 PySide6 冗余模块以优化体积...")
        try:
            with open(clean_json, "r", encoding="utf-8") as f:
                clean_list = json.load(f)
            cleaned_count = 0
            for item in clean_list:
                item_path = pyside_dir / item
                if item_path.is_file():
                    item_path.unlink()
                    cleaned_count += 1
                elif item_path.is_dir():
                    shutil.rmtree(item_path, ignore_errors=True)
                    cleaned_count += 1
            print(f"[OK] 已清理 {cleaned_count} 个未被引用的冗余 Qt 库/文件")
        except Exception as e:
            print(f"跳过清理 (非致命): {e}")
    else:
        print("[3/4] 跳过动态库裁剪 (直接保留完整依赖)")

    # 3.5 纯净 Windows 依赖加固：同步镜像所有关键 VC++ 运行时与 Qt 核心 DLL 至根目录和 platforms 目录
    # 彻底杜绝纯净机（无 VC++ Redistributable）下 qwindows.dll 报告 Error 126
    if pyside_dir.exists():
        synced_dlls = 0
        for dll_file in pyside_dir.glob("*.dll"):
            target_file = dist_dir / dll_file.name
            if not target_file.exists():
                shutil.copy2(dll_file, target_file)
                synced_dlls += 1
        print(f"[OK] 成功镜像 {synced_dlls} 个关键 DLL 到应用根目录，达成完全自包含")

        # 将平台插件的核心前置依赖也镜像至 platforms 目录
        dst_platforms = dist_dir / "platforms"
        if dst_platforms.exists():
            for critical_name in ["MSVCP140.dll", "MSVCP140_1.dll", "MSVCP140_2.dll", "VCRUNTIME140.dll", "VCRUNTIME140_1.dll", "Qt6Core.dll", "Qt6Gui.dll"]:
                c_src = pyside_dir / critical_name
                c_dst = dst_platforms / critical_name
                if c_src.exists() and not c_dst.exists():
                    shutil.copy2(c_src, c_dst)
            print("[OK] 成功向 platforms 注入前置运行时依赖")

    # 3.6 生成便携安全启动器与诊断启动器（应对双击无响应或极端系统限制）
    launcher_bat = dist_dir / "启动 Class Widgets.bat"
    launcher_content = (
        "@echo off\r\n"
        "cd /d \"%~dp0\"\r\n"
        "set \"PATH=%~dp0;%~dp0PySide6;%PATH%\"\r\n"
        "start \"\" \"Class Widgets 2.exe\"\r\n"
    )
    with open(launcher_bat, "w", encoding="gbk", errors="ignore") as f:
        f.write(launcher_content)

    debug_bat = dist_dir / "启动并排查故障(显示控制台).bat"
    debug_content = (
        "@echo off\r\n"
        "chcp 65001 >nul\r\n"
        "cd /d \"%~dp0\"\r\n"
        "echo ========================================================\r\n"
        "echo 正在以诊断模式启动 Class Widgets 2...\r\n"
        "echo 如果出现任何启动异常或缺少插件，控制台将显示详细追踪日志\r\n"
        "echo ========================================================\r\n"
        "set \"PATH=%~dp0;%~dp0PySide6;%PATH%\"\r\n"
        "set QT_DEBUG_PLUGINS=1\r\n"
        "\"Class Widgets 2.exe\"\r\n"
        "if %errorlevel% neq 0 (\r\n"
        "    echo.\r\n"
        "    echo [错误提示] 程序异常退出，退出码: %errorlevel%\r\n"
        "    echo 请将上方出现的提示或错误信息截图提供给开发者排查。\r\n"
        "    echo.\r\n"
        "    pause\r\n"
        ")\r\n"
    )
    with open(debug_bat, "w", encoding="gbk", errors="ignore") as f:
        f.write(debug_content)
    print(f"[OK] 成功生成便捷启动器与诊断启动器")

    # 4. 压缩打包为 zip 文件便于分发
    zip_output = root_dir / "dist" / "ClassWidgets-2-Windows.zip"
    print(f"[4/4] 正在将分发目录压缩至 {zip_output} ...")
    if zip_output.exists():
        zip_output.unlink()

    with zipfile.ZipFile(zip_output, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(dist_dir)
                zf.write(full_path, arcname=str(Path("Class Widgets 2") / rel_path))

    zip_size_mb = zip_output.stat().st_size / (1024 * 1024)
    print(f"[SUCCESS] 打包与归档全部完成！")
    print(f"分发压缩包: {zip_output} ({zip_size_mb:.2f} MB)")
    print(f"免安装绿色文件夹: {dist_dir}")


if __name__ == "__main__":
    skip = "--skip-pyinstaller" in sys.argv
    run_build(skip_pyinstaller=skip)
