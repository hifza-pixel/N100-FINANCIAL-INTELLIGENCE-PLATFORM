
"""
validator.py

N100 Financial Intelligence Platform
Sprint 1 - Day 3

Production Data Quality Validator
Part 1

Implements:
DQ-01 Primary Key
DQ-02 Composite Key
DQ-03 Foreign Key
DQ-04 Balance Sheet Validation
"""

import os
import pandas as pd

# ==========================================================
# CONFIGURATION
# ==========================================================

DATA_PATH = "data/raw"
OUTPUT_PATH = "output"

TITLE_FILES = [
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "companies.xlsx",
    "documents.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx"
]

FILES = [
    "companies.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "profitandloss.xlsx",
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "stock_prices.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "peer_groups.xlsx",
    "prosandcons.xlsx",
    "sectors.xlsx"
]

os.makedirs(OUTPUT_PATH, exist_ok=True)

validation_failures = []
validation_summary = []

# ==========================================================
# LOADER
# ==========================================================

def load_file(file_name):

    file_path = os.path.join(DATA_PATH, file_name)

    if file_name in TITLE_FILES:
        return pd.read_excel(file_path, header=1)

    return pd.read_excel(file_path)

# ==========================================================
# LOGGER
# ==========================================================

def add_failure(table, rule, severity, row, message):

    validation_failures.append({
        "table": table,
        "rule": rule,
        "severity": severity,
        "row": row,
        "message": message
    })


def add_summary(rule, passed, failed):

    validation_summary.append({
        "rule": rule,
        "passed": passed,
        "failed": failed
    })

# ==========================================================
# DQ-01 PRIMARY KEY
# ==========================================================

def dq01_primary_key(df, table):

    if "id" not in df.columns:
        return

    duplicates = df[df["id"].duplicated()]

    if duplicates.empty:

        print(f"✅ DQ-01 PASS : {table}")

        add_summary("DQ-01", len(df), 0)

    else:

        print(f"❌ DQ-01 FAIL : {table}")

        for idx in duplicates.index:

            add_failure(
                table,
                "DQ-01",
                "CRITICAL",
                int(idx),
                "Duplicate Primary Key"
            )

        add_summary(
            "DQ-01",
            len(df)-len(duplicates),
            len(duplicates)
        )

# ==========================================================
# DQ-02 COMPOSITE KEY
# ==========================================================

def dq02_composite_key(df, table):

    required = ["company_id","year"]

    if not all(c in df.columns for c in required):
        return

    duplicates = df[df.duplicated(
        subset=["company_id","year"]
    )]

    if duplicates.empty:

        print(f"✅ DQ-02 PASS : {table}")

        add_summary("DQ-02", len(df),0)

    else:

        print(f"❌ DQ-02 FAIL : {table}")

        for idx in duplicates.index:

            add_failure(
                table,
                "DQ-02",
                "CRITICAL",
                int(idx),
                "Duplicate company_id-year"
            )

        add_summary(
            "DQ-02",
            len(df)-len(duplicates),
            len(duplicates)
        )

# ==========================================================
# DQ-03 FOREIGN KEY
# ==========================================================

def dq03_foreign_key(df, companies, table):

    if "company_id" not in df.columns:
        return

    valid = set(companies["id"])

    invalid = df[
        ~df["company_id"].isin(valid)
    ]

    if invalid.empty:

        print(f"✅ DQ-03 PASS : {table}")

        add_summary(
            "DQ-03",
            len(df),
            0
        )

    else:

        print(f"❌ DQ-03 FAIL : {table}")

        for idx in invalid.index:

            add_failure(
                table,
                "DQ-03",
                "CRITICAL",
                int(idx),
                "Foreign Key Missing"
            )

        add_summary(
            "DQ-03",
            len(df)-len(invalid),
            len(invalid)
        )

# ==========================================================
# DQ-04 BALANCE SHEET
# ==========================================================

def dq04_balance_sheet(df):

    if (
        "total_assets" not in df.columns
        or
        "total_liabilities" not in df.columns
    ):
        return

    diff = (
        abs(
            df["total_assets"]-
            df["total_liabilities"]
        )
        /
        df["total_assets"]
    )*100

    invalid = df[diff>1]

    if invalid.empty:

        print("✅ DQ-04 PASS")

        add_summary(
            "DQ-04",
            len(df),
            0
        )

    else:

        print("❌ DQ-04 FAIL")

        for idx in invalid.index:

            add_failure(
                "balancesheet.xlsx",
                "DQ-04",
                "WARNING",
                int(idx),
                "Balance Sheet Difference >1%"
            )

        add_summary(
            "DQ-04",
            len(df)-len(invalid),
            len(invalid)
        )
# ==========================================================
# DQ-05 OPM CROSS CHECK
# ==========================================================

