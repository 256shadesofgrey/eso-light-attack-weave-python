from os import environ

class KeyboardController:
  supported_backends = ["darwin", "win32", "uinput", "xorg", "dummy"]

  def __init__(self, settings={"backend":"auto"}):
    self.settings = settings

    if self.settings["backend"] != "auto":
      if self.settings["backend"] in self.supported_backends:
        environ_bak = environ.get("PYNPUT_BACKEND")
        environ["PYNPUT_BACKEND"] = self.settings["backend"]
        from pynput import keyboard
        from pynput.keyboard import Key
        if environ_bak != None:
          environ["PYNPUT_BACKEND"] = environ_bak
        else:
          environ.pop("PYNPUT_BACKEND")
    else:
      from pynput import keyboard
      from pynput.keyboard import Key

    self.keyboard = keyboard
    self.kc = self.keyboard.Controller()


  def press(self, key):
    try:
      self.kc.press(key.char)
    except AttributeError:
      self.kc.press(key)


  def release(self, key):
    try:
      self.kc.release(key.char)
    except AttributeError:
      self.kc.release(key)


  def tap(self, key):
    try:
      self.kc.tap(key.char)
    except AttributeError:
      self.kc.tap(key)
