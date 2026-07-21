"""Gate O15 -- exact tests for the octonionic dynamics wall.

Pins every claim in ``jordan_bootstrap/dynamics_wall.py`` to an exact rational
computation: what survives (alternativity, Moufang, isometric single-generator
flow), what breaks (Jacobi, hence no Lie algebra / no unitary group), the exact
identity ``J = 6[,]`` linking the break to non-associativity, the observable
path-ordering defect, and the surviving Malcev law.
"""

import unittest
from fractions import Fraction

from jordan_bootstrap.dynamics_wall import (
    DynamicsWallCensus,
    IMAGINARY_INDICES,
    associator,
    commutator,
    dynamics_wall_census,
    flow_is_isometric,
    flow_orbit,
    is_alternative,
    jacobi_failure_count,
    jacobiator,
    jacobiator_equals_six_associator,
    malcev_defect,
    malcev_identity_holds,
    moufang_identities_hold,
    ordering_defect,
)
from jordan_bootstrap.octonion import E, octonion


class DynamicsWallTest(unittest.TestCase):
    # --- what survives ---------------------------------------------------

    def test_octonions_are_alternative(self):
        self.assertTrue(is_alternative())

    def test_moufang_identities_hold_on_all_basis_triples(self):
        self.assertTrue(moufang_identities_hold())

    def test_single_generator_flow_is_isometric(self):
        u = octonion(0, Fraction(3, 5), Fraction(4, 5), 0, 0, 0, 0, 0)
        self.assertEqual(u.norm2(), 1)
        orbit = flow_orbit(u, E[5], 6)
        self.assertEqual(len(orbit), 7)
        self.assertTrue(all(x.norm2() == 1 for x in orbit))
        self.assertTrue(flow_is_isometric(u, E[5], 6))

    def test_isometry_rejects_non_unit_generator(self):
        with self.assertRaises(ValueError):
            flow_is_isometric(octonion(2, 0, 0, 0, 0, 0, 0, 0), E[1], 3)

    # --- what breaks: no Lie algebra ------------------------------------

    def test_jacobi_fails_on_168_of_343_triples(self):
        fails, total = jacobi_failure_count()
        self.assertEqual(total, 343)
        self.assertEqual(fails, 168)

    def test_not_a_lie_algebra(self):
        # An explicit non-associating imaginary triple with nonzero Jacobiator.
        j = jacobiator(E[1], E[2], E[4])
        self.assertFalse(j.is_zero())

    def test_quaternion_triple_still_satisfies_jacobi(self):
        # e1, e2, e3 associate (a quaternion subalgebra) -> Jacobiator vanishes.
        self.assertTrue(jacobiator(E[1], E[2], E[3]).is_zero())

    # --- the break IS the non-associativity -----------------------------

    def test_jacobiator_equals_six_times_associator(self):
        self.assertTrue(jacobiator_equals_six_associator())

    def test_jacobiator_six_associator_explicit(self):
        j = jacobiator(E[1], E[2], E[4])
        a = associator(E[1], E[2], E[4]).scaled(6)
        self.assertEqual(j, a)
        # e7 component is exactly 12 on this triple.
        self.assertEqual(j.coords[7], Fraction(12))

    # --- observable path-ordering defect --------------------------------

    def test_ordering_defect_is_associator_and_nonzero(self):
        u = octonion(0, Fraction(3, 5), Fraction(4, 5), 0, 0, 0, 0, 0)
        v = octonion(0, 0, 0, Fraction(5, 13), Fraction(12, 13), 0, 0, 0)
        x = E[5]
        defect = ordering_defect(u, v, x)
        self.assertEqual(defect, associator(u, v, x))
        self.assertFalse(defect.is_zero())

    def test_both_orderings_are_unit_norm(self):
        u = octonion(0, Fraction(3, 5), Fraction(4, 5), 0, 0, 0, 0, 0)
        v = octonion(0, 0, 0, Fraction(5, 13), Fraction(12, 13), 0, 0, 0)
        x = E[5]
        self.assertEqual(((u * v) * x).norm2(), 1)
        self.assertEqual((u * (v * x)).norm2(), 1)

    # --- what replaces the Lie law: Malcev -------------------------------

    def test_malcev_identity_holds_on_all_basis_triples(self):
        self.assertTrue(malcev_identity_holds())

    def test_malcev_defect_zero_but_jacobiator_nonzero(self):
        # The very triples where Jacobi fails still satisfy Malcev exactly.
        self.assertFalse(jacobiator(E[1], E[2], E[4]).is_zero())
        self.assertTrue(malcev_defect(E[1], E[2], E[4]).is_zero())

    # --- census ----------------------------------------------------------

    def test_census(self):
        c = dynamics_wall_census()
        self.assertIsInstance(c, DynamicsWallCensus)
        self.assertTrue(c.alternative)
        self.assertTrue(c.moufang)
        self.assertTrue(c.single_generator_flow_isometric)
        self.assertEqual(c.jacobi_failures, 168)
        self.assertEqual(c.jacobi_triples, 343)
        self.assertFalse(c.is_lie_algebra)
        self.assertTrue(c.jacobiator_is_six_associator)
        self.assertTrue(c.ordering_defect_is_associator)
        self.assertTrue(c.ordering_defect_nonzero)
        self.assertTrue(c.malcev_identity)


if __name__ == "__main__":
    unittest.main()
