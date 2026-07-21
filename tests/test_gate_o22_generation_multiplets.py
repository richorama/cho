"""Gate O22 -- exact tests for one generation's SM multiplets on C (x) H (x) O.

Pins ``jordan_bootstrap/generation_multiplets.py``: the 32-dim module decomposes
under the commuting colour ``su(3)`` and weak ``su(2)`` into the quark/lepton
weak-doublet pattern of one Standard-Model generation.
"""

import unittest

from jordan_bootstrap.generation_multiplets import (
    GenerationMultipletCensus,
    generation_multiplet_census,
    lepton_dimension,
    quark_dimension,
    weak_casimir_is_uniform_doublet,
    weak_singlet_dimension,
)


class GenerationMultipletTest(unittest.TestCase):
    def test_weak_casimir_is_uniform_doublet(self):
        self.assertTrue(weak_casimir_is_uniform_doublet())

    def test_no_weak_singlets(self):
        self.assertEqual(weak_singlet_dimension(), 0)

    def test_lepton_dimension(self):
        self.assertEqual(lepton_dimension(), 8)

    def test_quark_dimension(self):
        self.assertEqual(quark_dimension(), 24)

    def test_census(self):
        c = generation_multiplet_census()
        self.assertIsInstance(c, GenerationMultipletCensus)
        self.assertEqual(c.module_dimension, 32)
        self.assertTrue(c.weak_casimir_uniform_doublet)
        self.assertEqual(c.weak_singlet_dimension, 0)
        self.assertEqual(c.lepton_dimension, 8)
        self.assertEqual(c.quark_dimension, 24)
        self.assertTrue(c.is_one_generation_pattern)


if __name__ == "__main__":
    unittest.main()
