"""
Phase 4 continuum/RG matching audit.
=====================================

This is a gate, not a new fit. It separates four things that were previously
blurred in the electroweak/cosmology rows:

1. CHO algebraic boundary terms.
2. Standard one-loop SM running from declared inputs.
3. Threshold or vacuum-polarization data borrowed from the SM/experiment.
4. Matching scales inferred from the observed target.

A successful Phase 4 theorem would derive the matching scales and thresholds
from the CHO action before comparing to low-energy data. This audit exits zero
when the bookkeeping is explicit and the open assumptions are not hidden.
"""

from dataclasses import dataclass
import math


PI = math.pi

M_Z = 91.1876  # GeV
M_PLANCK = 1.221e19  # GeV
M_SEESAW = M_PLANCK / 3.0**9
M_W_OBS = 80.377  # GeV
ALPHA_EM_INV_0 = 137.035999084
ALPHA_EM_INV_MZ = 127.955
SIN2_W_MZ = 0.23122
ALPHA_S_MZ = 0.1179

# SM one-loop beta coefficients in GUT normalization:
# beta(g_i) = b_i g_i^3/(16*pi^2), so
# d alpha_i^{-1}/d ln(mu) = -b_i/(2*pi).
B1 = 41.0 / 10.0
B2 = -19.0 / 6.0
B3 = -7.0


@dataclass(frozen=True)
class GateCheck:
    requirement: str
    status: str
    metric: str
    note: str


@dataclass(frozen=True)
class BoundaryRow:
    observable: str
    cho_boundary: str
    scale_status: str
    residual: str
    verdict: str


@dataclass(frozen=True)
class CandidateScale:
    name: str
    scale_gev: float
    sin2: float
    status: str


def mz_gauge_couplings():
    """Return GUT-normalized inverse gauge couplings at M_Z."""
    alpha_em_mz = 1.0 / ALPHA_EM_INV_MZ
    alpha1_inv = (3.0 / 5.0) * (1.0 - SIN2_W_MZ) * ALPHA_EM_INV_MZ
    alpha2_inv = SIN2_W_MZ * ALPHA_EM_INV_MZ
    alpha3_inv = 1.0 / ALPHA_S_MZ
    return alpha1_inv, alpha2_inv, alpha3_inv


def inverse_coupling_at(inv_mz, beta_coefficient, scale_gev):
    """One-loop inverse coupling at scale_gev from the M_Z value."""
    return inv_mz - (beta_coefficient / (2.0 * PI)) * math.log(scale_gev / M_Z)


def sin2_from_inverse(alpha1_inv, alpha2_inv):
    """Compute sin^2(theta_W) from GUT-normalized alpha_1 and alpha_2."""
    alpha1 = 1.0 / alpha1_inv
    alpha2 = 1.0 / alpha2_inv
    return (3.0 / 5.0) * alpha1 / ((3.0 / 5.0) * alpha1 + alpha2)


def sin2_at_scale(scale_gev):
    alpha1_inv_mz, alpha2_inv_mz, _ = mz_gauge_couplings()
    alpha1_inv = inverse_coupling_at(alpha1_inv_mz, B1, scale_gev)
    alpha2_inv = inverse_coupling_at(alpha2_inv_mz, B2, scale_gev)
    return sin2_from_inverse(alpha1_inv, alpha2_inv)


def scale_for_sin2(target=0.25):
    """Analytic inverse-running scale where sin^2(theta_W)=target."""
    alpha1_inv_mz, alpha2_inv_mz, _ = mz_gauge_couplings()
    gut_factor = 3.0 / 5.0
    inverse_ratio = gut_factor * (1.0 - target) / target
    numerator = alpha1_inv_mz - inverse_ratio * alpha2_inv_mz
    denominator = (B1 / (2.0 * PI)) - inverse_ratio * (B2 / (2.0 * PI))
    log_scale_ratio = numerator / denominator
    return M_Z * math.exp(log_scale_ratio), log_scale_ratio


def alpha_boundary_inverse():
    return 128.0 * PI / 3.0


def qed_leptonic_delta(mu_gev):
    """Leading-log leptonic shift in alpha^{-1} from 0 to mu."""
    masses = (0.00051099895, 0.1056583755, 1.77686)
    delta = 0.0
    for mass in masses:
        if mu_gev > mass:
            delta += (2.0 / (3.0 * PI)) * math.log(mu_gev / mass)
    return delta


