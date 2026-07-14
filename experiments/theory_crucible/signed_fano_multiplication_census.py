"""Exhaustive signed-Fano multiplication census.

The unoriented Fano plane fixes which imaginary basis unit is the product of each
pair, but not the seven line orientations. This gate enumerates all 2^7 signings.
For each resulting eight-dimensional real algebra it checks, with exact integer
arithmetic:

* norm composition through L_i^T L_j + L_j^T L_i = 2 delta_ij I;
* alternativity through total antisymmetry of the basis associator;
* associativity versus genuine nonassociativity.

It then generates the full signed-coordinate orbit of the repository's standard
octonion table under all 168 Fano relabelings and all 2^7 imaginary-basis sign
changes. This determines whether every surviving table is merely the octonions in
different coordinates.

No physical constants or exceptional-group labels enter the selection criteria.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/signed_fano_multiplication_census.py
"""

from __future__ import annotations

from collections import Counter
from itertools import product

import numpy as np

from fano_selection_no_go import act_on_point, automorphisms


FANO_TRIPLES = (
    (1, 2, 3),
    (1, 4, 5),
    (1, 7, 6),
    (2, 4, 6),
    (2, 5, 7),
    (3, 4, 7),
    (3, 6, 5),
)


def multiplication_table(signs: tuple[int, ...]) -> np.ndarray:
    """Integer structure constants for one orientation of the Fano lines."""
    if len(signs) != len(FANO_TRIPLES) or any(sign not in (-1, 1) for sign in signs):
        raise ValueError("signs must contain seven values in {-1,+1}")

    table = np.zeros((8, 8, 8), dtype=np.int8)
    for index in range(8):
        table[0, index, index] = 1
        table[index, 0, index] = 1
    for index in range(1, 8):
        table[index, index, 0] = -1

    for sign, (left, right, result) in zip(signs, FANO_TRIPLES):
        for first, second, output in (
            (left, right, result),
            (right, result, left),
            (result, left, right),
        ):
            table[first, second, output] = sign
            table[second, first, output] = -sign
    return table


def left_multiplications(table: np.ndarray) -> tuple[np.ndarray, ...]:
    """Matrices for x -> e_i*x, with output coordinates on rows."""
    return tuple(table[index].T.astype(np.int64) for index in range(8))


def composition_residual(table: np.ndarray) -> int:
    """Exact residual of the bilinear norm-composition identities."""
    left = left_multiplications(table)
    identity = np.eye(8, dtype=np.int64)
    residual = 0
    for first in range(8):
        for second in range(8):
            target = 2 * identity if first == second else np.zeros((8, 8), dtype=np.int64)
            residual = max(
                residual,
                int(np.max(np.abs(left[first].T @ left[second] + left[second].T @ left[first] - target))),
            )
    return residual


def basis_associator(table: np.ndarray, first: int, second: int, third: int) -> np.ndarray:
    """Exact coordinates of (e_first e_second)e_third-e_first(e_second e_third)."""
    left_associated = np.einsum(
        "m,mk->k", table[first, second].astype(np.int64), table[:, third].astype(np.int64)
    )
    right_associated = np.einsum(
        "m,mk->k", table[second, third].astype(np.int64), table[first].astype(np.int64)
    )
    return left_associated - right_associated


def alternativity_residual(table: np.ndarray) -> int:
    """Associator is alternating iff adjacent transpositions reverse its sign."""
    residual = 0
    for first in range(8):
        for second in range(8):
            for third in range(8):
                associator = basis_associator(table, first, second, third)
                swap_first = basis_associator(table, second, first, third)
                swap_last = basis_associator(table, first, third, second)
                residual = max(
                    residual,
                    int(np.max(np.abs(associator + swap_first))),
                    int(np.max(np.abs(associator + swap_last))),
                )
    return residual


def associator_signature(table: np.ndarray) -> tuple[int, tuple[tuple[int, int], ...]]:
    """Count and squared-norm histogram of nonzero ordered basis associators."""
    squared_norms = []
    for first in range(1, 8):
        for second in range(1, 8):
            for third in range(1, 8):
                value = basis_associator(table, first, second, third)
                squared_norm = int(value @ value)
                if squared_norm:
                    squared_norms.append(squared_norm)
    histogram = tuple(sorted(Counter(squared_norms).items()))
    return len(squared_norms), histogram


