import unittest

from observer_bootstrap.census import (
    RobustnessCensus,
    deterministic_robustness_census,
    is_constant_or_identity,
    is_single_target_reset_mixture,
    is_universally_lumpable_stochastic,
    partitions_grouped_by_shape,
    stochastic_robustness_census,
)
from observer_bootstrap.coarse_graining import (
    canonical_deterministic_law,
    canonical_stochastic_law,
    rational_stochastic_updates,
)


class Gate02BlockingRobustness(unittest.TestCase):
    """Observer-independent blocking leaves only identity/reset dynamics."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.deterministic_4, cls.deterministic_universal_4, cls.deterministic_updates_4 = (
            deterministic_robustness_census(4)
        )
        cls.deterministic_5, cls.deterministic_universal_5, cls.deterministic_updates_5 = (
            deterministic_robustness_census(5)
        )
        (
            cls.stochastic_4,
            cls.stochastic_universal_4,
            cls.stochastic_updates_4,
        ) = stochastic_robustness_census(4)

    def test_partition_shapes_are_relabeling_invariant_families(self) -> None:
        self.assertEqual(
            {shape: len(partitions) for shape, partitions in partitions_grouped_by_shape(4).items()},
            {(3, 1): 4, (2, 2): 3, (2, 1, 1): 6},
        )
        self.assertEqual(
            {shape: len(partitions) for shape, partitions in partitions_grouped_by_shape(5).items()},
            {(4, 1): 5, (3, 2): 10, (3, 1, 1): 10, (2, 2, 1): 15, (2, 1, 1, 1): 10},
        )

    def test_weak_favorable_partition_control_is_nearly_generic(self) -> None:
        self.assertEqual(
            self.deterministic_4,
            RobustnessCensus(256, 242, 5, 5),
        )
        self.assertEqual(
            self.deterministic_5,
            RobustnessCensus(3125, 3101, 6, 6),
        )
        self.assertEqual(
            self.stochastic_4,
            RobustnessCensus(10000, 6766, 15, 9),
        )

    def test_deterministic_survivors_are_only_constants_and_identity(self) -> None:
        self.assertEqual(len(self.deterministic_updates_4), 5)
        self.assertEqual(len(self.deterministic_updates_5), 6)
        self.assertTrue(all(map(is_constant_or_identity, self.deterministic_updates_4)))
        self.assertTrue(all(map(is_constant_or_identity, self.deterministic_updates_5)))

    def test_universally_lumpable_stochastic_family_has_exact_form(self) -> None:
        characterized = tuple(
            update
            for update in rational_stochastic_updates(4, 2)
            if is_universally_lumpable_stochastic(update)
        )
        self.assertEqual(characterized, self.stochastic_universal_4)
        self.assertEqual(len(characterized), 15)

    def test_shape_compatible_stochastic_survivors_are_reset_mixtures(self) -> None:
        self.assertEqual(len(self.stochastic_updates_4), 9)
        self.assertTrue(all(map(is_single_target_reset_mixture, self.stochastic_updates_4)))

    def test_law_canonicalization_removes_coarse_labels(self) -> None:
        self.assertEqual(canonical_deterministic_law((1, 1)), (0, 0))
        self.assertEqual(
            canonical_stochastic_law(((0, 1), (0, 1))),
            canonical_stochastic_law(((1, 0), (1, 0))),
        )