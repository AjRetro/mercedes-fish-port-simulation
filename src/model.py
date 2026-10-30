# src/model.py
"""
Discrete-Event Simulation (DES) Core Engine for Mercedes Fish Port.
Engineered using SimPy with:
1. 4-Tier Constrained Maritime Network (Anchorage, Channel, Bancas, Wharf Berths)
2. Diurnal Non-Homogeneous Poisson Process (NHPP) via Thinning Algorithm
3. Parallel Lightering (Gang Allocation) with Physical Wharf Berth Contention
4. Common Random Numbers (CRN) using Lehmer LCG (M31 = 2^31 - 1)
"""

import math
import simpy
from typing import Optional, Dict, Any

from src.entities import MediumBoat
from src.resources import MercedesPort
from src.stats import StatsCollector
from src.prng import CRNStreamManager, VariateSampler


def calculate_nhpp_intensity(hour_of_day: float, base_rate: float = 0.15,
                             peak_multiplier: float = 1.8) -> float:
    """
    Diurnal arrival intensity function lambda(t) for Mercedes Fish Port.
    Reflects the early morning wholesale 'Bulungan' rush and afternoon returns.
    """
    t = hour_of_day % 24.0
    
    # Peak 1: Dawn Bulungan Market (06:00 AM, sigma = 1.5h)
    peak1 = peak_multiplier * math.exp(-((t - 6.0) ** 2) / (2 * (1.5 ** 2)))
    
    # Peak 2: Afternoon Artisanal Return (16:30, sigma = 1.2h)
    peak2 = (peak_multiplier * 0.6) * math.exp(-((t - 16.5) ** 2) / (2 * (1.2 ** 2)))
    
    return base_rate + peak1 + peak2


def direct_dock_process(env: simpy.Environment, boat: MediumBoat, port: MercedesPort,
                        unload_time_mean: float, channel_transit_time: float,
                        docking_sampler: VariateSampler, stats: StatsCollector, quiet: bool = True):
    """
    Process for a medium vessel executing direct wharf berthing:
    1. Queues at outer anchorage until channel and berth become available
    2. Navigates inbound through river mouth channel
    3. Occupies wharf berth for direct discharge
    4. Navigates outbound through channel and departs
    """
    stats.update_anchorage_queue(env.now, delta=+1)
    
    # Inbound Channel Transit
    chan_req_start = env.now
    with port.channel.request() as chan_req:
        yield chan_req
        boat.channel_wait_time += (env.now - chan_req_start)
        stats.update_channel_occupancy(env.now, port.channel.count)
        
        # Traverse channel to wharf
        yield env.timeout(channel_transit_time)
        stats.update_channel_occupancy(env.now, port.channel.count - 1)

    # Berth Seizure
    with port.berths.request() as berth_req:
        yield berth_req
        # Anchorage wait ends once berth is seized
        boat.anchorage_exit = env.now
        boat.wait_time_anchorage = boat.anchorage_exit - boat.arrival_time
        boat.service_start = env.now
        stats.update_anchorage_queue(env.now, delta=-1)
        stats.update_berth_occupancy(env.now, port.berths.count)
        
        # Unloading operation at berth
        maneuver_time = docking_sampler.triangular(0.2, 0.35, 0.6)
        yield env.timeout(maneuver_time)
        
        # Service duration based on mean
        unload_duration = docking_sampler.exponential(1.0 / max(0.1, unload_time_mean))
        yield from port.unload_direct_at_berth(boat, unload_duration, quiet=quiet)
        
        boat.service_end = env.now
        stats.update_berth_occupancy(env.now, port.berths.count - 1)

    # Outbound Channel Transit
    with port.channel.request() as chan_req:
        yield chan_req
        stats.update_channel_occupancy(env.now, port.channel.count)
        yield env.timeout(channel_transit_time)
        stats.update_channel_occupancy(env.now, port.channel.count - 1)

    # Finalize vessel metrics
    boat.finalize_metrics(departure_now=env.now)
    stats.record_boat_completion(boat)
    
    if not quiet:
        print(f"[{env.now:.1f}] {boat.name} Direct Unload Complete. Wait: {boat.wait_time_anchorage:.2f}h, Total: {boat.total_port_time:.2f}h")


