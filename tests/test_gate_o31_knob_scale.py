"""Gate O31 -- the knob denominator ``432 = 16 x 27`` from computed campaign dimensions.

Every claim is an exact integer identity pinned here: the chiral Weyl count (Gate
O25) times ``dim J_3(O)`` (Gate O24) equals the ``432`` of the adopted scale
``eps0^2 = pi/432`` used by Gates O28/O29/O30.
"""

import unittest
from fractions import Fraction

from jordan_bootstrap.knob_scale import (
    KnobScaleCensus,
    chiral_weyl_count,
    denominator_is_432,
    eps0_squared,
    eps0_squared_exact_denominator,
    factorisations_agree,
    higgs_factorisation,
    jordan_dimension,
    knob_denominator,
    knob_scale_census,
    matches_adopted_scale,
)
from jordan_bootstrap.chiral_projection import left_handed_dimension
from jordan_bootstrap.three_generations import (
    generation_slot_dimension,
    offdiagonal_dimension,
)


class TestGateO31KnobScale(unittest.TestCase):
    def test_chiral_weyl_count_is_16(self):
        """The 16 is Gate O25's one-chirality Weyl count, not an arbitrary integer."""
        self.assertEqual(chiral_weyl_count(), 16)
        self.assertEqual(chiral_weyl_count(), left_handed_dimension())

    def test_jordan_dimension_is_27(self):
        """dim J_3(O) = 27 = 3 generation slots + 24 octonionic off-diagonal (Gate O24)."""
        self.assertEqual(jordan_dimension(), 27)
        self.assertEqual(
            jordan_dimension(),
            generation_slot_dimension() + offdiagonal_dimension(),
        )

    def test_knob_denominator_is_432(self):
        """16 * 27 = 432 -- the adopted flavour-scale denominator, from computed dims."""
        self.assertEqual(knob_denominator(), 16 * 27)
        self.assertEqual(knob_denominator(), 432)
        self.assertTrue(denominator_is_432())

    def test_higgs_factorisation_consistency(self):
        """432 = 24 * 18 is a second exact factorisation of the same denominator."""
        a, b = higgs_factorisation()
        self.assertEqual(a * b, 432)
        self.assertTrue(factorisations_agree())

    def test_exact_denominator_fraction(self):
        """eps0^2 = pi * (1/432) exactly as a rational multiplier."""
        self.assertEqual(eps0_squared_exact_denominator(), Fraction(1, 432))

    def test_matches_adopted_scale(self):
        """pi/(16*27) reproduces the pi/432 knob used by O28/O29/O30."""
        self.assertTrue(matches_adopted_scale())
        self.assertAlmostEqual(eps0_squared(), 3.141592653589793 / 432.0, places=15)

    def test_census(self):
        census = knob_scale_census()
        self.assertIsInstance(census, KnobScaleCensus)
        self.assertEqual(census.chiral_weyl_count, 16)
        self.assertEqual(census.jordan_dimension, 27)
        self.assertEqual(census.knob_denominator, 432)
        self.assertTrue(census.denominator_is_432)
        self.assertTrue(census.factorisations_agree)
        self.assertTrue(census.matches_adopted_scale)


if __name__ == "__main__":
    unittest.main()
