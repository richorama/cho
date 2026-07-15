"""Pure exact censuses used by the observer-consistency test gates."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import permutations, product
from typing import Dict, NamedTuple, Tuple

from .coarse_graining import (
    block_count,
    canonical_partitions,
    deterministic_updates,
    induced_deterministic_update,
    induced_stochastic_update,
    is_nontrivial_partition,
    rational_stochastic_updates,
)
from .finite_process import (
    conjugate_permutation,
    relabel_vector,
)


class RepresentationCensus(NamedTuple):
    exact_checks: int
    operational_mismatches: int
    label_discrepancies: int


class CoarseCensusRow(NamedTuple):
    partitions: int
    pairs: int
    survivors: int


def binary_effect(bits: Tuple[int, ...]) -> Tuple[Fraction, ...]:
    return tuple(Fraction(value) for value in bits)


def representation_invariance_census(
    maximum_dimension: int = 5,
) -> RepresentationCensus:
    exact_checks = 0
    operational_mismatches = 0
    label_discrepancies = 0
    for dimension in range(2, maximum_dimension + 1):
        all_permutations = tuple(permutations(range(dimension)))
        effects = tuple(
            binary_effect(bits) for bits in product((0, 1), repeat=dimension)
        )
        translated_effects = {
            relabeling: tuple(
                relabel_vector(effect, relabeling) for effect in effects
            )
            for relabeling in all_permutations
        }
        for update in all_permutations:
            for relabeling in all_permutations:
                translated_update = conjugate_permutation(update, relabeling)
                for state in range(dimension):
                    translated_state = relabeling[state]
                    for effect, translated_effect in zip(
                        effects, translated_effects[relabeling]
                    ):
                        exact_checks += 1
                        probability = effect[update[state]]
                        translated_probability = translated_effect[
                            translated_update[translated_state]
                        ]
                        if translated_probability != probability:
                            operational_mismatches += 1
                        if translated_state != state:
                            label_discrepancies += 1
    return RepresentationCensus(
        exact_checks, operational_mismatches, label_discrepancies
    )


def block_sizes(partition: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(partition.count(block) for block in range(block_count(partition)))


def expected_deterministic_survivors(partition: Tuple[int, ...]) -> int:
    """Independent count: product_i sum_j |block_j|^|block_i|."""
    sizes = block_sizes(partition)
    result = 1
    for source_size in sizes:
        result *= sum(target_size ** source_size for target_size in sizes)
    return result


def deterministic_coarse_census(
    maximum_dimension: int = 5,
) -> Tuple[Dict[int, CoarseCensusRow], int]:
    rows = {}
    formula_mismatches = 0
    for dimension in range(2, maximum_dimension + 1):
        partitions = tuple(
            partition
            for partition in canonical_partitions(dimension)
            if is_nontrivial_partition(partition)
        )
        pair_count = 0
        survivor_count = 0
        survivor_by_partition = Counter()
        for update in deterministic_updates(dimension):
            for partition in partitions:
                pair_count += 1
                if induced_deterministic_update(update, partition) is not None:
                    survivor_count += 1
                    survivor_by_partition[partition] += 1
        formula_mismatches += sum(
            survivor_by_partition[partition]
            != expected_deterministic_survivors(partition)
            for partition in partitions
        )
        rows[dimension] = CoarseCensusRow(
            len(partitions), pair_count, survivor_count
        )
    return rows, formula_mismatches


def stochastic_coarse_census(
    maximum_dimension: int = 4, denominator: int = 2
) -> Dict[int, CoarseCensusRow]:
    rows = {}
    for dimension in range(2, maximum_dimension + 1):
        partitions = tuple(
            partition
            for partition in canonical_partitions(dimension)
            if is_nontrivial_partition(partition)
        )
        pair_count = 0
        survivor_count = 0
        for update in rational_stochastic_updates(dimension, denominator):
            for partition in partitions:
                pair_count += 1
                if induced_stochastic_update(update, partition) is not None:
                    survivor_count += 1
        rows[dimension] = CoarseCensusRow(
            len(partitions), pair_count, survivor_count
        )
    return rows