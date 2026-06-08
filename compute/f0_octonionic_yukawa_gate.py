"""
PHASE 1.2 step C — the OCTONIONIC YUKAWA: L_X enters the KO-6 triple ungraded,
closing the Phase-1.1 doubling obstruction, but the axioms do NOT force it.
=============================================================================

Why this module exists
----------------------
f0_associative_triple_gate (step B) built the associative KO-6 skeleton with a
GENERIC Yukawa+Majorana Dirac. Step C asks the CHO-specific follow-on: take the
SPECIFIC octonionic Jordan mass operator L_X (Jordan left-multiplication on
J3(O) = R^27, the operator whose spectrum is the averaging law
{a,b,c} u {(a+b)/2,(a+c)/2,(b+c)/2}) and ask (i) whether it slots into the
consistent KO-6 triple, and (ii) -- decisively -- whether the spectral-triple
axioms CONSTRAIN its texture or leave it free. The honest answer was genuinely
open: a fresh obstruction (e.g. order-one forcing L_X to a degenerate texture)
would have been an equally valid, equally reportable outcome. What the numbers
actually show is a precise two-sided result.

The faithful SM finite geometry (not a contrivance)
---------------------------------------------------
  H = H_charge (x) H_flavour = C^8 (x) C^27  (the step-B lepton slice (x) J3(O))
  - charge factor = step B's KO-6 lepton triple (chirality grading gamma1, J1)
  - flavour factor = J3(O) = C^27 as UNGRADED multiplicity (gamma_F = I27,
    real structure J_F = complex conjugation -> KO-0)
  - the Yukawa is  K_Yuk (x) L_X : the charge L<->R coupling K_Yuk (which is
    gamma1-ODD because it flips chirality) tensored with the octonionic
    generation matrix L_X. Because chirality is carried by the CHARGE factor,
    L_X enters UNGRADED.
  gamma = gamma1 (x) I27      (KO-6 (x) KO-0 = KO-6)
  J     = J1 (x) conj
  D     = K_Yuk (x) L_X + K_Maj (x) M_maj   (Yukawa + Majorana charge couplings,
          both gamma1-odd and J1-real; L_X, M_maj real-symmetric octonionic ops)

What is tested (all numbers from explicit 8x8 / 27x27 / 216x216 matrices)
------------------------------------------------------------------------
[A] L_X IS the octonionic operator: its spectrum is the Jordan averaging law
    for the seed (1, 0.6, 0.3) -- three singlets {1, 0.6, 0.3} and three octets
    {0.8, 0.65, 0.45} (mult 8 each), 27 total. Self-adjoint to 0.

[B] THE DOUBLING OBSTRUCTION IS DISSOLVED. The Phase-1.1 gate found L_X
    chirality-EVEN and concluded it needs particle/antiparticle doubling, which
    sent the finite KO-dim 6 (x) 6 -> 4. Here L_X needs NO doubling: once the
    chirality grading sits in the charge factor (gamma1) and L_X is the UNGRADED
    generation multiplier in the gamma1-odd Yukawa block K_Yuk (x) L_X, the
    product Dirac is gamma-odd automatically and the triple is KO-6. Verified:
    D self-adjoint, gamma^2 = I, gamma D = -D gamma, J D J^-1 = D, and KO signs
    (eps=+1, eps''=-1) -> KO-dim 6, with order-zero (~1e-15) and order-one
    (~1e-15) BOTH holding for the genuine octonionic D.

[C] BUT THE AXIOMS DO NOT FORCE THE YUKAWA. Order-one factors through the charge
    sector: each charge coupling tensored with a RANDOM Hermitian flavour
    operator still satisfies order-one (K_Yuk (x) random ~1e-14, K_Maj (x) random
    = 0). The gauge algebra acts on the charge factor and sees the flavour factor
    as pure multiplicity, so [[D, a], b^o] = 0 holds for ANY self-adjoint flavour
    operator, not just L_X. The octonionic texture is therefore ADMISSIBLE but
    NOT FORCED by the spectral-triple axioms.

Verdict / where this leaves F0
------------------------------
Two-sided and honest. POSITIVE: step C closes the second Phase-1.1 obstruction
(the Yukawa doubling that broke KO-6) -- the octonionic L_X lives in a consistent
KO-6 triple, ungraded, carrying its averaging-law masses into D's spectrum.
SOBERING: the triple axioms (order-zero, order-one, KO-6) are NECESSARY but do
NOT pin the Yukawa; any self-adjoint flavour operator passes them. Hence the CHO
predictive content -- that the masses follow the octonionic averaging law -- is
NOT secured by the existence of the triple. It must come from the spectral
ACTION Tr f(D/Lambda) (Phase 1.3), which selects D dynamically. epsilon_heat_kernel
already warns the spectral pi enters only via the Gaussian (4 pi)^(-d/2), so the
decisive Phase-1.3 test is more likely to REFUTE than confirm eps0^2 = pi/432 as
the a4/a2 ratio. This gate moves NO Bayes credit: F0 stays GEOMETRIC/open.

No scipy. Reuses f0_associative_triple_gate (step-B charge sector),
f0_spectral_triple_gate (jordan_left_mult, diag_seed) and epsilon_weyl_isomorphism
(jordan_product_tensor).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_octonionic_yukawa_gate.py
"""

