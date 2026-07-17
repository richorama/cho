import unittest
from fractions import Fraction

from amplitude_bootstrap.frame_function import (
    DimensionalWitness,
    TheoremWitness,
    dimensional_necessity_witnesses,
    theorem_witnesses,
)


class BornRuleTheorem(unittest.TestCase):
    """Exact certificate for the Born-rule selection theorem (BORN_RULE_THEOREM.md).

    On a single explicit configuration in C^3 the three ingredients of the proof are
    realised exactly over Q(i): Parseval sufficiency for r = 2, a complement-split
    necessity witness for r = 4 and r = 6, and monomial (relabel-with-phase) invariance
    showing that only genuine superposition can expose the alternatives.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.witness = theorem_witnesses()

    def test_is_the_declared_type(self) -> None:
        self.assertIsInstance(self.witness, TheoremWitness)

    def test_born_is_split_independent_and_parseval(self) -> None:
        # r = 2: both complement-splits give the frame total <s|s> = 3 for s = (1,1,1).
        self.assertEqual(self.witness.parseval_constant, Fraction(3))
        self.assertTrue(self.witness.born_split_equal)

    def test_alternatives_are_split_dependent(self) -> None:
        # r = 4 and r = 6: the two splits give different exact totals, so the normalised
        # rule is contextual. Basis A keeps the total at 3; basis B does not.
        self.assertEqual(
            self.witness.alternative_split_totals,
            (
                (2, Fraction(3), Fraction(3027, 625)),
                (3, Fraction(3), Fraction(5331, 625)),
            ),
        )
        for _, total_a, total_b in self.witness.alternative_split_totals:
            self.assertNotEqual(total_a, total_b)

    def test_monomial_relabelling_exposes_nothing(self) -> None:
        # A permutation-with-phase leaves the total unchanged for every exponent.
        self.assertTrue(self.witness.monomial_invariant_for_all_exponents)


class BornRuleNecessityAcrossDimensions(unittest.TestCase):
    """The complement-split necessity witness is exact in dimensions 3, 4 and 5.

    Each case shares the effect e0 between two orthonormal bases differing only by a
    rational rotation of the {1,2} complement plane, on s = (1,...,1). For r = 2 the two
    frame totals agree and equal <s|s> = d (Born / Parseval); for r = 4 and r = 6 they
    differ, so the Born exponent is necessary in every dimension d >= 3, not just d = 3.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.witnesses = dimensional_necessity_witnesses((3, 4, 5))

    def test_types_and_dimensions(self) -> None:
        self.assertEqual([w.dimension for w in self.witnesses], [3, 4, 5])
        for w in self.witnesses:
            self.assertIsInstance(w, DimensionalWitness)

    def test_born_total_is_parseval_in_every_dimension(self) -> None:
        for w in self.witnesses:
            self.assertEqual(w.parseval_constant, Fraction(w.dimension))
            r, total_a, total_b = w.splits[0]
            self.assertEqual(r, 2)
            self.assertEqual(total_a, Fraction(w.dimension))
            self.assertEqual(total_b, Fraction(w.dimension))

    def test_alternatives_split_and_match_closed_form(self) -> None:
        # split_A stays at d; split_B = (d - 2) + c_r/625 with c_4 = 2402, c_6 = 4706.
        expected = {4: Fraction(2402, 625), 6: Fraction(4706, 625)}
        for w in self.witnesses:
            d = w.dimension
            for r, total_a, total_b in w.splits[1:]:
                self.assertEqual(total_a, Fraction(d))
                self.assertEqual(total_b, Fraction(d - 2) + expected[r])
                self.assertNotEqual(total_a, total_b)

    def test_d3_reproduces_single_configuration_theorem(self) -> None:
        # The d = 3 case matches the totals certified by theorem_witnesses().
        d3 = next(w for w in self.witnesses if w.dimension == 3)
        self.assertEqual(
            d3.splits,
            (
                (2, Fraction(3), Fraction(3)),
                (4, Fraction(3), Fraction(3027, 625)),
                (6, Fraction(3), Fraction(5331, 625)),
            ),
        )


if __name__ == "__main__":
    unittest.main()
