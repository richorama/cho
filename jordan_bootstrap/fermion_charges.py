"""Gate O11 -- one fermion generation's charges from the complex octonions.

Gate O10 found colour ``su(3)`` as the derivations of ``O`` fixing one imaginary
unit. This gate takes the other half of the Gunaydin-Gursey / Furey picture: it
builds an explicit **fermionic Fock space** inside the complex octonions
``C (x) O`` and reads off the electric charges of a single Standard-Model
generation -- all exactly over the Gaussian rationals ``Q(i)``.

The construction is forced, not fitted:

1. **Clifford algebra.** The seven left-multiplications ``L_{e_k}`` by the
   imaginary octonion units are mutually anticommuting square roots of ``-1``:
   ``{L_i, L_j} = -2 delta_ij I``. They generate ``Cl(0,7)`` acting on the eight
   real dimensions of ``O`` (verified exactly over ``Q``).

2. **Fermionic ladder.** Complexifying with the ``C`` in ``C (x) O`` and pairing
   six of those seven operators gives three ladder operators
   ``alpha_k = (L_{2k-1} + i L_{2k}) / 2``. They satisfy the canonical
   anticommutation relations exactly: ``{alpha_j, alpha_k^dagger} = delta_jk I``,
   ``{alpha_j, alpha_k} = 0`` and ``alpha_k^2 = 0``. So ``C (x) O`` (eight complex
   dimensions) *is* the Fock space of three fermionic modes, ``2^3 = 8`` states.

3. **Charge = number operator.** The number operator
   ``N = sum_k alpha_k^dagger alpha_k`` has exact integer spectrum with
   multiplicities ``(1, 3, 3, 1)`` across eigenvalues ``0, 1, 2, 3`` -- the graded
   pieces ``1 (+) 3bar (+) 3 (+) 1``. Dividing by three gives electric charges
   ``0, 1/3, 2/3, 1``: a neutrino, an anti-down quark (colour ``3bar``), an up
   quark (colour ``3``) and a positron -- one full isospin-up generation.

4. **Unbroken SU(3) x U(1).** The nine bilinears ``alpha_j^dagger alpha_k``
   preserve ``N``; their eight traceless combinations close under the bracket into
   ``su(3)`` (colour), and ``N`` itself generates the commuting ``u(1)`` of
   electric charge. Colour therefore acts inside each charge sector -- trivially on
   the two singlets, as the triplet/antitriplet on the two three-dimensional
   sectors.

Non-claim: this exhibits colour ``SU(3) x U(1)_em`` acting on **one** generation
with the correct charges. It is not the electroweak ``SU(2)``, not the origin of
three generations, and not any dynamics -- it is exact representation theory of
``C (x) O``, no more.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Sequence, Tuple

from amplitude_bootstrap.gaussian import Gaussian
from .octonion import E
from .color_su3 import left_mult_matrix

CMatrix = Tuple[Tuple[Gaussian, ...], ...]

_ZERO = Gaussian(0, 0)
_ONE = Gaussian(1, 0)
_I = Gaussian(0, 1)
_HALF = Gaussian(Fraction(1, 2), 0)


def _complexify(real_matrix) -> CMatrix:
    """Embed a rational 8x8 matrix into Q(i) (zero imaginary part)."""
    return tuple(
        tuple(Gaussian(real_matrix[i][j], 0) for j in range(8)) for i in range(8)
    )


def _cadd(a: CMatrix, b: CMatrix) -> CMatrix:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(8)) for i in range(8))


def _csub(a: CMatrix, b: CMatrix) -> CMatrix:
    return tuple(tuple(a[i][j] - b[i][j] for j in range(8)) for i in range(8))


def _cscale(a: CMatrix, s: Gaussian) -> CMatrix:
    return tuple(tuple(a[i][j] * s for j in range(8)) for i in range(8))


def _cmul(a: CMatrix, b: CMatrix) -> CMatrix:
    n = len(a)
    out = [[_ZERO] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik = a[i][k]
            if aik.is_zero():
                continue
            brow = b[k]
            orow = out[i]
            for j in range(n):
                if not brow[j].is_zero():
                    orow[j] = orow[j] + aik * brow[j]
    return tuple(tuple(row) for row in out)


def _dagger(a: CMatrix) -> CMatrix:
    return tuple(
        tuple(a[j][i].conjugate() for j in range(8)) for i in range(8)
    )


def _anticommutator(a: CMatrix, b: CMatrix) -> CMatrix:
    return _cadd(_cmul(a, b), _cmul(b, a))


def _commutator(a: CMatrix, b: CMatrix) -> CMatrix:
    return _csub(_cmul(a, b), _cmul(b, a))


def _identity() -> CMatrix:
    return tuple(
        tuple(_ONE if i == j else _ZERO for j in range(8)) for i in range(8)
    )


def _cequal(a: CMatrix, b: CMatrix) -> bool:
    return a == b


def _is_zero(a: CMatrix) -> bool:
    return all(a[i][j].is_zero() for i in range(8) for j in range(8))


# -- exact rank / nullity over Q(i) -----------------------------------------


def _rank(matrix: CMatrix) -> int:
    rows = [list(row) for row in matrix]
    if not rows:
        return 0
    cols = len(rows[0])
    pivot_row = 0
    for col in range(cols):
        sel = None
        for r in range(pivot_row, len(rows)):
            if not rows[r][col].is_zero():
                sel = r
                break
        if sel is None:
            continue
        rows[pivot_row], rows[sel] = rows[sel], rows[pivot_row]
        piv = rows[pivot_row][col]
        rows[pivot_row] = [v / piv for v in rows[pivot_row]]
        for r in range(len(rows)):
            if r != pivot_row and not rows[r][col].is_zero():
                f = rows[r][col]
                rows[r] = [rows[r][c] - f * rows[pivot_row][c] for c in range(cols)]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def _nullity(matrix: CMatrix) -> int:
    return 8 - _rank(matrix)


# -- the construction --------------------------------------------------------


def clifford_generators() -> List[CMatrix]:
    """The seven imaginary-octonion left-multiplications as Q(i) matrices."""
    return [_complexify(left_mult_matrix(E[k])) for k in range(1, 8)]


def clifford_defect() -> CMatrix:
    """Sum of ``{L_i, L_j} + 2 delta_ij I`` over imaginaries; zero iff Cl(0,7)."""
    gens = clifford_generators()
    total = tuple(tuple(_ZERO for _ in range(8)) for _ in range(8))
    ident = _identity()
    for i in range(7):
        for j in range(7):
            anti = _anticommutator(gens[i], gens[j])
            want = _cscale(ident, Gaussian(-2, 0)) if i == j else \
                tuple(tuple(_ZERO for _ in range(8)) for _ in range(8))
            total = _cadd(total, _csub(anti, want))
    return total


def ladder_operators() -> List[CMatrix]:
    """Three fermionic annihilation operators ``alpha_k`` from six of the L's."""
    l = [_complexify(left_mult_matrix(E[k])) for k in range(8)]
    alphas = []
    for k in range(3):
        a = 2 * k + 1
        b = 2 * k + 2
        alphas.append(_cscale(_cadd(l[a], _cscale(l[b], _I)), _HALF))
    return alphas


