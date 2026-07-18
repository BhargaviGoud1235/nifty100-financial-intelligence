"""
Sprint 2 - Day 14
Review financial ratios
"""

import sqlite3

DATABASE = "db/nifty100.db"

conn = sqlite3.connect(DATABASE)

print("=" * 60)
print("Financial Ratios Summary")
print("=" * 60)

count = conn.execute(
    "SELECT COUNT(*) FROM financial_ratios"
).fetchone()[0]

print("Total Ratio Rows:", count)

print("\nTop 5 Companies")

rows = conn.execute("""
SELECT
company_id,
year,
roce,
roe
FROM financial_ratios
LIMIT 5
""").fetchall()

for row in rows:
    print(row)

print("\nTables")

tables = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
""").fetchall()

for table in tables:
    print("-", table[0])

conn.close()

print("\nSprint 2 Review Completed")