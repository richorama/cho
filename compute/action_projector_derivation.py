"""
Action-level epsilon projector diagnostic.

This file asks a deliberately narrow question: how much of the rank-one
epsilon bridge can be justified by the Fano incidence/action data already in
the repository?

It does not prove the CHO action. It separates three statements:

1. Fano incidence gives rank-one local support for any non-identical line
   transition, because two Fano lines intersect in exactly one imaginary unit.
2. Pure incidence is degenerate: all 21 unordered line pairs have that property.
3. The target epsilon trace on A_Weyl x J3(O) still requires a primitive Weyl
   and primitive Jordan matrix element. That embedding is not derived by Fano
   incidence alone.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations

import numpy as np


FANO_LINES = [
    (1, 2, 3),
    (1, 4, 5),
    (1, 7, 6),
    (2, 4, 6),
    (2, 5, 7),
    (3, 4, 7),
    (3, 6, 5),
]


@dataclass(frozen=True)
class TraceEmbedding:
    name: str
    weyl_rank: int
    jordan_rank: int
    note: str

    @property
    def rank(self) -> int:
        return self.weyl_rank * self.jordan_rank

    @property
    def epsilon_sq(self) -> float:
        return np.pi * self.rank / (16 * 27)


def incidence_matrix() -> np.ndarray:
    matrix = np.zeros((len(FANO_LINES), 7), dtype=int)
    for line_index, line in enumerate(FANO_LINES):
        for point in line:
            matrix[line_index, point - 1] = 1
    return matrix


def line_intersection(line_a: tuple[int, int, int], line_b: tuple[int, int, int]) -> tuple[int, ...]:
    return tuple(sorted(set(line_a).intersection(line_b)))


def transition_catalog() -> list[tuple[int, int, tuple[int, ...]]]:
    catalog = []
    for left, right in combinations(range(len(FANO_LINES)), 2):
        catalog.append((left, right, line_intersection(FANO_LINES[left], FANO_LINES[right])))
    return catalog


def fano_line_sets() -> tuple[frozenset[int], ...]:
    return tuple(frozenset(line) for line in FANO_LINES)


def fano_automorphisms() -> list[dict[int, int]]:
    """Return all point permutations preserving the unoriented Fano lines."""
    line_set = set(fano_line_sets())
    automorphisms: list[dict[int, int]] = []
    for permuted_points in permutations(range(1, 8)):
        mapping = {point: permuted_points[point - 1] for point in range(1, 8)}
        image = {
            frozenset(mapping[point] for point in line)
            for line in line_set
        }
        if image == line_set:
            automorphisms.append(mapping)
    return automorphisms


def unordered_line_pairs() -> set[frozenset[frozenset[int]]]:
    lines = fano_line_sets()
    return {
        frozenset((lines[left], lines[right]))
        for left, right in combinations(range(len(lines)), 2)
    }


def map_line_pair(pair: frozenset[frozenset[int]], mapping: dict[int, int]) -> frozenset[frozenset[int]]:
    return frozenset(
        frozenset(mapping[point] for point in line)
        for line in pair
    )


def line_pair_orbits() -> list[set[frozenset[frozenset[int]]]]:
    automorphisms = fano_automorphisms()
    remaining = unordered_line_pairs()
    orbits: list[set[frozenset[frozenset[int]]]] = []
    while remaining:
        seed = next(iter(remaining))
        orbit = {map_line_pair(seed, automorphism) for automorphism in automorphisms}
        orbits.append(orbit)
        remaining -= orbit
    return orbits


def trace_embeddings() -> list[TraceEmbedding]:
    return [
        TraceEmbedding(
            "primitive Weyl x primitive Jordan",
            1,
            1,
            "target rank-one embedding",
        ),
        TraceEmbedding(
            "full Weyl x primitive Jordan",
            16,
            1,
            "does not project the 16 Weyl states",
        ),
        TraceEmbedding(
            "primitive Weyl x full Jordan",
            1,
            27,
            "does not project the J3(O) trace",
        ),
        TraceEmbedding(
            "full Weyl x full Jordan",
            16,
            27,
            "no primitive embedding",
        ),
    ]


def print_incidence_action() -> None:
    print("ACTION PROJECTOR DIAGNOSTIC FOR EPSILON0")
    print("=" * 78)
    print("Fano incidence matrix B has rows = Fano lines and columns = imaginary units.")
    matrix = incidence_matrix()
    gram = matrix @ matrix.T
    print("Incidence Gram B B^T:")
    for row in gram:
        print("  " + " ".join(str(value) for value in row))
    print()
    off_diag = [gram[i, j] for i in range(7) for j in range(7) if i < j]
    print(f"off-diagonal overlaps: min={min(off_diag)}, max={max(off_diag)}, unique={sorted(set(off_diag))}")
    print("Thus every non-identical line transition has one shared imaginary unit.")
    print()


def print_transition_degeneracy() -> None:
    print("Rank-one local transition support")
    print("-" * 78)
    catalog = transition_catalog()
    rank_counts: dict[int, int] = {}
    for _, _, intersection in catalog:
        rank_counts[len(intersection)] = rank_counts.get(len(intersection), 0) + 1
    print(f"unordered line transitions = {len(catalog)}")
    print(f"intersection-rank counts   = {rank_counts}")
    print("sample transitions:")
    for left, right, intersection in catalog[:5]:
        print(f"  L{left + 1}{FANO_LINES[left]} -> L{right + 1}{FANO_LINES[right]} shares {intersection}")
    print()
    print("What this derives: if an adjacent Fano-line transition is forced, its")
    print("octonionic support is one-dimensional.")
    automorphisms = fano_automorphisms()
    orbits = line_pair_orbits()
    print()
    print(f"Fano automorphism count     = {len(automorphisms)}")
    print(f"unordered pair orbit sizes  = {[len(orbit) for orbit in orbits]}")
    print("Thus the 21 line-pair degeneracy is one automorphism orbit: selecting")
    print("a representative can be interpreted as vacuum/gauge choice once the")
    print("action or Higgs boundary breaks the symmetry.")
    print()
    print("What it does not derive: the action/boundary condition that selects a")
    print("representative, or how that one-dimensional support is embedded into")
    print("A_Weyl x J3(O).")
    print()


def print_trace_embedding_table() -> None:
    print("Embedding into A_Weyl x J3(O)")
    print("-" * 78)
    target = np.pi / (16 * 27)
    print(f"target epsilon0^2 = pi/(16*27) = {target:.10f}")
    print(f"{'embedding':<36} {'rank':>6} {'epsilon^2':>12} {'target x':>9}  note")
    for embedding in trace_embeddings():
        multiple = embedding.epsilon_sq / target
        print(
            f"{embedding.name:<36} "
            f"{embedding.rank:>6} "
            f"{embedding.epsilon_sq:>12.10f} "
            f"{multiple:>8.1f}x  "
            f"{embedding.note}"
        )
    print()
    print("Conclusion: the epsilon bridge is not closed by Fano incidence alone.")
    print("Fano incidence gives the local rank-one kernel. The normalized log-cos")
    print("action can then select the primitive Weyl x primitive Jordan product")
    print("by rank penalty; see compute/primitive_projector_derivation.py.")
    print("The physical transition ray, trace space, pi holonomy, and vacuum rule")
    print("remain open.")
    print()


def print_failure_closed_status() -> None:
    print("Failure-closed proof status")
    print("-" * 78)
    items = [
        ("local rank-one Fano support", "derived from incidence"),
        ("line-pair orbit", "one automorphism orbit; representative not derived"),
        ("A_Weyl primitive projector", "conditional from normalized rank penalty"),
        ("J3(O) primitive projector", "conditional from normalized rank penalty"),
        ("pi holonomy", "not derived here"),
        ("normalized trace pi/432", "conditional on ray, trace space, and pi"),
    ]
    for claim, status in items:
        print(f"  {claim:<34} {status}")


def main() -> None:
    print_incidence_action()
    print_transition_degeneracy()
    print_trace_embedding_table()
    print_failure_closed_status()


if __name__ == "__main__":
    main()
