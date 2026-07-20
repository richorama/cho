"""Gate O11 -- one fermion generation's charges from the complex octonions.

Exact assertions over Q(i): the imaginary octonion left-multiplications form a
Clifford algebra; three ladder operators built from them satisfy the canonical
anticommutation relations; the number operator's spectrum has multiplicities
(1,3,3,1) giving electric charges 0, 1/3, 2/3, 1 for one Standard-Model
generation; and the number-preserving bilinears give a colour su(3) commuting
with the U(1) of charge.
"""

import unittest

from jordan_bootstrap.fermion_charges import (
    FermionChargeCensus,
    charge_multiplicities,
    fermion_charge_census,
    ladder_operators,
    number_operator,
    su3_bilinears,
    _cmul,
    _dagger,
    _commutator,
    _is_zero,
    _identity,
    _cequal,
    _anticommutator,
)


class TestGateO11FermionCharges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.census = fermion_charge_census()

    def test_census_type(self):
        self.assertIsInstance(self.census, FermionChargeCensus)

    def test_imaginary_left_mults_form_clifford_algebra(self):
        self.assertTrue(self.census.clifford_relations_hold)

    def test_canonical_anticommutation_relations(self):
        self.assertTrue(self.census.car_creation_annihilation)
        self.assertTrue(self.census.car_annihilation_annihilation)
        self.assertTrue(self.census.ladder_operators_nilpotent)

    def test_number_operator_spectrum_is_one_generation(self):
        # multiplicities (1, 3, 3, 1): singlet, antitriplet, triplet, singlet
        self.assertEqual(self.census.charge_multiplicities, (1, 3, 3, 1))

    def test_electric_charges_are_correct(self):
        # charge = N/3 over the eight Fock states -> 0, 1/3 (x3), 2/3 (x3), 1
        self.assertEqual(
            self.census.charges_times_three, (0, 1, 1, 1, 2, 2, 2, 3)
        )

    def test_colour_su3_is_eight_dimensional_and_closed(self):
        self.assertEqual(self.census.su3_dimension, 8)
        self.assertTrue(self.census.su3_bracket_closed)

    def test_colour_commutes_with_charge(self):
        self.assertTrue(self.census.su3_commutes_with_number)
        self.assertTrue(self.census.number_is_central)

    def test_explicit_car_on_first_mode(self):
        alphas = ladder_operators()
        a0d = _dagger(alphas[0])
        anti = _anticommutator(alphas[0], a0d)
        self.assertTrue(_cequal(anti, _identity()))

    def test_ladder_lowers_number_by_one(self):
        # [N, alpha_k] = -alpha_k : annihilation lowers charge by one unit.
        n = number_operator()
        for a in ladder_operators():
            comm = _commutator(n, a)
            # comm should equal -alpha
            neg = tuple(tuple(-a[i][j] for j in range(8)) for i in range(8))
            self.assertTrue(_cequal(comm, neg))

    def test_multiplicities_sum_to_full_fock_space(self):
        self.assertEqual(sum(charge_multiplicities()), 8)

    def test_su3_generators_preserve_charge_sectors(self):
        # every su(3) generator commutes with N, so it maps each charge
        # eigenspace into itself (colour acts within a charge sector).
        n = number_operator()
        for g in su3_bilinears():
            self.assertTrue(_is_zero(_commutator(g, n)))


if __name__ == "__main__":
    unittest.main()
