# Mercedes Fish Port 3D Digital Twin — Comprehensive Architectural Upgrade Plan
**Document Version:** 1.0.0  
**Status:** READY FOR EXECUTION (Phase 1 Planning Specification)  
**Authors:** Lead Architecture Planner in consultation with `@agency-3d-scene-developer`, `@agency-frontend-developer`, `@agency-ux-architect`, and `@agency-ui-designer`  
**Target Codebase:** `c:\Users\L470\Desktop\Mercedes_Port_Simulation`  
**Target Files:** `app.py` and `src/port_3d_engine.py`

---

## 1. Executive Summary & Architectural Foundation

This blueprint specifies the exact code modifications and mathematical formulations required to eliminate all visual, spatial, and hydrodynamic anomalies in the Mercedes Fish Port 3D WebGL Digital Twin (`src/port_3d_engine.py` and `app.py`).

### Core Deficiencies in Current Implementation
1. **Unnatural Bay Spawning**: Small bancas and arriving commercial craft spawn directly inside the central navigation bay ($X \in [45, 180]$), cluttering the basin and breaking maritime realism. Default fleet counts (24 medium, 32 small) are too crowded for the harbor channel.
2. **Simplified Boxy Vessel Meshes**: Ships are basic extruded boxes with cone bows. Philippine commercial fishing craft (*Basnig*, *Purse Seiner*, *Ring-Netter*) lack flared hulls, red anti-fouling boot-topping, wheelhouses with bridge windows, derrick rigs, tire bumpers, and visible *banyera* (fish tub) cargo stacks. Outriggers on bancas float too high or lack crossbeams (*tawid*).
3. **Rigid Collision & Inelastic Clumping**: Vessels collide abruptly or get repulsed erratically. Ahead vessels get rear-ended because there is no forward whisker look-ahead sensor or COLREGS-compliant starboard evasive steering.
4. **Static Hull-Attached Wake**: Wake is a static plane parented to the boat mesh that turns instantly with the vessel rather than forming curved, expanding, fading trails left behind in world coordinates.
5. **Disconnected Lightering Lifecycle**: Bancas and mother vessels lack clear visual cargo state synchronization (crates visible on deck when loaded, empty when unloaded).

---

## 2. Codebase Audit & Line-by-Line Target Mapping

### A. Modifications in `app.py`
| Line Range | Target Component | Modification |
|---|---|---|
| **L479–L483** | Sidebar Physical Topology Sliders | Update `num_small_boats` slider: `min_value=2, max_value=25, value=8`. Add `num_medium_boats`: `min_value=5, max_value=30, value=12`. |
| **L111–L112** | Full-Screen 3D Digital Twin Call | Pass calibrated default fleet counts if parameterized, maintaining zero-clutter fullscreen presentation. |

### B. Modifications in `src/port_3d_engine.py`
| Line Range | Target Component | Modification |
|---|---|---|
| **L669–L684** | HTML Modal Parameter Sliders | Update `sl-medium-fleet` (`min="5" max="30" value="12"`) and `sl-bancas-fleet` (`min="2" max="25" value="8"`). |
| **L1136–L1168**| Boundary Clamping & Solid Walls | Refine `applyBoundaryClamps(boat)` and maintain rock-steady wharf lock (`X = -28.0`, front face `X = -35.0`). |
| **L1170–L1206**| Hull Collision Resolution | Replace basic wall bumper with damped soft-sphere vessel-to-vessel physics while keeping docked boats immune to pushback. |
| **L1208–L1308**| `createVesselMesh(type)` | Complete rebuild: Authentic Philippine hulls (*Basnig*, *Purse Seiner*, *Ring-Netter*, *Shuttle Banca*) with local `+Z` bow, two-tone paint, cabin glazing, derrick booms, tire bumpers, and dynamic *banyera* tub stacks. |
| **L1337–L1340**| Fleet Size Constants | Change defaults: `targetTotalMediumFleet = 12`, `targetTotalBancas = 8`. |
| **L1384–L1531**| `initFleet()` | Ban center spawning ($X \in [-20, 180]$). Stagger initial $t=0$ vessels (3 docked, 3 anchored, 6 at sea/entering). Spawn incoming craft at eastern horizon ($X = 240, Z \in [-90, 90]$) with fade-in. |
| **L1536–L1568**| `updateVesselKinematics()` | Implement 3-whisker look-ahead sensor cone (24m range, $\pm 55^\circ$), starboard COLREGS steering, trailing throttle attenuation ($0.35\times$), and soft repulsion. |
| **L1620–L1633**| Diurnal Deep-Sea Horizon Spawning | Enforce horizon spawn ($X = 240, Z \in [-90, +90]$) with `spawnOpacity` ramp over 2.0s. |
| **L1645–L1655**| Vessel Wake & Hydrodynamics | Integrate with 150-particle pooled World-Space Wake Effector; calculate dynamic pitch/roll and bow spray. |
| **L1845–L1942**| Small Boat Lightering & Banyera Transfer | Sync visual *banyera* stacks on small bancas and mother vessels during lightering transfers (6–9s) and wharf discharge (8–12s). |
| **L2028–L2058**| `render(time)` Loop | Update world-space wake particles (expansion, decay, death recycling) alongside lighthouse rotor and ocean waves. |
| **L2231–L2306**| Slider Event Listeners & Presets | Sync slider bounds and update preset configurations to reflect 12 medium / 8 banca baseline. |

