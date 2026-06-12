"""
Does a higher-order O(eps0^2) bridge correction explain the split?  No -- it deflates.
================================================================================

The lead (epsilon_rg_running_estimate.py [D])
---------------------------------------------
After RG running was disfavoured, the named "better lead" for the eps0 power-split
was a next-order O(eps0^2) BRIDGE correction -- specifically the sin-vs-angle /
half-angle refinement the framework already uses (|V_cb| via tan(pi/8)). The split
(~0.8-1.6%) is the right SIZE to be O(eps0^2) = pi/432 = 0.73%. This module
actually DERIVES that correction and TESTS it -- and reports an honest NEGATIVE:
the natural correction is the right size but does NOT clean up the split, so the
crack deflates toward noise rather than sharpening into a test.

The correction (exact trigonometry)
-----------------------------------
The framework's leading bridge reads a mixing AMPLITUDE as linear in its angle and
a PROBABILITY as the squared angle:

    amplitude     A = c * eps0           (c = sqrt7 for |V_us|, 1/2 for |V_cb|)
    probability   P = c * eps0^2         (c = 3, 4 for sin^2 th13, dm21/dm31)

But a transition amplitude is geometrically a SINE of an angle, not the bare angle
(this is exactly why the framework already uses sin(eps0/2) and tan(pi/8) for the
2-3 sector). The next-order reading is therefore

    amplitude     A = sin(theta),   theta = c * eps0           (mixing angles)
    probability   P = sin^2(theta), theta = sqrt(c) * eps0     (mixing probs)

so the framework's eps0 is recovered by INVERTING the sine:

    eps0(from A) = arcsin(A) / c           (was A/c)
    eps0(from P) = arcsin(sqrt P) / sqrt c (was sqrt(P/c))

This is a genuine, parameter-free O(eps0^2) correction (arcsin(x) = x + x^3/6+...),
the right size (~eps0^2/6 to ~c*eps0^2/6, i.e. 0.1-0.9%).

CRUCIAL SCOPE: the correction applies ONLY to the four genuine MIXING observables
(|V_us|, |V_cb|, sin^2 th13, dm21^2/dm31^2). The three charged-fermion MASS RATIOS
(m_c/m_t, m_s/m_b, m_mu/m_tau) are NOT sines of a mixing angle -- they are mass
ratios -- so no sin-correction applies to them, and (being same-sector) they are
1-loop RG-invariant too (mass_ratio_rg_audit.py). Yet they carry +0.5 to +1.2% of
the split. So whatever explains the split must NOT be the sin-correction for those.

What the test finds (DATA; printed, never asserted)
---------------------------------------------------
  * Right size: the sin-correction shifts each observable by ~0.3-0.9% -- O(eps0^2),
    as predicted.
  * But it does NOT tighten the back-solved eps0. The full 7-observable spread is
    2.23% (linear) vs 2.21% (sin) -- unchanged. Worse, the MIXING-ONLY spread
    GROWS from 1.73% to 2.21%: the correction pushes |V_us| from -0.59% to +0.27%
    (over-shooting through theory) while barely moving |V_cb| (still ~ -1.0%) and
    pushing the mixing PROBABILITIES further up (sin^2 th13 +0.49% -> +0.86%). It
    moves amplitudes and probabilities the SAME way (arcsin > linear for both), so
    it cannot close a gap in which amplitudes are low and probabilities are high.
  * The mass ratios (which take no correction) keep a ~0.5-1.2% spread on their own.

So the natural O(eps0^2) geometric correction is the right size but the WRONG shape:
it does not differentially raise amplitudes and lower probabilities, and it cannot
touch the mass ratios at all.

HONEST VERDICT -- the lead deflates
-----------------------------------
The power-split is NOT a single higher-order geometric correction. Combined with
the earlier exclusions (not a wrong pi/432; not the sqrt(n)-vs-n rule; not
dominantly RG), the residual is most consistent with (a) statistical noise -- the
whole split is only ~2 sigma -- plus possibly (b) a genuine ~1% imprecision in the
charged-fermion mass-ratio bridge factors (the Georgi-Jarlskog-type {1,3,8}), which
is a separate already-open obligation, not a knob correction. The "crack" therefore
does NOT become a sharp test; it deflates toward noise. The only thing that would
revive it as a test is ~3x better precision on |V_us| / the mixing angles AND the
open channel assignments being pinned so the correct trig reading is known.

This is a NEGATIVE result that closes the epsilon_rg_running_estimate [D] lead. It
is the honest outcome of actually doing the derivation rather than leaving it as a
hopeful pointer.

PROVED here (exact, measurement-independent):
  - the sin-correction is exact trigonometry: arcsin inverts the leading linear/
    square bridge, and the leading correction is O(eps0^2) of the stated size;
  - the correction is defined ONLY for mixing observables (mass ratios are not
    sines), verified by construction.
NOT asserted (printed): every back-solved eps0, every spread, and the verdict that
the correction fails to tighten -- all data.

DIAGNOSTIC: promotes no ledger row, moves no Bayes credit, touches no frozen file.
"""

