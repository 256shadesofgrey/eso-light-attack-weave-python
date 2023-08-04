#TODO: make it work nice with active keys that are mouse buttons.

from os import environ

class MouseListener:
  supported_backends = ["darwin", "win32", "uinput", "xorg", "dummy"]

  held_down = set()

  ignore_press = False
  ignore_release = False

  def __init__(self, mc=None, settings={"active_keys":[], "backend":"auto"}):
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

    if mc == None:
        self.mouse = mouse
        self.mc = self.mouse.Controller()
    else:
        self.mc = mc

    self.settings = settings
    #self.action = action

    # Start the actual listener.
    # with mouse.Listener(on_click=self.on_click, suppress=False) as listener_mouse:
    #     listener_mouse.join()
    self.listener = mouse.Listener(on_click=self.on_click, suppress=False)
    # self.listener.start()
    # self.listener.join()


  def start_listener(self):
    self.listener.start()


  def join_listener(self):
    self.listener.join()


  def stop_listener(self):
    self.listener.stop()


  def is_active_key(self, key):
    for i in range(len(self.settings["active_keys"])):
      if "'{0}'".format(self.settings["active_keys"][i]) == "{0}".format(key):
        return True
    return False


  def on_click(self, x, y, key, pressed):
    if pressed:
      print("Pressed: {0}".format(key))

      self.held_down.add(key)
    else:
      print("Released: {0}".format(key))

      if key in self.held_down:
        self.held_down.remove(key)


  def is_pressed(self, key):
    if key in self.held_down:
      return True
    else:
      return False
