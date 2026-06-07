"""
Structured audit contracts for the CHO theory-validation harness.

The audit scripts print human-readable verdicts. This module is the first
machine-readable layer above those scripts: every registered audit artifact gets
a claim contract saying which ledger entries it touches, whether it is a closed
result, an open bridge, a diagnostic, a locked registry, or an out-of-scope gate,
and what must remain visible in public prose.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/audit_contract.py
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
import json
import re
import sys
from typing import Iterable


STATUS_THEOREM = "theorem"
STATUS_DERIVED_BRIDGE = "derived_bridge"
STATUS_OPEN_BRIDGE = "open_bridge"
STATUS_FUTURE_TEST = "future_test"
STATUS_DIAGNOSTIC = "diagnostic"
STATUS_LOCKED_REGISTRY = "locked_registry"
STATUS_OUT_OF_SCOPE = "out_of_scope"
STATUS_EXPLORATORY = "exploratory"

VERDICT_CLOSED = "closed"
VERDICT_OPEN = "open"
VERDICT_DIAGNOSTIC = "diagnostic"
VERDICT_LOCKED = "locked"
VERDICT_DEMOTED = "demoted"
VERDICT_FUTURE_TEST = "future_test"

ALLOWED_STATUSES = frozenset({
    STATUS_THEOREM,
    STATUS_DERIVED_BRIDGE,
    STATUS_OPEN_BRIDGE,
    STATUS_FUTURE_TEST,
    STATUS_DIAGNOSTIC,
    STATUS_LOCKED_REGISTRY,
    STATUS_OUT_OF_SCOPE,
    STATUS_EXPLORATORY,
})

ALLOWED_VERDICTS = frozenset({
    VERDICT_CLOSED,
    VERDICT_OPEN,
    VERDICT_DIAGNOSTIC,
    VERDICT_LOCKED,
    VERDICT_DEMOTED,
    VERDICT_FUTURE_TEST,
})

OPEN_STATUSES = frozenset({STATUS_OPEN_BRIDGE, STATUS_EXPLORATORY})
LEDGER_ID_RE = re.compile(r"^[A-Z]+[0-9]+$")


@dataclass(frozen=True)
class AuditContract:
    artifact: str
    ledger_ids: tuple[str, ...]
    status: str
    verdict: str
    public_claim_policy: str
    assumptions: tuple[str, ...] = field(default_factory=tuple)
    open_bridges: tuple[str, ...] = field(default_factory=tuple)
    kill_conditions: tuple[str, ...] = field(default_factory=tuple)
    locked_predictions: tuple[str, ...] = field(default_factory=tuple)
    bridge_sensitivities: tuple[str, ...] = field(default_factory=tuple)


def contract(
    artifact: str,
    ledger_ids: tuple[str, ...],
    status: str,
    verdict: str,
    public_claim_policy: str,
    *,
    assumptions: tuple[str, ...] = (),
    open_bridges: tuple[str, ...] = (),
    kill_conditions: tuple[str, ...] = (),
    locked_predictions: tuple[str, ...] = (),
    bridge_sensitivities: tuple[str, ...] = (),
) -> AuditContract:
    return AuditContract(
        artifact=artifact,
        ledger_ids=ledger_ids,
        status=status,
        verdict=verdict,
        public_claim_policy=public_claim_policy,
        assumptions=assumptions,
        open_bridges=open_bridges,
        kill_conditions=kill_conditions,
        locked_predictions=locked_predictions,
        bridge_sensitivities=bridge_sensitivities,
    )


CONTRACTS = {
    "look_elsewhere": contract(
        "look_elsewhere",
        ("STAT1",),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Use as a hardness-to-vary diagnostic, not as a theorem promotion.",
    ),
    "scale_look_elsewhere": contract(
        "scale_look_elsewhere",
        ("S1", "N1", "CC1", "STAT1"),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Do not cite the 12/12-simplest figure for the power-of-three scale relations; "
        "their log-axis coverage is ~93%, so quote the integer exponent as the only sharp content.",
        open_bridges=(
            "The scale relations M_W=M_P/3^36, M_R=M_P/3^9, Lambda=(11/12)M_P/(sqrt2 3^64) "
            "are cheap log-axis hits; the O(1) prefactors are not forced.",
        ),
    ),
    "model_complexity": contract(
        "model_complexity",
        ("STAT1",),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Keep few-input and Occam-cost language visible; do not call the framework zero-parameter.",
    ),
    "independent_observables": contract(
        "independent_observables",
        ("STAT1",),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Use only for independent-observable bookkeeping and goodness-of-fit context.",
    ),
    "covariance_gof": contract(
        "covariance_gof",
        ("STAT1",),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Quote correlated GoF with the effective-observable caveat.",
    ),
    "derived_vs_residual": contract(
        "derived_vs_residual",
        ("A6", "S4", "S5", "STAT1"),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Use to separate derived pieces from continuum/RG residuals.",
        open_bridges=("Continuum scale and threshold terms are not theorem-level.",),
    ),
    "rg_matching_audit": contract(
        "rg_matching_audit",
        ("A6", "S4", "S5", "CC1"),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Do not promote alpha, sin^2(theta_W), M_W, or Lambda until CHO derives the matching scheme.",
        open_bridges=(
            "Matching scale selection.",
            "Threshold and vacuum-polarization scheme.",
            "Electroweak normalization and cosmological free-energy screen.",
        ),
        kill_conditions=("Inverse-matched scales remain selected to hit observed targets.",),
    ),
    "mass_ratio_rg_audit": contract(
        "mass_ratio_rg_audit",
        ("M5", "M6", "M7", "M8"),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Quote five of six mass relations as 1-loop RG-invariant; quote m_b/m_tau=7/3 (M5) "
        "only at a stated scale (mu ~ m_b).",
        open_bridges=(
            "m_b/m_tau=7/3 is scale-dependent and must carry a matching scale.",
        ),
        kill_conditions=("m_b/m_tau=7/3 is quoted as a scale-free prediction.",),
    ),
    "first_generation_audit": contract(
        "first_generation_audit",
        ("M9", "M10", "M11"),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Treat first-generation masses as bridge tests until their shape factors are selected by one operator.",
        open_bridges=("Dynamical reduction of the first-generation shape factors.",),
        kill_conditions=("The electron 1/(4 pi) factor cannot be derived inside the Yukawa operator.",),
    ),
    "predict_neutrino_sum": contract(
        "predict_neutrino_sum",
        ("N1",),
        STATUS_FUTURE_TEST,
        VERDICT_FUTURE_TEST,
        "Quote only through the locked prediction registry.",
        kill_conditions=("Robust future neutrino mass data falsify the frozen normal-ordering band.",),
    ),
    "forward_predictions": contract(
        "forward_predictions",
        ("N1", "N5", "CC1"),
        STATUS_FUTURE_TEST,
        VERDICT_FUTURE_TEST,
        "Separate positive predictions from bridge sensitivities; the registry is authoritative.",
        open_bridges=("Higgs self-coupling and m_nu3 threshold targets still depend on open matching bridges.",),
        kill_conditions=("A future target depends on an adjustable bridge after data arrive.",),
    ),
    "jordan_eigenvalue_generations": contract(
        "jordan_eigenvalue_generations",
        ("G1",),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim the algebraic count route, not a completed generation spectrum.",
        open_bridges=("Map the SM fermion content and Yukawa spectrum onto the rank-three structure.",),
    ),
    "ko_dimension_chirality": contract(
        "ko_dimension_chirality",
        ("K1",),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim the KO-dimension chirality condition; keep the Dirac operator open.",
        open_bridges=("Specify the physical Dirac operator and full chiral anomaly-free spectrum.",),
    ),
    "ladder_charges": contract(
        "ladder_charges",
        ("Q1",),
        STATUS_THEOREM,
        VERDICT_CLOSED,
        "Credit the Furey/Dubois-Violette one-generation charge result and cite it.",
        assumptions=("Minimal left-ideal one-generation construction.",),
    ),
    "weak_isospin_hypercharge": contract(
        "weak_isospin_hypercharge",
        ("Q2",),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim weak SU(2), GMN hypercharge bookkeeping, and the remaining chiral projection seam.",
        open_bridges=("Make only left-handed fields weak doublets via the KO-dimension-6 projector.",),
    ),
    "chiral_projector": contract(
        "chiral_projector",
        ("Q2", "K1"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Use as progress on the chiral split, while keeping the full content map explicit.",
        open_bridges=("Connect the projector to the full SM field-label functor.",),
    ),
    "physics_map_audit": contract(
        "physics_map_audit",
        ("Q3",),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim anomaly-clean bookkeeping, not a completed functorial content map.",
        open_bridges=("Map the three frame idempotents and tangent spinors to field labels functorially.",),
    ),
    "bayesian_evidence": contract(
        "bayesian_evidence",
        ("STAT1",),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Use as model-comparison accounting; status credits must follow the ledger.",
    ),
    "spectral_action": contract(
        "spectral_action",
        ("A4", "M1"),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Do not present the inverse-spectral scaffold as a forced mass operator.",
        open_bridges=("Find a chirality-odd algebra-internal Dirac operator with constants-out greater than knobs-in.",),
        kill_conditions=("The allowed operator class remains underconstrained.",),
    ),
    "spectral_action_432": contract(
        "spectral_action_432",
        ("A3", "M1"),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Quote only the parameter-free averaging law (mixing level = mean of two "
        "generation levels) as derived; do NOT quote the eps0 ladder as the "
        "measured Yukawa spectrum.",
        open_bridges=(
            "Supply a dynamical principle that selects the three diagonal J3(O) "
            "eigenvalues; the single eps0 ladder misses the lepton hierarchy by "
            "~1.4 decades.",
        ),
        kill_conditions=(
            "The eps0 ladder is presented as reproducing the measured fermion "
            "mass ratios.",
        ),
    ),
    "epsilon_generation_ladder": contract(
        "epsilon_generation_ladder",
        ("M1", "S1"),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Report the eps0-base generation exponents as a falsifiable target for a "
        "dynamical seed; quote the lepton triangular (0,1,3) hit WITH its "
        "look-elsewhere coverage and scheme caveats, not as a derived law.",
        open_bridges=(
            "Derive a (possibly sector-dependent) log-mass curvature law that "
            "outputs the measured eps0-base generation exponents.",
        ),
        kill_conditions=(
            "A non-universal per-sector integer-exponent fit is presented as a "
            "universal derived mass law.",
        ),
    ),
    "spurion_perturbation": contract(
        "spurion_perturbation",
        ("A3", "M1", "S1"),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Quote FACT 1 (rank-one spurion lifts one level per order) and FACT 2 "
        "(quadratic U_X gives multiplicative mixing {a^2,b^2,c^2}u{ab,bc,ca}) as "
        "theorems from the structure tensor; quote the triangular insertion chain "
        "c_n=(0,1,2) only as the minimal hypothesis matching leptons, NOT as "
        "derived or universal.",
        open_bridges=(
            "Derive (dynamically) that the spurion insertion-order chain is "
            "exactly c_n=n and explain its sector dependence across quarks.",
        ),
        kill_conditions=(
            "The triangular insertion chain is presented as a derived, "
            "sector-universal mass law.",
        ),
    ),
    "generation_cascade": contract(
        "generation_cascade",
        ("A3", "M1", "S1"),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Quote the Freudenthal seesaw as derived structure: generations are roots "
        "of the J3(O) cubic, so m2*m3=|N3|/m1 EXACTLY (light-pair product = cubic "
        "norm over heaviest) and the hierarchy reduces to two invariant-suppression "
        "orders (q,Q)=(ord T2, ord N3). Quote the lepton (1,4)=triangular reading "
        "WITH the explicit non-universality across quark sectors; do NOT present "
        "(q,Q) as derived or sector-universal.",
        open_bridges=(
            "Derive, from a dynamical/variational principle, the spurion "
            "suppression orders (q,Q) of the quadratic and cubic Freudenthal "
            "invariants and their sector dependence.",
        ),
        kill_conditions=(
            "The two-integer (q,Q) cascade is presented as a derived, "
            "sector-universal mass law rather than a reduction of the open seed.",
        ),
    ),
    "cascade_universality": contract(
        "cascade_universality",
        ("A3", "M1", "S1"),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Quote as a consistency reduction, not a closed mass law: the cascade "
        "(q,Q) sector-dependence is the independently-derived Georgi-Jarlskog "
        "prefactors {1,3,8}, so the second-generation suppression is universally "
        "eps0^2 (GJ-reduced middle exponent = 2.00 +/- 0.01). Always state WITH it "
        "that the lightest generation does NOT become universal -- it reduces to "
        "4 + logb(c3) with the first-generation prefactor c3 sector-dependent "
        "(only the lepton 1/(4 pi) identified; up and down remain open anomalies).",
        open_bridges=(
            "Derive the first-generation prefactors c3 (up ~1/4, down ~2.2) from "
            "dynamics; only the scheme-clean lepton c3 = 1/(4 pi) is identified.",
        ),
        kill_conditions=(
            "Middle-generation universality is presented as a full sector-universal "
            "mass law, or the still-open first-generation prefactors are treated as "
            "derived.",
        ),
    ),
    "cross_generation_count": contract(
        "cross_generation_count",
        ("A3", "M1"),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Use as knob-count pressure on flavour models, not as a completed flavour derivation.",
        open_bridges=("Turn the inter-generation count into a single diagonalized operator.",),
    ),
    "yukawa_operator_full": contract(
        "yukawa_operator_full",
        ("M1", "M2", "M3", "M4", "M5", "M9", "M10", "M11", "C1", "C2", "C3", "C4", "N2", "N3", "N4", "N5"),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Do not promote masses, CKM, or PMNS to one-operator derivations yet.",
        open_bridges=(
            "CKM corrected magnitudes and Jarlskog from one charged diagonalization.",
            "PMNS DeltaY/DeltaM dynamics.",
            "Operator selection of sector projectors and first-generation shape factors.",
        ),
        kill_conditions=("CKM magnitudes and Jarlskog cannot coexist in one operator.",),
    ),
    "three_generations_frame": contract(
        "three_generations_frame",
        ("G1", "G2"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim count and chirality obstruction removal; keep the spectrum and content map open.",
        open_bridges=("Build the physical content map and Yukawa spectrum over the frame idempotents.",),
    ),
    "epsilon_cubic_discriminant": contract(
        "epsilon_cubic_discriminant",
        ("F0",),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Use as a negative discriminator: the cubic discriminant does not force the 27.",
    ),
    "epsilon_heat_kernel": contract(
        "epsilon_heat_kernel",
        ("F0",),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Use as a negative discriminator against a heat-kernel origin of the pi.",
    ),
    "epsilon_state_count": contract(
        "epsilon_state_count",
        ("F0",),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim the 16-dim rank-one state count while keeping the normalized measure open.",
        open_bridges=("Derive the invariant normalized transition measure.",),
    ),
    "epsilon_product_space": contract(
        "epsilon_product_space",
        ("F0",),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim the trace-space stratification only with the remaining measure caveat.",
        open_bridges=("Lift the product-space identification into the CHO action measure.",),
    ),
    "epsilon_weyl_isomorphism": contract(
        "epsilon_weyl_isomorphism",
        ("F0", "G1"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim the Spin(9) spinor isomorphism; do not claim F0 is closed by this alone.",
        open_bridges=("Connect the isomorphism to the invariant transition measure.",),
    ),
    "epsilon_spin9_embedding": contract(
        "epsilon_spin9_embedding",
        ("F0",),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim the shared Spin(9) seam up to the remaining frame/measure choice.",
        open_bridges=("Derive the frame choice and normalized measure from the action.",),
    ),
    "epsilon_rank_one_kernel": contract(
        "epsilon_rank_one_kernel",
        ("F0", "G1"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim rank-one primitivity as a structural result; keep vacuum purity selection explicit.",
        open_bridges=("Show the action uniquely selects the rank-one transition kernel.",),
    ),
    "epsilon_free_action": contract(
        "epsilon_free_action",
        ("F0", "A4"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim the free-action/topological-term structure with the measure residual visible.",
        open_bridges=("Turn the action into the normalized transition trace without choosing the trace space.",),
    ),
    "epsilon_channel_coefficients": contract(
        "epsilon_channel_coefficients",
        ("M1", "M2", "M3"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim Fock-grade channel ranks; keep their selection by the Yukawa operator open.",
        open_bridges=("Show the Yukawa map selects these Fock-grade traces dynamically.",),
    ),
    "epsilon_mixing_coefficients": contract(
        "epsilon_mixing_coefficients",
        ("M11", "C1", "N2", "N3", "N5"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim Fano counts and the lepton sphere-measure identification; keep the operator reduction open.",
        open_bridges=("Derive the lepton Yukawa trace reduction and PMNS perturbation dynamically.",),
    ),
    "epsilon_vcb_halfangle": contract(
        "epsilon_vcb_halfangle",
        ("C2", "C3"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim the half-angle coefficient; keep channel assignment and Vub placement open.",
        open_bridges=("Derive channel assignment inside the charged Yukawa matrices.",),
    ),
    "epsilon_a4_two_level": contract(
        "epsilon_a4_two_level",
        ("F0", "A3"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Claim the two-level/A4 structural origin with the measure and frame caveat.",
        open_bridges=("Connect the two-level symmetry to the unique normalized transition trace.",),
    ),
    "epsilon_measure_audit": contract(
        "epsilon_measure_audit",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Keep epsilon0^2 = pi/432 as the explicit Bayes hinge until the invariant measure theorem closes.",
        open_bridges=("Hypothesis H4: the invariant normalized transition measure.",),
        kill_conditions=("The normalized measure cannot be derived without choosing the trace space by hand.",),
    ),
    "epsilon_measure_witness": contract(
        "epsilon_measure_witness",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Treat H4 as the live theorem seam; do not promote F0 from this witness alone.",
        open_bridges=("Derive the invariant normalized transition measure from the CHO action.",),
        kill_conditions=("If H4 remains a normalization choice, demote F0 in the Bayes accounting.",),
    ),
    "gravity_curvature": contract(
        "gravity_curvature",
        ("GR1",),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "Describe only as a kinematic internal metric brick, not dynamical gravity.",
        open_bridges=("No canonical 4D Lorentzian reduction or Einstein/Newton dynamics.",),
        kill_conditions=("Do not count this as gravity unless a future gate supplies Lorentzian dynamics.",),
    ),
    "gravity_gate_audit": contract(
        "gravity_gate_audit",
        ("GR1",),
        STATUS_OUT_OF_SCOPE,
        VERDICT_DEMOTED,
        "Gravity is out of scope for the present framework unless a future gate supplies Lorentzian dynamics.",
        open_bridges=("Canonical invariant four-plane, Lorentzian signature, and dynamics are absent.",),
        kill_conditions=("A hand-picked four-plane or non-dynamical metric is the only available construction.",),
    ),
    "prediction_registry": contract(
        "prediction_registry",
        ("N1", "N5"),
        STATUS_LOCKED_REGISTRY,
        VERDICT_LOCKED,
        "Future-facing claims are authoritative only when they are hash-locked here.",
        kill_conditions=("Silent retune or digest drift in any frozen prediction entry.",),
        locked_predictions=("Sigma_m_nu", "Theta23_octant", "P2_m_betabeta"),
        bridge_sensitivities=("P1_m_nu3_tension", "P3_kappa_lambda"),
    ),
    "scoreboard": contract(
        "scoreboard",
        ("STAT1", "F0"),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Move Bayes credit only when ledger statuses change; F0 remains the sign-flip hinge.",
        open_bridges=("Whether epsilon0^2 = pi/432 is geometrically forced at theorem level.",),
    ),
}


def contract_records() -> list[dict[str, object]]:
    return [asdict(contract_entry) for contract_entry in CONTRACTS.values()]


def validation_payload(
    artifact_names: Iterable[str],
    positive_prediction_names: Iterable[str],
    bridge_sensitivity_names: Iterable[str],
) -> dict[str, object]:
    errors = validate_contracts(artifact_names)
    errors.extend(validate_prediction_contract(positive_prediction_names, bridge_sensitivity_names))
    return {
        "audit_status": "PASS" if not errors else "FAIL",
        "registered_artifacts": list(artifact_names),
        "contracted_artifacts": list(CONTRACTS),
        "contracts": contract_records(),
        "errors": errors,
    }


def validate_contract(contract_entry: AuditContract) -> list[str]:
    errors = []
    if not re.match(r"^[a-z0-9_]+$", contract_entry.artifact):
        errors.append(f"{contract_entry.artifact}: artifact name must be snake_case")
    if not contract_entry.ledger_ids:
        errors.append(f"{contract_entry.artifact}: missing ledger_ids")
    for ledger_id in contract_entry.ledger_ids:
        if not LEDGER_ID_RE.match(ledger_id):
            errors.append(f"{contract_entry.artifact}: invalid ledger id {ledger_id!r}")
    if contract_entry.status not in ALLOWED_STATUSES:
        errors.append(f"{contract_entry.artifact}: invalid status {contract_entry.status!r}")
    if contract_entry.verdict not in ALLOWED_VERDICTS:
        errors.append(f"{contract_entry.artifact}: invalid verdict {contract_entry.verdict!r}")
    if not contract_entry.public_claim_policy.strip():
        errors.append(f"{contract_entry.artifact}: missing public_claim_policy")
    if contract_entry.status in OPEN_STATUSES and not contract_entry.open_bridges:
        errors.append(f"{contract_entry.artifact}: open status requires open_bridges")
    if contract_entry.verdict == VERDICT_OPEN and contract_entry.status != STATUS_DIAGNOSTIC and not contract_entry.open_bridges:
        errors.append(f"{contract_entry.artifact}: open verdict requires open_bridges")
    if contract_entry.status in {STATUS_FUTURE_TEST, STATUS_LOCKED_REGISTRY, STATUS_OUT_OF_SCOPE} and not contract_entry.kill_conditions:
        errors.append(f"{contract_entry.artifact}: status {contract_entry.status!r} requires kill_conditions")
    if contract_entry.status == STATUS_OUT_OF_SCOPE and contract_entry.verdict != VERDICT_DEMOTED:
        errors.append(f"{contract_entry.artifact}: out_of_scope must use demoted verdict")
    return errors


def validate_contracts(artifact_names: Iterable[str] | None = None) -> list[str]:
    errors = []
    for contract_entry in CONTRACTS.values():
        errors.extend(validate_contract(contract_entry))

    if artifact_names is not None:
        registered_artifacts = set(artifact_names)
        contracted_artifacts = set(CONTRACTS)
        missing = sorted(registered_artifacts - contracted_artifacts)
        extra = sorted(contracted_artifacts - registered_artifacts)
        if missing:
            errors.append("missing contracts: " + ", ".join(missing))
        if extra:
            errors.append("contracts for non-audit artifacts: " + ", ".join(extra))
    return errors


def validate_prediction_contract(
    positive_prediction_names: Iterable[str],
    bridge_sensitivity_names: Iterable[str],
) -> list[str]:
    registry_contract = CONTRACTS["prediction_registry"]
    errors = []
    positives = tuple(positive_prediction_names)
    sensitivities = tuple(bridge_sensitivity_names)
    if registry_contract.locked_predictions != positives:
        errors.append(
            "prediction_registry locked_predictions mismatch: "
            f"contract={registry_contract.locked_predictions!r}, registry={positives!r}"
        )
    if registry_contract.bridge_sensitivities != sensitivities:
        errors.append(
            "prediction_registry bridge_sensitivities mismatch: "
            f"contract={registry_contract.bridge_sensitivities!r}, registry={sensitivities!r}"
        )
    return errors


def _artifact_names_from_audit() -> tuple[str, ...]:
    import audit

    return tuple(name for name, _, _ in audit.ARTIFACTS)


def _prediction_names_from_registry() -> tuple[tuple[str, ...], tuple[str, ...]]:
    import prediction_registry

    positives = tuple(
        entry.name
        for entry in prediction_registry.FROZEN_ENTRIES
        if entry.category == "positive_quantitative"
    )
    sensitivities = tuple(
        entry.name
        for entry in prediction_registry.FROZEN_ENTRIES
        if entry.category == "bridge_sensitivity"
    )
    return positives, sensitivities


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and export CHO audit contracts.")
    parser.add_argument("--json", action="store_true", help="emit machine-readable contract JSON")
    args = parser.parse_args()

    artifact_names = _artifact_names_from_audit()
    positive_prediction_names, bridge_sensitivity_names = _prediction_names_from_registry()
    payload = validation_payload(artifact_names, positive_prediction_names, bridge_sensitivity_names)
    errors = payload["errors"]

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        if errors:
            sys.exit(1)
        return

    print("CHO THEORY VALIDATION CONTRACT")
    print(f"registered audit artifacts : {len(artifact_names)}")
    print(f"contracted artifacts       : {len(CONTRACTS)}")
    print()
    for contract_entry in CONTRACTS.values():
        ledger = ",".join(contract_entry.ledger_ids)
        print(f"{contract_entry.artifact:<34} {contract_entry.status:<16} {contract_entry.verdict:<11} {ledger}")

    if errors:
        print()
        print("AUDIT STATUS: FAIL - theory-validation contract drift detected.")
        for error in errors:
            print(" - " + error)
        sys.exit(1)

    print()
    print("AUDIT STATUS: PASS - every artifact has a structured claim contract.")


if __name__ == "__main__":
    main()