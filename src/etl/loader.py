"""
loader.py

Loads all Excel source files and displays basic information.
"""

import os
import pandas as pd



DATA_PATH = "data/raw"

FILES = [
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "companies.xlsx",
    "documents.xlsx",
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx"
]

def load_excel(file_name):
    """
    Load Excel file with the correct header row.
    """

    file_path = os.path.join(DATA_PATH, file_name)

    # Files having title row in first row
    title_files = [
        "analysis.xlsx",
        "balancesheet.xlsx",
        "cashflow.xlsx",
        "companies.xlsx",
        "documents.xlsx",
        "profitandloss.xlsx",
        "prosandcons.xlsx"
    ]

    if file_name in title_files:
        df = pd.read_excel(file_path, header=1)
    else:
        df = pd.read_excel(file_path)

    return df

def main():

    print("=" * 60)
    print("N100 Financial Intelligence Platform")
    print("Loading Source Files")
    print("=" * 60)

    for file in FILES:

        try:

            df = load_excel(file)

            print(f"\n✅ {file}")
            print(f"Rows    : {df.shape[0]}")
            print(f"Columns : {df.shape[1]}")

            print("Column Names:")
            print(df.columns.tolist())

        except Exception as e:

            print(f"\n❌ Error loading {file}")
            print(e)


if __name__ == "__main__":
    main()