def alpha_leptonic_only_matching_scale(target_delta):
    """Find the leptonic-only scale that would supply target_delta."""
    low = 0.000511
    high = 1.0e6
    for _ in range(120):
        mid = math.sqrt(low * high)
        if qed_leptonic_delta(mid) < target_delta:
            low = mid
        else:
            high = mid
    return math.sqrt(low * high)


def qcd_scale_alpha_example(mu_gev=0.700):
    """Legacy QCD-threshold example: leptonic logs plus a hadronic VP remainder."""
    needed_delta = ALPHA_EM_INV_0 - alpha_boundary_inverse()
    leptonic = qed_leptonic_delta(mu_gev)
    hadronic_needed = needed_delta - leptonic
    return needed_delta, leptonic, hadronic_needed


def w_mass_boundary():
    boundary = M_PLANCK / 3.0**36
    normalization = M_W_OBS / boundary
    return boundary, normalization


def cc_boundary_mev():
    # Formula is Lambda^(1/4) = (11/12) M_P/(sqrt(2) 3^64).
    gev = (11.0 / 12.0) * M_PLANCK / (math.sqrt(2.0) * 3.0**64)
    return gev * 1.0e12


def boundary_rows():
    alpha_delta = ALPHA_EM_INV_0 - alpha_boundary_inverse()
    mw_boundary, mw_norm = w_mass_boundary()
    cc_mev = cc_boundary_mev()
    return [
        BoundaryRow(
            "alpha^-1(0)",
            f"128*pi/3 = {alpha_boundary_inverse():.3f}",
            "OPEN: EM/QCD matching scale not derived",
            f"VP residual needed = {alpha_delta:+.3f}",
            "OPEN",
        ),
        BoundaryRow(
            "sin^2(theta_W)",
            "1/4 at an algebraic electroweak scale",
            "OPEN: scale is target-implied unless derived",
            "standard one-loop running shifts 0.250 -> 0.23122",
            "OPEN",
        ),
        BoundaryRow(
            "M_W",
            f"M_P/3^36 = {mw_boundary:.3f} GeV",
            "Planck scale input; EW normalization open",
            f"multiplicative normalization = {mw_norm:.4f}",
            "OPEN NORMALIZATION",
        ),
        BoundaryRow(
            "Lambda^(1/4)",
            f"(11/12) M_P/(sqrt(2) 3^64) = {cc_mev:.3f} meV",
            "not an RG flow; free-energy matching open",
            "derive 3^64 and 11/12 screen from action",
            "OPEN",
        ),
    ]


def candidate_scales():
    target_scale, _ = scale_for_sin2(0.25)
    return [
        CandidateScale("target-implied sin^2=1/4 scale", target_scale,
                       sin2_at_scale(target_scale), "INVERSE MATCH"),
        CandidateScale("seesaw scale M_P/3^9", M_SEESAW,
                       sin2_at_scale(M_SEESAW), "NOT A MATCH"),
        CandidateScale("Planck scale", M_PLANCK,
                       sin2_at_scale(M_PLANCK), "NOT A MATCH"),
    ]


def structured_matching_report():
    return {
        "boundary_conditions": boundary_rows(),
        "candidate_scales": candidate_scales(),
        "gate_checks": gate_checks(),
    }


def gate_checks():
    target_scale, _ = scale_for_sin2(0.25)
    needed_delta, leptonic_qcd, hadronic_needed = qcd_scale_alpha_example()
    mw_boundary, mw_norm = w_mass_boundary()
    return [
        GateCheck(
            "standard one-loop convention declared",
            "PASS",
            "d alpha_i^-1/dln(mu) = -b_i/(2*pi)",
            "the sign convention is explicit and testable",
        ),
        GateCheck(
            "sin^2 matching scale not hidden",
            "OPEN",
            f"mu_* = {target_scale:.3e} GeV by inverse running",
            "derive this scale from CHO or keep S5 open",
        ),
        GateCheck(
            "alpha vacuum-polarization residual not hidden",
            "OPEN",
            f"needed {needed_delta:.3f}; at 0.7 GeV leptonic {leptonic_qcd:.3f}, hadronic remainder {hadronic_needed:.3f}",
            "hadronic VP and matching scale are external inputs today",
        ),
        GateCheck(
            "M_W normalization not hidden",
            "OPEN",
            f"M_P/3^36={mw_boundary:.3f} GeV, obs/boundary={mw_norm:.4f}",
            "the base-3 scale is close, but the EW normalization is not derived here",
        ),
        GateCheck(
            "cosmological constant kept outside RG promotion",
            "OPEN",
            f"Lambda^(1/4) formula gives {cc_boundary_mev():.3f} meV",
            "free-energy factorization and 11/12 screen remain separate obligations",
        ),
    ]


