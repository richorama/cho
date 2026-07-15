import unittest

from amplitude_bootstrap.contextuality import (
    MAGIC_SQUARE,
    coarse_grained_surviving_observables,
    kochen_specker_contradiction,
    line_products_match_signs,
    lines_are_jointly_measurable,
    no_line_survives_coarse_graining,
    noncontextual_assignment_count,
    observables_are_dichotomic,
)


class GateQ08Contextuality(unittest.TestCase):
    """Amplitude Gate Q08: state-independent contextuality and its coarse-graining fate.

    The Peres-Mermin square is an exact Kochen-Specker contradiction over Q(i): no
    context-independent value assignment exists at any state. Unlike the complex phase
    of Q07, this contextuality is a fine-grained resource that the single-qubit
    coarse-graining destroys, making it resolution dependent.
    """

    def test_magic_square_shape(self) -> None:
        self.assertEqual(len(MAGIC_SQUARE), 3)
        self.assertTrue(all(len(row) == 3 for row in MAGIC_SQUARE))

    def test_observables_are_dichotomic(self) -> None:
        self.assertTrue(observables_are_dichotomic())

    def test_lines_are_jointly_measurable(self) -> None:
        self.assertTrue(lines_are_jointly_measurable())

    def test_exactly_one_line_is_negative(self) -> None:
        self.assertTrue(line_products_match_signs())

    def test_no_noncontextual_assignment_exists(self) -> None:
        # State-independent Kochen-Specker contradiction: 0 of 512 assignments work.
        self.assertEqual(noncontextual_assignment_count(), 0)
        self.assertTrue(kochen_specker_contradiction())

    def test_contextuality_is_destroyed_by_coarse_graining(self) -> None:
        # Only the two observables trivial on the erased qubit survive the trace.
        self.assertEqual(coarse_grained_surviving_observables(), 2)
        # With seven observables gone, every line is broken: no contradiction remains.
        self.assertTrue(no_line_survives_coarse_graining())


if __name__ == "__main__":
    unittest.main()
