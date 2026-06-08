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