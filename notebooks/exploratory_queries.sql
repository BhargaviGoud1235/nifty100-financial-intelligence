-- Query 1: Total Companies
SELECT COUNT(*) AS total_companies
FROM companies;

-- Query 2: List all companies
SELECT id, company_name
FROM companies
ORDER BY company_name;

-- Query 3: Companies with highest ROE
SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- Query 4: Companies with highest ROCE
SELECT company_name, roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;

-- Query 5: Profit & Loss row count
SELECT COUNT(*)
FROM profitandloss;

-- Query 6: Balance Sheet row count
SELECT COUNT(*)
FROM balancesheet;

-- Query 7: Cash Flow row count
SELECT COUNT(*)
FROM cashflow;

-- Query 8: Documents row count
SELECT COUNT(*)
FROM documents;

-- Query 9: Pros and Cons row count
SELECT COUNT(*)
FROM prosandcons;

-- Query 10: Analysis row count
SELECT COUNT(*)
FROM analysis;