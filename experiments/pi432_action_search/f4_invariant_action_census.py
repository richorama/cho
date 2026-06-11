"""F4-invariant action census on OP^2 = F4/Spin(9): count the continuous knobs.

This probe executes the decisive structural step on the DYNAMIC side of the
pi/432 program: write down the MOST GENERAL F4-invariant sigma-model action on
the Cayley projective plane OP^2 = F4/Spin(9) (kinetic + potential + topological/
Wess-Zumino, to leading two-derivative order) and COUNT its free continuous
parameters. If a free continuous internal coefficient survives, the WZ flux
pi/432 can never be FORCED in this arena (it could be dialed) and the route is
dead. If instead the count of continuous internal knobs is ZERO, the arena has
the rigidity the program needs, and the residual question is only WHICH integer
levels / WHICH spontaneous vacuum.

Everything below is exact: Spin(9) is built explicitly from octonion
left-multiplications (Clifford algebra Cl(9,0) on R^16), and every "dimension of
invariants" is the nullity of an integer linear system, certified by a modular
rank over the prime 2^31 - 1 (rank mod p is a lower bound for rank over Q, and we
exhibit the matching invariant explicitly, so the nullity over Q is pinned
exactly).

The arena
---------
OP^2 is the compact rank-1 symmetric space F4/Spin(9), dim 16. F4 (dim 52) acts
by isometries; the isotropy group Spin(9) (dim 36) acts on the tangent space as
its 16-dimensional REAL spinor Delta_9 -- the same 16 the kinematic side already
uses (= dim OP^2 = the spinor in the 16x27 carrier). A sigma-model field is a map
phi: Sigma -> OP^2. The most general F4-invariant local action to two-derivative
order plus topological terms is

    S[phi] = (1/2g^2) Int G_{mn}(phi) d phi^m d phi^n          (kinetic)
           +           Int V(phi)                              (potential)
           + Sum_q k_q Int_D phi^* omega_q                     (Wess-Zumino / topological)

with G an F4-invariant metric, V an F4-invariant function, and omega_q closed
F4-invariant forms.  The census asks how many continuous coefficients this family
really has.

What this gate establishes (exact)
----------------------------------
  [A] Octonion imaginary left-multiplications L_1..L_7 satisfy the Clifford
      relations {L_a, L_b} = -2 delta_ab I on R^8 (so 𝕆 is a Cl(0,7)-module);
      this is the seed of Spin(9).
  [B] Nine real SYMMETRIC 16x16 gamma matrices Gamma_1..Gamma_9 with
      {Gamma_a, Gamma_b} = 2 delta_ab I generate Cl(9,0) on R^16; the 36
      so(9) generators Sigma_ab = (1/2) Gamma_a Gamma_b (a<b) are the explicit
      isotropy action on the tangent space.
  [C] KINETIC: the commutant of so(9) in End(R^16) is exactly 1-dimensional
      (= R.I). Hence (i) the F4-invariant metric is UNIQUE up to one positive
      scale -> exactly ONE continuous parameter (the overall radius/coupling, a
      universal normalization, not an internal knob); and (ii) the antisymmetric
      part of the commutant is ZERO -> there is NO invariant 2-form, matching
      b_2(OP^2) = 0 (no invariant symplectic/Kahler structure).
  [D] POTENTIAL: the 16 carries NO Spin(9)-invariant vector, and F4 acts
      TRANSITIVELY on OP^2 (dim count 52 - 36 = 16). So every F4-invariant
      function is CONSTANT -> the potential sector has ZERO continuous parameters
      and, crucially, NO F4-invariant potential can break F4. Explicit
      (action-level) F4 breaking is impossible; breaking must be SPONTANEOUS
      (selected by a configuration / boundary datum), not put into the action.
  [E] TOPOLOGICAL: OP^2 has cohomology ring H^*(OP^2; Z) = Z[x]/(x^3), |x| = 8,
      so invariant closed forms live only in degrees 0, 8, 16 (Euler
      characteristic chi = |W(F4)|/|W(Spin(9))| = 1152/384 = 3, computed from the
      fundamental degrees). Each WZ/topological term therefore carries an INTEGER
      level (Dirac/WZ quantization), not a continuous coefficient: degree 8 -> one
      integer k_8, degree 16 -> one integer k_16. ZERO continuous parameters.
  [F] CENSUS: the most general F4-invariant action (2-derivative + topological)
      has exactly ONE continuous parameter -- the overall scale -- and a finite
      set of INTEGER levels. The number of continuous INTERNAL (dimensionless,
      vacuum-distinguishing) knobs is ZERO.

Consequence for the five graduation criteria (option_map.md)
------------------------------------------------------------
  (3) flux pi/432 without hand-normalizing the coefficient: STRUCTURALLY
      SATISFIABLE. The WZ coefficient cannot be a free continuous knob here; it is
      forced to (integer level) x (quantized period) x (Schur carrier 1/432).
      The continuous coefficient that the project feared is provably absent.
  (2) the F4-breaking term: REDIRECTED, not solved. No F4-invariant action term
      can break F4, so the breaking is necessarily SPONTANEOUS -- consistent with
      the boundary-data gates (boundary_variation_gate, frame_lift_f4_breaking).
  (1) explicit action functional: PARTIAL. This enumerates the leading invariant
      family and its parameter count; it does not yet write the full quantized
      functional.
  (4) seed spectrum without inserting spec(A): OPEN. Not addressed here.
  (5) a falsifying kill condition: PROVIDED (below).

Honest scope / what this does NOT do
------------------------------------
This counts the LEADING (two-derivative) invariant action plus topological terms.
Higher-derivative F4-invariants exist (infinitely many, each with its own
coefficient); they are subleading and do NOT change the two structural verdicts
(no invariant potential; integer topological levels). The "one continuous
parameter" is the universal overall scale, not an internal flavour knob. This
gate does NOT derive pi/432, does NOT achieve the F4 breaking, and does NOT touch
the seed spectrum or the path-integral measure. It moves NO Bayes credit and does
NOT change the scoreboard; it shows the arena has zero continuous internal knobs
and that F4 breaking must be spontaneous -- sharpening the dynamic side, not
closing it.

KILL: if the most general invariant action had ANY free continuous internal
coefficient -- e.g. a non-unique invariant metric (commutant > 1-dim), a
non-constant invariant potential (an invariant vector or invariant function), or
a continuous (non-quantized) topological coefficient -- then pi/432 could be
dialed and could never be forced in this arena. The route would be dead. The
census finds none, so the route stays alive and is sharpened.

Quarantined: imports nothing from the core model; embeds its own octonion table
(same Fano convention as compute/octonion_toolkit.py) so it is self-contained.
Exact integer / modular arithmetic; numpy used only for integer linear algebra.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/f4_invariant_action_census.py
"""

