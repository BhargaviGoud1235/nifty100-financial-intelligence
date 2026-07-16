"""
Sprint 2 - Day 10
CAGR Engine
"""

def calculate_cagr(start_value, end_value, years):
    """
    CAGR Formula:
    ((End / Start) ** (1 / Years) - 1) * 100
    """

    if years <= 0:
        return None, "INVALID_PERIOD"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    cagr = ((end_value / start_value) ** (1 / years) - 1) * 100

    return round(cagr, 2), "OK"