def dq05_opm(df):

    required = ["sales", "operating_profit", "opm_percentage"]

    if not all(col in df.columns for col in required):
        return

    calc = (df["operating_profit"] / df["sales"]) * 100

    diff = abs(calc - df["opm_percentage"])

    invalid = df[diff > 1]

    if invalid.empty:

        print("✅ DQ-05 PASS")

        add_summary("DQ-05", len(df), 0)

    else:

        print("❌ DQ-05 FAIL")

        for idx in invalid.index:

            add_failure(
                "profitandloss.xlsx",
                "DQ-05",
                "WARNING",
                int(idx),
                "Incorrect OPM%"
            )

        add_summary(
            "DQ-05",
            len(df)-len(invalid),
            len(invalid)
        )
# ==========================================================
# DQ-06 POSITIVE SALES
# ==========================================================

def dq06_positive_sales(df):

    if "sales" not in df.columns:
        return

    invalid = df[df["sales"] <= 0]

    if invalid.empty:

        print("✅ DQ-06 PASS")

        add_summary("DQ-06", len(df), 0)

    else:

        print("❌ DQ-06 FAIL")

        for idx in invalid.index:

            add_failure(
                "profitandloss.xlsx",
                "DQ-06",
                "CRITICAL",
                int(idx),
                "Sales must be positive"
            )

        add_summary(
            "DQ-06",
            len(df)-len(invalid),
            len(invalid)
        )
# ==========================================================
# DQ-07 NET CASH FLOW
# ==========================================================

def dq07_net_cash(df):

    required = [
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow"
    ]

    if not all(col in df.columns for col in required):
        return

    calc = (
        df["operating_activity"]
        + df["investing_activity"]
        + df["financing_activity"]
    )

    diff = abs(calc - df["net_cash_flow"])

    invalid = df[diff > 1]

    if invalid.empty:

        print("✅ DQ-07 PASS")

        add_summary("DQ-07", len(df), 0)

    else:

        print("❌ DQ-07 FAIL")

        for idx in invalid.index:

            add_failure(
                "cashflow.xlsx",
                "DQ-07",
                "WARNING",
                int(idx),
                "Net Cash Flow mismatch"
            )

        add_summary(
            "DQ-07",
            len(df)-len(invalid),
            len(invalid)
        )
# ==========================================================
# DQ-08 TAX RATE
# ==========================================================

def dq08_tax(df):

    if "tax_percentage" not in df.columns:
        return

    invalid = df[
        (df["tax_percentage"] < 0)
        |
        (df["tax_percentage"] > 100)
    ]

    if invalid.empty:

        print("✅ DQ-08 PASS")

        add_summary("DQ-08", len(df), 0)

    else:

        print("❌ DQ-08 FAIL")

        for idx in invalid.index:

            add_failure(
                "profitandloss.xlsx",
                "DQ-08",
                "WARNING",
                int(idx),
                "Tax rate outside 0-100%"
            )

        add_summary(
            "DQ-08",
            len(df)-len(invalid),
            len(invalid)
        )
# ==========================================================
# DQ-09 DIVIDEND PAYOUT
# ==========================================================

def dq09_dividend(df):

    if "dividend_payout" not in df.columns:
        return

    invalid = df[
        (df["dividend_payout"] < 0)
        |
        (df["dividend_payout"] > 100)
    ]

    if invalid.empty:

        print("✅ DQ-09 PASS")

        add_summary("DQ-09", len(df), 0)

    else:

        print("❌ DQ-09 FAIL")

        for idx in invalid.index:

            add_failure(
                "profitandloss.xlsx",
                "DQ-09",
                "WARNING",
                int(idx),
                "Dividend payout outside 0-100%"
            )

        add_summary(
            "DQ-09",
            len(df)-len(invalid),
            len(invalid)
        )
# ==========================================================
# DQ-10 EPS
# ==========================================================

def dq10_eps(df):

    if "eps" not in df.columns:
        return

    invalid = df[df["eps"].isna()]

    if invalid.empty:

        print("✅ DQ-10 PASS")

        add_summary("DQ-10", len(df), 0)

    else:

        print("❌ DQ-10 FAIL")

        for idx in invalid.index:

            add_failure(
                "profitandloss.xlsx",
                "DQ-10",
                "WARNING",
                int(idx),
                "EPS missing"
            )

        add_summary(
            "DQ-10",
            len(df)-len(invalid),
            len(invalid)
        )
# ==========================================================
# DQ-11 DUPLICATE COMPANY NAME
# ==========================================================

def dq11_duplicate_company(df):

    if "company_name" not in df.columns:
        return

    invalid = df[df["company_name"].duplicated()]

    if invalid.empty:

        print("✅ DQ-11 PASS")

        add_summary("DQ-11", len(df), 0)

    else:

        print("❌ DQ-11 FAIL")

        for idx in invalid.index:

            add_failure(
                "companies.xlsx",
                "DQ-11",
                "WARNING",
                int(idx),
                "Duplicate company name"
            )

        add_summary(
            "DQ-11",
            len(df)-len(invalid),
            len(invalid)
        )
# ==========================================================
# DQ-12 WEBSITE URL
# ==========================================================

