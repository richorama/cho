"""
Candidate CHO Yukawa/seesaw bridge operator.

This is a composite operator diagnostic, not a theorem. It puts the epsilon
trace, sector projectors, NNI cascade factors, Fano CKM phase, and PMNS seesaw
target into one auditable object. The remaining task is to derive the selected
projectors and perturbations from the CHO action, rather than choosing them as
the minimal operator components.
"""

from __future__ import annotations

from dataclasses import dataclass

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


OBSERVED = {
    "m_u": 2.16e-3,
    "m_d": 4.67e-3,
    "m_s": 93.4e-3,
    "m_c": 1.27,
    "m_b": 4.18,
    "m_t": 172.76,
    "m_e": 0.511e-3,
    "m_mu": 0.10566,
    "m_tau": 1.777,
    "V_us": 0.2243,
    "V_cb": 0.0422,
    "V_ub": 0.00382,
    "J_ckm": 3.08e-5,
    "sin2_theta13": 0.02203,
    "sin2_theta12": 0.307,
    "sin2_theta23": 0.572,
}


@dataclass(frozen=True)
class CHODimensions:
    dim_weyl: int = 16
    dim_jordan: int = 27
    dim_quaternion: int = 4
    dim_octonion: int = 8
    dim_imag_octonion: int = 7
    n_color: int = 3
    theta_break: float = np.pi

    @property
    def bridge_dim(self) -> int:
        return self.dim_weyl * self.dim_jordan


@dataclass(frozen=True)
class SectorDefinition:
    name: str
    projector_indices: tuple[int, ...]
    observed_first_over_third: float
    observed_second_over_third: float
    origin: str

    @property
    def rank(self) -> int:
        return len(self.projector_indices)


def pct_error(predicted: float, observed: float) -> float:
    return (predicted - observed) / observed * 100.0


def rank_one_projector(size: int, index: int = 0) -> np.ndarray:
    vector = np.zeros(size, dtype=complex)
    vector[index] = 1.0
    return np.outer(vector, np.conj(vector))


def diagonal_projector(size: int, indices: tuple[int, ...]) -> np.ndarray:
    projector = np.zeros((size, size), dtype=complex)
    for index in indices:
        projector[index, index] = 1.0
    return projector


def normalized_trace(matrix: np.ndarray) -> float:
    return float(np.trace(matrix).real / matrix.shape[0])


def fano_line_vector(line: tuple[int, int, int]) -> np.ndarray:
    vector = np.zeros(7, dtype=float)
    for unit in line:
        vector[unit - 1] = 1.0
    return vector


def fano_phase(line_a: tuple[int, int, int], line_b: tuple[int, int, int]) -> tuple[float, float]:
    vector_a = fano_line_vector(line_a)
    vector_b = fano_line_vector(line_b)
    overlap = float(np.dot(vector_a, vector_b) / (np.linalg.norm(vector_a) * np.linalg.norm(vector_b)))
    return overlap, float(np.arccos(overlap))


def fano_intersection(line_a: tuple[int, int, int], line_b: tuple[int, int, int]) -> tuple[int, tuple[int, ...]]:
    intersection = tuple(sorted(set(line_a).intersection(line_b)))
    return len(intersection), intersection


def generation_adjacency() -> np.ndarray:
    return np.array([
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ], dtype=int)


def fock_grade_indices() -> dict[str, tuple[int, ...]]:
    """Furey-style C tensor O ladder grades for one generation.

    The chosen vacuum omega = (1 + i e7)/2 defines three color ladder
    operators. Their exterior/Fock grades have dimensions C(3, k):
    1, 3, 3, 1, with total rank 8.
    """
    return {
        "vacuum_singlet": (0,),
        "single_ladder_triplet": (1, 2, 3),
        "double_ladder_triplet": (4, 5, 6),
        "triple_ladder_singlet": (7,),
        "full_fock_space": tuple(range(8)),
    }


