"""Gate O16 -- exact tests for octonionic evolution as rotations.

Pins every claim in ``jordan_bootstrap/isometric_flow.py``: unit-octonion steps
are exact isometries, a single generator closes into a one-parameter group, the
imaginary generators close into ``so(8)`` (dim 28) under the commutator, the map
``u |-> L_u`` fails to be a homomorphism (defect = the O15 associator), and the
operator Moufang law survives.
"""

import unittest
from fractions import Fraction

from jordan_bootstrap.dynamics_wall import associator
from jordan_bootstrap.isometric_flow import (
    FlowCensus,
    flow_census,
    homomorphism_defect,
    imaginary_generators_independent_dimension,
    is_orthogonal,
    left_mult_gram,
    lie_closure_dimension,
    moufang_operator_closes,
    octonion_power,
    single_generator_closes,
)
from jordan_bootstrap.color_su3 import left_mult_matrix, _matmul
from jordan_bootstrap.octonion import E, octonion, ONE


def _identity():
    return tuple(
        tuple(Fraction(1) if i == j else Fraction(0) for j in range(8))
        for i in range(8)
    )


class IsometricFlowTest(unittest.TestCase):
    # --- steps are exact isometries -------------------------------------

    def test_unit_generator_is_orthogonal(self):
        u = octonion(0, Fraction(3, 5), Fraction(4, 5), 0, 0, 0, 0, 0)
        self.assertEqual(u.norm2(), 1)
        self.assertTrue(is_orthogonal(u))
        self.assertEqual(left_mult_gram(u), _identity())

    def test_gram_is_norm_squared_times_identity(self):
        w = octonion(2, 0, 0, 0, 0, 0, 0, 0)
        expected = tuple(
            tuple(Fraction(4) if i == j else Fraction(0) for j in range(8))
            for i in range(8)
        )
        self.assertEqual(left_mult_gram(w), expected)

    # --- single generator closes into a one-parameter group -------------

    def test_octonion_power(self):
        u = octonion(0, 1, 0, 0, 0, 0, 0, 0)  # e1, e1^2 = -1
        self.assertEqual(octonion_power(u, 0).coords, ONE.coords)
        self.assertEqual(octonion_power(u, 2).coords, (-ONE).coords)

    def test_single_generator_group_law(self):
        u = octonion(0, Fraction(3, 5), Fraction(4, 5), 0, 0, 0, 0, 0)
        self.assertTrue(single_generator_closes(u, upto=7))

    # --- generators close into so(8) ------------------------------------

    def test_imaginary_generators_independent(self):
        self.assertEqual(imaginary_generators_independent_dimension(), 7)

    def test_lie_closure_is_so8(self):
        self.assertEqual(lie_closure_dimension(), 28)

    # --- the wall lives in the map u -> L_u -----------------------------

    def test_map_is_not_a_homomorphism(self):
        u = octonion(0, Fraction(3, 5), Fraction(4, 5), 0, 0, 0, 0, 0)
        v = octonion(0, 0, 0, Fraction(5, 13), Fraction(12, 13), 0, 0, 0)
        defect = homomorphism_defect(u, v)
        self.assertTrue(any(x != 0 for row in defect for x in row))

    def test_homomorphism_defect_is_associator(self):
        # (L_u L_v - L_{uv}) x = u(vx) - (uv)x = -associator(u, v, x) for all x.
        u = octonion(0, Fraction(3, 5), Fraction(4, 5), 0, 0, 0, 0, 0)
        v = octonion(0, 0, 0, Fraction(5, 13), Fraction(12, 13), 0, 0, 0)
        defect = homomorphism_defect(u, v)
        for k in range(8):
            col = tuple(defect[i][k] for i in range(8))
            expected = (-associator(u, v, E[k])).coords
            self.assertEqual(col, expected)

    # --- the surviving Moufang operator law -----------------------------

    def test_moufang_operator_closure(self):
        u = octonion(0, Fraction(3, 5), Fraction(4, 5), 0, 0, 0, 0, 0)
        v = octonion(0, 0, 0, Fraction(5, 13), Fraction(12, 13), 0, 0, 0)
        self.assertTrue(moufang_operator_closes(u, v))

    def test_moufang_holds_on_basis_pairs(self):
        self.assertTrue(
            all(moufang_operator_closes(E[i], E[j]) for i in range(8) for j in range(8))
        )

    # --- census ----------------------------------------------------------

    def test_census(self):
        c = flow_census()
        self.assertIsInstance(c, FlowCensus)
        self.assertTrue(c.steps_are_isometries)
        self.assertTrue(c.single_generator_group)
        self.assertEqual(c.imaginary_generator_dimension, 7)
        self.assertEqual(c.lie_closure_dimension, 28)
        self.assertTrue(c.is_so8)
        self.assertTrue(c.homomorphism_defect_nonzero)
        self.assertTrue(c.moufang_operator_closes)


if __name__ == "__main__":
    unittest.main()