def number_operator() -> CMatrix:
    """``N = sum_k alpha_k^dagger alpha_k`` -- the electric-charge generator x3."""
    total = tuple(tuple(_ZERO for _ in range(8)) for _ in range(8))
    for a in ladder_operators():
        total = _cadd(total, _cmul(_dagger(a), a))
    return total


def charge_multiplicities() -> Tuple[int, ...]:
    """Multiplicities of eigenvalues 0,1,2,3 of ``N`` (exact, over Q(i))."""
    n = number_operator()
    ident = _identity()
    mults = []
    for value in range(4):
        shifted = _csub(n, _cscale(ident, Gaussian(value, 0)))
        mults.append(_nullity(shifted))
    return tuple(mults)


def su3_bilinears() -> List[CMatrix]:
    """The eight traceless number-preserving bilinears ``alpha_j^dagger alpha_k``.

    The nine operators ``alpha_j^dagger alpha_k`` span ``u(3)``; removing the
    trace direction ``N`` leaves the eight generators of colour ``su(3)``.
    """
    alphas = ladder_operators()
    daggers = [_dagger(a) for a in alphas]
    raw = [[_cmul(daggers[j], alphas[k]) for k in range(3)] for j in range(3)]
    n = number_operator()
    third = Gaussian(Fraction(1, 3), 0)
    generators: List[CMatrix] = []
    # Off-diagonal ladders (6) plus two traceless Cartan combinations (2).
    for j in range(3):
        for k in range(3):
            if j != k:
                generators.append(raw[j][k])
    generators.append(_csub(raw[0][0], raw[1][1]))
    generators.append(_csub(raw[1][1], raw[2][2]))
    return generators


