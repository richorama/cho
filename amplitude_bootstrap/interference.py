"""Gate Q03: interference as an unselected holdout.

Nonclassicality is never part of the selection objective. Here it is measured on
the already-frozen effective channels of Gates Q01 and Q02, two ways:

* A configuration-independent witness ``transmits_coherence``: the channel carries
  a computational-basis coherence to a nonzero output coherence. No classical
  stochastic channel on the two basis states can do this, so a positive result
  certifies a nonclassical effective law.
* An operational Mach-Zehnder ``interference_visibility``: the exact gap between a
  coherent two-path recombination and a which-path measurement. A classical
  which-path model forces this gap to zero.

The central finding is an exact equivalence for this family: an effective channel
transmits coherence if and only if it is reversible (Choi rank one). Decoherence
and the loss of interference coincide exactly, and both are induced precisely by
interacting microscopic dynamics.
"""

from __future__ import annotations

from typing import NamedTuple, Tuple

from .coarse_graining import (
    ENVIRONMENTS,
    _R,
    _apply_channel,
    _basis_operator,
    choi_rank,
    ensemble,
    fixed_environment_channel,
)
from .gaussian import ONE, ZERO, Gaussian
from .linalg import Matrix, dagger, matmul

# The beam splitter of the interferometer: an exact rational (Pythagorean) rotation.
_BEAM_SPLITTER: Matrix = _R
_INPUT: Matrix = ((ONE, ZERO), (ZERO, ZERO))

# A fully dephasing channel: the canonical classical control, in vec form.
DEPHASING_CHANNEL: Matrix = (
    (ONE, ZERO, ZERO, ZERO),
    (ZERO, ZERO, ZERO, ZERO),
    (ZERO, ZERO, ZERO, ZERO),
    (ZERO, ZERO, ZERO, ONE),
)


def _dephase(operator: Matrix) -> Matrix:
    return ((operator[0][0], ZERO), (ZERO, operator[1][1]))


def transmits_coherence(channel: Matrix) -> bool:
    """Configuration-independent nonclassicality witness for a qubit channel."""
    image = _apply_channel(channel, _basis_operator(2, 0, 1))
    return (not image[0][1].is_zero()) or (not image[1][0].is_zero())


def interference_visibility(channel: Matrix) -> Gaussian:
    """Exact Mach-Zehnder gap ``p(both paths) - p(which-path)``.

    The effective channel sits between two beam splitters. The which-path variant
    removes the input path coherence before the channel. A classical which-path
    account predicts an identical outcome distribution, so a nonzero result is a
    direct interference signature.
    """
    splitter = _BEAM_SPLITTER
    splitter_dagger = dagger(splitter)
    prepared = matmul(matmul(splitter, _INPUT), splitter_dagger)

    both = matmul(
        matmul(splitter, _apply_channel(channel, prepared)), splitter_dagger
    )
    which_path = matmul(
        matmul(splitter, _apply_channel(channel, _dephase(prepared))), splitter_dagger
    )
    return both[0][0] - which_path[0][0]


class ClassicalityRow(NamedTuple):
    environment: str
    nonclassical: int
    classical: int
    nonclassical_local: int
    nonclassical_entangling: int


def classicality_census(traced: int = 1) -> Tuple[ClassicalityRow, ...]:
    """Per-environment tally of coherence-transmitting (nonclassical) channels."""
    members = ensemble()
    rows = []
    for name, environment in ENVIRONMENTS:
        nonclassical = 0
        classical = 0
        nonclassical_local = 0
        nonclassical_entangling = 0
        for tag, unitary in members:
            channel = fixed_environment_channel(unitary, environment, traced)
            if transmits_coherence(channel):
                nonclassical += 1
                if tag == "local":
                    nonclassical_local += 1
                else:
                    nonclassical_entangling += 1
            else:
                classical += 1
        rows.append(
            ClassicalityRow(
                environment=name,
                nonclassical=nonclassical,
                classical=classical,
                nonclassical_local=nonclassical_local,
                nonclassical_entangling=nonclassical_entangling,
            )
        )
    return tuple(rows)


def coherence_matches_reversibility(traced: int = 1) -> bool:
    """Exact equivalence: transmits coherence iff reversible, over every case."""
    for _, environment in ENVIRONMENTS:
        for _, unitary in ensemble():
            channel = fixed_environment_channel(unitary, environment, traced)
            if transmits_coherence(channel) != (choi_rank(channel) == 1):
                return False
    return True
