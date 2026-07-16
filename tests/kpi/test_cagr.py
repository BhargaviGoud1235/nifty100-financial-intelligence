import unittest

from src.analytics.cagr import calculate_cagr


class TestCAGR(unittest.TestCase):

    def test_normal_cagr(self):
        value, flag = calculate_cagr(100, 200, 5)
        self.assertEqual(flag, "OK")

    def test_zero_base(self):
        value, flag = calculate_cagr(0, 100, 5)
        self.assertEqual(flag, "ZERO_BASE")

    def test_turnaround(self):
        value, flag = calculate_cagr(-100, 200, 5)
        self.assertEqual(flag, "TURNAROUND")

    def test_decline(self):
        value, flag = calculate_cagr(200, -100, 5)
        self.assertEqual(flag, "DECLINE_TO_LOSS")

    def test_both_negative(self):
        value, flag = calculate_cagr(-100, -200, 5)
        self.assertEqual(flag, "BOTH_NEGATIVE")

    def test_invalid_period(self):
        value, flag = calculate_cagr(100, 200, 0)
        self.assertEqual(flag, "INVALID_PERIOD")


if __name__ == "__main__":
    unittest.main()