from app.util_finance import pmt_loan, pmt_lease

def test_pmt_loan_zero_rate():
    assert round(pmt_loan(12000, 0.0, 12), 2) == 1000.00

def test_pmt_loan_positive_rate():
    # Known payment ~ $440.96 for 24mo at 8% on $10k
    p = pmt_loan(10000, 0.08, 24)
    assert 440 < p < 442

def test_pmt_lease_basic():
    # $10k cap, 30% residual, 6% APR, 24 mo → sanity ~ $337-$360
    p = pmt_lease(10000, 0.30, 0.06, 24)
    assert 330 < p < 370
