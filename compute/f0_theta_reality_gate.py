"""
F0 THETA-REALITY GATE — KO-6 reality forces theta = 0 (the THIRD converging-negative).
=====================================================================================

Why this module exists
----------------------
After the Phase-1 closeout, the question was raised: can a *new* idea close the
gate that Phase 1.3 (heat-kernel a4/a2) and Phase 1.4 (spectrum ratios) left open?
The most promising "mind-bending" route was a TOPOLOGICAL one, and it is genuinely
DIFFERENT from the two already refuted:

  pi/432 = theta / dim , with theta = pi * nu , nu in {0,1} a Z2 index QUANTIZED
  by the real structure J (the KO-6 reality), and CHO sitting in the nu = 1 class.

This is not the heat-kernel a4/a2 that Phase 1.3 refuted: a theta-term is
NON-PERTURBATIVE -- it never appears in the rational Seeley-DeWitt moments Tr(D^2k)
-- so the rational-moment kill of 1.3 does not touch it. A first-power pi in the
NUMERATOR (which pi/432 has) is exactly the signature of a holonomy/topological
quantity rather than an analytic one, so this was the natural place to look.

This gate RECORDS the outcome so the route is never re-attempted: it falls on the
NEGATIVE side, cleanly and robustly. KO-6 reality forces theta = 0.

What is computed (three independent topological invariants of the genuine D)
---------------------------------------------------------------------------
On the genuine 216-dim octonionic KO-6 Dirac D (the step-C triple), all three
natural sources of a theta = pi vanish, for every seed and with the Majorana
sector on or off:

  [A] SPECTRAL-ASYMMETRY (eta-invariant) theta. The parity-anomaly / APS angle is
      theta_eta = pi * eta(D) with eta = #(lambda>0) - #(lambda<0). But D is
      gamma-ODD (gamma D = -D gamma, residual 0), so its spectrum is EXACTLY
      +/- symmetric (108 / 108, no zero modes) and eta = 0 identically. The very
      grading that DEFINES chirality forces the spectral-asymmetry theta to vanish.

  [B] CHIRAL mod-2 INDEX. The KO-6 real index is nu = dim ker(D: H+ -> H-) mod 2.
      The chiral block is FULL RANK (rank 108, zero kernel), so nu = 0 -- there are
      no protected zero modes to carry a Z2 index.

  [C] KRAMERS / FU-KANE Z2. The time-reversal topological-insulator theta = pi
      invariant requires a Kramers structure J^2 = -1 (symplectic / class AII). But
      KO-6 has J^2 = +1 (the REAL class), so this Z2 is not even DEFINED here.

Hence theta = pi * nu = 0, and the candidate pi*nu/432 = 0 != pi/432 = 0.00727221.

The reading (two-sided; moves no credit)
----------------------------------------
The topological-theta route is CLOSED -- a THIRD independent converging-negative,
joining the Phase-1.3 prefactor and the Phase-1.4 ratios. All three localise the
remaining F0 gap to the SAME object and for the SAME reason: each is KINEMATICS /
TOPOLOGY, and the gap is DYNAMICS. The pi that the program legitimately has is the
Berry half-solid-angle (1/2)(2 pi) = pi -- a holonomy of the CONTINUOUS vacuum-
selection Bloch sphere, a property of the (still-missing) dynamics that picks the
vacuum direction, NOT a topological invariant of the finite operator D.

So pi/432 is not a theta-angle of D either; it stays the Berry/Schur GEOMETRIC
quantity it always was. F0 stays GEOMETRIC/open -- not demoted (the geometric
reading is untouched), not promoted (no new earn-path opened). No Bayes credit
moves; the scoreboard ladder (-21.3 / -3.2 / +5.6 / +36.2) and the frozen registry
are untouched. Scope is honest: this refutes theta = pi for THIS finite KO-6
triple via its three natural sources; it is not a claim about every conceivable
construction -- but it closes the concrete route that was proposed.

No scipy. Reuses f0_octonionic_yukawa_gate (the step-C triple builder) and
epsilon_weyl_isomorphism (the Jordan product tensor).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_theta_reality_gate.py
"""

