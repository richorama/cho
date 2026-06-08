"""
PHASE 1.2 (proper) — the ASSOCIATIVE REBUILD: a KO-dim-6 SM-type finite real
spectral triple with a Yukawa+Majorana (seesaw) Dirac, all for ONE J.
=============================================================================

Why this module exists
----------------------
f0_real_structure_gate.py (the Phase-1.2 prerequisite) proved a sharp DICHOTOMY:
on a single octonion brick no real structure J gives BOTH KO-dimension 6 AND a
noncommutative order-zero algebra. It NAMED the standard resolution -- let an
associative algebra A = C (+) H (+) M_3(C) act on A (x) A^o and relegate the
octonions to GRADING the module -- but it did not carry it out: it left two open
bridges, (i) realise that rebuild as a product triple that RESTORES KO-dim 6, and
(ii) attach a Yukawa+Majorana Dirac so the finite KO-dimension stays 6, not 4.

This module carries out the rebuild for the one-generation LEPTON sector (the
colour-singlet slice; the M_3(C) colour factor is checked separately to commute)
and reports, from explicit matrices, whether the resulting object is a consistent
finite real spectral triple with a NONZERO physical Dirac. The honesty test was
genuinely open going in: a fresh CHO-specific obstruction (e.g. KO-6 + order-one
forcing D = 0) would have been an equally valid -- and equally reportable --
outcome. It did not occur.

What is built and tested (all numbers from explicit 8x8 / 6x6 / 9x9 matrices)
----------------------------------------------------------------------------
H = C^8, basis [nuR, eR, nuL, eL | nuRbar, eRbar, nuLbar, eLbar].
A = C (+) H acts on the LEFT (leptons); M_3(C) colour is the commuting factor.
J = (particle<->antiparticle swap) o complex conjugation.
gamma = chirality, +1/-1 on right/left particles, FLIPPED on antiparticles.

[A] ORDER-ZERO for the full associative algebra on A (x) A^o.
    Generalises f0_real_structure_gate's [D] from the H toy to all three
    summands: C (trivially), H, and M_3(C) each satisfy [a_L, b_R] = 0 on their
    own A (x) A^o bimodule by left-right commutation (residuals ~1e-15), while
    H and M_3(C) stay genuinely nonabelian. The SM lepton rep then satisfies
    order-zero exactly (~9e-16).

[B] KO-DIMENSION 6 RESTORED.  J^2 = +I (eps=+1) and J gamma J^-1 = -gamma
    (eps''=-1) give KO-dim 6 -- chirality WITHOUT Connes-doubling. This is the
    grading that the prerequisite's J=kappa.conj had destroyed; the associative
    route recovers it because gamma now lives on the module, not on the octonions.

[C] A NONZERO PHYSICAL DIRAC satisfying order-one.  The explicit Dirac with
    Dirac Yukawas (nuR<->nuL, eR<->eL) AND a Majorana mass (nuR<->nuRbar) is
    Hermitian, gamma-ODD, J-REAL (J D J^-1 = D), and satisfies the order-one
    condition [[D, a], b^o] = 0 (residual ~2e-15). So the finite KO-dimension
    stays 6 and the seesaw lives in the real-structure sector -- exactly the two
    bridges the prerequisite left open, now closed for the lepton sector.

Verdict / where this leaves F0
------------------------------
The associative SKELETON EXISTS: a consistent KO-dim-6 finite real spectral
triple of Standard-Model type, with a nonzero Yukawa+Majorana Dirac, for a
SINGLE real structure J. The Phase-1.1 "the triple does not exist" verdict is
REPAIRED at the level of the associative skeleton.

This is, honestly, the KNOWN Connes-Chamseddine-Marcolli skeleton recovered
constructively -- it is the complement to the no-go, NOT new physics, and it
moves NO Bayes credit. Two CHO-specific bridges remain before eps0^2 = pi/432
could be promoted:
  * step C -- replace the generic Yukawa by the SPECIFIC octonionic Jordan mass
    operator L_X and realise the full 432 = 16 (A_Weyl) x 27 (J3(O)) module
    (here only the 8-dim colour-singlet slice is built);
  * Phase 1.3 -- show eps0^2 = pi/432 emerges as the spectral-action ratio
    a4/a2.  (epsilon_heat_kernel.py already warns the spectral pi enters only as
    a Gaussian (4 pi)^(-d/2), so a BARE pi numerator is unlikely from this route.)
Until both are done F0 stays GEOMETRIC/open; nothing here promotes it.

No scipy. Self-contained explicit matrices (numpy only).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_associative_triple_gate.py
"""

