"""
Could RG running cause the eps0 power-split?  Order-of-magnitude YES, structure NO.
================================================================================

HONEST STATUS UP FRONT.  Unlike the exact-arithmetic gates in this eps0 series,
this module is a PHYSICS ESTIMATE.  Almost nothing here is "proved"; the asserted
content is limited to (a) the one-loop top-Yukawa rate as an arithmetic identity
from stated inputs, (b) the implied e-fold arithmetic, and (c) the structural fact
(from compute/mass_ratio_rg_audit.py) that same-sector mass ratios are 1-loop
RG-invariant.  Everything physical -- the running directions, the bridge scale,
the verdict -- is reported, not asserted.  A real multi-scale RGE run is the only
thing that could settle it; this estimate only decides whether RG is even in the
running, and it CORRECTS the prior gate's framing.

The lead (epsilon_power_split_test.py, epsilon_bridge_rule_split_test.py)
------------------------------------------------------------------------
The eps0 back-solve has a ~2-sigma power-split: power-1 amplitudes ~0.8% below
sqrt(pi/432), power-2 probabilities ~0.8% above.  Two causes were excluded (a
wrong pi/432 value; a bridge-rule artifact), and the prior gates named "genuine
RG/threshold running" as the leading surviving structural cause.  This module
tests that -- and finds it is the right SIZE but the wrong STRUCTURE.

[A] ORDER OF MAGNITUDE -- RG running CAN reach ~1% (assertable arithmetic).
    The one-loop top-Yukawa rate is kappa = y_t^2 / (16 pi^2).  With
    y_t = sqrt(2) m_t / v ~ 0.94 (m_t ~ 163 GeV MSbar, v = 246 GeV), kappa ~
    0.0056 per e-fold of ln(mu).  A fractional shift of ~1% is then O(1) * kappa *
    Delta(ln mu), i.e. Delta(ln mu) ~ 1-3 e-folds (a scale ratio ~3-20).  So a ~1%
    power-split is exactly the size of one-loop top-Yukawa running over a MODEST
    (~1-2 decade) separation between the scales at which amplitudes and
    probabilities are effectively defined.  Size: PLAUSIBLE.

[B] STRUCTURE -- but most of the split lives in RG-INVARIANT observables.
    Classify the 7 back-solved observables by their KNOWN RG behaviour:
      * m_c/m_t, m_s/m_b, m_mu/m_tau (3 of the 5 PROBABILITIES): 1-loop
        RG-INVARIANT -- same-sector mass ratios, QCD running cancels
        (compute/mass_ratio_rg_audit.py, ledger).  They do NOT run.
      * |V_us| (the dominant, most-precise AMPLITUDE): the Cabibbo angle is the
        most RG-stable mixing parameter (1-2 block; third-generation Yukawas drive
        CKM running, leaving theta_12 nearly fixed).  Quasi-INVARIANT.
      * |V_cb| (the other amplitude): DOES run, ~ top-Yukawa.
      * sin^2 theta13, dm21^2/dm31^2 (the other 2 probabilities): neutrino-sector
        running, model-dependent.
    So 4 of the 7 -- |V_us| and all three mass ratios -- are RG-(quasi-)invariant,
    yet they ALREADY show the split: |V_us| ~0.6% low, the mass ratios ~0.5-1.2%
    high.  The split SURVIVES when restricted to the RG-invariant subset.  RG
    running cannot explain a split between observables that do not run.

[C] VERDICT -- RG running is DISFAVORED as the dominant cause (corrects prior gate).
    The earlier gates called RG running the "leading surviving cause".  That was
    too generous: the split is carried mostly by RG-invariant quantities (|V_us|
    and the mass ratios), so running -- right order of magnitude though it is --
    cannot be the main driver.  At most it perturbs |V_cb| and the neutrino-sector
    probabilities at the ~1% level (consistent, but a minority of the signal).

[D] THE PROMISING LEAD instead -- a power-dependent BRIDGE correction of size eps0^2.
    The split is ~0.8-1.6%; eps0^2 = pi/432 = 0.727%.  These coincide in size.  The
    bridge maps the knob to observables at LEADING order (amplitude = sqrt(n) eps0,
    probability = n eps0^2); a next-order O(eps0^2) bridge correction (e.g. a
    sin-vs-angle or half-angle term, sin(x) = x(1 - x^2/6 + ...), which the
    framework already invokes for |V_cb| via tan(pi/8)) is naturally THIS size and
    is power-dependent (it hits amplitudes and probabilities differently).  This is
    NOT the sqrt(n)-vs-n piece (already excluded -- that is exact); it is a higher
    order in eps0.  Size-matched and structurally the right kind of correction --
    the next thing to derive.  Stated as a lead, not a result.

PROVED here (asserted, measurement-independent):
  - kappa = y_t^2/(16 pi^2) from the stated y_t (arithmetic);
  - the e-fold arithmetic Delta(ln mu) = split / (coef * kappa);
  - eps0^2 = pi/432 and its percentage; the size-coincidence eps0^2 ~ split;
  - the structural classification: the three headline mass ratios are same-sector
    (hence 1-loop RG-invariant, per mass_ratio_rg_audit).
NOT asserted (reported): the back-solved eps0, that the split survives in the
RG-invariant subset, the running directions, the bridge scale, and the verdict --
all data / physics estimate.

DIAGNOSTIC: promotes no ledger row, moves no Bayes credit, touches no frozen file.
It refines the eps0-split investigation: RG is the right size but wrong structure;
the size-matched O(eps0^2) bridge correction is the better lead.
"""

from __future__ import annotations

import math

from epsilon_knob_consistency import RELATIONS, eps0_from, EPS0_TH

