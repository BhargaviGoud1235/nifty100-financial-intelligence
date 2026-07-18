"""
Sprint 2 - Day 13
Ratio Edge Case Detection
"""

import sqlite3

DATABASE = "db/nifty100.db"


def check_ratio_edge_cases():

    conn = sqlite3.connect(DATABASE)

    query = """
    SELECT
        f.company_id,
        f.year,
        f.roce,
        c.roce_percentage,
        f.roe,
        c.roe_percentage
    FROM financial_ratios f
    JOIN companies c
        ON f.company_id = c.id
    """

    rows = conn.execute(query).fetchall()

    with open("output/ratio_edge_cases.log", "w") as file:

        for row in rows:

            company = row[0]
            year = row[1]

            calc_roce = row[2]
            source_roce = row[3]

            calc_roe = row[4]
            source_roe = row[5]

            if calc_roce is not None and source_roce is not None:

                if abs(calc_roce - source_roce) > 5:

                    file.write(
                        f"{company} {year} : ROCE difference = "
                        f"{round(calc_roce-source_roce,2)}\n"
                    )

            if calc_roe is not None and source_roe is not None:

                if abs(calc_roe - source_roe) > 5:

                    file.write(
                        f"{company} {year} : ROE difference = "
                        f"{round(calc_roe-source_roe,2)}\n"
                    )

    conn.close()

    print("ratio_edge_cases.log generated.")