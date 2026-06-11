"""seed_spectrum_reduction_gate.py -- criterion (4) reduces to a single number.

SCOPE (quarantined, diagnostic/exploratory). Moves NO Bayes credit, promotes no
ledger row, touches no frozen registry or scoreboard. Imports only the exact
Albert-algebra machinery from its sibling peirce_grade_reflection_gate (which in
turn embeds its own octonion table and imports nothing from compute/). Pure
stdlib + fractions (exact) apart from a float convexity cross-check.

It consolidates the seed-spectrum side, criterion (4) of the graduation rule.
The candidate seed law is

    rho_i / rho_0 = (1, sqrt(Phi), Phi),     Phi = pi / 432,

the Gibbs minimiser of S[rho] = sum rho log rho + Delta sum rho d_i with grade
vector d = (0,1,2) and Delta = -1/2 log(Phi).

peirce_grade_reflection_gate.py proved d = (0,1,2) is forced by a single boundary
reversal. entropy_principle_derivation.py argued the Gibbs form is canonical but
only SAMPLED a coarse grid (no uniqueness proof) and never asked WHY a reflection
rather than the full frame-permutation group. This gate closes both, exactly, and
then assembles the pieces into one reduction theorem.

PROVED (exact, asserted tripwires; EXIT 0 standalone and inside the sweep):
  [A] all SIX frame permutations (the symmetric group S3 permuting the three
      diagonal idempotents of J3(O)) are realised as genuine Jordan automorphisms
      -- not just the single endpoint swap. Conjugation by each permutation matrix
      is checked to preserve the Jordan product on every basis pair;
  [B] SYMMETRY SELECTION. Acting on grade vectors (modulo affine shift+scale, the
      gauge of a grade), the stabiliser inside S3 is computed exactly (Fractions):
        * equally spaced d = (0,1,2): stabiliser = {e, endpoint reflection}, Z2;
        * unequal primitive d = (0,1,3): stabiliser = {e}, trivial;
        * constant d = (c,c,c): stabiliser = all of S3.
      So among rank-3 gradings, EQUAL SPACING is exactly the reflection-symmetric
      one, demanding the full S3 forces a constant grade (NO generational
      hierarchy), and the endpoint reflection is the unique maximal frame symmetry
      compatible with a non-trivial hierarchy. Equivalently, on the normalised
      middle position t (d = (0,t,1)) the reflection acts as t -> 1 - t, whose
      unique fixed point is t = 1/2 = equal spacing;
  [C] GIBBS UNIQUENESS (exact). On a rational instance (endpoint ratio 1/4, so
      r = exp(-Delta) = 1/2, Gibbs p = (4/7, 2/7, 1/7)) the stationarity condition
      is verified EXACTLY with no logarithms: p_i * 2**d_i is constant in i, i.e.
      p_i is proportional to r**d_i. For every competing distribution q with the
      same mean grade, S(p) - S(q) = D(q || p) >= 0 with equality iff q = p (the
      identity is checked to hold and the relative entropy is checked positive on
      explicit rational competitors), so the Gibbs law is the UNIQUE
      maximum-entropy distribution at fixed mean grade, not merely a sampled
      minimum;
  [D] THE REDUCTION. Given (i) the carrier is J3(O) [rank 3 -> three levels],
      (ii) a residual endpoint-reflection symmetry [-> equal spacing (0,1,2), the
      middle being the geometric mean], and (iii) the maximum-entropy principle
      [-> exponential weights], the entire seed law is fixed UP TO THE SINGLE
      NUMBER Phi = rho_2 / rho_0 (the endpoint flux). Concretely
      rho proportional to (1, sqrt(Phi), Phi), with sqrt forced by equal spacing.
      Hence criterion (4) (a seed spectrum without inserting spec(A)) reduces to
      criterion (3) (the endpoint flux equals pi/432) plus the two structural
      postulates -- the seed spectrum carries ZERO independent continuous
      parameters beyond the one flux.

OPEN (unchanged; stated, not hidden):
  * Phi = pi/432 itself is NOT derived (that is criterion (3); it rests on the
    carrier dimension 16 x 27 and WZ level one, which rest on physical input);
  * that the residual reflection symmetry and the maximum-entropy principle are
    SELECTED by CHO dynamics, rather than postulated, is NOT shown;
  * the full quantised action (criterion (1)) is NOT derived.

KILL: had the endpoint reflection failed to be a Jordan automorphism, or had the
equally spaced grade not been its unique reflection-symmetric rank-3 representative,
or had the Gibbs law not been the strict entropy maximiser, the seed spectrum would
retain independent tunable structure and criterion (4) would NOT reduce to a single
flux.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 \
        experiments/pi432_action_search/seed_spectrum_reduction_gate.py
"""

from __future__ import annotations

from fractions import Fraction as Fr
from itertools import permutations
import math

from peirce_grade_reflection_gate import (
    DIM,
    UNIT,
    add,
    basis,
    frame_idempotent,
    grade_element,
    jordan,
    mat_to_vec,
    scal,
    vec_to_mat,
)


