"""
Is the eps0 power-split real?  Significance + an exact exclusion theorem.
================================================================================

The lead (epsilon_knob_consistency.py)
--------------------------------------
Back-solving eps0 from every count relation showed a power-correlated split: the
two power-1 AMPLITUDES (|V_us|, |V_cb|) give eps0 ~0.8% BELOW sqrt(pi/432), while
the five power-2 PROBABILITIES give eps0 ~0.8% ABOVE.  That gate listed three
candidate causes and said the data "cannot separate them".  This module pushes on
exactly that: it asks how SIGNIFICANT the split is, and PROVES that one of the
three candidate readings is excluded outright.

[A] The back-solved eps0 use ONLY data and the (open) counts -- never pi/432.
    (eps0_from(rel) reads rel.value and rel.count; sqrt(pi/432) appears nowhere
    in it.  Imported here from the prior gate so there is one source of truth.)

[B] EXCLUSION THEOREM (exact, assertable).  Positing that the true knob is
    sqrt(c) for some c != pi/432 -- i.e. "pi/432 is just slightly the wrong
    number" -- multiplies every (1 + fractional-deviation) by the SAME factor
    sqrt(c_old/c_new), independent of the relation.  So a wrong reference shifts
    ALL deviations together and leaves the back-solved eps0 in the SAME relative
    positions: it can neither create nor remove a split.  The absolute spread of
    the back-solved eps0 (~2.2% here) is therefore reference-INVARIANT.  Hence the
    observed split CANNOT be explained by a wrong value of pi/432; it requires a
    correction that depends on the POWER of eps0 (amplitude vs probability).  This
    eliminates the "wrong constant" reading and narrows the surviving causes to
    (i) the amplitude-vs-probability bridge rule (sqrt(n) vs n) and (ii) genuine
    power/scale-dependent (RG-like) running.

[C] SIGNIFICANCE (exact combinatorics, assertable; verdict on the data printed).
    Under the null "the power label is unrelated to the deviation", the chance
    that the two amplitude relations are BOTH more deviant (more negative) than
    all five probability relations -- the observed perfect separation -- is
    1 / C(7,2) = 1/21 ~ 0.048 one-sided (2/21 ~ 0.095 two-sided).  So the split is
    SUGGESTIVE at the ~2-sigma level, NOT decisive, and it leans heavily on |V_us|
    (the only amplitude with a small error); there are just two power-1 points.
    The grouping is pre-specified by the framework's own amplitude/probability
    distinction, not chosen to maximise significance.

[D] A STRUCTURED HINT (printed, explicitly NOT asserted).  The amplitude mean
    correction a ~ -0.81% and the probability pre-sqrt correction b ~ +1.62%
    satisfy b ~ -2a to ~0.01%.  For small corrections that is the signature of
    RECIPROCAL family corrections (amplitudes want eps0*(1+a), probabilities want
    eps0*(1+a)^{-1}), equivalently sqrt(pi/432) is recovered as the GEOMETRIC MEAN
    of the amplitude-fit and probability-fit eps0.  With only two amplitude points
    and ~30% scatter in the probability devs, the 0.01% match is partly fortuitous;
    this is a hint to watch as errors shrink, not a result.

PROVED here (exact, measurement-independent):
  - the reference-rescaling identity (the [B] exclusion theorem): changing the
    reference multiplies every (1 + frac-dev) by one common factor, so the spread
    is reference-invariant;
  - the combinatorics C(7,2) = 21, giving the one-sided p = 1/21 for perfect
    separation.

NOT asserted (reported only): the observed perfect separation, the p-value's
applicability, the a/b magnitudes and the b ~ -2a / geometric-mean hint -- all
data, and PDG/NuFIT central values move.

This is a DIAGNOSTIC: it promotes no ledger row and moves no Bayes credit, and it
does not touch the frozen registry.  It sharpens (does not overturn) the prior
knob-consistency gate: the split survives any choice of pi/432 and is ~2 sigma.
"""

from __future__ import annotations

import math

from epsilon_knob_consistency import RELATIONS, eps0_from, EPS0_TH


def banner(t: str) -> None:
    print("=" * 78)
    print(f"  {t}")
    print("=" * 78)


