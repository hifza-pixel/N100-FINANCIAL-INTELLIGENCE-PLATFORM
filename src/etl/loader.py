"""
loader.py

Load all Excel files into SQLite Database
"""

import sqlite3
import pandas as pd
import os

DATABASE = "db/nifty100.db"
DATA_PATH = "data/raw"


print("Database Path Used:")
print(os.path.abspath(DATABASE))
TITLE_FILES = [
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "companies.xlsx",
    "documents.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx"
]

FILES = {
    "companies.xlsx": "companies",
    "balancesheet.xlsx": "balancesheet",
    "cashflow.xlsx": "cashflow",
    "profitandloss.xlsx": "profitandloss",
    "financial_ratios.xlsx": "financial_ratios",
    "market_cap.xlsx": "market_cap",
    "peer_groups.xlsx": "peer_groups",
    "analysis.xlsx": "analysis",
    "documents.xlsx": "documents",
    "prosandcons.xlsx": "prosandcons",
    "sectors.xlsx": "sectors"
    
}


def load_excel(file):

    path = os.path.join(DATA_PATH, file)

    if file in TITLE_FILES:
        return pd.read_excel(path, header=1)

    return pd.read_excel(path)


def main():

    conn = sqlite3.connect(DATABASE)

    conn.execute("PRAGMA foreign_keys=ON")

    print("="*60)
    print("Loading Excel Files into SQLite")
    print("="*60)

    audit=[]

    for file, table in FILES.items():

        print(f"\nLoading {file}")

        df=load_excel(file)

        rows=len(df)

        df.to_sql(table,conn,if_exists="replace",index=False)
        conn.commit()

        audit.append({
            "table":table,
            "rows_loaded":rows
        })

        print(f"✓ {rows} rows inserted")

    audit_df=pd.DataFrame(audit)

    os.makedirs("output",exist_ok=True)

    audit_df.to_csv(
        "output/load_audit.csv",
        index=False
    )

    

    conn.close()

    print("\nDatabase Loading Complete.")

    print("Audit File Created")

    print("output/load_audit.csv")


if __name__=="__main__":
    main()