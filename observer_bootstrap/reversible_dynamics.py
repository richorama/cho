"""Exact reversible second-order binary cellular automata."""

from __future__ import annotations

from itertools import product
from typing import Callable, Dict, Iterator, NamedTuple, Optional, Tuple


ReversibleCell = Tuple[int, int]
ReversibleConfiguration = Tuple[ReversibleCell, ...]
ChannelBlocking = Callable[[int, int], int]


class ReversibleFlowRow(NamedTuple):
    microscopic_rule: int
    decimation_rule: int
    parity_rule: int


class TrajectoryConflict(NamedTuple):
    rule: int
    blocking_name: str
    first: ReversibleConfiguration
    first_coarse_site: int
    second: ReversibleConfiguration
    second_coarse_site: int


class BlockingAuditRow(NamedTuple):
    blocking_code: int
    is_constant: bool
    is_affine: bool
    survivors: Tuple[int, ...]


def reversible_configurations(size: int) -> Iterator[ReversibleConfiguration]:
    if size < 1:
        raise ValueError("size must be positive")
    cells = tuple(product((0, 1), repeat=2))
    yield from product(cells, repeat=size)


def local_output(rule: int, left: int, center: int, right: int) -> int:
    if rule < 0 or rule > 255:
        raise ValueError("rule must be an ECA rule")
    return (rule >> (4 * left + 2 * center + right)) & 1


def is_affine_rule(rule: int) -> bool:
    """Return whether the Boolean local rule is affine over GF(2)."""
    constant = local_output(rule, 0, 0, 0)
    linear_rule = rule ^ (255 if constant else 0)
    for left in range(8):
        for right in range(8):
            if ((linear_rule >> (left ^ right)) & 1) != (
                ((linear_rule >> left) & 1) ^ ((linear_rule >> right) & 1)
            ):
                return False
    return True


def reversible_step(
    rule: int, configuration: ReversibleConfiguration
) -> ReversibleConfiguration:
    """Map (current, previous) to (f(current) XOR previous, current)."""
    if len(configuration) < 3:
        raise ValueError("ring size must be at least three")
    if any(bit not in (0, 1) for cell in configuration for bit in cell):
        raise ValueError("configuration channels must be binary")
    size = len(configuration)
    current = tuple(cell[0] for cell in configuration)
    previous = tuple(cell[1] for cell in configuration)
    return tuple(
        (
            local_output(
                rule,
                current[(index - 1) % size],
                current[index],
                current[(index + 1) % size],
            )
            ^ previous[index],
            current[index],
        )
        for index in range(size)
    )


def inverse_reversible_step(
    rule: int, configuration: ReversibleConfiguration
) -> ReversibleConfiguration:
    """Invert one second-order step exactly."""
    size = len(configuration)
    old_current = tuple(cell[1] for cell in configuration)
    return tuple(
        (
            old_current[index],
            configuration[index][0]
            ^ local_output(
                rule,
                old_current[(index - 1) % size],
                old_current[index],
                old_current[(index + 1) % size],
            ),
        )
        for index in range(size)
    )


def recover_two_step_current(
    rule: int, future_window: Tuple[ReversibleCell, ReversibleCell, ReversibleCell]
) -> int:
    """Recover the central current bit from its radius-one state two steps later."""
    return future_window[1][0] ^ local_output(
        rule,
        future_window[0][1],
        future_window[1][1],
        future_window[2][1],
    )


def second_step_record_is_one_time_padded(rule: int) -> bool:
    """The unknown previous bit can mask either value of every new record bit."""
    return all(
        {
            local_output(rule, left, center, right) ^ previous
            for previous in (0, 1)
        }
        == {0, 1}
        for left, center, right in product((0, 1), repeat=3)
    )


def decimate_channel(left: int, right: int) -> int:
    del right
    return left


def parity_channel(left: int, right: int) -> int:
    return left ^ right


def boolean_pair_blocking(code: int) -> ChannelBlocking:
    if code < 0 or code > 15:
        raise ValueError("pair blocking code must be a four-bit truth table")

    def blocking(left: int, right: int) -> int:
        return (code >> (2 * left + right)) & 1

    return blocking


def pair_blocking_is_affine(code: int) -> bool:
    blocking = boolean_pair_blocking(code)
    nonlinear_coefficient = (
        blocking(0, 0)
        ^ blocking(0, 1)
        ^ blocking(1, 0)
        ^ blocking(1, 1)
    )
    return nonlinear_coefficient == 0


