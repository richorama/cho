"""
Bayesian model evidence: CHO vs an O(1)-numerology null.
========================================================

`independent_observables.py` and `covariance_gof.py` answer "is the fit
statistically acceptable?" (yes, marginally). They do NOT answer the question a
skeptic actually asks: "is the STRUCTURE favoured over chance, once you pay for
the parameters you spent?" That is a model-comparison question, and the honest
tool is a Bayes factor, not a chi-square.

This module computes a transparent log Bayes factor

    ln B = ln Z(CHO) - ln Z(null)

between two models of the independent observable set:

  * CHO       — each observable is predicted as a FIXED number P_i (no free
                continuous parameter per observable), at the cost of a set of
                discrete structural choices (prefactors) whose total description
                length is K_bits (from model_complexity.py). Spending those bits
                is charged as an Occam prior penalty.

  * null      — "it's just O(1) numerology": each observable's prediction is a
                free value drawn from a wide prior of width R_i = F * |O_i|
                (the prediction could have landed anywhere within a factor ~F of
                the right order of magnitude). A free parameter that can fit the
                datum carries the usual Occam factor sigma_i / R_i.

Per observable the evidence ratio is the standard Occam factor

    ln B_i = ln(R_i / sigma_i) - 0.5 ln(2 pi) - 0.5 pull_i^2,

summed over the observables, CORRELATION-CORRECTED by the factor N_eff / N (the
shared-eps0 common mode means the rows are not N independent pieces of
evidence — reuses covariance_gof), and finally charged the discrete-parameter
penalty:

    ln B = (N_eff / N) * sum_i ln B_i  -  K_bits * ln 2.

Interpretation (Jeffreys/Kass-Raftery): ln B > 0 favours CHO; |ln B| < 1 is
"not worth more than a bare mention", 1-3 positive, 3-5 strong, > 5 very strong.
The result is reported for several prior widths F, because B depends on the
stated prior — that dependence is shown openly, not hidden.

No scipy. Reuses covariance_gof and model_complexity.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/bayesian_evidence.py
"""

import math

import numpy as np

from covariance_gof import (
    build_independent_set,
    covariance,
    correlation_from_cov,
    effective_independent_count,
)
from model_complexity import STRUCTURAL_CHOICES


def discrete_parameter_bits(credited=("derived",)):
    """Total description length (bits) of the discrete choices still PAID for.

    `credited` is the set of derivation statuses that cost nothing (their numbers
    are forced by the algebra). Every choice whose status is NOT in `credited` is
    paid for in full. Default credits only the numerically-closed ("derived")
    items — the defensible floor. scoreboard.py sweeps `credited` to show how the
    Bayes factor moves as the derivation program credits more statuses.
    """
    return sum(bits for _label, bits, status, _note in STRUCTURAL_CHOICES
               if status not in credited)


def log_bayes_factor(F, credited=("derived",)):
    """ln B for prior width factor F (R_i = F * |O_i|) and a credited status set."""
    names, preds, obs, sig_exp, powers = build_independent_set()
    cov = covariance(preds, sig_exp, powers)
    corr = correlation_from_cov(cov)
    n = len(names)
    n_eff = effective_independent_count(corr)

    sigma = np.sqrt(np.diag(cov))
    resid = preds - obs
    pulls = resid / sigma

    R = F * np.abs(obs)
    ln_Bi = np.log(R / sigma) - 0.5 * math.log(2 * math.pi) - 0.5 * pulls ** 2
    raw_sum = float(np.sum(ln_Bi))
    corrected = raw_sum * (n_eff / n)

    k_bits = discrete_parameter_bits(credited)
    penalty = k_bits * math.log(2.0)

    ln_B = corrected - penalty
    return {
        "n": n,
        "n_eff": n_eff,
        "raw_sum": raw_sum,
        "corrected": corrected,
        "k_bits": k_bits,
        "penalty": penalty,
        "ln_B": ln_B,
        "ln_Bi": ln_Bi,
        "names": names,
        "pulls": pulls,
    }


