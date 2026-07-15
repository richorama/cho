import unittest

from observer_bootstrap.local_dynamics import (
    LocalFlowRow,
    block_pairs,
    decimate_pair,
    elementary_step,
    essential_inputs,
    induced_elementary_rule,
    is_additive_elementary_rule,
    is_trivial_elementary_rule,
    local_blocking_flow_census,
    parity_pair,
)


class Gate03LocalRecursiveConsistency(unittest.TestCase):
    """Local product structure must support a nontrivial exact blocking flow."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.flow = local_blocking_flow_census()

    def test_elementary_rule_convention_matches_known_rule_90_step(self) -> None:
        configuration = (0, 0, 1, 0, 0)
        self.assertEqual(elementary_step(90, configuration), (0, 1, 0, 1, 0))

    def test_blockings_are_distinct_local_product_maps(self) -> None:
        configuration = (1, 1, 0, 1, 1, 0)
        self.assertEqual(block_pairs(configuration, decimate_pair), (1, 0, 1))
        self.assertEqual(block_pairs(configuration, parity_pair), (0, 1, 1))

    def test_induced_rules_are_stable_across_three_ring_sizes(self) -> None:
        for row in self.flow:
            self.assertEqual(
                {
                    induced_elementary_rule(
                        row.microscopic_rule, size, decimate_pair, 2
                    )
                    for size in (6, 8, 10)
                },
                {row.decimation_rule},
            )
            self.assertEqual(
                {
                    induced_elementary_rule(
                        row.microscopic_rule, size, parity_pair, 2
                    )
                    for size in (6, 8, 10)
                },
                {row.parity_rule},
            )

    def test_one_step_blocking_leaves_only_noninteracting_controls(self) -> None:
        one_step = local_blocking_flow_census(microscopic_steps=1)
        self.assertEqual(
            tuple(row.microscopic_rule for row in one_step),
            (0, 51, 204, 255),
        )

    def test_two_step_blocking_has_twenty_exact_survivors(self) -> None:
        self.assertEqual(
            self.flow,
            (
                LocalFlowRow(0, 0, 0),
                LocalFlowRow(8, 0, 0),
                LocalFlowRow(15, 240, 240),
                LocalFlowRow(51, 204, 204),
                LocalFlowRow(60, 60, 60),
                LocalFlowRow(64, 0, 0),
                LocalFlowRow(85, 170, 170),
                LocalFlowRow(90, 90, 90),
                LocalFlowRow(102, 102, 102),
                LocalFlowRow(105, 150, 150),
                LocalFlowRow(150, 150, 150),
                LocalFlowRow(153, 153, 102),
                LocalFlowRow(165, 165, 90),
                LocalFlowRow(170, 170, 170),
                LocalFlowRow(195, 195, 60),
                LocalFlowRow(204, 204, 204),
                LocalFlowRow(239, 255, 0),
                LocalFlowRow(240, 240, 240),
                LocalFlowRow(253, 255, 0),
                LocalFlowRow(255, 255, 0),
            ),
        )

    def test_both_effective_flows_remain_inside_survivor_set(self) -> None:
        survivors = {row.microscopic_rule for row in self.flow}
        self.assertTrue(
            all(
                row.decimation_rule in survivors and row.parity_rule in survivors
                for row in self.flow
            )
        )

    def test_common_fixed_points_include_four_interacting_rules(self) -> None:
        common_fixed_points = {
            row.microscopic_rule
            for row in self.flow
            if row.decimation_rule == row.microscopic_rule
            and row.parity_rule == row.microscopic_rule
        }
        interacting = {
            rule
            for rule in common_fixed_points
            if sum(essential_inputs(rule)) >= 2
            and not is_trivial_elementary_rule(rule)
        }
        self.assertEqual(common_fixed_points, {0, 60, 90, 102, 150, 170, 204, 240})
        self.assertEqual(interacting, {60, 90, 102, 150})
        self.assertTrue(all(map(is_additive_elementary_rule, interacting)))


if __name__ == "__main__":
    unittest.main()