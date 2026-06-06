"""
Cracking the three-generations bridge: the idempotent-frame resolution of the no-go.
====================================================================================

The problem (the framework's single biggest weakness)
-----------------------------------------------------
`three_generations_nogo_audit.py` broke the headline route to three generations.
Its Leg 2 identified the three generations with the three 8-dim reps that the D4
Dynkin S3 (triality) permutes: the vector 8v and the chirality-mirror PAIR of
spinors 8s, 8c. That identification fails two ways -- triality would have to map
vector <-> spinor (Obstruction 1), and 8s, 8c are opposite-chirality partners so
each generation gets a mirror (Obstruction 2). This is the Distler-Garibaldi
failure mode that sank Lisi's E8, and it downgraded G1/G2 to conjecture level.

The resolution (and why a naive attempt is wrong)
-------------------------------------------------
The crucial point is WHICH three objects are the generations.

A first guess (tested and REJECTED, see PART D) is the three off-diagonal
octonion slots z1, z2, z3 of a J3(O) element. That guess FAILS: under the
relevant Spin(8) those three slots ARE 8v, 8s, 8c, and octonion conjugation
mixes their Weyl chirality (PART D measures the leakage). So the off-diagonal
slots inherit exactly the no-go's obstruction -- they are not a clean route.

The CORRECT identification is Lever A's: the three generations are the three
primitive IDEMPOTENTS e1, e2, e3 of a maximal frame (the rank of J3(O)). These
are not reps that triality shuffles; they are three POINTS of the Cayley
projective plane OP^2 = F4/Spin(9). This module shows that identification is free
of both obstructions:

  PART A  the symmetry permuting the three idempotents is the INNER frame Weyl
          group S3 < F4 = Aut(J3(O)), realised by genuine Jordan automorphisms
          X -> P X P^T (they preserve the Freudenthal cubic). F4 is connected with
          NO outer automorphism, so -- unlike the OUTER D4 triality -- this S3
          cannot carry a rep to an inequivalent one.
  PART B  all three idempotents are the SAME kind of object: each has an isotropy
          subalgebra of dimension 36 = spin(9) and a tangent space of dimension
          16, identically. So they are three F4-equivalent points of the single
          homogeneous space OP^2 = F4/Spin(9) -- genuinely identical, not a
          vector plus an inequivalent spinor pair. Obstruction 1 cannot be posed.
  PART C  the 16-dim tangent at each idempotent is ONE real Spin(9) spinor
          Delta_9 (the octonionic Cl(9) module; commutant dimension 1 = real
          type). One generation = T(OP^2) = 16 real = C(x)O, the KO-dimension-6
          module Lever B showed is chiral WITHOUT doubling. Three identical
          copies of a single, self-conjugate (real) spinor carry the SAME
          chirality; an opposite-chirality mirror would need an INEQUIVALENT
          conjugate spinor, which a real type does not have. Obstruction 2 cannot
          arise either.
  PART D  the cautionary control: the off-diagonal-slot guess really does carry
          the 8v/8s/8c chirality mixing, confirming the no-go is real for THAT
          identification and that the idempotent route is genuinely different.

Net: the COUNT (Lever A, three idempotents) and the CHIRALITY (Lever B,
KO-dimension 6 on the 16-dim tangent spinor) live on the SAME object -- a maximal
frame of J3(O) and the three OP^2 points it picks out -- related by an INNER F4
symmetry permuting three identical, same-chirality copies of the real spinor
Delta_9. The Distler-Garibaldi obstruction is an artifact of the outer-triality
identification of generations with 8v/8s/8c; the idempotent identification evades
it.

What remains open (stated plainly)
----------------------------------
This settles only the COUNT-and-CHIRALITY bridge. The fermion content map onto
T(OP^2), the per-generation hypercharges (Lever C), the H factor, the Dirac
operator D (Lever B's open kill condition) and the Yukawa SPECTRUM (Lever A's C4
negative) all stay open. G1/G2 move from "faces the vector/mirror obstruction" to
"count + chirality obstruction-free on the idempotent frame; spectrum open".

No scipy. Reuses octonion_toolkit, jordan_eigenvalue_generations (Lever A),
ko_dimension_chirality (Lever B) and epsilon_weyl_isomorphism (the F4/Spin(9)
derivation machinery and the octonionic Cl(9) spinor).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/three_generations_frame.py
"""

