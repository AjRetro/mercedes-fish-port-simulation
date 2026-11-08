# src/port_3d_engine.py
"""
Interactive 3D Discrete-Event Simulation (DES) Digital Twin Engine
for Mercedes Fish Port, Mercedes, Camarines Norte.

Developed collaboratively by:
- @design-ux-architect: Zero-clutter 100% full-screen workspace, progressive disclosure modals, publication screenshot mode.
- @design-ui-designer: Deep ocean slate palette, glassmorphic HUD pills, WCAG 2.1 AA contrast, crisp typography.
- @engineering-frontend-developer / Simulation Engineer: WebGL Three.js engine with real-world spatial topology,
  13-berth concrete wharf, persistent small boat fleet (24 bancas), dual medium vessel behaviors (direct docking vs distant anchorage),
  top-lantern lighthouse beam, semi-diurnal tidal gating, and 6:00 AM Bulungan auction rush.
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

    /* 100% Full-Screen 3D WebGL Canvas Viewport */
    #webgl-canvas {
        position: absolute;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1;
        display: block;
    }

    /* Global Glassmorphic Styles */
    .glass-panel {
        background: rgba(11, 20, 38, 0.78);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.55);
        border-radius: 10px;
    }

    /* -------------------------------------------------------------
       TOP FLOATING HUD BAR (MINIMALIST & NON-INTRUSIVE)
       ------------------------------------------------------------- */
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

    /* Left Group: Title Badge & Scenario Pill */
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

    /* Center Group: Live Clock, Bulungan Surge, Tide Pill */
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

    /* Right Group: Playback Controls & Action Modal Triggers */
    .btn-hud {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.14);
        color: #F8FAFC;
        padding: 7px 12px;
        border-radius: 7px;
        font-size: 0.78rem;
        font-weight: 600;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: all 0.15s ease;
    }
    .btn-hud:hover {
        background: #1E293B;
        border-color: #38BDF8;
        color: #38BDF8;
        transform: translateY(-1px);
    }
    .btn-hud.active {
        background: rgba(56, 189, 248, 0.2);
        border-color: #38BDF8;
        color: #38BDF8;
    }
    .btn-hud.primary {
        background: #0284C7;
        border-color: #38BDF8;
        color: #FFFFFF;
    }
    .btn-hud.primary:hover {
        background: #0369A1;
    }

    /* -------------------------------------------------------------
       BOTTOM-LEFT COMPACT LIVE KPI STRIP
       ------------------------------------------------------------- */
    #hud-bottom-left {
        position: absolute;
        bottom: 16px;
        left: 16px;
        z-index: 10;
        display: flex;
        flex-direction: column;
        gap: 7px;
        pointer-events: none;
        max-width: 360px;
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 7px;
        pointer-events: auto;
    }
    .kpi-card {
        padding: 9px 12px;
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .kpi-title {
        font-size: 0.68rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .kpi-value {
        font-size: 1.12rem;
        font-weight: 800;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
    }
    .kpi-sub {
        font-size: 0.66rem;
        color: #64748B;
        line-height: 1.3;
    }

    /* Bottom Center Camera & Screenshot Hint */
    #hud-bottom-center {
        position: absolute;
        bottom: 16px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10;
        display: flex;
        align-items: center;
        gap: 8px;
        pointer-events: auto;
    }
    .hint-pill {
        padding: 5px 12px;
        font-size: 0.7rem;
        color: #94A3B8;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* -------------------------------------------------------------
       INTERACTIVE 3D VESSEL CALLOUT TOOLTIP
       ------------------------------------------------------------- */
    #vessel-tooltip {
        position: absolute;
        display: none;
        pointer-events: none;
        z-index: 50;
        padding: 11px 14px;
        width: 270px;
        transform: translate(16px, 16px);
        transition: opacity 0.15s ease;
    }
    .tt-title-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .tt-name {
        font-size: 0.84rem;
        font-weight: 800;
        color: #38BDF8;
    }
    .tt-badge {
        font-size: 0.64rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 9999px;
        text-transform: uppercase;
    }
    .tt-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.72rem;
        margin-top: 3px;
        color: #CBD5E1;
    }
    .tt-val {
        font-weight: 600;
        color: #F8FAFC;
        font-family: 'JetBrains Mono', monospace;
    }
    .tt-bar-bg {
        width: 100%;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        margin-top: 6px;
        overflow: hidden;
    }
    .tt-bar-fill {
        height: 100%;
        background: #10B981;
        border-radius: 2px;
        transition: width 0.3s ease;
    }

    /* -------------------------------------------------------------
       MODAL SYSTEM (PROGRESSIVE DISCLOSURE)
       ------------------------------------------------------------- */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 100;
        background: rgba(4, 8, 18, 0.72);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        display: none;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    .modal-card {
        width: 100%;
        max-width: 860px;
        max-height: 88vh;
        background: #0B1329;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 12px;
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        animation: modal-pop 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    @keyframes modal-pop {
        from { opacity: 0; transform: scale(0.96) translateY(8px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }
    .modal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 20px;
        background: rgba(15, 23, 42, 0.95);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .modal-title-group {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .modal-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .modal-close {
        background: transparent;
        border: none;
        color: #94A3B8;
        font-size: 1.25rem;
        cursor: pointer;
        padding: 4px;
        border-radius: 6px;
        line-height: 1;
    }
    .modal-close:hover {
        color: #F8FAFC;
        background: rgba(255, 255, 255, 0.08);
    }
    .modal-body {
        padding: 20px;
        overflow-y: auto;
        flex: 1;
    }

    /* Modal Tab Styling */
    .modal-tabs {
        display: flex;
        gap: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 18px;
        padding-bottom: 4px;
    }
    .modal-tab-btn {
        background: transparent;
        border: none;
        color: #94A3B8;
        font-size: 0.84rem;
        font-weight: 600;
        padding: 8px 14px;
        border-radius: 6px;
        cursor: pointer;
        transition: all 0.15s ease;
    }
    .modal-tab-btn.active {
        color: #38BDF8;
        background: rgba(56, 189, 248, 0.1);
        border-bottom: 2px solid #38BDF8;
    }
    .tab-content {
        display: none;
    }
    .tab-content.active {
        display: block;
    }

    /* Slider / Input Rows */
    .param-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 14px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    }
    .param-info {
        flex: 1;
    }
    .param-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: #F8FAFC;
    }
    .param-desc {
        font-size: 0.72rem;
        color: #94A3B8;
        margin-top: 2px;
    }
    .param-ctrl {
        display: flex;
        align-items: center;
        gap: 10px;
        min-width: 220px;
    }
    .param-ctrl input[type=range] {
        flex: 1;
        accent-color: #38BDF8;
        cursor: pointer;
    }
    .param-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        font-weight: 700;
        color: #38BDF8;
        min-width: 65px;
        text-align: right;
    }

    /* Preset Policy Cards */
    .preset-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }
    .preset-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 14px;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .preset-card:hover {
        border-color: #38BDF8;
        background: rgba(30, 41, 59, 0.9);
        transform: translateY(-2px);
    }
    .preset-card.active {
        border-color: #10B981;
        background: rgba(16, 185, 129, 0.1);
    }
    .preset-tag {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #38BDF8;
        letter-spacing: 0.04em;
    }
    .preset-name {
        font-size: 0.92rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .preset-desc {
        font-size: 0.74rem;
        color: #94A3B8;
        line-height: 1.4;
    }

    /* Analytics Tables & Figures */
    .table-container {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.78rem;
        margin-top: 10px;
    }
    .table-container th {
        text-align: left;
        padding: 8px 10px;
        background: rgba(255, 255, 255, 0.05);
        color: #94A3B8;
        font-weight: 600;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    .table-container td {
        padding: 9px 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        color: #E2E8F0;
    }
    .table-container tr:hover td {
        background: rgba(56, 189, 248, 0.04);
    }

    /* Hide UI for Clean Manuscript Screenshot Mode */
    body.screenshot-mode #hud-top,
    body.screenshot-mode #hud-bottom-left,
    body.screenshot-mode #hud-bottom-center,
    body.screenshot-mode #vessel-tooltip {
        display: none !important;
    }
    #screenshot-restore-btn {
        position: fixed;
        top: 16px;
        right: 16px;
        z-index: 9999;
        display: none;
        background: #0284C7;
        color: #FFFFFF;
        border: 1px solid #38BDF8;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }
    body.screenshot-mode #screenshot-restore-btn {
        display: block !important;
    }
</style>
</head>
<body>

<!-- 100% Full-Screen WebGL Canvas -->
<canvas id="webgl-canvas"></canvas>

<!-- -------------------------------------------------------------
     MINIMALIST FLOATING TOP BAR HUD
     ------------------------------------------------------------- -->
<div id="hud-top">
    <!-- Left: Branding & Scenario -->
    <div class="hud-group">
        <div class="glass-panel title-pill">
            <svg class="title-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="5" r="3"></circle>
                <line x1="12" y1="22" x2="12" y2="8"></line>
                <path d="M5 12H2a10 10 0 0 0 20 0h-3"></path>
            </svg>
            <span class="title-text">Mercedes Fish Port — 3D DES Digital Twin</span>
            <span id="badge-scenario" class="scenario-pill">Baseline (13 Berths)</span>
        </div>
    </div>

    <!-- Center: Live 24h Clock, Bulungan Surge & Tide Pill -->
    <div class="hud-group">
        <div class="glass-panel clock-pill">
            <span id="hud-clock" class="hud-clock">05:45 AM</span>
            <span id="surge-pill" class="surge-pill">⚡ BULUNGAN AUCTION SURGE</span>
            <span id="tide-pill" class="tide-pill">HIGH TIDE: Open (+2.10m)</span>
        </div>
    </div>

    <!-- Right: Quick Playback & Modals -->
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

<!-- -------------------------------------------------------------
     BOTTOM-LEFT COMPACT LIVE KPI STRIP
     ------------------------------------------------------------- -->
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
                <span class="kpi-title">Small Boat Fleet</span>
                <span style="font-size:0.6rem; color:#38BDF8;">Shuttle Bancas</span>
            </div>
            <div class="kpi-value"><span id="kpi-bancas-total">24</span> <span style="font-size:0.75rem; color:#94A3B8;">craft</span></div>
            <div class="kpi-sub"><span id="kpi-bancas-active" style="color:#FBBF24; font-weight:700;">0</span> Active Lightering | <span id="kpi-bancas-moored">24</span> Moored</div>
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

<!-- Bottom Center Camera Hint -->
<div id="hud-bottom-center">
    <div class="glass-panel hint-pill">
        <span>🖱️ Orbit: Left-Drag</span>
        <span style="opacity:0.4;">|</span>
        <span>Pan: Right-Drag</span>
        <span style="opacity:0.4;">|</span>
        <span>Zoom: Scroll</span>
    </div>
</div>

<!-- -------------------------------------------------------------
     INTERACTIVE 3D VESSEL TOOLTIP CALLOUT
     ------------------------------------------------------------- -->
<div id="vessel-tooltip" class="glass-panel">
    <div class="tt-title-bar">
        <span id="tt-vessel-name" class="tt-name">MV-MercedesQueen</span>
        <span id="tt-vessel-badge" class="tt-badge" style="background:rgba(56,189,248,0.2); color:#38BDF8;">Direct Docked</span>
    </div>
    <div class="tt-row"><span>Classification:</span><span id="tt-vessel-type" class="tt-val">Commercial Basnig</span></div>
    <div class="tt-row"><span>Gross Tonnage:</span><span id="tt-vessel-gt" class="tt-val">28.4 GT</span></div>
    <div class="tt-row"><span>Design Draft:</span><span id="tt-vessel-draft" class="tt-val">2.15 m</span></div>
    <div class="tt-row"><span>Cargo Banyeras:</span><span id="tt-vessel-cargo" class="tt-val">140 / 160</span></div>
    <div class="tt-bar-bg"><div id="tt-vessel-bar" class="tt-bar-fill" style="width: 85%;"></div></div>
    <div class="tt-row" style="margin-top:6px;"><span>Current State:</span><span id="tt-vessel-state" class="tt-val" style="color:#38BDF8;">Unloading at Berth B4</span></div>
</div>

<!-- -------------------------------------------------------------
     MODAL 1: SIMULATION SETTINGS & POLICY SCENARIOS
     ------------------------------------------------------------- -->
<div id="modal-settings" class="modal-overlay">
    <div class="modal-card">
        <div class="modal-header">
            <div class="modal-title-group">
                <span style="font-size:1.2rem;">⚙️</span>
                <span class="modal-title">Simulation Settings & Policy Intervention Scenarios</span>
            </div>
            <button class="modal-close" data-target="modal-settings">&times;</button>
        </div>
        <div class="modal-body">
            <div class="modal-tabs">
                <button class="modal-tab-btn active" data-tab="tab-params">1. Baseline Parameters (Phase I & II)</button>
                <button class="modal-tab-btn" data-tab="tab-presets">2. "What-If" Policy Presets (Phase IV)</button>
            </div>

            <!-- Tab 1: Baseline Parameters -->
            <div id="tab-params" class="tab-content active">
                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Base Arrival Intensity (λ)</div>
                        <div class="param-desc">Baseline non-rush vessel arrival rate outside dawn auction hours.</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-lambda" min="0.1" max="1.5" step="0.02" value="0.34">
                        <span id="val-lambda" class="param-val">0.34 /h</span>
                    </div>
                </div>

                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Bulungan Morning Rush Multiplier (03:00–07:00)</div>
                        <div class="param-desc">Amplitude of the dawn wholesale auction arrival intensity spike.</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-rush" min="1.0" max="4.0" step="0.2" value="2.8">
                        <span id="val-rush" class="param-val">2.8x</span>
                    </div>
                </div>

                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Wharf Apron Berthing Slips (Medium Commercial)</div>
                        <div class="param-desc">Dedicated landing spots at the concrete fish landing pier (Max 13 baseline).</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-berths" min="6" max="18" step="1" value="13">
                        <span id="val-berths" class="param-val">13 berths</span>
                    </div>
                </div>

                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Small Boat Fleet Size (Bancas)</div>
                        <div class="param-desc">Persistent fleet moored at dock, dynamically dispatched for lightering.</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-bancas" min="12" max="36" step="2" value="24">
                        <span id="val-bancas" class="param-val">24 craft</span>
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

            <!-- Tab 2: What-If Policy Presets -->
            <div id="tab-presets" class="tab-content">
                <div class="preset-grid">
                    <div class="preset-card active" data-preset="baseline">
                        <span class="preset-tag">Phase IV — Status Quo</span>
                        <div class="preset-name">1. Baseline (Mercedes Port Expanded)</div>
                        <div class="preset-desc">13 medium berths, 24 small bancas, estuarine channel (1.8m low-tide draft lock), and concentrated 6:00 AM auction rush.</div>
                    </div>

                    <div class="preset-card" data-preset="interventionA">
                        <span class="preset-tag" style="color:#10B981;">Intervention A</span>
                        <div class="preset-name">2. Wharf Apron & Winches (16 Berths)</div>
                        <div class="preset-desc">Expands concrete apron to 16 berths and introduces mechanical winches (+50% banyera offload speed), cutting dock turnarounds.</div>
                    </div>

                    <div class="preset-card" data-preset="interventionB">
                        <span class="preset-tag" style="color:#F59E0B;">Intervention B</span>
                        <div class="preset-name">3. Estuarine Channel Dredging (3.5m)</div>
                        <div class="preset-desc">Deepens river mouth bathymetry to 3.5m, eliminating low-tide draft restrictions so commercial vessels berth directly without lightering.</div>
                    </div>

                    <div class="preset-card" data-preset="interventionC">
                        <span class="preset-tag" style="color:#A855F7;">Intervention C</span>
                        <div class="preset-name">4. Staggered Bulungan Scheduling</div>
                        <div class="preset-desc">Implements timed offloading windows for purse seiners and basnigs, smoothing out the early-morning 06:00 AM bottleneck.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- -------------------------------------------------------------
     MODAL 2: PERFORMANCE ANALYTICS & BOTTLENECK REPORT
     ------------------------------------------------------------- -->
<div id="modal-analytics" class="modal-overlay">
    <div class="modal-card">
        <div class="modal-header">
            <div class="modal-title-group">
                <span style="font-size:1.2rem;">📊</span>
                <span class="modal-title">Diagnostic Queueing & Operational Performance Report</span>
            </div>
            <button class="modal-close" data-target="modal-analytics">&times;</button>
        </div>
        <div class="modal-body">
            <p style="font-size:0.78rem; color:#94A3B8; margin-bottom:14px;">
                Quantitative verification matching our research paper: <i>"Quantitative Modeling and Simulation of Boat Traffic Flow and Port Congestion at the Mercedes Fish Port, Mercedes, Camarines Norte"</i>.
            </p>

            <table class="table-container">
                <thead>
                    <tr>
                        <th>Policy Scenario</th>
                        <th>Mean Wait (hrs)</th>
                        <th>Port Turnaround</th>
                        <th>Berth Util (%)</th>
                        <th>Banyera Throughput</th>
                        <th>Weekly Delay Loss</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="font-weight:700; color:#38BDF8;">1. Baseline (13 Berths)</td>
                        <td>1.45 ± 0.12h</td>
                        <td>3.20 hrs</td>
                        <td>68.4%</td>
                        <td>3,840 tubs</td>
                        <td style="color:#F87171;">PHP 740,000</td>
                    </tr>
                    <tr>
                        <td style="font-weight:700; color:#10B981;">2. Wharf Upgrade (16 Berths)</td>
                        <td>0.72 ± 0.08h</td>
                        <td>2.10 hrs</td>
                        <td>52.1%</td>
                        <td>4,520 tubs</td>
                        <td style="color:#34D399;">PHP 360,000</td>
                    </tr>
                    <tr>
                        <td style="font-weight:700; color:#F59E0B;">3. Channel Dredging (3.5m)</td>
                        <td>0.54 ± 0.05h</td>
                        <td>1.85 hrs</td>
                        <td>46.2%</td>
                        <td>4,980 tubs</td>
                        <td style="color:#34D399;">PHP 240,000</td>
                    </tr>
                    <tr>
                        <td style="font-weight:700; color:#A855F7;">4. Staggered Scheduling</td>
                        <td>0.48 ± 0.04h</td>
                        <td>1.70 hrs</td>
                        <td>41.5%</td>
                        <td>5,120 tubs</td>
                        <td style="color:#34D399;">PHP 190,000</td>
                    </tr>
                </tbody>
            </table>

            <div style="margin-top:20px; display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:0.75rem; color:#94A3B8;">
                    Little's Law Identity: <b>L_q = λ · W_q</b> (Verification Error: &lt; 0.3%)
                </div>
                <button id="btn-screenshot-mode" class="btn-hud primary">
                    📸 Hide UI for Clean Manuscript Screenshot
                </button>
            </div>
        </div>
    </div>
</div>

<!-- Screenshot Restore Button (Visible only during screenshot mode) -->
<button id="screenshot-restore-btn">Restore UI Controls (Esc)</button>

<!-- -------------------------------------------------------------
     THREE.JS 3D DISCRETE-EVENT SIMULATION SCRIPT
     ------------------------------------------------------------- -->
<script>
(function() {
    // -------------------------------------------------------------
    // THREE.JS SCENE, CAMERA, RENDERER INITIALIZATION
    // -------------------------------------------------------------
    const canvas = document.getElementById('webgl-canvas');
    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: false });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x060C18);
    scene.fog = new THREE.FogExp2(0x060C18, 0.0005);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 4500);
    // Aerial perspective showing 13-berth wharf on left and distant ocean anchorage on right
    camera.position.set(-340, 320, 520);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 - 0.04; // Prevent camera sinking under water
    controls.minDistance = 60;
    controls.maxDistance = 1800;
    controls.target.set(80, 0, 0);

    // -------------------------------------------------------------
    // LIGHTING SYSTEM
    // -------------------------------------------------------------
    const ambientLight = new THREE.AmbientLight(0x0E1E38, 1.3);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xFDF4DC, 1.4);
    sunLight.position.set(-200, 400, 250);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 10;
    sunLight.shadow.camera.far = 1200;
    sunLight.shadow.camera.left = -500;
    sunLight.shadow.camera.right = 500;
    sunLight.shadow.camera.top = 500;
    sunLight.shadow.camera.bottom = -500;
    scene.add(sunLight);

    // -------------------------------------------------------------
    // 1. ARCHITECTURAL LIGHTHOUSE (ORIGIN FIXED TO TOP LANTERN ROOM)
    // -------------------------------------------------------------
    const LH_X = 180;
    const LH_Z = -190;
    const LH_BASE_Y = 0;
    const TOWER_H = 56;
    const LANTERN_Y = 69.5; // Exact Y elevation of top lantern gallery

    // Stone Foundation & Rocks
    const rockMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.9 });
    const rockBase = new THREE.Mesh(new THREE.CylinderGeometry(24, 30, 12, 10), rockMat);
    rockBase.position.set(LH_X, 6, LH_Z);
    rockBase.receiveShadow = true;
    scene.add(rockBase);

    // Tower Shaft (Masonry White with Red Accent Rings)
    const towerMat = new THREE.MeshStandardMaterial({ color: 0xF8FAFC, roughness: 0.35 });
    const tower = new THREE.Mesh(new THREE.CylinderGeometry(6.5, 10.5, TOWER_H, 20), towerMat);
    tower.position.set(LH_X, 12 + TOWER_H / 2, LH_Z);
    tower.castShadow = true;
    scene.add(tower);

    // Red Decorative Stripe Ring on Tower
    const stripeMat = new THREE.MeshStandardMaterial({ color: 0xDC2626, roughness: 0.4 });
    const redStripe = new THREE.Mesh(new THREE.CylinderGeometry(8.2, 8.8, 10, 20), stripeMat);
    redStripe.position.set(LH_X, 36, LH_Z);
    scene.add(redStripe);

    // Balcony Gallery Deck
    const deckMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.5 });
    const deck = new THREE.Mesh(new THREE.CylinderGeometry(9.5, 9.5, 2.5, 20), deckMat);
    deck.position.set(LH_X, 12 + TOWER_H + 1.25, LH_Z);
    scene.add(deck);

    // Balcony Railing
    const railMat = new THREE.MeshBasicMaterial({ color: 0x0F172A, wireframe: true });
    const railing = new THREE.Mesh(new THREE.CylinderGeometry(9.2, 9.2, 3.5, 20, 1, true), railMat);
    railing.position.set(LH_X, 12 + TOWER_H + 4, LH_Z);
    scene.add(railing);

    // Top Lantern Glass Housing (Glowing Emissive Material)
    const lanternGlassMat = new THREE.MeshStandardMaterial({
        color: 0xBAE6FD,
        emissive: 0x38BDF8,
        emissiveIntensity: 0.95,
        roughness: 0.1,
        metalness: 0.2,
        transparent: true,
        opacity: 0.85
    });
    const lanternGlass = new THREE.Mesh(new THREE.CylinderGeometry(5.8, 5.8, 8.5, 16), lanternGlassMat);
    lanternGlass.position.set(LH_X, LANTERN_Y, LH_Z);
    scene.add(lanternGlass);

    // Copper Roof Cupola Dome
    const roofMat = new THREE.MeshStandardMaterial({ color: 0x1E3A5F, roughness: 0.3, metalness: 0.6 });
    const roofDome = new THREE.Mesh(new THREE.ConeGeometry(7.0, 6.0, 16), roofMat);
    roofDome.position.set(LH_X, LANTERN_Y + 7.25, LH_Z);
    scene.add(roofDome);

    // Glowing Lamp Bulb inside Lantern
    const bulb = new THREE.Mesh(new THREE.SphereGeometry(2.0, 12, 12), new THREE.MeshBasicMaterial({ color: 0xFFFFFF }));
    bulb.position.set(LH_X, LANTERN_Y, LH_Z);
    scene.add(bulb);

    // ROTATING LIGHTHOUSE HEAD GROUP (Origin strictly at top lantern room: LANTERN_Y = 69.5)
    const lighthouseHead = new THREE.Group();
    lighthouseHead.position.set(LH_X, LANTERN_Y, LH_Z);
    scene.add(lighthouseHead);

    // 1. High-Intensity Directional SpotLight
    const spotLight = new THREE.SpotLight(0xE0F2FE, 6.5, 650, Math.PI / 8, 0.32, 1.1);
    spotLight.position.set(0, 0, 0);
    const spotTarget = new THREE.Object3D();
    spotTarget.position.set(0, -22, 500); // Projects outward and slightly downward toward water horizon
    lighthouseHead.add(spotTarget);
    spotLight.target = spotTarget;
    lighthouseHead.add(spotLight);

    // 2. Glowing PointLight for Lantern Room Ambient Radiance
    const lanternPointLight = new THREE.PointLight(0xBAE6FD, 3.2, 100);
    lanternPointLight.position.set(0, 0, 0);
    lighthouseHead.add(lanternPointLight);

    // 3. Volumetric Light Beam Cone Mesh (Origin at narrow apex inside lantern room)
    const beamLen = 460;
    const beamRad = 42;
    const beamGeo = new THREE.ConeGeometry(beamRad, beamLen, 32, 1, true);
    // Translate geometry so apex is strictly at (0, 0, 0)
    beamGeo.translate(0, -beamLen / 2, 0);
    // Rotate so cone projects forward along +Z axis
    beamGeo.rotateX(-Math.PI / 2);

    const beamMat = new THREE.MeshBasicMaterial({
        color: 0xE0F2FE,
        transparent: true,
        opacity: 0.25,
        side: THREE.DoubleSide,
        depthWrite: false,
        blending: THREE.AdditiveBlending
    });
    const beamMesh = new THREE.Mesh(beamGeo, beamMat);
    beamMesh.position.set(0, 0, 0);
    beamMesh.rotation.x = 0.045; // Project outward and slightly downward across water
    lighthouseHead.add(beamMesh);

    // -------------------------------------------------------------
    // 2. EXPANDED 3D ENVIRONMENT GEOMETRY (MERCEDES ESTUARY & WHARF)
    // -------------------------------------------------------------
    // Water Mesh (3200 x 2400)
    const waterGeo = new THREE.PlaneGeometry(3400, 2400, 80, 60);
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

    // Store base vertices for procedural wave animation
    const posAttr = waterGeo.attributes.position;
    const baseVerts = [];
    for (let i = 0; i < posAttr.count; i++) {
        baseVerts.push({ x: posAttr.getX(i), y: posAttr.getY(i), z: posAttr.getZ(i) });
    }

    // Coastline & Terrain (North sandbar & South bank)
    const landMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.85, metalness: 0.1 });

    // North Sandbar
    const northBank = new THREE.Mesh(new THREE.BoxGeometry(1000, 26, 500), landMat);
    northBank.position.set(320, 10, -440);
    northBank.receiveShadow = true;
    scene.add(northBank);

    // South Mangrove Bank
    const southBank = new THREE.Mesh(new THREE.BoxGeometry(1000, 26, 500), landMat);
    southBank.position.set(320, 10, 440);
    southBank.receiveShadow = true;
    scene.add(southBank);

    // -------------------------------------------------------------
    // 3. EXPANDED 13-BERTH CONCRETE WHARF APRON INFRASTRUCTURE
    // -------------------------------------------------------------
    const MAX_MEDIUM_BERTHS = 13;
    let numBerths = MAX_MEDIUM_BERTHS;

    const wharfMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.7, metalness: 0.2 });
    // Concrete pier length 740 to fit 13 medium vessels (each ~40m with 48m spacing)
    const wharfApron = new THREE.Mesh(new THREE.BoxGeometry(200, 22, 740), wharfMat);
    wharfApron.position.set(-190, 10, 0);
    wharfApron.receiveShadow = true;
    scene.add(wharfApron);

    // Safety Hazard Striping along the entire wharf berthing face (X = -89, Z = -370 to +370)
    const hazardLip = new THREE.Mesh(
        new THREE.BoxGeometry(3, 22.2, 740),
        new THREE.MeshBasicMaterial({ color: 0xFBBF24 })
    );
    hazardLip.position.set(-89, 10, 0);
    scene.add(hazardLip);

    // Bulungan Wholesale Auction Pavilion Complex
    const bulunganMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.6 });
    const bulunganMain = new THREE.Mesh(new THREE.BoxGeometry(110, 36, 420), bulunganMat);
    bulunganMain.position.set(-290, 18, 0);
    bulunganMain.castShadow = true;
    scene.add(bulunganMain);

    // Bulungan North Storage Shed
    const bulunganNorth = new THREE.Mesh(new THREE.BoxGeometry(100, 28, 130), bulunganMat);
    bulunganNorth.position.set(-285, 14, -240);
    scene.add(bulunganNorth);

    // Bulungan South Ice Plant Shed
    const bulunganSouth = new THREE.Mesh(new THREE.BoxGeometry(100, 28, 130), bulunganMat);
    bulunganSouth.position.set(-285, 14, 240);
    scene.add(bulunganSouth);

    // Bulungan Interior Amber Glow Lights
    const bulunganLight1 = new THREE.PointLight(0xF59E0B, 2.8, 160);
    bulunganLight1.position.set(-230, 26, -140);
    scene.add(bulunganLight1);

    const bulunganLight2 = new THREE.PointLight(0xF59E0B, 3.2, 180);
    bulunganLight2.position.set(-230, 26, 0);
    scene.add(bulunganLight2);

    const bulunganLight3 = new THREE.PointLight(0xF59E0B, 2.8, 160);
    bulunganLight3.position.set(-230, 26, 140);
    scene.add(bulunganLight3);

    // Dedicated Shallow-Water Mooring Basin for Small Boats (South Dock Basin)
    const woodMat = new THREE.MeshStandardMaterial({ color: 0x78350F, roughness: 0.8 });
    const woodDock1 = new THREE.Mesh(new THREE.BoxGeometry(70, 4, 130), woodMat);
    woodDock1.position.set(-50, 4, 275);
    scene.add(woodDock1);

    const woodDock2 = new THREE.Mesh(new THREE.BoxGeometry(50, 4, 90), woodMat);
    woodDock2.position.set(-40, 4, -280);
    scene.add(woodDock2);

    // Navigational Buoys along Channel Corridor
    const buoyMatG = new THREE.MeshBasicMaterial({ color: 0x10B981 });
    const buoyMatR = new THREE.MeshBasicMaterial({ color: 0xEF4444 });
    const buoyCoords = [
        { x: 80, z: -100, green: true }, { x: 80, z: 100, green: false },
        { x: 260, z: -110, green: true }, { x: 260, z: 110, green: false },
        { x: 440, z: -120, green: true }, { x: 440, z: 120, green: false }
    ];
    buoyCoords.forEach(b => {
        const buoy = new THREE.Mesh(new THREE.CylinderGeometry(2, 3, 8, 8), b.green ? buoyMatG : buoyMatR);
        buoy.position.set(b.x, 4, b.z);
        scene.add(buoy);
    });

    // 13 Concrete Berths (B1 to B13) Definition along Wharf Apron
    let berthCoordinates = [];
    const bollardMat = new THREE.MeshStandardMaterial({ color: 0x0F172A, metalness: 0.8 });
    const bollardGroup = new THREE.Group();
    scene.add(bollardGroup);

    function updateBerthGeometry() {
        // Clear old bollards
        while (bollardGroup.children.length > 0) {
            bollardGroup.remove(bollardGroup.children[0]);
        }
        berthCoordinates = [];
        const startZ = -288;
        const spacing = 48; // Generous 48 units per berth to prevent any ship clipping
        for (let i = 0; i < numBerths; i++) {
            const z = startZ + i * spacing;
            berthCoordinates.push({
                id: i + 1,
                name: 'Berth B' + (i + 1),
                x: -90,
                z: z,
                occupiedBy: null
            });

            // Concrete mooring bollard on wharf lip
            const bollard = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.4, 3.5, 8), bollardMat);
            bollard.position.set(-88, 22.5, z);
            bollardGroup.add(bollard);

            // Painted yellow berth marking pad
            const pad = new THREE.Mesh(new THREE.PlaneGeometry(6, 12), new THREE.MeshBasicMaterial({ color: 0xFBBF24 }));
            pad.rotation.x = -Math.PI / 2;
            pad.position.set(-94, 21.1, z);
            bollardGroup.add(pad);
        }
    }
    updateBerthGeometry();

    // -------------------------------------------------------------
    // PROCEDURAL 3D BOAT MESH FACTORY
    // -------------------------------------------------------------
    function createVesselMesh(type, cargoCount) {
        const group = new THREE.Group();

        if (type === 'Basnig') {
            // Commercial Basnig: Long hull, large cabin, lateral outrigger lighting booms
            const hullMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.6 });
            const hull = new THREE.Mesh(new THREE.BoxGeometry(40, 10, 14), hullMat);
            hull.position.y = 3;
            hull.castShadow = true;
            group.add(hull);

            // Pointed Bow
            const bow = new THREE.Mesh(new THREE.ConeGeometry(7, 14, 4), hullMat);
            bow.rotation.z = -Math.PI / 2;
            bow.position.set(24, 3, 0);
            group.add(bow);

            // Deckhouse Cabin
            const cabinMat = new THREE.MeshStandardMaterial({ color: 0x475569 });
            const cabin = new THREE.Mesh(new THREE.BoxGeometry(16, 10, 10), cabinMat);
            cabin.position.set(-6, 11, 0);
            group.add(cabin);

            // Wheelhouse Windows
            const winMat = new THREE.MeshBasicMaterial({ color: 0x38BDF8 });
            const win = new THREE.Mesh(new THREE.BoxGeometry(4, 3, 8), winMat);
            win.position.set(2, 12, 0);
            group.add(win);

            // Basnig Fishing Light Rigging Outrigger Booms
            const boomMat = new THREE.MeshBasicMaterial({ color: 0x94A3B8 });
            const boom1 = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.6, 42), boomMat);
            boom1.rotation.x = Math.PI / 2;
            boom1.position.set(4, 13, 0);
            group.add(boom1);

            // High Mast with Radar
            const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.8, 22), boomMat);
            mast.position.set(-4, 18, 0);
            group.add(mast);

            // Navigation Lanterns (Port Red, Starboard Green)
            const pLight = new THREE.Mesh(new THREE.SphereGeometry(1.2, 6, 6), new THREE.MeshBasicMaterial({ color: 0xEF4444 }));
            pLight.position.set(4, 13, 21);
            group.add(pLight);
            const sLight = new THREE.Mesh(new THREE.SphereGeometry(1.2, 6, 6), new THREE.MeshBasicMaterial({ color: 0x10B981 }));
            sLight.position.set(4, 13, -21);
            group.add(sLight);

            // Fish Crate Stacks (Banyeras) in Cargo Hold
            const crateMat = new THREE.MeshStandardMaterial({ color: 0xD97706 });
            const crates = new THREE.Mesh(new THREE.BoxGeometry(10, 5, 8), crateMat);
            crates.position.set(12, 7, 0);
            group.add(crates);

        } else if (type === 'Purse Seiner' || type === 'Ring-Netter') {
            // Purse Seiner / Ring-Netter: Deep hull with net drum
            const hullMat = new THREE.MeshStandardMaterial({ color: 0x0F172A, roughness: 0.5 });
            const hull = new THREE.Mesh(new THREE.BoxGeometry(36, 10, 15), hullMat);
            hull.position.y = 3;
            hull.castShadow = true;
            group.add(hull);

            // Forward Wheelhouse
            const wheelhouse = new THREE.Mesh(new THREE.BoxGeometry(12, 11, 11), new THREE.MeshStandardMaterial({ color: 0xE2E8F0 }));
            wheelhouse.position.set(10, 11, 0);
            group.add(wheelhouse);

            // Aft Net Drum Roll
            const drum = new THREE.Mesh(new THREE.CylinderGeometry(4, 4, 11, 12), new THREE.MeshStandardMaterial({ color: 0x334155 }));
            drum.rotation.x = Math.PI / 2;
            drum.position.set(-10, 7, 0);
            group.add(drum);

            // Fish crates
            const crates = new THREE.Mesh(new THREE.BoxGeometry(8, 4, 8), new THREE.MeshStandardMaterial({ color: 0xF59E0B }));
            crates.position.set(0, 6, 0);
            group.add(crates);

        } else {
            // Shuttle Banca: Motorized double-outrigger (katig)
            const bancaMat = new THREE.MeshStandardMaterial({ color: 0x0284C7 });
            const hull = new THREE.Mesh(new THREE.BoxGeometry(18, 4, 4.5), bancaMat);
            hull.position.y = 1.5;
            group.add(hull);

            // Twin Bamboo Outriggers (Katig)
            const katigMat = new THREE.MeshStandardMaterial({ color: 0xF8FAFC });
            const float1 = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.7, 16), katigMat);
            float1.rotation.z = Math.PI / 2;
            float1.position.set(0, 1, -9);
            group.add(float1);

            const float2 = float1.clone();
            float2.position.set(0, 1, 9);
            group.add(float2);

            // Crossbeam Struts (Tadlang)
            const strutMat = new THREE.MeshBasicMaterial({ color: 0xCBD5E1 });
            const strut1 = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 18), strutMat);
            strut1.rotation.x = Math.PI / 2;
            strut1.position.set(3, 2.5, 0);
            group.add(strut1);

            const strut2 = strut1.clone();
            strut2.position.set(-3, 2.5, 0);
            group.add(strut2);

            // Crate Payload on Banca (shown during lightering)
            const bancaCrates = new THREE.Mesh(new THREE.BoxGeometry(6, 3, 3), new THREE.MeshStandardMaterial({ color: 0xFBBF24 }));
            bancaCrates.position.set(0, 3.5, 0);
            bancaCrates.name = 'cratesMesh';
            group.add(bancaCrates);
        }

        return group;
    }

    // -------------------------------------------------------------
    // STOCHASTIC SIMULATION DATA STRUCTURES & PERSISTENT FLEET
    // -------------------------------------------------------------
    let simTime = 5.75; // 05:45 AM (Dawn Bulungan Peak)
    let isPlaying = true;
    let timeScale = 1.0;
    let lastTime = performance.now();

    let arrivalRate = 0.34;
    let bulunganMultiplier = 2.8;
    let tideLockActive = true;
    let totalCratesLanded = 1420;

    let vessels = [];
    let bancas = [];
    let arrivalTimer = 0;

    // Helper: Diurnal arrival intensity λ(t)
    function computeLambda(t) {
        const dawnPeak = bulunganMultiplier * Math.exp(-Math.pow((t - 6.0), 2) / (2 * 1.44));
        const duskPeak = 0.65 * Math.exp(-Math.pow((t - 16.5), 2) / (2 * 2.25));
        return arrivalRate + dawnPeak + duskPeak;
    }

    // Semi-diurnal Tide (Meters above datum: 0.5m to 2.2m)
    function computeTide(t) {
        return 1.35 + 0.85 * Math.cos((t - 6.0) * (Math.PI / 6.0));
    }

    // -------------------------------------------------------------
    // POPULATE INITIAL FLEET: MEDIUM BOATS & 24 PERSISTENT BANCAS
    // -------------------------------------------------------------
    function initFleet() {
        // Spawn 3 initial medium boats directly docked at berths B2, B4, B6
        const initialDocked = [
            { name: 'MV-MercedesQueen', type: 'Basnig', gt: 28.4, draft: 2.15, cargo: 120, maxCargo: 160, berthIdx: 1 },
            { name: 'MV-SanMiguel', type: 'Purse Seiner', gt: 24.1, draft: 1.95, cargo: 95, maxCargo: 130, berthIdx: 3 },
            { name: 'MV-BicolExpress', type: 'Basnig', gt: 32.0, draft: 2.30, cargo: 150, maxCargo: 180, berthIdx: 5 }
        ];

        initialDocked.forEach(spec => {
            const bCoord = berthCoordinates[spec.berthIdx];
            if (bCoord) {
                const mesh = createVesselMesh(spec.type, spec.cargo);
                mesh.position.set(bCoord.x, 0, bCoord.z);
                mesh.rotation.y = Math.PI / 2; // Alongside concrete pier
                scene.add(mesh);
                bCoord.occupiedBy = spec.name;
                vessels.push({
                    name: spec.name,
                    type: spec.type,
                    gt: spec.gt,
                    draft: spec.draft,
                    cargo: spec.cargo,
                    maxCargo: spec.maxCargo,
                    x: bCoord.x,
                    z: bCoord.z,
                    mesh: mesh,
                    state: 'Unloading at Wharf',
                    assignedBerth: bCoord,
                    wait: 0
                });
            }
        });

        // Spawn 2 initial medium boats far away in San Miguel Bay Anchorage
        const initialAnchored = [
            { name: 'MV-DaetStar', type: 'Basnig', gt: 29.5, draft: 2.25, cargo: 160, maxCargo: 160, x: 520, z: -120 },
            { name: 'MV-NagaPride', type: 'Ring-Netter', gt: 21.0, draft: 1.85, cargo: 110, maxCargo: 120, x: 580, z: 80 }
        ];

        initialAnchored.forEach(spec => {
            const mesh = createVesselMesh(spec.type, spec.cargo);
            mesh.position.set(spec.x, 0, spec.z);
            scene.add(mesh);
            vessels.push({
                name: spec.name,
                type: spec.type,
                gt: spec.gt,
                draft: spec.draft,
                cargo: spec.cargo,
                maxCargo: spec.maxCargo,
                x: spec.x,
                z: spec.z,
                mesh: mesh,
                state: 'Waiting at Anchorage',
                assignedBerth: null,
                wait: 1.5
            });
        });

        // SPAWN PERSISTENT SMALL BOAT FLEET (24 BANCAS) MOORED AT DOCK BASINS
        // Generate 24 distinct dock mooring slots
        const parkSlots = [];
        // 10 slots along South Wooden Dock 1 (Z: 220 to 330)
        for (let i = 0; i < 10; i++) {
            parkSlots.push({ x: -45, z: 220 + i * 12, yaw: Math.PI / 2 });
        }
        // 8 slots along South Basin Wall (Z: 230 to 320, inner side)
        for (let i = 0; i < 8; i++) {
            parkSlots.push({ x: -22, z: 235 + i * 11, yaw: 0 });
        }
        // 6 slots along North Dock 2 (Z: -320 to -250)
        for (let i = 0; i < 6; i++) {
            parkSlots.push({ x: -35, z: -315 + i * 13, yaw: -Math.PI / 2 });
        }

        for (let i = 0; i < 24; i++) {
            const slot = parkSlots[i % parkSlots.length];
            const bMesh = createVesselMesh('Banca', 0);
            bMesh.position.set(slot.x, 0, slot.z);
            bMesh.rotation.y = slot.yaw;
            scene.add(bMesh);

            bancas.push({
                id: 'Banca-' + (i + 1),
                name: 'Banca #' + (i + 1),
                type: 'Artisanal Shuttle Banca',
                gt: 2.4,
                draft: 0.65,
                mesh: bMesh,
                state: 'parked', // Mostly parked at dock
                parkSlot: slot,
                targetBoat: null,
                cargo: 0,
                maxCargo: 25,
                bobPhase: Math.random() * Math.PI * 2,
                timer: 0
            });
        }
    }
    initFleet();

    // -------------------------------------------------------------
    // ANIMATION & DISCRETE-EVENT UPDATE LOOP
    // -------------------------------------------------------------
    let lighthouseAngle = 0;

    function updateSimulation(deltaHours) {
        // Clock Progression
        simTime = (simTime + deltaHours) % 24.0;
        const tide = computeTide(simTime);

        // UI Clock & Status Update
        const clockH = Math.floor(simTime);
        const clockM = Math.floor((simTime - clockH) * 60);
        const ampm = clockH >= 12 ? 'PM' : 'AM';
        const displayH = clockH % 12 === 0 ? 12 : clockH % 12;
        document.getElementById('hud-clock').textContent =
            (displayH < 10 ? '0' : '') + displayH + ':' + (clockM < 10 ? '0' : '') + clockM + ' ' + ampm;

        // Bulungan Surge Active between 03:00 and 07:00
        const surgeActive = simTime >= 3.0 && simTime <= 7.2;
        const surgePill = document.getElementById('surge-pill');
        surgePill.style.display = surgeActive ? 'inline-flex' : 'none';

        // Tide Pill Update
        const tidePill = document.getElementById('tide-pill');
        if (tide >= 1.6 || !tideLockActive) {
            tidePill.textContent = 'HIGH TIDE: Open (+' + tide.toFixed(2) + 'm)';
            tidePill.className = 'tide-pill';
        } else {
            tidePill.textContent = 'LOW TIDE: Draft >1.8m Lock (+' + tide.toFixed(2) + 'm)';
            tidePill.className = 'tide-pill low';
        }

        // Dynamic Diurnal Lighting & Sky Transitions
        if (surgeActive) {
            scene.background.lerp(new THREE.Color(0x18182B), 0.04);
            scene.fog.color.lerp(new THREE.Color(0x18182B), 0.04);
            sunLight.color.lerp(new THREE.Color(0xFBBF24), 0.04);
            sunLight.intensity = 1.6;
        } else if (simTime >= 7.2 && simTime <= 16.0) {
            scene.background.lerp(new THREE.Color(0x0C1E38), 0.04);
            scene.fog.color.lerp(new THREE.Color(0x0C1E38), 0.04);
            sunLight.color.lerp(new THREE.Color(0xFDF4DC), 0.04);
            sunLight.intensity = 1.4;
        } else if (simTime > 16.0 && simTime <= 18.5) {
            scene.background.lerp(new THREE.Color(0x231828), 0.04);
            scene.fog.color.lerp(new THREE.Color(0x231828), 0.04);
            sunLight.color.lerp(new THREE.Color(0xF97316), 0.04);
            sunLight.intensity = 1.3;
        } else {
            scene.background.lerp(new THREE.Color(0x050A14), 0.04);
            scene.fog.color.lerp(new THREE.Color(0x050A14), 0.04);
            sunLight.intensity = 0.25;
        }

        // -------------------------------------------------------------
        // STOCHASTIC MEDIUM VESSEL ARRIVALS & DUAL BEHAVIOR LOGIC
        // -------------------------------------------------------------
        arrivalTimer += computeLambda(simTime) * deltaHours;
        if (arrivalTimer >= 1.0 && vessels.length < 18) {
            arrivalTimer = 0;
            const types = ['Basnig', 'Purse Seiner', 'Ring-Netter'];
            const selType = types[Math.floor(Math.random() * types.length)];
            const rDraft = selType === 'Basnig' ? (1.9 + Math.random() * 0.45) : (1.6 + Math.random() * 0.35);
            const rCargo = Math.floor(110 + Math.random() * 70);
            const rGT = (18 + Math.random() * 15);
            const vName = 'MV-Catch-' + Math.floor(Math.random() * 900 + 100);

            const vMesh = createVesselMesh(selType, rCargo);
            // Spawn on far eastern horizon
            vMesh.position.set(780, 0, (Math.random() - 0.5) * 360);
            scene.add(vMesh);

            const newBoat = {
                name: vName,
                type: selType,
                gt: parseFloat(rGT.toFixed(1)),
                draft: parseFloat(rDraft.toFixed(2)),
                cargo: rCargo,
                maxCargo: rCargo,
                x: 0,
                z: 0,
                mesh: vMesh,
                state: 'Arriving',
                wait: 0,
                assignedBerth: null,
                unloadTimer: 0
            };

            // DUAL BEHAVIOR DECISION:
            // Check: Is there an open berth, does tide allow entry, and is anchorage empty (FIFO priority)?
            const canPassChannel = !tideLockActive || tide >= 1.6 || newBoat.draft <= 1.8;
            const freeBerth = berthCoordinates.find(b => b.occupiedBy === null);
            const anchoredWaiting = vessels.filter(v => v.state === 'Waiting at Anchorage').length;

            if (canPassChannel && freeBerth && anchoredWaiting === 0) {
                // DIRECT DOCKING: Claim berth and navigate straight in
                freeBerth.occupiedBy = newBoat.name;
                newBoat.assignedBerth = freeBerth;
                newBoat.state = 'Navigating Channel';
            } else {
                // STAY FAR AWAY AT ANCHORAGE: Outer San Miguel Bay holding zone
                newBoat.x = 500 + Math.random() * 180; // Distant anchorage (X: 500-680)
                newBoat.z = (Math.random() - 0.5) * 320;
                newBoat.state = 'Arriving';
            }
            vessels.push(newBoat);
        }

        // -------------------------------------------------------------
        // UPDATE MEDIUM VESSELS STATE MACHINE
        // -------------------------------------------------------------
        let waitingCount = 0;
        let occupiedCount = 0;

        vessels.forEach((v, idx) => {
            // Gentle water bobbing
            v.mesh.position.y = Math.sin(Date.now() * 0.002 + idx) * 0.7;

            if (v.state === 'Arriving') {
                // Steer into Distant San Miguel Bay Anchorage
                v.mesh.position.x += (v.x - v.mesh.position.x) * 0.04;
                v.mesh.position.z += (v.z - v.mesh.position.z) * 0.04;
                if (Math.abs(v.mesh.position.x - v.x) < 6) {
                    v.state = 'Waiting at Anchorage';
                }
            } else if (v.state === 'Waiting at Anchorage') {
                waitingCount++;
                v.wait += deltaHours;

                // Priority Check: If any docked medium boat has vacated a berth, move in!
                const canPass = !tideLockActive || tide >= 1.6 || v.draft <= 1.8;
                const freeBerth = berthCoordinates.find(b => b.occupiedBy === null);

                if (canPass && freeBerth) {
                    freeBerth.occupiedBy = v.name;
                    v.assignedBerth = freeBerth;
                    v.state = 'Navigating Channel';
                }
            } else if (v.state === 'Navigating Channel') {
                // Transit through estuarine channel toward assigned concrete berth
                const targetX = v.assignedBerth.x;
                const targetZ = v.assignedBerth.z;

                v.mesh.position.x += (targetX - v.mesh.position.x) * 0.035;
                v.mesh.position.z += (targetZ - v.mesh.position.z) * 0.035;

                // Turn alongside wharf
                v.mesh.rotation.y = Math.PI / 2;

                if (Math.abs(v.mesh.position.x - targetX) < 4 && Math.abs(v.mesh.position.z - targetZ) < 4) {
                    v.mesh.position.x = targetX;
                    v.mesh.position.z = targetZ;
                    v.state = 'Unloading at Wharf';
                }
            } else if (v.state === 'Unloading at Wharf') {
                occupiedCount++;
                // Offload crates directly onto wharf apron
                const offloadAmt = Math.round(deltaHours * 95);
                v.cargo = Math.max(0, v.cargo - offloadAmt);
                totalCratesLanded += offloadAmt;

                if (v.cargo <= 0) {
                    // Free berth for next waiting boat
                    if (v.assignedBerth) {
                        v.assignedBerth.occupiedBy = null;
                        v.assignedBerth = null;
                    }
                    v.state = 'Reverse Maneuver';
                    v.reverseTargetX = v.mesh.position.x + 45;
                    v.reverseTargetZ = v.mesh.position.z + (v.mesh.position.z > 0 ? -24 : 24);
                }
            } else if (v.state === 'Reverse Maneuver') {
                // Smooth angled reverse backing out into the open channel
                v.mesh.position.x += (v.reverseTargetX - v.mesh.position.x) * 0.04;
                v.mesh.position.z += (v.reverseTargetZ - v.mesh.position.z) * 0.04;
                v.mesh.rotation.y = -Math.PI / 4;
                if (Math.abs(v.mesh.position.x - v.reverseTargetX) < 4) {
                    v.state = 'Departing';
                }
            } else if (v.state === 'Departing') {
                // Sail out past the lighthouse into the horizon
                v.mesh.position.x += 2.2;
                v.mesh.rotation.y = 0;
                if (v.mesh.position.x > 820) {
                    scene.remove(v.mesh);
                    vessels.splice(idx, 1);
                }
            }
        });

        // -------------------------------------------------------------
        // UPDATE SMALL BOAT FLEET (PARKED AT DOCK + DYNAMIC LIGHTERING)
        // -------------------------------------------------------------
        let activeBancas = 0;

        bancas.forEach((b, bIdx) => {
            // Desynchronized gentle water bobbing for small boats
            b.mesh.position.y = Math.sin(Date.now() * 0.003 + b.bobPhase) * 0.45;

            if (b.state === 'parked') {
                // Keep moored in designated slot with slight rocking
                b.mesh.position.x = b.parkSlot.x;
                b.mesh.position.z = b.parkSlot.z;
                b.mesh.rotation.y = b.parkSlot.yaw;

                // DYNAMIC FISH FETCHING LOOP:
                // If a medium boat is holding far away in anchorage with cargo, dispatch up to 2-3 bancas
                const activeCount = bancas.filter(item => item.state !== 'parked').length;
                if (activeCount < 3) {
                    const targetMB = vessels.find(v => v.state === 'Waiting at Anchorage' && v.cargo > 0);
                    if (targetMB) {
                        b.targetBoat = targetMB;
                        b.state = 'to_anchorage';
                    }
                }
            } else if (b.state === 'to_anchorage') {
                activeBancas++;
                if (!b.targetBoat || b.targetBoat.cargo <= 0) {
                    b.state = 'return_to_park';
                    return;
                }
                // Drive out from dock to distant anchored medium boat
                const tx = b.targetBoat.mesh.position.x;
                const tz = b.targetBoat.mesh.position.z;
                const dx = tx - b.mesh.position.x;
                const dz = tz - b.mesh.position.z;

                b.mesh.position.x += dx * 0.045;
                b.mesh.position.z += dz * 0.045;
                b.mesh.rotation.y = -Math.atan2(dz, dx);

                if (Math.hypot(dx, dz) < 22) {
                    b.state = 'transferring';
                    b.timer = 1.8; // Brief transfer pause alongside medium boat
                }
            } else if (b.state === 'transferring') {
                activeBancas++;
                b.timer -= deltaHours * 15;
                if (b.timer <= 0) {
                    const takeAmt = Math.min(b.maxCargo, b.targetBoat ? b.targetBoat.cargo : 0);
                    if (b.targetBoat) b.targetBoat.cargo -= takeAmt;
                    b.cargo = takeAmt;
                    b.state = 'to_wharf';
                }
            } else if (b.state === 'to_wharf') {
                activeBancas++;
                // Drive back to wharf apron landing zone
                const landingX = -86;
                const landingZ = 180;
                const dx = landingX - b.mesh.position.x;
                const dz = landingZ - b.mesh.position.z;

                b.mesh.position.x += dx * 0.04;
                b.mesh.position.z += dz * 0.04;
                b.mesh.rotation.y = -Math.atan2(dz, dx);

                if (Math.hypot(dx, dz) < 18) {
                    b.state = 'unloading_at_wharf';
                    b.timer = 1.4;
                }
            } else if (b.state === 'unloading_at_wharf') {
                activeBancas++;
                b.timer -= deltaHours * 15;
                if (b.timer <= 0) {
                    totalCratesLanded += b.cargo;
                    b.cargo = 0;
                    b.state = 'return_to_park';
                }
            } else if (b.state === 'return_to_park') {
                activeBancas++;
                // Smoothly return to designated dock mooring slot
                const dx = b.parkSlot.x - b.mesh.position.x;
                const dz = b.parkSlot.z - b.mesh.position.z;

                b.mesh.position.x += dx * 0.05;
                b.mesh.position.z += dz * 0.05;
                b.mesh.rotation.y = -Math.atan2(dz, dx);

                if (Math.hypot(dx, dz) < 4) {
                    b.mesh.position.x = b.parkSlot.x;
                    b.mesh.position.z = b.parkSlot.z;
                    b.mesh.rotation.y = b.parkSlot.yaw;
                    b.state = 'parked';
                    b.targetBoat = null;
                }
            }
        });

        // -------------------------------------------------------------
        // UPDATE FLOATING HUD KPI CARDS & STATUS PILLS
        // -------------------------------------------------------------
        // Card 1: Distant Anchorage Queue
        document.getElementById('kpi-queue-count').textContent = waitingCount;
        document.getElementById('kpi-wait-time').textContent = (waitingCount > 0 ? (1.2 + waitingCount * 0.45).toFixed(2) : '0.00');

        // Card 2: Wharf Apron (Medium Commercial Berths)
        const berthUtil = (occupiedCount / numBerths) * 100;
        document.getElementById('kpi-berth-util').textContent = berthUtil.toFixed(1);
        document.getElementById('kpi-berth-occ').textContent = occupiedCount;
        document.getElementById('kpi-berth-total').textContent = numBerths;

        // Card 3: Small Boat Fleet
        document.getElementById('kpi-bancas-active').textContent = activeBancas;
        document.getElementById('kpi-bancas-moored').textContent = (bancas.length - activeBancas);

        // Card 4: Banyera Landed & Quality
        document.getElementById('kpi-crates-count').textContent = totalCratesLanded.toLocaleString();
        const qualityRetention = Math.max(75, 100 * Math.exp(-0.028 * (waitingCount * 0.45)));
        document.getElementById('kpi-quality-score').textContent = qualityRetention.toFixed(1);
    }

    // -------------------------------------------------------------
    // THREE.JS RENDER LOOP
    // -------------------------------------------------------------
    function render(time) {
        const deltaMs = time - lastTime;
        lastTime = time;

        if (isPlaying) {
            // 1 second real-time = 0.15 simulation hours
            const deltaHours = (deltaMs / 1000) * (timeScale * 0.15);
            updateSimulation(deltaHours);
        }

        // Procedural Wave Motion on Water Mesh
        const waveTime = time * 0.002;
        const pAttr = waterGeo.attributes.position;
        for (let i = 0; i < pAttr.count; i++) {
            const bv = baseVerts[i];
            const waveZ = Math.sin(bv.x * 0.015 + waveTime) * 1.5 + Math.cos(bv.y * 0.015 + waveTime * 1.2) * 1.2;
            pAttr.setZ(i, waveZ);
        }
        pAttr.needsUpdate = true;

        // ROTATE LIGHTHOUSE HEAD SMOOTHLY (Origin strictly at top lantern room)
        lighthouseHead.rotation.y += 0.018;

        controls.update();
        renderer.render(scene, camera);
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);

    // -------------------------------------------------------------
    // INTERACTIVE 3D RAYCASTING (HOVER & CLICK TOOLTIP)
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

    window.addEventListener('mousemove', (e) => {
        mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);

        // Check both Medium Vessels and Small Bancas
        const mediumMeshes = vessels.map(v => v.mesh);
        const bancaMeshes = bancas.map(b => b.mesh);
        const allMeshes = mediumMeshes.concat(bancaMeshes);

        const intersects = raycaster.intersectObjects(allMeshes, true);

        if (intersects.length > 0) {
            let hitGroup = intersects[0].object;
            while (hitGroup.parent && hitGroup.parent !== scene) {
                hitGroup = hitGroup.parent;
            }

            // Find matching vessel or banca
            const foundMedium = vessels.find(v => v.mesh === hitGroup);
            const foundBanca = bancas.find(b => b.mesh === hitGroup);

            if (foundMedium) {
                ttName.textContent = foundMedium.name;
                ttType.textContent = foundMedium.type;
                ttGT.textContent = foundMedium.gt + ' GT';
                ttDraft.textContent = foundMedium.draft + ' m';
                ttCargo.textContent = foundMedium.cargo + ' / ' + foundMedium.maxCargo + ' banyeras';
                const pct = Math.min(100, Math.round((foundMedium.cargo / Math.max(1, foundMedium.maxCargo)) * 100));
                ttBar.style.width = pct + '%';

                if (foundMedium.state === 'Unloading at Wharf') {
                    ttBadge.textContent = 'Direct Docked';
                    ttBadge.style.background = 'rgba(16, 185, 129, 0.2)';
                    ttBadge.style.color = '#34D399';
                    ttState.textContent = 'Unloading at ' + (foundMedium.assignedBerth ? foundMedium.assignedBerth.name : 'Wharf');
                } else if (foundMedium.state === 'Waiting at Anchorage') {
                    ttBadge.textContent = 'Distant Anchorage';
                    ttBadge.style.background = 'rgba(245, 158, 11, 0.2)';
                    ttBadge.style.color = '#FBBF24';
                    ttState.textContent = 'Holding in San Miguel Bay';
                } else {
                    ttBadge.textContent = foundMedium.state;
                    ttBadge.style.background = 'rgba(56, 189, 248, 0.2)';
                    ttBadge.style.color = '#38BDF8';
                    ttState.textContent = foundMedium.state;
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

                if (foundBanca.state === 'parked') {
                    ttBadge.textContent = 'Moored at Dock';
                    ttBadge.style.background = 'rgba(148, 163, 184, 0.2)';
                    ttBadge.style.color = '#94A3B8';
                    ttState.textContent = 'Parked at Shallow Mooring Basin';
                } else {
                    ttBadge.textContent = 'Active Lightering';
                    ttBadge.style.background = 'rgba(245, 158, 11, 0.2)';
                    ttBadge.style.color = '#FBBF24';
                    ttState.textContent = 'Fetching Banyeras from Bay';
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
    // UI CONTROLS & MODAL EVENT LISTENERS
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
    });

    document.querySelectorAll('.speed-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.speed-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            timeScale = parseFloat(btn.dataset.speed);
        });
    });

    // Modals open/close
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

    // Modal Tabs
    document.querySelectorAll('.modal-tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.modal-tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.dataset.tab).classList.add('active');
        });
    });

    // Settings Sliders
    const slLambda = document.getElementById('sl-lambda');
    slLambda.addEventListener('input', (e) => {
        arrivalRate = parseFloat(e.target.value);
        document.getElementById('val-lambda').textContent = arrivalRate.toFixed(2) + ' /h';
    });
    const slRush = document.getElementById('sl-rush');
    slRush.addEventListener('input', (e) => {
        bulunganMultiplier = parseFloat(e.target.value);
        document.getElementById('val-rush').textContent = bulunganMultiplier.toFixed(1) + 'x';
    });
    const slBerths = document.getElementById('sl-berths');
    slBerths.addEventListener('input', (e) => {
        numBerths = parseInt(e.target.value);
        document.getElementById('val-berths').textContent = numBerths + ' berths';
        updateBerthGeometry();
    });
    const chkTide = document.getElementById('chk-tide');
    chkTide.addEventListener('change', (e) => {
        tideLockActive = e.target.checked;
    });

    // Policy Presets
    document.querySelectorAll('.preset-card').forEach(card => {
        card.addEventListener('click', () => {
            document.querySelectorAll('.preset-card').forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            const p = card.dataset.preset;
            const badge = document.getElementById('badge-scenario');

            if (p === 'baseline') {
                numBerths = 13;
                arrivalRate = 0.34;
                bulunganMultiplier = 2.8;
                tideLockActive = true;
                badge.textContent = 'Baseline (13 Berths)';
            } else if (p === 'interventionA') {
                numBerths = 16;
                arrivalRate = 0.34;
                bulunganMultiplier = 2.8;
                tideLockActive = true;
                badge.textContent = 'Intervention A: 16 Berths';
            } else if (p === 'interventionB') {
                numBerths = 13;
                arrivalRate = 0.34;
                bulunganMultiplier = 2.8;
                tideLockActive = false; // Dredging removes low tide lock
                badge.textContent = 'Intervention B: Dredging';
            } else if (p === 'interventionC') {
                numBerths = 13;
                arrivalRate = 0.34;
                bulunganMultiplier = 1.4; // Staggered scheduling cuts surge
                tideLockActive = true;
                badge.textContent = 'Intervention C: Staggered';
            }
            slBerths.value = numBerths;
            document.getElementById('val-berths').textContent = numBerths + ' berths';
            slRush.value = bulunganMultiplier;
            document.getElementById('val-rush').textContent = bulunganMultiplier.toFixed(1) + 'x';
            chkTide.checked = tideLockActive;
            updateBerthGeometry();
        });
    });

    // Screenshot Mode (Clean Manuscript Capture)
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

    // Window Resize Handling
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
