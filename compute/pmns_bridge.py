"""
PMNS bridge scaffold.

This script derives the leading tribimaximal pattern from residual symmetry
generators and turns the corrected CHO PMNS formulas into an explicit
broken-triality Majorana mass-matrix target.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Inputs:
    dim_complex_algebra: int = 16
    dim_jordan: int = 27
    dim_imag_octonion: int = 7
    n_color: int = 3

    @property
    def epsilon_sq(self) -> float:
        return np.pi / (self.dim_complex_algebra * self.dim_jordan)

    @property
    def epsilon(self) -> float:
        return np.sqrt(self.epsilon_sq)

    @property
    def fano_phase(self) -> float:
        return np.arccos(1.0 / 3.0)


OBSERVED = {
    "sin2_theta13": 0.02203,
    "sin2_theta12": 0.307,
    "sin2_theta23": 0.572,
}


def pct_error(predicted: float, observed: float) -> float:
    return (predicted - observed) / observed * 100.0


def tbm_matrix() -> np.ndarray:
    """PDG-aligned tribimaximal mixing matrix with columns v1, v2, v3."""
    return np.array([
        [2 / np.sqrt(6), 1 / np.sqrt(3), 0.0],
        [-1 / np.sqrt(6), 1 / np.sqrt(3), 1 / np.sqrt(2)],
        [1 / np.sqrt(6), -1 / np.sqrt(3), 1 / np.sqrt(2)],
    ], dtype=complex)


def mixing_matrix_from_angles(theta12: float, theta23: float, theta13: float, delta: float) -> np.ndarray:
    c12, s12 = np.cos(theta12), np.sin(theta12)
    c23, s23 = np.cos(theta23), np.sin(theta23)
    c13, s13 = np.cos(theta13), np.sin(theta13)
    phase_pos = np.exp(1j * delta)
    phase_neg = np.exp(-1j * delta)
    return np.array([
        [c12 * c13, s12 * c13, s13 * phase_neg],
        [-s12 * c23 - c12 * s23 * s13 * phase_pos, c12 * c23 - s12 * s23 * s13 * phase_pos, s23 * c13],
        [s12 * s23 - c12 * c23 * s13 * phase_pos, -c12 * s23 - s12 * c23 * s13 * phase_pos, c23 * c13],
    ], dtype=complex)


def majorana_matrix(masses: np.ndarray, mixing: np.ndarray) -> np.ndarray:
    """Return M_nu = U diag(m_i) U^T for Majorana neutrinos."""
    return mixing @ np.diag(masses) @ mixing.T


def residual_reflections(mixing: np.ndarray) -> list[np.ndarray]:
    """Reflections G_i = 2 v_i v_i^dagger - I for the mixing columns."""
    identity = np.eye(3, dtype=complex)
    return [2.0 * np.outer(mixing[:, i], np.conj(mixing[:, i])) - identity for i in range(3)]


def corrected_angles(inputs: Inputs) -> tuple[float, float, float, float]:
    sin2_13 = inputs.n_color * inputs.epsilon_sq
    sin2_12 = 1.0 / (3.0 + np.sqrt(inputs.dim_imag_octonion) * inputs.epsilon)
    sin2_23 = 4.0 / inputs.dim_imag_octonion
    delta = np.pi + inputs.fano_phase
    return np.arcsin(np.sqrt(sin2_12)), np.arcsin(np.sqrt(sin2_23)), np.arcsin(np.sqrt(sin2_13)), delta


def print_tbm_derivation() -> np.ndarray:
    print("PMNS BRIDGE: TBM RESIDUAL SYMMETRIES")
    print("=" * 78)
    mixing = tbm_matrix()
    masses = np.array([0.0, 0.2, 1.0])
    mass_matrix = majorana_matrix(masses, mixing)
    print("U_TBM columns:")
    for index in range(3):
        column = mixing[:, index]
        print("  v{} = [".format(index + 1) + ", ".join(f"{value.real:+.6f}" for value in column) + "]")
    print()
    print("Residual invariance checks ||G_i^T M G_i - M||:")
    for index, generator in enumerate(residual_reflections(mixing), 1):
        residual = generator.T @ mass_matrix @ generator - mass_matrix
        print(f"  G{index}: {np.linalg.norm(residual):.3e}")
    print()
    print("Derived leading angles: sin^2(theta12)=1/3, sin^2(theta23)=1/2, sin^2(theta13)=0")
    print()
    return mixing


def print_corrected_target(inputs: Inputs, tbm: np.ndarray) -> None:
    print("Broken-triality corrected PMNS target")
    print("-" * 78)
    theta12, theta23, theta13, delta = corrected_angles(inputs)
    corrected = mixing_matrix_from_angles(theta12, theta23, theta13, delta)
    sin2_values = {
        "sin2_theta13": np.sin(theta13) ** 2,
        "sin2_theta12": np.sin(theta12) ** 2,
        "sin2_theta23": np.sin(theta23) ** 2,
    }
    for key, value in sin2_values.items():
        print(f"{key:<14} target={value:.6f} observed={OBSERVED[key]:.6f} err={pct_error(value, OBSERVED[key]):+.2f}%")
    print(f"delta target = {np.degrees(delta):.3f} deg")
    print()

    masses = np.array([0.0, 2.0 * inputs.epsilon, 1.0])
    m_tbm = majorana_matrix(masses, tbm)
    m_corr = majorana_matrix(masses, corrected)
    delta_m = m_corr - m_tbm
    print("Normalized Majorana mass perturbation DeltaM / epsilon:")
    scaled = delta_m / inputs.epsilon
    for row in scaled:
        print("  [" + ", ".join(f"{value.real:+.4f}{value.imag:+.4f}i" for value in row) + "]")
    print()
    print(f"||DeltaM|| / ||M_TBM|| = {np.linalg.norm(delta_m) / np.linalg.norm(m_tbm):.3f}")
    print("Status: this perturbation is the broken-triality operator target; it is not yet derived from CHO.")
    print()


def print_proof_obligations() -> None:
    print("Proof obligations")
    print("-" * 78)
    obligations = [
        "Derive the TBM residual symmetries from the unbroken triality/Majorana sector.",
        "Construct the broken-triality seesaw perturbation whose matrix equals DeltaM above.",
        "Show why the perturbation entries scale as epsilon0 and epsilon0^2 in the required places.",
        "Derive the 4/7 atmospheric factor dynamically from Im(O), not as a chosen angle.",
        "Connect the same perturbation to Delta m21^2 / Delta m31^2 = 4 epsilon0^2.",
    ]
    for index, obligation in enumerate(obligations, 1):
        print(f"{index}. {obligation}")


def main() -> None:
    inputs = Inputs()
    tbm = print_tbm_derivation()
    print_corrected_target(inputs, tbm)
    print_proof_obligations()


if __name__ == "__main__":
    main()
