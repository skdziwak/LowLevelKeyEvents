import os
import ctypes

KEY_PRESS = 256
KEY_RELEASE = 257

_llkeDll = ctypes.WinDLL(os.path.join(os.getcwd(), 'LLKE.dll'))
_set_event = getattr(_llkeDll, '?setEvent@@YAXHP6AXHH@Z_N@Z')
_loop = getattr(_llkeDll, '?loop@@YAXXZ')
_reset = getattr(_llkeDll, '?reset@@YAXXZ')
_set_debug = getattr(_llkeDll, '?setDebug@@YAX_N@Z')
_fptr = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_int, ctypes.c_int) #void return type; int action; int vk;
_reset()
    
functions = []
def set_event(vk, f, block=True):
    ptr = _fptr(f)
    functions.append(ptr)
    _set_event(ctypes.c_int(vk), ptr, ctypes.c_bool(block))

def loop():
    print("Starting loop")
    _loop()

def set_debug(d):
    _set_debug(ctypes.c_bool(d))