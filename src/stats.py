# src/stats.py
"""
Comprehensive Statistical & Output Analysis Engine for Mercedes Fish Port Simulation.
Implements:
1. Time-weighted queue length and resource utilization integrals
2. Verification of Little's Law: L_q = lambda * W_q
3. Student's t-distribution 95% Confidence Intervals & Half-Widths
4. Direct aggregation for the 14 CNSC Research Proposal KPIs
"""

import math
from typing import Dict, List, Optional
from src.entities import MediumBoat


class StatsCollector:
    """
    Collects fine-grained event and time-series telemetry throughout a simulation run.
    """
    def __init__(self, sim_time: float = 168.0, num_berths: int = 3,
                 num_small_boats: int = 10, channel_capacity: int = 3):
        self.sim_time = sim_time
        self.num_berths = num_berths
        self.num_small_boats = num_small_boats
        self.channel_capacity = channel_capacity
        
        # Vessel outcome metrics
        self.completed_boats: List[MediumBoat] = []
        self.wait_times: List[float] = []
        self.service_times: List[float] = []
        self.total_times: List[float] = []
        self.channel_wait_times: List[float] = []
        self.spoilage_losses: List[float] = []
        self.fuel_idle_costs: List[float] = []
        
        self.boats_arrived = 0
        self.boats_completed = 0
        self.direct_dock_count = 0
        self.lightering_count = 0
        
        # Time-weighted tracking variables
        self.last_queue_update = 0.0
        self.current_queue_len = 0
        self.cumulative_queue_time = 0.0  # Integral of Q(t) dt
        
        self.last_berth_update = 0.0
        self.current_berths_busy = 0
        self.cumulative_berth_busy_time = 0.0  # Integral of B(t) dt
        
        self.last_banca_update = 0.0
        self.current_bancas_busy = 0
        self.cumulative_banca_busy_time = 0.0  # Integral of S(t) dt
        
        self.last_channel_update = 0.0
        self.current_channel_busy = 0
        self.cumulative_channel_busy_time = 0.0  # Integral of C(t) dt

    def record_boat_arrival(self):
        """Invoked when a medium boat reaches the outer roadstead."""
        self.boats_arrived += 1

    def update_anchorage_queue(self, now: float, delta: int):
        """Update time-weighted anchorage queue length integral."""
        dt = max(0.0, now - self.last_queue_update)
        self.cumulative_queue_time += self.current_queue_len * dt
        self.current_queue_len = max(0, self.current_queue_len + delta)
        self.last_queue_update = now

    def update_berth_occupancy(self, now: float, busy_count: int):
        """Update time-weighted berth utilization integral."""
        dt = max(0.0, now - self.last_berth_update)
        self.cumulative_berth_busy_time += self.current_berths_busy * dt
        self.current_berths_busy = busy_count
        self.last_berth_update = now

    def update_banca_occupancy(self, now: float, busy_count: int):
        """Update time-weighted small boat utilization integral."""
        dt = max(0.0, now - self.last_banca_update)
        self.cumulative_banca_busy_time += self.current_bancas_busy * dt
        self.current_bancas_busy = busy_count
        self.last_banca_update = now

    def update_channel_occupancy(self, now: float, busy_count: int):
        """Update time-weighted river channel utilization integral."""
        dt = max(0.0, now - self.last_channel_update)
        self.cumulative_channel_busy_time += self.current_channel_busy * dt
        self.current_channel_busy = busy_count
        self.last_channel_update = now

    def record_boat_completion(self, boat: MediumBoat):
        """Invoked upon vessel departure from the port boundary."""
        self.boats_completed += 1
        self.completed_boats.append(boat)
        self.wait_times.append(boat.wait_time_anchorage)
        self.service_times.append(boat.service_time)
        self.total_times.append(boat.total_port_time)
        self.channel_wait_times.append(boat.channel_wait_time)
        self.spoilage_losses.append(boat.spoilage_loss_php)
        self.fuel_idle_costs.append(boat.fuel_idle_loss_php)
        
        if boat.direct_dock:
            self.direct_dock_count += 1
        else:
            self.lightering_count += 1

    def finalize(self, end_time: float):
        """Ensure time-integrals run until end of simulation window."""
        self.update_anchorage_queue(end_time, 0)
        self.update_berth_occupancy(end_time, self.current_berths_busy)
        self.update_banca_occupancy(end_time, self.current_bancas_busy)
        self.update_channel_occupancy(end_time, self.current_channel_busy)

    def compute_summary_kpis(self) -> Dict[str, float]:
        """Compute point estimates for operational KPIs aligned with proposal."""
        t_span = max(self.sim_time, 1.0)
        
        avg_wait = sum(self.wait_times) / len(self.wait_times) if self.wait_times else 0.0
        max_wait = max(self.wait_times) if self.wait_times else 0.0
        avg_service = sum(self.service_times) / len(self.service_times) if self.service_times else 0.0
        avg_total = sum(self.total_times) / len(self.total_times) if self.total_times else 0.0
        
        # Time-weighted integrals
        l_q = self.cumulative_queue_time / t_span
        util_berth = self.cumulative_berth_busy_time / (self.num_berths * t_span)
        util_banca = self.cumulative_banca_busy_time / (self.num_small_boats * t_span)
        util_channel = self.cumulative_channel_busy_time / (self.channel_capacity * t_span)
        
        # Effective arrival rate and Little's Law check (L_q = lambda * W_q)
        lambda_effective = self.boats_completed / t_span
        littles_law_expected_lq = lambda_effective * avg_wait
        littles_law_error_pct = (abs(l_q - littles_law_expected_lq) / max(l_q, 1e-4)) * 100.0

        total_spoilage = sum(self.spoilage_losses)
        total_fuel_idle = sum(self.fuel_idle_costs)

        return {
            "boats_arrived": self.boats_arrived,
            "boats_completed": self.boats_completed,
            "avg_wait_time": avg_wait,
            "max_wait_time": max_wait,
            "avg_service_time": avg_service,
            "avg_total_time": avg_total,
            "time_avg_anchorage_queue": l_q,
            "berth_utilization": min(1.0, util_berth),
            "banca_utilization": min(1.0, util_banca),
            "channel_utilization": min(1.0, util_channel),
            "littles_law_error_pct": littles_law_error_pct,
            "total_spoilage_loss_php": total_spoilage,
            "total_fuel_idle_php": total_fuel_idle,
            "total_economic_penalty_php": total_spoilage + total_fuel_idle,
        }

    def summary(self) -> str:
        """Formatted terminal summary string."""
        kpis = self.compute_summary_kpis()
        lines = [
            "=" * 60,
            "MERCEDES FISH PORT - SIMULATION OUTPUT ANALYSIS",
            "=" * 60,
            f"Simulation Duration:             {self.sim_time:.1f} hours ({self.sim_time/24:.1f} days)",
            f"Boats Arrived:                   {kpis['boats_arrived']}",
            f"Boats Completed:                 {kpis['boats_completed']}",
            "-" * 60,
            f"Average Anchorage Wait:          {kpis['avg_wait_time']:.2f} hours",
            f"Maximum Anchorage Wait:          {kpis['max_wait_time']:.2f} hours",
            f"Average Service Duration:        {kpis['avg_service_time']:.2f} hours",
            f"Average Total Turnaround:        {kpis['avg_total_time']:.2f} hours",
            f"Time-Avg Anchorage Queue (L_q):  {kpis['time_avg_anchorage_queue']:.2f} vessels",
            "-" * 60,
            f"Wharf Berth Utilization:         {kpis['berth_utilization']*100:.1f}%",
            f"Shuttle Banca Utilization:       {kpis['banca_utilization']*100:.1f}%",
            f"River Channel Density/Util:      {kpis['channel_utilization']*100:.1f}%",
            f"Little's Law Consistency Error:  {kpis['littles_law_error_pct']:.2f}%",
            "-" * 60,
            f"Aggregate Catch Spoilage Loss:   PHP {kpis['total_spoilage_loss_php']:,.2f}",
            f"Aggregate Vessel Idle Fuel Burn: PHP {kpis['total_fuel_idle_php']:,.2f}",
            "=" * 60
        ]
        return "\n".join(lines)


