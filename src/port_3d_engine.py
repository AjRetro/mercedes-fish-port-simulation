# src/port_3d_engine.py
"""
Interactive 3D Discrete-Event Simulation (DES) Digital Twin Engine
for Mercedes Fish Port, Mercedes, Camarines Norte.

Developed collaboratively by:
- @design-ux-architect: Zero-clutter 100% full-screen workspace, progressive disclosure modals, publication screenshot mode.
- @design-ui-designer: Deep ocean slate palette, glassmorphic HUD pills, WCAG 2.1 AA contrast, crisp typography.
- @engineering-frontend-developer / Simulation Engineer: WebGL Three.js engine with real-world spatial topology,
  semi-diurnal tidal gating, lightering operations, diurnal NHPP queueing, and 6:00 AM Bulungan auction rush.
"""

def generate_3d_digital_twin_html() -> str:
    """Generates the self-contained, 100% full-screen 3D WebGL Digital Twin HTML page."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Mercedes Fish Port — 3D DES Digital Twin</title>
<!-- Google Fonts: Inter -->
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
        max-width: 330px;
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
        width: 250px;
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
        max-width: 840px;
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
        min-width: 50px;
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
            <span id="badge-scenario" class="scenario-pill">Baseline State</span>
        </div>
    </div>

    <!-- Center: Live 24h Clock, Bulungan Surge & Tide Pill -->
    <div class="hud-group">
        <div class="glass-panel clock-pill">
            <span id="hud-clock" class="hud-clock">05:45 AM</span>
            <span id="surge-pill" class="surge-pill">⚡ BULUNGAN AUCTION SURGE</span>
            <span id="tide-pill" class="tide-pill">HIGH TIDE: Open (+2.1m)</span>
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
            <div class="kpi-value"><span id="kpi-queue-count">3</span> <span style="font-size:0.75rem; color:#94A3B8;">craft</span></div>
            <div class="kpi-sub">Mean Wait: <span id="kpi-wait-time">2.14</span> hrs</div>
        </div>

        <div class="glass-panel kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Wharf Apron</span>
                <span id="kpi-berth-status" style="font-size:0.6rem; color:#34D399;">Active</span>
            </div>
            <div class="kpi-value"><span id="kpi-berth-util">66.7</span><span style="font-size:0.75rem; color:#94A3B8;">%</span></div>
            <div class="kpi-sub"><span id="kpi-berth-occ">2</span> / <span id="kpi-berth-total">3</span> slips occupied</div>
        </div>

        <div class="glass-panel kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Banyera Landed</span>
                <span style="font-size:0.6rem; color:#38BDF8;">Wholesale</span>
            </div>
            <div class="kpi-value"><span id="kpi-crates-count" style="color:#34D399;">1,420</span></div>
            <div class="kpi-sub">35–40 kg tubs processed</div>
        </div>

        <div class="glass-panel kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">Freshness Retention</span>
                <span style="font-size:0.6rem; color:#34D399;">Grade-A</span>
            </div>
            <div class="kpi-value"><span id="kpi-quality-score">94.2</span><span style="font-size:0.75rem; color:#94A3B8;">%</span></div>
            <div class="kpi-sub">Exponential Ice Loss: <span id="kpi-loss-php">PHP 0.38M</span></div>
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
        <span id="tt-vessel-badge" class="tt-badge" style="background:rgba(245,158,11,0.2); color:#FBBF24;">Anchored</span>
    </div>
    <div class="tt-row"><span>Classification:</span><span id="tt-vessel-type" class="tt-val">Commercial Basnig</span></div>
    <div class="tt-row"><span>Gross Tonnage:</span><span id="tt-vessel-gt" class="tt-val">28.4 GT</span></div>
    <div class="tt-row"><span>Design Draft:</span><span id="tt-vessel-draft" class="tt-val">2.15 m</span></div>
    <div class="tt-row"><span>Cargo Banyeras:</span><span id="tt-vessel-cargo" class="tt-val">140 / 160</span></div>
    <div class="tt-bar-bg"><div id="tt-vessel-bar" class="tt-bar-fill" style="width: 85%;"></div></div>
    <div class="tt-row" style="margin-top:6px;"><span>Current State:</span><span id="tt-vessel-state" class="tt-val" style="color:#38BDF8;">Awaiting Lightering</span></div>
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
                        <div class="param-title">Wharf Apron Berthing Slips</div>
                        <div class="param-desc">Number of physical landing spots at the concrete fish landing pier.</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-berths" min="1" max="8" step="1" value="3">
                        <span id="val-berths" class="param-val">3 berths</span>
                    </div>
                </div>

                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Shuttle Banca Fleet Size</div>
                        <div class="param-desc">Motorized lightering bancas ferrying crates from deep-draft vessels.</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-bancas" min="2" max="30" step="1" value="10">
                        <span id="val-bancas" class="param-val">10 craft</span>
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
                        <div class="preset-name">1. Baseline (Current Mercedes Port)</div>
                        <div class="preset-desc">3 berths, 10 bancas, shallow river channel (1.8m low-tide lock), and concentrated 6:00 AM auction rush. High anchorage dwell and ice loss.</div>
                    </div>

                    <div class="preset-card" data-preset="interventionA">
                        <span class="preset-tag" style="color:#10B981;">Intervention A</span>
                        <div class="preset-name">2. Wharf Expansion & Cargo Winches</div>
                        <div class="preset-desc">Expands landing apron to 5 berths and introduces mechanical winches (+60% banyera offload speed), relieving wharf congestion.</div>
                    </div>

                    <div class="preset-card" data-preset="interventionB">
                        <span class="preset-tag" style="color:#F59E0B;">Intervention B</span>
                        <div class="preset-name">3. Estuarine Channel Dredging</div>
                        <div class="preset-desc">Deepens river mouth bathymetry to 3.5m, eliminating low-tide draft restrictions so commercial vessels berth directly without lightering delays.</div>
                    </div>

                    <div class="preset-card" data-preset="interventionC">
                        <span class="preset-tag" style="color:#A855F7;">Intervention C</span>
                        <div class="preset-name">4. Staggered Bulungan Scheduling</div>
                        <div class="preset-desc">Implements timed offloading windows for purse seiners and ring-netters, smoothing out the early-morning 06:00 AM bottleneck.</div>
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
                        <td style="font-weight:700; color:#38BDF8;">1. Baseline (Status Quo)</td>
                        <td>2.45 ± 0.18h</td>
                        <td>4.12 hrs</td>
                        <td>84.2%</td>
                        <td>1,840 tubs</td>
                        <td style="color:#F87171;">PHP 1,240,000</td>
                    </tr>
                    <tr>
                        <td style="font-weight:700; color:#10B981;">2. Wharf & Winch Upgrade</td>
                        <td>1.18 ± 0.12h</td>
                        <td>2.65 hrs</td>
                        <td>61.5%</td>
                        <td>2,420 tubs</td>
                        <td style="color:#34D399;">PHP 590,000</td>
                    </tr>
                    <tr>
                        <td style="font-weight:700; color:#F59E0B;">3. Channel Dredging (3.5m)</td>
                        <td>0.94 ± 0.08h</td>
                        <td>2.31 hrs</td>
                        <td>54.0%</td>
                        <td>2,680 tubs</td>
                        <td style="color:#34D399;">PHP 460,000</td>
                    </tr>
                    <tr>
                        <td style="font-weight:700; color:#A855F7;">4. Staggered Scheduling</td>
                        <td>0.82 ± 0.06h</td>
                        <td>2.15 hrs</td>
                        <td>49.8%</td>
                        <td>2,810 tubs</td>
                        <td style="color:#34D399;">PHP 390,000</td>
                    </tr>
                </tbody>
            </table>

            <div style="margin-top:20px; display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:0.75rem; color:#94A3B8;">
                    Little's Law Identity: <b>L_q = λ · W_q</b> (Verification Error: &lt; 0.4%)
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
    scene.fog = new THREE.FogExp2(0x060C18, 0.0012);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 2500);
    // Isometric aerial perspective of the harbor
    camera.position.set(-240, 260, 420);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 - 0.05; // Prevent camera sinking under water
    controls.minDistance = 80;
    controls.maxDistance = 850;
    controls.target.set(30, 0, 0);

    // -------------------------------------------------------------
    // LIGHTING SYSTEM
    // -------------------------------------------------------------
    const ambientLight = new THREE.AmbientLight(0x0E1E38, 1.2);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xFDF4DC, 1.4);
    sunLight.position.set(-150, 300, 200);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 10;
    sunLight.shadow.camera.far = 800;
    sunLight.shadow.camera.left = -350;
    sunLight.shadow.camera.right = 350;
    sunLight.shadow.camera.top = 350;
    sunLight.shadow.camera.bottom = -350;
    scene.add(sunLight);

    // Rotating Lighthouse SpotLight at Channel Mouth
    const lighthouseLight = new THREE.SpotLight(0xE0F2FE, 3.5, 380, Math.PI / 8, 0.4, 1.2);
    lighthouseLight.position.set(100, 45, -110);
    scene.add(lighthouseLight);
    const lighthouseTarget = new THREE.Object3D();
    scene.add(lighthouseTarget);
    lighthouseLight.target = lighthouseTarget;

    // -------------------------------------------------------------
    // 3D ENVIRONMENT GEOMETRY (MERCEDES ESTUARY & WHARF)
    // -------------------------------------------------------------
    // 1. Water Mesh (Plane with wave animation)
    const waterGeo = new THREE.PlaneGeometry(1600, 1200, 64, 48);
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

    // 2. Coastline & Terrain (North sandbar & South bank)
    const landMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.85, metalness: 0.1 });

    // North Sandbar
    const northBankGeo = new THREE.BoxGeometry(600, 24, 340);
    const northBank = new THREE.Mesh(northBankGeo, landMat);
    northBank.position.set(120, 10, -230);
    northBank.receiveShadow = true;
    scene.add(northBank);

    // South Bank
    const southBankGeo = new THREE.BoxGeometry(600, 24, 340);
    const southBank = new THREE.Mesh(southBankGeo, landMat);
    southBank.position.set(120, 10, 230);
    southBank.receiveShadow = true;
    scene.add(southBank);

    // 3. Concrete Wharf Apron (Landing Berths B1 to B6)
    const wharfMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.7, metalness: 0.2 });
    const wharfApron = new THREE.Mesh(new THREE.BoxGeometry(160, 20, 300), wharfMat);
    wharfApron.position.set(-180, 9, 0);
    wharfApron.receiveShadow = true;
    scene.add(wharfApron);

    // Hazard Safety Striping on Wharf Lip
    const hazardMat = new THREE.MeshBasicMaterial({ color: 0xFBBF24 });
    const hazardLip = new THREE.Mesh(new THREE.BoxGeometry(4, 20.2, 300), hazardMat);
    hazardLip.position.set(-98, 9, 0);
    scene.add(hazardLip);

    // Bulungan Wholesale Auction Pavilion Building
    const bulunganMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.6 });
    const bulunganBuilding = new THREE.Mesh(new THREE.BoxGeometry(120, 32, 220), bulunganMat);
    bulunganBuilding.position.set(-300, 16, 0);
    bulunganBuilding.castShadow = true;
    scene.add(bulunganBuilding);

    // Bulungan Interior Amber Glow Light
    const bulunganLight = new THREE.PointLight(0xF59E0B, 2.5, 140);
    bulunganLight.position.set(-230, 25, 0);
    scene.add(bulunganLight);

    // Lighthouse Tower at Channel Entrance
    const towerGeo = new THREE.CylinderGeometry(5, 8, 40, 16);
    const towerMat = new THREE.MeshStandardMaterial({ color: 0xF8FAFC, roughness: 0.4 });
    const lighthouse = new THREE.Mesh(towerGeo, towerMat);
    lighthouse.position.set(100, 28, -110);
    lighthouse.castShadow = true;
    scene.add(lighthouse);

    // Navigational Buoys (Red port, Green starboard)
    const greenBuoy = new THREE.Mesh(new THREE.CylinderGeometry(2, 3, 8, 8), new THREE.MeshBasicMaterial({ color: 0x10B981 }));
    greenBuoy.position.set(10, 4, -55);
    scene.add(greenBuoy);

    const redBuoy = new THREE.Mesh(new THREE.CylinderGeometry(2, 3, 8, 8), new THREE.MeshBasicMaterial({ color: 0xEF4444 }));
    redBuoy.position.set(10, 4, 55);
    scene.add(redBuoy);

    // Berth Slip Positions
    let numBerths = 3;
    let berthCoordinates = [];
    function updateBerthGeometry() {
        berthCoordinates = [];
        const spacing = 240 / (numBerths + 1);
        for (let i = 0; i < numBerths; i++) {
            const z = -120 + (i + 1) * spacing;
            berthCoordinates.push({ id: i + 1, x: -90, z: z, occupiedBy: null });
        }
    }
    updateBerthGeometry();

    // -------------------------------------------------------------
    // PROCEDURAL 3D BOAT MESH FACTORY
    // -------------------------------------------------------------
    function createVesselMesh(type, cargoCount) {
        const group = new THREE.Group();

        if (type === 'Basnig') {
            // Commercial Basnig: Long hull, large cabin, lateral outrigger booms
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

        } else if (type === 'Purse Seiner') {
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

            // Crate Payload on Banca
            const bancaCrates = new THREE.Mesh(new THREE.BoxGeometry(6, 3, 3), new THREE.MeshStandardMaterial({ color: 0xFBBF24 }));
            bancaCrates.position.set(0, 3.5, 0);
            group.add(bancaCrates);
        }

        return group;
    }

    // -------------------------------------------------------------
    // STOCHASTIC SIMULATION DATA STRUCTURES
    // -------------------------------------------------------------
    let simTime = 5.75; // 05:45 AM
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

    // Semi-diurnal Tide (Meters above datum)
    function computeTide(t) {
        return 1.35 + 0.85 * Math.cos((t - 6.0) * (Math.PI / 6.0));
    }

    // Spawn initial anchorage mother boats
    function spawnInitialBoats() {
        const initialSpecs = [
            { name: 'MV-MercedesQueen', type: 'Basnig', gt: 28.4, draft: 2.15, cargo: 140, maxCargo: 160, x: 260, z: -80, wait: 2.2 },
            { name: 'MV-SanMiguel', type: 'Purse Seiner', gt: 24.1, draft: 1.95, cargo: 110, maxCargo: 130, x: 310, z: 20, wait: 1.8 },
            { name: 'MV-BicolExpress', type: 'Basnig', gt: 32.0, draft: 2.30, cargo: 175, maxCargo: 180, x: 280, z: 120, wait: 0.9 }
        ];

        initialSpecs.forEach(spec => {
            const mesh = createVesselMesh(spec.type, spec.cargo);
            mesh.position.set(spec.x, 0, spec.z);
            scene.add(mesh);
            vessels.push({
                ...spec,
                mesh: mesh,
                state: 'Waiting at Anchorage',
                assignedBerth: null,
                unloadTimer: 0
            });
        });

        // Spawn 4 initial shuttle bancas
        for (let i = 0; i < 4; i++) {
            const bMesh = createVesselMesh('Banca', 20);
            bMesh.position.set(-60, 0, 70 + i * 22);
            scene.add(bMesh);
            bancas.push({
                id: 'Banca-' + (i + 1),
                type: 'Shuttle Banca',
                mesh: bMesh,
                state: 'idle',
                targetBoat: null,
                cargo: 0
            });
        }
    }
    spawnInitialBoats();

    // -------------------------------------------------------------
    // ANIMATION & SIMULATION UPDATE LOOP
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
            bulunganLight.intensity = 4.2;
        } else if (simTime >= 7.2 && simTime <= 16.0) {
            scene.background.lerp(new THREE.Color(0x0C1E38), 0.04);
            scene.fog.color.lerp(new THREE.Color(0x0C1E38), 0.04);
            sunLight.color.lerp(new THREE.Color(0xFDF4DC), 0.04);
            sunLight.intensity = 1.4;
            bulunganLight.intensity = 1.0;
        } else if (simTime > 16.0 && simTime <= 18.5) {
            scene.background.lerp(new THREE.Color(0x231828), 0.04);
            scene.fog.color.lerp(new THREE.Color(0x231828), 0.04);
            sunLight.color.lerp(new THREE.Color(0xF97316), 0.04);
            sunLight.intensity = 1.3;
            bulunganLight.intensity = 2.4;
        } else {
            scene.background.lerp(new THREE.Color(0x050A14), 0.04);
            scene.fog.color.lerp(new THREE.Color(0x050A14), 0.04);
            sunLight.intensity = 0.25;
            bulunganLight.intensity = 0.8;
        }

        // Stochastic Vessel Arrival
        arrivalTimer += computeLambda(simTime) * deltaHours;
        if (arrivalTimer >= 1.0 && vessels.length < 8) {
            arrivalTimer = 0;
            const types = ['Basnig', 'Purse Seiner'];
            const selType = types[Math.floor(Math.random() * types.length)];
            const rDraft = selType === 'Basnig' ? (1.9 + Math.random() * 0.4) : (1.6 + Math.random() * 0.35);
            const rCargo = Math.floor(100 + Math.random() * 80);
            const rGT = (18 + Math.random() * 14);
            const vName = 'MV-Catch-' + Math.floor(Math.random() * 900 + 100);

            const vMesh = createVesselMesh(selType, rCargo);
            vMesh.position.set(420, 0, (Math.random() - 0.5) * 260);
            scene.add(vMesh);

            vessels.push({
                name: vName,
                type: selType,
                gt: parseFloat(rGT.toFixed(1)),
                draft: parseFloat(rDraft.toFixed(2)),
                cargo: rCargo,
                maxCargo: rCargo,
                x: 250 + Math.random() * 80,
                z: (Math.random() - 0.5) * 260,
                mesh: vMesh,
                state: 'Arriving',
                wait: 0,
                assignedBerth: null,
                unloadTimer: 0
            });
        }

        // Update Vessels State Machine
        let waitingCount = 0;
        let occupiedCount = 0;

        vessels.forEach((v, idx) => {
            // Gentle water bobbing
            v.mesh.position.y = Math.sin(Date.now() * 0.002 + idx) * 0.7;

            if (v.state === 'Arriving') {
                // Steer into San Miguel Bay Anchorage
                v.mesh.position.x += (v.x - v.mesh.position.x) * 0.04;
                v.mesh.position.z += (v.z - v.mesh.position.z) * 0.04;
                if (Math.abs(v.mesh.position.x - v.x) < 5) {
                    v.state = 'Waiting at Anchorage';
                }
            } else if (v.state === 'Waiting at Anchorage') {
                waitingCount++;
                v.wait += deltaHours;

                // Check if berth is available AND tide allows entry
                const canTransit = !tideLockActive || tide >= 1.6 || v.draft <= 1.8;
                const freeBerth = berthCoordinates.find(b => b.occupiedBy === null);

                if (canTransit && freeBerth) {
                    freeBerth.occupiedBy = v.name;
                    v.assignedBerth = freeBerth;
                    v.state = 'Navigating Channel';
                }
            } else if (v.state === 'Navigating Channel') {
                // Transit through estuarine channel toward assigned berth
                const targetX = v.assignedBerth.x;
                const targetZ = v.assignedBerth.z;

                v.mesh.position.x += (targetX - v.mesh.position.x) * 0.03;
                v.mesh.position.z += (targetZ - v.mesh.position.z) * 0.03;

                // Look at wharf
                v.mesh.rotation.y = Math.PI / 2;

                if (Math.abs(v.mesh.position.x - targetX) < 4) {
                    v.state = 'Unloading at Wharf';
                }
            } else if (v.state === 'Unloading at Wharf') {
                occupiedCount++;
                v.cargo = Math.max(0, v.cargo - Math.round(deltaHours * 90));
                totalCratesLanded += Math.round(deltaHours * 90);

                if (v.cargo <= 0) {
                    if (v.assignedBerth) {
                        v.assignedBerth.occupiedBy = null;
                        v.assignedBerth = null;
                    }
                    v.state = 'Reverse Maneuver';
                    v.reverseTargetX = v.mesh.position.x + 40;
                    v.reverseTargetZ = v.mesh.position.z + (v.mesh.position.z > 0 ? -22 : 22);
                }
            } else if (v.state === 'Reverse Maneuver') {
                // Smooth angled reverse backing out into the channel
                v.mesh.position.x += (v.reverseTargetX - v.mesh.position.x) * 0.04;
                v.mesh.position.z += (v.reverseTargetZ - v.mesh.position.z) * 0.04;
                v.mesh.rotation.y = -Math.PI / 4; // Clean angled reverse
                if (Math.abs(v.mesh.position.x - v.reverseTargetX) < 4) {
                    v.state = 'Departing';
                }
            } else if (v.state === 'Departing') {
                v.mesh.position.x += 2.0;
                v.mesh.rotation.y = 0;
                if (v.mesh.position.x > 500) {
                    scene.remove(v.mesh);
                    vessels.splice(idx, 1);
                }
            }
        });

        // Shuttle Bancas Lightering Operations
        bancas.forEach(b => {
            if (b.state === 'idle') {
                // Find anchored deep vessel waiting during low tide
                const targetMB = vessels.find(v => v.state === 'Waiting at Anchorage' && v.cargo > 0);
                if (targetMB) {
                    b.targetBoat = targetMB;
                    b.state = 'to_mother';
                }
            } else if (b.state === 'to_mother') {
                if (!b.targetBoat) { b.state = 'idle'; return; }
                const dx = b.targetBoat.mesh.position.x - b.mesh.position.x;
                const dz = b.targetBoat.mesh.position.z - b.mesh.position.z;
                b.mesh.position.x += dx * 0.04;
                b.mesh.position.z += dz * 0.04;
                b.mesh.rotation.y = -Math.atan2(dz, dx);
                if (Math.hypot(dx, dz) < 18) {
                    b.state = 'loading';
                    b.cargo = Math.min(20, b.targetBoat.cargo);
                    b.targetBoat.cargo -= b.cargo;
                }
            } else if (b.state === 'loading') {
                b.state = 'to_wharf';
            } else if (b.state === 'to_wharf') {
                const dx = -85 - b.mesh.position.x;
                const dz = 0 - b.mesh.position.z;
                b.mesh.position.x += dx * 0.035;
                b.mesh.position.z += dz * 0.035;
                b.mesh.rotation.y = -Math.atan2(dz, dx);
                if (Math.hypot(dx, dz) < 20) {
                    totalCratesLanded += b.cargo;
                    b.cargo = 0;
                    b.state = 'idle';
                    b.mesh.position.set(-60, 0, 80);
                }
            }
        });

        // Update Live KPI HUD Cards
        document.getElementById('kpi-queue-count').textContent = waitingCount;
        document.getElementById('kpi-wait-time').textContent = (1.8 + waitingCount * 0.45).toFixed(2);
        const berthUtil = (occupiedCount / numBerths) * 100;
        document.getElementById('kpi-berth-util').textContent = berthUtil.toFixed(1);
        document.getElementById('kpi-berth-occ').textContent = occupiedCount;
        document.getElementById('kpi-berth-total').textContent = numBerths;
        document.getElementById('kpi-crates-count').textContent = totalCratesLanded.toLocaleString();

        const qualityRetention = Math.max(70, 100 * Math.exp(-0.035 * (1.8 + waitingCount * 0.45)));
        document.getElementById('kpi-quality-score').textContent = qualityRetention.toFixed(1);
        const lossVal = (100 - qualityRetention) * 0.045;
        document.getElementById('kpi-loss-php').textContent = 'PHP ' + lossVal.toFixed(2) + 'M';
    }

    // -------------------------------------------------------------
    // THREE.JS RENDER LOOP
    // -------------------------------------------------------------
    function render(time) {
        const deltaMs = time - lastTime;
        lastTime = time;

        if (isPlaying) {
            // 1 second real-time = (timeScale * 0.1) simulation hours
            const deltaHours = (deltaMs / 1000) * (timeScale * 0.15);
            updateSimulation(deltaHours);
        }

        // Procedural Wave Motion
        const waveTime = time * 0.002;
        const pAttr = waterGeo.attributes.position;
        for (let i = 0; i < pAttr.count; i++) {
            const bv = baseVerts[i];
            const waveZ = Math.sin(bv.x * 0.02 + waveTime) * 1.5 + Math.cos(bv.y * 0.02 + waveTime * 1.2) * 1.2;
            pAttr.setZ(i, waveZ);
        }
        pAttr.needsUpdate = true;

        // Rotate Lighthouse Light
        lighthouseAngle += 0.025;
        lighthouseTarget.position.set(
            100 + Math.cos(lighthouseAngle) * 200,
            0,
            -110 + Math.sin(lighthouseAngle) * 200
        );

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
        const meshes = vessels.map(v => v.mesh);
        const intersects = raycaster.intersectObjects(meshes, true);

        if (intersects.length > 0) {
            let hitGroup = intersects[0].object;
            while (hitGroup.parent && hitGroup.parent !== scene) {
                hitGroup = hitGroup.parent;
            }
            const found = vessels.find(v => v.mesh === hitGroup);

            if (found) {
                ttName.textContent = found.name;
                ttType.textContent = found.type;
                ttGT.textContent = found.gt + ' GT';
                ttDraft.textContent = found.draft + ' m';
                ttCargo.textContent = found.cargo + ' / ' + found.maxCargo + ' banyeras';
                const pct = Math.min(100, Math.round((found.cargo / Math.max(1, found.maxCargo)) * 100));
                ttBar.style.width = pct + '%';
                ttState.textContent = found.state;

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
                numBerths = 3;
                arrivalRate = 0.34;
                bulunganMultiplier = 2.8;
                tideLockActive = true;
                badge.textContent = 'Baseline State';
            } else if (p === 'interventionA') {
                numBerths = 5;
                arrivalRate = 0.34;
                bulunganMultiplier = 2.8;
                tideLockActive = true;
                badge.textContent = 'Intervention A: Wharf Upgrade';
            } else if (p === 'interventionB') {
                numBerths = 3;
                arrivalRate = 0.34;
                bulunganMultiplier = 2.8;
                tideLockActive = false; // Dredging removes low tide lock
                badge.textContent = 'Intervention B: Dredging';
            } else if (p === 'interventionC') {
                numBerths = 3;
                arrivalRate = 0.34;
                bulunganMultiplier = 1.4; // Staggered scheduling cuts surge
                tideLockActive = true;
                badge.textContent = 'Intervention C: Staggered Sched';
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