def dq12_url(df):

    if "website" not in df.columns:
        return

    invalid = df[
        ~df["website"].fillna("").str.startswith(("http://","https://"))
    ]

    if invalid.empty:

        print("✅ DQ-12 PASS")

        add_summary("DQ-12", len(df), 0)

    else:

        print("❌ DQ-12 FAIL")

        for idx in invalid.index:

            add_failure(
                "companies.xlsx",
                "DQ-12",
                "WARNING",
                int(idx),
                "Invalid Website URL"
            )

        add_summary(
            "DQ-12",
            len(df)-len(invalid),
            len(invalid)
        )
# ==========================================================
# DQ-13 MISSING YEARS
# ==========================================================

def dq13_missing_year(df, table):

    if "year" not in df.columns:
        return

    invalid = df[df["year"].isna()]

    if invalid.empty:

        print("✅ DQ-13 PASS")

        add_summary("DQ-13", len(df), 0)

    else:

        print("❌ DQ-13 FAIL")

        for idx in invalid.index:

            add_failure(
                table,
                "DQ-13",
                "WARNING",
                int(idx),
                "Year missing"
            )

        add_summary(
            "DQ-13",
            len(df)-len(invalid),
            len(invalid)
        )
# ==========================================================
# DQ-14 DATE FORMAT
# ==========================================================

def dq14_date(df):

    if "date" not in df.columns:
        return

    invalid = pd.to_datetime(
        df["date"],
        errors="coerce"
    ).isna()

    if invalid.sum()==0:

        print("✅ DQ-14 PASS")

        add_summary("DQ-14", len(df), 0)

    else:

        print("❌ DQ-14 FAIL")

        rows = df[invalid]

        for idx in rows.index:

            add_failure(
                "stock_prices.xlsx",
                "DQ-14",
                "WARNING",
                int(idx),
                "Invalid Date"
            )

        add_summary(
            "DQ-14",
            len(df)-len(rows),
            len(rows)
        )
# ==========================================================
# DQ-15 NUMERIC TYPE
# ==========================================================

def dq15_numeric(df, table):

    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:

        invalid = pd.to_numeric(
            df[col],
            errors="coerce"
        ).isna()

        if invalid.sum()>0:

            for idx in df[invalid].index:

                add_failure(
                    table,
                    "DQ-15",
                    "WARNING",
                    int(idx),
                    f"{col} not numeric"
                )

    print("✅ DQ-15 Completed")

    add_summary("DQ-15", len(df), 0)
# ==========================================================
# DQ-16 COVERAGE
# ==========================================================

def dq16_coverage(df, table):

    if "company_id" not in df.columns:
        return

    if "year" not in df.columns:
        return

    coverage = df.groupby(
        "company_id"
    )["year"].nunique()

    invalid = coverage[coverage<5]

    if invalid.empty:

        print("✅ DQ-16 PASS")

        add_summary(
            "DQ-16",
            len(coverage),
            0
        )

    else:

        print("❌ DQ-16 FAIL")

        for company in invalid.index:

            add_failure(
                table,
                "DQ-16",
                "WARNING",
                company,
                "Less than 5 years data"
            )

        add_summary(
            "DQ-16",
            len(coverage)-len(invalid),
            len(invalid)
        )                                    
# ==========================================================
# SAVE REPORTS
# ==========================================================

def save_reports():

    pd.DataFrame(validation_failures).to_csv(
        "output/validation_failures.csv",
        index=False
    )

    pd.DataFrame(validation_summary).to_csv(
        "output/validation_summary.csv",
        index=False
    )

    with open(
        "output/validation_log.txt",
        "w",
        encoding="utf-8"
    ) as log:

        log.write("N100 Financial Intelligence Platform\n")
        log.write("="*50+"\n\n")

        log.write("Validation Summary\n\n")

        for item in validation_summary:

            log.write(
                f"{item['rule']} : Passed={item['passed']} Failed={item['failed']}\n"
            )

        log.write("\nCompleted Successfully.\n")

# ==========================================================
# MAIN
# ==========================================================

def main():

    print("="*60)
    print("N100 Financial Intelligence Platform")
    print("Production Validator")
    print("="*60)

    companies = load_file("companies.xlsx")

    for file in FILES:

        print("\nChecking :",file)

        df = load_file(file)

        dq01_primary_key(df,file)
        dq02_composite_key(df,file)
        dq03_foreign_key(df,companies,file)

        if file == "balancesheet.xlsx":
         dq04_balance_sheet(df)

        if file == "profitandloss.xlsx":
            dq05_opm(df)
            dq06_positive_sales(df)
            dq08_tax(df)
            dq09_dividend(df)
            dq10_eps(df)

        if file == "cashflow.xlsx":
           dq07_net_cash(df)

        if file == "companies.xlsx":
          dq11_duplicate_company(df)
          dq12_url(df)

        dq13_missing_year(df, file)
        dq15_numeric(df, file)
        dq16_coverage(df, file)

        if file == "stock_prices.xlsx":
           dq14_date(df)
    save_reports()

    print("\nReports Generated Successfully")

    print("output/validation_failures.csv")

    print("output/validation_summary.csv")


if __name__=="__main__":

    main()