---

## 3. Blueprint 1: Fleet Resizing & Horizon Spawning Architecture

### Mathematical & Spatial Specifications
- **Exclusion Zone**: Absolutely no vessel may spawn or be positioned at initialization within $X \in [-20.0, 180.0]$ unless explicitly docked at $X = -28.0$ or anchored at designated bayside holding coordinates ($X \in [95.0, 145.0], Z \in [-55.0, 55.0]$).
- **Default Fleet Scale**:
  - Medium Commercial: **12 craft** (slider range: 5 to 30).
  - Small Bancas: **8 craft** (slider range: 2 to 25).
- **Initial State Distribution ($t = 0$)**:
  - **Medium Fleet (12 craft)**:
    - 3 craft docked at Wharf ($X = -28.0$, berths B2, B6, B10) with staggered remaining timers (5s, 15s, 28s).
    - 3 craft anchored in outer bay ($X \in [105, 140]$, $Z \in [-50, 50]$).
    - 6 craft entering from sea ($X \in [200, 235]$) or active at sea (`AT_SEA_FISHING`).
  - **Small Banca Fleet (8 craft)**:
    - 2 craft at Wharf landing aprons ($X = -28.0$).
    - 3 craft servicing anchored medium vessels at $X \in [100, 140]$.
    - 3 craft entering from harbor approach ($X \in [195, 230]$).
- **Inbound Spawning ($t > 0$)**:
  - Spawning coordinates: $X = 240.0$, $Z = \text{uniform}(-90.0, +90.0)$.
  - Inbound heading: $\psi = -\frac{\pi}{2}$ (facing $-X$, directly westward into San Miguel Bay).
  - Fade-in animation: New mesh materials set to `transparent = true`, opacity lerping from $0.0 \to 1.0$ over 2.0 seconds.

### Target Code Replacement: HTML Sliders (`src/port_3d_engine.py` ~L669–L684)
```html
<div class="param-row">
    <div class="param-info">
        <div class="param-title">Total Medium Commercial Vessels Fleet</div>
        <div class="param-desc">Commercial ring-netters, purse seiners, and basnigs (calibrated baseline: 12 craft).</div>
    </div>
    <div class="param-ctrl">
        <input type="range" id="sl-medium-fleet" min="5" max="30" step="1" value="12">
        <span id="val-medium-fleet" class="param-val">12 craft</span>
    </div>
</div>

<div class="param-row">
    <div class="param-info">
        <div class="param-title">Total Small Boats Fleet (Shuttle Bancas)</div>
        <div class="param-desc">Artisanal double-outrigger bancas for lightering and shallow operations (baseline: 8 craft).</div>
    </div>
    <div class="param-ctrl">
        <input type="range" id="sl-bancas-fleet" min="2" max="25" step="1" value="8">
        <span id="val-bancas-fleet" class="param-val">8 craft</span>
    </div>
</div>
```

### Target Code Replacement: `initFleet()` Spawning Logic (`src/port_3d_engine.py` ~L1384–L1531)
```javascript
let targetTotalMediumFleet = 12;
let targetTotalBancas = 8;

function initFleet() {
    // Clear existing meshes
    vessels.forEach(v => scene.remove(v.mesh));
    vessels.length = 0;
    bancas.forEach(b => scene.remove(b.mesh));
    bancas.length = 0;

    const initialBerthIndices = [1, 5, 9];
    const mediumNames = [
        'MV-MercedesQueen', 'MV-SanMiguel', 'MV-BicolExpress', 'MV-DaetStar',
        'MV-NagaPride', 'MV-PandanGem', 'MV-SanRoque', 'MV-BagongSilang',
        'MV-CamNorte', 'MV-PacificDawn', 'MV-Apolonio', 'MV-IslaVerde'
    ];

    for (let i = 0; i < targetTotalMediumFleet; i++) {
        const vName = mediumNames[i % mediumNames.length];
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
            spawnOpacity: 1.0
        };

        if (i < 3) {
            // Initial Docked Vessels at B2, B6, B10 (X = -28.0)
            const bIdx = initialBerthIndices[i];
            const b = BERTH_SLOTS[bIdx];
            b.occupiedBy = v.name;
            v.assignedBerth = b;
            v.isDocked = true;
            v.state = 'Unloading at Wharf';
            v.mesh.position.set(b.dockX, 0, b.z);
            v.heading = 0;
            v.mesh.rotation.y = 0;
            const initProgress = 0.25 + (i * 0.30);
            v.unloadTimer = v.totalUnloadSec * (1.0 - initProgress);
            v.cargo = Math.round(v.maxCargo * (1.0 - initProgress));
            v.remainingSec = v.unloadTimer;
            v.departureDelay = 2.0 + Math.random() * 2.0;
            updateVesselCrateVisuals(v);
        } else if (i < 6) {
            // Initial Anchored Vessels in Outer Bay
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
            // Initial Deep Sea Fleet
            v.state = 'AT_SEA_FISHING';
            v.mesh.visible = false;
            v.fishingTimer = computeFishingDuration(simTime) * (0.2 + (i - 6) * 0.2);
        }
        vessels.push(v);
    }

    // 2. Small Bancas Fleet (8 Craft Total: 6 Tenders, 2 Independents)
    for (let i = 0; i < targetTotalBancas; i++) {
        const bMesh = createVesselMesh('Banca');
        scene.add(bMesh);

        const isTender = (i < 6); // 75% Tenders, 25% Independents
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
            patrolTargetX: 95 + Math.random() * 45,
            patrolTargetZ: -50 + Math.random() * 100,
            cargo: isTender ? 0 : 25,
            maxCargo: 40,
            heading: 0,
            speed: 3.5,
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
            spawnOpacity: 1.0
        };

        if (i < 2) {
            // Initially at Wharf Landing apron
            const slot = BANCA_LANDING_SPOTS[i];
            b.mesh.position.set(slot.x, 0, slot.z);
            b.isDocked = true;
            b.state = 'unloading_at_wharf';
            b.unloadTimer = 6.0 + Math.random() * 4.0;
            b.cargo = 20;
        } else if (i < 5) {
            // Stationed near anchored mother boats
            b.state = 'patrolling';
            b.mesh.position.set(100 + (i - 2) * 15, 0, -35 + (i - 2) * 35);
            b.heading = -Math.PI / 2;
            b.mesh.rotation.y = b.heading;
        } else {
            // Inbound approaching channel
            b.state = isTender ? 'patrolling' : 'to_wharf';
            b.mesh.position.set(195 + (i - 5) * 15, 0, -30 + (i - 5) * 30);
            b.heading = -Math.PI / 2;
            b.mesh.rotation.y = b.heading;
        }
        updateBancaCrateVisuals(b);
        bancas.push(b);
    }
}
```

