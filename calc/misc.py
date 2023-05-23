INT = "987654321"
FIELD_VIEW_META = {
    "ticker": {"label": "ticker", "example": "MOON"},
    "name": {"label": "company", "example": "Moon Corp"},
    "sector": {"label": "industries", "example": "Technology"},
    "ebitda": {"label": "ebitda", "example": INT},
    "sales": {"label": "sales", "example": INT},
    "net_profit": {"label": "net profit", "example": INT},
    "market_price": {"label": "market price", "example": INT},
    "net_debt": {"label": "net debt", "example": INT},
    "assets": {"label": "assets", "example": INT},
    "equity": {"label": "equity", "example": INT},
    "cash_equivalents": {"label": "cash equivalents", "example": INT},
    "liabilities": {"label": "liabilities", "example": INT},
}
COMPANIES_FIELDS = ["ticker", "name", "sector"]
FINANCIAL_FIELDS = [
    "ticker", "ebitda", "sales", "net_profit", "market_price",
    "net_debt", "assets", "equity", "cash_equivalents", "liabilities"
]
UPDATE_FIELDS = [
    "ebitda", "sales", "net_profit", "market_price", "net_debt",
    "assets", "equity", "cash_equivalents", "liabilities"
]


def p_e(company):
    if (company["market_price"] is None) or (company["net_profit"] is None):
        return None
    return company["market_price"] / company["net_profit"]


def p_s(company):
    if (company["market_price"] is None) or (company["sales"] is None):
        return None
    return company["market_price"] / company["sales"]


def p_b(company):
    if (company["market_price"] is None) or (company["assets"] is None):
        return None
    return company["market_price"] / company["assets"]


def nd_ebitda(company):
    if (company["net_debt"] is None) or (company["ebitda"] is None):
        return None
    return company["net_debt"] / company["ebitda"]


def roe(company):
    if (company["net_profit"] is None) or (company["equity"] is None):
        return None
    return company["net_profit"] / company["equity"]


def roa(company):
    if (company["net_profit"] is None) or (company["assets"] is None):
        return None
    return company["net_profit"] / company["assets"]


def l_a(company):
    if (company["liabilities"] is None) or (company["assets"] is None):
        return None
    return company["liabilities"] / company["assets"]


STATISTICS = {
    "P/E": p_e,
    "P/S": p_s,
    "P/B": p_b,
    "ND/EBITDA": nd_ebitda,
    "ROE": roe,
    "ROA": roa,
    "L/A": l_a,
}