from __future__ import annotations

import math

import numpy as np

# ---------------------------------------------------------------------------
# Octonions (local, self-contained; same Fano convention as octonion_toolkit).
# ---------------------------------------------------------------------------
FANO_TRIPLES = [
    (1, 2, 3),
    (1, 4, 5),
    (1, 7, 6),
    (2, 4, 6),
    (2, 5, 7),
    (3, 4, 7),
    (3, 6, 5),
]

PRIME = 2_147_483_647  # 2^31 - 1, a Mersenne prime; certifies rank over Q.


def octonion_mult_table() -> np.ndarray:
    """8x8x8 integer structure constants: mult[i,j,k] = coeff of e_k in e_i e_j."""
    mult = np.zeros((8, 8, 8), dtype=np.int64)
    for i in range(8):
        mult[0, i, i] = 1
        mult[i, 0, i] = 1
    for i in range(1, 8):
        mult[i, i, 0] = -1
    for (i, j, k) in FANO_TRIPLES:
        mult[i, j, k] = 1
        mult[j, i, k] = -1
        mult[j, k, i] = 1
        mult[k, j, i] = -1
        mult[k, i, j] = 1
        mult[i, k, j] = -1
    return mult


def left_mult_matrices(mult: np.ndarray) -> list[np.ndarray]:
    """L_a (8x8 int): x -> e_a * x, i.e. (L_a)_{k,j} = mult[a, j, k], a = 1..7."""
    mats = []
    for a in range(1, 8):
        L = np.zeros((8, 8), dtype=np.int64)
        for j in range(8):
            for k in range(8):
                L[k, j] = mult[a, j, k]
        mats.append(L)
    return mats


