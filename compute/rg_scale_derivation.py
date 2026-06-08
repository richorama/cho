"""
Item 3 -- can the electroweak matching scale be DERIVED, or is it inverse-fit?
=============================================================================

Context (roadmap item 3, foundations/10_continuum_rg.md, rg_matching_audit.py)
------------------------------------------------------------------------------
The critical-evaluation roadmap asks to "derive the RG matching scales instead
of inverse-fitting them." The existing gate `rg_matching_audit.py` already flags
the matching scale mu_* (where one-loop running makes sin^2(theta_W) = 1/4) as an
INVERSE match: it is read off from the requirement, scale ~ 3.68 TeV, and is NOT
derived from the CHO action. The honest question this module closes is sharper:

    Is there ANY single CHO matching scale at which BOTH electroweak boundary
    conditions hold simultaneously?  CHO posits TWO algebraic boundaries,

        alpha_em^-1 = 128 pi / 3      (the fine-structure boundary)
        sin^2(theta_W) = 1/4          (the mixing boundary).

    Together these fix BOTH gauge couplings at the would-be matching scale mu_*:

        alpha_2^-1(mu_*) = sin^2 . alpha_em^-1            = 32 pi / 3   = 33.510
        alpha_1^-1(mu_*) = (3/5) cos^2 . alpha_em^-1      = 96 pi / 5   = 60.319

    (GUT-normalized alpha_1.) These are TWO numbers at ONE scale -- an
    OVER-DETERMINED system once we demand consistency with the measured M_Z
    couplings under standard one-loop running.

What this module finds (a KILL-branch result, reported honestly)
----------------------------------------------------------------
Running each measured M_Z coupling to its CHO boundary value INDEPENDENTLY:

    alpha_1^-1 reaches 60.319 at mu ~ 1.2e1  GeV   (just below M_Z)
    alpha_2^-1 reaches 33.510 at mu ~ 2.2e5  GeV

These two scales differ by a factor ~1.8e4. There is NO single scale mu_* at
which both CHO electroweak boundaries are consistent with the data at one loop.
Therefore the "matching scale" is not one derived number: it is selected
observable-by-observable to hit each target -- exactly the kill condition stated
in the rg_matching_audit contract.

Two corroborating facts:
  * No INDEPENDENTLY-derived CHO scale (Higgs vev v, M_W = M_P/3^36, the seesaw
    M_P/3^9, or M_P) yields sin^2(theta_W) = 1/4 under one-loop running -- the
    nearest, v, gives 0.236, and the seesaw gives 0.402.
  * The lone inverse-matched scale where sin^2 = 1/4 (3.68 TeV) is M_P/3^32.5 --
    a NON-integer power of 3, so it is not a clean CHO scale either; and (the
    look-elsewhere point of scale_look_elsewhere.py) powers of 3 tile that energy
    window so densely that a near-integer hit would carry no weight.

Verdict: the matching scale is NOT derived. Per the kill rule in
foundations/10_continuum_rg.md, S4/S5 stay Open bridge -- now with a sharper,
falsification-grade reason: the single-continuum-scale reading of the two CHO
electroweak boundaries is inconsistent with one-loop running by ~4 orders of
magnitude. This module does NOT promote any ledger row and does NOT touch the
scoreboard; it is the "kill" half of "close or kill the matching-scale seam".

numpy-free. Reuses rg_matching_audit (the one-loop running convention).
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from rg_matching_audit import (
    PI,
    M_Z,
    M_PLANCK,
    M_SEESAW,
    B1,
    B2,
    ALPHA_EM_INV_0,
    mz_gauge_couplings,
    inverse_coupling_at,
    sin2_from_inverse,
    sin2_at_scale,
    scale_for_sin2,
    alpha_boundary_inverse,
)

SIN2_CHO = 0.25                       # the mixing boundary
ALPHA_EM_INV_CHO = alpha_boundary_inverse()   # 128 pi / 3
HIGGS_VEV = 246.0                     # GeV
M_W_SCALE = M_PLANCK / 3.0**36        # the CHO M_W boundary scale

TOL = 1e-9
RATIO_FLOOR = 100.0                   # "single scale" would need ratio ~ 1


@dataclass(frozen=True)
class ScaleRow:
    label: str
    scale_gev: float
    sin2: float
    aem_inv: float
    note: str


def cho_implied_couplings():
    """The two CHO electroweak boundaries fix BOTH GUT-normalized inverse
    couplings at the would-be matching scale. Returns (alpha1_inv, alpha2_inv).

        alpha_2^-1 = sin^2 . alpha_em^-1                 = 32 pi / 3
        alpha_1^-1 = (3/5)(1 - sin^2) . alpha_em^-1      = 96 pi / 5
    """
    alpha2_inv = SIN2_CHO * ALPHA_EM_INV_CHO
    alpha1_inv = (3.0 / 5.0) * (1.0 - SIN2_CHO) * ALPHA_EM_INV_CHO
    return alpha1_inv, alpha2_inv


def scale_for_inverse_coupling(inv_mz, beta_coefficient, target_inv):
    """Scale where one coupling reaches target_inv under one-loop running.

    Inverts  target = inv_mz - (b/2pi) ln(mu/M_Z).
    Returns (scale_gev, ln_ratio).
    """
    ln_ratio = (inv_mz - target_inv) * (2.0 * PI) / beta_coefficient
    return M_Z * math.exp(ln_ratio), ln_ratio


def aem_inverse_at(scale_gev):
    """alpha_em^-1 reconstructed from the one-loop EW gauge couplings:
        1/alpha_em = 1/alpha_2 + (5/3)/alpha_1   (non-GUT hypercharge piece).
    Perturbative only (no hadronic vacuum polarization)."""
    a1_mz, a2_mz, _ = mz_gauge_couplings()
    a1_inv = inverse_coupling_at(a1_mz, B1, scale_gev)
    a2_inv = inverse_coupling_at(a2_mz, B2, scale_gev)
    return a2_inv + (5.0 / 3.0) * a1_inv


def overdetermination():
    """The core test: each CHO electroweak boundary, run independently, implies a
    DIFFERENT matching scale. Returns a dict of the two scales and their ratio."""
    a1_mz, a2_mz, _ = mz_gauge_couplings()
    a1_cho, a2_cho = cho_implied_couplings()
    mu1, ln1 = scale_for_inverse_coupling(a1_mz, B1, a1_cho)
    mu2, ln2 = scale_for_inverse_coupling(a2_mz, B2, a2_cho)
    ratio = max(mu1, mu2) / min(mu1, mu2)
    return {
        "a1_cho": a1_cho,
        "a2_cho": a2_cho,
        "mu_alpha1": mu1,
        "mu_alpha2": mu2,
        "ratio": ratio,
    }


def power_of_three_below_planck(scale_gev):
    """Express scale as M_P / 3^n; return (n, distance to nearest integer)."""
    n = math.log(M_PLANCK / scale_gev) / math.log(3.0)
    dist = abs(n - round(n))
    return n, dist


def derived_scale_rows():
    """Independently-derived CHO scales and the sin^2 / alpha they predict."""
    rows = []
    for label, mu, note in (
        ("Higgs vev v", HIGGS_VEV, "EW scale (input)"),
        ("M_W = M_P/3^36", M_W_SCALE, "CHO W-mass boundary"),
        ("seesaw M_P/3^9", M_SEESAW, "CHO neutrino seesaw"),
        ("Planck M_P", M_PLANCK, "UV boundary"),
    ):
        rows.append(
            ScaleRow(label, mu, sin2_at_scale(mu), aem_inverse_at(mu), note)
        )
    return rows


def main() -> bool:
    print("=" * 78)
    print("  ITEM 3 -- IS THE ELECTROWEAK MATCHING SCALE DERIVED OR INVERSE-FIT?")
    print("=" * 78)
    print("  CHO posits TWO electroweak boundaries: alpha_em^-1 = 128*pi/3 and")
    print("  sin^2(theta_W) = 1/4. A single derived matching scale must satisfy BOTH.")
    print(f"  alpha_em^-1(CHO) = 128*pi/3 = {ALPHA_EM_INV_CHO:.6f}")
    print()

    ok = True
    a1_mz, a2_mz, _ = mz_gauge_couplings()
    a1_cho, a2_cho = cho_implied_couplings()

    # [A] The over-determination test.
    od = overdetermination()
    print("-" * 78)
    print("  [A] OVER-DETERMINATION: two boundaries -> two DIFFERENT scales")
    print("-" * 78)
    print(f"      measured at M_Z : alpha_1^-1 = {a1_mz:.3f}   alpha_2^-1 = {a2_mz:.3f}")
    print(f"      CHO boundary    : alpha_1^-1 = {a1_cho:.3f}   alpha_2^-1 = {a2_cho:.3f}")
    print(f"        (= 96*pi/5 = {96.0 * PI / 5.0:.3f},  32*pi/3 = {32.0 * PI / 3.0:.3f})")
    print(f"      alpha_1^-1 -> CHO at mu = {od['mu_alpha1']:.3e} GeV")
    print(f"      alpha_2^-1 -> CHO at mu = {od['mu_alpha2']:.3e} GeV")
    print(f"      scale ratio = {od['ratio']:.3e}   (a single scale would give ~1)")
    a_ok = od["ratio"] > RATIO_FLOOR
    print(f"      [{'CONFIRMED' if a_ok else 'no'}] no single scale fits both boundaries "
          f"(ratio >> 1) -> matching scale is NOT one derived number")
    ok = ok and a_ok
    print()

    # [B] The lone inverse match (sin^2 = 1/4) is not a clean CHO scale.
    mu_sin, _ = scale_for_sin2(SIN2_CHO)
    n_sin, dist_sin = power_of_three_below_planck(mu_sin)
    print("-" * 78)
    print("  [B] THE INVERSE-MATCHED sin^2=1/4 SCALE IS NOT A CLEAN CHO SCALE")
    print("-" * 78)
    print(f"      sin^2(theta_W) = 1/4 at mu_* = {mu_sin:.3e} GeV (inverse match)")
    print(f"      mu_* = M_P / 3^{n_sin:.2f}   (nearest integer power off by {dist_sin:.2f})")
    b_ok = dist_sin > 0.1
    print(f"      [{'CONFIRMED' if b_ok else 'no'}] non-integer power of 3 -> not derived as M_P/3^n")
    ok = ok and b_ok
    print()

    # [C] No independently-derived CHO scale yields sin^2 = 1/4.
    rows = derived_scale_rows()
    print("-" * 78)
    print("  [C] NO INDEPENDENTLY-DERIVED CHO SCALE GIVES sin^2 = 1/4")
    print("-" * 78)
    print(f"      {'scale':<18} {'mu [GeV]':>12} {'sin^2':>9} {'alpha_em^-1':>12}  note")
    nearest = 1.0
    for r in rows:
        print(f"      {r.label:<18} {r.scale_gev:>12.3e} {r.sin2:>9.4f} "
              f"{r.aem_inv:>12.3f}  {r.note}")
        nearest = min(nearest, abs(r.sin2 - SIN2_CHO))
    print(f"      closest approach to sin^2=1/4 : {nearest:.4f}  (none within 0.01)")
    c_ok = nearest > 0.01
    print(f"      [{'CONFIRMED' if c_ok else 'no'}] every derived scale misses 1/4")
    ok = ok and c_ok
    print()

    # Theorems (stable arithmetic; assert so a genuine regression crashes).
    assert abs(a2_cho - 32.0 * PI / 3.0) < TOL          # 32 pi / 3
    assert abs(a1_cho - 96.0 * PI / 5.0) < TOL          # 96 pi / 5
    # round-trip: each implied scale reproduces its CHO target
    assert abs(inverse_coupling_at(a1_mz, B1, od["mu_alpha1"]) - a1_cho) < 1e-6
    assert abs(inverse_coupling_at(a2_mz, B2, od["mu_alpha2"]) - a2_cho) < 1e-6
    # the inverse-matched scale really gives sin^2 = 1/4
    assert abs(sin2_at_scale(mu_sin) - SIN2_CHO) < 1e-6
    # the over-determination is real (guards the honest negative finding)
    assert abs(math.log(od["mu_alpha2"] / od["mu_alpha1"])) > 1.0

    print("=" * 78)
    print("  VERDICT")
    print("=" * 78)
    print("  The electroweak matching scale is NOT derived. CHO's two algebraic")
    print("  boundaries (alpha_em^-1 = 128*pi/3 and sin^2 = 1/4) cannot both hold at")
    print(f"  one scale: one-loop running needs scales {od['ratio']:.1e} apart. The lone")
    print("  sin^2=1/4 inverse match sits at M_P/3^32.5 (non-integer), and no")
    print("  independently-derived CHO scale lands at 1/4. Per the kill rule in")
    print("  foundations/10_continuum_rg.md, S4/S5 stay OPEN -- now with a sharper,")
    print("  falsification-grade reason. No ledger row promoted; scoreboard untouched.")
    print()
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}   (audit explicit; THEOREM status: OPEN)")
    return ok


if __name__ == "__main__":
    main()
