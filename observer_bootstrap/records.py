"""Exact causal-influence and record holdouts for local binary dynamics."""

from __future__ import annotations

from itertools import product
from typing import NamedTuple, Optional, Tuple

from .local_dynamics import BinaryConfiguration, elementary_step


class RecordCensus(NamedTuple):
    total_rules: int
    background_independent: int
    persistent: int
    redundant_imprints: int


def evolve(
    rule: int, configuration: BinaryConfiguration, steps: int
) -> BinaryConfiguration:
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    result = configuration
    for _ in range(steps):
        result = elementary_step(rule, result)
    return result


def perturbation_response(
    rule: int,
    configuration: BinaryConfiguration,
    source: int,
    steps: int,
) -> BinaryConfiguration:
    """XOR response to flipping one source bit in a fixed background."""
    if source < 0 or source >= len(configuration):
        raise ValueError("source must index the configuration")
    perturbed = list(configuration)
    perturbed[source] ^= 1
    baseline_target = evolve(rule, configuration, steps)
    perturbed_target = evolve(rule, tuple(perturbed), steps)
    return tuple(
        baseline ^ changed
        for baseline, changed in zip(baseline_target, perturbed_target)
    )


def background_independent_response(
    rule: int, size: int, steps: int, source: Optional[int] = None
) -> Optional[BinaryConfiguration]:
    """Return the common response over all backgrounds, if one exists."""
    if size < 3:
        raise ValueError("size must be at least three")
    source = size // 2 if source is None else source
    common = None
    for configuration in product((0, 1), repeat=size):
        response = perturbation_response(rule, configuration, source, steps)
        if common is None:
            common = response
        elif response != common:
            return None
    return common


def has_persistent_redundant_imprint(
    rule: int, size: int = 11, horizon: int = 4
) -> bool:
    """A source flip has a universal nonzero response and final replication."""
    responses = tuple(
        background_independent_response(rule, size, steps)
        for steps in range(1, horizon + 1)
    )
    return (
        all(response is not None and any(response) for response in responses)
        and sum(responses[-1]) >= 2
    )


def response_respects_light_cone(
    response: BinaryConfiguration, source: int, steps: int
) -> bool:
    size = len(response)
    return all(
        not bit or min((index - source) % size, (source - index) % size) <= steps
        for index, bit in enumerate(response)
    )


def source_is_locally_decodable(rule: int, steps: int, radius: int) -> bool:
    """Test passive recovery of a source bit from a local future window."""
    if steps < 1 or radius < 0:
        raise ValueError("steps must be positive and radius nonnegative")
    past_radius = steps + radius
    size = 2 * past_radius + 3
    source = size // 2
    observed = (set(), set())
    for local_background in product((0, 1), repeat=2 * past_radius + 1):
        configuration = [0] * size
        configuration[source - past_radius : source + past_radius + 1] = (
            local_background
        )
        target = evolve(rule, tuple(configuration), steps)
        word = tuple(target[index] for index in range(source - radius, source + radius + 1))
        source_value = configuration[source]
        observed[source_value].add(word)
        if word in observed[1 - source_value]:
            return False
    return True


def record_census(
    rules: Tuple[int, ...], size: int = 11, horizon: int = 4
) -> RecordCensus:
    independent = persistent = redundant = 0
    for rule in rules:
        responses = tuple(
            background_independent_response(rule, size, steps)
            for steps in range(1, horizon + 1)
        )
        is_independent = all(response is not None for response in responses)
        is_persistent = is_independent and all(any(response) for response in responses)
        is_redundant = is_persistent and sum(responses[-1]) >= 2
        independent += is_independent
        persistent += is_persistent
        redundant += is_redundant
    return RecordCensus(len(rules), independent, persistent, redundant)