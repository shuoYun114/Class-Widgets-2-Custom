#include <windows.h>

static HMODULE hRealUia = NULL;

typedef BOOL (WINAPI *PFN_UiaClientsAreListening)(void);
typedef LRESULT (WINAPI *PFN_UiaReturnRawElementProvider)(HWND, WPARAM, LPARAM, void*);
typedef HRESULT (WINAPI *PFN_UiaHostProviderFromHwnd)(HWND, void**);
typedef HRESULT (WINAPI *PFN_UiaRaiseNotificationEvent)(void*, int, int, BSTR, BSTR);
typedef HRESULT (WINAPI *PFN_UiaRaiseAutomationPropertyChangedEvent)(void*, int, VARIANT, VARIANT);
typedef HRESULT (WINAPI *PFN_UiaRaiseAutomationEvent)(void*, int);

static PFN_UiaClientsAreListening pfnUiaClientsAreListening = NULL;
static PFN_UiaReturnRawElementProvider pfnUiaReturnRawElementProvider = NULL;
static PFN_UiaHostProviderFromHwnd pfnUiaHostProviderFromHwnd = NULL;
static PFN_UiaRaiseNotificationEvent pfnUiaRaiseNotificationEvent = NULL;
static PFN_UiaRaiseAutomationPropertyChangedEvent pfnUiaRaiseAutomationPropertyChangedEvent = NULL;
static PFN_UiaRaiseAutomationEvent pfnUiaRaiseAutomationEvent = NULL;

static void EnsureRealUiaLoaded(void) {
    if (!hRealUia) {
        wchar_t sysDir[MAX_PATH];
        if (GetSystemDirectoryW(sysDir, MAX_PATH) > 0) {
            wchar_t uiaPath[MAX_PATH];
            wsprintfW(uiaPath, L"%s\\UIAutomationCore.dll", sysDir);
            hRealUia = LoadLibraryW(uiaPath);
            if (hRealUia) {
                pfnUiaClientsAreListening = (PFN_UiaClientsAreListening)GetProcAddress(hRealUia, "UiaClientsAreListening");
                pfnUiaReturnRawElementProvider = (PFN_UiaReturnRawElementProvider)GetProcAddress(hRealUia, "UiaReturnRawElementProvider");
                pfnUiaHostProviderFromHwnd = (PFN_UiaHostProviderFromHwnd)GetProcAddress(hRealUia, "UiaHostProviderFromHwnd");
                pfnUiaRaiseNotificationEvent = (PFN_UiaRaiseNotificationEvent)GetProcAddress(hRealUia, "UiaRaiseNotificationEvent");
                pfnUiaRaiseAutomationPropertyChangedEvent = (PFN_UiaRaiseAutomationPropertyChangedEvent)GetProcAddress(hRealUia, "UiaRaiseAutomationPropertyChangedEvent");
                pfnUiaRaiseAutomationEvent = (PFN_UiaRaiseAutomationEvent)GetProcAddress(hRealUia, "UiaRaiseAutomationEvent");
            }
        }
    }
}

__declspec(dllexport) BOOL WINAPI UiaClientsAreListening(void) {
    EnsureRealUiaLoaded();
    if (pfnUiaClientsAreListening) return pfnUiaClientsAreListening();
    return FALSE;
}

__declspec(dllexport) LRESULT WINAPI UiaReturnRawElementProvider(HWND hwnd, WPARAM wParam, LPARAM lParam, void *el) {
    EnsureRealUiaLoaded();
    if (pfnUiaReturnRawElementProvider) return pfnUiaReturnRawElementProvider(hwnd, wParam, lParam, el);
    return 0;
}

__declspec(dllexport) HRESULT WINAPI UiaHostProviderFromHwnd(HWND hwnd, void **ppProvider) {
    EnsureRealUiaLoaded();
    if (pfnUiaHostProviderFromHwnd) return pfnUiaHostProviderFromHwnd(hwnd, ppProvider);
    if (ppProvider) *ppProvider = NULL;
    return (HRESULT)0x80004001L; // E_NOTIMPL
}

__declspec(dllexport) HRESULT WINAPI UiaRaiseNotificationEvent(
    void *provider,
    int notificationKind,
    int notificationProcessing,
    BSTR displayString,
    BSTR activityId
) {
    EnsureRealUiaLoaded();
    if (pfnUiaRaiseNotificationEvent) {
        return pfnUiaRaiseNotificationEvent(provider, notificationKind, notificationProcessing, displayString, activityId);
    }
    return S_OK;
}

__declspec(dllexport) HRESULT WINAPI UiaRaiseAutomationPropertyChangedEvent(void *pProvider, int id, VARIANT oldValue, VARIANT newValue) {
    EnsureRealUiaLoaded();
    if (pfnUiaRaiseAutomationPropertyChangedEvent) {
        return pfnUiaRaiseAutomationPropertyChangedEvent(pProvider, id, oldValue, newValue);
    }
    return S_OK;
}

__declspec(dllexport) HRESULT WINAPI UiaRaiseAutomationEvent(void *pProvider, int id) {
    EnsureRealUiaLoaded();
    if (pfnUiaRaiseAutomationEvent) {
        return pfnUiaRaiseAutomationEvent(pProvider, id);
    }
    return S_OK;
}

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    if (fdwReason == DLL_PROCESS_ATTACH) {
        DisableThreadLibraryCalls(hinstDLL);
    }
    return TRUE;
}
