import unittest

from amplitude_bootstrap.spatial4 import (
    Recursion4Summary,
    chain_ensemble,
    recursion_summary,
)


class GateQ10Dimension(unittest.TestCase):
    """Amplitude Gate Q10: dimension robustness of the nested spatial recursion.

    Gate Q06's three-qubit findings are rerun one dimension up, on a four-qubit chain
    A-B-C-D with a genuine three-level recursion (trace D, then C, then B). Each nested
    blocking removes exactly the coupling across the newly erased boundary, no interacting
    member reaches the bottom, the surviving law is reversible, parameters contract
    monotonically, and the irreducible complex phase (Q07) still survives. The structural
    story is not an artefact of the smallest chain.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = recursion_summary()

    def test_ensemble_size_is_exact(self) -> None:
        # {I, S} on each of 4 sites (16 products) times 4 boundary entanglers.
        self.assertEqual(len(chain_ensemble()), 64)
        self.assertEqual(self.summary.total, 64)

    def test_each_blocking_removes_its_boundary_coupling(self) -> None:
        # 64 -> 48 (trace D drops cnot_cd) -> 32 (trace C drops cnot_bc)
        # -> 16 (trace B drops cnot_ab). Each level removes exactly 16 members.
        self.assertEqual(self.summary.level1_survivors, 48)
        self.assertEqual(self.summary.level2_survivors, 32)
        self.assertEqual(self.summary.level3_survivors, 16)

    def test_no_interacting_member_reaches_the_bottom(self) -> None:
        self.assertEqual(self.summary.interacting_reaching_level2, 16)
        self.assertEqual(self.summary.interacting_reaching_level3, 0)

    def test_bottom_level_dynamics_is_reversible(self) -> None:
        self.assertTrue(self.summary.level3_all_reversible)

    def test_parameters_contract_monotonically(self) -> None:
        self.assertEqual(self.summary.distinct_level1_channels, 24)
        self.assertEqual(self.summary.distinct_level2_channels, 8)
        self.assertEqual(self.summary.distinct_level3_channels, 2)
        self.assertLess(
            self.summary.distinct_level3_channels,
            self.summary.distinct_level2_channels,
        )
        self.assertLess(
            self.summary.distinct_level2_channels,
            self.summary.distinct_level1_channels,
        )

    def test_complex_phase_survives_to_the_bottom(self) -> None:
        # Exactly one of the two bottom channels is genuinely complex (the S factor).
        self.assertEqual(self.summary.complex_level3_channels, 1)

    def test_summary_is_the_declared_type(self) -> None:
        self.assertIsInstance(self.summary, Recursion4Summary)


if __name__ == "__main__":
    unittest.main()
