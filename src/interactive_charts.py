# src/interactive_charts.py
"""
Interactive Plotly Visualization Suite for Mercedes Fish Port Simulation.
Engineered for modern dark-theme Streamlit dashboards:
- High contrast, WCAG 2.1 AA compliant color palette (Deep Harbor Design Tokens)
- Responsive layout with touch and hover tooltips
- Interactive zoom, pan, and hover telemetry
- Plotly 6/7+ compliant without deprecated axis properties
"""

from typing import List, Dict, Any, Tuple
import numpy as np
import plotly.graph_objects as go

# Deep Harbor Design Tokens
DARK_BG = "#080C14"
SURFACE_BG = "#0F172A"
SURFACE_ELEV = "#1E293B"
BORDER_COLOR = "rgba(255, 255, 255, 0.08)"
TEXT_COLOR = "#F8FAFC"
MUTED_TEXT = "#94A3B8"
GRID_COLOR = "rgba(255, 255, 255, 0.04)"

ACCENT_CYAN = "#38BDF8"
ACCENT_EMERALD = "#34D399"
ACCENT_AMBER = "#FBBF24"
ACCENT_ROSE = "#F87171"
ACCENT_PURPLE = "#A78BFA"


def _apply_dark_layout(fig: go.Figure, height: int = 340, title: str = "") -> go.Figure:
    """Applies standardized dark theme layout across all Plotly figures."""
    fig.update_layout(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(family="Inter, -apple-system, sans-serif", size=13, color=TEXT_COLOR),
            x=0.01,
            y=0.96
        ) if title else None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=SURFACE_BG,
        height=height,
        margin=dict(l=45, r=25, t=44 if title else 20, b=42),
        font=dict(family="Inter, -apple-system, sans-serif", color=TEXT_COLOR, size=11),
        legend=dict(
            bgcolor="rgba(15, 23, 42, 0.85)",
            bordercolor=BORDER_COLOR,
            borderwidth=1,
            font=dict(size=10, color=TEXT_COLOR)
        ),
        hoverlabel=dict(
            bgcolor=SURFACE_ELEV,
            bordercolor=ACCENT_CYAN,
            font=dict(family="Inter, -apple-system, sans-serif", size=12, color=TEXT_COLOR)
        ),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=BORDER_COLOR,
            tickfont=dict(color=MUTED_TEXT, size=10),
            title_font=dict(color=MUTED_TEXT, size=11),
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            zerolinecolor=BORDER_COLOR,
            tickfont=dict(color=MUTED_TEXT, size=10),
            title_font=dict(color=MUTED_TEXT, size=11),
        )
    )
    return fig


def plot_interactive_wait_histogram(wait_times: List[float], mean_wait: float) -> go.Figure:
    """Interactive histogram of anchorage waiting times with mean, p90, and Grade A window."""
    if not wait_times:
        wait_times = [0.0]

    p90_wait = float(np.percentile(wait_times, 90))

    fig = go.Figure()
    
    # Grade A Prime Holding Window Background (0 to 3 hours)
    fig.add_vrect(
        x0=0,
        x1=3.0,
        fillcolor="rgba(16, 185, 129, 0.08)",
        layer="below",
        line_width=0,
        annotation_text="Prime Grade-A Window (≤3h)",
        annotation_position="top left",
        annotation_font=dict(color=ACCENT_EMERALD, size=9)
    )

    fig.add_trace(go.Histogram(
        x=wait_times,
        nbinsx=28,
        marker=dict(
            color=ACCENT_CYAN,
            opacity=0.85,
            line=dict(color="#0284C7", width=1)
        ),
        hovertemplate="Wait Range: %{x:.2f}h<br>Vessel Count: %{y}<extra></extra>",
        name="Vessels"
    ))

    # Mean Wait Vertical Line
    fig.add_vline(
        x=mean_wait,
        line_width=2,
        line_dash="dash",
        line_color=ACCENT_ROSE,
        annotation_text=f"Mean: {mean_wait:.2f}h",
        annotation_position="top right",
        annotation_font=dict(color=ACCENT_ROSE, size=10)
    )

    # 90th Percentile Vertical Line
    fig.add_vline(
        x=p90_wait,
        line_width=1.5,
        line_dash="dot",
        line_color=ACCENT_AMBER,
        annotation_text=f"P90: {p90_wait:.2f}h",
        annotation_position="top left",
        annotation_font=dict(color=ACCENT_AMBER, size=10)
    )

    fig.update_xaxes(title_text="Anchorage Waiting Time (Hours)")
    fig.update_yaxes(title_text="Vessel Arrivals")
    return _apply_dark_layout(fig, height=330, title="Anchorage Waiting Time Distribution & Grade-A Window")


