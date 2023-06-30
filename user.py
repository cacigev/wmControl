#!/usr/bin/env python
from __future__ import annotations

import logging
import sys

from decouple import UndefinedValueError, config

from wmControl import control


def parse_log_level(log_level: int | str) -> int:
    """
    Parse an int or string, then return its standard log level definition.
    Parameters
    ----------
    log_level: int or str
        The log level. Either a string or a number.
    Returns
    -------
    int
        The log level as defined by the standard library. Returns logging.INFO as default
    """
    try:
        level = int(log_level)
    except ValueError:
        # parse the string
        level = logging.getLevelName(str(log_level).upper())
    if isinstance(level, int):
        return level
    return logging.INFO  # default log level


logging.basicConfig(
    # format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    format="%(message)s",
    level=config("APPLICATION_LOG_LEVEL", default=logging.INFO, cast=parse_log_level),
    datefmt="%Y-%m-%d %H:%M:%S",
)


# wm0 = control.Wavemeter(4734, dll_path="./wmControl/wlmData.dll")  # Quips C 192.168.1.45
# wm1 = control.Wavemeter(536)  # Quips B 192.168.1.240
if sys.platform == "win32":
    wm2 = control.Wavemeter(4711, dll_path="./wmControl/wlmData.dll", start_main=True)  # Quips B 192.168.1.240
elif sys.platform == "linux":
    wm2 = control.Wavemeter(4711, dll_path="./wmControl/libwlmData.so", start_main=True)


# wm1.wavelengths(1)
# wm2.wavelengths(1)
# wm1.wavelengths(1)
# wm1.frequencys(1)
# wm2.frequencys(1)
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
