"""
manual_review.py

Sprint 1 - Day 6
Manual Data Quality Review
"""

import sqlite3
import pandas as pd
import random
import os

DATABASE = "db/nifty100.db"

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect(DATABASE)

# Load companies
companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

# Random 5 companies
sample = companies.sample(5, random_state=42)

report = []

print("="*60)
print("MANUAL REVIEW")
print("="*60)

for _, row in sample.iterrows():

    company = row["id"]
    name = row["company_name"]

    years = pd.read_sql(f"""
        SELECT COUNT(DISTINCT year) AS total_years
        FROM profitandloss
        WHERE company_id='{company}'
    """, conn)

    total = int(years.iloc[0]["total_years"])

    status = "PASS" if total >= 5 else "REVIEW"

    print(f"{company:<15} {name:<30} Years: {total}")

    report.append({
        "company_id": company,
        "company_name": name,
        "year_coverage": total,
        "status": status
    })

report_df = pd.DataFrame(report)

report_df.to_csv(
    "output/manual_review.csv",
    index=False
)

print("\nmanual_review.csv generated successfully.")

conn.close()