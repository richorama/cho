import unittest

from amplitude_bootstrap.recursion import (
    ROTATION,
    ContractionResult,
    SurvivorComparison,
    composition_is_closed_and_reversible,
    effective_channel_contraction,
    rotated_survivors_all_reversible,
    survivor_comparison,
)


class GateQ05Recursion(unittest.TestCase):
    """Amplitude Gate Q05: a different blocking, and parameter contraction.

    Level 2 requires effective structure to survive a *structurally different*
    coarse-graining and to not grow in parameter count under repeated blocking.
    A rotated factorisation (conjugate by CNOT, then trace) supplies the different
    blocking; the collapse of ``a kron b`` survivors to environment-free channels
    plus their closure under composition supplies the contraction and stability.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.comparison = survivor_comparison()
        cls.contraction = effective_channel_contraction()

    def test_rotation_is_self_inverse(self) -> None:
        from amplitude_bootstrap.linalg import identity, matmul

        self.assertEqual(matmul(ROTATION, ROTATION), identity(4))

    def test_rotated_factorisation_is_a_different_coarse_graining(self) -> None:
        self.assertIsInstance(self.comparison, SurvivorComparison)
        self.assertEqual(self.comparison.computational, 36)
        self.assertEqual(self.comparison.rotated, 16)
        # Genuinely inequivalent: not a relabelling of the same survivor set.
        self.assertNotEqual(self.comparison.rotated, self.comparison.computational)
        self.assertEqual(self.comparison.shared, 12)
        self.assertEqual(self.comparison.rotated_only, 4)

    def test_rotated_survivors_stay_reversible_and_nonclassical(self) -> None:
        self.assertTrue(rotated_survivors_all_reversible())

    def test_environment_factor_is_forgotten(self) -> None:
        self.assertIsInstance(self.contraction, ContractionResult)
        self.assertTrue(self.contraction.environment_is_forgotten)

    def test_survivors_contract_to_six_effective_channels(self) -> None:
        self.assertEqual(self.contraction.local_survivors, 36)
        self.assertEqual(self.contraction.distinct_effective_channels, 6)
        self.assertLess(
            self.contraction.distinct_effective_channels,
            self.contraction.local_survivors,
        )

    def test_recursion_does_not_grow_the_parameter_class(self) -> None:
        self.assertTrue(composition_is_closed_and_reversible())


if __name__ == "__main__":
    unittest.main()
