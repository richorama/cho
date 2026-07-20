import unittest
from fractions import Fraction

from amplitude_bootstrap.interaction_relevance import (
    GATE_FAMILY,
    _ISWAP,
    classify,
    gate_defect_flow,
    light_cone_reach,
    relevance_census,
    sweep_summary,
)


class GateQ15InteractionRelevance(unittest.TestCase):
    """Amplitude Gate Q15: no coupling escapes the renormalisation flow.

    A broad declared family of exactly-unitary, genuinely entangling two-qubit
    generators is swept as nearest-neighbour couplings on a chain and classified by its
    closure-defect flow. Every generator is interacting (positive level-one defect) yet
    irrelevant (the defect contracts to zero under coarse-graining); none is marginal or
    relevant. Circuit depth spreads the interaction (the light-cone reach grows) but
    never makes it relevant, because each spatial decimation dilutes the defect by the
    Hilbert dimension of the traced factor. This is the amplitude echo, at the level of
    renormalisation relevance, of the campaign's non-interacting verdict.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = relevance_census(3, 1)
        cls.summary = sweep_summary(3, 1)

    # --- The family is broad, entangling, and exactly unitary. -----------------

    def test_family_is_the_declared_seven_generators(self) -> None:
        self.assertEqual(len(GATE_FAMILY), 7)
        self.assertEqual(self.summary.family_size, 7)

    def test_every_generator_is_genuinely_interacting(self) -> None:
        self.assertTrue(self.summary.all_entangling)
        self.assertTrue(all(row.level_one_positive for row in self.census))

    # --- Exact defect flows (tests own the values). ----------------------------

    def test_defect_flows_are_exact(self) -> None:
        expected = {
            "cnot": (Fraction(16), Fraction(0)),
            "cz": (Fraction(16), Fraction(4)),
            "swap": (Fraction(24), Fraction(0)),
            "iswap": (Fraction(24), Fraction(0)),
            "cs": (Fraction(8), Fraction(2)),
            "crot": (Fraction(144, 25), Fraction(576, 625)),
            "dcnot": (Fraction(24), Fraction(0)),
        }
        got = {row.name: row.defects for row in self.census}
        self.assertEqual(got, expected)

    # --- The central verdict: no coupling escapes the flow. --------------------

    def test_every_generator_is_irrelevant(self) -> None:
        self.assertTrue(self.summary.all_irrelevant)
        self.assertTrue(all(row.classification == "irrelevant" for row in self.census))

    def test_no_relevant_or_marginal_coupling_exists(self) -> None:
        self.assertEqual(self.summary.relevant_found, 0)
        self.assertEqual(self.summary.marginal_found, 0)

    def test_local_product_control_is_a_fixed_point(self) -> None:
        self.assertTrue(self.summary.local_control_is_fixed_point)

    # --- The classifier itself, on synthetic flows. ----------------------------

    def test_classifier_distinguishes_the_three_regimes(self) -> None:
        self.assertEqual(classify((Fraction(16), Fraction(4))), "irrelevant")
        self.assertEqual(classify((Fraction(4), Fraction(4))), "marginal")
        self.assertEqual(classify((Fraction(4), Fraction(9))), "relevant")
        self.assertEqual(classify((Fraction(0), Fraction(0))), "fixed_point")

    # --- Depth spreads interaction but does not make it relevant. --------------

    def test_iswap_light_cone_reach_grows_with_depth(self) -> None:
        # The number of coarse-graining steps the defect survives grows one-for-one
        # with circuit depth: interaction transports further under time.
        self.assertEqual(light_cone_reach(_ISWAP, 4, (1, 2, 3)), ((1, 1), (2, 2), (3, 3)))

    def test_iswap_stays_irrelevant_at_every_depth(self) -> None:
        for depth in (1, 2, 3):
            flow = gate_defect_flow(_ISWAP, 4, depth)
            self.assertEqual(classify(flow), "irrelevant")


if __name__ == "__main__":
    unittest.main()
