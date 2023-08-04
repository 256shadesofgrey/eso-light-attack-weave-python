from pynput import keyboard
from pynput.keyboard import Key
from time import sleep

kc = keyboard.Controller()
ignore_press = False
ignore_release = False

def on_press(key):
  # Make sure we don't intercept the key we just sent.
  global ignore_press
  if ignore_press:
    ignore_press = False
    return
  ignore_press = True

  try:
    kc.press(key.char)
  except AttributeError:
    kc.press(key)


def on_release(key):
  # Make sure we don't intercept the key we just sent.
  global ignore_release
  if ignore_release:
    ignore_release = False
    return
  ignore_release = True

  try:
    kc.release(key.char)
  except AttributeError:
    kc.release(key)


with keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True) as listener:
  listener.join()




# sleep(3)
#
# kc.press(Key.backspace)
# kc.release(Key.backspace)
