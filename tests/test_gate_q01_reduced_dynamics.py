import unittest

from amplitude_bootstrap import (
    choi_rank,
    partial_trace_b,
    reduced_channel,
    reduced_dynamics_census,
)
from amplitude_bootstrap.coarse_graining import (
    ONE_QUBIT_GATES,
    _CNOT,
    _CZ,
    _I2,
    _R,
    _S,
    _SWAP,
    _apply_channel,
    _basis_operator,
    ensemble,
)
from amplitude_bootstrap.gaussian import ONE, ZERO, Gaussian
from amplitude_bootstrap.linalg import dagger, kron, matmul


class GateQ01ReducedDynamics(unittest.TestCase):
    """Amplitude Gate Q01: when does a coarse qubit evolve by an autonomous law?"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = reduced_dynamics_census()

    def test_partial_trace_of_identity_is_scaled_identity(self) -> None:
        identity4 = tuple(
            tuple(ONE if r == c else ZERO for c in range(4)) for r in range(4)
        )
        self.assertEqual(
            partial_trace_b(identity4),
            ((Gaussian(2), ZERO), (ZERO, Gaussian(2))),
        )

    def test_ensemble_size_is_declared_and_finite(self) -> None:
        self.assertEqual(self.census.ensemble_size, 144)
        self.assertEqual(len(ensemble()), 144)

    def test_autonomous_law_selects_exactly_the_noninteracting_unitaries(self) -> None:
        self.assertEqual(self.census.autonomous, 36)
        self.assertEqual(self.census.autonomous_local, 36)
        self.assertEqual(self.census.autonomous_entangling, 0)
        self.assertEqual(self.census.entangling_total, 108)

    def test_every_survivor_is_reversible_no_decoherence_emerges(self) -> None:
        self.assertEqual(self.census.reversible, 36)
        self.assertEqual(self.census.decohering, 0)

    def test_local_product_reduces_to_conjugation_by_the_visible_factor(self) -> None:
        channel = reduced_channel(kron(_R, _S))
        self.assertIsNotNone(channel)
        self.assertEqual(choi_rank(channel), 1)
        for i in range(2):
            for j in range(2):
                basis = _basis_operator(2, i, j)
                expected = matmul(matmul(_R, basis), dagger(_R))
                self.assertEqual(_apply_channel(channel, basis), expected)

    def test_entangling_gates_admit_no_autonomous_coarse_law(self) -> None:
        self.assertIsNone(reduced_channel(_CNOT))
        self.assertIsNone(reduced_channel(_CZ))
        self.assertIsNone(reduced_channel(_SWAP))

    def test_survivors_are_precisely_the_local_tagged_members(self) -> None:
        for tag, unitary in ensemble():
            autonomous = reduced_channel(unitary) is not None
            self.assertEqual(autonomous, tag == "local")

    def test_pythagorean_rotation_is_exactly_unitary(self) -> None:
        product = matmul(dagger(_R), _R)
        self.assertEqual(product, ((ONE, ZERO), (ZERO, ONE)))


if __name__ == "__main__":
    unittest.main()