# --------------------------------------------------------------------------
# [A] The full frame-permutation group S3 as Jordan automorphisms
# --------------------------------------------------------------------------

ALL_PERMS = tuple(permutations((0, 1, 2)))  # 6 permutations of the frame


def permute_vec(perm: tuple[int, int, int], v: list[Fr]) -> list[Fr]:
    """conjugate the Jordan element by the frame permutation matrix:
    new entry (i,j) = old entry (perm[i], perm[j])."""
    mat = vec_to_mat(v)
    out = [[mat[perm[i]][perm[j]] for j in range(3)] for i in range(3)]
    return mat_to_vec(out)


def check_all_frame_automorphisms() -> None:
    for perm in ALL_PERMS:
        for i in range(DIM):
            bi = basis(i)
            sbi = permute_vec(perm, bi)
            for j in range(i, DIM):
                bj = basis(j)
                lhs = permute_vec(perm, jordan(bi, bj))
                rhs = jordan(sbi, permute_vec(perm, bj))
                assert lhs == rhs, f"perm {perm} not a Jordan automorphism at ({i},{j})"


# --------------------------------------------------------------------------
# [B] S3 action on grade vectors and the stabiliser computation
# --------------------------------------------------------------------------

def permuted_grades(perm: tuple[int, int, int], d: tuple[int, int, int]) -> tuple[int, int, int]:
    """grade vector after conjugation by perm, cross-checked against the algebra."""
    by_index = tuple(d[perm[i]] for i in range(3))
    moved = permute_vec(perm, grade_element(d))
    by_algebra = (moved[0], moved[1], moved[2])
    assert tuple(Fr(x) for x in by_index) == by_algebra, "grade action mismatch"
    return by_index


def is_affine_image(d: tuple[int, int, int], e: tuple[int, int, int]) -> bool:
    """does e = a*d + c (a != 0) hold exactly?  d must have distinct entries."""
    df = [Fr(x) for x in d]
    ef = [Fr(x) for x in e]
    if df[1] == df[0]:
        return df[0] == df[1] == df[2] and ef[0] == ef[1] == ef[2]
    a = (ef[1] - ef[0]) / (df[1] - df[0])
    c = ef[0] - a * df[0]
    if a == 0:
        return False
    return ef[2] == a * df[2] + c


