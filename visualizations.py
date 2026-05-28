"""
visualizations.py — Step 3: Professional Publication-Quality Charts
====================================================================

🎯 LEARNING POINT: Visualization is where analysis becomes communication.
A great chart should:
  1. Have a clear title that states the INSIGHT, not just the topic
  2. Label axes with units
  3. Use consistent styling (colors, fonts, spacing)
  4. Annotate notable data points
  5. Remove visual clutter (unnecessary gridlines, borders, etc.)

This module creates 6 charts that together tell the story of
India's space budget from 2010 to 2025.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

# ─────────────────────────────────────────────────────────────────────
# 🎯 LEARNING POINT — Global Style Configuration
# Define your entire visual identity ONCE at the top, then use it
# everywhere. This ensures consistency across all charts and makes
# it easy to rebrand the entire project later.
# ─────────────────────────────────────────────────────────────────────

# ISRO-inspired color palette
COLORS = {
    "primary":       "#1B4F72",    # Deep space blue
    "secondary":     "#F39C12",    # Saffron/amber accent
    "positive":      "#27AE60",    # Green for growth
    "negative":      "#E74C3C",    # Red for decline
    "neutral":       "#7F8C8D",    # Gray for context
    "bg":            "#0D1117",    # Dark background
    "card_bg":       "#161B22",    # Slightly lighter card
    "text":          "#E6EDF3",    # Light text
    "text_muted":    "#8B949E",    # Muted text
    "grid":          "#21262D",    # Subtle grid
    "area_fill":     "#1B4F72",    # Area chart fill (blue)
    "area_fill_re":  "#F39C12",    # Area chart fill (amber)
    "highlight":     "#58A6FF",    # Highlight blue
}

# Apply global matplotlib style
plt.rcParams.update({
    "figure.facecolor":  COLORS["bg"],
    "axes.facecolor":    COLORS["card_bg"],
    "axes.edgecolor":    COLORS["grid"],
    "axes.labelcolor":   COLORS["text"],
    "text.color":        COLORS["text"],
    "xtick.color":       COLORS["text_muted"],
    "ytick.color":       COLORS["text_muted"],
    "grid.color":        COLORS["grid"],
    "grid.alpha":        0.5,
    "font.family":       "sans-serif",
    "font.size":         11,
    "axes.titlesize":    15,
    "axes.labelsize":    12,
    "figure.dpi":        150,
    "savefig.dpi":       150,
    "savefig.bbox":      "tight",
    "savefig.facecolor": COLORS["bg"],
})


def _ensure_output_dir(output_dir: str) -> None:
    """Create output directory if it doesn't exist."""
    os.makedirs(output_dir, exist_ok=True)


def _add_watermark(ax) -> None:
    """Add a subtle watermark/credit to each chart."""
    ax.text(
        0.99, 0.01, "Source: Union Budget of India / PIB / ISRO",
        transform=ax.transAxes, fontsize=7,
        color=COLORS["text_muted"], alpha=0.6,
        ha="right", va="bottom"
    )


