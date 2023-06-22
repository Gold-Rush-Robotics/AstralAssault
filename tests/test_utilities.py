from grr.utilities.clamp_range import clamp_range
import pytest


@pytest.mark.parametrize("test_value,test_min,test_max,expected", [
    (0, -1, 1, 0),
    (2, -1, 1, 1),
    (-2, -1, 1, -1),
    (0, -4, -2, -2),
    (2, 1, 5, 2),
    (.2, -1, 1, .2)
])
def test_clamp_normal(test_value, test_min, test_max, expected):
    assert clamp_range(test_value, test_min, test_max) == expected


@pytest.mark.parametrize("test_value,test_min,test_max,expected", [
    (0, 1, -1, 0),
    (0, 2, 1, 0),
    (0, -1, -4, 0)
])
def test_clamp_error(test_value, test_min, test_max, expected):
    with pytest.raises(ValueError):
        assert clamp_range(test_value, test_min, test_max) == expected
