"""
analysis.py — Step 2: Compute Derived Metrics & Statistical Analysis
=====================================================================

🎯 LEARNING POINT: Raw data is rarely enough. The real insight comes from
*derived* columns — ratios, growth rates, inflation-adjusted values, etc.

This module takes a clean DataFrame and enriches it with computed metrics.
Separating analysis from visualization keeps your code modular and testable.
"""

import pandas as pd
import numpy as np


def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Enrich the budget DataFrame with derived analytical columns.

    🎯 LEARNING POINT — Why a separate function?
    By isolating the computation logic:
      1. You can unit-test it independently (pass in a small test DataFrame).
      2. You can swap the visualization layer without touching analysis logic.
      3. It's easier to review — someone reading your code can see
         *what* you computed vs. *how* you displayed it.

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame from data_loader.load_data()

    Returns
    -------
    pd.DataFrame
        Same DataFrame with additional computed columns.
    """

    # Make a copy so we don't mutate the original
    # 🎯 LEARNING POINT: Avoid side effects. Functions should not
    # silently modify their inputs.
    df = df.copy()

    # ── 1. Year-over-Year (YoY) Growth Rate ─────────────────────────────
    # Formula: ((current - previous) / previous) * 100
    #
    # 🎯 LEARNING POINT: pct_change() is a Pandas shortcut.
    # It computes (x[i] - x[i-1]) / x[i-1] for each row.
    # The first row will be NaN because there's no "previous" value.
    df["yoy_growth_pct"] = df["budget_estimate_crores"].pct_change() * 100

    # ── 2. Budget as Percentage of GDP ───────────────────────────────────
    # This contextualizes the budget relative to the economy.
    # A budget can "grow" in absolute terms but *shrink* as a share
    # of GDP if the economy is growing faster.
    #
    # 🎯 LEARNING POINT: Always contextualize absolute numbers.
    # ₹13,000 crore in 2025 is very different from ₹13,000 crore in 2010
    # because the economy was much smaller back then.
    df["budget_pct_of_gdp"] = (
        df["budget_estimate_crores"]             # in crore (= 10^7)
        / (df["gdp_trillion_inr"] * 1e5)         # convert trillion to crore
    ) * 100                                       # express as percentage

    # ── 3. Inflation-Adjusted (Real) Budget ──────────────────────────────
    # We deflate nominal values using CPI to compare purchasing power
    # across years.  Base year: 2012 (CPI index = 100).
    #
    # Formula: real_value = nominal_value × (100 / CPI_current)
    #
    # 🎯 LEARNING POINT: "Nominal" = face value in that year's money.
    # "Real" = adjusted to a base year's purchasing power.
    # Without this adjustment, growth looks more impressive than it is,
    # because part of the "growth" is just inflation.
    BASE_CPI = 100  # CPI index value for base year 2012
    df["real_budget_crores"] = (
        df["budget_estimate_crores"] * (BASE_CPI / df["cpi_index"])
    ).round(2)

    # ── 4. Budget Estimate vs Revised Estimate Variance ──────────────────
    # How well does the government estimate match actual spending?
    # Positive = over-estimated (budget cut), Negative = under-estimated.
    #
    # 🎯 LEARNING POINT: This "planning accuracy" metric is useful in
    # any budgeting analysis — corporate, government, or personal.
    df["be_re_variance_pct"] = (
        (df["budget_estimate_crores"] - df["revised_estimate_crores"])
        / df["budget_estimate_crores"]
    ) * 100

    # ── 5. Three-Year Rolling Average ────────────────────────────────────
    # Smooths out year-to-year volatility to reveal the underlying trend.
    #
    # 🎯 LEARNING POINT: Rolling averages are a fundamental tool in
    # time-series analysis. A 3-year window is common for annual data.
    # Too wide a window over-smooths; too narrow adds noise.
    df["rolling_avg_3yr"] = (
        df["budget_estimate_crores"]
        .rolling(window=3, min_periods=1)
        .mean()
        .round(2)
    )

    return df


def compute_summary_stats(df: pd.DataFrame) -> dict:
    """
    Compute headline summary statistics for the entire period.

    🎯 LEARNING POINT: After computing per-row metrics, step back
    and compute aggregate stats that tell the overall story.

    Returns
    -------
    dict
        Dictionary of key summary statistics.
    """
    stats = {}

    # ── CAGR (Compound Annual Growth Rate) ──────────────────────────────
    # The single best number to summarize long-term growth.
    #
    # Formula: CAGR = (ending / beginning)^(1/n) - 1
    # where n = number of years.
    #
    # 🎯 LEARNING POINT: CAGR is better than simple average growth
    # because it accounts for compounding. If someone asks
    # "how fast did the budget grow?", CAGR is the answer.
    beginning = df["budget_estimate_crores"].iloc[0]
    ending = df["budget_estimate_crores"].iloc[-1]
    n_years = df["start_year"].iloc[-1] - df["start_year"].iloc[0]

    cagr = (ending / beginning) ** (1 / n_years) - 1
    stats["cagr_pct"] = round(cagr * 100, 2)

    # ── Absolute growth ─────────────────────────────────────────────────
    stats["total_growth_pct"] = round(
        ((ending - beginning) / beginning) * 100, 2
    )
    stats["budget_start"] = beginning
    stats["budget_end"] = ending
    stats["period"] = f"FY {df['fiscal_year'].iloc[0]} to FY {df['fiscal_year'].iloc[-1]}"

    # ── Average annual budget ───────────────────────────────────────────
    stats["avg_annual_budget"] = round(df["budget_estimate_crores"].mean(), 2)

    # ── Max YoY growth ──────────────────────────────────────────────────
    max_growth_idx = df["yoy_growth_pct"].idxmax()
    stats["max_yoy_growth_pct"] = round(df.loc[max_growth_idx, "yoy_growth_pct"], 2)
    stats["max_yoy_growth_year"] = df.loc[max_growth_idx, "fiscal_year"]

    # ── Min YoY growth (or max decline) ─────────────────────────────────
    min_growth_idx = df["yoy_growth_pct"].idxmin()
    stats["min_yoy_growth_pct"] = round(df.loc[min_growth_idx, "yoy_growth_pct"], 2)
    stats["min_yoy_growth_year"] = df.loc[min_growth_idx, "fiscal_year"]

    # ── Average BE-RE variance ──────────────────────────────────────────
    stats["avg_be_re_variance_pct"] = round(df["be_re_variance_pct"].mean(), 2)

    # ── Real (inflation-adjusted) growth ────────────────────────────────
    real_beginning = df["real_budget_crores"].iloc[0]
    real_ending = df["real_budget_crores"].iloc[-1]
    real_cagr = (real_ending / real_beginning) ** (1 / n_years) - 1
    stats["real_cagr_pct"] = round(real_cagr * 100, 2)

    # ── GDP share range ─────────────────────────────────────────────────
    stats["gdp_share_min_pct"] = round(df["budget_pct_of_gdp"].min(), 4)
    stats["gdp_share_max_pct"] = round(df["budget_pct_of_gdp"].max(), 4)

    return stats


def print_summary(stats: dict) -> None:
    """Print a formatted summary report to the console."""

    print("\n" + "=" * 60)
    print("📈  SUMMARY STATISTICS")
    print("=" * 60)
    print(f"\n   Period            : {stats['period']}")
    print(f"   Starting Budget   : ₹{stats['budget_start']:,.0f} Cr")
    print(f"   Ending Budget     : ₹{stats['budget_end']:,.0f} Cr")
    print(f"   Total Growth      : {stats['total_growth_pct']}%")
    print(f"   CAGR (nominal)    : {stats['cagr_pct']}%")
    print(f"   CAGR (real)       : {stats['real_cagr_pct']}%")
    print(f"   Avg Annual Budget : ₹{stats['avg_annual_budget']:,.0f} Cr")
    print(f"\n   Best YoY Growth   : {stats['max_yoy_growth_pct']}% ({stats['max_yoy_growth_year']})")
    print(f"   Worst YoY Growth  : {stats['min_yoy_growth_pct']}% ({stats['min_yoy_growth_year']})")
    print(f"   Avg BE→RE Variance: {stats['avg_be_re_variance_pct']}%")
    print(f"\n   GDP Share Range   : {stats['gdp_share_min_pct']}% – {stats['gdp_share_max_pct']}%")
    print("=" * 60)
