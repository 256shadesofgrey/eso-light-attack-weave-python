from os import environ

class KeyboardListener:
  supported_backends = ["darwin", "win32", "uinput", "xorg", "dummy"]

  held_down = set()

  ignore_press = False
  ignore_release = False

  enabled = True

  skill_keys_different_from_active_keys = False

  def __init__(self, kc=None, action=None, settings={"active_keys":[], "skill_keys":[], "backend":"auto"}):
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

    for i in range(len(settings["skill_keys"])):
      if self.settings["skill_keys"][i] != self.settings["active_keys"][i]:
        self.skill_keys_different_from_active_keys = True
        break

    if self.skill_keys_different_from_active_keys:
      self.listener = keyboard.Listener(on_press=self.on_press_different_skill_key, on_release=self.on_release_different_skill_key, suppress=False)
    else:
      self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release, suppress=True)


  def start_listener(self):
    self.listener.start()


  def join_listener(self):
    self.listener.join()


  def stop_listener(self):
    self.listener.stop()


  def match_skill(self, key):
    if not self.is_active_key(key):
      return False
    key_index = self.settings["active_keys"].index(key)
    if key_index >= len(self.settings["skill_keys"]):
      return False
    print("Matched with:", self.settings["skill_keys"][key_index])
    return self.settings["skill_keys"][key_index]


  def is_active_key(self, key):
    # Suspend key is always active.
    if "'{0}'".format(self.settings["active_keys"][len(self.settings["active_keys"])-1]) == "{0}".format(key):
      return True

    # If not enabled, there are no active keys.
    if not self.enabled:
      return False

    for i in range(len(self.settings["active_keys"])):
      #print("{0}".format(self.settings["active_keys"][i]))
      #print("{0}".format(key))
      if "'{0}'".format(self.settings["active_keys"][i]) == "{0}".format(key) or "{0}".format(self.settings["active_keys"][i]) == "{0}".format(key):
        return True

    return False


  def on_press(self, key):
    # Make sure we don't intercept the key we just sent.
    if self.ignore_press:
      self.ignore_press = False
      return
    self.ignore_press = True

    print("Pressed: {0}".format(key))

    self.held_down.add(key)

    if not self.is_active_key(key):
      # If it's not a skill key or the key is disabled, just pass it through.
      self.kc.press(key)
    else:
      self.action(key)


  def on_release(self, key):
    # Make sure we don't intercept the key we just sent.
    if self.ignore_release:
      self.ignore_release = False
      return
    self.ignore_release = True

    print("Released: {0}".format(key))

    if key in self.held_down:
      self.held_down.remove(key)

    self.kc.release(key)


  def on_press_different_skill_key(self, key):
    print("*Pressed: {0}".format(key))

    self.held_down.add(key)

    if self.is_active_key(key):
      self.action(self.match_skill(key))


  def on_release_different_skill_key(self, key):
    print("*Released: {0}".format(key))

    if key in self.held_down:
      self.held_down.remove(key)


  def is_pressed(self, key):
    if key in self.held_down:
      return True
    else:
      return False


  def enable(self):
    self.enabled = True


  def disable(self):
    self.enabled = False
