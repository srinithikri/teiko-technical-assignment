import sqlite3
import pandas as pd

conn = sqlite3.connect("cell_counts.db")

# read the cell count table from the database
counts = pd.read_sql("""
    SELECT sample, population, count
    FROM cell_counts
""", conn)

# total number of cells in each sample
totals = counts.groupby("sample")["count"].sum().reset_index()
totals = totals.rename(columns={"count": "total_count"})

# add total count back to each row
summary = counts.merge(totals, on="sample")

# calculate relative frequency
summary["percentage"] = (summary["count"] / summary["total_count"]) * 100

# order columns based on assignment
summary = summary[
    ["sample", "total_count", "population", "count", "percentage"]
]

# save as csv and also back into database
summary.to_csv("summary_table.csv", index=False)

summary.to_sql(
    "summary_table",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Summary table created")