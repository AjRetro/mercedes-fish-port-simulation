# src/replications.py

import simpy
import random
from src.resources import Port
from src.stats import StatsCollector
from src.model import medium_boat_process, boat_arrival_generator


def run_single_replication(sim_time, num_berths, num_small_boats, arrival_rate, unload_time_mean, seed):
    """
    Runs ONE replication of the simulation with a specific random seed.
    Returns a StatsCollector with the results.
    """
    # Set the random seed for this replication
    random.seed(seed)
    
    # Create fresh environment, port, and stats for this run
    env = simpy.Environment()
    port = Port(env, num_berths=num_berths, num_small_boats=num_small_boats)
    stats = StatsCollector()
    
    # Run the simulation
    env.process(boat_arrival_generator(env, port, arrival_rate, unload_time_mean, stats, quiet=True))
    env.run(until=sim_time)
    
    return stats


def run_replications(num_replications, sim_time, num_berths, num_small_boats, arrival_rate, unload_time_mean):
    """
    Runs multiple replications and aggregates the results.
    """
    print("=" * 60)
    print(f"RUNNING {num_replications} REPLICATIONS")
    print("=" * 60)
    print()
    
    # Store results from each replication
    all_avg_waits = []
    all_max_waits = []
    all_avg_totals = []
    all_completed = []
    
    # Run each replication with a different seed
    for i in range(num_replications):
        seed = 1000 + i  # Seeds: 1000, 1001, 1002, ...
        stats = run_single_replication(
            sim_time, num_berths, num_small_boats, arrival_rate, unload_time_mean, seed
        )
        
        # Compute averages for this replication
        if stats.wait_times:
            avg_wait = sum(stats.wait_times) / len(stats.wait_times)
            max_wait = max(stats.wait_times)
            avg_total = sum(stats.total_times) / len(stats.total_times)
            
            all_avg_waits.append(avg_wait)
            all_max_waits.append(max_wait)
            all_avg_totals.append(avg_total)
            all_completed.append(stats.boats_completed)
            
            print(f"Replication {i+1:2d} (seed={seed}): "
                  f"avg wait = {avg_wait:6.2f}, "
                  f"max wait = {max_wait:6.2f}, "
                  f"avg total = {avg_total:6.2f}, "
                  f"completed = {stats.boats_completed}")
    
    print()
    print("=" * 60)
    print("AGGREGATED RESULTS (ACROSS ALL REPLICATIONS)")
    print("=" * 60)
    
    # Compute averages across replications
    grand_avg_wait = sum(all_avg_waits) / len(all_avg_waits)
    grand_avg_max_wait = sum(all_max_waits) / len(all_max_waits)
    grand_avg_total = sum(all_avg_totals) / len(all_avg_totals)
    grand_avg_completed = sum(all_completed) / len(all_completed)
    
    print(f"Average of avg wait times:    {grand_avg_wait:.2f} time units")
    print(f"Average of max wait times:    {grand_avg_max_wait:.2f} time units")
    print(f"Average of avg total times:   {grand_avg_total:.2f} time units")
    print(f"Average boats completed:      {grand_avg_completed:.1f}")
    print()
    
    # Show variability (min and max across replications)
    print("Variability across replications:")
    print(f"  Avg wait range: {min(all_avg_waits):.2f} to {max(all_avg_waits):.2f}")
    print(f"  Max wait range: {min(all_max_waits):.2f} to {max(all_max_waits):.2f}")
    print(f"  Completed range: {min(all_completed)} to {max(all_completed)}")
    print("=" * 60)
    
    return {
        "avg_wait": grand_avg_wait,
        "avg_max_wait": grand_avg_max_wait,
        "avg_total": grand_avg_total,
        "avg_completed": grand_avg_completed,
        "all_avg_waits": all_avg_waits,
        "all_max_waits": all_max_waits,
    }