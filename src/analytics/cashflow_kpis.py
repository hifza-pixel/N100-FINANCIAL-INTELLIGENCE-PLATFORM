"""
cashflow_kpis.py

Sprint 2 - Day 11
Cash Flow KPI Engine
"""

import os
import pandas as pd


# ---------------------------------------------------
# KPI FUNCTIONS
# ---------------------------------------------------

def free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow
    """

    return round(operating_activity + investing_activity, 2)


def cfo_quality_score(cfo_history, pat_history):
    """
    Average CFO/PAT Ratio
    """

    if len(cfo_history) != len(pat_history):
        raise ValueError("Length mismatch.")

    ratios = []

    for cfo, pat in zip(cfo_history, pat_history):

        if pat == 0:
            continue

        ratios.append(cfo / pat)

    if len(ratios) == 0:
        return None, None

    average = round(sum(ratios) / len(ratios), 2)

    if average > 1:

        label = "High Quality"

    elif average >= 0.5:

        label = "Moderate"

    else:

        label = "Accrual Risk"

    return average, label


def capex_intensity(investing_activity, sales):

    if sales <= 0:
        return None, None

    value = round(abs(investing_activity) / sales * 100, 2)

    if value < 3:

        label = "Asset Light"

    elif value <= 8:

        label = "Moderate"

    else:

        label = "Capital Intensive"

    return value, label


def fcf_conversion_rate(fcf, operating_profit):

    if operating_profit <= 0:
        return None

    return round((fcf / operating_profit) * 100, 2)


# ---------------------------------------------------
# CAPITAL ALLOCATION
# ---------------------------------------------------

def capital_allocation_pattern(cfo, cfi, cff, cfo_pat_ratio=None):

    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):

        if cfo_pat_ratio is not None and cfo_pat_ratio > 1:
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"

    elif pattern == ("+", "+", "-"):

        label = "Liquidating Assets"

    elif pattern == ("-", "+", "+"):

        label = "Distress Signal"

    elif pattern == ("-", "-", "+"):

        label = "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):

        label = "Cash Accumulator"

    elif pattern == ("-", "-", "-"):

        label = "Pre-Revenue"

    elif pattern == ("+", "-", "+"):

        label = "Mixed"

    else:

        label = "Other"

    return {

        "cfo_sign": cfo_sign,
        "cfi_sign": cfi_sign,
        "cff_sign": cff_sign,
        "pattern_label": label

    }


# ---------------------------------------------------
# CSV GENERATOR
# ---------------------------------------------------

def generate_capital_allocation_csv(df):

    rows = []

    for _, row in df.iterrows():

        ratio = None

        if pd.notna(row["net_profit"]) and row["net_profit"] != 0:

            ratio = row["operating_activity"] / row["net_profit"]

        pattern = capital_allocation_pattern(

            row["operating_activity"],
            row["investing_activity"],
            row["financing_activity"],
            ratio

        )

        rows.append({

            "company_id": row["company_id"],
            "year": row["year"],

            "cfo_sign": pattern["cfo_sign"],
            "cfi_sign": pattern["cfi_sign"],
            "cff_sign": pattern["cff_sign"],

            "pattern_label": pattern["pattern_label"]

        })

    result = pd.DataFrame(rows)

    os.makedirs("output", exist_ok=True)

    output_file = "output/capital_allocation.csv"

    result.to_csv(output_file, index=False)

    print("\n====================================")
    print("Capital Allocation Report Generated")
    print("====================================")
    print(result.head())
    print()
    print("Rows :", len(result))
    print("Saved:", output_file)

    return result


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------

def main():

    print("=" * 60)
    print("Loading Data")
    print("=" * 60)

    cashflow = pd.read_excel(

        "data/raw/cashflow.xlsx",
        header=1

    )

    profit = pd.read_excel(

        "data/raw/profitandloss.xlsx",
        header=1

    )

    print("Cashflow Rows :", len(cashflow))
    print("Profit Rows   :", len(profit))

    final_dataframe = cashflow.merge(

        profit[

            [
                "company_id",
                "year",
                "net_profit"
            ]

        ],

        on=["company_id", "year"],
        how="left"

    )

    print()
    print("Merged Rows :", len(final_dataframe))

    generate_capital_allocation_csv(final_dataframe)


if __name__ == "__main__":
    main()