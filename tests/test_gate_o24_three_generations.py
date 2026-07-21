"""Gate O24 -- exact tests for three generations as a Jordan frame of J_3(O).

Pins ``jordan_bootstrap/three_generations.py``: the three generations are the
three primitive idempotents of a J_3(O) frame (a resolution of the identity),
linearly independent (unlike the O12 triality towers), with the Peirce
decomposition ``3 + 24 = 27``.
"""

import unittest

from jordan_bootstrap.three_generations import (
    GenerationFrameCensus,
    family_count,
    frame_resolves_identity,
    generation_frame_census,
    generation_slot_dimension,
    idempotent_span_dimension,
    offdiagonal_dimension,
    peirce_spectrum,
    standard_generation_frame,
)


class GenerationFrameTest(unittest.TestCase):
    def test_family_count_three(self):
        self.assertEqual(family_count(), 3)

    def test_frame_resolves_identity(self):
        self.assertTrue(frame_resolves_identity())

    def test_idempotents_are_independent(self):
        self.assertEqual(idempotent_span_dimension(), 3)

    def test_peirce_spectrum(self):
        spectrum = peirce_spectrum(standard_generation_frame()[0])
        self.assertEqual(spectrum, {"1": 1, "1/2": 16, "0": 10})

    def test_generation_slot_dimension(self):
        self.assertEqual(generation_slot_dimension(), 3)

    def test_offdiagonal_dimension(self):
        self.assertEqual(offdiagonal_dimension(), 24)

    def test_census(self):
        c = generation_frame_census()
        self.assertIsInstance(c, GenerationFrameCensus)
        self.assertEqual(c.family_count, 3)
        self.assertTrue(c.frame_resolves_identity)
        self.assertEqual(c.idempotent_span_dimension, 3)
        self.assertEqual(dict(c.peirce_spectrum), {"1": 1, "1/2": 16, "0": 10})
        self.assertEqual(c.generation_slot_dimension, 3)
        self.assertEqual(c.offdiagonal_dimension, 24)
        self.assertEqual(c.total_dimension, 27)
        self.assertTrue(c.is_rank_three_frame)


if __name__ == "__main__":
    unittest.main()
