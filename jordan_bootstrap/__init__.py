"""Octonion campaign: observer-consistency on the last normed division algebra.

This package changes exactly one premise beyond the amplitude campaign: complex
amplitudes over ``Q(i)`` are replaced by octonions over the rationals, the top of
the Cayley-Dickson ladder ``R -> C -> H -> O``. Its gates are the
``tests/test_gate_o*.py`` contracts.
"""

from .octonion import (
    E,
    ONE,
    ZERO,
    UNIT_OCTONIONS,
    Octonion,
    basis,
    cd_mul,
    cd_norm2,
    census_states,
    octonion,
)
from .census import (
    OctonionInvarianceCensus,
    representation_invariance_census,
)
from .frame import (
    FrameConsistencyCensus,
    frame_consistency_census,
    frame_total,
    frames,
    is_orthogonal,
    theorem_witnesses,
)
from .jordan import (
    JordanStateCensus,
    is_jordan_frame,
    is_primitive_idempotent,
    jordan_product,
    jordan_state_census,
    outer,
    trace,
    trace_form,
)

__all__ = [
    "E",
    "ONE",
    "ZERO",
    "UNIT_OCTONIONS",
    "Octonion",
    "basis",
    "cd_mul",
    "cd_norm2",
    "census_states",
    "octonion",
    "OctonionInvarianceCensus",
    "representation_invariance_census",
    "FrameConsistencyCensus",
    "frame_consistency_census",
    "frame_total",
    "frames",
    "is_orthogonal",
    "theorem_witnesses",
    "JordanStateCensus",
    "is_jordan_frame",
    "is_primitive_idempotent",
    "jordan_product",
    "jordan_state_census",
    "outer",
    "trace",
    "trace_form",
]
