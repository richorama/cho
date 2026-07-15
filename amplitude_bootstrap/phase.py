"""Gate Q07: an irreducible complex phase survives the recursion (Level 3).

Gate Q06 showed that recursive spatial coarse-graining *filters out* interaction: no
coupling across an erased boundary survives. Level 3 asks the opposite question — is
there an unselected nonclassical structure that the recursion cannot remove?

The candidate is the irreducible complex phase: the departure from real-amplitude
dynamics. A channel is realisable with real amplitudes exactly when its superoperator
(the exact vec-matrix over Q(i)) has zero imaginary part. That property is invariant
under any real change of basis, because conjugating by a real matrix maps the imaginary
part to ``R B R^{-1}``, which vanishes only if ``B`` already vanishes. So a channel whose
superoperator carries a nonzero imaginary entry is genuinely complex in a
basis-independent sense — no real recombination or real coarse-graining can launder the
``i`` away.

The phase gate ``S = diag(1, i)`` produces such a channel, and it is a legal
non-interacting factor, so it survives the three-qubit recursion to the bottom and
survives the rotated blocking as well. The complex phase was never rewarded by any
objective, yet it is exactly the nonclassical content the recursion preserves. That is
Level-3 evidence: an unselected complex structure survives multiple blockings robustly.
"""

from __future__ import annotations

from typing import NamedTuple, Tuple

from .coarse_graining import (
    _I2,
    _R,
    _S,
    _X,
    _Z,
    ensemble,
    kron,
    reduced_channel,
)
from .linalg import Matrix, dagger, matmul
from .recursion import rotated_reduced_channel
from .spatial import (
    _CHAIN_QUBITS,
    _channel_action,
    _conjugation,
    chain_ensemble,
    reduce_map,
)

# Real-orthogonal single-qubit gates (real-amplitude dynamics) versus the phase gate.
REAL_GATES: Tuple[Matrix, ...] = (_I2, _X, _Z, _R, matmul(_X, _R))
COMPLEX_GATE: Matrix = _S


def is_genuinely_complex(channel: Matrix) -> bool:
    """True iff the channel superoperator has a nonzero imaginary entry."""
    return any(value.imag != 0 for row in channel for value in row)


def conjugation_channel(unitary: Matrix) -> Matrix:
    """The single-qubit channel ``sigma -> u sigma u^dagger`` as a 4x4 vec-matrix."""
    return reduced_channel(kron(unitary, _I2))


def real_gates_are_real_superoperators() -> bool:
    """Every real-amplitude gate induces a real (imaginary-free) channel."""
    return all(
        not is_genuinely_complex(conjugation_channel(gate)) for gate in REAL_GATES
    )


def phase_gate_is_genuinely_complex() -> bool:
    """The phase gate induces a genuinely complex channel."""
    return is_genuinely_complex(conjugation_channel(COMPLEX_GATE))


def _conjugate_channel(channel: Matrix, basis: Matrix) -> Matrix:
    forward = conjugation_channel(basis)
    backward = conjugation_channel(dagger(basis))
    return matmul(matmul(forward, channel), backward)


def witness_invariant_under_real_basis_change() -> bool:
    """No real change of coarse basis removes the phase, nor manufactures one."""
    complex_channel = conjugation_channel(COMPLEX_GATE)
    real_channel = conjugation_channel(_I2)
    for basis in (_X, _R, _Z):
        if not is_genuinely_complex(_conjugate_channel(complex_channel, basis)):
            return False
        if is_genuinely_complex(_conjugate_channel(real_channel, basis)):
            return False
    return True


class PhaseSurvival(NamedTuple):
    distinct_level1: int
    complex_level1: int
    distinct_level2: int
    complex_level2: int


def complex_phase_survives_recursion() -> PhaseSurvival:
    """Count genuinely complex channels among the distinct survivors at each level."""
    level1 = set()
    level2 = set()
    for member in chain_ensemble():
        first = reduce_map(_conjugation(member.unitary), _CHAIN_QUBITS, 2)
        if first is None:
            continue
        level1.add(first)
        second = reduce_map(_channel_action(first, 4), 2, 1)
        if second is None:
            continue
        level2.add(second)
    return PhaseSurvival(
        distinct_level1=len(level1),
        complex_level1=sum(1 for c in level1 if is_genuinely_complex(c)),
        distinct_level2=len(level2),
        complex_level2=sum(1 for c in level2 if is_genuinely_complex(c)),
    )


def complex_phase_survives_rotated_blocking() -> int:
    """Distinct genuinely complex survivors under the rotated (CNOT) blocking."""
    complex_survivors = set()
    for _, unitary in ensemble():
        channel = rotated_reduced_channel(unitary)
        if channel is not None and is_genuinely_complex(channel):
            complex_survivors.add(channel)
    return len(complex_survivors)
