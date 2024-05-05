# eso-light-attack-weave-python
This is a rewrite of [this](https://github.com/256shadesofgrey/eso-light-attack-weave) AutoHotkey script in python.
 The original macro only works on Windows, but I have since switched to Linux as my daily driver,
 and hence I decided to rewrite it in a language supported on both platforms.
 Because I rarely play ESO any more, the development will be slow, so don't expect feature parity with the AHK script any time soon.
 For this reason I highly recommend that you keep using the AHK script for the time being.

# Disclaimer
**I will not provide any support on this script at the present time.**
 This script is currently just a proof of concept, so it will have bugs and miss crucial features.
 **All bug reports, feature and support requests will be ignored or even deleted** until I have implemented what I consider to be ready for daily use.

# Limitations
This script currently just bluntly replaces keyboard keys 1-5 with mouse click followed by the key pressed.
 Unlike the AHK script, it does not check whether you're blocking, doing a heavy attack or whether you swapped bars recently.
 Nor does it queue your inputs or respect any kind of timings, like the global cooldown etc.
 It does not have a suspend key function at present, so if you want to stop the script, you have to kill the process running it.
 It also does not check for the active window. So if you have it running, and try to type text somewhere outside of the ESO window,
 it will keep clicking the mouse whenever you press any of the 1-5 keys.

# Installation instructions
## Linux
1. Make sure you have python3 installed. If not, use the package manager to do so.
2. Install the package pyinput (use pip3 instead of pip if applicable):
```pip install pynput```
3. Clone this repository to your PC.

# Usage instructions
1. Enter the directory containing the script and run the eso-light-attack-weave.py from terminal (use python3 instead of python if applicable):
```python eso-light-attack-weave.py```
