"""
Gap audit for the candidate CHO bridge operator.

This script quantifies the remaining proof gaps instead of treating them as
wording caveats. It is intentionally diagnostic: a successful run is not a proof
that the gaps are solved.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


OBSERVED = {
    "m_u": 2.16e-3,
    "m_d": 4.67e-3,
    "m_s": 93.4e-3,
    "m_c": 1.27,
    "m_b": 4.18,
    "m_t": 172.76,
    "V_us": 0.2243,
    "V_cb": 0.0422,
    "V_ub": 0.00382,
    "J": 3.08e-5,
}

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
class CKMScanResult:
    name: str
    parameters: tuple[float, ...]
    values: dict[str, float]
    score: float


def pct_error(predicted: float, observed: float) -> float:
    return (predicted - observed) / observed * 100.0


def fano_intersection_rank(line_a: tuple[int, int, int], line_b: tuple[int, int, int]) -> tuple[int, tuple[int, ...]]:
    intersection = tuple(sorted(set(line_a).intersection(line_b)))
    return len(intersection), intersection


def construct_nni_matrix(masses: tuple[float, float, float], phase_a: float, phase_b: float, d_frac: float) -> np.ndarray | None:
    m1, m2, m3 = masses
    d_entry = d_frac * (m1 - m2)
    c_entry = (m1 - m2 + m3) - d_entry
    if c_entry <= 0:
        return None
    a_sq = m1 * m2 * m3 / c_entry
    s2 = -m1 * m2 + m1 * m3 - m2 * m3
    b_sq = d_entry * c_entry - a_sq - s2
    if a_sq < 0.0 or b_sq < 0.0:
        return None
    a_entry = np.sqrt(a_sq) * np.exp(1j * phase_a)
    b_entry = np.sqrt(b_sq) * np.exp(1j * phase_b)
    return np.array([
        [0.0, a_entry, 0.0],
        [np.conj(a_entry), d_entry, b_entry],
        [0.0, np.conj(b_entry), c_entry],
    ], dtype=complex)


def diagonalize_hermitian(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    order = np.argsort(np.abs(eigenvalues))
    return eigenvalues[order], eigenvectors[:, order]


def jarlskog(matrix: np.ndarray) -> float:
    return abs(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


def ckm_values(matrix: np.ndarray) -> dict[str, float]:
    abs_matrix = np.abs(matrix)
    return {
        "V_us": float(abs_matrix[0, 1]),
        "V_cb": float(abs_matrix[1, 2]),
        "V_ub": float(abs_matrix[0, 2]),
        "J": jarlskog(matrix),
    }


def ckm_score(values: dict[str, float]) -> float:
    return float(sum(((values[key] - OBSERVED[key]) / OBSERVED[key]) ** 2 for key in ["V_us", "V_cb", "V_ub", "J"]))


def ckm_from_nni(d_up: float, d_down: float, phase_split: float, delta: float) -> dict[str, float] | None:
    up = construct_nni_matrix((OBSERVED["m_u"], OBSERVED["m_c"], OBSERVED["m_t"]), 0.0, 0.0, d_up)
    down = construct_nni_matrix(
        (OBSERVED["m_d"], OBSERVED["m_s"], OBSERVED["m_b"]),
        phase_split * delta,
        (phase_split - 1.0) * delta,
        d_down,
    )
    if up is None or down is None:
        return None
    _, unitary_up = diagonalize_hermitian(up)
    _, unitary_down = diagonalize_hermitian(down)
    return ckm_values(unitary_up.conj().T @ unitary_down)


def scan_common_deformation(delta: float) -> CKMScanResult:
    best = CKMScanResult("common D and phase split", (0.0, 0.0), {}, float("inf"))
    for d_frac in np.linspace(-1.0, 2.0, 301):
        for phase_split in np.linspace(0.0, 1.0, 101):
            values = ckm_from_nni(d_frac, d_frac, phase_split, delta)
            if values is None:
                continue
            score = ckm_score(values)
            if score < best.score:
                best = CKMScanResult("common D and phase split", (float(d_frac), float(phase_split)), values, score)
    return best


def scan_sector_deformation(delta: float) -> CKMScanResult:
    best = CKMScanResult("sector D, fixed Fano phase placement", (0.0, 0.0), {}, float("inf"))
    for d_up in np.linspace(-1.0, 2.0, 241):
        for d_down in np.linspace(-1.0, 2.0, 241):
            values = ckm_from_nni(d_up, d_down, 1.0, delta)
            if values is None:
                continue
            score = ckm_score(values)
            if score < best.score:
                best = CKMScanResult("sector D, fixed Fano phase placement", (float(d_up), float(d_down)), values, score)
    return best


def mixing_matrix(theta12: float, theta23: float, theta13: float, delta: float) -> np.ndarray:
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


def tbm_matrix() -> np.ndarray:
    return np.array([
        [2 / np.sqrt(6), 1 / np.sqrt(3), 0.0],
        [-1 / np.sqrt(6), 1 / np.sqrt(3), 1 / np.sqrt(2)],
        [1 / np.sqrt(6), -1 / np.sqrt(3), 1 / np.sqrt(2)],
    ], dtype=complex)


def pmns_delta_matrix() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    epsilon = np.sqrt(np.pi / (16 * 27))
    delta = np.pi + np.arccos(1.0 / 3.0)
    sin2_13 = 3.0 * epsilon**2
    sin2_12 = 1.0 / (3.0 + np.sqrt(7.0) * epsilon)
    sin2_23 = 4.0 / 7.0
    corrected = mixing_matrix(np.arcsin(np.sqrt(sin2_12)), np.arcsin(np.sqrt(sin2_23)), np.arcsin(np.sqrt(sin2_13)), delta)
    tbm = tbm_matrix()
    masses = np.array([0.0, 2.0 * epsilon, 1.0])
    m_tbm = tbm @ np.diag(masses) @ tbm.T
    m_corr = corrected @ np.diag(masses) @ corrected.T
    return m_tbm, m_corr, m_corr - m_tbm


def print_rank_and_projector_gaps() -> None:
    print("RANK AND PROJECTOR GAPS")
    print("=" * 78)
    rank, intersection = fano_intersection_rank(FANO_LINES[0], FANO_LINES[1])
    print(f"Adjacent Fano lines {FANO_LINES[0]} and {FANO_LINES[1]} intersect in {intersection}; rank = {rank}.")
    print("This makes a rank-one adjacent overlap natural, but it does not yet prove the bridge projector on A_Weyl x J3(O).")
    print()
    print("Sector projectors currently use ranks 1, 3, and 8.")
    print("They are still selected by the candidate basis; no minimal-ideal derivation exists in this repo yet.")
    print("The lepton 1/pi factor is likewise still an inserted coset-average target, not an evaluated measure integral.")
    print()


def print_ckm_gap() -> None:
    print("CKM RECONCILIATION GAP")
    print("=" * 78)
    delta = np.arccos(1.0 / 3.0)
    results = [scan_common_deformation(delta), scan_sector_deformation(delta)]
    print(f"Fixed phase: arccos(1/3) = {np.degrees(delta):.3f} deg")
    print(f"{'scan':<36} {'params':<24} {'V_us':>8} {'V_cb':>8} {'V_ub':>8} {'J':>11} {'score':>9}")
    for result in results:
        values = result.values
        print(
            f"{result.name:<36} "
            f"{str(tuple(round(value, 4) for value in result.parameters)):<24} "
            f"{values['V_us']:>8.5f} "
            f"{values['V_cb']:>8.5f} "
            f"{values['V_ub']:>8.5f} "
            f"{values['J']:>11.4e} "
            f"{result.score:>9.3f}"
        )
    print(f"{'observed':<36} {'':<24} {OBSERVED['V_us']:>8.5f} {OBSERVED['V_cb']:>8.5f} {OBSERVED['V_ub']:>8.5f} {OBSERVED['J']:>11.4e}")
    print()
    print("Conclusion: simple diagonal NNI deformations at fixed Fano phase do not solve the CKM problem.")
    print("A real CHO operator must change the texture more structurally or derive a different phase placement.")
    print()


def print_pmns_gap() -> None:
    print("PMNS PERTURBATION GAP")
    print("=" * 78)
    m_tbm, _, delta_m = pmns_delta_matrix()
    epsilon = np.sqrt(np.pi / (16 * 27))
    singular_values = np.linalg.svd(delta_m, compute_uv=False)
    cyclic = np.array([
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 0],
    ], dtype=complex)
    delta_z3_residual = np.linalg.norm(cyclic.T @ delta_m @ cyclic - delta_m) / np.linalg.norm(delta_m)
    tbm_z3_residual = np.linalg.norm(cyclic.T @ m_tbm @ cyclic - m_tbm) / np.linalg.norm(m_tbm)
    print("singular values of DeltaM / epsilon0:")
    print("  " + ", ".join(f"{value / epsilon:.4f}" for value in singular_values))
    print(f"numerical rank of DeltaM: {np.sum(singular_values > 1e-10)}")
    print(f"cyclic-Z3 residual for DeltaM: {delta_z3_residual:.3f}")
    print(f"cyclic-Z3 residual for M_TBM:  {tbm_z3_residual:.3f}")
    print()
    print("Conclusion: the current PMNS perturbation is a full-rank target matrix reverse-engineered from angles.")
    print("Also, the simple cyclic permutation is not the residual symmetry of the TBM mass matrix in this basis;")
    print("the symmetry language should be residual TBM/Klein plus broken triality unless a true Z3 action is constructed.")
    print()


def print_continuum_gap() -> None:
    print("CONTINUUM/RG GAP")
    print("=" * 78)
    items = [
        "alpha: lattice-to-continuum matching and vacuum-polarization thresholds",
        "sin^2(theta_W): matching scale and threshold derivation",
        "M_W: derivation of each hierarchy factor and normalization without using v",
        "Lambda: free-energy/path-integral factorization and 11/12 screening factor",
    ]
    for item in items:
        print(f"- {item}")
    print("These are outside the current Yukawa/seesaw operator files and need separate continuum/RG artifacts.")


def main() -> None:
    print_rank_and_projector_gaps()
    print_ckm_gap()
    print_pmns_gap()
    print_continuum_gap()


if __name__ == "__main__":
    main()
