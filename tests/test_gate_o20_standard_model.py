"""Gate O20 -- exact tests for the Standard Model gauge algebra on C (x) H (x) O.

Pins every claim in ``jordan_bootstrap/standard_model.py``: colour ``su(3)``
(``I_H (x) C_a``) and weak ``su(2)`` (``W_i (x) I_O``) close on the 32-dim
``H (x) O`` module, commute with each other, the ``u(1)`` is central, and the
total algebra is exactly 12-dimensional ``su(3) (+) su(2) (+) u(1)``.
"""

import unittest

from jordan_bootstrap.standard_model import (
    StandardModelGaugeCensus,
    colour_generators,
    colour_is_closed_su3,
    colour_weak_commute,
    gauge_algebra_dimension,
    hypercharge_is_central,
    standard_model_gauge_census,
    weak_generators,
    weak_su2_relations,
)


class StandardModelGaugeTest(unittest.TestCase):
    def test_module_is_thirtytwo_dimensional(self):
        self.assertEqual(len(colour_generators()[0]), 32)

    def test_colour_closes_into_su3(self):
        self.assertTrue(colour_is_closed_su3())

    def test_colour_has_eight_generators(self):
        self.assertEqual(len(colour_generators()), 8)

    def test_weak_su2_relations(self):
        self.assertTrue(weak_su2_relations())

    def test_weak_has_three_generators(self):
        self.assertEqual(len(weak_generators()), 3)

    def test_colour_and_weak_commute(self):
        self.assertTrue(colour_weak_commute())

    def test_hypercharge_is_central(self):
        self.assertTrue(hypercharge_is_central())

    def test_total_dimension_is_twelve(self):
        self.assertEqual(gauge_algebra_dimension(), 12)

    def test_census(self):
        c = standard_model_gauge_census()
        self.assertIsInstance(c, StandardModelGaugeCensus)
        self.assertEqual(c.module_dimension, 32)
        self.assertEqual(c.colour_dimension, 8)
        self.assertTrue(c.colour_closed)
        self.assertEqual(c.weak_dimension, 3)
        self.assertTrue(c.weak_su2_relations)
        self.assertTrue(c.colour_weak_commute)
        self.assertTrue(c.hypercharge_central)
        self.assertEqual(c.total_dimension, 12)
        self.assertTrue(c.is_standard_model_algebra)


if __name__ == "__main__":
    unittest.main()