import numpy as np

import f0_octonionic_yukawa_gate as C
from epsilon_weyl_isomorphism import jordan_product_tensor


PI = np.pi
TARGET = PI / 432.0          # eps0^2 = pi/432, the number a theta-angle would have to give
TOL = 1.0e-9
_T = jordan_product_tensor()

# (seed, majorana, label) — physical point plus robustness variations.
SEEDS = [
    ((1.0, 0.6, 0.3), (0.2, 0.0, 0.0), "physical"),
    ((0.8, 0.6, 0.4), (0.2, 0.0, 0.0), "second seed"),
    ((1.0, 0.6, 0.3), (0.0, 0.0, 0.0), "no Majorana"),
    ((1.0, 0.6, 0.3), (0.5, 0.3, 0.1), "full Majorana"),
]


# --------------------------------------------------------------------------
def build_triple(seed=(1.0, 0.6, 0.3), maj=(0.2, 0.0, 0.0)):
    """(GAMMA, D, UP) for the genuine 216-dim octonionic KO-6 step-C triple."""
    L_X = C.octonionic_yukawa(_T, *seed)
    M_maj = C.octonionic_yukawa(_T, *maj)
    GAMMA, D, UP = C.build_product(C.yukawa_coupling(), C.majorana_coupling(),
                                   L_X, M_maj)
    return GAMMA, D, UP


def eta_invariant(D):
    """Spectral asymmetry eta = #(lambda>0) - #(lambda<0); gamma-odd => 0.

    Returns (eta, npos, nneg, nzero, pm_sym) where pm_sym is the max deviation
    from exact +/- symmetry of the spectrum (0 for a genuinely odd D)."""
    ev = np.linalg.eigvalsh((D + D.conj().T) / 2.0)
    npos = int(np.sum(ev > TOL))
    nneg = int(np.sum(ev < -TOL))
    nzero = int(np.sum(np.abs(ev) <= TOL))
    pm_sym = float(np.max(np.abs(np.sort(ev) + np.sort(-ev)[::-1])))
    return npos - nneg, npos, nneg, nzero, pm_sym


def chiral_mod2_index(GAMMA, D):
    """nu = dim ker(D: H+ -> H-) mod 2; full-rank D => 0. Returns (nu, ker, rank)."""
    gv, gvec = np.linalg.eigh(GAMMA)
    plus = gvec[:, gv > 0.0]
    minus = gvec[:, gv < 0.0]
    block = minus.conj().T @ D @ plus          # the H+ -> H- chiral block
    s = np.linalg.svd(block, compute_uv=False)
    ker_dim = int(np.sum(s <= 1e-7))
    rank = int(np.sum(s > 1e-7))
    return ker_dim % 2, ker_dim, rank


def kramers_available(UP):
    """KO-6 has J^2 = +1 (real class) => no Kramers/Fu-Kane Z2 (needs J^2 = -1).

    Returns (j2_is_plus, pfaffian_available)."""
    n = UP.shape[0]
    J2 = UP @ np.conjugate(UP)
    j2_plus = bool(np.allclose(J2, np.eye(n)))
    return j2_plus, (not j2_plus)


