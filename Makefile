load:
python src/etl/loader.py

test:
pytest tests/

report:
python src/report.py

dashboard:
python src/dashboard.py

clean:
rm -rf **pycache**

# Sprint 1 Completion Report

## Completed Modules

- Environment Setup
- Excel Loader
- Data Normaliser
- SQLite Database
- Data Validation
- Load Audit
- Manual Data Review
- Foreign Key Validation

## Database

- SQLite
- 12 Excel Source Files
- 12 Tables Loaded

## Validation

- 16 Data Quality Rules
- Validation Reports
- Load Audit
- Manual Review

## Status

Sprint 1 Successfully Completed