def print_boundary_ledger():
    print("BOUNDARY / RESIDUAL LEDGER")
    print("=" * 78)
    print(f"{'observable':<19} {'CHO boundary':<33} {'verdict':<18} residual")
    print("-" * 78)
    for row in boundary_rows():
        print(f"{row.observable:<19} {row.cho_boundary:<33} {row.verdict:<18} {row.residual}")
        print(f"{'':<19} scale: {row.scale_status}")
    print()


def print_sm_running():
    print("STANDARD ONE-LOOP SM GAUGE RUNNING")
    print("=" * 78)
    alpha1_inv, alpha2_inv, alpha3_inv = mz_gauge_couplings()
    print(f"Inputs at M_Z={M_Z:.4f} GeV:")
    print(f"  alpha_em^-1(M_Z) = {ALPHA_EM_INV_MZ:.3f}")
    print(f"  sin^2(theta_W)(M_Z) = {SIN2_W_MZ:.5f}")
    print(f"  alpha_s(M_Z) = {ALPHA_S_MZ:.4f}")
    print(f"  alpha_1^-1(M_Z) = {alpha1_inv:.3f}  (GUT normalized)")
    print(f"  alpha_2^-1(M_Z) = {alpha2_inv:.3f}")
    print(f"  alpha_3^-1(M_Z) = {alpha3_inv:.3f}")
    print()
    print(f"{'scale':<34} {'mu [GeV]':>13} {'sin^2_W(mu)':>14} provenance")
    print("-" * 78)
    for scale in candidate_scales():
        print(f"{scale.name:<34} {scale.scale_gev:>13.3e} {scale.sin2:>14.6f} {scale.status}")
    print()


def print_alpha_matching():
    print("ALPHA MATCHING ACCOUNTING")
    print("=" * 78)
    needed_delta, leptonic_qcd, hadronic_needed = qcd_scale_alpha_example()
    leptonic_only_scale = alpha_leptonic_only_matching_scale(needed_delta)
    print(f"CHO boundary alpha^-1 = 128*pi/3 = {alpha_boundary_inverse():.6f}")
    print(f"Thomson alpha^-1(0)   = {ALPHA_EM_INV_0:.6f}")
    print(f"Residual needed       = {needed_delta:.6f}")
    print()
    print("Two honest ways to view the current residual:")
    print(f"  leptonic-only inverse scale : {leptonic_only_scale:.3f} GeV")
    print(f"  legacy QCD-scale example    : 0.700 GeV + hadronic remainder")
    print(f"    leptonic logs at 0.700 GeV = {leptonic_qcd:.3f}")
    print(f"    hadronic VP remainder      = {hadronic_needed:.3f}")
    print("Both are external until the CHO action derives the matching scale and VP term.")
    print()


def print_gate():
    print("PHASE 4 GATE VERDICT")
    print("=" * 78)
    internal_fail = False
    for check in gate_checks():
        print(f"{check.status:<6} {check.requirement:<46} {check.metric}")
        print(f"       {check.note}")
        if check.status == "FAIL":
            internal_fail = True
    print()
    print("AUDIT STATUS: PASS - continuum/RG residuals are explicit.")
    print("THEOREM STATUS: OPEN - do not promote alpha, sin^2(theta_W), M_W, or Lambda to closed predictions yet.")
    if internal_fail:
        raise SystemExit(1)


def main():
    print("=" * 78)
    print("  PHASE 4 - CONTINUUM / RG MATCHING GATE")
    print("  Boundary terms, SM running, threshold inputs, and inverse matches separated.")
    print("=" * 78)
    print()
    print_boundary_ledger()
    print_sm_running()
    print_alpha_matching()
    print_gate()


if __name__ == "__main__":
    main()
