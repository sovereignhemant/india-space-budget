"""
data_loader.py — Step 1: Load, Inspect & Validate the Dataset
=============================================================

🎯 LEARNING POINT: Every data analysis project starts here.
Before writing a single chart, you must understand your data:
  • What columns exist?  What are their types?
  • Are there missing values or outliers?
  • Do the values make logical sense?

This module wraps that entire process into a reusable function.
"""

import pandas as pd
import os
import sys


def load_data(csv_path: str = None) -> pd.DataFrame:
    """
    Load the India Space Budget CSV and return a clean DataFrame.

    🎯 LEARNING POINT — Function Signature:
    We provide a default path so the function works out-of-the-box,
    but also accept a custom path for flexibility (e.g., testing
    with a different dataset).

    Parameters
    ----------
    csv_path : str, optional
        Path to the CSV file. If None, defaults to 'data/india_space_budget.csv'
        relative to the project root.

    Returns
    -------
    pd.DataFrame
        Validated, typed DataFrame ready for analysis.
    """

    # ── 1. Resolve file path ────────────────────────────────────────────
    if csv_path is None:
        # __file__ gives us the path to THIS module.
        # We go up one level to reach the project root, then into data/.
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(project_root, "data", "india_space_budget.csv")

    if not os.path.exists(csv_path):
        print(f"❌ Error: File not found at '{csv_path}'")
        sys.exit(1)

    # ── 2. Load CSV ─────────────────────────────────────────────────────
    # 🎯 LEARNING POINT: Always peek at data types after loading.
    # pd.read_csv infers types, but the inference isn't always correct
    # (e.g., fiscal_year like "2010-11" should be a string, not parsed as
    #  a date range).
    df = pd.read_csv(csv_path)

    # ── 3. Inspect ──────────────────────────────────────────────────────
    print("=" * 60)
    print("📊  DATA INSPECTION")
    print("=" * 60)
    print(f"\n📁  Source : {csv_path}")
    print(f"📐  Shape  : {df.shape[0]} rows × {df.shape[1]} columns\n")

    print("── Column Types ──")
    print(df.dtypes.to_string())
    print()

    print("── Missing Values ──")
    nulls = df.isnull().sum()
    if nulls.sum() == 0:
        print("   ✅ No missing values found.\n")
    else:
        print(nulls[nulls > 0].to_string())
        print()

    print("── First 3 Rows ──")
    print(df.head(3).to_string(index=False))
    print()

    # ── 4. Validate ─────────────────────────────────────────────────────
    # 🎯 LEARNING POINT: "Defensive programming" — check assumptions
    # about your data before running analysis.  Catching issues here
    # saves hours of debugging later.

    errors = []

    # 4a. Required columns must exist
    required_cols = [
        "fiscal_year", "start_year", "budget_estimate_crores",
        "revised_estimate_crores", "gdp_trillion_inr", "cpi_index"
    ]
    for col in required_cols:
        if col not in df.columns:
            errors.append(f"Missing required column: '{col}'")

    # 4b. No negative budget values
    for col in ["budget_estimate_crores", "revised_estimate_crores"]:
        if col in df.columns and (df[col] < 0).any():
            errors.append(f"Negative values found in '{col}'")

    # 4c. Years should be in ascending order
    if "start_year" in df.columns:
        if not df["start_year"].is_monotonic_increasing:
            errors.append("'start_year' is not in ascending order")

    # 4d. Budget values should be reasonable (> 0 and < 100,000 crore)
    for col in ["budget_estimate_crores", "revised_estimate_crores"]:
        if col in df.columns:
            if (df[col] <= 0).any() or (df[col] > 100000).any():
                errors.append(f"Suspicious values in '{col}' (expected 0–100,000)")

    # Report results
    if errors:
        print("── ⚠️  Validation Issues ──")
        for e in errors:
            print(f"   • {e}")
        print()
    else:
        print("── ✅ Validation Passed ──")
        print("   All checks passed. Data is ready for analysis.\n")

    print("=" * 60)
    return df
