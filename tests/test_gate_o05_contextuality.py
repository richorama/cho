import unittest
from fractions import Fraction

from jordan_bootstrap.contextuality import (
    contexts,
    contextuality_census,
    godsil_zaks_value,
    is_rational_unit_ray,
    odd_position,
    primitive,
    ray_to_state,
)
from jordan_bootstrap.jordan import is_jordan_frame, is_primitive_idempotent

BOUND = 13


class GateO05Contextuality(unittest.TestCase):
    """Octonion premise, Gate O05: the rational verdict on Kochen-Specker.

    The composite (Peres-Mermin) road to contextuality is closed by O03. The only
    remaining road is the single-system Kochen-Specker theorem in ``d = 3``. Over the
    exact-rational rays of ``h_3(O)`` it too closes: an explicit deterministic
    non-contextual value-state exists (Godsil-Zaks), so genuine contextuality here is
    an irrational phenomenon. The octonionic Born rule remains a distinct,
    probabilistic non-contextual assignment.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = contextuality_census(BOUND)

    def test_census_shape(self) -> None:
        self.assertEqual(self.census.bound, 13)
        self.assertEqual(self.census.ray_count, 219)
        self.assertEqual(self.census.context_count, 69)

    def test_every_rational_ray_lifts_to_a_primitive_idempotent(self) -> None:
        self.assertTrue(self.census.all_rays_are_primitive_idempotents)

    def test_every_context_is_a_jordan_frame(self) -> None:
        self.assertTrue(self.census.all_contexts_are_jordan_frames)

    def test_lemma_1_every_ray_has_exactly_one_odd_coordinate(self) -> None:
        self.assertEqual(
            self.census.rays_with_unique_odd_coordinate, self.census.ray_count
        )

    def test_lemma_2_orthogonal_rays_have_distinct_odd_positions(self) -> None:
        self.assertGreater(self.census.orthogonal_pairs_checked, 0)
        self.assertEqual(
            self.census.orthogonal_pairs_with_distinct_odd_position,
            self.census.orthogonal_pairs_checked,
        )

    def test_godsil_zaks_value_state_is_exactly_one_per_context(self) -> None:
        self.assertEqual(self.census.godsil_zaks_context_violations, 0)

    def test_born_rule_is_a_noncontextual_probability_assignment(self) -> None:
        self.assertGreater(self.census.born_context_sum_checks, 0)
        self.assertEqual(self.census.born_context_sum_violations, 0)

    # --- explicit witnesses --------------------------------------------------

    def test_rational_unit_ray_predicate(self) -> None:
        self.assertTrue(is_rational_unit_ray((1, 2, 2)))   # norm 9
        self.assertTrue(is_rational_unit_ray((2, 3, 6)))   # norm 49
        self.assertFalse(is_rational_unit_ray((1, 0, 1)))  # norm 2, irrational unit
        self.assertFalse(is_rational_unit_ray((1, 1, 1)))  # norm 3

    def test_explicit_odd_positions_and_values(self) -> None:
        self.assertEqual(odd_position((1, 2, 2)), 0)
        self.assertEqual(odd_position((2, 1, 2)), 1)
        self.assertEqual(odd_position((2, 2, 1)), 2)
        self.assertEqual(godsil_zaks_value((1, 2, 2)), 1)
        self.assertEqual(godsil_zaks_value((2, 1, 2)), 0)
        self.assertEqual(godsil_zaks_value((2, 2, 1)), 0)

    def test_explicit_rational_context_is_a_jordan_frame_and_colored(self) -> None:
        u, v, w = (1, 2, 2), (2, -2, 1), (2, 1, -2)
        frame = tuple(ray_to_state(r) for r in (u, v, w))
        for p in frame:
            self.assertTrue(is_primitive_idempotent(p))
        self.assertTrue(is_jordan_frame(frame))
        self.assertEqual(sum(godsil_zaks_value(r) for r in (u, v, w)), 1)

    def test_ray_to_state_uses_exact_rational_normalization(self) -> None:
        p = ray_to_state((1, 2, 2))  # unit vector (1/3, 2/3, 2/3)
        self.assertEqual(p[0][0].coords[0], Fraction(1, 9))
        self.assertEqual(p[1][1].coords[0], Fraction(4, 9))
        self.assertEqual(p[2][2].coords[0], Fraction(4, 9))

    def test_primitive_canonicalization(self) -> None:
        self.assertEqual(primitive((2, 4, 4)), (1, 2, 2))
        self.assertEqual(primitive((-1, -2, -2)), (1, 2, 2))
        self.assertEqual(primitive((0, -3, 3)), (0, 1, -1))

    def test_the_web_is_contextually_connected(self) -> None:
        # Colorability is non-trivial only if rays are shared across contexts.
        frames = contexts(BOUND)
        from collections import Counter

        appearances = Counter(r for f in frames for r in f)
        shared = sum(1 for r, n in appearances.items() if n >= 2)
        self.assertGreater(shared, 0)


if __name__ == "__main__":
    unittest.main()
