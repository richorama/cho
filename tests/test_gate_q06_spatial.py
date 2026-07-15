import unittest

from amplitude_bootstrap.spatial import (
    RecursionSummary,
    chain_ensemble,
    partial_trace_qubit,
    recursion_summary,
)
from amplitude_bootstrap.linalg import kron
from amplitude_bootstrap.coarse_graining import _I2, _X


class GateQ06Spatial(unittest.TestCase):
    """Amplitude Gate Q06: nested spatial coarse-graining of a three-qubit chain.

    Two nested blockings (trace qubit C, then trace qubit B) form a genuine spatial
    recursion. Each blocking removes any dynamics coupling across the newly erased
    boundary, and the surviving effective structure contracts in parameter count at
    every level while staying reversible.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = recursion_summary()

    def test_ensemble_size_is_exact(self) -> None:
        # 3 single-qubit gates on each of 3 sites, times 3 entangler layers.
        self.assertEqual(len(chain_ensemble()), 81)
        self.assertEqual(self.summary.total, 81)

    def test_partial_trace_of_a_product_forgets_the_traced_factor(self) -> None:
        product = kron(kron(_X, _I2), _I2)  # a kron b kron c on three qubits
        # Tracing the last qubit multiplies by Tr(c) = Tr(I2) = 2 and drops c.
        traced = partial_trace_qubit(product, 3, 2)
        two = _I2[0][0] + _I2[1][1]
        expected = tuple(
            tuple(value * two for value in row) for row in kron(_X, _I2)
        )
        self.assertEqual(traced, expected)

    def test_first_blocking_keeps_only_boundary_respecting_dynamics(self) -> None:
        # Tracing C keeps non-interacting products and A-B interactions, drops B-C.
        self.assertEqual(self.summary.level1_survivors, 54)

    def test_second_blocking_keeps_only_non_interacting_products(self) -> None:
        self.assertEqual(self.summary.level2_survivors, 27)
        self.assertEqual(self.summary.interacting_reaching_level2, 0)

    def test_bottom_level_dynamics_is_reversible(self) -> None:
        self.assertTrue(self.summary.level2_all_reversible)

    def test_parameters_contract_at_every_level(self) -> None:
        # Distinct effective channels shrink 81 members -> 18 -> 3 as factors drop.
        self.assertEqual(self.summary.distinct_level1_channels, 18)
        self.assertEqual(self.summary.distinct_level2_channels, 3)
        self.assertLess(
            self.summary.distinct_level2_channels,
            self.summary.distinct_level1_channels,
        )

    def test_summary_is_the_declared_type(self) -> None:
        self.assertIsInstance(self.summary, RecursionSummary)


if __name__ == "__main__":
    unittest.main()
