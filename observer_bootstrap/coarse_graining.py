"""Exact partitions and autonomous coarse dynamics for finite processes."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from typing import Iterator, Optional, Tuple


Partition = Tuple[int, ...]
DeterministicUpdate = Tuple[int, ...]
StochasticRow = Tuple[Fraction, ...]
StochasticUpdate = Tuple[StochasticRow, ...]


def canonical_partitions(dimension: int) -> Iterator[Partition]:
    """Yield set partitions as restricted-growth strings in canonical order."""
    if dimension < 1:
        raise ValueError("dimension must be positive")

    def extend(prefix: Tuple[int, ...], maximum: int) -> Iterator[Partition]:
        if len(prefix) == dimension:
            yield prefix
            return
        for label in range(maximum + 2):
            yield from extend(prefix + (label,), max(maximum, label))

    yield from extend((0,), 0)


def block_count(partition: Partition) -> int:
    if not partition or partition[0] != 0:
        raise ValueError("partition must be a nonempty restricted-growth string")
    maximum = 0
    for index, label in enumerate(partition):
        if label < 0 or label > maximum + 1:
            raise ValueError("partition must be a restricted-growth string")
        if index and label == maximum + 1:
            maximum = label
    return maximum + 1


def is_nontrivial_partition(partition: Partition) -> bool:
    blocks = block_count(partition)
    return 1 < blocks < len(partition)


def induced_deterministic_update(
    update: DeterministicUpdate, partition: Partition
) -> Optional[DeterministicUpdate]:
    """Return U_B when B U = U_B B, or None when no autonomous law exists."""
    if len(update) != len(partition) or any(
        target < 0 or target >= len(update) for target in update
    ):
        raise ValueError("update and partition need one valid common dimension")
    blocks = block_count(partition)
    coarse_targets = [None] * blocks
    for source, target in enumerate(update):
        source_block = partition[source]
        target_block = partition[target]
        previous = coarse_targets[source_block]
        if previous is not None and previous != target_block:
            return None
        coarse_targets[source_block] = target_block
    return tuple(int(target) for target in coarse_targets)


def induced_stochastic_update(
    update: StochasticUpdate, partition: Partition
) -> Optional[StochasticUpdate]:
    """Exact strong lumpability test and induced row-stochastic update."""
    dimension = len(partition)
    if len(update) != dimension or any(len(row) != dimension for row in update):
        raise ValueError("update and partition need one common dimension")
    if any(sum(row) != 1 or any(value < 0 for value in row) for row in update):
        raise ValueError("every stochastic row must be a probability distribution")

    blocks = block_count(partition)
    coarse_rows = [None] * blocks
    for source, row in enumerate(update):
        coarse_row = tuple(
            sum(row[target] for target in range(dimension) if partition[target] == block)
            for block in range(blocks)
        )
        source_block = partition[source]
        previous = coarse_rows[source_block]
        if previous is not None and previous != coarse_row:
            return None
        coarse_rows[source_block] = coarse_row
    return tuple(coarse_row for coarse_row in coarse_rows if coarse_row is not None)


def weak_compositions(total: int, parts: int) -> Iterator[Tuple[int, ...]]:
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in weak_compositions(total - first, parts - 1):
            yield (first,) + rest


def rational_stochastic_rows(
    dimension: int, denominator: int
) -> Tuple[StochasticRow, ...]:
    if dimension < 1 or denominator < 1:
        raise ValueError("dimension and denominator must be positive")
    return tuple(
        tuple(Fraction(value, denominator) for value in composition)
        for composition in weak_compositions(denominator, dimension)
    )


def deterministic_updates(dimension: int) -> Iterator[DeterministicUpdate]:
    yield from product(range(dimension), repeat=dimension)


def rational_stochastic_updates(
    dimension: int, denominator: int
) -> Iterator[StochasticUpdate]:
    rows = rational_stochastic_rows(dimension, denominator)
    yield from product(rows, repeat=dimension)