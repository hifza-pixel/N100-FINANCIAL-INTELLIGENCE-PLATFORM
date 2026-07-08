from pathlib import Path
import sqlite3
import pandas as pd
import yaml

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE = BASE_DIR / "db" / "nifty100.db"

CONFIG = BASE_DIR / "config" / "screener_config.yaml"


# ==========================
# Load YAML Config
# ==========================

def load_config():

    with open(CONFIG, "r") as file:
        return yaml.safe_load(file)


# ==========================
# Load financial_ratios table
# ==========================

def load_financial_ratios():

    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )

    conn.close()

    return df
def apply_filters(df, config):
    """
    Apply Screener Filters from YAML Config
    """

    filters = config["filters"]

    result = df.copy()

    # ROE
    if "roe_min" in filters:
        result = result[
            result["return_on_equity_pct"] >= filters["roe_min"]
        ]

    # Debt to Equity
    if "debt_to_equity_max" in filters:
        result = result[
            result["debt_to_equity"] <= filters["debt_to_equity_max"]
        ]

    # Free Cash Flow
    if "free_cash_flow_min" in filters:
        result = result[
            result["free_cash_flow_cr"] >= filters["free_cash_flow_min"]
        ]

    # Revenue CAGR
    if "revenue_cagr_5yr_min" in filters and "revenue_cagr_5yr" in result.columns:
        result = result[
            result["revenue_cagr_5yr"] >= filters["revenue_cagr_5yr_min"]
        ]

    # PAT CAGR
    if "pat_cagr_5yr_min" in filters and "pat_cagr_5yr" in result.columns:
        result = result[
            result["pat_cagr_5yr"] >= filters["pat_cagr_5yr_min"]
        ]

    # Operating Profit Margin
    if "operating_profit_margin_min" in filters:
        result = result[
            result["operating_profit_margin_pct"] >= filters["operating_profit_margin_min"]
        ]

    # Interest Coverage
    if "interest_coverage_min" in filters:
        result = result[
            (
                result["interest_coverage"] >= filters["interest_coverage_min"]
            )
            |
            (
                result["interest_coverage"].isna()
            )
        ]

    # Asset Turnover
    if "asset_turnover_min" in filters:
        result = result[
            result["asset_turnover"] >= filters["asset_turnover_min"]
        ]

    # Net Profit
    if "net_profit_min" in filters and "net_profit" in result.columns:
        result = result[
            result["net_profit"] >= filters["net_profit_min"]
        ]

    # Sales
    if "sales_min" in filters and "sales" in result.columns:
        result = result[
            result["sales"] >= filters["sales_min"]
        ]

    return result.reset_index(drop=True)

def calculate_composite_score(df):
    """
    Basic Composite Quality Score (Day 15)

    Day 17 me isko weighted scoring se replace karenge.
    """

    result = df.copy()

    metrics = [
        "return_on_equity_pct",
        "operating_profit_margin_pct",
        "asset_turnover",
        "interest_coverage",
        "free_cash_flow_cr",
    ]

    for metric in metrics:

        if metric not in result.columns:
            continue

        minimum = result[metric].min()
        maximum = result[metric].max()

        if minimum == maximum:

            result[metric + "_score"] = 50

        else:

            result[metric + "_score"] = (
                (
                    result[metric] - minimum
                )
                /
                (
                    maximum - minimum
                )
            ) * 100

    score_columns = [
        col
        for col in result.columns
        if col.endswith("_score")
    ]

    result["composite_quality_score"] = (
        result[score_columns]
        .mean(axis=1)
        .round(2)
    )

    return result
# ==========================
# Main
# ==========================

if __name__ == "__main__":

    config = load_config()

    df = load_financial_ratios()

    print("Original Rows :", len(df))

    filtered = apply_filters(df, config)

    print("Filtered Rows :", len(filtered))

    print(filtered.head())
    filtered = calculate_composite_score(filtered)

    filtered = filtered.sort_values(
        by="composite_quality_score",
        ascending=False,
    ).reset_index(drop=True)
    print("\nTop Companies\n")

print(

    filtered[
        [
            "company_id",
            "year",
            "return_on_equity_pct",
            "debt_to_equity",
            "composite_quality_score",
        ]
    ].head(10)

)