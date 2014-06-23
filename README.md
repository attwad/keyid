KeyInjectionDetector
====================

Python module to check for an expected number of keyboards on a system, useful to detect when you're getting [facedanced](http://goodfet.sourceforge.net/hardware/facedancer11/)...

Usage
-----

If you expect to have 2 keyboards on your system and you indeed have 2 keyboards connected:

```
  > python check_num_keyboards.py 2
  found 5 devices on this system
  Got info on all those devices:
  hDevice: 131141
  dwType:  2
  HID, not mouse nor keyboard
  hDevice: 65603
  dwType:  1
  KEYBOARD
  hDevice: 720961
  dwType:  1
  KEYBOARD
  hDevice: 65599
  dwType:  0
  MOUSE
  hDevice: 720957
  dwType:  0
  MOUSE
  Found 2 keyboard(s) on this system
```

But if you don't have the expected number of keyboards on your system, an alert [popup](https://github.com/attwad/keyid/blob/master/error_num_keyboards.png) will be shown.

I suggest setting up a scheduled task on windows using something like:

`schtasks /create /sc minute /mo 1 /tn "Check num keyboards" /tr C:\keyid\run.bat`

Linux
-----
To come, but if you're using linux there are much easier ways to check for this kind of things, no need for python nor ctypes, just plain old
