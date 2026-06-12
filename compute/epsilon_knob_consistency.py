"""
Is the one knob really ONE knob?  Back-solve eps0 from every count relation.
================================================================================

The pivot (ledger C1/C2/N2/N3, M3; chi_squared.py, epsilon_free_*_*.py)
----------------------------------------------------------------------
The framework's whole flavour sector is supposed to run on a SINGLE number
eps0 = sqrt(pi/432) = 0.085277..., entering each observable as (count) times a
power of eps0:

    AMPLITUDES   (power 1):   |V_us| = sqrt(7) eps0      |V_cb| = (1/2) eps0
    PROBABILITIES(power 2):   sin^2 th13 = 3 eps0^2      dm21^2/dm31^2 = 4 eps0^2
                              m_c/m_t = 1 eps0^2         m_s/m_b = 3 eps0^2
                              m_mu/m_tau = 8 eps0^2

The cleanest possible test of "one knob" is therefore to INVERT each relation --
solve it for eps0 from the measured value and the (open) count -- and ask whether
all the back-solved eps0 agree with each other AND with the theory value
sqrt(pi/432).  This is stronger than any single ratio: if the one-knob story is
right, these seven numbers must coincide.

This module is the global consistency check.  It is the inverse direction of
chi_squared.py (which goes eps0 -> observable); the back-solve eps0 <- observable
view has not been isolated before, and it changes the conclusion of the previous
gate (epsilon_free_mass_mixing_bridge.py).

What the data say (PDG/NuFIT-class central values; PRINTED, never asserted)
---------------------------------------------------------------------------
The back-solved eps0 values fall into a clean POWER-CORRELATED pattern:

    AMPLITUDES (power 1):  eps0 ~ 0.0848 (|V_us|), 0.0844 (|V_cb|)  -> BELOW theory
    PROBABILITIES(power 2):eps0 ~ 0.0857-0.0863                     -> ABOVE theory
    theory sqrt(pi/432) = 0.08528                                    sits BETWEEN

So the residual is NOT a single bad count (the previous gate read |V_us| as "the
weak link"; that was too narrow).  It is a ~1.5% offset that correlates with the
POWER of eps0: the amplitude (power-1) relations want eps0 ~ 0.8% low, the
probability (power-2) relations want eps0 ~ 0.8% high.  No single rescaling of eps0
can remove it, because the two families move in opposite directions about theory.

Honest candidate causes (the data cannot distinguish them):
  (i)  the amplitude-vs-probability bridge rule (sqrt(n) for amplitudes vs n for
       probabilities, the C1/N3 "RMS of n random phases" argument) carries a
       ~1.5% systematic;
  (ii) genuine RG / threshold running between the scales at which CKM, PMNS, and
       charged-fermion masses are defined, absent from the tree-level bridges
       (cf. the B1/B2 bridge-sensitivity entries);
  (iii)the intrinsic noise of a one-knob fit that is only ~1-2% accurate.

The metric to read is the FRACTIONAL deviation of each eps0 from theory.  The
per-observable sigma-pull is reported too, but it mostly ranks observables by
EXPERIMENTAL precision: m_mu/m_tau is measured to ~1e-5, so its ~1% framework
offset shows up as a >100-sigma pull -- a statement about the precision of the
muon/tau masses, not a 100-sigma "falsification" of CHO.  The framework-relevant
number is the ~1% fractional spread.

PROVED here (exact arithmetic, asserted):
  - the back-solve inverts the forward relation exactly (synthetic round-trip:
    feed eps0_theory through count*eps0^p, recover eps0_theory);
  - the amplitude counts {sqrt(7), 1/2} and probability counts {1,3,4,8}, and the
    theory value eps0 = sqrt(pi/432).
These are independent of any measurement.

NOT asserted (reported only): every data-derived number -- the back-solved eps0,
the fractional deviations, the sigma-pulls, and the amplitude-below/probability-
above clustering -- because PDG/NuFIT central values move.  A predictions audit
reports tensions; it does not assert them.

This is a DIAGNOSTIC: it promotes no ledger row and moves no Bayes credit, and it
does not touch the frozen registry.  It refines (does not overturn) the prior
mass<->mixing gate's reading.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

EPS0_TH = math.sqrt(math.pi / 432.0)       # 0.085277...


@dataclass(frozen=True)
class Relation:
    name: str
    power: int            # 1 = amplitude, 2 = probability
    count: float          # the framework integer/root count
    value: float          # measured central value
    sigma: float          # measured 1-sigma


# Counts: open C1/C2 (amplitudes), N2/N3/M3 (probabilities). Data single-source-
# consistent with compute/chi_squared.py.
RELATIONS = (
    Relation("|V_us|",      1, math.sqrt(7.0), 0.2243, 0.0005),
    Relation("|V_cb|",      1, 0.5,            0.0422, 0.0008),
    Relation("sin^2(th13)", 2, 3.0,  0.02203, 0.00056),
    Relation("dm21^2/dm31^2", 2, 4.0, 0.02950, 0.00086),
    Relation("m_c/m_t",     2, 1.0,  1.27 / 172.76,
             (1.27 / 172.76) * math.hypot(0.02 / 1.27, 0.30 / 172.76)),
    Relation("m_s/m_b",     2, 3.0,  0.0934 / 4.18,
             (0.0934 / 4.18) * math.hypot(0.0008 / 0.0934, 0.03 / 4.18)),
    Relation("m_mu/m_tau",  2, 8.0,  0.10566 / 1.77700,
             (0.10566 / 1.77700) * math.hypot(0.00001 / 0.10566, 0.00024 / 1.77700)),
)


def eps0_from(rel: Relation) -> tuple[float, float]:
    """Back-solve eps0 and its 1-sigma from a single count relation."""
    if rel.power == 1:                      # value = count * eps0
        e = rel.value / rel.count
        se = rel.sigma / rel.count
    else:                                   # value = count * eps0^2
        e = math.sqrt(rel.value / rel.count)
        se = rel.sigma / (2.0 * math.sqrt(rel.count * rel.value))
    return e, se


def banner(t: str) -> None:
    print("=" * 78)
    print(f"  {t}")
    print("=" * 78)


def main() -> bool:
    banner("IS THE ONE KNOB ONE KNOB?  eps0 back-solved from every count relation")
    print(f"\n  theory   eps0 = sqrt(pi/432) = {EPS0_TH:.6f}")

    # ---- [A] the back-solve inverts the forward relation exactly ----------
    print("\n[A] Round-trip check: count * eps0_th^p -> back-solve -> eps0_th (exact)")
    for power, count in ((1, math.sqrt(7.0)), (2, 3.0)):
        synth = count * EPS0_TH ** power
        rec = (synth / count) if power == 1 else math.sqrt(synth / count)
        assert abs(rec - EPS0_TH) < 1e-15, "back-solve is not the exact inverse"
    print("    power-1 and power-2 inversions recover eps0_theory to 1e-15: OK")

    # counts are the framework's (open) assignments
    amp_counts = sorted({r.count for r in RELATIONS if r.power == 1})
    prob_counts = sorted({int(r.count) for r in RELATIONS if r.power == 2})
    assert prob_counts == [1, 3, 4, 8], "probability counts must be {1,3,4,8}"
    assert abs(amp_counts[0] - 0.5) < 1e-15 and abs(amp_counts[1] - math.sqrt(7)) < 1e-12
    print(f"    amplitude counts {{1/2, sqrt7}}, probability counts {{1,3,4,8}}: OK")

    # ---- [B] back-solve eps0 from each measured observable (printed) -------
    print("\n[B] Back-solved eps0 (DATA; printed, never asserted)")
    print("    relation        pow  count   eps0      frac.dev   sigma-pull")
    rows = []
    for r in RELATIONS:
        e, se = eps0_from(r)
        frac = (e - EPS0_TH) / EPS0_TH
        z = (e - EPS0_TH) / se
        rows.append((r, e, se, frac, z))
        cnt = f"{r.count:.4f}" if r.power == 1 else f"{int(r.count)}"
        print(f"    {r.name:14s} {r.power}   {cnt:>6}  {e:.6f}  {frac*100:+6.2f}%  "
              f"{z:+8.2f}")
    print("    (sigma-pull mostly ranks by EXPERIMENTAL precision -- e.g. m_mu/m_tau")
    print("     known to ~1e-5, so its ~1% offset reads as a huge pull; the")
    print("     framework-relevant metric is the ~1% fractional deviation.)")

    # ---- [C] the power-correlated clustering (printed) --------------------
    print("\n[C] Amplitude (power 1) vs probability (power 2) clustering (DATA)")
    amp = [fr for (r, _, _, fr, _) in rows if r.power == 1]
    prob = [fr for (r, _, _, fr, _) in rows if r.power == 2]
    amp_mean = sum(amp) / len(amp)
    prob_mean = sum(prob) / len(prob)
    all_eps = [e for (_, e, _, _, _) in rows]
    spread = (max(all_eps) - min(all_eps)) / EPS0_TH
    print(f"    amplitude  mean frac.dev = {amp_mean*100:+.2f}%  (eps0 BELOW theory)")
    print(f"    probability mean frac.dev = {prob_mean*100:+.2f}%  (eps0 ABOVE theory)")
    print(f"    full spread of back-solved eps0 = {spread*100:.2f}% of eps0_theory")
    print(f"    theory sits BETWEEN the two clusters: amplitudes low, probabilities high.")

    # ---- [D] honest reading -----------------------------------------------
    print("\n[D] Honest reading -- refines the prior 'weak link' diagnosis")
    print("    The previous gate (epsilon_free_mass_mixing_bridge) read |V_us| as the")
    print("    single weak link. This global view shows it is NOT one bad count: the")
    print("    WHOLE amplitude (power-1) side runs ~1% low and the WHOLE probability")
    print("    (power-2) side ~1% high, so the residual correlates with the POWER of")
    print("    eps0, not with one observable. No single eps0 rescaling fixes it (the")
    print("    two families straddle theory). Candidate causes (data cannot separate):")
    print("      (i)  the amplitude-vs-probability bridge rule (sqrt(n) vs n) carries")
    print("           a ~1.5% systematic;")
    print("      (ii) RG/threshold running between CKM, PMNS, mass scales (not in the")
    print("           tree-level bridges; cf. B1/B2 bridge sensitivities);")
    print("      (iii)the intrinsic ~1-2% noise of a one-knob fit.")
    print("    Falsifiable handle: if future data keep amplitudes low and")
    print("    probabilities high as errors shrink, (i)/(ii) -- a real power-")
    print("    dependent correction -- is favoured over (iii).")

    print("\n[V] Sandbox verdict")
    print("    back-solve inverts the forward relation exactly        : PASS")
    print("    counts {1/2,sqrt7} (amp), {1,3,4,8} (prob); eps0=sqrt(pi/432): PASS")
    print("    back-solved eps0 span ~2%, centered near theory        : REPORTED (data)")
    print("    amplitudes BELOW / probabilities ABOVE theory          : REPORTED (data)")
    print("    cause (bridge rule vs RG vs one-knob noise)            : OPEN")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
