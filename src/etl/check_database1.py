import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

tables = [
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

for table in tables:

    cursor.execute(f"SELECT COUNT(*) FROM {table}")

    rows = cursor.fetchone()[0]

    print(table, rows)

conn.close()