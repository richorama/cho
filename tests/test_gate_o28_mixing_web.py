"""Gate O28 -- the parameter-free Fano mixing web and its data confrontation.

Every scientific claim of Gate O28 is pinned to an exact ``Q`` check here; the
data-agreement test is the falsifiable half.
"""

import unittest
from fractions import Fraction

from jordan_bootstrap.mixing_web import (
    MixingWebCensus,
    cabibbo_count,
    data_confrontation,
    mass_splitting_count,
    max_absolute_deviation,
    mixing_web_census,
    octant_matches_gate_o26,
    ratio_splitting_over_cabibbo,
    ratio_splitting_over_theta13,
    ratio_theta13_over_cabibbo,
    reactor_count,
    sin2_theta23,
    sum_rule_holds,
    web_agrees_with_data,
    web_is_two_dimensional,
)


class TestGateO28MixingWeb(unittest.TestCase):
    def test_fano_counts(self):
        """The three Fano multiplicities are 7 (all), 3 (through), 4 (avoiding)."""
        self.assertEqual(cabibbo_count(), 7)
        self.assertEqual(reactor_count(), 3)
        self.assertEqual(mass_splitting_count(), 4)

    def test_reactor_tied_to_cabibbo(self):
        """R1 = sin^2(theta13) / |V_us|^2 = 3/7 -- a cross-sector, parameter-free tie."""
        self.assertEqual(ratio_theta13_over_cabibbo(), Fraction(3, 7))

    def test_r2_and_r3(self):
        """R2 = 4/7 and R3 = 4/3 (avoiding/total, avoiding/through)."""
        self.assertEqual(ratio_splitting_over_cabibbo(), Fraction(4, 7))
        self.assertEqual(ratio_splitting_over_theta13(), Fraction(4, 3))

    def test_sum_rule(self):
        """Fano completeness 7 = 3 + 4 -> sin^2(theta13) + dm21^2/dm31^2 = |V_us|^2."""
        self.assertTrue(sum_rule_holds())

    def test_web_is_two_dimensional(self):
        """R3 = R2/R1 and R1 + R2 = 1 -- only two independent ratios."""
        self.assertTrue(web_is_two_dimensional())

    def test_octant_matches_o26(self):
        """R2 equals the Gate O26 atmospheric octant 4/7."""
        self.assertTrue(octant_matches_gate_o26())
        self.assertEqual(sin2_theta23(), Fraction(4, 7))

    def test_predicted_values_are_exact_rationals(self):
        """Every predicted entry in the data table is the exact Fano rational."""
        preds = {row[0]: row[1] for row in data_confrontation()}
        self.assertEqual(preds["R1 = sin2_theta13 / |V_us|^2"], Fraction(3, 7))
        self.assertEqual(preds["R2 = (dm21^2/dm31^2) / |V_us|^2"], Fraction(4, 7))
        self.assertEqual(preds["R3 = (dm21^2/dm31^2) / sin2_theta13"], Fraction(4, 3))
        self.assertEqual(preds["sin2_theta23 = 4/7"], Fraction(4, 7))

    def test_web_agrees_with_current_data(self):
        """The parameter-free web agrees with PDG/NuFIT central values within 5%."""
        self.assertTrue(web_agrees_with_data(0.05))
        # the actual worst deviation is a few percent
        self.assertLess(max_absolute_deviation(), 0.03)

    def test_census_is_fully_consistent(self):
        """The assembled O28 ledger reports the exact web and its data agreement."""
        c = mixing_web_census()
        self.assertIsInstance(c, MixingWebCensus)
        self.assertEqual(c.cabibbo_count, 7)
        self.assertEqual(c.reactor_count, 3)
        self.assertEqual(c.splitting_count, 4)
        self.assertEqual(c.r1_theta13_cabibbo, Fraction(3, 7))
        self.assertEqual(c.r2_splitting_cabibbo, Fraction(4, 7))
        self.assertEqual(c.r3_splitting_theta13, Fraction(4, 3))
        self.assertTrue(c.sum_rule_holds)
        self.assertTrue(c.web_two_dimensional)
        self.assertTrue(c.octant_matches_o26)
        self.assertTrue(c.agrees_within_five_percent)


if __name__ == "__main__":
    unittest.main()
