# src/data_loader.py
"""
Field Data Ingestion & Empirical Parameter Calibration Engine.
Processes maritime observation logs (Sheet A) collected at Mercedes Fish Port.
Supports CSV file paths, uploaded file buffers, and pandas DataFrames.
"""

import csv
import json
import os
import re
from typing import Dict, List, Any, Union
import pandas as pd


def parse_time_to_hours(val: Any) -> float:
    """
    Robustly convert diverse time representations to decimal hours of the day (float).
    Examples:
      '06:30'    -> 6.5
      '6:30 AM'  -> 6.5
      '02:15 PM' -> 14.25
      '14:20:00' -> 14.333
      6.75       -> 6.75
    """
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)

    time_str = str(val).strip()
    # Extract AM/PM if present
    is_pm = "PM" in time_str.upper()
    is_am = "AM" in time_str.upper()
    cleaned = re.sub(r"[^\d:]", "", time_str)
    
    parts = cleaned.split(":")
    if not parts or not parts[0]:
        return 0.0
        
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    seconds = int(parts[2]) if len(parts) > 2 and parts[2] else 0
    
    if is_pm and hours < 12:
        hours += 12
    elif is_am and hours == 12:
        hours = 0
        
    return hours + (minutes / 60.0) + (seconds / 3600.0)


def load_field_observations(filepath: str = "data/raw/field_observations.csv") -> List[Dict[str, Any]]:
    """
    Reads the field observation CSV (Sheet A).
    Returns a list of dicts with standardized computed fields.
    """
    rows = []
    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Handle varied column naming conventions
            arrival_str = row.get("arrival_time") or row.get("Arrival Time") or row.get("arrival") or "06:00"
            svc_start_str = row.get("service_start") or row.get("Service Start") or row.get("docking_time") or arrival_str
            svc_end_str = row.get("service_end") or row.get("Service End") or row.get("departure_time") or svc_start_str
            dep_str = row.get("departure_time") or row.get("Departure Time") or svc_end_str
            wait_flag = row.get("wait_flag") or row.get("Wait Flag") or row.get("waited") or "N"
            b_type = (row.get("boat_type") or row.get("Boat Type") or row.get("type") or "medium").strip().lower()
            b_id = row.get("boat_id") or row.get("Boat ID") or f"B{len(rows)+1}"

            arrival = parse_time_to_hours(arrival_str)
            svc_start = parse_time_to_hours(svc_start_str)
            svc_end = parse_time_to_hours(svc_end_str)
            departure = parse_time_to_hours(dep_str)
            
            wait_time = max(0.0, svc_start - arrival)
            svc_time = max(0.0, svc_end - svc_start)
            total_time = max(0.0, departure - arrival)

            rows.append({
                "boat_id": b_id,
                "boat_type": b_type,
                "arrival_time": arrival,
                "service_start": svc_start,
                "service_end": svc_end,
                "departure_time": departure,
                "wait_time": wait_time,
                "service_time": svc_time,
                "total_time": total_time,
                "waited": str(wait_flag).strip().upper() in ["Y", "YES", "TRUE", "1"],
            })
    return rows


def compute_parameters(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compute simulation parameters from the observation data records.
    Returns a dict with empirical distributions ready for DES calibration.
    """
    if not rows:
        raise ValueError("No observations to compute parameters from.")
    
    rows_sorted = sorted(rows, key=lambda r: r["arrival_time"])
    total_boats = len(rows)
    first_arrival = rows_sorted[0]["arrival_time"]
    last_arrival = rows_sorted[-1]["arrival_time"]
    span_hours = last_arrival - first_arrival
    if span_hours <= 0:
        span_hours = 1.0  # avoid division by zero
    
    # Empirical arrival rate lambda
    arrival_rate = total_boats / span_hours
    
    # Service times (in hours)
    service_times = [r["service_time"] for r in rows if r["service_time"] > 0]
    avg_service_time = sum(service_times) / len(service_times) if service_times else 1.0
    
    # Wait times
    wait_times = [r["wait_time"] for r in rows]
    avg_wait = sum(wait_times) / len(wait_times) if wait_times else 0.0
    
    # Boat type breakdown
    type_counts = {}
    for r in rows:
        t = r["boat_type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    
    # Ratio of direct-docking vs lightered boats
    direct_docked = sum(1 for r in rows if not r["waited"])
    direct_dock_prob = direct_docked / total_boats if total_boats else 0.15
    
    params = {
        "source": "empirical_observations",
        "total_boats": total_boats,
        "span_hours": round(span_hours, 2),
        "arrival_rate": round(arrival_rate, 4),
        "avg_service_time_hours": round(avg_service_time, 3),
        "avg_wait_time_hours": round(avg_wait, 3),
        "direct_dock_probability": round(direct_dock_prob, 3),
        "boat_type_breakdown": type_counts,
    }
    return params


def compute_parameters_from_df(df: pd.DataFrame) -> Dict[str, Any]:
    """Processes a pandas DataFrame directly (e.g. from Streamlit file upload)."""
    rows = []
    col_map = {col.lower().replace(" ", "_"): col for col in df.columns}
    
    for idx, r in df.iterrows():
        arrival_val = r[col_map.get("arrival_time", df.columns[min(2, len(df.columns)-1)])]
        svc_start_val = r[col_map.get("service_start", arrival_val)]
        svc_end_val = r[col_map.get("service_end", svc_start_val)]
        dep_val = r[col_map.get("departure_time", svc_end_val)]
        b_type = str(r.get(col_map.get("boat_type", "medium"), "medium")).strip().lower()
        b_id = str(r.get(col_map.get("boat_id", f"B{idx+1}"), f"B{idx+1}"))
        wait_flag = str(r.get(col_map.get("wait_flag", "N"), "N"))

        arr = parse_time_to_hours(arrival_val)
        start = parse_time_to_hours(svc_start_val)
        end = parse_time_to_hours(svc_end_val)
        dep = parse_time_to_hours(dep_val)
        
        rows.append({
            "boat_id": b_id,
            "boat_type": b_type,
            "arrival_time": arr,
            "service_start": start,
            "service_end": end,
            "departure_time": dep,
            "wait_time": max(0.0, start - arr),
            "service_time": max(0.0, end - start),
            "total_time": max(0.0, dep - arr),
            "waited": wait_flag.upper() in ["Y", "YES", "TRUE", "1"]
        })
    return compute_parameters(rows)


def save_parameters(params: Dict[str, Any], output_file: str = "data/processed/parameters.json"):
    """Save computed parameters to JSON for reproducibility."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(params, f, indent=2)
    return params


def print_parameters(params: Dict[str, Any]):
    """Print parameters in a human-readable format."""
    print()
    print("=" * 60)
    print("COMPUTED SIMULATION PARAMETERS")
    print("=" * 60)
    print(f"Source:                   {params['source']}")
    print(f"Total boats observed:     {params['total_boats']}")
    print(f"Observation span:         {params['span_hours']} hours")
    print(f"Arrival rate:             {params['arrival_rate']} boats/hour")
    print(f"Average service time:     {params['avg_service_time_hours']} hours")
    print(f"Average wait time:        {params['avg_wait_time_hours']} hours")
    print(f"Direct dock probability:  {params['direct_dock_probability']}")
    print(f"Boat type breakdown:      {params['boat_type_breakdown']}")
    print("=" * 60)
