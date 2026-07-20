from fractions import Fraction
import unittest

from jordan_bootstrap.census import representation_invariance_census
from jordan_bootstrap.octonion import (
    E,
    ONE,
    UNIT_OCTONIONS,
    cd_mul,
    cd_norm2,
    octonion,
)


class GateO00RepresentationInvariance(unittest.TestCase):
    """Octonion premise, Gate O00: unit-octonion relabelings cannot move the Born norm.

    This is the octonionic successor to amplitude Gate Q00. The representation
    changes are exact rational unit octonions; the invariant is the Born norm
    |x|^2. Hurwitz multiplicativity makes the invariance exact, genuine non-unit
    controls are rejected, and the algebra's non-associativity is exhibited yet
    irrelevant to the norm invariance.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = representation_invariance_census()

    def test_declared_unit_census_size(self) -> None:
        self.assertEqual(self.census.unit_count, 240)
        self.assertEqual(len(UNIT_OCTONIONS), 240)

    def test_state_census_size(self) -> None:
        self.assertEqual(self.census.state_count, 20)

    def test_unit_multiplication_preserves_the_born_norm_exactly(self) -> None:
        self.assertEqual(self.census.norm_preservation_checks, 4_800)
        self.assertEqual(self.census.norm_mismatches, 0)

    def test_unit_set_is_closed_under_multiplication(self) -> None:
        self.assertEqual(self.census.composition_checks, 57_600)
        self.assertEqual(self.census.composition_non_units, 0)

    def test_non_unit_scaling_control_is_rejected(self) -> None:
        self.assertEqual(self.census.nonunit_control_checks, 60)
        self.assertEqual(self.census.nonunit_control_rejections, 60)

    def test_algebra_is_genuinely_non_associative(self) -> None:
        self.assertEqual(self.census.nonassociative_triples, 168)

    def test_norm_is_multiplicative_hurwitz_identity(self) -> None:
        x = octonion(1, 2, 3, 4, 5, 6, 7, 8)
        y = octonion(8, -7, 6, -5, 4, -3, 2, -1)
        self.assertEqual((x * y).norm2(), x.norm2() * y.norm2())

    def test_every_nonzero_octonion_has_an_exact_two_sided_inverse(self) -> None:
        x = octonion(1, 2, 3, 4, 5, 6, 7, 8)
        self.assertEqual((x * x.inverse()).coords, ONE.coords)
        self.assertEqual((x.inverse() * x).coords, ONE.coords)

    def test_zero_octonion_has_no_inverse(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            octonion(0, 0, 0, 0, 0, 0, 0, 0).inverse()

    def test_ladder_recovers_associative_quaternions(self) -> None:
        # Level-2 Cayley-Dickson (quaternions) is a control: it must associate.
        i = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
        j = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
        k = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
        self.assertEqual(cd_mul(i, j), k)
        self.assertEqual(cd_mul(cd_mul(i, j), k), cd_mul(i, cd_mul(j, k)))

    def test_ladder_kill_condition_sedenions_break_the_norm(self) -> None:
        # One doubling past the octonions the norm stops being multiplicative:
        # this is why the octonions are the last stop (Hurwitz).
        def s(*coords: int):
            return tuple(Fraction(c) for c in coords)

        x = s(0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)
        y = s(0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1)
        self.assertNotEqual(cd_norm2(cd_mul(x, y)), cd_norm2(x) * cd_norm2(y))

    def test_axis_subgroup_recovers_signed_relabeling(self) -> None:
        # The +-e_k units act as the octonionic 'monomial' subgroup: multiplying a
        # state by e_1 permutes-and-signs its coordinates without touching the norm.
        state = octonion(1, 2, 3, 4, 5, 6, 7, 8)
        moved = E[1] * state
        self.assertNotEqual(moved.coords, state.coords)
        self.assertEqual(moved.norm2(), state.norm2())


if __name__ == "__main__":
    unittest.main()
