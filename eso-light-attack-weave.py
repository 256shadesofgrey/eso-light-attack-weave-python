from pynput import keyboard, mouse
from pynput.keyboard import Key
from pynput.mouse import Button

__all__ = []

#========== Configuration ==========

# Keys used for the skills.
skill_keys = ["1", "2", "3", "4", "5", "r"]

# Which skills will be used with weaving (same order as in skill_keys).
weaving_enabled = [1, 1, 1, 1, 1, 0]

# Which skills will be block cancelled (same order as in skill_keys).
block_cancelling_enabled = [0, 0, 0, 0, 0, 0]


#===================================

kc = keyboard.Controller()
mc = mouse.Controller()

ignore_key = False

def is_skill_key(key):
    print("is_skill_key()")
    for k in skill_keys:
        if "'{0}'".format(k) == "{0}".format(key):
            return True
    return False

def on_press(key):
    # Make sure we don't intercept the key we just sent.
    global ignore_key
    if ignore_key:
        ignore_key = False
        return
    ignore_key = True
    
    if not is_skill_key(key):
        # If it's not a skill key, just pass it through.
        kc.press(key.char)
    else:
        # TODO: implement the actual macro here.
        return False

def main():
    with keyboard.Listener(on_press=on_press, suppress=True) as listener:
        listener.join()

if __name__ == "__main__":main()
