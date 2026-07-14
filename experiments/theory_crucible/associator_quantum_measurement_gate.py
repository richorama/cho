"""Can associator Gram projectors act as distinctive quantum measurements?

Each octonion source pair (a,b) gives P_ab = G_ab/4, a rank-four orthogonal
projector on the seven-dimensional imaginary space. This gate classifies the 21
projectors and tests whether their relative geometry supplies incompatible quantum
measurements, which would be needed for basis-independent interference or mixing.

Result preview: the 21 pairs collapse to seven projectors, one per Fano line.
Each projector is simply one on the four coordinates outside that line and zero on
the three coordinates on it. All seven commute. Distinct projectors intersect in
rank two, with principal-angle cosines squared (1,1,0,0), and sum to 4I. This is a
beautiful tight family of compatible yes/no questions, but compatibility makes it
classical in one common basis; it does not generate quantum mixing by itself.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/associator_quantum_measurement_gate.py
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

import numpy as np

from associator_discriminator_gate import transport_defect
from signed_fano_multiplication_census import (
    FANO_TRIPLES,
    multiplication_table,
    standard_signed_orbit,
)


FANO_LINES = tuple(frozenset(triple) for triple in FANO_TRIPLES)


def source_line(first: int, second: int) -> frozenset[int]:
    """Unique Fano line containing a pair of distinct imaginary units."""
    matches = tuple(line for line in FANO_LINES if first in line and second in line)
    assert len(matches) == 1
    return matches[0]


def associator_projector(table: np.ndarray, first: int, second: int) -> np.ndarray:
    defect = transport_defect(table, first, second)
    return (defect.T @ defect).astype(float) / 4.0


def complement_projector(line: frozenset[int]) -> np.ndarray:
    return np.diag([0.0 if index in line else 1.0 for index in range(1, 8)])


def is_orthogonal_projector(matrix: np.ndarray, tolerance: float = 1e-12) -> bool:
    return bool(
        np.linalg.norm(matrix - matrix.T) < tolerance
        and np.linalg.norm(matrix @ matrix - matrix) < tolerance
    )


def unique_projectors(
    labelled_projectors: tuple[tuple[tuple[int, int], np.ndarray], ...]
) -> tuple[tuple[np.ndarray, tuple[tuple[int, int], ...]], ...]:
    representatives: list[np.ndarray] = []
    labels: list[list[tuple[int, int]]] = []
    for label, projector in labelled_projectors:
        for index, representative in enumerate(representatives):
            if np.array_equal(projector, representative):
                labels[index].append(label)
                break
        else:
            representatives.append(projector)
            labels.append([label])
    return tuple(
        (representative, tuple(projector_labels))
        for representative, projector_labels in zip(representatives, labels)
    )


def principal_cosines_squared(first: np.ndarray, second: np.ndarray) -> tuple[float, ...]:
    first_values, first_vectors = np.linalg.eigh(first)
    second_values, second_vectors = np.linalg.eigh(second)
    first_frame = first_vectors[:, first_values > 0.5]
    second_frame = second_vectors[:, second_values > 0.5]
    singular_values = np.linalg.svd(first_frame.T @ second_frame, compute_uv=False)
    return tuple(np.round(singular_values * singular_values, 12))


def random_rank_projector(rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(7, 4))
    frame, _ = np.linalg.qr(matrix)
    return frame @ frame.T


def main() -> None:
    table = multiplication_table((1,) * 7)
    source_pairs = tuple(combinations(range(1, 8), 2))
    labelled = tuple(
        ((first, second), associator_projector(table, first, second))
        for first, second in source_pairs
    )

    assert len(labelled) == 21
    for (first, second), projector in labelled:
        assert is_orthogonal_projector(projector)
        assert int(round(np.trace(projector))) == 4
        assert np.array_equal(projector, complement_projector(source_line(first, second)))

    unique = unique_projectors(labelled)
    projectors = tuple(projector for projector, _ in unique)
    class_sizes = tuple(sorted(len(labels) for _, labels in unique))
    assert len(projectors) == 7
    assert class_sizes == (3,) * 7

    overlap_histogram: Counter[int] = Counter()
    angle_histogram: Counter[tuple[float, ...]] = Counter()
    maximum_commutator = 0.0
    for first, second in combinations(projectors, 2):
        maximum_commutator = max(
            maximum_commutator, np.linalg.norm(first @ second - second @ first)
        )
        overlap_histogram[int(round(np.trace(first @ second)))] += 1
        angle_histogram[principal_cosines_squared(first, second)] += 1

    assert maximum_commutator == 0.0
    assert overlap_histogram == Counter({2: 21})
    assert angle_histogram == Counter({(1.0, 1.0, 0.0, 0.0): 21})
    assert np.array_equal(sum(projectors, np.zeros((7, 7))), 4.0 * np.eye(7))

    reflections = tuple(2.0 * projector - np.eye(7) for projector in projectors)
    assert all(np.array_equal(reflection.T @ reflection, np.eye(7)) for reflection in reflections)
    assert all(
        np.array_equal(first @ second, second @ first)
        for first, second in combinations(reflections, 2)
    )

    survivor_orbit = standard_signed_orbit()
    rejected_valid_counts = []
    for signs in product((-1, 1), repeat=7):
        if signs in survivor_orbit:
            continue
        rejected_table = multiplication_table(signs)
        valid_count = sum(
            is_orthogonal_projector(
                associator_projector(rejected_table, first, second)
            )
            and int(
                round(
                    np.trace(
                        associator_projector(rejected_table, first, second)
                    )
                )
            )
            == 4
            for first, second in source_pairs
        )
        rejected_valid_counts.append(valid_count)
    assert len(rejected_valid_counts) == 112
    assert max(rejected_valid_counts) == 0

    rng = np.random.default_rng(20260714)
    random_commutators = []
    random_overlaps = []
    for _ in range(200):
        first = random_rank_projector(rng)
        second = random_rank_projector(rng)
        random_commutators.append(np.linalg.norm(first @ second - second @ first))
        random_overlaps.append(float(np.trace(first @ second)))
    assert min(random_commutators) > 1e-3
    assert np.std(random_overlaps) > 1e-2

    print("=" * 74)
    print("THEORY CRUCIBLE 10: ASSOCIATOR QUANTUM-MEASUREMENT GATE")
    print("=" * 74)
    print(f"source pairs                         : 21")
    print(f"distinct associator measurements    : {len(projectors)}")
    print(f"source pairs per measurement        : {class_sizes}")
    print(f"rank of every yes-space             : 4")
    print(f"largest projector commutator        : {maximum_commutator:.1f}")
    print(f"distinct-pair overlap Tr(PQ)         : {dict(overlap_histogram)}")
    print(f"principal cosines squared            : {dict(angle_histogram)}")
    print(f"tight-frame sum                      : sum P_line = 4 I_7")
    print(f"rejected products with any valid P   : {sum(value > 0 for value in rejected_valid_counts)} / 112")
    print(f"random-control commutator range      : {min(random_commutators):.3f} .. {max(random_commutators):.3f}")
    print(f"random-control overlap std           : {np.std(random_overlaps):.3f}")
    print()
    print("PROVED")
    print("  * The 21 source pairs collapse to seven rank-four measurements, one")
    print("    for each Fano line; its no-space is exactly that three-point line.")
    print("  * All seven measurements commute and share a common coordinate basis.")
    print("  * Every distinct pair shares exactly two yes-directions and has")
    print("    principal cosines squared (1,1,0,0).")
    print("  * The seven projectors form a tight compatible family: sum P = 4I.")
    print("  * No rejected signed-Fano product yields even one valid rank-four")
    print("    associator projector; generic rank-four controls do not commute.")
    print()
    print("NOT PROVED")
    print("  * a quantum transition or interference law;")
    print("  * a physical meaning for the common seven-state basis;")
    print("  * a mechanism that turns compatible questions into PMNS mixing.")
    print()
    print("VERDICT: the associator supplies a uniquely octonionic measurement")
    print("         geometry, but it is simultaneously diagonalizable and therefore")
    print("         classical by itself. A second noncommuting structure is required")
    print("         before this can generate quantum mixing.")


if __name__ == "__main__":
    main()