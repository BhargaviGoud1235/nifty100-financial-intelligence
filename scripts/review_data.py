import sqlite3
import random

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

print("=" * 60)
print("5 Random Companies")
print("=" * 60)

companies = cursor.execute(
    "SELECT id, company_name FROM companies"
).fetchall()

sample = random.sample(companies, 5)

for company in sample:
    print(company)

print("\n" + "=" * 60)
print("Company Count")
print("=" * 60)

count = cursor.execute(
    "SELECT COUNT(*) FROM companies"
).fetchone()[0]

print(count)

print("\n" + "=" * 60)
print("Profit & Loss Rows")
print("=" * 60)

rows = cursor.execute(
    "SELECT COUNT(*) FROM profitandloss"
).fetchone()[0]

print(rows)

conn.close()