from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE = BASE_DIR / "db" / "nifty100.db"
def get_connection():
    return sqlite3.connect(DATABASE)
def load_peer_groups():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM peer_groups",conn    )
    conn.close()
    return df
def load_financial_ratios():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM financial_ratios",conn    )
    conn.close()
    return df
def merge_data():
    peer = load_peer_groups()
    ratios = load_financial_ratios()
    merged = pd.merge(ratios,peer,on="company_id",how="left")
    print("\nMerged Rows :", len(merged))
    print("\nMerged Columns:")
    print(merged.columns.tolist())
    return merged
def calculate_peer_percentiles(df):
    result = df.copy()
    metrics = [
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "eps_cagr_5yr",
        "interest_coverage",
        "asset_turnover",
        ]
    for metric in metrics:
        if metric not in result.columns:
            result[metric] = 0
    for metric in metrics:
        if metric == "debt_to_equity":
            # Lower D/E = Higher Rank
            result[metric + "_percentile"] = (1- result.groupby("peer_group_name")[metric].rank(pct=True))
        else:
            result[metric + "_percentile"] = (result.groupby("peer_group_name")[metric].rank(pct=True))
    return result
def save_peer_percentiles(df):
    conn = get_connection()
    metric_mapping = {
        "return_on_equity_pct":
        "ROE",
        "return_on_capital_employed_pct":
        "ROCE",
        "net_profit_margin_pct":
        "Net Profit Margin",
        "debt_to_equity":
        "Debt to Equity",
        "free_cash_flow_cr":
        "Free Cash Flow",
        "pat_cagr_5yr":
        "PAT CAGR 5Y",
        "revenue_cagr_5yr":
        "Revenue CAGR 5Y",
        "eps_cagr_5yr":
        "EPS CAGR 5Y",
        "interest_coverage":
        "Interest Coverage",
        "asset_turnover":
        "Asset Turnover",
    }
    rows = []
    for _, record in df.iterrows():
        for column, metric in metric_mapping.items():
            percentile_column = column + "_percentile"
            if (
                column not in df.columns
                or
                percentile_column not in df.columns
            ):
                continue
            rows.append({
                "company_id":
                record["company_id"],
                "peer_group_name":
                record["peer_group_name"],
                "metric":
                metric,
                "value":
                record[column],
                "percentile_rank":
                record[percentile_column],
                "year":
                record["year"]

            })
    output = pd.DataFrame(rows)
    output.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False
    )
    conn.commit()
    conn.close()
    print("\nPeer Percentiles Saved")
    print("Rows :", len(output))
if __name__ == "__main__":
    merged = merge_data()
    ranked = calculate_peer_percentiles(merged)
    save_peer_percentiles(ranked)
    print("\nSample Output\n")
    print(
        ranked[
            [
                "company_id",
                "peer_group_name",
                "return_on_equity_pct_percentile",
                "debt_to_equity_percentile",
            ]].head(10) )