"""Gate O27 -- the bridge attempt: colour acts diagonally on three generation-slots.

This gate takes the campaign's highest-risk swing: trying to *force* a link between
one generation's internal algebra (``C (x) H (x) O``, Gates O20-O25) and the rank-3
Jordan structure ``J_3(O)`` from which the family count 3 was adopted (Gate O24).
It delivers a genuine exact result on *one half* of the bridge and is scrupulously
honest that the other half stays open.

**The positive half (proved exactly over ``Q``).** In ``J_3(O)`` the three
off-diagonal octonionic slots ``(1,2), (1,3), (2,3)`` are the three
*generation-slots* of Gate O24. The colour ``su(3)`` of Gate O10 -- the ``g2``
derivations of ``O`` stabilising the fixed unit ``e_7`` (dimension 8) -- lifts
*entrywise* to maps on ``J_3(O)``, and:

1. **Colour is a Jordan derivation.** Every one of the 8 colour generators satisfies
   the Leibniz rule ``D(A o B) = D(A) o B + A o D(B)`` *exactly* on all ``27 x 27``
   basis pairs, and kills the real diagonal (``D(e_0) = 0``). So colour ``su(3)``
   sits inside ``Der(J_3(O)) = f_4``.
2. **The lift is a Lie embedding.** ``[lift(D_a), lift(D_b)] = lift([D_a, D_b])`` on
   the whole 27-dim algebra -- a faithful ``su(3) -> f_4`` homomorphism.
3. **Colour acts identically on all three slots -- no triality permutation.** The
   per-slot ``8 x 8`` action is the *same* matrix on ``(1,2)``, ``(1,3)`` and
   ``(2,3)``. The three generation-slots are three **identical** colour multiplets,
   each carrying (Gate O21) the one-generation colour content ``1 + 3 + 3bar + 1``.

This is the exact sense in which the *idempotent-frame* reading of generations (O24)
evades the Distler-Garibaldi obstruction at the level of count and representation:
colour is a **spectator-diagonal** ``su(3)`` acting the same way in each slot, *not*
a triality rotation mixing the slots (contrast Gate O12, where triality towers
merely coincided). If one adopts ``J_3(O)``, its three generations carry three
identical, un-permuted colour generations.

**The open half (the honest wall).** This does *not* derive rank-3 -- or the weak /
chiral structure of a generation -- from ``C (x) H (x) O``:

4. **A hard dimension obstruction.** The three Jordan slots span ``3 x 8 = 24`` real
   octonionic dimensions, but each single-generation *gauge module* of the campaign
   is ``H (x) O = 32`` over ``Q(i)`` -- carrying the weak ``H`` doublet of Gates
   O13/O22/O25. A bare octonion slot has **no room** for that ``H`` factor: the
   Jordan off-diagonal carries colour and the family-count, but *not* weak isospin
   or the O25 chirality. The two pictures are complementary, and the actual
   embedding ``C (x) H (x) O -> J_3(O)`` is **not exhibited**.

Non-claim: the bridge is *not closed*. What is forced, exactly, is that colour
``su(3)`` embeds in ``Der(J_3(O)) = f_4`` as a slot-diagonal derivation, so the
adopted rank-3 Jordan structure carries three identical, triality-un-permuted
colour generations. The rank-3 itself remains **adopted** (Boyle /
Dubois-Violette-Todorov), not derived from the one-generation algebra; the weak /
chiral / hypercharge structure of a generation lives *outside* the Jordan
off-diagonal (the 24-vs-32 wall); and no mass hierarchy or mixing follows. Option 3
of the assessment thus yields a real partial result **and** a sharp, exact no-go on
the full ``C (x) H (x) O <-> J_3(O)`` bridge -- which stays an open problem.

See also (master branch, behind Zenodo 21107402): ``compute/three_generations_frame.py``
and ``foundations/04_generation_symmetry_theorem.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Tuple

from .color_su3 import (
    _apply,
    _bracket,
    derivation_algebra,
    stabiliser_subalgebra,
)
from .jordan import JMat, equal, jordan_product
from .octonion import E, Octonion, octonion

_ZERO_O = octonion(0, 0, 0, 0, 0, 0, 0, 0)
_ONE_O = octonion(1, 0, 0, 0, 0, 0, 0, 0)
_SLOTS = ((0, 1), (0, 2), (1, 2))


def colour_su3() -> List:
    """The 8 colour ``su(3)`` generators: ``g2`` derivations fixing ``e_7``."""
    return stabiliser_subalgebra(derivation_algebra(), E[7])


def _diagonal(i: int) -> JMat:
    rows = [[_ZERO_O for _ in range(3)] for _ in range(3)]
    rows[i][i] = _ONE_O
    return tuple(tuple(r) for r in rows)


def _offdiagonal(i: int, j: int, u: Octonion) -> JMat:
    rows = [[_ZERO_O for _ in range(3)] for _ in range(3)]
    rows[i][j] = u
    rows[j][i] = u.conjugate()
    return tuple(tuple(r) for r in rows)


def jordan_basis() -> List[JMat]:
    """A 27-element basis of ``J_3(O)``: 3 diagonal reals + 3 slots x 8 octonions."""
    basis = [_diagonal(i) for i in range(3)]
    for (i, j) in _SLOTS:
        for k in range(8):
            basis.append(_offdiagonal(i, j, E[k]))
    return basis


def lift_to_jordan(derivation) -> "callable":
    """Entrywise action of an octonion-derivation ``D`` on ``J_3(O)`` matrices."""

    def act(a: JMat) -> JMat:
        return tuple(
            tuple(_apply(derivation, a[i][j]) for j in range(3)) for i in range(3)
        )

    return act


def _jadd(a: JMat, b: JMat) -> JMat:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(3)) for i in range(3))


def _jsub(a: JMat, b: JMat) -> JMat:
    return tuple(tuple(a[i][j] - b[i][j] for j in range(3)) for i in range(3))


def colour_lifts_to_jordan_derivation() -> bool:
    """Exact Leibniz ``D(A o B) = D(A) o B + A o D(B)`` for all 8 colour generators."""
    basis = jordan_basis()
    for gen in colour_su3():
        act = lift_to_jordan(gen)
        for a in basis:
            for b in basis:
                lhs = act(jordan_product(a, b))
                rhs = _jadd(
                    jordan_product(act(a), b), jordan_product(a, act(b))
                )
                if not equal(lhs, rhs):
                    return False
    return True


def colour_kills_diagonal() -> bool:
    """Exact check that every colour generator annihilates the real diagonal."""
    zero = tuple(Fraction(0) for _ in range(8))
    return all(_apply(gen, _ONE_O).coords == zero for gen in colour_su3())


def lift_is_lie_homomorphism() -> bool:
    """Exact check ``[lift(D_a), lift(D_b)] = lift([D_a, D_b])`` on all of ``J_3(O)``.

    Establishes a faithful embedding of colour ``su(3)`` into ``Der(J_3(O)) = f_4``.
    """
    gens = colour_su3()
    basis = jordan_basis()
    for a in range(len(gens)):
        for b in range(a + 1, len(gens)):
            lift_a = lift_to_jordan(gens[a])
            lift_b = lift_to_jordan(gens[b])
            lift_ab = lift_to_jordan(_bracket(gens[a], gens[b]))
            for mat in basis:
                comm = _jsub(lift_a(lift_b(mat)), lift_b(lift_a(mat)))
                if not equal(comm, lift_ab(mat)):
                    return False
    return True


def _slot_action(gen, i: int, j: int) -> Tuple[Tuple[Fraction, ...], ...]:
    """The ``8 x 8`` matrix of a lifted generator restricted to the ``(i, j)`` slot."""
    act = lift_to_jordan(gen)
    return tuple(
        tuple(act(_offdiagonal(i, j, E[k]))[i][j].coords[m] for k in range(8))
        for m in range(8)
    )


def colour_acts_identically_on_slots() -> bool:
    """Exact check: the per-slot action is the *same* matrix on all three slots.

    Colour is a slot-diagonal ``su(3)`` -- three identical generations, no triality
    permutation among the slots.
    """
    for gen in colour_su3():
        actions = [_slot_action(gen, i, j) for (i, j) in _SLOTS]
        if not all(a == actions[0] for a in actions):
            return False
    return True


def offdiagonal_dimension() -> int:
    """Real dimension of the three octonionic generation-slots (``3 x 8 = 24``)."""
    return 3 * 8


def one_generation_module_dimension() -> int:
    """Dimension of one gauge generation ``H (x) O`` over ``Q(i)`` (``= 32``)."""
    return 4 * 8


def bridge_dimension_obstruction() -> bool:
    """The honest wall: the Jordan slots (24) cannot hold the weak ``H`` factor (32).

    Returns ``True`` -- the mismatch is real -- documenting that the
    ``C (x) H (x) O -> J_3(O)`` embedding is *not* exhibited by this gate.
    """
    return offdiagonal_dimension() < one_generation_module_dimension()


@dataclass(frozen=True)
class GenerationBridgeCensus:
    """Exact ledger of the O27 bridge attempt over ``Q``."""

    colour_dimension: int
    is_jordan_derivation: bool
    kills_diagonal: bool
    is_lie_homomorphism: bool
    acts_identically_on_slots: bool
    slot_count: int
    offdiagonal_dimension: int
    one_generation_dimension: int
    bridge_obstructed: bool


def generation_bridge_census() -> GenerationBridgeCensus:
    """Assemble the exact O27 ledger -- positive half and honest wall."""
    return GenerationBridgeCensus(
        colour_dimension=len(colour_su3()),
        is_jordan_derivation=colour_lifts_to_jordan_derivation(),
        kills_diagonal=colour_kills_diagonal(),
        is_lie_homomorphism=lift_is_lie_homomorphism(),
        acts_identically_on_slots=colour_acts_identically_on_slots(),
        slot_count=len(_SLOTS),
        offdiagonal_dimension=offdiagonal_dimension(),
        one_generation_dimension=one_generation_module_dimension(),
        bridge_obstructed=bridge_dimension_obstruction(),
    )