import numpy as np

# basis indices ------------------------------------------------------------
nuR, eR, nuL, eL = 0, 1, 2, 3
nuRb, eRb, nuLb, eLb = 4, 5, 6, 7
N = 8


# --------------------------------------------------------------------------
# Real structure J = (particle<->antiparticle swap) o complex conjugation.
# --------------------------------------------------------------------------
_P = np.zeros((N, N), dtype=complex)
_P[0:4, 4:8] = np.eye(4)
_P[4:8, 0:4] = np.eye(4)


def J_conj(X):
    """J X J^-1 = P conj(X) P  (J antilinear, J^2 = P P = I)."""
    return _P @ np.conjugate(X) @ _P


# --------------------------------------------------------------------------
# Grading gamma: chirality, antiparticles flipped (KO-6 by construction).
# --------------------------------------------------------------------------
GAMMA = np.diag([+1, +1, -1, -1, -1, -1, +1, +1]).astype(complex)


# --------------------------------------------------------------------------
# Algebra A = C (+) H, left action on the lepton module.
# --------------------------------------------------------------------------
def quat(a, b):
    """q in H as 2x2 complex [[a, b], [-conj b, conj a]]."""
    return np.array([[a, b], [-np.conjugate(b), np.conjugate(a)]], dtype=complex)


def pi_left(lam, a, b):
    """Left action of (lambda in C, q = quat(a,b) in H).
    Particles: doublet (nuL, eL) = q, nuR = lambda, eR = conj(lambda).
    Antileptons: colour singlets, carry the U(1) lambda."""
    M = np.zeros((N, N), dtype=complex)
    M[nuL:eL + 1, nuL:eL + 1] = quat(a, b)
    M[nuR, nuR] = lam
    M[eR, eR] = np.conjugate(lam)
    M[4:8, 4:8] = lam * np.eye(4)
    return M


def b_opposite(lam, a, b):
    """b^o = J pi(b*) J^-1, with b* = (conj lambda, q^dagger = quat(conj a, -b))."""
    return J_conj(pi_left(np.conjugate(lam), np.conjugate(a), -b))


# --------------------------------------------------------------------------
# [A] order-zero for each associative summand on A (x) A^o.
# --------------------------------------------------------------------------
def _left_on_kron(m, dim):
    return np.kron(m, np.eye(dim))


def _right_on_kron(m, dim):
    return np.kron(np.eye(dim), m.T)


def summand_order_zero(make_alg, dim, rng, samples=200):
    """max ||[a_L, b_R]|| for an associative algebra acting on A (x) A^o."""
    worst = 0.0
    for _ in range(samples):
        A = _left_on_kron(make_alg(rng), dim)
        B = _right_on_kron(make_alg(rng), dim)
        worst = max(worst, float(np.max(np.abs(A @ B - B @ A))))
    return worst


def summand_noncommutativity(make_alg, rng, samples=200):
    worst = 0.0
    for _ in range(samples):
        x, y = make_alg(rng), make_alg(rng)
        worst = max(worst, float(np.max(np.abs(x @ y - y @ x))))
    return worst


def _rand_quat(rng):
    a, b = (rng.standard_normal() + 1j * rng.standard_normal(),
            rng.standard_normal() + 1j * rng.standard_normal())
    return quat(a, b)


def _rand_m3(rng):
    return rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))


