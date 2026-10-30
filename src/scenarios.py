# src/scenarios.py
"""
Scenario Execution Engine for Mercedes Fish Port Simulation.
Defines and simulates 5 comparative policy interventions (Objectives #11, #12, #13, #14)
using Common Random Numbers (CRN) and Student's t 95% Confidence Intervals.
"""

from typing import Dict, List, Any
from src.model import run_simulation
from src.stats import compute_confidence_interval


def get_default_scenario_definitions(base_params: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Returns the 5 structured research intervention scenarios.
    """
    scenarios = []

    # 0. Baseline Operations (Current State)
    s0 = base_params.copy()
    s0["scenario_id"] = "s0"
    s0["name"] = "Baseline (As-Is)"
    s0["description"] = "3 berths, 10 bancas, serial lightering (1 banca/boat), 15% direct dock."
    scenarios.append(s0)

    # 1. Operational Scheduling & Coordinated Dispatching (Low-Cost / Zero-CAPEX)
    s1 = base_params.copy()
    s1["scenario_id"] = "s1"
    s1["name"] = "Operational Scheduling"
    s1["description"] = "Staggered peak appointments, buoy-marked channel navigation (travel 0.35h), priority queueing."
    s1["travel_time"] = 0.35
    s1["scheduling_priority"] = True
    scenarios.append(s1)

    # 2. Dynamic Parallel Lightering (Fleet Sizing)
    s2 = base_params.copy()
    s2["scenario_id"] = "s2"
    s2["name"] = "Parallel Lightering"
    s2["description"] = "Fleet expanded to 16 bancas, parallel gang dispatch (up to 3 bancas/mother boat), capacity 25."
    s2["num_small_boats"] = 16
    s2["max_parallel_bancas"] = 3
    s2["small_boat_capacity"] = 25
    scenarios.append(s2)

    # 3. Channel Dredging & Direct Deep Berthing (Infrastructure CAPEX)
    s3 = base_params.copy()
    s3["scenario_id"] = "s3"
    s3["name"] = "Channel Dredging"
    s3["description"] = "Dredged river mouth: direct docking increases to 50%, travel time reduced to 0.25h, channel cap 5."
    s3["direct_dock_probability"] = 0.50
    s3["travel_time"] = 0.25
    s3["channel_capacity"] = 5
    s3["dredged_channel"] = True
    scenarios.append(s3)

    # 4. Integrated Master Modernization Strategy (Combined Interventions)
    s4 = base_params.copy()
    s4["scenario_id"] = "s4"
    s4["name"] = "Integrated Master Strategy"
    s4["description"] = "Dredged channel + 5 wharf berths (+2 pontoons) + 16 bancas with parallel lightering + scheduling."
    s4["num_berths"] = 5
    s4["num_small_boats"] = 16
    s4["max_parallel_bancas"] = 3
    s4["small_boat_capacity"] = 25
    s4["direct_dock_probability"] = 0.50
    s4["travel_time"] = 0.25
    s4["channel_capacity"] = 5
    s4["dredged_channel"] = True
    s4["scheduling_priority"] = True
    scenarios.append(s4)

    return scenarios


def run_scenario(scenario_name: str, params: Dict[str, Any], num_replications: int = 5,
                 sim_time: float = 168.0, base_seed: int = 20261000) -> Dict[str, Any]:
    """
    Executes multiple independent replications of a scenario using Common Random Numbers (CRN).
    Aggregates point estimates and 95% Confidence Intervals.
    """
    rep_avg_waits = []
    rep_max_waits = []
    rep_avg_totals = []
    rep_avg_services = []
    rep_completed = []
    rep_berth_util = []
    rep_banca_util = []
    rep_channel_util = []
    rep_spoilage = []
    rep_fuel = []
    all_raw_waits = []
    all_raw_services = []

    for i in range(num_replications):
        seed = base_seed + (i * 104729)  # Prime stride for stream independence
        stats = run_simulation(
            sim_time=sim_time,
            num_berths=params.get("num_berths", 3),
            num_small_boats=params.get("num_small_boats", 10),
            arrival_rate=params.get("arrival_rate", 0.34),
            unload_time_mean=params.get("unload_time_mean", 1.0),
            small_boat_capacity=params.get("small_boat_capacity", 20),
            load_time=params.get("load_time", 0.3),
            travel_time=params.get("travel_time", 0.5),
            unload_time=params.get("unload_time", 0.4),
            direct_dock_probability=params.get("direct_dock_probability", 0.15),
            channel_capacity=params.get("channel_capacity", 3),
            max_parallel_bancas=params.get("max_parallel_bancas", 1),
            seed=seed,
            quiet=True
        )
        
        kpi = stats.compute_summary_kpis()
        rep_avg_waits.append(kpi["avg_wait_time"])
        rep_max_waits.append(kpi["max_wait_time"])
        rep_avg_totals.append(kpi["avg_total_time"])
        rep_avg_services.append(kpi["avg_service_time"])
        rep_completed.append(kpi["boats_completed"])
        rep_berth_util.append(kpi["berth_utilization"])
        rep_banca_util.append(kpi["banca_utilization"])
        rep_channel_util.append(kpi["channel_utilization"])
        rep_spoilage.append(kpi["total_spoilage_loss_php"])
        rep_fuel.append(kpi["total_fuel_idle_php"])
        all_raw_waits.extend(stats.wait_times)
        all_raw_services.extend(stats.service_times)

    ci_wait = compute_confidence_interval(rep_avg_waits)
    ci_total = compute_confidence_interval(rep_avg_totals)
    ci_service = compute_confidence_interval(rep_avg_services)

    return {
        "name": scenario_name,
        "description": params.get("description", ""),
        "replications": num_replications,
        "sim_time": sim_time,
        "avg_wait": ci_wait["mean"],
        "ci_wait_half_width": ci_wait["ci_half_width"],
        "ci_wait_lower": ci_wait["ci_lower"],
        "ci_wait_upper": ci_wait["ci_upper"],
        "avg_max_wait": sum(rep_max_waits) / num_replications if rep_max_waits else 0.0,
        "avg_service": ci_service["mean"],
        "avg_total": ci_total["mean"],
        "ci_total_half_width": ci_total["ci_half_width"],
        "avg_completed": sum(rep_completed) / num_replications if rep_completed else 0.0,
        "berth_utilization": sum(rep_berth_util) / num_replications if rep_berth_util else 0.0,
        "banca_utilization": sum(rep_banca_util) / num_replications if rep_banca_util else 0.0,
        "channel_utilization": sum(rep_channel_util) / num_replications if rep_channel_util else 0.0,
        "total_spoilage_loss_php": sum(rep_spoilage) / num_replications if rep_spoilage else 0.0,
        "total_fuel_idle_php": sum(rep_fuel) / num_replications if rep_fuel else 0.0,
        "total_economic_penalty_php": (sum(rep_spoilage) + sum(rep_fuel)) / num_replications if rep_spoilage else 0.0,
        "raw_waits": all_raw_waits,
        "raw_services": all_raw_services,
    }


def run_all_scenarios_for_ui(base_params: Dict[str, Any] = None, num_replications: int = 5,
                             sim_time: float = 168.0) -> List[Dict[str, Any]]:
    """
    Executes the entire 5-scenario evaluation suite.
    """
    if base_params is None:
        base_params = {
            "num_berths": 3,
            "num_small_boats": 10,
            "arrival_rate": 0.34,
            "unload_time_mean": 1.0,
            "small_boat_capacity": 20,
            "load_time": 0.3,
            "travel_time": 0.5,
            "unload_time": 0.4,
            "direct_dock_probability": 0.15,
            "channel_capacity": 3,
            "max_parallel_bancas": 1
        }
        
    scenario_defs = get_default_scenario_definitions(base_params)
    results = []
    
    for s_def in scenario_defs:
        res = run_scenario(
            scenario_name=s_def["name"],
            params=s_def,
            num_replications=num_replications,
            sim_time=sim_time
        )
        results.append(res)
        
    return results


def print_comparison_table(results: List[Dict[str, Any]]):
    """Outputs high-precision academic comparison matrix to terminal."""
    print()
    print("=" * 110)
    print(f"{'SCENARIO PERFORMANCE COMPARISON & 95% CONFIDENCE INTERVALS':^110}")
    print("=" * 110)
    print(f"{'Scenario Name':<28} {'Avg Wait (h)':>18} {'Turnaround (h)':>16} {'Completed':>12} {'Berth %':>10} {'Banca %':>10} {'Chan %':>10}")
    print("-" * 110)
    
    for r in results:
        wait_str = f"{r['avg_wait']:.2f} +/- {r['ci_wait_half_width']:.2f}"
        print(f"{r['name']:<28} "
              f"{wait_str:>18} "
              f"{r['avg_total']:>16.2f} "
              f"{r['avg_completed']:>12.1f} "
              f"{r['berth_utilization']*100:>9.1f}% "
              f"{r['banca_utilization']*100:>9.1f}% "
              f"{r['channel_utilization']*100:>9.1f}%")
              
    print("=" * 110)
    
    baseline = results[0]
    print()
    print(f"{'PERCENTAGE IMPROVEMENT VS BASELINE':^110}")
    print("-" * 110)
    print(f"{'Scenario Name':<28} {'Wait Reduction':>22} {'Turnaround Reduction':>25} {'Throughput Gain':>22}")
    print("-" * 110)
    
    for r in results[1:]:
        wait_red = ((baseline["avg_wait"] - r["avg_wait"]) / max(baseline["avg_wait"], 1e-4)) * 100
        total_red = ((baseline["avg_total"] - r["avg_total"]) / max(baseline["avg_total"], 1e-4)) * 100
        thru_gain = ((r["avg_completed"] - baseline["avg_completed"]) / max(baseline["avg_completed"], 1e-4)) * 100
        print(f"{r['name']:<28} "
              f"{wait_red:>21.1f}% "
              f"{total_red:>24.1f}% "
              f"{thru_gain:>21.1f}%")
    print("=" * 110)
