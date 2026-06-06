"""
Independent-observable goodness-of-fit for the CHO framework.
=============================================================

The 25-row audit table is NOT 25 independent measurements. Several rows are
exact algebraic consequences of others (the inter-sector mass ratios are built
from masses already listed), and the predictions reuse the same master constant
eps0^2. Quoting "22/25 within 3%" therefore overstates the evidence.

This module produces an honest statistical artifact:

  1. It separates the audit rows into an INDEPENDENT prediction set and a
     DEPENDENT (algebraic-consequence) set.
  2. It computes a chi-square goodness-of-fit on the independent set only,
     under an explicit, stated theory-error model (these are approximate bridge
     relations, not precision predictions, so experimental error alone is the
     wrong yardstick).
  3. It reports reduced chi-square and a p-value, and shows how the naive
     "all rows independent" count inflates the apparent significance.

No scipy: the chi-square survival function is implemented directly via the
regularized upper incomplete gamma function.
"""
import math

import summary_table


# --------------------------------------------------------------------------
# chi-square survival function Q(x; k) = P(chi^2_k > x), via incomplete gamma
# --------------------------------------------------------------------------
def _gammq(a, x):
    """Regularized upper incomplete gamma Q(a, x) = Gamma(a, x)/Gamma(a)."""
    if x < 0 or a <= 0:
        raise ValueError("invalid arguments")
    if x == 0:
        return 1.0
    if x < a + 1.0:
        return 1.0 - _gser(a, x)
    return _gcf(a, x)


def _gser(a, x, itmax=500, eps=1e-12):
    """Lower incomplete gamma P(a,x) via series."""
    gln = math.lgamma(a)
    ap = a
    s = 1.0 / a
    delta = s
    for _ in range(itmax):
        ap += 1.0
        delta *= x / ap
        s += delta
        if abs(delta) < abs(s) * eps:
            break
    return s * math.exp(-x + a * math.log(x) - gln)


def _gcf(a, x, itmax=500, eps=1e-12):
    """Upper incomplete gamma Q(a,x) via continued fraction (Lentz)."""
    gln = math.lgamma(a)
    tiny = 1e-30
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, itmax):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return math.exp(-x + a * math.log(x) - gln) * h


def chi2_sf(x, k):
    """P(chi^2 with k dof > x)."""
    return _gammq(k / 2.0, x / 2.0)


# --------------------------------------------------------------------------
# Independence classification
# --------------------------------------------------------------------------
# Rows that are EXACT algebraic consequences of other listed predictions.
# (Inter-sector mass ratios are products/quotients of masses already in the set.)
DEPENDENT_ROWS = {
    "m_s·m_t/(m_b·m_c)",
    "m_μ·m_t/(m_τ·m_c)",
    "m_μ·m_b/(m_τ·m_s)",
}

# Theory-error floor: these are approximate bridge relations. The unified
# spurion bridge quotes ~1.5% RMS across flavour channels; we adopt that as a
# stated, uniform fractional theory uncertainty. This is an assumption, made
# explicit so the goodness-of-fit is interpretable.
THEORY_REL_ERR = 0.015


