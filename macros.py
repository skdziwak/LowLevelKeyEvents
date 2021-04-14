import json
import LLKE
import ctypes
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('config', type=str)
args = parser.parse_args()

config = json.loads(Path(args.config).read_text())

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

def a_shell(action, vk):
    m = get_macro(vk)
    if m and action == LLKE.KEY_RELEASE:
        os.system(m['target'])
        return True
    return False

def a_switch(action, vk):
    m = get_macro(vk)
    if m:
        if action == LLKE.KEY_RELEASE:
            if m['target'] in enabled_classes:
                enabled_classes.remove(m['target'])
            else:
                enabled_classes.add(m['target'])
        return True
    return False

def a_hold(action, vk):
    m = get_macro(vk)
    if m:
        if action == LLKE.KEY_PRESS:
            enabled_classes.add(m['target'])
        elif action == LLKE.KEY_RELEASE:
            enabled_classes.discard(m['target'])
        return True
    return False

for cl, macros in config['classes'].items():
    for m in macros:
        m['keycode'] = LLKE.keycode(m['key'])
        if m['action'] == 'switch':
            LLKE.set_event(m['keycode'], a_switch)
        elif m['action'] == 'press':
            LLKE.set_event(m['keycode'], a_press)
            m['target'] = [LLKE.keycode(e) for e in m['target'].split(':')]
        elif m['action'] == 'hold':
            LLKE.set_event(m['keycode'], a_hold)
        elif m['action'] == 'shell':
            LLKE.set_event(m['keycode'], a_shell)



#LLKE.set_event('VK_ESCAPE', activate)

LLKE.loop()