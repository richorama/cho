from fractions import Fraction
import unittest

from observer_bootstrap import FiniteExperiment, conjugate_experiment
from observer_bootstrap.census import representation_invariance_census


class Gate00RepresentationInvariance(unittest.TestCase):
    """Every Gate 00 scientific claim is an executable test contract."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = representation_invariance_census(maximum_dimension=5)

    def test_exhaustive_census_size(self) -> None:
        self.assertEqual(self.census.exact_checks, 2_341_760)

    def test_operational_probabilities_are_exactly_invariant(self) -> None:
        self.assertEqual(self.census.operational_mismatches, 0)

    def test_label_sensitive_control_is_rejected(self) -> None:
        self.assertEqual(self.census.label_discrepancies, 1_871_440)

    def test_fractional_preparation_is_invariant(self) -> None:
        experiment = FiniteExperiment(
            preparation=(Fraction(1, 3), Fraction(2, 3), Fraction(0)),
            update=(1, 2, 0),
            effect=(Fraction(0), Fraction(1, 2), Fraction(1)),
        )
        translated = conjugate_experiment(experiment, (2, 0, 1))
        self.assertEqual(translated.probability(), experiment.probability())

    def test_invalid_permutation_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            FiniteExperiment(
                preparation=(Fraction(1), Fraction(0)),
                update=(0, 0),
                effect=(Fraction(0), Fraction(1)),
            )