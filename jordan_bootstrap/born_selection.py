"""Gate O06: the Born rule as the unique frame-consistent rule on ``h_3(O)``.

Gates O01-O02 *assumed* the trace-form Born rule ``p(P) = tr(P o Psi)``. This gate
turns the exponent itself into a holdout and asks whether observer-consistency forces
it, exactly reproducing the amplitude campaign's selection (Gates Q11/Q12) one algebra
higher -- on the exceptional Jordan algebra.

Consider the one-parameter family of ``p``-power rules that assign a ray (primitive
idempotent) ``P`` the weight ``t(P)^p`` with ``t(P) = tr(P o Psi)`` the exact Born
weight (a rational) and ``p = 1, 2, 3, ...``.  Observer-consistency is
*frame-consistency*: the total weight of a complete measurement -- the sum over the
three rays of any Jordan frame -- must not depend on which frame (which maximal set of
jointly measurable outcomes) the observer chose, else the total probability would track
the arbitrary fine measurement rather than the state.

The exact censuses below, over the rationals, show:

* ``p = 1`` (Born): the frame total is ``sum_i tr(P_i o Psi) = tr(Psi o I) = tr(Psi) =
  1`` for *every* Jordan frame -- the resolution of the identity is an octonionic
  Parseval identity.  So the normalised probability of a shared ray depends only on the
  ray and the state: zero contextual discrepancies.
* ``p = 2`` and ``p = 3``: the frame total depends on the frame, so a ray shared between
  two frames is assigned two different normalised probabilities -- a genuine
  Kochen-Specker-style discrepancy, exact over the rationals.
* Only a genuinely *superposing* change of frame exposes ``p > 1``; a classical
  relabelling (permuting the three rays of one frame) leaves the total unchanged for
  every exponent, so superposition is what does the selecting.

Hence ``p = 1`` -- the trace-form Born rule -- is the unique frame-consistent exponent,
and it remains so on the *non-associative* ``h_3(O)``: the exceptional Jordan algebra
does not spoil the Gleason-style selection.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Tuple

from .contextuality import IntRay, contexts, ray_to_state
from .jordan import JMat, is_jordan_frame, outer, trace_form
from .octonion import E, octonion

EXPONENTS: Tuple[int, ...] = (1, 2, 3)


def octonionic_reference_state() -> JMat:
    """A genuinely octonionic pure state used as the probe density.

    ``v = (2/3, (2/3) e_1, (1/3) e_2)`` is a rational unit vector whose entries span a
    quaternion subalgebra, so ``outer(v)`` is a primitive idempotent that lives strictly
    outside the real part of ``h_3(O)``.
    """
    v = (
        octonion(Fraction(2, 3), 0, 0, 0, 0, 0, 0, 0),
        E[1].scaled(Fraction(2, 3)),
        E[2].scaled(Fraction(1, 3)),
    )
    return outer(v)


def born_weight(psi: JMat, ray: IntRay) -> Fraction:
    """The exact Born weight ``t(P) = tr(P o Psi)`` of a ray, a rational scalar."""
    value = trace_form(psi, ray_to_state(ray))
    if any(c != 0 for c in value.coords[1:]):
        raise ValueError("Born weight is not real -- Psi or P is not Hermitian")
    return value.coords[0]


def frame_total(psi: JMat, frame: Tuple[IntRay, ...], p: int) -> Fraction:
    """The ``p``-power total ``sum_i t(P_i)^p`` over a frame's three rays."""
    return sum((born_weight(psi, r) ** p for r in frame), Fraction(0))


def frame_consistent_exponents(
    psi: JMat, frames: Tuple[Tuple[IntRay, ...], ...], exponents: Tuple[int, ...]
) -> Tuple[int, ...]:
    """Exponents whose frame total is the *same* rational for every frame."""
    consistent = []
    for p in exponents:
        totals = {frame_total(psi, f, p) for f in frames}
        if len(totals) == 1:
            consistent.append(p)
    return tuple(consistent)


def contextual_discrepancies(
    psi: JMat, frames: Tuple[Tuple[IntRay, ...], ...], p: int
) -> int:
    """Shared rays whose normalised probability ``t^p / total`` is frame-dependent."""
    ray_frames: Dict[IntRay, List[Tuple[IntRay, ...]]] = defaultdict(list)
    for f in frames:
        for r in f:
            ray_frames[r].append(f)
    discrepant = 0
    for ray, fs in ray_frames.items():
        if len(fs) < 2:
            continue
        weight = born_weight(psi, ray) ** p
        probs = {weight / frame_total(psi, f, p) for f in fs}
        if len(probs) > 1:
            discrepant += 1
    return discrepant


def shared_ray_count(frames: Tuple[Tuple[IntRay, ...], ...]) -> int:
    counts: Dict[IntRay, int] = defaultdict(int)
    for f in frames:
        for r in f:
            counts[r] += 1
    return sum(1 for n in counts.values() if n >= 2)


@dataclass(frozen=True)
class BornSelectionCensus:
    bound: int
    context_count: int
    shared_ray_count: int
    all_contexts_are_jordan_frames: bool
    born_frame_total_is_always_one: bool
    born_contextual_discrepancies: int
    power2_distinct_frame_totals: int
    power2_contextual_discrepancies: int
    power3_distinct_frame_totals: int
    power3_contextual_discrepancies: int
    frame_consistent_exponents: Tuple[int, ...]
    permutation_leaves_total_invariant: bool


def born_selection_census(bound: int = 15) -> BornSelectionCensus:
    psi = octonionic_reference_state()
    frames = contexts(bound)

    all_frames = all(
        is_jordan_frame(tuple(ray_to_state(r) for r in f)) for f in frames
    )

    born_totals = {frame_total(psi, f, 1) for f in frames}
    born_all_one = born_totals == {Fraction(1)}

    p2_totals = {frame_total(psi, f, 2) for f in frames}
    p3_totals = {frame_total(psi, f, 3) for f in frames}

    # A classical relabelling (permuting a frame's rays) cannot change the total for
    # any exponent, so it certifies nothing -- superposition does the selecting.
    perm_invariant = True
    for f in frames:
        base = frame_total(psi, f, 2)
        for perm in ((f[1], f[2], f[0]), (f[2], f[0], f[1]), (f[0], f[2], f[1])):
            if frame_total(psi, perm, 2) != base:
                perm_invariant = False
                break
        if not perm_invariant:
            break

    return BornSelectionCensus(
        bound=bound,
        context_count=len(frames),
        shared_ray_count=shared_ray_count(frames),
        all_contexts_are_jordan_frames=all_frames,
        born_frame_total_is_always_one=born_all_one,
        born_contextual_discrepancies=contextual_discrepancies(psi, frames, 1),
        power2_distinct_frame_totals=len(p2_totals),
        power2_contextual_discrepancies=contextual_discrepancies(psi, frames, 2),
        power3_distinct_frame_totals=len(p3_totals),
        power3_contextual_discrepancies=contextual_discrepancies(psi, frames, 3),
        frame_consistent_exponents=frame_consistent_exponents(psi, frames, EXPONENTS),
        permutation_leaves_total_invariant=perm_invariant,
    )
