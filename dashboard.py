import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Immune Cell Analysis",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Immune Cell Analysis Dashboard")
st.write(
    "Interactive dashboard for exploring immune cell population frequencies, "
    "treatment response patterns, and baseline melanoma PBMC samples."
)

conn = sqlite3.connect("cell_counts.db")

summary = pd.read_sql("SELECT * FROM summary_table", conn)
stats = pd.read_sql("SELECT * FROM significance_results", conn)

project_counts = pd.read_csv("project_counts.csv")
response_counts = pd.read_csv("response_counts.csv")
sex_counts = pd.read_csv("sex_counts.csv")
avg_b = pd.read_csv("average_b_cells_male_responders.csv")

# sidebar
st.sidebar.header("Filters")

sample = st.sidebar.selectbox(
    "Choose a sample",
    sorted(summary["sample"].unique())
)

population_filter = st.sidebar.multiselect(
    "Choose cell populations",
    sorted(summary["population"].unique()),
    default=sorted(summary["population"].unique())
)

filtered_summary = summary[
    (summary["sample"] == sample) &
    (summary["population"].isin(population_filter))
]

# top metrics
st.subheader("Project Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Samples", summary["sample"].nunique())
col2.metric("Cell Populations", summary["population"].nunique())
col3.metric("Significant Populations", stats["significant"].sum())
col4.metric(
    "Avg B Cells",
    f"{avg_b['avg_b_cells'][0]:.2f}"
)

st.divider()

# part 2
st.header("Part 2: Cell Population Frequencies")

left, right = st.columns([1.2, 1])

with left:
    st.write(f"Showing relative immune cell frequencies for sample `{sample}`.")
    st.dataframe(
        filtered_summary,
        use_container_width=True
    )

with right:
    chart_data = filtered_summary.set_index("population")["percentage"]
    st.bar_chart(chart_data)

st.divider()

# part 3
st.header("Part 3: Responder vs Non-Responder Analysis")

col1, col2 = st.columns([1.4, 1])

with col1:
    st.image(
        "boxplot_response.png",
        caption="Relative cell population frequencies by response group",
    )

with col2:
    st.subheader("Significance Results")
    st.dataframe(
        stats,
        use_container_width=True
    )

    significant = stats[stats["significant"] == 1]

    if len(significant) > 0:
        st.success(
            "Significant difference found for: "
            + ", ".join(significant["population"])
        )
    else:
        st.warning("No significant differences found.")

st.divider()

# part 4
st.header("Part 4: Baseline Melanoma PBMC Analysis")

m1, m2, m3 = st.columns(3)

m1.metric("Project prj1 Samples", int(project_counts.loc[project_counts["project"] == "prj1", "sample_count"].iloc[0]))
m2.metric("Project prj3 Samples", int(project_counts.loc[project_counts["project"] == "prj3", "sample_count"].iloc[0]))
m3.metric("Male Responder Avg B Cells", f"{avg_b['avg_b_cells'][0]:.2f}")

c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("Samples by Project")
    st.dataframe(project_counts, use_container_width=True)
    st.bar_chart(project_counts.set_index("project")["sample_count"])

with c2:
    st.subheader("Subjects by Response")
    st.dataframe(response_counts, use_container_width=True)
    st.bar_chart(response_counts.set_index("response")["subject_count"])

with c3:
    st.subheader("Subjects by Sex")
    st.dataframe(sex_counts, use_container_width=True)
    st.bar_chart(sex_counts.set_index("sex")["subject_count"])

conn.close()