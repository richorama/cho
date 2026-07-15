import unittest

from observer_bootstrap.local_dynamics import essential_inputs
from observer_bootstrap.reversible_dynamics import (
    ReversibleFlowRow,
    inverse_reversible_step,
    is_affine_rule,
    recover_two_step_current,
    reversible_blocking_flow_census,
    reversible_configurations,
    reversible_step,
    reversible_trajectory_flow_census,
    second_step_record_is_one_time_padded,
)


class Gate05ReversibleRecords(unittest.TestCase):
    """Reversibility must coexist with exact local scale consistency."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.instantaneous_flow = reversible_blocking_flow_census(
            microscopic_steps=1
        )
        cls.trajectory_flow = reversible_trajectory_flow_census()

    def test_every_local_rule_is_exactly_reversible(self) -> None:
        configurations = tuple(reversible_configurations(3))
        for rule in range(256):
            for configuration in configurations:
                self.assertEqual(
                    inverse_reversible_step(rule, reversible_step(rule, configuration)),
                    configuration,
                )

    def test_record_channel_receives_the_previous_current_state(self) -> None:
        configuration = ((1, 0), (0, 1), (1, 1))
        target = reversible_step(90, configuration)
        self.assertEqual(
            tuple(cell[1] for cell in target),
            tuple(cell[0] for cell in configuration),
        )

    def test_instantaneous_spatial_blocking_leaves_only_controls(self) -> None:
        self.assertEqual(
            self.instantaneous_flow,
            (
                ReversibleFlowRow(0, 0, 0),
                ReversibleFlowRow(51, 51, 204),
                ReversibleFlowRow(204, 204, 204),
                ReversibleFlowRow(255, 255, 0),
            ),
        )

    def test_trajectory_blocking_has_an_interacting_survivor(self) -> None:
        interacting = tuple(
            row
            for row in self.trajectory_flow
            if sum(essential_inputs(row.microscopic_rule)) >= 2
        )
        self.assertTrue(interacting)

    def test_trajectory_flow_is_exact_and_size_stable(self) -> None:
        expected = (
            ReversibleFlowRow(0, 0, 0),
            ReversibleFlowRow(15, 15, 240),
            ReversibleFlowRow(51, 51, 204),
            ReversibleFlowRow(60, 60, 60),
            ReversibleFlowRow(85, 85, 170),
            ReversibleFlowRow(90, 90, 90),
            ReversibleFlowRow(102, 102, 102),
            ReversibleFlowRow(105, 105, 150),
            ReversibleFlowRow(150, 150, 150),
            ReversibleFlowRow(153, 102, 102),
            ReversibleFlowRow(165, 90, 90),
            ReversibleFlowRow(170, 170, 170),
            ReversibleFlowRow(195, 60, 60),
            ReversibleFlowRow(204, 204, 204),
            ReversibleFlowRow(240, 240, 240),
            ReversibleFlowRow(255, 0, 0),
        )
        self.assertEqual(self.trajectory_flow, expected)
        self.assertEqual(
            tuple(rule for rule in range(256) if is_affine_rule(rule)),
            tuple(row.microscopic_rule for row in expected),
        )
        self.assertEqual(
            reversible_trajectory_flow_census(
                source_size=8,
                rules=tuple(row.microscopic_rule for row in expected),
            ),
            expected,
        )

    def test_declared_record_is_readable_after_one_step(self) -> None:
        configuration = ((0, 1), (1, 0), (0, 0))
        for rule in (60, 90, 102, 150):
            self.assertEqual(reversible_step(rule, configuration)[1][1], 1)

    def test_local_inverse_recovers_every_rule_after_two_steps(self) -> None:
        for rule in range(256):
            for configuration in reversible_configurations(3):
                future = reversible_step(rule, reversible_step(rule, configuration))
                self.assertEqual(
                    recover_two_step_current(rule, future),
                    configuration[1][0],
                )

    def test_record_channel_alone_does_not_persist_for_two_steps(self) -> None:
        self.assertTrue(
            all(second_step_record_is_one_time_padded(rule) for rule in range(256))
        )


if __name__ == "__main__":
    unittest.main()