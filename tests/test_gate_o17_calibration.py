"""Gate O17 -- exact tests for the associative calibration and G2 3-form.

Pins every claim in ``jordan_bootstrap/calibration.py``: ``phi`` is the totally
antisymmetric associative 3-form (42 nonzero, values +-1/0), the associator is
exactly the coassociative 4-form ``psi`` (168 nonzero), ``g2`` preserves ``phi``,
and the Akivis structure equation holds and collapses to the O15 identity.
"""

import unittest
from fractions import Fraction

from jordan_bootstrap.calibration import (
    CalibrationCensus,
    akivis_collapses_to_six_associator,
    akivis_right_hand_side,
    akivis_structure_equation_holds,
    associative_form,
    associator_from_coassociative,
    associator_matches_coassociative,
    calibration_census,
    coassociative_component,
    coassociative_is_totally_antisymmetric,
    coassociative_nonzero_count,
    derivation_preserves_form,
    form_is_totally_antisymmetric,
    form_nonzero_count,
    g2_preserves_form,
    inner_product,
)
from jordan_bootstrap.dynamics_wall import associator, jacobiator
from jordan_bootstrap.octonion import E


class CalibrationTest(unittest.TestCase):
    # --- the associative 3-form phi -------------------------------------

    def test_phi_totally_antisymmetric(self):
        self.assertTrue(form_is_totally_antisymmetric())

    def test_phi_values_and_count(self):
        values = {
            associative_form(E[i], E[j], E[k])
            for i in range(1, 8) for j in range(1, 8) for k in range(1, 8)
        }
        self.assertEqual(values, {Fraction(-1), Fraction(0), Fraction(1)})
        self.assertEqual(form_nonzero_count(), 42)

    def test_phi_reads_a_fano_line(self):
        # e1 e2 = e3 (a Fano line), so phi(e1, e2, e3) = <e1, e2 e3>... check a
        # concrete nonzero value and its antisymmetry.
        v = associative_form(E[1], E[2], E[3])
        self.assertNotEqual(v, 0)
        self.assertEqual(associative_form(E[2], E[1], E[3]), -v)

    # --- the coassociative 4-form psi = associator ----------------------

    def test_psi_totally_antisymmetric(self):
        self.assertTrue(coassociative_is_totally_antisymmetric())

    def test_psi_values_and_count(self):
        values = {
            coassociative_component(i, j, k, l)
            for i in range(1, 8) for j in range(1, 8)
            for k in range(1, 8) for l in range(1, 8)
        }
        self.assertEqual(values, {Fraction(-1), Fraction(0), Fraction(1)})
        self.assertEqual(coassociative_nonzero_count(), 168)

    def test_associator_is_the_coassociative_form(self):
        self.assertTrue(associator_matches_coassociative())
        # spot check a non-associating triple.
        self.assertEqual(
            associator_from_coassociative(1, 2, 4), associator(E[1], E[2], E[4])
        )

    # --- G2 invariance --------------------------------------------------

    def test_g2_preserves_phi(self):
        self.assertTrue(g2_preserves_form())

    def test_non_derivation_generally_moves_phi(self):
        # A random skew matrix that is not a derivation should not preserve phi.
        # Use the left-multiplication generator L_{e1}, which is in so(7) but not g2.
        from jordan_bootstrap.color_su3 import left_mult_matrix
        self.assertFalse(derivation_preserves_form(left_mult_matrix(E[1])))

    # --- Akivis structure equation --------------------------------------

    def test_akivis_structure_equation(self):
        self.assertTrue(akivis_structure_equation_holds())

    def test_akivis_collapses_to_six_associator(self):
        self.assertTrue(akivis_collapses_to_six_associator())

    def test_akivis_rhs_matches_jacobiator_explicit(self):
        rhs = akivis_right_hand_side(E[1], E[2], E[4])
        self.assertEqual(rhs, jacobiator(E[1], E[2], E[4]))
        self.assertEqual(rhs, associator(E[1], E[2], E[4]).scaled(6))

    def test_inner_product(self):
        self.assertEqual(inner_product(E[3], E[3]), 1)
        self.assertEqual(inner_product(E[3], E[4]), 0)

    # --- census ----------------------------------------------------------

    def test_census(self):
        c = calibration_census()
        self.assertIsInstance(c, CalibrationCensus)
        self.assertTrue(c.form_totally_antisymmetric)
        self.assertEqual(c.form_nonzero, 42)
        self.assertTrue(c.coassociative_totally_antisymmetric)
        self.assertEqual(c.coassociative_nonzero, 168)
        self.assertTrue(c.associator_is_coassociative_form)
        self.assertTrue(c.g2_preserves_form)
        self.assertTrue(c.akivis_structure_equation)
        self.assertTrue(c.akivis_collapses_to_six_associator)


if __name__ == "__main__":
    unittest.main()
