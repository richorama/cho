import unittest

from amplitude_bootstrap.phase import (
    PhaseSurvival,
    complex_phase_survives_recursion,
    complex_phase_survives_rotated_blocking,
    conjugation_channel,
    is_genuinely_complex,
    phase_gate_is_genuinely_complex,
    real_gates_are_real_superoperators,
    witness_invariant_under_real_basis_change,
)
from amplitude_bootstrap.coarse_graining import _I2, _S


class GateQ07Phase(unittest.TestCase):
    """Amplitude Gate Q07: an irreducible complex phase survives the recursion.

    The complex-phase witness is nonzero iff a channel cannot be realised with real
    amplitudes, and it is invariant under any real change of basis. Gate Q06 showed the
    recursion filters out interaction; this gate shows it does not filter out the
    complex phase, which was never selected for — the Level-3 signature.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.survival = complex_phase_survives_recursion()

    def test_real_amplitude_gates_have_real_channels(self) -> None:
        self.assertTrue(real_gates_are_real_superoperators())

    def test_phase_gate_is_genuinely_complex(self) -> None:
        self.assertTrue(phase_gate_is_genuinely_complex())
        # The identity channel is the real reference point.
        self.assertFalse(is_genuinely_complex(conjugation_channel(_I2)))

    def test_witness_is_a_real_basis_invariant(self) -> None:
        self.assertTrue(witness_invariant_under_real_basis_change())

    def test_complex_phase_survives_to_the_bottom_of_the_recursion(self) -> None:
        self.assertIsInstance(self.survival, PhaseSurvival)
        # Contrast with Q06: interaction reaches 0 at the bottom, the phase does not.
        self.assertEqual(self.survival.distinct_level2, 3)
        self.assertEqual(self.survival.complex_level2, 1)
        self.assertGreater(self.survival.complex_level2, 0)

    def test_complex_phase_is_present_at_the_intermediate_level(self) -> None:
        self.assertEqual(self.survival.distinct_level1, 18)
        self.assertEqual(self.survival.complex_level1, 10)

    def test_complex_phase_survives_a_second_blocking(self) -> None:
        # Robustness: the rotated (CNOT) blocking also keeps genuinely complex channels.
        self.assertEqual(complex_phase_survives_rotated_blocking(), 3)


if __name__ == "__main__":
    unittest.main()
