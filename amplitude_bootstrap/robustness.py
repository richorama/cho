"""Gate Q04: robustness under a second, inequivalent coarse-graining.

Every result of Gates Q01 to Q03 used a single coarse-graining: trace out qubit B.
Before any feature may be called resolution independent it must survive a second,
independently specified coarse-graining. Here that is tracing out qubit A instead.
The two are genuinely inequivalent because the ensemble is A/B asymmetric (for
example CNOT uses qubit A as control), so this is a real test rather than a
relabeling.

The gate separates robust conclusions from coarse-graining artefacts:

* Robust: only non-interacting product unitaries admit an autonomous coarse law;
  such unitaries are always reversible and coherence preserving; all decoherence
  and all loss of coherence require interaction; and reversibility always implies a
  nonclassical (coherence-transmitting) effective law.
* Artefact: the exact equivalence "coherence transmitted iff reversible" holds only
  for the trace-B coarse-graining. Under trace-A there are irreversible channels
  that still transmit coherence (partial decoherence), so "decoherence equals total
  loss of interference" is specific to the first coarse-graining, not fundamental.
"""

from __future__ import annotations

from typing import NamedTuple, Tuple

from .coarse_graining import (
    ENVIRONMENTS,
    choi_rank,
    ensemble,
    fixed_environment_channel,
    reduced_channel,
)
from .interference import transmits_coherence

# The two independently specified coarse-grainings, by traced-out qubit.
COARSE_GRAININGS: Tuple[Tuple[str, int], ...] = (("trace_b", 1), ("trace_a", 0))


def reversibility_implies_nonclassicality(traced: int) -> bool:
    """A reversible effective law always transmits coherence, for this map."""
    for _, environment in ENVIRONMENTS:
        for _, unitary in ensemble():
            channel = fixed_environment_channel(unitary, environment, traced)
            if choi_rank(channel) == 1 and not transmits_coherence(channel):
                return False
    return True


def irreversible_but_coherent_count(traced: int) -> int:
    """Number of irreversible channels that still transmit coherence, for this map."""
    count = 0
    for _, environment in ENVIRONMENTS:
        for _, unitary in ensemble():
            channel = fixed_environment_channel(unitary, environment, traced)
            if choi_rank(channel) != 1 and transmits_coherence(channel):
                count += 1
    return count


def noninteracting_dynamics_is_invariant(traced: int) -> bool:
    """Local product unitaries stay autonomous, reversible and nonclassical."""
    for tag, unitary in ensemble():
        if tag != "local":
            continue
        if reduced_channel(unitary, traced) is None:
            return False
        for _, environment in ENVIRONMENTS:
            channel = fixed_environment_channel(unitary, environment, traced)
            if choi_rank(channel) != 1 or not transmits_coherence(channel):
                return False
    return True


def decoherence_requires_interaction(traced: int) -> bool:
    """No non-interacting unitary ever decoheres, under any environment."""
    for tag, unitary in ensemble():
        if tag != "local":
            continue
        for _, environment in ENVIRONMENTS:
            channel = fixed_environment_channel(unitary, environment, traced)
            if choi_rank(channel) != 1:
                return False
    return True


class RobustnessRow(NamedTuple):
    coarse_graining: str
    autonomous_survivors: int
    reversibility_implies_nonclassicality: bool
    noninteracting_invariant: bool
    decoherence_requires_interaction: bool
    equivalence_holds: bool
    irreversible_but_coherent: int


def robustness_summary() -> Tuple[RobustnessRow, ...]:
    """Compare the two coarse-grainings across the robust and artefact properties."""
    from .interference import coherence_matches_reversibility

    rows = []
    for name, traced in COARSE_GRAININGS:
        survivors = sum(
            1 for _, unitary in ensemble() if reduced_channel(unitary, traced) is not None
        )
        rows.append(
            RobustnessRow(
                coarse_graining=name,
                autonomous_survivors=survivors,
                reversibility_implies_nonclassicality=(
                    reversibility_implies_nonclassicality(traced)
                ),
                noninteracting_invariant=noninteracting_dynamics_is_invariant(traced),
                decoherence_requires_interaction=decoherence_requires_interaction(traced),
                equivalence_holds=coherence_matches_reversibility(traced),
                irreversible_but_coherent=irreversible_but_coherent_count(traced),
            )
        )
    return tuple(rows)