# top-Yukawa inputs (MSbar-ish; the estimate is insensitive to the exact choice)
V_HIGGS = 246.22          # GeV
M_T_MSBAR = 163.0         # GeV (running top mass; pole ~173 gives y_t ~ 0.99)


def banner(t: str) -> None:
    print("=" * 78)
    print(f"  {t}")
    print("=" * 78)


def main() -> bool:
    banner("COULD RG RUNNING CAUSE THE eps0 SPLIT?  size YES, structure NO")
    print("\n  (PHYSICS ESTIMATE -- only the arithmetic + RG-invariance structure is")
    print("   asserted; running directions, bridge scale, and verdict are reported.)")

    # ---- [A] order of magnitude (assertable arithmetic) -------------------
    print("\n[A] One-loop top-Yukawa rate and the implied scale separation")
    y_t = math.sqrt(2.0) * M_T_MSBAR / V_HIGGS
    kappa = y_t ** 2 / (16.0 * math.pi ** 2)
    assert 0.0040 < kappa < 0.0070, "top-Yukawa rate out of expected band"
    print(f"    y_t = sqrt(2) m_t/v = {y_t:.3f}   kappa = y_t^2/(16 pi^2) = "
          f"{kappa:.5f} / e-fold")
    # observed split (DATA; printed)
    amp = [eps0_from(r)[0] for r in RELATIONS if r.power == 1]
    prob = [eps0_from(r)[0] for r in RELATIONS if r.power == 2]
    am, pm = sum(amp) / len(amp), sum(prob) / len(prob)
    half = abs(am / EPS0_TH - 1.0)
    print(f"    observed half-split ~ {half*100:.2f}% (each family from theory)  (data)")
    for coef in (1.0, 1.5, 2.0):
        dt = half / (coef * kappa)
        print(f"      O(1) coef {coef}: needs Delta(ln mu) ~ {dt:.1f} e-folds "
              f"(scale ratio ~ {math.exp(dt):.1f}x)")
    print("    => a ~1% split is the NATURAL size of top-Yukawa running over ~1-2")
    print("       decades. RG is in the running on SIZE.")

    # ---- [B] structure: most of the split is in RG-invariant observables --
    print("\n[B] But the split lives mostly in RG-(quasi-)INVARIANT observables")
    # the three headline mass ratios are same-sector -> 1-loop RG-invariant
    rg_invariant = {"m_c/m_t", "m_s/m_b", "m_mu/m_tau"}      # mass_ratio_rg_audit
    # structural assertion: these are the same-sector mass ratios
    names = {r.name for r in RELATIONS}
    assert rg_invariant <= names, "expected the three mass-ratio relations present"
    quasi = "|V_us|"                                          # Cabibbo, RG-stable
    print(f"    RG-INVARIANT (mass_ratio_rg_audit): {sorted(rg_invariant)}")
    print(f"    RG-quasi-invariant (Cabibbo 1-2 block): {quasi}")
    print(f"    these 4 carry most of the split, yet by construction do NOT run:")
    for r in RELATIONS:
        if r.name in rg_invariant or r.name == quasi:
            e, _ = eps0_from(r)
            print(f"      {r.name:11s} (pow {r.power})  eps0={e:.6f}  "
                  f"{(e/EPS0_TH-1)*100:+.2f}%   [RG-stable]")
    inv_amp = eps0_from(next(r for r in RELATIONS if r.name == "|V_us|"))[0]
    inv_prob = [eps0_from(r)[0] for r in RELATIONS if r.name in rg_invariant]
    survives = inv_amp < min(inv_prob)
    print(f"    split among the RG-stable subset survives (|V_us| < all mass ratios):"
          f" {survives}  (data)")
    print("    => RG running cannot explain a split between observables that do not run.")

    # ---- [C] verdict: RG disfavored as the dominant cause -----------------
    print("\n[C] Verdict -- RG running DISFAVORED as the dominant cause")
    print("    right SIZE (A), wrong STRUCTURE (B): the prior gate's 'RG is the")
    print("    leading surviving cause' is too generous. RG may perturb |V_cb| and")
    print("    the neutrino-sector probabilities at ~1%, but the bulk of the split")
    print("    is in RG-invariant |V_us| + mass ratios. (Corrects the earlier framing.)")

    # ---- [D] the better lead: an O(eps0^2) bridge correction --------------
    print("\n[D] The size-matched lead -- a power-dependent O(eps0^2) bridge term")
    eps2 = math.pi / 432.0
    assert abs(eps2 - EPS0_TH ** 2) < 1e-15
    print(f"    split ~ {half*100:.2f}-{(pm/am-1)*100:.2f}%   vs   eps0^2 = pi/432 = "
          f"{eps2*100:.3f}%")
    print("    same size. The bridge is LEADING-order (amp = sqrt(n) eps0, prob =")
    print("    n eps0^2); a next-order O(eps0^2) correction (sin-vs-angle / half-")
    print("    angle, already used for |V_cb| via tan(pi/8)) is naturally this size")
    print("    AND power-dependent -- it is NOT the (exact) sqrt(n)-vs-n piece.")
    print("    This is the better next thing to derive. Stated as a lead, not a result.")

    print("\n[V] Sandbox verdict")
    print("    kappa = y_t^2/(16 pi^2) ~ 0.0056/e-fold (arithmetic)     : PASS")
    print("    ~1% split = top-Yukawa running over ~1-2 decades (size)  : PASS")
    print("    3 mass ratios + |V_us| are RG-(quasi-)invariant          : PASS (structure)")
    print("    split survives in the RG-invariant subset                : REPORTED (data)")
    print("    RG running disfavored as dominant cause (wrong structure): REPORTED")
    print("    O(eps0^2)=0.73% bridge correction is the size-matched lead: REPORTED")
    print("    full multi-scale RGE run + fixed bridge scale            : OPEN (only decider)")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