import numpy as np

import f0_associative_triple_gate as B
from f0_spectral_triple_gate import jordan_left_mult, diag_seed
from epsilon_weyl_isomorphism import jordan_product_tensor


# charge basis indices (from step B)
nuR, eR, nuL, eL = 0, 1, 2, 3
nuRb, eRb, nuLb, eLb = 4, 5, 6, 7
NC = 8
NF = 27


# --------------------------------------------------------------------------
# Octonionic Jordan Yukawa L_X (real-symmetric, averaging-law spectrum).
# --------------------------------------------------------------------------
def octonionic_yukawa(T, a, b, c):
    LX = jordan_left_mult(T, diag_seed(a, b, c))
    return 0.5 * (LX + LX.T)


def averaging_law_set(a, b, c):
    """The expected {singlets} and {octets} of L_X for seed diag(a,b,c)."""
    singlets = sorted({round(a, 6), round(b, 6), round(c, 6)})
    octets = sorted({round((a + b) / 2, 6), round((a + c) / 2, 6),
                     round((b + c) / 2, 6)})
    return singlets, octets


def spectrum_multiplicities(M, decimals=6):
    ev = np.linalg.eigvalsh(0.5 * (M + M.conj().T))
    vals, counts = np.unique(np.round(ev, decimals), return_counts=True)
    return dict(zip(vals.tolist(), counts.tolist()))


# --------------------------------------------------------------------------
# Charge-sector couplings (step-B structure, unit weights).
# --------------------------------------------------------------------------
def _E(i, j):
    M = np.zeros((NC, NC), dtype=complex)
    M[i, j] = 1.0
    return M


def yukawa_coupling():
    """L<->R coupling on particles AND antiparticles (gamma1-odd, J1-real)."""
    return (_E(nuR, nuL) + _E(nuL, nuR) + _E(eR, eL) + _E(eL, eR)
            + _E(nuRb, nuLb) + _E(nuLb, nuRb) + _E(eRb, eLb) + _E(eLb, eRb))


def majorana_coupling():
    """particle<->antiparticle (nuR<->nuRbar) coupling (gamma1-odd, J1-real)."""
    return _E(nuR, nuRb) + _E(nuRb, nuR)


def _J1c(X):
    return B._P @ np.conjugate(X) @ B._P


def coupling_is_valid(K):
    """(Hermitian, gamma1-odd, J1-real) for a charge coupling."""
    herm = np.allclose(K, K.conj().T)
    odd = np.allclose(B.GAMMA @ K, -K @ B.GAMMA)
    real1 = np.allclose(_J1c(K), K)
    return herm, odd, real1


# --------------------------------------------------------------------------
# Product triple and axiom residuals.
# --------------------------------------------------------------------------
def build_product(K_Yuk, K_Maj, L_X, M_maj):
    I27 = np.eye(NF, dtype=complex)
    GAMMA = np.kron(B.GAMMA, I27)
    D = np.kron(K_Yuk, L_X) + np.kron(K_Maj, M_maj)
    UP = np.kron(B._P, I27)          # linear part of J = (P (x) I) . conj
    return GAMMA, D, UP


def _Jp(UP, X):
    return UP @ np.conjugate(X) @ UP


