from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from ipaddress import IPv4Interface, IPv6Interface, ip_interface

import pytest
from pydantic import ValidationError

from config_parser import parse_wavemeter_config


@pytest.mark.parametrize(
    "wavemeter_config, expectation, result",
    [
        ('[[1000,"127.0.0.1",5555]]', does_not_raise(), [(1000, ip_interface("127.0.0.1"), 5555)]),
        ("[[1000,null,5555]]", does_not_raise(), [(1000, None, 5555)]),
        ("[[1000,null,5555], [1001,null,5556]]", does_not_raise(), [(1000, None, 5555), (1001, None, 5556)]),
        ("[[abc,null,5555]]", pytest.raises(ValidationError), []),
        ('[[1000,"localhost",5555]]', pytest.raises(ValidationError), []),
        ('[[1000,"192.168.1.5",abc]]', pytest.raises(ValidationError), []),
    ],
)
def test_wavemeter_config_parser(
    wavemeter_config: str,
    expectation,
    result: list[tuple[int, IPv4Interface | IPv6Interface | tuple[IPv4Interface | IPv6Interface] | None, int]],
):
    with expectation:
        assert parse_wavemeter_config(wavemeter_config) == result
