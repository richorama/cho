"""Exact amplitude experiments for the observer-consistency pivot campaign."""

from .amplitude_process import (
    AmplitudeExperiment,
    MonomialUnitary,
    conjugate_experiment,
    monomial_group,
)
from .coarse_graining import (
    choi_rank,
    channel_preserves_trace,
    environment_decoherence_census,
    fixed_environment_channel,
    partial_trace_b,
    reduced_channel,
    reduced_dynamics_census,
)
from .gaussian import Gaussian, born_probability
from .interference import (
    classicality_census,
    coherence_matches_reversibility,
    interference_visibility,
    transmits_coherence,
)

__all__ = [
    "AmplitudeExperiment",
    "MonomialUnitary",
    "conjugate_experiment",
    "monomial_group",
    "choi_rank",
    "channel_preserves_trace",
    "environment_decoherence_census",
    "fixed_environment_channel",
    "partial_trace_b",
    "reduced_channel",
    "reduced_dynamics_census",
    "classicality_census",
    "coherence_matches_reversibility",
    "interference_visibility",
    "transmits_coherence",
    "Gaussian",
    "born_probability",
]
