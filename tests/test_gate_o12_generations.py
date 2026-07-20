"""Gate O12 -- three generations via triality: an honest negative result.

Exact assertions over Q(i): three triality-related pairings of the octonionic
ladder each give a (1,3,3,1) generation spectrum and are cyclically permuted by
an order-three axis map, but their Fock towers coincide as a single 8-complex-
dimensional module -- so triality does NOT yield three independent generations
within C(x)O.
"""

import unittest

from jordan_bootstrap.generations import (
    GenerationCensus,
    PAIRINGS,
    charge_spectrum,
    fock_tower,
    generation_census,
    ladders_from,
    number_from,
    _rank,
)


class TestGateO12Generations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.census = generation_census()

    def test_census_type(self):
        self.assertIsInstance(self.census, GenerationCensus)

    def test_triality_cycle_has_order_three(self):
        self.assertTrue(self.census.triality_cycle_order_three)

    def test_triality_cycles_the_three_pairings(self):
        self.assertTrue(self.census.triality_cycles_the_pairings)

    def test_each_pairing_reproduces_one_generation(self):
        self.assertTrue(self.census.each_pairing_gives_one_generation)
        for spectrum in self.census.per_pairing_spectra:
            self.assertEqual(spectrum, (1, 3, 3, 1))

    def test_each_tower_spans_the_full_module(self):
        self.assertTrue(self.census.each_tower_spans_full_module)

    def test_the_three_towers_coincide_as_one_module(self):
        # The honest crux: combined span is 8, not 24.
        self.assertEqual(self.census.combined_span_dimension, 8)
        self.assertTrue(self.census.three_towers_coincide_as_one_module)

    def test_three_generations_are_not_independent(self):
        self.assertFalse(self.census.three_generations_are_independent)

    def test_vacua_are_not_three_independent_states(self):
        # even the three vacua span only 2 dimensions, not 3
        self.assertEqual(self.census.vacua_span_dimension, 2)

    def test_generation_problem_is_unsolved_here(self):
        self.assertTrue(self.census.generation_problem_unsolved_here)

    def test_there_are_three_declared_pairings(self):
        self.assertEqual(len(PAIRINGS), 3)

    def test_explicit_first_pairing_is_one_generation(self):
        spectrum = charge_spectrum(number_from(ladders_from(PAIRINGS[0])))
        self.assertEqual(spectrum, (1, 3, 3, 1))

    def test_explicit_combined_span_is_eight(self):
        towers = [fock_tower(p) for p in PAIRINGS]
        combined = _rank([s for t in towers for s in t])
        self.assertEqual(combined, 8)


if __name__ == "__main__":
    unittest.main()
