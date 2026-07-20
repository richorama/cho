import unittest
from fractions import Fraction

from jordan_bootstrap.triality import (
    all_permutations,
    apply_permutation,
    compose,
    occupied_slots,
    slot_state,
    triality_census,
)
from jordan_bootstrap.jordan import trace_form, is_primitive_idempotent
from jordan_bootstrap.contextuality import ray_to_state


class GateO08Triality(unittest.TestCase):
    """Octonion premise, Gate O08: triality -- the S_3 symmetry of the three slots.

    O04 certified the entrywise (G_2) symmetries that fix matrix positions. This gate
    certifies the complementary symmetry that moves positions: conjugation by a 3x3
    permutation matrix is a Jordan automorphism, the six of them form an S_3, and the
    three-cycle cyclically permutes the three off-diagonal octonion slots -- the three
    inequivalent 8-dim Spin(8) reps -- the finite shadow of triality, which only the
    octonions possess. It preserves every Born probability and enlarges the certified
    F_4 symmetry beyond O04.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = triality_census()

    def test_six_permutations_form_s3(self) -> None:
        self.assertEqual(self.census.permutation_count, 6)
        self.assertEqual(len(set(all_permutations())), 6)

    def test_every_permutation_is_a_jordan_automorphism(self) -> None:
        self.assertTrue(self.census.all_are_jordan_automorphisms)
        self.assertTrue(self.census.trace_preserving)

    def test_permutations_preserve_states_and_frames(self) -> None:
        self.assertTrue(self.census.idempotent_preserving)
        self.assertTrue(self.census.frame_preserving)

    def test_born_probabilities_are_invariant(self) -> None:
        self.assertEqual(self.census.born_invariant_checks, 270)
        self.assertEqual(self.census.born_invariant_mismatches, 0)

    def test_three_cycle_has_order_three(self) -> None:
        self.assertEqual(self.census.three_cycle_order, 3)

    def test_three_cycle_rotates_the_three_slots(self) -> None:
        self.assertTrue(self.census.slots_are_cyclically_permuted)
        cycle = (1, 2, 0)
        self.assertEqual(occupied_slots(apply_permutation(cycle, slot_state(0))), (2,))
        self.assertEqual(occupied_slots(apply_permutation(cycle, slot_state(1))), (0,))
        self.assertEqual(occupied_slots(apply_permutation(cycle, slot_state(2))), (1,))

    def test_permutation_is_not_an_entrywise_o04_automorphism(self) -> None:
        self.assertTrue(self.census.permutation_moves_positions)

    def test_composition_with_o04_still_preserves_born(self) -> None:
        self.assertGreater(self.census.combined_with_o04_born_checks, 0)
        self.assertEqual(self.census.combined_with_o04_born_mismatches, 0)

    # --- explicit witnesses --------------------------------------------------

    def test_explicit_permutation_preserves_a_born_probability(self) -> None:
        sigma = (2, 0, 1)
        p = ray_to_state((1, 2, 2))
        q = ray_to_state((2, -2, 1))
        self.assertTrue(is_primitive_idempotent(apply_permutation(sigma, p)))
        self.assertEqual(
            trace_form(apply_permutation(sigma, p), apply_permutation(sigma, q)).coords,
            trace_form(p, q).coords,
        )

    def test_permutation_moves_diagonal_content(self) -> None:
        from jordan_bootstrap.octonion import octonion

        diag = ray_to_state((1, 0, 0))  # content at position (0,0)
        moved = apply_permutation((1, 2, 0), diag)
        one = octonion(1, 0, 0, 0, 0, 0, 0, 0)
        self.assertEqual(diag[0][0].coords, one.coords)
        self.assertEqual(moved[0][0].coords, octonion(0, 0, 0, 0, 0, 0, 0, 0).coords)
        self.assertEqual(moved[2][2].coords, one.coords)

    def test_compose_is_group_law(self) -> None:
        cycle = (1, 2, 0)
        self.assertEqual(compose(cycle, cycle), (2, 0, 1))
        self.assertEqual(compose(cycle, compose(cycle, cycle)), (0, 1, 2))
        swap = (1, 0, 2)
        self.assertEqual(compose(swap, swap), (0, 1, 2))


if __name__ == "__main__":
    unittest.main()
