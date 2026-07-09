"""
populate_financial_ratios.py
Sprint 2 - Production Version
Purpose
-------
Populate financial_ratios table with all calculated KPIs
required for Sprint 2 and Sprint 3.
"""
import sqlite3
from pathlib import Path
import numpy as np
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
# PATH CONFIGURATION
BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE = BASE_DIR / "db" / "nifty100.db"

# SQLITE CONNECTION

def get_connection():
    """
    Returns SQLite connection.
    """
    return sqlite3.connect(DATABASE)


# ==========================================================
# LOAD TABLES
# ==========================================================


def load_tables(conn):
    """
    Load all required tables from SQLite.
    """

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn,
    )

    profit_loss = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn,
    )

    balance_sheet = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn,
    )

    cash_flow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn,
    )

    financial_ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )

    return (
        companies,
        profit_loss,
        balance_sheet,
        cash_flow,
        financial_ratios,
    )


# ==========================================================
# SAFE DIVISION
# ==========================================================


def safe_divide(a, b):
    """
    Prevent division by zero.

    Returns None if denominator is invalid.
    """

    if pd.isna(a):
        return None

    if pd.isna(b):
        return None

    if b == 0:
        return None

    return a / b


# ==========================================================
# CAGR FUNCTION
# ==========================================================


def calculate_cagr(start_value, end_value, years):
    """
    CAGR %

    Formula

    ((Ending / Beginning) ** (1 / Years) - 1) * 100
    """

    if pd.isna(start_value):
        return None

    if pd.isna(end_value):
        return None

    if start_value <= 0:
        return None

    if years <= 0:
        return None

    try:

        value = (
            (
                end_value / start_value
            ) ** (1 / years)
            - 1
        ) * 100

        return round(value, 2)

    except Exception:
        return None


# ==========================================================
# SCHEMA CHECK
# ==========================================================


def column_exists(conn, table, column):
    """
    Check whether a column exists.
    """

    cursor = conn.execute(
        f"PRAGMA table_info({table})"
    )

    cols = [row[1] for row in cursor.fetchall()]

    return column in cols


def add_column_if_missing(
    conn,
    table,
    column,
    datatype="REAL",
):
    """
    Automatically add missing column.
    """

    if not column_exists(
        conn,
        table,
        column,
    ):

        print(f"Adding Column -> {column}")

        conn.execute(
            f"""
            ALTER TABLE {table}
            ADD COLUMN {column} {datatype}
            """
        )

        conn.commit()
# ==========================================================
# CREATE REQUIRED KPI COLUMNS
# ==========================================================

