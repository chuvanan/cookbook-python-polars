import polars as pl

dta = pl.read_csv(
    source="data/On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2022_1.csv",
    has_header=True,
)

print("shape of the dataset:", dta.shape)

rows_by_day = (
    dta.group_by(["DayofMonth"]).agg(pl.len().alias("Count")).sort("DayofMonth")
)

rows_by_day.describe()
