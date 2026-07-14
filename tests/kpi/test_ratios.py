import unittest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    check_opm,
)


class TestRatios(unittest.TestCase):

    def test_net_profit_margin(self):
        self.assertEqual(net_profit_margin(100, 1000), 10.0)

    def test_npm_zero_sales(self):
        self.assertIsNone(net_profit_margin(100, 0))

    def test_opm(self):
        self.assertEqual(operating_profit_margin(200, 1000), 20.0)

    def test_opm_zero_sales(self):
        self.assertIsNone(operating_profit_margin(100, 0))

    def test_opm_crosscheck(self):
        self.assertTrue(check_opm(25, 27))

    def test_roe(self):
        self.assertEqual(return_on_equity(100, 200, 300), 20.0)

    def test_negative_equity(self):
        self.assertIsNone(return_on_equity(100, -100, 50))

    def test_roce(self):
        self.assertEqual(
            return_on_capital_employed(
            100,
            10,
            300,
            200,
            100
        ),
        18.33
    )

    def test_roa(self):
        self.assertEqual(return_on_assets(100, 500), 20.0)

    def test_roa_zero_assets(self):
        self.assertIsNone(return_on_assets(100, 0))


if __name__ == "__main__":
    unittest.main()