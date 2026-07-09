from src.etl.loader import load_excel
from src.etl.validator import DataValidator

df = load_excel("data/raw/companies.xlsx")

validator = DataValidator()

report = validator.validate(df)

print(report)

validator.save_report()