# =====================================================================
# CHART 1: Budget Trend — BE vs RE (Dual Area Chart)
# =====================================================================
def plot_budget_trend(df, output_dir: str) -> None:
    """
    🎯 LEARNING POINT — Why an area chart?
    Area charts are ideal for showing magnitude over time.
    By overlaying Budget Estimate (BE) and Revised Estimate (RE),
    we can visually see the "gap" — i.e., how much was cut or added
    during the year.
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    years = df["start_year"].values
    be = df["budget_estimate_crores"].values
    re = df["revised_estimate_crores"].values

    # Area fill for Budget Estimate
    ax.fill_between(years, be, alpha=0.30, color=COLORS["area_fill"], label="_nolegend_")
    ax.plot(years, be, color=COLORS["highlight"], linewidth=2.5,
            marker="o", markersize=6, label="Budget Estimate (BE)", zorder=5)

    # Area fill for Revised Estimate
    ax.fill_between(years, re, alpha=0.20, color=COLORS["area_fill_re"], label="_nolegend_")
    ax.plot(years, re, color=COLORS["secondary"], linewidth=2.0,
            marker="s", markersize=5, linestyle="--", label="Revised Estimate (RE)", zorder=4)

    # Shade the gap between BE and RE
    ax.fill_between(years, be, re, alpha=0.15, color=COLORS["negative"],
                    label="BE–RE Gap", where=(be > re))

    # Value labels on BE line
    for x, y in zip(years, be):
        ax.annotate(f"₹{y:,.0f}",
                    (x, y), textcoords="offset points",
                    xytext=(0, 14), ha="center", fontsize=7,
                    color=COLORS["text_muted"])

    ax.set_title("India's Space Budget: Budget Estimate vs Revised Estimate (2010–2025)",
                 fontweight="bold", pad=15)
    ax.set_xlabel("Financial Year (starting)")
    ax.set_ylabel("Budget Allocation (₹ Crores)")
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], rotation=45, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.legend(loc="upper left", framealpha=0.3, edgecolor=COLORS["grid"])
    ax.grid(True, alpha=0.3)
    _add_watermark(ax)

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "01_budget_trend.png"))
    plt.close(fig)
    print("   ✅ Chart 1 saved — Budget Trend (BE vs RE)")


# =====================================================================
# CHART 2: Year-over-Year Growth Rate (Color-Coded Bar Chart)
# =====================================================================
def plot_yoy_growth(df, output_dir: str) -> None:
    """
    🎯 LEARNING POINT — Color encoding:
    Using green for positive and red for negative growth makes the
    chart instantly readable. The viewer doesn't need to check the
    axis — the color tells the story.
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    # Skip first row (NaN because no prior year)
    plot_df = df.dropna(subset=["yoy_growth_pct"])
    years = plot_df["start_year"].values
    growth = plot_df["yoy_growth_pct"].values

    # Color-code: green for positive, red for negative
    colors = [COLORS["positive"] if g >= 0 else COLORS["negative"] for g in growth]

    bars = ax.bar(years, growth, color=colors, width=0.7, edgecolor="none", alpha=0.85)

    # Add value labels on each bar
    for bar, val in zip(bars, growth):
        y_pos = bar.get_height()
        va = "bottom" if val >= 0 else "top"
        offset = 0.5 if val >= 0 else -0.5
        ax.text(bar.get_x() + bar.get_width() / 2, y_pos + offset,
                f"{val:+.1f}%", ha="center", va=va, fontsize=8,
                fontweight="bold", color=COLORS["text"])

    # Zero line
    ax.axhline(y=0, color=COLORS["text_muted"], linewidth=0.8, linestyle="-")

    # Average growth line
    avg_growth = growth.mean()
    ax.axhline(y=avg_growth, color=COLORS["highlight"], linewidth=1.2,
               linestyle=":", alpha=0.7, label=f"Average: {avg_growth:+.1f}%")

    ax.set_title("Year-over-Year Growth in Space Budget Estimate",
                 fontweight="bold", pad=15)
    ax.set_xlabel("Financial Year (starting)")
    ax.set_ylabel("YoY Growth (%)")
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], rotation=45, ha="right")
    ax.legend(loc="upper right", framealpha=0.3, edgecolor=COLORS["grid"])
    ax.grid(True, axis="y", alpha=0.3)
    _add_watermark(ax)

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "02_yoy_growth.png"))
    plt.close(fig)
    print("   ✅ Chart 2 saved — YoY Growth Rate")


