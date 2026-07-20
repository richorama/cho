import unittest
from fractions import Fraction

from jordan_bootstrap.born_selection import (
    born_selection_census,
    born_weight,
    contextual_discrepancies,
    frame_consistent_exponents,
    frame_total,
    octonionic_reference_state,
)
from jordan_bootstrap.contextuality import contexts
from jordan_bootstrap.jordan import is_primitive_idempotent

BOUND = 15


class GateO06BornSelection(unittest.TestCase):
    """Octonion premise, Gate O06: Born is the unique frame-consistent rule on h_3(O).

    Turn the exponent of the trace-form rule into a holdout. Among the p-power rules
    weight(P) = tr(P o Psi)^p, only p = 1 (Born) has a frame-independent total -- the
    resolution of the identity forces sum_i tr(P_i o Psi) = tr(Psi) = 1 for every Jordan
    frame. Every p > 1 makes a shared ray's normalised probability frame-dependent, a
    Kochen-Specker-style discrepancy, exact over the rationals. The selection survives
    the jump to the non-associative exceptional Jordan algebra.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = born_selection_census(BOUND)

    def test_census_shape(self) -> None:
        self.assertEqual(self.census.bound, 15)
        self.assertEqual(self.census.context_count, 107)
        self.assertEqual(self.census.shared_ray_count, 15)

    def test_reference_state_is_a_genuine_octonionic_pure_state(self) -> None:
        psi = octonionic_reference_state()
        self.assertTrue(is_primitive_idempotent(psi))
        # It is genuinely octonionic: an off-diagonal entry is imaginary.
        self.assertTrue(any(c != 0 for c in psi[0][1].coords[1:]))

    def test_all_contexts_are_jordan_frames(self) -> None:
        self.assertTrue(self.census.all_contexts_are_jordan_frames)

    def test_born_total_is_one_in_every_frame(self) -> None:
        self.assertTrue(self.census.born_frame_total_is_always_one)
        self.assertEqual(self.census.born_contextual_discrepancies, 0)

    def test_higher_powers_are_contextual(self) -> None:
        self.assertGreater(self.census.power2_distinct_frame_totals, 1)
        self.assertEqual(self.census.power2_contextual_discrepancies, 14)
        self.assertGreater(self.census.power3_distinct_frame_totals, 1)
        self.assertEqual(self.census.power3_contextual_discrepancies, 14)

    def test_born_is_the_unique_frame_consistent_exponent(self) -> None:
        self.assertEqual(self.census.frame_consistent_exponents, (1,))

    def test_classical_relabelling_certifies_nothing(self) -> None:
        # Permuting a frame's rays never changes the total, for any exponent, so only a
        # superposing change of frame does the selecting.
        self.assertTrue(self.census.permutation_leaves_total_invariant)

    # --- explicit exact witnesses -------------------------------------------

    def test_explicit_born_weights(self) -> None:
        psi = octonionic_reference_state()
        self.assertEqual(born_weight(psi, (0, 1, 0)), Fraction(4, 9))
        self.assertEqual(born_weight(psi, (1, 2, 2)), Fraction(8, 27))

    def test_explicit_contextual_discrepancy_for_p_equals_two(self) -> None:
        psi = octonionic_reference_state()
        ray = (0, 1, 0)
        computational = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        tilted = ((4, 0, 3), (3, 0, -4), (0, 1, 0))

        # p = 1: both totals are exactly 1, so the shared ray gets the same probability.
        self.assertEqual(frame_total(psi, computational, 1), Fraction(1))
        self.assertEqual(frame_total(psi, tilted, 1), Fraction(1))

        # p = 2: the totals differ, so the shared ray is assigned two probabilities.
        t2_comp = frame_total(psi, computational, 2)
        t2_tilt = frame_total(psi, tilted, 2)
        self.assertEqual(t2_comp, Fraction(11, 27))
        self.assertEqual(t2_tilt, Fraction(6011, 16875))
        self.assertNotEqual(t2_comp, t2_tilt)

        w2 = born_weight(psi, ray) ** 2
        self.assertEqual(w2 / t2_comp, Fraction(16, 33))
        self.assertEqual(w2 / t2_tilt, Fraction(10000, 18033))

    def test_helpers_agree_with_census(self) -> None:
        psi = octonionic_reference_state()
        frames = contexts(BOUND)
        self.assertEqual(frame_consistent_exponents(psi, frames, (1, 2, 3)), (1,))
        self.assertEqual(contextual_discrepancies(psi, frames, 1), 0)
        self.assertGreater(contextual_discrepancies(psi, frames, 2), 0)


if __name__ == "__main__":
    unittest.main()
