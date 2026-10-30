# tests/test_simulation.py
"""
Unit and System Test Suite for Mercedes Fish Port Simulation.
Tests:
1. Dr. Nicart PRNG Primitive Root & Period Properties
2. Deterministic D/D/1 Queueing Verification
3. 4-Tier Constrained Maritime Resource Seizure (Berth contention)
4. Post-Harvest Economic Loss Calculations
5. NHPP Arrival Process Execution
"""

import unittest
import math
import simpy

from src.prng import LehmerLCG, CRNStreamManager, VariateSampler
from src.entities import MediumBoat, ShuttleBanca
from src.resources import MercedesPort
from src.stats import StatsCollector, compute_confidence_interval
from src.validation import run_deterministic_verification
from src.cost_benefit import calculate_vessel_economic_loss, estimate_scenario_incremental_cost
from src.model import run_simulation, calculate_nhpp_intensity


class TestPRNGEngine(unittest.TestCase):
    def test_primitive_root_m31(self):
        """Verify that a = 16807 is a primitive root of M31."""
        res = LehmerLCG.verify_primitive_root(16807, LehmerLCG.MERSENNE_PRIME_31)
        self.assertTrue(res["is_primitive_root"])
        self.assertEqual(res["max_period_length"], 2147483646)

    def test_hull_dobell_checker(self):
        """Verify Hull-Dobell theorem implementation."""
        # Standard full-period LCG: X_{n+1} = (5*X_n + 1) mod 8
        # primes dividing 8 is 2: 5 mod 2 = 1 (mod 2). 4 divides 8: 5 mod 4 = 1. gcd(1, 8) = 1.
        res = LehmerLCG.check_hull_dobell(a=5, c=1, m=8)
        self.assertTrue(res["full_period"])

    def test_crn_stream_independence(self):
        """Ensure CRN streams produce different sequences."""
        crn = CRNStreamManager(base_seed=12345)
        u_arr = crn.get_stream("arrivals").uniform(0, 1)
        u_cargo = crn.get_stream("cargo").uniform(0, 1)
        self.assertNotEqual(u_arr, u_cargo)


class TestQueueingVerification(unittest.TestCase):
    def test_deterministic_dd1(self):
        """Verify that the D/D/1 deterministic queue test matches theoretical wait time."""
        v = run_deterministic_verification()
        self.assertTrue(v["passed"])
        self.assertEqual(v["theoretical_avg_wait"], 2.0)
        self.assertEqual(v["simulated_avg_wait"], 2.0)

    def test_confidence_interval(self):
        """Test Student's t confidence interval function."""
        data = [10.0, 12.0, 11.0, 9.0, 10.5]
        ci = compute_confidence_interval(data)
        self.assertAlmostEqual(ci["mean"], 10.5, places=2)
        self.assertGreater(ci["ci_half_width"], 0.0)
        self.assertTrue(ci["ci_lower"] <= ci["mean"] <= ci["ci_upper"])


class TestMaritimeEconomics(unittest.TestCase):
    def test_spoilage_loss_decay(self):
        """Verify that spoilage loss increases with wait time."""
        loss_1h = calculate_vessel_economic_loss(cargo_units=100, delay_hours=1.0)
        loss_5h = calculate_vessel_economic_loss(cargo_units=100, delay_hours=5.0)
        self.assertGreater(loss_5h["spoilage_loss"], loss_1h["spoilage_loss"])
        self.assertGreater(loss_5h["total_vessel_loss"], loss_1h["total_vessel_loss"])


class TestModelSimulation(unittest.TestCase):
    def test_nhpp_intensity(self):
        """Verify diurnal peaks at dawn bulungan rush."""
        dawn_intensity = calculate_nhpp_intensity(6.0)
        midday_intensity = calculate_nhpp_intensity(12.0)
        self.assertGreater(dawn_intensity, midday_intensity)

    def test_short_simulation_execution(self):
        """Verify simulation runs without exceptions."""
        stats = run_simulation(sim_time=24.0, num_berths=2, num_small_boats=6, quiet=True)
        kpi = stats.compute_summary_kpis()
        self.assertGreater(kpi["boats_arrived"], 0)
        self.assertGreaterEqual(kpi["boats_completed"], 0)


if __name__ == "__main__":
    unittest.main()

