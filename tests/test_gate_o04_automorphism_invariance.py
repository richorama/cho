import unittest
from fractions import Fraction

from jordan_bootstrap.automorphism import (
    Automorphism,
    apply_jordan,
    apply_octonion,
    automorphism_census,
    automorphism_group,
    is_octonion_automorphism,
)
from jordan_bootstrap.octonion import octonion
from jordan_bootstrap.jordan import is_primitive_idempotent, outer, trace_form


class GateO04AutomorphismInvariance(unittest.TestCase):
    """Octonion premise, Gate O04: Born invariance under the octonion automorphisms.

    Strengthen O00's relabeling to genuine algebra automorphisms. The monomial
    octonion automorphism group has order 1344 = 168 x 8 (the Fano collineation
    group GL(3,2) extended by the 2^3 sign changes, a finite subgroup of G_2).
    Lifted entrywise to h_3(O) each is a Jordan automorphism that preserves the
    trace, maps pure states to pure states, and leaves every Born trace-form
    probability invariant.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = automorphism_census()

    def test_group_order_is_1344_fano_times_signs(self) -> None:
        self.assertEqual(self.census.group_order, 1344)
        self.assertEqual(len(automorphism_group()), 1344)
        # 1344 = 168 x 8; 168 = |GL(3,2)| = |PSL(2,7)|, the Fano-plane group.
        self.assertEqual(self.census.fano_factor, 168)
        self.assertEqual(self.census.group_order, 168 * 8)

    def test_every_element_is_an_octonion_automorphism(self) -> None:
        self.assertTrue(self.census.all_are_octonion_automorphisms)

    def test_automorphisms_preserve_the_octonion_norm(self) -> None:
        self.assertEqual(self.census.norm_checks, 1344)
        self.assertEqual(self.census.norm_mismatches, 0)

    def test_pure_states_map_to_pure_states(self) -> None:
        self.assertEqual(self.census.idempotent_checks, 4032)
        self.assertEqual(self.census.idempotent_failures, 0)

    def test_born_trace_form_is_invariant_under_every_automorphism(self) -> None:
        self.assertEqual(self.census.born_checks, 4032)
        self.assertEqual(self.census.born_mismatches, 0)

    def test_trace_is_preserved(self) -> None:
        self.assertEqual(self.census.trace_checks, 4032)
        self.assertEqual(self.census.trace_mismatches, 0)

    def test_lift_is_a_jordan_automorphism(self) -> None:
        self.assertEqual(self.census.jordan_hom_checks, 4032)
        self.assertEqual(self.census.jordan_hom_failures, 0)

    def test_group_contains_identity_and_is_distinct(self) -> None:
        group = automorphism_group()
        identity = Automorphism(perm=tuple(range(1, 8)), sign=(1,) * 7)
        self.assertIn(identity, group)
        self.assertEqual(len(set(group)), 1344)

    def test_apply_octonion_is_a_multiplicative_homomorphism(self) -> None:
        # Pick a non-identity automorphism and check phi(x y) = phi(x) phi(y).
        group = automorphism_group()
        aut = next(a for a in group if a.perm != tuple(range(1, 8)))
        self.assertTrue(is_octonion_automorphism(aut))
        x = octonion(1, 2, 0, 3, 0, 0, 4, 0)
        y = octonion(0, 1, 5, 0, 2, 0, 0, 3)
        self.assertEqual(
            apply_octonion(aut, x * y).coords,
            (apply_octonion(aut, x) * apply_octonion(aut, y)).coords,
        )

    def test_explicit_state_and_effect_born_probability_is_moved_consistently(self) -> None:
        group = automorphism_group()
        aut = next(a for a in group if a.perm != tuple(range(1, 8)))
        Z = octonion(0, 0, 0, 0, 0, 0, 0, 0)
        p = outer((octonion(Fraction(3, 5), 0, 0, 0, 0, 0, 0, 0),
                   octonion(Fraction(4, 5), 0, 0, 0, 0, 0, 0, 0), Z))
        q = outer((octonion(1, 0, 0, 0, 0, 0, 0, 0), Z, Z))
        moved_p = apply_jordan(aut, p)
        moved_q = apply_jordan(aut, q)
        self.assertTrue(is_primitive_idempotent(moved_p))
        self.assertEqual(trace_form(moved_p, moved_q).coords, trace_form(p, q).coords)


if __name__ == "__main__":
    unittest.main()
