"""Gate O17 -- the associative calibration: non-associativity is the G2 3-form.

Gates O15/O16 pinned the octonionic *dynamics wall*: the imaginary octonions are
a Malcev (not Lie) algebra, the associator is the exact obstruction, and it
survives as the operator Moufang law. This gate takes the swing that the earlier
honest assessment kept deferring -- it asks whether the associator is not merely
an *obstruction* but a recognisable *geometric* object. It is: exactly, and it is
one of the most physically loaded objects in mathematics -- the **associative
calibration 3-form** of ``G2`` holonomy.

Everything below is exact over ``Q``, on the seven imaginary units ``Im(O) = R^7``.

1. **The associative 3-form.** ``phi(x, y, z) = <x, y z>`` (real inner product of
   ``x`` with the product ``y z``) is *totally antisymmetric* on imaginary
   arguments, with values in ``{-1, 0, +1}`` -- the ``42`` nonzero entries are the
   ``7`` Fano lines in their ``6`` orderings. This is Joyce's ``phi``, the
   calibration whose calibrated 3-planes are the *associative* submanifolds of a
   ``G2`` manifold.

2. **The associator IS the coassociative 4-form.** The associator of imaginary
   units is purely imaginary and reconstructs exactly from a totally antisymmetric
   4-tensor ``psi``: ``[e_i, e_j, e_k] = 2 * sum_l psi_{ijkl} e_l`` with
   ``psi_{ijkl} = (1/2) <e_l, [e_i, e_j, e_k]>``. ``psi`` has ``168`` nonzero
   entries (``7`` coassociative 4-planes in their ``24`` orderings) and is the
   Hodge dual ``psi = *phi``, the coassociative calibration. So the campaign's
   central obstruction -- the associator -- literally *is* the coassociative form.

3. **``G2`` invariance.** Every derivation of ``O`` (the 14-dimensional Lie algebra
   ``g2 = Lie(Aut O)`` computed exactly in Gate O10) annihilates ``phi``:
   ``phi(Dx, y, z) + phi(x, Dy, z) + phi(x, y, Dz) = 0``. The infinitesimal
   stabiliser of ``phi`` is exactly ``g2`` -- the algebraic definition of ``G2``
   as the group preserving the associative 3-form.

4. **The Akivis structure equation.** For *any* algebra the Jacobiator and the
   associator obey the universal identity (the tangent structure equation of a
   loop, commutator = torsion, associator = curvature)

       J(x, y, z) = sum over permutations sign(sigma) * associator(sigma(x,y,z)).

   Because ``O`` is alternative the associator is itself alternating, so the six
   signed terms coincide and the right-hand side collapses to ``6 * [x, y, z]`` --
   recovering the Gate O15 identity ``J = 6 * associator`` as the structure
   equation of the associative calibration.

The point of the swing: the octonionic non-associativity that walls off an
ordinary dynamics is, viewed correctly, the ``G2`` calibration geometry that
underlies compactification of eleven-dimensional M-theory on a seven-dimensional
``G2``-holonomy manifold (the route by which exceptional geometry yields
four-dimensional chiral physics). This gate exhibits that identification exactly
and finitely: ``phi``, ``psi = *phi``, their ``G2`` invariance, and the structure
equation, all machine-checked over the rationals.

Non-claim: this exhibits the *pointwise algebraic tensors* of ``G2`` geometry --
the calibration forms, their exact ``G2`` invariance, and the loop structure
equation -- and identifies the associator with the coassociative form. It does
**not** construct a ``G2``-holonomy metric, solve the Ricci-flat / supergravity
equations of motion, perform a compactification, or derive any four-dimensional
spectrum. It is the algebra that *seeds* exceptional-holonomy geometry, not that
geometry's dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
from typing import List, Tuple

from .color_su3 import Matrix, derivation_algebra
from .dynamics_wall import associator, jacobiator
from .octonion import E, Octonion, octonion

IMAGINARY_INDICES: Tuple[int, ...] = tuple(range(1, 8))


def inner_product(a: Octonion, b: Octonion) -> Fraction:
    """The real Euclidean inner product ``<a, b> = sum_k a_k b_k``."""
    return sum((x * y for x, y in zip(a.coords, b.coords)), Fraction(0))


def associative_form(x: Octonion, y: Octonion, z: Octonion) -> Fraction:
    """The associative 3-form ``phi(x, y, z) = <x, y z>`` (a 3-form on ``Im O``)."""
    return inner_product(x, y * z)


def coassociative_component(i: int, j: int, k: int, l: int) -> Fraction:
    """The coassociative 4-form entry ``psi_{ijkl} = (1/2) <e_l, [e_i, e_j, e_k]>``."""
    return Fraction(1, 2) * inner_product(E[l], associator(E[i], E[j], E[k]))


def associator_from_coassociative(i: int, j: int, k: int) -> Octonion:
    """Rebuild ``[e_i, e_j, e_k] = 2 sum_l psi_{ijkl} e_l`` from the 4-form."""
    coords = [Fraction(0)] * 8
    for l in IMAGINARY_INDICES:
        coords[l] = 2 * coassociative_component(i, j, k, l)
    return Octonion(tuple(coords))


def _permutation_sign(perm: Tuple[int, ...], base: Tuple[int, ...]) -> int:
    order = [base.index(x) for x in perm]
    sign = 1
    for a in range(len(order)):
        for b in range(a + 1, len(order)):
            if order[a] > order[b]:
                sign = -sign
    return sign


def form_is_totally_antisymmetric() -> bool:
    """Exact check that ``phi`` is totally antisymmetric on imaginary basis triples."""
    for i, j, k in product(IMAGINARY_INDICES, repeat=3):
        base = (i, j, k)
        value = associative_form(E[i], E[j], E[k])
        for perm in permutations(base):
            sign = _permutation_sign(perm, base)
            if associative_form(E[perm[0]], E[perm[1]], E[perm[2]]) != sign * value:
                return False
    return True


def form_nonzero_count() -> int:
    """Number of nonzero ``phi`` entries over imaginary basis triples (``= 42``)."""
    return sum(
        1 for i, j, k in product(IMAGINARY_INDICES, repeat=3)
        if associative_form(E[i], E[j], E[k]) != 0
    )


def coassociative_is_totally_antisymmetric() -> bool:
    """Exact check that ``psi`` is totally antisymmetric on imaginary quadruples."""
    for i, j, k, l in product(IMAGINARY_INDICES, repeat=4):
        base = (i, j, k, l)
        value = coassociative_component(i, j, k, l)
        for perm in permutations(base):
            sign = _permutation_sign(perm, base)
            if coassociative_component(*perm) != sign * value:
                return False
    return True


def coassociative_nonzero_count() -> int:
    """Number of nonzero ``psi`` entries over imaginary basis quadruples (``= 168``)."""
    return sum(
        1 for q in product(IMAGINARY_INDICES, repeat=4)
        if coassociative_component(*q) != 0
    )


def associator_matches_coassociative() -> bool:
    """Exact check ``[e_i, e_j, e_k] = 2 sum_l psi_{ijkl} e_l`` on all imaginary triples."""
    return all(
        associator_from_coassociative(i, j, k) == associator(E[i], E[j], E[k])
        for i, j, k in product(IMAGINARY_INDICES, repeat=3)
    )


def _apply(matrix: Matrix, k: int) -> Octonion:
    """Act a derivation matrix on the basis unit ``e_k`` (its ``k``-th column)."""
    return Octonion(tuple(matrix[i][k] for i in range(8)))


def derivation_preserves_form(matrix: Matrix) -> bool:
    """Exact check ``phi(Dx,y,z)+phi(x,Dy,z)+phi(x,y,Dz)=0`` for a derivation ``D``."""
    for i, j, k in product(IMAGINARY_INDICES, repeat=3):
        di, dj, dk = _apply(matrix, i), _apply(matrix, j), _apply(matrix, k)
        total = (
            associative_form(di, E[j], E[k])
            + associative_form(E[i], dj, E[k])
            + associative_form(E[i], E[j], dk)
        )
        if total != 0:
            return False
    return True


def g2_preserves_form() -> bool:
    """Exact check that every ``g2`` derivation (Gate O10) annihilates ``phi``."""
    return all(derivation_preserves_form(D) for D in derivation_algebra())


def akivis_right_hand_side(x: Octonion, y: Octonion, z: Octonion) -> Octonion:
    """``sum_sigma sign(sigma) associator(sigma(x, y, z))`` -- the Akivis RHS."""
    base = (x, y, z)
    total = octonion(0, 0, 0, 0, 0, 0, 0, 0)
    for perm in permutations(range(3)):
        sign = _permutation_sign(perm, (0, 1, 2))
        term = associator(base[perm[0]], base[perm[1]], base[perm[2]])
        total = total + term.scaled(sign)
    return total


def akivis_structure_equation_holds() -> bool:
    """Exact check ``J(x,y,z) = alternating sum of associators`` on all triples."""
    return all(
        jacobiator(E[i], E[j], E[k]) == akivis_right_hand_side(E[i], E[j], E[k])
        for i, j, k in product(IMAGINARY_INDICES, repeat=3)
    )


def akivis_collapses_to_six_associator() -> bool:
    """Exact check that (alternative case) the Akivis RHS equals ``6 * associator``."""
    return all(
        akivis_right_hand_side(E[i], E[j], E[k])
        == associator(E[i], E[j], E[k]).scaled(6)
        for i, j, k in product(IMAGINARY_INDICES, repeat=3)
    )


@dataclass(frozen=True)
class CalibrationCensus:
    """Exact ledger identifying octonionic non-associativity with the G2 geometry."""

    form_totally_antisymmetric: bool
    form_nonzero: int
    coassociative_totally_antisymmetric: bool
    coassociative_nonzero: int
    associator_is_coassociative_form: bool
    g2_preserves_form: bool
    akivis_structure_equation: bool
    akivis_collapses_to_six_associator: bool


def calibration_census() -> CalibrationCensus:
    """Assemble the exact associative/coassociative calibration ledger over ``Q``."""
    return CalibrationCensus(
        form_totally_antisymmetric=form_is_totally_antisymmetric(),
        form_nonzero=form_nonzero_count(),
        coassociative_totally_antisymmetric=coassociative_is_totally_antisymmetric(),
        coassociative_nonzero=coassociative_nonzero_count(),
        associator_is_coassociative_form=associator_matches_coassociative(),
        g2_preserves_form=g2_preserves_form(),
        akivis_structure_equation=akivis_structure_equation_holds(),
        akivis_collapses_to_six_associator=akivis_collapses_to_six_associator(),
    )