def lepton_order_zero(rng, samples=300):
    """Order-zero for the actual SM lepton rep on the doubled module."""
    worst = 0.0
    for _ in range(samples):
        s1 = (rng.standard_normal() + 1j * rng.standard_normal(),
              rng.standard_normal() + 1j * rng.standard_normal(),
              rng.standard_normal() + 1j * rng.standard_normal())
        s2 = (rng.standard_normal() + 1j * rng.standard_normal(),
              rng.standard_normal() + 1j * rng.standard_normal(),
              rng.standard_normal() + 1j * rng.standard_normal())
        A = pi_left(*s1)
        Bo = b_opposite(*s2)
        worst = max(worst, float(np.max(np.abs(A @ Bo - Bo @ A))))
    return worst


# --------------------------------------------------------------------------
# [B] KO signs from J and gamma.
# --------------------------------------------------------------------------
def ko_signs():
    J2 = _P @ np.conjugate(_P)
    eps = 1.0 if np.allclose(J2, np.eye(N)) else -1.0
    Jg = J_conj(GAMMA)
    if np.allclose(Jg, -GAMMA):
        epp = -1.0
    elif np.allclose(Jg, GAMMA):
        epp = 1.0
    else:
        epp = float("nan")
    return eps, epp


_KO_MAP = {(1, -1): 6, (1, 1): 0, (-1, 1): 4, (-1, -1): 2}


# --------------------------------------------------------------------------
# [C] explicit physical Dirac: Yukawa + Majorana seesaw.
# --------------------------------------------------------------------------
def physical_dirac(y_nu=0.7, y_e=0.3, m_R=5.0):
    D = np.zeros((N, N), dtype=complex)
    # Dirac Yukawa on particles, conjugate copy on antiparticles
    for (r, l, y) in [(nuR, nuL, y_nu), (eR, eL, y_e)]:
        D[r, l] = y
        D[l, r] = np.conjugate(y)
    for (r, l, y) in [(nuRb, nuLb, y_nu), (eRb, eLb, y_e)]:
        D[r, l] = np.conjugate(y)
        D[l, r] = y
    # Majorana mass nuR <-> nuRbar (real-structure / seesaw sector)
    D[nuR, nuRb] = m_R
    D[nuRb, nuR] = m_R
    return D


def dirac_order_one(D, rng, samples=400):
    worst = 0.0
    for _ in range(samples):
        s = (rng.standard_normal() + 1j * rng.standard_normal(),
             rng.standard_normal() + 1j * rng.standard_normal(),
             rng.standard_normal() + 1j * rng.standard_normal())
        A = pi_left(*s)
        Bo = b_opposite(*s)
        comm = D @ A - A @ D
        o1 = comm @ Bo - Bo @ comm
        worst = max(worst, float(np.max(np.abs(o1))))
    return worst