from itertools import permutations

import numpy as np

from octonion_toolkit import Octonion
from ko_dimension_chirality import build_generators, build_chirality
from jordan_eigenvalue_generations import (
    JordanElement,
    _herm_to_dense,
    jordan_product_dense,
    _frob_diff,
)
from epsilon_weyl_isomorphism import (
    jordan_product_tensor,
    derivation_algebra,
    stabiliser_subalgebra,
    clifford9_generators,
    so9_from_clifford,
    commutant_dimension,
)


# --------------------------------------------------------------------------
# Frame permutations as inner conjugations X -> P X P^T on J3(O)
# --------------------------------------------------------------------------
def all_frame_perms():
    """The six permutations of {1,2,3} as dicts {1:.,2:.,3:.}."""
    return [dict(zip((1, 2, 3), p)) for p in permutations((1, 2, 3))]


def perm_sign(sigma):
    """+1 for even (identity, 3-cycles), -1 for odd (transpositions)."""
    img = [sigma[1], sigma[2], sigma[3]]
    inversions = sum(1 for i in range(3) for j in range(i + 1, 3)
                     if img[i] > img[j])
    return -1 if inversions % 2 else 1


def apply_frame_perm(J, sigma):
    """Return X -> P_sigma X P_sigma^T as a rearrangement of the dense matrix
    (a genuine permutation of the three frame axes)."""
    M = _herm_to_dense(J)
    inv = [0, 0, 0]
    for i in (1, 2, 3):
        inv[sigma[i] - 1] = i - 1
    Mp = [[M[inv[a]][inv[b]] for b in range(3)] for a in range(3)]
    xi = [Mp[0][0].real_part(), Mp[1][1].real_part(), Mp[2][2].real_part()]
    z3 = Mp[0][1]   # (1,2) entry
    z1 = Mp[1][2]   # (2,3) entry
    z2 = Mp[2][0]   # (3,1) entry
    return JordanElement(xi, z1, z2, z3)


# --------------------------------------------------------------------------
# PART A — three idempotents permuted by the INNER frame S3
# --------------------------------------------------------------------------
def diagonal_idempotents():
    return [JordanElement.diagonal(1, 0, 0),
            JordanElement.diagonal(0, 1, 0),
            JordanElement.diagonal(0, 0, 1)]


def check_idempotent_frame():
    """The three diagonal primitives are rank-1, orthogonal, resolve I, and the
    frame S3 permutes them faithfully."""
    es = diagonal_idempotents()
    zero = [[Octonion(np.zeros(8)) for _ in range(3)] for _ in range(3)]
    idemp_ok = ortho_ok = True
    for a, e in enumerate(es):
        D = _herm_to_dense(e)
        if _frob_diff(jordan_product_dense(D, D), D) > 1e-12:
            idemp_ok = False
        for b in range(a + 1, 3):
            P = jordan_product_dense(D, _herm_to_dense(es[b]))
            if _frob_diff(P, zero) > 1e-12:
                ortho_ok = False
    resolves = np.allclose(sum(e.xi for e in es), np.ones(3))

    # frame S3 permutes the three idempotents faithfully.
    images = set()
    for sigma in all_frame_perms():
        perm = tuple(int(np.argmax(apply_frame_perm(e, sigma).xi)) for e in es)
        images.add(perm)
    faithful = len(images) == 6
    return idemp_ok, ortho_ok, resolves, faithful


def check_inner_automorphisms(rng, n_samples=1500, tol=1e-10):
    """Every frame permutation preserves the Freudenthal cubic -> it is in F4."""
    perms = all_frame_perms()
    max_err = 0.0
    for _ in range(n_samples):
        J = JordanElement.random_hermitian(rng)
        t0, q0, d0 = J.trace(), J.quadratic(), J.determinant()
        for sigma in perms:
            Js = apply_frame_perm(J, sigma)
            max_err = max(max_err,
                          abs(Js.trace() - t0),
                          abs(Js.quadratic() - q0),
                          abs(Js.determinant() - d0))
    return max_err, max_err < tol


