import unittest
from fractions import Fraction

from amplitude_bootstrap import (
    closure_defect,
    controlled_rotation,
    coupling_flow,
    defect_spectrum,
    exact_defect_matches_reduced_channel,
    tolerance_ladder,
)
from amplitude_bootstrap.coarse_graining import _CNOT, _CZ, _SWAP, ensemble, kron
from amplitude_bootstrap.coarse_graining import _I2, _R, _S


class GateQ13ApproximateClosure(unittest.TestCase):
    """Amplitude Gate Q13: interaction is observer-consistent *approximately*.

    Gates Q01/Q09 proved an exact no-go: only the 36 non-interacting product
    unitaries admit an exact autonomous coarse law. Q13 relaxes exact closure to a
    bounded misfit, measured by the exact least-squares Frobenius residual of the
    best-fit autonomous law (the *closure defect*, an exact rational over Q(i)).

    Two exact facts follow: the defect reproduces the exact no-go in the limit
    ``eps -> 0`` (defect zero iff product unitary) and grows monotonically with the
    declared tolerance, admitting interaction at a quantified cost; and along a
    controlled-rotation coupling family the defect is exactly ``4 b^2``, flowing to
    zero quadratically as the coupling ``b -> 0``. Weakly interacting microscopic
    dynamics is approximately autonomous.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.spectrum = defect_spectrum()
        cls.flow = coupling_flow()

    # --- Recovery of the exact Q01/Q09 no-go as the eps -> 0 limit. -------------

    def test_ensemble_size_is_the_declared_144(self) -> None:
        self.assertEqual(len(self.spectrum), 144)

    def test_exact_closure_selects_precisely_the_36_products(self) -> None:
        exact = [row for row in self.spectrum if row.exactly_autonomous]
        self.assertEqual(len(exact), 36)
        self.assertTrue(all(row.tag == "local" for row in exact))

    def test_every_entangler_has_a_strictly_positive_defect(self) -> None:
        entanglers = [row for row in self.spectrum if row.tag != "local"]
        self.assertEqual(len(entanglers), 108)
        self.assertTrue(all(row.defect > 0 for row in entanglers))

    def test_defect_zero_matches_the_exact_reduced_channel(self) -> None:
        # Q13's continuous defect and Q01's exact solvability agree everywhere.
        self.assertTrue(exact_defect_matches_reduced_channel())

    # --- The defect is a local-unitary invariant of the interaction. -----------

    def test_defect_depends_only_on_the_entangler_not_the_local_dressing(self) -> None:
        # All 36 local dressings of each entangler share one defect: the closure
        # defect measures genuinely non-local content only.
        by_tag = {}
        for row in self.spectrum:
            by_tag.setdefault(row.tag, set()).add(row.defect)
        self.assertEqual(by_tag["local"], {Fraction(0)})
        self.assertEqual(by_tag["cz"], {Fraction(4)})
        self.assertEqual(by_tag["cnot"], {Fraction(4)})
        self.assertEqual(by_tag["swap"], {Fraction(6)})

    def test_bare_entangler_defects_are_exact(self) -> None:
        self.assertEqual(closure_defect(_CZ), Fraction(4))
        self.assertEqual(closure_defect(_CNOT), Fraction(4))
        self.assertEqual(closure_defect(_SWAP), Fraction(6))
        # Swap, which fully exchanges system and environment, is the least autonomous.
        self.assertGreater(closure_defect(_SWAP), closure_defect(_CNOT))

    def test_local_products_have_exactly_zero_defect(self) -> None:
        self.assertEqual(closure_defect(kron(_R, _S)), Fraction(0))
        self.assertEqual(closure_defect(kron(_S, _I2)), Fraction(0))

    # --- Tolerance relaxation: interaction survives at a cost. ------------------

    def test_raising_tolerance_admits_interaction_monotonically(self) -> None:
        ladder = tolerance_ladder(
            (Fraction(0), Fraction(4), Fraction(5), Fraction(6))
        )
        self.assertEqual(ladder.exact_survivors, 36)
        self.assertTrue(ladder.exact_are_all_local)
        self.assertTrue(ladder.entanglers_all_positive)
        self.assertTrue(ladder.monotone)
        self.assertEqual(
            ladder.ladder,
            (
                (Fraction(0), 36, 0),     # eps = 0 : Q01 no-go, no interaction
                (Fraction(4), 108, 72),   # eps = 4 : cz and cnot admitted
                (Fraction(5), 108, 72),   # eps = 5 : plateau
                (Fraction(6), 144, 108),  # eps = 6 : every interaction admitted
            ),
        )

    # --- The coupling flow: defect = 4 b^2 -> 0 as b -> 0. ----------------------

    def test_zero_coupling_is_exactly_autonomous(self) -> None:
        self.assertTrue(self.flow.zero_coupling_is_exact)
        self.assertEqual(self.flow.points[0].coupling, Fraction(0))
        self.assertEqual(self.flow.points[0].defect, Fraction(0))

    def test_every_nonzero_coupling_is_inexact(self) -> None:
        self.assertTrue(self.flow.positive_coupling_is_inexact)

    def test_defect_is_exactly_four_b_squared(self) -> None:
        for point in self.flow.points:
            self.assertEqual(point.defect, 4 * point.coupling * point.coupling)

    def test_defect_flows_monotonically_to_zero_with_coupling(self) -> None:
        self.assertTrue(self.flow.strictly_increasing)
        self.assertTrue(self.flow.flows_to_zero)

    def test_controlled_rotation_is_exactly_unitary(self) -> None:
        from amplitude_bootstrap.linalg import dagger, matmul, identity

        gate = controlled_rotation(Fraction(3, 5), Fraction(4, 5))
        self.assertEqual(matmul(dagger(gate), gate), identity(4))

    def test_controlled_rotation_rejects_non_pythagorean_pairs(self) -> None:
        with self.assertRaises(ValueError):
            controlled_rotation(Fraction(1, 2), Fraction(1, 2))


if __name__ == "__main__":
    unittest.main()
