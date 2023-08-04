from os import environ

class KeyboardListener:
  supported_backends = ["darwin", "win32", "uinput", "xorg", "dummy"]

  held_down = set()

  ignore_press = False
  ignore_release = False

  def __init__(self, kc=None, action=None, settings={"active_keys":[], "backend":"auto"}):
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

    if kc == None:
        self.keyboard = keyboard
        self.kc = self.keyboard.Controller()
    else:
        self.kc = kc

    self.settings = settings
    self.action = action

    # Start the actual listener.
    with keyboard.Listener(on_press=self.on_press, on_release=self.on_release,
                           suppress=True) as listener:
        listener.join()


  def is_active_key(self, key):
    for i in range(len(self.settings["active_keys"])):
      if "'{0}'".format(self.settings["active_keys"][i]) == "{0}".format(key):
        return True
    return False


  def on_press(self, key):
    # Make sure we don't intercept the key we just sent.
    global ignore_press
    if self.ignore_press:
      self.ignore_press = False
      return
    self.ignore_press = True

    print("Pressed: {0}".format(key))

    self.held_down.add(key)

    if not self.is_active_key(key):
      # If it's not a skill key or the key is disabled, just pass it through.
      try:
        self.kc.press(key.char)
      except AttributeError:
        self.kc.press(key)
    else:
      self.action(key)


  def on_release(self, key):
    # Make sure we don't intercept the key we just sent.
    global ignore_release
    if self.ignore_release:
      self.ignore_release = False
      return
    self.ignore_release = True

    print("Released: {0}".format(key))

    if key in self.held_down:
      self.held_down.remove(key)

    try:
      self.kc.release(key.char)
    except AttributeError:
      self.kc.release(key)


  def is_pressed(self, key):
    if key in self.held_down:
      return True
    else:
      return False