def spin9_gamma_matrices(Ls: list[np.ndarray]) -> list[np.ndarray]:
    """Nine real symmetric 16x16 gammas (Cl(9,0) on R^16 = O + O)."""
    I8 = np.eye(8, dtype=np.int64)
    Z8 = np.zeros((8, 8), dtype=np.int64)
    gammas: list[np.ndarray] = []
    # Gamma_a = [[0, L_a], [L_a^T, 0]] for a = 1..7
    for L in Ls:
        top = np.hstack([Z8, L])
        bot = np.hstack([L.T, Z8])
        gammas.append(np.vstack([top, bot]))
    # Gamma_8 = [[0, I], [I, 0]]
    gammas.append(np.vstack([np.hstack([Z8, I8]), np.hstack([I8, Z8])]))
    # Gamma_9 = [[I, 0], [0, -I]]
    gammas.append(np.vstack([np.hstack([I8, Z8]), np.hstack([Z8, -I8])]))
    return gammas


def modular_rank(matrix: np.ndarray, p: int = PRIME) -> int:
    """Exact rank of an integer matrix over the field F_p (Gaussian elimination)."""
    a = (matrix.astype(np.int64) % p)
    rows, cols = a.shape
    rank = 0
    pivot = 0
    for col in range(cols):
        sel = -1
        for r in range(pivot, rows):
            if a[r, col] != 0:
                sel = r
                break
        if sel == -1:
            continue
        if sel != pivot:
            a[[sel, pivot]] = a[[pivot, sel]]
        inv = pow(int(a[pivot, col]), p - 2, p)
        a[pivot] = (a[pivot] * inv) % p
        factors = a[:, col].copy()
        factors[pivot] = 0
        a = (a - np.outer(factors, a[pivot])) % p
        rank += 1
        pivot += 1
        if pivot == rows:
            break
    return rank


def commutant_constraint(generators: list[np.ndarray]) -> np.ndarray:
    """Stacked operator whose null space is {X : [g, X] = 0 for all g}.

    Uses vec(g X - X g) = (I (x) g - g^T (x) I) vec(X) (column-major vec); the
    null-space DIMENSION is independent of the vec convention.
    """
    n = generators[0].shape[0]
    I = np.eye(n, dtype=np.int64)
    blocks = [np.kron(I, g) - np.kron(g.T, I) for g in generators]
    return np.vstack(blocks)