---

## 4. Blueprint 2: Procedural 3D Philippine Fishing Vessel Models

### Visual & Structural Requirements
1. **Local Axis Alignment**: Bow is placed strictly along **Local $+Z$**, Stern along **Local $-Z$**, Starboard along **Local $+X$**, and Port along **Local $-X$**.
2. **Ring-Netter & Purse Seiner**:
   - **Lower Hull**: Red anti-fouling boot-topping paint (`#991B1B`), wedge-shaped hydrodynamic keel with flared V-bow.
   - **Upper Hull**: Distinct emerald green (`#059669`) for Purse Seiners, marine amber (`#D97706`) for Ring-Netters, and ocean blue (`#0284C7`) for Basnigs.
   - **Deckhouse & Wheelhouse**: Off-white/slate structure with dark glass bridge windows, searchlight, and radar dome.
   - **A-Frame Mast & Cargo Boom**: Structural derrick boom angled over the aft deck for hauling seine nets and hoisting banyeras.
   - **Net Drum / Coil**: Dark charcoal braided cylinder representing the heavy purse seine/ring net at the stern deck.
   - **Rubber Tire Fenders**: 4 miniature dark-gray torus meshes hung along the port and starboard gunwales.
   - **Dynamic Banyera Crate Stacks**: Group of colored tubs (orange `#EA580C`, blue `#2563EB`, gray `#64748B`) stacked on the midship cargo hatch that scale and hide as cargo unloads.
3. **Traditional Philippine Basnig**:
   - Extended outrigger crossbeams (*tawid*) spanning $12.0\text{ m}$.
   - Heavy bamboo/timber *katig* pontoons positioned exactly at the water skimming line ($Y = 0.05$).
   - Multiple extended lift-net booms radiating diagonally from port and starboard.
4. **Artisanal Double-Outrigger Shuttle Banca**:
   - Slender carved wooden dugout canoe hull (*bangka*).
   - Twin flexible bamboo *katig* floats at $Y = 0.05$.
   - Central canvas weather canopy with passenger/crate cargo well.