# =====================================================================
# CHART 3: Budget as % of GDP (Line Chart)
# =====================================================================
def plot_gdp_share(df, output_dir: str) -> None:
    """
    🎯 LEARNING POINT — Contextual metrics:
    Absolute numbers can be misleading. ₹13,000 Cr sounds like a lot,
    but as a share of India's GDP (~₹350 lakh Cr), it's tiny.
    This chart reveals the *relative priority* of space spending.
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    years = df["start_year"].values
    share = df["budget_pct_of_gdp"].values

    # Gradient fill under the line
    ax.fill_between(years, share, alpha=0.25, color=COLORS["highlight"])
    ax.plot(years, share, color=COLORS["highlight"], linewidth=2.5,
            marker="D", markersize=6, zorder=5)

    # Annotate each point
    for x, y in zip(years, share):
        ax.annotate(f"{y:.3f}%", (x, y),
                    textcoords="offset points", xytext=(0, 12),
                    ha="center", fontsize=8, color=COLORS["text_muted"])

    # Average line
    avg_share = share.mean()
    ax.axhline(y=avg_share, color=COLORS["secondary"], linewidth=1.2,
               linestyle=":", alpha=0.8, label=f"Period Average: {avg_share:.3f}%")

    ax.set_title("Space Budget as a Share of India's GDP — Declining Despite Absolute Growth",
                 fontweight="bold", pad=15)
    ax.set_xlabel("Financial Year (starting)")
    ax.set_ylabel("Budget as % of GDP")
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], rotation=45, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.3f}%"))
    ax.legend(loc="upper right", framealpha=0.3, edgecolor=COLORS["grid"])
    ax.grid(True, alpha=0.3)
    _add_watermark(ax)

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "03_gdp_share.png"))
    plt.close(fig)
    print("   ✅ Chart 3 saved — Budget as % of GDP")


# =====================================================================
# CHART 4: Nominal vs Real (Inflation-Adjusted) Budget
# =====================================================================
def plot_nominal_vs_real(df, output_dir: str) -> None:
    """
    🎯 LEARNING POINT — Inflation adjustment:
    This is arguably the most important chart. It answers:
    "Did spending REALLY increase, or was it just inflation?"
    The gap between the two lines IS the inflation effect.
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    years = df["start_year"].values
    nominal = df["budget_estimate_crores"].values
    real = df["real_budget_crores"].values

    ax.plot(years, nominal, color=COLORS["highlight"], linewidth=2.5,
            marker="o", markersize=6, label="Nominal Budget (as stated)")
    ax.plot(years, real, color=COLORS["positive"], linewidth=2.5,
            marker="^", markersize=6, label="Real Budget (2012 prices)")

    # Shade the inflation gap
    ax.fill_between(years, nominal, real, alpha=0.15, color=COLORS["negative"],
                    label="Inflation Effect")

    # Annotate the endpoints to make the comparison easy
    ax.annotate(f"₹{nominal[-1]:,.0f} Cr\n(nominal)",
                (years[-1], nominal[-1]),
                textcoords="offset points", xytext=(10, 5),
                fontsize=9, color=COLORS["highlight"], fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=COLORS["highlight"], lw=0.8))

    ax.annotate(f"₹{real[-1]:,.0f} Cr\n(real, 2012 ₹)",
                (years[-1], real[-1]),
                textcoords="offset points", xytext=(10, -25),
                fontsize=9, color=COLORS["positive"], fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=COLORS["positive"], lw=0.8))

    ax.set_title("Nominal vs Real Space Budget — How Much Is Just Inflation?",
                 fontweight="bold", pad=15)
    ax.set_xlabel("Financial Year (starting)")
    ax.set_ylabel("Budget (₹ Crores)")
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], rotation=45, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.legend(loc="upper left", framealpha=0.3, edgecolor=COLORS["grid"])
    ax.grid(True, alpha=0.3)
    _add_watermark(ax)

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "04_nominal_vs_real.png"))
    plt.close(fig)
    print("   ✅ Chart 4 saved — Nominal vs Real Budget")


