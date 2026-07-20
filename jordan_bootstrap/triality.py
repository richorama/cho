"""Gate O08: triality -- the S_3 symmetry of the three octonionic slots of h_3(O).

Gate O04 certified the entrywise symmetries of ``h_3(O)``: the automorphisms of the
octonions (the finite skeleton of ``G_2``) applied to each matrix entry, fixing the
three matrix *positions*. This gate certifies the complementary symmetry that O04 cannot
reach -- the one that *moves the positions* -- and identifies it as triality.

Write a Hermitian octonionic matrix as ::

        [ a   z   y* ]
        [ z*  b   x  ]
        [ y   x*  c  ]

with real diagonal ``a, b, c`` and three off-diagonal octonions ``x, y, z``. Conjugating
by a ``3x3`` permutation matrix, ``phi_sigma(A)_{ij} = A_{sigma(i), sigma(j)}``, is a
Jordan automorphism for every permutation ``sigma`` (a reindexing of the matrix-product
sum, valid despite non-associativity). The six of them form an ``S_3``, and the
three-cycle *cyclically permutes the three off-diagonal slots* ``x -> y -> z``.

Those three slots are exactly the three inequivalent eight-dimensional representations
of ``Spin(8)`` -- the vector ``8_v`` and the two spinors ``8_s, 8_c`` -- and the cyclic
permutation that rotates them is the finite shadow of *triality*, the order-three outer
automorphism of ``Spin(8)`` that only the octonions possess (``R, C, H`` have no such
symmetry). Combined with O04's entrywise ``G_2`` action it generates a strictly larger
finite subgroup of ``F_4 = Aut(h_3(O))``.

Everything is exact over the rationals. The census verifies that each permutation is a
Jordan automorphism preserving the trace, primitive idempotents, Jordan frames and every
Born trace-form probability; that the three-cycle has order three and rotates the slots;
that a permutation genuinely moves content between positions (so it is *not* an entrywise
O04 automorphism); and that composing a permutation with an O04 monomial still preserves
the Born rule -- the two symmetries generate a common invariance.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations
from typing import Tuple

from .octonion import E, Octonion, octonion
from .jordan import (
    JMat,
    equal,
    is_jordan_frame,
    is_primitive_idempotent,
    jordan_product,
    outer,
    trace,
    trace_form,
)
from .contextuality import ray_to_state
from .born_selection import octonionic_reference_state
from .automorphism import apply_jordan, automorphism_group

Perm = Tuple[int, int, int]

_ZERO = octonion(0, 0, 0, 0, 0, 0, 0, 0)


def all_permutations() -> Tuple[Perm, ...]:
    """The six index permutations -- the S_3 acting on the three coordinates."""
    return tuple(permutations((0, 1, 2)))


def apply_permutation(sigma: Perm, a: JMat) -> JMat:
    """Conjugation by the permutation matrix: ``phi(A)_{ij} = A_{sigma(i),sigma(j)}``."""
    return tuple(tuple(a[sigma[i]][sigma[j]] for j in range(3)) for i in range(3))


def compose(sigma: Perm, tau: Perm) -> Perm:
    """The permutation applying ``tau`` then ``sigma``."""
    return tuple(sigma[tau[i]] for i in range(3))


def hermitian(
    a: Octonion, b: Octonion, c: Octonion, x: Octonion, y: Octonion, z: Octonion
) -> JMat:
    """Assemble a Hermitian octonionic matrix from its diagonal and three slots."""
    return (
        (a, z, y.conjugate()),
        (z.conjugate(), b, x),
        (y, x.conjugate(), c),
    )


def slot_state(slot: int) -> JMat:
    """A primitive idempotent whose off-diagonal content sits in a single slot.

    ``slot`` 0/1/2 -> the ``x``/``y``/``z`` slot, built from a real rational unit vector
    supported on the two coordinates that meet that slot.
    """
    r = octonion(Fraction(3, 5), 0, 0, 0, 0, 0, 0, 0)
    s = octonion(Fraction(4, 5), 0, 0, 0, 0, 0, 0, 0)
    if slot == 0:      # x-slot: positions (1,2)/(2,1)
        v = (_ZERO, r, s)
    elif slot == 1:    # y-slot: positions (0,2)/(2,0)
        v = (r, _ZERO, s)
    else:              # z-slot: positions (0,1)/(1,0)
        v = (r, s, _ZERO)
    return outer(v)


# The upper off-diagonal position that defines each slot: x -> (1,2), y -> (0,2), z -> (0,1).
_SLOT_POSITION = {0: (1, 2), 1: (0, 2), 2: (0, 1)}


def occupied_slots(a: JMat) -> Tuple[int, ...]:
    """Which off-diagonal slots carry nonzero content."""
    return tuple(
        slot for slot, (i, j) in _SLOT_POSITION.items() if not a[i][j].is_zero()
    )


def _test_matrices() -> Tuple[JMat, ...]:
    a = octonion(Fraction(1), 0, 0, 0, 0, 0, 0, 0)
    b = octonion(Fraction(-2), 0, 0, 0, 0, 0, 0, 0)
    c = octonion(Fraction(3), 0, 0, 0, 0, 0, 0, 0)
    x = E[1].scaled(Fraction(2, 3)) + E[4].scaled(Fraction(1, 5))
    y = E[2].scaled(Fraction(-1, 2)) + E[7].scaled(Fraction(1, 3))
    z = E[3].scaled(Fraction(1, 4)) + E[6].scaled(Fraction(2, 7))
    return (
        hermitian(a, b, c, x, y, z),
        octonionic_reference_state(),
        hermitian(octonion(1, 0, 0, 0, 0, 0, 0, 0), _ZERO, _ZERO, _ZERO, _ZERO, _ZERO),
    )


def _states() -> Tuple[JMat, ...]:
    rays = ((1, 2, 2), (2, -2, 1), (2, 1, -2), (1, 0, 0), (0, 1, 0))
    return tuple(ray_to_state(r) for r in rays) + (
        octonionic_reference_state(),
        slot_state(0),
        slot_state(1),
        slot_state(2),
    )


def _frames() -> Tuple[Tuple[JMat, ...], ...]:
    a = tuple(ray_to_state(r) for r in ((1, 2, 2), (2, -2, 1), (2, 1, -2)))
    b = tuple(ray_to_state(r) for r in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    return (a, b)


@dataclass(frozen=True)
class TrialityCensus:
    permutation_count: int
    all_are_jordan_automorphisms: bool
    trace_preserving: bool
    idempotent_preserving: bool
    frame_preserving: bool
    born_invariant_checks: int
    born_invariant_mismatches: int
    three_cycle_order: int
    slots_are_cyclically_permuted: bool
    permutation_moves_positions: bool
    combined_with_o04_born_checks: int
    combined_with_o04_born_mismatches: int


def triality_census() -> TrialityCensus:
    perms = all_permutations()
    mats = _test_matrices()
    states = _states()
    frames = _frames()

    # 1. Each permutation is a Jordan automorphism preserving the trace.
    auto = True
    trace_ok = True
    for sigma in perms:
        for a in mats:
            for b in mats:
                if not equal(
                    apply_permutation(sigma, jordan_product(a, b)),
                    jordan_product(apply_permutation(sigma, a), apply_permutation(sigma, b)),
                ):
                    auto = False
            if trace(apply_permutation(sigma, a)).coords != trace(a).coords:
                trace_ok = False

    # 2. Idempotents, frames and Born probabilities are preserved.
    idem_ok = all(
        is_primitive_idempotent(apply_permutation(sigma, p))
        for sigma in perms for p in states
    )
    frame_ok = all(
        is_jordan_frame(tuple(apply_permutation(sigma, q) for q in f))
        for sigma in perms for f in frames
    )
    born_checks = 0
    born_mismatch = 0
    for sigma in perms:
        for i in range(len(states)):
            for j in range(i, len(states)):
                born_checks += 1
                lhs = trace_form(states[i], states[j])
                rhs = trace_form(
                    apply_permutation(sigma, states[i]),
                    apply_permutation(sigma, states[j]),
                )
                if lhs.coords != rhs.coords:
                    born_mismatch += 1

    # 3. The three-cycle has order three and rotates the three slots.
    cycle: Perm = (1, 2, 0)
    order = 1
    power = cycle
    identity: Perm = (0, 1, 2)
    while power != identity and order < 10:
        power = compose(cycle, power)
        order += 1
    s0, s1, s2 = slot_state(0), slot_state(1), slot_state(2)
    rotated = [occupied_slots(apply_permutation(cycle, s)) for s in (s0, s1, s2)]
    # Each single-slot state maps to a single-slot state, and the three images occupy
    # three distinct slots forming a non-trivial 3-cycle of {x, y, z}.
    slot_rotation = (
        all(len(r) == 1 for r in rotated)
        and {r[0] for r in rotated} == {0, 1, 2}
        and rotated[0][0] != 0
    )

    # 4. A permutation moves content between positions, so it is not an entrywise O04
    # automorphism (those fix every position; a real diagonal is left in place).
    diag = _test_matrices()[2]  # content only at position (0,0)
    moved = apply_permutation(cycle, diag)
    entrywise_images = {
        tuple(apply_jordan(g, diag)[i][j].coords for i in range(3) for j in range(3))
        for g in automorphism_group()
    }
    moved_key = tuple(moved[i][j].coords for i in range(3) for j in range(3))
    moves_positions = moved_key not in entrywise_images

    # 5. Composing a permutation with an O04 monomial still preserves Born.
    sample = automorphism_group()[:24]
    combined_checks = 0
    combined_mismatch = 0
    for g in sample:
        for i in range(len(states)):
            j = (i + 1) % len(states)
            combined_checks += 1
            p = apply_permutation(cycle, apply_jordan(g, states[i]))
            q = apply_permutation(cycle, apply_jordan(g, states[j]))
            if trace_form(p, q).coords != trace_form(states[i], states[j]).coords:
                combined_mismatch += 1

    return TrialityCensus(
        permutation_count=len(perms),
        all_are_jordan_automorphisms=auto,
        trace_preserving=trace_ok,
        idempotent_preserving=idem_ok,
        frame_preserving=frame_ok,
        born_invariant_checks=born_checks,
        born_invariant_mismatches=born_mismatch,
        three_cycle_order=order,
        slots_are_cyclically_permuted=slot_rotation,
        permutation_moves_positions=moves_positions,
        combined_with_o04_born_checks=combined_checks,
        combined_with_o04_born_mismatches=combined_mismatch,
    )
