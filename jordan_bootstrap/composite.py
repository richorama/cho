"""Gate O03: the composite-system wall for octonionic quantum mechanics.

Gates O00-O02 built a consistent *single* octonionic system: a norm-preserving
representation group, a frame-consistent Born rule, and genuine pure states on
the exceptional Jordan algebra ``h_3(O)``. This gate asks whether two such systems
can be composed -- and finds the honest wall.

Composing observables (and forming a tensor product of state spaces) requires an
*associative* envelope: in ordinary quantum mechanics the observable algebra
``h_n(C)`` is *special*, i.e. it sits inside the associative matrix algebra
``M_n(C)`` via ``A o B = (AB + BA)/2``, and it is exactly this associative product
that lets ``M_m(C) tensor M_n(C) = M_{mn}(C)`` define the joint system. The
mechanism fails for octonions: octonionic matrix multiplication is
*non-associative*, so there is no associative envelope and hence no consistent
composite.

The failure is sharp and computable. By Artin's theorem any *two* octonions
generate an associative subalgebra, so a size-2 realization ``h_2(O)`` still
associates; the obstruction needs *three* independent imaginary directions, which
is why it appears precisely at ``h_3(O)`` -- the same size at which the octonionic
projective plane exists at all. This gate exhibits an exact nonzero associator of
octonionic matrix multiplication and verifies that every complex and quaternionic
sub-realization associates exactly.

Non-claim. This is the finite *mechanism* of the obstruction, consistent with
Albert's theorem that ``h_3(O)`` is exceptional (not special) and with Zelmanov's
classification; it is not a re-derivation of those theorems. Operationally it
sharpens the amplitude campaign's boundary (observer-consistency buys the
probability calculus, not interacting dynamics): octonionic quantum mechanics is
a consistent *single-system* probability calculus with *no* composite extension.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple

from .octonion import E, Octonion, octonion
from .jordan import JMat, _add, _matmul, _scale, equal, _zeros

_ZERO_O = octonion(0, 0, 0, 0, 0, 0, 0, 0)


def elementary(i: int, j: int, value: Octonion) -> JMat:
    """The 3x3 octonionic matrix with ``value`` at ``(i, j)`` and zeros elsewhere."""
    return tuple(
        tuple(value if (r, c) == (i, j) else _ZERO_O for c in range(3))
        for r in range(3)
    )


def associator(a: JMat, b: JMat, c: JMat) -> JMat:
    """The matrix-multiplication associator ``(AB)C - A(BC)`` of octonionic matrices."""
    return _add(_matmul(_matmul(a, b), c), _scale(_matmul(a, _matmul(b, c)), Fraction(-1)))


def associates(a: JMat, b: JMat, c: JMat) -> bool:
    """True iff ``(AB)C == A(BC)`` exactly."""
    return equal(associator(a, b, c), _zeros())


def _triple(x: Octonion, y: Octonion, z: Octonion) -> Tuple[JMat, JMat, JMat]:
    """Route the octonion associator ``[x, y, z]`` into entry ``(0, 0)`` of the product.

    ``A = x at (0,1)``, ``B = y at (1,2)``, ``C = z at (2,0)``, so ``(AB)C`` places
    ``(x y) z`` at ``(0, 0)`` and ``A(BC)`` places ``x (y z)`` there; their
    difference is exactly the octonion associator.
    """
    return elementary(0, 1, x), elementary(1, 2, y), elementary(2, 0, z)


# Three genuinely non-associative octonion direction-triples (not Fano lines).
_OCTONIONIC = ((1, 2, 4), (3, 4, 6), (2, 3, 5))
# Complex directions live in span{1, e_1}; quaternionic in a Fano-line subalgebra.
_COMPLEX = (
    (octonion(1, 2, 0, 0, 0, 0, 0, 0), octonion(3, 1, 0, 0, 0, 0, 0, 0), octonion(0, 5, 0, 0, 0, 0, 0, 0)),
    (octonion(2, 1, 0, 0, 0, 0, 0, 0), octonion(1, 4, 0, 0, 0, 0, 0, 0), octonion(1, 1, 0, 0, 0, 0, 0, 0)),
)
_QUATERNIONIC = ((1, 2, 3), (1, 4, 5), (2, 4, 6))  # associative Fano lines in this convention


@dataclass(frozen=True)
class CompositeWallCensus:
    octonionic_checks: int
    octonionic_non_associative: int      # every octonionic triple must fail to associate
    complex_checks: int
    complex_non_associative: int         # complex realizations associate: must be 0
    quaternionic_checks: int
    quaternionic_non_associative: int    # quaternionic realizations associate: must be 0


def composite_wall_census() -> CompositeWallCensus:
    """Exact tallies for Gate O03, owned and asserted by the test contract."""
    oct_fail = 0
    for i, j, k in _OCTONIONIC:
        if not associates(*_triple(E[i], E[j], E[k])):
            oct_fail += 1

    cplx_fail = 0
    for x, y, z in _COMPLEX:
        if not associates(*_triple(x, y, z)):
            cplx_fail += 1

    quat_fail = 0
    for i, j, k in _QUATERNIONIC:
        if not associates(*_triple(E[i], E[j], E[k])):
            quat_fail += 1

    return CompositeWallCensus(
        octonionic_checks=len(_OCTONIONIC),
        octonionic_non_associative=oct_fail,
        complex_checks=len(_COMPLEX),
        complex_non_associative=cplx_fail,
        quaternionic_checks=len(_QUATERNIONIC),
        quaternionic_non_associative=quat_fail,
    )


def canonical_associator_witness() -> Octonion:
    """The exact ``(0, 0)`` associator entry for the ``(e_1, e_2, e_4)`` route."""
    a, b, c = _triple(E[1], E[2], E[4])
    return associator(a, b, c)[0][0]
