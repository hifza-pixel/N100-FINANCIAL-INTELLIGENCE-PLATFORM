"""
populate_financial_ratios.py

Sprint 2 – Day 12
Step 3: Calculate Financial KPIs
"""

from itertools import count
import sqlite3
from pathlib import Path

import pandas as pd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
)

from src.analytics.cashflow_kpis import free_cash_flow


BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE = BASE_DIR / "db" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DATABASE)


def main():

    print("=" * 70)
    print("Loading SQLite Tables")
    print("=" * 70)

    conn = get_connection()

    companies = pd.read_sql("SELECT * FROM companies", conn)
    pnl = pd.read_sql("SELECT * FROM profitandloss", conn)
    balance = pd.read_sql("SELECT * FROM balancesheet", conn)
    cashflow = pd.read_sql("SELECT * FROM cashflow", conn)

    print(f"Companies      : {len(companies)}")
    print(f"Profit & Loss  : {len(pnl)}")
    print(f"Balance Sheet  : {len(balance)}")
    print(f"Cash Flow      : {len(cashflow)}")

    print("\nMerging tables...")

    final_df = pnl.merge(
        balance,
        on=["company_id", "year"],
        how="inner",
        suffixes=("_pnl", "_bs"),
    )

    final_df = final_df.merge(
        cashflow,
        on=["company_id", "year"],
        how="left",
    )

    final_df = final_df.merge(
        companies[
            [
                "id",
                "company_name",
                "roce_percentage",
                "roe_percentage",
            ]
        ],
        left_on="company_id",
        right_on="id",
        how="left",
    )

    print(f"Merged Rows : {len(final_df)}")

    print("\nCalculating KPIs...")

    # Profitability
    final_df["net_profit_margin_pct"] = final_df.apply(
        lambda x: net_profit_margin(x["net_profit"], x["sales"]),
        axis=1,
    )

    final_df["operating_profit_margin_pct"] = final_df.apply(
        lambda x: operating_profit_margin(
            x["operating_profit"],
            x["sales"],
        ),
        axis=1,
    )

    final_df["return_on_equity_pct"] = final_df.apply(
        lambda x: return_on_equity(
            x["net_profit"],
            x["equity_capital"],
            x["reserves"],
        ),
        axis=1,
    )

    final_df["return_on_capital_employed_pct"] = final_df.apply(
    lambda x: return_on_capital_employed(
        x["operating_profit"],
        x["other_income"],
        x["equity_capital"],
        x["reserves"],
        x["borrowings"],
    ),
    axis=1,
)

    final_df["return_on_assets_pct"] = final_df.apply(
        lambda x: return_on_assets(
            x["net_profit"],
            x["total_assets"],
        ),
        axis=1,
    )

    # Leverage
    final_df["debt_to_equity"] = final_df.apply(
        lambda x: debt_to_equity(
            x["borrowings"],
            x["equity_capital"],
            x["reserves"],
        ),
        axis=1,
    )

    final_df["interest_coverage"] = final_df.apply(
        lambda x: interest_coverage_ratio(
            x["operating_profit"],
            x["other_income"],
            x["interest"],
        ),
        axis=1,
    )

    final_df["asset_turnover"] = final_df.apply(
        lambda x: asset_turnover(
            x["sales"],
            x["total_assets"],
        ),
        axis=1,
    )

    # Cash Flow
    final_df["free_cash_flow_cr"] = final_df.apply(
        lambda x: free_cash_flow(
            x["operating_activity"],
            x["investing_activity"],
        ),
        axis=1,
    )

    # Existing values
    final_df["earnings_per_share"] = final_df["eps"]

    final_df["book_value_per_share"] = (
        final_df["equity_capital"] + final_df["reserves"]
    )

    final_df["dividend_payout_ratio_pct"] = final_df["dividend_payout"]

    final_df["total_debt_cr"] = final_df["borrowings"]

    final_df["cash_from_operations_cr"] = final_df["operating_activity"]

    print("✅ KPI calculation completed.\n")

    print(
        final_df[
            [
                "company_id",
                "year",
                "net_profit_margin_pct",
                "operating_profit_margin_pct",
                "return_on_equity_pct",
                "debt_to_equity",
                "interest_coverage",
                "asset_turnover",
                "free_cash_flow_cr",
            ]
        ].head()
    )
    print("\nUpdating financial_ratios table...")

    update_query = """
UPDATE financial_ratios
SET
    net_profit_margin_pct=?,
    operating_profit_margin_pct=?,
    return_on_equity_pct=?,
    debt_to_equity=?,
    interest_coverage=?,
    asset_turnover=?,
    free_cash_flow_cr=?,
    earnings_per_share=?,
    book_value_per_share=?,
    dividend_payout_ratio_pct=?,
    total_debt_cr=?,
    cash_from_operations_cr=?
WHERE
    company_id=? AND year=?
"""

    cursor = conn.cursor()

    updated_rows = 0

    for _, row in final_df.iterrows():

        cursor.execute(
          update_query,
        (
            row["net_profit_margin_pct"],
            row["operating_profit_margin_pct"],
            row["return_on_equity_pct"],
            row["debt_to_equity"],
            row["interest_coverage"],
            row["asset_turnover"],
            row["free_cash_flow_cr"],
            row["earnings_per_share"],
            row["book_value_per_share"],
            row["dividend_payout_ratio_pct"],
            row["total_debt_cr"],
            row["cash_from_operations_cr"],
            row["company_id"],
            row["year"],
        ),
    )

        updated_rows += cursor.rowcount

    conn.commit()

    print(f"Updated Rows : {updated_rows}")
    print("\nVerifying financial_ratios table...")

    count = pd.read_sql(
    "SELECT COUNT(*) AS total FROM financial_ratios",
    conn
)

    print(count)

    if count.loc[0, "total"] >= 1100:
      print(" PASS : financial_ratios table populated.")
    else:
      print(" FAIL : Less than expected rows.")
    print("\nManual Spot Check")

    spot = pd.read_sql(
"""
SELECT
company_id,
year,
net_profit_margin_pct,
operating_profit_margin_pct,
return_on_equity_pct,
debt_to_equity,
interest_coverage,
asset_turnover,
free_cash_flow_cr
FROM financial_ratios
LIMIT 3
""",
conn,
)

    print(spot)  
    conn.close()


if __name__ == "__main__":
    main()