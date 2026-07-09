import pytest

from src.etl.normaliser import normalize_ticker
from src.etl.normaliser import normalize_year


@pytest.mark.parametrize(
    "input_year,expected",
    [
        ("Mar-23", "2023-03"),
        ("Mar 23", "2023-03"),
        ("Mar-2023", "2023-03"),
        ("FY23", "2023-03"),
        ("FY2023", "2023-03"),
        ("2023", "2023-03"),
        ("Dec-22", "2022-12"),
    ],
)
def test_normalize_year(input_year, expected):

    assert normalize_year(input_year) == expected


@pytest.mark.parametrize(
    "ticker,expected",
    [
        ("infy", "INFY"),
        ("INFY", "INFY"),
        (" Infy ", "INFY"),
        ("tcs", "TCS"),
        (" reliance ", "RELIANCE"),
    ],
)
def test_normalize_ticker(ticker, expected):

    assert normalize_ticker(ticker) == expected