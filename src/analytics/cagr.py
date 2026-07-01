"""
cagr.py

Sprint 2 - Day 10
Compound Annual Growth Rate Engine
"""

def calculate_cagr(start_value, end_value, years):
    """
    CAGR Formula

    CAGR = ((End / Start) ** (1 / Years) - 1) * 100

    Returns:
        (value, flag)
    """

    # Less than required years
    if years <= 0:
        return None, "INSUFFICIENT"

    # Zero base
    if start_value == 0:
        return None, "ZERO_BASE"

    # Positive -> Positive
    if start_value > 0 and end_value > 0:
        cagr = ((end_value / start_value) ** (1 / years) - 1) * 100
        return round(cagr, 2), "OK"

    # Positive -> Negative
    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    # Negative -> Positive
    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    # Negative -> Negative
    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "UNKNOWN"



def revenue_cagr(history):
    return growth_cagr(history, "revenue")    
    """
    Compute Revenue CAGR for
    3Y, 5Y and 10Y.

    Input:
        revenue_history

    Example:

        {
            2015:120,
            2016:135,
            ...
            2024:310
        }

    Returns:

    {
        "revenue_cagr_3yr": ...,
        "revenue_cagr_3yr_flag": ...,
        ...
    }
    """

    result = {}

    if len(revenue_history) == 0:
        return result

    years = sorted(revenue_history.keys())

    latest_year = years[-1]

    windows = [3, 5, 10]

    for window in windows:

        target_year = latest_year - window

        if target_year not in revenue_history:

            result[f"revenue_cagr_{window}yr"] = None
            result[f"revenue_cagr_{window}yr_flag"] = "INSUFFICIENT"

            continue

        start_value = revenue_history[target_year]
        end_value = revenue_history[latest_year]

        value, flag = calculate_cagr(
            start_value,
            end_value,
            window
        )

        result[f"revenue_cagr_{window}yr"] = value
        result[f"revenue_cagr_{window}yr_flag"] = flag

    return result

def growth_cagr(history, metric_name):
    """
    Generic CAGR engine.

    Parameters
    ----------
    history : dict

        Example:
        {
            2020:120,
            2021:150,
            ...
        }

    metric_name

        revenue
        pat
        eps

    Returns
    -------
    dict
    """

    result = {}

    if not history:
        return result

    years = sorted(history.keys())

    latest_year = years[-1]

    for window in [3, 5, 10]:

        target_year = latest_year - window

        if target_year not in history:

            result[f"{metric_name}_cagr_{window}yr"] = None
            result[f"{metric_name}_cagr_{window}yr_flag"] = "INSUFFICIENT"

            continue

        value, flag = calculate_cagr(
            history[target_year],
            history[latest_year],
            window
        )

        result[f"{metric_name}_cagr_{window}yr"] = value
        result[f"{metric_name}_cagr_{window}yr_flag"] = flag

    return result

def pat_cagr(history):
    """
    PAT CAGR Engine
    """
    return growth_cagr(history, "pat")

def eps_cagr(history):
    """
    EPS CAGR Engine
    """
    return growth_cagr(history, "eps")