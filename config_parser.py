from __future__ import annotations

import logging
from ipaddress import IPv4Interface, IPv6Interface

from pydantic import IPvAnyInterface, TypeAdapter


def parse_wavemeter_config(
    wavemeter_configs: str,
) -> list[tuple[int, IPv4Interface | IPv6Interface | tuple[IPv4Interface | IPv6Interface] | None, int]]:
    """
    Parse the wavemeter config supplied via the WAVEMETERS environment variable.

    Parameters
    ----------
    wavemeter_configs: str
        A JSON formatted string, that contains a list of wavemeter configs. Each config contains a tuple of the wavemeter
        product_id (int), the interface to bind to (an ip address or a list of ip addresses), and the port to bind to.

    Returns
    -------
    A tuple of tuples of int, IPvAnyInterface, int
        A validated tuple of wavemeter configs
    """
    ta = TypeAdapter(list[tuple[int, IPvAnyInterface | tuple[IPvAnyInterface] | None, int],])
    return ta.validate_json(wavemeter_configs)


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
