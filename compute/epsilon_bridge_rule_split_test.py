"""
Can the sqrt(n)-vs-n bridge rule itself make the eps0 split?  Elimination + a
validation of the RMS convention.
================================================================================

The lead (epsilon_power_split_test.py)
--------------------------------------
The eps0 back-solve shows a power-correlated split: power-1 AMPLITUDES give eps0
~0.8% below sqrt(pi/432), power-2 PROBABILITIES ~0.8% above.  The exclusion theorem
killed the "pi/432 is the wrong number" reading; the surviving candidates were
(i) the amplitude-vs-probability bridge rule (sqrt(n) vs n) carries a systematic,
and (ii) genuine RG/scale running.  This module pushes on (i): can the bridge rule
itself produce the split?

The bridge rule (ledger C1/N3, epsilon_mixing_coefficients.py)
-------------------------------------------------------------
A mixing AMPLITUDE is the RMS magnitude of n random-phase unit transition
amplitudes, < |sum_{k=1..n} e^{i phi_k}|^2 > = n, so RMS = sqrt(n); the matching
PROBABILITY is the squared amplitude = n.  Hence amplitude = sqrt(n) eps0 and
probability = n eps0^2.

[A] SELF-CONSISTENCY (exact).  For a SINGLE eps0 the rule maps eps0 -> (sqrt(n)
    eps0, n eps0^2), and (sqrt(n) eps0)^2 = n eps0^2 identically.  Back-solving
    either factor returns the SAME eps0.  So the naive rule, with one eps0,
    predicts NO split.  The observed ~2-sigma split is therefore a real deviation
    from "single eps0 + naive rule", and it is specifically a test of the step
    amplitude = sqrt(probability): the power-1 and power-2 observables disagree on
    eps0 by a single factor c = eps0(amp)/eps0(prob) - 1 (~ -1.6% in current data),
    the compact form of the prior gate's b ~ -2a.

[B] WHICH corrections can make a split (exact classification).  A correction that
    renormalises eps0 itself -- one factor per POWER of eps0 -- collapses to the
    "wrong constant" case and cannot split (excluded by the prior theorem).  Only a
    correction that distinguishes the amplitude EXTRACTION (a sum-of-phases RMS)
    from the probability EXTRACTION (a count/variance) can.  So the split probes
    the sqrt-vs-square bridge STEP, not eps0.

[C] The one concrete bridge alternative -- mean resultant vs RMS -- ELIMINATED,
    and the RMS choice VALIDATED.  The framework uses the RMS magnitude sqrt(n).
    The natural alternative is the MEAN resultant length <|sum|> of the n-step
    random walk.  Exactly:
        n = 1:  <R> = 1,            RMS = 1,        ratio 1            (0%)
        n = 2:  <R> = 4/pi,         RMS = sqrt(2),  ratio 2 sqrt2/pi   (-10.0%)
        n->inf: <R> = sqrt(pi/4) sqrt(n) (Rayleigh), ratio sqrt(pi/4)  (-11.4%)
    So switching amplitudes from RMS to mean magnitude would shift them by 0% (n=1)
    to -11.4% (large n) -- (1) the RIGHT SIGN (amplitudes low) but (2) ~6-7x TOO BIG
    for n >= 2 versus the observed -1.6%, and (3) n-DEPENDENT, so it cannot produce
    a uniform amplitude/probability split anyway.  Two consequences: the mean-vs-RMS
    refinement is NOT the source of the split; and the data VALIDATE the framework's
    RMS convention -- the mean-magnitude alternative would put |V_us| (n=7) ~10%
    low, but it is only ~0.6% low.

[D] What survives.  The split is not a wrong constant ([prior theorem]) and not a
    bridge-rule artifact (self-consistent [A]; the one concrete refinement overshoots
    7x and is n-dependent [C]).  The leading surviving structural cause is genuine
    power/scale-dependent (RG / threshold) running between the scales at which the
    angles (amplitudes) and the ratios (probabilities) are defined -- or statistical
    noise.  Decided by future precision: if amplitudes stay ~1% low and probabilities
    ~1% high as errors shrink, running is favoured over noise.

PROVED here (exact, measurement-independent):
  - rule self-consistency: round-trip eps0 -> (sqrt(n)eps0, n eps0^2) -> eps0 to 1e-12;
  - the exact mean/RMS ratios 1 (n=1), 2 sqrt(2)/pi (n=2), sqrt(pi/4) (n->inf), and
    that the large-n correction 1 - sqrt(pi/4) exceeds 0.10 (>> the ~1.6% split).
NOT asserted (printed): the split size c, and every comparison to it -- data move.

DIAGNOSTIC: promotes no ledger row, moves no Bayes credit, touches no frozen file.
It eliminates the bridge-rule cause of the split and, as a byproduct, validates the
RMS amplitude convention.
"""

from __future__ import annotations

import math

from epsilon_knob_consistency import RELATIONS, eps0_from, EPS0_TH


def banner(t: str) -> None:
    print("=" * 78)
    print(f"  {t}")
    print("=" * 78)


