"""Exact finite-dimensional tools for quantum coarse-graining."""

from .autonomy import (
    closure_defect,
    linear_operator_entanglement,
    normalized_closure_defect,
    operator_entanglement_identity_holds,
)
from .cartan import (
    cartan_effective_channel,
    cartan_effective_channel_is_cptp,
    cartan_joint_pauli_covariance_certificate,
    cartan_pauli_coefficients,
    cartan_pauli_weights,
    cartan_symmetry_certificate,
    cartan_unitary,
    cartan_visible_sector_certificate,
)
from .exact import Gaussian, I, ONE, ZERO
from .ising import (
    diamond_autonomy_defect,
    flagged_state_witness_certificate,
    hidden_correlation_witness_holds,
    ising_decomposition_holds,
    ising_theorem_certificate,
    ising_unitary,
    witness_trace_norm_certificate,
)
from .swap import (
    swap_ancilla_witness_certificate,
    swap_decomposition_holds,
    swap_diamond_autonomy_defect,
    swap_theorem_certificate,
    swap_unitary,
)

__all__ = [
    "Gaussian",
    "I",
    "ONE",
    "ZERO",
    "closure_defect",
    "cartan_effective_channel",
    "cartan_effective_channel_is_cptp",
    "cartan_joint_pauli_covariance_certificate",
    "cartan_pauli_coefficients",
    "cartan_pauli_weights",
    "cartan_symmetry_certificate",
    "cartan_unitary",
    "cartan_visible_sector_certificate",
    "linear_operator_entanglement",
    "normalized_closure_defect",
    "operator_entanglement_identity_holds",
    "diamond_autonomy_defect",
    "flagged_state_witness_certificate",
    "hidden_correlation_witness_holds",
    "ising_decomposition_holds",
    "ising_theorem_certificate",
    "ising_unitary",
    "witness_trace_norm_certificate",
    "swap_ancilla_witness_certificate",
    "swap_decomposition_holds",
    "swap_diamond_autonomy_defect",
    "swap_theorem_certificate",
    "swap_unitary",
]
