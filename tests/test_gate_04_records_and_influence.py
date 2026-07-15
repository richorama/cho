import unittest

from observer_bootstrap.local_dynamics import local_blocking_flow_census
from observer_bootstrap.records import (
    EncodedRecall,
    RecordCensus,
    background_independent_response,
    encoded_recall_passers,
    has_persistent_redundant_imprint,
    record_census,
    recalls_both_values_above_chance,
    repetition_recall,
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

    def test_encoded_protocol_is_fixed_and_exact(self) -> None:
        self.assertEqual(repetition_recall(204), EncodedRecall(256, 240, 240))
        self.assertEqual(repetition_recall(0), EncodedRecall(256, 256, 0))

    def test_encoded_recall_does_not_select_interacting_fixed_points(self) -> None:
        self.assertEqual(
            tuple(repetition_recall(rule) for rule in self.fixed_interacting),
            (
                EncodedRecall(256, 168, 88),
                EncodedRecall(256, 128, 128),
                EncodedRecall(256, 168, 88),
                EncodedRecall(256, 128, 128),
            ),
        )
        self.assertFalse(
            any(
                recalls_both_values_above_chance(repetition_recall(rule))
                for rule in self.fixed_interacting
            )
        )

    def test_encoded_recall_is_not_enriched_among_survivors(self) -> None:
        selected_passers = encoded_recall_passers(self.survivors)
        control_passers = encoded_recall_passers(self.controls)
        self.assertEqual(selected_passers, (15, 51, 85, 170, 204, 240))
        self.assertEqual(len(control_passers), 88)
        self.assertLess(
            len(selected_passers) * len(self.controls),
            len(control_passers) * len(self.survivors),
        )


if __name__ == "__main__":
    unittest.main()