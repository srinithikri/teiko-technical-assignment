# Immune Cell Analysis Dashboard

This project analyzes immune cell population data from a clinical trial dataset. The pipeline loads the provided CSV data into a SQLite database, calculates relative immune cell frequencies, performs statistical analysis comparing treatment responders and non-responders, and displays the results in an interactive Streamlit dashboard.

---

## Setup

Install all required dependencies:

```bash
make setup
```

---

## Run the Full Pipeline

Execute the entire workflow:

```bash
make pipeline
```

This command will:

1. Create and initialize the SQLite database
2. Load the CSV data into the database
3. Generate the summary frequency table
4. Perform statistical analysis
5. Generate significance results and visualizations
6. Run the subset analysis queries

Generated output files include:

* `cell_counts.db`
* `summary_table.csv`
* `significance_results.csv`
* `boxplot_response.png`
* `project_counts.csv`
* `response_counts.csv`
* `sex_counts.csv`
* `average_b_cells_male_responders.csv`

---

## Launch Dashboard

Start the Streamlit dashboard:

```bash
make dashboard
```

The dashboard will launch locally and can be accessed through the URL displayed in the terminal.

Dashboard Link:

```text
The dashboard can be launched locally using:

make dashboard
```

---

## Database Schema

### samples

Stores metadata associated with each biological sample.

| Column                    | Description                     |
| ------------------------- | ------------------------------- |
| sample                    | Unique sample identifier        |
| project                   | Project identifier              |
| subject                   | Subject identifier              |
| condition                 | Disease indication              |
| age                       | Subject age                     |
| sex                       | Subject sex                     |
| treatment                 | Treatment received              |
| response                  | Treatment response              |
| sample_type               | Sample type                     |
| time_from_treatment_start | Timepoint relative to treatment |

Primary Key:

```text
sample
```

### cell_counts

Stores immune cell counts in long format.

| Column     | Description            |
| ---------- | ---------------------- |
| id         | Unique row identifier  |
| sample     | Sample identifier      |
| population | Immune cell population |
| count      | Cell count             |

Foreign Key:

```text
sample -> samples.sample
```

---

## Schema Design Rationale

The database separates sample metadata from immune cell measurements.

The `samples` table stores information that applies to an entire biological sample, while the `cell_counts` table stores measurements for individual immune cell populations.

This design avoids repeating metadata and makes the schema easier to maintain. Instead of storing each immune population as a separate column, immune populations are stored as rows in the `cell_counts` table.

This structure scales well because new immune populations can be added without modifying the database schema. If the dataset expanded to hundreds of projects, thousands of samples, or additional immune populations, the same schema would continue to support filtering, aggregation, and statistical analysis efficiently.

---

## Project Structure

```text
.
├── load_data.py
├── analysis.py
├── stats_analysis.py
├── subset_analysis.py
├── dashboard.py
├── Makefile
├── requirements.txt
├── README.md
├── cell_counts.db
└── output files
```

### File Descriptions

**load_data.py**

Creates the SQLite database schema and loads the CSV data into the database.

**analysis.py**

Calculates total cell counts and relative frequencies for each immune cell population.

**stats_analysis.py**

Filters melanoma PBMC samples treated with miraclib, generates responder vs non-responder boxplots, and performs Mann-Whitney U statistical testing.

**subset_analysis.py**

Performs the required baseline melanoma PBMC subset analysis and generates summary outputs.

**dashboard.py**

Provides an interactive Streamlit dashboard for exploring analysis results.

**Makefile**

Provides commands for setup, pipeline execution, and dashboard launch.

---

## Statistical Analysis

To compare responders and non-responders, I filtered for:

* Melanoma patients
* PBMC samples
* Miraclib treatment

For each immune cell population, relative frequencies were compared using the Mann-Whitney U test.

### Results

| Population | p-value  | Significant |
| ---------- | -------- | ----------- |
| b_cell     | 0.055702 | No          |
| cd8_t_cell | 0.639086 | No          |
| cd4_t_cell | 0.013344 | Yes         |
| nk_cell    | 0.121051 | No          |
| monocyte   | 0.163150 | No          |

The analysis found a statistically significant difference in relative CD4 T cell frequencies between responders and non-responders.

---

## Subset Analysis Results

Baseline melanoma PBMC samples treated with miraclib:

### Samples Per Project

| Project | Samples |
| ------- | ------- |
| prj1    | 384     |
| prj3    | 272     |

### Subjects By Response

| Response | Subjects |
| -------- | -------- |
| no       | 325      |
| yes      | 331      |

### Subjects By Sex

| Sex | Subjects |
| --- | -------- |
| F   | 312      |
| M   | 344      |

### Average B Cell Count

For melanoma male responders at baseline (time_from_treatment_start = 0):

```text
10401.28
```

---

## Dependencies

* pandas
* scipy
* matplotlib
* streamlit
* sqlite3

Dependencies are installed automatically using:

```bash
make setup
```
