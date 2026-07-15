import unittest

from amplitude_bootstrap import (
    channel_preserves_trace,
    choi_rank,
    environment_decoherence_census,
    fixed_environment_channel,
)
from amplitude_bootstrap.coarse_graining import (
    DecoherenceRow,
    ENVIRONMENTS,
    ONE_QUBIT_GATES,
    _CNOT,
    _I2,
    _R,
    _S,
    local_channels_are_environment_independent,
)
from amplitude_bootstrap.linalg import kron


class GateQ02FixedEnvironmentDecoherence(unittest.TestCase):
    """Amplitude Gate Q02: irreversibility emerging under a fixed environment."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = environment_decoherence_census()
        cls.environments = dict(ENVIRONMENTS)

    def test_every_channel_is_trace_preserving(self) -> None:
        for row in self.census:
            self.assertEqual(row.trace_preserving, 144)

    def test_census_matches_exact_expected_counts(self) -> None:
        self.assertEqual(
            self.census,
            (
                DecoherenceRow("zero", 72, 72, 72, 144),
                DecoherenceRow("one", 72, 72, 72, 144),
                DecoherenceRow("plus", 72, 72, 72, 144),
                DecoherenceRow("plus_i", 36, 108, 108, 144),
                DecoherenceRow("mixed", 36, 108, 108, 144),
            ),
        )

    def test_all_decoherence_comes_from_entangling_dynamics(self) -> None:
        for row in self.census:
            self.assertEqual(row.decohering, row.decohering_entangling)
            self.assertGreaterEqual(row.reversible, 36)

    def test_mixed_environment_separates_interaction_cleanly(self) -> None:
        mixed = next(row for row in self.census if row.environment == "mixed")
        self.assertEqual(mixed.reversible, 36)
        self.assertEqual(mixed.decohering, 108)

    def test_local_unitaries_never_decohere_and_ignore_environment(self) -> None:
        for gate in ONE_QUBIT_GATES:
            self.assertTrue(local_channels_are_environment_independent(gate))
            channel = fixed_environment_channel(kron(gate, _I2), self.environments["mixed"])
            self.assertEqual(choi_rank(channel), 1)

    def test_reversible_microscopic_dynamics_yields_irreversible_channel(self) -> None:
        channel = fixed_environment_channel(_CNOT, self.environments["mixed"])
        self.assertTrue(channel_preserves_trace(channel))
        self.assertEqual(choi_rank(channel), 2)

    def test_decoherence_depends_on_the_environment_state(self) -> None:
        eigenstate_env = fixed_environment_channel(_CNOT, self.environments["plus"])
        coherent_env = fixed_environment_channel(_CNOT, self.environments["plus_i"])
        self.assertEqual(choi_rank(eigenstate_env), 1)
        self.assertEqual(choi_rank(coherent_env), 2)


if __name__ == "__main__":
    unittest.main()
