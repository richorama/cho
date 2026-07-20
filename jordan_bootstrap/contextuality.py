"""Gate O05: Kochen-Specker contextuality on ``h_3(O)`` -- the rational verdict.

The amplitude campaign found state-independent contextuality (Gate Q08) through the
Peres-Mermin magic square, a *two-qubit* construction living in ``M_4(C)``. That road
is closed here: Gate O03 proved octonions admit no composite system, so the
magic-square route to contextuality cannot even be posed over ``O``.

The only remaining road is the original, single-system Kochen-Specker theorem in
dimension three -- exactly the size at which ``h_3(O)`` (the octonionic projective
plane) lives. A *context* is a Jordan frame: three mutually Jordan-orthogonal
primitive idempotents (rank-one projectors / rays) summing to the identity. A
deterministic non-contextual value-state is a ``{0, 1}`` labelling of the rays that
gives exactly one ``1`` in every context. Kochen and Specker showed no such labelling
exists over the *real* unit sphere -- but their rays are irrational.

Under this repository's exact-rational discipline a ray must be a *rational* unit
vector, i.e. a primitive integer vector ``(a, b, c)`` whose norm ``a^2 + b^2 + c^2``
is a perfect square (only then is ``(a, b, c) / sqrt(norm)`` rational and
``outer(v)`` a genuine primitive idempotent of ``h_3(O)``). Over these rays the
Kochen-Specker obstruction *disappears*, and it does so constructively:

  Lemma 1. A primitive integer vector with perfect-square norm has exactly one odd
  coordinate.  (Mod 4 a square is ``0`` or ``1``; the norm is congruent to the number
  of odd coordinates, ruling out three odds, and primitivity rules out zero.)

  Lemma 2. Two orthogonal such rays carry their odd coordinate in *different*
  positions.  (If they shared a position the dot product would be odd, hence nonzero.)

  Corollary (Godsil-Zaks, 1988). Label every rational ray ``1`` iff its unique odd
  coordinate sits in position ``0``.  By Lemma 2 the three rays of any context occupy
  three distinct positions, so exactly one is labelled ``1``: an explicit, exact,
  deterministic non-contextual value-state on *all* rational rays at once.

So both roads to contextuality close over the exact-rational octonions: the composite
road is blocked by O03, and the single-system road by an explicit rational colouring.
Genuine Kochen-Specker contextuality in ``d = 3`` is an *irrational* phenomenon --
invisible at the resolution this campaign computes in. Meanwhile the octonionic Born
rule remains a (different, probabilistic) non-contextual assignment: for any state the
three Born probabilities of a context sum to exactly ``1``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd, isqrt
from typing import Dict, List, Tuple

from .jordan import (
    is_jordan_frame,
    is_primitive_idempotent,
    outer,
    trace_form,
)
from .octonion import Octonion, octonion

IntRay = Tuple[int, int, int]


# --- rational-ray geometry (exact integers) ---------------------------------

def _dot(a: IntRay, b: IntRay) -> int:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a: IntRay, b: IntRay) -> IntRay:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def primitive(v: IntRay) -> IntRay:
    """Reduce a nonzero integer vector to its canonical primitive representative.

    Divide out the gcd and fix the sign so the first nonzero coordinate is positive;
    this makes each ray (a one-dimensional subspace) a unique tuple.
    """
    g = gcd(gcd(abs(v[0]), abs(v[1])), abs(v[2]))
    if g == 0:
        raise ValueError("the zero vector is not a ray")
    v = (v[0] // g, v[1] // g, v[2] // g)
    for x in v:
        if x != 0:
            if x < 0:
                v = (-v[0], -v[1], -v[2])
            break
    return v


def is_rational_unit_ray(v: IntRay) -> bool:
    """True iff ``v`` scales to a rational point of the unit sphere.

    Equivalently its squared norm is a perfect square, so ``v / sqrt(norm)`` has
    rational coordinates and ``outer`` of it is an exact idempotent of ``h_3(O)``.
    """
    n = _dot(v, v)
    r = isqrt(n)
    return r * r == n


def rational_unit_rays(bound: int) -> Tuple[IntRay, ...]:
    """All rational-unit rays with integer coordinates in ``[-bound, bound]``."""
    seen: Dict[IntRay, None] = {}
    for x in range(-bound, bound + 1):
        for y in range(-bound, bound + 1):
            for z in range(-bound, bound + 1):
                if (x, y, z) == (0, 0, 0):
                    continue
                if not is_rational_unit_ray((x, y, z)):
                    continue
                seen.setdefault(primitive((x, y, z)), None)
    return tuple(seen)


def contexts(bound: int) -> Tuple[Tuple[IntRay, IntRay, IntRay], ...]:
    """Every orthonormal triple (Jordan frame) drawn from the rational-unit rays.

    Two orthogonal rational-unit rays complete uniquely: their cross product is a
    third ray, automatically of perfect-square norm ``|u|^2 |v|^2``.
    """
    rays = rational_unit_rays(bound)
    index = {r: i for i, r in enumerate(rays)}
    frames: List[Tuple[IntRay, IntRay, IntRay]] = []
    for i, u in enumerate(rays):
        for j in range(i + 1, len(rays)):
            w = rays[j]
            if _dot(u, w) != 0:
                continue
            c = primitive(_cross(u, w))
            k = index.get(c)
            if k is not None and k > j:
                frames.append((u, w, c))
    return tuple(frames)


# --- the octonionic lift ----------------------------------------------------

def ray_to_state(v: IntRay):
    """Embed a rational-unit ray as a real primitive idempotent of ``h_3(O)``."""
    m = isqrt(_dot(v, v))
    coords = tuple(octonion(Fraction(c, m), 0, 0, 0, 0, 0, 0, 0) for c in v)
    return outer(coords)


# --- Lemma 1 / Lemma 2: the exact parity structure --------------------------

def odd_position(v: IntRay) -> int:
    """The index of the unique odd coordinate (Lemma 1); raises if not unique."""
    odds = [i for i, x in enumerate(v) if x % 2 != 0]
    if len(odds) != 1:
        raise ValueError(f"ray {v} does not have exactly one odd coordinate")
    return odds[0]


def godsil_zaks_value(v: IntRay) -> int:
    """The explicit deterministic non-contextual value: ``1`` iff odd coord at 0."""
    return 1 if odd_position(v) == 0 else 0


# --- census -----------------------------------------------------------------

@dataclass(frozen=True)
class ContextualityCensus:
    bound: int
    ray_count: int
    context_count: int
    all_rays_are_primitive_idempotents: bool
    all_contexts_are_jordan_frames: bool
    rays_with_unique_odd_coordinate: int
    orthogonal_pairs_checked: int
    orthogonal_pairs_with_distinct_odd_position: int
    godsil_zaks_context_violations: int
    born_context_sum_checks: int
    born_context_sum_violations: int


def contextuality_census(bound: int = 11) -> ContextualityCensus:
    rays = rational_unit_rays(bound)
    frames = contexts(bound)

    all_idem = all(is_primitive_idempotent(ray_to_state(r)) for r in rays)
    all_frames = all(
        is_jordan_frame(tuple(ray_to_state(r) for r in f)) for f in frames
    )

    unique_odd = sum(
        1 for r in rays if len([i for i, x in enumerate(r) if x % 2]) == 1
    )

    # Lemma 2: orthogonal pairs sit in distinct odd-coordinate positions.
    pairs = 0
    distinct = 0
    for i, u in enumerate(rays):
        for j in range(i + 1, len(rays)):
            w = rays[j]
            if _dot(u, w) != 0:
                continue
            pairs += 1
            if odd_position(u) != odd_position(w):
                distinct += 1

    # Corollary: the explicit value-state gives exactly one 1 per context.
    gz_violations = sum(
        1 for f in frames if sum(godsil_zaks_value(r) for r in f) != 1
    )

    # Positive companion: the octonionic Born rule is a non-contextual probability
    # assignment. Use a genuinely octonionic state (entries in an octonion subalgebra)
    # and check every context's three Born probabilities sum to exactly one.
    psi = _octonionic_state()
    born_checks = 0
    born_violations = 0
    one = octonion(1, 0, 0, 0, 0, 0, 0, 0)
    for f in frames:
        total = octonion(0, 0, 0, 0, 0, 0, 0, 0)
        for r in f:
            total = total + trace_form(psi, ray_to_state(r))
        born_checks += 1
        if total.coords != one.coords:
            born_violations += 1

    return ContextualityCensus(
        bound=bound,
        ray_count=len(rays),
        context_count=len(frames),
        all_rays_are_primitive_idempotents=all_idem,
        all_contexts_are_jordan_frames=all_frames,
        rays_with_unique_odd_coordinate=unique_odd,
        orthogonal_pairs_checked=pairs,
        orthogonal_pairs_with_distinct_odd_position=distinct,
        godsil_zaks_context_violations=gz_violations,
        born_context_sum_checks=born_checks,
        born_context_sum_violations=born_violations,
    )


def _octonionic_state():
    """A genuine pure state of ``h_3(O)`` with entries outside the reals.

    ``v = (2/3, (2/3) e_1, (1/3) e_2)`` is a rational unit vector whose entries span
    a quaternion subalgebra, so ``outer(v)`` is a primitive idempotent living
    strictly inside the octonionic (non-real) part of the algebra.
    """
    from .octonion import E

    v = (
        octonion(Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0),
        E[1].scaled(Fraction(2, 3)),
        E[2].scaled(Fraction(1, 3)),
    )
    return outer(v)