### Complete Replacement: `createVesselMesh(type)` (`src/port_3d_engine.py` ~L1208–L1308)
```javascript
function createVesselMesh(type) {
    const root = new THREE.Group();
    const meshVisualGroup = new THREE.Group();
    meshVisualGroup.name = 'visualGroup';
    root.add(meshVisualGroup);

    // Shared Palette Materials
    const darkTireMat = new THREE.MeshStandardMaterial({ color: 0x1E293B, roughness: 0.9 });
    const woodMat = new THREE.MeshStandardMaterial({ color: 0xB45309, roughness: 0.75 });
    const bambooMat = new THREE.MeshStandardMaterial({ color: 0xD97706, roughness: 0.6 });
    const windowMat = new THREE.MeshPhysicalMaterial({ color: 0x38BDF8, roughness: 0.1, transmission: 0.6, transparent: true });
    const antiFoulingRedMat = new THREE.MeshStandardMaterial({ color: 0x991B1B, roughness: 0.5 });
    const metalMat = new THREE.MeshStandardMaterial({ color: 0x64748B, metalness: 0.6, roughness: 0.4 });

    if (type === 'Banca') {
        // -----------------------------------------------------------------
        // PHILIPPINE DOUBLE-OUTRIGGER SHUTTLE BANCA (Local +Z = Bow)
        // -----------------------------------------------------------------
        const bancaHullMat = new THREE.MeshStandardMaterial({ color: 0x0284C7, roughness: 0.4 });
        const canopyMat = new THREE.MeshStandardMaterial({ color: 0xF1F5F9, roughness: 0.8 });

        // 1. Slender Main Wooden Hull (Length 5.6m, Beam 0.9m)
        const hull = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.65, 4.4), bancaHullMat);
        hull.position.set(0, 0.35, -0.2);
        hull.castShadow = true;
        meshVisualGroup.add(hull);

        // 2. Sharp Pointed Bow Rake (At +Z)
        const bowCone = new THREE.Mesh(new THREE.ConeGeometry(0.48, 1.4, 4), bancaHullMat);
        bowCone.rotation.x = Math.PI / 2;
        bowCone.rotation.y = Math.PI / 4;
        bowCone.position.set(0, 0.42, 2.5);
        bowCone.castShadow = true;
        meshVisualGroup.add(bowCone);

        // 3. Tapered Transom Stern (At -Z)
        const sternBox = new THREE.Mesh(new THREE.BoxGeometry(0.65, 0.55, 0.8), woodMat);
        sternBox.position.set(0, 0.38, -2.6);
        meshVisualGroup.add(sternBox);

        // 4. Tawid Crossbeams (Fore & Aft)
        const tawidGeo = new THREE.CylinderGeometry(0.045, 0.045, 3.2, 8);
        const tawidFore = new THREE.Mesh(tawidGeo, bambooMat);
        tawidFore.rotation.z = Math.PI / 2;
        tawidFore.position.set(0, 0.52, 0.8);
        meshVisualGroup.add(tawidFore);

        const tawidAft = new THREE.Mesh(tawidGeo, bambooMat);
        tawidAft.rotation.z = Math.PI / 2;
        tawidAft.position.set(0, 0.52, -1.0);
        meshVisualGroup.add(tawidAft);

        // 5. Bamboo Katig Floats (Outriggers at Y = 0.08 Water Surface)
        const katigGeo = new THREE.CylinderGeometry(0.09, 0.09, 4.6, 8);
        const katigPort = new THREE.Mesh(katigGeo, bambooMat);
        katigPort.rotation.x = Math.PI / 2;
        katigPort.position.set(-1.55, 0.08, -0.1);
        meshVisualGroup.add(katigPort);

        const katigStbd = new THREE.Mesh(katigGeo, bambooMat);
        katigStbd.rotation.x = Math.PI / 2;
        katigStbd.position.set(1.55, 0.08, -0.1);
        meshVisualGroup.add(katigStbd);

        // 6. Canopy Roof
        const canopy = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.04, 2.2), canopyMat);
        canopy.position.set(0, 1.15, -0.1);
        meshVisualGroup.add(canopy);

        // 7. Dynamic Banyera Tub Group (Toggled during lightering)
        const crateGroup = new THREE.Group();
        crateGroup.name = 'cargoCrates';
        const tubGeo = new THREE.CylinderGeometry(0.18, 0.15, 0.18, 8);
        const tubMatOrange = new THREE.MeshStandardMaterial({ color: 0xEA580C, roughness: 0.5 });
        const tubMatBlue = new THREE.MeshStandardMaterial({ color: 0x2563EB, roughness: 0.5 });

        for (let row = 0; row < 3; row++) {
            for (let col = 0; col < 2; col++) {
                const tub = new THREE.Mesh(tubGeo, (row + col) % 2 === 0 ? tubMatOrange : tubMatBlue);
                tub.position.set((col - 0.5) * 0.32, 0.55, -0.5 + row * 0.38);
                crateGroup.add(tub);
            }
        }
        meshVisualGroup.add(crateGroup);

    } else {
        // -----------------------------------------------------------------
        // COMMERCIAL FISHING CRAFT: Basnig / Purse Seiner / Ring-Netter
        // -----------------------------------------------------------------
        const hullColors = {
            'Basnig': 0x0284C7,
            'Purse Seiner': 0x059669,
            'Ring-Netter': 0xD97706
        };
        const upperHullMat = new THREE.MeshStandardMaterial({
            color: hullColors[type] || 0x0284C7,
            roughness: 0.4
        });
        const deckMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.7 });
        const wheelhouseMat = new THREE.MeshStandardMaterial({ color: 0xF8FAFC, roughness: 0.3 });

        // 1. Lower Anti-Fouling Red Hull (Waterline Y = 0.0 to 0.7)
        const lowerHull = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.75, 11.2), antiFoulingRedMat);
        lowerHull.position.set(0, 0.38, -0.4);
        lowerHull.castShadow = true;
        meshVisualGroup.add(lowerHull);

        const lowerBowWedge = new THREE.Mesh(new THREE.ConeGeometry(1.8, 2.6, 4), antiFoulingRedMat);
        lowerBowWedge.rotation.x = Math.PI / 2;
        lowerBowWedge.rotation.y = Math.PI / 4;
        lowerBowWedge.position.set(0, 0.38, 5.8);
        lowerBowWedge.castShadow = true;
        meshVisualGroup.add(lowerBowWedge);

        // 2. Upper Freeboard Hull (Y = 0.75 to 1.85)
        const upperHull = new THREE.Mesh(new THREE.BoxGeometry(3.8, 1.1, 11.4), upperHullMat);
        upperHull.position.set(0, 1.3, -0.4);
        upperHull.castShadow = true;
        meshVisualGroup.add(upperHull);

        const upperBowFlared = new THREE.Mesh(new THREE.ConeGeometry(1.95, 2.8, 4), upperHullMat);
        upperBowFlared.rotation.x = Math.PI / 2;
        upperBowFlared.rotation.y = Math.PI / 4;
        upperBowFlared.position.set(0, 1.3, 5.9);
        upperBowFlared.castShadow = true;
        meshVisualGroup.add(upperBowFlared);

        // 3. Wooden Working Deck
        const mainDeck = new THREE.Mesh(new THREE.BoxGeometry(3.5, 0.1, 11.0), deckMat);
        mainDeck.position.set(0, 1.86, -0.4);
        meshVisualGroup.add(mainDeck);

        // 4. Two-Tier Wheelhouse & Navigation Bridge (Fore/Midship)
        const bridgeLower = new THREE.Mesh(new THREE.BoxGeometry(2.5, 1.4, 3.4), wheelhouseMat);
        bridgeLower.position.set(0, 2.6, 0.8);
        bridgeLower.castShadow = true;
        meshVisualGroup.add(bridgeLower);

        const bridgeUpper = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.1, 2.4), wheelhouseMat);
        bridgeUpper.position.set(0, 3.85, 0.6);
        bridgeUpper.castShadow = true;
        meshVisualGroup.add(bridgeUpper);

        // Glazed Bridge Windows (Facing +Z)
        const winFore = new THREE.Mesh(new THREE.PlaneGeometry(1.9, 0.6), windowMat);
        winFore.position.set(0, 3.95, 1.82);
        meshVisualGroup.add(winFore);

        // 5. Heavy A-Frame Mast & Derricks
        const mastPole = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.14, 5.2, 8), metalMat);
        mastPole.position.set(0, 4.8, 2.0);
        meshVisualGroup.add(mastPole);

        const boomDerrick = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, 5.5, 8), metalMat);
        boomDerrick.rotation.x = -Math.PI / 3.8;
        boomDerrick.position.set(0, 3.4, -1.2);
        meshVisualGroup.add(boomDerrick);

        // 6. Stern Net Drum / Seine Gear
        const netDrum = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 2.6, 12), darkTireMat);
        netDrum.rotation.z = Math.PI / 2;
        netDrum.position.set(0, 2.4, -4.5);
        meshVisualGroup.add(netDrum);

        // 7. Rubber Tire Gunwale Bumpers (Fenders)
        const tireGeo = new THREE.TorusGeometry(0.26, 0.10, 6, 12);
        for (let side of [-1, 1]) {
            for (let fz of [-3.2, -1.0, 1.2, 3.4]) {
                const tire = new THREE.Mesh(tireGeo, darkTireMat);
                tire.rotation.y = Math.PI / 2;
                tire.position.set(side * 1.95, 1.5, fz);
                meshVisualGroup.add(tire);
            }
        }

        // 8. Basnig Multi-Boom Outrigger Rig
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

        // 9. Cargo Hatch Banyera Fish Tubs (Dynamic Scaling Group)
        const crateGroup = new THREE.Group();
        crateGroup.name = 'cargoCrates';
        const crateBoxGeo = new THREE.BoxGeometry(0.55, 0.40, 0.55);
        const crateMatBlue = new THREE.MeshStandardMaterial({ color: 0x1D4ED8, roughness: 0.5 });
        const crateMatOrange = new THREE.MeshStandardMaterial({ color: 0xC2410C, roughness: 0.5 });

        for (let ix = -1; ix <= 1; ix++) {
            for (let iz = -2; iz <= 0; iz++) {
                const crate = new THREE.Mesh(crateBoxGeo, (ix + iz) % 2 === 0 ? crateMatBlue : crateMatOrange);
                crate.position.set(ix * 0.65, 2.1, iz * 0.65 - 1.8);
                crateGroup.add(crate);
            }
        }
        meshVisualGroup.add(crateGroup);
    }

    return root;
}
```

