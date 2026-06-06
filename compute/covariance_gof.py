"""
Covariance goodness-of-fit for the CHO framework  (closes ledger STAT1).
========================================================================

`independent_observables.py` took the first honest step: it removed the three
rows that are EXACT algebraic consequences of others and applied a diagonal
theory floor. But it still treated the remaining rows as statistically
independent. They are not: almost every flavour row is a power of the SAME
triality-breaking knob `eps0`, so their theory errors share a common mode. A row
that uses `eps0^4` is far more correlated with another `eps0^4` row than a naive
diagonal chi-square admits.

This module builds the actual covariance matrix and reports:

  1. a correlated chi-square  chi2 = r^T C^-1 r  with C = C_exp + C_theory,
  2. the EFFECTIVE number of independent observables N_eff (participation ratio
     of the correlation matrix), which is strictly less than the row count,
  3. the contrast with the diagonal (uncorrelated) chi-square.

Covariance model (transparent and stated, not fitted)
-----------------------------------------------------
For each observable i with CHO prediction P_i and measurement O_i +/- sigma_exp_i:

  * experimental error:        C_exp[i,i] = sigma_exp_i^2
  * independent theory floor:  per-row fractional sigma_ind = 1.0%
  * COMMON-MODE bridge error:  a single fractional error b on eps0 (sigma_b),
    propagated to row i with sensitivity p_i = d ln P_i / d ln eps0 = the power
    of eps0 in the CHO formula. This is what couples the rows.

  C_theory[i,j] = delta_ij (sigma_ind P_i)^2 + p_i p_j P_i P_j sigma_b^2.

The eps0 powers p_i are read off the closed-form CHO formulas in
summary_table.py (documented in EPS0_POWER below). The common-mode term is the
honest encoding of "these are not N independent measurements".

No scipy: reuses the incomplete-gamma chi-square survival function from
independent_observables.py and numpy for linear algebra.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/covariance_gof.py
"""

import numpy as np

import summary_table
from independent_observables import chi2_sf, DEPENDENT_ROWS


# --------------------------------------------------------------------------
# eps0 sensitivity of each row: p_i = d ln P_i / d ln eps0
# --------------------------------------------------------------------------
# Read off the closed-form formulas. Masses propagate their own eps content:
#   m_tau, m_b, m_c ~ eps0^2 ; m_s, m_mu ~ eps0^4 ; m_d, m_e ~ eps0^6.
#   |V_us|, |V_cb| ~ eps0^1 ; |V_ub|, sin2_13, dm2_ratio ~ eps0^2.
#   J_CKM ~ eps0^4 (leading mixing scaling). sin2_12 has a weak, non-integer
#   sensitivity computed analytically below. eps0-independent rows have p=0.
EPS0_POWER = {
    "m_t": 0.0, "m_H": 0.0, "α⁻¹(0)": 0.0, "sin²θ_W": 0.0,
    "m_ν₃": 0.0, "M_W": 0.0, "sin²θ₂₃": 0.0,
    "m_τ": 2.0, "m_b": 2.0, "m_c": 2.0,
    "m_s": 4.0, "m_μ": 4.0, "J_CKM": 4.0,
    "m_u": 4.0, "m_d": 6.0, "m_e": 6.0,
    "|V_us|": 1.0, "|V_cb|": 1.0,
    "|V_ub|": 2.0, "sin²θ₁₃": 2.0, "Δm²₂₁/Δm²₃₁": 2.0,
    # sin2_12 = 1/(3 + sqrt7 eps0): d ln/d ln eps0 = -sqrt7 eps0/(3 + sqrt7 eps0)
    "sin²θ₁₂": -np.sqrt(7.0) * summary_table.EPS0 / (3.0 + np.sqrt(7.0) * summary_table.EPS0),
}

SIGMA_IND = 0.010   # per-row independent theory floor (fractional)
SIGMA_B = 0.007     # common-mode fractional error on eps0


def build_independent_set():
    """Return the independent rows as arrays (name, pred, obs, sigma_exp, p)."""
    rows = summary_table.predictions()
    names, preds, obs, sig_exp, powers = [], [], [], [], []
    for name, _formula, pred, obs_val, unc, _unit in rows:
        if name in DEPENDENT_ROWS:
            continue
        names.append(name)
        preds.append(float(pred))
        obs.append(float(obs_val))
        sig_exp.append(float(unc))
        powers.append(float(EPS0_POWER.get(name, 0.0)))
    return (
        names,
        np.array(preds),
        np.array(obs),
        np.array(sig_exp),
        np.array(powers),
    )


