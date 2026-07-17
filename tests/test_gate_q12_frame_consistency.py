import unittest

from amplitude_bootstrap.frame_function import (
    FrameConsistency,
    born_is_exactly_parseval,
    frame_consistency_census,
)


class GateQ12FrameConsistency(unittest.TestCase):
    """Amplitude Gate Q12: the Born rule as a resolution-agreement theorem.

    The r-norm rules are recast as frame functions and tested for resolution
    consistency — whether the total weight of a complete measurement is independent of
    the orthonormal frame the observer chose. Only r = 2 (Born) is frame-consistent (it
    is exactly Parseval), and this holds in dimensions three and four; every r > 2 is
    frame-dependent under superposition but not under a classical relabelling. This
    hardens Q11 to higher dimension and states it in the project's own coarse-graining
    language.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.dim3 = frame_consistency_census(3)
        cls.dim4 = frame_consistency_census(4)

    def test_census_shapes(self) -> None:
        self.assertIsInstance(self.dim3, FrameConsistency)
        # Nonzero vectors over {0, 1, i}: 3**d - 1.
        self.assertEqual(self.dim3.total_states, 26)
        self.assertEqual(self.dim4.total_states, 80)

    def test_born_is_frame_consistent_in_both_dimensions(self) -> None:
        self.assertEqual(self.dim3.born_inconsistent, 0)
        self.assertEqual(self.dim4.born_inconsistent, 0)

    def test_born_frame_sum_is_exactly_parseval(self) -> None:
        # For r = 2 the frame sum equals <s|s> in every declared basis.
        self.assertTrue(born_is_exactly_parseval(3))
        self.assertTrue(born_is_exactly_parseval(4))

    def test_other_exponents_are_frame_dependent_under_superposition(self) -> None:
        # Every superposing frame exposes r = 4 and r = 6 for essentially every state.
        self.assertEqual(self.dim3.alternative_inconsistent, ((2, 26), (3, 26)))
        self.assertEqual(self.dim4.alternative_inconsistent, ((2, 78), (3, 78)))

    def test_born_is_the_unique_consistent_exponent(self) -> None:
        self.assertTrue(self.dim3.born_is_uniquely_consistent)
        self.assertTrue(self.dim4.born_is_uniquely_consistent)

    def test_classical_relabelling_exposes_nothing(self) -> None:
        # A permutation of outcomes leaves the frame sum unchanged for every exponent, in
        # both dimensions: only superposition does the selecting.
        for census in (self.dim3, self.dim4):
            for _, count in census.relabelling_inconsistent:
                self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
