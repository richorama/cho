"""Exact finite preparations, reversible updates, and measurement effects."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Tuple


Vector = Tuple[Fraction, ...]
Permutation = Tuple[int, ...]


def validate_permutation(permutation: Permutation) -> None:
    if tuple(sorted(permutation)) != tuple(range(len(permutation))):
        raise ValueError("permutation must contain every state index exactly once")


def inverse_permutation(permutation: Permutation) -> Permutation:
    validate_permutation(permutation)
    inverse = [0] * len(permutation)
    for source, target in enumerate(permutation):
        inverse[target] = source
    return tuple(inverse)


def relabel_vector(vector: Vector, relabeling: Permutation) -> Vector:
    """Move the value at old index i to new index relabeling[i]."""
    validate_permutation(relabeling)
    if len(vector) != len(relabeling):
        raise ValueError("vector and relabeling dimensions differ")
    result = [Fraction(0)] * len(vector)
    for old_index, new_index in enumerate(relabeling):
        result[new_index] = vector[old_index]
    return tuple(result)


def conjugate_permutation(
    update: Permutation, relabeling: Permutation
) -> Permutation:
    """Return r composed with update composed with inverse(r)."""
    validate_permutation(update)
    validate_permutation(relabeling)
    if len(update) != len(relabeling):
        raise ValueError("update and relabeling dimensions differ")
    inverse = inverse_permutation(relabeling)
    return tuple(
        relabeling[update[inverse[new_source]]]
        for new_source in range(len(update))
    )


@dataclass(frozen=True)
class FiniteExperiment:
    preparation: Vector
    update: Permutation
    effect: Vector

    def __post_init__(self) -> None:
        dimension = len(self.preparation)
        if dimension == 0 or len(self.update) != dimension or len(self.effect) != dimension:
            raise ValueError("preparation, update, and effect need one common dimension")
        validate_permutation(self.update)
        if sum(self.preparation) != 1 or any(value < 0 for value in self.preparation):
            raise ValueError("preparation must be a probability distribution")
        if any(value < 0 or value > 1 for value in self.effect):
            raise ValueError("effect values must lie in [0,1]")

    def probability(self) -> Fraction:
        return sum(
            self.preparation[source] * self.effect[self.update[source]]
            for source in range(len(self.update))
        )


def conjugate_experiment(
    experiment: FiniteExperiment, relabeling: Permutation
) -> FiniteExperiment:
    return FiniteExperiment(
        preparation=relabel_vector(experiment.preparation, relabeling),
        update=conjugate_permutation(experiment.update, relabeling),
        effect=relabel_vector(experiment.effect, relabeling),
    )