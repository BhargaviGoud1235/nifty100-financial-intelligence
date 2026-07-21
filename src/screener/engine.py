"""
Sprint 3 - Day 15
Screener Filter Engine Core
"""

import sqlite3
from pathlib import Path

import pandas as pd
import yaml


DATABASE = "db/nifty100.db"
CONFIG_FILE = "config/screener_config.yaml"


def load_config():
    """Load screener configuration from YAML."""

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_financial_ratios():
    """Load latest financial ratio record for each company."""

    conn = sqlite3.connect(DATABASE)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    # Keep only one latest record per company
    # This prevents multiple years of the same company
    # from appearing in the screener.
    if "company_id" in df.columns and "year" in df.columns:

        # Prefer TTM if available
        ttm = df[df["year"].astype(str).str.upper() == "TTM"]

        if not ttm.empty:
            df = ttm

        else:
            # Otherwise take the last available year
            df = (
                df.sort_values("year")
                .groupby("company_id", as_index=False)
                .tail(1)
            )

    return df.reset_index(drop=True)
def apply_filters(df, filters):
    """
    Apply threshold filters to financial ratios.

    Supported filters:
    - ROE minimum
    - Debt-to-Equity maximum
    - FCF minimum
    - Revenue CAGR 5yr minimum
    - PAT CAGR 5yr minimum
    - OPM minimum
    - P/E maximum
    - P/B maximum
    - Dividend Yield minimum
    - ICR minimum
    - Market Cap minimum
    - Net Profit minimum
    - EPS CAGR minimum
    - Asset Turnover minimum
    - Sales minimum
    """

    result = df.copy()

    # ROE
    if "roe_min" in filters and "roe" in result.columns:
        result = result[result["roe"] >= filters["roe_min"]]

    # Debt-to-Equity
    if "debt_to_equity_max" in filters and "debt_to_equity" in result.columns:
        result = result[
            result["debt_to_equity"] <= filters["debt_to_equity_max"]
        ]

    # Free Cash Flow
    if "fcf_min" in filters and "free_cash_flow_cr" in result.columns:
        result = result[
            result["free_cash_flow_cr"] >= filters["fcf_min"]
        ]

    # Revenue CAGR
    if "revenue_cagr_5yr_min" in filters and "revenue_cagr_5yr" in result.columns:
        result = result[
            result["revenue_cagr_5yr"] >= filters["revenue_cagr_5yr_min"]
        ]

    # PAT CAGR
    if "pat_cagr_5yr_min" in filters and "pat_cagr_5yr" in result.columns:
        result = result[
            result["pat_cagr_5yr"] >= filters["pat_cagr_5yr_min"]
        ]

    # Operating Profit Margin
    if "opm_min" in filters and "operating_profit_margin_pct" in result.columns:
        result = result[
            result["operating_profit_margin_pct"] >= filters["opm_min"]
        ]

    # P/E
    if "pe_max" in filters and "pe" in result.columns:
        result = result[
            result["pe"] <= filters["pe_max"]
        ]

    # P/B
    if "pb_max" in filters and "pb" in result.columns:
        result = result[
            result["pb"] <= filters["pb_max"]
        ]

    # Dividend Yield
    if "dividend_yield_min" in filters and "dividend_yield" in result.columns:
        result = result[
            result["dividend_yield"] >= filters["dividend_yield_min"]
        ]

    # Interest Coverage Ratio
    if "icr_min" in filters and "interest_coverage" in result.columns:
        result = result[
            result["interest_coverage"] >= filters["icr_min"]
        ]

    # Market Cap
    if "market_cap_min" in filters and "market_cap" in result.columns:
        result = result[
            result["market_cap"] >= filters["market_cap_min"]
        ]

    # Net Profit
    if "net_profit_min" in filters and "net_profit" in result.columns:
        result = result[
            result["net_profit"] >= filters["net_profit_min"]
        ]

    # EPS CAGR
    if "eps_cagr_min" in filters and "eps_cagr_5yr" in result.columns:
        result = result[
            result["eps_cagr_5yr"] >= filters["eps_cagr_min"]
        ]

    # Asset Turnover
    if "asset_turnover_min" in filters and "asset_turnover" in result.columns:
        result = result[
            result["asset_turnover"] >= filters["asset_turnover_min"]
        ]

    # Sales
    if "sales_min" in filters and "sales" in result.columns:
        result = result[
            result["sales"] >= filters["sales_min"]
        ]

    return result


def calculate_composite_quality_score(df):
    """
    Calculate a basic composite quality score.

    This is a temporary Day 15 implementation.
    Full weighted scoring will be completed on Day 17.
    """

    result = df.copy()

    score_columns = []

    for column in [
        "roe",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "asset_turnover"
    ]:
        if column in result.columns:
            score_columns.append(column)

    if score_columns:
        result["composite_quality_score"] = (
            result[score_columns]
            .rank(pct=True)
            .mean(axis=1)
            * 100
        )
    else:
        result["composite_quality_score"] = 0

    return result

def run_screener(filters):
    """
    Run screener:
    1. Load latest financial ratios
    2. Apply filters
    3. Calculate composite quality score
    4. Sort by composite score descending
    """

    # Load latest data
    df = load_financial_ratios()

    # Apply configured filters
    filtered = apply_filters(df, filters)

    # Calculate composite score
    scored = calculate_composite_quality_score(filtered)

    # Sort highest quality companies first
    scored = scored.sort_values(
        "composite_quality_score",
        ascending=False
    ).reset_index(drop=True)

    return scored


def run_preset(preset_name):
    """
    Run one of the 6 predefined screener presets.
    """

    config = load_config()

    if preset_name not in config:
        raise ValueError(
            f"Unknown preset: {preset_name}"
        )

    filters = config[preset_name]

    result = run_screener(filters)

    return result


def run_all_presets():
    """
    Run all 6 screener presets.
    """

    config = load_config()

    results = {}

    for preset_name in config.keys():

        print("\n" + "=" * 60)
        print(preset_name.upper())
        print("=" * 60)

        try:
            result = run_preset(preset_name)

            results[preset_name] = result

            print(
                f"Companies found: "
                f"{result['company_id'].nunique()}"
            )

            if not result.empty:

                print(
                    result[
                        [
                            "company_id",
                            "year",
                            "composite_quality_score"
                        ]
                    ].head(10)
                )

        except Exception as error:

            print(
                f"Error running {preset_name}: "
                f"{error}"
            )

    return results


if __name__ == "__main__":

    print("=" * 60)
    print("SPRINT 3 - DAY 16")
    print("6 PRESET SCREENERS")
    print("=" * 60)

    results = run_all_presets()

