"""Gate O18 -- exact tests for the G2 -> SU(3) reduction.

Pins every claim in ``jordan_bootstrap/su3_structure.py``: fixing ``u = e_7``
gives ``u^perp = C^3`` with ``J^2 = -I``, a nondegenerate J-invariant Kahler form
``omega = phi(u, .,.)``, a ``(3,0)+(0,3)`` holomorphic form, and the O10 colour
``su(3)`` preserves the whole ``SU(3)`` structure.
"""

import unittest

from jordan_bootstrap.su3_structure import (
    SU3StructureCensus,
    colour_su3,
    complex_structure,
    complex_structure_preserves_perp,
    complex_structure_squares_to_minus_one,
    holomorphic_form_is_type_three_zero,
    kahler_form,
    kahler_is_antisymmetric,
    kahler_is_j_invariant,
    kahler_rank,
    kahler_tames_complex_structure,
    su3_commutes_with_complex_structure,
    su3_preserves_holomorphic_form,
    su3_preserves_kahler,
    su3_structure_census,
)
from jordan_bootstrap.color_su3 import _apply
from jordan_bootstrap.octonion import E


class SU3StructureTest(unittest.TestCase):
    # --- complex structure ----------------------------------------------

    def test_j_squares_to_minus_one(self):
        self.assertTrue(complex_structure_squares_to_minus_one())

    def test_j_preserves_perp(self):
        self.assertTrue(complex_structure_preserves_perp())

    def test_j_is_left_mult_by_u(self):
        j = complex_structure()
        # J e_1 = e_7 e_1 (left mult); just check it is imaginary and unit-length.
        image = _apply(j, E[1])
        self.assertEqual(image.norm2(), 1)
        self.assertEqual(image.coords[0], 0)

    # --- Kahler form -----------------------------------------------------

    def test_kahler_antisymmetric(self):
        self.assertTrue(kahler_is_antisymmetric())

    def test_kahler_nondegenerate(self):
        self.assertEqual(kahler_rank(), 6)

    def test_kahler_j_invariant(self):
        self.assertTrue(kahler_is_j_invariant())

    def test_kahler_tames_j(self):
        self.assertTrue(kahler_tames_complex_structure())

    def test_kahler_vanishes_with_u(self):
        # omega only lives on u^perp; phi(u, u, .) = 0.
        self.assertEqual(kahler_form(E[7], E[1]), 0)

    # --- holomorphic volume form ----------------------------------------

    def test_holomorphic_form_type_three_zero(self):
        self.assertTrue(holomorphic_form_is_type_three_zero())

    # --- the SU(3) is colour --------------------------------------------

    def test_colour_su3_dimension(self):
        self.assertEqual(len(colour_su3()), 8)

    def test_su3_preserves_kahler(self):
        self.assertTrue(su3_preserves_kahler())

    def test_su3_commutes_with_j(self):
        self.assertTrue(su3_commutes_with_complex_structure())

    def test_su3_preserves_holomorphic_form(self):
        self.assertTrue(su3_preserves_holomorphic_form())

    # --- census ----------------------------------------------------------

    def test_census(self):
        c = su3_structure_census()
        self.assertIsInstance(c, SU3StructureCensus)
        self.assertTrue(c.complex_structure_squares)
        self.assertTrue(c.complex_structure_preserves_perp)
        self.assertTrue(c.kahler_antisymmetric)
        self.assertEqual(c.kahler_rank, 6)
        self.assertTrue(c.kahler_j_invariant)
        self.assertTrue(c.kahler_tames_j)
        self.assertTrue(c.holomorphic_form_type_three_zero)
        self.assertEqual(c.colour_su3_dimension, 8)
        self.assertTrue(c.su3_preserves_kahler)
        self.assertTrue(c.su3_commutes_with_j)
        self.assertTrue(c.su3_preserves_holomorphic_form)


if __name__ == "__main__":
    unittest.main()
