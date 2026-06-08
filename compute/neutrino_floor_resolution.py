"""
Item 4 -- resolve the neutrino-floor falsifier (honest theory-error budget).
============================================================================

Context (roadmap item 4, predict_neutrino_sum.floor_violation)
--------------------------------------------------------------
CHO identifies the heaviest neutrino with the tree-level seesaw

    m_nu3 = (y_nu3)^2 * v^2 / (2 * M_R),     y_nu3 = 1,   M_R = M_P / 3^9,

which evaluates to m_nu3 = 48.86 meV. The oscillation "floor" -- the smallest
value the heaviest normal-ordering mass can take, reached when the lightest
mass -> 0 -- is sqrt(Dm31^2) = 50.10 +/- 0.27 meV. The central value therefore
sits 1.24 meV BELOW the floor, and `predict_neutrino_sum.floor_violation()`
reports this as a 4.6 sigma deficit. Taken at face value that is a falsification.

The flaw in the 4.6 sigma framing
---------------------------------
The 4.6 sigma divides the 1.24 meV deficit by the EXPERIMENTAL error on the
floor alone (0.27 meV). It assigns ZERO theory error to m_nu3 -- but m_nu3 is a
TREE-LEVEL seesaw built from two inputs that CHO derives only up to an O(1)
normalization:

  (1) M_R = M_P / 3^9.  The exponent 9 is derived (N_R = 18 half-powers of 1/3);
      the O(1) prefactor is NOT.  Its SISTER on the same power-of-three ladder is
      M_W = M_P / 3^36, whose CHO value 81.35 GeV overshoots the measured
      80.377 GeV by +1.21%.  That +1.21% is the ladder's own normalization error.

  (2) y_nu3 = 1 (norm saturation).  This is the SAME assumption as the top
      Yukawa y_t = 1, which gives m_t = v/sqrt(2) = 174.10 GeV against the pole
      mass 172.76 GeV -- a +0.78% miss.  In the seesaw the Dirac coupling enters
      SQUARED, so this propagates as 2 * 0.78% = 1.56%.

Combining in quadrature, the tree-level theory error on m_nu3 is

    sigma_theory = sqrt( (2*0.78%)^2 + (1.21%)^2 ) ~= 1.97%  ->  +/- 0.96 meV,

i.e. m_nu3 = 48.9 +/- 1.0 meV.  Folding this with the floor's experimental error,
the deficit's significance is 1.24 / sqrt(0.27^2 + 0.96^2) = 1.2 sigma, NOT 4.6.

What this module does (and does NOT) claim
-------------------------------------------
It does NOT fake a fix.  The central value still sits just below the physical
floor; that fact is printed plainly and asserted, not hidden.  What it shows is
that the "4.6 sigma falsification" conflates experimental precision with
tree-level theory error: once the row carries the error budget calibrated from
CHO's OWN sister rows (M_W, m_t), the deficit is a mild ~1.2 sigma undershoot --
consistent, not a clean kill.

DECISION (honest, two-sided):
  * N1 is DEMOTED.  It cannot be quoted as a ~2% precision prediction; its
    honest theory error (~1.0 meV) is comparable to the 1.24 meV gap.  Its
    evidential weight drops to "order-1 consistent within tree-level seesaw
    error; central value sits ~1 sigma below the physical floor."
  * The discriminating content that survives is the ORDERING (normal) and the
    BALLPARK sum, NOT a precise m_nu3.  The frozen Sum m_nu band (57-62 meV)
    already covers the minimal normal-ordering sum with m3 ON the floor
    (58.7 meV), so the locked forward prediction is unaffected.
  * LIVE OBLIGATION (identical to M_W / S1): DERIVE the O(1) seesaw normalization
    and the y_nu3 = 1 saturation.  Closing the gap needs only y_nu3 = 1.013 or
    M_R * 0.975 (a +0.023 shift in the exponent -- the integer 9 is untouched).
  * GENUINE KILL CONDITION: a pinned, DERIVED normalization that STILL leaves
    m_nu3 below the floor beyond the (then-shrunk) theory error.

A note on RG running (pre-empting an objection)
-----------------------------------------------
One might hope Weinberg-operator running from M_R to M_Z supplies the missing
+2.5%.  It does not, cleanly: read as a high-scale boundary condition the
running is large and WRONG-signed (the 6*y_t^2 term makes the coefficient grow,
SUPPRESSING m_nu and worsening the deficit); read as a low-scale effective
relation it is already absorbed.  The resolution deliberately does NOT lean on
it; it rests only on the tree-level normalization error the row must carry.

This module promotes no ledger row and does NOT touch the scoreboard or the
frozen prediction registry.  It imports the frozen constants read-only.

numpy-free.  Reuses predict_neutrino_sum (the frozen seesaw inputs).
"""

