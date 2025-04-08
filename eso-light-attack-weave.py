#!/usr/bin/env python3

import sys
import os

# Imports for the KDE backend.
try:
    import dbus
    from PySide6.QtCore import QObject
    from PySide6.QtCore import QCoreApplication
    from PySide6.QtGui import QMouseEvent
    import subprocess
except ImportError:
    pass

# Imports for the windows backend.
try:
    import keyboard
except ImportError:
    pass


# --- Common Interface for Platform Backends ---
class InputBackend:
    """Abstract base class for platform-specific input handling."""

    def register_hotkey(self, key, callback):
        raise NotImplementedError

    def unregister_hotkeys(self):
        raise NotImplementedError

    def is_left_button_pressed(self):
        raise NotImplementedError

    def is_right_button_pressed(self):
        raise NotImplementedError

    def press_and_release(self, key):
        raise NotImplementedError


# --- KDE Plasma Backend (X11 or Wayland) ---
class KDEPlasmaBackend(InputBackend):
    def __init__(self):
        if not QCoreApplication.instance(): #Create a new app instance if one isn't already running
            self.app = QCoreApplication(sys.argv)
        else:
            self.app = QCoreApplication.instance()  # Use the existing application

        self.bus = dbus.SessionBus()
        self.kga = self.bus.get_object("org.kde.kglobalaccel", "/kglobalaccel")
        self.shortcuts = {}  # Store shortcut names for unregistration

        self.mouse_filter = MouseEventFilter()
        self.app.installEventFilter(self.mouse_filter)

    def register_hotkey(self, key, callback):
        """Registers a global hotkey with KDE."""
        shortcut_name = f"eso_script_shortcut_{key}" # Unique name
        try:
            self.kga.RegisterShortcut(shortcut_name, key, callback)  # Register the shortcut
            self.shortcuts[key] = shortcut_name # Store for unregistration
            print(f"Registered hotkey '{key}' as '{shortcut_name}'")
        except dbus.exceptions.DBusException as e:
            print(f"Error registering hotkey '{key}': {e}")

    def unregister_hotkeys(self):
        """Unregisters all dynamically created hotkeys."""
        for key, shortcut_name in self.shortcuts.items():
            try:
                self.kga.UnregisterShortcut(shortcut_name)  # Unregister the shortcut
                print(f"Unregistered hotkey '{key}' ('{shortcut_name}')")
            except dbus.exceptions.DBusException as e:
                print(f"Error unregistering hotkey '{key}': {e}")

    def is_left_button_pressed(self):
        return self.mouse_filter.left_button_pressed

    def is_right_button_pressed(self):
        return self.mouse_filter.right_button_pressed

    def press_and_release(self, key):
        subprocess.run(["ydotool", "key", key], check=True)


# --- Windows Backend ---
class WindowsBackend(InputBackend):
    def __init__(self):
        self.registered_keys = {}

    def register_hotkey(self, key, callback):
        keyboard.add_hotkey(key, callback)  # Register shortcut
        self.registered_keys.append(key)
        return True

    def unregister_hotkeys(self):
        for key in self.registered_keys: # registered_keys is a member variable that needs to be populated when registering keys
            keyboard.remove_hotkey(key)

    def is_left_button_pressed(self):
        return keyboard.is_pressed('left')

    def is_right_button_pressed(self):
        return keyboard.is_pressed('right')

    def press_and_release(self, key):
        keyboard.press_and_release(key)


# --- Mouse Event Filter (KDE Plasma Only) ---
class MouseEventFilter(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.left_button_pressed = False
        self.right_button_pressed = False

    def eventFilter(self, watched_object, event):
        if isinstance(event, QMouseEvent):
            if event.type() == QMouseEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    self.left_button_pressed = True
                elif event.button() == Qt.RightButton:
                    self.right_button_pressed = True
            elif event.type() == QMouseEvent.MouseButtonRelease:
                if event.button() == Qt.LeftButton:
                    self.left_button_pressed = False
                elif event.button() == Qt.RightButton:
                    self.right_button_pressed = False

        return super().eventFilter(watched_object, event)  # Pass events to other filters


# --- Core Hotkey Handler ---
class HotkeyHandler:
    def __init__(self, backend):
        self.backend = backend
        self.registered_keys = []

    def register_hotkey(self, key, callback):
        if self.backend.register_hotkey(key, callback):
            self.registered_keys.append(key)
            return True
        else:
            return False

    def unregister_hotkeys(self):
        self.backend.unregister_hotkeys()
        self.registered_keys = []

    def simulate_click_and_key(self, event=None):  # Callback function (Windows passes event object)
        """Simulates a mouse click followed by the given key press."""

        print(event)

        if self.backend.is_left_button_pressed() or self.backend.is_right_button_pressed():
            print("Mouse button held down. Passing through key.")
            self.backend.press_and_release(event if event else "a")
            return  # Exit function without injecting a click

        print("Injecting click + key.")
        self.backend.press_and_release(event if event else "a")


# --- Main Execution Block ---
if __name__ == "__main__":
    #TODO: check if os.environ["XDG_SESSION_DESKTOP"] and os.environ["XDG_SESSION_TYPE"] exist, because if they do not, the following checks will cause an error.
    if sys.platform == "win32":
        backend = WindowsBackend()
    elif sys.platform == "linux": #and os.environ["XDG_SESSION_DESKTOP"] == "KDE":
        try:
            backend = KDEPlasmaBackend()
        except ImportError:
            print("Failed to initialize KDE Plasma backend")
            sys.exit(1)
    elif sys.platform == "linux" and os.environ["XDG_SESSION_TYPE"] == "x11":
        print("TODO: Implement desktop-independent X11 fallback")
    elif sys.platform == "linux" and os.environ["XDG_SESSION_TYPE"] == "wayland":
        print("TODO: Implement desktop-independent wayland fallback")
    else:
        print("Unsupported platform.")
        sys.exit(1)

    handler = HotkeyHandler(backend)

    # Register hotkeys here
    hotkeys_to_register = ['1', '2', '3', '4', '5', 'r']
    for key in hotkeys_to_register:
        handler.register_hotkey(key, handler.simulate_click_and_key)

    print("Hotkeys registered. Script running...")

    try:
        if sys.platform == "win32":
            keyboard.wait()  # Keep script alive on Windows
        elif isinstance(backend, KDEPlasmaBackend):
            backend.app.exec() #Keep running on KDE Plasma, Wayland
        else:
            print("TODO: Not (yet) supported platform.")
    except KeyboardInterrupt:
        handler.unregister_hotkeys()
        print("KeyboardInterrupt: Hotkeys unregistered.")
        sys.exit(1)
    finally:
        handler.unregister_hotkeys()
        print("Hotkeys unregistered.")
        sys.exit(1)