def jeffreys(ln_B):
    a = abs(ln_B)
    if a < 1.0:
        verdict = "inconclusive (not worth more than a bare mention)"
    elif a < 3.0:
        verdict = "positive"
    elif a < 5.0:
        verdict = "strong"
    else:
        verdict = "very strong"
    return ("favours CHO" if ln_B > 0 else "favours the null"), verdict


def main():
    print("=" * 78)
    print("  BAYESIAN MODEL EVIDENCE — CHO vs an O(1)-numerology null")
    print("  Occam factor on the independent set, correlation- and parameter-")
    print("  penalised. Reported across prior widths F (shown, not hidden).")
    print("=" * 78)

    base = log_bayes_factor(3.0)
    print(f"\n  Independent observables N         : {base['n']}")
    print(f"  Effective independent N_eff       : {base['n_eff']:.1f}"
          f"  (shared-eps0 common mode)")
    print(f"  Discrete structural bits K_bits   : {base['k_bits']:.1f}"
          f"  -> Occam penalty {base['penalty']:.2f} nats")

    print("\n  Per-observable Occam contributions ln B_i (at F = 3):")
    print("  " + "-" * 60)
    order = np.argsort(base["ln_Bi"])
    for idx in order:
        print(f"    {base['names'][idx]:<16} ln B_i = {base['ln_Bi'][idx]:+6.2f}"
              f"   (pull {base['pulls'][idx]:+.2f})")
    print("  " + "-" * 60)

    print("\n  Prior-width sensitivity (R_i = F * |O_i|):")
    print(f"    {'F':>5}{'corrected sum':>16}{'- penalty':>12}"
          f"{'ln B':>10}{'log10 B':>10}")
    for F in (2.0, 3.0, 5.0, 10.0):
        r = log_bayes_factor(F)
        print(f"    {F:>5.0f}{r['corrected']:>16.2f}{-r['penalty']:>12.2f}"
              f"{r['ln_B']:>10.2f}{r['ln_B'] / math.log(10):>10.2f}")

    side, verdict = jeffreys(base["ln_B"])
    print("\n  " + "-" * 74)
    print("  RESULT (at the stated reference prior F = 3)")
    print(f"   * ln B = {base['ln_B']:+.2f}  (log10 B = {base['ln_B']/math.log(10):+.2f})")
    print(f"   * Jeffreys reading: {side}, {verdict}.")

    # Break-even: how many derived bits flip ln B to zero?
    # ln B = corrected - k_bits * ln2 = 0  ->  k_bits* = corrected / ln2.
    corrected = base["corrected"]
    k_breakeven = corrected / math.log(2.0)
    bits_to_derive = base["k_bits"] - k_breakeven
    print("\n  HONEST READING (conservative credit: only numerically-closed items)")
    print(f"   * Credited only the DERIVED (numerically-closed) prefactors as free;")
    print(f"     all remaining {base['k_bits']:.0f} bits of chosen/geometric choices are paid")
    print(f"     in full ({base['penalty']:.1f} nats). Even so the evidence gain")
    print(f"     ({corrected:.1f} nats) is smaller than the penalty, so at this credit")
    print("     level CHO does not yet beat O(1) numerology. This is the skeptic's")
    print("     strongest point, stated plainly rather than hidden behind a row-count.")
    print(f"   * BREAK-EVEN: ln B reaches 0 when the paid description length falls to")
    print(f"     ~{k_breakeven:.0f} bits, i.e. when ~{bits_to_derive:.0f} more of the current "
          f"{base['k_bits']:.0f} bits of")
    print("     prefactors are DERIVED from the algebra (cost -> 0) instead of chosen.")
    print("   * So the Bayesian verdict is a sharp target, not a death sentence: the")
    print("     derivation program (DERIVATION_LEDGER.md) is precisely what converts")
    print("     paid bits into free ones. See scoreboard.py for the before/now/target")
    print("     movement as the eps0 work credits the geometric pi/16/27 as well.")
    print("   * It also depends on the prior width F: only for implausibly wide")
    print("     priors does the bare fit overcome the penalty. Honesty")
    print("     demands quoting the F-dependence, shown above.")
    print()


if __name__ == "__main__":
    main()
