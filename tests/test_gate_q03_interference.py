import unittest

from fractions import Fraction

from amplitude_bootstrap import (
    classicality_census,
    coherence_matches_reversibility,
    fixed_environment_channel,
    interference_visibility,
    transmits_coherence,
)
from amplitude_bootstrap.coarse_graining import ENVIRONMENTS, _CNOT
from amplitude_bootstrap.interference import ClassicalityRow, DEPHASING_CHANNEL
from amplitude_bootstrap.linalg import identity


class GateQ03Interference(unittest.TestCase):
    """Amplitude Gate Q03: interference as an unselected nonclassicality holdout."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = classicality_census()
        cls.environments = dict(ENVIRONMENTS)

    def test_classical_control_shows_no_interference(self) -> None:
        self.assertFalse(transmits_coherence(DEPHASING_CHANNEL))
        self.assertEqual(interference_visibility(DEPHASING_CHANNEL).real, Fraction(0))

    def test_reversible_channel_shows_exact_interference(self) -> None:
        visibility = interference_visibility(identity(4))
        self.assertEqual(visibility.imag, Fraction(0))
        self.assertEqual(visibility.real, Fraction(-288, 625))

    def test_census_matches_exact_expected_counts(self) -> None:
        self.assertEqual(
            self.census,
            (
                ClassicalityRow("zero", 72, 72, 36, 36),
                ClassicalityRow("one", 72, 72, 36, 36),
                ClassicalityRow("plus", 72, 72, 36, 36),
                ClassicalityRow("plus_i", 36, 108, 36, 0),
                ClassicalityRow("mixed", 36, 108, 36, 0),
            ),
        )

    def test_noninteracting_dynamics_is_always_nonclassical(self) -> None:
        for row in self.census:
            self.assertEqual(row.nonclassical_local, 36)

    def test_interaction_erases_nonclassicality_under_generic_environment(self) -> None:
        mixed = next(row for row in self.census if row.environment == "mixed")
        self.assertEqual(mixed.nonclassical_entangling, 0)
        self.assertEqual(mixed.classical, 108)
        channel = fixed_environment_channel(_CNOT, self.environments["mixed"])
        self.assertFalse(transmits_coherence(channel))
        self.assertEqual(interference_visibility(channel).real, Fraction(0))

    def test_coherence_transmission_equals_reversibility_exactly(self) -> None:
        self.assertTrue(coherence_matches_reversibility())


if __name__ == "__main__":
    unittest.main()
