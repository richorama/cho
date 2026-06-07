"""
Renormalization-scale audit for the CHO mass relations.
=======================================================

The CHO mass relations are compared to measured masses, but a mass ratio is a
renormalization-scheme/scale dependent statement. This module classifies every
CHO mass relation as either

  * RG-INVARIANT (1-loop): the QCD anomalous dimensions cancel, so the relation
    holds at any scale and no renormalization point need be quoted; or
  * SCALE-DEPENDENT: the QCD running does NOT cancel, so the relation is only
    true near one specific scale, which must be stated.

It then demonstrates the scale dependence of the one genuinely scale-dependent
headline relation, m_b/m_tau = 7/3 (ledger M5), by running m_b across scales.

Background (1-loop): a quark mass runs as m(mu2)/m(mu1) = (as(mu2)/as(mu1))^(g0/b0)
with a UNIVERSAL g0/b0, so any ratio of two SAME-sector quark masses is
RG-invariant. Lepton masses run only under QED (negligible here), so a
quark/lepton ratio inherits the quark's QCD running and is NOT invariant.

Reuses the 1-loop machinery in compute/rg_running.py. No scipy.
"""
import math

import rg_running as rg


# Reference MSbar masses at their own scales / PDG anchors (GeV).
M_T = 172.76
M_B = 4.18      # m_b(m_b)
M_C = 1.27      # m_c(m_c)
M_S = 0.0934    # m_s(2 GeV)
M_TAU = 1.77686
M_MU = 0.105658


def _alpha_s_at(mu):
    """1-loop as(mu) anchored at M_Z, with crude flavour thresholds."""
    a_mb = rg.alpha_s_running(rg.M_B_MSBAR, rg.M_Z, rg.ALPHA_S_MZ, nf=5)
    if mu >= rg.M_B_MSBAR:
        return rg.alpha_s_running(mu, rg.M_Z, rg.ALPHA_S_MZ, nf=5)
    return rg.alpha_s_running(mu, rg.M_B_MSBAR, a_mb, nf=4)


def m_b_at(mu):
    """Run m_b(m_b) to scale mu (1-loop, nf=5 above m_b, nf=4 below)."""
    a_mb = rg.alpha_s_running(rg.M_B_MSBAR, rg.M_Z, rg.ALPHA_S_MZ, nf=5)
    if mu >= rg.M_B_MSBAR:
        return rg.mass_running(M_B, rg.M_B_MSBAR, mu, a_mb, nf=5)
    return rg.mass_running(M_B, rg.M_B_MSBAR, mu, a_mb, nf=4)


# (label, formula, CHO value, classification, note)
RELATIONS = [
    ("m_c/m_t = eps0^2", M_C / M_T, math.pi / 432, "RG-INVARIANT",
     "up/up quark ratio -> QCD running cancels"),
    ("m_s/m_b = 3 eps0^2", M_S / M_B, 3 * math.pi / 432, "RG-INVARIANT",
     "down/down quark ratio -> QCD running cancels"),
    ("m_mu/m_tau = 8 eps0^2", M_MU / M_TAU, 8 * math.pi / 432, "RG-INVARIANT",
     "lepton/lepton ratio -> only tiny QED running"),
    ("m_s m_t/(m_b m_c) = 3", (M_S * M_T) / (M_B * M_C), 3.0, "RG-INVARIANT",
     "(m_s/m_b)(m_t/m_c): each factor a same-sector quark ratio"),
    ("m_mu m_b/(m_tau m_s) = 8/3", (M_MU * M_B) / (M_TAU * M_S), 8 / 3,
     "RG-INVARIANT",
     "(m_mu/m_tau)(m_b/m_s): lepton ratio x down-quark ratio, both cancel"),
    ("m_b/m_tau = 7/3", M_B / M_TAU, 7 / 3, "SCALE-DEPENDENT",
     "down-quark / lepton: QCD running of m_b does NOT cancel -> holds only near mu ~ m_b"),
]


def main():
    print("=" * 76)
    print("  CHO MASS-RELATION RENORMALIZATION-SCALE AUDIT")
    print("  A mass ratio is scheme/scale dependent unless the running cancels.")
    print("=" * 76)
    print(f"  {'Relation':<30}{'CHO':>9}{'obs':>9}{'err':>7}  classification")
    print("  " + "-" * 72)
    for label, obs, cho, cls, _note in RELATIONS:
        err = (cho - obs) / obs * 100
        print(f"  {label:<30}{cho:>9.4f}{obs:>9.4f}{err:>+6.1f}%  {cls}")
    print("  " + "-" * 72)
    print("  Notes:")
    for label, _obs, _cho, cls, note in RELATIONS:
        tag = "OK " if cls == "RG-INVARIANT" else "!! "
        print(f"   {tag}{label:<28} {note}")

    # Demonstrate the scale dependence of the one scale-dependent relation.
    print()
    print("  SCALE DEPENDENCE OF m_b/m_tau (m_tau ~ const under QCD):")
    print(f"  {'scale mu':<16}{'m_b(mu) GeV':>12}{'m_b/m_tau':>11}{'vs 7/3':>9}")
    print("  " + "-" * 48)
    target = 7.0 / 3.0
    scales = [
        ("m_b = 4.18 GeV", rg.M_B_MSBAR),
        ("2 GeV", 2.0),
        ("M_Z = 91 GeV", rg.M_Z),
        ("1e3 GeV", 1.0e3),
        ("1e16 GeV (GUT)", 1.0e16),
    ]
    best_label, best_dev = None, 1e9
    for name, mu in scales:
        mb = m_b_at(mu)
        ratio = mb / M_TAU
        dev = (ratio - target) / target * 100
        if abs(dev) < best_dev:
            best_dev, best_label = abs(dev), name
        print(f"  {name:<16}{mb:>12.3f}{ratio:>11.3f}{dev:>+8.1f}%")
    print("  " + "-" * 48)
    print(f"  -> 7/3 is closest at mu = {best_label} ({best_dev:.1f}% off);")
    print(f"     it drifts strongly with scale, so M5 must be quoted AT a scale.")
    print()
    print("  VERDICT: five of six headline mass relations are 1-loop RG-invariant")
    print("  and need no scale (their products pair like-sector ratios). Only")
    print("  m_b/m_tau = 7/3 (M5) is scale-dependent and must carry a stated")
    print("  matching scale (mu ~ m_b) -- this is a real open caveat, not a")
    print("  scale-free prediction. (NOTE: this 1-loop QCD treatment ignores")
    print("  the small QED/electroweak running of the lepton; the conclusion")
    print("  -- only the lone quark/lepton ratio is scale-sensitive -- is robust.)")
    print()


if __name__ == "__main__":
    main()
