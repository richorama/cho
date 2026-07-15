from fractions import Fraction
import unittest

from observer_bootstrap import FiniteExperiment, conjugate_experiment


class RepresentationInvarianceTests(unittest.TestCase):
    def test_conjugation_preserves_probability(self) -> None:
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


if __name__ == "__main__":
    unittest.main()