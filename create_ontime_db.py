import duckdb

con = duckdb.connect("data/ontime.duckdb")

con.execute("""
    CREATE TABLE IF NOT EXISTS ontime AS
    SELECT * FROM read_csv(
        'data/On_Time_Reporting_Carrier_On_Time_Performance_(1987_present)_2022_*.csv',
        union_by_name = true
    )
""")

count = con.execute("SELECT COUNT(*) FROM ontime").fetchone()[0]
print(f"Rows inserted: {count:,}")

# Verify all 12 months are present
result = con.execute("""
    SELECT Month, COUNT(*) AS row_count
    FROM ontime
    GROUP BY Month
    ORDER BY Month
""").df()
print(result)

con.close()
