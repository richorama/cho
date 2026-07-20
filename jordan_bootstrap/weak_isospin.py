"""Gate O13 -- weak isospin su(2) from the quaternion factor.

Gate O10/O11 pulled colour ``su(3)`` and one generation's electric charges out
of the octonions ``O``. The Standard Model's other non-abelian factor, the weak
isospin ``SU(2)_L``, does not live in ``O`` -- in the Furey/Dixon programme it
comes from the *quaternions* ``H``. This gate builds it explicitly and exactly
over ``Q(i)``, and is scrupulous about the boundary.

The quaternions sit one rung below the octonions on the Cayley-Dickson ladder
``R -> C -> H -> O`` that the octonion module already implements. Two facts,
checked exactly over the rationals:

1. **``su(2)`` is the imaginary quaternion left-multiplications.** Because ``H``
   is associative, ``L_a L_b = L_{ab}``, so the three imaginary units obey
   ``[L_i, L_j] = 2 L_k`` and cyclically, with ``L_a^2 = -I``. That *is* the weak
   isospin Lie algebra ``su(2)`` (dimension 3, bracket closed, compact). The unit
   quaternions themselves form the group ``SU(2) = Sp(1)``.

2. **An isospin doublet.** Complexifying with the ``C`` in ``C (x) H`` and pairing
   two of the generators gives one fermionic ladder ``beta = (L_i + i L_j)/2``
   with ``{beta, beta^dagger} = I`` and ``beta^2 = 0``. Its number operator has
   eigenvalues ``0`` and ``1``; shifting by ``-1/2`` gives the third isospin
   component ``T_3 = -1/2, +1/2`` -- a left-handed weak doublet (down-type,
   up-type). ``C (x) H`` carries two such doublets.

Non-claim: this exhibits ``su(2)`` weak isospin and its doublet from ``H`` alone.
It is a *separate* algebra from the octonionic colour ``su(3)`` of Gate O10/O11;
this gate does **not** assemble the full Standard-Model gauge group
``SU(3) x SU(2) x U(1)`` on the tensor product ``C (x) H (x) O`` (Furey 2018), nor
does it address chirality dynamics or the Higgs mechanism that actually breaks
``SU(2)_L``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Tuple

from amplitude_bootstrap.gaussian import Gaussian
from .octonion import cd_mul

RMatrix = Tuple[Tuple[Fraction, ...], ...]
CMatrix = Tuple[Tuple[Gaussian, ...], ...]

_ZERO = Gaussian(0, 0)
_ONE = Gaussian(1, 0)
_I = Gaussian(0, 1)
_HALF = Gaussian(Fraction(1, 2), 0)

_DIM = 4  # quaternions are four real dimensions


def _qunit(k: int) -> Tuple[Fraction, ...]:
    return tuple(Fraction(1) if t == k else Fraction(0) for t in range(_DIM))


def quaternion_left_mult(k: int) -> RMatrix:
    """Left multiplication by the ``k``-th quaternion unit as a 4x4 rational matrix."""
    cols = [cd_mul(_qunit(k), _qunit(j)) for j in range(_DIM)]
    return tuple(tuple(cols[j][i] for j in range(_DIM)) for i in range(_DIM))


# -- real 4x4 helpers --------------------------------------------------------


def _rmul(a: RMatrix, b: RMatrix) -> RMatrix:
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(_DIM)), Fraction(0))
              for j in range(_DIM))
        for i in range(_DIM)
    )


def _rcomm(a: RMatrix, b: RMatrix) -> RMatrix:
    ab = _rmul(a, b)
    ba = _rmul(b, a)
    return tuple(tuple(ab[i][j] - ba[i][j] for j in range(_DIM)) for i in range(_DIM))


def _rscale(a: RMatrix, s: Fraction) -> RMatrix:
    return tuple(tuple(a[i][j] * s for j in range(_DIM)) for i in range(_DIM))


def _rident(sign: int = 1) -> RMatrix:
    return tuple(
        tuple(Fraction(sign) if i == j else Fraction(0) for j in range(_DIM))
        for i in range(_DIM)
    )


# -- complex 4x4 helpers -----------------------------------------------------


def _complexify(m: RMatrix) -> CMatrix:
    return tuple(tuple(Gaussian(m[i][j], 0) for j in range(_DIM)) for i in range(_DIM))


def _cmul(a: CMatrix, b: CMatrix) -> CMatrix:
    out = [[_ZERO] * _DIM for _ in range(_DIM)]
    for i in range(_DIM):
        for k in range(_DIM):
            aik = a[i][k]
            if aik.is_zero():
                continue
            for j in range(_DIM):
                if not b[k][j].is_zero():
                    out[i][j] = out[i][j] + aik * b[k][j]
    return tuple(tuple(r) for r in out)


def _cadd(a: CMatrix, b: CMatrix) -> CMatrix:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(_DIM)) for i in range(_DIM))


def _csub(a: CMatrix, b: CMatrix) -> CMatrix:
    return tuple(tuple(a[i][j] - b[i][j] for j in range(_DIM)) for i in range(_DIM))


def _cscale(a: CMatrix, s: Gaussian) -> CMatrix:
    return tuple(tuple(a[i][j] * s for j in range(_DIM)) for i in range(_DIM))


def _dagger(a: CMatrix) -> CMatrix:
    return tuple(
        tuple(a[j][i].conjugate() for j in range(_DIM)) for i in range(_DIM)
    )


def _cident() -> CMatrix:
    return tuple(
        tuple(_ONE if i == j else _ZERO for j in range(_DIM)) for i in range(_DIM)
    )


def _cequal(a: CMatrix, b: CMatrix) -> bool:
    return a == b


def _cis_zero(a: CMatrix) -> bool:
    return all(a[i][j].is_zero() for i in range(_DIM) for j in range(_DIM))


def _crank(matrix: CMatrix) -> int:
    rows = [list(row) for row in matrix]
    cols = _DIM
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


def isospin_ladder() -> CMatrix:
    """One fermionic isospin ladder ``beta = (L_i + i L_j)/2`` over Q(i)."""
    li = _complexify(quaternion_left_mult(1))
    lj = _complexify(quaternion_left_mult(2))
    return _cscale(_cadd(li, _cscale(lj, _I)), _HALF)


def isospin_number_operator() -> CMatrix:
    beta = isospin_ladder()
    return _cmul(_dagger(beta), beta)


@dataclass(frozen=True)
class WeakIsospinCensus:
    su2_bracket_relations: bool
    su2_generators_square_to_minus_one: bool
    su2_dimension: int
    su2_bracket_closed: bool
    car_holds: bool
    ladder_nilpotent: bool
    number_multiplicities: Tuple[int, ...]
    doublet_count: int


def _independent_dimension(mats: List[RMatrix]) -> int:
    rows = [[m[i][j] for i in range(_DIM) for j in range(_DIM)] for m in mats]
    # exact rational rank
    pivot_row = 0
    cols = _DIM * _DIM
    R = [list(r) for r in rows]
    for col in range(cols):
        sel = None
        for r in range(pivot_row, len(R)):
            if R[r][col] != 0:
                sel = r
                break
        if sel is None:
            continue
        R[pivot_row], R[sel] = R[sel], R[pivot_row]
        piv = R[pivot_row][col]
        R[pivot_row] = [v / piv for v in R[pivot_row]]
        for r in range(len(R)):
            if r != pivot_row and R[r][col] != 0:
                f = R[r][col]
                R[r] = [R[r][c] - f * R[pivot_row][c] for c in range(cols)]
        pivot_row += 1
        if pivot_row == len(R):
            break
    return pivot_row


def weak_isospin_census() -> WeakIsospinCensus:
    li, lj, lk = (quaternion_left_mult(k) for k in (1, 2, 3))

    relations = (
        _rcomm(li, lj) == _rscale(lk, Fraction(2))
        and _rcomm(lj, lk) == _rscale(li, Fraction(2))
        and _rcomm(lk, li) == _rscale(lj, Fraction(2))
    )
    squares = all(
        _rmul(g, g) == _rident(-1) for g in (li, lj, lk)
    )
    dim = _independent_dimension([li, lj, lk])
    brackets = [_rcomm(li, lj), _rcomm(lj, lk), _rcomm(lk, li)]
    closed = _independent_dimension([li, lj, lk] + brackets) == dim

    beta = isospin_ladder()
    bd = _dagger(beta)
    car = _cequal(_cadd(_cmul(beta, bd), _cmul(bd, beta)), _cident())
    nilpotent = _cis_zero(_cmul(beta, beta))

    n = isospin_number_operator()
    ident = _cident()
    mults = []
    for value in range(2):
        shifted = _csub(n, _cscale(ident, Gaussian(value, 0)))
        mults.append(_DIM - _crank(shifted))

    return WeakIsospinCensus(
        su2_bracket_relations=relations,
        su2_generators_square_to_minus_one=squares,
        su2_dimension=dim,
        su2_bracket_closed=closed,
        car_holds=car,
        ladder_nilpotent=nilpotent,
        number_multiplicities=tuple(mults),
        doublet_count=mults[1] if mults else 0,
    )
