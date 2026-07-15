import unittest
from itertools import product

from observer_bootstrap.boolean_algebra import (
    affine_operator_terms,
    dyadic_affine_block_rule,
    dyadic_affine_effective_rules,
    is_affine_anf,
    rule_to_anf,
    sampled_affine_operator_terms,
)
from observer_bootstrap.reversible_dynamics import local_output, reversible_step


class Gate07DyadicRenormalization(unittest.TestCase):
    """Affine trajectory closure extends through the full dyadic scale tower."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.affine_rules = tuple(
            rule for rule in range(256) if is_affine_anf(rule_to_anf(rule))
        )

    def test_every_affine_sampled_operator_collapses_at_dyadic_scales(self) -> None:
        for rule in self.affine_rules:
            microscopic_terms = affine_operator_terms(rule)
            for block_size in (2, 4, 8, 16, 32):
                self.assertEqual(
                    sampled_affine_operator_terms(rule, block_size),
                    tuple(block_size * exponent for exponent in microscopic_terms),
                )

    def test_direct_dyadic_trajectories_match_symbolic_laws(self) -> None:
        for rule in self.affine_rules:
            for block_size in (2, 4, 8):
                decimation_rule, parity_rule = dyadic_affine_effective_rules(
                    rule, block_size
                )
                for blocking_name, effective_rule in (
                    ("decimation", decimation_rule),
                    ("parity", parity_rule),
                ):
                    self._assert_basis_trajectories_close(
                        rule, block_size, blocking_name, effective_rule
                    )

    def test_every_nonconstant_affine_block_functional_closes(self) -> None:
        for rule in self.affine_rules:
            for block_size in (2, 4):
                for weights in product((0, 1), repeat=block_size):
                    if not any(weights):
                        continue
                    for offset in (0, 1):
                        effective_rule = dyadic_affine_block_rule(
                            rule, block_size, weights, offset
                        )
                        self._assert_affine_block_basis_trajectories_close(
                            rule,
                            block_size,
                            weights,
                            offset,
                            effective_rule,
                        )

    def test_dyadic_flows_stabilize_after_one_step(self) -> None:
        for rule in self.affine_rules:
            decimation_rule, parity_rule = dyadic_affine_effective_rules(rule, 2)
            for block_size in (2, 4, 8, 16):
                self.assertEqual(
                    dyadic_affine_effective_rules(rule, block_size),
                    (decimation_rule, parity_rule),
                )
                self.assertEqual(
                    dyadic_affine_effective_rules(decimation_rule, block_size)[0],
                    decimation_rule,
                )
                self.assertEqual(
                    dyadic_affine_effective_rules(parity_rule, block_size),
                    (parity_rule, parity_rule),
                )

    def test_affine_block_flows_have_only_fixed_points_or_constant_two_cycles(self) -> None:
        for rule in self.affine_rules:
            coefficients = rule_to_anf(rule)
            coefficient_sum = coefficients[1] ^ coefficients[2] ^ coefficients[4]
            for block_size in (2, 4):
                for weights in product((0, 1), repeat=block_size):
                    if not any(weights):
                        continue
                    for offset in (0, 1):
                        first = dyadic_affine_block_rule(
                            rule, block_size, weights, offset
                        )
                        second = dyadic_affine_block_rule(
                            first, block_size, weights, offset
                        )
                        if coefficient_sum and sum(weights) % 2 and offset:
                            self.assertNotEqual(first, rule)
                            self.assertEqual(second, rule)
                        else:
                            self.assertEqual(second, first)

    def test_stride_three_exposes_non_block_aligned_shifts(self) -> None:
        self.assertEqual(affine_operator_terms(150), (-1, 0, 1))
        self.assertEqual(
            sampled_affine_operator_terms(150, 3),
            (-3, -2, -1, 1, 2, 3),
        )
        self.assertTrue(
            any(exponent % 3 for exponent in sampled_affine_operator_terms(150, 3))
        )

    def test_dyadic_api_rejects_out_of_scope_inputs(self) -> None:
        for block_size in (0, 1, 3, 6):
            with self.assertRaises(ValueError):
                dyadic_affine_effective_rules(150, block_size)
        with self.assertRaises(ValueError):
            dyadic_affine_effective_rules(30, 2)
        with self.assertRaises(ValueError):
            dyadic_affine_block_rule(150, 4, (0, 0, 0, 0))
        with self.assertRaises(ValueError):
            dyadic_affine_block_rule(150, 4, (1, 0))
        with self.assertRaises(ValueError):
            dyadic_affine_block_rule(150, 4, (1, 0, 0, 2))
        with self.assertRaises(ValueError):
            dyadic_affine_block_rule(150, 4, (1, 0, 0, 0), offset=2)
        with self.assertRaises(ValueError):
            sampled_affine_operator_terms(150, 0)

    def _assert_basis_trajectories_close(
        self, rule, block_size, blocking_name, effective_rule
    ) -> None:
        if blocking_name == "decimation":
            weights = (1,) + (0,) * (block_size - 1)
        elif blocking_name == "parity":
            weights = (1,) * block_size
        else:
            raise ValueError("unknown blocking")
        self._assert_affine_block_basis_trajectories_close(
            rule, block_size, weights, 0, effective_rule
        )

    def _assert_affine_block_basis_trajectories_close(
        self, rule, block_size, weights, offset, effective_rule
    ) -> None:
        source_size = 3 * block_size
        configurations = [tuple((0, 0) for _ in range(source_size))]
        for index in range(source_size):
            for channel in range(2):
                configuration = [[0, 0] for _ in range(source_size)]
                configuration[index][channel] = 1
                configurations.append(tuple(tuple(cell) for cell in configuration))

        for configuration in configurations:
            previous = self._block_current(configuration, weights, offset)
            evolved = configuration
            for _ in range(block_size):
                evolved = reversible_step(rule, evolved)
            current = self._block_current(evolved, weights, offset)
            for _ in range(block_size):
                evolved = reversible_step(rule, evolved)
            next_values = self._block_current(evolved, weights, offset)

            predicted = tuple(
                local_output(
                    effective_rule,
                    current[(index - 1) % 3],
                    current[index],
                    current[(index + 1) % 3],
                )
                ^ previous[index]
                for index in range(3)
            )
            self.assertEqual(next_values, predicted)

    @staticmethod
    def _block_current(configuration, weights, offset):
        block_size = len(weights)
        blocks = tuple(
            configuration[index : index + block_size]
            for index in range(0, len(configuration), block_size)
        )
        return tuple(
            offset
            ^ (sum(weight * cell[0] for weight, cell in zip(weights, block)) % 2)
            for block in blocks
        )


if __name__ == "__main__":
    unittest.main()