"""Exact product-local dynamics and blocking flows on binary rings."""

from __future__ import annotations

from itertools import product
from typing import Callable, Dict, Iterator, NamedTuple, Optional, Tuple


BinaryConfiguration = Tuple[int, ...]
GlobalUpdate = Tuple[BinaryConfiguration, ...]
PairBlocking = Callable[[int, int], int]


class LocalFlowRow(NamedTuple):
    microscopic_rule: int
    decimation_rule: int
    parity_rule: int


def binary_configurations(size: int) -> Iterator[BinaryConfiguration]:
    if size < 1:
        raise ValueError("size must be positive")
    yield from product((0, 1), repeat=size)


def elementary_step(rule: int, configuration: BinaryConfiguration) -> BinaryConfiguration:
    """Apply a radius-one elementary cellular automaton on a periodic ring."""
    if rule < 0 or rule > 255 or len(configuration) < 3:
        raise ValueError("rule must be an ECA rule and ring size must be at least three")
    if any(bit not in (0, 1) for bit in configuration):
        raise ValueError("configuration must be binary")
    size = len(configuration)
    return tuple(
        (rule >> (
            4 * configuration[(index - 1) % size]
            + 2 * configuration[index]
            + configuration[(index + 1) % size]
        ))
        & 1
        for index in range(size)
    )


def decimate_pair(left: int, right: int) -> int:
    del right
    return left


def parity_pair(left: int, right: int) -> int:
    return left ^ right


def block_pairs(
    configuration: BinaryConfiguration, blocking: PairBlocking
) -> BinaryConfiguration:
    if len(configuration) % 2:
        raise ValueError("pair blocking requires an even ring size")
    return tuple(
        blocking(configuration[index], configuration[index + 1])
        for index in range(0, len(configuration), 2)
    )


def induced_block_update(
    rule: int,
    source_size: int,
    blocking: PairBlocking,
    microscopic_steps: int = 1,
) -> Optional[Dict[BinaryConfiguration, BinaryConfiguration]]:
    """Return the exact coarse update, or None when a blocking fiber splits."""
    if microscopic_steps < 1:
        raise ValueError("microscopic_steps must be positive")
    coarse_update = {}
    for configuration in binary_configurations(source_size):
        source = block_pairs(configuration, blocking)
        evolved = configuration
        for _ in range(microscopic_steps):
            evolved = elementary_step(rule, evolved)
        target = block_pairs(evolved, blocking)
        previous = coarse_update.get(source)
        if previous is not None and previous != target:
            return None
        coarse_update[source] = target
    return coarse_update


def infer_elementary_rule(
    update: Dict[BinaryConfiguration, BinaryConfiguration]
) -> Optional[int]:
    """Identify a radius-one rule producing a complete coarse global update."""
    if not update:
        raise ValueError("update must not be empty")
    size = len(next(iter(update)))
    expected_sources = set(binary_configurations(size))
    if size < 3 or set(update) != expected_sources:
        raise ValueError("update must cover every configuration of a ring of size >= 3")

    outputs = {}
    for source, target in update.items():
        if len(target) != size:
            raise ValueError("source and target sizes must agree")
        for index, output in enumerate(target):
            neighborhood = (
                source[(index - 1) % size],
                source[index],
                source[(index + 1) % size],
            )
            previous = outputs.get(neighborhood)
            if previous is not None and previous != output:
                return None
            outputs[neighborhood] = output
    if len(outputs) != 8:
        return None
    return sum(
        output << (4 * left + 2 * center + right)
        for (left, center, right), output in outputs.items()
    )


def induced_elementary_rule(
    rule: int,
    source_size: int,
    blocking: PairBlocking,
    microscopic_steps: int = 1,
) -> Optional[int]:
    update = induced_block_update(rule, source_size, blocking, microscopic_steps)
    return None if update is None else infer_elementary_rule(update)


def local_blocking_flow_census(
    source_sizes: Tuple[int, ...] = (6, 8, 10),
    microscopic_steps: int = 2,
) -> Tuple[LocalFlowRow, ...]:
    """Rules closing under both fixed blockings with size-independent flows."""
    rows = []
    for rule in range(256):
        decimation_rules = tuple(
            induced_elementary_rule(rule, size, decimate_pair, microscopic_steps)
            for size in source_sizes
        )
        parity_rules = tuple(
            induced_elementary_rule(rule, size, parity_pair, microscopic_steps)
            for size in source_sizes
        )
        if (
            decimation_rules[0] is not None
            and len(set(decimation_rules)) == 1
            and parity_rules[0] is not None
            and len(set(parity_rules)) == 1
        ):
            rows.append(LocalFlowRow(rule, decimation_rules[0], parity_rules[0]))
    return tuple(rows)


def essential_inputs(rule: int) -> Tuple[bool, bool, bool]:
    """Report whether left, center, and right can each change the local output."""
    if rule < 0 or rule > 255:
        raise ValueError("rule must be an ECA rule")
    result = []
    for input_index in range(3):
        essential = False
        for neighborhood in product((0, 1), repeat=3):
            flipped = list(neighborhood)
            flipped[input_index] ^= 1
            index = 4 * neighborhood[0] + 2 * neighborhood[1] + neighborhood[2]
            flipped_index = 4 * flipped[0] + 2 * flipped[1] + flipped[2]
            if ((rule >> index) & 1) != ((rule >> flipped_index) & 1):
                essential = True
                break
        result.append(essential)
    return tuple(result)


def is_additive_elementary_rule(rule: int) -> bool:
    """Return whether the local Boolean rule is linear over GF(2)."""
    if rule < 0 or rule > 255:
        raise ValueError("rule must be an ECA rule")
    for left in range(8):
        for right in range(8):
            if ((rule >> (left ^ right)) & 1) != (
                ((rule >> left) & 1) ^ ((rule >> right) & 1)
            ):
                return False
    return True


def is_trivial_elementary_rule(rule: int) -> bool:
    """Constant, identity, and complement rules are noninteracting controls."""
    return rule in (0, 51, 204, 255)