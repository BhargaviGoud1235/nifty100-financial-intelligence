"""
Sprint 3 - Day 19
Company Comparison Report
"""

import sqlite3
import pandas as pd


DATABASE = "db/nifty100.db"


def load_company_data(companies):
    """
    Load latest TTM financial data for selected companies.
    """

    conn = sqlite3.connect(DATABASE)

    placeholders = ",".join(["?"] * len(companies))

    query = f"""
        SELECT
            company_id,
            year,
            pe,
            pb,
            roe,
            roce,
            net_profit_margin_pct,
            operating_profit_margin_pct,
            debt_to_equity,
            interest_coverage,
            revenue_cagr_5yr,
            pat_cagr_5yr,
            eps_cagr_5yr,
            free_cash_flow_cr,
            composite_quality_score
        FROM financial_ratios
        WHERE company_id IN ({placeholders})
        AND year = 'TTM'
    """

    df = pd.read_sql(
        query,
        conn,
        params=companies
    )

    conn.close()

    return df


def compare_companies(companies):
    """
    Compare selected companies using key financial metrics.
    """

    df = load_company_data(companies)

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
    print("COMPANY COMPARISON REPORT")
    print("=" * 60)

    comparison = compare_companies(companies)

    print()
    print(comparison.to_string(index=False))

    output_file = "output/company_comparison.csv"

    comparison.to_csv(
        output_file,
        index=False
    )

    print()
    print("=" * 60)
    print("COMPARISON COMPLETE")
    print("=" * 60)
    print(f"Companies compared: {len(comparison)}")
    print(f"Output file: {output_file}")