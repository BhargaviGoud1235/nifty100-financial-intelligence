import unittest

from src.analytics.cashflow_kpis import *


class TestCashflowKPIs(unittest.TestCase):

    def test_free_cash_flow(self):
        self.assertEqual(free_cash_flow(100, -40), 60)

    def test_cfo_quality(self):
        self.assertEqual(cfo_quality_score(120, 100), "High Quality")

    def test_capex(self):
        self.assertEqual(capex_intensity(-20, 1000), "Asset Light")

    def test_fcf_conversion(self):
        self.assertEqual(fcf_conversion_rate(100, 200), 50.0)

    def test_pattern(self):
        self.assertEqual(
            capital_allocation_pattern(100, -50, -20),
            "Reinvestor"
        )


if __name__ == "__main__":
    unittest.main()