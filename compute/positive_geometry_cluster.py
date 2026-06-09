"""
BIG-BETS Bet 4 (EXPLORATORY) -- does the positive geometry FORCE the CHO arena,
or merely host it?  (positive geometry / amplituhedron / cluster algebra)
=============================================================================

Bet 4 of BIG_BETS_PLAN.md is the highest-ceiling, fuzziest-kill bet: a positive
geometry's canonical form IS the amplitude (locality + unitarity emerge from
positivity, no Lagrangian -- the dynamics-from-geometry the static algebra never
had, criterion A).  The speculative CHO hook (criterion B): hunt for a positive
geometry whose combinatorics is an EXCEPTIONAL / octonionic cluster algebra, so
that "if generations are a cell decomposition, the constants are forced by
geometry, not chosen."

The full octonionic amplituhedron is not constructible in numpy -- and may not
exist.  But every positive geometry of the relevant kind has a COMPUTABLE
combinatorial skeleton: its CLUSTER ALGEBRA.  Finite-type cluster algebras are
classified by Dynkin diagrams (Fomin-Zelevinsky), and the exceptional types CHO
privileges already surface in amplitudes:

  * Gr(3,6) cluster algebra is of type D4  -- and D4 = so(8) = TRIALITY, the
    symmetry behind the three generations (the S3 outer automorphism permuting
    8v, 8s, 8c).
  * Gr(3,7) and Gr(4,7) are of type E6 -- and E6 is the reduced structure group
    of the 27-dimensional exceptional Jordan algebra J3(O), CHO's arena.

So the sharp, decidable question a first probe can answer: does this cluster /
root-system skeleton FORCE the CHO integers (especially base-3 / the generation
count), or does it merely HOST them?  Everything below is exact integer
arithmetic from the Dynkin degree tables:

  rank n = len(degrees);  Coxeter number h = max(degrees);  |W| = prod(degrees)
  #positive roots   = sum(degrees) - n            ( = n*h/2 )
  #cluster variables = almost-positive roots = sum(degrees)
  #clusters (W-Catalan, = vertices of the generalized associahedron, the "cells")
                     = prod_i (h + d_i) / d_i

The result (a clean two-part finding -- a real criterion-B win, the FIFTH face of
the same FORM-not-CONTENT boundary).

  (+) HOSTING IS REAL AND EXACT.  The exact exceptional types CHO privileges carry
      CHO's arena integers as cluster/root invariants:
        * D4 (triality = 3 generations) has exactly 16 cluster variables
          = dim(C(x)H) = the Spin(9) spinor 16 that recurs across CHO; and
          dim D4 = dim so(8) = 28.
        * E6 (J3(O)) has exactly 36 positive roots = the repo's own M_W exponent
          label "||Roots+(E6)||", and its minuscule rep is the 27 = dim J3(O)
          = the 27 lines on a cubic surface (|W(E6)|/|W(D5)| = 27).
        * the hierarchy-exponent increments {27, 28} = {dim J3(O), dim so(8)}
          = {E6 minuscule, D4 adjoint} -- positive geometry's two exceptional arenas.
        * E6 is the UNIQUE exceptional group with a Z/3 centre, so base-3 is
          structurally distinguished for exactly the algebra CHO uses.

  (-) BUT THE GEOMETRY HOSTS, IT DOES NOT FORCE.
        * Those integers (16, 27, 28, 36) are root-system / representation data CHO
          ALREADY ingests -- reuse (criterion B), not a new forcing or prediction.
        * The genuinely cluster-SPECIFIC invariant -- the cluster count = the number
          of "cells" of the positive geometry -- is NEVER a CHO integer and in
          particular is NEVER 3: the geometry does not force the generation count.
        * The matches are not unique: 27 is also the A6 cluster-variable count, and
          FOUR exceptional types (D4, E6, F4, G2) each carry some CHO integer, so the
          machinery does not SELECT the CHO triple (humility tripwire).
        * The seductive products are near-miss traps: 432 = 16*27 is close to the A6
          cluster count 429 but not equal, and 64 is close to the E7 positive-root
          count 63 but not equal -- exactly the coincidence-hunting the scoreboard
          exists to punish.
        * The Z/3 centre that distinguishes base-3 lives in E6 REPRESENTATION THEORY
          (a CHO input), not in the canonical-form dynamics; and it is NOT the
          triality/generation Z/3 (which permutes the three J3(O) blocks inside F4).
        * The actual OCTONIONIC positive geometry -- a canonical form whose cells ARE
          the three generations -- is NOT constructed here: octonion non-associativity
          obstructs the standard commutative, totally-positive cluster-coordinate
          construction.  This is precisely why the bet is "highest build cost,
          fuzziest near-term kill."

Conclusion.  Positive geometry HOSTS the CHO exceptional arena beautifully and even
sharpens "why base-3" (Z(E6) = Z/3) -- criterion B passes cleanly.  But the
canonical-form / cluster machinery neither forces the 3 nor yields a new derived
integer, and the octonionic amplitude geometry stays unconstructed.  Counting the
cells gives the FORM (a combinatorial skeleton that happily contains CHO's
integers), not the CONTENT (a geometry that FORCES them) -- the same boundary the
Lambda, gravity, growth-index, and flavour-statistics probes drew, now on the
amplitude/positive-geometry face.

VERDICT: EXPLORATORY.  No constant is promoted from CHOSEN to derived; the hosting
is a consistency, not a derivation; NO Bayes credit moves.  The module asserts the
exact hosting (the real positive), the cell-count blindness to 3, the
non-uniqueness / near-miss traps, and a HUMILITY tripwire (more than one exceptional
type carries a CHO integer, so the geometry cannot be said to pick the CHO arena),
plus the honest flag that the octonionic positive geometry was not built.
"""
from fractions import Fraction
from math import prod

