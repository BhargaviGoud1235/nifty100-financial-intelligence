"""
Utility functions for normalizing company tickers and financial years.
"""

import re


def normalize_ticker(ticker: str) -> str:
    """
    Normalize company ticker.

    Examples
    --------
    infy -> INFY
    INFY -> INFY
     infy  -> INFY
    """

    if ticker is None:
        return ""

    return str(ticker).strip().upper()


def normalize_year(year) -> str:
    """
    Convert year formats into YYYY-MM.

    Examples
    --------
    Mar-23     -> 2023-03
    Mar 23     -> 2023-03
    Mar-2023   -> 2023-03
    FY23       -> 2023-03
    FY2023     -> 2023-03
    Dec-22     -> 2022-12
    2023       -> 2023-03
    """

    if year is None:
        return ""

    year = str(year).strip()

    if year.isdigit():
        if len(year) == 4:
            return f"{year}-03"

        if len(year) == 2:
            yr = int(year)
            yr += 2000 if yr < 50 else 1900
            return f"{yr}-03"

    fy_match = re.match(r"FY\s*[- ]?(\d{2,4})", year, re.IGNORECASE)
    if fy_match:
        yr = fy_match.group(1)

        if len(yr) == 2:
            yr = str(2000 + int(yr))

        return f"{yr}-03"

    month_map = {
        "JAN": "01",
        "FEB": "02",
        "MAR": "03",
        "APR": "04",
        "MAY": "05",
        "JUN": "06",
        "JUL": "07",
        "AUG": "08",
        "SEP": "09",
        "OCT": "10",
        "NOV": "11",
        "DEC": "12",
    }

    m = re.match(r"([A-Za-z]{3})[- ]?(\d{2,4})", year)

    if m:

        month = month_map[m.group(1).upper()]
        yr = m.group(2)

        if len(yr) == 2:
            yr = str(2000 + int(yr))

        return f"{yr}-{month}"

    return year