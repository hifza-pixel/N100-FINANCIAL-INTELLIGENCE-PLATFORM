"""
load_audit.py

Sprint 1 - Day 5
Load Audit & Database Verification
"""

import sqlite3
import pandas as pd
import os

DATABASE = "db/nifty100.db"

TABLES = [
    "companies",
    "balancesheet",
    "cashflow",
    "profitandloss",
    "financial_ratios",
    "market_cap",
    "peer_groups",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "stock_prices"
]

os.makedirs("output", exist_ok=True)


def main():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    audit = []

    print("="*60)
    print("LOAD AUDIT")
    print("="*60)

    for table in TABLES:

        cursor.execute(f"SELECT COUNT(*) FROM {table}")

        rows = cursor.fetchone()[0]

        audit.append({
            "table": table,
            "rows_loaded": rows
        })

        print(f"{table:<20} {rows}")

    audit_df = pd.DataFrame(audit)

    audit_df.to_csv(
        "output/load_audit.csv",
        index=False
    )

    print("\nload_audit.csv generated successfully.")

    conn.close()


if __name__ == "__main__":
    main()