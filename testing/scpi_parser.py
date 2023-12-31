from contextlib import nullcontext as does_not_raise

import pytest

import scpi_protocol


@pytest.mark.parametrize(
    "scpi_channel_list, expectation, result",
    [
        ("(@1)", does_not_raise(), [0]),
        ("(@1,2)", does_not_raise(), [0, 1]),
        ("(@2,1)", does_not_raise(), [1, 0]),
        ("(@1,2,4:6)", does_not_raise(), [0, 1, 3, 4, 5]),
        ("(@1,2,6:4)", does_not_raise(), [0, 1, 5, 4, 3]),
        ("(@1,2,4:6,9)", does_not_raise(), [0, 1, 3, 4, 5, 8]),
        ("(@1,2,4:6,9:13)", does_not_raise(), [0, 1, 3, 4, 5, 8, 9, 10, 11, 12]),
        ("1", pytest.raises(scpi_protocol.CommandHeaderError), None),
        ("1,2", pytest.raises(scpi_protocol.CommandHeaderError), None),
        ("(@1", pytest.raises(scpi_protocol.CommandHeaderError), None),
        ("@1", pytest.raises(scpi_protocol.CommandHeaderError), None),
        ("(@a)", pytest.raises(scpi_protocol.CommandHeaderError), None),
        ("(@1;2)", pytest.raises(scpi_protocol.CommandHeaderError), None),
        ("(@1:)", pytest.raises(scpi_protocol.CommandHeaderError), None),
    ],
)
def test_channel_list_parser(scpi_channel_list: str, expectation, result: list[int]):
    with expectation:
        assert scpi_protocol._parse_channel_list(scpi_channel_list) == result