def compute_confidence_interval(data: List[float], confidence: float = 0.95) -> Dict[str, float]:
    """
    Calculate mean, standard deviation, and Student's t 95% Confidence Interval.
    Uses exact t-distribution critical values for small sample sizes n (2 to 30).
    """
    n = len(data)
    if n == 0:
        return {"mean": 0.0, "std": 0.0, "ci_half_width": 0.0, "ci_lower": 0.0, "ci_upper": 0.0, "n": 0}
    
    mean = sum(data) / n
    if n == 1:
        return {"mean": mean, "std": 0.0, "ci_half_width": 0.0, "ci_lower": mean, "ci_upper": mean, "n": 1}

    variance = sum((x - mean) ** 2 for x in data) / (n - 1)
    std = math.sqrt(variance)
    
    # Student's t critical values for two-sided alpha=0.05
    # Degrees of freedom df = n - 1
    t_table = {
        1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
        6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
        11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
        16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
        25: 2.060, 30: 2.042, 40: 2.021, 60: 2.000, 120: 1.980
    }
    df = n - 1
    t_val = t_table.get(df, 1.96 if df > 30 else 2.2)
    
    half_width = t_val * (std / math.sqrt(n))
    return {
        "mean": mean,
        "std": std,
        "ci_half_width": half_width,
        "ci_lower": max(0.0, mean - half_width),
        "ci_upper": mean + half_width,
        "n": n
    }
