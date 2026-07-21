"""Gate O18 -- G2 to SU(3): colour is the holonomy of the Calabi-Yau slice.

The campaign has two halves that have so far stood apart. The *gauge* half
(O10-O14) pulled colour ``su(3)`` out of the octonions as the stabiliser of one
imaginary unit. The *geometry* half (O17) showed the associator is the ``G2``
associative calibration ``phi``. This gate joins them with a single exact
construction: **choosing a preferred imaginary unit reduces the ``G2`` structure
to an ``SU(3)`` structure, and the ``SU(3)`` that appears is exactly the O10
colour algebra.** It is the pointwise algebraic shadow of the standard fact that a
seven-dimensional ``G2``-holonomy manifold contains a six-dimensional Calabi-Yau
(``SU(3)``-holonomy) slice, whose complex structure, Kahler form and holomorphic
volume form are all read off from ``phi``.

Fix the preferred unit ``u = e_7``. It splits the imaginary octonions
``Im(O) = R^7 = <u> (+) u^perp`` with ``u^perp = span(e_1..e_6)`` six-dimensional.
Everything below is exact over ``Q``.

1. **A complex structure.** ``J = L_u`` (left multiplication by ``u``) restricted to
   ``u^perp`` satisfies ``J^2 = -I`` and maps ``u^perp`` to itself: it makes
   ``u^perp`` into ``C^3``.

2. **A Kahler form.** ``omega(x, y) = phi(u, x, y)`` is antisymmetric,
   *nondegenerate* (rank ``6``), ``J``-invariant (``omega(Jx, Jy) = omega(x, y)``)
   and *tames* ``J`` (``omega(x, Jx) = |x|^2 > 0``). It is the Kahler form of the
   ``C^3`` slice.

3. **A holomorphic volume form.** The associative form restricted to ``u^perp``,
   ``Re Omega = phi|_{u^perp}``, is of type ``(3,0)+(0,3)``: ``phi(Jx, Jy, z) =
   -phi(x, y, z)`` for all ``x, y, z`` in ``u^perp``. Together ``(omega, Omega)``
   are an ``SU(3)`` structure.

4. **The ``SU(3)`` is colour.** The O10 stabiliser ``su(3) = {D in g2 : D u = 0}``
   (dimension ``8``) **preserves ``omega``**, **commutes with ``J``**, and
   **preserves ``Re Omega``**. So the colour algebra of Gates O10-O14 is exactly
   the ``su(3)`` holonomy algebra of the Calabi-Yau slice defined by ``phi``. The
   two halves of the campaign are one object seen two ways: colour ``SU(3)`` is the
   structure group of the ``G2 -> SU(3)`` reduction.

Non-claim: this is the exact *pointwise linear-algebraic* reduction of the ``G2``
structure ``phi`` to an ``SU(3)`` structure ``(omega, Omega)`` on the tangent
space, and the identification of that ``SU(3)`` with the O10 colour algebra. It
does **not** build a Calabi-Yau metric, integrate the complex structure to a
genuine complex manifold, solve the Ricci-flat equations, or claim the colour
gauge field is a gravitational holonomy. It is the algebra of the reduction, not a
compactification.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Tuple

from .color_su3 import (
    Matrix,
    _apply,
    _matmul,
    _rref,
    derivation_algebra,
    left_mult_matrix,
    stabiliser_subalgebra,
)
from .calibration import associative_form, inner_product
from .octonion import E, Octonion

PREFERRED_UNIT: Octonion = E[7]
PERP_INDICES: Tuple[int, ...] = tuple(range(1, 7))  # e_1 .. e_6 span u^perp


def _perp_basis() -> List[Octonion]:
    return [E[k] for k in PERP_INDICES]


def complex_structure() -> Matrix:
    """The candidate complex structure ``J = L_u`` (left multiplication by ``u``)."""
    return left_mult_matrix(PREFERRED_UNIT)


def complex_structure_squares_to_minus_one() -> bool:
    """Exact check ``J^2 = -I`` on ``u^perp`` (so ``u^perp`` is ``C^3``)."""
    j = complex_structure()
    for x in _perp_basis():
        if _apply(j, _apply(j, x)) != -x:
            return False
    return True


def complex_structure_preserves_perp() -> bool:
    """Exact check that ``J`` maps ``u^perp`` into itself (real and ``u`` parts zero)."""
    j = complex_structure()
    for x in _perp_basis():
        image = _apply(j, x)
        if image.coords[0] != 0 or image.coords[7] != 0:
            return False
    return True


def kahler_form(x: Octonion, y: Octonion) -> Fraction:
    """The Kahler 2-form ``omega(x, y) = phi(u, x, y)`` of the ``C^3`` slice."""
    return associative_form(PREFERRED_UNIT, x, y)


def kahler_is_antisymmetric() -> bool:
    perp = _perp_basis()
    return all(kahler_form(x, y) == -kahler_form(y, x) for x in perp for y in perp)


def kahler_rank() -> int:
    """Rank of ``omega`` on ``u^perp`` (``= 6``: nondegenerate)."""
    perp = _perp_basis()
    rows = [[kahler_form(x, y) for y in perp] for x in perp]
    _, pivots = _rref([list(map(Fraction, r)) for r in rows])
    return len(pivots)


def kahler_is_j_invariant() -> bool:
    j = complex_structure()
    perp = _perp_basis()
    return all(
        kahler_form(_apply(j, x), _apply(j, y)) == kahler_form(x, y)
        for x in perp for y in perp
    )


def kahler_tames_complex_structure() -> bool:
    """Exact check ``omega(x, Jx) = |x|^2`` (positive taming) on ``u^perp``."""
    j = complex_structure()
    return all(
        kahler_form(x, _apply(j, x)) == inner_product(x, x) for x in _perp_basis()
    )


def holomorphic_form_is_type_three_zero() -> bool:
    """Exact check ``phi(Jx, Jy, z) = -phi(x, y, z)`` on ``u^perp`` (``Re Omega``)."""
    j = complex_structure()
    perp = _perp_basis()
    return all(
        associative_form(_apply(j, x), _apply(j, y), z) == -associative_form(x, y, z)
        for x in perp for y in perp for z in perp
    )


def colour_su3() -> List[Matrix]:
    """The O10 colour algebra ``su(3) = {D in g2 : D u = 0}`` (dimension 8)."""
    return stabiliser_subalgebra(derivation_algebra(), PREFERRED_UNIT)


def su3_preserves_kahler() -> bool:
    perp = _perp_basis()
    for d in colour_su3():
        for x in perp:
            for y in perp:
                if kahler_form(_apply(d, x), y) + kahler_form(x, _apply(d, y)) != 0:
                    return False
    return True


def su3_commutes_with_complex_structure() -> bool:
    j = complex_structure()
    return all(_matmul(d, j) == _matmul(j, d) for d in colour_su3())


def su3_preserves_holomorphic_form() -> bool:
    perp = _perp_basis()
    for d in colour_su3():
        for x in perp:
            for y in perp:
                for z in perp:
                    total = (
                        associative_form(_apply(d, x), y, z)
                        + associative_form(x, _apply(d, y), z)
                        + associative_form(x, y, _apply(d, z))
                    )
                    if total != 0:
                        return False
    return True


@dataclass(frozen=True)
class SU3StructureCensus:
    """Exact ledger of the ``G2 -> SU(3)`` reduction identifying colour with holonomy."""

    complex_structure_squares: bool
    complex_structure_preserves_perp: bool
    kahler_antisymmetric: bool
    kahler_rank: int
    kahler_j_invariant: bool
    kahler_tames_j: bool
    holomorphic_form_type_three_zero: bool
    colour_su3_dimension: int
    su3_preserves_kahler: bool
    su3_commutes_with_j: bool
    su3_preserves_holomorphic_form: bool


def su3_structure_census() -> SU3StructureCensus:
    """Assemble the exact ``G2 -> SU(3)`` reduction ledger over ``Q``."""
    return SU3StructureCensus(
        complex_structure_squares=complex_structure_squares_to_minus_one(),
        complex_structure_preserves_perp=complex_structure_preserves_perp(),
        kahler_antisymmetric=kahler_is_antisymmetric(),
        kahler_rank=kahler_rank(),
        kahler_j_invariant=kahler_is_j_invariant(),
        kahler_tames_j=kahler_tames_complex_structure(),
        holomorphic_form_type_three_zero=holomorphic_form_is_type_three_zero(),
        colour_su3_dimension=len(colour_su3()),
        su3_preserves_kahler=su3_preserves_kahler(),
        su3_commutes_with_j=su3_commutes_with_complex_structure(),
        su3_preserves_holomorphic_form=su3_preserves_holomorphic_form(),
    )
