import pytest

from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr
)


# -------------------------
# Basic CAGR Tests
# -------------------------

def test_normal_cagr():
    value, flag = calculate_cagr(100, 200, 5)

    assert round(value, 2) == 14.87
    assert flag == "OK"


def test_decline_to_loss():
    value, flag = calculate_cagr(100, -50, 5)

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_turnaround():
    value, flag = calculate_cagr(-100, 50, 5)

    assert value is None
    assert flag == "TURNAROUND"


def test_both_negative():
    value, flag = calculate_cagr(-100, -50, 5)

    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():
    value, flag = calculate_cagr(0, 100, 5)

    assert value is None
    assert flag == "ZERO_BASE"


def test_insufficient():
    value, flag = calculate_cagr(100, 200, 0)

    assert value is None
    assert flag == "INSUFFICIENT"


# -------------------------
# Revenue CAGR
# -------------------------

def test_revenue_cagr():

    history = {
        2019:100,
        2020:120,
        2021:140,
        2022:170,
        2023:200,
        2024:250
    }

    result = revenue_cagr(history)

    assert result["revenue_cagr_5yr_flag"] == "OK"


# -------------------------
# PAT CAGR
# -------------------------

def test_pat_cagr():

    history = {
        2019:100,
        2020:120,
        2021:140,
        2022:170,
        2023:200,
        2024:250
    }

    result = pat_cagr(history)

    assert result["pat_cagr_5yr_flag"] == "OK"


# -------------------------
# EPS CAGR
# -------------------------

def test_eps_cagr():

    history = {
        2019:10,
        2020:12,
        2021:15,
        2022:18,
        2023:22,
        2024:28
    }

    result = eps_cagr(history)

    assert result["eps_cagr_5yr_flag"] == "OK"


# -------------------------
# Insufficient Data
# -------------------------

def test_insufficient_history():

    history = {
        2023:100,
        2024:150
    }

    result = revenue_cagr(history)

    assert result["revenue_cagr_3yr_flag"] == "INSUFFICIENT"