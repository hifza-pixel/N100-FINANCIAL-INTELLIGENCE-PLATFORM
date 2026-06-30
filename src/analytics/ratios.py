"""
ratios.py

Financial Ratio Engine
Sprint 2 - Day 08
"""

def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin (%)

    Formula:
        (Net Profit / Sales) × 100

    Returns:
        float
        or None if sales is zero
    """

    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)

def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin (%)

    Formula:
        (Operating Profit / Sales) × 100

    Returns:
        float
        or None if sales is zero
    """

    if sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def opm_cross_check(calculated_opm, source_opm, tolerance=1.0):
    """
    Cross-check calculated OPM with source OPM.

    Returns:
        (status, difference)

    status:
        PASS
        MISMATCH
    """

    if calculated_opm is None or source_opm is None:
        return "SKIPPED", None

    difference = abs(calculated_opm - source_opm)

    if difference > tolerance:
        return "MISMATCH", round(difference, 2)

    return "PASS", round(difference, 2)

def return_on_equity(net_profit, equity_capital, reserves):
    """
    Return on Equity (ROE)

    Formula:
        Net Profit / (Equity Capital + Reserves) × 100

    Returns:
        float
        None if equity <= 0
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)   

def return_on_capital_employed(
    operating_profit,
    other_income,
    equity_capital,
    reserves,
    borrowings
):
    """
    Return on Capital Employed (ROCE)

    Formula:
        EBIT / Capital Employed × 100

    EBIT = Operating Profit + Other Income

    Capital Employed =
        Equity Capital + Reserves + Borrowings
    """

    ebit = operating_profit + other_income

    capital_employed = (
        equity_capital
        + reserves
        + borrowings
    )

    if capital_employed <= 0:
        return None

    return round(
        (ebit / capital_employed) * 100,
        2
    )

def roce_benchmark(roce, broad_sector):
    """
    ROCE Benchmark

    Financial companies use sector-relative benchmark.

    Returns:
        NORMAL
        FINANCIAL
    """

    if broad_sector is None:
        return "NORMAL"

    if broad_sector.strip().lower() == "financials":
        return "FINANCIAL"

    return "NORMAL"

def return_on_assets(net_profit, total_assets):
    """
    Return on Assets (ROA)

    Formula:
        Net Profit / Total Assets × 100

    Returns:
        float
        None if total_assets <= 0
    """

    if total_assets <= 0:
        return None

    return round((net_profit / total_assets) * 100, 2) 