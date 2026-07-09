"""
Excel Loader
Reads Excel files with header row = 1
"""

from pathlib import Path

import pandas as pd


def load_excel(file_path: str, header: int = 1) -> pd.DataFrame:
    """
    Load Excel file.

    Parameters
    ----------
    file_path : str
        Path to Excel file

    header : int
        Excel header row

    Returns
    -------
    pandas.DataFrame
    """

    file = Path(file_path)

    if not file.exists():
        raise FileNotFoundError(f"File not found: {file}")

    df = pd.read_excel(file, header=header)

# Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
)

    # Clean company IDs
    from src.etl.normaliser import normalize_ticker

    if "id" in df.columns:
     df["id"] = df["id"].apply(normalize_ticker)

    return df



def preview_excel(file_path: str):
    """
    Print quick summary of Excel.
    """

    df = load_excel(file_path)

    print("=" * 60)
    print("Shape:", df.shape)
    print("=" * 60)
    print(df.head())
    print("=" * 60)
    print(df.columns.tolist())

    return df


if __name__ == "__main__":

    FILE = "data/raw/companies.xlsx"

    preview_excel(FILE)