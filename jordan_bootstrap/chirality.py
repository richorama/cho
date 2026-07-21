"""Gate O23 -- handedness and the vector-like wall: chirality on C (x) H (x) O.

Gate O22 found the multiplet *pattern* of one generation but noted it comes
*doubled* -- every state is a weak doublet, with no chiral (left-only) asymmetry.
This gate confronts chirality head-on, and is scrupulously honest about where the
algebra succeeds and where it stops.

The quaternion factor carries *two* commuting ``su(2)``s -- the algebra
``C (x) H = M_2(C)`` has ``so(4) = su(2)_L (+) su(2)_R``:

* **``su(2)_L``** is the weak isospin of Gates O13/O20: imaginary quaternion
  **left** multiplications ``W_i`` (``[W_i, W_j] = 2 W_k``).
* **``su(2)_R``** is imaginary quaternion **right** multiplications ``R_i``
  (``[R_i, R_j] = -2 R_k``). Because ``H`` is associative, left and right
  multiplications commute: ``[W_i, R_j] = 0``.

The right action supplies a **canonical handedness projector** built from the
``C`` of ``C (x) H`` and one right unit,

    P = (1/2) (I + i R_1),   P^2 = P,

which commutes with the *entire* Standard-Model gauge algebra (colour on the
``O`` factor; weak, since ``[W, R] = 0``). On the 32-dim module ``P`` and ``I - P``
each project onto a 16-dimensional, gauge-invariant half -- the two minimal left
ideals of ``C (x) H``, a "left-handed" and a "right-handed" copy of the generation.

Exact facts over ``Q(i)``:

1. **Two commuting ``su(2)``s.** ``[R_i, R_j] = -2 R_k`` (a second ``su(2)``) and
   ``[W_i, R_j] = 0`` (``so(4) = su(2)_L x su(2)_R``).
2. **Canonical handedness projector.** ``P = (1/2)(I + i R_1)`` satisfies
   ``P^2 = P``, and ``P``, ``I - P`` split the 32 states into two gauge-invariant
   16-dim halves (``[P, colour] = [P, weak] = 0``).
3. **The vector-like wall (honest negative).** Genuine Standard-Model chirality
   would require the two halves to carry *inequivalent* weak representations -- one
   with doublets, the other with singlets. Instead the weak Casimir is ``-3 I``
   *uniformly* on the whole module, so **both** halves are pure weak doublets:
   the construction is exactly **vector-like**. ``C (x) H (x) O`` alone reproduces
   the multiplet content of one generation but **not** its chiral asymmetry.

Non-claim: this gate exhibits the canonical handedness splitting of ``C (x) H (x)
O`` and proves the construction is vector-like -- it does **not** derive the
Standard Model's chiral (``SU(2)_L``-only) structure, which needs an additional
ingredient beyond the division-algebra module (a chirality projector selecting one
ideal *and* collapsing the other's weak doublets to singlets -- put in by hand in
the Furey/Dixon programme, not forced here). No hypercharge split, no dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Tuple

from amplitude_bootstrap.gaussian import Gaussian

from .octonion import cd_mul
from .standard_model import (
    CMatrix,
    _cmul,
    _commutator,
    _cscale,
    _csub,
    _identity,
    _is_zero,
    _kron,
    colour_generators,
    weak_generators,
)
from .weak_isospin import _complexify

_ZERO = Gaussian(0, 0)
_ONE = Gaussian(1, 0)
_I = Gaussian(0, 1)
_MODULE_DIM = 32


def _quaternion_unit(k: int) -> Tuple[Fraction, ...]:
    return tuple(Fraction(1) if t == k else Fraction(0) for t in range(4))


def _quaternion_right_mult(k: int) -> Tuple[Tuple[Fraction, ...], ...]:
    """Right multiplication by the ``k``-th quaternion unit as a 4x4 matrix."""
    cols = [cd_mul(_quaternion_unit(j), _quaternion_unit(k)) for j in range(4)]
    return tuple(tuple(cols[j][i] for j in range(4)) for i in range(4))


def right_generators() -> List[CMatrix]:
    """The three ``su(2)_R`` generators ``R_i (x) I_O`` on ``H (x) O``."""
    io = _identity(8)
    return [_kron(_complexify(_quaternion_right_mult(k)), io) for k in (1, 2, 3)]


def right_su2_relations() -> bool:
    """Exact check ``[R_i, R_j] = -2 R_k`` cyclically (a second ``su(2)``)."""
    r = right_generators()
    neg_two = Gaussian(-2, 0)
    return (
        _commutator(r[0], r[1]) == _cscale(r[2], neg_two)
        and _commutator(r[1], r[2]) == _cscale(r[0], neg_two)
        and _commutator(r[2], r[0]) == _cscale(r[1], neg_two)
    )


def left_right_commute() -> bool:
    """Exact check ``[W_i, R_j] = 0`` -- weak and right ``su(2)`` commute."""
    return all(
        _is_zero(_commutator(w, r))
        for w in weak_generators() for r in right_generators()
    )


def handedness_projector() -> CMatrix:
    """The canonical projector ``P = (1/2)(I + i R_1)`` on ``H (x) O``."""
    ident = _identity(_MODULE_DIM)
    r1 = right_generators()[0]
    shifted = tuple(
        tuple(ident[i][j] + _I * r1[i][j] for j in range(_MODULE_DIM))
        for i in range(_MODULE_DIM)
    )
    return _cscale(shifted, Gaussian(Fraction(1, 2), 0))


def projector_is_idempotent() -> bool:
    """Exact check ``P^2 = P``."""
    p = handedness_projector()
    return _cmul(p, p) == p


def _rank(matrix: CMatrix) -> int:
    rows = [list(row) for row in matrix]
    width = len(rows[0])
    pivot = 0
    for col in range(width):
        sel = None
        for r in range(pivot, len(rows)):
            if rows[r][col] != _ZERO:
                sel = r
                break
        if sel is None:
            continue
        rows[pivot], rows[sel] = rows[sel], rows[pivot]
        piv = rows[pivot][col]
        rows[pivot] = [x / piv for x in rows[pivot]]
        for r in range(len(rows)):
            if r != pivot and rows[r][col] != _ZERO:
                f = rows[r][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[pivot])]
        pivot += 1
    return pivot


def handedness_dimensions() -> Tuple[int, int]:
    """Ranks of ``P`` and ``I - P`` -- the two handedness halves (``16, 16``)."""
    p = handedness_projector()
    q = _csub(_identity(_MODULE_DIM), p)
    return _rank(p), _rank(q)


def projector_commutes_with_gauge() -> bool:
    """Exact check ``[P, colour] = [P, weak] = 0`` -- both halves gauge-invariant."""
    p = handedness_projector()
    return all(
        _is_zero(_commutator(p, g))
        for g in colour_generators() + weak_generators()
    )


def weak_casimir_uniform_doublet() -> bool:
    """Exact check the weak Casimir ``sum_i W_i^2 = -3 I`` on the whole module."""
    total = tuple(tuple(_ZERO for _ in range(_MODULE_DIM)) for _ in range(_MODULE_DIM))
    for w in weak_generators():
        total = tuple(
            tuple(total[i][j] + p for j, p in enumerate(row))
            for i, row in enumerate(_cmul(w, w))
        )
    return _csub(total, _cscale(_identity(_MODULE_DIM), Gaussian(-3, 0))) == tuple(
        tuple(_ZERO for _ in range(_MODULE_DIM)) for _ in range(_MODULE_DIM)
    )


def is_vector_like() -> bool:
    """Both handedness halves are pure weak doublets -- the construction is
    vector-like (no Standard-Model chiral asymmetry).

    The weak Casimir is ``-3 I`` uniformly and ``P`` commutes with the weak
    generators, so each 16-dim half is a sum of spin-1/2 weak doublets: the two
    halves carry equivalent weak representations. Genuine chirality would instead
    give one half doublets and the other singlets.
    """
    left, right = handedness_dimensions()
    return (
        weak_casimir_uniform_doublet()
        and projector_commutes_with_gauge()
        and left == 16
        and right == 16
    )


@dataclass(frozen=True)
class ChiralityCensus:
    """Exact ledger of handedness and the vector-like wall on C (x) H (x) O."""

    right_su2_relations: bool
    left_right_commute: bool
    projector_idempotent: bool
    handedness_dimensions: Tuple[int, int]
    projector_commutes_with_gauge: bool
    weak_casimir_uniform_doublet: bool
    is_vector_like: bool
    produces_chiral_asymmetry: bool


def chirality_census() -> ChiralityCensus:
    """Assemble the exact handedness / vector-like ledger over ``Q(i)``."""
    return ChiralityCensus(
        right_su2_relations=right_su2_relations(),
        left_right_commute=left_right_commute(),
        projector_idempotent=projector_is_idempotent(),
        handedness_dimensions=handedness_dimensions(),
        projector_commutes_with_gauge=projector_commutes_with_gauge(),
        weak_casimir_uniform_doublet=weak_casimir_uniform_doublet(),
        is_vector_like=is_vector_like(),
        produces_chiral_asymmetry=False,
    )
