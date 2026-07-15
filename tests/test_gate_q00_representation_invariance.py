from fractions import Fraction
import unittest

from amplitude_bootstrap import (
    AmplitudeExperiment,
    MonomialUnitary,
    conjugate_experiment,
)
from amplitude_bootstrap.census import representation_invariance_census
from amplitude_bootstrap.gaussian import Gaussian, born_probability, from_int_pairs


class GateQ00RepresentationInvariance(unittest.TestCase):
    """Amplitude premise, Gate Q00: basis changes cannot move a Born probability."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = representation_invariance_census(dimensions=(2, 3))

    def test_exhaustive_census_size(self) -> None:
        self.assertEqual(self.census.exact_checks, 261_632)

    def test_born_probabilities_are_exactly_invariant(self) -> None:
        self.assertEqual(self.census.operational_mismatches, 0)

    def test_basis_sensitive_control_is_rejected(self) -> None:
        self.assertEqual(self.census.basis_discrepancies, 3_136)

    def test_superposition_gives_one_half(self) -> None:
        effect = from_int_pairs(((1, 0), (0, 0)))
        state = from_int_pairs(((1, 0), (1, 0)))
        self.assertEqual(born_probability(effect, state), Fraction(1, 2))

    def test_relative_phase_forces_exact_orthogonality(self) -> None:
        effect = from_int_pairs(((1, 0), (0, 1)))
        state = from_int_pairs(((1, 0), (0, -1)))
        self.assertEqual(born_probability(effect, state), Fraction(0))

    def test_phase_change_is_a_genuine_amplitude_representation_change(self) -> None:
        experiment = AmplitudeExperiment(
            preparation=from_int_pairs(((1, 0), (1, 0))),
            effect=from_int_pairs(((1, 0), (0, 0))),
        )
        phase_unitary = MonomialUnitary(
            image=(0, 1),
            phases=(Gaussian(Fraction(1)), Gaussian(Fraction(0), Fraction(1))),
        )
        translated = conjugate_experiment(experiment, phase_unitary)
        self.assertNotEqual(translated.preparation, experiment.preparation)
        self.assertEqual(translated.probability(), experiment.probability())

    def test_permutation_subgroup_recovers_classical_relabeling(self) -> None:
        swap = MonomialUnitary(image=(1, 0), phases=(Gaussian(Fraction(1)),) * 2)
        state = from_int_pairs(((1, 0), (0, 1)))
        self.assertEqual(swap.apply(state), from_int_pairs(((0, 1), (1, 0))))

    def test_non_unit_phase_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            MonomialUnitary(image=(0, 1), phases=(Gaussian(Fraction(2)), Gaussian(Fraction(1))))

    def test_non_permutation_image_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            MonomialUnitary(image=(0, 0), phases=(Gaussian(Fraction(1)),) * 2)


if __name__ == "__main__":
    unittest.main()
