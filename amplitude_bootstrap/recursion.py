"""Gate Q05: a structurally different coarse-graining and parameter contraction.

Gate Q04 used two tensor-factor traces. Level 2 also needs a structurally different
blocking and evidence that recursive coarse-graining does not grow the surviving
parameter count. This gate supplies both.

A rotated factorisation coarse-grains in a different system/environment split: apply
a fixed non-local unitary ``W`` (here CNOT, a Clifford over Q(i)), then trace out a
qubit. Autonomy of ``U`` under this map is exactly autonomy of ``W U W^dagger`` under
the plain trace, so it probes a genuinely different bipartition. On the fixed
ensemble it keeps a different set of survivors, confirming inequivalence.

Parameter contraction: the non-interacting survivors ``a kron b`` all reduce to the
single-qubit conjugation ``E(sigma) = a sigma a^dagger``, forgetting the environment
factor ``b`` entirely. The 36 survivors collapse to 6 distinct effective channels,
and these compose within the reversible single-qubit family — recursion stays in a
strictly smaller, non-growing parameter class.
"""

from __future__ import annotations

from typing import FrozenSet, NamedTuple, Tuple

from .coarse_graining import (
    ONE_QUBIT_GATES,
    _CNOT,
    _I2,
    choi_rank,
    ensemble,
    reduced_channel,
)
from .interference import transmits_coherence
from .linalg import Matrix, dagger, kron, matmul

# A fixed non-local Clifford defining the rotated bipartition. CNOT is self-inverse.
ROTATION: Matrix = _CNOT


def _conjugate(unitary: Matrix, rotation: Matrix) -> Matrix:
    return matmul(matmul(rotation, unitary), dagger(rotation))


def rotated_reduced_channel(unitary: Matrix, rotation: Matrix = ROTATION):
    """Autonomous channel under the rotated factorisation, or None."""
    return reduced_channel(_conjugate(unitary, rotation))


def _survivor_indices(rotation: Matrix = None) -> FrozenSet[int]:
    survivors = set()
    for index, (_, unitary) in enumerate(ensemble()):
        channel = (
            reduced_channel(unitary)
            if rotation is None
            else rotated_reduced_channel(unitary, rotation)
        )
        if channel is not None:
            survivors.add(index)
    return frozenset(survivors)


class SurvivorComparison(NamedTuple):
    computational: int
    rotated: int
    shared: int
    rotated_only: int


def survivor_comparison() -> SurvivorComparison:
    """Compare plain-trace and rotated-factorisation survivors on the ensemble."""
    computational = _survivor_indices(None)
    rotated = _survivor_indices(ROTATION)
    return SurvivorComparison(
        computational=len(computational),
        rotated=len(rotated),
        shared=len(computational & rotated),
        rotated_only=len(rotated - computational),
    )


def rotated_survivors_all_reversible() -> bool:
    """Every rotated-factorisation survivor induces a reversible, nonclassical law."""
    for _, unitary in ensemble():
        channel = rotated_reduced_channel(unitary)
        if channel is None:
            continue
        if choi_rank(channel) != 1 or not transmits_coherence(channel):
            return False
    return True


class ContractionResult(NamedTuple):
    local_survivors: int
    distinct_effective_channels: int
    environment_is_forgotten: bool


def effective_channel_contraction() -> ContractionResult:
    """The non-interacting survivors collapse to few environment-free channels."""
    channels = set()
    environment_is_forgotten = True
    for a in ONE_QUBIT_GATES:
        reference = None
        for b in ONE_QUBIT_GATES:
            channel = reduced_channel(kron(a, b))
            channels.add(channel)
            if reference is None:
                reference = channel
            elif channel != reference:
                environment_is_forgotten = False
    return ContractionResult(
        local_survivors=len(ONE_QUBIT_GATES) ** 2,
        distinct_effective_channels=len(channels),
        environment_is_forgotten=environment_is_forgotten,
    )


def composition_is_closed_and_reversible() -> bool:
    """Effective channels compose to ``conj(a2 a1)`` and stay Choi rank one."""
    for a1 in ONE_QUBIT_GATES:
        first = reduced_channel(kron(a1, _I2))
        for a2 in ONE_QUBIT_GATES:
            second = reduced_channel(kron(a2, _I2))
            composed = matmul(second, first)
            direct = reduced_channel(kron(matmul(a2, a1), _I2))
            if composed != direct or choi_rank(composed) != 1:
                return False
    return True