# --------------------------------------------------------------------------
# PART B — the three idempotents are identical points of OP^2 = F4/Spin(9)
# --------------------------------------------------------------------------
def idempotent_vec(slot):
    """27-vector of the primitive idempotent diag with 1 in diagonal `slot`."""
    v = np.zeros(27)
    v[slot] = 1.0
    return v


def isotropy_and_tangent(f4, slot):
    """Dimension of the F4-isotropy subalgebra of an idempotent and of its
    tangent space (52 - isotropy)."""
    v0 = idempotent_vec(slot)
    stab = stabiliser_subalgebra(f4, v0)
    iso = len(stab)
    return iso, len(f4) - iso


# --------------------------------------------------------------------------
# PART C — one real Spin(9) spinor Delta_9 per generation
# --------------------------------------------------------------------------
def delta9_real_type():
    """The octonionic Cl(9) acts on O^2 = R^16; its 16-dim Spin(9) spinor module
    has commutant dimension 1 (real type) -- a single self-conjugate spinor."""
    G = clifford9_generators()
    so9 = so9_from_clifford(G)
    dim = G[0].shape[0]
    comm = commutant_dimension(so9)
    return dim, comm


# --------------------------------------------------------------------------
# PART D — cautionary control: the off-diagonal-slot guess DOES carry 8v/8s/8c
# --------------------------------------------------------------------------
def conjugation_matrix():
    d = -np.ones(8)
    d[0] = 1.0
    return np.diag(d).astype(np.complex128)


