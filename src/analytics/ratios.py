def debt_to_equity(borrowings, equity, reserves):
    """
    Debt-to-Equity Ratio
    """

    capital = equity + reserves

    if borrowings == 0:
        return 0

    if capital <= 0:
        return None

    return round(borrowings / capital, 2)


def high_leverage_flag(de_ratio, sector):
    """
    High leverage warning
    """

    if de_ratio is None:
        return False

    if sector == "Financials":
        return False

    return de_ratio > 5


def interest_coverage_ratio(operating_profit, other_income, interest):
    """
    Interest Coverage Ratio
    """

    if interest == 0:
        return None

    return round((operating_profit + other_income) / interest, 2)


def icr_label(icr):
    """
    Display label
    """

    if icr is None:
        return "Debt Free"

    return ""


def icr_warning(icr):
    """
    Warning if company cannot cover interest
    """

    if icr is None:
        return False

    return icr < 1.5


def net_debt(borrowings, investments):
    """
    Net Debt
    """

    return borrowings - investments


def asset_turnover(sales, total_assets):
    """
    Asset Turnover
    """

    if total_assets == 0:
        return None

    return round(sales / total_assets, 2)