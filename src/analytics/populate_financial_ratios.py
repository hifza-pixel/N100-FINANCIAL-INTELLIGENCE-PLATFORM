"""
populate_financial_ratios.py

Sprint 2 – Day 12 & Day 13
Financial Ratio Population Engine
"""

import sqlite3
from pathlib import Path
import os
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

from src.analytics.cashflow_kpis import (
    free_cash_flow,
)

# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE = BASE_DIR / "db" / "nifty100.db"


def get_connection():
    """
    Create SQLite Connection
    """
    return sqlite3.connect(DATABASE)


# ==========================================================
# EDGE CASE LOGGER
# ==========================================================

def log_edge_case(file, company, year, metric, calculated, source):
    """
    Log ROCE / ROE mismatches (>5%)
    """

    if pd.isna(calculated) or pd.isna(source):
        return

    difference = abs(calculated - source)

    if difference <= 5:
        return

    file.write(
        f"""
====================================================
Company      : {company}
Year         : {year}
Metric       : {metric}
Calculated   : {round(calculated,2)}
Source       : {round(source,2)}
Difference   : {round(difference,2)}
Category     : Formula Difference
====================================================

"""
    )


# ==========================================================
# LOAD TABLES
# ==========================================================

def load_tables(conn):

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    pnl = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    balance = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    return (
        companies,
        pnl,
        balance,
        cashflow,
        ratios,
    )


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 70)
    print("Loading SQLite Tables")
    print("=" * 70)

    conn = get_connection()

    (
        companies,
        pnl,
        balance,
        cashflow,
        ratios,
    ) = load_tables(conn)

    print(f"Companies      : {len(companies)}")
    print(f"Profit & Loss  : {len(pnl)}")
    print(f"Balance Sheet  : {len(balance)}")
    print(f"Cash Flow      : {len(cashflow)}")

    print("\nCompanies Columns:")
    print(companies.columns.tolist())

    print("\nMerging Tables...")
    # ==========================================================
# MERGE ALL TABLES
# ==========================================================

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