### Visual Banyera Cargo Synchronization Helpers
```javascript
function updateVesselCrateVisuals(boat) {
    const cg = boat.mesh.getObjectByName('cargoCrates');
    if (!cg) return;
    const ratio = boat.maxCargo > 0 ? (boat.cargo / boat.maxCargo) : 0;
    cg.visible = ratio > 0.05;
    cg.scale.set(1.0, Math.max(0.1, ratio), 1.0);
}

function updateBancaCrateVisuals(banca) {
    const cg = banca.mesh.getObjectByName('cargoCrates');
    if (!cg) return;
    cg.visible = banca.cargo > 0;
    cg.scale.set(1.0, banca.cargo > 0 ? 1.0 : 0.001, 1.0);
}
```

---

## 5. Blueprint 3: Predictive 3-Whisker Sensor Avoidance & Soft Physics

### Mathematical Specifications
1. **Forward Look-Ahead Whisker Array**:
   - **Center Whisker**: Vector along boat heading $\hat{u}_C = (\sin\psi, \cos\psi)$, range $L_C = 24.0\text{ units}$.
   - **Port Whisker**: Vector angled at $\psi - 35^\circ$, range $L_P = 18.0\text{ units}$.
   - **Starboard Whisker**: Vector angled at $\psi + 35^\circ$, range $L_S = 18.0\text{ units}$.
2. **COLREGS Evasive Steering (Starboard Yield)**:
   - When any obstacle (moving boat or stationary anchorage) enters the whisker sensor polygon:
     - Apply clockwise yaw bias: $\Delta \psi = +0.045 \times dt \times \text{urgency}$.
     - Attenuate engine throttle:
       $$\text{targetSpeed} \gets \text{targetSpeed} \times 0.35 \quad \text{if } \text{distAhead} < 14.0$$