def block_reversible_pairs(
    configuration: ReversibleConfiguration, blocking: ChannelBlocking
) -> ReversibleConfiguration:
    if len(configuration) % 2:
        raise ValueError("pair blocking requires an even ring size")
    return tuple(
        (
            blocking(configuration[index][0], configuration[index + 1][0]),
            blocking(configuration[index][1], configuration[index + 1][1]),
        )
        for index in range(0, len(configuration), 2)
    )


def infer_reversible_rule(
    update: Dict[ReversibleConfiguration, ReversibleConfiguration]
) -> Optional[int]:
    outputs = {}
    for source, target in update.items():
        size = len(source)
        if len(target) != size:
            raise ValueError("source and target sizes must agree")
        current = tuple(cell[0] for cell in source)
        for index, target_cell in enumerate(target):
            if target_cell[1] != current[index]:
                return None
            neighborhood = (
                current[(index - 1) % size],
                current[index],
                current[(index + 1) % size],
            )
            output = target_cell[0] ^ source[index][1]
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


def induced_reversible_rule(
    rule: int,
    source_size: int,
    blocking: ChannelBlocking,
    microscopic_steps: int = 2,
) -> Optional[int]:
    if microscopic_steps < 1:
        raise ValueError("microscopic_steps must be positive")
    coarse_update = {}
    for configuration in reversible_configurations(source_size):
        source = block_reversible_pairs(configuration, blocking)
        evolved = configuration
        for _ in range(microscopic_steps):
            evolved = reversible_step(rule, evolved)
        target = block_reversible_pairs(evolved, blocking)
        previous = coarse_update.get(source)
        if previous is not None and previous != target:
            return None
        coarse_update[source] = target
    return infer_reversible_rule(coarse_update)


def reversible_blocking_flow_census(
    source_size: int = 6, microscopic_steps: int = 2
) -> Tuple[ReversibleFlowRow, ...]:
    rows = []
    for rule in range(256):
        decimation_rule = induced_reversible_rule(
            rule, source_size, decimate_channel, microscopic_steps
        )
        parity_rule = induced_reversible_rule(
            rule, source_size, parity_channel, microscopic_steps
        )
        if decimation_rule is not None and parity_rule is not None:
            rows.append(ReversibleFlowRow(rule, decimation_rule, parity_rule))
    return tuple(rows)


def induced_reversible_trajectory_rule(
    rule: int,
    source_size: int,
    blocking: ChannelBlocking,
    temporal_stride: int = 2,
) -> Optional[int]:
    """Infer a reversible law from spatially blocked, time-sampled trajectories."""
    if temporal_stride < 1:
        raise ValueError("temporal_stride must be positive")
    outputs = {}
    for configuration in reversible_configurations(source_size):
        coarse_previous = block_reversible_pairs(configuration, blocking)
        evolved = configuration
        for _ in range(temporal_stride):
            evolved = reversible_step(rule, evolved)
        coarse_current = block_reversible_pairs(evolved, blocking)
        for _ in range(temporal_stride):
            evolved = reversible_step(rule, evolved)
        coarse_next = block_reversible_pairs(evolved, blocking)

        previous_values = tuple(cell[0] for cell in coarse_previous)
        current_values = tuple(cell[0] for cell in coarse_current)
        next_values = tuple(cell[0] for cell in coarse_next)
        size = len(current_values)
        for index in range(size):
            neighborhood = (
                current_values[(index - 1) % size],
                current_values[index],
                current_values[(index + 1) % size],
            )
            output = next_values[index] ^ previous_values[index]
            prior = outputs.get(neighborhood)
            if prior is not None and prior != output:
                return None
            outputs[neighborhood] = output
    if len(outputs) != 8:
        return None
    return sum(
        output << (4 * left + 2 * center + right)
        for (left, center, right), output in outputs.items()
    )


def _trajectory_local_observations(
    rule: int,
    configuration: ReversibleConfiguration,
    blocking: ChannelBlocking,
    temporal_stride: int,
) -> Tuple[Tuple[Tuple[int, int, int, int], int], ...]:
    coarse_previous = block_reversible_pairs(configuration, blocking)
    evolved = configuration
    for _ in range(temporal_stride):
        evolved = reversible_step(rule, evolved)
    coarse_current = block_reversible_pairs(evolved, blocking)
    for _ in range(temporal_stride):
        evolved = reversible_step(rule, evolved)
    coarse_next = block_reversible_pairs(evolved, blocking)

    previous_values = tuple(cell[0] for cell in coarse_previous)
    current_values = tuple(cell[0] for cell in coarse_current)
    next_values = tuple(cell[0] for cell in coarse_next)
    size = len(current_values)
    return tuple(
        (
            (
                previous_values[index],
                current_values[(index - 1) % size],
                current_values[index],
                current_values[(index + 1) % size],
            ),
            next_values[index] ^ previous_values[index],
        )
        for index in range(size)
    )