# --------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("F0 THETA-REALITY GATE: does KO-6 reality quantize a theta = pi for D?")
    print("=" * 78)
    print("  candidate identity:  pi/432 = theta/dim , theta = pi*nu , nu in {0,1}")
    print("  (a NON-perturbative theta-term -- a different channel from 1.3's a4/a2)")
    print()
    print(f"  {'case':<14} {'KO':<4} {'eta':<5} {'nu':<4} {'J^2=+1':<7}"
          f" {'+/-sym':<9} {'theta':<7} {'pi*nu/432'}")
    print("  " + "-" * 72)

    results = []
    for seed, maj, label in SEEDS:
        GAMMA, D, UP = build_triple(seed, maj)
        n = D.shape[0]

        eps, epp = C.ko_signs(GAMMA, UP)
        ko = C._KO_MAP.get((int(eps), int(epp)), -1)

        # honesty: the operator really is the genuine self-adjoint, gamma-odd, J-real D
        herm = float(np.max(np.abs(D - D.conj().T)))
        godd = float(np.max(np.abs(GAMMA @ D + D @ GAMMA)))
        jreal = float(np.max(np.abs(UP @ np.conjugate(D) @ UP - D)))

        eta, npos, nneg, nzero, pm_sym = eta_invariant(D)
        nu, ker, rank = chiral_mod2_index(GAMMA, D)
        j2_plus, pfaff = kramers_available(UP)
        theta = PI * nu
        cand = PI * nu / 432.0

        print(f"  {label:<14} {ko:<4d} {eta:<5d} {nu:<4d} {str(j2_plus):<7}"
              f" {pm_sym:<9.1e} {theta:<7.4f} {cand:.8f}")

        results.append(dict(label=label, ko=ko, herm=herm, godd=godd, jreal=jreal,
                            eta=eta, nzero=nzero, pm_sym=pm_sym, nu=nu, ker=ker,
                            rank=rank, j2_plus=j2_plus, pfaff=pfaff, theta=theta,
                            cand=cand, n=n))

    print()
    print("  [A] eta-invariant theta : gamma D = -D gamma forces +/- symmetric")
    print("      spectrum (108/108, no zero modes) -> eta = 0 identically.")
    print("  [B] chiral mod-2 index  : the H+ -> H- block is full rank (108) ->")
    print("      zero kernel -> nu = 0, no protected Z2.")
    print("  [C] Kramers/Fu-Kane Z2  : KO-6 has J^2 = +1 (real class) -> the")
    print("      time-reversal theta = pi invariant is not even defined (needs J^2 = -1).")
    print()
    print("  VERDICT: theta = 0 across all seeds and Majorana settings -- the")
    print("  topological-theta route is CLOSED, a THIRD independent converging-")
    print("  negative (with the 1.3 prefactor and the 1.4 ratios). All three are")
    print("  KINEMATICS/TOPOLOGY; the gap is DYNAMICS. pi/432 is not a theta-angle")
    print("  of D -- it stays the Berry half-solid-angle (1/2)(2 pi) = pi holonomy of")
    print("  the CONTINUOUS vacuum sphere, a property of the missing action, not of D.")
    print("  F0 stays GEOMETRIC/open; no Bayes credit moves; scoreboard + registry")
    print("  untouched.")
    print("=" * 78)

    # ---- stable assertions (audit.py ignores the return value) ----------
    assert TARGET > 1e-3, "sanity: pi/432 is the nonzero number a theta would have to give"
    for r in results:
        # the operator is genuinely the self-adjoint, gamma-odd, J-real KO-6 Dirac
        assert r["ko"] == 6, f"{r['label']}: not KO-dim 6"
        assert r["herm"] < TOL and r["godd"] < TOL and r["jreal"] < TOL, \
            f"{r['label']}: D is not the genuine self-adjoint gamma-odd J-real Dirac"
        # [A] spectral-asymmetry theta vanishes (forced by gamma-oddness)
        assert r["eta"] == 0, f"{r['label']}: eta-invariant is nonzero (theta_eta != 0!)"
        assert r["pm_sym"] < TOL, f"{r['label']}: spectrum not +/- symmetric"
        assert r["nzero"] == 0, f"{r['label']}: unexpected zero modes"
        # [B] chiral mod-2 index vanishes (full rank)
        assert r["nu"] == 0, f"{r['label']}: chiral mod-2 index is nontrivial (nu=1)!"
        # [C] no Kramers Z2 in the real (J^2=+1) class
        assert r["j2_plus"] and not r["pfaff"], \
            f"{r['label']}: unexpected Kramers (J^2=-1) structure"
        # the refutation: theta = 0, so pi*nu/432 = 0 misses pi/432 by the full target
        assert r["theta"] == 0.0, f"{r['label']}: theta is not zero"
        assert abs(r["cand"] - TARGET) > 1e-3, \
            f"{r['label']}: pi*nu/432 unexpectedly near pi/432"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
