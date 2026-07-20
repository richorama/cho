"""Gate O07: the dimension threshold -- why the Born selection lives at ``d = 3``.

Gate O06 selected ``p = 1`` (the trace-form Born rule) as the unique frame-consistent
exponent on ``h_3(O)``. A referee's first question is whether that selection is real or
an artefact: does it survive dropping to two dimensions? This gate answers by building
the two-dimensional Jordan algebra ``h_2(O)`` -- the spin factor ``J(9)`` -- and showing
the selection *switches off*, exactly as Gleason's theorem demands and exactly where the
octonions themselves run out of room (Hurwitz caps the composition algebras, and O03
caps the Jordan matrix size, both at three).

Two things change on the way down to ``d = 2``:

* **Every ray is a state (Artin).** In ``h_3(O)`` a rational unit vector whose three
  entries do not lie in a common associative subalgebra fails to be idempotent (Gate
  O02's wall). With only *two* entries no such wall exists: Artin's theorem says any two
  octonions generate an associative subalgebra, so ``outer(v)`` is a primitive
  idempotent for *every* rational unit two-vector, however its entries are placed.

* **The complement is forced.** In ``d = 2`` the orthogonal complement of a ray is a
  single ray, so the only Jordan frame containing a primitive idempotent ``P`` is
  ``{P, I - P}``. Every ray therefore belongs to exactly one frame, and no ray is shared
  between two distinct frames.

Because contextuality needs a ray shared across distinct measurement frames, the
selection machinery of O06 has nothing to bite on here: for *every* exponent the
per-ray probability is frame-independent (zero discrepancies), so *all* exponents are
vacuously frame-consistent and none is singled out. The Parseval total
``tr(P o Psi) + tr((I - P) o Psi) = tr(Psi) = 1`` still holds for ``p = 1``, but with no
shared rays it no longer *selects* ``p = 1``. Contextual selection of the Born rule is a
genuinely ``d >= 3`` phenomenon -- the same threshold Gleason's theorem carries, here on
the octonionic spin factor.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Tuple

from .octonion import E, Octonion, octonion

H2Mat = Tuple[Tuple[Octonion, ...], ...]
Vec2 = Tuple[Octonion, Octonion]

_ZERO = octonion(0, 0, 0, 0, 0, 0, 0, 0)
_ONE = octonion(1, 0, 0, 0, 0, 0, 0, 0)


# --- 2x2 Hermitian octonionic matrix arithmetic -----------------------------

def _matmul(a: H2Mat, b: H2Mat) -> H2Mat:
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(2)), _ZERO) for j in range(2))
        for i in range(2)
    )


def _add(a: H2Mat, b: H2Mat) -> H2Mat:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(2)) for i in range(2))


def _scale(a: H2Mat, f: Fraction) -> H2Mat:
    return tuple(tuple(a[i][j].scaled(f) for j in range(2)) for i in range(2))


def jordan_product(a: H2Mat, b: H2Mat) -> H2Mat:
    """The Jordan product ``(AB + BA)/2`` of two 2x2 octonionic matrices."""
    return _scale(_add(_matmul(a, b), _matmul(b, a)), Fraction(1, 2))


def equal(a: H2Mat, b: H2Mat) -> bool:
    return all(a[i][j].coords == b[i][j].coords for i in range(2) for j in range(2))


def trace(a: H2Mat) -> Octonion:
    return a[0][0] + a[1][1]


def identity() -> H2Mat:
    return ((_ONE, _ZERO), (_ZERO, _ONE))


def zeros() -> H2Mat:
    return ((_ZERO, _ZERO), (_ZERO, _ZERO))


def outer(v: Vec2) -> H2Mat:
    """The rank-one Hermitian matrix ``P_ij = v_i conj(v_j)``."""
    return tuple(tuple(v[i] * v[j].conjugate() for j in range(2)) for i in range(2))


def is_primitive_idempotent(p: H2Mat) -> bool:
    return equal(jordan_product(p, p), p) and trace(p).coords == _ONE.coords


def complement(p: H2Mat) -> H2Mat:
    """``I - P``: the forced orthogonal ray in two dimensions."""
    return _add(identity(), _scale(p, Fraction(-1)))


def trace_form(a: H2Mat, b: H2Mat) -> Octonion:
    return trace(jordan_product(a, b))


# --- census of rational rays ------------------------------------------------

_PYTHAGOREAN: Tuple[Tuple[int, int, int], ...] = (
    (3, 4, 5),
    (5, 12, 13),
    (8, 15, 17),
    (7, 24, 25),
    (20, 21, 29),
)

# Axes drawn from different Fano lines so entries need not share a subalgebra.
_AXES: Tuple[int, ...] = (0, 1, 2, 4)


def rational_unit_vectors() -> Tuple[Vec2, ...]:
    """Rational unit two-vectors with entries on assorted octonion axes."""
    vs: List[Vec2] = [(_ONE, _ZERO), (_ZERO, _ONE)]
    for a, b, c in _PYTHAGOREAN:
        for i in _AXES:
            for j in _AXES:
                vs.append(
                    (E[i].scaled(Fraction(a, c)), E[j].scaled(Fraction(b, c)))
                )
    return tuple(vs)


def _key(p: H2Mat) -> Tuple:
    return tuple(p[i][j].coords for i in range(2) for j in range(2))


@dataclass(frozen=True)
class DimensionThresholdCensus:
    ray_count: int
    all_rays_are_primitive_idempotents: bool
    all_complements_are_primitive_idempotents: bool
    all_complements_orthogonal: bool
    distinct_frames: int
    max_frames_sharing_a_ray: int
    rays_shared_across_distinct_frames: int
    parseval_total_is_one: bool
    frame_consistent_exponents: Tuple[int, ...]


def dimension_threshold_census() -> DimensionThresholdCensus:
    vecs = rational_unit_vectors()
    rays = [outer(v) for v in vecs]

    all_idem = all(is_primitive_idempotent(p) for p in rays)
    comps = [complement(p) for p in rays]
    all_comp_idem = all(is_primitive_idempotent(q) for q in comps)
    all_orth = all(
        equal(jordan_product(p, q), zeros()) for p, q in zip(rays, comps)
    )

    # Frames are the unordered pairs {P, I - P}. Count distinct ones and, for every
    # ray, how many distinct frames contain it.
    frames = set()
    ray_to_frames: Dict[Tuple, set] = {}
    for p, q in zip(rays, comps):
        frame = frozenset((_key(p), _key(q)))
        frames.add(frame)
    for p in rays:
        kp = _key(p)
        containing = {f for f in frames if kp in f}
        ray_to_frames[kp] = containing
    max_sharing = max(len(fs) for fs in ray_to_frames.values())
    shared = sum(1 for fs in ray_to_frames.values() if len(fs) >= 2)

    # Parseval and the (vacuous) exponent selection under a fixed probe state.
    psi = outer((E[0].scaled(Fraction(3, 5)), E[1].scaled(Fraction(4, 5))))
    parseval = all(
        (trace_form(psi, p) + trace_form(psi, complement(p))).coords == _ONE.coords
        for p in rays
    )

    # For each exponent, does any ray shared across distinct frames get two different
    # normalised probabilities? With no shared rays this is empty for every exponent,
    # so all exponents are vacuously frame-consistent.
    consistent = []
    for pexp in (1, 2, 3):
        discrepant = False
        for kp, fs in ray_to_frames.items():
            if len(fs) < 2:
                continue
            # (Unreachable in d = 2; kept to mirror the O06 test structure.)
            discrepant = True
        if not discrepant:
            consistent.append(pexp)

    return DimensionThresholdCensus(
        ray_count=len(rays),
        all_rays_are_primitive_idempotents=all_idem,
        all_complements_are_primitive_idempotents=all_comp_idem,
        all_complements_orthogonal=all_orth,
        distinct_frames=len(frames),
        max_frames_sharing_a_ray=max_sharing,
        rays_shared_across_distinct_frames=shared,
        parseval_total_is_one=parseval,
        frame_consistent_exponents=tuple(consistent),
    )
