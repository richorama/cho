import unittest

from amplitude_bootstrap.born_selection import (
    BornSelection,
    COMPUTATIONAL,
    PERMUTED,
    PHASE_SUPERPOSED,
    REAL_SUPERPOSED,
    born_selection_census,
    contextual_mismatches,
    qubit_cannot_distinguish,
)


class GateQ11BornSelection(unittest.TestCase):
    """Amplitude Gate Q11: observer-consistency selects the Born rule.

    Among the r-norm outcome rules q_r(k) = |<e_k|s>|^r / sum_j |<e_j|s>|^r, only r = 2
    (Born) assigns a shared measurement outcome the same probability in every complete
    measurement that contains it. Every r > 2 is exposed as contextual, but only by a
    genuinely superposing change of description — a classical relabelling certifies
    nothing — and only in Hilbert dimension at least three. The Born rule is an unselected
    holdout the amplitude premise forces.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = born_selection_census()

    def test_born_is_perfectly_noncontextual(self) -> None:
        self.assertEqual(self.census.born_mismatches_under_superposition, 0)

    def test_every_other_exponent_is_contextual_under_superposition(self) -> None:
        # r = 4 (p = 2) and r = 6 (p = 3) each produce 12 contextual mismatches per
        # superposing basis, so 24 summed over the two declared superposing bases.
        self.assertEqual(
            self.census.alternative_mismatches_under_superposition,
            ((2, 24), (3, 24)),
        )

    def test_born_is_the_unique_noncontextual_exponent(self) -> None:
        self.assertTrue(self.census.born_is_uniquely_noncontextual)
        self.assertIsInstance(self.census, BornSelection)

    def test_both_real_and_complex_superposition_expose_the_alternatives(self) -> None:
        # Neither a real (Pythagorean) nor a complex (phase) rotation is special: both
        # expose r = 4 as contextual, while Born stays clean under each.
        self.assertEqual(contextual_mismatches(COMPUTATIONAL, REAL_SUPERPOSED, 1), 0)
        self.assertEqual(contextual_mismatches(COMPUTATIONAL, PHASE_SUPERPOSED, 1), 0)
        self.assertEqual(contextual_mismatches(COMPUTATIONAL, REAL_SUPERPOSED, 2), 12)
        self.assertEqual(contextual_mismatches(COMPUTATIONAL, PHASE_SUPERPOSED, 2), 12)

    def test_classical_relabelling_selects_nothing(self) -> None:
        # A permutation of outcomes leaves the weight multiset unchanged, so no exponent
        # is exposed: only superposition does the selecting.
        self.assertTrue(self.census.relabelling_exposes_nothing)
        for power in (1, 2, 3):
            self.assertEqual(contextual_mismatches(COMPUTATIONAL, PERMUTED, power), 0)

    def test_selection_requires_dimension_at_least_three(self) -> None:
        # In a qubit every exponent is non-contextual, recovering Gleason's threshold.
        self.assertTrue(qubit_cannot_distinguish())


if __name__ == "__main__":
    unittest.main()