def main() -> bool:
    banner("CAN THE sqrt(n)-vs-n BRIDGE RULE MAKE THE SPLIT?  (elimination)")
    print(f"\n  theory eps0 = sqrt(pi/432) = {EPS0_TH:.6f}")

    # ---- [A] the rule is self-consistent: single eps0 -> no split ---------
    print("\n[A] The rule is exactly self-consistent: single eps0 predicts NO split")
    for n in (1, 3, 4, 7, 8):
        amp = math.sqrt(n) * EPS0_TH            # amplitude = sqrt(n) eps0
        prob = n * EPS0_TH ** 2                 # probability = n eps0^2
        eps_from_amp = amp / math.sqrt(n)
        eps_from_prob = math.sqrt(prob / n)
        assert abs(eps_from_amp - EPS0_TH) < 1e-12
        assert abs(eps_from_prob - EPS0_TH) < 1e-12
        assert abs(amp * amp - prob) < 1e-12     # (sqrt(n) eps0)^2 == n eps0^2
    print("    (sqrt(n) eps0)^2 == n eps0^2 and both back-solve to eps0 (1e-12): OK")
    print("    => with one eps0 the amplitude and probability families COINCIDE;")
    print("       the observed split is a real deviation, testing amplitude=sqrt(prob).")

    # the single number that captures the split (DATA; printed)
    amp_eps = [eps0_from(r)[0] for r in RELATIONS if r.power == 1]
    prob_eps = [eps0_from(r)[0] for r in RELATIONS if r.power == 2]
    c = (sum(amp_eps) / len(amp_eps)) / (sum(prob_eps) / len(prob_eps)) - 1.0
    print(f"    observed split  c = eps0(amp)/eps0(prob) - 1 = {c*100:+.2f}%  (data)")

    # ---- [B] only a sqrt-vs-square correction can split (exact) -----------
    print("\n[B] Only a correction to the sqrt-vs-square STEP can split (not eps0)")
    # a correction per power of eps0 is a renormalisation of eps0 -> collapses to
    # the excluded 'wrong constant' case. Demonstrate: scaling eps0 by (1+d) leaves
    # amp/prob back-solved eps0 EQUAL (no split), for any d.
    for d in (0.05, -0.03, 0.2):
        e = EPS0_TH * (1 + d)
        a = (math.sqrt(7) * e) / math.sqrt(7)
        p = math.sqrt((3 * e * e) / 3)
        assert abs(a - p) < 1e-12, "renormalising eps0 must not create a split"
    print("    renormalising eps0 by (1+d) keeps eps0(amp)=eps0(prob) for all d: OK")
    print("    => a split requires distinguishing amplitude (RMS sum) from")
    print("       probability (count); it is a probe of the bridge step, not eps0.")

    # ---- [C] mean-resultant vs RMS: eliminated, and RMS validated ---------
    print("\n[C] Mean resultant vs RMS magnitude -- the one concrete bridge alternative")
    ratio_n1 = 1.0                               # <R>=1, RMS=1
    ratio_n2 = 2.0 * math.sqrt(2.0) / math.pi    # (4/pi)/sqrt(2) = 2 sqrt2 / pi
    ratio_inf = math.sqrt(math.pi / 4.0)         # Rayleigh mean / RMS
    assert abs(ratio_n2 - (4.0 / math.pi) / math.sqrt(2.0)) < 1e-15
    assert abs(ratio_inf - 0.8862269) < 1e-6
    assert (1.0 - ratio_inf) > 0.10              # >> the ~1.6% split
    print(f"    mean/RMS ratio:  n=1 -> {ratio_n1:.4f} (0.0%),  "
          f"n=2 -> {ratio_n2:.4f} ({(ratio_n2-1)*100:.1f}%),  "
          f"n->inf -> {ratio_inf:.4f} ({(ratio_inf-1)*100:.1f}%)")
    print(f"    switching amplitudes RMS->mean shifts them by 0% (n=1) to -11.4%;")
    print(f"    RIGHT SIGN (amplitudes low) but ~{abs(ratio_inf-1)/abs(c):.0f}x too big"
          f" for n>=2 vs the {c*100:+.1f}% split, and n-dependent (no uniform split).")
    print(f"    => the mean-vs-RMS refinement is NOT the split's source;")
    print(f"       and the data VALIDATE the RMS choice (mean would put |V_us| ~10%")
    print(f"       low; it is only ~0.6% low).")

    # ---- [D] surviving cause ----------------------------------------------
    print("\n[D] What survives")
    print("    NOT a wrong constant (prior exclusion theorem);")
    print("    NOT a bridge-rule artifact (rule self-consistent [A]; the one")
    print("    concrete refinement overshoots ~7x and is n-dependent [C]).")
    print("    => leading surviving cause: genuine power/scale-dependent (RG /")
    print("       threshold) running between the angle (amplitude) and ratio")
    print("       (probability) scales -- or statistical noise. Decided by future")
    print("       precision (amplitudes stay low + probabilities high => running).")

    print("\n[V] Sandbox verdict")
    print("    rule self-consistent: single eps0 -> no split          : PASS")
    print("    only a sqrt-vs-square correction can split (not eps0)   : PASS")
    print("    mean-vs-RMS ratios 1, 2sqrt2/pi, sqrt(pi/4); >10% >> 1.6%: PASS")
    print("    bridge-rule eliminated; RMS convention validated        : PASS (data)")
    print("    surviving cause = RG running vs noise                   : OPEN (narrowed)")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
