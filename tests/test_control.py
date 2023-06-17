import pytest

from grr.control.pid import PID


@pytest.mark.parametrize("kP, kI, kD, min_clamp, max_clamp, goal, values, expected", [
    (1, 0, 0, -1, 1, 0, [2, 1.5, 1, .5, 0], [-1, -1, -1, -.5, 0])
])
def test_PID(kP: float, kI: float, kD: float, min_clamp: float, max_clamp: float, goal: float, values: list[float], expected: list[float]):
    pid = PID(kP, kI, kD, min_clamp, max_clamp)
    for i, val in enumerate(values):
        assert pid.calculate(goal, val) == expected[i]
