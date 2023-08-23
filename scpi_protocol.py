from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from decimal import Decimal
from functools import partial
from typing import Callable, Iterable

from scpi import Cmd, Commands

from wmControl.wavemeter import Wavemeter
from wmControl.wlmConst import WavemeterType, LowSignalError


@dataclass
class ScpiException(Exception):
    """Syntax errors of scpi-command. See also SCPI-Volume 2-Command Reference page 21-13 and 21-15ff."""
    error_code: int
    error_description: str


@dataclass(init=False)
class InvalidSyntaxException(ScpiException):
    """Invalid syntax"""
    error_info: str

    def __init__(self, info: str):
        super().__init__(error_code=-102, error_description="Invalid syntax", error_info=info)


    def __str__(self):
        return f'{self.error_code},"{self.error_description};{self.error_info}"'


@dataclass(init=False)
class UnexpectedNumberOfParameterException(ScpiException):
    """Too many or few parameters."""
    error_info: str

    def __init__(self, info: str):
        super().__init__(error_code=-115, error_description="Unexpected number of parameters", error_info=info)


    def __str__(self):
        return f'{self.error_code},"{self.error_description};"'#{self.error_info}"'


def _encode_idn(value: tuple[WavemeterType, int, tuple[int, int]]) -> str:
    wavemeter, serial, software_version = value
    return f"HighFinesse,{wavemeter.name},{serial},{software_version[0]}.{software_version[1]}".upper()


def _encode_number(values: int | float | Decimal | Iterable[float] | Iterable[float] | Iterable[Decimal]) -> str:
    try:
        return ",".join(map(str, values))
    except TypeError:
        # if values is not a list
        return str(values)


# matches channel_lists. See page 8-4 of the SCPI-99 "syntax and style" handbook of the SCPI standard
# https://www.ivifoundation.org/docs/scpi-99.pdf
match_channel_list = re.compile(r"^\(@([\d,:]+)\)$")
match_channel = re.compile(r"^(?:\d+|\d+:\d+)$")


def _parse_channel_list(channels: str) -> list[int]:
    """
    Takes a channel list in SCPI 99 syntax and returns an ordered list of integers. The list is order sensitive. For
    more details see Volume 1: Syntax and Style of the SCPI standard at https://www.ivifoundation.org/docs/scpi-99.pdf,
    page 8-3.
    Parameters
    ----------
    channels: str
        SCPI formatted channel_list string
    Returns
    -------
    list of int
        A list of integers containing the parsed channels.
    """
    sanitized_channels = match_channel_list.match(channels)
    if sanitized_channels is None:
        raise UnexpectedNumberOfParameterException(f"{channels}")

    parsed_channels = []
    for channel in sanitized_channels.group(1).split(","):
        if match_channel.match(channel) is None:
            raise InvalidSyntaxException(f"{channel}")

        try:
            parsed_channels.append(int(channel))
        except ValueError:
            # The channel is a list not an int
            channel_range = list(map(int, channel.split(":")))
            if channel_range[1] >= channel_range[0]:
                channel_range[1] += 1
                parsed_channels.extend(range(*channel_range))
            else:
                channel_range[1] -= 1
                parsed_channels.extend(range(*channel_range, -1))

    return parsed_channels


async def _query_channel(
    function: Callable, channels: Iterable[int]
) -> Iterable[int] | Iterable[float] | Iterable[Decimal]:
    coros = [function(channel) for channel in channels]

    # results = await asyncio.gather(*coros)
    # return results
    # results = []
    # for coro in asyncio.as_completed(coros):
    #     try:
    #         results.append(await coro)
    #     except LowSignalError:
    #         results.append("-1")

    results = await asyncio.gather(*coros, return_exceptions=True)
    if LowSignalError in results:
        results = ["-1" if result is LowSignalError() else result for result in results]
    return results


IDNCmd = partial(Cmd, encode=_encode_idn, decode=lambda x: x, doc="identification query")
NumberCmdR = partial(Cmd, encode=_encode_number)


def create_scpi_protocol(wavemeter: Wavemeter) -> Commands:
    """
    Creates for every wavemeter a dictionary of commands.

    Parameter
    ---------
    wavemeter: Wavemeter
        Device which receive commands.
    """
    return Commands(
        {
            # Mandatory commands.
            "*CLS": "Clear Status Command",
            "*ESE": "Standard Event Status Enable Command",
            "*ESR": "Standard Event Status Register Query",
            "*IDN": IDNCmd(get=wavemeter.get_wavemeter_info),
            "*OPC": "Operation Complete Command",
            "*RST": "Reset Command",  # No switcher mode active? Setting wavelength measurement to vacuum wavelength? ...
            "*SRE": "Service Request Enable Command",
            "*STB": "Read Status Byte Query",
            "*TST": "Self-Test Query",
            "*WAI": "Wait-to-Continue Command",
            # Device specific commands.
            "MEASure:WAVElength:CHannel": NumberCmdR(
                decode=_parse_channel_list,
                get=partial(_query_channel, wavemeter.get_wavelength),
                doc="wavelength measurement query",
            ),  # wavelength of specific channel
            # Note for thesis: Calling wavelength and right after frequency leads to two different measurements.
            "MEASure:FREQuency:CHannel": NumberCmdR(
                decode=_parse_channel_list,
                get=partial(_query_channel, wavemeter.get_frequency),
                doc="frequency measurement query",
            ),
            "MEASure:TEMPerature": NumberCmdR(decode=lambda x: x, get=wavemeter.get_temperature),
            "GET:CHannel": NumberCmdR(decode=lambda x: x, get=wavemeter.get_channel),
            "GET:CHannel:COUNT": NumberCmdR(decode=lambda x: x, get=wavemeter.get_channel_count),
            "GET:CALibration": NumberCmdR(decode=lambda x: x, get=wavemeter.get_calibration),  # Not SCPI conform
            "GET:CAL:TEST": NumberCmdR(decode=lambda x: x, get=wavemeter.get_calibration_ba_0),  # Not SCPI conform
            "GET:CAL:DIF": NumberCmdR(decode=lambda x: x, get=wavemeter.get_calibration_dif),  # Not SCPI conform
        }
    )
