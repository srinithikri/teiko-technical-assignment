import sqlite3
import pandas as pd

conn = sqlite3.connect("cell_counts.db")

# baseline melanoma PBMC samples treated with miraclib
baseline = pd.read_sql("""
    SELECT *
    FROM samples
    WHERE condition = 'melanoma'
      AND treatment = 'miraclib'
      AND sample_type = 'PBMC'
      AND time_from_treatment_start = 0
""", conn)

# samples from each project
project_counts = (
    baseline.groupby("project")["sample"]
    .count()
    .reset_index()
)

project_counts.columns = ["project", "sample_count"]

# distinct subjects by response
response_counts = (
    baseline.groupby("response")["subject"]
    .nunique()
    .reset_index()
)

response_counts.columns = ["response", "subject_count"]

# distinct subjects by sex
sex_counts = (
    baseline.groupby("sex")["subject"]
    .nunique()
    .reset_index()
)

sex_counts.columns = ["sex", "subject_count"]

# average B cells for melanoma male responders at baseline
# dataset uses M/F instead of male/female
avg_b_cells = pd.read_sql("""
    SELECT AVG(c.count) AS avg_b_cells
    FROM samples s
    JOIN cell_counts c
        ON s.sample = c.sample
    WHERE s.condition = 'melanoma'
      AND s.treatment = 'miraclib'
      AND s.sample_type = 'PBMC'
      AND s.time_from_treatment_start = 0
      AND s.sex = 'M'
      AND s.response = 'yes'
      AND c.population = 'b_cell'
""", conn)

avg_b_cell_value = avg_b_cells["avg_b_cells"].iloc[0]

print("\nSamples from each project:")
print(project_counts)

print("\nSubjects by response:")
print(response_counts)

print("\nSubjects by sex:")
print(sex_counts)

print("\nAverage B cells for male responders at baseline:")
if avg_b_cell_value is not None:
    print(f"{avg_b_cell_value:.2f}")
else:
    print("No matching samples found")

project_counts.to_csv("project_counts.csv", index=False)
response_counts.to_csv("response_counts.csv", index=False)
sex_counts.to_csv("sex_counts.csv", index=False)
avg_b_cells.to_csv("average_b_cells_male_responders.csv", index=False)

conn.close()