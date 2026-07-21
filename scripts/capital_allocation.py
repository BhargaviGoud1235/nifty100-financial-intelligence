"""
Sprint 2 - Day 11
Generate capital allocation patterns for all company-years.
"""

import sqlite3
import pandas as pd

from src.analytics.cashflow_kpis import (
    capital_allocation_pattern,
    get_cash_flow_sign,
    cfo_quality_score
)

DATABASE = "db/nifty100.db"
OUTPUT_FILE = "output/capital_allocation.csv"


def generate_capital_allocation():

    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            operating_activity,
            investing_activity,
            financing_activity
        FROM cashflow
        """,
        conn
    )

    conn.close()

    results = []

    for _, row in df.iterrows():

        cfo = row["operating_activity"]
        cfi = row["investing_activity"]
        cff = row["financing_activity"]

        cfo_sign = get_cash_flow_sign(cfo)
        cfi_sign = get_cash_flow_sign(cfi)
        cff_sign = get_cash_flow_sign(cff)

        pattern_label = capital_allocation_pattern(
            cfo,
            cfi,
            cff
        )

        results.append({
            "company_id": row["company_id"],
            "year": row["year"],
            "cfo_sign": cfo_sign,
            "cfi_sign": cfi_sign,
            "cff_sign": cff_sign,
            "pattern_label": pattern_label
        })

    output = pd.DataFrame(results)

    output.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("=" * 60)
    print("CAPITAL ALLOCATION REPORT")
    print("=" * 60)
    print(f"Rows generated: {len(output)}")
    print(f"Output file: {OUTPUT_FILE}")
    print()
    print(output.head(10))

    print()
    print("Pattern Summary:")
    print(output["pattern_label"].value_counts())


if __name__ == "__main__":
    generate_capital_allocation()