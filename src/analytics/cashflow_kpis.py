"""
Sprint 2 - Day 11
Cash Flow KPIs & Capital Allocation
"""


def free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow = Operating Activity + Investing Activity

    Negative FCF is allowed.
    """
    if operating_activity is None or investing_activity is None:
        return None

    return round(operating_activity + investing_activity, 2)


def cfo_quality_score(cfo, pat):
    """
    CFO Quality Score = CFO / PAT

    Returns:
    - High Quality: > 1.0
    - Moderate: 0.5 to 1.0
    - Accrual Risk: < 0.5

    Returns None if PAT = 0.
    """

    if cfo is None or pat is None:
        return None, None

    if pat == 0:
        return None, None

    ratio = cfo / pat

    if ratio > 1.0:
        label = "High Quality"
    elif ratio >= 0.5:
        label = "Moderate"
    else:
        label = "Accrual Risk"

    return round(ratio, 2), label


def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity = abs(Investing Activity) / Sales * 100

    < 3%   = Asset Light
    3-8%   = Moderate
    > 8%   = Capital Intensive
    """

    if investing_activity is None or sales is None:
        return None, None

    if sales == 0:
        return None, None

    intensity = abs(investing_activity) / sales * 100

    if intensity < 3:
        label = "Asset Light"
    elif intensity <= 8:
        label = "Moderate"
    else:
        label = "Capital Intensive"

    return round(intensity, 2), label


def fcf_conversion_rate(fcf, operating_profit):
    """
    FCF Conversion Rate = FCF / Operating Profit * 100

    Returns None if operating profit = 0.
    """

    if fcf is None or operating_profit is None:
        return None

    if operating_profit == 0:
        return None

    return round((fcf / operating_profit) * 100, 2)


def capital_allocation_pattern(cfo, cfi, cff, cfo_pat_ratio=None):
    """
    Classify capital allocation pattern using signs of:
    CFO = Cash Flow from Operations
    CFI = Cash Flow from Investing
    CFF = Cash Flow from Financing
    """

    if cfo is None or cfi is None or cff is None:
        return None

    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):
        if cfo_pat_ratio is not None and cfo_pat_ratio > 1.0:
            return "Shareholder Returns"
        return "Reinvestor"

    if pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    if pattern == ("-", "+", "+"):
        return "Distress Signal"

    if pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    if pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    if pattern == ("+", "-", "+"):
        return "Mixed"

    return "Unknown"


def get_cash_flow_sign(value):
    """
    Return + or - based on cash flow value.
    """

    if value is None:
        return None

    return "+" if value >= 0 else "-"