def ensure_financial_ratio_schema(conn):
    """
    Ensure all KPI columns exist in financial_ratios table.
    """

    required_columns = [

        # Profitability
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "return_on_assets_pct",

        # Leverage
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",

        # Cash Flow
        "free_cash_flow_cr",
        "capex_cr",
        "cash_from_operations_cr",
        "cfo_pat_ratio",
        "fcf_conversion_ratio",
        "capex_intensity_pct",

        # Growth
        "revenue_cagr_3yr",
        "revenue_cagr_5yr",
        "pat_cagr_3yr",
        "pat_cagr_5yr",
        "eps_cagr_3yr",
        "eps_cagr_5yr",

        # Existing
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "total_debt_cr",

    ]

    print("\nChecking financial_ratios schema...\n")

    for column in required_columns:

        add_column_if_missing(
            conn,
            "financial_ratios",
            column,
            "REAL",
        )

    print("Schema verification completed.\n")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 70)
    print("Loading SQLite Tables")
    print("=" * 70)

    conn = get_connection()

    ensure_financial_ratio_schema(conn)

    (
        companies,
        pnl,
        balance,
        cashflow,
        financial_ratios,
    ) = load_tables(conn)

    print(f"Companies      : {len(companies)}")
    print(f"Profit & Loss  : {len(pnl)}")
    print(f"Balance Sheet  : {len(balance)}")
    print(f"Cash Flow      : {len(cashflow)}")
    print(f"Financial Ratio: {len(financial_ratios)}")

    print("\nMerging Tables...")

    # ----------------------------
    # P&L + Balance Sheet
    # ----------------------------

    final_df = pnl.merge(

        balance,

        on=[
            "company_id",
            "year",
        ],

        how="inner",

        suffixes=(
            "_pnl",
            "_bs",
        ),

    )

    # ----------------------------
    # Cash Flow
    # ----------------------------

    final_df = final_df.merge(

        cashflow,

        on=[
            "company_id",
            "year",
        ],

        how="left",

    )

    # ----------------------------
    # Company Master
    # ----------------------------

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

    print("\nColumns Available:\n")

    print(final_df.columns.tolist())

    print("\nStarting KPI Calculation...\n")
    # ==========================================================
    # PROFITABILITY KPIs
    # ==========================================================

    print("Calculating Profitability KPIs...")

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

    # ==========================================================
    # LEVERAGE KPIs
    # ==========================================================

    print("Calculating Leverage KPIs...")

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

    # ==========================================================
    # CASH FLOW KPIs
    # ==========================================================

    print("Calculating Cash Flow KPIs...")

    final_df["free_cash_flow_cr"] = final_df.apply(
        lambda x: free_cash_flow(
            x["operating_activity"],
            x["investing_activity"],
        ),
        axis=1,
    )

    final_df["cash_from_operations_cr"] = final_df["operating_activity"]

    final_df["total_debt_cr"] = final_df["borrowings"]

    final_df["earnings_per_share"] = final_df["eps"]

    final_df["book_value_per_share"] = (
        final_df["equity_capital"]
        + final_df["reserves"]
    )

    final_df["dividend_payout_ratio_pct"] = (
        final_df["dividend_payout"]
    )

    # ==========================================================
    # EXTRA CASH FLOW METRICS
    # ==========================================================

    final_df["capex_cr"] = (
        final_df["investing_activity"] * (-1)
    )

    final_df["cfo_pat_ratio"] = final_df.apply(
        lambda x: safe_divide(
            x["operating_activity"],
            x["net_profit"],
        ),
        axis=1,
    )

    final_df["fcf_conversion_ratio"] = final_df.apply(
        lambda x: safe_divide(
            x["free_cash_flow_cr"],
            x["operating_activity"],
        ),
        axis=1,
    )

    final_df["capex_intensity_pct"] = final_df.apply(
        lambda x: safe_divide(
            abs(x["capex_cr"]),
            x["sales"],
        ) * 100
        if safe_divide(abs(x["capex_cr"]), x["sales"]) is not None
        else None,
        axis=1,
    )

    print("Profitability + Leverage + Cash Flow KPIs Completed.")
    # ==========================================================
    # GROWTH KPIs (3Y & 5Y CAGR)
    # ==========================================================

    print("Calculating Growth KPIs...")

    # Initialize columns

    final_df["revenue_cagr_3yr"] = None
    final_df["revenue_cagr_5yr"] = None

    final_df["pat_cagr_3yr"] = None
    final_df["pat_cagr_5yr"] = None

    final_df["eps_cagr_3yr"] = None
    final_df["eps_cagr_5yr"] = None

    # Calculate company-wise CAGR

    for company in final_df["company_id"].unique():

        company_df = (
            final_df[
                final_df["company_id"] == company
            ]
            .copy()
            .sort_values("year")
            .reset_index()
        )

        for i in range(len(company_df)):

            # -------------------------
            # Revenue CAGR
            # -------------------------

            if i >= 3:

                final_df.loc[
                    company_df.loc[i, "index"],
                    "revenue_cagr_3yr",
                ] = calculate_cagr(
                    company_df.loc[i - 3, "sales"],
                    company_df.loc[i, "sales"],
                    3,
                )

            if i >= 5:

                final_df.loc[
                    company_df.loc[i, "index"],
                    "revenue_cagr_5yr",
                ] = calculate_cagr(
                    company_df.loc[i - 5, "sales"],
                    company_df.loc[i, "sales"],
                    5,
                )

            # -------------------------
            # PAT CAGR
            # -------------------------

            if i >= 3:

                final_df.loc[
                    company_df.loc[i, "index"],
                    "pat_cagr_3yr",
                ] = calculate_cagr(
                    company_df.loc[i - 3, "net_profit"],
                    company_df.loc[i, "net_profit"],
                    3,
                )

            if i >= 5:

                final_df.loc[
                    company_df.loc[i, "index"],
                    "pat_cagr_5yr",
                ] = calculate_cagr(
                    company_df.loc[i - 5, "net_profit"],
                    company_df.loc[i, "net_profit"],
                    5,
                )

            # -------------------------
            # EPS CAGR
            # -------------------------

            if i >= 3:

                final_df.loc[
                    company_df.loc[i, "index"],
                    "eps_cagr_3yr",
                ] = calculate_cagr(
                    company_df.loc[i - 3, "eps"],
                    company_df.loc[i, "eps"],
                    3,
                )

            if i >= 5:

                final_df.loc[
                    company_df.loc[i, "index"],
                    "eps_cagr_5yr",
                ] = calculate_cagr(
                    company_df.loc[i - 5, "eps"],
                    company_df.loc[i, "eps"],
                    5,
                )

    print("Growth KPI Calculation Completed.")

    print("\nGrowth KPI Sample\n")

    print(

        final_df[
            [
                "company_id",
                "year",
                "revenue_cagr_3yr",
                "revenue_cagr_5yr",
                "pat_cagr_3yr",
                "pat_cagr_5yr",
                "eps_cagr_3yr",
                "eps_cagr_5yr",
            ]
        ].head(10)

    )
        # ==========================================================
    # UPDATE financial_ratios TABLE
    # ==========================================================

    print("\nUpdating financial_ratios table...\n")

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
        capex_cr=?,
        earnings_per_share=?,
        book_value_per_share=?,
        dividend_payout_ratio_pct=?,
        total_debt_cr=?,
        cash_from_operations_cr=?,
        cfo_pat_ratio=?,
        fcf_conversion_ratio=?,
        capex_intensity_pct=?,
        revenue_cagr_3yr=?,
        revenue_cagr_5yr=?,
        pat_cagr_3yr=?,
        pat_cagr_5yr=?,
        eps_cagr_3yr=?,
        eps_cagr_5yr=?
    WHERE
        company_id=?
        AND year=?
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
                row["capex_cr"],
                row["earnings_per_share"],
                row["book_value_per_share"],
                row["dividend_payout_ratio_pct"],
                row["total_debt_cr"],
                row["cash_from_operations_cr"],
                row["cfo_pat_ratio"],
                row["fcf_conversion_ratio"],
                row["capex_intensity_pct"],
                row["revenue_cagr_3yr"],
                row["revenue_cagr_5yr"],
                row["pat_cagr_3yr"],
                row["pat_cagr_5yr"],
                row["eps_cagr_3yr"],
                row["eps_cagr_5yr"],
                row["company_id"],
                row["year"],
            ),
        )

        updated_rows += cursor.rowcount

    conn.commit()

    print(f"Updated Rows : {updated_rows}")
        # ==========================================================
    # VERIFY DATABASE
    # ==========================================================

    print("\nVerifying financial_ratios table...\n")

    count = pd.read_sql(
        "SELECT COUNT(*) AS total FROM financial_ratios",
        conn,
    )

    print(count)

    if count.loc[0, "total"] >= 1100:
        print("\nPASS : financial_ratios populated successfully.")
    else:
        print("\nWARNING : Less than expected rows.")

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
            free_cash_flow_cr,
            revenue_cagr_5yr,
            pat_cagr_5yr,
            eps_cagr_5yr
        FROM financial_ratios
        LIMIT 10
        """,
        conn,
    )

    print(spot)

    print("\nDatabase Update Completed Successfully.")

    conn.close()


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    main()            