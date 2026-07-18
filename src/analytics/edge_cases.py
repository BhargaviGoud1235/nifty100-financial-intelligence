"""
Sprint 2 - Day 13
ROE / ROCE Edge Case Logger
"""

import sqlite3
from pathlib import Path

DATABASE = "db/nifty100.db"
LOG_FILE = "output/ratio_edge_cases.log"


def log_edge_cases():

    Path("output").mkdir(exist_ok=True)

    conn = sqlite3.connect(DATABASE)

    companies = conn.execute("""
        SELECT
            id,
            company_name,
            roce_percentage,
            roe_percentage
        FROM companies
    """).fetchall()

    ratios = conn.execute("""
        SELECT
            company_id,
            return_on_capital_employed_pct,
            return_on_equity_pct
        FROM financial_ratios
    """).fetchall()

    ratio_dict = {}

    for row in ratios:
        ratio_dict[row[0]] = row

    with open(LOG_FILE, "w") as log:

        for company in companies:

            company_id = company[0]
            company_name = company[1]

            source_roce = company[2]
            source_roe = company[3]

            if company_id not in ratio_dict:
                continue

            calc_roce = ratio_dict[company_id][1]
            calc_roe = ratio_dict[company_id][2]

            if calc_roce is not None and source_roce is not None:

                diff = abs(calc_roce - source_roce)

                if diff > 5:

                    log.write(f"Company : {company_name}\n")
                    log.write("Metric : ROCE\n")
                    log.write(f"Source : {source_roce}\n")
                    log.write(f"Computed : {calc_roce}\n")
                    log.write(f"Difference : {round(diff,2)}\n")
                    log.write("Category : Formula Difference\n\n")

            if calc_roe is not None and source_roe is not None:

                diff = abs(calc_roe - source_roe)

                if diff > 5:

                    log.write(f"Company : {company_name}\n")
                    log.write("Metric : ROE\n")
                    log.write(f"Source : {source_roe}\n")
                    log.write(f"Computed : {calc_roe}\n")
                    log.write(f"Difference : {round(diff,2)}\n")
                    log.write("Category : Data Source Issue\n\n")

    conn.close()

    print("Edge case log generated.")
    print("Saved -> output/ratio_edge_cases.log")


if __name__ == "__main__":
    log_edge_cases()