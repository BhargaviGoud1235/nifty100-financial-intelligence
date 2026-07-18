"""
Sprint 2 - Day 13
Check Financial Ratios Table
"""

import sqlite3

conn = sqlite3.connect("db/nifty100.db")

print("=" * 60)
print("Financial Ratios Count")
print("=" * 60)

count = conn.execute(
    "SELECT COUNT(*) FROM financial_ratios"
).fetchone()[0]

print(count)

print("\n" + "=" * 60)
print("Sample Rows")
print("=" * 60)

rows = conn.execute("""
SELECT
company_id,
year,
return_on_equity_pct,
return_on_capital_employed_pct
FROM financial_ratios
LIMIT 10
""").fetchall()

for row in rows:
    print(row)

conn.close()