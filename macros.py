import LLKE
import ctypes

active = False

LLKE.set_debug(True)

def activate(action, vk):
    global active
    active = action == LLKE.KEY_PRESS
    print(active)

LLKE.set_event(0x5B, activate, True)

LLKE.loop()