def construct_fritzsch_matrix(masses: tuple[float, float, float], phase_a: float, phase_b: float) -> np.ndarray:
    m1, m2, m3 = masses
    c_entry = m1 - m2 + m3
    a_sq = m1 * m2 * m3 / c_entry
    s2 = -m1 * m2 + m1 * m3 - m2 * m3
    b_sq = -s2 - a_sq
    a_entry = np.sqrt(max(a_sq, 0.0)) * np.exp(1j * phase_a)
    b_entry = np.sqrt(max(b_sq, 0.0)) * np.exp(1j * phase_b)
    return np.array([
        [0.0, a_entry, 0.0],
        [np.conj(a_entry), 0.0, b_entry],
        [0.0, np.conj(b_entry), c_entry],
    ], dtype=complex)


def diagonalize_hermitian(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    eigenvalues, unitary = np.linalg.eigh(matrix)
    order = np.argsort(np.abs(eigenvalues))
    return eigenvalues[order], unitary[:, order]


def ckm_matrix_from_sines(s12_mag: float, s23_mag: float, s13_mag: float, delta: float) -> np.ndarray:
    c12 = np.sqrt(1.0 - s12_mag**2)
    c23 = np.sqrt(1.0 - s23_mag**2)
    c13 = np.sqrt(1.0 - s13_mag**2)
    phase_pos = np.exp(1j * delta)
    phase_neg = np.exp(-1j * delta)
    return np.array([
        [c12 * c13, s12_mag * c13, s13_mag * phase_neg],
        [
            -s12_mag * c23 - c12 * s23_mag * s13_mag * phase_pos,
            c12 * c23 - s12_mag * s23_mag * s13_mag * phase_pos,
            s23_mag * c13,
        ],
        [
            s12_mag * s23_mag - c12 * c23 * s13_mag * phase_pos,
            -c12 * s23_mag - s12_mag * c23 * s13_mag * phase_pos,
            c23 * c13,
        ],
    ], dtype=complex)


def mixing_matrix_from_angles(theta12: float, theta23: float, theta13: float, delta: float) -> np.ndarray:
    return ckm_matrix_from_sines(np.sin(theta12), np.sin(theta23), np.sin(theta13), delta)


def jarlskog(matrix: np.ndarray) -> float:
    return abs(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


def tbm_matrix() -> np.ndarray:
    return np.array([
        [2 / np.sqrt(6), 1 / np.sqrt(3), 0.0],
        [-1 / np.sqrt(6), 1 / np.sqrt(3), 1 / np.sqrt(2)],
        [1 / np.sqrt(6), -1 / np.sqrt(3), 1 / np.sqrt(2)],
    ], dtype=complex)


def majorana_matrix(yukawa: np.ndarray) -> np.ndarray:
    return yukawa @ yukawa.T


class CHOBridgeOperator:
    def __init__(self, dims: CHODimensions = CHODimensions()) -> None:
        self.dims = dims

    def epsilon_operator(self) -> np.ndarray:
        rank, _ = fano_intersection(FANO_LINES[0], FANO_LINES[1])
        projector = np.zeros((self.dims.bridge_dim, self.dims.bridge_dim), dtype=complex)
        for index in range(rank):
            projector[index, index] = 1.0
        return self.dims.theta_break * projector

    def epsilon_sq(self) -> float:
        return normalized_trace(self.epsilon_operator())

    def weak_shape_projector(self) -> np.ndarray:
        return rank_one_projector(self.dims.dim_quaternion)

    def weak_shape_trace(self) -> float:
        return normalized_trace(self.weak_shape_projector())

    def sectors(self) -> list[SectorDefinition]:
        grades = fock_grade_indices()
        return [
            SectorDefinition(
                "up",
                grades["vacuum_singlet"],
                OBSERVED["m_u"] / OBSERVED["m_t"],
                OBSERVED["m_c"] / OBSERVED["m_t"],
                "grade-0 singlet from omega=(1+i e7)/2",
            ),
            SectorDefinition(
                "down",
                grades["single_ladder_triplet"],
                OBSERVED["m_d"] / OBSERVED["m_b"],
                OBSERVED["m_s"] / OBSERVED["m_b"],
                "grade-1 color triplet from three alpha_i^dagger ladders",
            ),
            SectorDefinition(
                "lepton",
                grades["full_fock_space"],
                OBSERVED["m_e"] / OBSERVED["m_tau"],
                OBSERVED["m_mu"] / OBSERVED["m_tau"],
                "full eight-state Fock trace; still a Yukawa-trace assumption",
            ),
        ]

    def sector_projector(self, sector: SectorDefinition) -> np.ndarray:
        return diagonal_projector(self.dims.dim_octonion, sector.projector_indices)

    def sector_multiplicity(self, sector: SectorDefinition) -> float:
        return float(np.trace(self.sector_projector(sector)).real)

    def shape_factor(self, sector: SectorDefinition) -> float:
        weak = self.weak_shape_trace()
        if sector.name == "lepton":
            return weak / self.dims.theta_break
        return weak * self.sector_multiplicity(sector) ** 2

    def second_over_third(self, sector: SectorDefinition) -> float:
        return self.sector_multiplicity(sector) * self.epsilon_sq()

    def first_over_third(self, sector: SectorDefinition) -> float:
        q_value = self.second_over_third(sector)
        return self.shape_factor(sector) * q_value * q_value

    def fano_phase(self) -> tuple[float, float]:
        return fano_phase(FANO_LINES[0], FANO_LINES[1])

    def ckm_fritzsch_phase_diagnostic(self) -> tuple[np.ndarray, float]:
        _, phase = self.fano_phase()
        up = construct_fritzsch_matrix((OBSERVED["m_u"], OBSERVED["m_c"], OBSERVED["m_t"]), 0.0, 0.0)
        down = construct_fritzsch_matrix((OBSERVED["m_d"], OBSERVED["m_s"], OBSERVED["m_b"]), phase, 0.0)
        _, unitary_up = diagonalize_hermitian(up)
        _, unitary_down = diagonalize_hermitian(down)
        matrix = unitary_up.conj().T @ unitary_down
        return matrix, jarlskog(matrix)

    def ckm_magnitude_scaffold(self) -> tuple[np.ndarray, float]:
        _, phase = self.fano_phase()
        epsilon = np.sqrt(self.epsilon_sq())
        v_us = np.sqrt(self.dims.dim_imag_octonion) * epsilon
        v_cb = epsilon / 2.0
        v_ub = (np.sqrt(2.0) - 1.0) * v_us * v_cb
        c13 = np.sqrt(1.0 - v_ub**2)
        matrix = ckm_matrix_from_sines(v_us / c13, v_cb / c13, v_ub, phase)
        return matrix, jarlskog(matrix)

    def pmns_seesaw_target(self) -> dict[str, float | np.ndarray]:
        epsilon = np.sqrt(self.epsilon_sq())
        sin2_13 = self.dims.n_color * self.epsilon_sq()
        sin2_12 = 1.0 / (3.0 + np.sqrt(self.dims.dim_imag_octonion) * epsilon)
        sin2_23 = 4.0 / self.dims.dim_imag_octonion
        _, phase = self.fano_phase()
        delta = np.pi + phase
        theta12 = np.arcsin(np.sqrt(sin2_12))
        theta23 = np.arcsin(np.sqrt(sin2_23))
        theta13 = np.arcsin(np.sqrt(sin2_13))
        corrected = mixing_matrix_from_angles(theta12, theta23, theta13, delta)
        tbm = tbm_matrix()
        light_masses = np.array([0.0, 2.0 * epsilon, 1.0])
        sqrt_masses = np.diag(np.sqrt(light_masses))
        y_tbm = tbm @ sqrt_masses
        y_corr = corrected @ sqrt_masses
        m_tbm = majorana_matrix(y_tbm)
        m_corr = majorana_matrix(y_corr)
        delta_m = m_corr - m_tbm
        return {
            "sin2_theta13": sin2_13,
            "sin2_theta12": sin2_12,
            "sin2_theta23": sin2_23,
            "delta": delta,
            "yukawa_tbm": y_tbm,
            "yukawa_corrected": y_corr,
            "delta_m": delta_m,
            "delta_m_norm_ratio": float(np.linalg.norm(delta_m) / np.linalg.norm(m_tbm)),
            "delta_y_norm_ratio": float(np.linalg.norm(y_corr - y_tbm) / np.linalg.norm(y_tbm)),
        }


def print_operator_header(operator: CHOBridgeOperator) -> None:
    dims = operator.dims
    print("CANDIDATE CHO YUKAWA/SEESAW BRIDGE OPERATOR")
    print("=" * 78)
    print("Composite components")
    print("-" * 78)
    print("H_triality = pi |tau><tau| on A_Weyl x J3(O)")
    print("P_sector   = Fock-grade projectors with traces 1, 3, 8")
    print("W_H        = rank-one quaternionic weak/Higgs projector with normalized trace 1/4")
    print("A_gen      = one-step generation adjacency path 1 <-> 2 <-> 3")
    print("Phi_Fano   = relative phase from adjacent Fano lines")
    print("M_nu       = Y_nu M_R^-1 Y_nu^T, shown here with normalized M_R = I")
    print()
    print(f"Bridge trace dimension = {dims.dim_weyl} * {dims.dim_jordan} = {dims.bridge_dim}")
    print()


def print_epsilon_component(operator: CHOBridgeOperator) -> None:
    h_triality = operator.epsilon_operator()
    fano_rank, intersection = fano_intersection(FANO_LINES[0], FANO_LINES[1])
    print("Epsilon trace component")
    print("-" * 78)
    print(f"adjacent Fano-line intersection = {intersection}")
    print(f"intersection rank              = {fano_rank}")
    print(f"rank(H_triality/pi) = {np.linalg.matrix_rank(h_triality / operator.dims.theta_break)}")
    print("bridge-rank factorization = Weyl rank 1 x Jordan/Fano rank 1 (assumed)")
    print(f"if Weyl rank stayed 16: pi*16/432 = {np.pi * 16.0 / operator.dims.bridge_dim:.10f}")
    print(f"Tr(H_triality)      = {np.trace(h_triality).real:.10f}")
    print(f"Tr(H)/dim           = {operator.epsilon_sq():.10f}")
    print(f"target pi/432       = {np.pi / 432.0:.10f}")
    print()


def print_generation_component() -> None:
    adjacency = generation_adjacency()
    print("Generation adjacency component")
    print("-" * 78)
    for row in adjacency:
        print("  " + " ".join(str(value) for value in row))
    print(f"direct M13 entry       = {adjacency[0, 2]}")
    print(f"two-step 1->3 paths    = {(adjacency @ adjacency)[0, 2]}")
    print()


def print_sector_component(operator: CHOBridgeOperator) -> None:
    print("Sector projectors and NNI cascade")
    print("-" * 78)
    print(f"weak normalized trace = {operator.weak_shape_trace():.6f}")
    header = f"{'sector':<8} {'Tr(P)':>6} {'shape k':>12} {'m2/m3':>12} {'m1/m3':>12} {'obs m1/m3':>12} {'err':>8}"
    print(header)
    print("-" * len(header))
    for sector in operator.sectors():
        first = operator.first_over_third(sector)
        print(
            f"{sector.name:<8} "
            f"{operator.sector_multiplicity(sector):>6.1f} "
            f"{operator.shape_factor(sector):>12.6f} "
            f"{operator.second_over_third(sector):>12.6e} "
            f"{first:>12.6e} "
            f"{sector.observed_first_over_third:>12.6e} "
            f"{pct_error(first, sector.observed_first_over_third):>+7.1f}%"
        )
    print()
    print("Projector origins:")
    for sector in operator.sectors():
        print(f"  {sector.name:<8} {sector.origin}")
    print()
    print("Interpretation: the 1 and 3 ranks now come from the chosen Fock-grade representation; proving that the CHO Yukawa map must use these grades remains open.")
    print("The lepton rank-8 trace is still the strongest assumption: it uses the full Fock space rather than a derived charged-lepton ideal.")
    print()


def print_ckm_component(operator: CHOBridgeOperator) -> None:
    overlap, phase = operator.fano_phase()
    print("CKM phase-placement diagnostics")
    print("-" * 78)
    print(f"adjacent Fano lines: {FANO_LINES[0]} and {FANO_LINES[1]}")
    print(f"normalized incidence overlap = {overlap:.6f}")
    print(f"phase = arccos(overlap)     = {np.degrees(phase):.3f} deg")
    print()
    fritzsch, j_fritzsch = operator.ckm_fritzsch_phase_diagnostic()
    scaffold, j_scaffold = operator.ckm_magnitude_scaffold()
    rows = [
        ("Fritzsch phase", fritzsch, j_fritzsch, "uses observed masses; J works, V_cb high"),
        ("CHO magnitudes", scaffold, j_scaffold, "magnitudes work; J phase placement high"),
    ]
    print(f"{'projection':<16} {'V_us':>9} {'V_cb':>9} {'V_ub':>9} {'J':>12}  status")
    for name, matrix, invariant, note in rows:
        abs_matrix = np.abs(matrix)
        print(
            f"{name:<16} "
            f"{abs_matrix[0, 1]:>9.6f} "
            f"{abs_matrix[1, 2]:>9.6f} "
            f"{abs_matrix[0, 2]:>9.6f} "
            f"{invariant:>12.4e}  {note}"
        )
    print(f"{'observed':<16} {OBSERVED['V_us']:>9.6f} {OBSERVED['V_cb']:>9.6f} {OBSERVED['V_ub']:>9.6f} {OBSERVED['J_ckm']:>12.4e}")
    print()
    print("Interpretation: Fano incidence derives the phase. A full operator must still reconcile the Fritzsch J placement with corrected CKM magnitudes.")
    print()


def print_pmns_component(operator: CHOBridgeOperator) -> None:
    target = operator.pmns_seesaw_target()
    print("PMNS seesaw target")
    print("-" * 78)
    for key in ["sin2_theta13", "sin2_theta12", "sin2_theta23"]:
        value = float(target[key])
        print(f"{key:<14} target={value:.6f} observed={OBSERVED[key]:.6f} err={pct_error(value, OBSERVED[key]):+.2f}%")
    print(f"delta_PMNS     target={np.degrees(float(target['delta'])):.3f} deg")
    print(f"||Delta Y||/||Y_TBM|| = {target['delta_y_norm_ratio']:.3f}")
    print(f"||Delta M||/||M_TBM|| = {target['delta_m_norm_ratio']:.3f}")
    print()
    print("DeltaM / epsilon0 target:")
    scaled = target["delta_m"] / np.sqrt(operator.epsilon_sq())
    assert isinstance(scaled, np.ndarray)
    for row in scaled:
        print("  [" + ", ".join(f"{value.real:+.4f}{value.imag:+.4f}i" for value in row) + "]")
    print()
    print("Interpretation: the seesaw factorization is explicit; deriving DeltaY from broken triality remains open.")
    print()


def print_status() -> None:
    print("Status")
    print("-" * 78)
    print("Promotes:")
    print("  - epsilon0, sector traces, shape factors, Fano phase, and PMNS target now sit in one composite operator diagnostic.")
    print("  - the operator gives concrete projectors and perturbation matrices to derive or falsify.")
    print("Still open:")
    print("  - derive the rank-one transition, including Weyl rank one and Jordan/Fano embedding, from the CHO action.")
    print("  - derive the sector projectors and lepton 1/pi average from the CHO action.")
    print("  - produce one diagonalization that gives both corrected CKM magnitudes and the Fritzsch-level Jarlskog placement.")
    print("  - derive the PMNS DeltaY perturbation dynamically from broken triality, not from target angles.")


def main() -> None:
    operator = CHOBridgeOperator()
    print_operator_header(operator)
    print_epsilon_component(operator)
    print_generation_component()
    print_sector_component(operator)
    print_ckm_component(operator)
    print_pmns_component(operator)
    print_status()


if __name__ == "__main__":
    main()
