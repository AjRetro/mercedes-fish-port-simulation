# src/port_3d_engine.py
"""
Interactive 3D Discrete-Event Simulation (DES) Digital Twin Engine
for Mercedes Fish Port, Mercedes, Camarines Norte.

Architectural Standards Applied from Agency Agents Skills:
- C:/Users/L470/.gemini/config/skills/agency-frontend-developer/SKILL.md: Non-holonomic 3-DOF kinematics, 60fps budget, zero console errors.
- C:/Users/L470/.gemini/config/skills/agency-3d-scene-developer/SKILL.md: Infinite-thickness half-space collision, rock-steady pier mooring, clean breakwaters.
- C:/Users/L470/.gemini/config/skills/agency-ux-architect/SKILL.md: Zero-clutter viewport, progressive disclosure modal hierarchy.
- C:/Users/L470/.gemini/config/skills/agency-ui-designer/SKILL.md: High-contrast maritime design tokens, WCAG AA compliance.

Core Mathematical & Spatial Systems:
1. 13-Berth Clean Concrete Wharf Apron: X = -75.0 to -35.0, Z = -105.0 to +105.0. Front wharf face at X = -35.0, berths at X = -28.0.
2. Rock-Steady Pier Mooring (Zero Shaking): Collision pushback completely disabled during DOCKED_UNLOADING.
3. Rapid 15–35s Real-Time Catch Unloading: Skewed banyera hauls (Light: 14s, Med: 24s, Heavy: 35s) with guaranteed per-frame countdown.
4. Infinite-Thickness Half-Space Wall Clamping: Impossible for vessels to tunnel or clip into wharf or seawalls.
5. Dual-Role Small Boat Fleet: 70% Partner Lightering Tenders (servicing bay anchorage) + 30% Independent Artisanal Bancas.
6. Medium Vessel Dynamics: 60% Direct Wharf Docking vs 40% Convenience Bay Anchorage with tender pickup.
"""