def parallel_lightering_worker(env: simpy.Environment, mother_boat: MediumBoat, port: MercedesPort,
                               banca_id: int, small_boat_capacity: int, load_time: float,
                               travel_time: float, unload_time: float,
                               stats: StatsCollector, quiet: bool = True):
    """
    Sub-process for an individual shuttle banca servicing a mother vessel.
    Runs concurrently with other bancas until the mother vessel's fish cargo is depleted.
    """
    while mother_boat.remaining_cargo > 0:
        # Determine cargo parcel for this trip
        cargo_this_trip = min(small_boat_capacity, mother_boat.remaining_cargo)
        mother_boat.remaining_cargo -= cargo_this_trip
        
        # Execute 4-step lightering cycle (Load -> Channel In -> Berth Unload -> Channel Out)
        yield from port.execute_shuttle_trip(
            mother_boat=mother_boat,
            banca_id=banca_id,
            load_time=load_time,
            travel_time=travel_time,
            unload_time=unload_time,
            cargo_units=cargo_this_trip,
            quiet=quiet
        )
        mother_boat.banca_trips_completed += 1


def lightering_process(env: simpy.Environment, mother_boat: MediumBoat, port: MercedesPort,
                       small_boat_capacity: int, load_time: float, travel_time: float,
                       unload_time: float, max_parallel_bancas: int,
                       stats: StatsCollector, quiet: bool = True):
    """
    Lightering operation for a mother commercial vessel at outer anchorage:
    1. Arrives in anchorage, enters queue.
    2. Requests a gang of up to k parallel small bancas from the pool.
    3. First banca arrival marks the end of anchorage waiting delay.
    4. Bancas operate in parallel, transferring fish crates to the wharf apron.
    5. Releases bancas and departs anchorage.
    """
    stats.update_anchorage_queue(env.now, delta=+1)
    mother_boat.banca_trips_needed = math.ceil(mother_boat.cargo / small_boat_capacity)
    
    # Request first shuttle banca (measures true congestion wait experienced)
    first_banca_req = port.small_boats.request()
    yield first_banca_req
    
    # Record anchorage wait exit
    mother_boat.anchorage_exit = env.now
    mother_boat.wait_time_anchorage = mother_boat.anchorage_exit - mother_boat.arrival_time
    mother_boat.service_start = env.now
    stats.update_anchorage_queue(env.now, delta=-1)
    stats.update_banca_occupancy(env.now, port.small_boats.count)
    
    # Determine how many additional bancas can be assigned in parallel
    assigned_requests = [first_banca_req]
    workers = []
    
    # Try grabbing up to (max_parallel_bancas - 1) additional bancas if available
    for _ in range(max_parallel_bancas - 1):
        if port.small_boats.count < port.num_small_boats and mother_boat.remaining_cargo > small_boat_capacity:
            req = port.small_boats.request()
            assigned_requests.append(req)
        else:
            break
            
    mother_boat.parallel_bancas_assigned = len(assigned_requests)
    stats.update_banca_occupancy(env.now, port.small_boats.count)
    
    # Launch parallel lightering worker processes
    for idx, _ in enumerate(assigned_requests):
        w = env.process(parallel_lightering_worker(
            env=env,
            mother_boat=mother_boat,
            port=port,
            banca_id=idx + 1,
            small_boat_capacity=small_boat_capacity,
            load_time=load_time,
            travel_time=travel_time,
            unload_time=unload_time,
            stats=stats,
            quiet=quiet
        ))
        workers.append(w)
        
    # Wait until all cargo is cleared by parallel workers
    yield simpy.AllOf(env, workers)
    
    # Release all reserved small boats
    for req in assigned_requests:
        port.small_boats.release(req)
    stats.update_banca_occupancy(env.now, port.small_boats.count)
    
    mother_boat.service_end = env.now
    mother_boat.finalize_metrics(departure_now=env.now)
    stats.record_boat_completion(mother_boat)
    
    if not quiet:
        print(f"[{env.now:.1f}] {mother_boat.name} Lightering Depleted. Trips: {mother_boat.banca_trips_completed}, Total: {mother_boat.total_port_time:.2f}h")


