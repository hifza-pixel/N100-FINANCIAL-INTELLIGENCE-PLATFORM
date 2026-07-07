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

def debt_to_equity(borrowings, equity_capital, reserves):
    """
    Debt-to-Equity Ratio

    Formula:
        Borrowings / (Equity Capital + Reserves)

    Rules:
        • Return 0 if borrowings = 0
        • Return None if equity <= 0
    """

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)

def high_leverage_flag(de_ratio, broad_sector):
    """
    High leverage flag.

    Rule:
    D/E > 5 AND company is NOT Financials
    """

    if de_ratio is None:
        return False

    if broad_sector is None:
        broad_sector = ""

    if broad_sector.strip().lower() == "financials":
        return False

    return de_ratio > 5

def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio (ICR)

    Formula:
        (Operating Profit + Other Income) / Interest

    Returns:
        float
        None if interest == 0
    """

    if interest == 0:
        return None

    ebit = operating_profit + other_income

    return round(ebit / interest, 2)

def icr_label(icr):
    """
    Returns display label for ICR.
    """

    if icr is None:
        return "Debt Free"

    return ""


def icr_warning_flag(icr):
    """
    Company may struggle to cover interest.

    Rule:
        ICR < 1.5
    """

    if icr is None:
        return False

    return icr < 1.5

def net_debt(borrowings, investments):
    """
    Net Debt

    Formula:
        Borrowings - Investments

    Returns:
        float
    """

    return round(borrowings - investments, 2)

def asset_turnover(sales, total_assets):
    """
    Asset Turnover

    Formula:
        Sales / Total Assets

    Returns:
        float
        None if total_assets <= 0
    """

    if total_assets <= 0:
        return None

    return round(sales / total_assets, 2)

def is_financial_company(broad_sector):
    """
    Check whether company belongs to Financials sector.

    Returns:
        True / False
    """

    if broad_sector is None:
        return False

    return broad_sector.strip().lower() == "financials"