"""Gate O10 -- colour su(3) from the octonionic complex-structure stabiliser.

Every claim below is an exact rational assertion: the derivation algebra of the
octonions is 14-dimensional (g2), the subalgebra fixing one imaginary unit is
8-dimensional, that subalgebra is the compact simple algebra su(3), and the
fixed unit induces a complex structure that turns the remaining six imaginaries
into C^3 -- the colour triplet.
"""

import unittest
from fractions import Fraction

from jordan_bootstrap.color_su3 import (
    ColorSU3Census,
    color_su3_census,
    derivation_algebra,
    is_derivation,
    left_mult_matrix,
    stabiliser_subalgebra,
)
from jordan_bootstrap.octonion import E


class TestGateO10ColorSU3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.census = color_su3_census()

    def test_census_type(self):
        self.assertIsInstance(self.census, ColorSU3Census)

    def test_derivation_algebra_is_g2_dimension_14(self):
        self.assertEqual(self.census.derivation_dimension, 14)

    def test_every_basis_element_is_a_derivation(self):
        self.assertTrue(self.census.all_basis_are_derivations)

    def test_g2_is_a_lie_subalgebra(self):
        self.assertTrue(self.census.g2_bracket_closed)

    def test_g2_is_compact_semisimple(self):
        self.assertTrue(self.census.g2_killing_nondegenerate)
        self.assertTrue(self.census.g2_killing_negative_definite)

    def test_stabiliser_is_dimension_8(self):
        self.assertEqual(self.census.stabiliser_dimension, 8)

    def test_stabiliser_is_a_lie_subalgebra(self):
        self.assertTrue(self.census.stabiliser_bracket_closed)

    def test_stabiliser_is_compact_semisimple(self):
        self.assertTrue(self.census.stabiliser_killing_nondegenerate)
        self.assertTrue(self.census.stabiliser_killing_negative_definite)

    def test_dimension_8_forces_simple_hence_su3(self):
        # 8 is not a sum of copies of su(2)=3, so a semisimple algebra of
        # dimension 8 is simple; the unique compact simple algebra of that
        # dimension is A2 = su(3).
        self.assertTrue(self.census.dimension_forbids_semisimple_split)

    def test_left_mult_is_a_complex_structure(self):
        self.assertTrue(self.census.complex_structure_squares_to_minus_one)

    def test_stabiliser_is_complex_linear(self):
        # D(u)=0 forces [D, L_u]=0, so su(3) acts C-linearly on the 6 remaining
        # imaginaries: they become C^3 (the 3 + 3bar quark reps).
        self.assertTrue(self.census.stabiliser_commutes_with_complex_structure)

    def test_fixed_direction_is_a_singlet(self):
        self.assertTrue(self.census.fixed_direction_is_singlet)

    def test_choice_of_fixed_unit_is_immaterial(self):
        # The same 8-dimensional su(3) appears no matter which imaginary axis is
        # singled out; check a second axis gives the same certificate.
        other = color_su3_census(u_index=3)
        self.assertEqual(other.stabiliser_dimension, 8)
        self.assertTrue(other.stabiliser_killing_negative_definite)
        self.assertTrue(other.stabiliser_commutes_with_complex_structure)

    def test_stabiliser_actually_fixes_u_and_lives_in_g2(self):
        g2 = derivation_algebra()
        self.assertEqual(len(g2), 14)
        u = E[7]
        stab = stabiliser_subalgebra(g2, u)
        self.assertEqual(len(stab), 8)
        for d in stab:
            self.assertTrue(is_derivation(d))
            image = tuple(
                sum((d[i][j] * u.coords[j] for j in range(8)), Fraction(0))
                for i in range(8)
            )
            self.assertTrue(all(c == 0 for c in image))

    def test_complex_structure_matches_left_multiplication(self):
        j = left_mult_matrix(E[7])
        # column j equals e7 * e_j
        for col in range(8):
            expected = (E[7] * E[col]).coords
            got = tuple(j[row][col] for row in range(8))
            self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main()
