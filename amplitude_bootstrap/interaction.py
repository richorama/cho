"""Gate Q09: is any *interacting* amplitude law observer-consistent? (make-or-break)

Every amplitude gate so far shares one honest limitation: the effective structure that
survives coarse-graining is always the *non-interacting* family, exactly as in the
classical campaign. Gate Q06/Q10 sharpen *why* — interaction couples across the erased
boundary — but leave the load-bearing question open: does *any* interacting unitary
admit an autonomous coarse law under two independent blockings? If one did, the amplitude
premise would manufacture an interacting nonclassical law the classical crucible could
not; if none does, observer-consistent amplitude dynamics are provably non-interacting,
and the nonclassical content that survives (Q07 phase) can only ride on non-interacting
dynamics.

This gate answers the question by exact enumeration over a declared family of six
independent blockings of the fixed Q01 ensemble:

* ``traceB`` / ``traceA`` — the two canonical tensor-factor partial traces (Q01, Q04);
* ``cnot`` / ``rcnot`` — rotated bipartitions via CNOT and reverse-CNOT (Q05 style);
* ``swap`` / ``cz`` — two further Clifford-rotated bipartitions.

The result is a clean no-go. Under the two canonical traces the interacting survivor
count is exactly zero. Broadening to all six blockings, every non-interacting unitary is
robustly autonomous (under at least three blockings), while no interacting unitary is
autonomous under more than one *structurally distinct* blocking: the single exception
(the CZ gate) closes only within the CNOT/reverse-CNOT frame pair, a bespoke rotation
that shares one entangling resource, exactly the "one coarse-graining map per rule"
pattern the constitution disallows as evidence. Every interacting law that does close
under any single cut is reversible — the amplitude echo of the classical interaction
obstruction.
"""

from __future__ import annotations

from typing import Callable, Dict, List, NamedTuple, Tuple

from .coarse_graining import (
    _CNOT,
    _CZ,
    _SWAP,
    choi_rank,
    ensemble,
    reduced_channel,
)
from .gaussian import ONE, ZERO
from .interference import transmits_coherence
from .linalg import Matrix, dagger, matmul

# Reverse CNOT: qubit B controls qubit A, |a, b> -> |a xor b, b>.
_RCNOT_PERM: Tuple[int, ...] = (0, 3, 2, 1)
_RCNOT: Matrix = tuple(
    tuple(ONE if c == _RCNOT_PERM[r] else ZERO for c in range(4)) for r in range(4)
)


def _conjugate(unitary: Matrix, rotation: Matrix) -> Matrix:
    return matmul(matmul(rotation, unitary), dagger(rotation))


# The declared family of independent blockings. Each maps a two-qubit unitary to its
# autonomous coarse channel (or None). ``traced`` picks the kept tensor factor; the
# rotated frames conjugate by a fixed Clifford before the plain trace.
BLOCKINGS: Dict[str, Callable[[Matrix], object]] = {
    "traceB": lambda u: reduced_channel(u, 1),
    "traceA": lambda u: reduced_channel(u, 0),
    "cnot": lambda u: reduced_channel(_conjugate(u, _CNOT), 1),
    "rcnot": lambda u: reduced_channel(_conjugate(u, _RCNOT), 1),
    "swap": lambda u: reduced_channel(_conjugate(u, _SWAP), 1),
    "cz": lambda u: reduced_channel(_conjugate(u, _CZ), 1),
}

# The two canonical tensor-factor traces define the make-or-break intersection.
CANONICAL: Tuple[str, str] = ("traceA", "traceB")


class InteractionCensus(NamedTuple):
    ensemble_size: int
    interacting_total: int
    non_interacting_total: int
    # Make-or-break: survivors of the two canonical traces at once.
    canonical_survivors: int
    canonical_interacting: int
    # Broad family, per member: how many blockings it is autonomous under.
    max_blockings_any_interacting: int
    interacting_multi_blocking: int
    min_blockings_any_non_interacting: int
    # Every interacting law that closes under any cut is reversible.
    interacting_autonomous_instances: int
    all_interacting_laws_reversible: bool


def _survived(unitary: Matrix) -> List[str]:
    return [name for name, blocking in BLOCKINGS.items() if blocking(unitary) is not None]


def interaction_census() -> InteractionCensus:
    """Exact survival profile of the ensemble across the six-blocking family."""
    members = ensemble()
    interacting_total = 0
    non_interacting_total = 0
    canonical_survivors = 0
    canonical_interacting = 0
    max_blockings_interacting = 0
    interacting_multi = 0
    min_blockings_local = len(BLOCKINGS) + 1
    interacting_instances = 0
    all_reversible = True

    for tag, unitary in members:
        is_interacting = tag != "local"
        if is_interacting:
            interacting_total += 1
        else:
            non_interacting_total += 1

        survived = _survived(unitary)
        count = len(survived)

        if all(name in survived for name in CANONICAL):
            canonical_survivors += 1
            if is_interacting:
                canonical_interacting += 1

        if is_interacting:
            max_blockings_interacting = max(max_blockings_interacting, count)
            if count >= 2:
                interacting_multi += 1
            for name in survived:
                interacting_instances += 1
                channel = BLOCKINGS[name](unitary)
                if choi_rank(channel) != 1:
                    all_reversible = False
        else:
            min_blockings_local = min(min_blockings_local, count)

    return InteractionCensus(
        ensemble_size=len(members),
        interacting_total=interacting_total,
        non_interacting_total=non_interacting_total,
        canonical_survivors=canonical_survivors,
        canonical_interacting=canonical_interacting,
        max_blockings_any_interacting=max_blockings_interacting,
        interacting_multi_blocking=interacting_multi,
        min_blockings_any_non_interacting=min_blockings_local,
        interacting_autonomous_instances=interacting_instances,
        all_interacting_laws_reversible=all_reversible,
    )


def multi_blocking_interacting_frames() -> Tuple[Tuple[str, Tuple[str, ...]], ...]:
    """Every interacting member autonomous under >= 2 blockings, with its frame set.

    The make-or-break claim is that this list contains only bespoke single-resource
    frames, never two structurally distinct blockings.
    """
    result = []
    for tag, unitary in ensemble():
        if tag == "local":
            continue
        survived = tuple(sorted(_survived(unitary)))
        if len(survived) >= 2:
            result.append((tag, survived))
    return tuple(result)


def non_interacting_survivors_are_nonclassical() -> bool:
    """Every autonomous non-interacting law is reversible and transmits coherence."""
    for tag, unitary in ensemble():
        if tag != "local":
            continue
        for blocking in BLOCKINGS.values():
            channel = blocking(unitary)
            if channel is None:
                continue
            if choi_rank(channel) != 1 or not transmits_coherence(channel):
                return False
    return True