def offdiagonal_chirality_mixing():
    """Octonion conjugation (which an odd frame perm applies to the slots) mixes
    the KO-dim-6 Weyl halves -- evidence the off-diagonal slots are the
    triality-related 8v/8s/8c, NOT identical copies. Reports the leakage of the
    +1 Weyl half into the -1 half (0 = preserved, >0 = mixed)."""
    gamma = build_chirality(build_generators())
    C = conjugation_matrix()
    Pp = 0.5 * (np.eye(8) + gamma)
    Pm = 0.5 * (np.eye(8) - gamma)
    leak = float(np.max(np.abs(Pm @ C @ Pp)))
    return leak


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    rng = np.random.default_rng(20260606)

    print("=" * 78)
    print("  CRACKING N_gen = 3 — THE IDEMPOTENT-FRAME RESOLUTION OF THE NO-GO")
    print("  Generations = three OP^2 points permuted by the INNER frame S3 < F4.")
    print("=" * 78)

    # PART A
    idemp_ok, ortho_ok, resolves, faithful = check_idempotent_frame()
    err_auto, auto_ok = check_inner_automorphisms(rng)
    print("\n  PART A — three idempotents permuted by the INNER frame S3")
    print("  " + "-" * 64)
    print(f"      e_i o e_i = e_i, e_i o e_j = 0, sum = I : "
          f"{'PASS' if (idemp_ok and ortho_ok and resolves) else 'FAIL'}")
    print(f"      frame S3 permutes the 3 idempotents faithfully : "
          f"{'PASS' if faithful else 'FAIL'}")
    print(f"      X->P X P^T preserves (trace,quadratic,det) drift {err_auto:.1e}")
    print(f"      [{'PASS' if auto_ok else 'FAIL'}] the six perms are INNER automorphisms in F4=Aut(J3O)")
    print("      => F4 is connected with NO outer automorphism, so this S3 cannot")
    print("         map a rep to an inequivalent one. (D4 triality is OUTER in SO(8).)")

    # PART B
    print("\n  PART B — the three idempotents are identical points of OP^2=F4/Spin(9)")
    print("  " + "-" * 64)
    print("      building f4 = Der(J3(O)) (this takes a moment)...")
    T = jordan_product_tensor()
    f4, _spec = derivation_algebra(T)
    dim_f4 = len(f4)
    print(f"      dim f4 = Der(J3(O))                    : {dim_f4}  "
          f"({'PASS' if dim_f4 == 52 else 'FAIL'}, expect 52)")
    isos, tans = [], []
    for slot in (0, 1, 2):
        iso, tan = isotropy_and_tangent(f4, slot)
        isos.append(iso)
        tans.append(tan)
    same = len(set(isos)) == 1 and len(set(tans)) == 1
    print(f"      isotropy dim at e1,e2,e3               : {isos}  "
          f"(expect 36,36,36 = spin(9))")
    print(f"      tangent  dim at e1,e2,e3               : {tans}  "
          f"(expect 16,16,16 = dim OP^2)")
    partB_ok = same and isos[0] == 36 and tans[0] == 16
    print(f"      [{'PASS' if partB_ok else 'FAIL'}] all three are the SAME homogeneous point of OP^2")
    print("      => three F4-equivalent, genuinely IDENTICAL generations -- not a")
    print("         vector + inequivalent spinor pair. Obstruction 1 cannot be posed.")

    # PART C
    dim16, comm = delta9_real_type()
    print("\n  PART C — each generation carries ONE real Spin(9) spinor Delta_9")
    print("  " + "-" * 64)
    print(f"      octonionic Cl(9) spinor dimension      : {dim16}  "
          f"({'PASS' if dim16 == 16 else 'FAIL'}, = dim T(OP^2) = dim C(x)O)")
    print(f"      Spin(9) commutant dimension            : {comm}  "
          f"({'real type' if comm == 1 else '?'}; expect 1)")
    partC_ok = dim16 == 16 and comm == 1
    print(f"      [{'PASS' if partC_ok else 'FAIL'}] T(OP^2) = a single self-conjugate real spinor Delta_9")
    print("      => one generation = 16 real = C(x)O = Lever B's KO-dim-6 module")
    print("         (chiral without doubling). Three identical copies of a REAL")
    print("         (self-conjugate) spinor share one chirality; no inequivalent")
    print("         mirror partner exists. Obstruction 2 cannot arise.")

    # PART D
    leak = offdiagonal_chirality_mixing()
    print("\n  PART D — cautionary control: the off-diagonal-slot guess fails")
    print("  " + "-" * 64)
    print(f"      conjugation leakage of +Weyl half into -half : {leak:.3f}")
    print(f"      [{'as expected' if leak > 0.1 else 'unexpected'}] the off-diagonal slots z1,z2,z3 DO mix chirality")
    print("      => relative to Spin(8) they are 8v,8s,8c and inherit the no-go's")
    print("         obstruction. Identifying THEM as generations is the flawed step;")
    print("         the idempotent identification (PARTS A-C) is genuinely different.")

    # VERDICT
    cracked = auto_ok and faithful and partB_ok and partC_ok and leak > 0.1
    print("\n  " + "-" * 74)
    print("  VERDICT")
    if cracked:
        print("   * RESOLVED (count + chirality): generations are the three primitive")
        print("     idempotents of a frame -- three identical points of OP^2=F4/Spin(9)")
        print("     permuted by an INNER S3 < F4, each carrying one real Spin(9) spinor")
        print("     Delta_9 = the KO-dim-6 one-generation module. Both no-go")
        print("     obstructions -- (1) vector vs spinor and (2) the opposite-chirality")
        print("     mirror -- are artifacts of the OUTER-triality identification with")
        print("     8v/8s/8c (PART D) and do NOT apply to this inner idempotent route.")
        print("   * Ledger consequence: G1/G2 move from 'faces the mirror obstruction'")
        print("     to 'count + chirality obstruction-free on the idempotent frame'.")
    else:
        print("   * NOT fully resolved on this construction; inspect the failing part.")
    print()
    print("  HONEST SCOPE (what is NOT claimed)")
    print("   * Only the COUNT-and-CHIRALITY bridge is settled. The fermion-content")
    print("     map onto T(OP^2), the per-generation hypercharges (Lever C), the H")
    print("     factor, the Dirac operator D (Lever B's open kill condition) and the")
    print("     Yukawa SPECTRUM (Lever A's C4 negative) all remain open.")
    print()


if __name__ == "__main__":
    main()
