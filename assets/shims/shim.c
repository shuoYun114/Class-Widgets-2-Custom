#include <windows.h>

static HMODULE hShcore = NULL;

typedef HRESULT (WINAPI *PFN_GetDpiForMonitor)(HMONITOR, int, UINT*, UINT*);
typedef HRESULT (WINAPI *PFN_GetProcessDpiAwareness)(HANDLE, int*);
typedef HRESULT (WINAPI *PFN_SetProcessDpiAwareness)(int);
typedef HRESULT (WINAPI *PFN_GetScaleFactorForMonitor)(HMONITOR, int*);

static PFN_GetDpiForMonitor pfnGetDpiForMonitor = NULL;
static PFN_GetProcessDpiAwareness pfnGetProcessDpiAwareness = NULL;
static PFN_SetProcessDpiAwareness pfnSetProcessDpiAwareness = NULL;
static PFN_GetScaleFactorForMonitor pfnGetScaleFactorForMonitor = NULL;

static void EnsureShCoreLoaded(void) {
    if (!hShcore) {
        hShcore = LoadLibraryW(L"SHCore.dll");
        if (hShcore) {
            pfnGetDpiForMonitor = (PFN_GetDpiForMonitor)GetProcAddress(hShcore, "GetDpiForMonitor");
            pfnGetProcessDpiAwareness = (PFN_GetProcessDpiAwareness)GetProcAddress(hShcore, "GetProcessDpiAwareness");
            pfnSetProcessDpiAwareness = (PFN_SetProcessDpiAwareness)GetProcAddress(hShcore, "SetProcessDpiAwareness");
            pfnGetScaleFactorForMonitor = (PFN_GetScaleFactorForMonitor)GetProcAddress(hShcore, "GetScaleFactorForMonitor");
        }
    }
}

__declspec(dllexport) HRESULT WINAPI GetDpiForMonitor(HMONITOR hmonitor, int dpiType, UINT *dpiX, UINT *dpiY) {
    EnsureShCoreLoaded();
    if (pfnGetDpiForMonitor) {
        return pfnGetDpiForMonitor(hmonitor, dpiType, dpiX, dpiY);
    }
    if (dpiX) *dpiX = 96;
    if (dpiY) *dpiY = 96;
    return S_OK;
}

__declspec(dllexport) HRESULT WINAPI GetProcessDpiAwareness(HANDLE hprocess, int *value) {
    EnsureShCoreLoaded();
    if (pfnGetProcessDpiAwareness) {
        return pfnGetProcessDpiAwareness(hprocess, value);
    }
    if (value) *value = 2; // Process_Per_Monitor_DPI_Aware
    return S_OK;
}

__declspec(dllexport) HRESULT WINAPI SetProcessDpiAwareness(int value) {
    EnsureShCoreLoaded();
    if (pfnSetProcessDpiAwareness) {
        return pfnSetProcessDpiAwareness(value);
    }
    return S_OK;
}

__declspec(dllexport) HRESULT WINAPI GetScaleFactorForMonitor(HMONITOR hMon, int *pScale) {
    EnsureShCoreLoaded();
    if (pfnGetScaleFactorForMonitor) {
        return pfnGetScaleFactorForMonitor(hMon, pScale);
    }
    if (pScale) *pScale = 100; // 100% scale
    return S_OK;
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    return TRUE;
}
