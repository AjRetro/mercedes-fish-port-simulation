# src/cost_benefit.py
"""
Maritime Economic Evaluation & Post-Harvest Spoilage Loss Engine for Mercedes Fish Port.
Evaluates:
1. Fish quality deterioration & price depreciation (Banyera crate value loss over delay)
2. Vessel auxiliary engine diesel consumption while idling in outer anchorage
3. Crushed ice melting replenishment penalties
4. Capital and operational expenditures (CAPEX / OPEX) in Philippine Pesos (PHP)
5. Net Economic Benefit, Benefit-Cost Ratio (BCR), and Investment Payback Period
"""

from typing import Dict, List, Tuple, Any


# ============================================================
# REAL-WORLD MARITIME & POST-HARVEST ECONOMIC PARAMETERS (PHP)
# Calibrated for Mercedes, Camarines Norte (San Miguel Bay)
# ============================================================

# Fish Cargo Valuation
PRICE_PER_BANYERA_GRADE_A = 2500.0        # Premium price per tub (approx 35-40kg fresh catch)
AMBIENT_SPOILAGE_RATE_PER_HR = 0.035      # Quality decay coefficient at tropical temp (30°C)
ICE_MELT_COST_PER_VESSEL_HR = 150.0       # Crushed ice loss/melting penalty per hour of delay
IDLE_DIESEL_BURN_PER_HR = 350.0           # Aux generator / engine idling burn at anchorage (5L/hr @ ₱70/L)

# Infrastructure & Fleet Costs (Weekly Basis)
WEEKLY_COST_PER_SMALL_BANCA = 4500.0      # Fuel, crew wage share, banca maintenance
WEEKLY_COST_PER_WHARF_BERTH = 12500.0     # Wharf pontoon maintenance and harbor staff
WEEKLY_COST_SCHEDULING_SYSTEM = 2000.0    # Administrative slot dispatching & radio communications

# One-time Investments (Amortized to weekly cost)
AMORTIZATION_WEEKS_CAPEX = 156            # 3-Year amortization horizon (3 * 52 weeks)
CAPEX_CHANNEL_DREDGING = 1500000.0        # Capital dredging of river bar mouth for deep passage
CAPEX_BERTH_EXPANSION = 600000.0          # Additional landing pontoon installation
CAPEX_BANCA_MODIFICATION = 45000.0        # High-capacity insulated fish holds per banca


def calculate_vessel_economic_loss(cargo_units: int, delay_hours: float) -> Dict[str, float]:
    """
    Computes economic loss incurred by a single fishing vessel during port delay:
    1. Post-harvest fish quality degradation (spoilage loss)
    2. Crushed ice melting cost
    3. Idling engine diesel fuel cost
    """
    if delay_hours <= 0:
        return {"spoilage_loss": 0.0, "ice_loss": 0.0, "fuel_loss": 0.0, "total_vessel_loss": 0.0}

    gross_cargo_value = cargo_units * PRICE_PER_BANYERA_GRADE_A
    # Exponential quality discount curve: V(t) = V0 * (1 - e^(-k * t))
    spoilage_loss = gross_cargo_value * (1.0 - (2.718281828 ** (-AMBIENT_SPOILAGE_RATE_PER_HR * delay_hours)))
    ice_loss = delay_hours * ICE_MELT_COST_PER_VESSEL_HR
    fuel_loss = delay_hours * IDLE_DIESEL_BURN_PER_HR
    
    total = spoilage_loss + ice_loss + fuel_loss
    return {
        "spoilage_loss": round(spoilage_loss, 2),
        "ice_loss": round(ice_loss, 2),
        "fuel_loss": round(fuel_loss, 2),
        "total_vessel_loss": round(total, 2)
    }


