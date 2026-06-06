"""
Diagnostic scaffold for the epsilon0^2 = pi / 432 bridge.

This is not an operator proof. It formalizes the bridge target as an
angle-weighted normalized trace and records the nearby alternatives that a
real proof must exclude.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class BridgeSpace:
    """State-space data for the epsilon bridge trace target."""

    dim_complex_algebra: int = 16
    dim_real_algebra: int = 64
    dim_jordan: int = 27
    dim_jordan_traceless: int = 26
    dim_octonion: int = 8
    dim_imag_octonion: int = 7
    theta_break: float = np.pi

    @property
    def trace_dimension(self) -> int:
        return self.dim_complex_algebra * self.dim_jordan

    @property
    def epsilon_sq(self) -> float:
        return self.theta_break / self.trace_dimension

    @property
    def epsilon(self) -> float:
        return np.sqrt(self.epsilon_sq)


@dataclass(frozen=True)
class EpsilonEstimator:
    """One empirical estimate of epsilon0^2 from a bridge-reusing row."""

    name: str
    value: float
    formula: str


@dataclass(frozen=True)
class CandidateTrace:
    """Nearby trace/angle model to compare with the target."""

    name: str
    numerator: float
    denominator: float
    note: str

    @property
    def value(self) -> float:
        return self.numerator / self.denominator


OBSERVED = {
    "m_c": 1.27,
    "m_t": 172.76,
    "m_s": 93.4e-3,
    "m_b": 4.18,
    "m_mu": 0.10566,
    "m_tau": 1.777,
    "V_us": 0.2243,
    "V_cb": 0.0422,
    "sin2_theta13": 0.02203,
    "dm2_ratio": 0.02950,
}


def pct_error(predicted: float, observed: float) -> float:
    return (predicted - observed) / observed * 100.0


def empirical_estimators() -> list[EpsilonEstimator]:
    """Extract epsilon0^2 estimates from rows that should share the bridge."""
    return [
        EpsilonEstimator("up mass", OBSERVED["m_c"] / OBSERVED["m_t"], "m_c / m_t"),
        EpsilonEstimator("down mass", OBSERVED["m_s"] / OBSERVED["m_b"] / 3.0, "(m_s / m_b) / 3"),
        EpsilonEstimator("lepton mass", OBSERVED["m_mu"] / OBSERVED["m_tau"] / 8.0, "(m_mu / m_tau) / 8"),
        EpsilonEstimator("Cabibbo", OBSERVED["V_us"] ** 2 / 7.0, "|V_us|^2 / 7"),
        EpsilonEstimator("CKM 2-3", (2.0 * OBSERVED["V_cb"]) ** 2, "(2 |V_cb|)^2"),
        EpsilonEstimator("PMNS reactor", OBSERVED["sin2_theta13"] / 3.0, "sin^2(theta13) / 3"),
        EpsilonEstimator("nu splitting", OBSERVED["dm2_ratio"] / 4.0, "dm21^2 / dm31^2 / 4"),
    ]


def candidate_traces(space: BridgeSpace) -> list[CandidateTrace]:
    """Nearby trace normalizations that a real derivation must exclude."""
    return [
        CandidateTrace(
            "target: pi/(16*27)",
            space.theta_break,
            space.dim_complex_algebra * space.dim_jordan,
            "complex CHO Weyl states times full J3(O)",
        ),
        CandidateTrace(
            "real algebra: pi/(64*27)",
            space.theta_break,
            space.dim_real_algebra * space.dim_jordan,
            "averaging over real A would be four times too small",
        ),
        CandidateTrace(
            "traceless J3: pi/(16*26)",
            space.theta_break,
            space.dim_complex_algebra * space.dim_jordan_traceless,
            "drops the Jordan trace direction",
        ),
        CandidateTrace(
            "octonion only: pi/(8*27)",
            space.theta_break,
            space.dim_octonion * space.dim_jordan,
            "ignores C and H internal structure",
        ),
        CandidateTrace(
            "imaginary O: pi/(7*27)",
            space.theta_break,
            space.dim_imag_octonion * space.dim_jordan,
            "uses Im(O) instead of the CHO Weyl space",
        ),
        CandidateTrace(
            "raw reciprocal: 1/(16*27)",
            1.0,
            space.dim_complex_algebra * space.dim_jordan,
            "same trace space without the angular half-turn",
        ),
        CandidateTrace(
            "full turn: 2pi/(16*27)",
            2.0 * space.theta_break,
            space.dim_complex_algebra * space.dim_jordan,
            "same trace space with a full-turn holonomy",
        ),
    ]


def rms_relative_error(candidate: float, estimators: list[EpsilonEstimator]) -> float:
    errors = [(candidate - item.value) / item.value for item in estimators]
    return float(np.sqrt(np.mean(np.square(errors))) * 100.0)


def print_trace_target(space: BridgeSpace) -> None:
    print("EPSILON0 BRIDGE TRACE TARGET")
    print("=" * 78)
    print("Proposed bridge state space:")
    print("  H_epsilon = S_A x J3(O)")
    print(f"  dim_C(S_A)     = {space.dim_complex_algebra}")
    print(f"  dim(J3(O))     = {space.dim_jordan}")
    print(f"  trace dimension= {space.trace_dimension}")
    print(f"  theta_break    = pi")
    print()
    print("Trace target:")
    print("  epsilon0^2 = theta_break * Tr(P_adj T_break P_adj) / dim(H_epsilon)")
    print("  required Tr(P_adj T_break P_adj) = 1")
    print(f"  epsilon0^2 = pi/{space.trace_dimension} = {space.epsilon_sq:.10f}")
    print(f"  epsilon0   = {space.epsilon:.10f}")
    print()


def print_empirical_estimators(space: BridgeSpace, estimators: list[EpsilonEstimator]) -> None:
    print("Empirical bridge estimates (comparison only)")
    print("-" * 78)
    print(f"{'source':<16} {'formula':<26} {'estimate':>12} {'target err':>12}")
    for item in estimators:
        print(f"{item.name:<16} {item.formula:<26} {item.value:>12.8f} {pct_error(space.epsilon_sq, item.value):>+11.2f}%")
    mean_estimate = float(np.mean([item.value for item in estimators]))
    spread = float(np.std([item.value for item in estimators]))
    print("-" * 78)
    print(f"mean estimate: {mean_estimate:.8f}")
    print(f"std spread:    {spread:.8f}")
    print(f"target:        {space.epsilon_sq:.8f}")
    print()


def print_candidate_table(space: BridgeSpace, estimators: list[EpsilonEstimator]) -> None:
    print("Nearby trace normalizations")
    print("-" * 78)
    print(f"{'candidate':<30} {'value':>12} {'RMS err':>9}  note")
    for candidate in candidate_traces(space):
        print(
            f"{candidate.name:<30} "
            f"{candidate.value:>12.8f} "
            f"{rms_relative_error(candidate.value, estimators):>8.1f}%  "
            f"{candidate.note}"
        )
    print()


def print_proof_obligations() -> None:
    print("Proof obligations")
    print("-" * 78)
    obligations = [
        "Construct S_A as the 16-dimensional complex CHO Weyl-state space.",
        "Show the flavour transition averages over the full 27-dimensional J3(O).",
        "Derive theta_break = pi from the relevant triality/coset path.",
        "Build T_break and prove Tr(P_adj T_break P_adj) = 1.",
        "Insert T_break into a CHO Yukawa operator that yields the sector factors 1, 3, and 8.",
        "Explain why CKM/PMNS use epsilon0 at amplitude level while mass ratios use epsilon0^2.",
    ]
    for index, obligation in enumerate(obligations, 1):
        print(f"{index}. {obligation}")
    print()
    print("Status: scaffolded bridge target, not a theorem.")


def main() -> None:
    space = BridgeSpace()
    estimators = empirical_estimators()
    print_trace_target(space)
    print_empirical_estimators(space, estimators)
    print_candidate_table(space, estimators)
    print_proof_obligations()


if __name__ == "__main__":
    main()