def extract_signs(table: np.ndarray) -> tuple[int, ...]:
    """Read line orientations relative to FANO_TRIPLES."""
    return tuple(int(table[left, right, result]) for left, right, result in FANO_TRIPLES)


def signed_coordinate_transform(
    table: np.ndarray, point_permutation: dict[int, int], basis_signs: tuple[int, ...]
) -> np.ndarray:
    """Express a product table in a signed-permuted imaginary basis."""
    transformed = np.zeros_like(table)
    transformed[0, 0, 0] = 1
    permutation = (0,) + tuple(point_permutation[index] for index in range(1, 8))
    signs = (1,) + basis_signs
    inverse = {old: new for new, old in enumerate(permutation)}

    for first in range(8):
        for second in range(8):
            old_first = permutation[first]
            old_second = permutation[second]
            for old_output in range(8):
                coefficient = int(table[old_first, old_second, old_output])
                if coefficient:
                    new_output = inverse[old_output]
                    transformed[first, second, new_output] = (
                        coefficient * signs[first] * signs[second] * signs[new_output]
                    )
    return transformed


def standard_signed_orbit() -> frozenset[tuple[int, ...]]:
    """All line signings equivalent to the standard table by signed Fano coordinates."""
    standard = multiplication_table((1,) * 7)
    orbit = set()
    for matrix in automorphisms():
        point_permutation = {
            point: act_on_point(matrix, point) for point in range(1, 8)
        }
        for basis_signs in product((-1, 1), repeat=7):
            transformed = signed_coordinate_transform(
                standard, point_permutation, basis_signs
            )
            signs = extract_signs(transformed)
            assert all(sign in (-1, 1) for sign in signs)
            orbit.add(signs)
    return frozenset(orbit)


def main() -> None:
    rows = []
    for signs in product((-1, 1), repeat=7):
        table = multiplication_table(signs)
        composition = composition_residual(table)
        alternative = alternativity_residual(table)
        signature = associator_signature(table)
        rows.append((signs, composition, alternative, signature))

    composition_survivors = frozenset(
        signs for signs, composition, _, _ in rows if composition == 0
    )
    alternative_survivors = frozenset(
        signs for signs, _, alternative, _ in rows if alternative == 0
    )
    joint_survivors = composition_survivors & alternative_survivors
    standard_orbit = standard_signed_orbit()
    joint_signatures = {signature for signs, _, _, signature in rows if signs in joint_survivors}

    assert len(rows) == 128
    assert (1,) * 7 in joint_survivors
    assert joint_survivors
    assert joint_survivors == standard_orbit
    assert len(joint_signatures) == 1
    assert all(signature[0] > 0 for signature in joint_signatures)
    assert len(joint_survivors) < len(rows)

    print("=" * 74)
    print("THEORY CRUCIBLE 07: SIGNED-FANO MULTIPLICATION CENSUS")
    print("=" * 74)
    print(f"unoriented-incidence signings tested : {len(rows)}")
    print(f"norm-composition survivors           : {len(composition_survivors)}")
    print(f"alternativity survivors              : {len(alternative_survivors)}")
    print(f"joint survivors                      : {len(joint_survivors)}")
    print(f"standard signed-coordinate orbit     : {len(standard_orbit)}")
    print(f"survivors equal standard orbit       : {joint_survivors == standard_orbit}")
    print(f"survivor associator signature(s)     : {sorted(joint_signatures)}")
    print()
    print("PROVED WITHIN THE SIGNED-FANO FAMILY")
    print("  * Incidence alone permits 128 multiplication orientations.")
    print("  * Norm composition plus alternativity rejects every orientation outside")
    print("    the signed-coordinate orbit of the standard octonion table.")
    print("  * Every survivor is genuinely nonassociative with the same basis")
    print("    associator signature; the differences are coordinate conventions.")
    print()
    print("NOT PROVED")
    print("  * that norm composition and alternativity are selected by dynamics;")
    print("  * uniqueness among arbitrary real eight-dimensional products not sharing")
    print("    the Fano support pattern (Hurwitz addresses a broader theorem class);")
    print("  * any physical observable derived from the surviving associator.")
    print()
    print("VERDICT: the same incidence data that made 4/7 generic becomes")
    print("         octonion-specific only after neutral multiplication axioms are")
    print("         imposed. The next gate must test whether those axioms are stable")
    print("         outputs or simply a renamed octonion assumption.")


if __name__ == "__main__":
    main()