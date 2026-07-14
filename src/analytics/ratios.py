"""
Sprint 2 - Day 08
Profitability Ratio Engine
"""

def net_profit_margin(net_profit, sales):
    """Net Profit Margin (%)"""
    if sales == 0:
        return None
    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):
    """Operating Profit Margin (%)"""
    if sales == 0:
        return None
    return round((operating_profit / sales) * 100, 2)


def check_opm(computed_opm, source_opm):
    """Cross-check OPM"""
    if computed_opm is None or source_opm is None:
        return False

    return abs(computed_opm - source_opm) > 1


def return_on_equity(net_profit, equity_capital, reserves):
    """ROE (%)"""
    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    operating_profit,
    interest,
    equity_capital,
    reserves,
    borrowings
):
    """
    ROCE (%)
    EBIT = Operating Profit + Interest
    """

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    ebit = operating_profit + interest

    return round((ebit / capital) * 100, 2)


def return_on_assets(net_profit, total_assets):
    """ROA (%)"""

    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)