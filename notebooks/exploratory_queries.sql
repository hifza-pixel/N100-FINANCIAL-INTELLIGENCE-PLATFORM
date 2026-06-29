-- 1. Total Companies
SELECT COUNT(*) AS total_companies
FROM companies;

-- 2. Top 10 Companies by ROE
SELECT company_name, roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- 3. Companies by Sector
SELECT broad_sector, COUNT(*) AS total
FROM sectors
GROUP BY broad_sector
ORDER BY total DESC;

-- 4. Average Sales by Year
SELECT year,
AVG(sales) AS avg_sales
FROM profitandloss
GROUP BY year
ORDER BY year;

-- 5. Highest Market Cap
SELECT company_id,
market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

-- 6. Highest Net Profit
SELECT company_id,
net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- 7. Highest Operating Profit Margin
SELECT company_id,
operating_profit_margin_pct
FROM financial_ratios
ORDER BY operating_profit_margin_pct DESC
LIMIT 10;

-- 8. Stock Price Records
SELECT COUNT(*)
FROM stock_prices;

-- 9. Companies Having More Than 10 Years Data
SELECT company_id,
COUNT(DISTINCT year) AS years
FROM profitandloss
GROUP BY company_id
HAVING years>=10;

-- 10. Foreign Key Check
PRAGMA foreign_key_check;