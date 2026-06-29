"""Utility functions for cleaning and standardizing
raw financial data."""

def normalize_year(year):
    """
    Convert year to integer.

    Example:
    "2024" -> 2024
    2023 -> 2023
    """

    if year is None:
        return None

    return int(str(year).strip())


def normalize_ticker(ticker):
    """
    Standardize stock ticker.

    Example:
    " tcs " -> "TCS"
    "infy" -> "INFY"
    """

    if ticker is None:
        return None

    return str(ticker).strip().upper()