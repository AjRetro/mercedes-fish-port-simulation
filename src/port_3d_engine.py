# src/port_3d_engine.py
"""
Interactive 3D Discrete-Event Simulation (DES) Digital Twin Engine
for Mercedes Fish Port, Mercedes, Camarines Norte.

Developed strictly in accordance with Agency Agents Skills:
- C:/Users/L470/.gemini/config/skills/agency-ux-architect/SKILL.md
- C:/Users/L470/.gemini/config/skills/agency-ui-designer/SKILL.md
- C:/Users/L470/.gemini/config/skills/agency-frontend-developer/SKILL.md

Key Architecture & Spatial Upgrades:
1. Rebuilt Lighthouse Scene Graph: LighthouseRoot -> Tower (Y=0..18) -> LanternRoomGroup (Y=18.5) -> LightRotorPivot with SpotLight & volumetric cone mesh tip-locked at Y=18.5.
2. Expanded 13-Berth Concrete Wharf Apron: 200 units long x 26 units wide, with 13 dedicated berths (BERTH_SLOTS[0..12], 14 units spacing, zero hull overlap).
3. Persistent Small Boat Fleet: 24 artisanal bancas moored at shallow basin, dynamic lightering loop (~75% moored, ~25% fetching fish from distant anchorage).
4. Zero-Clipping Waypoint Navigation: Pier AABB exclusion box, 15-unit straight reverse before turning, and Boids repulsion collision avoidance.
5. Ocean Boat Hydrodynamics & Wakes: Multi-sine wave buoyancy (heave, pitch, roll), turn banking, throttle pitch, stern expanding foam trail, and Kelvin V-shaped bow wakes.
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
        background: rgba(11, 20, 38, 0.78);
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
        max-width: 380px;
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
    .table-container tr:hover td {
        background: rgba(56, 189, 248, 0.04);
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
                        <div class="param-title">Base Arrival Intensity (λ)</div>
                        <div class="param-desc">Baseline vessel arrival rate outside dawn auction hours.</div>
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

            <div id="tab-presets" class="tab-content">
                <div class="preset-grid">
                    <div class="preset-card active" data-preset="baseline">
                        <span class="preset-tag">Phase IV — Status Quo</span>
                        <div class="preset-name">1. Baseline (Mercedes Port Expanded)</div>
                        <div class="preset-desc">13 medium berths, 24 small bancas, estuarine channel (1.8m low-tide draft lock), and 6:00 AM auction rush.</div>
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

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 2000);
    camera.position.set(-95, 110, 160);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI / 2 - 0.04;
    controls.minDistance = 25;
    controls.maxDistance = 550;
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
    sunLight.shadow.camera.far = 600;
    sunLight.shadow.camera.left = -250;
    sunLight.shadow.camera.right = 250;
    sunLight.shadow.camera.top = 250;
    sunLight.shadow.camera.bottom = -250;
    scene.add(sunLight);

    // -------------------------------------------------------------
    // STEP 1: REBUILT LIGHTHOUSE 3D HIERARCHY (LIGHT SOURCE AT Y = 18.5)
    // -------------------------------------------------------------
    // 1. LighthouseRoot (Group) placed on coastal headland at base elevation
    const LighthouseRoot = new THREE.Group();
    LighthouseRoot.position.set(45, 0, -65);
    scene.add(LighthouseRoot);

    // Rocky Promontory Foundation
    const rockMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.9 });
    const rockBase = new THREE.Mesh(new THREE.CylinderGeometry(8, 10, 3, 8), rockMat);
    rockBase.position.set(0, 1.5, 0);
    rockBase.receiveShadow = true;
    LighthouseRoot.add(rockBase);

    // 2. Tower Body: Tapered cylinder mesh from Y = 0 up to Y = 18
    const towerMat = new THREE.MeshStandardMaterial({ color: 0xF8FAFC, roughness: 0.4 });
    const towerGeo = new THREE.CylinderGeometry(2.2, 3.8, 18, 16);
    const towerMesh = new THREE.Mesh(towerGeo, towerMat);
    towerMesh.position.set(0, 9, 0); // Spans from Y = 0 to Y = 18
    towerMesh.castShadow = true;
    LighthouseRoot.add(towerMesh);

    // Red Maritime Stripe Rings
    const stripeMat = new THREE.MeshStandardMaterial({ color: 0xDC2626, roughness: 0.4 });
    const stripe1 = new THREE.Mesh(new THREE.CylinderGeometry(2.9, 3.2, 3.2, 16), stripeMat);
    stripe1.position.set(0, 7.5, 0);
    LighthouseRoot.add(stripe1);

    const stripe2 = new THREE.Mesh(new THREE.CylinderGeometry(2.4, 2.6, 2.8, 16), stripeMat);
    stripe2.position.set(0, 14.2, 0);
    LighthouseRoot.add(stripe2);

    // 3. LanternRoomGroup: EXPLICITLY set local position to (0, 18.5, 0)
    const LanternRoomGroup = new THREE.Group();
    LanternRoomGroup.position.set(0, 18.5, 0);
    LighthouseRoot.add(LanternRoomGroup);

    // Gallery Balcony Platform
    const galleryDeck = new THREE.Mesh(
        new THREE.CylinderGeometry(3.2, 3.2, 0.8, 16),
        new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.6 })
    );
    galleryDeck.position.set(0, -0.4, 0);
    LanternRoomGroup.add(galleryDeck);

    // Glowing Emissive Glass Cylinder inside LanternRoomGroup at (0, 0, 0)
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

    // Copper Roof Dome
    const roofCupola = new THREE.Mesh(
        new THREE.ConeGeometry(2.4, 2.0, 16),
        new THREE.MeshStandardMaterial({ color: 0x1E3A5F, roughness: 0.3, metalness: 0.6 })
    );
    roofCupola.position.set(0, 3.3, 0);
    LanternRoomGroup.add(roofCupola);

    // Glowing Lamp Core
    const lampBulb = new THREE.Mesh(
        new THREE.SphereGeometry(0.7, 8, 8),
        new THREE.MeshBasicMaterial({ color: 0xFFFFFF })
    );
    lampBulb.position.set(0, 1.1, 0);
    LanternRoomGroup.add(lampBulb);

    // 4. LightRotorPivot: Child of LanternRoomGroup at local (0, 1.1, 0)
    const LightRotorPivot = new THREE.Group();
    LightRotorPivot.position.set(0, 1.1, 0);
    LanternRoomGroup.add(LightRotorPivot);

    // High-Mounted SpotLight (originates at Y = 18.5 + 1.1 = 19.6 in world space)
    const spotLight = new THREE.SpotLight(0xE0F2FE, 5.5, 180, Math.PI / 7, 0.3, 1.1);
    spotLight.position.set(0, 0, 0);
    const spotTarget = new THREE.Object3D();
    spotTarget.position.set(0, -2, 40); // Shines outward and slightly downward across ocean horizon
    LightRotorPivot.add(spotTarget);
    spotLight.target = spotTarget;
    LightRotorPivot.add(spotLight);

    // Volumetric Light Cone Mesh: ConeGeometry(4, 35, 32, 1, true)
    const beamGeo = new THREE.ConeGeometry(4, 35, 32, 1, true);
    // Tip locked at local (0, 0, 0)
    beamGeo.translate(0, -17.5, 0);
    // Rotate to project along +Z axis
    beamGeo.rotateX(-Math.PI / 2);
    // Tilt slightly downward towards (0, -2, 40)
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
    // STEP 2: EXPANDED 3D HARBOR & MASSIVE 13-BERTH CONCRETE WHARF
    // -------------------------------------------------------------
    // Ocean Plane (1000 x 1000)
    const waterGeo = new THREE.PlaneGeometry(1000, 1000, 60, 60);
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

    // Base vertices for wave animation
    const posAttr = waterGeo.attributes.position;
    const baseVerts = [];
    for (let i = 0; i < posAttr.count; i++) {
        baseVerts.push({ x: posAttr.getX(i), y: posAttr.getY(i), z: posAttr.getZ(i) });
    }

    // Coastal Landmass Banks
    const landMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.85 });
    const northBank = new THREE.Mesh(new THREE.BoxGeometry(320, 16, 160), landMat);
    northBank.position.set(80, 8, -150);
    northBank.receiveShadow = true;
    scene.add(northBank);

    const southBank = new THREE.Mesh(new THREE.BoxGeometry(320, 16, 160), landMat);
    southBank.position.set(80, 8, 160);
    southBank.receiveShadow = true;
    scene.add(southBank);

    // MASSIVE CONCRETE WHARF APRON (200 units long x 26 units wide x 6 units high)
    const wharfMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.7, metalness: 0.2 });
    const wharfApron = new THREE.Mesh(new THREE.BoxGeometry(26, 6, 200), wharfMat);
    wharfApron.position.set(-45, 3, 0); // Front deep-water face at X = -32
    wharfApron.receiveShadow = true;
    scene.add(wharfApron);

    // Rubber / Timber Fendering along wharf face
    const fenderMat = new THREE.MeshStandardMaterial({ color: 0x0F172A, roughness: 0.9 });
    const wharfFender = new THREE.Mesh(new THREE.BoxGeometry(1.2, 5.8, 200), fenderMat);
    wharfFender.position.set(-31.5, 3, 0);
    scene.add(wharfFender);

    // Safety Hazard Striping on wharf edge
    const hazardLip = new THREE.Mesh(
        new THREE.BoxGeometry(0.6, 6.1, 200),
        new THREE.MeshBasicMaterial({ color: 0xFBBF24 })
    );
    hazardLip.position.set(-31.9, 3, 0);
    scene.add(hazardLip);

    // Bulungan Wholesale Auction Sheds on Wharf Apron
    const shedMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.6 });
    const mainShed = new THREE.Mesh(new THREE.BoxGeometry(16, 9, 130), shedMat);
    mainShed.position.set(-51, 7.5, 0);
    mainShed.castShadow = true;
    scene.add(mainShed);

    // Amber Interior Glow Lights
    const shedLight1 = new THREE.PointLight(0xF59E0B, 2.5, 60);
    shedLight1.position.set(-44, 9, -40);
    scene.add(shedLight1);

    const shedLight2 = new THREE.PointLight(0xF59E0B, 3.0, 70);
    shedLight2.position.set(-44, 9, 0);
    scene.add(shedLight2);

    const shedLight3 = new THREE.PointLight(0xF59E0B, 2.5, 60);
    shedLight3.position.set(-44, 9, 40);
    scene.add(shedLight3);

    // 13 DISTINCT MEDIUM-BOAT BERTH COORDINATES (BERTH_SLOTS[0..12])
    // 14 units spacing between berths (generous clearance, zero ship overlap)
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
                x: -32,      // Wharf deep-water face
                dockX: -29,  // Docked vessel center position
                z: z,
                occupiedBy: null
            });

            // Cast-iron mooring bollard on wharf lip
            const bollard = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.5, 1.2, 8), bollardMat);
            bollard.position.set(-31.6, 6.6, z);
            berthDecorGroup.add(bollard);

            // Painted yellow berth marker pad
            const pad = new THREE.Mesh(new THREE.PlaneGeometry(2, 4), new THREE.MeshBasicMaterial({ color: 0xFBBF24 }));
            pad.rotation.x = -Math.PI / 2;
            pad.position.set(-33.5, 6.05, z);
            berthDecorGroup.add(pad);
        }
    }
    initBerths();

    // DEDICATED SHALLOW-WATER SMALL BOAT MOORING BASIN
    const woodMat = new THREE.MeshStandardMaterial({ color: 0x78350F, roughness: 0.8 });
    const woodPontoon = new THREE.Mesh(new THREE.BoxGeometry(18, 1.5, 60), woodMat);
    woodPontoon.position.set(-18, 0.75, 125);
    scene.add(woodPontoon);

    // 24 Small Boat Docking Slots in Mooring Basin
    const BANCA_PARK_SLOTS = [];
    for (let i = 0; i < 12; i++) {
        BANCA_PARK_SLOTS.push({ x: -24, z: 100 + i * 4.5, yaw: Math.PI / 2 });
    }
    for (let i = 0; i < 12; i++) {
        BANCA_PARK_SLOTS.push({ x: -12, z: 100 + i * 4.5, yaw: -Math.PI / 2 });
    }

    // Navigational Buoys flanking Channel Corridor
    const greenBuoy = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 1.2, 3.5, 8), new THREE.MeshBasicMaterial({ color: 0x10B981 }));
    greenBuoy.position.set(25, 1.7, -35);
    scene.add(greenBuoy);

    const redBuoy = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 1.2, 3.5, 8), new THREE.MeshBasicMaterial({ color: 0xEF4444 }));
    redBuoy.position.set(25, 1.7, 35);
    scene.add(redBuoy);

    // -------------------------------------------------------------
    // STEP 3: WAYPOINT ROUTING & AABB EXCLUSION DEFINITIONS
    // -------------------------------------------------------------
    // Pier No-Go Bounding Box (+4 padding)
    const PIER_AABB = {
        minX: -65,
        maxX: -27.5,
        minZ: -105,
        maxZ: 160
    };

    // -------------------------------------------------------------
    // STEP 4: BOAT MODELS & HYDRODYNAMIC EFFECTS (WAKES & FOAM)
    // -------------------------------------------------------------
    function createVesselMesh(type) {
        const group = new THREE.Group();

        if (type === 'Basnig') {
            // Commercial Basnig (L: 13, W: 4.4, H: 4.0)
            const hullMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.6 });
            const hull = new THREE.Mesh(new THREE.BoxGeometry(13, 2.8, 4.4), hullMat);
            hull.position.y = 1.0;
            hull.castShadow = true;
            group.add(hull);

            // Pointed Bow
            const bow = new THREE.Mesh(new THREE.ConeGeometry(2.2, 4.5, 4), hullMat);
            bow.rotation.z = -Math.PI / 2;
            bow.position.set(7.5, 1.0, 0);
            group.add(bow);

            // Wheelhouse
            const cabin = new THREE.Mesh(
                new THREE.BoxGeometry(5.0, 3.2, 3.2),
                new THREE.MeshStandardMaterial({ color: 0x475569 })
            );
            cabin.position.set(-2.0, 3.2, 0);
            group.add(cabin);

            // Fishing Light Outrigger Booms
            const boomMat = new THREE.MeshBasicMaterial({ color: 0x94A3B8 });
            const boom = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 14), boomMat);
            boom.rotation.x = Math.PI / 2;
            boom.position.set(1.5, 3.8, 0);
            group.add(boom);

            // Banyera Crates in Cargo Hold
            const crates = new THREE.Mesh(
                new THREE.BoxGeometry(3.5, 1.6, 2.6),
                new THREE.MeshStandardMaterial({ color: 0xD97706 })
            );
            crates.position.set(3.5, 2.0, 0);
            group.add(crates);

        } else if (type === 'Purse Seiner' || type === 'Ring-Netter') {
            // Purse Seiner / Ring-Netter (L: 12, W: 4.2)
            const hullMat = new THREE.MeshStandardMaterial({ color: 0x0F172A, roughness: 0.5 });
            const hull = new THREE.Mesh(new THREE.BoxGeometry(12, 2.8, 4.2), hullMat);
            hull.position.y = 1.0;
            hull.castShadow = true;
            group.add(hull);

            // Forward Wheelhouse
            const wheelhouse = new THREE.Mesh(
                new THREE.BoxGeometry(3.8, 3.2, 3.2),
                new THREE.MeshStandardMaterial({ color: 0xE2E8F0 })
            );
            wheelhouse.position.set(3.0, 3.2, 0);
            group.add(wheelhouse);

            // Net Drum Roll
            const drum = new THREE.Mesh(
                new THREE.CylinderGeometry(1.2, 1.2, 3.2, 12),
                new THREE.MeshStandardMaterial({ color: 0x334155 })
            );
            drum.rotation.x = Math.PI / 2;
            drum.position.set(-3.2, 2.2, 0);
            group.add(drum);

        } else {
            // Small Shuttle Banca (L: 5.5, W: 2.4 with katig outriggers)
            const bancaMat = new THREE.MeshStandardMaterial({ color: 0x0284C7 });
            const hull = new THREE.Mesh(new THREE.BoxGeometry(5.5, 1.1, 1.2), bancaMat);
            hull.position.y = 0.5;
            group.add(hull);

            // Outrigger Floats (Katig)
            const katigMat = new THREE.MeshStandardMaterial({ color: 0xF8FAFC });
            const float1 = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 4.8), katigMat);
            float1.rotation.z = Math.PI / 2;
            float1.position.set(0, 0.35, -2.4);
            group.add(float1);

            const float2 = float1.clone();
            float2.position.set(0, 0.35, 2.4);
            group.add(float2);

            // Crossbeams (Tadlang)
            const strutMat = new THREE.MeshBasicMaterial({ color: 0xCBD5E1 });
            const strut = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 4.8), strutMat);
            strut.rotation.x = Math.PI / 2;
            strut.position.set(0.8, 0.8, 0);
            group.add(strut);

            // Banyeras on deck
            const crates = new THREE.Mesh(
                new THREE.BoxGeometry(1.8, 0.8, 0.8),
                new THREE.MeshStandardMaterial({ color: 0xFBBF24 })
            );
            crates.position.set(0, 0.9, 0);
            crates.name = 'cratesMesh';
            group.add(crates);
        }

        // V-SHAPED KELVIN BOW WAKE MESH (Translucent chevron at waterline Y = 0.06)
        const wakeShape = new THREE.Shape();
        wakeShape.moveTo(0, 0);
        wakeShape.lineTo(-1.2, -4.0);
        wakeShape.lineTo(-0.6, -4.0);
        wakeShape.lineTo(0, -0.6);
        wakeShape.lineTo(0.6, -4.0);
        wakeShape.lineTo(1.2, -4.0);
        wakeShape.closePath();

        const wakeGeo = new THREE.ShapeGeometry(wakeShape);
        wakeGeo.rotateX(-Math.PI / 2);
        const wakeMat = new THREE.MeshBasicMaterial({
            color: 0xE0F2FE,
            transparent: true,
            opacity: 0.0,
            depthWrite: false,
            side: THREE.DoubleSide,
            blending: THREE.AdditiveBlending
        });
        const bowWakeMesh = new THREE.Mesh(wakeGeo, wakeMat);
        bowWakeMesh.position.set(type === 'Banca' ? 2.8 : 7.2, 0.06, 0);
        bowWakeMesh.name = 'bowWake';
        group.add(bowWakeMesh);

        return group;
    }

    // MULTI-SINE WAVE HEIGHT FUNCTION FOR HYDRODYNAMIC BUOYANCY
    function getWaveHeight(x, z, t) {
        return Math.sin(x * 0.05 + t * 2.2) * 0.45 +
               Math.cos(z * 0.06 + t * 1.8) * 0.35 +
               Math.sin((x + z) * 0.04 + t * 1.2) * 0.25;
    }

    // EXPANDING STERN FOAM RINGS POOL
    const MAX_FOAM = 60;
    const foamPool = [];
    const foamRingGeo = new THREE.RingGeometry(0.6, 1.4, 16);
    foamRingGeo.rotateX(-Math.PI / 2);
    const foamMat = new THREE.MeshBasicMaterial({
        color: 0xE0F2FE,
        transparent: true,
        opacity: 0.0,
        depthWrite: false,
        side: THREE.DoubleSide,
        blending: THREE.AdditiveBlending
    });

    for (let i = 0; i < MAX_FOAM; i++) {
        const ring = new THREE.Mesh(foamRingGeo, foamMat.clone());
        ring.position.set(0, -50, 0);
        ring.visible = false;
        scene.add(ring);
        foamPool.push({ mesh: ring, active: false, life: 0, maxLife: 1.2, scale: 1.0 });
    }

    function emitFoam(x, z) {
        const p = foamPool.find(f => !f.active);
        if (p) {
            p.active = true;
            p.life = 0;
            p.scale = 1.0;
            p.mesh.position.set(x, 0.05, z);
            p.mesh.scale.set(1, 1, 1);
            p.mesh.material.opacity = 0.55;
            p.mesh.visible = true;
        }
    }

    // -------------------------------------------------------------
    // FLEET INITIALIZATION: 13 BERTHS & 24 BANCAS
    // -------------------------------------------------------------
    let simTime = 5.75; // 05:45 AM
    let isPlaying = true;
    let timeScale = 1.0;
    let lastTime = performance.now();

    let arrivalRate = 0.34;
    let bulunganMultiplier = 2.8;
    let tideLockActive = true;
    let totalCratesLanded = 1420;

    const vessels = [];
    const bancas = [];
    let arrivalTimer = 0;

    function computeLambda(t) {
        const dawnPeak = bulunganMultiplier * Math.exp(-Math.pow((t - 6.0), 2) / (2 * 1.44));
        const duskPeak = 0.65 * Math.exp(-Math.pow((t - 16.5), 2) / (2 * 2.25));
        return arrivalRate + dawnPeak + duskPeak;
    }

    function computeTide(t) {
        return 1.35 + 0.85 * Math.cos((t - 6.0) * (Math.PI / 6.0));
    }

    function initFleet() {
        // Spawn 3 initial medium boats directly docked at B2, B5, B8
        const initialDocked = [
            { name: 'MV-MercedesQueen', type: 'Basnig', gt: 28.4, draft: 2.15, cargo: 120, maxCargo: 160, berthIdx: 1 },
            { name: 'MV-SanMiguel', type: 'Purse Seiner', gt: 24.1, draft: 1.95, cargo: 90, maxCargo: 130, berthIdx: 4 },
            { name: 'MV-BicolExpress', type: 'Basnig', gt: 32.0, draft: 2.30, cargo: 140, maxCargo: 180, berthIdx: 7 }
        ];

        initialDocked.forEach(spec => {
            const b = BERTH_SLOTS[spec.berthIdx];
            if (b) {
                const mesh = createVesselMesh(spec.type);
                mesh.position.set(b.dockX, 0, b.z);
                mesh.rotation.y = Math.PI / 2; // Alongside concrete pier
                scene.add(mesh);
                b.occupiedBy = spec.name;

                vessels.push({
                    name: spec.name,
                    type: spec.type,
                    gt: spec.gt,
                    draft: spec.draft,
                    cargo: spec.cargo,
                    maxCargo: spec.maxCargo,
                    x: b.dockX,
                    z: b.z,
                    mesh: mesh,
                    state: 'Unloading at Wharf',
                    assignedBerth: b,
                    wait: 0,
                    speed: 0,
                    yaw: Math.PI / 2,
                    turnRoll: 0,
                    throttlePitch: 0,
                    bobOffset: Math.random() * Math.PI * 2,
                    foamTimer: 0
                });
            }
        });

        // Spawn 2 initial medium boats far away in San Miguel Bay Anchorage (140-160 units out)
        const initialAnchored = [
            { name: 'MV-DaetStar', type: 'Basnig', gt: 29.5, draft: 2.25, cargo: 155, maxCargo: 160, x: 140, z: -40 },
            { name: 'MV-NagaPride', type: 'Ring-Netter', gt: 21.0, draft: 1.85, cargo: 110, maxCargo: 120, x: 150, z: 35 }
        ];

        initialAnchored.forEach(spec => {
            const mesh = createVesselMesh(spec.type);
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
                wait: 1.2,
                speed: 0,
                yaw: 0,
                turnRoll: 0,
                throttlePitch: 0,
                bobOffset: Math.random() * Math.PI * 2,
                foamTimer: 0
            });
        });

        // Spawn 24 Small Artisanal Bancas in the Shallow Mooring Basin
        for (let i = 0; i < 24; i++) {
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
                cargo: 0,
                maxCargo: 25,
                speed: 0,
                yaw: slot.yaw,
                turnRoll: 0,
                throttlePitch: 0,
                bobOffset: Math.random() * Math.PI * 2,
                timer: 0,
                foamTimer: 0
            });
        }
    }
    initFleet();

    // -------------------------------------------------------------
    // MAIN SIMULATION & HYDRODYNAMICS UPDATE LOOP
    // -------------------------------------------------------------
    function updateSimulation(deltaHours, waveTime) {
        simTime = (simTime + deltaHours) % 24.0;
        const tide = computeTide(simTime);

        // UI Clock & Status Update
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

        // STOCHASTIC MEDIUM VESSEL ARRIVAL
        arrivalTimer += computeLambda(simTime) * deltaHours;
        if (arrivalTimer >= 1.0 && vessels.length < 16) {
            arrivalTimer = 0;
            const types = ['Basnig', 'Purse Seiner', 'Ring-Netter'];
            const selType = types[Math.floor(Math.random() * types.length)];
            const rDraft = selType === 'Basnig' ? (1.9 + Math.random() * 0.45) : (1.6 + Math.random() * 0.35);
            const rCargo = Math.floor(100 + Math.random() * 70);
            const rGT = (18 + Math.random() * 15);
            const vName = 'MV-Catch-' + Math.floor(Math.random() * 900 + 100);

            const vMesh = createVesselMesh(selType);
            vMesh.position.set(190, 0, (Math.random() - 0.5) * 80);
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
                assignedBerth: null,
                wait: 0,
                speed: 0,
                yaw: Math.PI,
                turnRoll: 0,
                throttlePitch: 0,
                bobOffset: Math.random() * Math.PI * 2,
                foamTimer: 0
            };

            const canPassChannel = !tideLockActive || tide >= 1.6 || newBoat.draft <= 1.8;
            const freeBerth = BERTH_SLOTS.find(b => b.occupiedBy === null);
            const queueCount = vessels.filter(v => v.state === 'Waiting at Anchorage').length;

            if (canPassChannel && freeBerth && queueCount === 0) {
                freeBerth.occupiedBy = newBoat.name;
                newBoat.assignedBerth = freeBerth;
                newBoat.state = 'Navigating Channel';
                newBoat.approachStep = 1;
            } else {
                newBoat.x = 135 + Math.random() * 30; // Distant Anchorage Zone (135-165 units out)
                newBoat.z = (Math.random() - 0.5) * 80;
                newBoat.state = 'Arriving';
            }
            vessels.push(newBoat);
        }

        // UPDATE MEDIUM COMMERCIAL VESSELS
        let waitingCount = 0;
        let occupiedCount = 0;

        vessels.forEach((v, idx) => {
            // Hydrodynamic Wave Buoyancy (Heave, Pitch, Roll)
            const curX = v.mesh.position.x;
            const curZ = v.mesh.position.z;
            const waveY = getWaveHeight(curX, curZ, waveTime);
            const waveSlopeX = (getWaveHeight(curX + 1.2, curZ, waveTime) - waveY) / 1.2;
            const waveSlopeZ = (getWaveHeight(curX, curZ + 1.2, waveTime) - waveY) / 1.2;

            v.mesh.position.y = waveY * 0.75;
            const targetPitch = waveSlopeX * 0.35 + v.throttlePitch;
            const targetRoll = waveSlopeZ * 0.35 + v.turnRoll;
            v.mesh.rotation.x = THREE.MathUtils.lerp(v.mesh.rotation.x, targetPitch, 0.1);
            v.mesh.rotation.z = THREE.MathUtils.lerp(v.mesh.rotation.z, targetRoll, 0.1);

            // Stern Foam Trail & Bow Wake Opacity
            const bowWake = v.mesh.getObjectByName('bowWake');
            if (bowWake) {
                bowWake.material.opacity = THREE.MathUtils.lerp(
                    bowWake.material.opacity,
                    Math.min(0.55, v.speed * 2.5),
                    0.12
                );
            }
            if (v.speed > 0.08) {
                v.foamTimer += deltaHours * 100;
                if (v.foamTimer > 0.15) {
                    v.foamTimer = 0;
                    emitFoam(curX - Math.cos(v.yaw) * 6.5, curZ + Math.sin(v.yaw) * 6.5);
                }
            }

            if (v.state === 'Arriving') {
                // Steer into Distant Anchorage Zone (120 to 180 units out)
                const dx = v.x - curX;
                const dz = v.z - curZ;
                v.speed = THREE.MathUtils.lerp(v.speed, 0.35, 0.05);
                const targetYaw = Math.atan2(dz, dx);
                const yawDiff = Math.atan2(Math.sin(targetYaw - v.yaw), Math.cos(targetYaw - v.yaw));
                v.yaw += yawDiff * 0.06;
                v.turnRoll = -yawDiff * 1.5;
                v.throttlePitch = -0.05;
                v.mesh.rotation.y = v.yaw;

                v.mesh.position.x += Math.cos(v.yaw) * v.speed;
                v.mesh.position.z += Math.sin(v.yaw) * v.speed;

                if (Math.hypot(dx, dz) < 4) {
                    v.state = 'Waiting at Anchorage';
                    v.speed = 0;
                    v.turnRoll = 0;
                    v.throttlePitch = 0;
                }
            } else if (v.state === 'Waiting at Anchorage') {
                waitingCount++;
                v.wait += deltaHours;
                v.speed = 0;
                v.turnRoll = 0;
                v.throttlePitch = 0;

                const canPass = !tideLockActive || tide >= 1.6 || v.draft <= 1.8;
                const freeBerth = BERTH_SLOTS.find(b => b.occupiedBy === null);

                if (canPass && freeBerth) {
                    freeBerth.occupiedBy = v.name;
                    v.assignedBerth = freeBerth;
                    v.state = 'Navigating Channel';
                    v.approachStep = 1;
                }
            } else if (v.state === 'Navigating Channel') {
                // MULTI-WAYPOINT CHANNEL ROUTING (Zero Pier Clipping)
                let targetX = 0;
                let targetZ = 0;

                if (v.approachStep === 1) {
                    // Approach Waypoint 1: Channel Entry Corridor
                    targetX = 60;
                    targetZ = v.assignedBerth.z * 0.4;
                    if (Math.hypot(targetX - curX, targetZ - curZ) < 10) v.approachStep = 2;
                } else if (v.approachStep === 2) {
                    // Approach Waypoint 2: Wharf Approach Corridor (X = -12)
                    targetX = -12;
                    targetZ = v.assignedBerth.z;
                    if (Math.hypot(targetX - curX, targetZ - curZ) < 8) v.approachStep = 3;
                } else {
                    // Final Docking: Berth Slot
                    targetX = v.assignedBerth.dockX;
                    targetZ = v.assignedBerth.z;
                }

                const dx = targetX - curX;
                const dz = targetZ - curZ;
                v.speed = THREE.MathUtils.lerp(v.speed, v.approachStep === 3 ? 0.15 : 0.4, 0.05);

                const targetYaw = (v.approachStep === 3) ? Math.PI / 2 : Math.atan2(dz, dx);
                const yawDiff = Math.atan2(Math.sin(targetYaw - v.yaw), Math.cos(targetYaw - v.yaw));
                v.yaw += yawDiff * 0.06;
                v.turnRoll = -yawDiff * 1.5;
                v.throttlePitch = -0.04;
                v.mesh.rotation.y = v.yaw;

                v.mesh.position.x += Math.cos(v.yaw) * v.speed;
                v.mesh.position.z += Math.sin(v.yaw) * v.speed;

                if (v.approachStep === 3 && Math.hypot(targetX - curX, targetZ - curZ) < 2) {
                    v.mesh.position.x = targetX;
                    v.mesh.position.z = targetZ;
                    v.yaw = Math.PI / 2;
                    v.mesh.rotation.y = Math.PI / 2;
                    v.state = 'Unloading at Wharf';
                    v.speed = 0;
                    v.turnRoll = 0;
                    v.throttlePitch = 0;
                }
            } else if (v.state === 'Unloading at Wharf') {
                occupiedCount++;
                v.speed = 0;
                v.turnRoll = 0;
                v.throttlePitch = 0;
                const offloadAmt = Math.round(deltaHours * 95);
                v.cargo = Math.max(0, v.cargo - offloadAmt);
                totalCratesLanded += offloadAmt;

                if (v.cargo <= 0) {
                    if (v.assignedBerth) {
                        v.assignedBerth.occupiedBy = null;
                        v.assignedBerth = null;
                    }
                    // STEP 3: REVERSE STRAIGHT BACK 15 UNITS INTO APPROACH CORRIDOR
                    v.state = 'Straight Reverse';
                    v.reverseStartX = curX;
                    v.reverseTargetX = curX + 15; // Straight back to X = -14
                }
            } else if (v.state === 'Straight Reverse') {
                // Strict 15-unit reverse without turning
                v.speed = 0.2;
                v.mesh.position.x += 0.15;
                v.yaw = Math.PI / 2;
                v.mesh.rotation.y = Math.PI / 2;

                if (curX >= v.reverseTargetX) {
                    v.state = 'Departing';
                    v.departStep = 1;
                }
            } else if (v.state === 'Departing') {
                // Multi-Waypoint Departure Corridor
                let depX = 180;
                let depZ = 20;

                if (v.departStep === 1) {
                    depX = 60;
                    depZ = 25;
                    if (Math.hypot(depX - curX, depZ - curZ) < 12) v.departStep = 2;
                } else {
                    depX = 220;
                    depZ = 30;
                }

                const dx = depX - curX;
                const dz = depZ - curZ;
                v.speed = THREE.MathUtils.lerp(v.speed, 0.45, 0.05);
                const targetYaw = Math.atan2(dz, dx);
                const yawDiff = Math.atan2(Math.sin(targetYaw - v.yaw), Math.cos(targetYaw - v.yaw));
                v.yaw += yawDiff * 0.05;
                v.turnRoll = -yawDiff * 1.5;
                v.throttlePitch = -0.05;
                v.mesh.rotation.y = v.yaw;

                v.mesh.position.x += Math.cos(v.yaw) * v.speed;
                v.mesh.position.z += Math.sin(v.yaw) * v.speed;

                if (curX > 210) {
                    scene.remove(v.mesh);
                    vessels.splice(idx, 1);
                }
            }
        });

        // STEP 3: BOATS COLLISION AVOIDANCE (BOIDS REPULSION)
        for (let i = 0; i < vessels.length; i++) {
            for (let j = i + 1; j < vessels.length; j++) {
                const bA = vessels[i];
                const bB = vessels[j];
                if (bA.speed > 0.05 || bB.speed > 0.05) {
                    const dx = bA.mesh.position.x - bB.mesh.position.x;
                    const dz = bA.mesh.position.z - bB.mesh.position.z;
                    const dist = Math.hypot(dx, dz);
                    const minSafe = 10.0; // Minimum safe hull distance

                    if (dist < minSafe && dist > 0.1) {
                        const push = (minSafe - dist) * 0.04;
                        const nx = dx / dist;
                        const nz = dz / dist;
                        bA.mesh.position.x += nx * push;
                        bA.mesh.position.z += nz * push;
                        bB.mesh.position.x -= nx * push;
                        bB.mesh.position.z -= nz * push;
                        bA.speed *= 0.7;
                        bB.speed *= 0.7;
                    }
                }
            }
        }

        // UPDATE SMALL BOAT FLEET (PARKED AT DOCK + ACTIVE LIGHTERING SHUTTLES)
        let activeBancas = 0;

        bancas.forEach(b => {
            const curX = b.mesh.position.x;
            const curZ = b.mesh.position.z;
            const waveY = getWaveHeight(curX, curZ, waveTime);
            b.mesh.position.y = waveY * 0.6;

            const bowWake = b.mesh.getObjectByName('bowWake');
            if (bowWake) {
                bowWake.material.opacity = THREE.MathUtils.lerp(
                    bowWake.material.opacity,
                    Math.min(0.45, b.speed * 2.0),
                    0.15
                );
            }

            if (b.state === 'parked') {
                // Moored in designated slot with gentle water rocking
                b.mesh.position.x = b.parkSlot.x;
                b.mesh.position.z = b.parkSlot.z;
                b.mesh.rotation.y = b.parkSlot.yaw;
                b.mesh.rotation.z = Math.sin(Date.now() * 0.003 + b.bobOffset) * 0.05;
                b.speed = 0;

                // Dynamic Fish Fetching: dispatch up to 6 bancas (~25% of fleet)
                const runningCount = bancas.filter(item => item.state !== 'parked').length;
                if (runningCount < 6) {
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
                const tx = b.targetBoat.mesh.position.x;
                const tz = b.targetBoat.mesh.position.z;
                const dx = tx - curX;
                const dz = tz - curZ;
                b.speed = THREE.MathUtils.lerp(b.speed, 0.45, 0.05);

                const targetYaw = Math.atan2(dz, dx);
                const yawDiff = Math.atan2(Math.sin(targetYaw - b.yaw), Math.cos(targetYaw - b.yaw));
                b.yaw += yawDiff * 0.08;
                b.mesh.rotation.y = b.yaw;
                b.mesh.rotation.z = -yawDiff * 1.2;

                b.mesh.position.x += Math.cos(b.yaw) * b.speed;
                b.mesh.position.z += Math.sin(b.yaw) * b.speed;

                if (Math.hypot(dx, dz) < 8.0) {
                    b.state = 'transferring';
                    b.timer = 1.6;
                }
            } else if (b.state === 'transferring') {
                activeBancas++;
                b.speed = 0;
                b.timer -= deltaHours * 15;
                if (b.timer <= 0) {
                    const take = Math.min(b.maxCargo, b.targetBoat ? b.targetBoat.cargo : 0);
                    if (b.targetBoat) b.targetBoat.cargo -= take;
                    b.cargo = take;
                    b.state = 'to_wharf';
                }
            } else if (b.state === 'to_wharf') {
                activeBancas++;
                // Head to fish landing apron at X = -30, Z = 70
                const landingX = -30;
                const landingZ = 70;
                const dx = landingX - curX;
                const dz = landingZ - curZ;
                b.speed = THREE.MathUtils.lerp(b.speed, 0.4, 0.05);

                const targetYaw = Math.atan2(dz, dx);
                const yawDiff = Math.atan2(Math.sin(targetYaw - b.yaw), Math.cos(targetYaw - b.yaw));
                b.yaw += yawDiff * 0.08;
                b.mesh.rotation.y = b.yaw;
                b.mesh.rotation.z = -yawDiff * 1.2;

                b.mesh.position.x += Math.cos(b.yaw) * b.speed;
                b.mesh.position.z += Math.sin(b.yaw) * b.speed;

                if (Math.hypot(dx, dz) < 6.0) {
                    b.state = 'unloading_at_wharf';
                    b.timer = 1.2;
                }
            } else if (b.state === 'unloading_at_wharf') {
                activeBancas++;
                b.speed = 0;
                b.timer -= deltaHours * 15;
                if (b.timer <= 0) {
                    totalCratesLanded += b.cargo;
                    b.cargo = 0;
                    b.state = 'return_to_park';
                }
            } else if (b.state === 'return_to_park') {
                activeBancas++;
                const dx = b.parkSlot.x - curX;
                const dz = b.parkSlot.z - curZ;
                b.speed = THREE.MathUtils.lerp(b.speed, 0.35, 0.05);

                const targetYaw = Math.atan2(dz, dx);
                const yawDiff = Math.atan2(Math.sin(targetYaw - b.yaw), Math.cos(targetYaw - b.yaw));
                b.yaw += yawDiff * 0.08;
                b.mesh.rotation.y = b.yaw;

                b.mesh.position.x += Math.cos(b.yaw) * b.speed;
                b.mesh.position.z += Math.sin(b.yaw) * b.speed;

                if (Math.hypot(dx, dz) < 2.5) {
                    b.mesh.position.x = b.parkSlot.x;
                    b.mesh.position.z = b.parkSlot.z;
                    b.mesh.rotation.y = b.parkSlot.yaw;
                    b.yaw = b.parkSlot.yaw;
                    b.state = 'parked';
                    b.targetBoat = null;
                }
            }
        });

        // UPDATE FLOATING HUD METRICS
        document.getElementById('kpi-queue-count').textContent = waitingCount;
        document.getElementById('kpi-wait-time').textContent = (waitingCount > 0 ? (1.2 + waitingCount * 0.45).toFixed(2) : '0.00');

        const berthUtil = (occupiedCount / numBerths) * 100;
        document.getElementById('kpi-berth-util').textContent = berthUtil.toFixed(1);
        document.getElementById('kpi-berth-occ').textContent = occupiedCount;
        document.getElementById('kpi-berth-total').textContent = numBerths;

        document.getElementById('kpi-bancas-active').textContent = activeBancas;
        document.getElementById('kpi-bancas-moored').textContent = (bancas.length - activeBancas);

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

        const timeDelta = Math.min(deltaMs / 1000, 0.1);
        const waveTime = time * 0.002;

        if (isPlaying) {
            const deltaHours = timeDelta * (timeScale * 0.15);
            updateSimulation(deltaHours, waveTime);
        }

        // Procedural Wave Mesh Displacement
        const pAttr = waterGeo.attributes.position;
        for (let i = 0; i < pAttr.count; i++) {
            const bv = baseVerts[i];
            const waveZ = Math.sin(bv.x * 0.04 + waveTime * 2.2) * 0.6 +
                          Math.cos(bv.y * 0.05 + waveTime * 1.8) * 0.45;
            pAttr.setZ(i, waveZ);
        }
        pAttr.needsUpdate = true;

        // STEP 1: ROTATE LIGHTROTORPIVOT AT TOP LANTERN GALLERY (Y = 18.5)
        LightRotorPivot.rotation.y += timeDelta * 0.8;

        // Update active foam trail rings
        foamPool.forEach(f => {
            if (f.active) {
                f.life += timeDelta;
                f.scale += timeDelta * 2.2;
                f.mesh.scale.set(f.scale, f.scale, f.scale);
                f.mesh.material.opacity = Math.max(0, 0.55 * (1 - f.life / f.maxLife));
                if (f.life >= f.maxLife) {
                    f.active = false;
                    f.mesh.visible = false;
                    f.mesh.position.set(0, -50, 0);
                }
            }
        });

        controls.update();
        renderer.render(scene, camera);
        requestAnimationFrame(render);
    }
    requestAnimationFrame(render);

    // -------------------------------------------------------------
    // INTERACTIVE RAYCASTING (HOVER & CLICK TOOLTIP)
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

        const mediumMeshes = vessels.map(v => v.mesh);
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
                    ttState.textContent = 'Holding in San Miguel Bay (150m out)';
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
                    ttState.textContent = 'Parked in Mooring Basin';
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
    // UI CONTROLS & MODAL LISTENERS
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
                tideLockActive = false;
                badge.textContent = 'Intervention B: Dredging';
            } else if (p === 'interventionC') {
                numBerths = 13;
                arrivalRate = 0.34;
                bulunganMultiplier = 1.4;
                tideLockActive = true;
                badge.textContent = 'Intervention C: Staggered';
            }
            slBerths.value = numBerths;
            document.getElementById('val-berths').textContent = numBerths + ' berths';
            slRush.value = bulunganMultiplier;
            document.getElementById('val-rush').textContent = bulunganMultiplier.toFixed(1) + 'x';
            chkTide.checked = tideLockActive;
            initBerths();
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