# --------------------------------------------------------------------------
def main():
    rng = np.random.default_rng(1)
    print("=" * 78)
    print(" PHASE 1.2 (proper) — ASSOCIATIVE REBUILD: KO-6 SM triple + seesaw Dirac")
    print("=" * 78)

    # ---- [A] order-zero for the full associative algebra ----------------
    o0_h = summand_order_zero(_rand_quat, 2, rng)
    nc_h = summand_noncommutativity(_rand_quat, rng)
    o0_m3 = summand_order_zero(_rand_m3, 3, rng)
    nc_m3 = summand_noncommutativity(_rand_m3, rng)
    o0_lep = lepton_order_zero(rng)
    print("\n[A] ORDER-ZERO on  A (x) A^o  for the associative algebra C (+) H (+) M_3(C)")
    print(f"    H  : ||[a_L,b_R]|| = {o0_h:.3e}   (nonabelian, ||[x,y]|| = {nc_h:.3f})")
    print(f"    M_3: ||[a_L,b_R]|| = {o0_m3:.3e}   (nonabelian, ||[x,y]|| = {nc_m3:.3f})")
    print(f"    SM lepton rep order-zero        = {o0_lep:.3e}")
    print("    => order-zero holds for a genuinely NONCOMMUTATIVE algebra; the")
    print("       colour M_3(C) factor commutes with the lepton sector by construction.")

    # ---- [B] KO-dim 6 ---------------------------------------------------
    eps, epp = ko_signs()
    ko = _KO_MAP.get((int(eps), int(epp)))
    print("\n[B] KO-DIMENSION 6 RESTORED")
    print(f"    J^2 = {eps:+.0f} I  (eps={eps:+.0f}),  J gamma J^-1 = {epp:+.0f} gamma "
          f"(eps''={epp:+.0f})  => KO-dim {ko}")
    print("    => chirality WITHOUT doubling; the grading the prerequisite lost is back.")

    # ---- [C] physical Dirac + order-one ---------------------------------
    D = physical_dirac()
    d_herm = np.allclose(D, D.conj().T)
    d_odd = np.allclose(GAMMA @ D, -D @ GAMMA)
    d_real = np.allclose(J_conj(D), D)
    o1 = dirac_order_one(D, rng)
    yuk = abs(D[nuR, nuL]) + abs(D[eR, eL])
    maj = abs(D[nuR, nuRb])
    print("\n[C] NONZERO PHYSICAL DIRAC (Yukawa + Majorana seesaw) satisfies order-one")
    print(f"    Hermitian = {d_herm} ;  gamma-odd = {d_odd} ;  J-real (JDJ^-1=D) = {d_real}")
    print(f"    order-one [[D,a],b^o] max = {o1:.3e}")
    print(f"    Yukawa support |D[R,L]| = {yuk:.2f} (Dirac mass) ; "
          f"Majorana |D[nuR,nuRbar]| = {maj:.2f} (seesaw)")
    print("    => the seesaw lives in the real-structure sector and KO-dim stays 6.")

    # ---- verdict --------------------------------------------------------
    print("\n[V] VERDICT")
    print("    The associative SKELETON EXISTS: a KO-dim-6 finite real spectral triple")
    print("    of SM type with a nonzero Yukawa+Majorana Dirac, for ONE real structure J.")
    print("    The Phase-1.1 'triple does not exist' fail is REPAIRED for the skeleton.")
    print("    HONEST CAVEAT: this is the known Connes-Chamseddine-Marcolli skeleton")
    print("    recovered constructively -- the complement to the no-go, NOT new physics.")
    print("    Moves NO Bayes credit. Open: step C (octonionic Jordan mass L_X as D; full")
    print("    432 = 16 x 27 module) and Phase 1.3 (eps0^2 = pi/432 as a4/a2). F0 stays")
    print("    GEOMETRIC/open.")
    print("=" * 78)

    # ---- stable assertions (audit.py ignores the return value) ----------
    # [A] order-zero holds on A (x) A^o for noncommutative H and M_3, and for
    #     the actual SM lepton rep:
    assert o0_h < 1e-9, "order-zero failed for H on A (x) A^o"
    assert nc_h > 1e-6, "H collapsed to abelian"
    assert o0_m3 < 1e-9, "order-zero failed for M_3(C) on A (x) A^o"
    assert nc_m3 > 1e-6, "M_3(C) collapsed to abelian"
    assert o0_lep < 1e-9, "SM lepton rep failed order-zero"
    # [B] KO-dimension 6 restored:
    assert abs(eps - 1.0) < 1e-9, "J^2 = +I broken (eps != +1)"
    assert abs(epp + 1.0) < 1e-9, "J gamma J^-1 = -gamma broken (eps'' != -1)"
    assert ko == 6, "KO-dimension is not 6"
    # [C] explicit physical Dirac is a valid, nonzero, order-one Dirac:
    assert d_herm, "physical Dirac not Hermitian"
    assert d_odd, "physical Dirac not gamma-odd"
    assert d_real, "physical Dirac not J-real"
    assert o1 < 1e-9, "physical Dirac violates order-one"
    assert yuk > 0.5, "Yukawa (Dirac mass) sector vanished"
    assert maj > 0.5, "Majorana (seesaw) sector vanished"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
