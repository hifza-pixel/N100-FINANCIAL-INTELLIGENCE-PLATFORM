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
