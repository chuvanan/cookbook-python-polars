import glob
import sqlite3

import duckdb
import polars as pl

# --- Create SQLite database and table schema from DuckDB ---

type_map = {"BIGINT": "INTEGER", "DOUBLE": "REAL", "VARCHAR": "TEXT"}

con_duck = duckdb.connect("data/ontime.duckdb")
schema = con_duck.execute("DESCRIBE ontime").df()
con_duck.close()

col_defs = ", ".join(
    f'"{row["column_name"]}" {type_map.get(row["column_type"], "TEXT")}'
    for _, row in schema.iterrows()
)

con_sqlite = sqlite3.connect("data/ontime.sqlite")
cur = con_sqlite.cursor()
cur.execute("DROP TABLE IF EXISTS ontime")
cur.execute(f"CREATE TABLE ontime ({col_defs})")
con_sqlite.commit()
print("Table created.")

# --- Insert data from all 12 CSV files ---

placeholders = ", ".join(["?"] * len(schema))
col_names = ", ".join(f'"{c}"' for c in schema["column_name"])
insert_sql = f"INSERT INTO ontime ({col_names}) VALUES ({placeholders})"

csv_files = sorted(glob.glob(
    "data/On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2022_*.csv"
))

total = 0
for f in csv_files:
    df = pl.scan_csv(f, infer_schema_length=1000).collect()
    rows = df.rows()
    cur.executemany(insert_sql, rows)
    con_sqlite.commit()
    total += len(rows)
    print(f"{f.split('/')[-1]}: {len(rows):,} rows (cumulative: {total:,})")

con_sqlite.close()
print(f"\nDone. Total rows inserted: {total:,}")

# --- Verify row counts per month ---

con_sqlite = sqlite3.connect("data/ontime.sqlite")
result = con_sqlite.execute("""
    SELECT Month, COUNT(*) AS row_count
    FROM ontime
    GROUP BY Month
    ORDER BY Month
""").fetchall()
con_sqlite.close()

print(f"\n{'Month':>6}  {'Row Count':>10}")
print("-" * 20)
for month, count in result:
    print(f"{month:>6}  {count:>10,}")
