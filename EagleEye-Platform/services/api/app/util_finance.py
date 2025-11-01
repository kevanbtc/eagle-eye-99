from math import isclose

def pmt_loan(principal: float, apr: float, term_months: int) -> float:
    """Monthly payment for a fully amortizing loan."""
    if term_months <= 0:
        raise ValueError("term_months must be > 0")
    r = apr / 12.0
    if isclose(r, 0.0, abs_tol=1e-12):
        return principal / term_months
    return principal * (r * (1 + r) ** term_months) / ((1 + r) ** term_months - 1)

def pmt_lease(cap_cost: float, residual_pct: float, apr: float, term_months: int) -> float:
    """Simple closed-end lease payment (approx): depreciation + finance charge."""
    residual = cap_cost * residual_pct
    depreciation = (cap_cost - residual) / term_months
    money_factor = apr / 24.0  # approx APR→MF
    finance_charge = (cap_cost + residual) * money_factor
    return depreciation + finance_charge
