# 🇮🇳 India's Space Budget Analysis (2010–2025)

A Python data analysis project that examines India's Department of Space budget allocations over 15 years, revealing trends in nominal growth, real (inflation-adjusted) spending, GDP share, and correlations with major ISRO missions.

---

## 📂 Project Structure

```
india-space-budget/
├── data/
│   └── india_space_budget.csv     ← Curated dataset (16 fiscal years)
├── src/
│   ├── data_loader.py             ← Step 1: Load & validate
│   ├── analysis.py                ← Step 2: Compute derived metrics
│   └── visualizations.py          ← Step 3: Generate all charts
├── output/                        ← Generated chart PNGs (auto-created)
├── main.py                        ← Run the full pipeline
├── requirements.txt               ← Python dependencies
└── README.md                      ← You are here
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or later
- pip (Python package manager)

### Install & Run

```bash
# 1. Navigate to the project directory
cd india-space-budget

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the analysis
python main.py
```

All 6 charts will be saved as PNGs in the `output/` folder.

---

## 📊 What This Project Analyses

| Chart | What It Shows |
|-------|---------------|
| Budget Trend (BE vs RE) | How the allocation changed over time, and how much was actually spent vs. planned |
| YoY Growth Rate | Which years saw the biggest jumps or cuts |
| Budget as % of GDP | Whether space spending is keeping up with India's economic growth |
| Nominal vs Real Budget | How much of the "growth" is just inflation |
| Mission Timeline | Connecting budget patterns to real ISRO milestones |
| Summary Dashboard | Key metrics at a glance |

---

## 🧠 How to Approach ANY Budget/Data Analysis Project

This project teaches a **reusable methodology** you can apply to any dataset:

### Step 1: Define Your Question
> "Is India spending more on space, and is it keeping up with the economy?"

Before touching data, write down 2–3 questions you want to answer.

### Step 2: Collect & Curate Data
- Find primary sources (government budget docs, PIB, official reports)
- Build a clean CSV with consistent columns
- Document your sources

### Step 3: Load & Validate
- Check for missing values, duplicates, wrong types
- Sanity-check ranges (no negative budgets, years in order)

### Step 4: Compute Derived Metrics
Don't just visualize raw data. Compute:
- **Growth rates** (YoY, CAGR) → trend direction
- **Ratios** (% of GDP) → contextual importance
- **Inflation-adjusted values** → real purchasing power
- **Rolling averages** → smooth out noise
- **Variance metrics** (BE vs RE) → planning accuracy

### Step 5: Visualize with Purpose
Each chart should answer a specific question:
- Use **area/line charts** for trends over time
- Use **bar charts** for comparing discrete values
- Use **annotations** to connect data to real-world events
- Use a **consistent color scheme** across all charts

### Step 6: Summarize Insights
Don't just show data — state what it MEANS. Lead with the insight:
- ❌ "Here is a chart of the budget"
- ✅ "India's space budget tripled in nominal terms, but GDP share fell"

---

## 📋 Data Sources

| Source | What |
|--------|------|
| [Union Budget Documents](https://www.indiabudget.gov.in/) | Official budget estimates (BE) and revised estimates (RE) |
| [PIB Press Releases](https://pib.gov.in/) | Department of Space budget announcements |
| [ISRO Annual Reports](https://www.isro.gov.in/) | Mission details, actual expenditure |
| [RBI Handbook](https://www.rbi.org.in/) | GDP data, CPI inflation indices |

> **Note:** Budget figures are "Budget Estimates" (BE) as presented in Parliament.
> Revised Estimates (RE) may differ due to mid-year adjustments.

---

## 📜 License

This is an educational project. Data is sourced from public government documents.