from __future__ import annotations

import math

EPS0 = math.sqrt(math.pi / 432.0)


# (name, kind, leading coefficient c, power, value, sigma|None)
#   mixing amplitude:    A = c eps0     (sin reading: A = sin(c eps0))
#   mixing probability:  P = c eps0^2   (sin reading: P = sin^2(sqrt(c) eps0))
#   mass ratio:          M = c eps0^2   (NO sine: a mass ratio, not a mixing angle)
OBSERVABLES = [
    ("|V_us|",     "mix_amp",  math.sqrt(7.0), 1, 0.2243, 0.0005),
    ("|V_cb|",     "mix_amp",  0.5,            1, 0.0422, 0.0008),
    ("sin2_th13",  "mix_prob", 3.0,            2, 0.02203, 0.00056),
    ("dm21/dm31",  "mix_prob", 4.0,            2, 0.02950, 0.00086),
    ("m_c/m_t",    "mass",     1.0,            2, 1.27 / 172.76, None),
    ("m_s/m_b",    "mass",     3.0,            2, 0.0934 / 4.18, None),
    ("m_mu/m_tau", "mass",     8.0,            2, 0.10566 / 1.77700, None),
]


def eps0_linear(kind, c, power, value):
    return value / c if power == 1 else math.sqrt(value / c)


def eps0_sin(kind, c, power, value):
    if kind == "mix_amp":
        return math.asin(value) / c
    if kind == "mix_prob":
        return math.asin(math.sqrt(value)) / math.sqrt(c)
    return math.sqrt(value / c)        # mass ratio: not a sine, unchanged


def spread_pct(values):
    return (max(values) - min(values)) / EPS0 * 100.0


def banner(t):
    print("=" * 78)
    print(f"  {t}")
    print("=" * 78)


