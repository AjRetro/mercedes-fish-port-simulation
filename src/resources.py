# src/resources.py
"""
4-Tier Constrained Maritime Infrastructure Resources for Mercedes Fish Port.
Enforces realistic capacity constraints across:
1. Outer Anchorage (Queueing Area)
2. River Channel Navigation Corridor (Traffic Density & Safety Limits)
3. Shuttle Banca Fleet (Lightering Vessel Pool)
4. Wharf Apron Landing Berths (Direct Berthing & Lightering Discharge Contention)
"""

import simpy
from typing import Dict, List, Optional
from src.entities import MediumBoat, ShuttleBanca


class MercedesPort:
    """
    Comprehensive physical port resource model for Mercedes Fish Port, Camarines Norte.
    """
    def __init__(self, env: simpy.Environment, num_berths: int = 3, num_small_boats: int = 10,
                 channel_capacity: int = 3, max_parallel_bancas_per_boat: int = 2):
        self.env = env
        self.num_berths = num_berths
        self.num_small_boats = num_small_boats
        self.channel_capacity = channel_capacity
        self.max_parallel_bancas_per_boat = max_parallel_bancas_per_boat
        
        # SimPy Resource instances
        self.berths = simpy.Resource(env, capacity=num_berths)
        self.small_boats = simpy.Resource(env, capacity=num_small_boats)
        self.channel = simpy.Resource(env, capacity=channel_capacity)
        
        # Real-time state metrics & density tracking
        self.active_channel_transits = 0
        self.channel_transits_log: List[Dict[str, float]] = []
        self.berth_occupancy_log: List[Dict[str, float]] = []
        self.anchorage_queue_log: List[Dict[str, float]] = []
        
        # Accumulators
        self.total_channel_passages = 0
        self.total_lightering_trips = 0
        self.total_direct_docks = 0

    def log_channel_state(self):
        """Record instantaneous channel traffic density for Objective #12."""
        self.channel_transits_log.append({
            "timestamp": self.env.now,
            "density": self.active_channel_transits,
            "utilization": self.active_channel_transits / self.channel_capacity
        })

    def log_berth_state(self):
        """Record instantaneous berth occupancy."""
        self.berth_occupancy_log.append({
            "timestamp": self.env.now,
            "occupied_berths": self.berths.count,
            "berth_utilization": self.berths.count / self.num_berths
        })

    def log_anchorage_state(self, queue_len: int):
        """Record instantaneous anchorage queue length."""
        self.anchorage_queue_log.append({
            "timestamp": self.env.now,
            "anchorage_queue_length": queue_len
        })

    def transit_channel(self, vessel_name: str, transit_time: float, direction: str = "inbound", quiet: bool = True):
        """
        Simulate passage through the Mercedes river mouth / navigation channel.
        Contention occurs if channel capacity is saturated.
        """
        req_start = self.env.now
        with self.channel.request() as req:
            yield req
            channel_delay = self.env.now - req_start
            self.active_channel_transits += 1
            self.total_channel_passages += 1
            self.log_channel_state()
            
            if not quiet and channel_delay > 0.05:
                print(f"  [{self.env.now:.2f}] {vessel_name} waited {channel_delay:.2f}h to enter channel ({direction}).")
            
            yield self.env.timeout(transit_time)
            
            self.active_channel_transits -= 1
            self.log_channel_state()

    def unload_direct_at_berth(self, boat: MediumBoat, unload_duration: float, quiet: bool = True):
        """
        Simulate direct docking of a medium commercial fishing vessel at a wharf berth.
        """
        self.total_direct_docks += 1
        self.log_berth_state()
        yield self.env.timeout(unload_duration)
        self.log_berth_state()
        if not quiet:
            print(f"  [{self.env.now:.2f}] {boat.name} completed direct wharf unloading ({unload_duration:.2f}h).")

    def execute_shuttle_trip(self, mother_boat: MediumBoat, banca_id: int, load_time: float,
                             travel_time: float, unload_time: float, cargo_units: int, quiet: bool = True):
        """
        A single lightering cycle:
        1. Banca loads cargo from mother boat at anchorage (load_time)
        2. Banca navigates inbound through river channel to port wharf (travel_time)
        3. Banca requests and SEIZES a wharf berth slip to unload fish crates (unload_time)
        4. Banca navigates outbound through channel back to anchorage (travel_time)
        """
        # Step 1: Loading at mother boat
        yield self.env.timeout(load_time)
        
        # Step 2: Channel Inbound
        yield from self.transit_channel(f"Banca_{banca_id}", travel_time, direction="inbound", quiet=quiet)
        
        # Step 3: Wharf Berth Seizure & Unloading (Resolves previous 'virtual dock' limitation)
        berth_wait_start = self.env.now
        with self.berths.request() as berth_req:
            yield berth_req
            berth_wait = self.env.now - berth_wait_start
            self.log_berth_state()
            
            if not quiet and berth_wait > 0.05:
                print(f"    [{self.env.now:.2f}] Banca_{banca_id} waited {berth_wait:.2f}h for berth slip.")
            
            yield self.env.timeout(unload_time)
            self.log_berth_state()
        
        # Step 4: Channel Outbound
        yield from self.transit_channel(f"Banca_{banca_id}", travel_time, direction="outbound", quiet=quiet)
        self.total_lightering_trips += 1


# Compatibility class for legacy tests or wrappers
class Port(MercedesPort):
    """Alias for backwards compatibility with existing run scripts."""
    def __init__(self, env, num_berths=3, num_small_boats=10):
        super().__init__(env, num_berths=num_berths, num_small_boats=num_small_boats)
    
    def unload_at_berth(self, boat, unload_time, quiet=False):
        return self.unload_direct_at_berth(boat, unload_time, quiet=quiet)
    
    def shuttle_trip(self, medium_boat, small_boat, load_time, travel_time, unload_time, quiet=False):
        cargo = getattr(small_boat, "cargo", 20)
        return self.execute_shuttle_trip(medium_boat, 1, load_time, travel_time, unload_time, cargo, quiet=quiet)
