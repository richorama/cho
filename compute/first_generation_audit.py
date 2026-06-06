"""
First-generation mass audit: separate intrinsic error from propagated error.
============================================================================

The independent-observable goodness-of-fit flags m_e as a ~ -3.75 sigma outlier
-- by far the worst row. A hostile reviewer will lead with it. This script
confronts it honestly and shows the outlier is mostly an ERROR-PROPAGATION
artifact, not a single broken bridge factor.

Structure of the first-generation predictions (Gatto/NNI squared relations):

    m_first = k_sector * m_second^2 / m_third

with sector prefactors:

    up      k = 1/4              (= sin^2 theta_W tree)
    down    k = 9/4              (= N_c^2 * 1/4)
    lepton  k = 1/(4 pi)         (the 1/pi is an UNDERIVED measure assumption)

Two distinct error sources are tangled together in the headline number:

  (A) INTRINSIC factor error: how well does k itself reproduce the data when
      fed the MEASURED second/third-generation masses? This is the only part
      that tests the CHO bridge factor.

  (B) PROPAGATED error: the audit table feeds PREDICTED m_second and m_third
      (each already ~1% off) into a SQUARED relation, so a 1.4% muon error
      becomes ~2.8% in m_e before the factor is even applied.

Separating (A) from (B) shows where the real proof obligation is: the lepton
1/pi factor at the ~2% level, NOT a 5-6% modelling failure.
"""
import math

PI = math.pi

# Measured masses (GeV) and their absolute uncertainties.
OBS = {
    "m_u": (2.16e-3, 0.49e-3),
    "m_c": (1.270, 0.020),
    "m_t": (172.76, 0.30),
    "m_d": (4.67e-3, 0.48e-3),
    "m_s": (0.0934, 0.0008),
    "m_b": (4.18, 0.03),
    "m_e": (0.511e-3, 0.00001e-3),
    "m_mu": (0.10566, 0.00001),
    "m_tau": (1.77700, 0.00024),
}

# Predicted second/third-generation masses (the audit-table chain).
EPS2 = PI / 432
V = 246.22


def predicted_chain():
    m_t = V / math.sqrt(2)
    m_tau = math.sqrt(2) * EPS2 * m_t
    m_b = (7.0 / 3) * m_tau
    m_c = EPS2 * m_t
    m_s = 3 * EPS2 * m_b
    m_mu = 8 * EPS2 * m_tau
    return {"m_t": m_t, "m_tau": m_tau, "m_b": m_b,
            "m_c": m_c, "m_s": m_s, "m_mu": m_mu}


SECTORS = [
    # (label, k, k_repr, second, third, first)
    ("up",     0.25,        "1/4",      "m_c",  "m_t", "m_u"),
    ("down",   2.25,        "9/4",      "m_s",  "m_b", "m_d"),
    ("lepton", 1 / (4 * PI), "1/(4pi)", "m_mu", "m_tau", "m_e"),
]


def main():
    pred = predicted_chain()
    print("=" * 76)
    print("  FIRST-GENERATION MASS AUDIT")
    print("  Decomposing the m_e outlier: intrinsic factor vs propagated error.")
    print("=" * 76)

    print(f"\n  {'sector':<8}{'k':<10}{'first':<7}"
          f"{'full-pred':>11}{'obs-input':>11}{'measured':>11}")
    print("  " + "-" * 64)

    rows = []
    for label, k, krepr, sec, thr, fst in SECTORS:
        obs_first = OBS[fst][0]
        # (A) factor fed MEASURED inputs -> isolates the bridge factor.
        m_obs_input = k * OBS[sec][0] ** 2 / OBS[thr][0]
        # full prediction fed PREDICTED inputs -> the audit-table value.
        m_full = k * pred[sec] ** 2 / pred[thr]
        err_full = (m_full - obs_first) / obs_first * 100
        err_intrinsic = (m_obs_input - obs_first) / obs_first * 100
        rows.append((label, krepr, fst, m_full, m_obs_input, obs_first,
                     err_full, err_intrinsic))
        print(f"  {label:<8}{krepr:<10}{fst:<7}"
              f"{m_full*1e3:>10.4f}m{m_obs_input*1e3:>10.4f}m"
              f"{obs_first*1e3:>10.4f}m")

    print("\n  Error decomposition (percent vs measured):")
    print("  " + "-" * 64)
    print(f"  {'sector':<8}{'full-pred err':>16}{'intrinsic err':>16}"
          f"{'propagated':>14}")
    print("  " + "-" * 64)
    for (label, krepr, fst, mf, mo, of, ef, ei) in rows:
        propagated = ef - ei
        print(f"  {label:<8}{ef:>+15.1f}%{ei:>+15.1f}%{propagated:>+13.1f}%")

    print("\n  Reading guide:")
    print("   * 'intrinsic err' uses MEASURED 2nd/3rd-gen masses, so it tests")
    print("     ONLY the CHO bridge factor k. 'propagated' is the extra error")
    print("     from feeding already-off PREDICTED masses into a SQUARED ratio.")
    print("   * m_e: the headline -5.6% (-3.75 sigma) is mostly PROPAGATION;")
    print("     the genuinely-unproven 1/(4pi) factor is only ~ -2.2% on its own.")
    print("   * m_u, m_d look fine ONLY because their experimental errors are")
    print("     ~20%; their factors 1/4 and 9/4 are tested far less stringently.")

    # The honest stress test: factors against measured inputs.
    print("\n  HONEST FACTOR TEST (measured inputs):")
    print("  " + "-" * 64)
    print(f"  {'sector':<8}{'k':<10}{'frac err':>10}{'exp sigma':>12}"
          f"{'1.5%-floor sigma':>18}")
    print("  " + "-" * 64)
    for (label, krepr, fst, mf, mo, of, ef, ei) in rows:
        unc = OBS[fst][1]
        frac = (mo - of) / of
        pull_exp = (mo - of) / unc
        sigma_floor = math.sqrt(unc ** 2 + (0.015 * of) ** 2)
        pull_floor = (mo - of) / sigma_floor
        print(f"  {label:<8}{krepr:<10}{frac*100:>+9.1f}%"
              f"{pull_exp:>+12.1f}{pull_floor:>+18.2f}")
    print("  " + "-" * 64)
    print("   * 'exp sigma' uses experimental error ALONE. The electron mass is")
    print("     known to 8 digits, so its tiny error turns a 2.2% factor miss")
    print("     into a huge sigma -- this is why m_e can NEVER be a precision")
    print("     prediction at bridge level: the 1/pi factor must be derived")
    print("     EXACTLY, not to 2%, or the row must be demoted (ledger M11).")
    print("   * 'floor sigma' adds the stated 1.5% theory error; even then the")
    print("     electron factor is the one real tension while up/down pass")
    print("     trivially because their experimental errors are ~20%.")
    print()


if __name__ == "__main__":
    main()
