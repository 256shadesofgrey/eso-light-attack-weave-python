from pynput import keyboard, mouse
from pynput.keyboard import Key
from pynput.mouse import Button

from drivers.KeyboardController_pynput import KeyboardController
from drivers.KeyboardListener_pynput import KeyboardListener
from drivers.MouseController_pynput import MouseController
from drivers.MouseListener_pynput import MouseListener

__all__ = []

#========== Configuration ==========

# Keys used for the skills.
skill_keys = ["1", "2", "3", "4", "5", "r"]

# Key used to enable/disable the macro
suspend_key = ["tab"]

# Light attack key.
la_key = Button.left
# Block key.
block_key = Button.right

# Which skills will be used with weaving (same order as in skill_keys).
weaving_enabled = [1, 1, 1, 1, 1, 0]

#===================================

#kc = keyboard.Controller()
kc = KeyboardController({"backend":"xorg"})
#mc = mouse.Controller()
mc = MouseController({"backend":"xorg"})
ml = MouseListener(mc, {"backend":"xorg"})

#ignore_press = False
#ignore_release = False


def is_skill_key(key):
    for k in skill_keys:
        if "'{0}'".format(k) == "{0}".format(key):
            return True
    return False


def is_enabled_skill_key(key):
    for i in range(len(skill_keys)):
        if "'{0}'".format(skill_keys[i]) == "{0}".format(key) and \
                weaving_enabled[i] == 1:
            return True
    return False


def is_suspend_key(key):
    for k in suspend_key:
        if "'{0}'".format(k) == "{0}".format(key):
            return True
    return False


def weave(key):
    # TODO: Check if la_key and block_key requires mouse or keyboard input.
    if not ml.is_pressed(la_key) and not ml.is_pressed(block_key):
        mc.tap(la_key)
    # mc.tap(la_key)
    kc.press(key)


def suspend_toggle(key):
    #TODO: implement suspend functionality
    return True


def action(key):
    if is_enabled_skill_key(key):
        weave(key)
    elif is_suspend_key(key):
        suspend_toggle(key)


# ml = MouseListener(mc, {"backend":"xorg"})
kl = KeyboardListener(kc, action, {"active_keys":skill_keys+suspend_key, "backend":"xorg"})
# ml = MouseListener(mc, {"backend":"xorg"})

ml.start_listener()
kl.start_listener()
ml.join_listener()
kl.join_listener()

# def on_press(key):
#     # Make sure we don't intercept the key we just sent.
#     global ignore_press
#     if ignore_press:
#         ignore_press = False
#         return
#     ignore_press = True
#
#     print("Pressed: {0}".format(key))
#
#     if not is_enabled_skill_key(key):
#         # If it's not a skill key or the key is disabled, just pass it through.
#         try:
#             kc.press(key.char)
#         except AttributeError:
#             kc.press(key)
#     else:
#         weave(key)
#
#
# def on_release(key):
#     # Make sure we don't intercept the key we just sent.
#     global ignore_release
#     if ignore_release:
#         ignore_release = False
#         return
#     ignore_release = True
#
#     print("Released: {0}".format(key))
#
#     try:
#         kc.release(key.char)
#     except AttributeError:
#         kc.release(key)


# def main():
#     with keyboard.Listener(on_press=on_press, on_release=on_release,
#                            suppress=True) as listener:
#         listener.join()
#
#
# if __name__ == "__main__":main()
