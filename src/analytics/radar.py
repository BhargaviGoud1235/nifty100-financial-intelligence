import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "db/nifty100.db"
OUTPUT_DIR = Path("reports/radar_charts")

METRICS = [
    "roe",
    "roce",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "pat_cagr_5yr",
    "revenue_cagr_5yr",
    "composite_quality_score",
]

METRIC_LABELS = [
    "ROE",
    "ROCE",
    "NPM",
    "D/E",
    "FCF",
    "PAT CAGR",
    "Revenue CAGR",
    "Quality Score",
]
def load_data():
    conn = sqlite3.connect(DB_PATH)

    query = """
        SELECT
            company_id,
            year,
            roe,
            roce,
            net_profit_margin_pct,
            debt_to_equity,
            free_cash_flow_cr,
            pat_cagr_5yr,
            revenue_cagr_5yr,
            composite_quality_score
        FROM financial_ratios
        WHERE year = 'TTM'
    """

    ratios = pd.read_sql_query(query, conn)

    peer_query = """
        SELECT company_id, peer_group_name
        FROM peer_groups
    """

    try:
        peers = pd.read_sql_query(peer_query, conn)
    except Exception:
        peers = pd.DataFrame(
            columns=["company_id", "peer_group_name"]
        )

    conn.close()

    return ratios, peers


def normalize_series(series):
    series = pd.to_numeric(
        series,
        errors="coerce"
    )

    if series.notna().sum() == 0:
        return pd.Series(
            50.0,
            index=series.index
        )

    median_value = series.median()

    series = series.fillna(
        median_value
    )

    min_value = series.min()
    max_value = series.max()

    if min_value == max_value:
        return pd.Series(
            50.0,
            index=series.index
        )

    return (
        (series - min_value)
        / (max_value - min_value)
        * 100
    ).clip(0, 100)


def prepare_data(ratios):
    result = ratios.copy()

    for metric in METRICS:
        result[metric] = normalize_series(
            result[metric]
        )

    return result
def create_radar(
    company_id,
    company_row,
    peer_rows,
    peer_group_name
):
    values = company_row[
        METRICS
    ].astype(float).tolist()

    if peer_rows.empty:
        peer_average = values.copy()
        title_suffix = "Nifty 100 Average Reference"
    else:
        peer_average = (
            peer_rows[METRICS]
            .mean()
            .astype(float)
            .tolist()
        )
        title_suffix = (
            f"{peer_group_name} Average"
        )

    angles = np.linspace(
        0,
        2 * np.pi,
        len(METRICS),
        endpoint=False
    ).tolist()

    values += values[:1]
    peer_average += peer_average[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(
        figsize=(9, 9),
        subplot_kw={"polar": True}
    )

    ax.plot(
        angles,
        values,
        linewidth=2,
        label=company_id
    )

    ax.fill(
        angles,
        values,
        alpha=0.20
    )

    ax.plot(
        angles,
        peer_average,
        linestyle="--",
        linewidth=2,
        label=title_suffix
    )

    ax.set_xticks(
        angles[:-1]
    )

    ax.set_xticklabels(
        METRIC_LABELS,
        fontsize=10
    )

    ax.set_ylim(
        0,
        100
    )

    ax.set_yticks(
        [20, 40, 60, 80, 100]
    )

    ax.set_yticklabels(
        ["20", "40", "60", "80", "100"],
        fontsize=8
    )

    ax.set_title(
        f"{company_id} - Peer Comparison Radar",
        fontsize=14,
        pad=25
    )

    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 1.10)
    )

    output_file = (
        OUTPUT_DIR
        / f"{company_id}_radar.png"
    )

    plt.tight_layout()

    plt.savefig(
        output_file,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    return output_file
def main():
    print("=" * 60)
    print("PEER RADAR CHART GENERATION")
    print("=" * 60)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    ratios, peers = load_data()

    if ratios.empty:
        print("No financial ratio data found.")
        return

    data = prepare_data(ratios)

    peer_map = dict(
        zip(
            peers["company_id"],
            peers["peer_group_name"]
        )
    )

    generated = 0

    for _, company_row in data.iterrows():

        company_id = company_row["company_id"]

        peer_group = peer_map.get(
            company_id
        )

        if peer_group:

            peer_company_ids = peers.loc[
                peers["peer_group_name"]
                == peer_group,
                "company_id"
            ].tolist()

            peer_rows = data[
                data["company_id"].isin(
                    peer_company_ids
                )
            ]

            peer_rows = peer_rows[
                peer_rows["company_id"]
                != company_id
            ]

            if peer_rows.empty:
                peer_rows = data[
                    data["company_id"].isin(
                        peer_company_ids
                    )
                ]

        else:
            peer_rows = pd.DataFrame(
                columns=METRICS
            )

        output_file = create_radar(
            company_id,
            company_row,
            peer_rows,
            peer_group
            if peer_group
            else "Nifty 100"
        )

        generated += 1

        print(
            f"Generated: {output_file}"
        )

    print()
    print("=" * 60)
    print("RADAR CHART GENERATION COMPLETE")
    print("=" * 60)
    print(
        f"Charts generated: {generated}"
    )
    print(
        f"Output directory: {OUTPUT_DIR}"
    )


if __name__ == "__main__":
    main()