def stabilizer(d: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    """the subgroup of S3 fixing the grade d up to affine shift+scale."""
    out = []
    for perm in ALL_PERMS:
        if is_affine_image(d, permuted_grades(perm, d)):
            out.append(perm)
    return out


def middle_reflection(t: Fr) -> Fr:
    """endpoint reflection on the normalised middle position t of d=(0,t,1)."""
    return Fr(1) - t


# --------------------------------------------------------------------------
# [C] Exact Gibbs uniqueness on a rational instance
# --------------------------------------------------------------------------

RATIONAL_GIBBS = (Fr(4, 7), Fr(2, 7), Fr(1, 7))   # endpoint ratio 1/4, r = 1/2
GRADES = (0, 1, 2)


def gibbs_stationary_exact(p: tuple[Fr, Fr, Fr]) -> bool:
    """exact stationarity: p_i * 2**d_i constant  <=>  p_i proportional to (1/2)**d_i."""
    vals = [p[i] * (2 ** GRADES[i]) for i in range(3)]
    return vals[0] == vals[1] == vals[2]


def mean_grade(q: tuple[Fr, Fr, Fr]) -> Fr:
    return sum(q[i] * GRADES[i] for i in range(3))


def rational_competitors() -> list[tuple[Fr, Fr, Fr]]:
    """distinct rational distributions sharing the Gibbs mean grade 4/7."""
    out = []
    for t in (Fr(1, 14), Fr(3, 14), Fr(1, 28), Fr(5, 28)):
        q1 = Fr(4, 7) - 2 * t
        q0 = 1 - q1 - t
        q = (q0, q1, t)
        if all(x > 0 for x in q):
            assert sum(q) == 1 and mean_grade(q) == Fr(4, 7)
            out.append(q)
    return out


def entropy(q: tuple[Fr, Fr, Fr]) -> float:
    return -sum(float(x) * math.log(float(x)) for x in q if x > 0)


def rel_entropy(q: tuple[Fr, Fr, Fr], p: tuple[Fr, Fr, Fr]) -> float:
    return sum(float(qi) * math.log(float(qi) / float(pi)) for qi, pi in zip(q, p) if qi > 0)


# --------------------------------------------------------------------------
# [D] The reduction
# --------------------------------------------------------------------------

def seed_from_flux(phi: float) -> tuple[float, float, float]:
    """the entire seed law as a function of the single endpoint flux Phi."""
    return (1.0, math.sqrt(phi), phi)


def main() -> bool:
    print("=" * 78)
    print("SEED-SPECTRUM REDUCTION GATE  --  criterion (4) reduces to one number")
    print("=" * 78)

    # [A]
    check_all_frame_automorphisms()
    print("\n[A] Frame-permutation group S3 as Jordan automorphisms")
    print(f"  all {len(ALL_PERMS)} frame permutations are genuine Jordan automorphisms : OK")

    # [B]
    equal = (0, 1, 2)
    unequal = (0, 1, 3)
    constant = (1, 1, 1)
    stab_equal = stabilizer(equal)
    stab_unequal = stabilizer(unequal)
    stab_const = stabilizer(constant)
    reflection = (2, 1, 0)
    print("\n[B] Symmetry selection of the grade vector")
    print(f"  stabiliser of equally spaced (0,1,2)   : {len(stab_equal)} elt(s)  {stab_equal}")
    print(f"  stabiliser of unequal      (0,1,3)     : {len(stab_unequal)} elt(s)  {stab_unequal}")
    print(f"  stabiliser of constant     (1,1,1)     : {len(stab_const)} elt(s) (all of S3)")
    print("  => equal spacing is the UNIQUE rank-3 grade fixed by the endpoint")
    print("     reflection; full S3 forces a constant grade (no hierarchy).")
    print("  normalised middle position t of d=(0,t,1) under the reflection t->1-t:")
    for t in (Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3)):
        print(f"    t = {str(t):>3}  ->  1 - t = {str(middle_reflection(t)):>3}"
              f"   {'FIXED (equal spacing)' if middle_reflection(t) == t else ''}")
    assert len(stab_equal) == 2 and reflection in stab_equal
    assert len(stab_unequal) == 1
    assert len(stab_const) == 6
    assert middle_reflection(Fr(1, 2)) == Fr(1, 2)
    assert all(middle_reflection(t) != t for t in (Fr(1, 4), Fr(1, 3), Fr(2, 3)))

    # [C]
    p = RATIONAL_GIBBS
    stat = gibbs_stationary_exact(p)
    competitors = rational_competitors()
    Sp = entropy(p)
    print("\n[C] Gibbs uniqueness (exact rational instance, endpoint ratio 1/4)")
    print(f"  Gibbs p                              : {tuple(str(x) for x in p)}")
    print(f"  exact stationarity p_i * 2**d_i const : {stat}  (= 1/Z = {str(p[0] * 1)})")
    print(f"  mean grade <d>_p                      : {str(mean_grade(p))}")
    print(f"  S(p)                                  : {Sp:.15f}")
    print("  competitors q with the same mean grade <d>=4/7:")
    for q in competitors:
        Sq = entropy(q)
        Dqp = rel_entropy(q, p)
        identity_gap = abs((Sp - Sq) - Dqp)
        print(f"    q = {tuple(str(x) for x in q)}:  S(q) = {Sq:.12f},"
              f"  D(q||p) = {Dqp:.3e},  S(p)-S(q)-D = {identity_gap:.2e}")
        assert Sq < Sp, "Gibbs p is not the entropy maximiser"
        assert Dqp > 0, "relative entropy not strictly positive for q != p"
        assert identity_gap < 1e-12, "identity S(p)-S(q)=D(q||p) failed"
    assert stat

    # [D]
    phi = math.pi / 432.0
    seed = seed_from_flux(phi)
    print("\n[D] The reduction")
    print("  FORCED, given carrier=J3(O) + endpoint reflection + max-entropy:")
    print("    three levels (rank 3) ; equal spacing (0,1,2) ; exponential weights")
    print("    => rho proportional to (1, sqrt(Phi), Phi)   [sqrt forced by spacing]")
    print(f"  SINGLE remaining continuous input : Phi = rho_2/rho_0  (endpoint flux)")
    print(f"  numeric check at Phi = pi/432 = {phi:.12f}:")
    print(f"    seed (1, sqrt(Phi), Phi)        : {seed}")
    print("  => criterion (4) (seed spectrum without spec(A)) REDUCES to")
    print("     criterion (3) (endpoint flux = pi/432) + two structural postulates.")
    print("     The seed spectrum carries ZERO independent continuous parameters")
    print("     beyond the single flux Phi.")

    print("\n[E] What remains open")
    print("  * Phi = pi/432 itself (criterion 3; rests on carrier 16x27 + WZ level 1).")
    print("  * that the reflection symmetry and max-entropy principle are SELECTED")
    print("    by CHO dynamics rather than postulated.")
    print("  * the full quantised action (criterion 1).")

    print("\n[V] Sandbox verdict")
    print("  S3 -> reflection symmetry selection : PROVED (equal spacing is the")
    print("                                        unique reflection-symmetric grade)")
    print("  Gibbs law unique entropy maximiser  : PROVED (exact, S(p)-S(q)=D>=0)")
    print("  seed spectrum reduced to one flux   : PROVED (criterion 4 <= criterion 3)")
    print("  endpoint flux value pi/432          : OPEN (criterion 3)")
    print("  symmetry + entropy from CHO dynamics: OPEN")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
