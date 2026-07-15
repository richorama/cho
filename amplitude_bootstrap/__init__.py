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
from .robustness import COARSE_GRAININGS, robustness_summary
from .recursion import (
    ROTATION,
    composition_is_closed_and_reversible,
    effective_channel_contraction,
    rotated_reduced_channel,
    rotated_survivors_all_reversible,
    survivor_comparison,
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
    "COARSE_GRAININGS",
    "robustness_summary",
    "ROTATION",
    "composition_is_closed_and_reversible",
    "effective_channel_contraction",
    "rotated_reduced_channel",
    "rotated_survivors_all_reversible",
    "survivor_comparison",
    "Gaussian",
    "born_probability",
]
