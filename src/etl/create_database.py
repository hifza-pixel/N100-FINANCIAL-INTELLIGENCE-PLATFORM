"""
create_database.py

Creates SQLite database from schema.sql
"""

import sqlite3

DATABASE = "db/nifty100.db"
SCHEMA = "db/schema.sql"


def create_database():

    conn = sqlite3.connect(DATABASE)

    conn.execute("PRAGMA foreign_keys = ON;")

    with open(SCHEMA, "r", encoding="utf-8") as file:
        sql = file.read()

    conn.executescript(sql)

    conn.commit()

    conn.close()

    print("=" * 50)
    print("N100 Financial Intelligence Platform")
    print("=" * 50)
    print("Database Created Successfully.")
    print("Database :", DATABASE)


if __name__ == "__main__":
    create_database()