from os import environ

class MouseController:
  supported_backends = ["darwin", "win32", "uinput", "xorg", "dummy"]

  def __init__(self, settings={"backend":"auto"}):
    self.settings = settings

    if self.settings["backend"] != "auto":
      if self.settings["backend"] in self.supported_backends:
        environ_bak = environ.get("PYNPUT_BACKEND")
        environ["PYNPUT_BACKEND"] = self.settings["backend"]
        from pynput import mouse
        from pynput.mouse import Button
        if environ_bak != None:
          environ["PYNPUT_BACKEND"] = environ_bak
        else:
          environ.pop("PYNPUT_BACKEND")
    else:
      from pynput import mouse
      from pynput.mouse import Button

    self.mouse = mouse
    self.mc = self.mouse.Controller()


  def press(self, key):
    try:
      self.mc.press(key.char)
    except AttributeError:
      self.mc.press(key)


  def release(self, key):
    try:
      self.mc.release(key.char)
    except AttributeError:
      self.mc.release(key)


  def tap(self, key):
    self.press(key)
    self.release(key)
