import json
import unittest

import export_affine_certificates

from observer_bootstrap.boolean_algebra import (
    affine_effective_rules,
    anf_to_rule,
    is_affine_anf,
    rule_to_anf,
)
from observer_bootstrap.reversible_dynamics import (
    pair_blocking_audit,
    reversible_trajectory_flow_census,
    trajectory_conflict_certificate,
    validates_trajectory_conflict,
)


class Gate06AffineClassification(unittest.TestCase):
    """The reversible trajectory survivors have exactly affine local laws."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.flow = reversible_trajectory_flow_census()
        cls.blocking_audit = pair_blocking_audit()

    def test_anf_round_trip_is_unique_and_exact(self) -> None:
        forms = tuple(rule_to_anf(rule) for rule in range(256))
        self.assertEqual(len(set(forms)), 256)
        self.assertEqual(
            tuple(anf_to_rule(coefficients) for coefficients in forms),
            tuple(range(256)),
        )

    def test_exactly_sixteen_rules_have_affine_normal_form(self) -> None:
        affine = tuple(
            rule for rule in range(256) if is_affine_anf(rule_to_anf(rule))
        )
        self.assertEqual(len(affine), 16)
        self.assertEqual(affine, tuple(row.microscopic_rule for row in self.flow))

    def test_symbolic_affine_flow_matches_every_census_row(self) -> None:
        self.assertEqual(
            tuple(
                (row.decimation_rule, row.parity_rule)
                for row in self.flow
            ),
            tuple(
                affine_effective_rules(row.microscopic_rule)
                for row in self.flow
            ),
        )

    def test_every_non_affine_rule_has_a_bounded_conflict_certificate(self) -> None:
        certificates = tuple(
            trajectory_conflict_certificate(rule)
            for rule in range(256)
            if not is_affine_anf(rule_to_anf(rule))
        )
        self.assertEqual(len(certificates), 240)
        self.assertTrue(all(certificate is not None for certificate in certificates))
        self.assertTrue(all(map(validates_trajectory_conflict, certificates)))
        self.assertTrue(
            all(certificate.blocking_name == "decimation" for certificate in certificates)
        )
        self.assertTrue(all(map(self._independently_validates_conflict, certificates)))

    @staticmethod
    def _independently_validates_conflict(certificate) -> bool:
        def step(configuration):
            size = len(configuration)
            current = tuple(cell[0] for cell in configuration)
            return tuple(
                (
                    ((certificate.rule >> (
                        4 * current[(index - 1) % size]
                        + 2 * current[index]
                        + current[(index + 1) % size]
                    )) & 1) ^ configuration[index][1],
                    current[index],
                )
                for index in range(size)
            )

        def observation(configuration, coarse_site):
            previous = tuple(configuration[index][0] for index in range(0, 6, 2))
            current_configuration = step(step(configuration))
            current = tuple(
                current_configuration[index][0] for index in range(0, 6, 2)
            )
            next_configuration = step(step(current_configuration))
            next_values = tuple(
                next_configuration[index][0] for index in range(0, 6, 2)
            )
            coarse_input = (
                previous[coarse_site],
                current[(coarse_site - 1) % 3],
                current[coarse_site],
                current[(coarse_site + 1) % 3],
            )
            return coarse_input, next_values[coarse_site] ^ previous[coarse_site]

        first = observation(certificate.first, certificate.first_coarse_site)
        second = observation(certificate.second, certificate.second_coarse_site)
        return first[0] == second[0] and first[1] != second[1]

    def test_affine_rules_have_no_conflict_certificate(self) -> None:
        self.assertTrue(
            all(
                trajectory_conflict_certificate(rule) is None
                for rule in range(256)
                if is_affine_anf(rule_to_anf(rule))
            )
        )

    def test_every_nonconstant_pair_blocking_rejects_non_affine_rules(self) -> None:
        affine_rules = {
            rule for rule in range(256) if is_affine_anf(rule_to_anf(rule))
        }
        self.assertTrue(
            all(
                set(row.survivors) <= affine_rules
                for row in self.blocking_audit
                if not row.is_constant
            )
        )

    def test_balanced_affine_blockings_select_all_sixteen_affine_rules(self) -> None:
        rows = tuple(
            row
            for row in self.blocking_audit
            if not row.is_constant and row.is_affine
        )
        self.assertEqual(tuple(row.blocking_code for row in rows), (3, 5, 6, 9, 10, 12))
        self.assertTrue(all(len(row.survivors) == 16 for row in rows))

    def test_nonlinear_blockings_leave_only_two_constant_rules(self) -> None:
        rows = tuple(
            row
            for row in self.blocking_audit
            if not row.is_constant and not row.is_affine
        )
        self.assertEqual(tuple(row.blocking_code for row in rows), (1, 2, 4, 7, 8, 11, 13, 14))
        self.assertTrue(all(row.survivors == (0, 255) for row in rows))

    def test_constant_blockings_are_operationally_degenerate(self) -> None:
        rows = tuple(row for row in self.blocking_audit if row.is_constant)
        self.assertEqual(tuple(row.blocking_code for row in rows), (0, 15))
        self.assertTrue(all(not row.survivors for row in rows))

    def test_portable_certificate_payload_replays_independently(self) -> None:
        artifact_text = export_affine_certificates.ARTIFACT_PATH.read_text(
            encoding="ascii"
        )
        payload = json.loads(artifact_text)
        export_affine_certificates.verify_payload(payload)
        self.assertEqual(
            artifact_text,
            export_affine_certificates.canonical_json(
                export_affine_certificates.certificate_payload()
            ),
        )


if __name__ == "__main__":
    unittest.main()