def trajectory_conflict_certificate(
    rule: int, source_size: int = 6, temporal_stride: int = 2
) -> Optional[TrajectoryConflict]:
    """Return a bounded witness against a radius-one coarse trajectory law."""
    for blocking_name, blocking in (
        ("decimation", decimate_channel),
        ("parity", parity_channel),
    ):
        seen = {}
        for configuration in reversible_configurations(source_size):
            observations = _trajectory_local_observations(
                rule, configuration, blocking, temporal_stride
            )
            for coarse_site, (coarse_input, output) in enumerate(observations):
                previous = seen.get(coarse_input)
                if previous is not None and previous[1] != output:
                    return TrajectoryConflict(
                        rule,
                        blocking_name,
                        previous[0],
                        previous[2],
                        configuration,
                        coarse_site,
                    )
                seen[coarse_input] = (configuration, output, coarse_site)
    return None


def validates_trajectory_conflict(certificate: TrajectoryConflict) -> bool:
    blocking = {
        "decimation": decimate_channel,
        "parity": parity_channel,
    }.get(certificate.blocking_name)
    if blocking is None:
        return False
    first = _trajectory_local_observations(
        certificate.rule, certificate.first, blocking, 2
    )[certificate.first_coarse_site]
    second = _trajectory_local_observations(
        certificate.rule, certificate.second, blocking, 2
    )[certificate.second_coarse_site]
    return first[0] == second[0] and first[1] != second[1]


def reversible_trajectory_flow_census(
    source_size: int = 6,
    temporal_stride: int = 2,
    rules: Tuple[int, ...] = tuple(range(256)),
) -> Tuple[ReversibleFlowRow, ...]:
    rows = []
    for rule in rules:
        decimation_rule = induced_reversible_trajectory_rule(
            rule, source_size, decimate_channel, temporal_stride
        )
        parity_rule = induced_reversible_trajectory_rule(
            rule, source_size, parity_channel, temporal_stride
        )
        if decimation_rule is not None and parity_rule is not None:
            rows.append(ReversibleFlowRow(rule, decimation_rule, parity_rule))
    return tuple(rows)


def pair_blocking_audit(
    source_size: int = 6, temporal_stride: int = 2
) -> Tuple[BlockingAuditRow, ...]:
    rows = []
    for code in range(16):
        blocking = boolean_pair_blocking(code)
        survivors = tuple(
            rule
            for rule in range(256)
            if induced_reversible_trajectory_rule(
                rule, source_size, blocking, temporal_stride
            )
            is not None
        )
        rows.append(
            BlockingAuditRow(
                code,
                code in (0, 15),
                pair_blocking_is_affine(code),
                survivors,
            )
        )
    return tuple(rows)


def source_current_is_locally_decodable(
    rule: int, steps: int, radius: int, channels: Tuple[int, ...] = (0, 1)
) -> bool:
    """Recover one initial current bit from a bounded future two-channel window."""
    if steps < 1 or radius < 0:
        raise ValueError("steps must be positive and radius nonnegative")
    if not channels or any(channel not in (0, 1) for channel in channels):
        raise ValueError("channels must select current, record, or both")
    past_radius = steps + radius
    size = 2 * past_radius + 3
    source = size // 2
    background_positions = tuple(
        (index, channel)
        for index in range(source - past_radius, source + past_radius + 1)
        for channel in range(2)
        if (index, channel) != (source, 0)
    )
    observed = (set(), set())
    for background in product((0, 1), repeat=len(background_positions)):
        for source_value in (0, 1):
            configuration = [[0, 0] for _ in range(size)]
            configuration[source][0] = source_value
            for (index, channel), value in zip(background_positions, background):
                configuration[index][channel] = value
            evolved = tuple(tuple(cell) for cell in configuration)
            for _ in range(steps):
                evolved = reversible_step(rule, evolved)
            word = tuple(
                evolved[index][channel]
                for index in range(source - radius, source + radius + 1)
                for channel in channels
            )
            observed[source_value].add(word)
            if word in observed[1 - source_value]:
                return False
    return True