def ko_signs(GAMMA, UP):
    n = GAMMA.shape[0]
    J2 = UP @ np.conjugate(UP)
    eps = 1.0 if np.allclose(J2, np.eye(n)) else -1.0
    JgJ = _Jp(UP, GAMMA)
    if np.allclose(JgJ, -GAMMA):
        epp = -1.0
    elif np.allclose(JgJ, GAMMA):
        epp = 1.0
    else:
        epp = float("nan")
    return eps, epp


_KO_MAP = {(1, -1): 6, (1, 1): 0, (-1, 1): 4, (-1, -1): 2}


def _algebra_samples(rng, n):
    I27 = np.eye(NF, dtype=complex)
    out = []
    for _ in range(n):
        s = (rng.standard_normal() + 1j * rng.standard_normal(),
             rng.standard_normal() + 1j * rng.standard_normal(),
             rng.standard_normal() + 1j * rng.standard_normal())
        a = np.kron(B.pi_left(*s), I27)
        bo = np.kron(B.b_opposite(*s), I27)
        out.append((a, bo))
    return out


def order_zero_residual(rng, n=120):
    return max(float(np.max(np.abs(a @ bo - bo @ a)))
               for a, bo in _algebra_samples(rng, n))


def order_one_residual(D, rng, n=120):
    worst = 0.0
    for a, bo in _algebra_samples(rng, n):
        comm = D @ a - a @ D
        worst = max(worst, float(np.max(np.abs(comm @ bo - bo @ comm))))
    return worst


def coupling_order_one(Kc, rng, n=120):
    """Order-one contribution of one charge coupling tensored with a RANDOM
    Hermitian flavour operator. ~0 => the coupling leaves flavour FREE."""
    F = rng.standard_normal((NF, NF)) + 1j * rng.standard_normal((NF, NF))
    F = F + F.conj().T
    Dc = np.kron(Kc, F)
    worst = 0.0
    for a, bo in _algebra_samples(rng, n):
        comm = Dc @ a - a @ Dc
        worst = max(worst, float(np.max(np.abs(comm @ bo - bo @ comm))))
    return worst