from __future__ import annotations

import math

from predict_neutrino_sum import (
    DM21_SQ,
    DM31_SQ,
    DM31_SQ_ERR,
    M_P,
    v,
    M_R,
    m_nu3_cho,
    floor_violation,
)

# ---------------------------------------------------------------------------
# Sister-row anchors (PDG central values; NOT frozen-registry constants).
# ---------------------------------------------------------------------------
M_W_OBS = 80.377        # GeV, measured W mass (PDG)
M_W_EXPONENT = 36       # M_W = M_P / 3^36 (sister of the seesaw on the same ladder)
SEESAW_EXPONENT = 9     # M_R = M_P / 3^9
M_T_POLE = 172.76       # GeV, top-quark pole mass (PDG)

TOL = 1e-9


# ---------------------------------------------------------------------------
# Sister-row calibration of the two tree-level inputs.
# ---------------------------------------------------------------------------
def sister_calibration() -> dict:
    """Fractional miss of each tree-level input's SISTER row.

    M_R normalization  <- M_W = M_P/3^36 (same power-of-three ladder).
    y_nu3 = 1 saturation <- y_t = 1 -> m_t = v/sqrt(2) (same norm assumption).
    """
    m_w_pred = M_P / 3.0**M_W_EXPONENT
    mw_err = (m_w_pred - M_W_OBS) / M_W_OBS

    m_t_pred = v / math.sqrt(2.0)
    mt_err = (m_t_pred - M_T_POLE) / M_T_POLE

    return {
        "m_w_pred": m_w_pred,
        "m_w_obs": M_W_OBS,
        "mw_err": mw_err,           # +1.21%
        "m_t_pred": m_t_pred,
        "m_t_pole": M_T_POLE,
        "mt_err": mt_err,           # +0.78%
    }


def tree_level_theory_error() -> dict:
    """Quadrature theory error on m_nu3 from its two O(1)-uncertain inputs.

    m_nu3 ~ y_nu3^2 / M_R: the Dirac coupling enters SQUARED (factor 2 on its
    fractional error), M_R linearly.
    """
    cal = sister_calibration()
    sigma_dirac = 2.0 * abs(cal["mt_err"])   # y^2 -> doubles the fractional miss
    sigma_mr = abs(cal["mw_err"])
    sigma_theory = math.sqrt(sigma_dirac**2 + sigma_mr**2)
    return {
        "sigma_dirac": sigma_dirac,
        "sigma_mr": sigma_mr,
        "sigma_theory": sigma_theory,        # ~1.97%
        "m_nu3_err_meV": sigma_theory * m_nu3_cho * 1e3,
    }


def significance_with_theory_error() -> dict:
    """Re-evaluate the floor deficit folding in the tree-level theory error."""
    fv = floor_violation()
    floor_meV = fv["floor_meV"]
    floor_err_meV = fv["floor_err_meV"]
    deficit_meV = fv["deficit_meV"]
    n_sigma_exp = fv["n_sigma"]

    theory = tree_level_theory_error()
    theory_err_meV = theory["m_nu3_err_meV"]
    total_err_meV = math.sqrt(floor_err_meV**2 + theory_err_meV**2)
    n_sigma_total = deficit_meV / total_err_meV

    return {
        "floor_meV": floor_meV,
        "floor_err_meV": floor_err_meV,
        "m_nu3_meV": m_nu3_cho * 1e3,
        "theory_err_meV": theory_err_meV,
        "deficit_meV": deficit_meV,
        "n_sigma_exp": n_sigma_exp,
        "total_err_meV": total_err_meV,
        "n_sigma_total": n_sigma_total,
    }


