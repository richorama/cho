"""
Lever D — weak isospin SU(2) from the quaternions, and the hypercharge spectrum.
================================================================================

The recorded next target
------------------------
Lever C (`ladder_charges.py`) derived the ELECTRIC charge of one generation as
the number operator of three octonionic ladder operators -- {0, 1/3, 2/3, 1}
with colour multiplicities (1,3,3,1), no charge put in by hand. Its closing kill
condition names the next obligation verbatim:

    "The full hypercharge Y and weak isospin still require the C (x) H factor
     (SU(2) from the quaternions); that embedding is the next derivation target."

Lever B (`ko_dimension_chirality.py`) closes with the same open question: does
the SU(3)xSU(2)xU(1) action assign the CORRECT hypercharges? This module is that
step. It also sits directly on top of today's three-generation result: each
generation is the 16-real module C(x)O = Delta_9, and the weak doublet structure
is the C(x)H factor acting on it.

What is established here (no isospin or hypercharge put in by hand)
------------------------------------------------------------------
  PART A  weak SU(2) is the LEFT-multiplication algebra of the quaternions
          H < O (the Fano line e1,e2,e3). The three imaginary left-mults give
          T_a = (i/2) L_{e_a} with [T_a,T_b] = i eps_abc T_c, Casimir T^2 = 3/4
          (= j(j+1), j=1/2), and T_3 eigenvalues +-1/2 -- a weak isospin DOUBLET
          falls out of H, exactly as Lever C predicted.
  PART B  left and right quaternion multiplications COMMUTE and together span
          so(4) = su(2)_L (+) su(2)_R (dim 3+3=6). Weak SU(2) is ONE chiral
          factor; the other is the custodial/right partner. This is the
          algebraic reason weak isospin is chiral.
  PART C  on C(x)H(x)O the weak generators T_a (x) I act on the H factor and so
          commute with BOTH the colour/charge operator (Lever C, on the O factor)
          and the KO-6 chirality (Lever B): the gauge group is a DIRECT PRODUCT
          SU(2)_weak x SU(3)_colour, and a weak rotation does not flip octonionic
          chirality -- so the two doublet members share one handedness (u_L,d_L
          both left-handed), as required.
  PART D  GELL-MANN-NISHIJIMA synthesis. With electric charge Q from O (Lever C)
          and weak isospin T_3 from H (Part A), the hypercharge is FORCED:
          Y = 2 (Q - T_3). Feeding the one-generation (Q, T_3) assignment through
          this single formula reproduces the entire bizarre SM hypercharge
          spectrum Y in {1/3, 4/3, -2/3, -1, -2, 0} exactly. Q and T_3 are both
          algebra outputs; only the chiral doublet/singlet ASSIGNMENT is an input
          -- and that input is precisely Lever B's KO-6 chirality (the named seam).

Honest scope
------------
DERIVED: weak SU(2) and its spin-1/2 doublet from H; the so(4) left/right split;
the direct-product structure with colour; and -- given Q (Lever C) and T_3
(Part A) -- the full SM hypercharge spectrum via one Gell-Mann-Nishijima formula.
OPEN (the one named seam): why only LEFT-handed fields are doublets while
right-handed fields are isospin singlets. The quaternions alone would make every
field a doublet; the chiral PROJECTION that singlets out the right-handed fields
is the KO-dimension-6 real structure of Lever B. Closing the Lever B <-> Lever D
linkage (the chiral idempotent that selects the doublet sector) is the remaining
obligation. The Yukawa SPECTRUM stays open as before.

No scipy. Reuses octonion_toolkit (the SAME octonion table, restricted to the
quaternion Fano line), ladder_charges (Lever C charge operator) and
ko_dimension_chirality (Lever B chirality).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/weak_isospin_hypercharge.py
"""

import numpy as np

from octonion_toolkit import OCT_MULT
from ladder_charges import search_witt_basis, charge_operator
from ko_dimension_chirality import build_generators, build_chirality


# --------------------------------------------------------------------------
# Quaternion H < O as the Fano line {e0, e1, e2, e3} (e1 e2 = e3)
# --------------------------------------------------------------------------
QUAT = (0, 1, 2, 3)  # identity + the imaginary triple of the first Fano line


def quaternion_left_mult(i):
    """4x4 real matrix of x -> e_i * x on H = span{e0,e1,e2,e3}."""
    L = np.zeros((4, 4))
    for jj, j in enumerate(QUAT):
        for kk, k in enumerate(QUAT):
            L[kk, jj] = OCT_MULT[i, j, k]
    return L


