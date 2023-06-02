def clamp_range(value: float, minimum: float, maximum: float) -> float:
    if (maximum < minimum):
        raise ValueError(f"Max({maximum}) smaller than min({minimum})")
    return min(maximum, max(minimum, value))
