"""
Sprint 2 - Day 10
CAGR Engine
"""


def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR percentage.

    Returns:
        (cagr_value, flag)
    """

    if start_value is None or end_value is None:
        return None, "INSUFFICIENT"

    if years <= 0:
        return None, "INSUFFICIENT"

    # Zero base
    if start_value == 0:
        return None, "ZERO_BASE"

    # Positive -> Positive
    if start_value > 0 and end_value > 0:

        cagr = (
            (end_value / start_value) ** (1 / years) - 1
        ) * 100

        return round(cagr, 2), None

    # Positive -> Negative
    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    # Negative -> Positive
    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    # Negative -> Negative
    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "INSUFFICIENT"