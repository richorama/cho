from fractions import Fraction
import unittest

from observer_bootstrap.census import (
    CoarseCensusRow,
    deterministic_coarse_census,
    stochastic_coarse_census,
)
from observer_bootstrap.coarse_graining import (
    canonical_partitions,
    induced_deterministic_update,
    induced_stochastic_update,
    is_nontrivial_partition,
)


class Gate01ExactCoarseGraining(unittest.TestCase):
    """Every Gate 01 scientific claim is an executable test contract."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.deterministic, cls.formula_mismatches = deterministic_coarse_census()
        cls.stochastic = stochastic_coarse_census()

    def test_partition_generator_matches_bell_number(self) -> None:
        self.assertEqual(len(tuple(canonical_partitions(4))), 15)

    def test_trivial_blockings_are_excluded(self) -> None:
        partitions = tuple(canonical_partitions(4))
        nontrivial = tuple(filter(is_nontrivial_partition, partitions))
        self.assertEqual(len(nontrivial), 13)
        self.assertNotIn((0, 0, 0, 0), nontrivial)
        self.assertNotIn((0, 1, 2, 3), nontrivial)

    def test_deterministic_census(self) -> None:
        self.assertEqual(
            self.deterministic,
            {
                2: CoarseCensusRow(0, 0, 0),
                3: CoarseCensusRow(3, 81, 45),
                4: CoarseCensusRow(13, 3328, 1216),
                5: CoarseCensusRow(50, 156250, 33050),
            },
        )

    def test_deterministic_census_matches_closed_formula(self) -> None:
        self.assertEqual(self.formula_mismatches, 0)

    def test_stochastic_census(self) -> None:
        self.assertEqual(
            self.stochastic,
            {
                2: CoarseCensusRow(0, 0, 0),
                3: CoarseCensusRow(3, 648, 252),
                4: CoarseCensusRow(13, 130000, 25228),
            },
        )

    def test_closure_is_selective_but_nonempty(self) -> None:
        for row in tuple(self.deterministic.values()) + tuple(self.stochastic.values()):
            if row.pairs:
                self.assertGreater(row.survivors, 0)
                self.assertLess(row.survivors, row.pairs)

    def test_known_deterministic_positive_and_negative_examples(self) -> None:
        partition = (0, 0, 1, 1)
        self.assertEqual(
            induced_deterministic_update((2, 3, 0, 1), partition),
            (1, 0),
        )
        self.assertIsNone(
            induced_deterministic_update((0, 2, 0, 1), partition)
        )

    def test_known_stochastic_positive_and_negative_examples(self) -> None:
        half = Fraction(1, 2)
        partition = (0, 0, 1)
        positive = (
            (half, 0, half),
            (0, half, half),
            (half, half, 0),
        )
        negative = (
            (1, 0, 0),
            (0, 0, 1),
            (half, half, 0),
        )
        self.assertEqual(
            induced_stochastic_update(positive, partition),
            ((half, half), (1, 0)),
        )
        self.assertIsNone(induced_stochastic_update(negative, partition))