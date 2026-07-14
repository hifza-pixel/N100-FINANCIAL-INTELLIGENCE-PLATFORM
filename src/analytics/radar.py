from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE = BASE_DIR / "db" / "nifty100.db"
OUTPUT = BASE_DIR / "reports" / "radar_charts"
def get_connection():
    return sqlite3.connect(DATABASE)
def load_peer_percentiles():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM peer_percentiles",conn,)
    conn.close()
    return df
def get_company_data(df, company_id):
    metrics = [
        "ROE",
        "ROCE",
        "Net Profit Margin",
        "Debt to Equity",
        "Free Cash Flow",
        "PAT CAGR 5Y",
        "Revenue CAGR 5Y",
        "Asset Turnover",
    ]
    company = df[
        (df["company_id"] == company_id)
        &
        (df["metric"].isin(metrics))].copy()
    company = company.drop_duplicates(subset="metric")
    return company
def create_radar_chart(company_df, peer_avg):
    if company_df.empty:
        return
    if peer_avg.empty:
        return
    OUTPUT.mkdir(parents=True,exist_ok=True,)
    metrics = [
        "ROE",
        "ROCE",
        "Net Profit Margin",
        "Debt to Equity",
        "Free Cash Flow",
        "PAT CAGR 5Y",
        "Revenue CAGR 5Y",
        "Asset Turnover",
    ]
    company_df = (company_df.set_index("metric").reindex(metrics).fillna(0).reset_index() )
    peer_avg = (peer_avg.set_index("metric").reindex(metrics).fillna(0).reset_index())
    labels = metrics
    values = company_df["percentile_rank"].tolist()
    peer_values = peer_avg["percentile_rank"].tolist()
    values += values[:1]
    peer_values += peer_values[:1]
    labels += labels[:1]
    angles = np.linspace(0,2 * np.pi,len(labels),endpoint=True,)
    company_name = company_df.iloc[0]["company_id"]
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    ax.plot(angles,values,linewidth=2,label=company_name,)
    ax.fill(angles,values,alpha=0.25,)
    ax.plot(angles,peer_values,linestyle="--",linewidth=2,label="Peer / Nifty Average",)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels[:-1])
    ax.set_ylim(0, 1)
    ax.legend(loc="upper right")
    plt.title(f"{company_name}\nPeer Comparison Radar",fontsize=14,)
    filename = OUTPUT / f"{company_name}_radar.png"
    plt.savefig(filename,dpi=300,bbox_inches="tight",)
    plt.close()
    print(f"Saved: {company_name}")
def generate_all_radar_charts(df):
    companies = sorted(df["company_id"].dropna().unique())
    generated = 0
    skipped = 0
    for company in companies:
        company_df = get_company_data(df, company)
        peer_avg = get_peer_average(df, company)
        if company_df.empty:
          print(f"Skipped : {company}")
          continue
        if peer_avg.empty:
           peer_avg = get_nifty_average(df)
           print(f"{company} -> Using Nifty100 Average")
        create_radar_chart(company_df, peer_avg,)
        generated += 1
    print()
    print("Charts Generated :", generated)
    print("Skipped :", skipped)
def get_peer_average(df, company_id):
    company = df[df["company_id"] == company_id]
    if company.empty:
        return pd.DataFrame()
    peer_group = company.iloc[0]["peer_group_name"]
    metrics = [
        "ROE",
        "ROCE",
        "Net Profit Margin",
        "Debt to Equity",
        "Free Cash Flow",
        "PAT CAGR 5Y",
        "Revenue CAGR 5Y",
        "Asset Turnover",
    ]
    peer = df[
        (df["peer_group_name"] == peer_group)
        &
        (df["metric"].isin(metrics))]
    average = (peer.groupby("metric", as_index=False)["percentile_rank"].mean())
    return average
def get_nifty_average(df):
    average = (df.groupby("metric")["percentile_rank"].mean().reset_index())
    return average
if __name__ == "__main__":
    df = load_peer_percentiles()
    generate_all_radar_charts(df)