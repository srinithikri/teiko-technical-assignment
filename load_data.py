import sqlite3
import pandas as pd

# create database connection
conn = sqlite3.connect("cell_counts.db")
cursor = conn.cursor()

# remove old tables if they exist
cursor.execute("DROP TABLE IF EXISTS cell_counts")
cursor.execute("DROP TABLE IF EXISTS samples")

# sample metadata table
cursor.execute("""
CREATE TABLE samples (
    sample TEXT PRIMARY KEY,
    project TEXT,
    subject TEXT,
    condition TEXT,
    age INTEGER,
    sex TEXT,
    treatment TEXT,
    response TEXT,
    sample_type TEXT,
    time_from_treatment_start INTEGER
)
""")

# immune cell counts table
cursor.execute("""
CREATE TABLE cell_counts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample TEXT,
    population TEXT,
    count INTEGER,
    FOREIGN KEY(sample) REFERENCES samples(sample)
)
""")

# load csv
df = pd.read_csv("data/cell-count.csv")

# store sample information
sample_info = [
    "sample",
    "project",
    "subject",
    "condition",
    "age",
    "sex",
    "treatment",
    "response",
    "sample_type",
    "time_from_treatment_start",
]

df[sample_info].to_sql(
    "samples",
    conn,
    if_exists="append",
    index=False
)

# convert cell columns into rows
cell_types = [
    "b_cell",
    "cd8_t_cell",
    "cd4_t_cell",
    "nk_cell",
    "monocyte",
]

counts_df = df.melt(
    id_vars=["sample"],
    value_vars=cell_types,
    var_name="population",
    value_name="count"
)

counts_df.to_sql(
    "cell_counts",
    conn,
    if_exists="append",
    index=False
)

conn.commit()
conn.close()

print("Database loaded successfully")