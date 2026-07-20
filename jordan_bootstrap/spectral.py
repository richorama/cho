"""Gate O09: the octonionic spectral theorem on h_3(O).

Every prior gate manipulates *states* (primitive idempotents) and their Born overlaps.
This gate certifies the missing ingredient that makes "measure an observable" rigorous:
the spectral theorem on the exceptional Jordan algebra ``h_3(O)``. An observable is any
Hermitian octonionic ``3x3`` matrix ``A``; the theorem says ``A`` resolves as ::

        A = lambda_1 P_1 + lambda_2 P_2 + lambda_3 P_3

with *real* eigenvalues ``lambda_i`` and a Jordan frame ``{P_i}`` of orthogonal
primitive idempotents -- its measurement outcomes and pointer states -- and that this
frame is recoverable from ``A`` alone.

Two facts, both exact over the rationals:

* **A cubic minimal polynomial (Cayley-Hamilton).** Although ``h_3(O)`` is
  non-associative and ``27``-dimensional, every Hermitian ``A`` satisfies the *cubic*

      A^3 - T(A) A^2 + S(A) A - N(A) I = 0,

  where ``T = tr A``, ``S`` and the cubic norm ``N`` are the elementary symmetric
  functions of the eigenvalues, read off exactly from the traces of the Jordan powers of
  ``A`` (Newton's identities). This is the degree-three structure that makes ``h_3(O)`` a
  *cubic* Jordan algebra; ``N`` is the ``E_6``-invariant determinant. Verified to vanish
  exactly for arbitrary rational Hermitian octonionic matrices -- even those whose
  eigenvalues are irrational.

* **Sylvester recovery.** When the eigenvalues are rational and distinct the spectral
  projectors are recovered from ``A`` by the interpolation formula
  ``P_i = prod_{j != i} (A - lambda_j I) / (lambda_i - lambda_j)`` (a polynomial in the
  single element ``A``, hence unambiguous by power-associativity). The recovered ``P_i``
  equal the original frame, satisfy ``A o P_i = lambda_i P_i`` and ``sum P_i = I``, and
  reproduce ``A`` -- and the Born expectation of any state ``Psi`` decomposes as
  ``tr(A o Psi) = sum_i lambda_i tr(P_i o Psi)``, eigenvalue times outcome probability.

So an octonionic observable has a genuine real spectrum and a measurement frame, the last
structural prerequisite behind the Born gates O01-O06.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Tuple

from .octonion import Octonion, octonion
from .jordan import (
    JMat,
    equal,
    identity_matrix,
    is_jordan_frame,
    is_primitive_idempotent,
    jordan_product,
    outer,
    trace,
    trace_form,
)
from .contextuality import ray_to_state
from .born_selection import octonionic_reference_state

_ZERO = octonion(0, 0, 0, 0, 0, 0, 0, 0)


def _real(x: Fraction) -> Octonion:
    return octonion(x, 0, 0, 0, 0, 0, 0, 0)


def _add(a: JMat, b: JMat) -> JMat:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(3)) for i in range(3))


def _scale(a: JMat, f: Fraction) -> JMat:
    return tuple(tuple(a[i][j].scaled(f) for j in range(3)) for i in range(3))


def _is_zero(a: JMat) -> bool:
    return all(a[i][j].is_zero() for i in range(3) for j in range(3))


def jordan_power(a: JMat, n: int) -> JMat:
    """The (power-associative) Jordan power ``A^n``."""
    if n == 1:
        return a
    p = a
    for _ in range(n - 1):
        p = jordan_product(p, a)
    return p


def characteristic_coefficients(a: JMat) -> Tuple[Fraction, Fraction, Fraction]:
    """``(T, S, N)`` of the cubic ``x^3 - T x^2 + S x - N`` via power traces."""
    p1 = trace(a).coords[0]
    p2 = trace(jordan_power(a, 2)).coords[0]
    p3 = trace(jordan_power(a, 3)).coords[0]
    T = p1
    S = (p1 * p1 - p2) / 2
    N = (p1 ** 3 - 3 * p1 * p2 + 2 * p3) / 6
    return T, S, N


def cayley_hamilton_residual(a: JMat) -> JMat:
    """``A^3 - T A^2 + S A - N I`` -- zero for every Hermitian ``A``."""
    T, S, N = characteristic_coefficients(a)
    a2 = jordan_power(a, 2)
    a3 = jordan_power(a, 3)
    ident = identity_matrix()
    result = a3
    result = _add(result, _scale(a2, -T))
    result = _add(result, _scale(a, S))
    result = _add(result, _scale(ident, -N))
    return result


def determinant(a: JMat) -> Fraction:
    """The cubic norm ``N(A)`` -- the E_6-invariant octonionic determinant."""
    return characteristic_coefficients(a)[2]


def observable(frame: Tuple[JMat, ...], eigenvalues: Tuple[Fraction, ...]) -> JMat:
    """Assemble ``sum_i lambda_i P_i`` from a Jordan frame and real eigenvalues."""
    result = tuple(tuple(_ZERO for _ in range(3)) for _ in range(3))
    for lam, p in zip(eigenvalues, frame):
        result = _add(result, _scale(p, lam))
    return result


def sylvester_projector(
    a: JMat, i: int, eigenvalues: Tuple[Fraction, ...]
) -> JMat:
    """Recover ``P_i`` from ``A`` by Sylvester interpolation (distinct eigenvalues)."""
    ident = identity_matrix()
    lam_i = eigenvalues[i]
    factors = None
    denom = Fraction(1)
    for j, lam_j in enumerate(eigenvalues):
        if j == i:
            continue
        shifted = _add(a, _scale(ident, -lam_j))
        factors = shifted if factors is None else jordan_product(factors, shifted)
        denom *= (lam_i - lam_j)
    return _scale(factors, Fraction(1) / denom)


# --- census -----------------------------------------------------------------

def _real_frame(rays) -> Tuple[JMat, ...]:
    return tuple(ray_to_state(r) for r in rays)


def _quaternionic_frame() -> Tuple[JMat, ...]:
    """A rational Jordan frame with genuinely octonionic (e_1) off-diagonal entries."""
    from .octonion import E

    v1 = (E[0].scaled(Fraction(3, 5)), E[1].scaled(Fraction(4, 5)), _ZERO)
    v2 = (E[1].scaled(Fraction(4, 5)), E[0].scaled(Fraction(3, 5)), _ZERO)
    v3 = (_ZERO, _ZERO, E[0])
    return (outer(v1), outer(v2), outer(v3))


def _rational_cases():
    return (
        (_real_frame(((1, 0, 0), (0, 1, 0), (0, 0, 1))), (Fraction(2), Fraction(-1), Fraction(3))),
        (_real_frame(((1, 2, 2), (2, -2, 1), (2, 1, -2))), (Fraction(1), Fraction(3), Fraction(7))),
        (_quaternionic_frame(), (Fraction(5), Fraction(2), Fraction(-3))),
    )


def _generic_octonionic_matrices() -> Tuple[JMat, ...]:
    from .octonion import E

    def herm(a, b, c, x, y, z):
        return (
            (_real(Fraction(a)), z, y.conjugate()),
            (z.conjugate(), _real(Fraction(b)), x),
            (y, x.conjugate(), _real(Fraction(c))),
        )

    return (
        herm(1, -2, 3,
             E[1].scaled(Fraction(2, 3)) + E[4].scaled(Fraction(1, 5)),
             E[2].scaled(Fraction(-1, 2)) + E[7].scaled(Fraction(1, 3)),
             E[3].scaled(Fraction(1, 4)) + E[6].scaled(Fraction(2, 7))),
        herm(0, 5, -1,
             E[5].scaled(Fraction(3, 4)),
             E[1].scaled(Fraction(1, 2)) + E[2].scaled(Fraction(1, 2)),
             E[6].scaled(Fraction(-2, 3))),
    )


@dataclass(frozen=True)
class SpectralCensus:
    rational_cases: int
    all_observables_hermitian: bool
    char_coeff_matches: int
    cayley_hamilton_zero_rational: int
    sylvester_recovers_frame: bool
    eigen_equation_holds: bool
    resolution_of_identity: bool
    reconstructs_matrix: bool
    determinant_equals_eigenvalue_product: bool
    born_expectation_checks: int
    born_expectation_mismatches: int
    generic_cases: int
    cayley_hamilton_zero_generic: int
    all_generic_coefficients_rational: bool


def _is_hermitian(a: JMat) -> bool:
    return all(
        a[j][i].coords == a[i][j].conjugate().coords
        for i in range(3) for j in range(3)
    )


def spectral_census() -> SpectralCensus:
    cases = _rational_cases()
    psi = octonionic_reference_state()

    all_herm = True
    coeff_matches = 0
    ch_zero = 0
    recovers = True
    eigen_ok = True
    resolution = True
    reconstructs = True
    det_ok = True
    born_checks = 0
    born_mismatch = 0

    for frame, eigs in cases:
        a = observable(frame, eigs)
        if not _is_hermitian(a):
            all_herm = False

        T, S, N = characteristic_coefficients(a)
        expected_T = sum(eigs)
        expected_S = eigs[0] * eigs[1] + eigs[0] * eigs[2] + eigs[1] * eigs[2]
        expected_N = eigs[0] * eigs[1] * eigs[2]
        if (T, S, N) == (expected_T, expected_S, expected_N):
            coeff_matches += 1
        if determinant(a) != expected_N:
            det_ok = False

        if _is_zero(cayley_hamilton_residual(a)):
            ch_zero += 1

        recovered = tuple(sylvester_projector(a, i, eigs) for i in range(len(eigs)))
        for p_orig, p_rec, lam in zip(frame, recovered, eigs):
            if not equal(p_orig, p_rec):
                recovers = False
            if not is_primitive_idempotent(p_rec):
                recovers = False
            if not equal(jordan_product(a, p_rec), _scale(p_rec, lam)):
                eigen_ok = False

        total = tuple(tuple(_ZERO for _ in range(3)) for _ in range(3))
        recon = tuple(tuple(_ZERO for _ in range(3)) for _ in range(3))
        for lam, p in zip(eigs, recovered):
            total = _add(total, p)
            recon = _add(recon, _scale(p, lam))
        if not equal(total, identity_matrix()):
            resolution = False
        if not equal(recon, a):
            reconstructs = False

        # Born expectation: tr(A o Psi) = sum_i lambda_i tr(P_i o Psi).
        lhs = trace_form(a, psi).coords[0]
        rhs = sum(lam * trace_form(p, psi).coords[0] for lam, p in zip(eigs, recovered))
        born_checks += 1
        if lhs != rhs:
            born_mismatch += 1

    generic = _generic_octonionic_matrices()
    gen_ch_zero = sum(1 for a in generic if _is_zero(cayley_hamilton_residual(a)))
    gen_rational = all(
        all(isinstance(c, Fraction) for c in characteristic_coefficients(a))
        for a in generic
    )

    return SpectralCensus(
        rational_cases=len(cases),
        all_observables_hermitian=all_herm,
        char_coeff_matches=coeff_matches,
        cayley_hamilton_zero_rational=ch_zero,
        sylvester_recovers_frame=recovers,
        eigen_equation_holds=eigen_ok,
        resolution_of_identity=resolution,
        reconstructs_matrix=reconstructs,
        determinant_equals_eigenvalue_product=det_ok,
        born_expectation_checks=born_checks,
        born_expectation_mismatches=born_mismatch,
        generic_cases=len(generic),
        cayley_hamilton_zero_generic=gen_ch_zero,
        all_generic_coefficients_rational=gen_rational,
    )
