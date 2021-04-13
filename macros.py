import LLKE
import ctypes

active = False

#LLKE.set_debug(True)

def activate(action, vk):
    global active
    active = action == LLKE.KEY_PRESS
    #LLKE.set_event(0x5B, None)
    print("XDD")
    return True

LLKE.set_event(0x5B, activate)

LLKE.loop()