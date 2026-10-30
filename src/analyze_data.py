# src/analyze_data.py

import csv


def load_arrivals(filepath="data/dummy/arrivals.csv"):
    """Load arrival data from CSV."""
    arrivals = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            arrivals.append({
                "arrival_time_hours": float(row["arrival_time_hours"]),
                "boat_type": row["boat_type"],
                "boat_size": row["boat_size"],
                "day": int(row["day"]),
            })
    return arrivals


def load_service_times(filepath="data/dummy/service_times.csv"):
    """Load service time data from CSV."""
    service_times = []
    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            service_times.append({
                "boat_size": row["boat_size"],
                "service_time_hours": float(row["service_time_hours"]),
            })
    return service_times


def analyze_arrivals(arrivals):
    """Analyze arrival patterns."""
    print("=" * 60)
    print("ARRIVAL DATA ANALYSIS")
    print("=" * 60)
    
    total = len(arrivals)
    print(f"Total arrivals: {total}")
    
    # Total time span
    first_time = min(a["arrival_time_hours"] for a in arrivals)
    last_time = max(a["arrival_time_hours"] for a in arrivals)
    time_span = last_time - first_time
    print(f"Time span: {time_span:.1f} hours ({time_span / 24:.1f} days)")
    
    # Arrival rate
    arrival_rate = total / time_span
    print(f"Average arrival rate: {arrival_rate:.4f} boats per hour")
    print(f"                    = {arrival_rate * 24:.2f} boats per day")
    
    # Boat type breakdown
    medium_count = sum(1 for a in arrivals if a["boat_type"] == "medium")
    small_count = sum(1 for a in arrivals if a["boat_type"] == "small")
    print(f"\nBoat type breakdown:")
    print(f"  Medium: {medium_count} ({100*medium_count/total:.1f}%)")
    print(f"  Small:  {small_count} ({100*small_count/total:.1f}%)")
    
    # Compute interarrival times
    sorted_arrivals = sorted(arrivals, key=lambda a: a["arrival_time_hours"])
    interarrival_times = []
    for i in range(1, len(sorted_arrivals)):
        gap = sorted_arrivals[i]["arrival_time_hours"] - sorted_arrivals[i-1]["arrival_time_hours"]
        interarrival_times.append(gap)
    
    avg_interarrival = sum(interarrival_times) / len(interarrival_times)
    print(f"\nInterarrival time statistics:")
    print(f"  Average: {avg_interarrival:.3f} hours")
    print(f"  Min:     {min(interarrival_times):.3f} hours")
    print(f"  Max:     {max(interarrival_times):.3f} hours")
    
    print("=" * 60)
    
    return {
        "arrival_rate": arrival_rate,
        "avg_interarrival": avg_interarrival,
        "total": total,
    }


def analyze_service_times(service_times):
    """Analyze service time patterns."""
    print()
    print("=" * 60)
    print("SERVICE TIME DATA ANALYSIS")
    print("=" * 60)
    
    # Group by boat size
    for size in ["small", "medium", "large"]:
        times = [s["service_time_hours"] for s in service_times if s["boat_size"] == size]
        if times:
            avg = sum(times) / len(times)
            print(f"{size.upper():8s}: count={len(times):3d}, avg={avg:.3f} hrs ({avg*60:.1f} min)")
    
    print("=" * 60)
    
    # Overall
    all_times = [s["service_time_hours"] for s in service_times]
    overall_avg = sum(all_times) / len(all_times)
    
    return {
        "overall_avg": overall_avg,
        "count": len(all_times),
    }


if __name__ == "__main__":
    arrivals = load_arrivals()
    service_times = load_service_times()
    
    arrival_stats = analyze_arrivals(arrivals)
    service_stats = analyze_service_times(service_times)
    
    print()
    print("=" * 60)
    print("SUMMARY FOR SIMULATION PARAMETERS")
    print("=" * 60)
    print(f"Arrival rate:       {arrival_stats['arrival_rate']:.4f} boats/hour")
    print(f"Mean service time:  {service_stats['overall_avg']:.3f} hours")
    print("=" * 60)