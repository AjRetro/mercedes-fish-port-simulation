# src/port_canvas.py
"""
Interactive Digital Twin Port Canvas for Mercedes Fish Port Simulation.
Engineered for University of Camarines Norte (UCN) discrete-event logistics presentation.

Features:
- Pure HTML5 / Canvas2D 60fps simulation engine (zero external CDN dependencies).
- Multi-tier spatial geometry: Outer Roadstead (Anchorage) -> Estuarine Channel -> Wharf Berths -> Bulungan Auction Pavilion.
- Authentic Philippine maritime craft: Mother Vessels (Basnig / Purse Seiners) and Shuttle Bancas with dual bamboo outriggers (katig).
- Real-time diurnal ambient engine: Dynamic day/night cycle with rotating lighthouse beam, sunrise glow, and 6:00 AM Bulungan wholesale auction rush.
- Interactive HUD: Play/Pause, speed multipliers (1x, 2x, 5x, 10x), 24h scrubber, and instant jump presets.
"""

def generate_digital_twin_html(num_berths: int = 3, num_bancas: int = 10, channel_capacity: int = 3, base_arrival_rate: float = 0.34) -> str:
    """Generates the self-contained HTML/JS/CSS string for the Streamlit iframe."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        user-select: none;
    }}
    body {{
        background: #080C14;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #F8FAFC;
        overflow: hidden;
        padding: 10px;
    }}
    .twin-card {{
        background: #0B132B;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        max-width: 100%;
        margin: 0 auto;
    }}
    /* Top HUD Header */
    .hud-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 16px;
        background: rgba(15, 23, 42, 0.95);
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}
    .hud-clock-group {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .hud-clock {{
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: 0.05em;
        color: #38BDF8;
        font-variant-numeric: tabular-nums;
    }}
    .hud-status-badge {{
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 3px 10px;
        border-radius: 9999px;
        background: rgba(56, 189, 248, 0.15);
        color: #38BDF8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        transition: all 0.3s ease;
    }}
    .hud-status-badge.rush {{
        background: rgba(245, 158, 11, 0.25);
        color: #FBBF24;
        border-color: #F59E0B;
        animation: pulse-glow 1.5s infinite alternate;
    }}
    @keyframes pulse-glow {{
        0% {{ box-shadow: 0 0 4px rgba(245, 158, 11, 0.3); }}
        100% {{ box-shadow: 0 0 14px rgba(245, 158, 11, 0.8); }}
    }}
    .hud-telemetry {{
        display: flex;
        align-items: center;
        gap: 16px;
        font-size: 0.8rem;
    }}
    .hud-stat {{
        display: flex;
        flex-direction: column;
        align-items: flex-end;
    }}
    .hud-stat-val {{
        font-weight: 700;
        color: #F8FAFC;
        font-variant-numeric: tabular-nums;
    }}
    .hud-stat-lbl {{
        font-size: 0.68rem;
        color: #94A3B8;
        text-transform: uppercase;
    }}

    /* Canvas Container */
    .canvas-wrap {{
        position: relative;
        width: 100%;
        background: #040812;
    }}
    canvas {{
        display: block;
        width: 100%;
        height: auto;
    }}

    /* Bottom Control Bar */
    .hud-footer {{
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        padding: 10px 16px;
        background: rgba(15, 23, 42, 0.95);
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        gap: 10px;
    }}
    .btn-group {{
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .hud-btn {{
        background: #1E293B;
        border: 1px solid rgba(255, 255, 255, 0.15);
        color: #F8FAFC;
        padding: 6px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.15s ease;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}
    .hud-btn:hover {{
        background: #334155;
        border-color: #38BDF8;
        color: #38BDF8;
    }}
    .hud-btn.active {{
        background: rgba(56, 189, 248, 0.2);
        border-color: #38BDF8;
        color: #38BDF8;
    }}
    .hud-btn.primary {{
        background: #0284C7;
        border-color: #38BDF8;
        color: #FFFFFF;
    }}
    .hud-btn.primary:hover {{
        background: #0369A1;
    }}
    .hud-btn.rush-btn {{
        background: rgba(245, 158, 11, 0.15);
        border-color: #F59E0B;
        color: #FBBF24;
    }}
    .hud-btn.rush-btn:hover {{
        background: rgba(245, 158, 11, 0.3);
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.4);
    }}
    .slider-wrap {{
        flex: 1;
        min-width: 180px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .slider-wrap input[type=range] {{
        flex: 1;
        accent-color: #38BDF8;
        cursor: pointer;
    }}
    .legend-bar {{
        display: flex;
        align-items: center;
        gap: 14px;
        font-size: 0.72rem;
        color: #94A3B8;
        padding: 4px 16px 8px 16px;
        background: rgba(15, 23, 42, 0.95);
        border-top: 1px solid rgba(255, 255, 255, 0.04);
    }}
    .legend-item {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }}
    .legend-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
    }}
</style>
</head>
<body>

<div class="twin-card">
    <!-- Top HUD Header -->
    <div class="hud-header">
        <div class="hud-clock-group">
            <div id="sim-clock" class="hud-clock">06:00 AM</div>
            <div id="status-pill" class="hud-status-badge rush">6:00 AM BULUNGAN RUSH</div>
        </div>
        <div class="hud-telemetry">
            <div class="hud-stat">
                <span id="stat-anchorage" class="hud-stat-val">3 craft</span>
                <span class="hud-stat-lbl">Roadstead Wait</span>
            </div>
            <div class="hud-stat">
                <span id="stat-channel" class="hud-stat-val">2 / {channel_capacity}</span>
                <span class="hud-stat-lbl">Channel Transits</span>
            </div>
            <div class="hud-stat">
                <span id="stat-bancas" class="hud-stat-val">6 / {num_bancas}</span>
                <span class="hud-stat-lbl">Bancas Active</span>
            </div>
            <div class="hud-stat">
                <span id="stat-berths" class="hud-stat-val">2 / {num_berths}</span>
                <span class="hud-stat-lbl">Wharf Slips</span>
            </div>
            <div class="hud-stat">
                <span id="stat-banyeras" class="hud-stat-val" style="color: #34D399;">1,240</span>
                <span class="hud-stat-lbl">Crates Landed</span>
            </div>
        </div>
    </div>

    <!-- Live Port Canvas -->
    <div class="canvas-wrap">
        <canvas id="port-canvas" width="980" height="460"></canvas>
    </div>

    <!-- Bottom Interactive Control Deck -->
    <div class="hud-footer">
        <div class="btn-group">
            <button id="btn-play" class="hud-btn primary">⏸ Pause</button>
            <button id="btn-reset" class="hud-btn">↺ Reset</button>
        </div>

        <div class="slider-wrap">
            <span style="font-size:0.75rem; color:#94A3B8;">00:00</span>
            <input type="range" id="time-slider" min="0" max="24" step="0.05" value="6.0">
            <span style="font-size:0.75rem; color:#94A3B8;">24:00</span>
        </div>

        <div class="btn-group">
            <button class="hud-btn speed-btn" data-speed="1">1x</button>
            <button class="hud-btn speed-btn active" data-speed="2">2x</button>
            <button class="hud-btn speed-btn" data-speed="5">5x</button>
            <button class="hud-btn speed-btn" data-speed="10">10x</button>
            <button id="btn-rush" class="hud-btn rush-btn">⚡ 6:00 AM Rush</button>
        </div>
    </div>

    <!-- Bottom Visual Legend -->
    <div class="legend-bar">
        <span style="font-weight:700; color:#F8FAFC;">TOPOLOGY LEGEND:</span>
        <div class="legend-item"><span class="legend-dot" style="background:#F59E0B;"></span> Mother Vessel (Basnig / Ring Netter)</div>
        <div class="legend-item"><span class="legend-dot" style="background:#38BDF8;"></span> Shuttle Banca (Katig Outrigger)</div>
        <div class="legend-item"><span class="legend-dot" style="background:#10B981;"></span> Direct Landing Craft</div>
        <div class="legend-item"><span class="legend-dot" style="background:#FBBF24;"></span> Wharf Slips 1–{num_berths}</div>
        <div class="legend-item"><span class="legend-dot" style="background:#A855F7;"></span> Bulungan Trading Floor</div>
    </div>
</div>

<script>
(function() {{
    const canvas = document.getElementById('port-canvas');
    const ctx = canvas.getContext('2d');
    const clockEl = document.getElementById('sim-clock');
    const statusPill = document.getElementById('status-pill');
    const timeSlider = document.getElementById('time-slider');
    const btnPlay = document.getElementById('btn-play');
    const btnReset = document.getElementById('btn-reset');
    const btnRush = document.getElementById('btn-rush');
    const speedButtons = document.querySelectorAll('.speed-btn');

    const statAnchorage = document.getElementById('stat-anchorage');
    const statChannel = document.getElementById('stat-channel');
    const statBancas = document.getElementById('stat-bancas');
    const statBerths = document.getElementById('stat-berths');
    const statBanyeras = document.getElementById('stat-banyeras');

    const NUM_BERTHS = {num_berths};
    const NUM_BANCAS = {num_bancas};
    const CHANNEL_CAP = {channel_capacity};
    const BASE_LAMBDA = {base_arrival_rate};

    let simTime = 6.0; // Starts right at 6:00 AM Bulungan Peak
    let isPlaying = true;
    let timeScale = 2.0; // hours per minute in real time
    let lastTimestamp = 0;
    let banyerasLanded = 1240;
    let lighthouseAngle = 0;

    // Simulation Spatial Geometry
    // Canvas: 980 x 460
    // Anchorage: x = 30 to 300, y = 80 to 420
    // Channel Corridor: x = 300 to 650, center path y = 250
    // Wharf Berths: x = 650 to 740, slips at y = 140, 200, 260, 320
    // Port Apron / Bulungan: x = 740 to 950, y = 110 to 360

    const BERTH_COORDS = [];
    const slipSpacing = Math.min(55, 240 / Math.max(1, NUM_BERTHS));
    const startY = 230 - ((NUM_BERTHS - 1) * slipSpacing) / 2;
    for (let i = 0; i < NUM_BERTHS; i++) {{
        BERTH_COORDS.push({{
            id: i + 1,
            x: 670,
            y: startY + i * slipSpacing,
            occupiedBy: null,
            progress: 0
        }});
    }}

    // Vessel Fleet State Collections
    let motherBoats = [
        {{ id: 'MV-SanMiguel', x: 120, y: 150, targetX: 120, targetY: 150, state: 'anchored', crates: 140, totalCrates: 150, waitTime: 1.4, assignedBancas: [] }},
        {{ id: 'MV-MercedesQueen', x: 200, y: 220, targetX: 200, targetY: 220, state: 'anchored', crates: 95, totalCrates: 120, waitTime: 2.1, assignedBancas: [] }},
        {{ id: 'MV-BicolExpress', x: 140, y: 310, targetX: 140, targetY: 310, state: 'anchored', crates: 160, totalCrates: 180, waitTime: 0.8, assignedBancas: [] }}
    ];

    let bancas = [];
    for (let i = 0; i < NUM_BANCAS; i++) {{
        bancas.push({{
            id: 'SB-' + (i + 1),
            x: 640 - (i % 5) * 20,
            y: 370 + Math.floor(i / 5) * 16,
            angle: 0,
            state: 'idle', // idle, to_mother, loading, to_wharf, unloading
            motherId: null,
            targetBerth: null,
            cargo: 0,
            progress: 0,
            speed: 1.2 + (i % 3) * 0.2
        }});
    }}

    // Particles (Wake trail & auction sparks)
    let wakeParticles = [];
    let auctionSparks = [];

    // Diurnal Arrival Rate Equation λ(t)
    function getArrivalRate(t) {{
        const dawnPeak = 1.15 * Math.exp(-Math.pow((t - 6.0), 2) / (2 * 1.44));
        const duskPeak = 0.65 * Math.exp(-Math.pow((t - 16.5), 2) / (2 * 2.25));
        return BASE_LAMBDA + dawnPeak + duskPeak;
    }}

    // Day/Night Ambient Light Gradient
    function getAmbientLighting(t) {{
        // Returns sky tint, ambient water tint, sun/dawn factor
        if (t >= 5.0 && t <= 7.2) {{
            // Dawn Bulungan Rush (Golden Sunrise)
            const f = (t - 5.0) / 2.2;
            return {{
                waterBase: '#0C2340',
                waterGlow: 'rgba(245, 158, 11, 0.22)',
                land: '#1E293B',
                bulunganGlow: 1.0,
                isNight: false,
                name: '6:00 AM BULUNGAN RUSH'
            }};
        }} else if (t > 7.2 && t < 16.0) {{
            // Daytime Operations
            return {{
                waterBase: '#0D294D',
                waterGlow: 'rgba(56, 189, 248, 0.12)',
                land: '#1E293B',
                bulunganGlow: 0.3,
                isNight: false,
                name: 'NORMAL DAY OPERATIONS'
            }};
        }} else if (t >= 16.0 && t <= 18.5) {{
            // Afternoon Peak / Sunset
            return {{
                waterBase: '#17223B',
                waterGlow: 'rgba(217, 119, 6, 0.25)',
                land: '#1A233A',
                bulunganGlow: 0.6,
                isNight: false,
                name: 'AFTERNOON ARTISANAL PEAK'
            }};
        }} else {{
            // Deep Night
            return {{
                waterBase: '#060E1A',
                waterGlow: 'rgba(30, 58, 138, 0.15)',
                land: '#0F172A',
                bulunganGlow: 0.1,
                isNight: true,
                name: 'NIGHT ROADSTEAD WATCH'
            }};
        }}
    }}

    function formatTime(decimalHours) {{
        let h = Math.floor(decimalHours);
        let m = Math.floor((decimalHours - h) * 60);
        let ampm = h >= 12 ? 'PM' : 'AM';
        let displayH = h % 12;
        if (displayH === 0) displayH = 12;
        return (displayH < 10 ? '0' : '') + displayH + ':' + (m < 10 ? '0' : '') + m + ' ' + ampm;
    }}

    // Spawn Mother Boats during peak hours
    let arrivalAccumulator = 0;
    function updateTrafficSimulation(dtHours) {{
        arrivalAccumulator += getArrivalRate(simTime) * dtHours;
        if (arrivalAccumulator >= 1.0 && motherBoats.length < 8) {{
            arrivalAccumulator = 0;
            const names = ['MV-DaetStar', 'MV-MercedesPride', 'MV-SanMiguel2', 'MV-BicolIsle', 'MV-PacificCatch'];
            const rName = names[Math.floor(Math.random() * names.length)] + '-' + Math.floor(Math.random() * 90 + 10);
            motherBoats.push({{
                id: rName,
                x: 40,
                y: 100 + Math.random() * 260,
                targetX: 80 + Math.random() * 180,
                targetY: 100 + Math.random() * 260,
                state: 'anchored',
                crates: Math.floor(100 + Math.random() * 80),
                totalCrates: 160,
                waitTime: 0,
                assignedBancas: []
            }});
        }}

        // Update Mother Boats
        for (let i = motherBoats.length - 1; i >= 0; i--) {{
            const b = motherBoats[i];
            b.waitTime += dtHours;
            // Smooth float to target anchorage
            b.x += (b.targetX - b.x) * 0.05;
            b.y += (b.targetY - b.y) * 0.05;

            // When cleared of crates, depart
            if (b.crates <= 0) {{
                b.targetX = -60;
                if (b.x < -40) {{
                    motherBoats.splice(i, 1);
                }}
            }}
        }}

        // Dispatch Bancas to Mother Boats with crates
        bancas.forEach((banca, idx) => {{
            if (banca.state === 'idle') {{
                // Find anchored mother boat that needs lightering
                const targetMB = motherBoats.find(mb => mb.crates > 0 && mb.assignedBancas.length < 2 && mb.x > 70);
                if (targetMB) {{
                    banca.state = 'to_mother';
                    banca.motherId = targetMB.id;
                    targetMB.assignedBancas.push(banca.id);
                }}
            }} else if (banca.state === 'to_mother') {{
                const targetMB = motherBoats.find(mb => mb.id === banca.motherId);
                if (!targetMB) {{
                    banca.state = 'idle';
                    return;
                }}
                const dx = (targetMB.x + 25) - banca.x;
                const dy = (targetMB.y + 10) - banca.y;
                const dist = Math.hypot(dx, dy);
                banca.angle = Math.atan2(dy, dx);
                if (dist > 8) {{
                    banca.x += (dx / dist) * banca.speed * 2.2;
                    banca.y += (dy / dist) * banca.speed * 2.2;
                    addWake(banca.x, banca.y);
                }} else {{
                    banca.state = 'loading';
                    banca.progress = 0;
                }}
            }} else if (banca.state === 'loading') {{
                banca.progress += dtHours * 15;
                if (banca.progress >= 1.0) {{
                    const targetMB = motherBoats.find(mb => mb.id === banca.motherId);
                    const loadAmount = Math.min(20, targetMB ? targetMB.crates : 20);
                    if (targetMB) targetMB.crates -= loadAmount;
                    banca.cargo = loadAmount;
                    banca.state = 'to_wharf';

                    // Reserve a berth slip
                    const freeBerth = BERTH_COORDS.find(slip => slip.occupiedBy === null);
                    if (freeBerth) {{
                        freeBerth.occupiedBy = banca.id;
                        banca.targetBerth = freeBerth;
                    }}
                }}
            }} else if (banca.state === 'to_wharf') {{
                // Navigate into channel then berth
                const destX = banca.targetBerth ? banca.targetBerth.x : 670;
                const destY = banca.targetBerth ? banca.targetBerth.y : 230;
                const dx = destX - banca.x;
                const dy = destY - banca.y;
                const dist = Math.hypot(dx, dy);
                banca.angle = Math.atan2(dy, dx);
                if (dist > 8) {{
                    banca.x += (dx / dist) * banca.speed * 2.0;
                    banca.y += (dy / dist) * banca.speed * 2.0;
                    addWake(banca.x, banca.y);
                }} else {{
                    banca.state = 'unloading';
                    banca.progress = 0;
                }}
            }} else if (banca.state === 'unloading') {{
                banca.progress += dtHours * 20;
                if (banca.progress >= 1.0) {{
                    banyerasLanded += banca.cargo;
                    banca.cargo = 0;
                    if (banca.targetBerth) {{
                        banca.targetBerth.occupiedBy = null;
                        banca.targetBerth = null;
                    }}
                    // Create auction floor particles
                    addAuctionBurst(770 + Math.random() * 120, 160 + Math.random() * 140);
                    banca.state = 'idle';
                    banca.x = 640 - (idx % 4) * 20;
                    banca.y = 380 + Math.floor(idx / 4) * 16;
                }}
            }}
        }});

        // Channel density check: count bancas with x between 300 and 640
        const inChannel = bancas.filter(b => b.x >= 300 && b.x <= 640).length;
        const occupiedBerths = BERTH_COORDS.filter(s => s.occupiedBy !== null).length;
        const activeBancas = bancas.filter(b => b.state !== 'idle').length;

        // Telemetry update
        statAnchorage.textContent = motherBoats.length + ' craft';
        statChannel.textContent = inChannel + ' / ' + CHANNEL_CAP;
        statBancas.textContent = activeBancas + ' / ' + NUM_BANCAS;
        statBerths.textContent = occupiedBerths + ' / ' + NUM_BERTHS;
        statBanyeras.textContent = banyerasLanded.toLocaleString();
    }}

    function addWake(x, y) {{
        if (wakeParticles.length < 90 && Math.random() > 0.4) {{
            wakeParticles.push({{ x, y, radius: 2.5, alpha: 0.6 }});
        }}
    }}

    function addAuctionBurst(x, y) {{
        for (let i = 0; i < 4; i++) {{
            auctionSparks.push({{
                x, y,
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                alpha: 1.0,
                color: Math.random() > 0.5 ? '#FBBF24' : '#34D399'
            }});
        }}
    }}

    // ==========================================
    // CANVAS RENDERING ENGINE
    // ==========================================
    function drawPortScene() {{
        const amb = getAmbientLighting(simTime);

        // 1. Water Background (San Miguel Bay & Mercedes Estuary)
        ctx.fillStyle = amb.waterBase;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Animated subtle water waves
        ctx.strokeStyle = amb.waterGlow;
        ctx.lineWidth = 1;
        const waveTime = Date.now() * 0.0015;
        for (let i = 0; i < 6; i++) {{
            ctx.beginPath();
            const yOffset = 70 + i * 65;
            ctx.moveTo(0, yOffset + Math.sin(waveTime + i) * 6);
            for (let x = 0; x < 660; x += 40) {{
                ctx.quadraticCurveTo(x + 20, yOffset + Math.sin(waveTime + x * 0.02) * 8, x + 40, yOffset + Math.cos(waveTime + x * 0.01) * 6);
            }}
            ctx.stroke();
        }}

        // 2. Sandbars & Estuarine Shoreline
        // Upper Shoreline (North sandbar)
        ctx.fillStyle = amb.land;
        ctx.beginPath();
        ctx.moveTo(310, 0);
        ctx.bezierCurveTo(360, 90, 480, 110, 650, 110);
        ctx.lineTo(980, 110);
        ctx.lineTo(980, 0);
        ctx.closePath();
        ctx.fill();
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
        ctx.stroke();

        // Lower Shoreline (South bank)
        ctx.beginPath();
        ctx.moveTo(340, 460);
        ctx.bezierCurveTo(420, 390, 520, 370, 650, 370);
        ctx.lineTo(980, 370);
        ctx.lineTo(980, 460);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();

        // 3. Channel Navigational Buoys (Red port, Green starboard)
        const buoyPulse = (Math.sin(Date.now() * 0.005) + 1) * 0.5;
        // Starboard Green Buoy
        ctx.fillStyle = '#10B981';
        ctx.beginPath(); ctx.arc(380, 145, 4, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = 'rgba(16, 185, 129, ' + (0.3 + buoyPulse * 0.5) + ')';
        ctx.beginPath(); ctx.arc(380, 145, 9, 0, Math.PI * 2); ctx.fill();

        // Port Red Buoy
        ctx.fillStyle = '#EF4444';
        ctx.beginPath(); ctx.arc(380, 335, 4, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = 'rgba(239, 68, 68, ' + (0.3 + buoyPulse * 0.5) + ')';
        ctx.beginPath(); ctx.arc(380, 335, 9, 0, Math.PI * 2); ctx.fill();

        // Channel Centerline Indicator
        ctx.setLineDash([6, 8]);
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.2)';
        ctx.beginPath();
        ctx.moveTo(320, 240);
        ctx.bezierCurveTo(450, 240, 560, 240, 650, 240);
        ctx.stroke();
        ctx.setLineDash([]);

        // 4. Physical Wharf Concrete Piers & Slips
        ctx.fillStyle = '#334155';
        ctx.fillRect(650, 110, 90, 260);

        // Hazard stripes on wharf apron edge
        ctx.fillStyle = '#FBBF24';
        for (let y = 115; y < 365; y += 18) {{
            ctx.fillRect(650, y, 4, 9);
        }}

        // Berth Slips
        BERTH_COORDS.forEach(slip => {{
            ctx.strokeStyle = slip.occupiedBy ? '#EF4444' : '#10B981';
            ctx.lineWidth = 2;
            ctx.strokeRect(slip.x - 12, slip.y - 14, 28, 28);
            ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
            ctx.font = '9px monospace';
            ctx.fillText('B' + slip.id, slip.x - 8, slip.y + 3);
        }});

        // 5. Bulungan Wholesale Fish Auction Hall
        const bGlow = amb.bulunganGlow;
        ctx.fillStyle = '#1E293B';
        ctx.fillRect(750, 130, 200, 220);
        ctx.strokeStyle = bGlow > 0.5 ? '#F59E0B' : 'rgba(255, 255, 255, 0.15)';
        ctx.lineWidth = bGlow > 0.5 ? 2 : 1;
        ctx.strokeRect(750, 130, 200, 220);

        // Bulungan Roof / Interior Glow
        ctx.fillStyle = 'rgba(245, 158, 11, ' + (0.1 + bGlow * 0.35) + ')';
        ctx.fillRect(755, 135, 190, 210);

        // Bulungan Signage
        ctx.fillStyle = bGlow > 0.5 ? '#FBBF24' : '#F8FAFC';
        ctx.font = 'bold 11px -apple-system, sans-serif';
        ctx.fillText('MERCEDES BULUNGAN', 775, 152);
        ctx.font = '9px sans-serif';
        ctx.fillStyle = '#94A3B8';
        ctx.fillText('Wholesale Auction Pavilion', 775, 166);

        // Animated Trading Activity Crowd inside Bulungan
        const crowdCount = Math.floor(10 + bGlow * 18);
        for (let i = 0; i < crowdCount; i++) {{
            const cx = 765 + (i * 17) % 170;
            const cy = 185 + Math.floor((i * 17) / 170) * 22;
            ctx.fillStyle = i % 2 === 0 ? '#38BDF8' : '#FBBF24';
            ctx.beginPath();
            ctx.arc(cx, cy, 2.5, 0, Math.PI * 2);
            ctx.fill();
        }}

        // Auction fish crates stacked
        for (let row = 0; row < 5; row++) {{
            for (let col = 0; col < 6; col++) {{
                ctx.fillStyle = '#D97706';
                ctx.fillRect(770 + col * 10, 280 + row * 10, 8, 8);
            }}
        }}
        ctx.fillStyle = '#34D399';
        ctx.font = '9px sans-serif';
        ctx.fillText('Prime Banyeras: ' + (banyerasLanded % 400 + 120), 770, 342);

        // 6. Draw Rotating Lighthouse Beam (Harbor entrance on north sandbar)
        const lx = 480, ly = 95;
        ctx.fillStyle = '#F8FAFC';
        ctx.beginPath(); ctx.arc(lx, ly, 6, 0, Math.PI * 2); ctx.fill();
        if (amb.isNight || bGlow > 0.4) {{
            lighthouseAngle += 0.025;
            const beamLength = 220;
            ctx.save();
            ctx.translate(lx, ly);
            ctx.rotate(lighthouseAngle);
            const beamGrad = ctx.createRadialGradient(0, 0, 5, 0, 0, beamLength);
            beamGrad.addColorStop(0, 'rgba(255, 255, 255, 0.5)');
            beamGrad.addColorStop(0.3, 'rgba(56, 189, 248, 0.2)');
            beamGrad.addColorStop(1, 'rgba(56, 189, 248, 0)');
            ctx.fillStyle = beamGrad;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.arc(0, 0, beamLength, -0.22, 0.22);
            ctx.closePath();
            ctx.fill();
            ctx.restore();
        }}

        // 7. Draw Wake Particles
        for (let i = wakeParticles.length - 1; i >= 0; i--) {{
            const p = wakeParticles[i];
            ctx.fillStyle = 'rgba(255, 255, 255, ' + p.alpha + ')';
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();
            p.radius += 0.15;
            p.alpha -= 0.025;
            if (p.alpha <= 0) wakeParticles.splice(i, 1);
        }}

        // 8. Draw Auction Sparks
        for (let i = auctionSparks.length - 1; i >= 0; i--) {{
            const sp = auctionSparks[i];
            ctx.fillStyle = sp.color;
            ctx.beginPath(); ctx.arc(sp.x, sp.y, 2, 0, Math.PI * 2); ctx.fill();
            sp.x += sp.vx; sp.y += sp.vy;
            sp.alpha -= 0.03;
            if (sp.alpha <= 0) auctionSparks.splice(i, 1);
        }}

        // 9. Draw Mother Vessels in Roadstead
        motherBoats.forEach(mb => {{
            ctx.save();
            ctx.translate(mb.x, mb.y);

            // Vessel Hull (Commercial Basnig / Ring Netter)
            ctx.fillStyle = '#1E293B';
            ctx.beginPath();
            ctx.moveTo(-22, -9);
            ctx.lineTo(14, -9);
            ctx.quadraticCurveTo(26, 0, 14, 9);
            ctx.lineTo(-22, 9);
            ctx.closePath();
            ctx.fill();
            ctx.strokeStyle = '#F59E0B';
            ctx.lineWidth = 1.5;
            ctx.stroke();

            // Cabin
            ctx.fillStyle = '#475569';
            ctx.fillRect(-12, -6, 14, 12);

            // Rigging Outrigger Boom (Basnig fishing light boom)
            ctx.strokeStyle = '#94A3B8';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(-4, -18); ctx.lineTo(-4, 18);
            ctx.stroke();

            // Navigation Light
            ctx.fillStyle = '#38BDF8';
            ctx.beginPath(); ctx.arc(16, 0, 2, 0, Math.PI * 2); ctx.fill();

            // Cargo Hold Level
            ctx.fillStyle = '#34D399';
            const pct = Math.max(0, mb.crates / mb.totalCrates);
            ctx.fillRect(-20, -3, 6, 6 * pct);

            // Text Label
            ctx.fillStyle = '#F8FAFC';
            ctx.font = 'bold 9px -apple-system, sans-serif';
            ctx.fillText(mb.id, -20, -13);
            ctx.font = '8px monospace';
            ctx.fillStyle = '#FBBF24';
            ctx.fillText(mb.crates + ' banyeras', -20, 21);

            ctx.restore();
        }});

        // 10. Draw Shuttle Bancas (Motorized Katig Outriggers)
        bancas.forEach(b => {{
            ctx.save();
            ctx.translate(b.x, b.y);
            ctx.rotate(b.angle);

            // Central Narrow Hull
            ctx.fillStyle = '#0284C7';
            ctx.beginPath();
            ctx.moveTo(-8, -2.5);
            ctx.lineTo(8, -2.5);
            ctx.quadraticCurveTo(12, 0, 8, 2.5);
            ctx.lineTo(-8, 2.5);
            ctx.closePath();
            ctx.fill();

            // Lateral Bamboo Outriggers (Katig)
            ctx.strokeStyle = '#E2E8F0';
            ctx.lineWidth = 1.2;
            // Floats
            ctx.beginPath();
            ctx.moveTo(-7, -8); ctx.lineTo(7, -8);
            ctx.moveTo(-7, 8); ctx.lineTo(7, 8);
            ctx.stroke();
            // Connecting Struts (Tadlang)
            ctx.lineWidth = 0.8;
            ctx.beginPath();
            ctx.moveTo(-2, -8); ctx.lineTo(-2, 8);
            ctx.moveTo(3, -8); ctx.lineTo(3, 8);
            ctx.stroke();

            // Cargo Crates Indicator on board
            if (b.cargo > 0) {{
                ctx.fillStyle = '#FBBF24';
                ctx.fillRect(-3, -2, 6, 4);
            }}

            ctx.restore();
        }});

        // 11. Zone Boundary Watermarks & Labels
        ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
        ctx.font = 'bold 10px sans-serif';
        ctx.fillText('OUTER ROADSTEAD (ANCHORAGE)', 25, 28);
        ctx.fillText('ESTUARINE CHANNEL CORRIDOR', 340, 28);
        ctx.fillText('WHARF BERTHS & BULUNGAN', 670, 28);
    }}

    // ==========================================
    // MAIN ANIMATION LOOP
    // ==========================================
    function animate(timestamp) {{
        if (!lastTimestamp) lastTimestamp = timestamp;
        const deltaMs = timestamp - lastTimestamp;
        lastTimestamp = timestamp;

        if (isPlaying) {{
            // Real-time time progression: 1 second = (timeScale / 60) hours
            const dtHours = (deltaMs / 1000) * (timeScale / 40);
            simTime = (simTime + dtHours) % 24.0;
            timeSlider.value = simTime;
            clockEl.textContent = formatTime(simTime);

            // Status Badge update
            if (simTime >= 5.0 && simTime <= 7.2) {{
                statusPill.textContent = '6:00 AM BULUNGAN RUSH';
                statusPill.className = 'hud-status-badge rush';
            }} else if (simTime >= 16.0 && simTime <= 18.5) {{
                statusPill.textContent = '16:30 ARTISANAL RETURN';
                statusPill.className = 'hud-status-badge rush';
            }} else if (simTime > 7.2 && simTime < 16.0) {{
                statusPill.textContent = 'STEADY DAYTIME DISCHARGE';
                statusPill.className = 'hud-status-badge';
            }} else {{
                statusPill.textContent = 'NIGHT HARBOR ANCHORAGE';
                statusPill.className = 'hud-status-badge';
            }}

            updateTrafficSimulation(dtHours);
        }}

        drawPortScene();
        requestAnimationFrame(animate);
    }}

    // ==========================================
    // INTERACTIVE CONTROLS
    // ==========================================
    btnPlay.addEventListener('click', () => {{
        isPlaying = !isPlaying;
        btnPlay.textContent = isPlaying ? '⏸ Pause' : '▶ Play';
        btnPlay.className = isPlaying ? 'hud-btn primary' : 'hud-btn';
    }});

    timeSlider.addEventListener('input', (e) => {{
        simTime = parseFloat(e.target.value);
        clockEl.textContent = formatTime(simTime);
    }});

    btnRush.addEventListener('click', () => {{
        simTime = 5.95;
        timeSlider.value = 5.95;
        clockEl.textContent = formatTime(5.95);
        if (!isPlaying) {{
            isPlaying = true;
            btnPlay.textContent = '⏸ Pause';
            btnPlay.className = 'hud-btn primary';
        }}
    }});

    btnReset.addEventListener('click', () => {{
        simTime = 6.0;
        timeSlider.value = 6.0;
        banyerasLanded = 1240;
        motherBoats = [
            {{ id: 'MV-SanMiguel', x: 120, y: 150, targetX: 120, targetY: 150, state: 'anchored', crates: 140, totalCrates: 150, waitTime: 1.4, assignedBancas: [] }},
            {{ id: 'MV-MercedesQueen', x: 200, y: 220, targetX: 200, targetY: 220, state: 'anchored', crates: 95, totalCrates: 120, waitTime: 2.1, assignedBancas: [] }},
            {{ id: 'MV-BicolExpress', x: 140, y: 310, targetX: 140, targetY: 310, state: 'anchored', crates: 160, totalCrates: 180, waitTime: 0.8, assignedBancas: [] }}
        ];
        bancas.forEach((b, i) => {{
            b.state = 'idle';
            b.cargo = 0;
            b.x = 640 - (i % 5) * 20;
            b.y = 370 + Math.floor(i / 5) * 16;
        }});
        BERTH_COORDS.forEach(s => s.occupiedBy = null);
    }});

    speedButtons.forEach(btn => {{
        btn.addEventListener('click', () => {{
            speedButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            timeScale = parseFloat(btn.dataset.speed) * 2.0;
        }});
    }});

    // Kick off animation
    requestAnimationFrame(animate);
}})();
</script>

</body>
</html>
"""
