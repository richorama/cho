import unittest
from fractions import Fraction

from jordan_bootstrap.spectral import (
    cayley_hamilton_residual,
    characteristic_coefficients,
    determinant,
    observable,
    spectral_census,
    sylvester_projector,
    _generic_octonionic_matrices,
    _quaternionic_frame,
    _real_frame,
)
from jordan_bootstrap.jordan import equal, is_primitive_idempotent, jordan_product
from jordan_bootstrap.contextuality import ray_to_state


def _zero_matrix(a) -> bool:
    return all(a[i][j].is_zero() for i in range(3) for j in range(3))


class GateO09SpectralTheorem(unittest.TestCase):
    """Octonion premise, Gate O09: the spectral theorem on h_3(O).

    Every Hermitian octonionic observable A resolves as A = sum_i lambda_i P_i with real
    eigenvalues and a Jordan frame of pointer states. Two exact facts carry it: a cubic
    Cayley-Hamilton minimal polynomial holds for arbitrary A (the cubic Jordan structure,
    with N the E_6 determinant), and Sylvester interpolation recovers the frame from A
    alone. This is the last structural prerequisite behind the Born gates O01-O06.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = spectral_census()

    def test_observables_are_hermitian(self) -> None:
        self.assertTrue(self.census.all_observables_hermitian)

    def test_characteristic_coefficients_are_symmetric_functions(self) -> None:
        self.assertEqual(self.census.char_coeff_matches, self.census.rational_cases)
        self.assertTrue(self.census.determinant_equals_eigenvalue_product)

    def test_cayley_hamilton_holds_on_rational_observables(self) -> None:
        self.assertEqual(
            self.census.cayley_hamilton_zero_rational, self.census.rational_cases
        )

    def test_cayley_hamilton_holds_on_generic_octonionic_matrices(self) -> None:
        self.assertEqual(self.census.generic_cases, 2)
        self.assertEqual(
            self.census.cayley_hamilton_zero_generic, self.census.generic_cases
        )
        self.assertTrue(self.census.all_generic_coefficients_rational)

    def test_sylvester_recovers_the_measurement_frame(self) -> None:
        self.assertTrue(self.census.sylvester_recovers_frame)
        self.assertTrue(self.census.eigen_equation_holds)

    def test_spectral_resolution_and_reconstruction(self) -> None:
        self.assertTrue(self.census.resolution_of_identity)
        self.assertTrue(self.census.reconstructs_matrix)

    def test_born_expectation_decomposes_over_the_spectrum(self) -> None:
        self.assertGreater(self.census.born_expectation_checks, 0)
        self.assertEqual(self.census.born_expectation_mismatches, 0)

    # --- explicit witnesses --------------------------------------------------

    def test_explicit_characteristic_coefficients(self) -> None:
        frame = _real_frame(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
        eigs = (Fraction(2), Fraction(-1), Fraction(3))
        a = observable(frame, eigs)
        T, S, N = characteristic_coefficients(a)
        self.assertEqual(T, Fraction(4))     # 2 + (-1) + 3
        self.assertEqual(S, Fraction(1))     # 2*-1 + 2*3 + -1*3
        self.assertEqual(N, Fraction(-6))    # 2 * -1 * 3
        self.assertTrue(_zero_matrix(cayley_hamilton_residual(a)))

    def test_pure_state_has_determinant_zero(self) -> None:
        # A rank-one projector has eigenvalues (1, 0, 0), so its cubic norm vanishes.
        self.assertEqual(determinant(ray_to_state((1, 2, 2))), Fraction(0))

    def test_explicit_sylvester_projector_on_quaternionic_frame(self) -> None:
        frame = _quaternionic_frame()
        eigs = (Fraction(5), Fraction(2), Fraction(-3))
        a = observable(frame, eigs)
        for i in range(3):
            p = sylvester_projector(a, i, eigs)
            self.assertTrue(is_primitive_idempotent(p))
            self.assertTrue(equal(p, frame[i]))
            self.assertTrue(equal(jordan_product(a, p),
                                  tuple(tuple(frame[i][r][c].scaled(eigs[i])
                                              for c in range(3)) for r in range(3))))

    def test_generic_octonionic_matrix_is_annihilated_by_its_cubic(self) -> None:
        a = _generic_octonionic_matrices()[0]
        self.assertTrue(_zero_matrix(cayley_hamilton_residual(a)))


if __name__ == "__main__":
    unittest.main()
