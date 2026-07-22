"""Gate O33 -- assignment, uncertainty, and renormalisation audit."""

import unittest

from jordan_bootstrap.flavour_assignment_audit import (
    adopted_assignment,
    adopted_assignment_rank,
    assignment_fits,
    empirical_results_are_promotion_gate,
    fixed_scale_chi_square,
    look_elsewhere_p_value,
    measurements,
    mixed_scale_mass_inputs,
    profiled_p_value,
)


class TestGateO33FlavourAssignmentAudit(unittest.TestCase):
    def test_all_fano_assignments_are_enumerated(self):
        fits = assignment_fits()
        self.assertEqual(len(fits), 6)
        self.assertEqual(len({fit.counts for fit in fits}), 6)

    def test_adopted_mapping_is_explicit_and_currently_best(self):
        self.assertEqual(adopted_assignment(), (7, 3, 4))
        self.assertEqual(adopted_assignment_rank(), 1)

    def test_uncertainties_are_present(self):
        self.assertEqual(len(measurements()), 3)
        self.assertTrue(all(item.sigma > 0 for item in measurements()))

    def test_statistics_are_reported_without_a_pass_threshold(self):
        self.assertGreater(profiled_p_value(), 0)
        self.assertGreaterEqual(look_elsewhere_p_value(), profiled_p_value())
        self.assertGreater(fixed_scale_chi_square(), 0)
        self.assertFalse(empirical_results_are_promotion_gate())

    def test_quark_mass_comparisons_use_mixed_scales(self):
        rows = mixed_scale_mass_inputs()
        self.assertFalse(rows[0][2])
        self.assertFalse(rows[1][2])
        self.assertTrue(rows[2][2])


if __name__ == "__main__":
    unittest.main()
