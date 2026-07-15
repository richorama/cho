import unittest

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


if __name__ == "__main__":
    unittest.main()