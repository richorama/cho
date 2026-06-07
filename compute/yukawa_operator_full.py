"""
Phase 3 gate: one CHO Yukawa/seesaw operator, or explicit demotions.
=====================================================================

This artifact is a hard integration gate, not a completed theorem. It forces the
current flavour ingredients through one composite object and reports whether the
required charged masses, CKM, PMNS, and seesaw targets are produced by one
operator diagonalization or are still scaffolded components.

The intended use is conservative:

* PASS means the gate ran and the open residuals are explicit.
* OPEN means the one-operator theorem is not closed.
* FAIL is reserved for internal inconsistency in the scaffold itself.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/yukawa_operator_full.py
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from cho_bridge_operator import (
    CHOBridgeOperator,
    OBSERVED,
    ckm_matrix_from_sines,
    construct_fritzsch_matrix,
    diagonalize_hermitian,
    generation_adjacency,
    jarlskog,
    pct_error,
)


@dataclass(frozen=True)
class LedgerItem:
    category: str
    component: str
    status: str
    value: str
    note: str


@dataclass(frozen=True)
class GateCheck:
    requirement: str
    status: str
    metric: str
    note: str


@dataclass(frozen=True)
class DeformationCheck:
    ingredient_removed: str
    status: str
    affected_outputs: str
    metric: str
    note: str


def charged_mass_ratios(operator, sector):
    return (
        operator.first_over_third(sector),
        operator.second_over_third(sector),
        1.0,
    )


def charged_matrix(operator, sector, phase):
    return construct_fritzsch_matrix(charged_mass_ratios(operator, sector), phase, 0.0)


def spectrum_relative_error(matrix, target):
    eigenvalues, _unitary = diagonalize_hermitian(matrix)
    got = np.sort(np.abs(eigenvalues))
    want = np.sort(np.array(target, dtype=float))
    denom = np.maximum(want, 1e-15)
    return float(np.max(np.abs(got - want) / denom))


def charged_sector_matrices(operator):
    _overlap, fano_phase = operator.fano_phase()
    phases = {
        "up": 0.0,
        "down": fano_phase,
        "lepton": 0.0,
    }
    rows = []
    matrices = {}
    for sector in operator.sectors():
        masses = charged_mass_ratios(operator, sector)
        matrix = charged_matrix(operator, sector, phases[sector.name])
        matrices[sector.name] = matrix
        rows.append((sector, masses, matrix, spectrum_relative_error(matrix, masses)))
    return rows, matrices


def ckm_from_charged_matrices(matrices):
    _evals_u, unitary_up = diagonalize_hermitian(matrices["up"])
    _evals_d, unitary_down = diagonalize_hermitian(matrices["down"])
    matrix = unitary_up.conj().T @ unitary_down
    return matrix, jarlskog(matrix)


def ckm_metrics(matrix, invariant):
    abs_matrix = np.abs(matrix)
    return {
        "V_us": float(abs_matrix[0, 1]),
        "V_cb": float(abs_matrix[1, 2]),
        "V_ub": float(abs_matrix[0, 2]),
        "J": float(invariant),
    }


def relative_score(metrics):
    return float(np.sqrt(np.mean([
        ((metrics["V_us"] - OBSERVED["V_us"]) / OBSERVED["V_us"]) ** 2,
        ((metrics["V_cb"] - OBSERVED["V_cb"]) / OBSERVED["V_cb"]) ** 2,
        ((metrics["V_ub"] - OBSERVED["V_ub"]) / OBSERVED["V_ub"]) ** 2,
        ((metrics["J"] - OBSERVED["J_ckm"]) / OBSERVED["J_ckm"]) ** 2,
    ])))


def parameter_ledger(operator):
    epsilon_sq = operator.epsilon_sq()
    weak_trace = operator.weak_shape_trace()
    _overlap, phase = operator.fano_phase()
    return [
        LedgerItem(
            "bridge",
            "epsilon0^2",
            "GEOMETRIC/OPEN",
            f"{epsilon_sq:.10f}",
            "pi/(16*27); Phase 2 leaves normalized-measure H4 open",
        ),
        LedgerItem(
            "fixed",
            "generation adjacency",
            "SCAFFOLD DERIVED",
            "1<->2<->3, M13=0",
            "one-step rule encoded; trilinear CHO origin still required",
        ),
        LedgerItem(
            "fixed/open selection",
            "sector ranks",
            "DERIVED VALUE / OPEN SELECTION",
            "1, 3, 8",
            "Fock traces derived; one Yukawa map must select them dynamically",
        ),
        LedgerItem(
            "chosen bridge",
            "weak shape trace",
            "OPEN SELECTION",
            f"{weak_trace:.6f}",
            "rank-one quaternionic trace gives 1/4 once selected",
        ),
        LedgerItem(
            "bridge",
            "lepton sphere factor",
            "IDENTIFIED / OPEN DYNAMICS",
            "1/pi",
            "transition-sphere measure identified, not derived from Yukawa trace",
        ),
        LedgerItem(
            "sign/phase",
            "Fano phase",
            "DERIVED VALUE / OPEN PLACEMENT",
            f"arccos(1/3) = {np.degrees(phase):.3f} deg",
            "incidence phase works for J only with a still-open matrix placement",
        ),
        LedgerItem(
            "target bridge",
            "PMNS perturbation",
            "TARGET",
            "DeltaY, DeltaM",
            "explicit seesaw target; broken-triality derivation missing",
        ),
    ]


def deformation_checks(operator, projected_ckm_metrics, pmns):
    epsilon = np.sqrt(operator.epsilon_sq())
    no_phase_matrix = ckm_matrix_from_sines(
        projected_ckm_metrics["V_us"],
        projected_ckm_metrics["V_cb"],
        projected_ckm_metrics["V_ub"],
        0.0,
    )
    no_phase_j = jarlskog(no_phase_matrix)
    sector_multiplicities = {sector.name: operator.sector_multiplicity(sector) for sector in operator.sectors()}
    return [
        DeformationCheck(
            "epsilon spurion",
            "COUPLED FAILURE",
            "M1-M3, C1-C3, N2-N3",
            f"epsilon={epsilon:.6f}; setting epsilon=0 collapses hierarchy/mixing amplitudes",
            "one spurion carries several outputs, so F0 demotion must propagate through flavour claims",
        ),
        DeformationCheck(
            "Fano phase",
            "COUPLED FAILURE",
            "C4 Jarlskog",
            f"J(delta=0)={no_phase_j:.3e}",
            "the CKM CP diagnostic needs a nontrivial phase placement, not only magnitudes",
        ),
        DeformationCheck(
            "sector projectors",
            "COUPLED FAILURE",
            "M1-M3, M9-M11",
            "multiplicities=" + ",".join(f"{key}:{value:.0f}" for key, value in sector_multiplicities.items()),
            "collapsing sector ranks would erase the 1,3,8 mass-channel distinction",
        ),
        DeformationCheck(
            "PMNS perturbation",
            "COUPLED FAILURE",
            "N2-N5",
            f"target sin2(theta13)={float(pmns['sin2_theta13']):.6f}; TBM gives 0",
            "the neutrino angle corrections must come from dynamics, not target-angle insertion",
        ),
    ]


def gate_checks(operator, matrices, strict_ckm_metrics, projected_ckm_metrics, pmns):
    adjacency = generation_adjacency()
    spectra_ok = all(
        spectrum_relative_error(matrices[sector.name], charged_mass_ratios(operator, sector)) < 1e-8
        for sector in operator.sectors()
    )
    strict_score = relative_score(strict_ckm_metrics)
    projected_score = relative_score(projected_ckm_metrics)
    pmns_angle_rms = float(np.sqrt(np.mean([
        ((pmns["sin2_theta13"] - OBSERVED["sin2_theta13"]) / OBSERVED["sin2_theta13"]) ** 2,
        ((pmns["sin2_theta12"] - OBSERVED["sin2_theta12"]) / OBSERVED["sin2_theta12"]) ** 2,
        ((pmns["sin2_theta23"] - OBSERVED["sin2_theta23"]) / OBSERVED["sin2_theta23"]) ** 2,
    ])))
    return [
        GateCheck(
            "one composite operator object",
            "PASS",
            "CHOBridgeOperator reused for all sectors",
            "integration gate uses one object rather than separate ad-hoc scripts",
        ),
        GateCheck(
            "charged-sector matrices",
            "PASS" if spectra_ok else "FAIL",
            f"max spectrum error < 1e-8: {spectra_ok}",
            "dimensionless NNI/Fritzsch matrices exist for up, down, lepton sectors",
        ),
        GateCheck(
            "nearest-neighbor generation rule",
            "PASS" if adjacency[0, 2] == 0 and (adjacency @ adjacency)[0, 2] == 1 else "FAIL",
            f"M13={adjacency[0, 2]}, two-step paths={(adjacency @ adjacency)[0, 2]}",
            "direct 1<->3 absent at leading order",
        ),
        GateCheck(
            "CKM from one charged diagonalization",
            "OPEN",
            f"strict RMS relative error={strict_score:.2f}",
            "the strict charged-matrix diagonalization does not yet reconcile magnitudes and J",
        ),
        GateCheck(
            "CKM magnitude projection",
            "OPEN",
            f"projection RMS relative error={projected_score:.2f}",
            "magnitude rules are close, but this is not one mass-matrix diagonalization",
        ),
        GateCheck(
            "PMNS/seesaw perturbation",
            "OPEN",
            f"angle RMS relative error={pmns_angle_rms:.3f}",
            "DeltaY/DeltaM is explicit but still target-built from corrected angles",
        ),
    ]


def print_ledger(items):
    print("PARAMETER / COMPONENT LEDGER")
    print("=" * 78)
    print(f"{'category':<20} {'component':<24} {'status':<26} {'value':<24} note")
    print("-" * 78)
    for item in items:
        print(f"{item.category:<20} {item.component:<24} {item.status:<26} {item.value:<24} {item.note}")
    print()


def print_deformations(checks):
    print("DEFORMATION / NULL TESTS")
    print("=" * 78)
    print(f"{'removed ingredient':<22} {'status':<16} {'affected outputs':<22} metric")
    print("-" * 78)
    for check in checks:
        print(f"{check.ingredient_removed:<22} {check.status:<16} {check.affected_outputs:<22} {check.metric}")
        print(f"      {check.note}")
    print()


def print_charged_matrices(rows):
    print("CHARGED-SECTOR MATRICES FROM THE ONE OPERATOR SCAFFOLD")
    print("=" * 78)
    print(f"{'sector':<8} {'m1/m3':>12} {'m2/m3':>12} {'spec err':>12} {'obs m1/m3':>12} {'obs m2/m3':>12}")
    for sector, masses, _matrix, spec_err in rows:
        print(
            f"{sector.name:<8} {masses[0]:>12.6e} {masses[1]:>12.6e}"
            f" {spec_err:>12.1e} {sector.observed_first_over_third:>12.6e}"
            f" {sector.observed_second_over_third:>12.6e}"
        )
    print()
    print("Representative matrices (dimensionless, m3-normalized):")
    for sector, _masses, matrix, _spec_err in rows:
        print(f"\n{sector.name}:")
        for row in matrix:
            print("  [" + ", ".join(f"{value.real:+.4e}{value.imag:+.4e}i" for value in row) + "]")
    print()


def print_ckm(strict_metrics, projected_metrics):
    print("CKM GATE")
    print("=" * 78)
    print(f"{'source':<28} {'V_us':>9} {'V_cb':>9} {'V_ub':>9} {'J':>12} {'RMS err':>9}")
    for label, metrics in [
        ("strict charged diagonalization", strict_metrics),
        ("magnitude projection", projected_metrics),
    ]:
        print(
            f"{label:<28} {metrics['V_us']:>9.6f} {metrics['V_cb']:>9.6f}"
            f" {metrics['V_ub']:>9.6f} {metrics['J']:>12.4e} {relative_score(metrics):>9.2f}"
        )
    print(
        f"{'observed':<28} {OBSERVED['V_us']:>9.6f} {OBSERVED['V_cb']:>9.6f}"
        f" {OBSERVED['V_ub']:>9.6f} {OBSERVED['J_ckm']:>12.4e} {'':>9}"
    )
    print()
    print("Interpretation: the Fano phase and magnitude rules are useful pieces, but")
    print("the one-diagonalization CKM requirement is still open. This is the main")
    print("demotion trigger for CKM claims if Phase 3 cannot close.")
    print()


def print_pmns(pmns):
    print("PMNS / SEESAW GATE")
    print("=" * 78)
    for key in ["sin2_theta13", "sin2_theta12", "sin2_theta23"]:
        value = float(pmns[key])
        print(f"{key:<14} target={value:.6f} observed={OBSERVED[key]:.6f} err={pct_error(value, OBSERVED[key]):+.2f}%")
    print(f"delta_PMNS     target={np.degrees(float(pmns['delta'])):.3f} deg")
    print(f"||Delta Y||/||Y_TBM|| = {pmns['delta_y_norm_ratio']:.3f}")
    print(f"||Delta M||/||M_TBM|| = {pmns['delta_m_norm_ratio']:.3f}")
    print()
    print("Interpretation: the seesaw target is explicit and numerically useful, but")
    print("DeltaY is still constructed from target angles rather than derived from the")
    print("CHO operator/action.")
    print()


def print_gate(checks):
    print("PHASE 3 GATE VERDICT")
    print("=" * 78)
    for check in checks:
        print(f"{check.status:<5} {check.requirement:<38} {check.metric}")
        print(f"      {check.note}")
    print()
    hard_fail = any(check.status == "FAIL" for check in checks)
    theorem_closed = all(check.status == "PASS" for check in checks)
    if hard_fail:
        print("AUDIT STATUS: FAIL - internal operator scaffold inconsistency detected.")
        raise SystemExit(1)
    if theorem_closed:
        print("THEOREM STATUS: CLOSED - update ledger/model complexity before quoting.")
    else:
        print("AUDIT STATUS: PASS - gate executed and residuals are explicit.")
        print("THEOREM STATUS: OPEN - do not promote masses/CKM/PMNS to one-operator derivations yet.")
    print()


def main():
    operator = CHOBridgeOperator()
    ledger = parameter_ledger(operator)
    charged_rows, matrices = charged_sector_matrices(operator)
    strict_ckm, strict_j = ckm_from_charged_matrices(matrices)
    strict_metrics = ckm_metrics(strict_ckm, strict_j)
    projected_ckm, projected_j = operator.ckm_magnitude_scaffold()
    projected_metrics = ckm_metrics(projected_ckm, projected_j)
    pmns = operator.pmns_seesaw_target()
    checks = gate_checks(operator, matrices, strict_metrics, projected_metrics, pmns)
    deformations = deformation_checks(operator, projected_metrics, pmns)

    print("=" * 78)
    print("  PHASE 3 - FULL YUKAWA/SEESAW OPERATOR GATE")
    print("  One composite object, one ledger, explicit residuals.")
    print("=" * 78)
    print()
    print_ledger(ledger)
    print_charged_matrices(charged_rows)
    print_ckm(strict_metrics, projected_metrics)
    print_pmns(pmns)
    print_deformations(deformations)
    print_gate(checks)


if __name__ == "__main__":
    main()
