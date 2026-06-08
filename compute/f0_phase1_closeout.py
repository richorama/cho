"""
PHASE 1 CLOSEOUT — the make-or-break gate is fully executed; both decisive
routes converge on ONE missing object: a dynamical seed-selection action.
=============================================================================

Why this module exists
----------------------
The gold-standard roadmap (ROBUSTNESS_ACTIONS.md) framed PHASE 1 as a single
binary gate: assemble the finite Connes spectral triple (A, H, D) and its
spectral action, and ask whether the CHO numbers are OUTPUTS. Phase 1 is now
fully executed:

  1.1 f0_spectral_triple_gate     — the naive triple has two obstructions.
  1.2 f0_real_structure_gate      — sharpen them into a real-structure dichotomy,
      f0_associative_triple_gate    rebuild the associative KO-6 skeleton, and
      f0_octonionic_yukawa_gate     slot the octonionic Yukawa L_X in (ungraded,
                                    no doubling) -- but the axioms do NOT pin it.
  1.3 f0_spectral_action_heatkernel — the DECISIVE prefactor test: is pi/432 the
                                    heat-kernel a4/a2 ratio?  REFUTED.
  1.4 spectral_action_432         — the ratio test: does the L_X spectrum give the
                                    mass hierarchy?  PARTIAL (structure forced,
                                    absolute seed open).

This module is the CLOSEOUT. It is NOT another invariance witness (the roadmap
explicitly warns that ~24 of those is past diminishing returns). It is the
opposite: it consolidates the two INDEPENDENT decisive results of Phase 1 into a
single falsifiable statement of where the program stands, by importing the two
source-of-truth numbers and recording their convergence.

The two independent decisive routes (and what each found)
---------------------------------------------------------
A finite spectral triple could secure the CHO content in exactly two ways: as a
PREFACTOR (the geometric constant eps0^2 = pi/432) or as a SPECTRUM (the mass
RATIOS). Phase 1 tested BOTH, and they are genuinely independent (one is a single
transcendental constant, the other is a set of multiplicative ratios):

  [A] PREFACTOR ROUTE (Phase 1.3, f0_spectral_action_heatkernel). For the finite
      triple the Seeley-DeWitt coefficients ARE the spectral moments a0=Tr(1),
      a2=Tr(D^2), a4=Tr(D^4). The dimensionless a4/a2 = M4/M2^2 = 0.00582895 is a
      pi-FREE rational (M2=2324/25, M4=31482/625), so it can never equal the
      transcendental pi/432 = 0.00727221. The only pi a spectral action emits is
      the continuum (4 pi)^(-d/2). => pi/432 is NOT a spectral-action output; it
      is Berry/Schur geometric. The dynamical earn-path for the prefactor is CLOSED.

  [B] RATIO ROUTE (Phase 1.4, spectral_action_432). The octonionic Jordan L_X
      forces the averaging law {a,b,c} u {(a+b)/2,(b+c)/2,(c+a)/2} (constants_out
      = 3, the mixing level = arithmetic mean of two generation levels) but the
      best single-knob eps0 ladder MISSES the measured charged-lepton hierarchy by
      1.40 decades. => the spectrum forces the STRUCTURE but not the absolute
      generation profile; the open problem localises to ONE scalar seed function.

The convergence (the actual closeout result)
--------------------------------------------
Both routes, though independent, localise the ENTIRE remaining F0 gap to the SAME
single missing object: a DYNAMICAL / VARIATIONAL principle (an ACTION) that would
have to (i) PRODUCE pi/432 as a spectral-action output -- refuted, the algebra's
spectral action does not -- and (ii) SELECT the three diagonal seed eigenvalues --
the lone open scalar function, which the algebra + symmetry + triple do NOT supply.
That missing object is exactly gold-standard criterion 1 (action -> EoM -> vacuum
-> spectrum), which the scorecard lists ABSENT. foundations/02_action.md is a
candidate, not a derivation.

The honest fork outcome (bounded, moves no credit)
--------------------------------------------------
Per the roadmap's binary fork, Phase 1's decisive experiment landed on the KILL
side for the DYNAMICAL route -- but bounded: F0 stays GEOMETRIC/open. The
Berry/Schur pi/432 reading SURVIVES (not demoted), the mass STRUCTURE (averaging
law, the (0,2,4) seesaw skeleton, the GJ {1,3,8} prefactors) is derived, but
neither pi/432 nor the absolute hierarchy is promotable to DERIVED without the
missing action. No Bayes credit moves; the scoreboard ladder
(-21.3 / -3.2 / +5.6 / +36.2) and the frozen registry are untouched. PHASE 2 (one
operator -> masses + CKM + PMNS) is GATED on this same dynamical seed selection.
Standing position: the standalone math (PAPER_JORDAN_THEOREMS.md) + the honest null.

No scipy. Reuses the two Phase-1 source modules (f0_spectral_action_heatkernel,
spectral_action_432) as the single source of truth for the two decisive numbers.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_phase1_closeout.py
"""

import numpy as np

from f0_spectral_action_heatkernel import (
    finite_octonionic_dirac,
    heat_kernel_moments,
)
from spectral_action_432 import ladder_mismatch


PI = np.pi
TARGET = PI / 432.0                       # eps0^2 = pi/432, the F0 constant
PREFACTOR_TOL = 1.0e-3                    # a4/a2 must clear pi/432 by this margin
RATIO_TOL_DECADES = 0.30                  # < 2x on every ratio would be a match


