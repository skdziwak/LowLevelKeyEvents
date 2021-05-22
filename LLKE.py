import os
import ctypes
import LLKE_KEYS

KEY_PRESS = 256
KEY_RELEASE = 257
NULL = ctypes.c_int(0)

_llkeDll = ctypes.WinDLL(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'LLKE.dll'))
_set_event = getattr(_llkeDll, '?setEvent@@YAXHP6A_NHH@Z_N@Z')
_loop = getattr(_llkeDll, '?loop@@YAXXZ')
_reset = getattr(_llkeDll, '?reset@@YAXXZ')
_set_debug = getattr(_llkeDll, '?setDebug@@YAX_N@Z')
_press_key = getattr(_llkeDll, '?pressKey@@YAXH@Z')
_release_key = getattr(_llkeDll, '?releaseKey@@YAXH@Z')
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
    if k.startswith('0x'):
        return int(k[2:], 16)
    if len(k) == 1:
        k = k.upper()
        b = bytes(k, encoding='ascii')[0]
        for fl, offset in KEYSETS:
            if b >= fl[0] and b <= fl[1]:
                return b - fl[0] + offset
    return getattr(LLKE_KEYS, k)

if __name__ == '__main__':
    import json
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument('config', type=str)
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text())

    active = False

    enabled_classes = set(config['enabled_classes'])

    def get_macro(k):
        global enabled_classes
        for c in enabled_classes:
            for m in config['classes'][c]:
                if m['keycode'] == k:
                    return m
        return None

    def a_press(action, vk):
        m = get_macro(vk)
        if m:
            for vk in m['target']:
                if action == KEY_PRESS:
                    _press_key(ctypes.c_int(vk))
                else:
                    _release_key(ctypes.c_int(vk))
            return True
        return False

    def a_shell(action, vk):
        m = get_macro(vk)
        if m and action == KEY_RELEASE:
            os.system(m['target'])
            return True
        return False

    def a_switch(action, vk):
        m = get_macro(vk)
        if m:
            if action == KEY_RELEASE:
                if m['target'] in enabled_classes:
                    enabled_classes.remove(m['target'])
                else:
                    enabled_classes.add(m['target'])
            return True
        return False

    def a_hold(action, vk):
        m = get_macro(vk)
        if m:
            if action == KEY_PRESS:
                enabled_classes.add(m['target'])
            elif action == KEY_RELEASE:
                enabled_classes.discard(m['target'])
            return True
        return False

    for cl, macros in config['classes'].items():
        for m in macros:
            m['keycode'] = keycode(m['key'])
            if m['action'] == 'switch':
                set_event(m['keycode'], a_switch)
            elif m['action'] == 'press':
                set_event(m['keycode'], a_press)
                m['target'] = [keycode(e) for e in m['target'].split(':')]
            elif m['action'] == 'hold':
                set_event(m['keycode'], a_hold)
            elif m['action'] == 'shell':
                set_event(m['keycode'], a_shell)

    loop()
