import os
import ctypes
import LLKE_KEYS

KEY_PRESS = 256
KEY_RELEASE = 257
NULL = ctypes.c_int(0)

_llkeDll = ctypes.WinDLL(os.path.join(os.getcwd(), 'LLKE.dll'))
_set_event = getattr(_llkeDll, '?setEvent@@YAXHP6A_NHH@Z_N@Z')
_loop = getattr(_llkeDll, '?loop@@YAXXZ')
_reset = getattr(_llkeDll, '?reset@@YAXXZ')
_set_debug = getattr(_llkeDll, '?setDebug@@YAX_N@Z')
_fptr = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int) #void return type; int action; int vk;
_reset()
    
functions = []
def set_event(vk, f):
    if type(vk) == str:
        vk = keycode(vk)
    if f == None:
        ptr = NULL
    else:
        ptr = _fptr(f)
        functions.append(ptr)
    _set_event(ctypes.c_int(vk), ptr)

def loop():
    print("Starting loop")
    _loop()

def set_debug(d):
    _set_debug(ctypes.c_bool(d))

KEYSETS = [
    (bytes('09', encoding='ascii'), 0x30),
    (bytes('AZ', encoding='ascii'), 0x41)
]

def keycode(k):
    if type(k) == int:
        return k
    if len(k) == 1:
        k = k.upper()
        b = bytes(k, encoding='ascii')[0]
        for fl, offset in KEYSETS:
            if b >= fl[0] and b <= fl[1]:
                return b - fl[0] + offset
    return getattr(LLKE_KEYS, k)