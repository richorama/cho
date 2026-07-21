"""Gate O25 -- chiral projection: discharging the O23 vector-like wall.

Every scientific claim of Gate O25 is pinned to an exact ``Q(i)`` check here.
"""

import unittest

from jordan_bootstrap.chiral_projection import (
    ChiralProjectionCensus,
    aligned_chirality,
    casimir_equals_projector_form,
    chiral_projection_census,
    chirality_commutes_with_charge,
    chirality_eigendimensions,
    chirality_is_involution,
    chirality_is_traceless,
    gauged_su2_relations,
    is_chiral,
    left_handed_dimension,
    left_projector,
    projector_is_idempotent,
    right_handed_dimension,
    ungauged_casimir_is_vector_like,
)


class TestGateO25ChiralProjection(unittest.TestCase):
    def test_chirality_is_an_involution(self):
        """gamma_Q^2 = I -- a genuine chirality."""
        self.assertTrue(chirality_is_involution())

    def test_chirality_is_traceless(self):
        """tr gamma_Q = 0 -- balanced +-1 eigenspaces."""
        self.assertTrue(chirality_is_traceless())

    def test_chirality_eigenspaces_split_four_four(self):
        """gamma_Q has 4-dim + and 4-dim - eigenspaces on the 8-dim O leg."""
        self.assertEqual(chirality_eigendimensions(), (4, 4))

    def test_chirality_commutes_with_charge(self):
        """[N, gamma_Q] = 0 -- the KO-6 alignment (colour axis e_7 dropped)."""
        self.assertTrue(chirality_commutes_with_charge())

    def test_projector_is_idempotent(self):
        """P_L = (1/2)(I + gamma_Q) satisfies P_L^2 = P_L."""
        self.assertTrue(projector_is_idempotent())

    def test_projector_has_rank_four(self):
        """P_L projects onto the 4-dim left-handed sector of the O leg."""
        p = left_projector()
        # trace of an idempotent equals its rank
        tr = sum((p[i][i] for i in range(len(p))), p[0][0] * 0)
        self.assertEqual(tr.real, 4)
        self.assertEqual(tr.imag, 0)

    def test_gauged_generators_close_as_su2(self):
        """[G_1, G_2] = 2 G_3 cyclically -- survives because P_L^2 = P_L."""
        self.assertTrue(gauged_su2_relations())

    def test_gauged_casimir_is_chiral(self):
        """sum_a G_a^2 = (-3 I_H) (x) P_L -- doublet on +, singlet on -."""
        self.assertTrue(casimir_equals_projector_form())

    def test_left_handed_sector_is_a_doublet(self):
        """The Casimir = -3 (weak doublet) sector is 16-dimensional."""
        self.assertEqual(left_handed_dimension(), 16)

    def test_right_handed_sector_is_a_singlet(self):
        """The Casimir = 0 (weak singlet) sector is 16-dimensional."""
        self.assertEqual(right_handed_dimension(), 16)

    def test_construction_is_genuinely_chiral(self):
        """16-dim doublet L + 16-dim singlet R -- inequivalent, hence chiral."""
        self.assertTrue(is_chiral())

    def test_ungauged_weak_casimir_is_vector_like(self):
        """Contrast: bare sum_a W_a^2 = -3 I is -3 on BOTH chirality sectors."""
        self.assertTrue(ungauged_casimir_is_vector_like())

    def test_census_is_fully_consistent(self):
        """The assembled O25 ledger reports the full chiral reconciliation."""
        c = chiral_projection_census()
        self.assertIsInstance(c, ChiralProjectionCensus)
        self.assertTrue(c.chirality_involution)
        self.assertTrue(c.chirality_traceless)
        self.assertEqual(c.eigendimensions, (4, 4))
        self.assertTrue(c.commutes_with_charge)
        self.assertTrue(c.projector_idempotent)
        self.assertTrue(c.gauged_su2)
        self.assertTrue(c.casimir_chiral)
        self.assertEqual(c.left_dimension, 16)
        self.assertEqual(c.right_dimension, 16)
        self.assertTrue(c.is_chiral)
        self.assertTrue(c.ungauged_vector_like)


if __name__ == "__main__":
    unittest.main()
