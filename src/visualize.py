# src/visualize.py
"""
Publication-Quality Visualization Suite for Mercedes Fish Port Simulation.
Produces thesis-ready figures with 95% Confidence Interval error bars,
distribution histograms, sensitivity curves, and PRNG spectral lattice plots.
Styled with a high-contrast dark aesthetic for modern interfaces.
"""

import os
from typing import List, Dict, Any
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("outputs/figures", exist_ok=True)

# Modern Design Tokens for Charts
CHART_BG = "#111827"        # Dark slate surface
TEXT_MAIN = "#F8FAFC"       # Crisp white
TEXT_MUTED = "#94A3B8"      # Slate 400
SPINE_COLOR = "#334155"     # Slate 700
GRID_COLOR = "#1E293B"      # Slate 800
COLOR_PRIMARY = "#3B82F6"   # Electric Blue
COLOR_DANGER = "#EF4444"    # Coral Red
COLOR_SUCCESS = "#10B981"   # Emerald
COLOR_WARNING = "#F59E0B"   # Amber


def apply_dark_theme(fig, ax):
    """Applies modern dark-mode styling to matplotlib figure and axis."""
    fig.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(CHART_BG)
    ax.tick_params(colors=TEXT_MUTED, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color(SPINE_COLOR)
    ax.grid(True, linestyle="--", alpha=0.5, color=GRID_COLOR)


def plot_scenario_comparison(results: List[Dict[str, Any]], output_file: str = "outputs/figures/scenario_comparison.png"):
    """
    Renders comparative bar charts with 95% Student's t Confidence Interval error bars.
    """
    names = [r["name"] for r in results]
    avg_waits = [r["avg_wait"] for r in results]
    ci_waits = [r.get("ci_wait_half_width", 0.0) for r in results]
    avg_totals = [r["avg_total"] for r in results]
    ci_totals = [r.get("ci_total_half_width", 0.0) for r in results]
    
    short_names = [(n[:16] + "...") if len(n) > 16 else n for n in names]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), facecolor=CHART_BG)
    colors = [COLOR_DANGER if i == 0 else COLOR_PRIMARY for i in range(len(names))]
    
    # 1. Anchorage Wait Time
    apply_dark_theme(fig, ax1)
    bars1 = ax1.bar(short_names, avg_waits, yerr=ci_waits, capsize=4, color=colors, edgecolor=SPINE_COLOR, alpha=0.9, linewidth=0.8)
    ax1.set_ylabel("Anchorage Waiting Time (hours)", fontsize=11, fontweight="600", color=TEXT_MAIN)
    ax1.set_title("Anchorage Waiting Time by Scenario\n(95% Student's t Confidence Intervals)", fontsize=12, fontweight="bold", color=TEXT_MAIN)
    ax1.tick_params(axis="x", rotation=25, labelsize=9, colors=TEXT_MUTED)
    for bar, val in zip(bars1, avg_waits):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 f"{val:.2f}h", ha="center", va="bottom", fontsize=9, fontweight="bold", color=TEXT_MAIN)
    
    # 2. Total Turnaround Time
    apply_dark_theme(fig, ax2)
    bars2 = ax2.bar(short_names, avg_totals, yerr=ci_totals, capsize=4, color=colors, edgecolor=SPINE_COLOR, alpha=0.9, linewidth=0.8)
    ax2.set_ylabel("Total Port Turnaround Time (hours)", fontsize=11, fontweight="600", color=TEXT_MAIN)
    ax2.set_title("Total Port Turnaround Time by Scenario\n(Arrival to Departure)", fontsize=12, fontweight="bold", color=TEXT_MAIN)
    ax2.tick_params(axis="x", rotation=25, labelsize=9, colors=TEXT_MUTED)
    for bar, val in zip(bars2, avg_totals):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
                 f"{val:.2f}h", ha="center", va="bottom", fontsize=9, fontweight="bold", color=TEXT_MAIN)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor=CHART_BG)
    plt.close()
    print(f"Saved: {output_file}")


