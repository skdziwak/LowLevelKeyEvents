// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"
#include <stdio.h>

LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam);
HHOOK hhkLowLevelKybd = NULL;

typedef bool (*event)(int, int);
event events[0xFF];
bool debug = FALSE;

// Hook and loop
__declspec(dllexport) void loop() {
    printf("Starting LLKE\n");
    hhkLowLevelKybd = SetWindowsHookEx(WH_KEYBOARD_LL, LowLevelKeyboardProc, 0, 0);
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    UnhookWindowsHookEx(hhkLowLevelKybd);
    hhkLowLevelKybd = NULL;
}

_declspec(dllexport) void setDebug(bool d) {
    debug = d;
}

__declspec(dllexport) void releaseKey(int k) {
    INPUT ip;
    ip.type = INPUT_KEYBOARD;
    ip.ki.wScan = 0;
    ip.ki.time = 0;
    ip.ki.dwExtraInfo = 0;
    ip.ki.wVk = k;
    ip.ki.dwFlags = 2;
    SendInput(1, &ip, sizeof(INPUT));
}

__declspec(dllexport) void pressKey(int k) {
    INPUT ip;
    ip.type = INPUT_KEYBOARD;
    ip.ki.wScan = 0;
    ip.ki.time = 0;
    ip.ki.dwExtraInfo = 0;
    ip.ki.wVk = k;
    ip.ki.dwFlags = 0;
    SendInput(1, &ip, sizeof(INPUT));
}

__declspec(dllexport) void reset() {
    for(int i = 0; i < 0xFF; i++) {
        events[i] = NULL;
    }
}

__declspec(dllexport) void setEvent(int vk, event e, bool d) {
    events[vk] = e;
}

// Callback
LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    PKBDLLHOOKSTRUCT p = (PKBDLLHOOKSTRUCT)lParam;
    if (debug) {
        printf("Key: %d; Action: %d\n", p->vkCode, wParam);
    }
    if (events[p->vkCode] != NULL) {
        if(events[p->vkCode](wParam, p->vkCode))
            return 1;
    }
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        if (hhkLowLevelKybd != NULL)
            UnhookWindowsHookEx(hhkLowLevelKybd);
        break;
    }
    return TRUE;
}