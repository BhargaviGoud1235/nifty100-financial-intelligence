"""
Data Quality Validator
Sprint 1 - Day 03
"""

from pathlib import Path
import pandas as pd


class DataValidator:
    def __init__(self):
        self.failures = []

    def add_failure(self, rule, severity, row, message):
        self.failures.append({
            "rule": rule,
            "severity": severity,
            "row": row,
            "message": message
        })

    def dq01_primary_key(self, df):
        """
        DQ-01
        Company ID must be unique
        """

        duplicates = df[df["id"].duplicated()]

        for index, row in duplicates.iterrows():
            self.add_failure(
                "DQ-01",
                "CRITICAL",
                index,
                f"Duplicate ID: {row['id']}"
            )

    def dq06_positive_book_value(self, df):
        """
        Book value must be positive
        """

        invalid = df[df["book_value"] <= 0]

        for index, row in invalid.iterrows():
            self.add_failure(
                "DQ-06",
                "WARNING",
                index,
                f"Invalid Book Value: {row['book_value']}"
            )

    def dq07_positive_roce(self, df):

        invalid = df[df["roce_percentage"] < 0]

        for index, row in invalid.iterrows():
            self.add_failure(
                "DQ-07",
                "WARNING",
                index,
                f"Negative ROCE: {row['roce_percentage']}"
            )

    def dq08_positive_roe(self, df):

        invalid = df[df["roe_percentage"] < 0]

        for index, row in invalid.iterrows():
            self.add_failure(
                "DQ-08",
                "WARNING",
                index,
                f"Negative ROE: {row['roe_percentage']}"
            )

    def dq09_missing_company_name(self, df):

        invalid = df[df["company_name"].isna()]

        for index, row in invalid.iterrows():
            self.add_failure(
                "DQ-09",
                "CRITICAL",
                index,
                "Company Name Missing"
            )

    def dq10_missing_website(self, df):

        invalid = df[df["website"].isna()]

        for index, row in invalid.iterrows():
            self.add_failure(
                "DQ-10",
                "WARNING",
                index,
                "Website Missing"
            )

    def validate(self, df):

        self.dq01_primary_key(df)
        self.dq06_positive_book_value(df)
        self.dq07_positive_roce(df)
        self.dq08_positive_roe(df)
        self.dq09_missing_company_name(df)
        self.dq10_missing_website(df)

        return pd.DataFrame(self.failures)

    def save_report(self, output="output/validation_failures.csv"):

        Path("output").mkdir(exist_ok=True)

        report = pd.DataFrame(self.failures)

        report.to_csv(output, index=False)

        print(f"Validation report saved -> {output}")