"""Gate O19 -- exact tests for the phase U(1) completing colour to U(3).

Pins every claim in ``jordan_bootstrap/phase_u1.py``: the complex structure ``J``
is a skew ``J^2=-I`` generator on ``u^perp``, the centraliser of ``J`` in
``so(6)`` is ``u(3)`` (dim 9), colour ``su(3)`` (dim 8) and the phase ``u(1)_J``
(dim 1) are mutual centralisers with ``su(3) (+) u(1)_J = u(3)``, and the phase
lies outside ``Aut(O)``.
"""

import unittest

from jordan_bootstrap.phase_u1 import (
    PhaseU1Census,
    centraliser_of_j_dimension,
    colour_dimension,
    commutant_of_colour_dimension,
    j_is_skew_square_minus_one,
    phase_commutes_with_colour,
    phase_is_outside_automorphisms,
    phase_u1_census,
    u3_dimension,
)


class PhaseU1Test(unittest.TestCase):
    def test_j_is_skew_and_squares_to_minus_one(self):
        self.assertTrue(j_is_skew_square_minus_one())

    def test_centraliser_of_j_is_u3(self):
        self.assertEqual(centraliser_of_j_dimension(), 9)

    def test_colour_dimension_is_eight(self):
        self.assertEqual(colour_dimension(), 8)

    def test_commutant_of_colour_is_one_dimensional(self):
        # The centraliser of colour su(3) in so(6) is exactly span(J) = u(1)_J.
        self.assertEqual(commutant_of_colour_dimension(), 1)

    def test_su3_plus_u1_equals_u3(self):
        # 8 + 1 = 9: colour su(3) and the phase generator J fill out u(3).
        self.assertEqual(u3_dimension(), 9)
        self.assertEqual(colour_dimension() + commutant_of_colour_dimension(),
                         u3_dimension())

    def test_phase_commutes_with_colour(self):
        self.assertTrue(phase_commutes_with_colour())

    def test_phase_is_outside_automorphisms(self):
        # J = L_u is not a derivation, so u(1)_J is a symmetry beyond g2 = Aut(O).
        self.assertTrue(phase_is_outside_automorphisms())

    def test_census(self):
        c = phase_u1_census()
        self.assertIsInstance(c, PhaseU1Census)
        self.assertTrue(c.j_skew_square_minus_one)
        self.assertEqual(c.centraliser_of_j_dimension, 9)
        self.assertEqual(c.colour_dimension, 8)
        self.assertEqual(c.commutant_of_colour_dimension, 1)
        self.assertEqual(c.u3_dimension, 9)
        self.assertTrue(c.phase_commutes_with_colour)
        self.assertTrue(c.phase_outside_automorphisms)


if __name__ == "__main__":
    unittest.main()