# --------------------------------------------------------------------------
def prefactor_route():
    """Phase 1.3 number: is the heat-kernel a4/a2 of the genuine D equal to pi/432?

    Returns (a4_over_a2, gap, closed) where closed=True means the spectral action
    does NOT emit pi/432 (the dynamical prefactor earn-path is closed)."""
    D = finite_octonionic_dirac()
    _M0, M2, M4, _M6 = heat_kernel_moments(D)
    a4_over_a2 = M4 / M2 ** 2
    gap = abs(a4_over_a2 - TARGET)
    return a4_over_a2, M2, M4, gap, gap > PREFACTOR_TOL


def ratio_route():
    """Phase 1.4 number: does the L_X spectrum's best one-knob ladder reproduce
    the measured lepton hierarchy?

    Returns (best_name, worst_log10_miss, open_) where open_=True means the
    spectrum does NOT give the absolute hierarchy (one seed function stays open)."""
    best, results, _meas = ladder_mismatch()
    miss = float(results[best]["worst_log10_miss"])
    return best, miss, miss > RATIO_TOL_DECADES


# --------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("PHASE 1 CLOSEOUT: the make-or-break gate is executed; where it leaves F0")
    print("=" * 78)

    # ---- [A] prefactor route (Phase 1.3) --------------------------------
    a4a2, M2, M4, pre_gap, pre_closed = prefactor_route()
    print("\n[A] PREFACTOR ROUTE (Phase 1.3, heat-kernel a4/a2 of the genuine D)")
    print(f"    a2 = Tr(D^2) = {M2:.6f} (=2324/25) , a4 = Tr(D^4) = {M4:.6f} (=31482/625)")
    print(f"    a4/a2 = M4/M2^2 = {a4a2:.8f}  vs  pi/432 = {TARGET:.8f}")
    print(f"    gap = {pre_gap:.8f}  ->  pi/432 is NOT a spectral-action output: {pre_closed}")
    print("    (a4/a2 is a pi-free rational; the only spectral pi is (4 pi)^(-d/2))")

    # ---- [B] ratio route (Phase 1.4) ------------------------------------
    best, miss, ratio_open = ratio_route()
    print("\n[B] RATIO ROUTE (Phase 1.4, L_X averaging-law spectrum vs the hierarchy)")
    print(f"    best single-knob eps0 ladder: {best}")
    print(f"    worst-case miss vs measured lepton ratios = {miss:.2f} decades")
    print(f"    spectrum does NOT give the absolute hierarchy: {ratio_open}")
    print("    (the averaging-law STRUCTURE is forced; the seed profile is open)")

    # ---- [C] the convergence --------------------------------------------
    both_need_action = pre_closed and ratio_open
    print("\n[C] CONVERGENCE — two independent routes, one missing object")
    print("    PREFACTOR (a single transcendental constant pi/432) and RATIOS (a set")
    print("    of multiplicative mass ratios) are independent tests, yet BOTH localise")
    print("    the entire remaining F0 gap to the SAME missing object:")
    print("    a DYNAMICAL/VARIATIONAL action that would have to (i) produce pi/432 as")
    print("    a spectral-action output [refuted] AND (ii) select the three diagonal")
    print("    seed eigenvalues [the lone open scalar function]. The algebra + symmetry")
    print("    + spectral triple supply NEITHER => gold-standard criterion 1 is ABSENT.")
    print(f"    both routes localise to the missing action: {both_need_action}")

    # ---- [D] the honest fork outcome ------------------------------------
    print("\n[D] FORK OUTCOME (bounded; moves no credit)")
    print("    Phase 1's decisive experiment landed on the KILL side for the DYNAMICAL")
    print("    route -- bounded: F0 stays GEOMETRIC/open. The Berry/Schur pi/432 reading")
    print("    SURVIVES (not demoted); the mass STRUCTURE (averaging law, (0,2,4)")
    print("    skeleton, GJ {1,3,8}) is derived; but neither pi/432 nor the absolute")
    print("    hierarchy is promotable to DERIVED without the missing action.")
    print("    No Bayes credit moves; the scoreboard ladder (-21.3 / -3.2 / +5.6 /")
    print("    +36.2) and the frozen registry are untouched. PHASE 2 (one operator ->")
    print("    masses+CKM+PMNS) is GATED on this same dynamical seed selection.")

    # ---- verdict --------------------------------------------------------
    print("\n[V] VERDICT  (the Phase 1 closeout, stated plainly)")
    print("    Phase 1 is fully executed. Its two independent decisive routes agree:")
    print("    the lone bottleneck is the ABSENT dynamical action. Standing position --")
    print("    the standalone math (PAPER_JORDAN_THEOREMS.md) + the honest null -- until")
    print("    and unless that action is derived. This gate is a consolidation: it")
    print("    closes the invariance-witness phase and moves NO credit.")
    print("=" * 78)

    # ---- stable assertions (audit.py ignores the return value) ----------
    # [A] the Phase-1.3 prefactor number, re-derived from the genuine D:
    assert abs(M2 - 92.96) < 1e-6, "a2=Tr(D^2) drifted from the Phase-1.3 value"
    assert abs(M4 - 50.3712) < 1e-6, "a4=Tr(D^4) drifted from the Phase-1.3 value"
    assert pre_closed, "a4/a2 came out at pi/432 (Phase 1.3 would have CONFIRMED!)"
    assert pre_gap > PREFACTOR_TOL, "prefactor route not bounded away from pi/432"
    # [B] the Phase-1.4 ratio number, from the source-of-truth module:
    assert ratio_open, "a single-knob ladder unexpectedly reproduced the hierarchy"
    assert miss > 1.0, "the ladder miss is not at least a full decade"
    # [C] the convergence: both independent routes need the same missing action:
    assert both_need_action, "the two routes did not converge on the missing action"
    # honesty guard: this gate computes only a consolidation, not a new number.
    assert TARGET not in (a4a2,), "pi/432 must not equal the computed a4/a2"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