def boat_arrival_nhpp_generator(env: simpy.Environment, port: MercedesPort, crn: CRNStreamManager,
                                base_arrival_rate: float, unload_time_mean: float,
                                small_boat_capacity: int, load_time: float, travel_time: float,
                                unload_time: float, direct_dock_probability: float,
                                max_parallel_bancas: int, stats: StatsCollector,
                                channel_transit_time: float = 0.25, quiet: bool = True):
    """
    Generates fishing vessel arrivals via Diurnal Non-Homogeneous Poisson Process (NHPP)
    using the Lewis-Shedler Thinning Algorithm.
    """
    arrival_stream = crn.get_stream("arrivals")
    cargo_stream = crn.get_stream("cargo")
    docking_stream = crn.get_stream("docking")
    
    # Upper bound intensity lambda_max across 24h
    lambda_max = base_rate = max(0.05, base_arrival_rate)
    peak_multiplier = 1.8 * (base_arrival_rate / 0.34)
    lambda_max = base_rate + (peak_multiplier * 1.6)
    
    boat_id_counter = 0
    t = env.now
    
    while True:
        # Step 1: Generate candidate arrival from homogeneous Poisson(lambda_max)
        delta_t = arrival_stream.exponential(lambda_max)
        yield env.timeout(delta_t)
        t = env.now
        
        # Step 2: Evaluate instantaneous diurnal intensity lambda(t)
        current_lambda = calculate_nhpp_intensity(t, base_rate=base_rate, peak_multiplier=peak_multiplier)
        acceptance_prob = min(1.0, current_lambda / lambda_max)
        
        # Step 3: Acceptance-Rejection Thinning test
        if arrival_stream.uniform(0.0, 1.0) <= acceptance_prob:
            boat_id_counter += 1
            cargo_units = cargo_stream.randint(50, 200)
            is_direct = (docking_stream.uniform(0.0, 1.0) < direct_dock_probability)
            
            vessel = MediumBoat(
                id=boat_id_counter,
                name=f"Vessel_{boat_id_counter}",
                arrival_time=env.now,
                cargo=cargo_units,
                boat_type="medium",
                direct_dock=is_direct
            )
            stats.record_boat_arrival()
            
            if is_direct:
                env.process(direct_dock_process(
                    env=env,
                    boat=vessel,
                    port=port,
                    unload_time_mean=unload_time_mean,
                    channel_transit_time=channel_transit_time,
                    docking_sampler=docking_stream,
                    stats=stats,
                    quiet=quiet
                ))
            else:
                env.process(lightering_process(
                    env=env,
                    mother_boat=vessel,
                    port=port,
                    small_boat_capacity=small_boat_capacity,
                    load_time=load_time,
                    travel_time=travel_time,
                    unload_time=unload_time,
                    max_parallel_bancas=max_parallel_bancas,
                    stats=stats,
                    quiet=quiet
                ))


def run_simulation(sim_time: float = 168.0, num_berths: int = 3, num_small_boats: int = 10,
                   arrival_rate: float = 0.34, unload_time_mean: float = 1.0,
                   small_boat_capacity: int = 20, load_time: float = 0.3,
                   travel_time: float = 0.5, unload_time: float = 0.4,
                   direct_dock_probability: float = 0.15, channel_capacity: int = 3,
                   max_parallel_bancas: int = 2, seed: int = 123456789,
                   quiet: bool = True) -> StatsCollector:
    """
    Executes a single replication of the full Mercedes Fish Port simulation model.
    """
    env = simpy.Environment()
    crn = CRNStreamManager(base_seed=seed)
    port = MercedesPort(
        env=env,
        num_berths=num_berths,
        num_small_boats=num_small_boats,
        channel_capacity=channel_capacity,
        max_parallel_bancas_per_boat=max_parallel_bancas
    )
    stats = StatsCollector(
        sim_time=sim_time,
        num_berths=num_berths,
        num_small_boats=num_small_boats,
        channel_capacity=channel_capacity
    )
    
    env.process(boat_arrival_nhpp_generator(
        env=env,
        port=port,
        crn=crn,
        base_arrival_rate=arrival_rate,
        unload_time_mean=unload_time_mean,
        small_boat_capacity=small_boat_capacity,
        load_time=load_time,
        travel_time=travel_time,
        unload_time=unload_time,
        direct_dock_probability=direct_dock_probability,
        max_parallel_bancas=max_parallel_bancas,
        stats=stats,
        quiet=quiet
    ))
    
    env.run(until=sim_time)
    stats.finalize(sim_time)
    return stats