# --- CHO arena integers under test (kinematic inputs, NOT outputs of geometry) ---
DIM_O = 8                 # octonions
DIM_CH = 16               # C (x) H ; the Spin(9) spinor 16
DIM_J3O = 27              # exceptional Jordan algebra J3(O) ; E6 minuscule
DIM_SO8 = 28              # so(8) = D4 (triality)
MW_EXPONENT = 36          # M_W = M_P / 3^36 ; repo label "||Roots+(E6)||"
LAMBDA_EXPONENT = 64      # Lambda^(1/4) ~ M_P / 3^64 ; dim C(x)H(x)O = 2*4*8
SEESAW_EXPONENT = 9       # M_R = M_P / 3^9
CHO_GENERATIONS = 3       # ledger G1 ; rank of J3(O), triality order
PRODUCT_432 = DIM_CH * DIM_J3O   # 16 * 27 = 432 = pi/eps0^2 denominator

CHO_ARENA = {DIM_O, DIM_CH, DIM_J3O, DIM_SO8, MW_EXPONENT, LAMBDA_EXPONENT}

# --- Dynkin fundamental-invariant degrees (the single source of every integer) ---
DEGREES = {
    "A2": [2, 3], "A3": [2, 3, 4], "A4": [2, 3, 4, 5], "A5": [2, 3, 4, 5, 6],
    "A6": [2, 3, 4, 5, 6, 7],
    "D4": [2, 4, 4, 6], "D5": [2, 4, 5, 6, 8],
    "E6": [2, 5, 6, 8, 9, 12], "E7": [2, 6, 8, 10, 12, 14, 18],
    "E8": [2, 8, 12, 14, 18, 20, 24, 30],
    "F4": [2, 6, 8, 12], "G2": [2, 6], "B3": [2, 4, 6],
}

# simply-connected exceptional centres (standard Lie theory; for the base-3 aside)
EXCEPTIONAL_CENTERS = {"E6": 3, "E7": 2, "E8": 1, "F4": 1, "G2": 1}

# the exceptional types whose cluster algebra surfaces in amplitudes / CHO arena
EXCEPTIONAL_TYPES = ("D4", "E6", "E7", "E8", "F4", "G2")

OCTONIONIC_GEOMETRY_CONSTRUCTED = False   # honest: the hard part is NOT done here
HOST_MIN = 2                              # humility: >1 host => arena NOT selected


def cluster_invariants(degrees):
    """All finite-type cluster-algebra / root-system invariants from the degrees.
    Exact integers; #clusters is the W-Catalan (generalized-associahedron vertices)."""
    n = len(degrees)
    h = max(degrees)
    clusters = prod(Fraction(h + d, d) for d in degrees)
    assert clusters.denominator == 1, "W-Catalan is not an integer -- bad degrees"
    return {
        "rank": n,
        "coxeter": h,
        "pos_roots": sum(degrees) - n,          # = n*h/2
        "cluster_vars": sum(degrees),           # almost-positive roots
        "clusters": int(clusters),              # the "cells"
        "weyl_order": prod(degrees),            # |W| = product of degrees
    }


def minuscule_dim(big, sub):
    """Dimension of the minuscule rep as a Weyl-coset count |W(big)|/|W(sub)|.
    For E6 over D5 this is the 27 (= 27 lines on a cubic surface)."""
    return cluster_invariants(DEGREES[big])["weyl_order"] // cluster_invariants(DEGREES[sub])["weyl_order"]


