import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

conn = sqlite3.connect("cell_counts.db")

# get summary table joined with sample metadata
df = pd.read_sql("""
    SELECT 
        s.sample,
        s.condition,
        s.treatment,
        s.response,
        s.sample_type,
        st.population,
        st.percentage
    FROM summary_table st
    JOIN samples s
        ON st.sample = s.sample
""", conn)

# only melanoma patients, miraclib treatment, and PBMC samples
filtered = df[
    (df["condition"] == "melanoma") &
    (df["treatment"] == "miraclib") &
    (df["sample_type"] == "PBMC")
]

# make boxplot
plt.figure(figsize=(10, 6))

filtered.boxplot(
    column="percentage",
    by=["population", "response"],
    rot=45
)

plt.title("Cell Population Frequencies by Response")
plt.suptitle("")
plt.xlabel("Population and Response")
plt.ylabel("Percentage")
plt.tight_layout()

plt.savefig("boxplot_response.png")
plt.close()

# statistics for each population
results = []

for population in filtered["population"].unique():
    pop_data = filtered[filtered["population"] == population]

    responders = pop_data[pop_data["response"] == "yes"]["percentage"]
    non_responders = pop_data[pop_data["response"] == "no"]["percentage"]

    if len(responders) > 0 and len(non_responders) > 0:
        stat, p_value = mannwhitneyu(
            responders,
            non_responders,
            alternative="two-sided"
        )

        results.append({
            "population": population,
            "p_value": p_value,
            "significant": p_value < 0.05
        })

results_df = pd.DataFrame(results)

results_df.to_csv("significance_results.csv", index=False)

results_df.to_sql(
    "significance_results",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Statistical analysis complete")
print(results_df)