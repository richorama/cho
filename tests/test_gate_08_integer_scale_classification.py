import unittest

from observer_bootstrap.boolean_algebra import (
    affine_rules_align_at_matched_scale,
    are_terms_block_aligned,
    is_affine_anf,
    rule_to_anf,
    sampled_affine_operator_terms,
)


class Gate08IntegerScaleClassification(unittest.TestCase):
    """Universal matched-scale affine alignment occurs exactly at dyadic scales."""

    def test_sampled_polynomials_obey_characteristic_two_doubling(self) -> None:
        affine_rules = tuple(
            rule for rule in range(256) if is_affine_anf(rule_to_anf(rule))
        )
        for rule in affine_rules:
            for scale in range(1, 33):
                terms = sampled_affine_operator_terms(rule, scale)
                self.assertEqual(
                    sampled_affine_operator_terms(rule, 2 * scale),
                    tuple(2 * exponent for exponent in terms),
                )

    def test_rule_60_hidden_shift_obstructs_every_sampled_non_dyadic_scale(
        self,
    ) -> None:
        for scale in range(2, 257):
            terms = sampled_affine_operator_terms(60, scale)
            low_bit = scale & -scale
            self.assertIn(-scale, terms)
            if scale == low_bit:
                self.assertTrue(are_terms_block_aligned(terms, scale))
            else:
                hidden_shift = -(scale - low_bit)
                self.assertIn(hidden_shift, terms)
                self.assertNotEqual(hidden_shift % scale, 0)
                self.assertFalse(are_terms_block_aligned(terms, scale))

    def test_all_affine_rules_align_exactly_at_sampled_dyadic_scales(self) -> None:
        for scale in range(2, 129):
            self.assertEqual(
                affine_rules_align_at_matched_scale(scale),
                scale & (scale - 1) == 0,
            )

    def test_alignment_api_rejects_invalid_scales(self) -> None:
        for scale in (-1, 0):
            with self.assertRaises(ValueError):
                are_terms_block_aligned((), scale)
        for scale in (-1, 0, 1):
            with self.assertRaises(ValueError):
                affine_rules_align_at_matched_scale(scale)


if __name__ == "__main__":
    unittest.main()