"""Joint quantum control from associator transports and Gram projectors.

The seven signed transports M_l alone generate so(7), while the seven phase
generators i P_l, with P_l=-M_l^2/4, commute. This gate computes their real Lie
closure together and tests the same construction on every signed Fano product.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/associator_quantum_control_gate.py
"""

from __future__ import annotations

from itertools import combinations, product

import numpy as np

from associator_quantum_measurement_gate import is_orthogonal_projector
from associator_transport_dynamics_gate import line_generators
from signed_fano_multiplication_census import (
    multiplication_table,
    standard_signed_orbit,
)


def real_vector(matrix: np.ndarray) -> np.ndarray:
    return np.concatenate((matrix.real.reshape(-1), matrix.imag.reshape(-1)))


def independent_basis(matrices: list[np.ndarray], tolerance: float = 1e-9) -> list[np.ndarray]:
    basis: list[np.ndarray] = []
    orthonormal = np.empty((98, 0), dtype=float)
    for matrix in matrices:
        residual = real_vector(matrix).astype(float)
        if orthonormal.shape[1]:
            residual -= orthonormal @ (orthonormal.T @ residual)
        norm = np.linalg.norm(residual)
        if norm > tolerance:
            basis.append(matrix)
            orthonormal = np.column_stack((orthonormal, residual / norm))
    return basis


def lie_closure_dimensions(generators: list[np.ndarray]) -> tuple[int, ...]:
    basis = independent_basis(generators)
    dimensions = [len(basis)]
    while True:
        brackets = [
            first @ second - second @ first
            for first, second in combinations(basis, 2)
        ]
        enlarged = independent_basis(basis + brackets)
        dimensions.append(len(enlarged))
        if len(enlarged) == len(basis):
            return tuple(dimensions)
        basis = enlarged


def controls(table: np.ndarray) -> tuple[tuple[np.ndarray, ...], tuple[np.ndarray, ...]]:
    transports = line_generators(table)
    projectors = tuple(transport.T @ transport / 4.0 for transport in transports)
    return transports, projectors


def quantum_admissible(
    transports: tuple[np.ndarray, ...],
    projectors: tuple[np.ndarray, ...],
    tolerance: float = 1e-12,
) -> bool:
    return all(
        np.linalg.norm(transport.T + transport) < tolerance
        for transport in transports
    ) and all(
        is_orthogonal_projector(projector)
        and int(round(np.trace(projector))) == 4
        for projector in projectors
    )


def matched_random_controls(
    rng: np.random.Generator, template: np.ndarray
) -> tuple[np.ndarray, ...]:
    """Seven independent conjugates preserving M^T=-M and M^2=-4P."""
    controls = []
    for _ in range(7):
        matrix = rng.normal(size=(7, 7))
        frame, _ = np.linalg.qr(matrix)
        controls.append(frame @ template @ frame.T)
    return tuple(controls)


def main() -> None:
    octonion_orbit = standard_signed_orbit()
    admissible_signings = []
    closure_rows = []
    for signs in product((-1, 1), repeat=7):
        transports, projectors = controls(multiplication_table(signs))
        if not quantum_admissible(transports, projectors):
            continue
        admissible_signings.append(signs)
        closure_rows.append(
            (
                lie_closure_dimensions(list(transports)),
                lie_closure_dimensions([1j * projector for projector in projectors]),
                lie_closure_dimensions(
                    list(transports) + [1j * projector for projector in projectors]
                ),
            )
        )

    assert frozenset(admissible_signings) == octonion_orbit
    assert len(admissible_signings) == 16
    assert set(closure_rows) == {((7, 18, 21, 21), (7, 7), (14, 35, 49, 49))}

    standard_transports, standard_projectors = controls(
        multiplication_table((1,) * 7)
    )
    combined = list(standard_transports) + [
        1j * projector for projector in standard_projectors
    ]
    assert all(np.linalg.norm(generator.conj().T + generator) < 1e-12 for generator in combined)
    assert sum(np.trace(projector) for projector in standard_projectors) == 28
    assert np.array_equal(sum(standard_projectors), 4.0 * np.eye(7))

    rng = np.random.default_rng(20260714)
    random_closures = []
    for _ in range(8):
        random_transports = matched_random_controls(rng, standard_transports[0])
        random_projectors = tuple(
            -transport @ transport / 4.0 for transport in random_transports
        )
        assert quantum_admissible(random_transports, random_projectors)
        random_closures.append(
            lie_closure_dimensions(
                list(random_transports)
                + [1j * projector for projector in random_projectors]
            )
        )
    assert all(dimensions[-1] == 49 for dimensions in random_closures)

    print("=" * 74)
    print("THEORY CRUCIBLE 12: ASSOCIATOR QUANTUM-CONTROL CLOSURE")
    print("=" * 74)
    print(f"signed-Fano products tested          : 128")
    print(f"quantum-admissible products          : {len(admissible_signings)}")
    print(f"admissible products equal octonions  : {frozenset(admissible_signings) == octonion_orbit}")
    print(f"transport-only closure               : (7, 18, 21, 21) = so(7)")
    print(f"phase-only closure                   : (7, 7), commuting")
    print(f"combined closure                     : (14, 35, 49, 49) = u(7)")
    print(f"matched random controls reaching u(7): {sum(row[-1] == 49 for row in random_closures)} / {len(random_closures)}")
    print()
    print("PROVED WITHIN THE SIGNED-FANO CENSUS")
    print("  * Exactly the 16 octonion coordinate copies make every derived")
    print("    transport and projector a valid anti-Hermitian quantum generator.")
    print("  * Their transports and projector phases jointly generate all of u(7),")
    print("    so the derived package permits arbitrary seven-state unitary motion.")
    print("  * Spectrum-matched generic controls also reach u(7): universality alone")
    print("    is capability, not an octonion discriminator or prediction.")
    print()
    print("NOT PROVED")
    print("  * a law selecting one control sequence, angle, or initial state;")
    print("  * a physical interpretation of the seven complex amplitudes;")
    print("  * any measured mixing matrix or transition probability.")
    print()
    print("VERDICT: octonion multiplication uniquely supplies the complete valid")
    print("         control package in the matched signed-Fano family. The package")
    print("         is quantum-universal, but universality increases freedom until")
    print("         a symmetry or dynamics selects one evolution.")


if __name__ == "__main__":
    main()