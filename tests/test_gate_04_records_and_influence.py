import unittest

from observer_bootstrap.local_dynamics import local_blocking_flow_census
from observer_bootstrap.records import (
    RecordCensus,
    background_independent_response,
    has_persistent_redundant_imprint,
    record_census,
    response_respects_light_cone,
    source_is_locally_decodable,
)


class Gate04RecordsAndInfluence(unittest.TestCase):
    """Frozen Gate 03 survivors face an unscored causal-record holdout."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.survivors = tuple(
            row.microscopic_rule for row in local_blocking_flow_census()
        )
        survivor_set = set(cls.survivors)
        cls.controls = tuple(rule for rule in range(256) if rule not in survivor_set)
        cls.fixed_interacting = (60, 90, 102, 150)

    def test_rule_90_light_cone_response_is_exact(self) -> None:
        response = background_independent_response(90, size=11, steps=4)
        self.assertEqual(
            response,
            (0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0),
        )
        self.assertTrue(response_respects_light_cone(response, source=5, steps=4))

    def test_all_interacting_fixed_points_leave_redundant_causal_imprints(self) -> None:
        self.assertTrue(
            all(map(has_persistent_redundant_imprint, self.fixed_interacting))
        )

    def test_causal_imprint_is_selected_against_unselected_controls(self) -> None:
        survivor_census = record_census(self.survivors)
        control_census = record_census(self.controls)
        self.assertEqual(survivor_census, RecordCensus(20, 16, 14, 8))
        self.assertEqual(control_census, RecordCensus(236, 0, 0, 0))

    def test_causal_imprints_are_not_passively_readable_records(self) -> None:
        self.assertFalse(
            any(
                source_is_locally_decodable(rule, steps, radius)
                for rule in self.fixed_interacting
                for steps in range(1, 5)
                for radius in range(steps + 1)
            )
        )


if __name__ == "__main__":
    unittest.main()