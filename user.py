#!/usr/bin/env python
import sys

from wmControl import control

# wm0 = control.Wavemeter(4734, dll_path="./wmControl/wlmData.dll")  # Quips C 192.168.1.45
# wm1 = control.Wavemeter(536)  # Quips B 192.168.1.240
if sys.platform == "win32":
    wm2 = control.Wavemeter(4711, dll_path="./wmControl/wlmData.dll")  # Quips B 192.168.1.240
elif sys.platform == "linux":
    wm2 = control.Wavemeter(4711, dll_path="./wmControl/libwlmData.so")


# wm1.wavelengths(1)
# wm2.wavelengths(1)
# wm1.wavelengths(1)
# wm1.frequencys(1)
wm2.frequencys(1)
# wm1.frequencys(1)
# wm0.wavelengths(1)
# wm0.frequencys(1)

##print(wm2.bfr)
# wm2.putBfr(0)
# print(wm2.bfr)

# wm0.getSwitcher(1)
# wm1.getSwitcher(1)
# wm2.getSwitcher(1)

# wm0.allwavelengths(1)
# wm2.allwavelengths(1)
