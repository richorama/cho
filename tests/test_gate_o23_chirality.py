"""Gate O23 -- exact tests for handedness and the vector-like wall on C (x) H (x) O.

Pins ``jordan_bootstrap/chirality.py``: the canonical handedness projector from
the second (right) ``su(2)`` splits each generation into two gauge-invariant
halves, but both are pure weak doublets -- the construction is vector-like and
does not produce the Standard Model's chiral asymmetry.
"""

import unittest

from jordan_bootstrap.chirality import (
    ChiralityCensus,
    chirality_census,
    handedness_dimensions,
    is_vector_like,
    left_right_commute,
    projector_commutes_with_gauge,
    projector_is_idempotent,
    right_su2_relations,
    weak_casimir_uniform_doublet,
)


class ChiralityTest(unittest.TestCase):
    def test_right_su2_relations(self):
        self.assertTrue(right_su2_relations())

    def test_left_right_commute(self):
        self.assertTrue(left_right_commute())

    def test_projector_is_idempotent(self):
        self.assertTrue(projector_is_idempotent())

    def test_handedness_dimensions(self):
        self.assertEqual(handedness_dimensions(), (16, 16))

    def test_projector_commutes_with_gauge(self):
        self.assertTrue(projector_commutes_with_gauge())

    def test_weak_casimir_uniform_doublet(self):
        self.assertTrue(weak_casimir_uniform_doublet())

    def test_is_vector_like(self):
        self.assertTrue(is_vector_like())

    def test_census(self):
        c = chirality_census()
        self.assertIsInstance(c, ChiralityCensus)
        self.assertTrue(c.right_su2_relations)
        self.assertTrue(c.left_right_commute)
        self.assertTrue(c.projector_idempotent)
        self.assertEqual(c.handedness_dimensions, (16, 16))
        self.assertTrue(c.projector_commutes_with_gauge)
        self.assertTrue(c.weak_casimir_uniform_doublet)
        self.assertTrue(c.is_vector_like)
        self.assertFalse(c.produces_chiral_asymmetry)


if __name__ == "__main__":
    unittest.main()