# --------------------------------------------------------------------------
def main():
    rng = np.random.default_rng(2)
    T = jordan_product_tensor()
    seed = (1.0, 0.6, 0.3)
    L_X = octonionic_yukawa(T, *seed)
    M_maj = octonionic_yukawa(T, 0.2, 0.0, 0.0)

    print("=" * 78)
    print(" PHASE 1.2 step C — OCTONIONIC YUKAWA L_X in the KO-6 triple")
    print("=" * 78)

    # ---- [A] L_X is the octonionic operator (averaging-law spectrum) -----
    lx_herm = float(np.max(np.abs(L_X - L_X.conj().T)))
    mult = spectrum_multiplicities(L_X)
    singlets, octets = averaging_law_set(*seed)
    got_singlets = sorted(v for v, c in mult.items() if c == 1)
    got_octets = sorted(v for v, c in mult.items() if c == 8)
    print("\n[A] L_X IS the octonionic Jordan operator (seed diag(1, 0.6, 0.3))")
    print(f"    self-adjoint residual          : {lx_herm:.2e}")
    print(f"    singlets (mult 1)  got {got_singlets}  expected {singlets}")
    print(f"    octets   (mult 8)  got {got_octets}  expected {octets}")
    print("    => spectrum = averaging law {a,b,c} u {(a+b)/2,(a+c)/2,(b+c)/2}.")

    # ---- charge couplings ------------------------------------------------
    K_Yuk = yukawa_coupling()
    K_Maj = majorana_coupling()
    vy = coupling_is_valid(K_Yuk)
    vm = coupling_is_valid(K_Maj)
    print("\n    charge couplings: K_Yuk (Herm,odd,J1-real)="
          f"{vy}, K_Maj={vm}")

    # ---- [B] product triple: doubling obstruction dissolved -------------
    GAMMA, D, UP = build_product(K_Yuk, K_Maj, L_X, M_maj)
    n = GAMMA.shape[0]
    d_herm = np.allclose(D, D.conj().T)
    g_sq = np.allclose(GAMMA @ GAMMA, np.eye(n))
    d_odd = np.allclose(GAMMA @ D, -D @ GAMMA)
    d_real = np.allclose(_Jp(UP, D), D)
    eps, epp = ko_signs(GAMMA, UP)
    ko = _KO_MAP.get((int(eps), int(epp)))
    o0 = order_zero_residual(rng)
    o1 = order_one_residual(D, rng)
    print("\n[B] PRODUCT TRIPLE  C^8 (x) C^27 (dim 216): L_X needs NO doubling")
    print(f"    D self-adjoint = {d_herm} ; gamma^2 = I : {g_sq}")
    print(f"    gamma D = -D gamma = {d_odd} ; J D J^-1 = D : {d_real}")
    print(f"    KO signs eps={eps:+.0f}, eps''={epp:+.0f} -> KO-dim {ko}  (chirality in")
    print("        the CHARGE factor; L_X ungraded -> the Phase-1.1 6(x)6->4 doubling")
    print("        obstruction is DISSOLVED)")
    print(f"    order-zero [a,b^o]                 : {o0:.2e}")
    print(f"    order-one  [[D,a],b^o] (octonionic): {o1:.2e}")

    # ---- [C] axioms do NOT force the Yukawa -----------------------------
    c_yuk = coupling_order_one(K_Yuk, rng)
    c_maj = coupling_order_one(K_Maj, rng)
    print("\n[C] BUT THE AXIOMS DO NOT FORCE THE YUKAWA")
    print("    order-one of each charge coupling (x) a RANDOM Hermitian flavour op:")
    print(f"      K_Yuk (x) random_flavour : {c_yuk:.2e}")
    print(f"      K_Maj (x) random_flavour : {c_maj:.2e}")
    print("    ~0 for BOTH => order-one factors through the charge sector; the gauge")
    print("    algebra sees flavour as pure multiplicity, so ANY self-adjoint flavour")
    print("    operator passes. The octonionic L_X is ADMISSIBLE but NOT FORCED.")

    # ---- verdict --------------------------------------------------------
    print("\n[V] VERDICT  (two-sided, honest)")
    print("    POSITIVE: step C closes the second Phase-1.1 obstruction -- the")
    print("    octonionic L_X lives in a consistent KO-6 triple, ungraded, with its")
    print("    averaging-law masses in D's spectrum; no doubling, KO stays 6.")
    print("    SOBERING: the triple axioms do NOT pin the Yukawa (any self-adjoint")
    print("    flavour operator passes), so the CHO mass texture is NOT secured by")
    print("    the triple -- it must come from the spectral ACTION (Phase 1.3).")
    print("    epsilon_heat_kernel warns the spectral pi enters only via (4 pi)^(-d/2),")
    print("    so Phase 1.3 is more likely to REFUTE than confirm eps0^2 = pi/432 as")
    print("    a4/a2. Moves NO Bayes credit: F0 stays GEOMETRIC/open.")
    print("=" * 78)

    # ---- stable assertions (audit.py ignores the return value) ----------
    # [A] L_X is genuinely the octonionic averaging-law operator:
    assert lx_herm < 1e-9, "L_X is not self-adjoint"
    assert got_singlets == singlets, "L_X singlet spectrum is not {a,b,c}"
    assert got_octets == octets, "L_X octet spectrum is not the pair-averages"
    assert sum(c for c in mult.values()) == 27, "L_X is not 27-dimensional"
    assert all(v[1] for v in (vy, vm)), "a charge coupling is not gamma1-odd"
    assert all(v[0] and v[2] for v in (vy, vm)), "a charge coupling is not Herm/J1-real"
    # [B] the octonionic L_X gives a consistent KO-6 triple WITHOUT doubling:
    assert d_herm, "product Dirac not self-adjoint"
    assert g_sq, "product grading not an involution"
    assert d_odd, "product Dirac not gamma-odd"
    assert d_real, "product Dirac not J-real"
    assert abs(eps - 1.0) < 1e-9 and abs(epp + 1.0) < 1e-9 and ko == 6, \
        "product triple is not KO-dim 6"
    assert o0 < 1e-9, "order-zero failed for the octonionic product triple"
    assert o1 < 1e-9, "order-one failed for the octonionic product triple"
    # [C] the decisive finding: order-one leaves the flavour operator FREE:
    assert c_yuk < 1e-9, "Yukawa coupling unexpectedly constrains flavour"
    assert c_maj < 1e-9, "Majorana coupling unexpectedly constrains flavour"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
