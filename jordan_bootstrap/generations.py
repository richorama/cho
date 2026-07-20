"""Gate O12 -- three generations via triality: an honest negative result.

Furey (2018) and others have speculated that the Standard Model's *three*
fermion generations might come from the triality of ``Spin(8)`` acting on the
octonions -- three copies of the ``C (x) O`` minimal ideal built in Gate O11,
cyclically related. This gate tests that idea *exactly*, and reports what the
arithmetic actually says rather than what one might hope.

Gate O11 built one fermionic Fock tower by pairing six of the seven imaginary
octonion units into three ladder operators. A different pairing gives a
different number operator, a different vacuum, and hence a different charge
grading. There is an order-three permutation of the paired axes,
``sigma = (e2 e4 e6)`` with ``sigma^3 = id``, that cyclically maps three such
pairings ``p1 -> p3 -> p4 -> p1`` -- a concrete ``Z3`` echo of the O08 triality.

The exact census establishes both halves of the honest picture:

* **Each grading is a full generation.** All three pairings give the identical
  charge spectrum with multiplicities ``(1, 3, 3, 1)`` -- one Standard-Model
  generation each.
* **But they are not independent generations.** Each Fock tower already spans the
  *entire* eight-complex-dimensional ``C (x) O``. The three towers therefore
  coincide as a single module: their combined span is ``8``, not ``24``, and the
  three vacua span only ``2`` dimensions, not ``3``. Triality permutes three
  *charge-gradings of one module*; it does not manufacture three linearly
  independent generations.

So within ``C (x) O`` alone, triality does **not** solve the generation problem.
This matches the state of the literature: the origin of three generations remains
open, and the honest content of this gate is a precise, machine-checked *no*.

Non-claim: this is a negative/boundary result. It does not rule out
generation-from-triality in the larger algebra ``C (x) H (x) O`` or in other
constructions; it only certifies that the naive "three triality-related ideals of
``C (x) O``" are one module in disguise.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

from amplitude_bootstrap.gaussian import Gaussian
from .octonion import E
from .color_su3 import left_mult_matrix
from .fermion_charges import (
    _cadd,
    _cmul,
    _complexify,
    _cscale,
    _dagger,
    _HALF,
    _I,
    _ONE,
    _ZERO,
)

CMatrix = Tuple[Tuple[Gaussian, ...], ...]
CVector = Tuple[Gaussian, ...]

# Three pairings of six imaginary axes, cyclically related by sigma=(2 4 6).
PAIRINGS: Tuple[Tuple[Tuple[int, int], ...], ...] = (
    ((1, 2), (3, 4), (5, 6)),
    ((1, 4), (3, 6), (5, 2)),
    ((1, 6), (5, 4), (3, 2)),
)

# The order-three axis permutation that cycles the three pairings.
TRIALITY_CYCLE: Dict[int, int] = {2: 4, 4: 6, 6: 2}


def _permute_pairs(pairs: Sequence[Tuple[int, int]],
                   sigma: Dict[int, int]) -> List[Tuple[int, int]]:
    return sorted(
        tuple(sorted((sigma.get(a, a), sigma.get(b, b)))) for a, b in pairs
    )


def ladders_from(pairs: Sequence[Tuple[int, int]]) -> List[CMatrix]:
    lmat = [_complexify(left_mult_matrix(E[k])) for k in range(8)]
    return [_cscale(_cadd(lmat[a], _cscale(lmat[b], _I)), _HALF) for a, b in pairs]


def number_from(alphas: Sequence[CMatrix]) -> CMatrix:
    total = tuple(tuple(_ZERO for _ in range(8)) for _ in range(8))
    for a in alphas:
        total = _cadd(total, _cmul(_dagger(a), a))
    return total


def _rank(rows: Sequence[Sequence[Gaussian]]) -> int:
    mat = [list(r) for r in rows]
    if not mat:
        return 0
    cols = len(mat[0])
    pivot_row = 0
    for col in range(cols):
        sel = None
        for r in range(pivot_row, len(mat)):
            if not mat[r][col].is_zero():
                sel = r
                break
        if sel is None:
            continue
        mat[pivot_row], mat[sel] = mat[sel], mat[pivot_row]
        piv = mat[pivot_row][col]
        mat[pivot_row] = [v / piv for v in mat[pivot_row]]
        for r in range(len(mat)):
            if r != pivot_row and not mat[r][col].is_zero():
                f = mat[r][col]
                mat[r] = [mat[r][c] - f * mat[pivot_row][c] for c in range(cols)]
        pivot_row += 1
        if pivot_row == len(mat):
            break
    return pivot_row


def charge_spectrum(number: CMatrix) -> Tuple[int, ...]:
    mults = []
    for value in range(4):
        shifted = tuple(
            tuple(number[i][j] - (Gaussian(value, 0) if i == j else _ZERO)
                  for j in range(8))
            for i in range(8)
        )
        mults.append(8 - _rank(shifted))
    return tuple(mults)


def _apply(op: CMatrix, vec: CVector) -> CVector:
    return tuple(
        sum((op[i][j] * vec[j] for j in range(8)), _ZERO) for i in range(8)
    )


def vacuum(number: CMatrix) -> CVector:
    """The unique (up to scale) charge-zero state annihilated by all ladders."""
    mat = [list(r) for r in number]
    piv: List[int] = []
    pr = 0
    for col in range(8):
        sel = None
        for r in range(pr, 8):
            if not mat[r][col].is_zero():
                sel = r
                break
        if sel is None:
            continue
        mat[pr], mat[sel] = mat[sel], mat[pr]
        p = mat[pr][col]
        mat[pr] = [v / p for v in mat[pr]]
        for r in range(8):
            if r != pr and not mat[r][col].is_zero():
                f = mat[r][col]
                mat[r] = [mat[r][c] - f * mat[pr][c] for c in range(8)]
        piv.append(col)
        pr += 1
    free = [c for c in range(8) if c not in piv]
    vec = [_ZERO] * 8
    vec[free[0]] = _ONE
    for i, pc in enumerate(piv):
        vec[pc] = -mat[i][free[0]]
    return tuple(vec)


def fock_tower(pairs: Sequence[Tuple[int, int]]) -> List[CVector]:
    """The eight Fock states vac, a_i^dagger vac, a_i^dag a_j^dag vac, ..."""
    alphas = ladders_from(pairs)
    number = number_from(alphas)
    vac = vacuum(number)
    dags = [_dagger(a) for a in alphas]
    states = [vac]
    for d in dags:
        states.append(_apply(d, vac))
    for i in range(3):
        for j in range(i + 1, 3):
            states.append(_apply(dags[i], _apply(dags[j], vac)))
    states.append(_apply(dags[0], _apply(dags[1], _apply(dags[2], vac))))
    return states


@dataclass(frozen=True)
class GenerationCensus:
    """Exact certificate of the three-generations-from-triality attempt."""

    triality_cycle_order_three: bool
    triality_cycles_the_pairings: bool
    each_pairing_gives_one_generation: bool
    per_pairing_spectra: Tuple[Tuple[int, ...], ...]
    each_tower_spans_full_module: bool
    combined_span_dimension: int
    three_towers_coincide_as_one_module: bool
    vacua_span_dimension: int
    three_generations_are_independent: bool
    generation_problem_unsolved_here: bool


def generation_census() -> GenerationCensus:
    sigma = TRIALITY_CYCLE
    order_three = all(
        sigma.get(sigma.get(sigma.get(k, k), k), k) == k for k in sigma
    )
    cycles = (
        _permute_pairs(PAIRINGS[0], sigma)
        == sorted(tuple(sorted(x)) for x in PAIRINGS[1])
        and _permute_pairs(PAIRINGS[1], sigma)
        == sorted(tuple(sorted(x)) for x in PAIRINGS[2])
        and _permute_pairs(PAIRINGS[2], sigma)
        == sorted(tuple(sorted(x)) for x in PAIRINGS[0])
    )

    spectra = tuple(
        charge_spectrum(number_from(ladders_from(p))) for p in PAIRINGS
    )
    each_generation = all(s == (1, 3, 3, 1) for s in spectra)

    towers = [fock_tower(p) for p in PAIRINGS]
    each_full = all(_rank(t) == 8 for t in towers)
    combined = _rank([s for t in towers for s in t])
    vacua = [t[0] for t in towers]
    vac_span = _rank(vacua)

    return GenerationCensus(
        triality_cycle_order_three=order_three,
        triality_cycles_the_pairings=cycles,
        each_pairing_gives_one_generation=each_generation,
        per_pairing_spectra=spectra,
        each_tower_spans_full_module=each_full,
        combined_span_dimension=combined,
        three_towers_coincide_as_one_module=(combined == 8),
        vacua_span_dimension=vac_span,
        three_generations_are_independent=(combined == 24),
        generation_problem_unsolved_here=(combined == 8),
    )
