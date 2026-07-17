import unittest
from fractions import Fraction

from amplitude_bootstrap.frame_function import TheoremWitness, theorem_witnesses


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


if __name__ == "__main__":
    unittest.main()
