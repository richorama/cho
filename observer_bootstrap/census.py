"""Pure exact censuses used by the observer-consistency test gates."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import permutations, product
from typing import Callable, Dict, NamedTuple, Optional, Tuple, TypeVar

from .coarse_graining import (
    block_count,
    canonical_deterministic_law,
    canonical_partitions,
    canonical_stochastic_law,
    deterministic_updates,
    induced_deterministic_update,
    induced_stochastic_update,
    is_nontrivial_partition,
    partition_shape,
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


class RobustnessCensus(NamedTuple):
    total_rules: int
    weak_multi_shape: int
    universal_lumpability: int
    shape_compatible_laws: int


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


Update = TypeVar("Update")
Law = TypeVar("Law")


def _robustness_status(
    update: Update,
    partitions_by_shape: Dict[Tuple[int, ...], Tuple[Tuple[int, ...], ...]],
    induce: Callable[[Update, Tuple[int, ...]], Optional[Law]],
    canonicalize: Callable[[Law], Law],
) -> Tuple[bool, bool, bool]:
    laws_by_shape = {
        shape: tuple(induce(update, partition) for partition in partitions)
        for shape, partitions in partitions_by_shape.items()
    }
    weak_multi_shape = sum(
        any(law is not None for law in laws) for laws in laws_by_shape.values()
    ) >= 2
    universal = all(
        all(law is not None for law in laws) for laws in laws_by_shape.values()
    )
    compatible = universal and all(
        len({canonicalize(law) for law in laws if law is not None}) == 1
        for laws in laws_by_shape.values()
    )
    return weak_multi_shape, universal, compatible


def partitions_grouped_by_shape(
    dimension: int,
) -> Dict[Tuple[int, ...], Tuple[Tuple[int, ...], ...]]:
    result = {}
    for partition in canonical_partitions(dimension):
        if not is_nontrivial_partition(partition):
            continue
        shape = partition_shape(partition)
        result.setdefault(shape, []).append(partition)
    return {shape: tuple(partitions) for shape, partitions in result.items()}


def deterministic_robustness_census(
    dimension: int,
) -> Tuple[
    RobustnessCensus,
    Tuple[Tuple[int, ...], ...],
    Tuple[Tuple[int, ...], ...],
]:
    grouped = partitions_grouped_by_shape(dimension)
    weak = universal = compatible = 0
    universal_updates = []
    compatible_updates = []
    total = 0
    for update in deterministic_updates(dimension):
        total += 1
        status = _robustness_status(
            update,
            grouped,
            induced_deterministic_update,
            canonical_deterministic_law,
        )
        weak += status[0]
        universal += status[1]
        compatible += status[2]
        if status[1]:
            universal_updates.append(update)
        if status[2]:
            compatible_updates.append(update)
    return (
        RobustnessCensus(total, weak, universal, compatible),
        tuple(universal_updates),
        tuple(compatible_updates),
    )


def stochastic_robustness_census(
    dimension: int, denominator: int = 2
) -> Tuple[
    RobustnessCensus,
    Tuple[Tuple[Tuple[Fraction, ...], ...], ...],
    Tuple[Tuple[Tuple[Fraction, ...], ...], ...],
]:
    grouped = partitions_grouped_by_shape(dimension)
    weak = universal = compatible = 0
    universal_updates = []
    compatible_updates = []
    total = 0
    for update in rational_stochastic_updates(dimension, denominator):
        total += 1
        status = _robustness_status(
            update,
            grouped,
            induced_stochastic_update,
            canonical_stochastic_law,
        )
        weak += status[0]
        universal += status[1]
        compatible += status[2]
        if status[1]:
            universal_updates.append(update)
        if status[2]:
            compatible_updates.append(update)
    return (
        RobustnessCensus(total, weak, universal, compatible),
        tuple(universal_updates),
        tuple(compatible_updates),
    )


def is_constant_or_identity(update: Tuple[int, ...]) -> bool:
    return update == tuple(range(len(update))) or len(set(update)) == 1


def is_universally_lumpable_stochastic(
    update: Tuple[Tuple[Fraction, ...], ...]
) -> bool:
    """Characterize P=aI+1c^T by column-constant off-diagonal entries."""
    dimension = len(update)
    return all(
        len({update[row][column] for row in range(dimension) if row != column})
        == 1
        for column in range(dimension)
    )


def is_single_target_reset_mixture(
    update: Tuple[Tuple[Fraction, ...], ...]
) -> bool:
    dimension = len(update)
    identity = tuple(
        tuple(Fraction(row == column) for column in range(dimension))
        for row in range(dimension)
    )
    if update == identity:
        return True
    for target in range(dimension):
        reset = tuple(
            tuple(Fraction(column == target) for column in range(dimension))
            for _ in range(dimension)
        )
        for keep in (Fraction(0), Fraction(1, 2)):
            candidate = tuple(
                tuple(
                    keep * identity[row][column]
                    + (1 - keep) * reset[row][column]
                    for column in range(dimension)
                )
                for row in range(dimension)
            )
            if update == candidate:
                return True
    return False