"""Gate O20 -- assembling the Standard Model gauge algebra on C (x) H (x) O.

The campaign has produced the three Standard-Model gauge factors separately:
colour ``su(3)`` from ``C (x) O`` (Gates O10/O11), weak isospin ``su(2)`` from the
quaternions ``H`` (Gate O13), and an abelian ``u(1)`` (Gates O11/O19). This gate
performs the Furey assembly: it realises all three at once as commuting operator
algebras acting on the single one-generation module

    C (x) H (x) O   (dimension 2 * 4 * 8 = 64 over R, i.e. H (x) O = 32 over Q(i)),

and verifies exactly, over ``Q(i)``, that together they form ``su(3) (+) su(2) (+)
u(1)`` -- dimension ``8 + 3 + 1 = 12``, the exact dimension of the Standard-Model
gauge algebra.

The construction uses Kronecker products on ``H (x) O``:

* **Colour** ``su(3)`` acts on the ``O`` factor: the eight number-preserving
  bilinears of Gate O11 become ``I_H (x) C_a`` (``a = 1..8``).
* **Weak** ``su(2)`` acts on the ``H`` factor: the three imaginary quaternion
  left-multiplications of Gate O13 become ``W_i (x) I_O`` (``i = 1..3``).
* **Hypercharge-like ``u(1)``** is the Gate O11 number operator on the ``O`` factor,
  ``I_H (x) N``.

Exact facts checked here:

1. **Colour closes** into ``su(3)`` (rank ``8``, bracket-closed) on the 32-dim
   module.
2. **Weak closes** into ``su(2)`` (``[W_i, W_j] = 2 W_k`` cyclically, rank ``3``).
3. **Colour and weak commute.** Every ``[I_H (x) C_a, W_i (x) I_O] = 0`` -- because
   colour lives on the ``O`` factor and weak on the ``H`` factor of the Cayley-Dickson
   tower. This is the algebraic reason the Standard-Model gauge group is a direct
   product.
4. **The ``u(1)`` is central and independent:** ``I_H (x) N`` commutes with colour
   and weak and is not in their span.
5. **The total algebra is 12-dimensional:** ``su(3) (+) su(2) (+) u(1)`` with
   ``8 + 3 + 1 = 12`` independent generators -- the Standard-Model gauge algebra,
   realised on one octonion-quaternion generation.

Non-claim: this is the standard Furey *embedding* of the Standard-Model gauge
algebra into the left-action algebra of ``C (x) H (x) O``. The colour-weak
commutation is *structural* -- the two factors act on different Cayley-Dickson
slots -- so the gate exhibits a consistent realisation of the ``su(3) (+) su(2) (+)
u(1)`` content, not a derivation that nature is forced to pick this product, the
chirality/representation assignment, the Higgs sector, or any dynamics. The
``u(1)`` here is the O11 colour-phase / number ``u(1)``, not the fully mixed
electroweak hypercharge (which entangles with the weak ``su(2)`` breaking absent
from this gate).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Sequence, Tuple

from amplitude_bootstrap.gaussian import Gaussian

from .fermion_charges import number_operator, su3_bilinears
from .weak_isospin import _complexify, quaternion_left_mult

CMatrix = Tuple[Tuple[Gaussian, ...], ...]

_ZERO = Gaussian(0, 0)
_ONE = Gaussian(1, 0)
_TWO = Gaussian(2, 0)


def _identity(n: int) -> CMatrix:
    return tuple(
        tuple(_ONE if i == j else _ZERO for j in range(n)) for i in range(n)
    )


def _cmul(a: CMatrix, b: CMatrix) -> CMatrix:
    inner = len(b)
    return tuple(
        tuple(sum((a[i][t] * b[t][j] for t in range(inner)), _ZERO)
              for j in range(len(b[0])))
        for i in range(len(a))
    )


def _csub(a: CMatrix, b: CMatrix) -> CMatrix:
    return tuple(
        tuple(a[i][j] - b[i][j] for j in range(len(a[0]))) for i in range(len(a))
    )


def _commutator(a: CMatrix, b: CMatrix) -> CMatrix:
    return _csub(_cmul(a, b), _cmul(b, a))


def _is_zero(a: CMatrix) -> bool:
    return all(x == _ZERO for row in a for x in row)


def _cscale(a: CMatrix, s: Gaussian) -> CMatrix:
    return tuple(tuple(x * s for x in row) for row in a)


def _kron(a: CMatrix, b: CMatrix) -> CMatrix:
    ra, ca = len(a), len(a[0])
    rb, cb = len(b), len(b[0])
    return tuple(
        tuple(a[i // rb][j // cb] * b[i % rb][j % cb] for j in range(ca * cb))
        for i in range(ra * rb)
    )


def _rank(mats: Sequence[CMatrix]) -> int:
    """Exact rank over ``Q(i)`` of the flattened generators (field elimination)."""
    rows = [[x for row in m for x in row] for m in mats]
    width = len(rows[0]) if rows else 0
    pivot_row = 0
    for col in range(width):
        sel = None
        for r in range(pivot_row, len(rows)):
            if rows[r][col] != _ZERO:
                sel = r
                break
        if sel is None:
            continue
        rows[pivot_row], rows[sel] = rows[sel], rows[pivot_row]
        piv = rows[pivot_row][col]
        rows[pivot_row] = [x / piv for x in rows[pivot_row]]
        for r in range(len(rows)):
            if r != pivot_row and rows[r][col] != _ZERO:
                f = rows[r][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[pivot_row])]
        pivot_row += 1
    return pivot_row


_DIM_H = 4
_DIM_O = 8


def colour_generators() -> List[CMatrix]:
    """The eight colour ``su(3)`` generators ``I_H (x) C_a`` on ``H (x) O``."""
    ih = _identity(_DIM_H)
    return [_kron(ih, c) for c in su3_bilinears()]


def weak_generators() -> List[CMatrix]:
    """The three weak ``su(2)`` generators ``W_i (x) I_O`` on ``H (x) O``."""
    io = _identity(_DIM_O)
    return [_kron(_complexify(quaternion_left_mult(k)), io) for k in (1, 2, 3)]


def hypercharge_generator() -> CMatrix:
    """The abelian ``u(1)`` generator ``I_H (x) N`` (O11 number operator on ``O``)."""
    return _kron(_identity(_DIM_H), number_operator())


def colour_is_closed_su3() -> bool:
    """Exact check that the colour generators close (rank 8, bracket-closed)."""
    gens = colour_generators()
    if _rank(gens) != 8:
        return False
    brackets = [
        _commutator(gens[i], gens[j])
        for i in range(len(gens)) for j in range(i + 1, len(gens))
    ]
    return _rank(gens + brackets) == 8


def weak_su2_relations() -> bool:
    """Exact check ``[W_i, W_j] = 2 W_k`` cyclically for the weak generators."""
    w = weak_generators()
    return (
        _commutator(w[0], w[1]) == _cscale(w[2], _TWO)
        and _commutator(w[1], w[2]) == _cscale(w[0], _TWO)
        and _commutator(w[2], w[0]) == _cscale(w[1], _TWO)
    )


def colour_weak_commute() -> bool:
    """Exact check that every colour generator commutes with every weak generator."""
    return all(
        _is_zero(_commutator(gc, gw))
        for gc in colour_generators() for gw in weak_generators()
    )


def hypercharge_is_central() -> bool:
    """Exact check that ``u(1)`` commutes with all colour and weak generators."""
    y = hypercharge_generator()
    return all(
        _is_zero(_commutator(y, g))
        for g in colour_generators() + weak_generators()
    )


def gauge_algebra_dimension() -> int:
    """Total independent dimension of ``su(3) (+) su(2) (+) u(1)`` (``= 12``)."""
    return _rank(colour_generators() + weak_generators() + [hypercharge_generator()])


@dataclass(frozen=True)
class StandardModelGaugeCensus:
    """Exact ledger of the SM gauge algebra assembled on ``C (x) H (x) O``."""

    module_dimension: int
    colour_dimension: int
    colour_closed: bool
    weak_dimension: int
    weak_su2_relations: bool
    colour_weak_commute: bool
    hypercharge_central: bool
    total_dimension: int
    is_standard_model_algebra: bool


def standard_model_gauge_census() -> StandardModelGaugeCensus:
    """Assemble the exact ``su(3) (+) su(2) (+) u(1)`` ledger over ``Q(i)``."""
    colour = colour_generators()
    weak = weak_generators()
    total = gauge_algebra_dimension()
    return StandardModelGaugeCensus(
        module_dimension=len(colour[0]),
        colour_dimension=_rank(colour),
        colour_closed=colour_is_closed_su3(),
        weak_dimension=_rank(weak),
        weak_su2_relations=weak_su2_relations(),
        colour_weak_commute=colour_weak_commute(),
        hypercharge_central=hypercharge_is_central(),
        total_dimension=total,
        is_standard_model_algebra=(total == 12),
    )
