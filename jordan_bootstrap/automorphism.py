"""Gate O04: Born invariance under the octonion automorphism group (Fano / F4).

Gate O00 showed that *relabelings* (signed permutations of the amplitude basis)
cannot move the Born norm. This gate strengthens "representation change" from a
mere relabeling to a genuine *algebra automorphism* of the octonions, and lifts it
to the exceptional Jordan algebra ``h_3(O)``.

The octonion automorphism group is the exceptional compact Lie group ``G_2``. Its
finite subgroup of *monomial* automorphisms -- those permuting the set
``{+-e_1, ..., +-e_7}`` -- has order **1344 = 168 x 8**: the Fano-plane collineation
group ``GL(3,2) = PSL(2,7)`` (order 168) extended by the ``2^3`` independent sign
changes. Every such ``phi`` is enumerated here exactly (no floating point).

Lifting ``phi`` entrywise to a Hermitian octonionic matrix gives an automorphism
``Phi`` of ``h_3(O)`` that fixes the real diagonal. This gate certifies exactly that
each ``Phi``:

* is a Jordan automorphism (``Phi(A o B) = Phi(A) o Phi(B)``) that preserves the trace;
* sends primitive idempotents to primitive idempotents (pure states of ``OP^2``);
* leaves every Born trace-form probability ``tr(P o Q)`` invariant.

So the Born rule of Gates O01/O02 is invariant under the full finite octonion
symmetry, not just under coordinate relabeling -- the resolution-agreement
principle expressed at the level of the algebra's automorphisms.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from typing import Dict, Tuple

from .octonion import E, Octonion, octonion
from .jordan import (
    JMat,
    is_primitive_idempotent,
    jordan_product,
    outer,
    trace,
    equal,
)

_ZERO_O = octonion(0, 0, 0, 0, 0, 0, 0, 0)
_SIGNED = tuple((s, k) for k in range(1, 8) for s in (1, -1))


@dataclass(frozen=True)
class Automorphism:
    """A monomial octonion automorphism ``e_i -> sign[i] e_{perm[i]}`` (``e_0`` fixed)."""

    perm: Tuple[int, ...]   # perm[i-1] = image index of e_i, for i in 1..7
    sign: Tuple[int, ...]   # sign[i-1] in {+1, -1}


def _signed_octonion(s: int, k: int) -> Octonion:
    return E[k].scaled(s)


def _as_signed_unit(o: Octonion) -> Tuple[int, int] | None:
    nz = [(k, o.coords[k]) for k in range(8) if o.coords[k] != 0]
    if len(nz) != 1:
        return None
    k, v = nz[0]
    if v == 1:
        return (1, k)
    if v == -1:
        return (-1, k)
    return None


def _table(i: int, j: int) -> Tuple[int, int]:
    """``e_i e_j = sign * e_k`` for distinct ``i, j`` in ``1..7``."""
    r = E[i] * E[j]
    for k in range(8):
        if r.coords[k] != 0:
            return (int(r.coords[k]), k)
    return (0, 0)


def apply_octonion(aut: Automorphism, o: Octonion) -> Octonion:
    """Apply ``phi`` to an octonion: fix the real part, permute-and-sign the rest."""
    coords = [Fraction(0)] * 8
    coords[0] = o.coords[0]
    for i in range(1, 8):
        coords[aut.perm[i - 1]] += o.coords[i] * aut.sign[i - 1]
    return Octonion(tuple(coords))


def is_octonion_automorphism(aut: Automorphism) -> bool:
    """Exact check ``phi(e_i e_j) = phi(e_i) phi(e_j)`` for all basis pairs."""
    images = {i: _signed_octonion(aut.sign[i - 1], aut.perm[i - 1]) for i in range(1, 8)}
    if sorted(aut.perm) != list(range(1, 8)):
        return False
    for i in range(1, 8):
        for j in range(1, 8):
            lhs = images[i] * images[j]
            if i == j:
                if lhs.coords != octonion(-1, 0, 0, 0, 0, 0, 0, 0).coords:
                    return False
            else:
                s, k = _table(i, j)
                if lhs.coords != images[k].scaled(s).coords:
                    return False
    return True


@lru_cache(maxsize=1)
def automorphism_group() -> Tuple[Automorphism, ...]:
    """Enumerate every monomial octonion automorphism (the order-1344 group)."""
    auts = []
    for m1 in _SIGNED:
        for m2 in _SIGNED:
            for m4 in _SIGNED:
                images: Dict[int, Octonion] = {
                    1: _signed_octonion(*m1),
                    2: _signed_octonion(*m2),
                    4: _signed_octonion(*m4),
                }
                images[3] = images[1] * images[2]   # e1 e2 = e3
                images[5] = images[1] * images[4]    # e1 e4 = e5
                images[6] = images[2] * images[4]    # e2 e4 = e6
                images[7] = images[3] * images[4]    # e3 e4 = e7
                units = [_as_signed_unit(images[i]) for i in range(1, 8)]
                if any(u is None for u in units):
                    continue
                perm = tuple(u[1] for u in units)
                sign = tuple(u[0] for u in units)
                if sorted(perm) != list(range(1, 8)):
                    continue
                aut = Automorphism(perm=perm, sign=sign)
                if is_octonion_automorphism(aut):
                    auts.append(aut)
    return tuple(auts)


def apply_jordan(aut: Automorphism, a: JMat) -> JMat:
    """Lift ``phi`` entrywise to a 3x3 octonionic matrix."""
    return tuple(
        tuple(apply_octonion(aut, a[i][j]) for j in range(3)) for i in range(3)
    )


def _real(x) -> Octonion:
    return octonion(x, 0, 0, 0, 0, 0, 0, 0)


def _census_idempotents() -> Tuple[JMat, ...]:
    """Three frozen primitive idempotents (pure states) on h_3(O)."""
    v_states = [
        (octonion(1, 0, 0, 0, 0, 0, 0, 0), _ZERO_O, _ZERO_O),
        (_real(Fraction(3, 5)), _real(Fraction(4, 5)), _ZERO_O),
        (_real(Fraction(2, 3)), E[1].scaled(Fraction(2, 3)), E[2].scaled(Fraction(1, 3))),
    ]
    return tuple(outer(v) for v in v_states)


@dataclass(frozen=True)
class AutomorphismCensus:
    group_order: int
    all_are_octonion_automorphisms: bool
    fano_factor: int                       # group_order / 8, should be 168 = |GL(3,2)|
    norm_checks: int
    norm_mismatches: int                   # phi must preserve the octonion norm
    idempotent_checks: int
    idempotent_failures: int               # Phi must map idempotents to idempotents
    born_checks: int
    born_mismatches: int                   # tr(Phi P o Phi Q) must equal tr(P o Q)
    trace_checks: int
    trace_mismatches: int
    jordan_hom_checks: int
    jordan_hom_failures: int               # Phi(A o B) == Phi(A) o Phi(B)


def automorphism_census() -> AutomorphismCensus:
    """Certify Born/idempotent/Jordan invariance under the full automorphism group."""
    group = automorphism_group()
    idempotents = _census_idempotents()
    n = len(idempotents)
    unordered = [(a, b) for a in range(n) for b in range(a + 1, n)]

    base_trace = [trace(p) for p in idempotents]
    base_jp = {(a, b): jordan_product(idempotents[a], idempotents[b]) for a, b in unordered}
    base_form = {(a, b): trace(base_jp[(a, b)]) for a, b in unordered}

    norm_state = octonion(1, 2, 3, 4, 5, 6, 7, 8)
    norm_checks = norm_mismatches = 0
    idem_checks = idem_fail = 0
    born_checks = born_mismatch = 0
    trace_checks = trace_mismatch = 0
    hom_checks = hom_fail = 0

    for aut in group:
        norm_checks += 1
        if apply_octonion(aut, norm_state).norm2() != norm_state.norm2():
            norm_mismatches += 1

        phi = [apply_jordan(aut, p) for p in idempotents]

        for k, pt in enumerate(phi):
            idem_checks += 1
            if not is_primitive_idempotent(pt):
                idem_fail += 1
            trace_checks += 1
            if trace(pt).coords != base_trace[k].coords:
                trace_mismatch += 1

        for a, b in unordered:
            moved_jp = jordan_product(phi[a], phi[b])

            born_checks += 1
            if trace(moved_jp).coords != base_form[(a, b)].coords:
                born_mismatch += 1

            hom_checks += 1
            if not equal(apply_jordan(aut, base_jp[(a, b)]), moved_jp):
                hom_fail += 1

    return AutomorphismCensus(
        group_order=len(group),
        all_are_octonion_automorphisms=all(is_octonion_automorphism(a) for a in group),
        fano_factor=len(group) // 8,
        norm_checks=norm_checks,
        norm_mismatches=norm_mismatches,
        idempotent_checks=idem_checks,
        idempotent_failures=idem_fail,
        born_checks=born_checks,
        born_mismatches=born_mismatch,
        trace_checks=trace_checks,
        trace_mismatches=trace_mismatch,
        jordan_hom_checks=hom_checks,
        jordan_hom_failures=hom_fail,
    )
