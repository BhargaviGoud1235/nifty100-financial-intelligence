
import sqlite3
from pathlib import Path

import pandas as pd


DB_PATH = Path("db/nifty100.db")
PEER_GROUPS_PATH = Path("data/raw/peer_groups.xlsx")


METRICS = {
    "roe": False,
    "roce": False,
    "net_profit_margin_pct": False,
    "debt_to_equity": True,  # Lower is better
    "free_cash_flow_cr": False,
    "pat_cagr_5yr": False,
    "revenue_cagr_5yr": False,
    "eps_cagr_5yr": False,
    "interest_coverage": False,
    "asset_turnover": False,
}


def load_peer_groups():
    """Load company-to-peer-group mapping."""

    df = pd.read_excel(PEER_GROUPS_PATH)

    df.columns = [str(c).strip().lower() for c in df.columns]

    # Support common column names
    rename_map = {}

    for col in df.columns:
        if col in ["company_id", "id", "symbol"]:
            rename_map[col] = "company_id"
        elif col in ["peer_group_name", "peer_group", "group"]:
            rename_map[col] = "peer_group_name"

    df = df.rename(columns=rename_map)

    required = ["company_id", "peer_group_name"]

    missing = [c for c in required if c not in df.columns]

    if missing:
        raise ValueError(
            f"Missing columns in peer_groups.xlsx: {missing}"
        )

    df = df[required].dropna()

    df["company_id"] = df["company_id"].astype(str).str.strip()
    df["peer_group_name"] = (
        df["peer_group_name"]
        .astype(str)
        .str.strip()
    )

    return df


def create_peer_percentiles_table(conn):
    """Create peer_percentiles table if it does not exist."""

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS peer_percentiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id TEXT NOT NULL,
            peer_group_name TEXT NOT NULL,
            metric TEXT NOT NULL,
            value REAL,
            percentile_rank REAL,
            year TEXT,
            UNIQUE(company_id, peer_group_name, metric, year)
        )
        """
    )

    conn.commit()


def calculate_percentile(series, value, inverse=False):
    """
    Calculate percentile rank.

    Higher value = higher percentile by default.
    For D/E, inverse=True so lower D/E = higher percentile.
    """

    valid = pd.to_numeric(series, errors="coerce").dropna()

    if pd.isna(value) or len(valid) == 0:
        return None

    # Percent rank:
    # percentage of values below or equal to current value
    rank = (valid <= value).sum() - 1

    if len(valid) <= 1:
        percentile = 1.0
    else:
        percentile = rank / (len(valid) - 1)

    if inverse:
        percentile = 1.0 - percentile

    return round(float(percentile), 4)


def calculate_peer_percentiles():
    """Calculate percentile rankings for all peer groups."""

    if not PEER_GROUPS_PATH.exists():
        raise FileNotFoundError(
            f"Peer groups file not found: {PEER_GROUPS_PATH}"
        )

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    peer_groups = load_peer_groups()

    conn = sqlite3.connect(DB_PATH)

    create_peer_percentiles_table(conn)

    ratios = pd.read_sql_query(
        "SELECT * FROM financial_ratios",
        conn
    )

    results = []

    for _, peer in peer_groups.iterrows():

        company_id = peer["company_id"]
        peer_group_name = peer["peer_group_name"]

        company_rows = ratios[
            ratios["company_id"].astype(str).str.strip()
            == company_id
        ]

        if company_rows.empty:
            continue

        # Use latest/TTM data where available
        if "year" in company_rows.columns:
            ttm_rows = company_rows[
                company_rows["year"].astype(str).str.upper() == "TTM"
            ]

            if not ttm_rows.empty:
                company_rows = ttm_rows

        row = company_rows.iloc[0]

        # Get all companies belonging to this peer group
        group_companies = peer_groups[
            peer_groups["peer_group_name"] == peer_group_name
        ]["company_id"].tolist()

        group_data = ratios[
            ratios["company_id"].astype(str).str.strip()
            .isin(group_companies)
        ].copy()

        if "year" in group_data.columns:
            ttm_data = group_data[
                group_data["year"].astype(str).str.upper() == "TTM"
            ]

            if not ttm_data.empty:
                group_data = ttm_data

        for metric, inverse in METRICS.items():

            if metric not in ratios.columns:
                continue

            value = row.get(metric)

            group_values = pd.to_numeric(
                group_data[metric],
                errors="coerce"
            )

            percentile = calculate_percentile(
                group_values,
                value,
                inverse=inverse
            )

            year = row.get("year", "TTM")

            results.append(
                {
                    "company_id": company_id,
                    "peer_group_name": peer_group_name,
                    "metric": metric,
                    "value": value,
                    "percentile_rank": percentile,
                    "year": year,
                }
            )

    result_df = pd.DataFrame(results)

    if result_df.empty:
        print("No peer percentile records generated.")
        conn.close()
        return

    # Replace existing results to keep table current
    conn.execute("DELETE FROM peer_percentiles")

    result_df.to_sql(
        "peer_percentiles",
        conn,
        if_exists="append",
        index=False
    )

    conn.commit()

    print("=" * 60)
    print("PEER PERCENTILE RANKINGS")
    print("=" * 60)

    print(f"Peer groups: {peer_groups['peer_group_name'].nunique()}")
    print(f"Companies mapped: {len(peer_groups)}")
    print(f"Metrics ranked: {len(METRICS)}")
    print(f"Percentile records: {len(result_df)}")

    print()
    print("Sample Results:")
    print(
        result_df.head(20).to_string(index=False)
    )

    print()
    print("Peer Groups:")
    print(
        peer_groups["peer_group_name"]
        .value_counts()
        .to_string()
    )

    print()
    print("PEER PERCENTILE CALCULATION COMPLETE")

    conn.close()


if __name__ == "__main__":
    calculate_peer_percentiles()

