"""Gate O29 -- the mass<->mixing bridge and its data confrontation.

Every scientific claim of Gate O29 is pinned to an exact ``Q`` check here; the
data-agreement test on the charm-free identities is the falsifiable half.
"""

import unittest
from fractions import Fraction

from jordan_bootstrap.mass_mixing_bridge import (
    MassMixingBridgeCensus,
    clean_bridge_agrees,
    data_confrontation,
    down_count,
    empirical_results_are_promotion_gate,
    headline_identity_holds,
    lepton_count,
    mass_counts,
    mass_mixing_bridge_census,
    matches_o28_reactor_ratio,
    max_clean_deviation,
    ratio_down_over_up,
    ratio_lepton_over_down,
    ratio_lepton_over_up,
    ratio_mmu_mtau_over_splitting,
    ratio_mmu_mtau_over_theta13,
    ratio_ms_mb_over_cabibbo,
    ratio_ms_mb_over_theta13,
    up_count,
)


class TestGateO29MassMixingBridge(unittest.TestCase):
    def test_mass_counts_are_fock_grade_traces(self):
        """The mass coefficients (1, 3, 8) are N-grade traces: Tr P_0, Tr P_1, Tr I."""
        self.assertEqual(up_count(), 1)
        self.assertEqual(down_count(), 3)
        self.assertEqual(lepton_count(), 8)
        self.assertEqual(mass_counts(), (1, 3, 8))

    def test_headline_identity(self):
        """m_s/m_b = sin^2(theta13): down grade-1 count = reactor Fano count = 3."""
        self.assertTrue(headline_identity_holds())
        self.assertEqual(ratio_ms_mb_over_theta13(), Fraction(1))

    def test_lepton_cross_identities(self):
        """m_mu/m_tau = 2*(dm21/dm31) and = (8/3)*sin^2(theta13)."""
        self.assertEqual(ratio_mmu_mtau_over_splitting(), Fraction(2))
        self.assertEqual(ratio_mmu_mtau_over_theta13(), Fraction(8, 3))

    def test_consistency_with_o28_web(self):
        """(m_s/m_b)/|V_us|^2 = 3/7 = the O28 ratio R1 (since m_s/m_b = sin^2 th13)."""
        self.assertEqual(ratio_ms_mb_over_cabibbo(), Fraction(3, 7))
        self.assertTrue(matches_o28_reactor_ratio())

    def test_mass_mass_ratios(self):
        """Grade counts give 3, 8/3, 8 for the pure mass-mass ratios."""
        self.assertEqual(ratio_down_over_up(), Fraction(3))
        self.assertEqual(ratio_lepton_over_down(), Fraction(8, 3))
        self.assertEqual(ratio_lepton_over_up(), Fraction(8))

    def test_predicted_values_are_exact_rationals(self):
        """Each row's prediction is the exact Fock/Fano rational."""
        preds = {row[0]: row[1] for row in data_confrontation()}
        self.assertEqual(preds["m_s/m_b = sin2_theta13"], Fraction(1))
        self.assertEqual(preds["m_mu/m_tau = 2*(dm21/dm31)"], Fraction(2))
        self.assertEqual(preds["m_mu/m_tau = (8/3)*sin2_theta13"], Fraction(8, 3))

    def test_data_table_is_diagnostic_not_a_promotion_gate(self):
        self.assertIsInstance(clean_bridge_agrees(0.03), bool)
        self.assertGreater(max_clean_deviation(), 0)
        self.assertFalse(empirical_results_are_promotion_gate())

    def test_scale_sensitive_rows_are_flagged(self):
        """The m_c/m_t identities are reported but flagged scale-sensitive."""
        flagged = {row[0]: row[4] for row in data_confrontation()}
        self.assertTrue(flagged["(m_s/m_b)/(m_c/m_t) = 3"])
        self.assertTrue(flagged["(m_mu/m_tau)/(m_c/m_t) = 8"])
        self.assertTrue(flagged["m_s/m_b = sin2_theta13"])
        self.assertTrue(flagged["(m_mu/m_tau)/(m_s/m_b) = 8/3"])
        self.assertEqual(sum(1 for row in data_confrontation() if not row[4]), 2)

    def test_census_is_fully_consistent(self):
        """The assembled O29 ledger reports the bridge and empirical caveat."""
        c = mass_mixing_bridge_census()
        self.assertIsInstance(c, MassMixingBridgeCensus)
        self.assertEqual(c.grade_multiplicities, (1, 3, 3, 1))
        self.assertEqual(c.mass_counts, (1, 3, 8))
        self.assertTrue(c.headline_identity)
        self.assertEqual(c.ms_mb_over_theta13, Fraction(1))
        self.assertEqual(c.mmu_mtau_over_splitting, Fraction(2))
        self.assertEqual(c.mmu_mtau_over_theta13, Fraction(8, 3))
        self.assertEqual(c.ms_mb_over_cabibbo, Fraction(3, 7))
        self.assertTrue(c.matches_o28_r1)
        self.assertFalse(c.empirical_promotion_allowed)


if __name__ == "__main__":
    unittest.main()