# =====================================================================
# CHART 5: Mission Milestone Timeline (Annotated)
# =====================================================================
def plot_mission_timeline(df, output_dir: str) -> None:
    """
    🎯 LEARNING POINT — Annotation-rich charts:
    The best data stories connect numbers to real-world events.
    Here we annotate the budget line with key ISRO missions,
    letting the viewer correlate funding spikes with mission activity.
    """
    fig, ax = plt.subplots(figsize=(16, 9))

    years = df["start_year"].values
    be = df["budget_estimate_crores"].values
    missions = df["key_mission"].values

    # Main budget line with glow effect
    ax.plot(years, be, color=COLORS["highlight"], linewidth=3, alpha=0.3, zorder=3)
    ax.plot(years, be, color=COLORS["highlight"], linewidth=2, zorder=4)
    ax.scatter(years, be, color=COLORS["secondary"], s=80, zorder=5,
               edgecolors=COLORS["bg"], linewidth=1.5)

    # Annotate each mission milestone
    # Alternate label positions (above/below) to avoid overlap
    for i, (x, y, mission) in enumerate(zip(years, be, missions)):
        if not isinstance(mission, str) or mission.strip() == "":
            continue

        # Shorten long labels
        label = mission if len(mission) <= 40 else mission[:37] + "..."

        # Alternate above/below
        offset_y = 45 if i % 2 == 0 else -55
        va = "bottom" if i % 2 == 0 else "top"

        ax.annotate(
            label,
            (x, y),
            textcoords="offset points",
            xytext=(0, offset_y),
            ha="center", va=va,
            fontsize=7.5,
            color=COLORS["text"],
            fontweight="normal",
            bbox=dict(boxstyle="round,pad=0.3",
                      facecolor=COLORS["card_bg"],
                      edgecolor=COLORS["grid"],
                      alpha=0.9),
            arrowprops=dict(arrowstyle="-|>",
                            color=COLORS["secondary"],
                            lw=0.8,
                            connectionstyle="arc3,rad=0.1"),
            zorder=6
        )

    ax.set_title("India's Space Budget with Mission Milestones (2010–2025)",
                 fontweight="bold", fontsize=16, pad=20)
    ax.set_xlabel("Financial Year (starting)")
    ax.set_ylabel("Budget Estimate (₹ Crores)")
    ax.set_xticks(years)
    ax.set_xticklabels([str(y) for y in years], rotation=45, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.grid(True, alpha=0.3)
    _add_watermark(ax)

    plt.tight_layout()
    fig.savefig(os.path.join(output_dir, "05_mission_timeline.png"))
    plt.close(fig)
    print("   ✅ Chart 5 saved — Mission Milestone Timeline")


# =====================================================================
# CHART 6: Summary Dashboard Panel
# =====================================================================
def plot_summary_dashboard(df, stats: dict, output_dir: str) -> None:
    """
    🎯 LEARNING POINT — Dashboard / Infographic panels:
    Sometimes the best visualization is not a chart at all, but a
    well-designed summary card. This combines key numbers with a
    small sparkline to give an at-a-glance overview.
    """
    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor(COLORS["bg"])

    # Create a grid: top row = 4 KPI cards, bottom row = sparkline + pie
    gs = fig.add_gridspec(2, 4, hspace=0.4, wspace=0.35,
                          top=0.88, bottom=0.08, left=0.06, right=0.94)

    fig.suptitle("India Space Budget  --  Key Metrics at a Glance",
                 fontsize=18, fontweight="bold", color=COLORS["text"], y=0.96)

    # ── KPI Cards (top row) ──────────────────────────────────────────
    kpi_data = [
        ("CAGR\n(Nominal)",   f"{stats['cagr_pct']}%",          COLORS["highlight"]),
        ("CAGR\n(Real)",      f"{stats['real_cagr_pct']}%",     COLORS["positive"]),
        ("Total\nGrowth",     f"{stats['total_growth_pct']}%",  COLORS["secondary"]),
        ("Avg Annual\nBudget", f"₹{stats['avg_annual_budget']:,.0f} Cr", COLORS["text"]),
    ]

    for i, (label, value, color) in enumerate(kpi_data):
        ax = fig.add_subplot(gs[0, i])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        # Card background
        rect = plt.Rectangle((0.05, 0.05), 0.9, 0.9, linewidth=1.5,
                              edgecolor=COLORS["grid"],
                              facecolor=COLORS["card_bg"],
                              transform=ax.transAxes, zorder=0,
                              clip_on=False)
        ax.add_patch(rect)

        # Value
        ax.text(0.5, 0.58, value, transform=ax.transAxes,
                fontsize=22, fontweight="bold", color=color,
                ha="center", va="center")

        # Label
        ax.text(0.5, 0.22, label, transform=ax.transAxes,
                fontsize=10, color=COLORS["text_muted"],
                ha="center", va="center")

    # ── Sparkline (bottom-left, spans 3 cols) ────────────────────────
    ax_spark = fig.add_subplot(gs[1, 0:3])
    years = df["start_year"].values
    be = df["budget_estimate_crores"].values

    ax_spark.fill_between(years, be, alpha=0.2, color=COLORS["highlight"])
    ax_spark.plot(years, be, color=COLORS["highlight"], linewidth=2)
    ax_spark.scatter([years[0], years[-1]], [be[0], be[-1]],
                     color=COLORS["secondary"], s=60, zorder=5)

    ax_spark.annotate(f"₹{be[0]:,.0f}", (years[0], be[0]),
                      textcoords="offset points", xytext=(-5, 12),
                      fontsize=9, color=COLORS["secondary"], fontweight="bold")
    ax_spark.annotate(f"₹{be[-1]:,.0f}", (years[-1], be[-1]),
                      textcoords="offset points", xytext=(5, 12),
                      fontsize=9, color=COLORS["secondary"], fontweight="bold")

    ax_spark.set_title("Budget Trajectory", fontsize=12, pad=8, color=COLORS["text"])
    ax_spark.set_xticks(years[::2])
    ax_spark.set_xticklabels([str(y) for y in years[::2]], fontsize=8)
    ax_spark.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x/1000:.1f}K"))
    ax_spark.grid(True, alpha=0.3)

    # ── Highlights card (bottom-right) ───────────────────────────────
    ax_info = fig.add_subplot(gs[1, 3])
    ax_info.axis("off")

    info_lines = [
        f"Period: {stats['period']}",
        f"Best year: {stats['max_yoy_growth_year']}",
        f"    ({stats['max_yoy_growth_pct']:+.1f}% growth)",
        f"Worst year: {stats['min_yoy_growth_year']}",
        f"    ({stats['min_yoy_growth_pct']:+.1f}% growth)",
        f"GDP share range:",
        f"    {stats['gdp_share_min_pct']:.3f}%–{stats['gdp_share_max_pct']:.3f}%",
    ]

    for j, line in enumerate(info_lines):
        ax_info.text(0.08, 0.90 - j * 0.13, line,
                     transform=ax_info.transAxes,
                     fontsize=9, color=COLORS["text"],
                     va="top", family="monospace")

    fig.savefig(os.path.join(output_dir, "06_summary_dashboard.png"))
    plt.close(fig)
    print("   ✅ Chart 6 saved — Summary Dashboard")


# =====================================================================
# Master function — generate all charts
# =====================================================================
def generate_all_charts(df, stats: dict, output_dir: str = "output") -> None:
    """
    Generate all 6 charts and save them to the output directory.

    🎯 LEARNING POINT — Master orchestrator:
    Having a single entry point to generate all charts makes it easy
    to run from the command line or integrate into a pipeline.
    """
    _ensure_output_dir(output_dir)

    print("\n" + "=" * 60)
    print("🎨  GENERATING CHARTS")
    print("=" * 60 + "\n")

    plot_budget_trend(df, output_dir)
    plot_yoy_growth(df, output_dir)
    plot_gdp_share(df, output_dir)
    plot_nominal_vs_real(df, output_dir)
    plot_mission_timeline(df, output_dir)
    plot_summary_dashboard(df, stats, output_dir)

    print(f"\n   📁 All charts saved to: {os.path.abspath(output_dir)}/")
    print("=" * 60)
