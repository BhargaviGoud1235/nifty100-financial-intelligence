"""
Sprint 2 - Day 12
Populate financial_ratios table
Includes 5-year CAGR calculations
"""

import sqlite3
import pandas as pd

DATABASE = "db/nifty100.db"


def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR and return (value, flag).
    """

    if pd.isna(start_value) or pd.isna(end_value):
        return None, "INSUFFICIENT"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0:

        cagr = (
            (end_value / start_value)
            ** (1 / years)
            - 1
        ) * 100

        return round(cagr, 2), None

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "INSUFFICIENT"


def get_5yr_cagr(group, column):
    """
    Calculate 5-year CAGR using historical records.

    Uses the oldest available value and the value
    approximately 5 years later.
    """

    group = group.copy()

    # Remove TTM for CAGR calculations
    group = group[
        group["year"].astype(str).str.upper() != "TTM"
    ]

    if group.empty:
        return None

    # Extract year number from strings such as:
    # Mar 2019
    # Dec 2020

    group["year_num"] = (
        group["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    group["year_num"] = pd.to_numeric(
        group["year_num"],
        errors="coerce"
    )

    group = group.dropna(
        subset=["year_num"]
    )

    group = group.sort_values(
        "year_num"
    )

    if len(group) < 6:
        return None

    latest = group.iloc[-1]

    latest_year = latest["year_num"]

    # Find record closest to 5 years before latest
    target_year = latest_year - 5

    group["distance"] = abs(
        group["year_num"] - target_year
    )

    start_row = group.sort_values(
        "distance"
    ).iloc[0]

    start_value = start_row[column]

    end_value = latest[column]

    cagr, flag = calculate_cagr(
        start_value,
        end_value,
        5
    )

    return cagr


def populate_ratios():

    conn = sqlite3.connect(
        DATABASE
    )

    # ---------------------------------------------
    # Read source tables
    # ---------------------------------------------

    pnl = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    bs = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cf = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    # ---------------------------------------------
    # Clean IDs
    # ---------------------------------------------

    for df in [pnl, bs, cf]:

        df["company_id"] = (
            df["company_id"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    # ---------------------------------------------
    # Remove duplicate company-year rows
    # ---------------------------------------------

    pnl = pnl.drop_duplicates(
        subset=[
            "company_id",
            "year"
        ],
        keep="first"
    )

    bs = bs.drop_duplicates(
        subset=[
            "company_id",
            "year"
        ],
        keep="first"
    )

    cf = cf.drop_duplicates(
        subset=[
            "company_id",
            "year"
        ],
        keep="first"
    )

    # ---------------------------------------------
    # Merge data
    # ---------------------------------------------

    data = pnl.merge(
        bs,
        on=[
            "company_id",
            "year"
        ],
        how="left"
    )

    data = data.merge(
        cf,
        on=[
            "company_id",
            "year"
        ],
        how="left"
    )

    # ---------------------------------------------
    # Calculate CAGR lookup
    # ---------------------------------------------

    cagr_lookup = {}

    for company_id, group in pnl.groupby(
        "company_id"
    ):

        revenue_cagr = get_5yr_cagr(
            group,
            "sales"
        )

        pat_cagr = get_5yr_cagr(
            group,
            "net_profit"
        )

        eps_cagr = get_5yr_cagr(
            group,
            "eps"
        )

        cagr_lookup[company_id] = {

            "revenue_cagr_5yr":
                revenue_cagr,

            "pat_cagr_5yr":
                pat_cagr,

            "eps_cagr_5yr":
                eps_cagr
        }

    # ---------------------------------------------
    # Calculate ratios
    # ---------------------------------------------

    rows = []

    for _, row in data.iterrows():

        company_id = row["company_id"]

        sales = row["sales"] or 0
        net_profit = row["net_profit"] or 0
        operating_profit = (
            row["operating_profit"] or 0
        )

        other_income = (
            row["other_income"] or 0
        )

        interest = (
            row["interest"] or 0
        )

        equity = (
            row["equity_capital"] or 0
        )

        reserves = (
            row["reserves"] or 0
        )

        borrowings = (
            row["borrowings"] or 0
        )

        investments = (
            row["investments"] or 0
        )

        total_assets = (
            row["total_assets"] or 0
        )

        cfo = (
            row["operating_activity"] or 0
        )

        cfi = (
            row["investing_activity"] or 0
        )

        capital = (
            equity + reserves
        )

        # Net Profit Margin
        if sales != 0:
            npm = (
                net_profit / sales
            ) * 100
        else:
            npm = None

        # OPM
        if sales != 0:
            opm = (
                operating_profit / sales
            ) * 100
        else:
            opm = None

        # ROE
        if capital > 0:
            roe = (
                net_profit / capital
            ) * 100
        else:
            roe = None

        # ROCE
        employed_capital = (
            capital + borrowings
        )

        if employed_capital > 0:
            roce = (
                operating_profit
                / employed_capital
            ) * 100
        else:
            roce = None

        # Debt-to-Equity
        if borrowings == 0:
            de = 0

        elif capital > 0:
            de = (
                borrowings / capital
            )

        else:
            de = None

        # Interest Coverage
        if interest == 0:

            icr = None
            icr_label = "Debt Free"

        else:

            icr = (
                operating_profit
                + other_income
            ) / interest

            icr_label = ""

        # Asset Turnover
        if total_assets != 0:

            asset_turnover = (
                sales / total_assets
            )

        else:

            asset_turnover = None

        # FCF
        fcf = (
            cfo + cfi
        )

        # Net Debt
        net_debt = (
            borrowings
            - investments
        )

        # FCF Conversion
        if operating_profit != 0:

            fcf_conversion = (
                fcf / operating_profit
            ) * 100

        else:

            fcf_conversion = None

        # CAGR values
        cagr_values = cagr_lookup.get(
            company_id,
            {}
        )

        rows.append({

            "company_id":
                company_id,

            "year":
                row["year"],

            "pe":
                None,

            "pb":
                None,

            "roce":
                roce,

            "roe":
                roe,

            "net_profit_margin_pct":
                npm,

            "operating_profit_margin_pct":
                opm,

            "return_on_equity_pct":
                roe,

            "debt_to_equity":
                de,

            "interest_coverage":
                icr,

            "icr_label":
                icr_label,

            "asset_turnover":
                asset_turnover,

            "free_cash_flow_cr":
                fcf,

            "capex_cr":
                abs(cfi),

            "earnings_per_share":
                row["eps"],

            "book_value_per_share":
                None,

            "dividend_payout_ratio_pct":
                row["dividend_payout"],

            "total_debt_cr":
                borrowings,

            "cash_from_operations_cr":
                cfo,

            "revenue_cagr_5yr":
                cagr_values.get(
                    "revenue_cagr_5yr"
                ),

            "pat_cagr_5yr":
                cagr_values.get(
                    "pat_cagr_5yr"
                ),

            "eps_cagr_5yr":
                cagr_values.get(
                    "eps_cagr_5yr"
                ),

            "fcf_conversion_pct":
                fcf_conversion,

            "net_debt_cr":
                net_debt,

            "composite_quality_score":
                None
        })

    ratios = pd.DataFrame(
        rows
    )

    # ---------------------------------------------
    # Remove duplicate keys
    # ---------------------------------------------

    ratios = ratios.drop_duplicates(
        subset=[
            "company_id",
            "year"
        ],
        keep="first"
    )

    # ---------------------------------------------
    # Clear old data
    # ---------------------------------------------

    conn.execute(
        "DELETE FROM financial_ratios"
    )

    conn.commit()

    # ---------------------------------------------
    # Insert new data
    # ---------------------------------------------

    ratios.to_sql(
        "financial_ratios",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()

    conn.close()

    print(
        f"Inserted {len(ratios)} rows "
        "into financial_ratios"
    )


if __name__ == "__main__":
    populate_ratios()