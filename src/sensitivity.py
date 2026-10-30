# src/sensitivity.py

import simpy
import random
from src.resources import Port
from src.stats import StatsCollector
from src.model import boat_arrival_generator


def run_one_point(param_name, param_value, base_params, num_replications=5, sim_time=168):
    """
    Run the simulation at ONE value of ONE parameter.
    Returns averaged KPIs.
    """
    avg_waits = []
    avg_totals = []
    completed = []
    
    for i in range(num_replications):
        random.seed(4000 + i)
        
        # Copy base params and override the parameter we're testing
        params = base_params.copy()
        params[param_name] = param_value
        
        env = simpy.Environment()
        port = Port(env, num_berths=params["num_berths"], num_small_boats=params["num_small_boats"])
        stats = StatsCollector()
        
        env.process(boat_arrival_generator(
            env, port,
            params["arrival_rate"],
            params["unload_time_mean"],
            params["small_boat_capacity"],
            params["load_time"],
            params["travel_time"],
            params["unload_time"],
            params["direct_dock_probability"],
            stats, quiet=True
        ))
        
        env.run(until=sim_time)
        
        if stats.wait_times:
            avg_waits.append(sum(stats.wait_times) / len(stats.wait_times))
            avg_totals.append(sum(stats.total_times) / len(stats.total_times))
            completed.append(stats.boats_completed)
    
    return {
        "value": param_value,
        "avg_wait": sum(avg_waits) / len(avg_waits) if avg_waits else 0,
        "avg_total": sum(avg_totals) / len(avg_totals) if avg_totals else 0,
        "completed": sum(completed) / len(completed) if completed else 0,
    }


def analyze_parameter(param_name, values, base_params, num_replications=5, sim_time=168):
    """
    Run sensitivity analysis over a range of values for one parameter.
    Returns list of results.
    """
    print(f"\n=== Sensitivity analysis: {param_name} ===")
    print(f"Testing values: {values}")
    
    results = []
    for v in values:
        r = run_one_point(param_name, v, base_params, num_replications, sim_time)
        results.append(r)
        print(f"  {param_name} = {v:>6}: avg wait = {r['avg_wait']:>7.2f}, "
              f"avg total = {r['avg_total']:>7.2f}, completed = {r['completed']:>5.1f}")
    
    return results


def print_sensitivity_table(param_name, results):
    """Print a nice table."""
    print()
    print("=" * 80)
    print(f"SENSITIVITY ANALYSIS: {param_name.upper()}")
    print("=" * 80)
    print(f"{param_name:>10} {'Avg Wait':>15} {'Avg Total':>15} {'Completed':>15}")
    print("-" * 80)
    
    for r in results:
        print(f"{r['value']:>10.2f} "
              f"{r['avg_wait']:>15.2f} "
              f"{r['avg_total']:>15.2f} "
              f"{r['completed']:>15.1f}")
    
    print("=" * 80)


def run_all_sensitivity(base_params=None, num_replications=5, sim_time=168):
    """
    Run sensitivity analysis for the most important parameters.
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
        }
    
    all_results = {}
    
    # 1. Arrival rate (most important - shows when port breaks)
    values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0]
    all_results["arrival_rate"] = analyze_parameter(
        "arrival_rate", values, base_params, num_replications, sim_time
    )
    
    # 2. Number of small boats (shows diminishing returns)
    values = [2, 4, 6, 8, 10, 15, 20]
    all_results["num_small_boats"] = analyze_parameter(
        "num_small_boats", values, base_params, num_replications, sim_time
    )
    
    # 3. Travel time (shows impact of shuttle speed)
    values = [0.2, 0.3, 0.4, 0.5, 0.7, 1.0, 1.5]
    all_results["travel_time"] = analyze_parameter(
        "travel_time", values, base_params, num_replications, sim_time
    )
    
    return all_results