def _flatten(m: CMatrix) -> Tuple[Gaussian, ...]:
    return tuple(m[i][j] for i in range(8) for j in range(8))


def _independent_dimension(mats: Sequence[CMatrix]) -> int:
    """Exact dimension of the Q(i)-span of a list of matrices."""
    rows = [list(_flatten(m)) for m in mats]
    return _rank(tuple(tuple(r) for r in rows))


@dataclass(frozen=True)
class FermionChargeCensus:
    """Exact certificate: one generation's SU(3) x U(1) charges from C (x) O."""

    clifford_relations_hold: bool
    car_creation_annihilation: bool
    car_annihilation_annihilation: bool
    ladder_operators_nilpotent: bool
    charge_multiplicities: Tuple[int, ...]
    charges_times_three: Tuple[int, ...]
    su3_dimension: int
    su3_bracket_closed: bool
    su3_commutes_with_number: bool
    number_is_central: bool


def fermion_charge_census() -> FermionChargeCensus:
    alphas = ladder_operators()
    daggers = [_dagger(a) for a in alphas]
    ident = _identity()

    # Canonical anticommutation relations.
    car_cd = True
    for j in range(3):
        for k in range(3):
            anti = _anticommutator(alphas[j], daggers[k])
            want = ident if j == k else \
                tuple(tuple(_ZERO for _ in range(8)) for _ in range(8))
            if not _cequal(anti, want):
                car_cd = False
    car_aa = all(
        _is_zero(_anticommutator(alphas[j], alphas[k]))
        for j in range(3) for k in range(3)
    )
    nilpotent = all(_is_zero(_cmul(a, a)) for a in alphas)

    mults = charge_multiplicities()

    n = number_operator()
    su3 = su3_bilinears()
    su3_dim = _independent_dimension(su3)
    su3_closed = _independent_dimension(
        list(su3) + [_commutator(su3[a], su3[b])
                     for a in range(len(su3)) for b in range(a + 1, len(su3))]
    ) == su3_dim
    su3_commutes = all(_is_zero(_commutator(g, n)) for g in su3)
    central = all(
        _is_zero(_commutator(n, _cmul(_dagger(alphas[j]), alphas[k])))
        for j in range(3) for k in range(3)
    )

    return FermionChargeCensus(
        clifford_relations_hold=_is_zero(clifford_defect()),
        car_creation_annihilation=car_cd,
        car_annihilation_annihilation=car_aa,
        ladder_operators_nilpotent=nilpotent,
        charge_multiplicities=mults,
        charges_times_three=tuple(v for v, m in enumerate(mults) for _ in range(m)),
        su3_dimension=su3_dim,
        su3_bracket_closed=su3_closed,
        su3_commutes_with_number=su3_commutes,
        number_is_central=central,
    )
