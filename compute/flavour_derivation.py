"""
CHO flavour derivation scaffold.

This script is deliberately stricter than the exploratory flavour scripts:
it starts from algebraic CHO inputs, builds the first-generation NNI bridge
factors, constructs CKM/PMNS unitary matrices from the resulting rules, and
only then compares with experimental values.

It is not the final operator proof. It makes the operator gap explicit:
the first-generation NNI factors are encoded as bridge rules, and the CKM
Jarlskog invariant still depends on how the Fano phase is placed in the full
NNI mass matrices.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class CHOInputs:
    """Algebraic inputs used by the flavour scaffold."""

    dim_complex_algebra: int = 16
    dim_jordan: int = 27
    n_color: int = 3
    dim_octonion: int = 8
    dim_imag_octonion: int = 7
    sin2_theta_w_tree: float = 0.25

    @property
    def epsilon_sq(self) -> float:
        return np.pi / (self.dim_complex_algebra * self.dim_jordan)

    @property
    def epsilon(self) -> float:
        return np.sqrt(self.epsilon_sq)

    @property
    def fano_phase(self) -> float:
        return np.arccos(1.0 / 3.0)


@dataclass(frozen=True)
class SectorRule:
    """One charged-sector rule in dimensionless m3-normalized units."""

    name: str
    second_over_third: float
    nni_factor: float
    nni_factor_label: str
    observed_first_over_third: float
    observed_second_over_third: float

    @property
    def first_over_third(self) -> float:
        return self.nni_factor * self.second_over_third**2

    @property
    def nni_ratio(self) -> float:
        return self.first_over_third / self.second_over_third**2


INPUTS = CHOInputs()


# Experimental values are intentionally isolated for final comparison only.
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
    "V_ub": 0.00394,
    "J_ckm": 3.08e-5,
    "sin2_theta13": 0.02203,
    "sin2_theta12": 0.307,
    "sin2_theta23": 0.572,
}


def pct_error(predicted: float, observed: float) -> float:
    return (predicted - observed) / observed * 100.0


def ckm_matrix_from_sines(s12_mag: float, s23_mag: float, s13_mag: float, delta: float) -> np.ndarray:
    """Return the PDG-parameterized CKM/PMNS unitary matrix."""
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


def jarlskog(matrix: np.ndarray) -> float:
    """Compute the Jarlskog invariant for a unitary mixing matrix."""
    return abs(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


def derive_sector_rules(inputs: CHOInputs = INPUTS) -> list[SectorRule]:
    """Derive dimensionless charged-sector spectra from CHO bridge rules."""
    eps2 = inputs.epsilon_sq
    tree = inputs.sin2_theta_w_tree
    n_color = inputs.n_color
    dim_o = inputs.dim_octonion

    return [
        SectorRule(
            name="up",
            second_over_third=eps2,
            nni_factor=tree,
            nni_factor_label="sin2(theta_W)_tree = 1/4",
            observed_first_over_third=OBSERVED["m_u"] / OBSERVED["m_t"],
            observed_second_over_third=OBSERVED["m_c"] / OBSERVED["m_t"],
        ),
        SectorRule(
            name="down",
            second_over_third=n_color * eps2,
            nni_factor=n_color**2 * tree,
            nni_factor_label="N_c^2 sin2(theta_W)_tree = 9/4",
            observed_first_over_third=OBSERVED["m_d"] / OBSERVED["m_b"],
            observed_second_over_third=OBSERVED["m_s"] / OBSERVED["m_b"],
        ),
        SectorRule(
            name="lepton",
            second_over_third=dim_o * eps2,
            nni_factor=tree / np.pi,
            nni_factor_label="sin2(theta_W)_tree / pi = 1/(4pi)",
            observed_first_over_third=OBSERVED["m_e"] / OBSERVED["m_tau"],
            observed_second_over_third=OBSERVED["m_mu"] / OBSERVED["m_tau"],
        ),
    ]


def nni_bridge_matrix(rule: SectorRule) -> np.ndarray:
    """
    Build the minimal nearest-neighbor amplitude matrix for a sector.

    This is not claimed to be the final Yukawa operator. It is a compact
    representation of the bridge rule: M13 = 0 and |A/C|^2 = nni_factor.
    The matrix is useful because it makes the operator gap testable: a future
    full CHO Yukawa operator should reduce to this adjacent-transition pattern.
    """
    a_over_c = np.sqrt(rule.nni_factor)
    return np.array([
        [0.0, a_over_c, 0.0],
        [a_over_c, 0.0, 1.0],
        [0.0, 1.0, 0.0],
    ])


def ckm_predictions(inputs: CHOInputs = INPUTS) -> dict[str, float | np.ndarray]:
    """Construct the CKM unitary matrix from CHO magnitude rules."""
    eps = inputs.epsilon
    v_us = np.sqrt(inputs.dim_imag_octonion) * eps
    v_cb = eps / 2.0
    v_ub = (np.sqrt(2.0) - 1.0) * v_us * v_cb

    # In the PDG parameterization, |V_us| = s12 c13 and |V_cb| = s23 c13.
    c13 = np.sqrt(1.0 - v_ub**2)
    s12 = v_us / c13
    s23 = v_cb / c13
    matrix = ckm_matrix_from_sines(s12, s23, v_ub, inputs.fano_phase)

    return {
        "V_us": abs(matrix[0, 1]),
        "V_cb": abs(matrix[1, 2]),
        "V_ub": abs(matrix[0, 2]),
        "J_unitary": jarlskog(matrix),
        "delta": inputs.fano_phase,
        "matrix": matrix,
    }


def pmns_predictions(inputs: CHOInputs = INPUTS) -> dict[str, float | np.ndarray]:
    """Construct the PMNS unitary matrix from corrected-TBM CHO rules."""
    eps = inputs.epsilon
    sin2_13 = inputs.n_color * inputs.epsilon_sq
    sin2_12 = 1.0 / (3.0 + np.sqrt(inputs.dim_imag_octonion) * eps)
    sin2_23 = 4.0 / inputs.dim_imag_octonion

    # Use the common convention that the leptonic phase is shifted by pi.
    delta = np.pi + inputs.fano_phase
    matrix = ckm_matrix_from_sines(np.sqrt(sin2_12), np.sqrt(sin2_23), np.sqrt(sin2_13), delta)

    return {
        "sin2_theta13": sin2_13,
        "sin2_theta12": sin2_12,
        "sin2_theta23": sin2_23,
        "J_pmns": jarlskog(matrix),
        "delta": delta,
        "matrix": matrix,
    }


def print_inputs(inputs: CHOInputs = INPUTS) -> None:
    print("CHO FLAVOUR DERIVATION SCAFFOLD")
    print("=" * 78)
    print("Algebraic inputs")
    print("-" * 78)
    print(f"dim_C(A)              = {inputs.dim_complex_algebra}")
    print(f"dim J3(O)             = {inputs.dim_jordan}")
    print(f"N_color               = {inputs.n_color}")
    print(f"dim(O), dim(Im O)     = {inputs.dim_octonion}, {inputs.dim_imag_octonion}")
    print(f"epsilon0^2            = pi/(16*27) = {inputs.epsilon_sq:.8f}")
    print(f"epsilon0              = {inputs.epsilon:.8f}")
    print(f"Fano phase            = arccos(1/3) = {np.degrees(inputs.fano_phase):.3f} deg")
    print()


def print_sector_table(rules: list[SectorRule]) -> None:
    print("Charged-sector NNI bridge rules")
    print("-" * 78)
    print("sector   m2/m3(pred)   |A/C|^2 rule                  m1/m3(pred)   m1/m3(obs)   err")
    for rule in rules:
        observed = rule.observed_first_over_third
        print(
            f"{rule.name:<8} "
            f"{rule.second_over_third:>12.6e}   "
            f"{rule.nni_factor_label:<30} "
            f"{rule.first_over_third:>12.6e}   "
            f"{observed:>11.6e}   "
            f"{pct_error(rule.first_over_third, observed):>+6.1f}%"
        )
    print()
    print("Minimal adjacent-transition matrices (diagnostic only)")
    print("Each matrix has M13 = 0 and |A/C|^2 equal to the sector bridge rule.")
    for rule in rules:
        matrix = nni_bridge_matrix(rule)
        eigenvalues = np.linalg.eigvalsh(matrix)
        print(f"\n{rule.name} bridge matrix:")
        for row in matrix:
            print("  [" + ", ".join(f"{value:8.4f}" for value in row) + "]")
        print("  diagnostic eigenvalues: " + ", ".join(f"{value:+.4f}" for value in eigenvalues))
    print()


def print_ckm_table(results: dict[str, float | np.ndarray]) -> None:
    print("CKM matrix from CHO magnitude rules")
    print("-" * 78)
    for key in ["V_us", "V_cb", "V_ub"]:
        print(f"{key:<8} pred={results[key]:.6f}  obs={OBSERVED[key]:.6f}  err={pct_error(results[key], OBSERVED[key]):+.2f}%")
    print(f"delta    pred={np.degrees(results['delta']):.3f} deg from Fano overlap")
    print(f"J(unitary PDG placement) = {results['J_unitary']:.4e}")
    print(f"J(observed)              = {OBSERVED['J_ckm']:.4e}")
    print(f"J error                  = {pct_error(results['J_unitary'], OBSERVED['J_ckm']):+.1f}%")
    print("Note: Paper 2 target J = 3.01e-5 requires the full NNI phase placement;")
    print("this scaffold exposes that as the remaining C4 operator-level task.")
    print()
    print("|V_CKM| scaffold:")
    matrix = results["matrix"]
    assert isinstance(matrix, np.ndarray)
    for row in np.abs(matrix):
        print("  [" + ", ".join(f"{value:.6f}" for value in row) + "]")
    print()


def print_pmns_table(results: dict[str, float | np.ndarray]) -> None:
    print("PMNS matrix from corrected-TBM CHO rules")
    print("-" * 78)
    for key in ["sin2_theta13", "sin2_theta12", "sin2_theta23"]:
        print(f"{key:<14} pred={results[key]:.6f}  obs={OBSERVED[key]:.6f}  err={pct_error(results[key], OBSERVED[key]):+.2f}%")
    print(f"delta_PMNS scaffold = {np.degrees(results['delta']):.3f} deg")
    print(f"J_PMNS scaffold     = {results['J_pmns']:.4e}")
    print()
    print("|U_PMNS| scaffold:")
    matrix = results["matrix"]
    assert isinstance(matrix, np.ndarray)
    for row in np.abs(matrix):
        print("  [" + ", ".join(f"{value:.6f}" for value in row) + "]")
    print()


def main() -> None:
    print_inputs()
    rules = derive_sector_rules()
    print_sector_table(rules)
    print_ckm_table(ckm_predictions())
    print_pmns_table(pmns_predictions())
    print("Bridge status")
    print("-" * 78)
    print("Promotes: first-generation NNI factors are now isolated as explicit")
    print("          sector bridge rules with M13=0 adjacent-transition matrices.")
    print("Exposes:  a full CHO Yukawa operator must still derive these matrices")
    print("          and the CKM phase placement that lowers J to the Paper 2 value.")


if __name__ == "__main__":
    main()