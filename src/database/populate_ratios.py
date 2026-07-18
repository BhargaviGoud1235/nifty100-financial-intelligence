"""
Sprint 2 - Day 12
Populate financial_ratios table
"""

import sqlite3
import pandas as pd

DATABASE = "db/nifty100.db"


def populate_ratios():
    conn = sqlite3.connect(DATABASE)

    # Clear existing rows
    conn.execute("DELETE FROM financial_ratios")
    conn.commit()

    # Read source tables
    pnl = pd.read_sql("SELECT * FROM profitandloss", conn)
    companies = pd.read_sql("SELECT * FROM companies", conn)

    # Clean IDs
    pnl["company_id"] = (
        pnl["company_id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    companies["id"] = (
        companies["id"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Company lookup dictionary
    company_lookup = companies.set_index("id").to_dict("index")

    rows = []

    for _, row in pnl.iterrows():

        company_id = row["company_id"]

        if company_id not in company_lookup:
            continue

        company = company_lookup[company_id]

        rows.append({
            "company_id": company_id,
            "year": row["year"],
            "pe": None,
            "pb": None,
            "roce": company["roce_percentage"],
            "roe": company["roe_percentage"]
        })

    # Convert to DataFrame
    ratios = pd.DataFrame(rows)

    # Remove duplicate (company_id, year) rows
    ratios = ratios.drop_duplicates(
        subset=["company_id", "year"],
        keep="first"
    )

    # Insert into SQLite
    if not ratios.empty:
        ratios.to_sql(
            "financial_ratios",
            conn,
            if_exists="append",
            index=False
        )

    conn.commit()
    conn.close()

    print(f"Inserted {len(ratios)} rows into financial_ratios")


if __name__ == "__main__":
    populate_ratios()