"""Gate O32 -- exact canonical-Yukawa go/no-go."""

import unittest

from jordan_bootstrap.yukawa_operator_gate import (
    canonical_yukawa_theorem_closed,
    gauge_equivariant_symmetric_dimension,
    genuine_three_generation_module_available,
    invariant_basis_is_identity_and_all_ones,
    invariant_operator_has_generation_degeneracy,
    permutation_invariant_symmetric_dimension,
    symmetric_generation_basis,
    yukawa_operator_gate_census,
)


class TestGateO32YukawaOperator(unittest.TestCase):
    def test_full_generation_module_is_still_missing(self):
        self.assertFalse(genuine_three_generation_module_available())

    def test_gauge_equivariance_leaves_all_symmetric_textures_free(self):
        self.assertEqual(len(symmetric_generation_basis()), 6)
        self.assertEqual(gauge_equivariant_symmetric_dimension(), 6)

    def test_frame_symmetry_reduces_to_identity_and_all_ones(self):
        self.assertEqual(permutation_invariant_symmetric_dimension(), 2)
        self.assertTrue(invariant_basis_is_identity_and_all_ones())

    def test_frame_symmetric_operator_has_a_degenerate_doublet(self):
        self.assertTrue(invariant_operator_has_generation_degeneracy())

    def test_theorem_remains_open(self):
        self.assertFalse(canonical_yukawa_theorem_closed())
        census = yukawa_operator_gate_census()
        self.assertFalse(census.full_generation_module)
        self.assertEqual(census.gauge_equivariant_symmetric_dimension, 6)
        self.assertEqual(census.permutation_invariant_symmetric_dimension, 2)
        self.assertTrue(census.invariant_generation_degeneracy)
        self.assertFalse(census.theorem_closed)


if __name__ == "__main__":
    unittest.main()
