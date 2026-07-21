"""Gate O27 -- the generation bridge: colour diagonal on three Jordan slots.

Every scientific claim of Gate O27 is pinned to an exact ``Q`` check here --
including the honest no-go on the full ``C (x) H (x) O <-> J_3(O)`` bridge.
"""

import unittest

from jordan_bootstrap.generation_bridge import (
    GenerationBridgeCensus,
    bridge_dimension_obstruction,
    colour_acts_identically_on_slots,
    colour_kills_diagonal,
    colour_lifts_to_jordan_derivation,
    colour_su3,
    generation_bridge_census,
    jordan_basis,
    lift_is_lie_homomorphism,
    offdiagonal_dimension,
    one_generation_module_dimension,
)


class TestGateO27GenerationBridge(unittest.TestCase):
    def test_colour_su3_has_dimension_eight(self):
        """The colour su(3) (g2 stabiliser of e_7) has 8 generators."""
        self.assertEqual(len(colour_su3()), 8)

    def test_jordan_basis_is_twentyseven(self):
        """J_3(O) basis: 3 diagonal + 24 off-diagonal = 27."""
        self.assertEqual(len(jordan_basis()), 27)

    def test_colour_lifts_to_a_jordan_derivation(self):
        """Every colour generator obeys Leibniz on all 27x27 Jordan pairs."""
        self.assertTrue(colour_lifts_to_jordan_derivation())

    def test_colour_kills_the_diagonal(self):
        """Colour derivations annihilate the real diagonal (D(e_0)=0)."""
        self.assertTrue(colour_kills_diagonal())

    def test_lift_is_a_lie_embedding_into_f4(self):
        """[lift(D_a),lift(D_b)] = lift([D_a,D_b]) -- su(3) embeds in Der(J_3O)=f4."""
        self.assertTrue(lift_is_lie_homomorphism())

    def test_colour_acts_identically_on_all_three_slots(self):
        """The per-slot action is the same matrix -- no triality permutation."""
        self.assertTrue(colour_acts_identically_on_slots())

    def test_the_honest_dimension_wall(self):
        """The 24-dim Jordan off-diagonal cannot hold the 32-dim H(x)O module."""
        self.assertEqual(offdiagonal_dimension(), 24)
        self.assertEqual(one_generation_module_dimension(), 32)
        self.assertTrue(bridge_dimension_obstruction())

    def test_census_reports_positive_half_and_wall(self):
        """The O27 ledger records the exact embedding and the open obstruction."""
        c = generation_bridge_census()
        self.assertIsInstance(c, GenerationBridgeCensus)
        self.assertEqual(c.colour_dimension, 8)
        self.assertTrue(c.is_jordan_derivation)
        self.assertTrue(c.kills_diagonal)
        self.assertTrue(c.is_lie_homomorphism)
        self.assertTrue(c.acts_identically_on_slots)
        self.assertEqual(c.slot_count, 3)
        self.assertEqual(c.offdiagonal_dimension, 24)
        self.assertEqual(c.one_generation_dimension, 32)
        self.assertTrue(c.bridge_obstructed)


if __name__ == "__main__":
    unittest.main()