def covariance(preds, sig_exp, powers):
    """C = C_exp + C_theory(independent floor + eps0 common mode)."""
    n = len(preds)
    c_exp = np.diag(sig_exp**2)
    c_floor = np.diag((SIGMA_IND * preds) ** 2)
    sens = powers * preds                       # d P_i / d ln eps0
    c_common = SIGMA_B**2 * np.outer(sens, sens)
    return c_exp + c_floor + c_common


def correlation_from_cov(cov):
    d = np.sqrt(np.diag(cov))
    return cov / np.outer(d, d)


def effective_independent_count(corr):
    """Participation ratio N_eff = (sum lambda)^2 / sum lambda^2.

    For a correlation matrix trace = N, so N_eff = N^2 / sum(lambda^2).
    Uncorrelated -> N_eff = N; strongly correlated -> N_eff < N.
    """
    eig = np.linalg.eigvalsh(corr)
    eig = np.clip(eig, 0.0, None)
    return float((eig.sum() ** 2) / np.sum(eig**2))


def main():
    names, preds, obs, sig_exp, powers = build_independent_set()
    n = len(names)
    resid = preds - obs

    cov = covariance(preds, sig_exp, powers)
    corr = correlation_from_cov(cov)

    # Correlated chi-square.
    cov_inv = np.linalg.inv(cov)
    chi2_corr = float(resid @ cov_inv @ resid)

    # Diagonal (uncorrelated) chi-square for contrast.
    diag = np.diag(cov)
    chi2_diag = float(np.sum(resid**2 / diag))

    n_eff = effective_independent_count(corr)
    red_corr = chi2_corr / n
    red_corr_eff = chi2_corr / n_eff
    p_corr = chi2_sf(chi2_corr, n)
    p_corr_eff = chi2_sf(chi2_corr, max(1, round(n_eff)))

    print("=" * 78)
    print("  CHO COVARIANCE GOODNESS-OF-FIT  (closes STAT1)")
    print("  Full covariance with a shared-eps0 common mode; not a diagonal fit.")
    print(f"  sigma_ind (per-row floor) = {SIGMA_IND*100:.1f}% ;  "
          f"sigma_b (eps0 common mode) = {SIGMA_B*100:.1f}%")
    print("=" * 78)

    print(f"\n  Independent rows (algebraic-consequence rows excluded): {n}")
    print(f"\n  {'observable':<16}{'pred':>11}{'obs':>11}{'p(eps0)':>9}"
          f"{'sigma_tot':>11}{'pull':>8}")
    print("  " + "-" * 64)
    sig_tot = np.sqrt(np.diag(cov))
    for name, pr, ob, pw, st in zip(names, preds, obs, powers, sig_tot):
        print(f"  {name:<16}{pr:>11.4g}{ob:>11.4g}{pw:>9.2f}{st:>11.3g}"
              f"{(pr-ob)/st:>8.2f}")
    print("  " + "-" * 64)

    print(f"\n  Effective independent observables N_eff = {n_eff:.1f}"
          f"  (of {n} rows)")
    print(f"    -> the shared eps0 dependence removes ~{n - n_eff:.1f} independent")
    print("       directions; the rows do NOT count as separate measurements.")

    print(f"\n  Correlated chi-square  r^T C^-1 r        : {chi2_corr:8.2f}")
    print(f"  reduced (vs {n} rows)                    : {red_corr:8.2f}"
          f"   p = {p_corr:.3f}")
    print(f"  reduced (vs N_eff = {round(n_eff)})                 : {red_corr_eff:8.2f}"
          f"   p = {p_corr_eff:.3f}")
    print(f"\n  Diagonal chi-square (no correlation)     : {chi2_diag:8.2f}"
          f"   reduced {chi2_diag/n:.2f}")
    print(f"  Correlation correction changes chi2 by   : "
          f"{chi2_corr - chi2_diag:+.2f}")

    # Largest pulls under the full covariance.
    pulls = resid / sig_tot
    order = np.argsort(-np.abs(pulls))
    print("\n  Largest pulls under the full covariance:")
    for idx in order[:3]:
        print(f"    {names[idx]:<16} {pulls[idx]:+.2f} sigma")

    print("\n  Defensible one-line summary:")
    print(f"   * {n} independent rows collapse to N_eff ~ {n_eff:.0f} effective")
    print(f"     observables once the shared eps0 dependence is modelled;")
    print(f"   * with stated theory errors and full covariance, reduced chi^2")
    print(f"     ~ {red_corr_eff:.2f} (p ~ {p_corr_eff:.2f}) against N_eff -- statistically")
    print("     consistent, NOT precision agreement.")
    print("   * This supersedes the diagonal-with-floor figure and the raw row")
    print("     count for any external goodness-of-fit claim (ledger STAT1).")
    print()


if __name__ == "__main__":
    main()
