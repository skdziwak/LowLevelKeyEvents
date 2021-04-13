import json
import LLKE
import ctypes
from pathlib import Path
from copy import copy

config = json.loads(Path('config.json').read_text())

active = False

#LLKE.set_debug(True)

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
            if action == LLKE.KEY_PRESS:
                LLKE._press_key(ctypes.c_int(vk))
            else:
                LLKE._release_key(ctypes.c_int(vk))
        return True
    return False

def a_switch(action, vk):
    if action == LLKE.KEY_RELEASE:
        m = get_macro(vk)
        if m:
            if m['target'] in enabled_classes:
                enabled_classes.remove(m['target'])
            else:
                enabled_classes.add(m['target'])
    return True

for cl, macros in config['classes'].items():
    for m in macros:
        m['keycode'] = LLKE.keycode(m['key'])
        if m['action'] == 'switch':
            LLKE.set_event(m['keycode'], a_switch)
        elif m['action'] == 'press':
            LLKE.set_event(m['keycode'], a_press)
            m['target'] = [LLKE.keycode(e) for e in m['target'].split(':')]



#LLKE.set_event('VK_ESCAPE', activate)

LLKE.loop()