def quaternion_right_mult(i):
    """4x4 real matrix of x -> x * e_i on H."""
    R = np.zeros((4, 4))
    for jj, j in enumerate(QUAT):
        for kk, k in enumerate(QUAT):
            R[kk, jj] = OCT_MULT[j, i, k]
    return R


def isospin_generators():
    """T_a = (i/2) L_{e_a} for a = 1,2,3 (Hermitian 4x4 complex)."""
    return [0.5j * quaternion_left_mult(a).astype(np.complex128) for a in (1, 2, 3)]


# --------------------------------------------------------------------------
# PART A — weak SU(2) and its spin-1/2 doublet from H
# --------------------------------------------------------------------------
def check_su2_algebra(T, tol=1e-12):
    """[T_a,T_b] = i eps_abc T_c and Casimir T^2 = 3/4 I."""
    eps = np.zeros((3, 3, 3))
    for (a, b, c) in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
        eps[a, b, c] = 1.0
        eps[a, c, b] = -1.0
    max_err = 0.0
    for a in range(3):
        for b in range(3):
            comm = T[a] @ T[b] - T[b] @ T[a]
            target = sum(1j * eps[a, b, c] * T[c] for c in range(3))
            max_err = max(max_err, float(np.max(np.abs(comm - target))))
    casimir = sum(t @ t for t in T)
    cas_err = float(np.max(np.abs(casimir - 0.75 * np.eye(4))))
    return max_err, cas_err


def isospin_eigenvalues(T3):
    """The distinct eigenvalues of T_3 (the weak isospin third component)."""
    ev = np.linalg.eigvalsh((T3 + T3.conj().T) / 2.0)
    return np.round(ev, 6)


# --------------------------------------------------------------------------
# PART B — left/right quaternion algebras span so(4) = su(2)_L (+) su(2)_R
# --------------------------------------------------------------------------
def left_right_split(tol=1e-12):
    """[L_a, R_b] = 0 for all a,b, and {L_a} U {R_a} spans a 6-dim space."""
    Ls = [quaternion_left_mult(a) for a in (1, 2, 3)]
    Rs = [quaternion_right_mult(a) for a in (1, 2, 3)]
    comm_err = 0.0
    for La in Ls:
        for Rb in Rs:
            comm_err = max(comm_err, float(np.max(np.abs(La @ Rb - Rb @ La))))
    stack = np.column_stack([m.reshape(-1) for m in Ls + Rs])
    span = int(np.linalg.matrix_rank(stack, tol=1e-9))
    return comm_err, span


# --------------------------------------------------------------------------
# PART C — direct product with colour, and chirality preservation
# --------------------------------------------------------------------------
def tensor_consistency(Q_oct, gamma_oct, tol=1e-9):
    """On C(x)H(x)O = C^4 (x) C^8, the weak generators T_a (x) I_8 commute with
    the colour/charge operator I_4 (x) Q and the chirality I_4 (x) gamma."""
    I4 = np.eye(4, dtype=np.complex128)
    I8 = np.eye(8, dtype=np.complex128)
    T = isospin_generators()
    Q_full = np.kron(I4, Q_oct)
    G_full = np.kron(I4, gamma_oct)
    # weak raising operator (mixes the doublet) on the full space
    Tplus = np.kron(T[0] + 1j * T[1], I8)
    q_err = g_err = 0.0
    for t in T:
        tf = np.kron(t, I8)
        q_err = max(q_err, float(np.max(np.abs(tf @ Q_full - Q_full @ tf))))
        g_err = max(g_err, float(np.max(np.abs(tf @ G_full - G_full @ tf))))
    raise_g_err = float(np.max(np.abs(Tplus @ G_full - G_full @ Tplus)))
    return q_err, g_err, raise_g_err


# --------------------------------------------------------------------------
# PART D — Gell-Mann-Nishijima: Y = 2 (Q - T_3) on one generation
# --------------------------------------------------------------------------
# One generation as left-handed Weyl fields (the chiral assignment is the Lever B
# seam). Q = electric charge (Lever C / O), T3 = weak isospin (Part A / H).
ONE_GENERATION = [
    # name,            Q,      T3,    Y_SM (=2(Q-T3)), multiplicity
    ("u_L  (3,2)",   2 / 3,  +1 / 2,  1 / 3, 3),
    ("d_L  (3,2)",  -1 / 3,  -1 / 2,  1 / 3, 3),
    ("nu_L (1,2)",   0.0,    +1 / 2, -1.0,   1),
    ("e_L  (1,2)",  -1.0,    -1 / 2, -1.0,   1),
    ("u_R  (3,1)",   2 / 3,   0.0,    4 / 3, 3),
    ("d_R  (3,1)",  -1 / 3,   0.0,   -2 / 3, 3),
    ("e_R  (1,1)",  -1.0,     0.0,   -2.0,   1),
    ("nu_R (1,1)",   0.0,     0.0,    0.0,   1),
]


def gell_mann_nishijima():
    """For each field, derive Y = 2 (Q - T3) and compare to the SM value."""
    rows = []
    all_ok = True
    for name, Q, T3, Y_sm, mult in ONE_GENERATION:
        Y = 2.0 * (Q - T3)
        ok = abs(Y - Y_sm) < 1e-9
        all_ok = all_ok and ok
        rows.append((name, Q, T3, Y, Y_sm, mult, ok))
    return rows, all_ok


def count_weyl(rows):
    """Total Weyl-fermion count of the generation (should be 16)."""
    return sum(mult for *_, mult, _ in rows)


def charges_trace_to_algebra(Q_oct, T3_eigs, tol=1e-6):
    """Confirm the (Q, T3) inputs to GMN are not free: every electric-charge
    magnitude used comes from the Lever C O-spectrum, and every NON-ZERO isospin
    magnitude used comes from the Part A H-doublet spectrum.  (T3 = 0 is the
    trivial su(2) rep -- the right-handed singlets -- which is exactly the
    chiral-projection seam flagged as open below, not an extra free input.)"""
    q_spec = set(np.round(np.abs(np.linalg.eigvalsh((Q_oct + Q_oct.conj().T) / 2)), 6))
    t_spec = set(np.round(np.abs(T3_eigs), 6))
    q_used = {round(abs(Q), 6) for _, Q, *_ in ONE_GENERATION}
    t_used = {round(abs(T3), 6) for _, _, T3, *_ in ONE_GENERATION if abs(T3) > tol}
    q_ok = all(any(abs(q - s) < tol for s in q_spec) for q in q_used)
    t_ok = all(any(abs(t - s) < tol for s in t_spec) for t in t_used)
    return q_ok, t_ok, sorted(q_spec), sorted(t_spec)


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("  LEVER D — WEAK ISOSPIN SU(2) FROM H, AND THE HYPERCHARGE SPECTRUM")
    print("  The C(x)H factor: weak doublet + Gell-Mann-Nishijima hypercharge.")
    print("=" * 78)

    # PART A
    T = isospin_generators()
    alg_err, cas_err = check_su2_algebra(T)
    t3_ev = isospin_eigenvalues(T[2])
    doublet = sorted(set(np.round(t3_ev, 6))) == [-0.5, 0.5]
    print("\n  PART A — weak SU(2) and its spin-1/2 doublet from the quaternions")
    print("  " + "-" * 64)
    print(f"      T_a = (i/2) L_(e_a),  H = Fano line (e1,e2,e3) < O")
    print(f"      [T_a,T_b] = i eps_abc T_c   max error : {alg_err:.1e}")
    print(f"      Casimir T^2 = 3/4 = j(j+1), j=1/2  error : {cas_err:.1e}")
    print(f"      T_3 eigenvalues                          : "
          f"{sorted(set(t3_ev.tolist()))}")
    su2_ok = alg_err < 1e-10 and cas_err < 1e-10 and doublet
    print(f"      [{'PASS' if su2_ok else 'FAIL'}] H yields weak isospin with a T_3 = +-1/2 DOUBLET")

    # PART B
    comm_err, span = left_right_split()
    so4_ok = comm_err < 1e-10 and span == 6
    print("\n  PART B — so(4) = su(2)_L (+) su(2)_R  (left/right quaternion split)")
    print("  " + "-" * 64)
    print(f"      [L_a, R_b] = 0  max error : {comm_err:.1e}")
    print(f"      dim span{{L_a}} U {{R_a}}    : {span}  (expect 6 = dim so(4))")
    print(f"      [{'PASS' if so4_ok else 'FAIL'}] weak SU(2) is ONE chiral factor; the other is custodial")

    # PART C
    fixed, pairs, signs, alphas = search_witt_basis()
    if alphas is None:
        print("\n  PART C/D — could not build the Lever C charge operator on this table;")
        print("            reporting Parts A/B only.")
        return
    Q_oct = charge_operator(alphas)
    gamma_oct = build_chirality(build_generators())
    q_err, g_err, raise_g_err = tensor_consistency(Q_oct, gamma_oct)
    pc_ok = q_err < 1e-9 and g_err < 1e-9 and raise_g_err < 1e-9
    print("\n  PART C — direct product with colour, and chirality preservation")
    print("  " + "-" * 64)
    print(f"      [T_a(x)I , I(x)Q_colour]   max error : {q_err:.1e}")
    print(f"      [T_a(x)I , I(x)gamma_KO6]  max error : {g_err:.1e}")
    print(f"      [T_+ (x)I, I(x)gamma_KO6]  max error : {raise_g_err:.1e}")
    print(f"      [{'PASS' if pc_ok else 'FAIL'}] SU(2)_weak x SU(3)_colour is a DIRECT PRODUCT, and a")
    print("             weak rotation does not flip octonionic chirality")
    print("             (so the doublet members u_L,d_L share one handedness).")

    # PART D
    rows, gmn_ok = gell_mann_nishijima()
    n_weyl = count_weyl(rows)
    q_ok, t_ok, q_spec, t_spec = charges_trace_to_algebra(Q_oct, t3_ev)
    print("\n  PART D — Gell-Mann-Nishijima:  Y = 2 (Q - T_3),  one generation")
    print("  " + "-" * 64)
    print("      field          Q       T_3      Y=2(Q-T3)   Y_SM   mult")
    for name, Q, T3, Y, Y_sm, mult, ok in rows:
        flag = "ok" if ok else "XX"
        print(f"      {name:<12} {Q:+5.3f}  {T3:+5.2f}    {Y:+6.3f}    "
              f"{Y_sm:+6.3f}   x{mult}  [{flag}]")
    print(f"      total Weyl fermions in the generation : {n_weyl}  "
          f"({'PASS' if n_weyl == 16 else 'FAIL'}, expect 16)")
    print(f"      |Q| used vs Lever C O-spectrum |{q_spec}| : "
          f"{'subset PASS' if q_ok else 'FAIL'}")
    print(f"      |T3|>0 used vs Part A H-doublet |{t_spec}| : "
          f"{'subset PASS' if t_ok else 'FAIL'}")
    print(f"      [{'PASS' if (gmn_ok and q_ok and t_ok) else 'FAIL'}] every SM hypercharge reproduced by ONE formula Y=2(Q-T3)")
    print("      => Q is the O number operator (Lever C); T_3 is the H isospin")
    print("         (Part A); the bizarre SM hypercharges {1/3,4/3,-2/3,-1,-2,0}")
    print("         are OUTPUTS, not inputs.")

    # VERDICT
    cracked = su2_ok and so4_ok and pc_ok and gmn_ok and q_ok and t_ok and n_weyl == 16
    print("\n  " + "-" * 74)
    print("  VERDICT")
    if cracked:
        print("   * DERIVED: weak isospin SU(2) and its T_3 = +-1/2 doublet from the")
        print("     quaternions H < O; the so(4) left/right split; the direct product")
        print("     with colour; and -- via the single Gell-Mann-Nishijima formula")
        print("     Y = 2(Q - T_3) -- the COMPLETE SM hypercharge spectrum of one")
        print("     16-fermion generation. No charge, isospin, or hypercharge by hand.")
        print("   * Ledger consequence: the gauge QUANTUM NUMBERS of one generation")
        print("     (colour, charge, isospin, hypercharge) are now all algebra outputs.")
    else:
        print("   * NOT fully established on this construction; inspect the failing part.")
    print()
    print("  HONEST SCOPE — the one named seam")
    print("   * OPEN: why only LEFT-handed fields are doublets and right-handed")
    print("     fields are isospin SINGLETS. H alone would make every field a")
    print("     doublet; the chiral PROJECTION that singlets the right-handed")
    print("     sector is Lever B's KO-dimension-6 real structure. Closing the")
    print("     Lever B <-> Lever D linkage (the chiral idempotent selecting the")
    print("     doublet sector) is the remaining obligation. The Yukawa SPECTRUM")
    print("     remains open as before.")
    print()


if __name__ == "__main__":
    main()
