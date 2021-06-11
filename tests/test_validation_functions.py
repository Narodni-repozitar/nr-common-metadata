import pytest

from nr_common.marshmallow.fields import extract_date, serialize_date


@pytest.mark.parametrize("test_input,expected",
                         [("2019-12-31", "2019-12-31"), ("2019-12", "2019-12"), ("2019", "2019"),
                          ("2018-12-31 / 2019-12-31", "2018-12-31 / 2019-12-31"),
                          ("2018-12 / 2019-12", "2018-12 / 2019-12"),
                          ("p2019", "2019"), ("c2019", "2019"), ("cop2019", "2019"),
                          ("[2019]", "2019"), ("©2019", "2019"), ("℗2019", "2019"),
                          ("2018-2019", "2018 / 2019"), ("copyright2019", "2019"),
                          ("fonogram2019", "2019"), ("2018 - 2019", "2018 / 2019")
                          ])
def test_validate_date(test_input, expected):
    res = serialize_date(test_input)
    assert res == expected


def test_extract_date():
    assert extract_date("2019-2020") == [('2019',), ('2020',)]