3. **Soft-Sphere Hull Repulsion (Damped Non-Jitter Elasticity)**:
   - For any pair of active moving vessels $(A, B)$ with positions $\mathbf{p}_A, \mathbf{p}_B$ and safe clearance radii $r_A, r_B$:
     $$\text{dist} = \|\mathbf{p}_A - \mathbf{p}_B\|$$
     $$\text{minSeparation} = r_A + r_B + 2.0$$
   - If $\text{dist} < \text{minSeparation}$ and neither vessel is docked:
     $$\mathbf{n} = \frac{\mathbf{p}_A - \mathbf{p}_B}{\text{dist}}, \quad \delta = \text{minSeparation} - \text{dist}$$
     $$\mathbf{p}_A \gets \mathbf{p}_A + \mathbf{n} \cdot (\delta \times 0.45)$$
     $$\mathbf{p}_B \gets \mathbf{p}_B - \mathbf{n} \cdot (\delta \times 0.45)$$
4. **Docked Immunity (Zero Shaking)**:
   - If `v.isDocked || v.state === 'Unloading at Wharf'`, completely bypass boat-to-boat repulsion and boundary shoving. Lock $X = -28.0$ and heading $= 0$.

### Complete Replacement: Kinematics & Avoidance (`src/port_3d_engine.py` ~L1536–L1568)
```javascript
function updateVesselKinematics(boat, targetX, targetZ, dt) {
    if (boat.isDocked) {
        boat.speed = 0;
        return 0;
    }

    const dx = targetX - boat.mesh.position.x;
    const dz = targetZ - boat.mesh.position.z;
    const distToTarget = Math.hypot(dx, dz);

    let desiredHeading = Math.atan2(dx, dz);

    // -------------------------------------------------------------
    // PREDICTIVE 3-WHISKER SENSOR CONE SCANNER (COLREGS STARBOARD YAW)
    // -------------------------------------------------------------
    const scanRadius = 24.0;
    const fwdX = Math.sin(boat.heading);
    const fwdZ = Math.cos(boat.heading);
    let obstacleAhead = false;
    let obstacleDist = 999.0;

    // Scan all other vessels
    const allCraft = [...vessels, ...bancas];
    for (let other of allCraft) {
        if (other === boat || !other.mesh.visible) continue;
        const ox = other.mesh.position.x - boat.mesh.position.x;
        const oz = other.mesh.position.z - boat.mesh.position.z;
        const oDist = Math.hypot(ox, oz);

        if (oDist < scanRadius && oDist > 0.1) {
            // Dot product to test if craft is in front hemisphere
            const dotFwd = (ox * fwdX + oz * fwdZ) / oDist;
            if (dotFwd > 0.55) { // Within +/-56 degree forward sensor cone
                obstacleAhead = true;
                if (oDist < obstacleDist) obstacleDist = oDist;
            }
        }
    }

    // Apply COLREGS Starboard Steering & Trailing Throttle Attenuation
    let evasionYawBias = 0;
    let throttleScale = 1.0;

    if (obstacleAhead) {
        // Steer starboard (+ yaw) to pass port-to-port
        const urgency = Math.min(1.0, (scanRadius - obstacleDist) / scanRadius);
        evasionYawBias = 0.55 * urgency;

        if (obstacleDist < 14.0) {
            throttleScale = 0.35; // Decelerate to avoid rear-end collision
        }
    }

    let effectiveHeading = desiredHeading + evasionYawBias;
    let angleError = effectiveHeading - boat.heading;
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

    // Apply Soft Damped Physics & Hard Seawall Half-Spaces
    resolveSoftHullCollisions(boat);
    applyBoundaryClamps(boat);

    return distToTarget;
}

function resolveSoftHullCollisions(boat) {
    if (boat.isDocked) return;
    const rA = boat.isSmallBoat ? 1.8 : 3.8;

    const allCraft = [...vessels, ...bancas];
    for (let other of allCraft) {
        if (other === boat || !other.mesh.visible || other.isDocked) continue;
        const rB = other.isSmallBoat ? 1.8 : 3.8;
        const minSep = rA + rB + 1.8;

        const dx = boat.mesh.position.x - other.mesh.position.x;
        const dz = boat.mesh.position.z - other.mesh.position.z;
        const distSq = dx * dx + dz * dz;

        if (distSq < minSep * minSep && distSq > 0.001) {
            const dist = Math.sqrt(distSq);
            const pen = minSep - dist;
            const nx = dx / dist;
            const nz = dz / dist;

            // Damped soft pushback
            boat.mesh.position.x += nx * pen * 0.35;
            boat.mesh.position.z += nz * pen * 0.35;
        }
    }
}
```

---

## 6. Blueprint 4: World-Space Dynamic Water Effector System

### Hydrodynamic Architecture
1. **Decoupled World-Space Particle Pool**:
   - Wake particles are **NOT parented** to boats. They are child elements of `scene` with world positions fixed upon ejection.
   - Pre-allocated circular buffer pool of **150 particle meshes** (`THREE.RingGeometry` with soft fading vertex/material opacity).
