"""
Sprint 3 - Day 17
Composite Quality Score Engine
"""

import sqlite3
import pandas as pd

DATABASE = "db/nifty100.db"


def calculate_quality_score(row):
    """
    Calculate weighted composite quality score.

    Score components:
    - ROE: 20%
    - ROCE: 15%
    - Revenue CAGR: 15%
    - PAT CAGR: 15%
    - EPS CAGR: 10%
    - Debt-to-Equity: 10%
    - Interest Coverage: 5%
    - FCF Conversion: 5%
    - Asset Turnover: 5%

    Final score is between 0 and 100.
    """

    score = 0
    total_weight = 0

    # ROE - higher is better
    if pd.notna(row.get("return_on_equity_pct")):
        value = max(0, min(row["return_on_equity_pct"], 30))
        score += (value / 30) * 20
        total_weight += 20

    # ROCE - higher is better
    if pd.notna(row.get("roce")):
        value = max(0, min(row["roce"], 30))
        score += (value / 30) * 15
        total_weight += 15

    # Revenue CAGR
    if pd.notna(row.get("revenue_cagr_5yr")):
        value = max(0, min(row["revenue_cagr_5yr"], 30))
        score += (value / 30) * 15
        total_weight += 15

    # PAT CAGR
    if pd.notna(row.get("pat_cagr_5yr")):
        value = max(0, min(row["pat_cagr_5yr"], 30))
        score += (value / 30) * 15
        total_weight += 15

    # EPS CAGR
    if pd.notna(row.get("eps_cagr_5yr")):
        value = max(0, min(row["eps_cagr_5yr"], 30))
        score += (value / 30) * 10
        total_weight += 10

    # Debt-to-Equity - lower is better
    if pd.notna(row.get("debt_to_equity")):
        value = max(0, min(row["debt_to_equity"], 2))
        score += ((2 - value) / 2) * 10
        total_weight += 10

    # Interest Coverage - higher is better
    if pd.notna(row.get("interest_coverage")):
        value = max(0, min(row["interest_coverage"], 10))
        score += (value / 10) * 5
        total_weight += 5

    # FCF Conversion - higher is better
    if pd.notna(row.get("fcf_conversion_pct")):
        value = max(0, min(row["fcf_conversion_pct"], 100))
        score += (value / 100) * 5
        total_weight += 5

    # Asset Turnover - higher is better
    if pd.notna(row.get("asset_turnover")):
        value = max(0, min(row["asset_turnover"], 5))
        score += (value / 5) * 5
        total_weight += 5

    if total_weight == 0:
        return None

    return round((score / total_weight) * 100, 2)


def populate_quality_scores():
    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    print("=" * 60)
    print("COMPOSITE QUALITY SCORE")
    print("=" * 60)

    print(f"Input rows: {len(df)}")

    # Calculate score for every row
    df["composite_quality_score"] = df.apply(
        calculate_quality_score,
        axis=1
    )

    # Update database
    cursor = conn.cursor()

    updated = 0

    for _, row in df.iterrows():

        cursor.execute(
            """
            UPDATE financial_ratios
            SET composite_quality_score = ?
            WHERE company_id = ?
            AND year = ?
            """,
            (
                row["composite_quality_score"],
                row["company_id"],
                row["year"]
            )
        )

        updated += cursor.rowcount

    conn.commit()

    print(f"Rows updated: {updated}")

    # Verification
    count = conn.execute(
        """
        SELECT COUNT(*)
        FROM financial_ratios
        WHERE composite_quality_score IS NOT NULL
        """
    ).fetchone()[0]

    print(f"Scores populated: {count}")

    # Display top companies
    top = pd.read_sql(
        """
        SELECT
            company_id,
            year,
            composite_quality_score
        FROM financial_ratios
        WHERE composite_quality_score IS NOT NULL
        ORDER BY composite_quality_score DESC
        LIMIT 10
        """,
        conn
    )

    print("\nTop 10 Companies:")
    print(top)

    conn.close()


if __name__ == "__main__":
    populate_quality_scores()