#include <windows.h>
#include <stdio.h>
#include <shlwapi.h>

#pragma comment(lib, "shlwapi.lib")
#pragma comment(lib, "user32.lib")

int main() {
    wchar_t exeDir[MAX_PATH] = { 0 };
    wchar_t targetExe[MAX_PATH] = { 0 };
    wchar_t cmdLine[MAX_PATH * 2] = { 0 };
    wchar_t oldPath[8192] = { 0 };
    wchar_t newPath[16384] = { 0 };
    HANDLE hReadPipe = NULL;
    HANDLE hWritePipe = NULL;
    SECURITY_ATTRIBUTES sa;

    GetModuleFileNameW(NULL, exeDir, MAX_PATH);
    PathRemoveFileSpecW(exeDir);
    SetCurrentDirectoryW(exeDir);

    printf("=================================================================\n");
    printf("       Class Widgets 2 Qt 插件深度诊断与错误抓取工具\n");
    printf("=================================================================\n\n");

    // 1. 设置环境变量
    SetEnvironmentVariableW(L"QT_DEBUG_PLUGINS", L"1");
    SetEnvironmentVariableW(L"QT_LOGGING_TO_CONSOLE", L"1");
    SetEnvironmentVariableW(L"QT_PLUGIN_PATH", NULL);
    SetEnvironmentVariableW(L"QT_QPA_PLATFORM_PLUGIN_PATH", NULL);
    SetDllDirectoryW(exeDir);

    GetEnvironmentVariableW(L"PATH", oldPath, 8192);
    wsprintfW(newPath, L"%s;%s\\PySide6;%s\\PySide6\\plugins;%s\\platforms;%s", exeDir, exeDir, exeDir, exeDir, oldPath);
    SetEnvironmentVariableW(L"PATH", newPath);

    wsprintfW(targetExe, L"%s\\Class Widgets 2.exe", exeDir);
    if (GetFileAttributesW(targetExe) == INVALID_FILE_ATTRIBUTES) {
        wsprintfW(targetExe, L"%s\\ClassWidgets.exe", exeDir);
    }

    if (GetFileAttributesW(targetExe) == INVALID_FILE_ATTRIBUTES) {
        printf("[ERROR] Cannot find 'Class Widgets 2.exe' in current directory!\n");
        system("pause");
        return 1;
    }

    // 2. 创建管道捕获 GUI 程序的输出
    sa.nLength = sizeof(SECURITY_ATTRIBUTES);
    sa.bInheritHandle = TRUE;
    sa.lpSecurityDescriptor = NULL;

    if (!CreatePipe(&hReadPipe, &hWritePipe, &sa, 0)) {
        printf("[ERROR] Failed to create pipe.\n");
        return 1;
    }
    SetHandleInformation(hReadPipe, HANDLE_FLAG_INHERIT, 0);

    STARTUPINFOW si;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    si.hStdOutput = hWritePipe;
    si.hStdError = hWritePipe;
    si.dwFlags |= STARTF_USESTDHANDLES;

    PROCESS_INFORMATION pi;
    ZeroMemory(&pi, sizeof(pi));

    wsprintfW(cmdLine, L"\"%s\"", targetExe);

    printf("[INFO] Launching Class Widgets 2 with QT_DEBUG_PLUGINS=1 ...\n");
    printf("[INFO] Output will be displayed below and saved to 'qt_debug_log.txt'\n");
    printf("-----------------------------------------------------------------\n\n");

    FILE *logFile = fopen("qt_debug_log.txt", "w");

    BOOL success = CreateProcessW(
        targetExe,
        cmdLine,
        NULL,
        NULL,
        TRUE, // 必须继承句柄
        0,
        NULL,
        exeDir,
        &si,
        &pi
    );

    CloseHandle(hWritePipe); // 父进程关闭写端

    if (!success) {
        printf("[ERROR] CreateProcess failed. Error code: %u\n", GetLastError());
        CloseHandle(hReadPipe);
        if (logFile) fclose(logFile);
        system("pause");
        return 1;
    }

    // 3. 循环读取子进程的输出
    char buffer[1024];
    DWORD bytesRead;
    while (ReadFile(hReadPipe, buffer, sizeof(buffer) - 1, &bytesRead, NULL) && bytesRead > 0) {
        buffer[bytesRead] = '\0';
        printf("%s", buffer);
        fflush(stdout);
        if (logFile) {
            fputs(buffer, logFile);
            fflush(logFile);
        }
    }

    CloseHandle(hReadPipe);
    WaitForSingleObject(pi.hProcess, INFINITE);

    DWORD exitCode = 0;
    GetExitCodeProcess(pi.hProcess, &exitCode);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    if (logFile) fclose(logFile);

    printf("\n-----------------------------------------------------------------\n");
    printf("[INFO] Process exited with code: %d (0x%X)\n", (int)exitCode, exitCode);
    printf("[INFO] Full log saved to: qt_debug_log.txt\n");
    printf("=================================================================\n");
    system("pause");
    return 0;
}
