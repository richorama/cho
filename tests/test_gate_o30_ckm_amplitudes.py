"""Gate O30 -- CKM amplitudes: vector ``sqrt(7)`` vs spinor ``1/2``.

Every structural claim is pinned to an exact ``Q`` check (the two leading transition
coefficients, the double-cover ``1/2``, and ``tan(pi/8) = sqrt(2) - 1`` in
``Q(sqrt 2)``); the data-agreement test is the falsifiable half.
"""

import unittest
from fractions import Fraction

from jordan_bootstrap.ckm_amplitudes import (
    CkmAmplitudeCensus,
    amplitudes_agree_with_data,
    ckm_amplitude_census,
    double_cover_factor,
    matches_o28_cabibbo_count,
    max_absolute_deviation,
    predictions,
    spinor_transition_coefficient,
    tan_pi8_is_positive_root,
    tan_pi8_satisfies_half_angle,
    vcb_coefficient,
    vector_channel_count,
    vector_transition_coefficient,
)
from jordan_bootstrap.mixing_web import cabibbo_count


class TestGateO30CkmAmplitudes(unittest.TestCase):
    def test_spinor_coefficient_is_half(self):
        """The spin-1/2 inter-generation leading transition coefficient is exactly 1/2."""
        self.assertEqual(spinor_transition_coefficient(), Fraction(1, 2))

    def test_vector_coefficient_is_one(self):
        """The Im(O) vector leading transition coefficient is exactly 1."""
        self.assertEqual(vector_transition_coefficient(), Fraction(1))

    def test_double_cover_factor(self):
        """spinor/vector = 1/2 is the SU(2)->SO(3) half-angle -- the |V_cb| coefficient."""
        self.assertEqual(double_cover_factor(), Fraction(1, 2))
        self.assertEqual(vcb_coefficient(), Fraction(1, 2))

    def test_vector_channel_matches_o28(self):
        """|V_us|^2 = (sqrt 7)^2 = 7 equals Gate O28's Cabibbo count."""
        self.assertEqual(vector_channel_count(), 7)
        self.assertEqual(vector_channel_count(), cabibbo_count())
        self.assertTrue(matches_o28_cabibbo_count())

    def test_tan_pi8_exact_identity(self):
        """tan(pi/8) = sqrt(2) - 1 verified exactly in Q(sqrt 2) via 2t/(1-t^2)=1."""
        self.assertTrue(tan_pi8_satisfies_half_angle())
        self.assertTrue(tan_pi8_is_positive_root())

    def test_predictions_present(self):
        """Two prediction rows: the vector |V_us| and the spinor |V_cb|."""
        rows = predictions()
        self.assertEqual(len(rows), 2)
        names = {r[0] for r in rows}
        self.assertIn("|V_us| (vector)", names)
        self.assertIn("|V_cb| (spinor)", names)

    def test_amplitudes_agree_with_data(self):
        """Both CKM amplitude predictions agree with PDG values within 3% (actual < 1.1%)."""
        self.assertTrue(amplitudes_agree_with_data(0.03))
        self.assertLess(max_absolute_deviation(), 1.1)

    def test_census(self):
        """The census bundles the exact coefficients and the data verdict."""
        census = ckm_amplitude_census()
        self.assertIsInstance(census, CkmAmplitudeCensus)
        self.assertEqual(census.spinor_coefficient, Fraction(1, 2))
        self.assertEqual(census.vector_coefficient, Fraction(1))
        self.assertEqual(census.double_cover_factor, Fraction(1, 2))
        self.assertEqual(census.vector_channel_count, 7)
        self.assertTrue(census.matches_o28_cabibbo)
        self.assertTrue(census.tan_pi8_exact)
        self.assertTrue(census.amplitudes_agree)


if __name__ == "__main__":
    unittest.main()