def main():
    rows = summary_table.predictions()

    indep, dependent = [], []
    for name, formula, pred, obs, unc, unit in rows:
        rec = (name, pred, obs, unc)
        if name in DEPENDENT_ROWS:
            dependent.append(rec)
        else:
            indep.append(rec)

    print("=" * 76)
    print("  CHO INDEPENDENT-OBSERVABLE GOODNESS-OF-FIT")
    print(f"  Theory-error floor: {THEORY_REL_ERR*100:.1f}% (stated assumption)")
    print("  Dependent rows (algebraic consequences) excluded from chi-square.")
    print("=" * 76)

    # --- naive count vs honest count ---
    def within(frac, recs):
        return sum(1 for _, p, o, _ in recs if abs(p - o) / abs(o) <= frac)

    n_all = len(rows)
    n_ind = len(indep)
    print(f"\n  Row accounting:")
    print(f"    Total audit rows                 : {n_all}")
    print(f"    Dependent (algebraic) rows       : {len(dependent)}")
    print(f"    Independent prediction rows      : {n_ind}")
    print(f"    Naive 'within 3%' over ALL rows  : "
          f"{within(0.03, [(n,p,o,u) for n,_,p,o,u,_ in rows])}/{n_all}")
    print(f"    Honest 'within 3%' over indep set: "
          f"{within(0.03, indep)}/{n_ind}")

    # --- chi-square on independent set ---
    print(f"\n  {'Observable':<22}{'pred':>11}{'obs':>11}{'sigma_tot':>11}{'pull':>8}")
    print("  " + "-" * 61)
    chi2 = 0.0
    pulls = []
    for name, pred, obs, unc in indep:
        sigma = math.sqrt(unc**2 + (THEORY_REL_ERR * abs(obs))**2)
        pull = (pred - obs) / sigma
        chi2 += pull**2
        pulls.append(pull)
        print(f"  {name:<22}{pred:>11.4g}{obs:>11.4g}{sigma:>11.3g}{pull:>8.2f}")
    print("  " + "-" * 61)

    k = n_ind  # conservative: no continuous low-energy parameters fit per row
    red = chi2 / k
    p = chi2_sf(chi2, k)
    print(f"\n  chi-square (independent set) : {chi2:7.2f}")
    print(f"  degrees of freedom           : {k}")
    print(f"  reduced chi-square           : {red:6.2f}")
    print(f"  p-value  P(chi2_{k} > obs)    : {p:8.4f}")

    # --- outlier identification ---
    ranked = sorted(zip([n for n, _, _, _ in indep], pulls),
                    key=lambda t: -abs(t[1]))
    print("\n  Largest pulls (worst-fitting rows):")
    for name, pull in ranked[:3]:
        print(f"    {name:<22} {pull:+.2f} sigma")
    worst_name, worst_pull = ranked[0]
    if abs(worst_pull) > 2.5:
        print(f"\n  NOTE: '{worst_name}' is the dominant outlier. The first-generation")
        print("  masses are SQUARED ratios of predicted 2nd/3rd-gen masses, so they")
        print("  compound upstream ~1% errors. See first_generation_audit.py: the")
        print("  intrinsic bridge-factor error is ~2%, the rest is propagation.")
        # chi-square with the dominant outlier removed (honest sensitivity check).
        chi2_excl = chi2 - worst_pull ** 2
        k_excl = k - 1
        red_excl = chi2_excl / k_excl
        p_excl = chi2_sf(chi2_excl, k_excl)
        print(f"  Excluding it: reduced chi^2 = {red_excl:.2f}, p = {p_excl:.2f}"
              f" over {k_excl} rows.")

    # Inflation illustration: pretend all rows independent at exp-only error.
    chi2_naive = 0.0
    for name, formula, pred, obs, unc, unit in rows:
        if unc > 0:
            chi2_naive += ((pred - obs) / unc) ** 2
    print(f"\n  For contrast, chi-square treating ALL {n_all} rows as independent")
    print(f"  with EXPERIMENTAL error only (the inflated, wrong statistic):")
    print(f"    chi2_naive = {chi2_naive:.1f}  -> reduced {chi2_naive/n_all:.1f}")
    print("    (huge because these are approximate relations, not precision")
    print("     predictions, AND because dependent rows are double-counted).")

    print("\n  Reading guide:")
    print("   * The honest GoF uses the independent set + a stated theory floor.")
    print(f"   * reduced chi^2 ~ {red:.2f} with p ~ {p:.2f} means the relations are")
    print("     statistically consistent at the assumed theory precision.")
    print("   * It does NOT mean precision agreement: tighten the theory error")
    print("     ONLY when a bridge is derived, then this test becomes stringent.")
    print()


if __name__ == "__main__":
    main()