# ==========================================================
# KPI CALCULATION
# ==========================================================

    print("\nCalculating KPIs...")

    # -------------------------
    # Profitability Ratios
    # -------------------------

    final_df["net_profit_margin_pct"] = final_df.apply(
        lambda x: net_profit_margin(
            x["net_profit"],
            x["sales"],
        ),
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

    # -------------------------
    # Leverage Ratios
    # -------------------------

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

    # -------------------------
    # Cash Flow KPIs
    # -------------------------

    final_df["free_cash_flow_cr"] = final_df.apply(
        lambda x: free_cash_flow(
            x["operating_activity"],
            x["investing_activity"],
        ),
        axis=1,
    )

    # -------------------------
    # Existing Database Values
    # -------------------------

    final_df["earnings_per_share"] = final_df["eps"]

    final_df["book_value_per_share"] = (
        final_df["equity_capital"]
        + final_df["reserves"]
    )

    final_df["dividend_payout_ratio_pct"] = (
        final_df["dividend_payout"]
    )

    final_df["total_debt_cr"] = final_df["borrowings"]

    final_df["cash_from_operations_cr"] = (
        final_df["operating_activity"]
    )

    print("✅ KPI Calculation Completed")

    print(
        final_df[
            [
                "company_id",
                "year",
                "net_profit_margin_pct",
                "operating_profit_margin_pct",
                "return_on_equity_pct",
                "return_on_capital_employed_pct",
                "return_on_assets_pct",
                "debt_to_equity",
                "interest_coverage",
                "asset_turnover",
                "free_cash_flow_cr",
            ]
        ].head()
    )
    # ==========================================================
# UPDATE financial_ratios TABLE
# ==========================================================

    print("\nUpdating financial_ratios table...")

    update_query = """
    UPDATE financial_ratios
    SET
        net_profit_margin_pct=?,
        operating_profit_margin_pct=?,
        return_on_equity_pct=?,
        return_on_capital_employed_pct=?,
        return_on_assets_pct=?,
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
                row["return_on_capital_employed_pct"],
                row["return_on_assets_pct"],
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
            )
        )

        updated_rows += cursor.rowcount

    conn.commit()

    print(f"✅ Updated Rows : {updated_rows}")

# ==========================================================
# VERIFY TABLE
# ==========================================================

    print("\nVerifying financial_ratios table...")

    count_df = pd.read_sql(
        "SELECT COUNT(*) AS total FROM financial_ratios",
        conn,
    )

    total_rows = count_df.loc[0, "total"]

    print(f"Total Rows : {total_rows}")

    if total_rows >= 1100:
        print("✅ PASS : financial_ratios table populated.")
    else:
        print("❌ FAIL : Less than expected rows.")

# ==========================================================
# MANUAL SPOT CHECK
# ==========================================================

    print("\nManual Spot Check\n")

    spot = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            net_profit_margin_pct,
            operating_profit_margin_pct,
            return_on_equity_pct,
            return_on_capital_employed_pct,
            return_on_assets_pct,
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
    # ==========================================================
# DAY 13
# ROCE / ROE EDGE CASE LOGGING
# ==========================================================

    print("\nGenerating ratio_edge_cases.log...")

    os.makedirs("output", exist_ok=True)

    log_path = "output/ratio_edge_cases.log"

    with open(log_path, "w", encoding="utf-8") as log:

        log.write("=" * 70 + "\n")
        log.write("SPRINT 2 - DAY 13\n")
        log.write("ROCE / ROE EDGE CASE REPORT\n")
        log.write("=" * 70 + "\n\n")

        log.write(
            "NOTE:\n"
            "Source dataset does not contain 'broad_sector'.\n"
            "Financial-sector carve-out could not be implemented.\n"
            "Standard ROCE calculation has been applied to all companies.\n\n"
        )

        roce_cases = 0
        roe_cases = 0

        for _, row in final_df.iterrows():

            # -----------------------
            # ROCE Cross Check
            # -----------------------

            if (
                pd.notna(row["return_on_capital_employed_pct"])
                and pd.notna(row["roce_percentage"])
            ):

                difference = abs(
                    row["return_on_capital_employed_pct"]
                    - row["roce_percentage"]
                )

                if difference > 5:

                    roce_cases += 1

                    log.write(
                        f"""
====================================================
Company      : {row['company_name']}
Company ID   : {row['company_id']}
Year         : {row['year']}
Metric       : ROCE

Calculated   : {round(row['return_on_capital_employed_pct'],2)}
Source       : {round(row['roce_percentage'],2)}
Difference   : {round(difference,2)}

Category     : Formula Difference
====================================================

"""
                    )

            # -----------------------
            # ROE Cross Check
            # -----------------------

            if (
                pd.notna(row["return_on_equity_pct"])
                and pd.notna(row["roe_percentage"])
            ):

                difference = abs(
                    row["return_on_equity_pct"]
                    - row["roe_percentage"]
                )

                if difference > 5:

                    roe_cases += 1

                    log.write(
                        f"""
====================================================
Company      : {row['company_name']}
Company ID   : {row['company_id']}
Year         : {row['year']}
Metric       : ROE

Calculated   : {round(row['return_on_equity_pct'],2)}
Source       : {round(row['roe_percentage'],2)}
Difference   : {round(difference,2)}

Category     : Formula Difference
====================================================

"""
                    )

        log.write("\n")
        log.write("=" * 70 + "\n")
        log.write(f"Total ROCE Edge Cases : {roce_cases}\n")
        log.write(f"Total ROE Edge Cases  : {roe_cases}\n")
        log.write("=" * 70 + "\n")

    print(f"✅ ratio_edge_cases.log saved -> {log_path}")
    print(f"ROCE Edge Cases : {roce_cases}")
    print(f"ROE Edge Cases  : {roe_cases}")

# ==========================================================
# FINISH
# ==========================================================

    conn.close()

    print("\n" + "=" * 70)
    print("Sprint 2 - Day 12 & Day 13 Completed Successfully")
    print("=" * 70)


if __name__ == "__main__":
    main()