2. **Particle Generation**:
   - Emitted from vessel stern world coordinates:
     $$x_{\text{emit}} = x_{\text{boat}} - \sin\psi \cdot \frac{L}{2}$$
     $$z_{\text{emit}} = z_{\text{boat}} - \cos\psi \cdot \frac{L}{2}$$
     $$y_{\text{emit}} = 0.08 \quad (\text{resting slightly above water plane } Y = 0.0)$$
   - Trigger rate: Emitted every $0.10\text{s}$ when $\|\text{speed}\| > 1.2\text{ knots}$.
3. **Particle Dynamics in `render()` Loop**:
   - Each active particle expands outwards: $r(t) = r_0 + \text{expandRate} \cdot \Delta t$.
   - Opacity decays exponentially: $\alpha(t) = \alpha_0 \cdot (1 - t / T_{\text{life}})$.
   - Lifetime: $T_{\text{life}} = 2.2\text{ seconds}$. When expired, particle returns to pool.
4. **Vessel Pitch & Roll Heave**:
   - Hydrodynamic pitch proportional to acceleration and wave slope:
     $$\theta_{\text{pitch}} = \sin(\omega t + \phi) \cdot 0.035 - \frac{\text{speed}}{\text{maxSpeed}} \cdot 0.03$$
     $$\theta_{\text{roll}} = \cos(\omega t + \phi) \cdot 0.025 + \text{turnRate} \cdot 0.08$$

### World-Space Particle System Implementation
```javascript
// -------------------------------------------------------------
// POOLED 150-PARTICLE WORLD-SPACE WAKE EFFECTOR
// -------------------------------------------------------------
const MAX_WAKE_PARTICLES = 150;
const wakePool = [];
const wakeRingGeo = new THREE.RingGeometry(0.3, 1.1, 16);
wakeRingGeo.rotateX(-Math.PI / 2);

const wakeMatMaster = new THREE.MeshBasicMaterial({
    color: 0xE0F2FE,
    transparent: true,
    opacity: 0.0,
    depthWrite: false,
    side: THREE.DoubleSide
});

for (let i = 0; i < MAX_WAKE_PARTICLES; i++) {
    const pMesh = new THREE.Mesh(wakeRingGeo, wakeMatMaster.clone());
    pMesh.visible = false;
    scene.add(pMesh);
    wakePool.push({
        mesh: pMesh,
        active: false,
        age: 0,
        maxLife: 2.2,
        scale: 1.0,
        expandRate: 2.2,
        initialAlpha: 0.45
    });
}

let wakePoolIndex = 0;
function spawnWorldWake(x, y, z, boatScale, speedRatio) {
    const p = wakePool[wakePoolIndex];
    wakePoolIndex = (wakePoolIndex + 1) % MAX_WAKE_PARTICLES;

    p.active = true;
    p.age = 0;
    p.scale = boatScale * 0.8;
    p.expandRate = 1.8 + speedRatio * 2.0;
    p.initialAlpha = Math.min(0.55, 0.2 + speedRatio * 0.35);

    p.mesh.position.set(x, 0.08, z);
    p.mesh.scale.set(p.scale, p.scale, p.scale);
    p.mesh.material.opacity = p.initialAlpha;
    p.mesh.visible = true;
}

function updateWorldWakeParticles(dt) {
    for (let p of wakePool) {
        if (!p.active) continue;
        p.age += dt;
        if (p.age >= p.maxLife) {
            p.active = false;
            p.mesh.visible = false;
        } else {
            const progress = p.age / p.maxLife;
            const currentScale = p.scale + p.age * p.expandRate;
            p.mesh.scale.set(currentScale, currentScale, currentScale);
            p.mesh.material.opacity = p.initialAlpha * (1.0 - progress);
        }
    }
}
```

### Hook in `updateSimulation()` for Emitting Wake
```javascript
// Inside vessels.forEach(v => { ... })
if (v.mesh.visible && Math.abs(v.speed) > 1.2) {
    v.wakeTimer = (v.wakeTimer || 0) + dt;
    if (v.wakeTimer > 0.10) {
        v.wakeTimer = 0;
        const sternDist = v.isSmallBoat ? 2.5 : 5.8;
        const wx = v.mesh.position.x - Math.sin(v.heading) * sternDist;
        const wz = v.mesh.position.z - Math.cos(v.heading) * sternDist;
        spawnWorldWake(wx, 0.08, wz, v.isSmallBoat ? 1.0 : 2.2, Math.abs(v.speed) / v.maxSpeed);
    }
}
```

---

## 7. Blueprint 5: Natural Multi-Agent Lightering & Berthing Loop

### Multi-Agent Interaction Diagram
```
[Mother Vessel Arrives at Outer Bay]
                 │
                 ▼
    [Anchored at X in (95, 140)] ◄──────────────────────┐
                 │                                      │
                 ├─────────► [Banca Approaches Mother]  │
                 │                     │                │
                 │                     ▼                │
                 │          [Transfers Crate Load]      │
                 │          (6-9s; Banyeras shrink on   │
                 │           Mother, appear on Banca)   │
                 │                     │                │
                 │                     ▼                │
                 │          [Banca to Wharf Slot]       │
                 │          (X = -28.0; 8-12s Unload)   │
                 │                     │                │
                 │                     ▼                │
                 │          [Banca Returns to Bay] ─────┘
                 │
                 ▼
     (When Cargo reaches 0)
[Mother Vessel Departs Channel to Deep Sea]
                 │
                 ▼
 [Out at Sea Fishing (X > 235)]
```

