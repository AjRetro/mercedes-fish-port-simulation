# src/entities.py
"""
Maritime Entity Definitions for the Mercedes Fish Port Simulation.
Models commercial fishing mother vessels, small shuttle bancas (lightering craft),
and passage events with detailed timestamp and quality tracking.
"""

import math
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class MediumBoat:
    """
    Represents a commercial fishing vessel (e.g., Basnig, Ring Netter)
    arriving at the Mercedes Fish Port outer roadstead/anchorage.
    """
    id: int
    name: str
    arrival_time: float
    cargo: int  # Initial cargo volume in units / fish tubs (banyera)
    boat_type: str = "medium"
    direct_dock: bool = False
    
    # State tracking
    remaining_cargo: int = field(init=False)
    anchorage_entry: float = field(init=False)
    anchorage_exit: Optional[float] = None
    service_start: Optional[float] = None
    service_end: Optional[float] = None
    departure_time: Optional[float] = None
    
    # Duration metrics
    wait_time_anchorage: float = 0.0
    channel_wait_time: float = 0.0
    channel_transit_time: float = 0.0
    docking_maneuver_time: float = 0.0
    service_time: float = 0.0
    total_port_time: float = 0.0
    
    # Operational counts
    banca_trips_needed: int = 0
    banca_trips_completed: int = 0
    parallel_bancas_assigned: int = 0
    
    # Economics & Perishability
    spoilage_loss_php: float = 0.0
    fuel_idle_loss_php: float = 0.0

    def __post_init__(self):
        self.remaining_cargo = self.cargo
        self.anchorage_entry = self.arrival_time

    @property
    def is_completed(self) -> bool:
        return self.remaining_cargo <= 0 and self.departure_time is not None

    def finalize_metrics(self, departure_now: float, price_per_unit_php: float = 2500.0,
                         ambient_decay_rate: float = 0.035, idle_fuel_cost_per_hr: float = 450.0):
        """
        Finalize vessel operational metrics, post-harvest perishability decay,
        and auxiliary generator idle fuel consumption.
        """
        self.departure_time = departure_now
        self.total_port_time = max(0.0, self.departure_time - self.arrival_time)
        if self.anchorage_exit is not None:
            self.wait_time_anchorage = max(0.0, self.anchorage_exit - self.anchorage_entry)
        else:
            self.wait_time_anchorage = max(0.0, self.service_start - self.arrival_time) if self.service_start else 0.0
        
        if self.service_start and self.service_end:
            self.service_time = max(0.0, self.service_end - self.service_start)

        # Economic loss formulation:
        # Spoilage decay = Cargo * Price0 * (1 - exp(-kappa * wait_hours))
        # Idle diesel burn = wait_hours * idle_fuel_rate
        total_delay_hours = self.wait_time_anchorage + self.channel_wait_time
        cargo_gross_value = self.cargo * price_per_unit_php
        spoilage_fraction = 1.0 - math.exp(-ambient_decay_rate * total_delay_hours)
        
        self.spoilage_loss_php = round(cargo_gross_value * spoilage_fraction, 2)
        self.fuel_idle_loss_php = round(total_delay_hours * idle_fuel_cost_per_hr, 2)


@dataclass
class ShuttleBanca:
    """
    Represents a motorized small craft (banca) providing lightering services
    transferring fish crates from mother vessels at anchorage to the port apron.
    """
    id: int
    name: str
    capacity: int = 20  # capacity in banyera (units)
    
    # Live operational state
    current_trip: int = 0
    total_trips_completed: int = 0
    total_cargo_transferred: int = 0
    total_transit_hours: float = 0.0
    total_berth_occupancy_hours: float = 0.0
    current_mother_boat_id: Optional[int] = None

    def record_trip(self, cargo_carried: int, transit_hours: float, berth_hours: float):
        self.total_trips_completed += 1
        self.total_cargo_transferred += cargo_carried
        self.total_transit_hours += transit_hours
        self.total_berth_occupancy_hours += berth_hours


# Backward compatibility alias for legacy code imports
class Boat:
    """Legacy compatibility wrapper."""
    def __init__(self, name, boat_type="medium", arrival_time=0.0, cargo=0):
        self.name = name
        self.boat_type = boat_type
        self.arrival_time = arrival_time
        self.cargo = cargo
        self.remaining_cargo = cargo
        self.wait_time = 0.0
        self.service_time = 0.0
        self.departure_time = 0.0
