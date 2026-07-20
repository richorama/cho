import unittest
from fractions import Fraction

from amplitude_bootstrap.renormalization_flow import (
    coupling_chain,
    controlled_rotation,
    defect_flow,
    is_unitary,
    renormalization_flow,
)


def _pair(a_num, b_num, denom):
    return Fraction(a_num, denom), Fraction(b_num, denom)


class GateQ14RenormalizationFlow(unittest.TestCase):
    """Amplitude Gate Q14: the closure defect renormalises to zero.

    A translation-invariant nearest-neighbour controlled-rotation coupling on a qubit
    chain is coarse-grained by tracing the end qubit repeatedly. The exact closure
    defect (Gate Q13) is recorded at every level. The coupling is *irrelevant*: the
    defect is positive at every finite scale but contracts by a factor of at least four
    per step (exactly ``a^2/4`` across the coupled cut and exactly ``1/4`` deeper), so
    the coarse world flows to the non-interacting fixed point that Gates Q01/Q09 found
    exactly. Interaction is real at every resolution and renormalises away.
    """

    # --- The coupling gate and chain are exactly unitary. ----------------------

    def test_controlled_rotation_is_exactly_unitary(self) -> None:
        a, b = _pair(4, 3, 5)
        self.assertTrue(is_unitary(controlled_rotation(0, 1, a, b, 3)))
        self.assertTrue(is_unitary(coupling_chain(4, a, b)))

    def test_controlled_rotation_rejects_non_pythagorean_pairs(self) -> None:
        with self.assertRaises(ValueError):
            controlled_rotation(0, 1, Fraction(1, 2), Fraction(1, 2), 3)

    # --- The non-interacting fixed point. --------------------------------------

    def test_zero_coupling_is_an_exact_fixed_point(self) -> None:
        for n in (3, 4):
            flow = renormalization_flow(n, Fraction(1), Fraction(0))
            self.assertEqual(flow.classification, "fixed_point")
            self.assertTrue(all(defect == 0 for defect in flow.defects))

    # --- Interaction is visible at every finite scale. -------------------------

    def test_interaction_is_positive_at_every_level(self) -> None:
        for n in (3, 4):
            for a, b in (_pair(4, 3, 5), _pair(12, 5, 13)):
                flow = renormalization_flow(n, a, b)
                self.assertTrue(flow.positive_at_every_level)
                self.assertEqual(len(flow.defects), n - 1)

    # --- The exact defect vectors (tests own the values). ----------------------

    def test_three_qubit_defect_vectors_are_exact(self) -> None:
        a, b = _pair(4, 3, 5)
        self.assertEqual(defect_flow(3, a, b), (Fraction(144, 25), Fraction(576, 625)))
        a, b = _pair(12, 5, 13)
        self.assertEqual(
            defect_flow(3, a, b), (Fraction(400, 169), Fraction(14400, 28561))
        )

    def test_four_qubit_defect_vectors_are_exact(self) -> None:
        a, b = _pair(4, 3, 5)
        self.assertEqual(
            defect_flow(4, a, b),
            (Fraction(576, 25), Fraction(2304, 625), Fraction(576, 625)),
        )
        a, b = _pair(12, 5, 13)
        self.assertEqual(
            defect_flow(4, a, b),
            (Fraction(1600, 169), Fraction(57600, 28561), Fraction(14400, 28561)),
        )

    # --- The renormalisation law: irrelevant, geometric contraction. -----------

    def test_boundary_step_contracts_by_exactly_a_squared_over_four(self) -> None:
        for n in (3, 4):
            for a, b in (_pair(4, 3, 5), _pair(12, 5, 13), _pair(24, 7, 25)):
                flow = renormalization_flow(n, a, b)
                self.assertTrue(flow.boundary_ratio_is_a2_over_4)
                self.assertEqual(flow.ratios[0], a * a / 4)

    def test_deep_steps_contract_by_exactly_one_quarter(self) -> None:
        # On the four-qubit chain the second reduction (away from the coupled cut)
        # contracts by exactly 1/4, the universal deep-recursion ratio.
        for a, b in (_pair(4, 3, 5), _pair(12, 5, 13), _pair(24, 7, 25)):
            flow = renormalization_flow(4, a, b)
            self.assertTrue(flow.deep_ratios_are_quarter)
            self.assertEqual(flow.ratios[1], Fraction(1, 4))

    def test_every_step_contracts_at_least_fourfold(self) -> None:
        for n in (3, 4):
            for a, b in (_pair(4, 3, 5), _pair(12, 5, 13), _pair(24, 7, 25)):
                flow = renormalization_flow(n, a, b)
                self.assertTrue(flow.strictly_contracting)
                self.assertTrue(all(ratio <= Fraction(1, 4) for ratio in flow.ratios))

    def test_coupling_is_classified_irrelevant(self) -> None:
        for n in (3, 4):
            for a, b in (_pair(4, 3, 5), _pair(12, 5, 13), _pair(24, 7, 25)):
                self.assertEqual(
                    renormalization_flow(n, a, b).classification, "irrelevant"
                )


if __name__ == "__main__":
    unittest.main()
