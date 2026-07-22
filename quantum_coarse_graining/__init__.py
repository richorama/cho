"""Exact finite-dimensional tools for quantum coarse-graining."""

from .autonomy import (
    closure_defect,
    linear_operator_entanglement,
    normalized_closure_defect,
    operator_entanglement_identity_holds,
)
from .exact import Gaussian, I, ONE, ZERO
from .ising import (
    diamond_autonomy_defect,
    hidden_correlation_witness_holds,
    ising_decomposition_holds,
    ising_theorem_certificate,
    ising_unitary,
    witness_trace_norm_certificate,
)

__all__ = [
    "Gaussian",
    "I",
    "ONE",
    "ZERO",
    "closure_defect",
    "linear_operator_entanglement",
    "normalized_closure_defect",
    "operator_entanglement_identity_holds",
    "diamond_autonomy_defect",
    "hidden_correlation_witness_holds",
    "ising_decomposition_holds",
    "ising_theorem_certificate",
    "ising_unitary",
    "witness_trace_norm_certificate",
]
