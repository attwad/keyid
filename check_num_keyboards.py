"""Module that checks that an expected number of keyboards is connected."""

import argparse
import ctypes
from ctypes import wintypes
import sys


# ctypes mapping of the structure defined at
# http://msdn.microsoft.com/en-us/library/windows/desktop/ms645568(v=vs.85).aspx
class RAWINPUTDEVICELIST(ctypes.Structure):
  _fields_ = [("hDevice", wintypes.HANDLE), ("dwType", wintypes.DWORD)]

  def __str__(self):
    return 'hDevice: %d\ndwType:  %d' % (self.hDevice, self.dwType)


def GetKeyboards():
  """Returns a list of RAWINPUTDEVICELIST that are of type keyboards."""
  nDevices = ctypes.c_uint()

  if ctypes.windll.user32.GetRawInputDeviceList(
      ctypes.POINTER(ctypes.c_int)(),
      ctypes.byref(nDevices),
      ctypes.sizeof(RAWINPUTDEVICELIST)) == -1:
    ctypes.WinError()
    sys.exit(-1)

  print('found {} devices on this system'.format(nDevices.value))

  devices = (RAWINPUTDEVICELIST * nDevices.value)()

  if ctypes.windll.user32.GetRawInputDeviceList(
      devices,
      ctypes.byref(nDevices),
      ctypes.sizeof(RAWINPUTDEVICELIST)) == -1:
    ctypes.WinError()
    sys.exit(-1)

  print('Got info on all those devices:')

  RIM_TYPEHID = 2
  RIM_TYPEKEYBOARD = 1
  RIM_TYPEMOUSE = 0
  for device in devices:
    print(device)
    if device.dwType == RIM_TYPEMOUSE:
      print('MOUSE')
    elif device.dwType== RIM_TYPEKEYBOARD:
      print('KEYBOARD')
    elif device.dwType == RIM_TYPEHID:
      print('HID, not mouse nor keyboard')
    else:
      print ('UNKNOWN')

  return [dev for dev in devices if dev.dwType == RIM_TYPEKEYBOARD]


def GetKeyboardsDetails(keyboards):
  details = []

  for index, device in enumerate(keyboards):
    sizeOfPData= ctypes.c_uint()
    nbChars = ctypes.windll.user32.GetRawInputDeviceInfoW(
        device.hDevice,
        0x20000007, # RIDI_DEVICENAME
        ctypes.POINTER(ctypes.c_int)(),
        ctypes.byref(sizeOfPData))
    if nbChars == -1:
      ctypes.WinError()
      sys.exit(-1)
    name = ctypes.create_unicode_buffer(sizeOfPData.value)
    nbChars = ctypes.windll.user32.GetRawInputDeviceInfoW(
        device.hDevice,
        0x20000007, # RIDI_DEVICENAME
        name,
        ctypes.byref(sizeOfPData))
    if nbChars == -1:
      ctypes.WinError()
      sys.exit(-1)
    if nbChars == -1:
      ctypes.WinError()
      sys.exit(-1)
    print("device {} has name:\n{}".format(index, name.value))
    details.append("device {} has name:\n{}".format(index, name.value))

  return details



if __name__ == "__main__":
  parser = argparse.ArgumentParser(
      description="Checks that the system has an expected number of input "
                  "devices.")
  parser.add_argument(
      "expected_num_keyboards",
      help="Number of expected keyboards on the system. -1 to ignore.",
      type=int)
  args = parser.parse_args()

  if args.expected_num_keyboards == -1:
    parser.print_help()
    sys.exit(0)

  keyboards = GetKeyboards()
  print('Found {} keyboard(s) on this system'.format(len(keyboards)))
  if len(keyboards) == args.expected_num_keyboards:
    sys.exit(0)

  # Get keyboards names.
  details = GetKeyboardsDetails(keyboards)

  # Get current keyboard info.
  t = ctypes.windll.user32.GetKeyboardType(0)
  KEYBOARD_TYPE_ = {
      1: "IBM PC/XT or compatible (83-key) keyboard",
      2: "Olivetti \"ICO\" (102-key) keyboard",
      3: "IBM PC/AT (84-key) or similar keyboard",
      4: "IBM enhanced (101- or 102-key) keyboard",
      5: "Nokia 1050 and similar keyboards",
      6: "Nokia 9140 and similar keyboards",
      7: "Japanese keyboard",
  }
  print("Current keyboard is a ", KEYBOARD_TYPE_[t])
  details.append("Current keyboard is a {}".format(KEYBOARD_TYPE_[t]))

  subtype = ctypes.windll.user32.GetKeyboardType(1)
  print("Current keyboard subtype: ", subtype)
  details.append("Current keyboard subtype: {}".format(subtype))

  ctypes.windll.user32.MessageBoxW(
      0, # NO_HANDLE
      "Unexpected number of keyboards: {}\n\nDetails:\n{}".format(
          len(keyboards), "\n".join(details)),
      u"Alert",
      0) # MB_OK