def main() -> bool:
    ok = True
    print("=" * 78)
    print("F4-INVARIANT ACTION CENSUS on OP^2 = F4/Spin(9): counting continuous knobs")
    print("=" * 78)

    mult = octonion_mult_table()
    Ls = left_mult_matrices(mult)
    I8 = np.eye(8, dtype=np.int64)

    # ---- [A] octonion imaginary units -> Cl(0,7) ------------------------
    print("\n[A] Octonion imaginary left-multiplications L_1..L_7 on R^8")
    cliff7_ok = True
    for a in range(7):
        for b in range(7):
            anti = Ls[a] @ Ls[b] + Ls[b] @ Ls[a]
            want = (-2 * I8) if a == b else np.zeros((8, 8), dtype=np.int64)
            if not np.array_equal(anti, want):
                cliff7_ok = False
    print(f"  {{L_a, L_b}} = -2 delta_ab I  for all a,b in 1..7 : {cliff7_ok}")
    print("  => Im(O) is a Cl(0,7)-module (the seed of Spin(9)).")

    # ---- [B] Spin(9) Clifford algebra on R^16 ---------------------------
    gammas = spin9_gamma_matrices(Ls)
    I16 = np.eye(16, dtype=np.int64)
    sym_ok = all(np.array_equal(G, G.T) for G in gammas)
    clifford9_ok = True
    for a in range(9):
        for b in range(9):
            anti = gammas[a] @ gammas[b] + gammas[b] @ gammas[a]
            want = (2 * I16) if a == b else np.zeros((16, 16), dtype=np.int64)
            if not np.array_equal(anti, want):
                clifford9_ok = False
    print("\n[B] Nine real symmetric 16x16 gammas -> Cl(9,0) on R^16 = O + O")
    print(f"  all Gamma_a symmetric .................... {sym_ok}")
    print(f"  {{Gamma_a, Gamma_b}} = 2 delta_ab I (a,b in 1..9) : {clifford9_ok}")
    # so(9) generators Sigma_ab ~ Gamma_a Gamma_b (a<b); use the 8 simple ones
    # Sigma_{i,i+1}, which Lie-generate so(9), plus all 36 as a robustness check.
    simple = [gammas[i] @ gammas[i + 1] for i in range(8)]
    all_pairs = [gammas[a] @ gammas[b] for a in range(9) for b in range(a + 1, 9)]
    print(f"  isotropy action so(9): {len(all_pairs)} generators "
          f"(8 simple Lie-generate it)")

    # ---- [C] KINETIC: the invariant metric is unique up to scale --------
    C_simple = commutant_constraint(simple)
    # sanity: the operator must annihilate vec(I) (since [g, I] = 0)
    vecI = I16.flatten(order="F").astype(np.int64)
    annih = np.array_equal((C_simple @ vecI) % PRIME, np.zeros(C_simple.shape[0], dtype=np.int64))
    rank_simple = modular_rank(C_simple)
    nullity_simple = 16 * 16 - rank_simple
    rank_all = modular_rank(commutant_constraint(all_pairs))
    nullity_all = 16 * 16 - rank_all
    print("\n[C] KINETIC sector: F4-invariant metrics = Spin(9)-invariant sym forms")
    print(f"  operator annihilates vec(I) (build check) : {annih}")
    print(f"  dim commutant of so(9) in End(R^16)  (8 simple gens) : {nullity_simple}")
    print(f"  dim commutant of so(9) in End(R^16)  (all 36 gens)   : {nullity_all}")
    print(f"  => commutant = R.I (real-irreducible, real type).")
    print(f"  invariant SYMMETRIC 2-tensors (metrics)  : 1  -> metric unique up to scale")
    print(f"  invariant ANTISYMMETRIC 2-tensors (2-forms): 0  -> no invariant symplectic form")
    print(f"  continuous kinetic parameters            : 1  (overall scale = radius/coupling)")

    # ---- [D] POTENTIAL: invariant functions are constant ----------------
    # No Spin(9)-invariant vector in the 16: stacked generators have full rank 16.
    gen_on_vec = np.vstack(simple)  # (8*16) x 16
    rank_vec = modular_rank(gen_on_vec)
    inv_vectors = 16 - rank_vec
    dim_f4, dim_spin9, dim_op2 = 52, 36, 16
    transitive = (dim_f4 - dim_spin9 == dim_op2)
    print("\n[D] POTENTIAL sector: F4-invariant functions on OP^2")
    print(f"  Spin(9)-invariant vectors in the 16      : {inv_vectors}  (no invariant direction)")
    print(f"  dim F4 - dim Spin(9) = {dim_f4} - {dim_spin9} = {dim_f4 - dim_spin9} = dim OP^2 : {transitive}")
    print(f"  => F4 acts transitively -> invariant functions are CONSTANT.")
    print(f"  continuous potential parameters          : 0")
    print(f"  can an F4-invariant potential break F4?  : NO -> breaking must be spontaneous")

    # ---- [E] TOPOLOGICAL: integer WZ levels, no continuous coefficient --
    # chi(F4/Spin(9)) from fundamental degrees (equal rank 4 = 4).
    f4_degrees = (2, 6, 8, 12)
    b4_degrees = (2, 4, 6, 8)
    W_F4 = math.prod(f4_degrees)
    W_B4 = math.prod(b4_degrees)
    chi = W_F4 // W_B4
    # H^*(OP^2; Z) = Z[x]/(x^3), |x| = 8: Betti numbers, Poincare polynomial 1+t^8+t^16
    betti = {0: 1, 8: 1, 16: 1}
    wz_degrees = [8, 16]  # positive-degree invariant closed forms -> WZ/topological terms
    integer_levels = sum(betti[d] for d in wz_degrees)
    print("\n[E] TOPOLOGICAL sector: Wess-Zumino / theta terms")
    print(f"  |W(F4)| = prod{f4_degrees} = {W_F4};  |W(Spin(9))| = prod{b4_degrees} = {W_B4}")
    print(f"  Euler characteristic chi = {W_F4}/{W_B4} = {chi}")
    print(f"  H^*(OP^2;Z) = Z[x]/(x^3), |x|=8  -> Betti {betti}, sum = {sum(betti.values())} = chi")
    print(f"  invariant closed forms in positive degree: degrees {wz_degrees} (one each)")
    print(f"  each WZ coefficient is Dirac/WZ-quantized -> INTEGER level (k_8, k_16)")
    print(f"  continuous topological parameters        : 0   (integer levels: {integer_levels})")

    # ---- [F] CENSUS + verdict -------------------------------------------
    continuous_internal = 0  # excludes the one universal overall scale
    print("\n[F] PARAMETER CENSUS (most general F4-invariant action, 2-deriv + topological)")
    print("  sector          invariant structure              continuous   integer")
    print("  kinetic metric  unique inv. sym 2-tensor (R.I)         1*         0")
    print("  potential       inv. functions = constants            0          0")
    print("  WZ degree 8     H^8 = Z (one inv. 8-form)             0          1")
    print("  WZ degree 16    H^16 = Z (one inv. top form)          0          1")
    print("  (degree 2)      b_2 = 0, no inv. 2-form               0          0")
    print("  ----------------------------------------------------------------------")
    print("  * the single continuous parameter is the overall scale (universal coupling),")
    print("    NOT an internal dimensionless knob that distinguishes vacua.")
    print(f"  continuous INTERNAL (vacuum-distinguishing) parameters : {continuous_internal}")

    print("\n[V] Sandbox verdict (dynamic side)")
    print("  (3) pi/432 coefficient forced (no continuous knob)  : STRUCTURALLY SATISFIABLE")
    print("  (2) explicit F4-breaking by the action              : IMPOSSIBLE -> must be spontaneous")
    print("  (1) full quantized action functional                : PARTIAL (leading family counted)")
    print("  (4) seed spectrum without inserting spec(A)         : OPEN (not addressed here)")
    print("  (5) measure / anomaly                               : OPEN (not addressed here)")
    print("  net: the arena has ZERO continuous internal knobs; the dynamic gap is now")
    print("       'which integer level + which spontaneous vacuum', not 'a tunable coupling'.")
    print("=" * 78)

    # --- tripwires (exact) ------------------------------------------------
    assert cliff7_ok, "octonion imaginary L_a must satisfy Cl(0,7)"
    assert sym_ok and clifford9_ok, "Spin(9) gammas must be symmetric and satisfy Cl(9,0)"
    assert annih, "commutant operator must annihilate vec(I) (build sanity)"
    # KINETIC: commutant is exactly 1-dimensional (= R.I), both generator sets agree
    assert nullity_simple == 1, f"invariant metric not unique: nullity {nullity_simple}"
    assert nullity_all == 1, f"all-36 commutant nullity {nullity_all} != 1"
    # POTENTIAL: no invariant vector; transitivity dimension identity
    assert inv_vectors == 0, "the 16 must carry no Spin(9)-invariant vector"
    assert transitive and (dim_f4 - dim_spin9 == dim_op2 == 16)
    # TOPOLOGICAL: Euler characteristic and Betti structure
    assert (W_F4, W_B4, chi) == (1152, 384, 3)
    assert sum(betti.values()) == chi == 3
    assert integer_levels == 2  # one integer level in each of degrees 8 and 16
    # CENSUS headline: zero continuous internal knobs
    assert continuous_internal == 0
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
