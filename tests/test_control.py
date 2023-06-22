import pytest
import numpy as np
import turtle

from grr.control.pid import PID
from time import sleep


@pytest.mark.parametrize("kP, kI, kD, min_clamp, max_clamp, goal, values, expected, dT", [
    (1, 0, 0, -1, 1, 0, [2, 1.5, 1, .5, 0], [-1, -1, -1, -.5, 0], .1),
    (1, 0, 0, -1, 1, 0, [-2, -1.5, -1, -.5, 0], [1, 1, 1, .5, 0], .1),
    (0, 1, 0, -1, 1, 0, [2, 1.5, 1, .5, 0], [-0.02, -0.19358575046493207, -0.2955632294978714, -0.3458556460172404, -0.3468338745078072], .1),
    (0, 0, 1, -1, 1, 0, [2, 1.5, 1, .5, 0], [-1, 1, 1, 1, 1], .1),

])
def test_PID_predetermined(kP: float, kI: float, kD: float, min_clamp: float, max_clamp: float,
                           goal: float, values: list[float], expected: list[float], dT: float):
    pid = PID(kP, kI, kD, min_clamp, max_clamp)
    for i, val in enumerate(values):
        assert np.isclose(pid.calculate(goal, val), expected[i], .1, .1)
        sleep(dT)


@pytest.mark.parametrize("kP, kI, kD, goal, start", [
    (1, 0, 0, 0, 10),
    (1, 1, 0, 5.5, 20)
])
def test_convergence(kP, kI, kD, goal: float, start: float):
    pid = PID(kP, kI, kD, -1, 1, False)
    curr = start
    while not np.isclose(curr, goal):
        curr += pid.calculate(goal, curr)
        print(curr)


def test_graphing():
    pid = PID(1, 0, 0, -10, 10, plot=True)
    curr = 0
    while not np.isclose(curr, 100):
        curr += pid.calculate(100, curr)
    pid.reset()
    assert True


def simulator(kP, kI, kD, goal, start, plot):
    pid = PID(kP, kI, kD, 0, 50, plot)
    t = turtle.Turtle()
    t.penup()
    t.goto(-50, goal)
    t.pendown()
    t.forward(100)
    t.penup()
    t.goto(0, start)
    t.left(90)
    curr = start
    dy = 0
    while True:
        ddy = -9.8 + pid.calculate(goal, curr)
        dy += ddy * .1
        curr = curr + dy * .1
        t.goto(0, curr)
        sleep(.1)


if __name__ == "__main__":
    simulator(.0, 0, 0, 150, -150, True)
