"""Gate O14 -- anomaly cancellation forces the Standard Model hypercharges.

Exact rational assertions: all six gauge/gravitational anomalies of one
generation vanish for the SM hypercharges; fixing the U(1) scale by the O11
electric charge reduces the cubic U(1)^3 anomaly to a quadratic whose only roots
are the SM up/down hypercharges (charge quantisation forced); and
sin^2(theta_W) = 3/8 exactly.
"""

import unittest
from fractions import Fraction

from jordan_bootstrap.hypercharge import (
    HyperchargeCensus,
    anchored_family,
    anchored_u1_cubed,
    grav_u1_anomaly,
    hypercharge_census,
    standard_model_generation,
    su2_sq_u1_anomaly,
    su3_cubed_anomaly,
    su3_sq_u1_anomaly,
    u1_cubed_anomaly,
    weinberg_sin2,
    witten_doublet_count,
)


class TestGateO14Hypercharge(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.census = hypercharge_census()
        cls.sm = standard_model_generation()

    def test_census_type(self):
        self.assertIsInstance(self.census, HyperchargeCensus)

    def test_all_six_anomalies_vanish(self):
        self.assertTrue(self.census.all_six_anomalies_vanish)

    def test_each_anomaly_is_exactly_zero(self):
        self.assertEqual(su3_cubed_anomaly(self.sm), 0)
        self.assertEqual(su3_sq_u1_anomaly(self.sm), 0)
        self.assertEqual(su2_sq_u1_anomaly(self.sm), 0)
        self.assertEqual(u1_cubed_anomaly(self.sm), 0)
        self.assertEqual(grav_u1_anomaly(self.sm), 0)

    def test_witten_global_anomaly_free(self):
        # even number of SU(2) doublets: 3 (quark colours) + 1 (lepton) = 4
        self.assertEqual(witten_doublet_count(self.sm), 4)
        self.assertEqual(witten_doublet_count(self.sm) % 2, 0)

    def test_electric_charges_are_the_standard_model(self):
        charges = {f.name: f.electric_charges() for f in self.sm}
        self.assertEqual(charges["Q"], (Fraction(2, 3), Fraction(-1, 3)))
        self.assertEqual(charges["u^c"], (Fraction(-2, 3),))
        self.assertEqual(charges["d^c"], (Fraction(1, 3),))
        self.assertEqual(charges["L"], (Fraction(0), Fraction(-1)))
        self.assertEqual(charges["e^c"], (Fraction(1),))

    def test_cubic_anomaly_collapses_to_quadratic(self):
        self.assertTrue(self.census.cubic_collapses_to_quadratic)

    def test_forcing_roots_are_exactly_the_sm_hypercharges(self):
        self.assertEqual(set(self.census.forcing_roots),
                         {Fraction(1, 3), Fraction(-2, 3)})

    def test_hypercharges_are_forced_up_to_relabelling(self):
        self.assertTrue(self.census.roots_are_sm_up_to_relabelling)
        self.assertTrue(self.census.hypercharges_are_forced)

    def test_no_other_rational_solution_survives(self):
        # the anchored U(1)^3 anomaly is the quadratic -(1/3)(3Y-1)(3Y+2);
        # confirm it is nonzero for a spread of non-SM rationals
        for y in [Fraction(0), Fraction(1), Fraction(-1), Fraction(1, 2),
                  Fraction(2, 3), Fraction(-1, 3), Fraction(1, 6)]:
            self.assertNotEqual(anchored_u1_cubed(y), 0)

    def test_both_roots_give_the_same_hypercharge_multiset(self):
        a = {f.hypercharge for f in anchored_family(Fraction(1, 3))}
        b = {f.hypercharge for f in anchored_family(Fraction(-2, 3))}
        self.assertEqual(a, b)

    def test_weak_mixing_angle_is_three_eighths(self):
        self.assertEqual(self.census.weinberg_sin2, Fraction(3, 8))
        self.assertEqual(weinberg_sin2(self.sm), Fraction(3, 8))


if __name__ == "__main__":
    unittest.main()
