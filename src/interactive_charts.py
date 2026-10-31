# src/interactive_charts.py
"""
Interactive Plotly Visualization Suite for Mercedes Fish Port Simulation.
Engineered for modern dark-theme Streamlit dashboards:
- High contrast, WCAG 2.1 AA compliant color palette
- Responsive layout with touch and hover tooltips
- Interactive zoom, pan, and hover telemetry
"""

from typing import List, Dict, Any, Tuple
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# High-Contrast Dark Theme Palette
DARK_BG = "#0B0F19"
SURFACE_BG = "#111827"
BORDER_COLOR = "#334155"
TEXT_COLOR = "#F8FAFC"
MUTED_TEXT = "#94A3B8"
GRID_COLOR = "rgba(255, 255, 255, 0.06)"

BLUE_ACCENT = "#38BDF8"
EMERALD_ACCENT = "#34D399"
AMBER_ACCENT = "#FBBF24"
ROSE_ACCENT = "#F87171"
PURPLE_ACCENT = "#A78BFA"


def _apply_dark_layout(fig: go.Figure, height: int = 340, title: str = "") -> go.Figure:
    """Applies standardized dark theme layout across all Plotly figures."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family="Inter, sans-serif", size=14, color=TEXT_COLOR),
            x=0.01,
            y=0.96
        ) if title else None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=SURFACE_BG,
        height=height,
        margin=dict(l=40, r=20, t=40 if title else 20, b=40),
        font=dict(family="Inter, sans-serif", color=TEXT_COLOR, size=11),
        legend=dict(
            bgcolor="rgba(17, 24, 39, 0.8)",
            bordercolor=BORDER_COLOR,
            borderwidth=1,
            font=dict(size=10, color=TEXT_COLOR)
        ),
        hoverlabel=dict(
            bgcolor=SURFACE_BG,
            bordercolor=BLUE_ACCENT,
            font=dict(family="Inter, sans-serif", size=12, color=TEXT_COLOR)
        ),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=BORDER_COLOR,
            tickfont=dict(color=MUTED_TEXT, size=10),
            titlefont=dict(color=MUTED_TEXT, size=11),
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=BORDER_COLOR,
            tickfont=dict(color=MUTED_TEXT, size=10),
            titlefont=dict(color=MUTED_TEXT, size=11),
        )
    )
    return fig


def plot_interactive_wait_histogram(wait_times: List[float], mean_wait: float) -> go.Figure:
    """Interactive histogram of anchorage waiting times with mean and p90 lines."""
    if not wait_times:
        wait_times = [0.0]

    p90_wait = float(np.percentile(wait_times, 90))

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=wait_times,
        nbinsx=28,
        marker=dict(
            color=BLUE_ACCENT,
            opacity=0.85,
            line=dict(color="#0284C7", width=1)
        ),
        hovertemplate="Wait: %{x:.2f}h<br>Vessel Count: %{y}<extra></extra>",
        name="Vessels"
    ))

    # Mean Wait Vertical Line
    fig.add_vline(
        x=mean_wait,
        line_width=2,
        line_dash="dash",
        line_color=ROSE_ACCENT,
        annotation_text=f"Mean: {mean_wait:.2f}h",
        annotation_position="top right",
        annotation_font=dict(color=ROSE_ACCENT, size=10)
    )

    # 90th Percentile Vertical Line
    fig.add_vline(
        x=p90_wait,
        line_width=1.5,
        line_dash="dot",
        line_color=AMBER_ACCENT,
        annotation_text=f"P90: {p90_wait:.2f}h",
        annotation_position="top left",
        annotation_font=dict(color=AMBER_ACCENT, size=10)
    )

    fig.update_xaxes(title_text="Anchorage Waiting Time (Hours)")
    fig.update_yaxes(title_text="Vessel Arrivals")
    return _apply_dark_layout(fig, height=330, title="Anchorage Waiting Time Distribution")


def plot_interactive_mode_donut(direct_count: int, lighter_count: int) -> go.Figure:
    """Interactive donut chart for vessel landing mode breakdown."""
    total = direct_count + lighter_count
    if total == 0:
        direct_count, lighter_count = 1, 1

    labels = ["Direct Wharf Landing", "Anchorage Lightering"]
    values = [direct_count, lighter_count]
    colors = [EMERALD_ACCENT, BLUE_ACCENT]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.58,
        marker=dict(colors=colors, line=dict(color=SURFACE_BG, width=2)),
        textinfo="percent+label",
        textfont=dict(color=TEXT_COLOR, size=11),
        hovertemplate="<b>%{label}</b><br>Vessels: %{value} (%{percent})<extra></extra>"
    )])

    fig.update_layout(
        annotations=[dict(
            text=f"<b>{total}</b><br><span style='font-size:10px; color:#94A3B8'>Total</span>",
            x=0.5, y=0.5,
            font=dict(size=14, color=TEXT_COLOR),
            showarrow=False
        )],
        showlegend=False
    )
    return _apply_dark_layout(fig, height=330, title="Landing Workflow Mode Breakdown")


def plot_interactive_scenario_comparison(scenario_results: List[Dict[str, Any]]) -> go.Figure:
    """Interactive bar chart comparing average waiting times with 95% Confidence Intervals."""
    names = [r["name"] for r in scenario_results]
    waits = [r["avg_wait"] for r in scenario_results]
    errs = [r.get("ci_wait_half_width", 0.0) for r in scenario_results]
    turnarounds = [r.get("avg_total", 0.0) for r in scenario_results]
    throughputs = [r.get("avg_completed", 0.0) for r in scenario_results]

    # Color highlights: Baseline is slate/neutral, Master Strategy is vibrant emerald, others blue/amber
    colors = []
    for n in names:
        if "Master" in n:
            colors.append(EMERALD_ACCENT)
        elif "Baseline" in n:
            colors.append(MUTED_TEXT)
        elif "Scheduling" in n:
            colors.append(BLUE_ACCENT)
        else:
            colors.append(AMBER_ACCENT)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=names,
        y=waits,
        error_y=dict(
            type="data",
            array=errs,
            visible=True,
            color=TEXT_COLOR,
            thickness=1.5,
            width=5
        ),
        marker=dict(
            color=colors,
            line=dict(color=BORDER_COLOR, width=1)
        ),
        customdata=np.stack((turnarounds, throughputs, errs), axis=-1),
        hovertemplate=(
            "<b>%{x}</b><br>"
            + "Mean Wait: %{y:.2f} ± %{customdata[2]:.2f} hrs<br>"
            + "Turnaround: %{customdata[0]:.2f} hrs<br>"
            + "Weekly Throughput: %{customdata[1]:.0f} vessels<extra></extra>"
        ),
        name="Mean Wait Time"
    ))

    fig.update_xaxes(tickangle=-15, title_text="")
    fig.update_yaxes(title_text="Anchorage Waiting Time (Hours)")
    return _apply_dark_layout(fig, height=360, title="Comparative Mean Anchorage Wait with 95% Student's t CI")


def plot_interactive_economics_comparison(cb_results: List[Dict[str, Any]]) -> go.Figure:
    """Interactive grouped bar chart comparing Gross Savings, Implementation Costs, and Net Economic Benefits."""
    names = [c["name"] for c in cb_results]
    savings = [c["gross_weekly_savings_php"] for c in cb_results]
    costs = [c["incremental_weekly_cost_php"] for c in cb_results]
    nets = [c["net_weekly_benefit_php"] for c in cb_results]
    bcrs = [c["benefit_cost_ratio"] for c in cb_results]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Gross Savings (Delay & Spoilage Avoided)",
        x=names,
        y=savings,
        marker=dict(color=BLUE_ACCENT),
        hovertemplate="Gross Savings: PHP %{y:,.0f}/week<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        name="Incremental Cost (CAPEX + OPEX)",
        x=names,
        y=costs,
        marker=dict(color=ROSE_ACCENT),
        hovertemplate="Implementation Cost: PHP %{y:,.0f}/week<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        name="Net Economic Benefit",
        x=names,
        y=nets,
        marker=dict(color=EMERALD_ACCENT),
        customdata=bcrs,
        hovertemplate="<b>Net Benefit: PHP %{y:,.0f}/week</b><br>BCR: %{customdata:.2f}<extra></extra>"
    ))

    fig.update_layout(barmode="group")
    fig.update_xaxes(tickangle=-15)
    fig.update_yaxes(title_text="Economic Value (PHP / Week)")
    return _apply_dark_layout(fig, height=380, title="Weekly Cost-Benefit & Economic Surplus Analysis (PHP)")


def plot_interactive_fish_perishability_curve(cargo_banyeras: int = 150,
                                              price_per_banyera: float = 2500.0,
                                              decay_rate: float = 0.035,
                                              diesel_cost_per_hr: float = 350.0,
                                              ice_cost_per_hr: float = 150.0) -> go.Figure:
    """Interactive curve showing exponential fish spoilage, fuel idling, and ice losses over delay hours."""
    hours = np.linspace(0, 16, 100)
    gross_value = cargo_banyeras * price_per_banyera

    spoilage = gross_value * (1.0 - np.exp(-decay_rate * hours))
    fuel = hours * diesel_cost_per_hr
    ice = hours * ice_cost_per_hr
    total_loss = spoilage + fuel + ice
    remaining_value = gross_value - spoilage

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=hours,
        y=remaining_value,
        mode="lines",
        name="Residual Cargo Market Value",
        line=dict(color=EMERALD_ACCENT, width=2.5),
        hovertemplate="Delay: %{x:.1f}h<br>Remaining Cargo Value: PHP %{y:,.0f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=hours,
        y=total_loss,
        mode="lines",
        name="Cumulative Congestion Penalty",
        line=dict(color=ROSE_ACCENT, width=2.5, dash="dash"),
        hovertemplate="Delay: %{x:.1f}h<br>Cumulative Loss: PHP %{y:,.0f}<extra></extra>"
    ))

    # Grade Threshold Vertical Lines
    fig.add_vline(x=3.0, line_dash="dot", line_color=AMBER_ACCENT, line_width=1,
                  annotation_text="Grade B Discount (~3h)", annotation_position="top left",
                  annotation_font=dict(color=AMBER_ACCENT, size=9))
    fig.add_vline(x=6.0, line_dash="dot", line_color=ROSE_ACCENT, line_width=1,
                  annotation_text="Grade C / Industrial (~6h)", annotation_position="top left",
                  annotation_font=dict(color=ROSE_ACCENT, size=9))

    fig.update_xaxes(title_text="Anchorage Delay (Hours)")
    fig.update_yaxes(title_text="Catch Financial Value (PHP)")
    return _apply_dark_layout(fig, height=340, title=f"Post-Harvest Quality Depreciation Curve ({cargo_banyeras} Banyeras)")


def plot_interactive_lattice(pairs: List[Tuple[float, float]]) -> go.Figure:
    """Interactive 2D spectral lattice test scatter for Lehmer PRNG."""
    u_i = [p[0] for p in pairs]
    u_next = [p[1] for p in pairs]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=u_i,
        y=u_next,
        mode="markers",
        marker=dict(
            size=4,
            color=BLUE_ACCENT,
            opacity=0.65
        ),
        hovertemplate="U_i: %{x:.4f}<br>U_{i+1}: %{y:.4f}<extra></extra>"
    ))

    fig.update_xaxes(title_text="Uniform Variate U_i", range=[0, 1])
    fig.update_yaxes(title_text="Uniform Variate U_{i+1}", range=[0, 1])
    return _apply_dark_layout(fig, height=340, title="2D Spectral Lattice Structure (Marsaglia Hyperplane Test)")
