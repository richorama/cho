"""Pure exact censuses for the amplitude observer-consistency gates.

Every scientific claim about the amplitude premise is owned by a test in
``tests/``; this module only computes finite exact quantities.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import NamedTuple, Tuple

from .amplitude_process import monomial_group
from .gaussian import Gaussian, Vector, born_probability

# Alphabet of exact amplitudes used to build census state vectors: 0, 1, and i.
# It contains genuine superposition and a nontrivial complex phase, so the census
# exercises interference rather than mere classical relabeling.
_ALPHABET: Tuple[Gaussian, ...] = (
    Gaussian(Fraction(0), Fraction(0)),
    Gaussian(Fraction(1), Fraction(0)),
    Gaussian(Fraction(0), Fraction(1)),
)


class AmplitudeRepresentationCensus(NamedTuple):
    exact_checks: int
    operational_mismatches: int
    basis_discrepancies: int


def census_state_vectors(dimension: int) -> Tuple[Vector, ...]:
    """Every nonzero vector over the amplitude alphabet ``{0, 1, i}``."""
    if dimension < 1:
        raise ValueError("dimension must be positive")
    vectors = []
    for entries in product(_ALPHABET, repeat=dimension):
        if any(not amplitude.is_zero() for amplitude in entries):
            vectors.append(tuple(entries))
    return tuple(vectors)


def _basis_readout(state: Vector) -> Fraction:
    """A basis-dependent diagnostic: probability of the first basis outcome."""
    effect = tuple(
        Gaussian(Fraction(1 if index == 0 else 0), Fraction(0))
        for index in range(len(state))
    )
    return born_probability(effect, state)


def representation_invariance_census(
    dimensions: Tuple[int, ...] = (2, 3),
) -> AmplitudeRepresentationCensus:
    """Exhaustively test Born-probability invariance under the monomial group.

    For every dimension, every monomial unitary, and every ordered pair of census
    state vectors used as effect and state, the operational Born probability must
    be exactly preserved. The basis readout is a deliberately basis-sensitive
    control that must change under some representation changes.
    """
    exact_checks = 0
    operational_mismatches = 0
    basis_discrepancies = 0

    for dimension in dimensions:
        states = census_state_vectors(dimension)
        base_probabilities = {
            (effect_index, state_index): born_probability(effect, state)
            for effect_index, effect in enumerate(states)
            for state_index, state in enumerate(states)
        }
        base_readouts = tuple(_basis_readout(state) for state in states)

        for unitary in monomial_group(dimension):
            rotated = tuple(unitary.apply(state) for state in states)
            for effect_index, effect in enumerate(rotated):
                if _basis_readout(effect) != base_readouts[effect_index]:
                    basis_discrepancies += 1
                for state_index, state in enumerate(rotated):
                    exact_checks += 1
                    if (
                        born_probability(effect, state)
                        != base_probabilities[(effect_index, state_index)]
                    ):
                        operational_mismatches += 1

    return AmplitudeRepresentationCensus(
        exact_checks=exact_checks,
        operational_mismatches=operational_mismatches,
        basis_discrepancies=basis_discrepancies,
    )
