"""Exact symmetry no-go for selecting the Fano upper-octant sector.

The full automorphism group GL(3,2) of the Fano plane is generated explicitly.
Without a selected vacuum it is transitive on lines, so an invariant diagonal
line observable is constant. After selecting one vacuum point, its stabilizer has
two line orbits: three incident lines and four avoiding lines. Symmetry therefore
permits two independent weights but cannot order them or choose one projector as
the atmospheric observable.

This is a finite exact calculation. No measured value or CHO constant is used.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/fano_selection_no_go.py
"""

from __future__ import annotations

from itertools import product

import numpy as np


POINTS = tuple(range(1, 8))
VACUUM = 7


def bits(point: int) -> np.ndarray:
    """Three-bit column vector representing a nonzero point of GF(2)^3."""
    return np.array([(point >> shift) & 1 for shift in range(3)], dtype=np.int8)


def point(vector: np.ndarray) -> int:
    """Encode a GF(2)^3 vector as an integer point label."""
    return sum(int(value) << shift for shift, value in enumerate(vector % 2))


def determinant_mod2(matrix: np.ndarray) -> int:
    """Determinant over GF(2), evaluated exactly for a 3 by 3 matrix."""
    a, b, c = (int(value) for value in matrix[0])
    d, e, f = (int(value) for value in matrix[1])
    g, h, i = (int(value) for value in matrix[2])
    return (a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)) % 2


def automorphisms() -> tuple[np.ndarray, ...]:
    """All 168 invertible 3 by 3 matrices over GF(2)."""
    matrices = []
    for entries in product((0, 1), repeat=9):
        matrix = np.array(entries, dtype=np.int8).reshape(3, 3)
        if determinant_mod2(matrix) == 1:
            matrices.append(matrix)
    return tuple(matrices)


def fano_lines() -> tuple[frozenset[int], ...]:
    """All two-dimensional subspaces of GF(2)^3 with zero removed."""
    lines = {
        frozenset((left, right, left ^ right))
        for left in POINTS
        for right in POINTS
        if left != right
    }
    return tuple(sorted(lines, key=lambda line: tuple(sorted(line))))


def act_on_point(matrix: np.ndarray, label: int) -> int:
    return point((matrix @ bits(label)) % 2)


def act_on_line(matrix: np.ndarray, line: frozenset[int]) -> frozenset[int]:
    return frozenset(act_on_point(matrix, label) for label in line)


def orbits(items: tuple, actions) -> tuple[frozenset, ...]:
    """Compute finite orbits from an iterable of action functions."""
    unseen = set(items)
    result = []
    while unseen:
        seed = next(iter(unseen))
        orbit = frozenset(action(seed) for action in actions)
        result.append(orbit)
        unseen -= orbit
    return tuple(sorted(result, key=lambda orbit: (len(orbit), repr(sorted(orbit, key=repr)))))


def invariant_diagonal_dimension(line_orbits: tuple[frozenset, ...]) -> int:
    """Dimension of diagonal observables constant on each line orbit."""
    return len(line_orbits)


def main() -> None:
    group = automorphisms()
    lines = fano_lines()
    line_set = set(lines)

    assert len(group) == 168
    assert len(lines) == 7
    assert all(len(line) == 3 for line in lines)
    assert all(act_on_line(matrix, line) in line_set for matrix in group for line in lines)

    full_actions = tuple(
        lambda line, matrix=matrix: act_on_line(matrix, line) for matrix in group
    )
    full_line_orbits = orbits(lines, full_actions)
    assert tuple(map(len, full_line_orbits)) == (7,)
    assert invariant_diagonal_dimension(full_line_orbits) == 1

    stabilizer = tuple(
        matrix for matrix in group if act_on_point(matrix, VACUUM) == VACUUM
    )
    stabilizer_actions = tuple(
        lambda line, matrix=matrix: act_on_line(matrix, line) for matrix in stabilizer
    )
    vacuum_line_orbits = orbits(lines, stabilizer_actions)
    orbit_sizes = tuple(sorted(map(len, vacuum_line_orbits)))

    assert len(stabilizer) == 24
    assert orbit_sizes == (3, 4)
    assert invariant_diagonal_dimension(vacuum_line_orbits) == 2

    through = frozenset(line for line in lines if VACUUM in line)
    avoiding = frozenset(line for line in lines if VACUUM not in line)
    assert set(vacuum_line_orbits) == {through, avoiding}

    through_projector = np.diag([float(line in through) for line in lines])
    avoiding_projector = np.diag([float(line in avoiding) for line in lines])
    assert np.array_equal(through_projector + avoiding_projector, np.eye(7))
    assert np.trace(through_projector) == 3
    assert np.trace(avoiding_projector) == 4

    print("=" * 74)
    print("THEORY CRUCIBLE 02: FANO SELECTION NO-GO")
    print("=" * 74)
    print(f"Aut(Fano) = GL(3,2) size            : {len(group)}")
    print(f"full-group line orbit sizes         : {tuple(map(len, full_line_orbits))}")
    print(f"vacuum stabilizer size              : {len(stabilizer)}")
    print(f"stabilizer line orbit sizes         : {orbit_sizes}")
    print(f"invariant diagonal dimensions       : 1 -> 2 after vacuum choice")
    print()
    print("PROVED")
    print("  * Before a vacuum is selected, Fano symmetry forces equal line weights.")
    print("  * A selected vacuum splits line space canonically into ranks 3 and 4.")
    print("  * The most general stabilizer-invariant diagonal observable has two")
    print("    independent sector weights: a P_through + b P_avoiding.")
    print()
    print("NOT PROVED")
    print("  * the sign or magnitude of b-a;")
    print("  * why P_avoiding rather than P_through is the atmospheric observable;")
    print("  * any map from either invariant sector to a PMNS matrix element.")
    print()
    print("VERDICT: symmetry creates the 3+4 alternatives but cannot select the")
    print("         upper-octant alternative. That choice must come from dynamics.")


if __name__ == "__main__":
    main()