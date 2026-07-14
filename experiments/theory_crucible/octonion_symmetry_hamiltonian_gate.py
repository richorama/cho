"""Classify Hamiltonians selected by octonion symmetry and one vacuum.

The quantum controls of Gate 12 span u(7), so selection must come from an
additional principle. This gate imposes the strongest neutral principle already
available: invariance under the exact finite signed-permutation automorphisms of
the octonion table. It then repeats the classification after selecting either an
unoriented vacuum line {+v,-v} or an oriented vacuum vector v.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/octonion_symmetry_hamiltonian_gate.py
"""

from __future__ import annotations

from itertools import product

import numpy as np

from associator_transport_dynamics_gate import line_generators
from fano_selection_no_go import act_on_point, automorphisms
from signed_fano_multiplication_census import (
    multiplication_table,
    signed_coordinate_transform,
)


VACUUM = 7


def finite_octonion_automorphisms(table: np.ndarray) -> tuple[np.ndarray, ...]:
    """All signed Fano-coordinate maps preserving the multiplication table."""
    result = []
    for matrix in automorphisms():
        permutation = {
            point: act_on_point(matrix, point) for point in range(1, 8)
        }
        for basis_signs in product((-1, 1), repeat=7):
            transformed = signed_coordinate_transform(
                table, permutation, basis_signs
            )
            if not np.array_equal(transformed, table):
                continue
            representation = np.zeros((7, 7))
            for source in range(1, 8):
                representation[permutation[source] - 1, source - 1] = (
                    basis_signs[source - 1]
                )
            result.append(representation)
    return tuple(result)


def commutant_dimension(group: tuple[np.ndarray, ...]) -> int:
    """Real dimension of matrices X satisfying RX=XR for every R."""
    matrix_units = []
    for row in range(7):
        for column in range(7):
            unit = np.zeros((7, 7))
            unit[row, column] = 1.0
            matrix_units.append(unit)
    constraints = np.vstack(
        [
            np.column_stack(
                [
                    (transform @ unit - unit @ transform).reshape(-1)
                    for unit in matrix_units
                ]
            )
            for transform in group
        ]
    )
    singular_values = np.linalg.svd(constraints, compute_uv=False)
    return int(np.count_nonzero(singular_values < 1e-9))


def commutes_with_group(matrix: np.ndarray, group: tuple[np.ndarray, ...]) -> bool:
    return all(
        np.linalg.norm(transform @ matrix - matrix @ transform) < 1e-12
        for transform in group
    )


def group_average(matrix: np.ndarray, group: tuple[np.ndarray, ...]) -> np.ndarray:
    return sum(
        (transform @ matrix @ transform.T for transform in group),
        np.zeros_like(matrix, dtype=float),
    ) / len(group)


def main() -> None:
    table = multiplication_table((1,) * 7)
    group = finite_octonion_automorphisms(table)
    assert len(group) == 1344
    assert len({tuple(matrix.reshape(-1)) for matrix in group}) == 1344
    assert all(np.array_equal(matrix.T @ matrix, np.eye(7)) for matrix in group)

    vacuum = np.eye(7)[:, VACUUM - 1]
    vacuum_projector = np.outer(vacuum, vacuum)
    complement_projector = np.eye(7) - vacuum_projector
    directed_stabilizer = tuple(
        matrix for matrix in group if np.array_equal(matrix @ vacuum, vacuum)
    )
    line_stabilizer = tuple(
        matrix
        for matrix in group
        if np.array_equal(np.abs(matrix @ vacuum), vacuum)
    )
    assert len(directed_stabilizer) == 96
    assert len(line_stabilizer) == 192

    full_dimension = commutant_dimension(group)
    line_dimension = commutant_dimension(line_stabilizer)
    directed_dimension = commutant_dimension(directed_stabilizer)
    assert (full_dimension, line_dimension, directed_dimension) == (1, 2, 3)

    identity = np.eye(7)
    vacuum_complex_structure = table[VACUUM, 1:, 1:].T.astype(float)
    assert np.array_equal(
        vacuum_complex_structure @ vacuum_complex_structure,
        -complement_projector,
    )
    assert np.array_equal(vacuum_complex_structure.T, -vacuum_complex_structure)
    assert np.array_equal(vacuum_complex_structure @ vacuum, np.zeros(7))

    assert commutes_with_group(identity, group)
    assert commutes_with_group(vacuum_projector, line_stabilizer)
    assert commutes_with_group(vacuum_complex_structure, directed_stabilizer)
    assert not commutes_with_group(vacuum_complex_structure, line_stabilizer)
    assert np.linalg.matrix_rank(
        np.column_stack(
            [
                identity.reshape(-1),
                vacuum_projector.reshape(-1),
                vacuum_complex_structure.reshape(-1),
            ]
        )
    ) == 3

    complex_spectrum = tuple(
        int(round(value))
        for value in np.linalg.eigvalsh(1j * vacuum_complex_structure)
    )
    assert complex_spectrum == (-1, -1, -1, 0, 1, 1, 1)

    transports = line_generators(table)
    projectors = tuple(-transport @ transport / 4.0 for transport in transports)
    assert all(
        np.linalg.norm(group_average(transport, group)) < 1e-12
        for transport in transports
    )
    assert all(
        np.linalg.norm(
            group_average(projector, group) - (4.0 / 7.0) * identity
        )
        < 1e-12
        for projector in projectors
    )
    assert np.array_equal(sum(projectors), 4.0 * identity)

    print("=" * 74)
    print("THEORY CRUCIBLE 13: OCTONION-SYMMETRY HAMILTONIAN SELECTION")
    print("=" * 74)
    print(f"finite octonion automorphisms        : {len(group)}")
    print(f"unoriented-vacuum stabilizer         : {len(line_stabilizer)}")
    print(f"oriented-vacuum stabilizer           : {len(directed_stabilizer)}")
    print(f"invariant matrix dimensions          : {full_dimension} -> {line_dimension} -> {directed_dimension}")
    print(f"full-symmetry Hamiltonians           : a I")
    print(f"unoriented-vacuum Hamiltonians       : a I + b P_v")
    print(f"oriented-vacuum Hamiltonians         : a I + b P_v + c i J_v")
    print(f"spectrum of i J_v                    : {complex_spectrum}")
    print(f"full average of every transport      : 0")
    print(f"full average of every projector      : (4/7) I")
    print()
    print("PROVED WITHIN THE FINITE AUTOMORPHISM WITNESS")
    print("  * Full octonion symmetry permits only a scalar Hamiltonian, hence only")
    print("    an unobservable global phase; it selects no dynamics.")
    print("  * An unoriented vacuum line permits one physical sector gap but no")
    print("    transfer between the vacuum and its six-dimensional complement.")
    print("  * Orienting the vacuum adds the canonical complex structure J_v. Its")
    print("    Hermitian generator i J_v splits the complement into two triplets.")
    print("  * After removing the global phase, the oriented-vacuum family still")
    print("    contains two free real coefficients, so symmetry does not select")
    print("    a unique Hamiltonian or timescale.")
    print()
    print("NOT PROVED")
    print("  * why a vacuum direction or its orientation is physically selected;")
    print("  * values for the two surviving gaps or a state-preparation rule;")
    print("  * that the two triplets are generations, flavours, or observed states.")
    print()
    print("VERDICT: the decisive trial does not produce a unique dynamics. Full")
    print("         symmetry is trivial; one oriented vacuum reveals a canonical")
    print("         1+3+3 spectral structure but leaves two physical knobs. This")
    print("         route stops unless an independent vacuum dynamics fixes them.")


if __name__ == "__main__":
    main()