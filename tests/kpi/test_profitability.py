import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    opm_cross_check,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets
)


# ---------- Net Profit Margin ----------

def test_npm_normal():
    assert net_profit_margin(500, 1000) == 50.0


def test_npm_zero_sales():
    assert net_profit_margin(100, 0) is None


# ---------- OPM ----------

def test_opm_normal():
    assert operating_profit_margin(300, 1000) == 30.0


def test_opm_crosscheck():
    status, diff = opm_cross_check(30, 28)
    assert status == "MISMATCH"
    assert diff == 2.0


# ---------- ROE ----------

def test_roe_normal():
    assert return_on_equity(500, 1000, 500) == 33.33


def test_roe_negative_equity():
    assert return_on_equity(100, 100, -200) is None


# ---------- ROCE ----------

def test_roce_normal():
    assert (
        return_on_capital_employed(
            500,
            50,
            1000,
            500,
            500
        ) == 27.5
    )


# ---------- ROA ----------

def test_roa_zero_assets():
    assert return_on_assets(100, 0) is None