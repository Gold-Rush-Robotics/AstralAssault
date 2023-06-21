from time import perf_counter
from grr.utilities.clamp_range import clamp_range
import matplotlib
import matplotlib.pyplot as plt

from sys import platform as sys_pf
if sys_pf == 'darwin':
    matplotlib.use("TkAgg")


class PID:
    kP: float
    kI: float
    kD: float
    min_clamp: float
    max_clamp: float
    deltaT: float
    _integral: float = 0
    _previous_error: float = 0
    _previous_time: float = -1.
    goal = 0.0
    plot = False
    xList: list[float] = []
    yList1: list[float] = []
    yList2: list[float] = []
    yList3: list[float] = []
    yList4: list[float] = []
    yList5: list[float] = []

    def __init__(self, kP: float, kI: float, kD: float, min_clamp=float('-inf'), max_clamp=float('inf'), plot=False) -> None:
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.min_clamp = min_clamp
        self.max_clamp = max_clamp
        self.plot = plot
        if plot:
            self.fig, (self.ax1, self.ax2, self.ax3, self.ax4, self.ax5) = plt.subplots(5, sharex=True)

    def calculate(self, goal: float, current: float) -> float:
        self.goal = goal
        if self._previous_time == -1:
            self.deltaT = 0.01
            self._previous_time = perf_counter()
        else:
            time = perf_counter()
            self.deltaT = time - self._previous_time
            self._previous_time = time

        error = goal-current

        proportial_component = self.kP * error

        self._integral += error * self.deltaT
        intergral_component = self._integral * self.kI

        derivitive = (error - self._previous_error) / self.deltaT
        derivitive_component = derivitive * self.kD

        output = proportial_component + intergral_component + derivitive_component

        output = clamp_range(output, self.min_clamp, self.max_clamp)

        self._previous_error = error

        if self.plot:
            self.xList.append(self._previous_time)
            self.yList1.append(current)
            self.yList2.append(error)
            self.yList3.append(self._integral)
            self.yList4.append(derivitive)
            self.yList5.append(output)
            self.ax1.cla()
            self.ax1.plot(self.xList, self.yList1)
            self.ax1.plot(self.xList, [goal]*len(self.yList1))
            self.ax1.set(ylabel='value')
            self.ax2.cla()
            self.ax2.plot(self.xList, self.yList2)
            self.ax2.set(ylabel='error')
            self.ax3.cla()
            self.ax3.plot(self.xList, self.yList3)
            self.ax3.set(ylabel='integral')
            self.ax4.cla()
            self.ax4.plot(self.xList, self.yList4)
            self.ax4.set(ylabel='derivitive')
            self.ax5.cla()
            self.ax5.plot(self.xList, self.yList5)
            self.ax5.set(ylabel='output')
            plt.pause(.00000000000000001)

        return output

    def reset(self):
        self._integral = 0
        self._previous_error = 0
        self._previous_time = -1
        self.goal = 0
