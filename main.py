"""
main.py — Entry Point: Run the Full Analysis Pipeline
======================================================

🎯 LEARNING POINT — The Pipeline Pattern:
Every data analysis project follows this structure:

    ┌──────────┐     ┌───────────┐     ┌─────────────┐     ┌──────────┐
    │  LOAD    │ ──▶ │  ANALYZE  │ ──▶ │  VISUALIZE  │ ──▶ │  REPORT  │
    │  data    │     │  compute  │     │  create      │     │  summary │
    └──────────┘     └───────────┘     │  charts      │     │  stats   │
                                       └─────────────┘     └──────────┘

This script ties together all three modules in the correct order.
Each step is independent and reusable on its own.

How to run:
    python main.py
"""

import os
import sys

# ── Ensure the project root is on the Python path ───────────────────
# 🎯 LEARNING POINT: This is needed so that `import src.xxx` works
# regardless of which directory you run the script from.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from src.data_loader import load_data
from src.analysis import compute_metrics, compute_summary_stats, print_summary
from src.visualizations import generate_all_charts


def main():
    """
    Run the full India Space Budget analysis pipeline.

    🎯 LEARNING POINT — main() function pattern:
    Wrapping your logic in a main() function (instead of writing it
    at the module top level) is a Python best practice. It:
      1. Prevents code from running on import
      2. Makes the script testable
      3. Clearly defines the entry point
    """

    print("\n" + "🚀" * 30)
    print("\n  INDIA'S SPACE BUDGET ANALYSIS (2010–2025)")
    print("  Analysing Department of Space allocations\n")
    print("🚀" * 30)

    # ── STEP 1: Load & Validate ─────────────────────────────────────
    # 🎯 WHY: You can't analyze what you haven't loaded and verified.
    # If the CSV is corrupt or has unexpected columns, we want to
    # know NOW, not 3 steps later with a cryptic KeyError.
    csv_path = os.path.join(PROJECT_ROOT, "data", "india_space_budget.csv")
    df = load_data(csv_path)

    # ── STEP 2: Compute Derived Metrics ─────────────────────────────
    # 🎯 WHY: Raw budget numbers alone don't tell the full story.
    # We need growth rates, GDP ratios, and inflation-adjusted values
    # to draw meaningful conclusions.
    df = compute_metrics(df)

    # Let's peek at the enriched data
    print("\n── Enriched Data (key columns) ──")
    display_cols = [
        "fiscal_year", "budget_estimate_crores", "yoy_growth_pct",
        "budget_pct_of_gdp", "real_budget_crores", "be_re_variance_pct"
    ]
    print(df[display_cols].to_string(index=False, float_format="%.2f"))

    # ── STEP 3: Compute Summary Statistics ──────────────────────────
    # 🎯 WHY: Before visualizing, get the headline numbers. These
    # will also feed into Chart 6 (the summary dashboard).
    stats = compute_summary_stats(df)
    print_summary(stats)

    # ── STEP 4: Generate All Charts ─────────────────────────────────
    # 🎯 WHY: Visualization is how you COMMUNICATE your findings.
    # A table of numbers is precise but hard to read. Charts make
    # patterns, trends, and outliers instantly visible.
    output_dir = os.path.join(PROJECT_ROOT, "output")
    generate_all_charts(df, stats, output_dir)

    # ── STEP 5: Final Report ────────────────────────────────────────
    print("\n" + "=" * 60)
    print("✅  ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"""
    📁 Charts saved to: {output_dir}

    Generated charts:
      1. 01_budget_trend.png       — BE vs RE over time
      2. 02_yoy_growth.png         — Year-over-year growth rates
      3. 03_gdp_share.png          — Budget as % of GDP
      4. 04_nominal_vs_real.png    — Inflation-adjusted comparison
      5. 05_mission_timeline.png   — Budget + ISRO milestones
      6. 06_summary_dashboard.png  — Key metrics dashboard

    💡 Key Insight: India's space budget grew from ₹{stats['budget_start']:,.0f} Cr
    to ₹{stats['budget_end']:,.0f} Cr (CAGR: {stats['cagr_pct']}% nominal,
    {stats['real_cagr_pct']}% real).  While absolute spending increased
    substantially, the GDP share has been declining, suggesting space
    spending is not keeping pace with overall economic growth.
    """)


# ── Guard clause ────────────────────────────────────────────────────
# 🎯 LEARNING POINT: This is Python's standard entry-point idiom.
# __name__ == "__main__" is True only when you run the file directly
# (python main.py), NOT when someone imports it as a module.
if __name__ == "__main__":
    main()