def estimate_scenario_incremental_cost(scenario_params: Dict[str, Any],
                                      baseline_params: Dict[str, Any]) -> Tuple[float, List[str]]:
    """
    Computes the weekly operational & amortized capital expenditure of an intervention.
    Returns (total_weekly_cost, breakdown_list).
    """
    total_weekly_cost = 0.0
    breakdown = []

    # 1. Additional Shuttle Bancas
    delta_bancas = scenario_params.get("num_small_boats", 10) - baseline_params.get("num_small_boats", 10)
    if delta_bancas > 0:
        weekly_banca_cost = delta_bancas * WEEKLY_COST_PER_SMALL_BANCA
        total_weekly_cost += weekly_banca_cost
        breakdown.append(f"+{delta_bancas} Shuttle Bancas: PHP {weekly_banca_cost:,.0f}/wk")

    # 2. Additional Wharf Berths / Pontoons
    delta_berths = scenario_params.get("num_berths", 3) - baseline_params.get("num_berths", 3)
    if delta_berths > 0:
        capex_amortized = (delta_berths * CAPEX_BERTH_EXPANSION) / AMORTIZATION_WEEKS_CAPEX
        opex_berths = delta_berths * WEEKLY_COST_PER_WHARF_BERTH
        combined_berth = capex_amortized + opex_berths
        total_weekly_cost += combined_berth
        breakdown.append(f"+{delta_berths} Wharf Berths (Amortized + Ops): PHP {combined_berth:,.0f}/wk")

    # 3. Channel Dredging (Enabling faster travel & higher direct docking)
    dredged = scenario_params.get("dredged_channel", False) or (scenario_params.get("direct_dock_probability", 0.15) > 0.35)
    if dredged and not baseline_params.get("dredged_channel", False):
        weekly_dredge = CAPEX_CHANNEL_DREDGING / AMORTIZATION_WEEKS_CAPEX
        total_weekly_cost += weekly_dredge
        breakdown.append(f"Channel Dredging (Amortized 3-yr): PHP {weekly_dredge:,.0f}/wk")

    # 4. Scheduling / Priority Appointment System
    scheduling_enabled = scenario_params.get("scheduling_priority", False)
    if scheduling_enabled and not baseline_params.get("scheduling_priority", False):
        total_weekly_cost += WEEKLY_COST_SCHEDULING_SYSTEM
        breakdown.append(f"Port Slot Scheduling System: PHP {WEEKLY_COST_SCHEDULING_SYSTEM:,.0f}/wk")

    # 5. Banca Capacity Upgrade
    delta_cap = scenario_params.get("small_boat_capacity", 20) - baseline_params.get("small_boat_capacity", 20)
    if delta_cap > 0:
        fleet = scenario_params.get("num_small_boats", 10)
        weekly_mod = (fleet * CAPEX_BANCA_MODIFICATION) / AMORTIZATION_WEEKS_CAPEX
        total_weekly_cost += weekly_mod
        breakdown.append(f"Banca Hold Insulated Upgrade: PHP {weekly_mod:,.0f}/wk")

    if not breakdown:
        breakdown.append("Baseline Operations (No added investment)")

    return round(total_weekly_cost, 2), breakdown


def analyze_scenarios(baseline_result: Dict[str, Any], baseline_params: Dict[str, Any],
                      scenario_results: List[Dict[str, Any]],
                      scenario_params_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Executes a comprehensive cost-benefit analysis across all simulated policy scenarios.
    """
    analysis = []
    baseline_loss = baseline_result.get("total_economic_penalty_php", 0.0)

    for res, params in zip(scenario_results, scenario_params_list):
        scenario_name = res.get("name", "Unknown Scenario")
        scenario_loss = res.get("total_economic_penalty_php", 0.0)
        
        # Economic savings from reduced delay & spoilage
        gross_weekly_savings = max(0.0, baseline_loss - scenario_loss)
        
        # Implementation cost
        weekly_cost, breakdown = estimate_scenario_incremental_cost(params, baseline_params)
        
        # Net Benefit & Benefit-Cost Ratio
        net_weekly_benefit = gross_weekly_savings - weekly_cost
        bcr = (gross_weekly_savings / weekly_cost) if weekly_cost > 0 else (1.0 if gross_weekly_savings == 0 else 99.9)
        
        # Payback period in months
        payback_months = (weekly_cost * 4.33 / gross_weekly_savings * 12) if gross_weekly_savings > weekly_cost else 0.0
        
        analysis.append({
            "name": scenario_name,
            "avg_wait_hours": res.get("avg_wait", 0.0),
            "avg_turnaround_hours": res.get("avg_total", 0.0),
            "weekly_delay_loss_php": scenario_loss,
            "gross_weekly_savings_php": gross_weekly_savings,
            "incremental_weekly_cost_php": weekly_cost,
            "net_weekly_benefit_php": net_weekly_benefit,
            "benefit_cost_ratio": round(bcr, 2),
            "cost_breakdown": breakdown,
            "is_economically_viable": net_weekly_benefit > 0
        })

    return analysis


def print_cost_benefit_table(analysis: List[Dict[str, Any]]):
    """Prints formatted cost-benefit matrix to the terminal."""
    print()
    print("=" * 115)
    print(f"{'COST-BENEFIT & POST-HARVEST ECONOMIC ANALYSIS (MERCEDES FISH PORT)':^115}")
    print("=" * 115)
    print(f"{'Scenario Name':<30} {'Avg Wait':>10} {'Turnaround':>12} {'Gross Savings':>16} {'Added Cost':>14} {'Net Benefit':>15} {'BCR':>8}")
    print("-" * 115)
    
    for row in analysis:
        print(f"{row['name']:<30} "
              f"{row['avg_wait_hours']:>9.2f}h "
              f"{row['avg_turnaround_hours']:>11.2f}h "
              f"PHP {row['gross_weekly_savings_php']:>12,.0f} "
              f"PHP {row['incremental_weekly_cost_php']:>10,.0f} "
              f"PHP {row['net_weekly_benefit_php']:>11,.0f} "
              f"{row['benefit_cost_ratio']:>8.2f}")
              
    print("=" * 115)
