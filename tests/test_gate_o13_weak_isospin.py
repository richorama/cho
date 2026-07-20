"""Gate O13 -- weak isospin su(2) from the quaternion factor.

Exact assertions over Q(i): the imaginary quaternion left-multiplications close
into su(2) ([L_i,L_j]=2L_k), and a quaternionic fermionic ladder realises a
left-handed weak-isospin doublet (T_3 = -1/2, +1/2).
"""

import unittest
from fractions import Fraction

from jordan_bootstrap.weak_isospin import (
    WeakIsospinCensus,
    isospin_ladder,
    isospin_number_operator,
    quaternion_left_mult,
    weak_isospin_census,
    _cmul,
    _dagger,
    _cadd,
    _cequal,
    _cident,
    _cis_zero,
)


class TestGateO13WeakIsospin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.census = weak_isospin_census()

    def test_census_type(self):
        self.assertIsInstance(self.census, WeakIsospinCensus)

    def test_imaginary_quaternions_close_into_su2(self):
        self.assertTrue(self.census.su2_bracket_relations)
        self.assertTrue(self.census.su2_generators_square_to_minus_one)

    def test_su2_is_three_dimensional_and_closed(self):
        self.assertEqual(self.census.su2_dimension, 3)
        self.assertTrue(self.census.su2_bracket_closed)

    def test_isospin_ladder_is_fermionic(self):
        self.assertTrue(self.census.car_holds)
        self.assertTrue(self.census.ladder_nilpotent)

    def test_number_operator_gives_doublets(self):
        # eigenvalues 0 and 1 each doubly degenerate: two weak doublets in C(x)H
        self.assertEqual(self.census.number_multiplicities, (2, 2))
        self.assertEqual(self.census.doublet_count, 2)

    def test_explicit_car(self):
        beta = isospin_ladder()
        bd = _dagger(beta)
        anti = _cadd(_cmul(beta, bd), _cmul(bd, beta))
        self.assertTrue(_cequal(anti, _cident()))

    def test_ladder_is_nilpotent_explicitly(self):
        beta = isospin_ladder()
        self.assertTrue(_cis_zero(_cmul(beta, beta)))

    def test_quaternion_units_square_to_minus_identity(self):
        from jordan_bootstrap.weak_isospin import _rmul, _rident
        for k in (1, 2, 3):
            g = quaternion_left_mult(k)
            self.assertEqual(_rmul(g, g), _rident(-1))

    def test_number_operator_is_hermitian_projector_like(self):
        # N = beta^dagger beta has spectrum in {0,1}, so N^2 = N (a projector).
        n = isospin_number_operator()
        self.assertTrue(_cequal(_cmul(n, n), n))


if __name__ == "__main__":
    unittest.main()
