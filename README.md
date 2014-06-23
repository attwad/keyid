KeyInjectionDetector
====================

Python module to check for an expected number of keyboards on a system, useful to detect when you're getting [facedanced](http://goodfet.sourceforge.net/hardware/facedancer11/)...

Example usage
-------------

If you expect ot have 2 keyboards on your system and you indeed have 2 keyboards connected:

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

But if you don't have the expected number of keyboards on your system, an alert popup will be shown:

