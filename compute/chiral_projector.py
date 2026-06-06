"""
The chiral idempotent — closing the Lever B <-> Lever D seam (input (C)).
========================================================================

The open seam (foundations/05_electroweak_su2_theorem.md, input (C))
--------------------------------------------------------------------
Theorems 1-3 of Lever D proved: weak su(2) from the quaternions H (T_a doublet),
the chiral split so(4) = su(2)_L (+) su(2)_R, and that on C(x)H(x)O the weak
generators T_a (x) I_8 COMMUTE with the colour/charge Q (Lever C) and the
KO-dimension-6 chirality gamma (Lever B).  Proposition 4 (the SM hypercharge
spectrum) was left CONDITIONAL on input (C): the left=doublet / right=singlet
assignment.

Why the naive projector fails -- and the fix
--------------------------------------------
Because T_a (x) I_8 COMMUTES with I_4 (x) gamma (Theorem 3), the chiral projector
(I +- gamma)/2 acting as a spectator on the O leg leaves T_a a FULL DOUBLET on
BOTH chiralities -- it does not singlet the right-handed sector.  The resolution
is that the physically GAUGED weak generators are the chirally PROJECTED
operators

    G_a := T_a (x) P_L ,     P_L := (I_8 + gamma) / 2     (the KO-6 idempotent),

NOT T_a (x) I_8.  Then on the gamma=+1 sector G_a = T_a (x) I is a doublet, and
on the gamma=-1 sector G_a = 0 is a singlet -- pattern (C) from ONE projector.

The alignment condition (an honest refinement of Lever B)
---------------------------------------------------------
For this to label CHARGE eigenstates as L or R, charge and chirality must commute.
Lever B's representative gamma = i L_1...L_6 keeps the colour-fixing axis and
gives [Q, gamma] = 1/3 != 0.  But Lever C's charge fixes a colour direction e_f
and is built (bilinearly, hence EVEN) from the other SIX imaginary directions.
The chirality VOLUME ELEMENT over those same six charge-carrying directions
(i.e. DROP the colour axis e_f) commutes with Q EXACTLY, and is still KO-6
((epsilon, epsilon'') = (+1, -1), since conj(i) = -i flips the sign of the
6-fold real product).  So the consistent KO-6 chirality to pair with Lever C is

    gamma_Q := i * prod_{i != f} L_{e_i}      (volume of the 6 ladder directions).

This module builds gamma_Q from Lever C's own fixed direction and verifies
[Q, gamma_Q] = 0.

What is established (no per-field assignment put in by hand)
-----------------------------------------------------------
  [A] {G_a} close su(2): [G_a, G_b] = i eps_abc G_c, BECAUSE P_L^2 = P_L.
  [B] the gauged Casimir C = sum_a G_a^2 = (3/4) I_4 (x) P_L has spectrum
      {3/4 on the gamma=+1 sector (DOUBLET, j=1/2), 0 on the gamma=-1 sector
      (SINGLET)} -- the single KO-6 idempotent realises pattern (C).
  [C] [Q, gamma_Q] = 0, so every Lever C electric-charge eigenstate has DEFINITE
      chirality; the projector applies charge-by-charge.  We tabulate (Q,
      chirality) for the eight charge states.

Honest residual after [A][B][C]
-------------------------------
The ORIENTATION -- which gamma-sign is "left", P_L = (I + gamma)/2 vs
(I - gamma)/2 -- is a convention (the definition of left-handedness), not a free
parameter per field.  Input (C) is thereby reduced from EIGHT per-field
doublet/singlet assignments to ONE chiral projector plus this orientation.  The
Yukawa SPECTRUM stays open as before.

No scipy.  Reuses ko_dimension_chirality (Lever B machinery), ladder_charges
(Lever C Q + fixed colour direction) and weak_isospin_hypercharge (Lever D T_a).
Companion proof: foundations/06_chiral_idempotent.md.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/chiral_projector.py
"""

import numpy as np

from ko_dimension_chirality import left_mult_matrix, J_conjugate_operator
from ladder_charges import search_witt_basis, charge_operator
from weak_isospin_hypercharge import isospin_generators


def levi_civita():
    eps = np.zeros((3, 3, 3))
    for (a, b, c) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        eps[a, b, c] = 1.0
        eps[a, c, b] = -1.0
    return eps


def aligned_chirality(fixed):
    """gamma_Q = i * product over the six imaginary directions != fixed.

    This is the KO-6 chirality volume element over Lever C's charge-carrying
    directions (dropping the colour-fixing axis e_fixed), so that it commutes
    with the charge operator Q."""
    L = [left_mult_matrix(i).astype(np.complex128) for i in range(8)]
    prod = np.eye(8, dtype=np.complex128)
    for i in range(1, 8):
        if i != fixed:
            prod = prod @ L[i]
    return 1j * prod


def ko6_signs(gamma):
    """(epsilon, epsilon'') for the real structure J = complex conjugation.

    epsilon = sign(J^2) = +1 (J = conjugation, J^2 = I).
    epsilon'' from J gamma J^{-1} = epsilon'' gamma; with J = conjugation this is
    conj(gamma) = epsilon'' gamma."""
    epsilon = 1.0  # J^2 = I for plain complex conjugation
    JgammaJ = J_conjugate_operator(gamma)  # = conj(gamma) since B = I
    num = np.vdot(gamma.reshape(-1), JgammaJ.reshape(-1))
    den = np.vdot(gamma.reshape(-1), gamma.reshape(-1))
    epp = np.real(num / den)
    return epsilon, epp


def chiral_projectors(gamma):
    I8 = np.eye(8, dtype=np.complex128)
    return 0.5 * (I8 + gamma), 0.5 * (I8 - gamma)


def gauged_generators(T, P):
    """G_a = T_a (x) P on C^4 (x) C^8."""
    return [np.kron(t, P) for t in T]


# --------------------------------------------------------------------------
# [A] su(2) closure of the chirally projected generators
# --------------------------------------------------------------------------
def check_projected_su2(G):
    eps = levi_civita()
    max_err = 0.0
    for a in range(3):
        for b in range(3):
            comm = G[a] @ G[b] - G[b] @ G[a]
            target = sum(1j * eps[a, b, c] * G[c] for c in range(3))
            max_err = max(max_err, float(np.max(np.abs(comm - target))))
    return max_err


def idempotent_error(P):
    return float(np.max(np.abs(P @ P - P)))


# --------------------------------------------------------------------------
# [B] gauged Casimir: doublet on gamma=+1, singlet on gamma=-1
# --------------------------------------------------------------------------
def gauged_casimir(G):
    C = np.zeros_like(G[0])
    for g in G:
        C += g @ g
    return C


def casimir_spectrum_by_chirality(C, gamma, tol=1e-6):
    """Eigenvalues of the gauged Casimir on the gamma=+1 and gamma=-1 sectors of
    the O leg (lifted to C^4 (x) C^8)."""
    I4 = np.eye(4, dtype=np.complex128)
    w, V = np.linalg.eigh((gamma + gamma.conj().T) / 2.0)
    plus = V[:, w > 1.0 - tol]
    minus = V[:, w < -1.0 + tol]
    Pp = np.kron(I4, plus @ plus.conj().T)
    Pm = np.kron(I4, minus @ minus.conj().T)
    cp = np.linalg.eigvalsh((Pp @ C @ Pp + (Pp @ C @ Pp).conj().T) / 2.0)
    cm = np.linalg.eigvalsh((Pm @ C @ Pm + (Pm @ C @ Pm).conj().T) / 2.0)
    plus_nonzero = sorted(set(np.round(cp[cp > tol], 6)))
    minus_max = float(np.max(np.abs(cm)))
    return plus_nonzero, minus_max


# --------------------------------------------------------------------------
# [C] compatibility of charge and chirality
# --------------------------------------------------------------------------
def commutator_norm(A, B):
    return float(np.max(np.abs(A @ B - B @ A)))


def charge_chirality_table(Q, gamma, tol=1e-6):
    """If [Q, gamma] = 0: simultaneously diagonalise and return (charge,
    chirality) of each eigenstate."""
    comm = commutator_norm(Q, gamma)
    if comm > tol:
        return comm, None
    Qh = (Q + Q.conj().T) / 2.0
    gh = (gamma + gamma.conj().T) / 2.0
    wq, Vq = np.linalg.eigh(Qh)
    order = np.argsort(np.round(wq, 6))
    wq, Vq = wq[order], Vq[:, order]
    pairs = []
    i, n = 0, len(wq)
    while i < n:
        j = i
        while j < n and abs(wq[j] - wq[i]) < tol:
            j += 1
        block = Vq[:, i:j]
        gsub = block.conj().T @ gh @ block
        for g in np.linalg.eigvalsh((gsub + gsub.conj().T) / 2.0):
            pairs.append((round(float(wq[i]), 6), int(round(float(g)))))
        i = j
    return comm, pairs


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("  THE CHIRAL IDEMPOTENT — closing the Lever B <-> Lever D seam (C)")
    print("  Gauged weak generators G_a = T_a (x) (I + gamma_Q)/2.")
    print("=" * 78)

    T = isospin_generators()                            # Lever D, H leg (4x4)
    fixed, pairs_, signs, alphas = search_witt_basis()  # Lever C
    if alphas is None:
        print("\n  Lever C Witt basis not found; cannot run. (inconclusive)")
        return
    Q = charge_operator(alphas)                         # Lever C charge (8x8)
    gamma = aligned_chirality(fixed)                    # KO-6 chirality aligned to Q

    eps, epp = ko6_signs(gamma)
    print(f"\n  Lever C fixes colour direction e{fixed}; chirality gamma_Q is the")
    print(f"  volume element over the six charge-carrying directions e_i (i != {fixed}).")
    print(f"      KO-6 signs (epsilon, epsilon'')   : ({eps:+.0f}, {epp:+.0f})   "
          "(expect (+1, -1) = KO-dim 6)")
    gamma_sq = float(np.max(np.abs(gamma @ gamma - np.eye(8))))
    print(f"      gamma_Q^2 = I error               : {gamma_sq:.2e}")

    P_L, P_R = chiral_projectors(gamma)
    G = gauged_generators(T, P_L)

    # [A]
    print("\n  [A] su(2) closure of the chirally projected generators")
    print("  " + "-" * 74)
    idem = idempotent_error(P_L)
    alg_err = check_projected_su2(G)
    print(f"      P_L^2 = P_L idempotent error      : {idem:.2e}")
    print(f"      [G_a,G_b] = i eps G_c  max error  : {alg_err:.2e}")
    a_ok = idem < 1e-9 and alg_err < 1e-8
    print(f"      [{'PASS' if a_ok else 'FAIL'}] projected generators close su(2) "
          "(P idempotent survives the bracket)")

    # [B]
    print("\n  [B] gauged Casimir: doublet on gamma=+1, singlet on gamma=-1")
    print("  " + "-" * 74)
    C = gauged_casimir(G)
    plus_nz, minus_max = casimir_spectrum_by_chirality(C, gamma)
    print(f"      Casimir on gamma=+1 sector        : {plus_nz}   "
          "(expect [0.75] = j=1/2 doublet)")
    print(f"      Casimir on gamma=-1 sector (max|.|): {minus_max:.2e}   "
          "(expect 0 = singlet)")
    b_ok = plus_nz == [0.75] and minus_max < 1e-9
    print(f"      [{'PASS' if b_ok else 'FAIL'}] one KO-6 idempotent gives "
          "doublet(L) + singlet(R) = pattern (C)")

    # [C]
    print("\n  [C] charge/chirality compatibility: [Q, gamma_Q] = 0 ?")
    print("  " + "-" * 74)
    comm, table = charge_chirality_table(Q, gamma)
    print(f"      |[Q, gamma_Q]|                    : {comm:.2e}   (expect 0)")
    c_ok = table is not None
    if c_ok:
        summary = {}
        for q, g in table:
            summary.setdefault(q, []).append(g)
        print("      every charge eigenstate has DEFINITE chirality:")
        for q in sorted(summary):
            chs = sorted(set(summary[q]))
            print(f"         Q = {q:+.3f} : chirality {chs}  (x{len(summary[q])})")
    print(f"      [{'PASS' if c_ok else 'FAIL'}] charge and chirality commute "
          "-> projector applies charge-by-charge")

    # Verdict
    print("\n" + "=" * 78)
    print("  VERDICT")
    print("=" * 78)
    if a_ok and b_ok and c_ok:
        print("  SEAM (C) STRUCTURALLY CLOSED. The gauged weak generators")
        print("  G_a = T_a (x) P_L with the SINGLE KO-dimension-6 idempotent")
        print("  P_L = (I + gamma_Q)/2 (gamma_Q the chirality over Lever C's six")
        print("  charge-carrying directions) close su(2), act as a DOUBLET on the")
        print("  gamma=+1 (left) sector and a SINGLET on the gamma=-1 (right) sector,")
        print("  and [Q, gamma_Q] = 0 so every electric-charge eigenstate is chirality-")
        print("  definite. Input (C) of Lever D is reduced from eight per-field")
        print("  doublet/singlet assignments to ONE chiral projector.")
        print()
        print("  Consequence: Proposition 4 (foundations/05) is no longer conditional")
        print("  on a per-field table -- only on the ORIENTATION (which gamma-sign is")
        print("  'left'), a convention. The Yukawa SPECTRUM stays open.")
    else:
        print("  SEAM (C) NOT fully closed — see the failing check above.")
    print()


if __name__ == "__main__":
    main()