def plot_interactive_mode_donut(direct_count: int, lighter_count: int) -> go.Figure:
    """Interactive donut chart for vessel landing mode breakdown with center total."""
    total = direct_count + lighter_count
    if total == 0:
        direct_count, lighter_count = 1, 1

    labels = ["Direct Wharf Landing", "Anchorage Lightering"]
    values = [direct_count, lighter_count]
    colors = [ACCENT_EMERALD, ACCENT_CYAN]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.62,
        marker=dict(colors=colors, line=dict(color=SURFACE_BG, width=2)),
        textinfo="percent+label",
        textfont=dict(color=TEXT_COLOR, size=11),
        hovertemplate="<b>%{label}</b><br>Vessels: %{value} (%{percent})<extra></extra>"
    )])

    fig.update_layout(
        annotations=[dict(
            text=f"<span style='font-size:20px; font-weight:700; color:{TEXT_COLOR}'>{total}</span><br><span style='font-size:11px; color:{MUTED_TEXT}'>Vessels</span>",
            x=0.5, y=0.5,
            showarrow=False
        )],
        showlegend=False
    )
    return _apply_dark_layout(fig, height=330, title="Vessel Landing Workflow Distribution")


def plot_interactive_scenario_comparison(scenario_results: List[Dict[str, Any]]) -> go.Figure:
    """Interactive bar chart comparing average waiting times with direct data labels and 95% CIs."""
    names = [r["name"] for r in scenario_results]
    waits = [r["avg_wait"] for r in scenario_results]
    errs = [r.get("ci_wait_half_width", 0.0) for r in scenario_results]
    turnarounds = [r.get("avg_total", 0.0) for r in scenario_results]
    throughputs = [r.get("avg_completed", 0.0) for r in scenario_results]

    colors = []
    for n in names:
        if "Master" in n:
            colors.append(ACCENT_EMERALD)
        elif "Baseline" in n:
            colors.append(MUTED_TEXT)
        elif "Scheduling" in n:
            colors.append(ACCENT_CYAN)
        else:
            colors.append(ACCENT_AMBER)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=names,
        y=waits,
        text=[f"{w:.2f}h" for w in waits],
        textposition="outside",
        textfont=dict(color=TEXT_COLOR, size=10),
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
            + "Throughput: %{customdata[1]:.0f} vessels<extra></extra>"
        ),
        name="Mean Wait Time"
    ))

    # Horizontal target line: Maximum safe dwell before ice melt & quality loss (4.0h)
    fig.add_hline(
        y=4.0,
        line_dash="dot",
        line_color=ACCENT_AMBER,
        line_width=1.5,
        annotation_text="Safe Quality Threshold (4.0h)",
        annotation_position="top left",
        annotation_font=dict(color=ACCENT_AMBER, size=10)
    )

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
        name="Gross Savings (Delay Avoided)",
        x=names,
        y=savings,
        marker=dict(color=ACCENT_CYAN),
        hovertemplate="Gross Savings: PHP %{y:,.0f}/wk<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        name="Added Cost (CAPEX + OPEX)",
        x=names,
        y=costs,
        marker=dict(color=ACCENT_ROSE),
        hovertemplate="Added Cost: PHP %{y:,.0f}/wk<extra></extra>"
    ))

    fig.add_trace(go.Bar(
        name="Net Economic Benefit",
        x=names,
        y=nets,
        marker=dict(color=ACCENT_EMERALD),
        customdata=bcrs,
        hovertemplate="<b>Net Benefit: PHP %{y:,.0f}/wk</b><br>BCR: %{customdata:.2f}<extra></extra>"
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
    """Interactive curve showing quality degradation across Grade A, B, and C holding zones."""
    hours = np.linspace(0, 16, 100)
    gross_value = cargo_banyeras * price_per_banyera

    spoilage = gross_value * (1.0 - np.exp(-decay_rate * hours))
    fuel = hours * diesel_cost_per_hr
    ice = hours * ice_cost_per_hr
    total_loss = spoilage + fuel + ice
    remaining_value = gross_value - spoilage

    fig = go.Figure()

    # Zone 1 (0 to 3 Hours): Grade-A Prime Catch
    fig.add_vrect(
        x0=0, x1=3.0,
        fillcolor="rgba(16, 185, 129, 0.08)",
        layer="below", line_width=0,
        annotation_text="Grade-A Prime (0–3h)",
        annotation_position="top left",
        annotation_font=dict(color=ACCENT_EMERALD, size=9)
    )

    # Zone 2 (3 to 6 Hours): Grade-B Commercial Discount
    fig.add_vrect(
        x0=3.0, x1=6.0,
        fillcolor="rgba(245, 158, 11, 0.08)",
        layer="below", line_width=0,
        annotation_text="Grade-B Discount (3–6h)",
        annotation_position="top left",
        annotation_font=dict(color=ACCENT_AMBER, size=9)
    )

    # Zone 3 (> 6 Hours): Grade-C Industrial Devaluation
    fig.add_vrect(
        x0=6.0, x1=16.0,
        fillcolor="rgba(239, 68, 68, 0.08)",
        layer="below", line_width=0,
        annotation_text="Grade-C / Industrial (>6h)",
        annotation_position="top left",
        annotation_font=dict(color=ACCENT_ROSE, size=9)
    )

    fig.add_trace(go.Scatter(
        x=hours,
        y=remaining_value,
        mode="lines",
        name="Residual Cargo Market Value",
        line=dict(color=ACCENT_EMERALD, width=2.5),
        hovertemplate="Delay: %{x:.1f}h<br>Remaining Cargo Value: PHP %{y:,.0f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=hours,
        y=total_loss,
        mode="lines",
        name="Cumulative Congestion Loss",
        line=dict(color=ACCENT_ROSE, width=2.5, dash="dash"),
        hovertemplate="Delay: %{x:.1f}h<br>Cumulative Loss: PHP %{y:,.0f}<extra></extra>"
    ))

    fig.update_xaxes(title_text="Anchorage Delay (Hours)", range=[0, 16])
    fig.update_yaxes(title_text="Catch Financial Value (PHP)")
    return _apply_dark_layout(fig, height=350, title=f"Post-Harvest Quality Depreciation Curve ({cargo_banyeras} Banyeras)")


def plot_interactive_lattice(pairs: List[Tuple[float, float]]) -> go.Figure:
    """Interactive 2D spectral lattice test scatter for Lehmer PRNG with 1:1 square aspect ratio."""
    u_i = [p[0] for p in pairs]
    u_next = [p[1] for p in pairs]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=u_i,
        y=u_next,
        mode="markers",
        marker=dict(
            size=4,
            color=ACCENT_CYAN,
            opacity=0.65
        ),
        hovertemplate="U_i: %{x:.4f}<br>U_{i+1}: %{y:.4f}<extra></extra>"
    ))

    fig.update_xaxes(title_text="Uniform Variate U_i", range=[0, 1])
    fig.update_yaxes(title_text="Uniform Variate U_{i+1}", range=[0, 1], scaleanchor="x", scaleratio=1)
    return _apply_dark_layout(fig, height=350, title="2D Spectral Lattice Structure (Marsaglia Hyperplane Test)")
