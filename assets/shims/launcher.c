#include <windows.h>
#include <shlwapi.h>

#pragma comment(lib, "shlwapi.lib")
#pragma comment(lib, "user32.lib")
#pragma comment(lib, "shell32.lib")

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    wchar_t exeDir[MAX_PATH] = { 0 };
    wchar_t targetExe[MAX_PATH] = { 0 };
    wchar_t cmdLine[MAX_PATH * 2] = { 0 };
    wchar_t oldPath[8192] = { 0 };
    wchar_t newPath[16384] = { 0 };
    wchar_t sysDir[MAX_PATH] = { 0 };
    wchar_t vcCheckPath[MAX_PATH] = { 0 };
    STARTUPINFOW si;
    PROCESS_INFORMATION pi;

    GetModuleFileNameW(NULL, exeDir, MAX_PATH);
    PathRemoveFileSpecW(exeDir);
    SetCurrentDirectoryW(exeDir);

    // 1. 检查是否安装了 VC++ 2015-2022 x64 运行库
    GetSystemDirectoryW(sysDir, MAX_PATH);
    wsprintfW(vcCheckPath, L"%s\\vcruntime140_1.dll", sysDir);
    if (GetFileAttributesW(vcCheckPath) == INVALID_FILE_ATTRIBUTES) {
        wchar_t vcInstaller[MAX_PATH] = { 0 };
        wsprintfW(vcInstaller, L"%s\\vc_redist.x64.exe", exeDir);
        if (GetFileAttributesW(vcInstaller) != INVALID_FILE_ATTRIBUTES) {
            int ret = MessageBoxW(
                NULL,
                L"检测到当前系统尚未安装【Microsoft Visual C++ 2015-2022 运行库】。\n这是导致 Qt 报错无法启动的主要原因。\n\n是否立即启动运行库安装程序？（安装只需 10 秒）",
                L"Class Widgets 2 环境检测",
                MB_ICONQUESTION | MB_YESNO
            );
            if (ret == IDYES) {
                ShellExecuteW(NULL, L"open", vcInstaller, NULL, exeDir, SW_SHOWNORMAL);
                return 0;
            }
        }
    }

    // 2. 清除外部 Qt 插件路径干扰
    SetEnvironmentVariableW(L"QT_PLUGIN_PATH", NULL);
    SetEnvironmentVariableW(L"QT_QPA_PLATFORM_PLUGIN_PATH", NULL);

    // 3. 强制启用 Windows 经典 GDI 字体引擎（解决 Win10 1703 字体消失且保证原生饱满粗细质感）
    SetEnvironmentVariableW(L"QT_QPA_PLATFORM", L"windows:fontengine=gdi");

    // 4. 清除旧版残废的软件光栅变量
    SetEnvironmentVariableW(L"QT_QUICK_BACKEND", NULL);
    SetEnvironmentVariableW(L"QT_OPENGL", NULL);

    // 5. 将当前目录注入 DLL 搜索链
    SetDllDirectoryW(exeDir);

    GetEnvironmentVariableW(L"PATH", oldPath, 8192);
    wsprintfW(newPath, L"%s;%s\\PySide6;%s\\PySide6\\plugins;%s\\platforms;%s", exeDir, exeDir, exeDir, exeDir, oldPath);
    SetEnvironmentVariableW(L"PATH", newPath);

    // 6. 查找主程序可执行文件
    wsprintfW(targetExe, L"%s\\Class Widgets 2.exe", exeDir);
    if (GetFileAttributesW(targetExe) == INVALID_FILE_ATTRIBUTES) {
        MessageBoxW(NULL, L"未在当前目录下找到 Class Widgets 2.exe，请确认安装包已完整解压！", L"Class Widgets 2 启动器", MB_ICONERROR);
        return 1;
    }

    // 命令行双重注入 -platform windows:fontengine=gdi
    wsprintfW(cmdLine, L"\"%s\" -platform windows:fontengine=gdi", targetExe);

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    if (CreateProcessW(targetExe, cmdLine, NULL, NULL, FALSE, 0, NULL, exeDir, &si, &pi)) {
        CloseHandle(pi.hProcess);
        CloseHandle(pi.hThread);
        return 0;
    }

    MessageBoxW(NULL, L"未能成功启动主程序进程。", L"Class Widgets 2 启动器", MB_ICONERROR);
    return 1;
}
