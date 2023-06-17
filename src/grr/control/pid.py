from time import perf_counter
from grr.utilities.clamp_range import clamp_range


class PID:
    kP: float
    kI: float
    kD: float
    min_clamp: float
    max_clamp: float
    deltaT: float
    _integral: float = 0
    _previous_error: float = 0
    _previous_time: float = 0

    def __init__(self, kP: float, kI: float, kD: float, min_clamp=float('-inf'), max_clamp=float('inf')) -> None:
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.min_clamp = min_clamp
        self.max_clamp = max_clamp

    def calculate(self, goal: float, current: float) -> float:
        if not self._previous_time:
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

        return output
