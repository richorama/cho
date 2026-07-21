"""Gate O26 -- the atmospheric mixing angle as a Fano-plane invariant.

This is the campaign's first genuinely *falsifiable* number. Every prior gate
reproduced known structure; this one emits an exact mixing rational and pins its
canonicity, exactly over ``Q``, porting the master-branch N5 result
(``compute/theta23_mixing_operator.py`` / ``theta23_fano_invariance.py``, behind
Zenodo 21107402) into the exact-arithmetic campaign.

The octonion multiplication triples ``e_i e_j = +- e_k`` are exactly the seven lines
of the **Fano plane** ``PG(2,2) = S(2,3,7)`` (Gate O17's associative 3-form ``phi``
is nonzero precisely on these lines). Pick a "vacuum" imaginary unit ``e_v``. Each
point of ``PG(2,2)`` lies on ``n + 1 = 3`` lines (order ``n = 2``) and therefore
*avoids* ``7 - 3 = 4``. The campaign's sharpest bet is the atmospheric octant

    sin^2(theta23) = (lines avoiding the vacuum) / (all lines) = 4/7,

the *only* vacuum-scale-independent exact mixing rational the framework emits
(``theta23 = arcsin(sqrt(4/7)) ~ 49.1 deg``, the upper octant).

The value is hardened here from "read one row of the multiplication table" to a
**basis-free spectral invariant**. On the 7-dim line-space the *vacuum-avoidance
operator* is the diagonal projector

    P_avoid(v) = diag[ 1 if v not in line L else 0 ],

a rank-4 orthogonal projector (``P^2 = P = P^T``, spectrum ``{1^4, 0^3}``) whose
normalized trace ``Tr P / 7`` is the spectral mean. Exact facts over ``Q``:

1. **Seven Fano lines.** The octonion triples give exactly the 7 lines of
   ``PG(2,2)`` -- a theorem about the multiplication, not a drawing convention.
2. **Vacuum-independence.** The split is ``(3 through, 4 avoiding)`` for *every* one
   of the 7 vacuum choices, so ``sin^2(theta23) = 4/7`` regardless of which
   imaginary unit is singled out.
3. **The value is a normalized trace.** ``Tr P_avoid / 7 = 4/7 = 1/2 + 1/14`` --
   maximal mixing plus the single-line Fano asymmetry -- a basis-free spectral
   quantity, not a chosen matrix entry.
4. **Convention-independence.** ``Aut(Fano) = PGL(3,2) = PSL(2,7)`` has order ``168``
   and acts *transitively* on the 7 points; the induced line-permutations satisfy
   ``Pi_g P_avoid(v) Pi_g^T = P_avoid(g(v))`` for all ``168`` collineations, so
   ``4/7`` is a single-orbit **class invariant**: no octonion relabelling changes it.
5. **Octant complementarity.** The mirror ``P_through`` is rank 3 -> ``3/7`` (lower
   octant), with ``4/7 + 3/7 = 1`` exactly.

Non-claim: what is forced, exactly and basis-free, is the *value* ``4/7`` **given**
two adopted inputs: (i) the physical map "atmospheric mixing probability = avoiding
lines / total lines" (the open "N5 bridge" -- not derived from any dynamics here),
and (ii) the octant choice of the *avoiding* (broken) sector over the *through*
(colour-``su(3)`` stabiliser) sector. A stable experimental lower-octant resolution
near ``3/7`` would falsify the octant choice. This gate derives neither the map nor
the octant; it proves that once they are adopted, the number is canonical and
convention-free. The current global-fit value ``sin^2(theta23) ~ 0.55-0.57`` sits
beside ``4/7 ~ 0.571`` -- the framework's one live, falsifiable contact with data.

See also (master branch): ``compute/theta23_fano_invariance.py`` and
``compute/theta23_mixing_operator.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, permutations
from typing import List, Tuple

from .calibration import associative_form
from .octonion import E

_Matrix = Tuple[Tuple[int, ...], ...]


def fano_lines() -> Tuple[Tuple[int, int, int], ...]:
    """The seven Fano lines: octonion triples with ``phi(e_i, e_j, e_k) != 0``."""
    lines = {
        frozenset((i, j, k))
        for i, j, k in combinations(range(1, 8), 3)
        if associative_form(E[i], E[j], E[k]) != 0
    }
    return tuple(sorted(tuple(sorted(line)) for line in lines))


_LINES = fano_lines()
_LINE_SET = tuple(frozenset(line) for line in _LINES)
_TOTAL = 7


def vacuum_split(vacuum: int) -> Tuple[int, int]:
    """Return ``(through, avoiding)`` line counts for a vacuum point ``1 <= v <= 7``."""
    through = sum(1 for line in _LINES if vacuum in line)
    return (through, _TOTAL - through)


def avoidance_projector(vacuum: int) -> _Matrix:
    """The rank-4 diagonal projector onto lines avoiding the vacuum point."""
    return tuple(
        tuple(
            1 if (i == j and vacuum not in _LINES[i]) else 0
            for j in range(_TOTAL)
        )
        for i in range(_TOTAL)
    )


def through_projector(vacuum: int) -> _Matrix:
    """The rank-3 complementary projector onto lines through the vacuum point."""
    return tuple(
        tuple(
            1 if (i == j and vacuum in _LINES[i]) else 0
            for j in range(_TOTAL)
        )
        for i in range(_TOTAL)
    )


def _matmul(a: _Matrix, b: _Matrix) -> _Matrix:
    n = len(a)
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n))
        for i in range(n)
    )


def _transpose(a: _Matrix) -> _Matrix:
    return tuple(zip(*a))


def _trace(a: _Matrix) -> int:
    return sum(a[i][i] for i in range(len(a)))


def normalized_trace(projector: _Matrix) -> Fraction:
    """The spectral mean ``Tr P / dim`` as an exact rational."""
    return Fraction(_trace(projector), _TOTAL)


def sin2_theta23() -> Fraction:
    """The atmospheric mixing prediction ``sin^2(theta23) = 4/7`` (upper octant)."""
    return normalized_trace(avoidance_projector(1))


def octant_mirror() -> Fraction:
    """The lower-octant mirror ``3/7 = Tr P_through / dim``."""
    return normalized_trace(through_projector(1))


def octants_are_complementary() -> bool:
    """Exact check ``4/7 + 3/7 = 1``."""
    return sin2_theta23() + octant_mirror() == 1


def is_orthogonal_rank_projector(projector: _Matrix, rank: int) -> bool:
    """Exact check ``P^2 = P = P^T`` with ``Tr P = rank``."""
    return (
        _matmul(projector, projector) == projector
        and _transpose(projector) == projector
        and _trace(projector) == rank
    )


def vacuum_independent() -> bool:
    """Exact check that every one of the 7 vacua gives the ``(3, 4)`` split -> 4/7."""
    return all(vacuum_split(v) == (3, 4) for v in range(1, _TOTAL + 1))


def _preserves_lines(perm: Tuple[int, ...]) -> bool:
    return all(
        frozenset(perm[p - 1] for p in line) in _LINE_SET for line in _LINES
    )


def collineation_group() -> List[Tuple[int, ...]]:
    """All point permutations of ``{1..7}`` preserving the Fano line-set (``|G| = 168``)."""
    return [p for p in permutations(range(1, 8)) if _preserves_lines(p)]


def collineation_group_order() -> int:
    """The order of ``Aut(Fano) = PSL(2,7)`` (``= 168``)."""
    return len(collineation_group())


def group_is_point_transitive() -> bool:
    """Exact check that the collineation group acts transitively on the 7 points."""
    group = collineation_group()
    return len({p[0] for p in group}) == _TOTAL


def _induced_line_permutation(perm: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(
        _LINE_SET.index(frozenset(perm[p - 1] for p in _LINES[i]))
        for i in range(_TOTAL)
    )


def _line_permutation_matrix(sigma: Tuple[int, ...]) -> _Matrix:
    return tuple(
        tuple(1 if sigma[j] == i else 0 for j in range(_TOTAL))
        for i in range(_TOTAL)
    )


def value_is_class_invariant() -> bool:
    """Exact check ``Pi_g P_avoid(v) Pi_g^T = P_avoid(g(v))`` for all 168 x 7 pairs.

    Together with point-transitivity this makes ``4/7`` a single-orbit invariant,
    independent of the octonion labelling convention.
    """
    for perm in collineation_group():
        pi = _line_permutation_matrix(_induced_line_permutation(perm))
        pit = _transpose(pi)
        for v in range(1, _TOTAL + 1):
            lhs = _matmul(_matmul(pi, avoidance_projector(v)), pit)
            if lhs != avoidance_projector(perm[v - 1]):
                return False
    return True


@dataclass(frozen=True)
class AtmosphericMixingCensus:
    """Exact ledger of the ``sin^2(theta23) = 4/7`` Fano invariant over ``Q``."""

    line_count: int
    vacuum_independent: bool
    sin2_theta23: Fraction
    octant_mirror: Fraction
    octants_complementary: bool
    projector_rank4_orthogonal: bool
    group_order: int
    point_transitive: bool
    value_is_class_invariant: bool


def atmospheric_mixing_census() -> AtmosphericMixingCensus:
    """Assemble the exact O26 ledger."""
    return AtmosphericMixingCensus(
        line_count=len(_LINES),
        vacuum_independent=vacuum_independent(),
        sin2_theta23=sin2_theta23(),
        octant_mirror=octant_mirror(),
        octants_complementary=octants_are_complementary(),
        projector_rank4_orthogonal=is_orthogonal_rank_projector(
            avoidance_projector(1), 4
        ),
        group_order=collineation_group_order(),
        point_transitive=group_is_point_transitive(),
        value_is_class_invariant=value_is_class_invariant(),
    )