def plot_wait_distribution(all_waits: List[float], output_file: str = "outputs/figures/wait_distribution.png"):
    """
    Renders histogram and empirical density of vessel waiting times in anchorage.
    """
    if not all_waits:
        return
        
    fig, ax = plt.subplots(figsize=(10, 6), facecolor=CHART_BG)
    apply_dark_theme(fig, ax)
    ax.hist(all_waits, bins=30, color=COLOR_PRIMARY, edgecolor=SPINE_COLOR, alpha=0.85, density=False)
    ax.set_xlabel("Anchorage Waiting Time (hours)", fontsize=11, fontweight="600", color=TEXT_MAIN)
    ax.set_ylabel("Vessel Count (Frequency)", fontsize=11, fontweight="600", color=TEXT_MAIN)
    ax.set_title("Distribution of Anchorage Waiting Times (Baseline Operations)", fontsize=13, fontweight="bold", color=TEXT_MAIN)
    
    mean_wait = sum(all_waits) / len(all_waits)
    ax.axvline(mean_wait, color=COLOR_DANGER, linestyle="--", linewidth=2.0,
               label=f"Sample Mean = {mean_wait:.2f} hours")
    ax.legend(fontsize=10, facecolor=CHART_BG, edgecolor=SPINE_COLOR, labelcolor=TEXT_MAIN)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor=CHART_BG)
    plt.close()
    print(f"Saved: {output_file}")


def plot_channel_density_and_utilization(results: List[Dict[str, Any]], output_file: str = "outputs/figures/channel_traffic_density.png"):
    """
    Visualizes River Channel Traffic Density & Wharf Utilization across scenarios (Objective #12).
    """
    names = [r["name"] for r in results]
    chan_utils = [r.get("channel_utilization", 0.0) * 100 for r in results]
    berth_utils = [r.get("berth_utilization", 0.0) * 100 for r in results]
    banca_utils = [r.get("banca_utilization", 0.0) * 100 for r in results]
    
    x = range(len(names))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(13, 6), facecolor=CHART_BG)
    apply_dark_theme(fig, ax)
    ax.bar([i - width for i in x], chan_utils, width=width, label="River Channel Traffic Utilization", color=COLOR_WARNING, edgecolor=SPINE_COLOR)
    ax.bar(x, berth_utils, width=width, label="Wharf Berth Utilization", color=COLOR_SUCCESS, edgecolor=SPINE_COLOR)
    ax.bar([i + width for i in x], banca_utils, width=width, label="Shuttle Banca Pool Utilization", color=COLOR_PRIMARY, edgecolor=SPINE_COLOR)
    
    ax.set_xticks(list(x))
    ax.set_xticklabels([(n[:16] + "...") if len(n) > 16 else n for n in names], rotation=25, fontsize=9, color=TEXT_MUTED)
    ax.set_ylabel("Resource Saturation / Utilization (%)", fontsize=11, fontweight="600", color=TEXT_MAIN)
    ax.set_title("Comparative Maritime Asset Utilization & Channel Density (Objective #12)", fontsize=13, fontweight="bold", color=TEXT_MAIN)
    ax.set_ylim(0, 105)
    ax.legend(fontsize=10, facecolor=CHART_BG, edgecolor=SPINE_COLOR, labelcolor=TEXT_MAIN)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor=CHART_BG)
    plt.close()
    print(f"Saved: {output_file}")


def plot_prng_lattice(points: List[tuple], output_file: str = "outputs/figures/prng_lattice.png"):
    """
    PRNG Spectral Test: Plots (U_i, U_{i+1}) 2D lattice structure
    demonstrating the uniformity and independence of the Lehmer LCG (M31 = 2^31 - 1, a = 16807).
    """
    fig, ax = plt.subplots(figsize=(8, 8), facecolor=CHART_BG)
    apply_dark_theme(fig, ax)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    
    ax.scatter(xs, ys, s=4, color="#38BDF8", alpha=0.6)
    ax.set_xlabel("Uniform Variate U_i", fontsize=11, fontweight="600", color=TEXT_MAIN)
    ax.set_ylabel("Uniform Variate U_{i+1}", fontsize=11, fontweight="600", color=TEXT_MAIN)
    ax.set_title("PRNG Uniformity Verification: 2D Spectral Lattice\nLehmer MCG (a = 16807, m = 2^31 - 1)", fontsize=13, fontweight="bold", color=TEXT_MAIN)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor=CHART_BG)
    plt.close()
    print(f"Saved: {output_file}")
