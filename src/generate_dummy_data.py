# src/generate_dummy_data.py

import csv
import random
import os


def generate_arrivals(num_days=30, output_file="data/dummy/arrivals.csv"):
    """
    Generates dummy boat arrival data.
    
    Pattern:
    - Weekdays: moderate arrivals
    - Weekends: more arrivals (fishing boats return)
    - Peak season days: many arrivals
    - Off-peak: few arrivals
    
    Each row: arrival_time_hours, boat_type, boat_size
    """
    rows = []
    current_time = 0.0  # in hours
    
    # Simulate 30 days
    for day in range(num_days):
        # Determine if this is a peak day
        is_weekend = (day % 7) in [5, 6]
        is_peak_season = day < 10  # First 10 days are "peak season"
        
        if is_peak_season and is_weekend:
            num_arrivals = random.randint(12, 18)  # Very busy
        elif is_peak_season:
            num_arrivals = random.randint(8, 12)   # Busy
        elif is_weekend:
            num_arrivals = random.randint(6, 10)   # Moderate
        else:
            num_arrivals = random.randint(3, 6)    # Quiet
        
        for _ in range(num_arrivals):
            # Random arrival time within the day
            hour_of_day = random.uniform(0, 24)
            arrival_time = (day * 24) + hour_of_day
            
            # Boat type: mostly medium, some small
            if random.random() < 0.85:
                boat_type = "medium"
            else:
                boat_type = "small"
            
            # Size category
            if boat_type == "medium":
                size = random.choice(["medium", "medium", "medium", "large"])
            else:
                size = "small"
            
            rows.append({
                "arrival_time_hours": round(arrival_time, 2),
                "boat_type": boat_type,
                "boat_size": size,
                "day": day + 1,
            })
    
    # Sort by arrival time
    rows.sort(key=lambda r: r["arrival_time_hours"])
    
    # Ensure the folder exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write to CSV
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["arrival_time_hours", "boat_type", "boat_size", "day"])
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Generated {len(rows)} arrivals -> {output_file}")
    return rows


def generate_service_times(output_file="data/dummy/service_times.csv"):
    """
    Generates dummy service time data.
    
    Service times vary by boat size:
    - Small: 15-30 minutes (0.25-0.5 hours)
    - Medium: 30-90 minutes (0.5-1.5 hours)
    - Large: 90-180 minutes (1.5-3 hours)
    """
    rows = []
    
    for _ in range(500):
        size = random.choice(["small", "medium", "medium", "medium", "large"])
        
        if size == "small":
            service_time_min = round(random.uniform(0.25, 0.5), 2)
        elif size == "medium":
            service_time_min = round(random.uniform(0.5, 1.5), 2)
        else:  # large
            service_time_min = round(random.uniform(1.5, 3.0), 2)
        
        rows.append({
            "boat_size": size,
            "service_time_hours": service_time_min,
        })
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["boat_size", "service_time_hours"])
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Generated {len(rows)} service time samples -> {output_file}")
    return rows


if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING DUMMY DATA FOR MERCEDES FISH PORT")
    print("=" * 60)
    generate_arrivals(num_days=30)
    generate_service_times()
    print("=" * 60)
    print("DONE")
    print("=" * 60)