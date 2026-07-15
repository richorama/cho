"""Exact amplitude experiments and their representation-change group.

This is the amplitude analogue of ``observer_bootstrap.finite_process``. A
classical experiment was a preparation distribution, a permutation update, and an
effect vector, compared under the permutation relabeling group. Here a
preparation is a pure state amplitude vector, an effect is a projective
measurement direction, and the representation-change group is the exact group of
monomial (generalised permutation) unitaries with fourth-root-of-unity phases.

Permutations sit inside this group as the phase-free monomial matrices, so this
premise strictly extends Gate 00: it adds complex superposition and phase while
keeping every amplitude in Q(i) and every probability an exact rational.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import permutations, product
from typing import Iterator, Tuple

from .gaussian import (
    FOURTH_ROOTS,
    ZERO,
    Gaussian,
    Vector,
    born_probability,
)


@dataclass(frozen=True)
class MonomialUnitary:
    """A unitary sending basis vector ``j`` to ``phase[j]`` times basis ``image[j]``.

    Every row and column carries exactly one unit-modulus entry, so the matrix is
    exactly unitary over Q(i) and preserves the Hermitian inner product exactly.
    """

    image: Tuple[int, ...]
    phases: Tuple[Gaussian, ...]

    def __post_init__(self) -> None:
        dimension = len(self.image)
        if len(self.phases) != dimension:
            raise ValueError("image and phases need one common dimension")
        if tuple(sorted(self.image)) != tuple(range(dimension)):
            raise ValueError("image must be a permutation of the basis indices")
        if any(phase.norm2() != 1 for phase in self.phases):
            raise ValueError("phases must have unit modulus")

    @property
    def dimension(self) -> int:
        return len(self.image)

    def apply(self, vector: Vector) -> Vector:
        """Return ``self @ vector`` exactly."""
        if len(vector) != self.dimension:
            raise ValueError("vector dimension differs from unitary dimension")
        result = [ZERO] * self.dimension
        for source, amplitude in enumerate(vector):
            result[self.image[source]] = self.phases[source] * amplitude
        return tuple(result)


def monomial_group(dimension: int) -> Iterator[MonomialUnitary]:
    """Enumerate every monomial unitary with fourth-root-of-unity phases.

    The group has ``dimension! * 4**dimension`` elements. The permutation subgroup
    (all phases equal to one) recovers exactly the classical relabeling group.
    """
    if dimension < 1:
        raise ValueError("dimension must be positive")
    for image in permutations(range(dimension)):
        for phases in product(FOURTH_ROOTS, repeat=dimension):
            yield MonomialUnitary(tuple(image), phases)


@dataclass(frozen=True)
class AmplitudeExperiment:
    """A pure-state preparation observed by one projective effect direction."""

    preparation: Vector
    effect: Vector

    def __post_init__(self) -> None:
        if len(self.preparation) != len(self.effect):
            raise ValueError("preparation and effect need one common dimension")

    def probability(self) -> Fraction:
        return born_probability(self.effect, self.preparation)


def conjugate_experiment(
    experiment: AmplitudeExperiment, unitary: MonomialUnitary
) -> AmplitudeExperiment:
    """Translate an experiment into a rotated basis via the representation change."""
    return AmplitudeExperiment(
        preparation=unitary.apply(experiment.preparation),
        effect=unitary.apply(experiment.effect),
    )
