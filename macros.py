import json
import LLKE
import ctypes
from pathlib import Path


active = False

LLKE.set_debug(True)

def activate(action, vk):
    global active
    active = action == LLKE.KEY_PRESS
    #LLKE.set_event(0x5B, None)
    print("XDD")
    return True

LLKE.set_event('VK_UP', activate)

LLKE.loop()