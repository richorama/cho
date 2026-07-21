"""Gate O26 -- atmospheric mixing angle sin^2(theta23) = 4/7 as a Fano invariant.

Every scientific claim of Gate O26 is pinned to an exact ``Q`` check here.
"""

import unittest
from fractions import Fraction

from jordan_bootstrap.atmospheric_mixing import (
    AtmosphericMixingCensus,
    atmospheric_mixing_census,
    avoidance_projector,
    collineation_group_order,
    fano_lines,
    group_is_point_transitive,
    is_orthogonal_rank_projector,
    octant_mirror,
    octants_are_complementary,
    sin2_theta23,
    through_projector,
    vacuum_independent,
    vacuum_split,
    value_is_class_invariant,
)


class TestGateO26AtmosphericMixing(unittest.TestCase):
    def test_octonion_triples_are_the_fano_plane(self):
        """The octonion multiplication triples are the 7 lines of PG(2,2)."""
        lines = fano_lines()
        self.assertEqual(len(lines), 7)
        # every point lies on exactly 3 lines (Fano incidence)
        for p in range(1, 8):
            self.assertEqual(sum(1 for line in lines if p in line), 3)

    def test_split_is_three_through_four_avoiding(self):
        """A vacuum point lies on 3 lines and avoids 4."""
        self.assertEqual(vacuum_split(7), (3, 4))

    def test_value_is_vacuum_independent(self):
        """The (3, 4) split holds for every one of the 7 vacuum choices."""
        self.assertTrue(vacuum_independent())

    def test_sin2_theta23_is_four_sevenths(self):
        """The atmospheric prediction sin^2(theta23) = 4/7 (upper octant)."""
        self.assertEqual(sin2_theta23(), Fraction(4, 7))

    def test_value_is_maximal_plus_fano_asymmetry(self):
        """4/7 = 1/2 + 1/14 -- maximal mixing plus the single-line asymmetry."""
        self.assertEqual(sin2_theta23(), Fraction(1, 2) + Fraction(1, 14))

    def test_octant_mirror_and_complementarity(self):
        """The lower-octant mirror is 3/7, with 4/7 + 3/7 = 1."""
        self.assertEqual(octant_mirror(), Fraction(3, 7))
        self.assertTrue(octants_are_complementary())

    def test_avoidance_projector_is_rank4_orthogonal(self):
        """P_avoid is an orthogonal projector with spectrum {1^4, 0^3}."""
        self.assertTrue(is_orthogonal_rank_projector(avoidance_projector(7), 4))

    def test_through_projector_is_rank3_orthogonal(self):
        """The mirror P_through is an orthogonal projector of rank 3."""
        self.assertTrue(is_orthogonal_rank_projector(through_projector(7), 3))

    def test_collineation_group_has_order_168(self):
        """Aut(Fano) = PSL(2,7) has order 168."""
        self.assertEqual(collineation_group_order(), 168)

    def test_group_is_point_transitive(self):
        """The collineation group acts transitively on the 7 points."""
        self.assertTrue(group_is_point_transitive())

    def test_value_is_a_class_invariant(self):
        """Pi_g P_avoid(v) Pi_g^T = P_avoid(g(v)) for all 168 x 7 pairs."""
        self.assertTrue(value_is_class_invariant())

    def test_census_is_fully_consistent(self):
        """The assembled O26 ledger reports the full Fano-invariant result."""
        c = atmospheric_mixing_census()
        self.assertIsInstance(c, AtmosphericMixingCensus)
        self.assertEqual(c.line_count, 7)
        self.assertTrue(c.vacuum_independent)
        self.assertEqual(c.sin2_theta23, Fraction(4, 7))
        self.assertEqual(c.octant_mirror, Fraction(3, 7))
        self.assertTrue(c.octants_complementary)
        self.assertTrue(c.projector_rank4_orthogonal)
        self.assertEqual(c.group_order, 168)
        self.assertTrue(c.point_transitive)
        self.assertTrue(c.value_is_class_invariant)


if __name__ == "__main__":
    unittest.main()