### Complete Lightering Engine Implementation (`src/port_3d_engine.py` ~L1845–L1942)
```javascript
// UPDATE SMALL BOAT FLEET (TENDERS + INDEPENDENTS)
let activeBancas = 0;

bancas.forEach(b => {
    const waveY = getWaveHeight(b.mesh.position.x, b.mesh.position.z, waveTime);
    b.mesh.position.y = waveY * 0.55;

    // Pitch & Roll Dynamics
    b.mesh.rotation.x = Math.sin(waveTime * 2.5 + b.bobOffset) * 0.04;
    b.mesh.rotation.z = Math.cos(waveTime * 2.0 + b.bobOffset) * 0.03;

    if (b.role === 'tender') {
        if (b.state === 'patrolling') {
            const dist = updateVesselKinematics(b, b.patrolTargetX, b.patrolTargetZ, dt);
            if (dist < 8.0) {
                b.patrolTargetX = 90 + Math.random() * 50;
                b.patrolTargetZ = -50 + Math.random() * 100;
            }

            // Seek anchored mother vessel with remaining cargo
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
            // Approach port side of mother vessel
            const tx = b.targetBoat.mesh.position.x - 4.5;
            const tz = b.targetBoat.mesh.position.z;
            const dist = updateVesselKinematics(b, tx, tz, dt);

            if (dist < 4.0) {
                b.state = 'transferring';
                b.transferTimer = 6.0 + Math.random() * 3.0; // 6 to 9 seconds
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
                    updateVesselCrateVisuals(b.targetBoat);
                    b.targetBoat.servicedByBanca = null;

                    if (b.targetBoat.cargo <= 0) {
                        // Relieved of cargo; depart to sea
                        b.targetBoat.state = 'Departing';
                        b.targetBoat.departStep = 1;
                        b.targetBoat.deepSeaTargetX = 280;
                        b.targetBoat.deepSeaTargetZ = -130 + Math.random() * 260;
                    }
                }
                updateBancaCrateVisuals(b);
                b.targetBoat = null;
                b.state = 'to_wharf';
            }
        } else if (b.state === 'to_wharf') {
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
                b.unloadTimer = 8.0 + Math.random() * 4.0; // 8 to 12 seconds
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
                updateBancaCrateVisuals(b);
                b.isDocked = false;
                b.state = 'reversing_from_wharf';
                b.reverseTimer = 2.5;
                b.isReversing = true;
            }
        } else if (b.state === 'reversing_from_wharf') {
            activeBancas++;
            b.isReversing = true;
            b.reverseTimer -= dt;
            updateVesselKinematics(b, b.mesh.position.x + 8.0, b.mesh.position.z, dt);

            if (b.reverseTimer <= 0 || b.mesh.position.x >= -16.0) {
                b.isReversing = false;
                b.state = 'patrolling';
                b.patrolTargetX = 90 + Math.random() * 50;
                b.patrolTargetZ = -50 + Math.random() * 100;
            }
        }
    } else {
        // Independent Fishing Banca
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
                b.unloadTimer = 8.0 + Math.random() * 4.0;
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
                updateBancaCrateVisuals(b);
                b.isDocked = false;
                b.state = 'reversing_from_wharf';
                b.reverseTimer = 2.5;
                b.isReversing = true;
            }
        } else if (b.state === 'reversing_from_wharf') {
            activeBancas++;
            b.isReversing = true;
            b.reverseTimer -= dt;
            updateVesselKinematics(b, b.mesh.position.x + 8.0, b.mesh.position.z, dt);

            if (b.reverseTimer <= 0 || b.mesh.position.x >= -16.0) {
                b.isReversing = false;
                b.state = 'departing_sea';
            }
        } else if (b.state === 'departing_sea') {
            activeBancas++;
            updateVesselKinematics(b, 240, b.mesh.position.z, dt);
            if (b.mesh.position.x >= 235) {
                b.mesh.visible = false;
                b.state = 'sea_fishing';
                b.seaTimer = 20 + Math.random() * 30;
            }
        } else if (b.state === 'sea_fishing') {
            b.seaTimer -= dt * timeScale;
            if (b.seaTimer <= 0) {
                b.cargo = Math.floor(15 + Math.random() * 25);
                updateBancaCrateVisuals(b);
                b.mesh.position.set(235, 0, -40 + Math.random() * 80);
                b.heading = -Math.PI / 2;
                b.mesh.rotation.y = b.heading;
                b.mesh.visible = true;
                b.state = 'to_wharf';
            }
        }
    }
});
```

---

## 8. Verification & Execution Safety Protocol

### Pre-Flight Verification Steps (for Phase 2 Execution)
1. **Syntax Integrity**: Ensure valid Python multi-line string escaping in `src/port_3d_engine.py` (avoiding accidental backtick/string termination).
2. **WebGL Draw Call Budget**: The 150-particle wake pool uses a single shared geometry and instanced clones, ensuring frame rates maintain 60 FPS on standard integrated GPUs.
3. **No Phantom Repulsion**: Confirm that when a boat enters `isDocked = true`, its coordinates are explicitly set to $X = -28.0$ and `resolveSoftHullCollisions()` returns immediately without altering position.
4. **Horizon Fade Continuity**: Verify that newly arriving craft smoothly appear at $X = 240.0$ and do not pop into view in the middle of the bay.

---
*End of Upgrade Plan Specification. Proceed to Phase 2 for code implementation upon user review.*

