"""Gate O21 -- exact tests for the colour-forcing theorem on C (x) O.

Pins every claim in ``jordan_bootstrap/colour_forcing.py``: the number-preserving
symmetry of one Fock generation is uniquely ``su(3) (+) u(1)``, acting as
``1 (+) 3 (+) 3bar (+) 1`` -- the colour content of one Standard-Model generation.
"""

import unittest

from jordan_bootstrap.colour_forcing import (
    ColourForcingCensus,
    colour_forcing_census,
    colour_singlet_on_leptons,
    commutant_dimension,
    fundamental_faithful_dimension,
    triplet_and_antitriplet,
    u3_bilinear_dimension,
)


class ColourForcingTest(unittest.TestCase):
    def test_grading_symmetry_is_twenty_dimensional(self):
        self.assertEqual(commutant_dimension(), 20)

    def test_bilinears_span_u3(self):
        self.assertEqual(u3_bilinear_dimension(), 9)

    def test_colour_singlet_on_leptons(self):
        self.assertTrue(colour_singlet_on_leptons())

    def test_charge_one_sector_is_faithful_fundamental(self):
        self.assertEqual(fundamental_faithful_dimension(), 8)

    def test_triplet_and_antitriplet(self):
        self.assertTrue(triplet_and_antitriplet())

    def test_census(self):
        c = colour_forcing_census()
        self.assertIsInstance(c, ColourForcingCensus)
        self.assertEqual(c.grading_symmetry_dimension, 20)
        self.assertEqual(c.u3_dimension, 9)
        self.assertEqual(c.su3_dimension, 8)
        self.assertTrue(c.su3_bracket_closed)
        self.assertTrue(c.colour_singlet_on_leptons)
        self.assertEqual(c.fundamental_faithful_dimension, 8)
        self.assertTrue(c.triplet_and_antitriplet)


if __name__ == "__main__":
    unittest.main()