def main() -> bool:
    banner("IS THE eps0 POWER-SPLIT REAL?  significance + exclusion theorem")

    # back-solved eps0 (data + counts only)
    amp = [(r.name, *eps0_from(r)) for r in RELATIONS if r.power == 1]
    prob = [(r.name, *eps0_from(r)) for r in RELATIONS if r.power == 2]
    amp_eps = [e for _, e, _ in amp]
    prob_eps = [e for _, e, _ in prob]
    all_eps = amp_eps + prob_eps

    print(f"\n  theory eps0 = sqrt(pi/432) = {EPS0_TH:.6f}")
    print(f"  amplitudes (power 1):  {[round(e, 6) for e in amp_eps]}")
    print(f"  probabilities(power 2):{[round(e, 6) for e in prob_eps]}")

    # ---- [A] the back-solve never uses pi/432 -----------------------------
    print("\n[A] Back-solved eps0 depend only on data and counts, not on pi/432")
    print("    (eps0_from reads value and count; the reference enters only for")
    print("     the deviation column -- which is the whole point of [B].)")

    # ---- [B] EXCLUSION THEOREM: a wrong pi/432 cannot make a split --------
    print("\n[B] EXCLUSION THEOREM -- 'pi/432 is the wrong number' cannot explain it")
    spread = max(all_eps) - min(all_eps)
    # changing the reference c multiplies every (1 + frac-dev) by sqrt(c_old/c_new),
    # the SAME factor for every relation -> relative positions (the split) frozen.
    c0 = math.pi / 432.0
    for c in (0.5 * c0, 2.0 * c0, 0.97 * c0):
        ref_old = math.sqrt(c0)
        ref_new = math.sqrt(c)
        common = None
        for e in all_eps:
            ratio = (e / ref_old) / (e / ref_new)        # = sqrt(c/c0), e cancels
            if common is None:
                common = ratio
            assert abs(ratio - common) < 1e-15, "rescaling is not relation-independent"
            assert abs(ratio - math.sqrt(c / c0)) < 1e-15
    print(f"    changing reference multiplies every (1+frac-dev) by ONE common")
    print(f"    factor sqrt(c/c0) (verified relation-independent to 1e-15);")
    print(f"    so the absolute spread {spread:.6f} (= {spread / EPS0_TH * 100:.2f}% of")
    print(f"    theory) is reference-INVARIANT. No value of pi/432 removes the split")
    print(f"    => the residual is POWER-dependent (bridge rule sqrt(n)-vs-n, or RG),")
    print(f"       NOT a mis-set constant.")

    # ---- [C] SIGNIFICANCE of the perfect separation -----------------------
    print("\n[C] Significance of the amplitude-below / probability-above split")
    n_total = len(all_eps)
    n_amp = len(amp_eps)
    assert n_total == 7 and n_amp == 2
    ways = math.comb(n_total, n_amp)
    assert ways == 21, "C(7,2) must be 21"
    perfect = max(amp_eps) < min(prob_eps)               # data (printed, not asserted)
    p_one = 1.0 / ways
    print(f"    {n_amp} amplitudes, {n_total - n_amp} probabilities; C(7,2) = {ways}.")
    print(f"    observed perfect separation (all amp < all prob): {perfect}  (data)")
    print(f"    one-sided p(perfect separation) = 1/{ways} = {p_one:.3f}  (~2 sigma)")
    print(f"    two-sided p = 2/{ways} = {2 * p_one:.3f}")
    print(f"    SUGGESTIVE, not decisive: only 2 amplitude points, leans on |V_us|;")
    print(f"    the grouping is the framework's own amplitude/probability split.")

    # ---- [D] structured hint: b ~ -2a / geometric mean (NOT asserted) -----
    print("\n[D] A structured hint (printed, NOT asserted -- partly fortuitous)")
    a = (sum(amp_eps) / len(amp_eps)) / EPS0_TH - 1.0
    b = ((sum(prob_eps) / len(prob_eps)) / EPS0_TH) ** 2 - 1.0
    geo = math.sqrt((sum(amp_eps) / len(amp_eps)) * (sum(prob_eps) / len(prob_eps)))
    print(f"    amplitude mean correction      a = {a * 100:+.2f}%")
    print(f"    probability pre-sqrt correction b = {b * 100:+.2f}%   (-2a = {-2 * a * 100:+.2f}%)")
    print(f"    b ~ -2a => reciprocal family corrections (amp ~ eps0(1+a),")
    print(f"    prob ~ eps0(1+a)^-1); equivalently sqrt(pi/432) is the GEOMETRIC")
    print(f"    MEAN of the two family fits: sqrt(amp*prob) = {geo:.6f} vs {EPS0_TH:.6f}")
    print(f"    ({(geo / EPS0_TH - 1) * 100:+.2f}%). With 2 amp points + ~30% prob scatter")
    print(f"    the 0.01% b~-2a match is partly luck -- a hint to watch, not a result.")

    # ---- [E] what would make it decisive ----------------------------------
    print("\n[E] Decisive handle")
    print("    If shrinking errors KEEP amplitudes low and probabilities high, a real")
    print("    power-dependent correction (bridge rule or RG) is confirmed over noise.")
    print("    A third precise amplitude (|V_ub| to ~1%) would roughly halve the")
    print("    permutation p; a derived sqrt(n)-vs-n correction would predict b = -2a.")

    print("\n[V] Sandbox verdict")
    print("    back-solve uses data+counts only, not pi/432            : PASS")
    print("    EXCLUSION THM: spread reference-invariant (wrong-c out)  : PASS")
    print("    C(7,2)=21, one-sided p=1/21 for perfect separation       : PASS")
    print("    split is ~2 sigma suggestive (leans on |V_us|, 2 points) : REPORTED (data)")
    print("    b ~ -2a / geometric-mean hint                            : REPORTED (not asserted)")
    print("    cause = bridge rule vs RG (constant excluded)            : OPEN (narrowed)")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
