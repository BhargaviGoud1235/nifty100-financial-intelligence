"""
Sprint 1 - Day 05
Load Excel files into SQLite
"""

import sqlite3
from pathlib import Path

import pandas as pd

from src.etl.loader import load_excel

DATABASE = "db/nifty100.db"
DATA_FOLDER = Path("data/raw")


TABLES = {
    "companies.xlsx": "companies",
    "analysis.xlsx": "analysis",
    "balancesheet.xlsx": "balancesheet",
    "cashflow.xlsx": "cashflow",
    "documents.xlsx": "documents",
    "profitandloss.xlsx": "profitandloss",
    "prosandcons.xlsx": "prosandcons",
}


def load_table(conn, filename, table):

    print(f"Loading {filename} -> {table}")

    df = load_excel(DATA_FOLDER / filename)

    # Only for child tables
    if table != "companies" and "company_id" in df.columns:

        companies = pd.read_sql(
            "SELECT id FROM companies",
            conn
        )

        valid_ids = set(companies["id"])

        invalid = df[~df["company_id"].isin(valid_ids)]

        if not invalid.empty:
            print(f"Skipped {len(invalid)} invalid rows in {table}")

            invalid.to_csv(
                f"output/{table}_invalid_fk.csv",
                index=False
            )

        df = df[df["company_id"].isin(valid_ids)]

    rows_loaded = len(df)

    try:
        df.to_sql(
            table,
            conn,
            if_exists="append",
            index=False
        )
        print(f"✅ Loaded {rows_loaded} rows into {table}")

    except Exception as e:
         print(f"\n❌ ERROR loading table: {table}")
         print(e)
         raise

    return rows_loaded


def main():

    conn = sqlite3.connect(DATABASE)

    conn.execute("PRAGMA foreign_keys = ON")

    audit = []

    for filename, table in TABLES.items():

        rows = load_table(conn, filename, table)

        audit.append({
            "table": table,
            "rows_loaded": rows
        })

    conn.commit()

    pd.DataFrame(audit).to_csv(
        "output/load_audit.csv",
        index=False
    )

    conn.close()

    print("\nLoad completed successfully.")
    print("Audit file saved to output/load_audit.csv")


if __name__ == "__main__":
    main()