def normalization_to_reach_floor() -> dict:
    """The minimal input shift that lands the central value ON the floor."""
    floor_meV = math.sqrt(DM31_SQ) * 1e3
    ratio = floor_meV / (m_nu3_cho * 1e3)
    return {
        "y_nu3_to_floor": math.sqrt(ratio),         # 1.013
        "mr_factor_to_floor": 1.0 / ratio,          # 0.975
        "exponent_shift": math.log(1.0 / ratio) / math.log(3.0),  # +0.023
    }


def frozen_band_covers_floor() -> dict:
    """Minimal normal-ordering sum with m3 ON the floor, vs the frozen band."""
    m1 = 0.0
    m2 = math.sqrt(m1**2 + DM21_SQ)
    m3 = math.sqrt(DM31_SQ)
    minimal_sum_meV = (m1 + m2 + m3) * 1e3
    return {
        "minimal_sum_meV": minimal_sum_meV,         # 58.7
        "band_lo_meV": 57.0,
        "band_hi_meV": 62.0,
        "covered": 57.0 <= minimal_sum_meV <= 62.0,
    }


def main() -> bool:
    sig = significance_with_theory_error()
    cal = sister_calibration()
    theory = tree_level_theory_error()
    norm = normalization_to_reach_floor()
    band = frozen_band_covers_floor()
    ok = True

    print("=" * 78)
    print("  ITEM 4 -- NEUTRINO-FLOOR FALSIFIER: HONEST THEORY-ERROR BUDGET")
    print("=" * 78)

    print()
    print("  [A] The falsifier AS STATED (experimental error only)")
    print("  " + "-" * 60)
    print(f"      m_nu3 (CHO)   = {sig['m_nu3_meV']:.2f} meV")
    print(f"      floor         = {sig['floor_meV']:.2f} +/- {sig['floor_err_meV']:.2f} meV"
          f"   (sqrt(Dm31^2))")
    print(f"      deficit       = {sig['deficit_meV']:.2f} meV")
    print(f"      => {sig['n_sigma_exp']:.1f} sigma  -- looks like a clean kill")
    print("      ... but this assigns ZERO theory error to a TREE-LEVEL seesaw.")

    print()
    print("  [B] The two tree-level inputs, calibrated from their SISTER rows")
    print("  " + "-" * 60)
    print(f"      (1) M_R = M_P/3^{SEESAW_EXPONENT} normalization")
    print(f"          sister M_W = M_P/3^{M_W_EXPONENT} = {cal['m_w_pred']:.2f} GeV "
          f"vs {cal['m_w_obs']} -> {cal['mw_err']*100:+.2f}%")
    print(f"      (2) y_nu3 = 1 saturation (same as y_t = 1)")
    print(f"          m_t = v/sqrt(2) = {cal['m_t_pred']:.2f} GeV "
          f"vs pole {cal['m_t_pole']} -> {cal['mt_err']*100:+.2f}%")
    print(f"      m_nu3 ~ y^2 / M_R: Dirac error doubles "
          f"-> {theory['sigma_dirac']*100:.2f}%, M_R -> {theory['sigma_mr']*100:.2f}%")
    print(f"      sigma_theory(m_nu3) = {theory['sigma_theory']*100:.2f}% "
          f"= +/- {theory['m_nu3_err_meV']:.2f} meV")

    print()
    print("  [C] Re-evaluated significance (experiment (+) theory)")
    print("  " + "-" * 60)
    print(f"      m_nu3 = {sig['m_nu3_meV']:.2f} +/- {sig['theory_err_meV']:.2f} meV (theory)")
    print(f"      total error = sqrt({sig['floor_err_meV']:.2f}^2 + "
          f"{sig['theory_err_meV']:.2f}^2) = {sig['total_err_meV']:.2f} meV")
    print(f"      deficit significance = {sig['deficit_meV']:.2f} / "
          f"{sig['total_err_meV']:.2f} = {sig['n_sigma_total']:.1f} sigma")
    print(f"      => the 4.6 sigma 'falsification' is a {sig['n_sigma_total']:.1f} sigma "
          f"undershoot once the row carries its error.")

    print()
    print("  [D] DECISION -- demote, do not hide, do not fake")
    print("  " + "-" * 60)
    print("      * NOT a clean kill: 4.6 sigma over-weights experimental precision.")
    print("      * NOT a precision success either: theory error ~ the gap itself.")
    print("        N1 demoted to 'order-1 consistent within tree-level seesaw error'.")
    print(f"      * Central value sits {sig['deficit_meV']:.2f} meV BELOW the physical")
    print("        floor -- stated plainly, ~1 sigma low, not softened.")
    print(f"      * To reach the floor: y_nu3 = {norm['y_nu3_to_floor']:.4f}  OR  "
          f"M_R *= {norm['mr_factor_to_floor']:.4f}")
    print(f"        (exponent shift {norm['exponent_shift']:+.3f}; the integer "
          f"{SEESAW_EXPONENT} is untouched).")
    print("      * LIVE OBLIGATION: derive the O(1) seesaw normalization + y_nu3=1.")
    print("      * GENUINE KILL: a pinned DERIVED normalization still below floor.")

    print()
    print("  [E] Frozen forward prediction is unaffected")
    print("  " + "-" * 60)
    print(f"      minimal normal-ordering sum with m3 ON floor = "
          f"{band['minimal_sum_meV']:.1f} meV")
    print(f"      frozen band [{band['band_lo_meV']:.0f}, {band['band_hi_meV']:.0f}] meV "
          f"covers it: {band['covered']}")

    # ----- Theorems (stable arithmetic; assert so a regression crashes) -----
    # The central value really is below the floor (do NOT hide it; guards the
    # frozen seesaw value against silent retuning above the floor).
    assert sig["deficit_meV"] > 0.0
    # The naive experimental-only framing really is > 4 sigma.
    assert sig["n_sigma_exp"] > 4.0
    # Folding the sister-calibrated theory error, it drops below 2 sigma.
    assert sig["n_sigma_total"] < 2.0
    # The seesaw exponent 9 is robust: reaching the floor needs |shift| << 1.
    assert abs(norm["exponent_shift"]) < 0.1
    # Sister-row anchors reproduce their known misses (guards the calibration).
    assert abs(cal["mw_err"] - (M_P / 3.0**M_W_EXPONENT - M_W_OBS) / M_W_OBS) < TOL
    assert abs(cal["mt_err"] - (v / math.sqrt(2.0) - M_T_POLE) / M_T_POLE) < TOL
    # The frozen Sum m_nu band still covers the on-floor minimal sum.
    assert band["covered"]

    print()
    print("=" * 78)
    print("  VERDICT")
    print("=" * 78)
    print("  The neutrino floor does NOT falsify CHO at 4.6 sigma: that figure")
    print("  assigns zero theory error to a tree-level seesaw. Folding the error")
    print("  calibrated from CHO's own sister rows (M_W +1.2%, y_t=1 top +0.8%),")
    print(f"  m_nu3 = {sig['m_nu3_meV']:.1f} +/- {sig['theory_err_meV']:.1f} meV and the deficit"
          f" is {sig['n_sigma_total']:.1f} sigma -- consistent.")
    print("  But the central value sits just BELOW the physical floor, so N1 is")
    print("  DEMOTED from a precision claim to order-1 consistency; the live")
    print("  obligation is to DERIVE the O(1) seesaw normalization. No ledger row")
    print("  promoted; scoreboard and frozen registry untouched.")
    print()
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}   (audit explicit; N1 status: DEMOTED/OPEN)")
    return ok


if __name__ == "__main__":
    main()