def generate_3d_digital_twin_html() -> str:
    """Generates the self-contained, 100% full-screen 3D WebGL Digital Twin HTML page."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Mercedes Fish Port — 3D DES Digital Twin</title>
<!-- Google Fonts: Inter & JetBrains Mono -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
<!-- Three.js and OrbitControls -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>

<style>
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        user-select: none;
        -webkit-user-select: none;
    }
    html, body {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: #060C18;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #F8FAFC;
    }

    #webgl-canvas {
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
        display: block;
    }

    .glass-panel {
        background: rgba(11, 20, 38, 0.82);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.55);
        border-radius: 10px;
    }

    #hud-top {
        position: absolute;
        top: 14px;
        left: 14px;
        right: 14px;
        z-index: 10;
        display: flex;
        align-items: center;
        justify-content: space-between;
        pointer-events: none;
        gap: 12px;
    }
    .hud-group {
        display: flex;
        align-items: center;
        gap: 8px;
        pointer-events: auto;
    }

    .title-pill {
        display: inline-flex;
        align-items: center;
        gap: 9px;
        padding: 8px 14px;
    }
    .title-icon {
        width: 18px;
        height: 18px;
        color: #38BDF8;
    }
    .title-text {
        font-size: 0.88rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.01em;
    }
    .scenario-pill {
        font-size: 0.72rem;
        font-weight: 600;
        padding: 3px 9px;
        border-radius: 9999px;
        background: rgba(56, 189, 248, 0.15);
        border: 1px solid rgba(56, 189, 248, 0.35);
        color: #38BDF8;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .clock-pill {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 7px 14px;
    }
    .hud-clock {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.15rem;
        font-weight: 700;
        color: #38BDF8;
        letter-spacing: 0.05em;
        font-variant-numeric: tabular-nums;
    }
    .surge-pill {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 3px 10px;
        border-radius: 9999px;
        background: rgba(245, 158, 11, 0.18);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
        display: none;
        align-items: center;
        gap: 5px;
        animation: pulse-amber 1.4s infinite alternate;
    }
    @keyframes pulse-amber {
        0% { box-shadow: 0 0 4px rgba(245, 158, 11, 0.2); }
        100% { box-shadow: 0 0 14px rgba(245, 158, 11, 0.75); }
    }
    .tide-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 9999px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34D399;
        font-family: 'JetBrains Mono', monospace;
    }
    .tide-pill.low {
        background: rgba(239, 68, 68, 0.15);
        border-color: rgba(239, 68, 68, 0.35);
        color: #F87171;
    }

    .btn-hud {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #E2E8F0;
        padding: 7px 12px;
        border-radius: 7px;
        font-size: 0.75rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.15s ease;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .btn-hud:hover {
        background: rgba(56, 189, 248, 0.15);
        border-color: #38BDF8;
        color: #FFFFFF;
        transform: translateY(-1px);
    }
    .btn-hud.primary {
        background: #0284C7;
        border-color: #38BDF8;
        color: #FFFFFF;
    }
    .btn-hud.primary:hover {
        background: #0369A1;
    }
    .btn-hud.active {
        background: rgba(56, 189, 248, 0.25);
        border-color: #38BDF8;
        color: #38BDF8;
    }

    #hud-bottom-left {
        position: absolute;
        bottom: 14px;
        left: 14px;
        z-index: 10;
        display: flex;
        flex-direction: column;
        gap: 7px;
        pointer-events: none;
        max-width: 420px;
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 7px;
    }
    .kpi-card {
        padding: 9px 12px;
        display: flex;
        flex-direction: column;
        gap: 3px;
        pointer-events: auto;
    }
    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .kpi-title {
        font-size: 0.65rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .kpi-sub {
        font-size: 0.68rem;
        color: #64748B;
    }

    #hud-bottom-center {
        position: absolute;
        bottom: 14px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10;
        pointer-events: none;
    }
    .hint-pill {
        padding: 6px 14px;
        font-size: 0.72rem;
        color: #94A3B8;
        display: flex;
        align-items: center;
        gap: 12px;
        pointer-events: auto;
    }

    #vessel-tooltip {
        position: absolute;
        display: none;
        pointer-events: none;
        z-index: 50;
        padding: 11px 14px;
        width: 280px;
        transform: translate(16px, 16px);
        transition: opacity 0.15s ease;
    }
    .tt-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 7px;
        padding-bottom: 5px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .tt-name {
        font-size: 0.85rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .tt-badge {
        font-size: 0.62rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .tt-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.72rem;
        margin-bottom: 4px;
        color: #CBD5E1;
    }
    .tt-label {
        color: #94A3B8;
    }
    .tt-val {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
    }
    .cargo-bar-bg {
        width: 100%;
        height: 6px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 3px;
        overflow: hidden;
        margin-top: 5px;
    }
    .cargo-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #38BDF8, #34D399);
        width: 0%;
        transition: width 0.3s ease;
    }

    .modal-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(3, 7, 18, 0.78);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        z-index: 100;
        display: none;
        align-items: center;
        justify-content: center;
    }
    .modal-window {
        width: 90%;
        max-width: 680px;
        max-height: 85vh;
        overflow-y: auto;
        padding: 24px;
        display: flex;
        flex-direction: column;
        gap: 18px;
    }
    .modal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .modal-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 9px;
    }
    .modal-close {
        background: transparent;
        border: none;
        color: #94A3B8;
        font-size: 1.3rem;
        cursor: pointer;
        padding: 4px 8px;
        line-height: 1;
    }
    .modal-close:hover {
        color: #F8FAFC;
    }
    .modal-tabs {
        display: flex;
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 8px;
    }
    .modal-tab-btn {
        background: transparent;
        border: none;
        color: #94A3B8;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 6px;
        cursor: pointer;
    }
    .modal-tab-btn.active {
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
    }
    .tab-content {
        display: none;
    }
    .tab-content.active {
        display: block;
    }

    .param-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .param-info {
        max-width: 60%;
    }
    .param-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #F1F5F9;
    }
    .param-desc {
        font-size: 0.7rem;
        color: #64748B;
        margin-top: 2px;
    }
    .param-ctrl {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .param-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        font-weight: 700;
        color: #38BDF8;
        min-width: 65px;
        text-align: right;
    }

    .preset-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 10px;
    }
    .preset-card {
        padding: 12px;
        border-radius: 8px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        cursor: pointer;
        transition: all 0.15s ease;
    }
    .preset-card:hover {
        border-color: #38BDF8;
        background: rgba(56, 189, 248, 0.08);
    }
    .preset-card.active {
        border-color: #38BDF8;
        background: rgba(56, 189, 248, 0.15);
    }
    .preset-name {
        font-size: 0.82rem;
        font-weight: 700;
        color: #F8FAFC;
        margin-bottom: 4px;
    }
    .preset-desc {
        font-size: 0.68rem;
        color: #94A3B8;
        line-height: 1.35;
    }
    .preset-tag {
        font-size: 0.6rem;
        font-weight: 700;
        color: #38BDF8;
        text-transform: uppercase;
        margin-bottom: 4px;
        display: block;
    }

    .table-container {
        width: 100%;
        overflow-x: auto;
        margin-top: 12px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.72rem;
    }
    th {
        text-align: left;
        padding: 8px 10px;
        background: rgba(255, 255, 255, 0.03);
        color: #94A3B8;
        font-weight: 600;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    td {
        padding: 8px 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        color: #E2E8F0;
    }

    body.screenshot-mode #hud-top,
    body.screenshot-mode #hud-bottom-left,
    body.screenshot-mode #hud-bottom-center,
    body.screenshot-mode #vessel-tooltip {
        display: none !important;
    }
    body.screenshot-mode #screenshot-restore-btn {
        display: block !important;
    }
    #screenshot-restore-btn {
        display: none;
        position: absolute;
        top: 14px;
        right: 14px;
        z-index: 999;
    }
</style>
</head>
<body>

<canvas id="webgl-canvas"></canvas>

<button id="screenshot-restore-btn" class="btn-hud primary">✕ Exit Screenshot Mode</button>

<!-- Top Floating HUD -->
<div id="hud-top">
    <div class="hud-group">
        <div class="glass-panel title-pill">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="5" r="3"/>
                <line x1="12" y1="22" x2="12" y2="8"/>
                <path d="M5 12H2a10 10 0 0 0 20 0h-3"/>
            </svg>
            <span class="title-text">Mercedes Fish Port — 3D DES Digital Twin</span>
            <span id="badge-scenario" class="scenario-pill">Baseline (13 Berths)</span>
        </div>

        <div class="glass-panel clock-pill">
            <span id="hud-clock" class="hud-clock">05:45 AM</span>
            <span id="surge-pill" class="surge-pill">⚡ BULUNGAN AUCTION SURGE</span>
            <span id="tide-pill" class="tide-pill">HIGH TIDE: Open (+2.10m)</span>
        </div>
    </div>

    <div class="hud-group">
        <button id="btn-play" class="btn-hud primary">⏸ Pause</button>
        <button class="btn-hud speed-btn active" data-speed="1">1x</button>
        <button class="btn-hud speed-btn" data-speed="2">2x</button>
        <button class="btn-hud speed-btn" data-speed="5">5x</button>
        <button id="btn-reset" class="btn-hud">↺ Reset</button>
        <button id="btn-open-settings" class="btn-hud">⚙️ Simulation Settings</button>
        <button id="btn-open-analytics" class="btn-hud">📊 Analytics & Report</button>
    </div>
</div>

<!-- Bottom-Left Live KPI Strip -->
<div id="hud-bottom-left">
    <div class="kpi-grid">
        <div class="glass-panel kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Anchorage Queue</span>
                <span id="kpi-queue-status" style="font-size:0.6rem; color:#FBBF24;">San Miguel Bay</span>
            </div>
            <div class="kpi-value"><span id="kpi-queue-count">0</span> <span style="font-size:0.75rem; color:#94A3B8;">craft</span></div>
            <div class="kpi-sub">Distant Wait: <span id="kpi-wait-time">0.00</span> hrs</div>
        </div>

        <div class="glass-panel kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Wharf Apron</span>
                <span id="kpi-berth-status" style="font-size:0.6rem; color:#34D399;">Medium Vessels</span>
            </div>
            <div class="kpi-value"><span id="kpi-berth-util">0.0</span><span style="font-size:0.75rem; color:#94A3B8;">%</span></div>
            <div class="kpi-sub"><span id="kpi-berth-occ">0</span> / <span id="kpi-berth-total">13</span> Medium Berths Occupied</div>
        </div>

        <div class="glass-panel kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Fleet Telemetry</span>
                <span style="font-size:0.6rem; color:#38BDF8;">Medium & Bancas</span>
            </div>
            <div class="kpi-value"><span id="kpi-at-sea-count">16</span> <span style="font-size:0.75rem; color:#94A3B8;">at sea fishing</span></div>
            <div class="kpi-sub"><span id="kpi-bancas-active" style="color:#FBBF24; font-weight:700;">0</span> Active Lightering | <span id="kpi-bancas-moored">32</span> Standby</div>
        </div>

        <div class="glass-panel kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Banyera Landed</span>
                <span style="font-size:0.6rem; color:#34D399;">Wholesale</span>
            </div>
            <div class="kpi-value"><span id="kpi-crates-count" style="color:#34D399;">1,420</span></div>
            <div class="kpi-sub">Freshness: <span id="kpi-quality-score">96.4</span>% Retention</div>
        </div>
    </div>
</div>

<div id="hud-bottom-center">
    <div class="glass-panel hint-pill">
        <span>🖱️ Orbit: Left-Drag</span>
        <span style="opacity:0.4;">|</span>
        <span>Pan: Right-Drag</span>
        <span style="opacity:0.4;">|</span>
        <span>Zoom: Scroll</span>
    </div>
</div>

<!-- Vessel Hover Tooltip -->
<div id="vessel-tooltip" class="glass-panel">
    <div class="tt-header">
        <span id="tt-vessel-name" class="tt-name">MV-MercedesQueen</span>
        <span id="tt-vessel-badge" class="tt-badge" style="background:rgba(56,189,248,0.2); color:#38BDF8;">Direct Docked</span>
    </div>
    <div class="tt-row">
        <span class="tt-label">Vessel Class:</span>
        <span id="tt-vessel-type" class="tt-val">Purse Seiner</span>
    </div>
    <div class="tt-row">
        <span class="tt-label">Gross Tonnage / Draft:</span>
        <span class="tt-val"><span id="tt-vessel-gt">24.5 GT</span> / <span id="tt-vessel-draft">2.1m</span></span>
    </div>
    <div class="tt-row">
        <span class="tt-label">Remaining Catch:</span>
        <span id="tt-vessel-cargo" class="tt-val">180 / 180 banyeras</span>
    </div>
    <div class="cargo-bar-bg">
        <div id="tt-vessel-bar" class="cargo-bar-fill"></div>
    </div>
    <div class="tt-row" style="margin-top:6px;">
        <span class="tt-label">Operational Status:</span>
        <span id="tt-vessel-state" class="tt-val" style="color:#38BDF8;">Unloading at Berth B4</span>
    </div>
    <div class="tt-row">
        <span class="tt-label">Cycle Countdown:</span>
        <span id="tt-vessel-timer" class="tt-val" style="color:#34D399;">24s remaining</span>
    </div>
</div>

<!-- Modal 1: Simulation Settings & Policy Presets -->
<div id="modal-settings" class="modal-overlay">
    <div class="glass-panel modal-window">
        <div class="modal-header">
            <div class="modal-title">
                <span>⚙️</span>
                <span>Simulation Configuration & Policy Presets</span>
            </div>
            <button class="modal-close" data-target="modal-settings">✕</button>
        </div>

        <div class="modal-tabs">
            <button class="modal-tab-btn active" data-tab="tab-params">Operational Parameters</button>
            <button class="modal-tab-btn" data-tab="tab-presets">Intervention Scenarios</button>
        </div>

        <div class="modal-body">
            <div id="tab-params" class="tab-content active">
                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Total Medium Commercial Vessels Fleet</div>
                        <div class="param-desc">Total fleet operating between San Miguel Bay fishing and port unloading.</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-medium-fleet" min="5" max="30" step="1" value="12">
                        <span id="val-medium-fleet" class="param-val">12 craft</span>
                    </div>
                </div>

                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Total Small Boats Fleet (Shuttle Bancas)</div>
                        <div class="param-desc">Pool of artisanal double-outrigger bancas for lightering and shallow ops.</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-bancas-fleet" min="2" max="25" step="1" value="8">
                        <span id="val-bancas-fleet" class="param-val">8 craft</span>
                    </div>
                </div>

                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Medium Boat Unload Duration Range</div>
                        <div class="param-desc">Base scale for banyera offload times at berths (light: ~14s, heavy: ~35s).</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-unload-scale" min="1.0" max="5.0" step="0.5" value="3.0">
                        <span id="val-unload-scale" class="param-val">15–35s</span>
                    </div>
                </div>

                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Wharf Apron Berthing Slips (Medium Commercial)</div>
                        <div class="param-desc">Physical landing berths along the deep-water concrete wharf lip.</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-berths" min="6" max="18" step="1" value="13">
                        <span id="val-berths" class="param-val">13 berths</span>
                    </div>
                </div>

                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Semi-Diurnal Shallow Bathymetry Gating</div>
                        <div class="param-desc">Enforce draft restriction (>1.8m) requiring outer anchorage during low tide.</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="checkbox" id="chk-tide" checked style="accent-color:#38BDF8; width:18px; height:18px; cursor:pointer;">
                        <span style="font-size:0.8rem; color:#34D399; font-weight:600;">Bathymetry Lock Active</span>
                    </div>
                </div>
            </div>

            <div id="tab-presets" class="tab-content">
                <div class="preset-grid">
                    <div class="preset-card active" data-preset="baseline">
                        <span class="preset-tag">Phase IV — Status Quo</span>
                        <div class="preset-name">1. Baseline (Mercedes Port Expanded)</div>
                        <div class="preset-desc">13 medium berths, 24 commercial vessels, 32 bancas, 1.8m low-tide draft lock, and 6:00 AM auction rush.</div>
                    </div>

                    <div class="preset-card" data-preset="interventionA">
                        <span class="preset-tag" style="color:#10B981;">Intervention A</span>
                        <div class="preset-name">2. Wharf Apron & Winches (16 Berths)</div>
                        <div class="preset-desc">Expands concrete apron to 16 berths and introduces mechanical winches (+50% banyera offload speed).</div>
                    </div>

                    <div class="preset-card" data-preset="interventionB">
                        <span class="preset-tag" style="color:#F59E0B;">Intervention B</span>
                        <div class="preset-name">3. Estuarine Channel Dredging (3.5m)</div>
                        <div class="preset-desc">Deepens river mouth bathymetry to 3.5m, eliminating low-tide draft restrictions so commercial vessels berth directly.</div>
                    </div>

                    <div class="preset-card" data-preset="interventionC">
                        <span class="preset-tag" style="color:#A855F7;">Intervention C</span>
                        <div class="preset-name">4. Staggered Bulungan Scheduling</div>
                        <div class="preset-desc">Implements timed offloading windows for purse seiners and basnigs, smoothing out the 06:00 AM bottleneck.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modal 2: Academic Analytics & Comparative Report -->
<div id="modal-analytics" class="modal-overlay">
    <div class="glass-panel modal-window" style="max-width: 780px;">
        <div class="modal-header">
            <div class="modal-title">
                <span>📊</span>
                <span>Operational Research Summary & Policy Matrix</span>
            </div>
            <button class="modal-close" data-target="modal-analytics">✕</button>
        </div>

        <div class="modal-body">
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Scenario Architecture</th>
                            <th>Wait Time (Wq)</th>
                            <th>Vessel Turnaround</th>
                            <th>Berth Util (ρ)</th>
                            <th>Post-Harvest Loss</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="font-weight:700;">1. Baseline (Mercedes Port Expanded)</td>
                            <td style="color:#FBBF24;">1.85 ± 0.18h</td>
                            <td>3.80 hrs</td>
                            <td>78.4%</td>
                            <td style="color:#F87171;">PHP 740,000</td>
                        </tr>
                        <tr>
                            <td style="font-weight:700; color:#10B981;">2. Wharf Upgrade (16 Berths)</td>
                            <td>0.72 ± 0.08h</td>
                            <td>2.10 hrs</td>
                            <td>52.1%</td>
                            <td style="color:#34D399;">PHP 240,000</td>
                        </tr>
                        <tr>
                            <td style="font-weight:700; color:#F59E0B;">3. Channel Dredging (3.5m)</td>
                            <td>0.45 ± 0.05h</td>
                            <td>1.75 hrs</td>
                            <td>46.2%</td>
                            <td style="color:#34D399;">PHP 160,000</td>
                        </tr>
                        <tr>
                            <td style="font-weight:700; color:#A855F7;">4. Staggered Scheduling</td>
                            <td>0.98 ± 0.11h</td>
                            <td>2.50 hrs</td>
                            <td>61.5%</td>
                            <td style="color:#34D399;">PHP 310,000</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div style="display:flex; justify-content:flex-end; margin-top:16px;">
                <button id="btn-screenshot-mode" class="btn-hud primary">📸 Enter Clean Screenshot Mode</button>
            </div>
        </div>
    </div>
</div>

<script>
(function() {
    'use strict';

    // -------------------------------------------------------------
    // THREE.JS SCENE, CAMERA, RENDERER
    // -------------------------------------------------------------
    const canvas = document.getElementById('webgl-canvas');
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: false });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x060C18);
    scene.fog = new THREE.FogExp2(0x060C18, 0.0016);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 2500);
    camera.position.set(-105, 115, 165);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 - 0.04;
    controls.minDistance = 20;
    controls.maxDistance = 850;
    controls.target.set(30, 0, 0);

    // -------------------------------------------------------------
    // LIGHTING SYSTEM
    // -------------------------------------------------------------
    const ambientLight = new THREE.AmbientLight(0x0E1E38, 1.4);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xFDF4DC, 1.3);
    sunLight.position.set(-120, 220, 150);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 10;
    sunLight.shadow.camera.far = 700;
    sunLight.shadow.camera.left = -300;
    sunLight.shadow.camera.right = 300;
    sunLight.shadow.camera.top = 300;
    sunLight.shadow.camera.bottom = -300;
    scene.add(sunLight);

    // -------------------------------------------------------------
    // LIGHTHOUSE (PERCHED ON NORTH BREAKWATER AT Y = 18.5)
    // -------------------------------------------------------------
    const LighthouseRoot = new THREE.Group();
    LighthouseRoot.position.set(70, 0, -103);
    scene.add(LighthouseRoot);

    const rockMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.9 });
    const rockBase = new THREE.Mesh(new THREE.CylinderGeometry(8, 10, 4, 8), rockMat);
    rockBase.position.set(0, 2.0, 0);
    rockBase.receiveShadow = true;
    LighthouseRoot.add(rockBase);

    const towerMat = new THREE.MeshStandardMaterial({ color: 0xF8FAFC, roughness: 0.4 });
    const towerGeo = new THREE.CylinderGeometry(2.2, 3.8, 18, 16);
    const towerMesh = new THREE.Mesh(towerGeo, towerMat);
    towerMesh.position.set(0, 11, 0);
    towerMesh.castShadow = true;
    LighthouseRoot.add(towerMesh);

    const stripeMat = new THREE.MeshStandardMaterial({ color: 0xDC2626, roughness: 0.4 });
    const stripe1 = new THREE.Mesh(new THREE.CylinderGeometry(2.9, 3.2, 3.2, 16), stripeMat);
    stripe1.position.set(0, 9.5, 0);
    LighthouseRoot.add(stripe1);

    const stripe2 = new THREE.Mesh(new THREE.CylinderGeometry(2.4, 2.6, 2.8, 16), stripeMat);
    stripe2.position.set(0, 16.2, 0);
    LighthouseRoot.add(stripe2);

    const LanternRoomGroup = new THREE.Group();
    LanternRoomGroup.position.set(0, 20.5, 0);
    LighthouseRoot.add(LanternRoomGroup);

    const galleryDeck = new THREE.Mesh(
        new THREE.CylinderGeometry(3.2, 3.2, 0.8, 16),
        new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.6 })
    );
    galleryDeck.position.set(0, -0.4, 0);
    LanternRoomGroup.add(galleryDeck);

    const glassMat = new THREE.MeshStandardMaterial({
        color: 0xBAE6FD,
        emissive: 0x38BDF8,
        emissiveIntensity: 0.95,
        roughness: 0.1,
        metalness: 0.2,
        transparent: true,
        opacity: 0.85
    });
    const lanternGlass = new THREE.Mesh(new THREE.CylinderGeometry(2.0, 2.0, 3.0, 16), glassMat);
    lanternGlass.position.set(0, 1.1, 0);
    LanternRoomGroup.add(lanternGlass);

    const roofCupola = new THREE.Mesh(
        new THREE.ConeGeometry(2.4, 2.0, 16),
        new THREE.MeshStandardMaterial({ color: 0x1E3A5F, roughness: 0.3, metalness: 0.6 })
    );
    roofCupola.position.set(0, 3.3, 0);
    LanternRoomGroup.add(roofCupola);

    const lampBulb = new THREE.Mesh(
        new THREE.SphereGeometry(0.7, 8, 8),
        new THREE.MeshBasicMaterial({ color: 0xFFFFFF })
    );
    lampBulb.position.set(0, 1.1, 0);
    LanternRoomGroup.add(lampBulb);

    const LightRotorPivot = new THREE.Group();
    LightRotorPivot.position.set(0, 1.1, 0);
    LanternRoomGroup.add(LightRotorPivot);

    const spotLight = new THREE.SpotLight(0xE0F2FE, 5.5, 180, Math.PI / 7, 0.3, 1.1);
    spotLight.position.set(0, 0, 0);
    const spotTarget = new THREE.Object3D();
    spotTarget.position.set(0, -2, 40);
    LightRotorPivot.add(spotTarget);
    spotLight.target = spotTarget;
    LightRotorPivot.add(spotLight);

    const beamGeo = new THREE.ConeGeometry(4, 35, 32, 1, true);
    beamGeo.translate(0, -17.5, 0);
    beamGeo.rotateX(-Math.PI / 2);
    beamGeo.rotateX(Math.atan2(2, 35));

    const beamMat = new THREE.MeshBasicMaterial({
        color: 0xE0F2FE,
        transparent: true,
        opacity: 0.18,
        depthWrite: false,
        side: THREE.DoubleSide,
        blending: THREE.AdditiveBlending
    });
    const beamMesh = new THREE.Mesh(beamGeo, beamMat);
    beamMesh.position.set(0, 0, 0);
    LightRotorPivot.add(beamMesh);

    // -------------------------------------------------------------
    // HARBOR ENVIRONMENT & CONTINUOUS CONCRETE WHARF APRON
    // -------------------------------------------------------------
    const waterGeo = new THREE.PlaneGeometry(1200, 1200, 60, 60);
    const waterMat = new THREE.MeshStandardMaterial({
        color: 0x0A2244,
        roughness: 0.15,
        metalness: 0.8,
        transparent: true,
        opacity: 0.92,
        flatShading: true
    });
    const water = new THREE.Mesh(waterGeo, waterMat);
    water.rotation.x = -Math.PI / 2;
    water.position.y = 0;
    water.receiveShadow = true;
    scene.add(water);

    const posAttr = waterGeo.attributes.position;
    const baseVerts = [];
    for (let i = 0; i < posAttr.count; i++) {
        baseVerts.push({ x: posAttr.getX(i), y: posAttr.getY(i), z: posAttr.getZ(i) });
    }

    // Coastal Landmass Banks (Flanking Fairway)
    const landMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.85 });
    const northBank = new THREE.Mesh(new THREE.BoxGeometry(340, 16, 160), landMat);
    northBank.position.set(85, 8, -193);
    northBank.receiveShadow = true;
    scene.add(northBank);

    const southBank = new THREE.Mesh(new THREE.BoxGeometry(340, 16, 160), landMat);
    southBank.position.set(85, 8, 193);
    southBank.receiveShadow = true;
    scene.add(southBank);

    // Clean Coastal Seawalls (No inner traps)
    const seawallMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.7, metalness: 0.3 });

    // North Breakwater Seawall (Z = -105.0, X: -75 to 245)
    const northSeawall = new THREE.Mesh(new THREE.BoxGeometry(320, 8, 8), seawallMat);
    northSeawall.position.set(85, 4, -109);
    scene.add(northSeawall);

    // South Breakwater Seawall (Z = +105.0, X: -75 to 245)
    const southSeawall = new THREE.Mesh(new THREE.BoxGeometry(320, 8, 8), seawallMat);
    southSeawall.position.set(85, 4, 109);
    scene.add(southSeawall);

    // 1 Continuous Wide Concrete Wharf Apron (X: -75.0 to -35.0, Z: -105.0 to +105.0)
    // Front face at X = -35.0
    const wharfMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.7, metalness: 0.2 });
    const wharfApron = new THREE.Mesh(new THREE.BoxGeometry(40, 6, 210), wharfMat);
    wharfApron.position.set(-55, 3, 0);
    wharfApron.receiveShadow = true;
    scene.add(wharfApron);

    // Fendering along front wharf face (X = -34.5)
    const fenderMat = new THREE.MeshStandardMaterial({ color: 0x0F172A, roughness: 0.9 });
    const wharfFender = new THREE.Mesh(new THREE.BoxGeometry(1.0, 5.8, 210), fenderMat);
    wharfFender.position.set(-34.5, 3, 0);
    scene.add(wharfFender);

    // Safety Hazard Striping (X = -34.8)
    const hazardLip = new THREE.Mesh(
        new THREE.BoxGeometry(0.6, 6.1, 210),
        new THREE.MeshBasicMaterial({ color: 0xFBBF24 })
    );
    hazardLip.position.set(-34.8, 3, 0);
    scene.add(hazardLip);

    // Bulungan Wholesale Auction Sheds
    const shedMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.6 });
    const mainShed = new THREE.Mesh(new THREE.BoxGeometry(18, 9, 140), shedMat);
    mainShed.position.set(-58, 7.5, 0);
    mainShed.castShadow = true;
    scene.add(mainShed);

    const shedLight1 = new THREE.PointLight(0xF59E0B, 2.5, 60);
    shedLight1.position.set(-46, 9, -40);
    scene.add(shedLight1);

    const shedLight2 = new THREE.PointLight(0xF59E0B, 3.0, 70);
    shedLight2.position.set(-46, 9, 0);
    scene.add(shedLight2);

    const shedLight3 = new THREE.PointLight(0xF59E0B, 2.5, 60);
    shedLight3.position.set(-46, 9, 40);
    scene.add(shedLight3);

    // -------------------------------------------------------------
    // 13 MEDIUM COMMERCIAL BERTHS (X = -28.0 IN OPEN WATER)
    // -------------------------------------------------------------
    const MAX_MEDIUM_BERTHS = 13;
    let numBerths = MAX_MEDIUM_BERTHS;
    const BERTH_SLOTS = [];
    const bollardMat = new THREE.MeshStandardMaterial({ color: 0x0F172A, metalness: 0.8 });
    const berthDecorGroup = new THREE.Group();
    scene.add(berthDecorGroup);

    function initBerths() {
        while (berthDecorGroup.children.length > 0) {
            berthDecorGroup.remove(berthDecorGroup.children[0]);
        }
        BERTH_SLOTS.length = 0;
        const startZ = -84.0;
        const spacing = 14.0;

        for (let i = 0; i < numBerths; i++) {
            const z = startZ + i * spacing;
            BERTH_SLOTS.push({
                id: i + 1,
                name: 'Berth B' + (i + 1),
                x: -28.0,
                dockX: -28.0,
                z: z,
                occupiedBy: null
            });

            // Mooring bollard on concrete wharf edge (X = -35.2)
            const bollard = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.5, 1.2, 8), bollardMat);
            bollard.position.set(-35.2, 6.6, z);
            berthDecorGroup.add(bollard);

            // Yellow berthing apron zone (X = -36.5)
            const pad = new THREE.Mesh(new THREE.PlaneGeometry(2, 4), new THREE.MeshBasicMaterial({ color: 0xFBBF24 }));
            pad.rotation.x = -Math.PI / 2;
            pad.position.set(-36.5, 6.05, z);
            berthDecorGroup.add(pad);
        }
    }
    initBerths();

    // 12 DISTRIBUTED BANCA LANDING POINTS ALONG FRONT APRON (X = -28.0)
    const BANCA_LANDING_SPOTS = [];
    for (let i = 0; i < 12; i++) {
        BANCA_LANDING_SPOTS.push({ x: -28.0, z: -77.0 + i * 14.0 });
    }

    // -------------------------------------------------------------
    // ORDERLY IALA BUOY CORRIDOR FAIRWAY (GREEN STARBOARD / RED PORT)
    // -------------------------------------------------------------
    const buoyGroup = new THREE.Group();
    scene.add(buoyGroup);

    const greenBuoyMat = new THREE.MeshBasicMaterial({ color: 0x10B981 });
    const redBuoyMat = new THREE.MeshBasicMaterial({ color: 0xEF4444 });
    const buoyBodyGeo = new THREE.CylinderGeometry(0.8, 1.3, 3.2, 10);
    const buoyLightGeo = new THREE.SphereGeometry(0.4, 8, 8);

    const BUOY_PAIRS = [
        { x: 165, zStarboard: -35, zPort: 35 }, // Pair 1: Outer Bay Entrance
        { x: 105, zStarboard: -30, zPort: 30 }, // Pair 2: Anchorage Gateway
        { x: 45,  zStarboard: -26, zPort: 26 }, // Pair 3: Mid-Channel Fairway
        { x: -5,  zStarboard: -22, zPort: 22 }  // Pair 4: Harbor Approach Gate
    ];

    BUOY_PAIRS.forEach(pair => {
        // Starboard (Green)
        const gBody = new THREE.Mesh(buoyBodyGeo, greenBuoyMat);
        gBody.position.set(pair.x, 1.6, pair.zStarboard);
        const gLight = new THREE.Mesh(buoyLightGeo, new THREE.MeshBasicMaterial({ color: 0x34D399 }));
        gLight.position.set(0, 2.0, 0);
        gBody.add(gLight);
        buoyGroup.add(gBody);

        // Port (Red)
        const rBody = new THREE.Mesh(buoyBodyGeo, redBuoyMat);
        rBody.position.set(pair.x, 1.6, pair.zPort);
        const rLight = new THREE.Mesh(buoyLightGeo, new THREE.MeshBasicMaterial({ color: 0xF87171 }));
        rLight.position.set(0, 2.0, 0);
        rBody.add(rLight);
        buoyGroup.add(rBody);
    });

    // -------------------------------------------------------------
    // SOLID WALLS & INFINITE-THICKNESS HALF-SPACE BOUNDARY CLAMPING
    // -------------------------------------------------------------
    const SOLID_WALLS = [
        { name: 'WHARF_APRON', minX: -75.0, maxX: -35.0, minZ: -105.0, maxZ: 105.0 },
        { name: 'NORTH_SEAWALL', minX: -75.0, maxX: 260.0, minZ: -180.0, maxZ: -105.0 },
        { name: 'SOUTH_SEAWALL', minX: -75.0, maxX: 260.0, minZ: 105.0, maxZ: 180.0 }
    ];

    function applyBoundaryClamps(boat) {
        if (boat.isDocked || boat.state === 'Unloading at Wharf' || boat.state === 'unloading_at_wharf') {
            return; // Rock-steady mooring at wharf
        }
        const R = boat.isSmallBoat ? 2.2 : 4.5;
        // 1. Wharf Front Barrier (X = -35.0)
        if (boat.mesh.position.x < -35.0 + R) {
            boat.mesh.position.x = -35.0 + R;
            boat.heading = Math.PI * 0.5; // Steer eastward away from wall (+X)
            boat.mesh.rotation.y = boat.heading;
            boat.speed *= 0.5;
        }
        // 2. North Seawall Barrier (Z = -105.0)
        if (boat.mesh.position.z < -105.0 + R) {
            boat.mesh.position.z = -105.0 + R;
            boat.heading = 0; // Steer southward toward +Z
            boat.mesh.rotation.y = boat.heading;
            boat.speed *= 0.5;
        }
        // 3. South Seawall Barrier (Z = +105.0)
        if (boat.mesh.position.z > 105.0 - R) {
            boat.mesh.position.z = 105.0 - R;
            boat.heading = Math.PI; // Steer northward toward -Z
            boat.mesh.rotation.y = boat.heading;
            boat.speed *= 0.5;
        }
    }

    function resolveHullCollision(boat) {
        if (boat.isDocked || boat.state === 'Unloading at Wharf' || boat.state === 'unloading_at_wharf') {
            return; // Zero collision pushback while docked!
        }
        const length = boat.isSmallBoat ? 5.5 : 13.0;
        const beam = boat.isSmallBoat ? 2.6 : 4.4;
        const dOffset = length / 2.4;
        const sinP = Math.sin(boat.heading);
        const cosP = Math.cos(boat.heading);

        const circles = [
            { x: boat.mesh.position.x + dOffset * sinP, z: boat.mesh.position.z + dOffset * cosP, r: beam * 0.55 },
            { x: boat.mesh.position.x,                 z: boat.mesh.position.z,                 r: beam * 0.60 },
            { x: boat.mesh.position.x - dOffset * sinP, z: boat.mesh.position.z - dOffset * cosP, r: beam * 0.55 }
        ];

        for (const c of circles) {
            for (const wall of SOLID_WALLS) {
                const qx = Math.max(wall.minX, Math.min(c.x, wall.maxX));
                const qz = Math.max(wall.minZ, Math.min(c.z, wall.maxZ));
                const dx = c.x - qx;
                const dz = c.z - qz;
                const distSq = dx * dx + dz * dz;

                if (distSq < c.r * c.r && distSq > 0.0001) {
                    const dist = Math.sqrt(distSq);
                    const nx = dx / dist;
                    const nz = dz / dist;
                    const pen = c.r - dist;

                    boat.mesh.position.x += nx * (pen + 0.2);
                    boat.mesh.position.z += nz * (pen + 0.2);
                    boat.speed *= 0.7;
                }
            }
        }
    }

    // -------------------------------------------------------------
    // PHILIPPINE 3D BOAT MESH FACTORY (BOW STRICTLY AT LOCAL +Z)
    // All vessels: bow = +Z, stern = -Z, stbd = +X, port = -X
    // -------------------------------------------------------------
    function createVesselMesh(type) {
        const root = new THREE.Group();
        const meshVisualGroup = new THREE.Group();
        meshVisualGroup.name = 'visualGroup';
        root.add(meshVisualGroup);

        // Shared palette materials
        const darkTireMat  = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.9 });
        const woodMat      = new THREE.MeshStandardMaterial({ color: 0xB45309, roughness: 0.75 });
        const bambooMat    = new THREE.MeshStandardMaterial({ color: 0xD97706, roughness: 0.6 });
        const metalMat     = new THREE.MeshStandardMaterial({ color: 0x64748B, metalness: 0.6, roughness: 0.4 });
        const antiFoulMat  = new THREE.MeshStandardMaterial({ color: 0x991B1B, roughness: 0.5 });
        const windowMat    = new THREE.MeshStandardMaterial({ color: 0x38BDF8, roughness: 0.1, transparent: true, opacity: 0.65 });

        if (type === 'Banca') {
            // -----------------------------------------------------------------
            // ARTISANAL DOUBLE-OUTRIGGER SHUTTLE BANCA (bow at local +Z)
            // -----------------------------------------------------------------
            const bancaHullMat = new THREE.MeshStandardMaterial({ color: 0x0284C7, roughness: 0.4 });
            const canopyMat    = new THREE.MeshStandardMaterial({ color: 0xF1F5F9, roughness: 0.8 });

            // Slender wooden hull
            const hull = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.65, 4.4), bancaHullMat);
            hull.position.set(0, 0.35, -0.2);
            hull.castShadow = true;
            meshVisualGroup.add(hull);

            // Sharp bow rake at +Z
            const bowCone = new THREE.Mesh(new THREE.ConeGeometry(0.48, 1.4, 4), bancaHullMat);
            bowCone.rotation.x = Math.PI / 2;
            bowCone.rotation.y = Math.PI / 4;
            bowCone.position.set(0, 0.42, 2.5);
            bowCone.castShadow = true;
            meshVisualGroup.add(bowCone);

            // Transom stern
            const sternBox = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.55, 0.8), woodMat);
            sternBox.position.set(0, 0.38, -2.6);
            meshVisualGroup.add(sternBox);

            // Tawid crossbeams (fore & aft)
            const tawidGeo = new THREE.CylinderGeometry(0.045, 0.045, 3.2, 8);
            const tawidFore = new THREE.Mesh(tawidGeo, bambooMat);
            tawidFore.rotation.z = Math.PI / 2;
            tawidFore.position.set(0, 0.52, 0.8);
            meshVisualGroup.add(tawidFore);
            const tawidAft = new THREE.Mesh(tawidGeo, bambooMat);
            tawidAft.rotation.z = Math.PI / 2;
            tawidAft.position.set(0, 0.52, -1.0);
            meshVisualGroup.add(tawidAft);

            // Bamboo katig floats at water skimline Y = 0.08
            const katigGeo = new THREE.CylinderGeometry(0.09, 0.09, 4.6, 8);
            const katigPort = new THREE.Mesh(katigGeo, bambooMat);
            katigPort.rotation.x = Math.PI / 2;
            katigPort.position.set(-1.55, 0.08, -0.1);
            meshVisualGroup.add(katigPort);
            const katigStbd = new THREE.Mesh(katigGeo, bambooMat);
            katigStbd.rotation.x = Math.PI / 2;
            katigStbd.position.set(1.55, 0.08, -0.1);
            meshVisualGroup.add(katigStbd);

            // Canvas canopy
            const canopy = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.04, 2.2), canopyMat);
            canopy.position.set(0, 1.15, -0.1);
            meshVisualGroup.add(canopy);

            // Dynamic banyera tub group
            const crateGroup = new THREE.Group();
            crateGroup.name = 'cargoCrates';
            const tubGeo = new THREE.CylinderGeometry(0.18, 0.15, 0.18, 8);
            const tubMatO = new THREE.MeshStandardMaterial({ color: 0xEA580C, roughness: 0.5 });
            const tubMatB = new THREE.MeshStandardMaterial({ color: 0x2563EB, roughness: 0.5 });
            for (let row = 0; row < 3; row++) {
                for (let col = 0; col < 2; col++) {
                    const tub = new THREE.Mesh(tubGeo, (row + col) % 2 === 0 ? tubMatO : tubMatB);
                    tub.position.set((col - 0.5) * 0.32, 0.55, -0.5 + row * 0.38);
                    crateGroup.add(tub);
                }
            }
            meshVisualGroup.add(crateGroup);

        } else {
            // -----------------------------------------------------------------
            // COMMERCIAL FISHING VESSEL: Basnig / Purse Seiner / Ring-Netter
            // -----------------------------------------------------------------
            const hullColors = { 'Basnig': 0x0284C7, 'Purse Seiner': 0x059669, 'Ring-Netter': 0xD97706 };
            const upperHullMat  = new THREE.MeshStandardMaterial({ color: hullColors[type] || 0x0284C7, roughness: 0.4 });
            const deckMat       = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.7 });
            const wheelhouseMat = new THREE.MeshStandardMaterial({ color: 0xF8FAFC, roughness: 0.3 });

            // Red anti-fouling lower hull (waterline strip)
            const lowerHull = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.75, 11.2), antiFoulMat);
            lowerHull.position.set(0, 0.38, -0.4);
            lowerHull.castShadow = true;
            meshVisualGroup.add(lowerHull);
            const lowerBow = new THREE.Mesh(new THREE.ConeGeometry(1.8, 2.6, 4), antiFoulMat);
            lowerBow.rotation.x = Math.PI / 2;
            lowerBow.rotation.y = Math.PI / 4;
            lowerBow.position.set(0, 0.38, 5.8);
            lowerBow.castShadow = true;
            meshVisualGroup.add(lowerBow);

            // Upper freeboard hull (flared V-bow at +Z)
            const upperHull = new THREE.Mesh(new THREE.BoxGeometry(3.8, 1.1, 11.4), upperHullMat);
            upperHull.position.set(0, 1.3, -0.4);
            upperHull.castShadow = true;
            meshVisualGroup.add(upperHull);
            const upperBow = new THREE.Mesh(new THREE.ConeGeometry(1.95, 2.8, 4), upperHullMat);
            upperBow.rotation.x = Math.PI / 2;
            upperBow.rotation.y = Math.PI / 4;
            upperBow.position.set(0, 1.3, 5.9);
            upperBow.castShadow = true;
            meshVisualGroup.add(upperBow);

            // Working deck
            const mainDeck = new THREE.Mesh(new THREE.BoxGeometry(3.5, 0.1, 11.0), deckMat);
            mainDeck.position.set(0, 1.86, -0.4);
            meshVisualGroup.add(mainDeck);

            // Two-tier wheelhouse (midship)
            const bridgeLower = new THREE.Mesh(new THREE.BoxGeometry(2.5, 1.4, 3.4), wheelhouseMat);
            bridgeLower.position.set(0, 2.6, 0.8);
            bridgeLower.castShadow = true;
            meshVisualGroup.add(bridgeLower);
            const bridgeUpper = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.1, 2.4), wheelhouseMat);
            bridgeUpper.position.set(0, 3.85, 0.6);
            bridgeUpper.castShadow = true;
            meshVisualGroup.add(bridgeUpper);
            // Glazed bridge windows facing +Z
            const winFore = new THREE.Mesh(new THREE.PlaneGeometry(1.9, 0.6), windowMat);
            winFore.position.set(0, 3.95, 1.82);
            meshVisualGroup.add(winFore);

            // A-frame mast & derrick boom
            const mastPole = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.14, 5.2, 8), metalMat);
            mastPole.position.set(0, 4.8, 2.0);
            meshVisualGroup.add(mastPole);
            const boomDerrick = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 5.5, 8), metalMat);
            boomDerrick.rotation.x = -Math.PI / 3.8;
            boomDerrick.position.set(0, 3.4, -1.2);
            meshVisualGroup.add(boomDerrick);

            // Stern seine / net drum
            const netDrum = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 2.6, 12), darkTireMat);
            netDrum.rotation.z = Math.PI / 2;
            netDrum.position.set(0, 2.4, -4.5);
            meshVisualGroup.add(netDrum);

            // Rubber tire gunwale fenders
            const tireGeo = new THREE.TorusGeometry(0.26, 0.10, 6, 12);
            for (const side of [-1, 1]) {
                for (const fz of [-3.2, -1.0, 1.2, 3.4]) {
                    const tire = new THREE.Mesh(tireGeo, darkTireMat);
                    tire.rotation.y = Math.PI / 2;
                    tire.position.set(side * 1.95, 1.5, fz);
                    meshVisualGroup.add(tire);
                }
            }

            // Basnig squid-light booms (extended outrigger rig)
            if (type === 'Basnig') {
                const outBoomGeo = new THREE.CylinderGeometry(0.09, 0.09, 10.5, 8);
                const boomPort = new THREE.Mesh(outBoomGeo, bambooMat);
                boomPort.rotation.z = Math.PI / 3.0;
                boomPort.position.set(-4.2, 3.2, 0.5);
                meshVisualGroup.add(boomPort);
                const boomStbd = new THREE.Mesh(outBoomGeo, bambooMat);
                boomStbd.rotation.z = -Math.PI / 3.0;
                boomStbd.position.set(4.2, 3.2, 0.5);
                meshVisualGroup.add(boomStbd);
            }

            // Dynamic banyera fish tub stacks on cargo hatch
            const crateGroup = new THREE.Group();
            crateGroup.name = 'cargoCrates';
            const crateBoxGeo  = new THREE.BoxGeometry(0.55, 0.40, 0.55);
            const crateMatBlue = new THREE.MeshStandardMaterial({ color: 0x1D4ED8, roughness: 0.5 });
            const crateMatOra  = new THREE.MeshStandardMaterial({ color: 0xC2410C, roughness: 0.5 });
            for (let ix = -1; ix <= 1; ix++) {
                for (let iz = -2; iz <= 0; iz++) {
                    const crate = new THREE.Mesh(crateBoxGeo, (ix + iz) % 2 === 0 ? crateMatBlue : crateMatOra);
                    crate.position.set(ix * 0.65, 2.1, iz * 0.65 - 1.8);
                    crateGroup.add(crate);
                }
            }
            meshVisualGroup.add(crateGroup);
        }

        // Shared bow-wake plane (now supplemented by world-space particles)
        const wakeMat = new THREE.MeshBasicMaterial({ color: 0xE0F2FE, transparent: true, opacity: 0.0, depthWrite: false, side: THREE.DoubleSide });
        const wakeGeo = new THREE.PlaneGeometry(type === 'Banca' ? 2.5 : 5.0, type === 'Banca' ? 4.0 : 8.0);
        const wake = new THREE.Mesh(wakeGeo, wakeMat);
        wake.rotation.x = -Math.PI / 2;
        wake.position.set(0, 0.05, type === 'Banca' ? -2.5 : -5.0);
        wake.name = 'bowWake';
        meshVisualGroup.add(wake);

        return root;
    }

    // Sync banyera crate visuals to cargo level (called on every docking state change)
    function updateVesselCrateVisuals(boat) {
        const cg = boat.mesh.getObjectByName('cargoCrates');
        if (!cg) return;
        const ratio = (boat.maxCargo > 0) ? (boat.cargo / boat.maxCargo) : 0;
        cg.visible = ratio > 0.04;
        cg.scale.set(1.0, Math.max(0.08, ratio), 1.0);
    }
    function updateBancaCrateVisuals(banca) {
        const cg = banca.mesh.getObjectByName('cargoCrates');
        if (!cg) return;
        cg.visible = banca.cargo > 0;
        if (banca.cargo > 0) cg.scale.set(1.0, 1.0, 1.0);
    }

    // -------------------------------------------------------------
    // OCEAN WAVE MOTION & TIDAL DYNAMICS
    // -------------------------------------------------------------
    function getWaveHeight(x, z, time) {
        return Math.sin(x * 0.04 + time * 2.0) * 0.35 +
               Math.cos(z * 0.05 + time * 1.5) * 0.25;
    }

    function computeTide(t) {
        // Semi-diurnal tide formula for Mercedes River mouth (San Miguel Bay)
        // Range: +0.60m (Low Tide) to +2.10m (High Tide) with ~12.42h periodicity
        return 1.35 + 0.75 * Math.cos((t - 6.0) * (Math.PI / 6.0));
    }

    // -------------------------------------------------------------
    // FLEET DATA & RANDOMIZED SKEWED CATCH LOADS
    // -------------------------------------------------------------
    let simTime = 5.75;
    let isPlaying = true;
    let timeScale = 1.0;
    let lastTime = performance.now();

    let arrivalRate = 0.34;
    let bulunganMultiplier = 2.8;
    let tideLockActive = true;
    let totalCratesLanded = 1420;

    let targetTotalMediumFleet = 12;
    let targetTotalBancas = 8;
    let unloadDurationScale = 3.0;

    const vessels = [];
    const bancas = [];

    // Realistic skewed catch generation: 15–35s real-time at 1x
    function rollCatchLoad() {
        const r = Math.random();
        let banyeras, durationSec, tier;
        if (r < 0.35) {
            // Light Catch: 30 to 90 banyeras (~14s real-time)
            banyeras = Math.floor(30 + Math.random() * 61);
            durationSec = 13.0 + Math.random() * 3.0; // 13-16s
            tier = 'Light Catch (Fast Haul)';
        } else if (r < 0.75) {
            // Medium Catch: 100 to 200 banyeras (~24s real-time)
            banyeras = Math.floor(100 + Math.random() * 101);
            durationSec = 22.0 + Math.random() * 5.0; // 22-27s
            tier = 'Medium Catch (Standard)';
        } else {
            // Heavy Catch: 210 to 380 banyeras (~35s real-time)
            banyeras = Math.floor(210 + Math.random() * 171);
            durationSec = 32.0 + Math.random() * 7.0; // 32-39s
            tier = 'Heavy Catch (Bulk Haul)';
        }
        durationSec *= (unloadDurationScale / 3.0);
        return {
            banyeras: banyeras,
            maxCargo: banyeras,
            targetSec: durationSec,
            tier: tier
        };
    }

    function computeFishingDuration(hour) {
        const isRush = hour >= 4.0 && hour <= 9.5;
        if (isRush) {
            return 25 + Math.random() * 30; // 25–55s return in rush
        } else if (hour >= 11.0 && hour <= 16.0) {
            return 80 + Math.random() * 70; // 80–150s at noon
        } else {
            return 45 + Math.random() * 45;
        }
    }

    // -------------------------------------------------------------
    // WORLD-SPACE 150-PARTICLE WAKE EFFECTOR POOL
    // Particles are scene children, NOT parented to boats → curved trails
    // -------------------------------------------------------------
    const MAX_WAKE_PARTICLES = 150;
    const wakePool = [];
    const _wakeRingGeo = new THREE.RingGeometry(0.3, 1.1, 16);
    _wakeRingGeo.rotateX(-Math.PI / 2);

    for (let _wi = 0; _wi < MAX_WAKE_PARTICLES; _wi++) {
        const _pm = new THREE.Mesh(_wakeRingGeo, new THREE.MeshBasicMaterial({
            color: 0xBAE6FD, transparent: true, opacity: 0.0,
            depthWrite: false, side: THREE.DoubleSide
        }));
        _pm.visible = false;
        _pm.position.y = 0.08;
        scene.add(_pm);
        wakePool.push({ mesh: _pm, active: false, age: 0, maxLife: 2.2,
                        expandRate: 2.0, initAlpha: 0.42, baseScale: 1.0 });
    }
    let _wakeIdx = 0;

    function spawnWorldWake(x, z, boatScale, speedRatio) {
        const p = wakePool[_wakeIdx];
        _wakeIdx = (_wakeIdx + 1) % MAX_WAKE_PARTICLES;
        p.active = true;
        p.age = 0;
        p.baseScale = boatScale;
        p.expandRate = 1.6 + speedRatio * 2.4;
        p.initAlpha = Math.min(0.55, 0.18 + speedRatio * 0.37);
        p.mesh.position.set(x, 0.08, z);
        p.mesh.scale.setScalar(boatScale);
        p.mesh.material.opacity = p.initAlpha;
        p.mesh.visible = true;
    }

    function updateWorldWakeParticles(dt) {
        for (const p of wakePool) {
            if (!p.active) continue;
            p.age += dt;
            if (p.age >= p.maxLife) {
                p.active = false;
                p.mesh.visible = false;
            } else {
                const progress = p.age / p.maxLife;
                p.mesh.scale.setScalar(p.baseScale + p.age * p.expandRate);
                p.mesh.material.opacity = p.initAlpha * (1.0 - progress);
            }
        }
    }

    function initFleet() {
        // Clear existing meshes
        vessels.forEach(v => scene.remove(v.mesh));
        vessels.length = 0;
        bancas.forEach(b => scene.remove(b.mesh));
        bancas.length = 0;

        // ---- 1. Medium Commercial Fleet ----------------------------------------
        // Initial distribution (no center spawning): 3 docked, 3 anchored, rest at sea
        const initialBerthIndices = [1, 5, 9]; // B2, B6, B10
        const mediumNames = [
            'MV-MercedesQueen', 'MV-SanMiguel', 'MV-BicolExpress', 'MV-DaetStar',
            'MV-NagaPride', 'MV-PandanGem', 'MV-SanRoque', 'MV-BagongSilang',
            'MV-CamNorte', 'MV-PacificDawn', 'MV-Apolonio', 'MV-IslaVerde'
        ];

        for (let i = 0; i < targetTotalMediumFleet; i++) {
            const vName = mediumNames[i % mediumNames.length] + (i >= mediumNames.length ? `-${Math.floor(i / mediumNames.length) + 1}` : '');
            const types = ['Basnig', 'Purse Seiner', 'Ring-Netter'];
            const selType = types[i % types.length];
            const rDraft = selType === 'Basnig' ? (1.9 + (i % 3) * 0.1) : (1.6 + (i % 3) * 0.1);
            const rGT = (18 + (i % 5) * 2.5);

            const catchData = rollCatchLoad();
            const mesh = createVesselMesh(selType);
            scene.add(mesh);

            const v = {
                id: 'Vessel-' + (i + 1),
                name: vName,
                type: selType,
                gt: parseFloat(rGT.toFixed(1)),
                draft: parseFloat(rDraft.toFixed(2)),
                cargo: catchData.banyeras,
                maxCargo: catchData.maxCargo,
                targetSec: catchData.targetSec,
                tier: catchData.tier,
                totalUnloadSec: catchData.targetSec,
                unloadTimer: catchData.targetSec,
                mesh: mesh,
                state: 'AT_SEA_FISHING',
                assignedBerth: null,
                servicedByBanca: null,
                wait: 0,
                heading: 0,
                speed: 0,
                maxSpeed: 14.0,
                maxReverseSpeed: 4.5,
                acceleration: 2.5,
                brakingDistance: 20.0,
                isSmallBoat: false,
                isDocked: false,
                isReversing: false,
                bobOffset: Math.random() * Math.PI * 2,
                laneOffset: (Math.random() - 0.5) * 12.0,
                fishingTimer: 0,
                departureDelay: 0,
                reverseTimer: 0,
                remainingSec: catchData.targetSec,
                baseAnchorHeading: 0,
                channelStep: 1,
                departStep: 1,
                deepSeaTargetX: 280,
                deepSeaTargetZ: 0,
                holdX: 110,
                holdZ: 0,
                wakeTimer: 0,
                spawnFadeTimer: 0
            };

            if (i < 3) {
                // ---- 3 boats docked at X = -28.0 (staggered timers) ----
                const bIdx = initialBerthIndices[i];
                const b = BERTH_SLOTS[bIdx];
                b.occupiedBy = v.name;
                v.assignedBerth = b;
                v.isDocked = true;
                v.state = 'Unloading at Wharf';
                v.mesh.position.set(b.dockX, 0, b.z);
                v.heading = 0;
                v.mesh.rotation.y = 0;
                const initProg = 0.25 + (i * 0.30); // 25%, 55%, 85% through unloading
                v.unloadTimer = v.totalUnloadSec * (1.0 - initProg);
                v.cargo = Math.round(v.maxCargo * (1.0 - initProg));
                v.remainingSec = v.unloadTimer;
                v.departureDelay = 2.0 + Math.random() * 2.0;
                updateVesselCrateVisuals(v);
            } else if (i < 6) {
                // ---- 3 boats anchored in outer bay (X in [105, 140]) ----
                v.state = 'Waiting at Anchorage';
                v.holdX = 105 + (i - 3) * 16;
                v.holdZ = -40 + (i - 3) * 40;
                v.mesh.position.set(v.holdX, 0, v.holdZ);
                v.baseAnchorHeading = -Math.PI / 2;
                v.heading = v.baseAnchorHeading;
                v.mesh.rotation.y = v.heading;
                v.wait = 0.5 + (i - 3) * 0.6;
                updateVesselCrateVisuals(v);
            } else {
                // ---- Rest at sea (invisible; return via horizon spawn X = 240) ----
                v.state = 'AT_SEA_FISHING';
                v.mesh.visible = false;
                v.fishingTimer = computeFishingDuration(simTime) * (0.2 + (i - 6) * 0.14);
            }
            vessels.push(v);
        }

        // ---- 2. Small Bancas Fleet -----------------------------------------------
        // 75% tenders, 25% independent; NO center spawning
        for (let i = 0; i < targetTotalBancas; i++) {
            const bMesh = createVesselMesh('Banca');
            scene.add(bMesh);

            const isTender = (i % 4 < 3); // 75% tenders

            const b = {
                id: 'Banca-' + (i + 1),
                name: (isTender ? 'Tender #' : 'Banca #') + (i + 1),
                type: isTender ? 'Partner Lightering Tender' : 'Independent Fishing Banca',
                role: isTender ? 'tender' : 'independent',
                gt: 2.4,
                draft: 0.65,
                mesh: bMesh,
                state: isTender ? 'patrolling' : 'to_wharf',
                targetBoat: null,
                landingSlotIdx: i % BANCA_LANDING_SPOTS.length,
                patrolTargetX: 90 + Math.random() * 50,
                patrolTargetZ: -50 + Math.random() * 100,
                cargo: isTender ? 0 : Math.floor(15 + Math.random() * 20),
                maxCargo: 40,
                heading: 0,
                speed: 3.0 + Math.random() * 2.0,
                maxSpeed: 17.0,
                maxReverseSpeed: 5.0,
                acceleration: 3.5,
                brakingDistance: 12.0,
                isSmallBoat: true,
                isDocked: false,
                isReversing: false,
                bobOffset: Math.random() * Math.PI * 2,
                laneOffset: (Math.random() - 0.5) * 8.0,
                transferTimer: 0,
                unloadTimer: 0,
                reverseTimer: 0,
                seaTimer: 0,
                wakeTimer: 0,
                spawnFadeTimer: 0
            };

            if (i < 2) {
                // 2 bancas initially at wharf landing apron
                const slot = BANCA_LANDING_SPOTS[i % BANCA_LANDING_SPOTS.length];
                b.mesh.position.set(slot.x, 0, slot.z);
                b.isDocked = true;
                b.state = 'unloading_at_wharf';
                b.unloadTimer = 6.0 + Math.random() * 4.0;
                b.cargo = 20;
            } else if (i < 5) {
                // 3 bancas stationed near anchored mother boats (X in [100, 140])
                b.state = 'patrolling';
                b.mesh.position.set(100 + (i - 2) * 15, 0, -35 + (i - 2) * 35);
                b.heading = -Math.PI / 2;
                b.mesh.rotation.y = b.heading;
            } else {
                // Remaining: inbound from harbour approach (X in [195, 230])
                b.state = isTender ? 'patrolling' : 'to_wharf';
                b.mesh.position.set(195 + ((i - 5) % 6) * 6, 0, -30 + ((i - 5) % 7) * 10);
                b.heading = -Math.PI / 2;
                b.mesh.rotation.y = b.heading;
            }
            updateBancaCrateVisuals(b);
            bancas.push(b);
        }
    }
    initFleet();

    // -------------------------------------------------------------
    // NON-HOLONOMIC 3-DOF KINEMATICS + 3-WHISKER COLREGS AVOIDANCE
    // -------------------------------------------------------------
    function updateVesselKinematics(boat, targetX, targetZ, dt) {
        if (boat.isDocked) { boat.speed = 0; return 0; }

        const dx = targetX - boat.mesh.position.x;
        const dz = targetZ - boat.mesh.position.z;
        const distToTarget = Math.hypot(dx, dz);

        let desiredHeading = Math.atan2(dx, dz);

        // ---- 3-Whisker Sensor Cone (COLREGS Starboard Yield) ----
        const scanRange = 24.0;
        const fwdX = Math.sin(boat.heading);
        const fwdZ = Math.cos(boat.heading);
        let obstacleAhead = false;
        let obstacleDist = 999.0;

        const allCraft = [...vessels, ...bancas];
        for (const other of allCraft) {
            if (other === boat || !other.mesh.visible || other.isDocked) continue;
            const ox = other.mesh.position.x - boat.mesh.position.x;
            const oz = other.mesh.position.z - boat.mesh.position.z;
            const oDist = Math.hypot(ox, oz);
            if (oDist < scanRange && oDist > 0.5) {
                const dotFwd = (ox * fwdX + oz * fwdZ) / oDist;
                if (dotFwd > 0.55) { // Within ±56° forward sensor cone
                    obstacleAhead = true;
                    if (oDist < obstacleDist) obstacleDist = oDist;
                }
            }
        }

        let evasionYaw = 0;
        let throttleScale = 1.0;
        if (obstacleAhead) {
            const urgency = Math.min(1.0, (scanRange - obstacleDist) / scanRange);
            evasionYaw = 0.55 * urgency; // Steer starboard
            if (obstacleDist < 14.0) throttleScale = 0.35; // Slow trailing
        }

        let angleError = (desiredHeading + evasionYaw) - boat.heading;
        while (angleError > Math.PI) angleError -= Math.PI * 2;
        while (angleError < -Math.PI) angleError += Math.PI * 2;

        const maxTurnRate = boat.isSmallBoat ? 2.0 : 0.95;
        const turnStep = Math.sign(angleError) * Math.min(Math.abs(angleError), maxTurnRate * dt);
        boat.heading += turnStep;
        boat.mesh.rotation.y = boat.heading;

        const turnSlowdown = Math.max(0.3, Math.cos(Math.min(Math.abs(angleError), Math.PI / 2)));
        const arrivalBraking = Math.min(1.0, distToTarget / Math.max(1.0, boat.brakingDistance));
        const targetSpeed = boat.isReversing
            ? -boat.maxReverseSpeed
            : boat.maxSpeed * turnSlowdown * arrivalBraking * throttleScale;

        boat.speed += (targetSpeed - boat.speed) * Math.min(1.0, boat.acceleration * dt);

        boat.mesh.position.x += Math.sin(boat.heading) * boat.speed * dt;
        boat.mesh.position.z += Math.cos(boat.heading) * boat.speed * dt;

        // Damped soft-sphere hull-to-hull separation
        resolveSoftHullCollisions(boat);
        applyBoundaryClamps(boat);

        return distToTarget;
    }

    function resolveSoftHullCollisions(boat) {
        if (boat.isDocked) return;
        const rA = boat.isSmallBoat ? 1.8 : 3.8;
        const allCraft = [...vessels, ...bancas];
        for (const other of allCraft) {
            if (other === boat || !other.mesh.visible || other.isDocked) continue;
            const rB = other.isSmallBoat ? 1.8 : 3.8;
            const minSep = rA + rB + 1.8;
            const dx = boat.mesh.position.x - other.mesh.position.x;
            const dz = boat.mesh.position.z - other.mesh.position.z;
            const distSq = dx * dx + dz * dz;
            if (distSq < minSep * minSep && distSq > 0.001) {
                const dist = Math.sqrt(distSq);
                const pen = minSep - dist;
                boat.mesh.position.x += (dx / dist) * pen * 0.35;
                boat.mesh.position.z += (dz / dist) * pen * 0.35;
            }
        }
    }

    // -------------------------------------------------------------
    // MAIN SIMULATION LOOP (DES + 24H DIURNAL TRAFFIC + KINEMATICS)
    // -------------------------------------------------------------
    function updateSimulation(deltaHours, dt, waveTime) {
        simTime = (simTime + deltaHours) % 24.0;
        const tide = computeTide(simTime);

        // UI Clock & Status
        const clockH = Math.floor(simTime);
        const clockM = Math.floor((simTime - clockH) * 60);
        const ampm = clockH >= 12 ? 'PM' : 'AM';
        const displayH = clockH % 12 === 0 ? 12 : clockH % 12;
        const timeStr = `${String(displayH).padStart(2, '0')}:${String(clockM).padStart(2, '0')} ${ampm}`;
        document.getElementById('hud-clock').textContent = timeStr;

        const surgeActive = simTime >= 3.0 && simTime <= 7.2;
        document.getElementById('surge-pill').style.display = surgeActive ? 'inline-flex' : 'none';

        const tidePill = document.getElementById('tide-pill');
        if (tide >= 1.6 || !tideLockActive) {
            tidePill.textContent = 'HIGH TIDE: Open (+' + tide.toFixed(2) + 'm)';
            tidePill.className = 'tide-pill';
        } else {
            tidePill.textContent = 'LOW TIDE: Draft >1.8m Lock (+' + tide.toFixed(2) + 'm)';
            tidePill.className = 'tide-pill low';
        }

        // DIURNAL RESPAWN CHECK FOR BOATS OUT AT SEA FISHING
        let atSeaCount = 0;
        vessels.forEach(v => {
            if (v.state === 'AT_SEA_FISHING') {
                atSeaCount++;
                v.fishingTimer -= dt * timeScale;

                if (v.fishingTimer <= 0) {
                    const rushHour = (simTime >= 3.5 && simTime <= 8.5);
                    const spawnProb = rushHour ? 0.90 : 0.40;

                    if (Math.random() < spawnProb) {
                        v.fishingTimer = 0;
                        const catchData = rollCatchLoad();
                        v.cargo = catchData.banyeras;
                        v.maxCargo = catchData.maxCargo;
                        v.targetSec = catchData.targetSec;
                        v.tier = catchData.tier;
                        v.totalUnloadSec = catchData.targetSec;
                        v.unloadTimer = catchData.targetSec;
                        v.remainingSec = catchData.targetSec;
                        v.isDocked = false;

                        // Spawn at eastern sea horizon (X = 240), invisible pop-in prevented
                        v.mesh.position.set(240, 0, -90 + Math.random() * 180);
                        v.heading = -Math.PI / 2; // Inbound westward
                        v.mesh.rotation.y = v.heading;
                        v.mesh.visible = true;
                        // Fade-in over 2 seconds via spawnFadeTimer
                        if (typeof v.spawnFadeTimer !== 'undefined') {
                            v.spawnFadeTimer = 2.0;
                            const vg = v.mesh.getObjectByName('visualGroup');
                            if (vg) vg.children.forEach(c => { if (c.material) c.material.transparent = true; });
                        }
                        v.holdX = 105 + Math.random() * 35; // Anchorage hold [105, 140]
                        v.holdZ = -55 + Math.random() * 110;
                        v.state = 'Arriving';
                    } else {
                        v.fishingTimer = 25 + Math.random() * 35;
                    }
                }
            }
        });

        // UPDATE MEDIUM COMMERCIAL FLEET
        let waitingCount = 0;
        let occupiedCount = 0;

        vessels.forEach(v => {
            if (!v.mesh.visible) return;

            const waveY = getWaveHeight(v.mesh.position.x, v.mesh.position.z, waveTime);

            // Bow Wake + World-Space Stern Wake Emission
            const bowWake = v.mesh.getObjectByName('bowWake');
            if (bowWake) {
                bowWake.material.opacity = THREE.MathUtils.lerp(
                    bowWake.material.opacity,
                    Math.min(0.55, Math.abs(v.speed) * 0.08),
                    0.15
                );
            }
            // Emit world-space ripple trails from stern (curved wake history)
            if (Math.abs(v.speed) > 1.2) {
                v.wakeTimer = (v.wakeTimer || 0) + dt;
                if (v.wakeTimer > 0.10) {
                    v.wakeTimer = 0;
                    const sternDist = 5.8;
                    const wx = v.mesh.position.x - Math.sin(v.heading) * sternDist;
                    const wz = v.mesh.position.z - Math.cos(v.heading) * sternDist;
                    spawnWorldWake(wx, wz, 2.4, Math.min(1.0, Math.abs(v.speed) / v.maxSpeed));
                }
            }

            if (v.state === 'Arriving') {
                // Hydrodynamic pitch/roll heave while underway
                const speedRatio = Math.abs(v.speed) / v.maxSpeed;
                v.mesh.position.y = waveY * 0.7;
                v.mesh.rotation.x = Math.sin(waveTime * 2.0 + v.bobOffset) * (0.03 + speedRatio * 0.025);
                v.mesh.rotation.z = Math.cos(waveTime * 1.6 + v.bobOffset) * 0.018;

                const targetX = v.holdX;
                const targetZ = v.holdZ + v.laneOffset;
                const dist = updateVesselKinematics(v, targetX, targetZ, dt);
                if (dist < 6.0) {
                    // Decide between Direct Docking (60%) or Convenience Bay Anchorage (40%)
                    const freeBerth = BERTH_SLOTS.find(b => b.occupiedBy === null);
                    const canPassTide = !tideLockActive || tide >= 1.6 || v.draft <= 1.8;
                    const prefersDirect = Math.random() < 0.60;

                    if (freeBerth && canPassTide && prefersDirect) {
                        freeBerth.occupiedBy = v.name;
                        v.assignedBerth = freeBerth;
                        v.state = 'Navigating Channel';
                        v.channelStep = 1;
                    } else {
                        v.state = 'Waiting at Anchorage';
                        v.baseAnchorHeading = -Math.PI / 2 + (Math.random() - 0.5) * 0.4;
                        v.heading = v.baseAnchorHeading;
                        v.mesh.rotation.y = v.heading;
                        v.speed = 0;
                    }
                }
            } else if (v.state === 'Waiting at Anchorage') {
                waitingCount++;
                v.wait += deltaHours;
                v.speed = 0;
                v.mesh.position.y = waveY * 0.7;

                // Gentle Anchored Weathervaning with tidal current (±8 degrees)
                v.heading = v.baseAnchorHeading + Math.sin(simTime * 4.0 + v.bobOffset) * 0.14;
                v.mesh.rotation.y = v.heading;

                // If cargo is fully picked up by small tenders, depart to sea!
                if (v.cargo <= 0) {
                    if (v.assignedBerth) {
                        v.assignedBerth.occupiedBy = null;
                        v.assignedBerth = null;
                    }
                    v.state = 'Departing';
                    v.departStep = 1;
                    v.deepSeaTargetX = 280;
                    v.deepSeaTargetZ = -130 + Math.random() * 260;
                } else if (!v.servicedByBanca) {
                    // If a berth opens up and tide permits, can optionally transition to direct docking
                    const canPassTide = !tideLockActive || tide >= 1.6 || v.draft <= 1.8;
                    const freeBerth = BERTH_SLOTS.find(b => b.occupiedBy === null);
                    if (canPassTide && freeBerth && Math.random() < 0.03) {
                        freeBerth.occupiedBy = v.name;
                        v.assignedBerth = freeBerth;
                        v.state = 'Navigating Channel';
                        v.channelStep = 1;
                    }
                }
            } else if (v.state === 'Navigating Channel') {
                v.mesh.position.y = waveY * 0.7;
                v.mesh.rotation.x = Math.sin(waveTime * 2.0 + v.bobOffset) * 0.03;

                let targetX = 0;
                let targetZ = 0;

                if (v.channelStep === 1) {
                    // Gateway Buoy Pair 2 (X = 105)
                    targetX = 105;
                    targetZ = (v.assignedBerth.z * 0.3) + (v.laneOffset * 0.4);
                    const d = updateVesselKinematics(v, targetX, targetZ, dt);
                    if (d < 12.0) v.channelStep = 2;
                } else if (v.channelStep === 2) {
                    // Harbor Approach Buoy Pair 4 (X = -5)
                    targetX = -5;
                    targetZ = v.assignedBerth.z + (v.laneOffset * 0.2);
                    const d = updateVesselKinematics(v, targetX, targetZ, dt);
                    if (d < 8.0) v.channelStep = 3;
                } else {
                    // Final Docking alongside Berth (X = -28.0)
                    targetX = v.assignedBerth.dockX;
                    targetZ = v.assignedBerth.z;
                    const d = updateVesselKinematics(v, targetX, targetZ, dt);
                    if (d < 2.5) {
                        // Snap cleanly into position with ZERO shaking!
                        v.mesh.position.set(targetX, 0, targetZ);
                        v.heading = 0;
                        v.mesh.rotation.y = 0;
                        v.speed = 0;
                        v.isDocked = true;
                        v.state = 'Unloading at Wharf';
                        v.totalUnloadSec = v.targetSec;
                        v.unloadTimer = v.targetSec;
                        v.departureDelay = 1.5 + Math.random() * 2.5;
                    }
                }
            } else if (v.state === 'Unloading at Wharf') {
                occupiedCount++;
                v.isDocked = true;
                v.speed = 0;
                v.heading = 0;
                v.mesh.rotation.y = 0;

                // ROCK-STEADY HORIZONTAL POSITION (Zero Shaking!)
                v.mesh.position.x = v.assignedBerth.dockX;
                v.mesh.position.z = v.assignedBerth.z;
                v.mesh.position.y = waveY * 0.35; // Gentle heave only
                v.mesh.rotation.x = Math.sin(waveTime * 1.5 + v.bobOffset) * 0.015;

                // GUARANTEED REAL-TIME UNLOADING COUNTDOWN (15 to 35 seconds)
                v.unloadTimer -= dt * timeScale;
                const progress = Math.min(1.0, Math.max(0, 1.0 - (v.unloadTimer / v.totalUnloadSec)));
                const prevCargo = v.cargo;
                v.cargo = Math.max(0, Math.round(v.maxCargo * (1.0 - progress)));
                const cratesThisFrame = Math.max(0, prevCargo - v.cargo);
                totalCratesLanded += cratesThisFrame;
                v.remainingSec = Math.max(0, v.unloadTimer);

                if (v.unloadTimer <= 0) {
                    v.departureDelay -= dt * timeScale;
                    if (v.departureDelay <= 0) {
                        if (v.assignedBerth) {
                            v.assignedBerth.occupiedBy = null;
                            v.assignedBerth = null;
                        }
                        v.isDocked = false;
                        v.state = 'Reverse Out';
                        v.reverseTimer = 3.0;
                        v.isReversing = true;
                    }
                }
            } else if (v.state === 'Reverse Out') {
                v.mesh.position.y = waveY * 0.7;
                v.isReversing = true;
                v.reverseTimer -= dt;
                updateVesselKinematics(v, v.mesh.position.x + 8, v.mesh.position.z, dt);

                if (v.reverseTimer <= 0 || v.mesh.position.x >= -14) {
                    v.isReversing = false;
                    v.state = 'Departing';
                    v.departStep = 1;
                    v.deepSeaTargetX = 280;
                    v.deepSeaTargetZ = -130 + Math.random() * 260;
                }
            } else if (v.state === 'Departing') {
                v.mesh.position.y = waveY * 0.7;
                let depX = 0;
                let depZ = 0;

                if (v.departStep === 1) {
                    // Fairway Center Corridor (X = 45)
                    depX = 45;
                    depZ = (v.mesh.position.z * 0.5) + v.laneOffset;
                    const d = updateVesselKinematics(v, depX, depZ, dt);
                    if (d < 12.0) v.departStep = 2;
                } else if (v.departStep === 2) {
                    // Outer Bay Gate (X = 165)
                    depX = 165;
                    depZ = 10 + v.laneOffset;
                    const d = updateVesselKinematics(v, depX, depZ, dt);
                    if (d < 14.0) v.departStep = 3;
                } else {
                    // Fanned Out Ocean Departure (X >= 235: loop into expedition)
                    depX = v.deepSeaTargetX;
                    depZ = v.deepSeaTargetZ;
                    updateVesselKinematics(v, depX, depZ, dt);

                    if (v.mesh.position.x >= 235) {
                        v.mesh.visible = false;
                        v.state = 'AT_SEA_FISHING';
                        v.speed = 0;
                        v.fishingTimer = computeFishingDuration(simTime);
                    }
                }
            }
        });

        // UPDATE SMALL BOAT FLEET (70% TENDERS + 30% INDEPENDENT)
        let activeBancas = 0;

        bancas.forEach(b => {
            const waveY = getWaveHeight(b.mesh.position.x, b.mesh.position.z, waveTime);
            b.mesh.position.y = waveY * 0.55;
            // Banca pitch/roll buoyancy
            b.mesh.rotation.x = Math.sin(waveTime * 2.5 + b.bobOffset) * 0.045;
            b.mesh.rotation.z = Math.cos(waveTime * 2.0 + b.bobOffset) * 0.03;

            const bowWake = b.mesh.getObjectByName('bowWake');
            if (bowWake) {
                bowWake.material.opacity = THREE.MathUtils.lerp(
                    bowWake.material.opacity,
                    Math.min(0.45, Math.abs(b.speed) * 0.08),
                    0.15
                );
            }
            // World-space wake ripples from banca stern
            if (Math.abs(b.speed) > 1.2) {
                b.wakeTimer = (b.wakeTimer || 0) + dt;
                if (b.wakeTimer > 0.12) {
                    b.wakeTimer = 0;
                    const wx = b.mesh.position.x - Math.sin(b.heading) * 2.4;
                    const wz = b.mesh.position.z - Math.cos(b.heading) * 2.4;
                    spawnWorldWake(wx, wz, 1.0, Math.min(1.0, Math.abs(b.speed) / b.maxSpeed));
                }
            }

            if (b.role === 'tender') {
                // ROLE A — PARTNER PICKUP TENDER FOR MEDIUM BOATS
                if (b.state === 'patrolling') {
                    // Cruise in the bay looking for anchored mother boats
                    const dist = updateVesselKinematics(b, b.patrolTargetX, b.patrolTargetZ, dt);
                    if (dist < 8.0) {
                        b.patrolTargetX = 90 + Math.random() * 50;
                        b.patrolTargetZ = -50 + Math.random() * 100;
                    }

                    const targetMB = vessels.find(v => v.mesh.visible && v.state === 'Waiting at Anchorage' && v.cargo > 0 && !v.servicedByBanca);
                    if (targetMB) {
                        targetMB.servicedByBanca = b.id;
                        b.targetBoat = targetMB;
                        b.state = 'to_anchorage';
                    }
                } else if (b.state === 'to_anchorage') {
                    activeBancas++;
                    if (!b.targetBoat || b.targetBoat.cargo <= 0 || !b.targetBoat.mesh.visible) {
                        b.state = 'patrolling';
                        b.targetBoat = null;
                        return;
                    }
                    const tx = b.targetBoat.mesh.position.x - 4.5;
                    const tz = b.targetBoat.mesh.position.z;
                    const dist = updateVesselKinematics(b, tx, tz, dt);

                    if (dist < 3.8) {
                        b.state = 'transferring';
                        b.transferTimer = 6.0 + Math.random() * 3.0; // 6 to 9 seconds!
                        b.speed = 0;
                    }
                } else if (b.state === 'transferring') {
                    activeBancas++;
                    b.speed = 0;
                    b.transferTimer -= dt * timeScale;

                    if (b.transferTimer <= 0) {
                        const take = Math.min(b.maxCargo, b.targetBoat ? b.targetBoat.cargo : 0);
                        b.cargo = take;
                        if (b.targetBoat) {
                            b.targetBoat.cargo -= take;
                            b.targetBoat.servicedByBanca = null;
                            // Sync crate visuals on mother vessel
                            updateVesselCrateVisuals(b.targetBoat);
                            if (b.targetBoat.cargo <= 0) {
                                // Mother vessel relieved — departs to sea
                                b.targetBoat.state = 'Departing';
                                b.targetBoat.departStep = 1;
                                b.targetBoat.deepSeaTargetX = 280;
                                b.targetBoat.deepSeaTargetZ = -130 + Math.random() * 260;
                            }
                        }
                        // Sync crate visuals on banca (now loaded)
                        updateBancaCrateVisuals(b);
                        b.targetBoat = null;
                        b.state = 'to_wharf';
                    }
                } else if (b.state === 'to_wharf') {
                    activeBancas++;
                    // Navigate to open landing spot on front wharf apron (X = -28.0)
                    const landing = BANCA_LANDING_SPOTS[b.landingSlotIdx % BANCA_LANDING_SPOTS.length];
                    const dist = updateVesselKinematics(b, landing.x, landing.z, dt);

                    if (dist < 3.0) {
                        b.mesh.position.set(landing.x, 0, landing.z);
                        b.heading = 0;
                        b.mesh.rotation.y = 0;
                        b.speed = 0;
                        b.isDocked = true;
                        b.state = 'unloading_at_wharf';
                        b.unloadTimer = 8.0 + Math.random() * 4.0; // 8 to 12 seconds!
                    }
                } else if (b.state === 'unloading_at_wharf') {
                    activeBancas++;
                    b.isDocked = true;
                    b.speed = 0;
                    b.mesh.position.x = -28.0;
                    b.unloadTimer -= dt * timeScale;

                    if (b.unloadTimer <= 0) {
                        totalCratesLanded += b.cargo;
                        b.cargo = 0;
                        updateBancaCrateVisuals(b); // Hide crates once empty
                        b.isDocked = false;
                        b.state = 'reversing_from_wharf';
                        b.reverseTimer = 2.0;
                        b.isReversing = true;
                    }
                } else if (b.state === 'reversing_from_wharf') {
                    activeBancas++;
                    b.isReversing = true;
                    b.reverseTimer -= dt;
                    updateVesselKinematics(b, b.mesh.position.x + 8, b.mesh.position.z, dt);

                    if (b.reverseTimer <= 0 || b.mesh.position.x >= -16) {
                        b.isReversing = false;
                        b.state = 'patrolling';
                        b.patrolTargetX = 90 + Math.random() * 50;
                        b.patrolTargetZ = -50 + Math.random() * 100;
                    }
                }
            } else {
                // ROLE B — INDEPENDENT ARTISANAL FISHING BANCA
                if (b.state === 'to_wharf') {
                    activeBancas++;
                    const landing = BANCA_LANDING_SPOTS[b.landingSlotIdx % BANCA_LANDING_SPOTS.length];
                    const dist = updateVesselKinematics(b, landing.x, landing.z, dt);

                    if (dist < 3.0) {
                        b.mesh.position.set(landing.x, 0, landing.z);
                        b.heading = 0;
                        b.mesh.rotation.y = 0;
                        b.speed = 0;
                        b.isDocked = true;
                        b.state = 'unloading_at_wharf';
                        b.unloadTimer = 10.0 + Math.random() * 5.0; // 10 to 15 seconds!
                    }
                } else if (b.state === 'unloading_at_wharf') {
                    activeBancas++;
                    b.isDocked = true;
                    b.speed = 0;
                    b.mesh.position.x = -28.0;
                    b.unloadTimer -= dt * timeScale;

                    if (b.unloadTimer <= 0) {
                        totalCratesLanded += b.cargo;
                        b.cargo = 0;
                        b.isDocked = false;
                        b.state = 'reversing_from_wharf';
                        b.reverseTimer = 2.5;
                        b.isReversing = true;
                    }
                } else if (b.state === 'reversing_from_wharf') {
                    activeBancas++;
                    b.isReversing = true;
                    b.reverseTimer -= dt;
                    updateVesselKinematics(b, b.mesh.position.x + 8, b.mesh.position.z, dt);

                    if (b.reverseTimer <= 0 || b.mesh.position.x >= -16) {
                        b.isReversing = false;
                        b.state = 'to_sea';
                        b.patrolTargetX = 240;
                        b.patrolTargetZ = -70 + Math.random() * 140;
                    }
                } else if (b.state === 'to_sea') {
                    activeBancas++;
                    const dist = updateVesselKinematics(b, b.patrolTargetX, b.patrolTargetZ, dt);
                    if (b.mesh.position.x >= 230 || dist < 10) {
                        b.state = 'at_sea_fishing';
                        b.seaTimer = 20.0 + Math.random() * 25.0;
                        b.mesh.visible = false;
                    }
                } else if (b.state === 'at_sea_fishing') {
                    b.seaTimer -= dt * timeScale;
                    if (b.seaTimer <= 0) {
                        b.cargo = Math.floor(15 + Math.random() * 20);
                        b.mesh.position.set(220, 0, -60 + Math.random() * 120);
                        b.heading = -Math.PI / 2;
                        b.mesh.rotation.y = b.heading;
                        b.mesh.visible = true;
                        b.state = 'to_wharf';
                    }
                }
            }
        });

        // UPDATE HUD KPI METRICS
        document.getElementById('kpi-queue-count').textContent = waitingCount;
        document.getElementById('kpi-wait-time').textContent = (waitingCount > 0 ? (1.2 + waitingCount * 0.45).toFixed(2) : '0.00');

        const berthUtil = (occupiedCount / numBerths) * 100;
        document.getElementById('kpi-berth-util').textContent = berthUtil.toFixed(1);
        document.getElementById('kpi-berth-occ').textContent = occupiedCount;
        document.getElementById('kpi-berth-total').textContent = numBerths;

        document.getElementById('kpi-at-sea-count').textContent = atSeaCount;
        document.getElementById('kpi-bancas-active').textContent = activeBancas;
        document.getElementById('kpi-bancas-moored').textContent = (bancas.length - activeBancas);

        document.getElementById('kpi-crates-count').textContent = Math.round(totalCratesLanded).toLocaleString();
        const qualityRetention = Math.max(75, 100 * Math.exp(-0.028 * (waitingCount * 0.45)));
        document.getElementById('kpi-quality-score').textContent = qualityRetention.toFixed(1);
    }

    // -------------------------------------------------------------
    // THREE.JS RENDER LOOP
    // -------------------------------------------------------------
    function render(time) {
        const deltaMs = time - lastTime;
        lastTime = time;

        const timeDelta = Math.min(deltaMs / 1000, 0.1);
        const waveTime = time * 0.002;

        if (isPlaying) {
            const deltaHours = timeDelta * (timeScale * 0.15);
            updateSimulation(deltaHours, timeDelta, waveTime);
        }

        // Advance world-space wake particle pool (expand + fade)
        updateWorldWakeParticles(timeDelta);

        // Ocean Wave Mesh Motion
        const pAttr = waterGeo.attributes.position;
        for (let i = 0; i < pAttr.count; i++) {
            const bv = baseVerts[i];
            const waveZ = Math.sin(bv.x * 0.04 + waveTime * 2.2) * 0.6 +
                          Math.cos(bv.y * 0.05 + waveTime * 1.8) * 0.45;
            pAttr.setZ(i, waveZ);
        }
        pAttr.needsUpdate = true;

        // Rotate Lighthouse Head at Top Lantern Room (Y = 20.5)
        LightRotorPivot.rotation.y += timeDelta * 0.8;

        controls.update();
        renderer.render(scene, camera);
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);

    // -------------------------------------------------------------
    // RAYCASTING & CATCH INDICATOR TOOLTIP
    // -------------------------------------------------------------
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    const tooltip = document.getElementById('vessel-tooltip');
    const ttName = document.getElementById('tt-vessel-name');
    const ttBadge = document.getElementById('tt-vessel-badge');
    const ttType = document.getElementById('tt-vessel-type');
    const ttGT = document.getElementById('tt-vessel-gt');
    const ttDraft = document.getElementById('tt-vessel-draft');
    const ttCargo = document.getElementById('tt-vessel-cargo');
    const ttBar = document.getElementById('tt-vessel-bar');
    const ttState = document.getElementById('tt-vessel-state');
    const ttTimer = document.getElementById('tt-vessel-timer');

    window.addEventListener('mousemove', (e) => {
        mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);

        const mediumMeshes = vessels.filter(v => v.mesh.visible).map(v => v.mesh);
        const bancaMeshes = bancas.filter(b => b.mesh.visible).map(b => b.mesh);
        const allMeshes = mediumMeshes.concat(bancaMeshes);

        const intersects = raycaster.intersectObjects(allMeshes, true);

        if (intersects.length > 0) {
            let hitGroup = intersects[0].object;
            while (hitGroup.parent && hitGroup.parent !== scene) {
                hitGroup = hitGroup.parent;
            }

            const foundMedium = vessels.find(v => v.mesh === hitGroup);
            const foundBanca = bancas.find(b => b.mesh === hitGroup);

            if (foundMedium) {
                ttName.textContent = foundMedium.name;
                ttType.textContent = foundMedium.type + ` (${foundMedium.tier})`;
                ttGT.textContent = foundMedium.gt + ' GT';
                ttDraft.textContent = foundMedium.draft + ' m';
                ttCargo.textContent = Math.round(foundMedium.cargo) + ' / ' + foundMedium.maxCargo + ' banyeras';
                const pct = Math.min(100, Math.round((foundMedium.cargo / Math.max(1, foundMedium.maxCargo)) * 100));
                ttBar.style.width = pct + '%';

                if (foundMedium.state === 'Unloading at Wharf') {
                    ttBadge.textContent = 'Direct Docked';
                    ttBadge.style.background = 'rgba(16, 185, 129, 0.2)';
                    ttBadge.style.color = '#34D399';
                    ttState.textContent = 'Unloading at ' + (foundMedium.assignedBerth ? foundMedium.assignedBerth.name : 'Wharf');
                    ttTimer.textContent = `${Math.ceil(foundMedium.remainingSec)}s remaining`;
                } else if (foundMedium.state === 'Waiting at Anchorage') {
                    ttBadge.textContent = 'Bay Anchorage';
                    ttBadge.style.background = 'rgba(245, 158, 11, 0.2)';
                    ttBadge.style.color = '#FBBF24';
                    ttState.textContent = foundMedium.servicedByBanca ? 'Tender Transfer in Progress' : 'Convenience Bay Holding';
                    ttTimer.textContent = `${Math.round(foundMedium.cargo)} banyeras aboard`;
                } else {
                    ttBadge.textContent = foundMedium.state;
                    ttBadge.style.background = 'rgba(56, 189, 248, 0.2)';
                    ttBadge.style.color = '#38BDF8';
                    ttState.textContent = foundMedium.state;
                    ttTimer.textContent = 'In transit';
                }

                tooltip.style.left = e.clientX + 'px';
                tooltip.style.top = e.clientY + 'px';
                tooltip.style.display = 'block';
                return;
            } else if (foundBanca) {
                ttName.textContent = foundBanca.name;
                ttType.textContent = foundBanca.type;
                ttGT.textContent = foundBanca.gt + ' GT';
                ttDraft.textContent = foundBanca.draft + ' m';
                ttCargo.textContent = foundBanca.cargo + ' / ' + foundBanca.maxCargo + ' banyeras';
                const pct = Math.min(100, Math.round((foundBanca.cargo / foundBanca.maxCargo) * 100));
                ttBar.style.width = pct + '%';

                if (foundBanca.role === 'tender') {
                    if (foundBanca.state === 'transferring') {
                        ttBadge.textContent = 'Partner Tender';
                        ttBadge.style.background = 'rgba(245, 158, 11, 0.2)';
                        ttBadge.style.color = '#FBBF24';
                        ttState.textContent = 'Loading Crates from ' + (foundBanca.targetBoat ? foundBanca.targetBoat.name : 'Mother Boat');
                        ttTimer.textContent = `${Math.ceil(foundBanca.transferTimer)}s loading`;
                    } else if (foundBanca.state === 'to_wharf') {
                        ttBadge.textContent = 'Lightering Shuttle';
                        ttBadge.style.background = 'rgba(56, 189, 248, 0.2)';
                        ttBadge.style.color = '#38BDF8';
                        ttState.textContent = 'Delivering Banyeras to Front Wharf';
                        ttTimer.textContent = `${foundBanca.cargo} banyeras loaded`;
                    } else if (foundBanca.state === 'unloading_at_wharf') {
                        ttBadge.textContent = 'Apron Landing';
                        ttBadge.style.background = 'rgba(16, 185, 129, 0.2)';
                        ttBadge.style.color = '#34D399';
                        ttState.textContent = 'Offloading at Front Wharf Apron';
                        ttTimer.textContent = `${Math.ceil(foundBanca.unloadTimer)}s remaining`;
                    } else {
                        ttBadge.textContent = 'Partner Tender';
                        ttBadge.style.background = 'rgba(148, 163, 184, 0.2)';
                        ttBadge.style.color = '#94A3B8';
                        ttState.textContent = 'Patrolling Bay for Mother Boats';
                        ttTimer.textContent = 'Standby in Harbor';
                    }
                } else {
                    ttBadge.textContent = 'Artisanal Banca';
                    ttBadge.style.background = 'rgba(56, 189, 248, 0.2)';
                    ttBadge.style.color = '#38BDF8';
                    ttState.textContent = foundBanca.state === 'unloading_at_wharf' ? 'Unloading Catch at Pier' : 'Artisanal Fishing';
                    ttTimer.textContent = `${foundBanca.cargo} banyeras`;
                }

                tooltip.style.left = e.clientX + 'px';
                tooltip.style.top = e.clientY + 'px';
                tooltip.style.display = 'block';
                return;
            }
        }
        tooltip.style.display = 'none';
    });

    // -------------------------------------------------------------
    // UI CONTROLS & EXPANDABLE FLEET SETTINGS LISTENERS
    // -------------------------------------------------------------
    const btnPlay = document.getElementById('btn-play');
    btnPlay.addEventListener('click', () => {
        isPlaying = !isPlaying;
        btnPlay.textContent = isPlaying ? '⏸ Pause' : '▶ Play';
        btnPlay.className = isPlaying ? 'btn-hud primary' : 'btn-hud';
    });

    document.getElementById('btn-reset').addEventListener('click', () => {
        simTime = 5.75;
        totalCratesLanded = 1420;
        initFleet();
    });

    document.querySelectorAll('.speed-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            timeScale = parseFloat(btn.dataset.speed);
        });
    });

    document.getElementById('btn-open-settings').addEventListener('click', () => {
        document.getElementById('modal-settings').style.display = 'flex';
    });
    document.getElementById('btn-open-analytics').addEventListener('click', () => {
        document.getElementById('modal-analytics').style.display = 'flex';
    });
    document.querySelectorAll('.modal-close').forEach(btn => {
        btn.addEventListener('click', () => {
            document.getElementById(btn.dataset.target).style.display = 'none';
        });
    });
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal-overlay')) {
            e.target.style.display = 'none';
        }
    });

    document.querySelectorAll('.modal-tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.modal-tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });

    // Fleet Scale Sliders
    const slMediumFleet = document.getElementById('sl-medium-fleet');
    slMediumFleet.addEventListener('input', (e) => {
        targetTotalMediumFleet = parseInt(e.target.value);
        document.getElementById('val-medium-fleet').textContent = targetTotalMediumFleet + ' craft';
        initFleet();
    });

    const slBancasFleet = document.getElementById('sl-bancas-fleet');
    slBancasFleet.addEventListener('input', (e) => {
        targetTotalBancas = parseInt(e.target.value);
        document.getElementById('val-bancas-fleet').textContent = targetTotalBancas + ' craft';
        initFleet();
    });

    const slUnloadScale = document.getElementById('sl-unload-scale');
    slUnloadScale.addEventListener('input', (e) => {
        unloadDurationScale = parseFloat(e.target.value);
        document.getElementById('val-unload-scale').textContent = `${(unloadDurationScale * 5).toFixed(0)}–${(unloadDurationScale * 12).toFixed(0)}s`;
    });

    const slBerths = document.getElementById('sl-berths');
    slBerths.addEventListener('input', (e) => {
        numBerths = parseInt(e.target.value);
        document.getElementById('val-berths').textContent = numBerths + ' berths';
        initBerths();
    });
    const chkTide = document.getElementById('chk-tide');
    chkTide.addEventListener('change', (e) => {
        tideLockActive = e.target.checked;
    });

    document.querySelectorAll('.preset-card').forEach(card => {
        card.addEventListener('click', () => {
            document.querySelectorAll('.preset-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            const p = card.dataset.preset;
            const badge = document.getElementById('badge-scenario');

            if (p === 'baseline') {
                numBerths = 13;
                targetTotalMediumFleet = 12;
                targetTotalBancas = 8;
                tideLockActive = true;
                badge.textContent = 'Baseline (13 Berths)';
            } else if (p === 'interventionA') {
                numBerths = 16;
                targetTotalMediumFleet = 18;
                targetTotalBancas = 12;
                unloadDurationScale = 1.8; // +50% offload speed
                tideLockActive = true;
                badge.textContent = 'Intervention A: 16 Berths';
            } else if (p === 'interventionB') {
                numBerths = 13;
                targetTotalMediumFleet = 12;
                targetTotalBancas = 8;
                tideLockActive = false;
                badge.textContent = 'Intervention B: Dredging';
            } else if (p === 'interventionC') {
                numBerths = 13;
                targetTotalMediumFleet = 12;
                targetTotalBancas = 8;
                tideLockActive = true;
                badge.textContent = 'Intervention C: Staggered';
            }
            slBerths.value = numBerths;
            document.getElementById('val-berths').textContent = numBerths + ' berths';
            slMediumFleet.value = targetTotalMediumFleet;
            document.getElementById('val-medium-fleet').textContent = targetTotalMediumFleet + ' craft';
            slBancasFleet.value = targetTotalBancas;
            document.getElementById('val-bancas-fleet').textContent = targetTotalBancas + ' craft';
            chkTide.checked = tideLockActive;
            initBerths();
            initFleet();
        });
    });

    const btnScreenshot = document.getElementById('btn-screenshot-mode');
    const restoreBtn = document.getElementById('screenshot-restore-btn');

    btnScreenshot.addEventListener('click', () => {
        document.getElementById('modal-analytics').style.display = 'none';
        document.body.classList.add('screenshot-mode');
    });

    function exitScreenshotMode() {
        document.body.classList.remove('screenshot-mode');
    }
    restoreBtn.addEventListener('click', exitScreenshotMode);
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') exitScreenshotMode();
    });

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

})();
</script>
</body>
</html>
"""
