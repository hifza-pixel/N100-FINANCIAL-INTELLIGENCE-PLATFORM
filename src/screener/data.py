import sqlite3
import os

db = r"C:\Users\Dell\Desktop\Nifty100_Projecct\db\nifty100.db"

print("Exists:", os.path.exists(db))
print("Size:", os.path.getsize(db))

conn = sqlite3.connect(db)
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM companies")
print("Companies:", cur.fetchone()[0])

cur.execute("SELECT COUNT(*) FROM profitandloss")
print("Profit & Loss:", cur.fetchone()[0])

conn.close()