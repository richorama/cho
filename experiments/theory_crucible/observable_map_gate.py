"""Classify vacuum-stabilizer-equivariant maps into three flavour dimensions.

The vacuum stabilizer has order 24 and acts on the seven Fano lines in orbits of
sizes three and four. Its line permutation representation decomposes as

    R^7 = 2*1 + 2 + 3.

There are two natural three-dimensional target representations:

* the permutation representation on the three through-vacuum lines, 1 + 2;
* the irreducible standard representation obtained from the zero-sum subspace of
  the four avoiding lines, 3.

Character inner products classify all equivariant maps. The first target admits
three independent intertwiners. The irreducible target admits exactly one up to
scale, but its canonical pullback is a rank-three projector with normalized trace
3/7, not the rank-four avoidance projector with trace 4/7.

No measured mixing value is used as an input.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/observable_map_gate.py
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from fano_selection_no_go import (
    VACUUM,
    act_on_line,
    act_on_point,
    automorphisms,
    fano_lines,
)


def permutation_matrix(permutation: tuple[int, ...]) -> np.ndarray:
    """Matrix sending coordinate basis vector i to permutation[i]."""
    matrix = np.zeros((len(permutation), len(permutation)), dtype=float)
    for source, target in enumerate(permutation):
        matrix[target, source] = 1.0
    return matrix


def induced_permutation(matrix: np.ndarray, items: tuple) -> tuple[int, ...]:
    """Permutation induced by a point automorphism on a tuple of Fano lines."""
    return tuple(items.index(act_on_line(matrix, item)) for item in items)


def fixed_count(permutation: tuple[int, ...]) -> int:
    return sum(index == image for index, image in enumerate(permutation))


def character_inner_product(left: tuple[int, ...], right: tuple[int, ...]) -> Fraction:
    """Exact finite-group character inner product."""
    assert len(left) == len(right)
    return Fraction(sum(a * b for a, b in zip(left, right)), len(left))


def zero_sum_basis(dimension: int) -> np.ndarray:
    """Orthonormal basis for vectors whose coordinates sum to zero."""
    difference = np.zeros((dimension, dimension - 1), dtype=float)
    for column in range(dimension - 1):
        difference[column, column] = 1.0
        difference[-1, column] = -1.0
    basis, _ = np.linalg.qr(difference)
    return basis


def intertwiner_dimension(
    domain_representations: tuple[np.ndarray, ...],
    target_representations: tuple[np.ndarray, ...],
) -> int:
    """Numerical nullity of T D(g) = F(g) T for every group element."""
    target_dimension = target_representations[0].shape[0]
    domain_dimension = domain_representations[0].shape[0]
    equations = []
    for domain, target in zip(domain_representations, target_representations):
        equations.append(
            np.kron(domain.T, np.eye(target_dimension))
            - np.kron(np.eye(domain_dimension), target)
        )
    singular_values = np.linalg.svd(np.vstack(equations), compute_uv=False)
    return int(np.count_nonzero(singular_values < 1e-10))


def main() -> None:
    lines = fano_lines()
    through = tuple(line for line in lines if VACUUM in line)
    avoiding = tuple(line for line in lines if VACUUM not in line)
    stabilizer = tuple(
        matrix
        for matrix in automorphisms()
        if act_on_point(matrix, VACUUM) == VACUUM
    )

    domain_permutations = tuple(
        induced_permutation(matrix, lines) for matrix in stabilizer
    )
    through_permutations = tuple(
        induced_permutation(matrix, through) for matrix in stabilizer
    )
    avoiding_permutations = tuple(
        induced_permutation(matrix, avoiding) for matrix in stabilizer
    )

    domain_characters = tuple(map(fixed_count, domain_permutations))
    through_characters = tuple(map(fixed_count, through_permutations))
    avoiding_characters = tuple(map(fixed_count, avoiding_permutations))
    standard_characters = tuple(value - 1 for value in avoiding_characters)
    trivial_characters = (1,) * len(stabilizer)
    two_dimensional_characters = tuple(
        value - 1 for value in through_characters
    )

    domain_multiplicities = {
        "trivial": character_inner_product(domain_characters, trivial_characters),
        "two_dimensional": character_inner_product(
            domain_characters, two_dimensional_characters
        ),
        "standard_three": character_inner_product(
            domain_characters, standard_characters
        ),
    }
    through_hom_dimension = character_inner_product(
        domain_characters, through_characters
    )
    standard_hom_dimension = character_inner_product(
        domain_characters, standard_characters
    )

    assert len(stabilizer) == 24
    assert domain_multiplicities == {
        "trivial": Fraction(2),
        "two_dimensional": Fraction(1),
        "standard_three": Fraction(1),
    }
    assert through_hom_dimension == 3
    assert standard_hom_dimension == 1

    domain_representations = tuple(
        permutation_matrix(permutation) for permutation in domain_permutations
    )
    through_representations = tuple(
        permutation_matrix(permutation) for permutation in through_permutations
    )
    avoiding_representations = tuple(
        permutation_matrix(permutation) for permutation in avoiding_permutations
    )
    standard_basis = zero_sum_basis(4)
    standard_representations = tuple(
        standard_basis.T @ representation @ standard_basis
        for representation in avoiding_representations
    )

    assert intertwiner_dimension(domain_representations, through_representations) == 3
    assert intertwiner_dimension(domain_representations, standard_representations) == 1

    avoiding_indices = tuple(lines.index(line) for line in avoiding)
    inclusion = np.zeros((4, 7), dtype=float)
    for avoiding_index, line_index in enumerate(avoiding_indices):
        inclusion[avoiding_index, line_index] = 1.0
    canonical_map = standard_basis.T @ inclusion
    pullback = canonical_map.T @ canonical_map
    avoidance_projector = inclusion.T @ inclusion

    equivariance_residual = max(
        np.linalg.norm(
            canonical_map @ domain - target @ canonical_map
        )
        for domain, target in zip(domain_representations, standard_representations)
    )
    assert equivariance_residual < 1e-12
    assert np.linalg.norm(pullback @ pullback - pullback) < 1e-12
    assert int(round(np.trace(pullback))) == 3
    assert int(round(np.trace(avoidance_projector))) == 4
    assert np.linalg.norm(avoidance_projector - pullback) > 0.9

    uniform_avoiding = inclusion.T @ np.ones(4) / 2.0
    assert np.linalg.norm(canonical_map @ uniform_avoiding) < 1e-12

    print("=" * 74)
    print("THEORY CRUCIBLE 04: OBSERVABLE-MAP CLASSIFICATION")
    print("=" * 74)
    print(f"vacuum stabilizer order             : {len(stabilizer)}")
    print("line-module decomposition           : 2*1 + 2 + 3")
    print(f"Hom(lines, through permutation 1+2): {through_hom_dimension}")
    print(f"Hom(lines, irreducible flavour 3)   : {standard_hom_dimension}")
    print(f"canonical-map equivariance residual : {equivariance_residual:.3e}")
    print(f"pullback projector rank/trace       : 3 -> {Fraction(3, 7)} normalized")
    print(f"avoidance projector rank/trace      : 4 -> {Fraction(4, 7)} normalized")
    print()
    print("PROVED")
    print("  * A reducible three-flavour target (1+2) leaves three intertwiners.")
    print("  * The irreducible three-flavour target admits one intertwiner up to scale.")
    print("  * That unique map removes the uniform avoiding mode and pulls back to")
    print("    the rank-three zero-sum projector, whose normalized trace is 3/7.")
    print("  * The rank-four avoidance projector cannot be the pullback of an")
    print("    isometric map into a three-dimensional flavour space.")
    print()
    print("NOT PROVED")
    print("  * that physical flavour transforms as this irreducible stabilizer 3;")
    print("  * a no-go for nonlinear, density-matrix, or non-isometric maps;")
    print("  * a complete PMNS matrix or oscillation Hamiltonian.")
    print()
    print("VERDICT: equivariance gives either knobs (target 1+2) or a unique map")
    print("         whose canonical trace is 3/7, not the frozen upper value 4/7.")


if __name__ == "__main__":
    main()