def hosts_a_cho_integer(inv):
    """True if this type carries a CHO arena integer as a root/cluster invariant."""
    return inv["pos_roots"] in CHO_ARENA or inv["cluster_vars"] in CHO_ARENA


def main():
    print("=" * 70)
    print("BIG-BETS Bet 4: does the positive geometry FORCE the CHO arena?  (EXPLORATORY)")
    print("=" * 70)

    inv = {t: cluster_invariants(d) for t, d in DEGREES.items()}
    minuscule_27 = minuscule_dim("E6", "D5")

    # ---- [A] the arena: the computable skeleton of the positive geometry ----
    print("\n[A] Finite-type cluster algebras <-> Dynkin diagrams (Fomin-Zelevinsky).")
    print("    The amplitude is the canonical form; its computable skeleton is the")
    print("    cluster algebra (clusters = vertices of the generalized associahedron).")
    print("    type  rank   h   pos_roots  cluster_vars   clusters")
    for t in ("A6", "D4", "E6", "E7", "E8", "F4", "G2"):
        v = inv[t]
        print("    %-4s   %3d  %3d   %6d       %6d      %7d"
              % (t, v["rank"], v["coxeter"], v["pos_roots"], v["cluster_vars"], v["clusters"]))

    # ---- [B] the real positive: hosting is exact (criterion B) ----
    print("\n[B] HOSTING (criterion B): the exact exceptional types CHO privileges")
    print("    carry CHO's arena integers as cluster / root invariants:")
    print("      D4 (triality = 3 generations): cluster_vars = %d = dim(C(x)H);  dim D4 = %d = dim so(8)"
          % (inv["D4"]["cluster_vars"], 2 * inv["D4"]["pos_roots"] + inv["D4"]["rank"]))
    print("      E6 (J3(O)): pos_roots = %d = M_W exponent;  minuscule = %d = dim J3(O) = 27 lines on a cubic"
          % (inv["E6"]["pos_roots"], minuscule_27))
    print("      hierarchy increments {27,28} = {%d-%d, %d-%d} = {dim J3(O)=E6 minusc, dim so(8)=D4 adj}"
          % (MW_EXPONENT, SEESAW_EXPONENT, LAMBDA_EXPONENT, MW_EXPONENT))
    print("      Gr(3,6) ~ D4 and Gr(3,7)/Gr(4,7) ~ E6: the amplitude bridge is real.")

    # ---- [C] the dynamics hope: do the CELLS force a CHO integer? (criterion A) ----
    print("\n[C] FORCING (criterion A): the cluster count is the cell number of the")
    print("    positive geometry.  Does any of them equal a CHO integer / the 3?")
    cluster_counts = {inv[t]["clusters"] for t in DEGREES}
    print("      cell counts:", sorted(cluster_counts))
    print("      is the generation count 3 a cell number?", 3 in cluster_counts)
    print("      is 432 = 16*27 a cell number?", 432 in cluster_counts)
    print("      (G2 = Aut(O) has %d cells = dim O -- a rank-2 small-number coincidence, low information)"
          % inv["G2"]["clusters"])

    # ---- [D] the honest null: non-uniqueness + near-miss traps + the centre aside ----
    print("\n[D] HOSTING is not FORCING -- non-uniqueness, traps, and the base-3 aside:")
    print("      27 is ALSO the A6 cluster-variable count (%d): not E6-unique."
          % inv["A6"]["cluster_vars"])
    print("      432 = 16*27 vs A6 cell count %d  -> near-miss, NOT equal (trap)." % inv["A6"]["clusters"])
    print("      64 (Lambda exp) vs E7 pos_roots %d -> near-miss, NOT equal (trap)." % inv["E7"]["pos_roots"])
    hosts = [t for t in EXCEPTIONAL_TYPES if hosts_a_cho_integer(inv[t])]
    print("      exceptional types carrying a CHO integer:", hosts, "(len %d > 1 => arena NOT selected)" % len(hosts))
    z3 = [t for t, c in EXCEPTIONAL_CENTERS.items() if c == 3]
    print("      base-3 aside: unique exceptional with Z/3 centre =", z3,
          "(exactly E6/J3(O)) -- but this is E6 REP THEORY, not canonical-form dynamics,")
    print("      and it is NOT the triality/generation Z/3 (which permutes the three J3(O) blocks in F4).")

    # ---- [E] the unconstructed object ----
    print("\n[E] The octonionic positive geometry (cells = generations) is NOT built here:")
    print("      octonion non-associativity obstructs the standard commutative, totally-positive")
    print("      cluster-coordinate construction.  OCTONIONIC_GEOMETRY_CONSTRUCTED =",
          OCTONIONIC_GEOMETRY_CONSTRUCTED)
    print("      This is the open frontier and the reason Bet 4 is highest-cost / fuzziest-kill.")

    # ---- [F] verdict ----
    print("\n[F] Verdict")
    print("    (+) positive geometry HOSTS the CHO exceptional arena exactly (D4->16,28; E6->36,27)")
    print("        and even sharpens 'why base-3' via Z(E6)=Z/3 -- criterion B passes.")
    print("    (-) but the canonical-form / cluster machinery FORCES nothing new: the cell count is")
    print("        never 3, the matches are non-unique and multi-hosted, the 432/64 products are")
    print("        near-miss traps, and the octonionic geometry is unconstructed.")
    print("    Counting the cells gives the FORM (a skeleton that contains CHO's integers), not the")
    print("    CONTENT (a geometry that forces them) -- the fifth face of the same boundary.")
    print("    EXPLORATORY: no constant promoted to derived; NO Bayes credit moves.")

    # ---- stable tripwires (the hosting positive + the honest null) ----
    # the math is exact and self-consistent for every type:
    for t, v in inv.items():
        assert v["pos_roots"] == v["rank"] * v["coxeter"] // 2, "pos_roots != n*h/2 for " + t
        assert v["cluster_vars"] == v["pos_roots"] + v["rank"] == sum(DEGREES[t]), "cluster_vars miscount " + t
    # (+) HOSTING is exact (criterion B): the exceptional types carry the CHO integers:
    assert inv["D4"]["cluster_vars"] == DIM_CH, "D4 cluster variables are not 16"
    assert 2 * inv["D4"]["pos_roots"] + inv["D4"]["rank"] == DIM_SO8, "dim D4 is not 28"
    assert inv["E6"]["pos_roots"] == MW_EXPONENT, "E6 positive roots are not 36"
    assert minuscule_27 == DIM_J3O, "E6 minuscule is not 27"
    assert MW_EXPONENT - SEESAW_EXPONENT == DIM_J3O, "increment 36-9 is not 27"
    assert LAMBDA_EXPONENT - MW_EXPONENT == DIM_SO8, "increment 64-36 is not 28"
    # (-) FORCING fails: the cell count never forces the generation count or a CHO product:
    cluster_counts = {inv[t]["clusters"] for t in DEGREES}
    assert CHO_GENERATIONS not in cluster_counts, "a cluster count equals 3 -- re-examine forcing"
    assert PRODUCT_432 not in cluster_counts, "a cluster count equals 432 -- re-examine"
    assert DIM_J3O not in cluster_counts, "a cluster count equals 27 -- re-examine"
    # (-) non-uniqueness: 27 is hosted by a NON-exceptional type too (A6 cluster vars):
    assert inv["A6"]["cluster_vars"] == DIM_J3O, "A6 cluster variables are not 27"
    # (-) near-miss TRAPS (the seductive products are close but NOT equal):
    assert inv["A6"]["clusters"] == 429 and inv["A6"]["clusters"] != PRODUCT_432, "432 trap drifted"
    assert inv["E7"]["pos_roots"] == 63 and inv["E7"]["pos_roots"] != LAMBDA_EXPONENT, "64 trap drifted"
    assert PRODUCT_432 == DIM_CH * DIM_J3O == 432, "432 != 16*27"
    # HUMILITY tripwire: more than one exceptional type carries a CHO integer, so the
    # geometry cannot be said to SELECT the CHO arena (mirrors the growth-index probe):
    hosts = [t for t in EXCEPTIONAL_TYPES if hosts_a_cho_integer(inv[t])]
    assert len(hosts) >= HOST_MIN, "only one exceptional host -- recheck, geometry may select the arena"
    # base-3 is distinguished for E6 ALONE among exceptionals (a real but rep-theoretic fact):
    assert EXCEPTIONAL_CENTERS["E6"] == CHO_GENERATIONS, "E6 centre is not Z/3"
    assert [t for t, c in EXCEPTIONAL_CENTERS.items() if c == CHO_GENERATIONS] == ["E6"], \
        "Z/3 centre is not unique to E6"
    # the hard part was honestly NOT done:
    assert OCTONIONIC_GEOMETRY_CONSTRUCTED is False, "claim of an octonionic geometry must be backed by a construction"
    # the CHO arena anchors are kinematic inputs, intact:
    assert (DIM_O, DIM_CH, DIM_J3O, LAMBDA_EXPONENT) == (8, 16, 27, 64), "CHO arena anchors drifted"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