def main() -> bool:
    banner("DOES AN O(eps0^2) BRIDGE CORRECTION EXPLAIN THE SPLIT?  (no -- deflates)")
    print(f"\n  theory eps0 = sqrt(pi/432) = {EPS0:.6f}")

    # ---- [A] the sin-correction is exact trig of the right size ----------
    print("\n[A] The sin-vs-angle correction is exact O(eps0^2) trigonometry")
    # arcsin(x) - x = x^3/6 + 3x^5/40 + ...; verify the x^3/6 coefficient at a
    # genuinely small x (where higher terms are negligible), then report sizes.
    x_small = 1e-3
    lead = (math.asin(x_small) - x_small) / (x_small ** 3 / 6.0)
    assert abs(lead - 1.0) < 1e-4, "arcsin leading correction must be x^3/6"
    print(f"    arcsin(x) - x = x^3/6 + ...  (leading coefficient verified = "
          f"{lead:.5f} at x={x_small})")
    for x_label, x in (("eps0", EPS0), ("sqrt7 eps0", math.sqrt(7) * EPS0)):
        print(f"    arcsin({x_label}) - {x_label} = +{(math.asin(x)-x)/x*100:.2f}% "
              f"of {x_label}  (~ x^2/6)")
    print("    => correction size is O(eps0^2): ~0.12% per unit angle, up to ~0.85%")
    print("       for the sqrt7 |V_us| angle. The RIGHT SIZE for the ~1% split.")

    # ---- [B] but it only applies to MIXING observables -------------------
    print("\n[B] Scope: the correction exists ONLY for genuine mixing angles")
    n_mix = sum(1 for _, k, *_ in OBSERVABLES if k.startswith("mix"))
    n_mass = sum(1 for _, k, *_ in OBSERVABLES if k == "mass")
    assert n_mix == 4 and n_mass == 3
    print(f"    {n_mix} mixing observables (sines) + {n_mass} mass ratios (NOT sines).")
    print("    mass ratios are same-sector => 1-loop RG-invariant (mass_ratio_rg_audit)")
    print("    AND not sines => no geometric O(eps0^2) correction applies to them,")
    print("    yet they carry +0.5..+1.2% of the split.")

    # ---- [C] test: does the correction tighten the spread? (DATA) --------
    print("\n[C] Back-solved eps0: linear vs sin reading (DATA; printed, not asserted)")
    print("    observable    kind       linear dev   sin dev")
    lin_all, sin_all = [], []
    lin_mix, sin_mix = [], []
    mass_dev = []
    for name, kind, c, power, value, _ in OBSERVABLES:
        el = eps0_linear(kind, c, power, value)
        es = eps0_sin(kind, c, power, value)
        lin_all.append(el)
        sin_all.append(es)
        if kind.startswith("mix"):
            lin_mix.append(el)
            sin_mix.append(es)
        else:
            mass_dev.append((es / EPS0 - 1) * 100)
        print(f"    {name:11s}  {kind:9s}  {(el/EPS0-1)*100:+6.2f}%     "
              f"{(es/EPS0-1)*100:+6.2f}%")

    full_lin, full_sin = spread_pct(lin_all), spread_pct(sin_all)
    mix_lin, mix_sin = spread_pct(lin_mix), spread_pct(sin_mix)
    print(f"\n    FULL spread (7 obs):    linear {full_lin:.2f}%  ->  sin {full_sin:.2f}%")
    print(f"    MIXING-ONLY spread (4): linear {mix_lin:.2f}%  ->  sin {mix_sin:.2f}%")
    print(f"    mass-only spread (3, uncorrectable): "
          f"{max(mass_dev)-min(mass_dev):.2f}%")
    # the honest finding: the correction does NOT tighten (it loosens mixing)
    print("    => the sin-correction does NOT tighten the split; it LOOSENS the")
    print("       mixing-only spread (it raises amplitudes AND probabilities together,")
    print("       so it cannot close an amplitude-low / probability-high gap).")

    # ---- [D] verdict: the lead deflates ----------------------------------
    print("\n[D] Verdict -- the higher-order lead deflates toward noise")
    print("    The natural O(eps0^2) geometric correction is the right SIZE but the")
    print("    WRONG SHAPE, and cannot touch the mass ratios that carry much of the")
    print("    split. With wrong-pi/432, the sqrt(n)-vs-n rule, and RG already")
    print("    excluded/disfavoured, the ~2 sigma split is most consistent with:")
    print("      (a) statistical noise (the whole effect is only ~2 sigma), plus")
    print("      (b) a possible ~1% imprecision in the mass-ratio bridge factors")
    print("          {1,3,8} (a separate already-open obligation, not a knob fix).")
    print("    Revival as a sharp TEST needs ~3x better mixing-angle precision AND")
    print("    the open channel assignments pinned (to fix the correct trig reading).")

    print("\n[V] Sandbox verdict")
    print("    sin-correction is exact O(eps0^2) trig of the right size : PASS")
    print("    correction applies to mixing only, not mass ratios       : PASS")
    print("    correction does NOT tighten the split (loosens mixing)   : REPORTED (data)")
    print("    power-split deflates toward noise + mass-bridge imprecision: REPORTED")
    print("    closes the epsilon_rg_running_estimate [D] 'better lead'  : (negative result)")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
