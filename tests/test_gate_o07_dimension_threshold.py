import unittest
from fractions import Fraction

from jordan_bootstrap.spin_factor import (
    complement,
    dimension_threshold_census,
    is_primitive_idempotent,
    jordan_product,
    outer,
    trace,
    zeros,
)
from jordan_bootstrap.octonion import E, octonion


def _v(a, i, b, j):
    return (E[i].scaled(a), E[j].scaled(b))


class GateO07DimensionThreshold(unittest.TestCase):
    """Octonion premise, Gate O07: the Born selection needs d >= 3.

    Drop from h_3(O) to the two-dimensional spin factor h_2(O). Two things change:
    every rational unit ray is now a state (Artin: two octonions always associate), and
    the complement of a ray is forced, so no ray is shared between distinct frames.
    Contextual selection has nothing to bite on, and every exponent becomes vacuously
    frame-consistent -- the O06 selection switches off, exactly at the Gleason
    dimension threshold.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = dimension_threshold_census()

    def test_census_shape(self) -> None:
        self.assertEqual(self.census.ray_count, 82)
        self.assertEqual(self.census.distinct_frames, 66)

    def test_every_ray_is_a_state_by_artin(self) -> None:
        self.assertTrue(self.census.all_rays_are_primitive_idempotents)

    def test_complements_are_states_and_orthogonal(self) -> None:
        self.assertTrue(self.census.all_complements_are_primitive_idempotents)
        self.assertTrue(self.census.all_complements_orthogonal)

    def test_complement_is_forced_no_shared_rays(self) -> None:
        self.assertEqual(self.census.max_frames_sharing_a_ray, 1)
        self.assertEqual(self.census.rays_shared_across_distinct_frames, 0)

    def test_parseval_still_holds(self) -> None:
        self.assertTrue(self.census.parseval_total_is_one)

    def test_selection_switches_off_all_exponents_are_consistent(self) -> None:
        # Contrast with O06 on h_3(O), where the frame-consistent exponents were (1,).
        self.assertEqual(self.census.frame_consistent_exponents, (1, 2, 3))

    # --- explicit witnesses --------------------------------------------------

    def test_cross_axis_ray_is_a_state_here_though_it_would_break_in_d3(self) -> None:
        # Entries on e_1 and e_4 (different Fano lines); with only two entries Artin
        # guarantees associativity, so outer(v) is a genuine primitive idempotent.
        p = outer(_v(Fraction(3, 5), 1, Fraction(4, 5), 4))
        self.assertTrue(is_primitive_idempotent(p))

    def test_explicit_complement_is_the_unique_orthogonal_ray(self) -> None:
        p = outer(_v(Fraction(3, 5), 0, Fraction(4, 5), 1))
        q = complement(p)
        self.assertTrue(is_primitive_idempotent(q))
        self.assertTrue(all(
            jordan_product(p, q)[i][j].coords == zeros()[i][j].coords
            for i in range(2) for j in range(2)
        ))
        # p + q resolves the identity: trace 2, and the pair is a frame.
        self.assertEqual(trace(p).coords, octonion(1, 0, 0, 0, 0, 0, 0, 0).coords)
        self.assertEqual(trace(q).coords, octonion(1, 0, 0, 0, 0, 0, 0, 0).coords)


if __name__ == "__main__":
    unittest.main()
