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
    "per_row_theory_error": contract(
        "per_row_theory_error",
        ("STAT1", "S1", "S4", "S5", "N1"),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Quote theory errors per row by derivation status; tighten a row ONLY "
        "when its bridge is derived. Never quote sub-percent precision for the "
        "eps0-ladder rows (m_s, m_mu) -- a 0.5% claim is falsified at >2 sigma.",
        open_bridges=(
            "alpha (S1 vacuum polarization) and sin^2 theta_W (S4/S5 RG scale) are "
            "derivation-limited: only the term is derived, so they carry no "
            "precision evidence and are excluded from the precision chi^2.",
            "The eps0-ladder normalization (geometric tier ~1.5%) is not derived, "
            "so the ladder rows cannot be promoted to sub-percent predictions.",
        ),
        kill_conditions=(
            "Lowering one global theory floor instead of tightening per row by status.",
            "Setting a row's theory error from its residual rather than its bridge status.",
            "Quoting the comfortable per-row chi^2 as evidence while hiding the stringent-core tension or the derivation-limited rows.",
            "Promoting any row or moving the scoreboard / Bayes factor on the basis of this GoF refinement.",
        ),
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
    "rg_scale_derivation": contract(
        "rg_scale_derivation",
        ("S4", "S5"),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only the NEGATIVE/sharpening result: CHO's two electroweak boundaries "
        "(alpha_em^-1 = 128*pi/3 and sin^2(theta_W) = 1/4) cannot both hold at one matching "
        "scale -- one-loop running needs scales ~1.8e4 apart (alpha_1^-1 at ~12 GeV, "
        "alpha_2^-1 at ~2.2e5 GeV); the lone sin^2=1/4 inverse match is M_P/3^32.5 (a "
        "non-integer power of 3) and no independently-derived CHO scale (v, M_W, seesaw, "
        "M_P) yields sin^2=1/4. This TRIGGERS the rg_matching_audit kill condition: the "
        "matching scale is inverse-fit, not derived. Do NOT present this as deriving the "
        "scale, and do NOT promote S4/S5 or touch the scoreboard.",
        open_bridges=(
            "Derive a single electroweak matching scale (and threshold/VP scheme) from the "
            "CHO action, or accept that alpha and sin^2 are independent low/high-scale "
            "inputs and demote the precision claims accordingly.",
        ),
        kill_conditions=(
            "The over-determination negative is spun as a positive derivation of the scale.",
            "sin^2=1/4 or alpha_em^-1=128*pi/3 is quoted as a closed prediction on the back "
            "of an inverse-fit scale.",
            "S4/S5 are promoted, or model_complexity/scoreboard credit is claimed.",
        ),
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
    "neutrino_floor_resolution": contract(
        "neutrino_floor_resolution",
        ("N1",),
        STATUS_DIAGNOSTIC,
        VERDICT_DEMOTED,
        "State the m_nu3 floor deficit as a ~1.2-sigma undershoot (theory error folded), "
        "NOT a 4.6-sigma falsification and NOT a precision success; the central value "
        "sits just below the physical floor and N1 is demoted to order-1 consistency.",
        assumptions=(
            "Tree-level m_nu3 theory error is calibrated from the M_W (M_P/3^36) and "
            "y_t=1 (m_t=v/sqrt2) sister rows: sqrt((2*0.78%)^2+(1.21%)^2) ~= 2.0%.",
        ),
        open_bridges=(
            "Derive the O(1) seesaw normalization (M_R prefactor) and the y_nu3=1 "
            "saturation, replacing the sister-calibrated theory error with a pinned value.",
        ),
        kill_conditions=(
            "Theory error is inflated beyond the sister-calibrated ~2% to dodge the deficit.",
            "The sub-floor central value (48.9 < 50.1 meV) is hidden or spun as a success.",
            "N1 is quoted as a ~2% precision prediction after this demotion.",
            "A pinned, DERIVED normalization still falls below the floor yet is reported as consistent.",
        ),
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
    "theta23_octant_prediction": contract(
        "theta23_octant_prediction",
        ("N5",),
        STATUS_FUTURE_TEST,
        VERDICT_FUTURE_TEST,
        "State sin^2(theta23)=4/7 (upper octant) as the single sharpest CHO bet: the only "
        "eps0-independent EXACT mixing rational, and a pre-registered verdict on a "
        "currently-unresolved binary. The frozen registry (Q2, Theta23_octant) stays "
        "authoritative; this module is the read-only analysis around it, not new evidence. "
        "Do NOT quote the octant as already confirmed and do NOT let it move the Bayes factor.",
        assumptions=(
            "N5 Fano-count bridge: sin^2(theta23) = (Fano lines avoiding the vacuum, 4) / "
            "(all Fano lines, 7) once the vacuum omega=(1+i e7)/2 fixes the point e7; the "
            "octant follows from 4 avoiding > 3 through-vacuum.",
            "Experimental anchors in the module are illustrative NuFIT-class normal-ordering "
            "numbers for context only; they are printed, never asserted.",
        ),
        open_bridges=(
            "The Fano-count -> physical atmospheric-angle map is a DERIVED BRIDGE (N5), not a "
            "hand-proven CHO-action theorem; 4/7 is exact only GIVEN that bridge.",
            "The octant is currently experimentally UNRESOLVED (T2K/NOvA tension); this is a "
            "forward bet awaiting DUNE / Hyper-Kamiokande.",
        ),
        kill_conditions=(
            "A stable lower-octant resolution (sin^2 theta23 < 1/2, the 3/7 side) at high confidence.",
            "An upper-octant value pinned far from 4/7, beyond the few-percent N5 bridge error.",
            "The octant claim is quoted as already-confirmed rather than a pre-registered bet.",
            "The N5 Fano bridge is presented as a closed theorem instead of a derived bridge.",
            "This forward test is allowed to promote a ledger row or move the Bayes factor.",
        ),
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
    "lepton_yukawa_action": contract(
        "lepton_yukawa_action",
        ("M11", "M3"),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only that the charged-lepton Yukawa is assembled as ONE Hermitian operator "
        "from ONE action's two-level Bloch sphere: the SAME S^2 whose hemisphere solid angle "
        "(2*pi) gives the Berry theta=pi supplies the first-generation shape factor "
        "k_l=1/(4*pi) as its total-solid-angle (Schur invariant-average) normalization. The "
        "second-generation 8 is the REUSED Fock trace (M3) and the cascade square is the "
        "rank-one bottleneck. The genuine increment is that 1/(4*pi) is FORCED (an invariant "
        "average), not chosen. Do NOT claim the trilinear is derived from CHO equations of "
        "motion, that the sector resolution is explained, or that the m_e residual is resolved.",
        open_bridges=(
            "Derive WHY the lepton first-generation channel uses the continuous-sphere "
            "(uniform SU(2)) average while the quark sectors use discrete weak-isospin "
            "projections (k_u=1/4, k_d=9/4, no pi).",
            "Derive the charged-lepton trilinear Yukawa from the CHO action's equations of "
            "motion; this module uses the action's geometry plus the derived traces, not a "
            "dynamical field equation.",
            "Resolve the ~6% intrinsic m_e first-generation residual (ledger M11, "
            "first_generation_audit.py).",
        ),
        kill_conditions=(
            "The single-operator assembly is presented as a full action-level derivation of "
            "the charged-lepton Yukawa rather than a geometry-plus-derived-traces assembly.",
            "The sphere-vs-discrete sector resolution is glossed as derived, or the e/tau "
            "-6.3% outlier is hidden behind the mu/tau -2.2% match.",
            "F0 is promoted or the up/down sectors are claimed closed from this lepton unit.",
        ),
    ),
    "sector_sphere_dichotomy": contract(
        "sector_sphere_dichotomy",
        ("M9", "M10", "M11", "M3"),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only the DISCRIMINANT shared by the first-generation shape factors: pi appears "
        "IFF the transition is averaged over a CONTINUOUS manifold (the colour-singlet lepton's "
        "two-level Bloch sphere S^2, giving k_l=1/(4pi)) and is ABSENT (rational) IFF over a "
        "DISCRETE Fock grade (the coloured quarks, k_u=1/4, k_d=9/4). Verified: a finite group "
        "(Q8) averages a rank-one projector to EXACTLY I/2 (rational, no pi) while the sphere "
        "gives 1/(4pi); and k_u=(Tr P_0/2)^2, k_d=(Tr P_1/2)^2=(1/4)N_c^2 reuse the SAME derived "
        "Fock-grade ranks (Tr P_0=1, Tr P_1=3=N_c). Do NOT claim M9/M10/M11 are closed: WHY the "
        "colour singlet uses the continuous average while the coloured sectors project onto a "
        "single grade (the dynamical selection) is still an input.",
        open_bridges=(
            "Derive from the CHO action the colour-singlet -> continuous-sphere vs coloured -> "
            "discrete-Fock-grade SELECTION, not merely its pi-vs-rational consequence.",
            "Promote the (Tr P_grade/2)^2 quark shape law (fit on the two quark sectors) to a "
            "multi-sector theorem, and resolve the ~6% intrinsic m_e residual (M11).",
        ),
        kill_conditions=(
            "The pi-vs-rational discriminant is presented as deriving the sector SELECTION, or "
            "M9/M10/M11 are marked closed from this module.",
            "The (Tr P_grade/2)^2 quark law is treated as a derived theorem rather than a "
            "two-sector fit tied to the already-derived Fock ranks, or F0 is promoted.",
        ),
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
    "epsilon_measure_schur": contract(
        "epsilon_measure_schur",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only that the 1/16 and 1/27 measure weights are FORCED by irreducibility "
        "(Schur): Spin(9) acts irreducibly on Delta_9 and the full cubic-norm group E6 "
        "(not F4 alone, which leaves 27 = 1+26) acts irreducibly on J3(O). Do NOT promote "
        "F0 to derived: the product phase space Delta_9 (x) J3(O) is still identified by hand.",
        open_bridges=("Derive why the transition phase space is the PRODUCT Delta_9 (x) J3(O) "
                      "(the representation identification), not merely its flat normalization.",),
        kill_conditions=("The flat 1/16 or 1/27 average is presented as a chosen normalization "
                         "rather than the Schur consequence of Spin(9)- / E6-irreducibility.",
                         "F4-on-27 reducibility (27 = 1 + 26) is glossed so that the full E6 "
                         "looks optional for the clean 1/27."),
    ),
    "epsilon_phase_space_product": contract(
        "epsilon_phase_space_product",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only that, under independent commuting sector actions (Spin(9) on Delta_9 and "
        "E6 on J3(O)), the canonical carrier is the tensor product Delta_9 (x) J3(O), and the "
        "factorized invariant average gives 1/432 exactly. Do NOT promote F0: deriving this "
        "sector-independence from the CHO action remains open.",
        open_bridges=("Derive Assumption P (independent commuting gauge/flavour sectors with "
                      "minimal multiplicity) from the CHO action / one-operator dynamics.",),
        kill_conditions=("The product carrier Delta_9 (x) J3(O) is presented as theorem-level "
                         "without stating the sector-independence assumption.",
                         "Direct-sum or single-sector alternatives are treated as equivalent to "
                         "a shared one-operator transition density over both sectors."),
    ),
    "epsilon_product_irreducible": contract(
        "epsilon_product_irreducible",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only that Delta_9 (x) J3(O) is irreducible under the factor-wise product group "
        "Spin(9) x E6, so by Schur ANY rank-one spurion (separable OR entangled) averages to "
        "I_432/432. This removes the separable-projector and minimal-multiplicity clauses of "
        "Assumption P, leaving the single clause 'factor-wise product invariance'. Do NOT promote "
        "F0: deriving that product arena / factor-wise symmetry from the CHO action remains open.",
        open_bridges=("Derive the factor-wise Spin(9) x E6 product symmetry (equivalently the "
                      "432-dim product arena) from the CHO action; foundations/02_action.md selects "
                      "theta=pi on the two-level sphere but does not supply the product arena.",),
        kill_conditions=("Product irreducibility is presented as a full action-level derivation of "
                         "Assumption P rather than a reduction of its clauses.",
                         "The surviving factor-wise-invariance clause is glossed as already derived, "
                         "or the F4 necessity control (factor-wise E6 is required) is omitted."),
    ),
    "epsilon_symplectic_volume": contract(
        "epsilon_symplectic_volume",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only that 16 and 27 are the Bohr-Sommerfeld / Borel-Weil dimensions of single "
        "coadjoint orbits (Spin(9) spinor, E6 minimal), so the product orbit's Liouville volume "
        "is 16x27=432 by multiplicativity, and pi is the half-flux of the minimal transition orbit "
        "CP^1 -- giving pi/432 as one geometric-quantization object. Do NOT promote F0: deriving "
        "which two orbits the CHO action quantizes remains open, and OP^2=F4/Spin(9) is itself "
        "non-symplectic (the carriers are orbits in so(9)^*, e6^*, not OP^2).",
        open_bridges=("Derive from the CHO action that the triality-breaking transition quantizes "
                      "exactly the Spin(9)-spinor and E6-minimal coadjoint orbits (which two orbits), "
                      "rather than assuming them; the product-of-volumes factorization then follows.",),
        kill_conditions=("The orbit-method factorization is presented as deriving the product arena "
                         "from the action, rather than recasting the assumed product as one product "
                         "orbit.",
                         "OP^2 is treated as a symplectic carrier, or the bare pi half-flux is "
                         "conflated with the full 2pi flux quantum."),
    ),
    "epsilon_orbit_selection": contract(
        "epsilon_orbit_selection",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only that the two coadjoint orbits behind 16 and 27 are the MINIMAL "
        "(coherent-state) orbits, and that 'minimal' is FORCED for both factors: (16) "
        "Spin(9) acts TRANSITIVELY on the spinor sphere S^15 (orbit-tangent dim 15 "
        "everywhere, stabiliser 21 = dim Spin(7)) so the spinor orbit is unique; (27) the "
        "E6 minimal orbit is the rank-one variety (Freudenthal X#=0), which is EXACTLY the "
        "action's own rank-one selection (epsilon_rank_one_kernel, epsilon_action_stationary). "
        "Do NOT promote F0: this GRANTS coherent-state (minimal-orbit) quantization and the "
        "external Delta_9 identification; it reduces 'which two orbits (assumed)' to 'the two "
        "minimal orbits (forced)', it does not derive coherent-state localization from CHO dynamics.",
        open_bridges=(
            "Derive from the FULL CHO dynamics that the triality-breaking transition LOCALIZES "
            "to a coherent (minimal-orbit) state -- the coherent-state hypothesis itself -- "
            "rather than assuming minimal-orbit quantization.",
            "Promote the Spin(9)-module isomorphism Delta_9 ~= T_E(OP^2) (route 4c) to a "
            "dynamical identity of the external gauge spinor with the internal minimal-orbit tangent.",
        ),
        kill_conditions=(
            "The coherent-state / minimal-orbit selection is presented as a full action-level "
            "derivation of WHICH two orbits the CHO action quantizes, rather than a forcedness "
            "result GIVEN coherent-state quantization.",
            "Spin(9)-transitivity on S^15 or the rank-one = E6-minimal identification is glossed "
            "as deriving the product arena, or F0 is promoted from this module.",
        ),
    ),
    "epsilon_factor_forcedness": contract(
        "epsilon_factor_forcedness",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only that 16x27 is the unique factorization of 432 whose BOTH factors are "
        "independently-derived transition carriers (16=Delta_9=dim OP^2, 27=dim J3(O)), and that "
        "432 is a fundamental/minimal irrep of no single simple group (G2..E8 scan) while being the "
        "Spin(9)xE6 bifundamental -- so a product realization is the economical one. This removes "
        "the factorization freedom; it does NOT by itself derive the two carrier dimensions, and "
        "does NOT promote F0.",
        open_bridges=("Derive (via the symplectic/Schur work) that the two carriers are 16- and "
                      "27-dimensional; this audit only shows no other split competes and that a "
                      "single simple group cannot host 432 as a minimal rep.",),
        kill_conditions=("The minimal/fundamental-rep scan is presented as an absolute no-go "
                         "(large non-fundamental irreps of dimension 432 do exist).",
                         "The derived-carrier ranking is presented as deriving 16 and 27 rather than "
                         "ranking pre-derived structure, or the forcedness registry is silently "
                         "tuned to make 16x27 win."),
    ),
    "epsilon_assumption_p_gate": contract(
        "epsilon_assumption_p_gate",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Treat this as operator-level evidence for Assumption P only: the scaffold epsilon "
        "operator is exactly primitive product-separable across 16x27 with pi/432 normalized "
        "trace. Do NOT promote F0 from this gate alone.",
        open_bridges=("Derive the separable primitive epsilon operator structure from the CHO "
                      "action / one-operator dynamics, rather than inserting it as scaffold data.",),
        kill_conditions=("Operator-level separability evidence is presented as a full derivation "
                         "of Assumption P without an action-level mechanism.",
                         "A non-separable mixed operator is treated as equivalent to the primitive "
                         "product kernel for the epsilon bridge value."),
    ),
    "epsilon_action_stationary": contract(
        "epsilon_action_stationary",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only that within the normalized link-action admissible class "
        "(O>=0, Tr(O)=pi), the primitive kernel O=pi|tau><tau| is the unique "
        "global maximizer and the current scaffold saturates that bound.",
        open_bridges=("Derive the physical transition ray tau and admissible "
                      "kernel class from full CHO action/one-operator dynamics.",),
        kill_conditions=("A variational result inside the chosen link-action class is "
                         "presented as full derivation of the CHO kernel dynamics.",
                         "The distinction between 'unique maximizer in class' and "
                         "'class derived from action' is collapsed."),
    ),
    "epsilon_action_selection": contract(
        "epsilon_action_selection",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only that the rank-one transition ray is the critical / global-"
        "minimising locus of the E6-invariant cubic norm N3 on the J3(O) state "
        "space, because the Freudenthal sharp is its gradient (X#=grad N3): the "
        "unconstrained critical set is X#=0 (rank<=1); the trace-constrained "
        "critical set X#=lam I is exactly {rank-one} U {central cI}; and on the "
        "physical slice {O>=0, Tr O=1} the cubic is in [0,1/27] (AM-GM) with the "
        "rank-one idempotents the global minimisers and I/3 the unique maximiser. "
        "This removes the rank-one INPUT of epsilon_action_stationary on the "
        "configuration-space side ('rank-one assumed' -> 'rank-one = minimiser of "
        "the invariant cubic potential'), and ties that same N3 (whose symmetry "
        "group E6 forces the flat 1/27 measure via epsilon_measure_schur) to the "
        "ray selection. Do NOT promote F0: this characterises the ray variationally; "
        "it does not derive that the CHO action's potential IS this cubic.",
        open_bridges=("Derive from the full CHO dynamics that the action's potential "
                      "term IS the E6-invariant cubic N3, rather than identifying it.",
                      "Fix the kinetic coefficient multiplying the great-circle Berry "
                      "angle (pi) and write the full time-dependent equations of motion "
                      "whose relaxation lands on the minimal-orbit (coherent) state."),
        kill_conditions=("The variational characterisation of the ray (minimiser of N3) "
                         "is presented as a full action-level derivation of the CHO "
                         "transition kernel, or as deriving the action's potential.",
                         "The value coincidence max N3 = 1/27 = 1/dim is leaned on as a "
                         "structural identity (it holds only because dim J3(O)=27=3^3), "
                         "or F0 is promoted / Bayes credit is moved from this module."),
    ),
    "f0_vacuum_majorization": contract(
        "f0_vacuum_majorization",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only that the rank-one transition ray is the MAJORIZATION-MAXIMAL "
        "element of the J3(O) state slice {O>=0, Tr O=1}: its spectrum (1,0,0) "
        "majorises every state and the maximally-mixed centre I/3 is majorised by "
        "every state. By Hardy-Littlewood-Polya this one order fixes the extremiser "
        "of an ENTIRE universality class of spectral actions at once \u2014 every "
        "Schur-concave action (the cubic norm N3=det, the von Neumann and Renyi "
        "entropies) is minimised at rank-one, and every Schur-convex action (purity "
        "Tr O^2, and the leading -a Tr Phi^2 + b Tr Phi^4 term of a Connes finite "
        "spectral action) is extremised there. This STRENGTHENS epsilon_action_selection "
        "from one chosen functional (the cubic norm) to a functional-independent "
        "statement, and connects the F0 vacuum to the standard spectral-action "
        "framework: a Connes-type action selects the same rank-one ray. Honest "
        "corrective: the spectral potential is EVEN (degree 2/4) whereas N3 is degree "
        "3, so they are DIFFERENT functionals that agree only on the vacuum. Do NOT "
        "promote F0: majorisation fixes the vacuum DIRECTION, not which action CHO "
        "realises, the kinetic coefficient, or the pi/432 normalisation.",
        open_bridges=("Derive from the full CHO dynamics WHICH action in the "
                      "Schur-concave/convex class is physically realised (majorisation "
                      "is agnostic to the choice within the class).",
                      "Fix the kinetic coefficient on the great-circle Berry angle (pi) "
                      "and the pi/432 normalisation; majorisation fixes only the vacuum "
                      "direction, not the transition measure."),
        kill_conditions=("The majorisation robustness is presented as deriving the "
                         "physical CHO action, the cubic-norm identification, or the "
                         "pi/432 normalisation.",
                         "F0 is promoted or Bayes credit is moved from this module \u2014 it "
                         "is a robustness theorem about the vacuum direction, not a "
                         "closure of the measure."),
    ),
    "f0_spectral_triple_gate": contract(
        "f0_spectral_triple_gate",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only the HONEST axiom ledger of the Phase-1.1 assembly: on the CHO "
        "432-space the KO-dim-6 spin brick (gamma8 = i L_1..L_6, J8 = complex "
        "conjugation, eps=+1/eps''=-1) is consistent and the assembled "
        "D = gamma8 (x) D_F is a self-adjoint, chirality-odd operator with "
        "gamma^2 = J^2 = +I -- the metric/real-structure HALF of a finite spectral "
        "triple. But the naive (A,H,D) is NOT yet a spectral triple: (1) the "
        "order-zero axiom [a, b^o] = 0 equals the octonion associator and FAILS for "
        "A = C(x)H(x)O (residual ~16; recovered only on a genuine associative "
        "bimodule ~1e-15 or on the complex line via flexibility), so A must be "
        "replaced by its associative/special-Jordan envelope; (2) the chirality-EVEN "
        "Jordan Yukawa L_X needs particle/antiparticle doubling, pushing the finite "
        "KO-dimension to 6+6 = 4 (mod 8) instead of 6. Both are KNOWN, repairable "
        "obstructions, NOT the irreparable KILL. Do NOT present the triple as "
        "existing, do NOT compute a spectral action on this naive object, and move "
        "NO Bayes credit: F0 stays GEOMETRIC/open and eps0^2 = pi/432 is not promoted.",
        open_bridges=(
            "Rebuild A as the associative/special-Jordan envelope (or a genuine "
            "associative bimodule) so order-zero and order-one hold; the octonion "
            "algebra acting on its own module violates both.",
            "Embed the Yukawa in the KO-dim-6 real structure (off-diagonal of J) "
            "rather than as an extra graded factor, so the finite KO-dimension stays "
            "6 instead of doubling to 4.",
            "Only once a consistent triple exists can Phase 1.2 (heat-kernel a0/a2/a4 "
            "as traces of Y) and Phase 1.3 (is pi/432 the normalised a4/a2 ratio?) run.",
        ),
        kill_conditions=(
            "The naive non-associative (A,H,D) is presented as a finished spectral "
            "triple, or a spectral action is computed on it as if the axioms held.",
            "The order-zero/associator failure or the KO-dimension doubling is hidden "
            "or spun as a success.",
            "F0 is promoted, eps0^2 = pi/432 is called geometrically forced, or "
            "model_complexity/scoreboard credit is claimed on the back of this assembly.",
        ),
    ),
    "f0_real_structure_gate": contract(
        "f0_real_structure_gate",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only the precise real-structure DICHOTOMY and its named resolution, "
        "computed on the octonion brick. A finite spectral triple has ONE real "
        "structure J and EVERY axiom must hold for that SAME J; the Phase-1.1 gate "
        "tested KO signs against J=conjugation but order-zero against right-mult, two "
        "different J's. Testing both axioms against each J shows: with J = complex "
        "conjugation (the KO-dim-6 choice) the opposite algebra J L_a J^-1 = L_a "
        "coincides with A, so order-zero forces A COMMUTATIVE (quaternions fail ~14, "
        "only the complex line holds ~1e-16) -- no SU(2)/SU(3) on one brick; with "
        "J = octonion conjugation one gets genuine right-multiplication (J L_a J^-1 "
        "= -R_a), order-zero becomes the associator and holds on the quaternion "
        "bimodule (~1e-15) for a noncommutative A, BUT J gamma J^-1 = -0.5 gamma is "
        "not +-gamma so the grading is not J-compatible and the KO-dimension is "
        "undefined. Hence on one irreducible brick NO single J yields BOTH KO-6 AND "
        "a noncommutative order-zero algebra. The RESOLUTION is the standard Connes "
        "route, computed here: a nonabelian A on A (x) A^o satisfies order-zero "
        "exactly (0) by left-right commutation, so the octonions must GRADE the "
        "module (gamma8, charges) rather than be the order-zero *-algebra. This "
        "SHARPENS the Phase-1.1 obstruction and names the rebuild; it does NOT build "
        "the triple and moves NO Bayes credit: F0 stays GEOMETRIC/open, eps0^2 = "
        "pi/432 is not promoted.",
        open_bridges=(
            "Carry out the associative rebuild A = C (+) H (+) M_3(C) acting on "
            "A (x) A^o as a genuine product triple that RESTORES KO-dimension 6, with "
            "the octonion brick supplying only the grading and charges.",
            "Embed the chirality-even Jordan Yukawa in the real-structure (Majorana) "
            "sector so the finite KO-dimension stays 6 rather than doubling to 4 "
            "(the second Phase-1.1 tension, still open).",
            "Only once that consistent KO-6 triple exists can Phase 1.2 (heat-kernel "
            "a0/a2/a4 as traces of Y) and Phase 1.3 (is pi/432 the a4/a2 ratio?) run.",
        ),
        kill_conditions=(
            "The dichotomy is spun as if a single J on one brick delivered both KO-6 "
            "and a noncommutative order-zero algebra.",
            "The A (x) A^o resolution is presented as a finished spectral triple, or "
            "a spectral action is computed on it, before the KO-6-restoring rebuild "
            "and the Yukawa real-structure embedding are actually carried out.",
            "F0 is promoted, eps0^2 = pi/432 is called geometrically forced, or "
            "model_complexity/scoreboard credit is claimed on the back of this gate.",
        ),
    ),
    "f0_associative_triple_gate": contract(
        "f0_associative_triple_gate",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only that the associative rebuild NAMED by f0_real_structure_gate "
        "is constructively realised for the one-generation LEPTON sector, and that "
        "it forms a consistent KO-dimension-6 finite real spectral triple with a "
        "nonzero Yukawa+Majorana Dirac for a SINGLE real structure J. Computed from "
        "explicit matrices: order-zero [a_L,b_R]=0 holds exactly (~9e-16) on "
        "A (x) A^o for the NONCOMMUTATIVE summands H and M_3(C) and for the SM "
        "lepton rep; KO-dimension 6 is RESTORED (J^2=+I, J gamma J^-1 = -gamma), "
        "chirality without doubling; and an explicit physical Dirac with Dirac "
        "Yukawas plus a Majorana mass is Hermitian, gamma-odd, J-real and satisfies "
        "order-one [[D,a],b^o]=0 (~9e-16), so the seesaw sits in the real-structure "
        "sector and the finite KO-dim stays 6. This REPAIRS the Phase-1.1 'triple "
        "does not exist' verdict at the level of the associative skeleton. It must "
        "be stated HONESTLY that this recovers the KNOWN Connes-Chamseddine-Marcolli "
        "skeleton -- the constructive complement to the no-go, NOT new physics -- "
        "and that it moves NO Bayes credit: F0 stays GEOMETRIC/open, eps0^2 = pi/432 "
        "is not promoted.",
        open_bridges=(
            "Replace the generic Dirac Yukawa by the SPECIFIC octonionic Jordan mass "
            "operator L_X and realise the full 432 = 16 (A_Weyl) x 27 (J3(O)) module "
            "(step C); only the 8-dim colour-singlet lepton slice is built here.",
            "Extend the explicit construction to the quark colour sector (the M_3(C) "
            "factor is only checked to commute) and to three generations, confirming "
            "order-zero/order-one and KO-6 survive the full SM content.",
            "Phase 1.3: show eps0^2 = pi/432 emerges as the spectral-action ratio "
            "a4/a2 of this triple -- epsilon_heat_kernel warns the spectral pi enters "
            "only via the Gaussian (4 pi)^(-d/2), so a bare pi numerator is unlikely.",
        ),
        kill_conditions=(
            "The recovered skeleton is presented as new/CHO-specific physics rather "
            "than the known Connes-Chamseddine-Marcolli construction.",
            "The generic Yukawa+Majorana Dirac is described as if it were already the "
            "octonionic Jordan mass operator L_X, or the 8-dim lepton slice is passed "
            "off as the full 432-dimensional module.",
            "F0 is promoted, eps0^2 = pi/432 is called geometrically forced, or "
            "model_complexity/scoreboard credit is claimed on the back of this gate.",
        ),
    ),
    "f0_octonionic_yukawa_gate": contract(
        "f0_octonionic_yukawa_gate",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only the precise two-sided result, computed from explicit 8x8 / "
        "27x27 / 216x216 matrices, of putting the SPECIFIC octonionic Jordan mass "
        "operator L_X into the step-B KO-6 triple. The faithful SM finite geometry "
        "is H = C^8 (x) C^27 (the step-B lepton charge factor tensored with the "
        "J3(O) flavour 27), with the Yukawa K_Yuk (x) L_X: the charge L<->R coupling "
        "K_Yuk is gamma1-ODD and L_X is the UNGRADED octonionic generation matrix "
        "(gamma = gamma1 (x) I27, J = J1 (x) conj). POSITIVE half: L_X is the genuine "
        "averaging-law operator (spectrum = three singlets {1,0.6,0.3} and three "
        "octets {0.8,0.65,0.45} of mult 8, 27 total) and it needs NO doubling -- "
        "because chirality sits in the charge factor, the product Dirac "
        "D = K_Yuk (x) L_X + K_Maj (x) M_maj is self-adjoint, gamma-odd, J-real, "
        "order-zero/order-one ~1e-15, and KO-dim 6 (eps=+1, eps''=-1). This DISSOLVES "
        "the second Phase-1.1 obstruction (L_X chirality-even -> doubling -> the "
        "6(x)6->4 KO collapse). SOBERING half, which must be stated with equal "
        "weight: order-one factors through the charge sector (each charge coupling "
        "tensored with a RANDOM Hermitian flavour operator still satisfies order-one, "
        "~1e-14 and 0), so the gauge algebra sees the flavour factor as pure "
        "multiplicity and ANY self-adjoint flavour operator passes -- the octonionic "
        "texture is ADMISSIBLE but NOT FORCED by the spectral-triple axioms. Moves "
        "NO Bayes credit: F0 stays GEOMETRIC/open, eps0^2 = pi/432 is not promoted.",
        open_bridges=(
            "The triple axioms do NOT fix the Yukawa; the CHO mass texture (the "
            "averaging law) must be shown to be SELECTED by the spectral action "
            "Tr f(D/Lambda) (Phase 1.3), not merely admitted by the triple.",
            "Phase 1.3: show eps0^2 = pi/432 emerges as the spectral-action ratio "
            "a4/a2 -- epsilon_heat_kernel warns the spectral pi enters only via the "
            "Gaussian (4 pi)^(-d/2), so this test is more likely to REFUTE than "
            "confirm the bare pi numerator.",
            "Extend from the C^8 (x) C^27 lepton slice to the full 432 = 16 x 27 "
            "module with the quark colour sector and three generations, confirming "
            "the no-doubling KO-6 construction survives the full SM content.",
        ),
        kill_conditions=(
            "The POSITIVE half (L_X slots into a KO-6 triple) is reported while the "
            "SOBERING half (the axioms do not force the Yukawa) is omitted or muted.",
            "The averaging-law spectrum of L_X is presented as if the triple axioms "
            "DERIVED it, rather than merely admitting it as one of many self-adjoint "
            "flavour operators.",
            "F0 is promoted, eps0^2 = pi/432 is called geometrically forced, or "
            "model_complexity/scoreboard credit is claimed on the back of this gate.",
        ),
    ),
    "f0_spectral_action_heatkernel": contract(
        "f0_spectral_action_heatkernel",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only the precise, two-sided result of the Phase-1.3 decisive "
        "experiment, computed from the explicit 216x216 step-C octonionic Dirac D. "
        "For the finite triple the Seeley-DeWitt coefficients ARE the spectral "
        "moments a0 = M0 = Tr(1) = 216, a2 = M2 = Tr(D^2) = 92.96, a4 = M4 = "
        "Tr(D^4) = 50.3712. The decisive question (the gold-standard make-or-break) "
        "is whether eps0^2 = pi/432 equals the dimensionless heat-kernel ratio "
        "a4/a2. It does NOT: the closest natural shape M4/M2^2 = 0.00582895 is 0.80x "
        "pi/432 (a clean 20% miss), and the result is a STRUCTURAL refutation, not a "
        "numerical near-miss -- the moments are EXACT rationals (M2 = 2324/25, "
        "M4 = 31482/625, residual ~1e-14) because Tr(D^2k) is a rational power sum of "
        "the algebraic Dirac spectrum, so a4/a2 = M4/M2^2 = 15741/2700488 is an exact "
        "rational and can NEVER equal the transcendental pi/432 (seed-independent: a "
        "second seed gives another pi-free rational). The ONLY pi a spectral action "
        "emits is the continuum (4 pi)^(-d/2) -- a denominator pi with half-integer "
        "power, (4 pi)^-2 = 0.00633 != pi/432 -- confirming epsilon_heat_kernel; the "
        "bare pi is instead the Berry half-solid-angle (1/2)(2 pi) = pi, a holonomy "
        "flux, so pi/432 = (Berry pi) x (Schur 1/432) is a flux-per-state count, a "
        "GEOMETRIC quantity not a spectral-action output. This gate moves NO Bayes "
        "credit: it REFUTES the heat-kernel earn-path for the +5.6 while leaving the "
        "Berry/Schur geometric reading untouched; F0 stays GEOMETRIC/open.",
        open_bridges=(
            "The spectral-action heat-kernel route to a DERIVED pi/432 is now CLOSED "
            "(refuted); any future promotion of eps0 from GEOMETRIC to DERIVED must "
            "come from a DIFFERENT dynamical mechanism, not the a4/a2 ratio of this "
            "(or any finite, rational-spectrum) triple.",
            "The Berry/Schur GEOMETRIC reading of pi/432 (pi from holonomy, 1/432 "
            "from the Schur flat measure) survives this refutation and remains the "
            "ceiling for pi/432 via this route -- it is neither derived nor demoted "
            "by this gate.",
        ),
        kill_conditions=(
            "The refutation is spun as a positive result -- e.g. a4/a2 is reported as "
            "'close to' or 'confirming' pi/432, or the 0.80x miss is presented as "
            "agreement rather than the clean structural KILL it is.",
            "The Berry/Schur geometric reading is presented as demoted or invalidated "
            "when only the heat-kernel CHANNEL is refuted; the geometric pi/432 maths "
            "is untouched and must not be reported as killed.",
            "F0 or eps0^2 = pi/432 is promoted on the back of this gate, OR the "
            "granted +5.6 is silently dropped to a headline -3.2 as if the geometric "
            "reading had been killed; model_complexity/scoreboard/registry credit is "
            "moved either way.",
        ),
    ),
    "f0_phase1_closeout": contract(
        "f0_phase1_closeout",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only the consolidation this gate computes: that PHASE 1 (the "
        "make-or-break finite-spectral-triple build) is fully executed and that its "
        "TWO independent decisive routes converge on ONE missing object. It imports "
        "the two source-of-truth numbers rather than re-deriving them loosely. "
        "PREFACTOR route (Phase 1.3, from f0_spectral_action_heatkernel on the "
        "genuine 216-dim D): a2 = Tr(D^2) = 92.96, a4 = Tr(D^4) = 50.3712, so the "
        "dimensionless a4/a2 = M4/M2^2 = 0.00582895 is a pi-FREE rational and is "
        "bounded away from the transcendental pi/432 = 0.00727221 (gap 0.00144 > "
        "1e-3) -- pi/432 is NOT a spectral-action output. RATIO route (Phase 1.4, "
        "from spectral_action_432.ladder_mismatch): the octonionic L_X forces the "
        "averaging law but the best single-knob eps0 ladder MISSES the measured "
        "charged-lepton hierarchy by 1.40 decades -- the spectrum forces STRUCTURE, "
        "not the absolute profile. The two routes are independent (a single "
        "transcendental constant vs a set of multiplicative ratios) yet both "
        "localise the entire remaining F0 gap to the SAME missing object: a "
        "dynamical/variational ACTION (gold-standard criterion 1, ABSENT) that "
        "would have to produce pi/432 [refuted] AND select the three seed "
        "eigenvalues [open]. This gate is a CONSOLIDATION, not a new physics "
        "result; it moves NO Bayes credit and touches no frozen artifact. F0 "
        "stays GEOMETRIC/open and Phase 2 is GATED on the missing action.",
        open_bridges=(
            "The lone surviving F0 bottleneck is a DERIVED dynamical/variational "
            "action (criterion 1): a principle whose stationary vacuum both fixes the "
            "pi/432 prefactor AND selects the three diagonal seed eigenvalues. Both "
            "decisive Phase-1 routes converge here; foundations/02_action.md only "
            "candidates it.",
            "Closing this bridge requires that derived action (and the Phase-2 "
            "operator -> masses+CKM+PMNS that would follow), NOT another invariance "
            "witness -- this gate explicitly closes the invariance-witness phase.",
        ),
        kill_conditions=(
            "The closeout is spun as a positive derivation or a Phase-1 'success' -- "
            "e.g. presenting the convergence as evidence FOR pi/432 or the hierarchy "
            "rather than as the bounded fork outcome (the dynamical route is closed, "
            "the geometric reading survives).",
            "The bounded fork is over-claimed as a TOTAL kill of F0 -- the Berry/Schur "
            "geometric pi/432 reading and the derived mass STRUCTURE (averaging law, "
            "(0,2,4) skeleton, GJ {1,3,8}) survive and must not be reported as killed.",
            "Any F0 / pi-432 / scoreboard / registry credit is moved on the back of "
            "this consolidation, in either direction.",
        ),
    ),
    "f0_theta_reality_gate": contract(
        "f0_theta_reality_gate",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only the precise negative this gate computes: that the TOPOLOGICAL "
        "route to pi/432 -- the candidate pi/432 = theta/dim with theta = pi*nu a Z2 "
        "angle quantized by the KO-6 real structure J -- is CLOSED for the genuine "
        "216-dim octonionic Dirac D, because all three natural sources of a theta = pi "
        "vanish. This is a genuinely DIFFERENT channel from Phase 1.3: a theta-term is "
        "NON-perturbative (it never enters the rational Seeley-DeWitt moments), so the "
        "1.3 rational-moment kill does not pre-empt it. The three invariants: (A) the "
        "spectral-asymmetry eta = #(lambda>0)-#(lambda<0) = 0 identically, forced by "
        "gamma-oddness (gamma D = -D gamma => +/- symmetric spectrum 108/108, no zero "
        "modes); (B) the chiral mod-2 index nu = dim ker(D:H+->H-) mod 2 = 0, the block "
        "being full rank (108); (C) the Kramers/Fu-Kane Z2 is undefined because KO-6 has "
        "J^2 = +1 (the real class), not the J^2 = -1 a time-reversal theta = pi needs. "
        "So theta = 0 and pi*nu/432 = 0 != pi/432. This is the THIRD independent "
        "converging-negative (with the 1.3 prefactor and the 1.4 ratios); pi/432 stays "
        "the Berry half-solid-angle holonomy of the CONTINUOUS vacuum sphere -- a "
        "property of the missing action, not a topological invariant of D. F0 stays "
        "GEOMETRIC/open; this moves NO Bayes credit and touches no frozen artifact.",
        open_bridges=(
            "The lone surviving F0 bottleneck is unchanged: a DERIVED dynamical/"
            "variational action whose stationary vacuum fixes pi/432 and selects the "
            "seed eigenvalues. The topological-theta route does NOT supply it -- it is "
            "now a recorded converging-negative, not an open lead.",
            "The surviving reading of pi/432 is the Berry/Schur holonomy of the "
            "continuous vacuum-selection sphere (the dynamics that picks the vacuum "
            "direction), which this gate leaves untouched -- neither derived nor "
            "demoted.",
        ),
        kill_conditions=(
            "The negative is spun as a positive -- e.g. theta reported as pi (rather "
            "than the computed 0), or the gate presented as evidence FOR a topological "
            "origin of pi/432.",
            "The bounded negative is over-claimed as a TOTAL kill of F0 -- the "
            "Berry/Schur geometric reading survives and must not be reported as killed; "
            "equally the scope (THIS finite KO-6 triple via its three natural sources) "
            "must not be inflated to 'no topological invariant can ever be pi'.",
            "Any F0 / pi-432 / scoreboard / registry credit is moved on the back of "
            "this gate, in either direction.",
        ),
    ),
    "gold_standard_closeout": contract(
        "gold_standard_closeout",
        ("F0",),
        STATUS_OPEN_BRIDGE,
        VERDICT_OPEN,
        "Claim only the consolidation this capstone computes: that the WHOLE "
        "seven-point gold-standard scorecard now reduces to one executable, "
        "self-checking statement, and that the honest-null STANDING POSITION (ship "
        "the standalone math PAPER_JORDAN_THEOREMS.md + the honest null) is asserted "
        "against its source-of-truth modules so it cannot silently drift. The single "
        "headline number is the scoreboard ln B ladder: historical -21.3 -> "
        "closed-theorem floor -3.2 (today's EARNED position) -> +5.6 if the geometric "
        "pi/432 is GRANTED -> +36.2 if the program completes; the SIGN FLIPS only at "
        "the pi/432 grant, so on EARNED credit the numerology null still wins (floor < "
        "0). The internal program TERMINATES in the precise sense that criteria 1 "
        "(dynamical principle, ABSENT), 3 (one unifying object, OPEN) and the open half "
        "of 2 all localise to the SAME missing derived dynamical action, while the "
        "remaining gaps are external: criterion 4 (pre-registered hit) awaits DUNE / "
        "Hyper-K, criterion 6 (single UV scale) is falsified, criterion 7 (independent "
        "reproduction) needs peer review. This capstone is NOT a new physics result "
        "and NOT another invariance witness; it is a REPORTER, not a source -- it "
        "grants no Bayes credit of its own, and its checks forbid only SILENT drift, "
        "never a DELIBERATE re-verified revision when the science earns one (nothing "
        "here is published, so nothing here is permanent).",
        open_bridges=(
            "The lone open INTERNAL lever is unchanged: a DERIVED dynamical/variational "
            "action whose stationary vacuum fixes pi/432 and selects the seed "
            "eigenvalues. Every internal criterion (1, 3, the open half of 2) waits on "
            "exactly this one object.",
            "The open EXTERNAL levers are not closable by more internal work: an "
            "experiment (criterion 4, sin^2 th23 = 4/7 at DUNE / Hyper-K) and peer "
            "acceptance (criterion 7).",
        ),
        kill_conditions=(
            "The honest null is spun as a positive -- e.g. the EARNED floor (ln B = "
            "-3.2 < 0) is reported as program success, or the GRANTED +5.6 is presented "
            "as earned rather than granted.",
            "A scorecard criterion is flipped (ABSENT/OPEN/PENDING -> met) without the "
            "underlying artifact being promoted first, or the capstone is read as "
            "CLOSING criteria 4 or 7, which only an experiment / external review can do.",
            "Any F0 / pi-432 / scoreboard / registry credit is moved on the back of "
            "this consolidation itself, in either direction (credit is earned in the "
            "physics artifacts it reads, never granted by this reporter).",
        ),
    ),
    "f0_direction_gate": contract(
        "f0_direction_gate",
        ("F0", "STAT1"),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Use as project-direction governance only: continue F0 work only when a "
        "next task retires a named live F0 bridge; otherwise pivot to falsification "
        "or submission packaging.",
        open_bridges=("Physical transition ray tau from action dynamics.",
                      "Admissible epsilon-kernel class from full CHO action dynamics."),
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
    "jordan_standalone_theorems": contract(
        "jordan_standalone_theorems",
        ("G1", "F0", "A3"),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Publish the three results as decoupled mathematics about J3(O); do not "
        "attach the physical (generation/measure/mass) interpretation, which is "
        "developed and gated separately and is not established by these theorems.",
        open_bridges=(
            "The physical generation map (G1), the pi/432 measure (F0), and the "
            "Yukawa spectrum (A3) stay open bridges; the decoupled math does not close them.",
        ),
        kill_conditions=(
            "Presenting the decoupled theorems as evidence that the physical interpretation is derived.",
            "Claiming novelty for the classical inputs (Albert algebra, F4 connectedness, Schur, Freudenthal cubic) instead of the assembly.",
            "Promoting F0/G1/A3 or moving Bayes credit on the basis of this consolidation.",
        ),
    ),
    "padic_hierarchy": contract(
        "padic_hierarchy",
        ("S1", "N1", "CC1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "BIG-BETS Bet 1. State only the EXACT arithmetic (9,36,64 are perfect squares; "
        "increments +27=dim J3(O), +28=dim so(8); 3-adic unit-scale / archimedean "
        "reframing) and the CONCEPTUAL gain (the hierarchy 'problem' is archimedean, "
        "so a real-analytic spectral action over R could never emit these scales). Do "
        "NOT present the arena-dimension labels as forcing the exponents: like the "
        "repo's own labels they are post-hoc, the exponents stay CHOSEN in "
        "model_complexity.py, and the look-elsewhere-corrected p (~0.018) is above the "
        "promotion bar. Report the CC base-3 contamination (dist ~0.42) honestly, not "
        "only the clean EW hit.",
        assumptions=(
            "The three stated exponents M_W=M_P/3^36, M_R=M_P/3^9, Lambda^1/4 ~ M_P/3^64 "
            "are taken as source-of-truth integers from summary_table / dark_sector / "
            "cc_prediction; only two (EW, CC) are data-anchored, the seesaw 9 is theory-internal.",
            "The CHO_DIMS catalogue used for the increment test is declared BEFORE testing "
            "so the look-elsewhere size is explicit; widening it weakens the increment hit.",
        ),
        open_bridges=(
            "No DERIVATION forces the exponents from the arena dimensions {9,+27,+28}; the "
            "identifications are post-hoc, so the exponents are not promotable from CHOSEN.",
            "The adelic/3-adic reframing is conceptual; it does not yet supply a DYNAMICS or "
            "measure that outputs the scales (the same missing object F0/Phase-1 localised).",
            "CC and the seesaw scale are not base-3-clean without O(1) prefactors; only the "
            "electroweak hierarchy is.",
        ),
        kill_conditions=(
            "Presenting the {9,+27,+28} ladder as a derivation, or moving any Bayes credit / "
            "changing a model_complexity status on the back of this EXPLORATORY module.",
            "Quoting the clean electroweak base-3 hit while suppressing the CC contamination "
            "or the look-elsewhere correction.",
            "If the look-elsewhere-corrected p ever crosses the 0.001 promotion bar, treating "
            "that as automatic promotion instead of re-deriving, widening the pattern menu, and "
            "moving credit deliberately on the scoreboard.",
        ),
    ),
    "causal_set_lambda": contract(
        "causal_set_lambda",
        ("CC1", "S1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "BIG-BETS Bet 2. State only the EXACT arithmetic (Sorkin V=Lambda^-2 round-trips; "
        "CHO's Lambda/M_P^4 is NOT exactly 3^-256 but 3^-257.6 once the (11/12)/sqrt2 "
        "prefactor is kept; the observed cosmic 4-volume is ~10^244 in every standard "
        "convention; Lambda^1/4 ~ V^(-1/8) recovers the CHOSEN exponent 64 to within ~0.5) "
        "and the CONCEPTUAL gain (the causal-set counting law supplies a candidate DYNAMICAL "
        "origin for the CC magnitude that the static algebra lacked). Do NOT present this as "
        "a derivation of 64: it uses the OBSERVED 4-volume as input (trading 'why 64' for the "
        "cosmic-coincidence 'why now'), the 1/8 power is fourth-root x Sorkin-sqrt and the "
        "match to dim(O)=8 is a coincidence not leaned on, and base 3 is unforced here (base 8 "
        "fits the volume better). The real payoff is the falsifier, not the number: CHO (Lambda "
        "constant, w=-1) vs Sorkin everpresent-Lambda (dynamical, w(t)!=-1).",
        assumptions=(
            "CHO's Lambda^1/4 = (11/12) M_P/(sqrt2 3^64) and the observed Lambda are taken as "
            "source-of-truth from cc_prediction.py; M_P is the full Planck mass.",
            "Sorkin's law Lambda ~ +/- 1/sqrt(V) is adopted as the causal-set heuristic (an "
            "order-of-magnitude, fluctuating-sign statement), not a rigorous identity.",
            "The observed cosmic 4-volume ~10^244 Planck-4-volumes is computed from the Hubble "
            "radius, the age, and the particle horizon; conventions differ at the ~10^+/-1 level.",
            "Base 3 is imported from Bet 1 (triality) as an EXTERNAL warrant; this module shows "
            "it is not forced by the volume match itself.",
        ),
        open_bridges=(
            "No DERIVATION forces the exponent 64: the bridge consumes the observed 4-volume as "
            "input, so it relocates the mystery to the cosmic-coincidence problem rather than "
            "abolishing it; the exponent stays CHOSEN in model_complexity.py.",
            "Putting CHO/Jordan internal state on causal-set elements and asking whether the "
            "growth dynamics SEES the internal index (forcing N=3 and supplying the action) is "
            "not done here; without it the counting law is borrowed, not derived from CHO.",
            "Lambda is not base-3-clean (log_3 = -257.6, the same prefactor contamination Bet 1 "
            "found), so the clean 'V=3^512' reading holds only up to an O(1) factor.",
        ),
        kill_conditions=(
            "Presenting 64 = (1/8) log_3(V) as a derivation, leaning on the 1/8 = 1/dim(O) "
            "coincidence, or moving any Bayes credit / changing a model_complexity status on the "
            "back of this EXPLORATORY module.",
            "Quoting the convention that lands nearest 64 while suppressing the spread (~0.5) or "
            "the fact that base 8 fits the cosmic volume better than base 3.",
            "If dark energy is confirmed an exact constant (w=-1 to high precision), continuing "
            "to present the causal-set everpresent-Lambda reading as live instead of recording "
            "that the dynamical mechanism is killed and only the static 'why-now' coincidence "
            "survives.",
        ),
    ),
    "entropic_gravity_cho": contract(
        "entropic_gravity_cho",
        ("GR1", "CC1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "BIG-BETS Bet 2 (gravity companion to causal_set_lambda). State only the EXACT "
        "bookkeeping (Jacobson: S=A/(4G)=A/4 + dQ=TdS => Einstein equations; tiling a horizon "
        "with cells of CHO internal dimension d gives the area law S=(A/a_cell)ln d ~ A; "
        "matching S=A/4 forces a_cell=4 ln d, reproducing the textbook it-from-bit 4 ln 2=2.77 "
        "at d=2; the identity N_cells*log2(d)=N_bits holds exactly) and the HONEST conclusion "
        "(counting supplies the area-extensive entropy Jacobson needs but does NOT fix the "
        "coefficient 1/4 = Newton's G: it is relocated to a_cell, and the CHO dimension is pure "
        "bit-bookkeeping for it). Do NOT present this as a derivation of G or of black-hole "
        "entropy. The payoff is the cross-module tension, not a number: the SAME Planck-density "
        "causal set that reproduces Lambda would overcount horizon entropy by 4 ln d (~13x for "
        "d=27) unless the CHO internal state is horizon-unresolved.",
        assumptions=(
            "Jacobson's thermodynamic derivation (Clausius dQ=TdS on local Rindler horizons with "
            "Unruh T and Bekenstein-Hawking S=A/4) is adopted as the route from horizon entropy "
            "to the Einstein equation of state; the coefficient 1/4 is its sole non-thermodynamic "
            "input.",
            "The counting ansatz tiles a horizon with independent cells each carrying a CHO "
            "internal Hilbert space of dimension d in {2,3,4,7,8,16,26,27,28,52,78}; the entropy "
            "is the log of the product multiplicity (no correlations / area law assumed local).",
            "The cross-module tension uses causal_set_lambda's Planck sprinkling density (one atom "
            "per Planck 4-volume) and the Dou-Sorkin result that horizon molecule counts scale "
            "with area; the O(1) molecule-counting constant is taken as ~1.",
        ),
        open_bridges=(
            "Newton's G (the coefficient 1/4) is NOT derived: it is relocated into the horizon "
            "cell area a_cell=4 ln d, which CHO does not independently fix, and the bit-bookkeeping "
            "identity shows the internal dimension carries no information about it.",
            "Whether the CHO internal state is a genuine horizon degree of freedom or is "
            "horizon-unresolved (gauge/projected) is not settled here; the cross-module "
            "consistency with the Lambda module REQUIRES the latter but does not prove it.",
            "No dynamics is derived FROM CHO: the area law is a generic consequence of local "
            "counting (locality + extensivity), so the 'win' is the structural prerequisite "
            "Jacobson needs, not a CHO-specific result.",
        ),
        kill_conditions=(
            "Presenting a_cell=4 ln d as a derivation of Newton's G or of the Bekenstein-Hawking "
            "1/4, leaning on any near-integer coincidence in the 4 ln d table, or moving Bayes "
            "credit / changing a model_complexity status on the back of this EXPLORATORY module.",
            "Quoting the area-law 'win' while suppressing that the coefficient is untouched (the "
            "bit-bookkeeping identity) or that Planck-density tiling overcounts by 4 ln d (the "
            "species problem).",
            "If the CHO internal state is shown to be a genuine horizon degree of freedom at "
            "Planck density, continuing to present the Lambda-fixing causal set as consistent "
            "instead of recording that it is then refuted (S is 4 ln d times too large).",
        ),
    ),
    "everpresent_lambda_tracking": contract(
        "everpresent_lambda_tracking",
        ("CC1", "S1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "BIG-BETS Bet 2a deepening. State only the EXACT, computed facts (the present-epoch "
        "anchors land: Hubble 4-volume today ~10^244, Lambda_everpresent today = H0^2 ~10^-122; "
        "the everpresent fraction Omega_Lambda(z) is epoch-independent by the Sorkin scaling "
        "Lambda~H^2 while the static fraction dilutes as Omega_L,0/E(z)^2; the two readings of "
        "the SAME exponent diverge as Om_ever/Om_static = E(z)^2, reaching ~6e8 at recombination) "
        "and the HONEST conclusion (the everpresent reading partly repays the why-now debit and "
        "yields a computed, live falsifier, but the entire time-structure is CAUSAL-SET content "
        "and CHO is a spectator in the dynamics). Do NOT present this as CHO predicting "
        "dark-energy evolution: the divergence SHAPE is invariant under the CHO exponent (it "
        "sets only today's normalization), and a confirmed evolving-DE signal supports Sorkin "
        "over the CHO-static w=-1, not CHO.",
        assumptions=(
            "The flat background (Omega_m=0.3153, Omega_L=0.6847, Omega_r~9.2e-5, consistent with "
            "cc_prediction) and H0, T_P are source-of-truth; the static reading is an exact "
            "cosmological constant (w=-1) and the everpresent reading uses Lambda(t) ~ 1/sqrt(V(t)) "
            "with the Hubble 4-volume V ~ H^-4.",
            "The everpresent magnitude and the static-vs-tracking contrast are HEURISTIC "
            "order-of-magnitude statements on a fixed LambdaCDM background, deliberately NOT a "
            "self-consistent stochastic solve of the modified Friedmann equation.",
            "Today's Lambda normalization is taken from causal_set_lambda / cc_prediction (the CHO "
            "exponent 64); it enters only the normalization, never the redshift shape.",
        ),
        open_bridges=(
            "The dynamical content (tracking, divergence, effective w!=-1) is causal-set, not CHO: "
            "the divergence shape is independent of the CHO exponent, so this module does NOT make "
            "CHO predict dark-energy evolution; it only makes the two readings distinguishable.",
            "A strictly smooth Lambda~H^2 is degenerate with a rescaled Newton constant (it does "
            "not accelerate); the genuine dark-energy content lives in the SIGN fluctuations of "
            "Lambda (Ahmed-Dodelson-Greene-Sorkin 2004; Zwane-Afshordi-Sorkin 2018), not simulated "
            "here, so no w0-wa fit is claimed.",
            "Whether CHO can supply the missing dynamical ingredient (e.g. an internal-state growth "
            "rule that fixes the fluctuation measure) is the open Bet-2 question this does not "
            "close; without it the everpresent dynamics stays borrowed.",
        ),
        kill_conditions=(
            "Presenting the everpresent tracking or the E(z)^2 divergence as a CHO prediction, or "
            "quoting the recovered ~10^-122 / ~10^244 anchors as a derivation of dark-energy "
            "evolution, or moving any Bayes credit on the back of this EXPLORATORY module.",
            "Quoting the why-now 'repayment' or the falsifier while suppressing that the dynamics "
            "is causal-set (CHO-spectator) or that the smooth limit is degenerate with rescaled G.",
            "If dark energy is confirmed an exact constant (w=-1 to high precision), continuing to "
            "present the everpresent reading as live; if evolving DE is confirmed, presenting it as "
            "a CHO success rather than a result that disfavours the CHO-static w=-1.",
        ),
    ),
    "causal_growth_index": contract(
        "causal_growth_index",
        ("G1",),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "BIG-BETS Bet 2 crux. State only the EXACT, computed facts (index-blind sequential "
        "growth is covariant — a genuine measure on histories; discrete general covariance is "
        "equivalent to a SYMMETRIC index coupling, demonstrated by the V poset splitting "
        "0.042 vs 0.126 under an asymmetric coupling and collapsing under a symmetric one; "
        "covariance leaves an N(N+1)/2 coupling family that is never empty, so a covariant "
        "non-spectator coupling exists for N in {2,3,4,5,6}; the index-blind causet marginal is "
        "exactly N-independent; Z/N inheritance is covariant for every N) and the HONEST "
        "conclusion (the growth dynamics is BLIND to the internal index's cardinality — it can "
        "carry a CHO index as a covariant passenger but cannot SELECT N=3). Do NOT present this "
        "as growth deriving the generation count: N=3 is NOT singled out by either CSG axiom; it "
        "remains a kinematic input (G1, from jordan_eigenvalue_generations / three_generations_frame).",
        assumptions=(
            "The dynamics is Rideout-Sorkin classical sequential growth in the transitive-"
            "percolation case, realised as i.i.d. pre-closure pair inclusions + transitive "
            "closure, so internal temporality, discrete general covariance, and Bell causality "
            "are all explicit and checkable on small (n=3) causets.",
            "Discrete general covariance is used in its computable form: all linear extensions "
            "(birth orders) of a fixed decorated poset must have equal sequential-growth "
            "probability.",
            "The internal index couples to the growth only through a pairwise inclusion "
            "probability p(s_i,s_j); inheritance is tested separately as a commutative associative "
            "product (Z/N) on the index.",
        ),
        open_bridges=(
            "The growth dynamics is blind to the index CARDINALITY: covariance constrains the "
            "coupling (symmetric) and Bell causality is automatic, but neither places any "
            "constraint on N, so this module does NOT derive N=3 — it remains a kinematic input "
            "(G1).",
            "A richer coupling (index-dependent t_n couplings beyond percolation, or a measure on "
            "internal states that feeds back into the growth) is not explored here; the negative "
            "is established for the percolation family + commutative inheritance, not for every "
            "conceivable index-growth coupling.",
            "The exceptional rank-3 selection lives in the kinematic Hurwitz/Jordan classification "
            "(non-associative octonionic composition), which this order-theoretic dynamics does "
            "not supply; whether any growth rule can internalise that classification is open.",
        ),
        kill_conditions=(
            "Presenting the covariant measure on histories as deriving N=3, or the symmetric-"
            "coupling result as growth 'selecting' the generation count, or moving any Bayes "
            "credit on the back of this EXPLORATORY module.",
            "Quoting the criterion-A win (counting gives a measure) while suppressing the "
            "N-blindness (that the same axioms admit a covariant non-spectator coupling for every "
            "tested N, so 3 is not singled out).",
            "Claiming the Z/N inheritance or any commutative closure forces 3, or presenting the "
            "octonionic/non-associative input as a dynamical output rather than a kinematic "
            "classification fact.",
        ),
    ),
    "statistical_flavour_ensemble": contract(
        "statistical_flavour_ensemble",
        ("C1",),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "BIG-BETS Bet 3. State only the EXACT, computed facts (a symmetry-blind anarchy "
        "ensemble produces LARGE mixing and reproduces the observed quark CKM moduli with "
        "probability ~ 0, so it is decisively falsified for quarks, yet the SAME anarchy reaches "
        "a PMNS-sized sin^2 theta13 a few percent of the time, so it stays viable for leptons — "
        "the observed quark/lepton dichotomy; the Gatto-Sartori-Tonin correlation "
        "corr(|V_us|, sqrt(m_d/m_s)) is ~ 0 for anarchy but ~ +0.48 for the Froggatt-Nielsen "
        "hierarchy ALONE, and CHO's derived triality texture zero lifts it only ~ +0.07 more) "
        "and the HONEST conclusion (going to distributions is a real methodological win — it "
        "kills symmetry-blind anarchy for quarks — but what beats anarchy is the mass HIERARCHY, "
        "an input the ledger already charges, not the CHO texture). Do NOT present this as CHO "
        "predicting the flavour distribution: the single-value bridges C1..C4 are untouched, and "
        "the texture zero is a sub-dominant refinement on top of the hierarchy, not the "
        "discriminator.",
        assumptions=(
            "Yukawas are 3x3 complex matrices; the up and down sectors are independent draws and "
            "the CKM matrix is U_u^dag U_d read from the left singular vectors, with the singular "
            "values identified as the masses (the standard random-texture setup).",
            "The hierarchy is modelled by a Froggatt-Nielsen scaling M_ij ~ eps0^(q_i+q_j) with "
            "charges (2,1,0) and eps0^2 = pi/432 (the CHO triality-breaking parameter, ledger F0); "
            "the CHO texture is the NNI zero set, of which triality derives only the (1,3),(3,1) "
            "entry (gen1<->gen3 needs two tau steps).",
            "The ensembles are Monte-Carlo at a FIXED seed and finite sample, so the medians, "
            "tail fractions, and correlations are estimates with sampling noise; the asserted "
            "thresholds carry margin around the seed-stable values.",
        ),
        open_bridges=(
            "The discriminating power is carried by the mass hierarchy (the eps-ladder, an F0 "
            "input the scoreboard already charges), not by the CHO texture: a symmetry-blind "
            "ensemble with the same hierarchy already reproduces the small angles and most of the "
            "GST correlation, so this module does NOT credit CHO — the single-value C1..C4 "
            "bridges stand exactly as charged.",
            "The NNI texture is emitted by every Froggatt-Nielsen model, so even the small "
            "texture-zero increment is not unique to CHO; whether the octonionic structure "
            "selects FN charges or the texture zeros dynamically is not addressed here.",
            "Only the percolation-like Gaussian ensemble with a fixed FN charge assignment is "
            "swept; a genuine large-N free-probability limit (where RMT universality is sharp) is "
            "not reachable at 3 generations, so the universality argument is heuristic.",
        ),
        kill_conditions=(
            "Presenting the anarchy falsification or the GST correlation as a CHO derivation of "
            "the flavour distribution, or moving any Bayes credit on the back of this EXPLORATORY "
            "module.",
            "Quoting the real positive (distributions kill symmetry-blind anarchy) while "
            "suppressing that the hierarchy — not the CHO texture — is what does it (the hierarchy "
            "increment to the correlation strictly exceeds the texture increment).",
            "Claiming the triality texture zero or the NNI form is a unique CHO prediction, or "
            "promoting any single-value CKM/PMNS bridge to 'derived' on the strength of the "
            "ensemble statistics.",
        ),
    ),
    "positive_geometry_cluster": contract(
        "positive_geometry_cluster",
        ("F0", "G1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "BIG-BETS Bet 4. State only the EXACT, computed facts (all exact integer arithmetic from "
        "the Dynkin degree tables: the exceptional types CHO privileges carry its arena integers "
        "as cluster / root invariants — D4 = triality has 16 cluster variables and dimension 28 = "
        "dim so(8), E6 = J3(O) has 36 positive roots and a 27-dimensional minuscule rep, the "
        "hierarchy increments {27,28} are the E6 minuscule and D4 adjoint dimensions, and E6 is "
        "the unique exceptional with a Z/3 centre; while the cluster count = the cell number of "
        "the positive geometry is NEVER a CHO integer and never 3, the 27 match is non-unique "
        "(also the A6 cluster-variable count), four exceptional types each carry a CHO integer, "
        "and 432=16*27 / 64 are near-misses to the A6 cell count 429 / the E7 root count 63) and "
        "the HONEST conclusion (positive geometry HOSTS the CHO exceptional arena — a real "
        "criterion-B consistency — but the canonical-form / cluster machinery FORCES nothing new: "
        "it does not select the arena, does not force base-3, and the octonionic positive "
        "geometry is not constructed). Do NOT present the hosting as deriving any CHO constant: "
        "the integers 16, 27, 28, 36 are root-system data CHO already ingests, the hosting is a "
        "consistency not a derivation, and no constant moves from CHOSEN to derived.",
        assumptions=(
            "The positive geometry is probed through its computable combinatorial skeleton, the "
            "finite-type cluster algebra (Fomin-Zelevinsky classification by Dynkin diagrams); "
            "the full canonical form / amplituhedron is not evaluated, only its cluster / "
            "generalized-associahedron invariants.",
            "Every integer is computed exactly from the Dynkin fundamental-invariant degrees "
            "(rank, Coxeter number, positive roots = sum(deg)-rank, cluster variables = sum(deg), "
            "clusters = prod (h+d_i)/d_i, Weyl order = prod(deg)); the minuscule 27 is the coset "
            "count |W(E6)|/|W(D5)|.",
            "The CHO arena integers (8, 16, 27, 28, 36, 64) and the generation count 3 are "
            "kinematic inputs under test, NOT outputs of this combinatorics; the amplitude bridge "
            "(Gr(3,6)~D4, Gr(3,7)/Gr(4,7)~E6) is cited from the cluster-algebra literature.",
        ),
        open_bridges=(
            "Hosting is not forcing: positive geometry carries the CHO integers because they are "
            "root-system data, but the cell count never equals a CHO integer or the 3, and more "
            "than one exceptional type hosts a CHO integer, so the machinery does NOT select the "
            "CHO arena or derive any constant (F0 hierarchy exponents and G1 generation count "
            "stay as charged).",
            "The Z/3 centre that distinguishes E6 (hence base-3) lives in E6 representation "
            "theory — a CHO input — not in the canonical-form dynamics, and it is not the "
            "triality/generation Z/3 that permutes the three J3(O) blocks; the rep-theoretic "
            "distinction is real but does not by itself force the physics.",
            "The actual octonionic positive geometry (a canonical form whose cells are the three "
            "generations) is not constructed: octonion non-associativity obstructs the standard "
            "commutative, totally-positive cluster-coordinate construction, so whether such a "
            "geometry exists is the open Bet-4 frontier this probe does not settle.",
        ),
        kill_conditions=(
            "Presenting the hosting (D4->16, E6->36/27, Z(E6)=Z/3) as deriving the CHO constants "
            "or the generation count, or moving any Bayes credit on the back of this EXPLORATORY "
            "module.",
            "Quoting the criterion-B win while suppressing that the cell count is blind to the 3, "
            "that the matches are non-unique and multi-hosted, or that 432/64 are near-miss traps "
            "(429/63), not exact cluster invariants.",
            "Claiming an octonionic positive geometry / amplituhedron has been built, or that the "
            "exceptional cluster algebras force base-3, without an explicit non-associative "
            "canonical-form construction.",
        ),
    ),
    "adelic_constant_relation": contract(
        "adelic_constant_relation",
        ("F0", "N1", "S1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "BIG-BETS Bet 1, second probe (the Moonshine follow-on). State only the EXACT "
        "factorisations (432 = 2^4*3^3 = 16*27; sin^2 theta23 = 4/7 and cos^2 = 3/7 are the "
        "Fano line split 7 = 4+3; the exponents 9,36,64 and arena dims 16,27,28,14 are all "
        "S-units over the three octonion primes {2,3,7}; |Aut(Fano)| = |PSL(2,7)| = 168 = "
        "2^3*3*7 has prime support exactly {2,3,7}) and the CONCEPTUAL gain (the predictive "
        "constants are arithmetic objects on the octonion-distinguished primes, extending "
        "padic_hierarchy from the exponents to the whole multiplicative set — why a "
        "real-analytic spectral action over R could never emit them). Do NOT present the "
        "{2,3,7} reading as deriving any constant: smoothness is generic for small integers, "
        "it BREAKS on CHO's own structure-group dimensions (dim F4 = 52 = 2^2*13, dim E6 = 78 "
        "= 2*3*13, dim E7 and dim E8 carry primes 13,19,31), 432 is NOT a Moonshine "
        "coefficient, and no non-trivial single arithmetic relation links the set. The "
        "constants stay CHOSEN; no Bayes credit moves.",
        assumptions=(
            "The predictive constants 432 (= the pi/432 denominator), sin^2 theta23 = 4/7, the "
            "power-of-three exponents 9,36,64 and the arena dimensions 16,27,28,14 are taken as "
            "source-of-truth from chi_squared / summary_table / dark_sector / cc_prediction; the "
            "pi in pi/432 is stripped and only the arithmetic content is tested.",
            "The three octonion-distinguished primes {2,3,7} (2 = Cayley-Dickson doubling, 3 = "
            "triality / Jordan rank 3 / generations, 7 = Im(O) / the 7 Fano points and lines) are "
            "declared BEFORE the smoothness test so the look-elsewhere size is fixed; the "
            "structure-group dimensions are the pre-declared control set.",
            "S-unit / smoothness is exact-integer arithmetic (trial-division factorisation); the "
            "Moonshine reference data (j-function and Monster irrep dimensions) is a fixed, "
            "pre-declared list, not fitted.",
        ),
        open_bridges=(
            "Hosting is not forcing: {2,3,7}-smoothness is generic for small integers and "
            "reflects the octonionic INPUT dimensions, so it does not derive any exponent, the "
            "mixing 4/7, or the generation count — the constants stay CHOSEN (F0, N1, S1 as "
            "charged).",
            "The pattern is not a theory-wide law: it BREAKS on the dimensions of CHO's own "
            "structure groups (dim F4 = 52 and dim E6 = 78 are divisible by 13, dim E7 = 133 by "
            "19, dim E8 = 248 by 31), so {2,3,7}-arithmetic is a property only of the subset that "
            "enters numerical predictions, not of the algebra.",
            "No single arithmetic object generates the set: 432 is not a j-function or Monster "
            "coefficient (the McKay 196884 = 196883 + 1 has no 432 analogue), and the only S-unit "
            "equations among the constants are trivial (7 = 4+3 and the additive increment ladder "
            "already recorded in padic_hierarchy).",
        ),
        kill_conditions=(
            "Presenting the {2,3,7} S-unit reading (432 = 16*27, the Fano split 4/7) as deriving "
            "any CHO constant or the generation count, or moving any Bayes credit on the back of "
            "this EXPLORATORY module.",
            "Quoting the (+) octonion-prime coherence while suppressing that smoothness is generic "
            "for small integers and BREAKS on CHO's own F4/E6/E7/E8 dimensions (primes 13,19,31), "
            "i.e. is a property of the predictive subset, not the theory.",
            "Claiming a single modular form / Moonshine relation behind the constant set, or that "
            "432 is a j-function or Monster coefficient, without an explicit exact arithmetic "
            "identity (the trivial 7 = 4+3 and the additive ladder do not count).",
        ),
    ),
    "big_bets_closeout": contract(
        "big_bets_closeout",
        ("F0", "G1", "CC1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "BIG-BETS branch CAPSTONE (a REPORTER, the analogue of gold_standard_closeout). "
        "Claim only the CONSOLIDATION this module computes: that the four ranked bets / eight "
        "EXPLORATORY modules reduce to SIX FORM-not-CONTENT faces, that every bet supplied the "
        "FORM (a dynamical/structural principle of the right shape — a counting measure, an "
        "automatic area law, a covariant Bell-causal growth law, a sharp distributional "
        "falsifier, an exact positive-geometry host, an adelic reframing) but none forced the "
        "CONTENT (the exponent 64, the 1/4, the 3, a CHO texture, arena selection, the specific "
        "values), and that this convergence CONFIRMS the internal gold_standard_closeout from "
        "six outside directions — the lone missing object is a single derived dynamical action "
        "that selects the seed/value. State the honest null: all eight probes stay "
        "STATUS_EXPLORATORY/VERDICT_OPEN, the earned scoreboard floor is unchanged at ln B = "
        "-3.2 < 0, and the whole arc moved NO Bayes credit. The one (+) keeper is a DIAGNOSIS, "
        "not a derivation: the constants are arithmetic objects on the octonion primes {2,3,7} "
        "(432 = 16*27) that a real-analytic spectral action over R could never emit — why Phase "
        "1 failed; it reframes the gap, it does not close it. Do NOT present any face's FORM win "
        "as deriving a CHO constant or moving credit; this module is a REPORTER, not a source.",
        assumptions=(
            "The eight big-bets modules and their verdicts are taken as source-of-truth from "
            "audit_contract.CONTRACTS; this capstone re-derives no physics — it only reads the "
            "contracts and the scoreboard and asserts they have not drifted.",
            "The six-faces partition is an editorial grouping of the eight modules; it is asserted "
            "to cover exactly those eight (no probe unaccounted, none double-counted), but the "
            "grouping itself carries no new claim beyond the per-module contracts.",
            "The EARNED floor ln B = -3.2 is read to 0.25 nat from scoreboard.scoreboard(F=3.0) "
            "as a drift tripwire, not a frozen constant — a deliberately re-verified change is "
            "allowed; only SILENT drift is forbidden.",
        ),
        open_bridges=(
            "The six-direction convergence is NEGATIVE evidence, not a derivation: it LOCALISES "
            "the missing object (one derived dynamical action that selects the seed/value) but "
            "does not supply it — the same open INTERNAL lever gold_standard_closeout names.",
            "The one (+) keeper (the constants are adelic objects a real-analytic action cannot "
            "emit) DIAGNOSES the failure mode but forces no constant; F0, G1, CC1 stay exactly "
            "as charged.",
            "Closing the gap needs the levers no synthesis can move — a derived action (internal) "
            "and an experiment / peer review (external); further probes would only re-read the "
            "same six faces.",
        ),
        kill_conditions=(
            "Presenting the consolidation, any face's FORM win, or the six-direction convergence "
            "as deriving a CHO constant, forcing N = 3, or moving any Bayes credit — this "
            "reporter grants none.",
            "Spinning the honest null as a positive: reporting the earned floor (ln B = -3.2 < 0) "
            "as success, or the adelic keeper as a derivation rather than a diagnosis of WHY "
            "Phase 1 failed.",
            "Letting a big-bets probe be promoted off EXPLORATORY/OPEN, or the scoreboard floor "
            "move, SILENTLY — any such change must be deliberate, re-verified, and reflected "
            "here, never absorbed without notice.",
        ),
    ),
    "berry_sigma_model_op2": contract(
        "berry_sigma_model_op2",
        ("F0", "S1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "DECISIVE topological-route test for pi/432, run as a Berry/Wess-Zumino sigma-model on "
        "the triality-vacuum manifold OP^2 (the rank-one idempotent variety of J3(O), dim 16 = "
        "the E6 minimal orbit) with the E6-invariant cubic norm N3 as potential, S = (Berry/WZ "
        "kinetic) - (N3 potential). Claim ONLY what the computation shows. [FORM] the Berry/WZ "
        "kinetic term's holonomy on the minimal great-circle (geodesic) loop of genuine rank-one "
        "J3(O) idempotents is pi (= 1/2 * 2pi solid angle, cross-checked against the "
        "source-of-truth great-circle phase; a non-geodesic loop gives pi/2, so pi is "
        "geodesic-selected), so the topological kinetic term DOES emit pi where the analytic "
        "spectral action provably cannot (Phase 1.3: a4/a2 = 0.00582895 is a pi-free rational). "
        "[CONTENT] the N3 potential — and EVERY F4-invariant, since F4 preserves the J3(O) "
        "spectrum — is CONSTANT on OP^2 (N3 = X# = 0, spectrum (1,0,0) there), so it cannot lift "
        "the vacuum degeneracy to select three distinct eigenvalue-seeds; the measured "
        "charged-lepton hierarchy is a non-symmetric triple that is NOT an N3 critical point (the "
        "global maximum 1/27 is the all-EQUAL anti-hierarchy), and the single-knob eps0 ladder "
        "misses by ~1.40 decades. NET: the sigma-model SEPARATES pi/432 — FORM (pi) is reachable "
        "by the topological route (kinetic term settled), CONTENT (the seeds) is NOT reachable "
        "from any invariant potential and REQUIRES an F4-BREAKING term (a NEW symmetry no-go). "
        "The scoreboard sign does NOT flip (CONTENT failed): pi/432 is NOT promoted, no Bayes "
        "credit moves, F0 stays GEOMETRIC/open. This CONFIRMS Phase 1.4 (structure forced, seed "
        "open) from an independent dynamical direction. Do NOT present the FORM pass as deriving "
        "a constant.",
        assumptions=(
            "The OP^2 vacuum manifold, the cubic norm N3 and its gradient X#, the J3(O) spectrum, "
            "the great-circle Berry phase, and the single-knob ladder miss are taken as "
            "source-of-truth from epsilon_orbit_selection / epsilon_action_selection / "
            "spectral_action_432; this module assembles them into the sigma-model and tests the "
            "two halves, re-deriving none of them.",
            "The candidate action S = (Berry/WZ kinetic) - (N3 potential) with target OP^2 and "
            "potential the E6-invariant N3 is the specific topological model the Phase-1.3 + "
            "adelic triangulation points at; it is asserted as a NAMED candidate, not proven to "
            "be the unique CHO action.",
            "The holonomy is computed on a CP^1 ⊂ OP^2 built from a complex (associative) 2-plane "
            "of O^3; the great circle is the minimal/geodesic loop and pi = 1/2 * (2pi solid "
            "angle) is read as its geodesic-selected Berry phase (a non-geodesic loop gives a "
            "different value, shown explicitly).",
        ),
        open_bridges=(
            "The FORM result settles only the KINETIC term: the Berry/WZ holonomy emits pi, but "
            "deriving that the FULL CHO dynamics realises THIS sigma-model (this target, this "
            "kinetic normalisation) rather than positing it remains open — the same architecture "
            "seam epsilon_action_selection / epsilon_orbit_selection carry.",
            "The CONTENT no-go (no F4-invariant potential selects the seeds) LOCALISES the missing "
            "object to a single F4-breaking seed-selection term on OP^2; it does not SUPPLY that "
            "term — F0 and S1 stay charged.",
            "Even granting the kinetic pi, pi/432 is not promoted: the 432 = 16*27 measure "
            "normalisation is Schur-forced elsewhere (epsilon_measure_schur) but the seed half — "
            "the absolute hierarchy — has no derived selector here.",
        ),
        kill_conditions=(
            "Presenting the FORM pass (pi emerges) as deriving pi/432, promoting F0, or moving any "
            "Bayes credit — only BOTH halves passing would flip the sign, and CONTENT fails.",
            "Spinning the result as positive: reporting that the topological route 'works' without "
            "the decisive CONTENT failure (N3 flat on OP^2, the hierarchy not an N3 critical "
            "point, the ~1.40-decade ladder miss) stated equally loudly.",
            "Hiding the no-go's scope: claiming seed-selection is merely 'not yet done' rather "
            "than IMPOSSIBLE for any F4-invariant potential (the symmetry obstruction), or letting "
            "the OP^2-flatness / great-circle-pi facts drift silently.",
        ),
    ),
    "berry_pi_intrinsic_op2": contract(
        "berry_pi_intrinsic_op2",
        ("F0", "G1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "HARDENS the FORM (the pi) of pi/432 — the pi that berry_sigma_model_op2 emitted was the "
        "Berry holonomy of ONE associative CP^1 slice of OP^2; this module proves the pi is "
        "INTRINSIC to OP^2 and explains WHY it is a half-turn, claiming ONLY what the computation "
        "shows. [A] ORIGIN: the transition CP^1's two antipodal poles are ORTHOGONAL primitive "
        "idempotents E1, E2 of J3(O) (Tr(E1 o E2) = 0 — two of the three generations); the Berry "
        "phase obeys gamma(theta) = pi(1 - cos theta) exactly, rising monotonically to the great "
        "circle — the unique closed geodesic, the locus EQUIDISTANT from the two orthogonal "
        "generations — which encloses the hemisphere (Omega = 2pi) and gives pi (a non-geodesic "
        "latitude gives < pi). So pi is the holonomy that SEPARATES two orthogonal generations, "
        "not an input. [B] INTRINSIC: F4 = Aut(J3(O)) preserves the Jordan product and trace, "
        "hence is an ISOMETRY of the trace metric (verified ~1e-13); transporting the great-circle "
        "loop by a random F4 automorphism keeps it a loop of genuine rank-one idempotents "
        "(P o P = P, N3 = 0), preserves EVERY consecutive overlap Tr(P_i o P_{i+1}) — the full "
        "metric data the Berry phase = 1/2 * (round area) depends on — yet moves it into GENUINELY "
        "OCTONIONIC directions (the e2..e7 components, zero on the associative slice, become ~0.2). "
        "Since OP^2 = F4/Spin(9) is two-point-homogeneous, every geodesic 2-sphere is an F4-image "
        "of the base CP^1 and the isometry-invariant Berry phase is the SAME pi: the pi belongs to "
        "OP^2, not to the complex slice. [C] SIGN: the great-circle Bargmann product is a NEGATIVE "
        "real number (e^{i pi} = -1, the vacuum ray returns to MINUS itself) — the SU(2) "
        "double-cover half-turn, the same sqrt/half-angle epsilon_vcb_halfangle reads as "
        "tan(pi/8). NET: the kinetic pi of pi/432 is hardened against the octonionic directions "
        "and tied to generation-orthogonality, WITHOUT evaluating an (ill-defined, non-associative) "
        "octonionic Bargmann product — it proves the phase-determining trace data is F4-invariant. "
        "This does NOT touch the CONTENT half (the three seeds): berry_sigma_model_op2 showed every "
        "F4-invariant is flat on OP^2, so seed-selection still needs an F4-BREAKING term. No Bayes "
        "credit moves, pi/432 is NOT promoted, F0 stays GEOMETRIC/open. Do NOT present hardening "
        "the FORM as deriving the constant or as closing the seed half.",
        assumptions=(
            "The J3(O) trace metric Tr(P o Q), the primitive idempotents E1,E2,E3, the cubic norm "
            "N3, the F4 automorphism action, and the great-circle Berry phase are taken as "
            "source-of-truth from epsilon_orbit_selection / epsilon_action_selection; this module "
            "embeds complex coherent states as rank-one J3(O) projectors (verified: embed(e_i)=E_i, "
            "P o P = P, N3 = 0, Tr(P o Q) = |<psi|phi>|^2) and measures the holonomy and its "
            "F4-invariance, re-deriving none of them.",
            "The transition sphere is the CP^1 in a complex (associative) 2-plane of O^3; its two "
            "poles are the orthogonal idempotents E1, E2 and the great circle is the "
            "minimal/geodesic loop. The phase is computed by the well-defined COMPLEX Bargmann "
            "product on this slice; the F4-transport argument proves INVARIANCE of the "
            "phase-determining trace data, NOT a re-evaluation of an octonionic Bargmann product "
            "(which is non-associative and ill-defined).",
            "Intrinsicness rests on F4 being an isometry (verified here to ~1e-13) PLUS the "
            "standard fact that the Berry phase = 1/2 * (round area) is isometry-invariant on a "
            "two-point-homogeneous (rank-one symmetric) space; that differential-geometric fact is "
            "CITED, not re-derived. The claim is that the phase-determining data is F4-invariant "
            "and the loop genuinely octonionic, hence the phase is the same pi.",
        ),
        open_bridges=(
            "This hardens only the FORM (the pi): it shows the kinetic holonomy is intrinsic and a "
            "half-turn, but deriving that the FULL CHO dynamics realises THIS Berry/WZ kinetic term "
            "(this target, this normalisation) rather than positing it stays open — the same "
            "architecture seam berry_sigma_model_op2 / epsilon_action_selection carry.",
            "The CONTENT half is untouched: every F4-invariant is flat on OP^2 "
            "(berry_sigma_model_op2), so the three eigenvalue-seeds still require an F4-BREAKING "
            "seed-selection term that this module does NOT supply — F0 and G1 stay charged.",
            "Even with the pi shown intrinsic and orthogonality-forced, pi/432 is NOT promoted: the "
            "432 = 16*27 measure is Schur-forced elsewhere (epsilon_measure_schur) and the "
            "seed/absolute-hierarchy half has no derived selector; the half-turn ties pi to N_gen=3 "
            "geometrically but does not by itself DERIVE the constant.",
        ),
        kill_conditions=(
            "Presenting the FORM hardening (pi intrinsic, half-turn from orthogonality) as DERIVING "
            "pi/432, promoting F0, or moving any Bayes credit — this module moves none; only the "
            "CONTENT half (the seeds), still open, could flip the sign.",
            "Letting the F4-invariance be read as a re-evaluated octonionic Bargmann phase (it is "
            "NOT — octonionic Tr(P1 P2 P3) is associator-ambiguous); the honest claim is INVARIANCE "
            "of the real trace data plus the cited isometry-invariance of the half-area phase.",
            "Claiming the CONTENT/seed half is closed or 'nearly closed' by this FORM result, or "
            "letting the orthogonal-poles / gamma=pi(1-cos theta) / F4-isometry / octonionic-support "
            "/ -1-sign facts drift silently.",
        ),
    ),
    "f4_breaking_seed_op2": contract(
        "f4_breaking_seed_op2",
        ("F0", "S1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "LOCALIZES the CONTENT (the three seeds) of pi/432 — berry_sigma_model_op2 proved a no-go "
        "(N3 and every F4-invariant is flat on OP^2, so seed-selection requires an F4-BREAKING "
        "term); this module tests whether the framework's OWN canonical F4-breaking object — the "
        "rank-one triality-breaking vacuum spurion |tau><tau| (epsilon_rank_one_kernel, "
        "spurion_bridge) — supplies it, and reports a TWO-SIDED result claiming ONLY what the "
        "computation shows. [POSITIVE — the no-go is EVADED] the linear frame-breaking height "
        "V_A(P) = Tr(P o A) has, on OP^2, critical points EXACTLY at the three primitive "
        "idempotents E1,E2,E3 of A's eigenframe (the standard Morse theory of a height function on "
        "the flag manifold F4/Spin(9)): the F4-gradient g_D = Tr((D.P) o A) vanishes (~1e-16) at "
        "all three generations for a frame-diagonal A, gradient ASCENT from random OP^2 points "
        "flows to the top generation (overlap 1.0000), and the F4-INVARIANT control A = I is flat "
        "(V = Tr P = 1, gradient ~1e-15 — reproduces the no-go). So the three generations ARE the "
        "critical set of the canonical frame-breaking potential, and the DIRECTION is "
        "frame-canonical, NOT circular: any distinct-spectrum A in the generation frame gives the "
        "SAME three critical points (only the values change). [HONEST OPEN — the magnitudes are "
        "INPUT] the critical VALUES are V_A(E_i) = spec(A), so the seed MAGNITUDES are the spurion "
        "spectrum (a tautology: seed in, seed out); and the canonical vacuum spurion is RANK-ONE, "
        "lifting EXACTLY ONE level (V(E_tau) = 1, the whole OP^1 of idempotents orthogonal to "
        "E_tau degenerate at value 0 — the geometric form of spurion_perturbation FACT 1), so "
        "three ISOLATED tiers require CUMULATIVE orders A = E1 + eps0 E2 + eps0^2 E3 whose spectrum "
        "(1, eps0, eps0^2) reproduces the generation cascade ladder, leaving the absolute scale "
        "eps0^2 = pi/432 (the geometric measure) as the lone surviving input. NET: tightens "
        "berry_sigma_model_op2's open clause 'seed-selection requires an F4-BREAKING term' into "
        "'the F4-breaking term IS the rank-one vacuum spurion; it makes the three generations the "
        "critical points (real, frame-canonical/non-circular DIRECTION), rank-one-ness forces the "
        "cumulative-order cascade, and the lone open scalar is the absolute scale eps0^2 = pi/432'. "
        "The CONTENT half is LOCALIZED to one scalar (the measure) but NOT closed: the seed "
        "magnitudes are still input. No Bayes credit moves, pi/432 is NOT promoted, F0 stays "
        "GEOMETRIC/open. Do NOT present evading the no-go (the FORM of selection) as deriving the "
        "seeds.",
        assumptions=(
            "The J3(O) trace metric Tr(P o Q), the three primitive idempotents E1,E2,E3 (the "
            "generation frame), the cubic norm N3, and the F4 = Aut(J3(O)) derivation/automorphism "
            "action are taken source-of-truth from epsilon_orbit_selection / "
            "epsilon_action_selection; this module forms the linear height V_A(P) = Tr(P o A) and "
            "its F4-orbit gradient g_D = Tr((D.P) o A) and measures the critical set, re-deriving "
            "none of the underlying algebra.",
            "That the three primitive idempotents are the critical points of a frame-diagonal "
            "height function is the STANDARD Morse theory of a height function on the flag manifold "
            "OP^2 = F4/Spin(9) (critical points = torus-fixed points = the eigenframe idempotents); "
            "it is CITED, not re-derived. The NEW content is the identification of the height "
            "function's linear term A with the framework's canonical rank-one vacuum spurion, and "
            "the rank-one => one-level => cascade chain.",
            "The canonical F4-breaking object is taken to be the rank-one triality-breaking vacuum "
            "spurion |tau><tau| = a primitive idempotent (epsilon_rank_one_kernel, spurion_bridge), "
            "and eps0^2 = pi/432 is taken from the measure (spurion_bridge); this module does NOT "
            "re-derive either — it tests what spectrum that spurion's height function selects.",
        ),
        open_bridges=(
            "The seed MAGNITUDES are not derived: V_A(E_i) = spec(A) is a tautology (the seed is "
            "put in as A's spectrum and read back as the critical values). The module localizes "
            "WHERE the input sits (the spurion spectrum) and WHY it is forced into cascade form "
            "(rank-one-ness), but does NOT remove it — F0 and S1 stay charged.",
            "The generation ASSIGNMENT (which idempotent is the heaviest) is the residual S3/Weyl "
            "freedom — the 'which channel' input — untouched here; the height function fixes the "
            "critical SET (the three generations) but not the ordering.",
            "Even with the three generations shown to be the critical points of the canonical "
            "spurion's height function, pi/432 is NOT promoted: the absolute scale eps0^2 = pi/432 "
            "is the lone surviving input and is fixed by the measure (epsilon_measure_schur, "
            "spurion_bridge) elsewhere, not derived here; localizing the seam is not closing it.",
        ),
        kill_conditions=(
            "Presenting the no-go EVASION (the three generations = critical points of the canonical "
            "frame-breaking height) as DERIVING the seed magnitudes, promoting F0/S1, or moving any "
            "Bayes credit — this module moves none; the magnitudes remain spec(A) input.",
            "Letting the frame-canonical (non-circular) DIRECTION be read as implying the "
            "MAGNITUDES are non-circular — they are not: spec(A) is the input. The honest claim is "
            "that the critical-point SET (the generations) is magnitude-free, NOT the values.",
            "Claiming the CONTENT/seed half is closed or 'nearly closed', or letting the "
            "critical-points-at-the-generations / values=spec(A) / rank-one-lifts-one-level / "
            "(1,eps0,eps0^2)-cascade / eps0^2=pi/432 facts drift silently.",
        ),
    ),
    "f0_sigma_model_closeout": contract(
        "f0_sigma_model_closeout",
        ("F0", "S1", "G1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "CLOSEOUT of the OP^2 Berry/Wess-Zumino sigma-model route to pi/432 — a REPORTER (it "
        "re-derives nothing and grants NO Bayes credit) that consolidates the three sigma-model "
        "EXPLORATORY modules (berry_sigma_model_op2 #86, berry_pi_intrinsic_op2 #87, "
        "f4_breaking_seed_op2 #88) and records the route as the FOURTH independent "
        "converging-negative on the one missing dynamical action. Claim ONLY what the consolidation "
        "shows. [CONVERGENCE] the sigma-model route reaches the SAME wall as the spectral-triple "
        "route (f0_phase1_closeout: prefactor a4/a2 REFUTED, L_X-spectrum ratios PARTIAL) and the "
        "topological-theta route (f0_theta_reality_gate: theta = 0): the entire remaining F0 gap is "
        "ONE derived dynamical action that must both PRODUCE pi/432 and SELECT the three seeds — "
        "now confirmed from the dynamical/topological side (asserted: all four routes name real "
        "audited contracts). [SHARPENING — the one genuinely-new thing] the route says what KIND of "
        "action is missing: #86's no-go proves any F4-INVARIANT action is flat on the vacuum "
        "manifold OP^2, so the missing action must BREAK F4; #88 then shows the canonical "
        "F4-breaking rank-one vacuum spurion supplies the DIRECTION (the three generations are "
        "EXACTLY the Morse critical points of the frame-breaking height V_A(P)=Tr(P o A)) but NOT "
        "the MAGNITUDE (the critical values are spec(A); the absolute scale is pi/432, the lone "
        "surviving input). So 'need a derived action' sharpens to 'need a derived F4-BREAKING action "
        "whose flux is pi/432 and whose spectrum is the seed' — DIRECTION solved, MAGNITUDE open. "
        "[STANDING] the scoreboard sign does NOT flip (CONTENT/magnitude stays open): pi/432 stays "
        "Berry/Schur GEOMETRIC, F0 stays GEOMETRIC/open, no Bayes credit moves, the earned floor "
        "stays ln B = -3.2 < 0 (asserted). Source-of-truth tripwires (asserted): the three "
        "sigma-model probes are still STATUS_EXPLORATORY/VERDICT_OPEN and still humble (>=1 open "
        "bridge AND >=1 kill condition). Do NOT present the convergence or the F4-breaking "
        "sharpening as deriving pi/432 or the seeds; recorded STATUS_EXPLORATORY / VERDICT_OPEN, "
        "forbids only SILENT drift.",
        assumptions=(
            "The three sigma-model module results (#86 FORM-passes/CONTENT-no-go, #87 pi "
            "F4-intrinsic, #88 generations = Morse critical points / values = spec(A)) and the four "
            "converging-negative contracts (f0_spectral_action_heatkernel, spectral_action_432, "
            "f0_theta_reality_gate, f4_breaking_seed_op2) are taken source-of-truth from their own "
            "modules; this reporter re-derives NONE of them — it asserts their status/verdict and "
            "consolidates the convergence and the sharpening.",
            "The 'fourth converging-negative' framing rests on f0_phase1_closeout (the prefactor "
            "and ratio routes) and f0_theta_reality_gate (the topological-theta route) being the "
            "prior three independent routes to the same missing object; this module CITES that "
            "established convergence, it does not re-run those routes.",
            "The honest fork (the sign does not flip; the FORM/pi is settled, the MAGNITUDE/seed "
            "stays open) and the lone input eps0^2 = pi/432 are taken from f4_breaking_seed_op2 / "
            "spurion_bridge / epsilon_measure_schur; this module records them, it does not "
            "re-derive the constant.",
        ),
        open_bridges=(
            "The CONTENT/magnitude half stays open: the missing F4-BREAKING action that would "
            "supply the absolute scale (= pi/432) and the seed magnitudes is LOCALISED by this "
            "consolidation, not SUPPLIED — F0 and S1 stay charged.",
            "This is a REPORTER over an EXPLORATORY arc: it adds no new derivation, and the "
            "architecture seam the three sigma-model modules carry (deriving that the FULL CHO "
            "dynamics realises THIS Berry/WZ sigma-model — this target, this normalisation, this "
            "F4-breaking term — rather than positing it) is untouched here.",
            "The four-route convergence is strong (negative) evidence that the missing object is "
            "SINGULAR, but it does not PROVE uniqueness or exhaust all routes; the genuinely new "
            "lever that could move the bottom line is the EXTERNAL datum sin^2 theta23 = 4/7 "
            "(theta23_octant_prediction; DUNE / Hyper-K), not another internal derivation.",
        ),
        kill_conditions=(
            "Presenting the convergence or the F4-breaking sharpening as DERIVING pi/432 or the "
            "seed magnitudes, promoting F0/S1/G1, or moving any Bayes credit — only BOTH halves "
            "(FORM and CONTENT) passing would flip the sign, and the CONTENT/magnitude half stays "
            "open.",
            "Spinning the route as a positive result: reporting that the sigma-model 'works' or "
            "that the FORM (pi) being settled and F4-intrinsic CLOSES the lever, without the "
            "CONTENT/magnitude failure (the seeds are spec(A) input, the absolute scale is the lone "
            "open pi/432) stated equally loudly.",
            "Letting the reporter drift: a sigma-model probe silently promoted out of "
            "EXPLORATORY/OPEN, the earned scoreboard floor silently moved off ln B = -3.2, or the "
            "four-route convergence silently reduced — the tripwire assertions must stay live.",
        ),
    ),
    "f4_breaking_action_origin_gate": contract(
        "f4_breaking_action_origin_gate",
        ("F0", "S1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "F4-breaking action-origin modulus gate. Claim only the narrowing result: "
        "the OP^2 height dynamics fixes the generation frame and the cascade form, "
        "but the family A(r)=E1+rE2+r^2E3 has the same critical set for a continuum "
        "of r, and the entropy/free-energy completion gives Gibbs ratios "
        "(1, exp(-beta), exp(-2 beta)) with beta a continuous Lagrange multiplier. "
        "Matching eps0 requires beta=-log(eps0)=0.5 log(432/pi), but this scalar "
        "is not selected by the current action. The live bridge is therefore narrowed "
        "to deriving beta or r=eps0 from CHO dynamics; do not promote F0/S1 or move "
        "Bayes credit.",
        assumptions=(
            "The generation-frame critical-set result and F4-orbit height dynamics are "
            "taken source-of-truth from f4_breaking_seed_op2; this module varies the "
            "spurion spectrum modulus and checks that the critical set persists.",
            "The entropy/free-energy completion is the standard constrained-entropy "
            "calculation with grade energy (0,1,2); it supplies the Gibbs form but not "
            "the inverse-temperature value.",
            "eps0^2=pi/432 is taken from the existing Berry/Schur measure reading; this "
            "module tests whether the current dynamics selects it and reports that it does not.",
        ),
        open_bridges=(
            "Derive the scalar modulus beta=0.5 log(432/pi) or r=eps0 from the actual "
            "CHO dynamics rather than inserting it as spec(A) or a Lagrange multiplier.",
            "Derive why the F4-breaking spurion's effective spectrum is cumulative "
            "(1, eps0, eps0^2) with this absolute scale, not merely why that form is stationary.",
        ),
        kill_conditions=(
            "Presenting the persistence of the critical set for A(r) as a derivation of eps0.",
            "Treating the Gibbs beta that matches eps0 as selected rather than fitted/inserted.",
            "Promoting F0/S1, moving model_complexity or scoreboard credit, or hiding that the "
            "new result is a modulus no-go/localization rather than a closure.",
        ),
    ),
    "f4_breaking_beta_selection_gate": contract(
        "f4_breaking_beta_selection_gate",
        ("F0", "S1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "F4-breaking beta-selection gate. Claim only the narrowed negative: after "
        "f4_breaking_action_origin_gate reduced the live bridge to beta=-log(eps0), "
        "this module tests the obvious scalar-fixing mechanisms and finds none selected "
        "by the current CHO dynamics. Entropy fixes beta only after a mean grade is supplied; "
        "dimension-only selectors miss pi/432; the exact identity exp(-2 beta)=pi/432 "
        "appears only if one postulates the Berry-flux/state-count map; WZ integrality "
        "leaves k*pi/432 and does not select k=1 by itself; additive Berry/Schur constants "
        "drop out of beta stationarity. The remaining bridge is a genuine beta-dependent "
        "CHO variational term or primitive-sector rule. Do not promote F0/S1 or move Bayes credit.",
        assumptions=(
            "The previous modulus gate is source-of-truth that the height dynamics and "
            "Gibbs cascade leave beta continuous; this module tests candidate scalar-fixing "
            "rules rather than re-proving the critical-set result.",
            "Entropy calculations use the grade set (0,1,2) and standard Gibbs duality: "
            "beta is conjugate to a supplied mean grade, so a target mean that reproduces "
            "eps0 is treated as fitted unless independently derived.",
            "The Berry flux pi and Schur state count 432 are existing source-of-truth pieces; "
            "the conditional identity exp(-2 beta)=pi/432 is tested as a map, not claimed as "
            "selected by the present action.",
        ),
        open_bridges=(
            "Derive a beta-dependent CHO variational term whose stationarity equation outputs "
            "beta=0.5 log(432/pi) rather than accepting beta as a Lagrange multiplier.",
            "Derive why the primitive WZ level k=1 is selected for the seed spectrum, rather "
            "than merely noting that k=1 reproduces the target while k>1 is also admissible.",
            "Derive the flux/state-to-spectrum map exp(-2 beta)=pi/432 from the action; otherwise "
            "it remains an inserted identification of the geometric measure with the spurion scale.",
        ),
        kill_conditions=(
            "Presenting exp(-2 beta)=pi/432 as a derivation of beta without deriving the map that "
            "turns Berry flux divided by state count into the Gibbs inverse temperature.",
            "Quoting the fitted target mean grade or primitive k=1 level while suppressing the "
            "natural-mean misses and the k*pi/432 family.",
            "Promoting F0/S1, moving scoreboard/model_complexity credit, or hiding that this is a "
            "scalar-selection no-go/localisation rather than a closure.",
        ),
    ),
    "f4_breaking_primitive_level_gate": contract(
        "f4_breaking_primitive_level_gate",
        ("F0", "S1"),
        STATUS_EXPLORATORY,
        VERDICT_OPEN,
        "F4-breaking primitive-level gate. Claim only the conditional narrowing: WZ filling "
        "independence for S_WZ=(k/2)Omega forces k to be an integer, killing continuous WZ "
        "normalisation freedom. With carrier weight 1/432, the half-turn density is k*pi/432; "
        "primitive positive k=1 gives exp(-2 beta)=pi/432 exactly. But integrality alone leaves "
        "many positive admissible levels, so k=1 remains a primitive-sector selection rule rather "
        "than a derived dynamical output. The remaining bridge is deriving primitive level-one "
        "selection from CHO dynamics; do not promote F0/S1 or move Bayes credit.",
        assumptions=(
            "The Berry half-turn pi and Schur carrier count 432 are source-of-truth from the "
            "existing OP^2/Berry and measure gates; this module only tests the WZ level sub-bridge.",
            "The WZ action is assumed to have the CP^1 disk form S_WZ=(k/2)Omega, so changing the "
            "filling by one sphere shifts the action by 2*pi*k; single-valuedness of exp(iS) is the "
            "integrality criterion under test.",
            "Positive Gibbs ratios require 0<k*pi/432<1; this leaves a finite but non-singleton "
            "integer family, so minimal positive level is treated as an extra primitive-sector rule.",
        ),
        open_bridges=(
            "Derive from CHO dynamics that the physical sector is primitive level one, rather than "
            "any other admissible positive integer level.",
            "Derive the oriented WZ term itself and its coupling to the F4-breaking seed spectrum; "
            "this gate only quantises its level once the term is assumed.",
            "Tie primitive level-one selection to the beta-dependent variational principle named by "
            "f4_breaking_beta_selection_gate, so exp(-2 beta)=pi/432 is selected rather than imposed.",
        ),
        kill_conditions=(
            "Presenting WZ integrality as deriving beta or the seed scale while suppressing the "
            "non-singleton integer level family.",
            "Treating primitive k=1 as forced by this gate rather than conditional on a separate "
            "primitive-sector selection principle.",
            "Promoting F0/S1, moving scoreboard/model_complexity credit, or hiding that this kills "
            "continuous normalization freedom but leaves discrete level selection open.",
        ),
    ),
    "theory_probation_closeout": contract(
        "theory_probation_closeout",
        ("F0", "S1", "G1"),
        STATUS_DIAGNOSTIC,
        VERDICT_DIAGNOSTIC,
        "Governance reporter only. Claim that the durable theorem-level core is to be "
        "preserved and polished (PAPER_JORDAN_THEOREMS.md / J3(O) idempotent frame / "
        "Schur weights / Freudenthal cubic seesaw / OP^2-Berry geometry), while the "
        "SM-constant physics claim is on probation. The only internal route worth more "
        "time is the f0_sigma_model_closeout route: derive an F4-BREAKING dynamical "
        "action whose flux gives pi/432 and whose spectrum gives the seed. If that "
        "cannot be done without inserting the scale/seed by hand, demote the SM-constant "
        "program to beautiful algebraic numerology with strong structure, not a theory "
        "of nature. Do NOT present this reporter as a derivation, a new physics result, "
        "or a Bayes-credit-moving artifact; it archives failed routes as null records "
        "and guards the probation policy against silent overclaiming.",
        assumptions=(
            "Durable-core artifacts are source-of-truth contracts already in the audit "
            "harness: jordan_standalone_theorems, three_generations_frame, "
            "epsilon_measure_schur, generation_cascade, berry_sigma_model_op2, "
            "berry_pi_intrinsic_op2, and f4_breaking_seed_op2.",
            "Inactive routes are preserved as negative/closeout records rather than "
            "deleted: f0_spectral_action_heatkernel, f0_theta_reality_gate, "
            "rg_scale_derivation, big_bets_closeout, and gold_standard_closeout.",
            "The earned scoreboard floor is read from scoreboard.scoreboard(F=3.0) as "
            "a tripwire against silent drift, not as a frozen constant; deliberate "
            "re-verified scientific changes are allowed.",
        ),
        open_bridges=(
            "This reporter closes no physics bridge. The live bridge remains exactly "
            "the one named by f0_sigma_model_closeout: derive the F4-breaking action "
            "whose flux is pi/432 and whose spectrum gives the seed.",
        ),
        kill_conditions=(
            "Citing the durable-core preservation as evidence that the SM constants are "
            "derived, or using this reporter to promote F0/S1/G1 or move Bayes credit.",
            "Treating archived null routes as active proof routes again without a new "
            "mechanism that directly derives the F4-breaking action.",
            "Suppressing the demotion rule: if the action cannot be derived without "
            "hand-inserting pi/432 or the seed spectrum, the physics claim must be "
            "demoted to structured algebraic numerology rather than defended as a "
            "theory of nature.",
        ),
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
    "f0_vacuum_orbit_gate": contract(
        "f0_vacuum_orbit_gate",
        ("F0", "Q1"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Use as a ray-selection checkpoint only: fixing the vacuum should collapse "
        "the transition class to one stabilizer orbit, but the CHO action-derived "
        "physical representative remains open.",
        open_bridges=("Physical transition ray representative from CHO action dynamics.",),
    ),
    "f0_transition_ray_gate": contract(
        "f0_transition_ray_gate",
        ("F0", "Q1", "K1", "STAT1"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Use as a consistency gate only: vacuum orbit, action-selected holonomy, "
        "and unique trace space all agree on one ray representative, but the CHO "
        "action still has not derived that representative from first principles.",
        open_bridges=("Physical transition ray representative from CHO action dynamics.",),
    ),
    "f0_action_ray_gate": contract(
        "f0_action_ray_gate",
        ("F0", "STAT1"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Use as an effective-dynamics derivation gate: the transition ray is "
        "derived as a unique stationary maximizer of the current action generator, "
        "while derivation of that generator from full CHO action remains open.",
        open_bridges=("Physical transition ray from full CHO action dynamics.",),
    ),
    "f0_action_kernel_dynamics_gate": contract(
        "f0_action_kernel_dynamics_gate",
        ("F0", "STAT1"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Use as an effective-dynamics admissible-class gate: O>=0 and Tr(O)=pi "
        "follow from action-flow closure in the current scaffold, while derivation "
        "of this flow from full CHO action remains open.",
        open_bridges=("Admissible epsilon-kernel class from full CHO action dynamics.",),
    ),
    "f0_kernel_class_gate": contract(
        "f0_kernel_class_gate",
        ("F0", "STAT1"),
        STATUS_DERIVED_BRIDGE,
        VERDICT_OPEN,
        "Use as admissible-class consistency only: positivity + trace normalization "
        "follow from current symmetry/convex closure assumptions, but deriving those "
        "assumptions from full CHO action dynamics remains open.",
        open_bridges=("Admissible epsilon-kernel class from full CHO action dynamics.",),
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