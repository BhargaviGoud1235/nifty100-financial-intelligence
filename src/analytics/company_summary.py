"""
Sprint 3 - Day 18
Company Financial Summary
"""

import sqlite3
import pandas as pd

DATABASE = "db/nifty100.db"


def load_company_summary(company_id):
    """
    Load the latest available financial data for a company.
    """

    conn = sqlite3.connect(DATABASE)

    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY
            CASE
                WHEN UPPER(year) = 'TTM' THEN 0
                ELSE 1
            END,
            year DESC
        LIMIT 1
        """,
        conn,
        params=(company_id,)
    )

    conn.close()

    if ratios.empty:
        return None

    return ratios.iloc[0].to_dict()


def print_company_summary(company_id):
    """
    Print a readable financial summary.
    """

    summary = load_company_summary(company_id)

    if summary is None:
        print(f"No financial data found for {company_id}")
        return

    print("=" * 60)
    print(f"FINANCIAL SUMMARY - {company_id}")
    print("=" * 60)

    print(f"Year: {summary.get('year')}")
    print(f"ROE: {summary.get('roe')}")
    print(f"ROCE: {summary.get('roce')}")
    print(f"P/E: {summary.get('pe')}")
    print(f"P/B: {summary.get('pb')}")
    print(
        f"Net Profit Margin: "
        f"{summary.get('net_profit_margin_pct')}"
    )
    print(
        f"Operating Profit Margin: "
        f"{summary.get('operating_profit_margin_pct')}"
    )
    print(
        f"Debt-to-Equity: "
        f"{summary.get('debt_to_equity')}"
    )
    print(
        f"Interest Coverage: "
        f"{summary.get('interest_coverage')}"
    )
    print(
        f"Revenue CAGR (5Y): "
        f"{summary.get('revenue_cagr_5yr')}"
    )
    print(
        f"PAT CAGR (5Y): "
        f"{summary.get('pat_cagr_5yr')}"
    )
    print(
        f"EPS CAGR (5Y): "
        f"{summary.get('eps_cagr_5yr')}"
    )
    print(
        f"Free Cash Flow: "
        f"{summary.get('free_cash_flow_cr')}"
    )
    print(
        f"Composite Quality Score: "
        f"{summary.get('composite_quality_score')}"
    )


def rank_companies(companies):
    """
    Rank companies by composite quality score.
    """

    results = []

    for company in companies:

        summary = load_company_summary(company)

        if summary is not None:
            results.append({
                "company_id": company,
                "year": summary.get("year"),
                "composite_quality_score": summary.get(
                    "composite_quality_score"
                ),
                "revenue_cagr_5yr": summary.get(
                    "revenue_cagr_5yr"
                ),
                "pat_cagr_5yr": summary.get(
                    "pat_cagr_5yr"
                ),
                "eps_cagr_5yr": summary.get(
                    "eps_cagr_5yr"
                ),
            })

    df = pd.DataFrame(results)

    if df.empty:
        print("No company data found.")
        return df

    df = df.sort_values(
        "composite_quality_score",
        ascending=False
    )

    return df.reset_index(drop=True)
if __name__ == "__main__":

    companies = [
        "TCS",
        "INFY",
        "RELIANCE",
        "HDFCBANK",
        "NESTLEIND"
    ]

    print("=" * 60)
    print("COMPANY QUALITY RANKING")
    print("=" * 60)

    ranking = rank_companies(companies)

    print(ranking.to_string(index=False))

    output_file = "output/company_quality_ranking.csv"

    ranking.to_csv(
        output_file,
        index=False
    )

    print()
    print("=" * 60)
    print("EXPORT COMPLETE")
    print("=" * 60)
    print(f"Rows exported: {len(ranking)}")
    print(f"Output file: {output_file}")