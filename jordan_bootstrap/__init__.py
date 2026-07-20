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
]
