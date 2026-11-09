# src/port_3d_engine.py
"""
Interactive 3D Discrete-Event Simulation (DES) Digital Twin Engine
for Mercedes Fish Port, Mercedes, Camarines Norte.

Architectural Standards Applied from Agency Agents Skills:
- C:/Users/L470/.gemini/config/skills/agency-frontend-developer/SKILL.md: Non-holonomic 3-DOF kinematics, 60fps budget, zero console errors.
- C:/Users/L470/.gemini/config/skills/agency-3d-scene-developer/SKILL.md: Accurate spatial lighting, buoy corridor fairway, wave displacement, seawalls.
- C:/Users/L470/.gemini/config/skills/agency-ux-architect/SKILL.md: Zero-clutter viewport, progressive disclosure modal hierarchy.
- C:/Users/L470/.gemini/config/skills/agency-ui-designer/SKILL.md: High-contrast maritime design tokens, WCAG AA compliance.

Core Mathematical & Spatial Systems:
1. Catch-Based Docking Timers (2-5 mins): Individual banyera loads with desynchronized startup and randomized departure delays.
2. Open Philippine Sea Loop: Departing boats fan out to X >= 235, transition to AT_SEA_FISHING, and respawn during diurnal surge.
3. Diurnal Fleet Cycle: 24-hour simulation curve (Morning Bulungan rush vs Noon ocean fishing lull) with expandable fleet sliders.
4. 3-Circle Hull Footprint Collision (Bow, Midship, Stern): Prevents clipping through 3D seawalls, wharf wings, and banks.
5. Organic Curved Trajectories: Per-boat lateral lane offsets, 12 distributed banca landing spots, and anchored weathervaning.
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

    #hud-bottom-left {
        position: absolute;
        bottom: 16px;
        left: 16px;
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

<canvas id="webgl-canvas"></canvas>

<!-- Top Floating HUD -->
<div id="hud-top">
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

    <div class="hud-group">
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
            <div class="kpi-sub"><span id="kpi-bancas-active" style="color:#FBBF24; font-weight:700;">0</span> Active Lightering | <span id="kpi-bancas-moored">32</span> Moored</div>
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
    <div class="tt-row"><span>Docking Timer Left:</span><span id="tt-vessel-timer" class="tt-val" style="color:#FBBF24;">145s (~2.4m)</span></div>
</div>

<!-- Modal 1: Settings -->
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

            <div id="tab-params" class="tab-content active">
                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Total Medium Commercial Vessels Fleet</div>
                        <div class="param-desc">Total fleet operating between San Miguel Bay fishing and port unloading.</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-medium-fleet" min="10" max="45" step="1" value="24">
                        <span id="val-medium-fleet" class="param-val">24 craft</span>
                    </div>
                </div>

                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Total Small Boats Fleet (Shuttle Bancas)</div>
                        <div class="param-desc">Pool of artisanal double-outrigger bancas for lightering and shallow ops.</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-bancas-fleet" min="15" max="60" step="1" value="32">
                        <span id="val-bancas-fleet" class="param-val">32 craft</span>
                    </div>
                </div>

                <div class="param-row">
                    <div class="param-info">
                        <div class="param-title">Medium Boat Unload Duration Range</div>
                        <div class="param-desc">Base scale for banyera offload times at berths (light: ~2m, heavy: ~5m).</div>
                    </div>
                    <div class="param-ctrl">
                        <input type="range" id="sl-unload-scale" min="1.0" max="5.0" step="0.5" value="3.0">
                        <span id="val-unload-scale" class="param-val">2–5 mins</span>
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

<!-- Modal 2: Analytics -->
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

<button id="screenshot-restore-btn">Restore UI Controls (Esc)</button>

<!-- -------------------------------------------------------------
     THREE.JS 3D ENGINE SCRIPT
     ------------------------------------------------------------- -->
<script>
(function() {
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
    camera.position.set(-95, 110, 160);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 - 0.04;
    controls.minDistance = 25;
    controls.maxDistance = 650;
    controls.target.set(20, 0, 0);

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
    // LIGHTHOUSE (LANTERN AT Y = 18.5)
    // -------------------------------------------------------------
    const LighthouseRoot = new THREE.Group();
    LighthouseRoot.position.set(45, 0, -65);
    scene.add(LighthouseRoot);

    const rockMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.9 });
    const rockBase = new THREE.Mesh(new THREE.CylinderGeometry(8, 10, 3, 8), rockMat);
    rockBase.position.set(0, 1.5, 0);
    rockBase.receiveShadow = true;
    LighthouseRoot.add(rockBase);

    const towerMat = new THREE.MeshStandardMaterial({ color: 0xF8FAFC, roughness: 0.4 });
    const towerGeo = new THREE.CylinderGeometry(2.2, 3.8, 18, 16);
    const towerMesh = new THREE.Mesh(towerGeo, towerMat);
    towerMesh.position.set(0, 9, 0);
    towerMesh.castShadow = true;
    LighthouseRoot.add(towerMesh);

    const stripeMat = new THREE.MeshStandardMaterial({ color: 0xDC2626, roughness: 0.4 });
    const stripe1 = new THREE.Mesh(new THREE.CylinderGeometry(2.9, 3.2, 3.2, 16), stripeMat);
    stripe1.position.set(0, 7.5, 0);
    LighthouseRoot.add(stripe1);

    const stripe2 = new THREE.Mesh(new THREE.CylinderGeometry(2.4, 2.6, 2.8, 16), stripeMat);
    stripe2.position.set(0, 14.2, 0);
    LighthouseRoot.add(stripe2);

    const LanternRoomGroup = new THREE.Group();
    LanternRoomGroup.position.set(0, 18.5, 0);
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
    // HARBOR ENVIRONMENT & SOLID 3D SEAWALL STRUCTURES
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

    // Coastal Landmass Banks
    const landMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.85 });
    const northBank = new THREE.Mesh(new THREE.BoxGeometry(340, 16, 160), landMat);
    northBank.position.set(80, 8, -152);
    northBank.receiveShadow = true;
    scene.add(northBank);

    const southBank = new THREE.Mesh(new THREE.BoxGeometry(340, 16, 160), landMat);
    southBank.position.set(80, 8, 152);
    southBank.receiveShadow = true;
    scene.add(southBank);

    // VISIBLE SOLID 3D CONCRETE SEAWALLS & BREAKWATERS
    const seawallMat = new THREE.MeshStandardMaterial({ color: 0x475569, roughness: 0.7, metalness: 0.3 });
    const seawallTopMat = new THREE.MeshStandardMaterial({ color: 0x64748B, roughness: 0.5 });

    // North Breakwater Coastal Wall (Z = -72, X: 10 to 240)
    const northSeawall = new THREE.Mesh(new THREE.BoxGeometry(230, 8, 6), seawallMat);
    northSeawall.position.set(125, 4, -72);
    scene.add(northSeawall);

    // South Breakwater Coastal Wall (Z = +72, X: 10 to 240)
    const southSeawall = new THREE.Mesh(new THREE.BoxGeometry(230, 8, 6), seawallMat);
    southSeawall.position.set(125, 4, 72);
    scene.add(southSeawall);

    // North Wharf Wing Wall (Z = -100, X: -60 to -32)
    const northWingWall = new THREE.Mesh(new THREE.BoxGeometry(30, 8, 6), seawallMat);
    northWingWall.position.set(-45, 4, -100);
    scene.add(northWingWall);

    // South Wharf Wing Wall (Z = +100, X: -60 to -32)
    const southWingWall = new THREE.Mesh(new THREE.BoxGeometry(30, 8, 6), seawallMat);
    southWingWall.position.set(-45, 4, 100);
    scene.add(southWingWall);

    // Small-Boat Basin Retaining Wall (X = -26, Z: 95 to 155)
    const basinRetainingWall = new THREE.Mesh(new THREE.BoxGeometry(6, 6, 60), seawallMat);
    basinRetainingWall.position.set(-26, 3, 125);
    scene.add(basinRetainingWall);

    // Concrete Wharf Apron (200 units long x 26 units wide x 6 units high)
    const wharfMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.7, metalness: 0.2 });
    const wharfApron = new THREE.Mesh(new THREE.BoxGeometry(26, 6, 200), wharfMat);
    wharfApron.position.set(-45, 3, 0);
    wharfApron.receiveShadow = true;
    scene.add(wharfApron);

    // Fendering along wharf edge
    const fenderMat = new THREE.MeshStandardMaterial({ color: 0x0F172A, roughness: 0.9 });
    const wharfFender = new THREE.Mesh(new THREE.BoxGeometry(1.2, 5.8, 200), fenderMat);
    wharfFender.position.set(-31.5, 3, 0);
    scene.add(wharfFender);

    // Safety Hazard Striping
    const hazardLip = new THREE.Mesh(
        new THREE.BoxGeometry(0.6, 6.1, 200),
        new THREE.MeshBasicMaterial({ color: 0xFBBF24 })
    );
    hazardLip.position.set(-31.9, 3, 0);
    scene.add(hazardLip);

    // Bulungan Wholesale Auction Sheds
    const shedMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.6 });
    const mainShed = new THREE.Mesh(new THREE.BoxGeometry(16, 9, 130), shedMat);
    mainShed.position.set(-51, 7.5, 0);
    mainShed.castShadow = true;
    scene.add(mainShed);

    const shedLight1 = new THREE.PointLight(0xF59E0B, 2.5, 60);
    shedLight1.position.set(-44, 9, -40);
    scene.add(shedLight1);

    const shedLight2 = new THREE.PointLight(0xF59E0B, 3.0, 70);
    shedLight2.position.set(-44, 9, 0);
    scene.add(shedLight2);

    const shedLight3 = new THREE.PointLight(0xF59E0B, 2.5, 60);
    shedLight3.position.set(-44, 9, 40);
    scene.add(shedLight3);

    // 13 Distinct Berths along Wharf Edge (X = -32, Z = -84 to +84)
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
        const startZ = -84;
        const spacing = 14;

        for (let i = 0; i < numBerths; i++) {
            const z = startZ + i * spacing;
            BERTH_SLOTS.push({
                id: i + 1,
                name: 'Berth B' + (i + 1),
                x: -32,
                dockX: -28.5,
                z: z,
                occupiedBy: null
            });

            const bollard = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.5, 1.2, 8), bollardMat);
            bollard.position.set(-31.6, 6.6, z);
            berthDecorGroup.add(bollard);

            const pad = new THREE.Mesh(new THREE.PlaneGeometry(2, 4), new THREE.MeshBasicMaterial({ color: 0xFBBF24 }));
            pad.rotation.x = -Math.PI / 2;
            pad.position.set(-33.5, 6.05, z);
            berthDecorGroup.add(pad);
        }
    }
    initBerths();

    // Shallow-water small boat mooring basin
    const woodMat = new THREE.MeshStandardMaterial({ color: 0x78350F, roughness: 0.8 });
    const woodPontoon = new THREE.Mesh(new THREE.BoxGeometry(18, 1.5, 60), woodMat);
    woodPontoon.position.set(-18, 0.75, 125);
    scene.add(woodPontoon);

    const BANCA_PARK_SLOTS = [];
    for (let i = 0; i < 16; i++) {
        BANCA_PARK_SLOTS.push({ x: -24, z: 100 + i * 3.4, yaw: Math.PI });
    }
    for (let i = 0; i < 16; i++) {
        BANCA_PARK_SLOTS.push({ x: -12, z: 100 + i * 3.4, yaw: 0 });
    }

    // 12 DISTRIBUTED BANCA LANDING POINTS ALONG SHALLOW APRON & MARKET STEPS
    const BANCA_LANDING_SPOTS = [];
    for (let i = 0; i < 12; i++) {
        BANCA_LANDING_SPOTS.push({ x: -28.0, z: 46 + i * 6.5 });
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
        { x: 155, zStarboard: -28, zPort: 28 }, // Pair 1: Outer Bay Entrance
        { x: 95,  zStarboard: -24, zPort: 24 }, // Pair 2: Anchorage Gateway
        { x: 35,  zStarboard: -20, zPort: 20 }, // Pair 3: Mid-Channel Fairway
        { x: -10, zStarboard: -18, zPort: 18 }  // Pair 4: Harbor Approach Gate
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
    // SOLID WALLS COLLISION AABBS
    // -------------------------------------------------------------
    const SOLID_WALLS = [
        { name: 'WHARF_MAIN', minX: -60, maxX: -31.5, minZ: -100, maxZ: 100 },
        { name: 'NORTH_WING', minX: -60, maxX: -31.5, minZ: -104, maxZ: -96 },
        { name: 'SOUTH_WING', minX: -60, maxX: -31.5, minZ: 96, maxZ: 104 },
        { name: 'BASIN_WALL', minX: -29, maxX: -23, minZ: 95, maxZ: 155 },
        { name: 'NORTH_BANK', minX: 10, maxX: 245, minZ: -160, maxZ: -69 },
        { name: 'SOUTH_BANK', minX: 10, maxX: 245, minZ: 69, maxZ: 160 }
    ];

    // -------------------------------------------------------------
    // NON-HOLONOMIC 3D BOAT MESH FACTORY (BOW STRICLY AT LOCAL +Z)
    // -------------------------------------------------------------
    function createVesselMesh(type) {
        const root = new THREE.Group();
        const meshVisualGroup = new THREE.Group();
        root.add(meshVisualGroup);

        if (type === 'Basnig') {
            const hullMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.6 });
            const hull = new THREE.Mesh(new THREE.BoxGeometry(4.4, 2.8, 13), hullMat);
            hull.position.y = 1.0;
            hull.castShadow = true;
            meshVisualGroup.add(hull);

            const bow = new THREE.Mesh(new THREE.ConeGeometry(2.2, 4.5, 4), hullMat);
            bow.rotation.x = Math.PI / 2;
            bow.position.set(0, 1.0, 7.5);
            meshVisualGroup.add(bow);

            const cabin = new THREE.Mesh(
                new THREE.BoxGeometry(3.2, 3.2, 5.0),
                new THREE.MeshStandardMaterial({ color: 0x475569 })
            );
            cabin.position.set(0, 3.2, -2.0);
            meshVisualGroup.add(cabin);

            const boomMat = new THREE.MeshBasicMaterial({ color: 0x94A3B8 });
            const boom = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 14), boomMat);
            boom.rotation.z = Math.PI / 2;
            boom.position.set(0, 3.8, 1.5);
            meshVisualGroup.add(boom);

            const crates = new THREE.Mesh(
                new THREE.BoxGeometry(2.6, 1.6, 3.5),
                new THREE.MeshStandardMaterial({ color: 0xD97706 })
            );
            crates.position.set(0, 2.0, 3.5);
            meshVisualGroup.add(crates);

        } else if (type === 'Purse Seiner' || type === 'Ring-Netter') {
            const hullMat = new THREE.MeshStandardMaterial({ color: 0x0F172A, roughness: 0.5 });
            const hull = new THREE.Mesh(new THREE.BoxGeometry(4.2, 2.8, 12), hullMat);
            hull.position.y = 1.0;
            hull.castShadow = true;
            meshVisualGroup.add(hull);

            const bow = new THREE.Mesh(new THREE.ConeGeometry(2.1, 4.0, 4), hullMat);
            bow.rotation.x = Math.PI / 2;
            bow.position.set(0, 1.0, 6.8);
            meshVisualGroup.add(bow);

            const wheelhouse = new THREE.Mesh(
                new THREE.BoxGeometry(3.2, 3.2, 3.8),
                new THREE.MeshStandardMaterial({ color: 0xE2E8F0 })
            );
            wheelhouse.position.set(0, 3.2, 2.5);
            meshVisualGroup.add(wheelhouse);

            const drum = new THREE.Mesh(
                new THREE.CylinderGeometry(1.2, 1.2, 3.2, 12),
                new THREE.MeshStandardMaterial({ color: 0x334155 })
            );
            drum.rotation.z = Math.PI / 2;
            drum.position.set(0, 2.2, -3.2);
            meshVisualGroup.add(drum);

        } else {
            const bancaMat = new THREE.MeshStandardMaterial({ color: 0x0284C7 });
            const hull = new THREE.Mesh(new THREE.BoxGeometry(1.2, 1.1, 5.5), bancaMat);
            hull.position.y = 0.5;
            meshVisualGroup.add(hull);

            const bow = new THREE.Mesh(new THREE.ConeGeometry(0.6, 2.0, 4), bancaMat);
            bow.rotation.x = Math.PI / 2;
            bow.position.set(0, 0.5, 3.4);
            meshVisualGroup.add(bow);

            const katigMat = new THREE.MeshStandardMaterial({ color: 0xF8FAFC });
            const float1 = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 4.8), katigMat);
            float1.rotation.x = Math.PI / 2;
            float1.position.set(-2.4, 0.35, 0);
            meshVisualGroup.add(float1);

            const float2 = float1.clone();
            float2.position.set(2.4, 0.35, 0);
            meshVisualGroup.add(float2);

            const strutMat = new THREE.MeshBasicMaterial({ color: 0xCBD5E1 });
            const strut = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 4.8), strutMat);
            strut.rotation.z = Math.PI / 2;
            strut.position.set(0, 0.8, 0.8);
            meshVisualGroup.add(strut);

            const crates = new THREE.Mesh(
                new THREE.BoxGeometry(0.8, 0.8, 1.8),
                new THREE.MeshStandardMaterial({ color: 0xFBBF24 })
            );
            crates.position.set(0, 0.9, 0);
            crates.name = 'cratesMesh';
            meshVisualGroup.add(crates);
        }

        const wakeGeo = new THREE.BufferGeometry();
        const wakeZTip = (type === 'Banca') ? 3.4 : 7.2;
        const wakeVertices = new Float32Array([
            0, 0.06, wakeZTip,      -1.4, 0.06, wakeZTip - 4.5,   -0.7, 0.06, wakeZTip - 4.5,
            0, 0.06, wakeZTip,       0.7, 0.06, wakeZTip - 4.5,    1.4, 0.06, wakeZTip - 4.5
        ]);
        wakeGeo.setAttribute('position', new THREE.BufferAttribute(wakeVertices, 3));

        const wakeMat = new THREE.MeshBasicMaterial({
            color: 0xE0F2FE,
            transparent: true,
            opacity: 0.0,
            depthWrite: false,
            side: THREE.DoubleSide,
            blending: THREE.AdditiveBlending
        });
        const bowWakeMesh = new THREE.Mesh(wakeGeo, wakeMat);
        bowWakeMesh.name = 'bowWake';
        root.add(bowWakeMesh);

        return root;
    }

    function getWaveHeight(x, z, t) {
        return Math.sin(x * 0.05 + t * 2.2) * 0.45 +
               Math.cos(z * 0.06 + t * 1.8) * 0.35 +
               Math.sin((x + z) * 0.04 + t * 1.2) * 0.25;
    }

    // -------------------------------------------------------------
    // FLEET SYSTEM & CATCH SIZE GENERATOR (2–5 MINS DOCKING TIMERS)
    // -------------------------------------------------------------
    let simTime = 5.75; // 05:45 AM
    let isPlaying = true;
    let timeScale = 1.0;
    let lastTime = performance.now();

    let arrivalRate = 0.34;
    let bulunganMultiplier = 2.8;
    let tideLockActive = true;
    let totalCratesLanded = 1420;

    let targetTotalMediumFleet = 24;
    let targetTotalBancas = 32;
    let unloadDurationScale = 3.0;

    const vessels = [];
    const bancas = [];

    // Helper: Generate randomized skewed catch load
    function rollCatchLoad() {
        const r = Math.random();
        let banyeras, durationSec, tier;
        if (r < 0.35) {
            // Light Catch: 30 to 90 banyeras (~120s / 2 mins)
            banyeras = Math.floor(30 + Math.random() * 61);
            durationSec = 110 + Math.random() * 25;
            tier = 'Light Catch (Fast Haul)';
        } else if (r < 0.75) {
            // Medium Catch: 100 to 200 banyeras (~180–220s / 3–3.5 mins)
            banyeras = Math.floor(100 + Math.random() * 101);
            durationSec = 180 + Math.random() * 40;
            tier = 'Medium Catch (Standard)';
        } else {
            // Heavy Catch: 210 to 380 banyeras (~240–300s / 4–5 mins)
            banyeras = Math.floor(210 + Math.random() * 171);
            durationSec = 240 + Math.random() * 60;
            tier = 'Heavy Catch (Bulk Haul)';
        }
        durationSec *= (unloadDurationScale / 3.0);
        return {
            banyeras: banyeras,
            maxCargo: banyeras,
            targetSec: durationSec,
            unloadRatePerSec: banyeras / durationSec,
            tier: tier
        };
    }

    function computeFishingDuration(hour) {
        // Longer expedition during midday (11:00 to 16:00), quicker return during morning rush
        const isRush = hour >= 4.0 && hour <= 9.5;
        if (isRush) {
            return 35 + Math.random() * 45; // 35–80s real-time
        } else if (hour >= 11.0 && hour <= 16.0) {
            return 120 + Math.random() * 120; // 120–240s (stay out fishing at noon)
        } else {
            return 60 + Math.random() * 60;
        }
    }

    function initFleet() {
        // Clear any existing
        vessels.forEach(v => scene.remove(v.mesh));
        vessels.length = 0;
        bancas.forEach(b => scene.remove(b.mesh));
        bancas.length = 0;

        // 1. Initial Docked Vessels at B2, B5, B8, B11 (Desynchronized startup!)
        const initialBerthIndices = [1, 4, 7, 10];
        const mediumNames = [
            'MV-MercedesQueen', 'MV-SanMiguel', 'MV-BicolExpress', 'MV-DaetStar',
            'MV-NagaPride', 'MV-PandanGem', 'MV-SanRoque', 'MV-BagongSilang',
            'MV-CamNorte', 'MV-PacificDawn', 'MV-Apolonio', 'MV-IslaVerde'
        ];

        for (let i = 0; i < targetTotalMediumFleet; i++) {
            const vName = mediumNames[i % mediumNames.length] + (i >= mediumNames.length ? `-${Math.floor(i/mediumNames.length)+1}` : '');
            const types = ['Basnig', 'Purse Seiner', 'Ring-Netter'];
            const selType = types[i % types.length];
            const rDraft = selType === 'Basnig' ? (1.9 + (i % 5) * 0.08) : (1.6 + (i % 4) * 0.08);
            const rGT = (18 + (i % 7) * 2.2);

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
                unloadRatePerSec: catchData.unloadRatePerSec,
                tier: catchData.tier,
                mesh: mesh,
                state: 'AT_SEA_FISHING',
                assignedBerth: null,
                servicedByBanca: null,
                wait: 0,
                heading: 0,
                speed: 0,
                maxSpeed: 14.0,
                maxReverseSpeed: 4.5,
                acceleration: 2.2,
                brakingDistance: 22.0,
                isSmallBoat: false,
                isReversing: false,
                bobOffset: Math.random() * Math.PI * 2,
                laneOffset: (Math.random() - 0.5) * 14.0,
                fishingTimer: 0,
                departureDelay: 0,
                reverseTimer: 0,
                remainingSec: catchData.targetSec,
                baseAnchorHeading: 0
            };

            if (i < 4) {
                // Docked at startup with desynchronized progress (15% to 92%)
                const bIdx = initialBerthIndices[i];
                const b = BERTH_SLOTS[bIdx];
                b.occupiedBy = v.name;
                v.assignedBerth = b;
                v.state = 'Unloading at Wharf';
                v.mesh.position.set(b.dockX, 0, b.z);
                v.heading = 0;
                v.mesh.rotation.y = 0;
                const initProg = 0.15 + (i * 0.22); // Desynchronized!
                v.cargo = Math.round(v.maxCargo * (1 - initProg));
                v.remainingSec = v.cargo / v.unloadRatePerSec;
                v.departureDelay = 6 + Math.random() * 18; // Staggered departure clearance!
            } else if (i < 7) {
                // Initial Waiting at Anchorage
                v.state = 'Waiting at Anchorage';
                v.holdX = 135 + (i - 4) * 12;
                v.holdZ = -45 + (i - 4) * 35;
                v.mesh.position.set(v.holdX, 0, v.holdZ);
                v.baseAnchorHeading = -Math.PI / 2;
                v.heading = v.baseAnchorHeading;
                v.mesh.rotation.y = v.heading;
                v.wait = 1.0 + (i - 4) * 0.6;
            } else {
                // Out in Philippine Sea fishing!
                v.state = 'AT_SEA_FISHING';
                v.mesh.visible = false;
                v.fishingTimer = computeFishingDuration(simTime) * (0.3 + (i - 7) * 0.15);
            }
            vessels.push(v);
        }

        // 2. Initial Small Bancas Fleet (Moored in Shallow Basin)
        for (let i = 0; i < targetTotalBancas; i++) {
            const slot = BANCA_PARK_SLOTS[i % BANCA_PARK_SLOTS.length];
            const bMesh = createVesselMesh('Banca');
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
                state: 'parked',
                parkSlot: slot,
                targetBoat: null,
                landingSlotIdx: i % BANCA_LANDING_SPOTS.length,
                serviceSide: (i % 2 === 0 ? 'port' : 'starboard'),
                cargo: 0,
                maxCargo: 25,
                heading: slot.yaw,
                speed: 0,
                maxSpeed: 18.0,
                maxReverseSpeed: 5.0,
                acceleration: 3.8,
                brakingDistance: 14.0,
                isSmallBoat: true,
                isReversing: false,
                bobOffset: Math.random() * Math.PI * 2,
                laneOffset: (Math.random() - 0.5) * 8.0,
                timer: 0
            });
        }
    }
    initFleet();

    // -------------------------------------------------------------
    // 3-CIRCLE HULL FOOTPRINT COLLISION CHECK
    // -------------------------------------------------------------
    function resolveHullCollision(boat) {
        const length = boat.isSmallBoat ? 5.5 : 13.0;
        const beam = boat.isSmallBoat ? 2.6 : 4.4;
        const dOffset = length / 2.4;
        const sinP = Math.sin(boat.heading);
        const cosP = Math.cos(boat.heading);

        const circles = [
            { x: boat.mesh.position.x + dOffset * sinP, z: boat.mesh.position.z + dOffset * cosP, r: beam * 0.6, name: 'bow' },
            { x: boat.mesh.position.x,                 z: boat.mesh.position.z,                 r: beam * 0.65, name: 'mid' },
            { x: boat.mesh.position.x - dOffset * sinP, z: boat.mesh.position.z - dOffset * cosP, r: beam * 0.6, name: 'stern' }
        ];

        for (const c of circles) {
            for (const wall of SOLID_WALLS) {
                // Closest point on wall AABB
                const qx = Math.max(wall.minX, Math.min(c.x, wall.maxX));
                const qz = Math.max(wall.minZ, Math.min(c.z, wall.maxZ));
                const dx = c.x - qx;
                const dz = c.z - qz;
                const distSq = dx * dx + dz * dz;

                if (distSq < c.r * c.r) {
                    const dist = Math.sqrt(distSq);
                    let nx = 0, nz = 0, pen = c.r - dist;

                    if (dist > 0.001) {
                        nx = dx / dist;
                        nz = dz / dist;
                    } else {
                        // Inside wall box: push to nearest face
                        const dLeft = Math.abs(c.x - wall.minX);
                        const dRight = Math.abs(c.x - wall.maxX);
                        const dTop = Math.abs(c.z - wall.minZ);
                        const dBottom = Math.abs(c.z - wall.maxZ);
                        const minD = Math.min(dLeft, dRight, dTop, dBottom);
                        if (minD === dLeft) { nx = -1; pen = dLeft + c.r; }
                        else if (minD === dRight) { nx = 1; pen = dRight + c.r; }
                        else if (minD === dTop) { nz = -1; pen = dTop + c.r; }
                        else { nz = 1; pen = dBottom + c.r; }
                    }

                    // Push boat out along outward normal
                    boat.mesh.position.x += nx * (pen + 0.3);
                    boat.mesh.position.z += nz * (pen + 0.3);

                    // Deflect heading away from wall
                    const dot = sinP * nx + cosP * nz;
                    if (dot < 0) {
                        boat.heading += Math.sign(dot) * 0.12;
                        boat.mesh.rotation.y = boat.heading;
                    }
                    boat.speed *= 0.6; // Hydrodynamic wall friction
                }
            }
        }
    }

    // -------------------------------------------------------------
    // NON-HOLONOMIC 3-DOF KINEMATIC UPDATE WITH WAYPOINT STEERING
    // -------------------------------------------------------------
    function updateVesselKinematics(boat, targetX, targetZ, dt) {
        const dx = targetX - boat.mesh.position.x;
        const dz = targetZ - boat.mesh.position.z;
        const distToTarget = Math.hypot(dx, dz);

        const desiredHeading = Math.atan2(dx, dz);

        let angleError = desiredHeading - boat.heading;
        while (angleError > Math.PI) angleError -= Math.PI * 2;
        while (angleError < -Math.PI) angleError += Math.PI * 2;

        const maxTurnRate = boat.isSmallBoat ? 1.8 : 0.85;
        const turnStep = Math.sign(angleError) * Math.min(Math.abs(angleError), maxTurnRate * dt);
        boat.heading += turnStep;
        boat.mesh.rotation.y = boat.heading;

        const turnSlowdown = Math.max(0.25, Math.cos(Math.min(Math.abs(angleError), Math.PI / 2)));
        const arrivalBraking = Math.min(1.0, distToTarget / Math.max(1.0, boat.brakingDistance));
        const targetSpeed = boat.isReversing 
            ? -boat.maxReverseSpeed 
            : boat.maxSpeed * turnSlowdown * arrivalBraking;

        boat.speed += (targetSpeed - boat.speed) * Math.min(1.0, boat.acceleration * dt);

        boat.mesh.position.x += Math.sin(boat.heading) * boat.speed * dt;
        boat.mesh.position.z += Math.cos(boat.heading) * boat.speed * dt;

        // Apply 3-Circle Hull Collision resolution against all solid seawalls
        resolveHullCollision(boat);

        return distToTarget;
    }

    // -------------------------------------------------------------
    // MAIN SIMULATION LOOP (DES + 24H DIURNAL TRAFFIC + KINEMATICS)
    // -------------------------------------------------------------
    // Semi-diurnal tidal height formula for Mercedes River mouth (San Miguel Bay)
    // Range: +0.60m (Low Tide) to +2.10m (High Tide) with ~12.42h periodicity
    function computeTide(t) {
        return 1.35 + 0.75 * Math.cos((t - 6.0) * (Math.PI / 6.0));
    }

    let bancaDispatchCooldown = 0;

    function updateSimulation(deltaHours, dt, waveTime) {
        simTime = (simTime + deltaHours) % 24.0;
        const tide = computeTide(simTime);

        // UI Clock & Status
        const clockH = Math.floor(simTime);
        const clockM = Math.floor((simTime - clockH) * 60);
        const ampm = clockH >= 12 ? 'PM' : 'AM';
        const displayH = clockH % 12 === 0 ? 12 : clockH % 12;
        document.getElementById('hud-clock').textContent =
            (displayH < 10 ? '0' : '') + displayH + ':' + (clockM < 10 ? '0' : '') + clockM + ' ' + ampm;

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
                v.fishingTimer -= dt;

                // Return trigger: timer finishes OR dawn surge awakens fleet
                const forceReturn = surgeActive && Math.random() < 0.008;
                if (v.fishingTimer <= 0 || forceReturn) {
                    // Respawn at scattered coordinate on eastern horizon
                    v.mesh.position.set(235, 0, -110 + Math.random() * 220);
                    v.heading = -Math.PI / 2 + (Math.random() - 0.5) * 0.35;
                    v.mesh.rotation.y = v.heading;

                    const newCatch = rollCatchLoad();
                    v.cargo = newCatch.banyeras;
                    v.maxCargo = newCatch.maxCargo;
                    v.targetSec = newCatch.targetSec;
                    v.unloadRatePerSec = newCatch.unloadRatePerSec;
                    v.tier = newCatch.tier;
                    v.remainingSec = newCatch.targetSec;

                    v.mesh.visible = true;
                    v.state = 'Arriving';
                    v.holdX = 135 + Math.random() * 25;
                    v.holdZ = -55 + Math.random() * 110;
                    v.wait = 0;
                }
            }
        });

        // UPDATE MEDIUM COMMERCIAL VESSELS
        let waitingCount = 0;
        let occupiedCount = 0;

        vessels.forEach(v => {
            if (!v.mesh.visible) return;

            // Wave Buoyancy Heave & Gentle Pitch
            const waveY = getWaveHeight(v.mesh.position.x, v.mesh.position.z, waveTime);
            v.mesh.position.y = waveY * 0.7;
            v.mesh.rotation.x = Math.sin(waveTime * 2.0 + v.bobOffset) * 0.03;

            // Bow Wake
            const bowWake = v.mesh.getObjectByName('bowWake');
            if (bowWake) {
                bowWake.material.opacity = THREE.MathUtils.lerp(
                    bowWake.material.opacity,
                    Math.min(0.55, Math.abs(v.speed) * 0.08),
                    0.15
                );
            }

            if (v.state === 'Arriving') {
                // Organic Curved Approach via Lane Offset
                const targetX = v.holdX;
                const targetZ = v.holdZ + v.laneOffset;
                const dist = updateVesselKinematics(v, targetX, targetZ, dt);
                if (dist < 5.0) {
                    v.state = 'Waiting at Anchorage';
                    v.baseAnchorHeading = v.heading;
                    v.speed = 0;
                }
            } else if (v.state === 'Waiting at Anchorage') {
                waitingCount++;
                v.wait += deltaHours;
                v.speed = 0;

                // Gentle Anchored Weathervaning with tidal current (±8 degrees)
                v.heading = v.baseAnchorHeading + Math.sin(simTime * 4.0 + v.bobOffset) * 0.14;
                v.mesh.rotation.y = v.heading;

                const canPass = !tideLockActive || tide >= 1.6 || v.draft <= 1.8;
                const freeBerth = BERTH_SLOTS.find(b => b.occupiedBy === null);

                if (canPass && freeBerth) {
                    freeBerth.occupiedBy = v.name;
                    v.assignedBerth = freeBerth;
                    v.state = 'Navigating Channel';
                    v.channelStep = 1;
                }
            } else if (v.state === 'Navigating Channel') {
                let targetX = 0;
                let targetZ = 0;

                if (v.channelStep === 1) {
                    // Gateway Buoy Pair 2 (X = 95) with organic lateral lane offset
                    targetX = 95;
                    targetZ = (v.assignedBerth.z * 0.3) + (v.laneOffset * 0.5);
                    const d = updateVesselKinematics(v, targetX, targetZ, dt);
                    if (d < 12.0) v.channelStep = 2;
                } else if (v.channelStep === 2) {
                    // Harbor Approach Buoy Pair 4 (X = -10)
                    targetX = -10;
                    targetZ = v.assignedBerth.z + (v.laneOffset * 0.2);
                    const d = updateVesselKinematics(v, targetX, targetZ, dt);
                    if (d < 8.0) v.channelStep = 3;
                } else {
                    // Final Docking alongside Berth (X = -28.5)
                    targetX = v.assignedBerth.dockX;
                    targetZ = v.assignedBerth.z;
                    const d = updateVesselKinematics(v, targetX, targetZ, dt);
                    if (d < 2.5) {
                        v.mesh.position.set(targetX, 0, targetZ);
                        v.heading = 0;
                        v.mesh.rotation.y = 0;
                        v.speed = 0;
                        v.state = 'Unloading at Wharf';
                        v.departureDelay = 6 + Math.random() * 18; // Randomized departure delay!
                    }
                }
            } else if (v.state === 'Unloading at Wharf') {
                occupiedCount++;
                v.speed = 0;

                // CATCH-BASED UNLOADING TIMER (Light: ~2m, Med: ~3m, Heavy: ~5m)
                const offloadAmt = v.unloadRatePerSec * dt * timeScale;
                v.cargo = Math.max(0, v.cargo - offloadAmt);
                totalCratesLanded += offloadAmt;
                v.remainingSec = Math.max(0, v.cargo / v.unloadRatePerSec);

                if (v.cargo <= 0) {
                    // Staggered departure clearance delay
                    v.departureDelay -= dt * timeScale;
                    if (v.departureDelay <= 0) {
                        if (v.assignedBerth) {
                            v.assignedBerth.occupiedBy = null;
                            v.assignedBerth = null;
                        }
                        v.state = 'Reverse Out';
                        v.reverseTimer = 3.5;
                        v.isReversing = true;
                    }
                }
            } else if (v.state === 'Reverse Out') {
                // Reverse straight back into fairway away from wharf face
                v.isReversing = true;
                v.reverseTimer -= dt;
                updateVesselKinematics(v, v.mesh.position.x + 8, v.mesh.position.z, dt);

                if (v.reverseTimer <= 0 || v.mesh.position.x >= -14) {
                    v.isReversing = false;
                    v.state = 'Departing';
                    v.departStep = 1;
                    // Assign unique fanned-out deep sea departure vector!
                    v.deepSeaTargetX = 280;
                    v.deepSeaTargetZ = -130 + Math.random() * 260;
                }
            } else if (v.state === 'Departing') {
                let depX = 0;
                let depZ = 0;

                if (v.departStep === 1) {
                    // Fairway Center Corridor (X = 35)
                    depX = 35;
                    depZ = (v.mesh.position.z * 0.5) + v.laneOffset;
                    const d = updateVesselKinematics(v, depX, depZ, dt);
                    if (d < 12.0) v.departStep = 2;
                } else if (v.departStep === 2) {
                    // Outer Bay Gate (X = 155)
                    depX = 155;
                    depZ = 10 + v.laneOffset;
                    const d = updateVesselKinematics(v, depX, depZ, dt);
                    if (d < 14.0) v.departStep = 3;
                } else {
                    // Fanned Out Ocean Departure (X >= 235: NO CLAMPING!)
                    depX = v.deepSeaTargetX;
                    depZ = v.deepSeaTargetZ;
                    updateVesselKinematics(v, depX, depZ, dt);

                    // TRANSITION TO AT_SEA_FISHING (Loop back into ocean expedition)
                    if (v.mesh.position.x >= 235) {
                        v.mesh.visible = false;
                        v.state = 'AT_SEA_FISHING';
                        v.speed = 0;
                        v.fishingTimer = computeFishingDuration(simTime);
                    }
                }
            }
        });

        // UPDATE SMALL BOAT FLEET (12+ DISTRIBUTED LANDING SPOTS & DYNAMIC LIGHTERING)
        let activeBancas = 0;
        bancaDispatchCooldown -= dt;

        bancas.forEach(b => {
            const waveY = getWaveHeight(b.mesh.position.x, b.mesh.position.z, waveTime);
            b.mesh.position.y = waveY * 0.6;

            const bowWake = b.mesh.getObjectByName('bowWake');
            if (bowWake) {
                bowWake.material.opacity = THREE.MathUtils.lerp(
                    bowWake.material.opacity,
                    Math.min(0.45, Math.abs(b.speed) * 0.08),
                    0.15
                );
            }

            if (b.state === 'parked') {
                b.mesh.position.x = b.parkSlot.x;
                b.mesh.position.z = b.parkSlot.z;
                b.mesh.rotation.y = b.parkSlot.yaw;
                b.speed = 0;

                // Anti-Snaking Staggered Launch: 1-to-1 mother vessel reservation + Port/Starboard standoff
                const runningCount = bancas.filter(item => item.state !== 'parked').length;
                if (runningCount < 5 && bancaDispatchCooldown <= 0) {
                    const targetMB = vessels.find(v => v.mesh.visible && v.state === 'Waiting at Anchorage' && v.cargo > 0 && !v.servicedByBanca);
                    if (targetMB) {
                        targetMB.servicedByBanca = b.id;
                        b.targetBoat = targetMB;
                        b.state = 'to_anchorage';
                        bancaDispatchCooldown = 3.2; // Stagger next launch
                    }
                }
            } else if (b.state === 'to_anchorage') {
                activeBancas++;
                if (!b.targetBoat || b.targetBoat.cargo <= 0 || !b.targetBoat.mesh.visible) {
                    b.state = 'return_to_park';
                    return;
                }
                // Port or Starboard standoff coordinate
                const sideOffset = (b.serviceSide === 'port' ? -5.5 : 5.5);
                const tx = b.targetBoat.mesh.position.x + sideOffset;
                const tz = b.targetBoat.mesh.position.z + (b.laneOffset * 0.2);
                const dist = updateVesselKinematics(b, tx, tz, dt);

                if (dist < 3.8) {
                    b.state = 'transferring';
                    b.timer = 2.0;
                    b.speed = 0;
                }
            } else if (b.state === 'transferring') {
                activeBancas++;
                b.speed = 0;
                b.timer -= dt;
                if (b.timer <= 0) {
                    const take = Math.min(b.maxCargo, b.targetBoat ? b.targetBoat.cargo : 0);
                    if (b.targetBoat) {
                        b.targetBoat.cargo -= take;
                        b.targetBoat.servicedByBanca = null;
                    }
                    b.cargo = take;
                    b.state = 'to_wharf';
                }
            } else if (b.state === 'to_wharf') {
                activeBancas++;
                // 12 DISTRIBUTED BANCA LANDING POINTS (No congestion bottleneck!)
                const landing = BANCA_LANDING_SPOTS[b.landingSlotIdx % BANCA_LANDING_SPOTS.length];
                const dist = updateVesselKinematics(b, landing.x, landing.z, dt);

                if (dist < 3.5) {
                    b.state = 'unloading_at_wharf';
                    b.timer = 1.6;
                    b.speed = 0;
                }
            } else if (b.state === 'unloading_at_wharf') {
                activeBancas++;
                b.speed = 0;
                b.timer -= dt;
                if (b.timer <= 0) {
                    totalCratesLanded += b.cargo;
                    b.cargo = 0;
                    b.state = 'return_to_park';
                }
            } else if (b.state === 'return_to_park') {
                activeBancas++;
                const dist = updateVesselKinematics(b, b.parkSlot.x, b.parkSlot.z, dt);

                if (dist < 2.0) {
                    b.mesh.position.set(b.parkSlot.x, 0, b.parkSlot.z);
                    b.heading = b.parkSlot.yaw;
                    b.mesh.rotation.y = b.parkSlot.yaw;
                    b.speed = 0;
                    b.state = 'parked';
                    b.targetBoat = null;
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

        // Ocean Wave Mesh Motion
        const pAttr = waterGeo.attributes.position;
        for (let i = 0; i < pAttr.count; i++) {
            const bv = baseVerts[i];
            const waveZ = Math.sin(bv.x * 0.04 + waveTime * 2.2) * 0.6 +
                          Math.cos(bv.y * 0.05 + waveTime * 1.8) * 0.45;
            pAttr.setZ(i, waveZ);
        }
        pAttr.needsUpdate = true;

        // Rotate Lighthouse Head at Top Lantern Room (Y = 18.5)
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
        const bancaMeshes = bancas.map(b => b.mesh);
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
                    ttTimer.textContent = `${Math.ceil(foundMedium.remainingSec)}s (${(foundMedium.remainingSec / 60).toFixed(1)}m remaining)`;
                } else if (foundMedium.state === 'Waiting at Anchorage') {
                    ttBadge.textContent = 'Distant Anchorage';
                    ttBadge.style.background = 'rgba(245, 158, 11, 0.2)';
                    ttBadge.style.color = '#FBBF24';
                    ttState.textContent = 'Holding in San Miguel Bay';
                    ttTimer.textContent = 'Awaiting berth clearance';
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

                if (foundBanca.state === 'parked') {
                    ttBadge.textContent = 'Moored at Dock';
                    ttBadge.style.background = 'rgba(148, 163, 184, 0.2)';
                    ttBadge.style.color = '#94A3B8';
                    ttState.textContent = 'Parked in Mooring Basin';
                    ttTimer.textContent = 'Standby';
                } else {
                    ttBadge.textContent = 'Active Lightering';
                    ttBadge.style.background = 'rgba(245, 158, 11, 0.2)';
                    ttBadge.style.color = '#FBBF24';
                    ttState.textContent = 'Fetching Banyeras from Bay';
                    ttTimer.textContent = 'In cycle';
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
        document.getElementById('val-unload-scale').textContent = `${(unloadDurationScale * 0.7).toFixed(1)}–${(unloadDurationScale * 1.6).toFixed(1)} mins`;
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
                targetTotalMediumFleet = 24;
                targetTotalBancas = 32;
                tideLockActive = true;
                badge.textContent = 'Baseline (13 Berths)';
            } else if (p === 'interventionA') {
                numBerths = 16;
                targetTotalMediumFleet = 30;
                targetTotalBancas = 36;
                unloadDurationScale = 1.8; // +50% offload speed
                tideLockActive = true;
                badge.textContent = 'Intervention A: 16 Berths';
            } else if (p === 'interventionB') {
                numBerths = 13;
                targetTotalMediumFleet = 24;
                targetTotalBancas = 32;
                tideLockActive = false;
                badge.textContent = 'Intervention B: Dredging';
            } else if (p === 'interventionC') {
                numBerths = 13;
                targetTotalMediumFleet = 24;
                targetTotalBancas = 32;
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
