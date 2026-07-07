DROP TABLE IF EXISTS companies;

CREATE TABLE companies (

    id TEXT PRIMARY KEY,

    company_logo TEXT,

    company_name TEXT NOT NULL,

    chart_link TEXT,

    about_company TEXT,

    website TEXT,

    nse_profile TEXT,

    bse_profile TEXT,

    face_value REAL,

    book_value REAL,

    roce_percentage REAL,

    roe_percentage REAL
);


DROP TABLE IF EXISTS balancesheet;

CREATE TABLE balancesheet (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    equity_capital REAL,

    reserves REAL,

    borrowings REAL,

    other_liabilities REAL,

    total_liabilities REAL,

    fixed_assets REAL,

    cwip REAL,

    investments REAL,

    other_asset REAL,

    total_assets REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(id)
);

DROP TABLE IF EXISTS cashflow;

CREATE TABLE cashflow (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    operating_activity REAL,

    investing_activity REAL,

    financing_activity REAL,

    net_cash_flow REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(id)
);

DROP TABLE IF EXISTS profitandloss;

CREATE TABLE profitandloss (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    sales REAL,

    expenses REAL,

    operating_profit REAL,

    opm_percentage REAL,

    other_income REAL,

    interest REAL,

    depreciation REAL,

    profit_before_tax REAL,

    tax_percentage REAL,

    net_profit REAL,

    eps REAL,

    dividend_payout REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(id)
);

DROP TABLE IF EXISTS financial_ratios;

CREATE TABLE financial_ratios (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    net_profit_margin_pct REAL,

    operating_profit_margin_pct REAL,

    return_on_equity_pct REAL,

    debt_to_equity REAL,

    interest_coverage REAL,

    asset_turnover REAL,

    free_cash_flow_cr REAL,

    capex_cr REAL,

    earnings_per_share REAL,

    book_value_per_share REAL,

    dividend_payout_ratio_pct REAL,

    total_debt_cr REAL,

    cash_from_operations_cr REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(id)
);

DROP TABLE IF EXISTS sectors;

CREATE TABLE sectors (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    broad_sector TEXT,

    sub_sector TEXT,

    index_weight_pct REAL,

    market_cap_category TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(id)
);

DROP TABLE IF EXISTS stock_prices;

CREATE TABLE stock_prices (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    date DATE,

    open_price REAL,

    high_price REAL,

    low_price REAL,

    close_price REAL,

    volume INTEGER,

    adjusted_close REAL,

    FOREIGN KEY(company_id)
    REFERENCES companies(id)
);

DROP TABLE IF EXISTS analysis;

CREATE TABLE analysis (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    analysis TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(id)
);

DROP TABLE IF EXISTS documents;

CREATE TABLE documents (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    document_name TEXT,

    document_url TEXT,

    FOREIGN KEY(company_id)
    REFERENCES companies(id)
);

DROP TABLE IF EXISTS peer_groups;

CREATE TABLE peer_groups (

    id INTEGER PRIMARY KEY,

    peer_group_name TEXT,

    company_id TEXT,

    is_benchmark INTEGER,

    FOREIGN KEY(company_id)
    REFERENCES companies(id)
);

SELECT
    company_id,
    year,
    return_on_equity_pct,
    debt_to_equity
FROM financial_ratios
WHERE
    return_on_equity_pct > 15
    AND debt_to_equity < 1
ORDER BY return_on_equity_pct DESC;