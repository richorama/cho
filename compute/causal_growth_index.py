"""
BIG-BETS Bet 2 crux (EXPLORATORY) -- does growth SEE the internal CHO index?
============================================================================

This is the make-or-break test the two earlier Bet-2 probes deferred.  The
synthesis idea (causal sets x CHO) is the only one with the ceiling to revive the
*physics* claim, because causal-set growth supplies the one object the static
algebra never could -- a measure on histories (dynamics from counting).  The two
prior modules drew the same boundary from opposite sides:

  * causal_set_lambda / everpresent_lambda_tracking : counting fixes Lambda's
    MAGNITUDE (a volume fluctuation), but the CHO exponent is a SPECTATOR -- the
    testable time-structure is causal-set content, invariant under the CHO number.
  * entropic_gravity_cho : counting fixes the FORM of horizon entropy (the area
    law), but the CHO internal dimension is pure bit-bookkeeping -- it never
    touches the coefficient 1/4 = G.

Both say: counting gives the FORM, never the CHO CONTENT.  The open question -- the
one that would actually CREDIT CHO rather than relocate a mystery -- is whether the
*growth dynamics itself* can see an internal index living on each causet element,
and thereby FORCE the generation count N = 3 (kinematically an input from
jordan_eigenvalue_generations / three_generations_frame, ledger G1) while supplying
the action.  That is the (B)/(C) test in BIG_BETS_PLAN.md.  This module runs it.

The model.  Rideout-Sorkin classical sequential growth, the clean transitive-
percolation case, defined via i.i.d. pre-closure pair inclusions + transitive
closure (so both CSG axioms are explicit and checkable):

  * INTERNAL TEMPORALITY: an element is born to the future of (or spacelike to)
    existing ones, so a relation always points earlier-born -> later-born.
  * DISCRETE GENERAL COVARIANCE: the probability of a given *unlabelled* causet is
    birth-order independent.  Computable form used here: every linear extension
    (birth order) of a fixed decorated poset must have EQUAL growth probability.
  * BELL CAUSALITY: spacelike births are independent.  The independent-pair model
    realises this by construction -- the growth probability is a product over
    pairs -- for ANY coupling and ANY index cardinality N.

Attach an internal index s_i in {1..N} to each element and let it COUPLE to the
growth via a pairwise inclusion probability p(s_i, s_j).  Then ask the two axioms
what they say about N.

The result (a clean, exact NEGATIVE -- the third face of the same boundary).
  * Covariance constrains the COUPLING, not the cardinality.  A related pair always
    has the lower element born first, so its factor p(s_lo, s_hi) is extension-
    independent automatically; an INCOMPARABLE pair {a,b} appears as 1 - p(s_a,s_b)
    in one birth order and 1 - p(s_b,s_a) in another, so covariance <=> the coupling
    is SYMMETRIC.  Symmetric N x N couplings exist for EVERY N: covariance leaves an
    N(N+1)/2-parameter family, never empty, so it never singles out N = 3.
  * Bell causality is automatic in the independent-pair model for every N (the
    measure factorises over pairs) -- also blind to N.
  * SPECTATOR limit: an index-blind coupling makes the causet marginal literally
    N-independent (growth blindness TV = 0 for all N).
  * Best shot for CHO -- a non-trivial INHERITANCE map (child index = product of
    parent indices): demanding it be covariant + commutative + associative is
    satisfied by Z/N for EVERY N, so even that does not force 3.  The exceptional
    rank-3 Albert algebra J3(O) is singled out only by the NON-ASSOCIATIVE
    octonionic composition -- a kinematic (Hurwitz/Jordan classification) input, not
    something the order-theoretic growth provides.

Conclusion.  The growth dynamics is provably BLIND to the internal index's
cardinality.  It can carry a CHO index as a covariant passenger but cannot SELECT
N = 3; the generation count stays a kinematic input (G1).  Counting supplies the
FORM (a covariant, Bell-causal measure on histories -- gold-standard criterion A)
but not the CONTENT (N = 3) -- exactly the boundary the Lambda and gravity probes
drew.  This resolves the Bet-2 crux as a NEGATIVE.

VERDICT: EXPLORATORY.  N = 3 is NOT derived from dynamics; G1 untouched; no
prediction promoted; NO Bayes credit moves.  The module asserts the covariance
obstruction, the N-blindness, and a HUMILITY tripwire (more than one N admits a
covariant non-spectator coupling, so the dynamics cannot be said to "pick 3").
"""
import itertools

import numpy as np

# --- CHO kinematic inputs under test (NOT outputs of this dynamics) ---
CHO_GENERATIONS = 3       # ledger G1: jordan_eigenvalue_generations / three_generations_frame
JORDAN_RANK = 3           # rank of J3(O); the "3" we ask the growth to reproduce

# --- transitive-percolation demonstration parameters ---
P_DEFAULT = 0.4           # index-blind inclusion probability for the baseline measure
N_RANGE = (2, 3, 4, 5, 6)  # internal-index cardinalities swept for covariance
COV_TOL = 1e-12           # max-min growth prob below this == covariant (path-independent)
BREAK_MIN = 1e-3          # an asymmetric coupling must break covariance by at least this
SELECTED_MIN = 2          # humility: >1 admissible N => dynamics does NOT pick a unique N


# ----------------------------------------------------------------------
# The four unlabelled posets on 3 elements that we exercise.
# rel[i, j] = 1  means  i < j  (i below j).
# ----------------------------------------------------------------------
def _poset(relations):
    R = np.zeros((3, 3), dtype=int)
    for i, j in relations:
        R[i, j] = 1
    return R


V_POSET = _poset([(0, 1), (0, 2)])          # 0 below 1 and 2; {1,2} incomparable
ANTICHAIN = _poset([])                       # no relations
CHAIN = _poset([(0, 1), (1, 2), (0, 2)])     # 0 < 1 < 2
LAMBDA_POSET = _poset([(0, 2), (1, 2)])      # 0 and 1 below 2; {0,1} incomparable
POSETS = {"V": V_POSET, "antichain": ANTICHAIN, "chain": CHAIN, "Lambda": LAMBDA_POSET}


def linear_extensions(rel):
    """All birth orders (permutations) consistent with internal temporality:
    if i < j (rel[i,j]) then i is born before j."""
    n = rel.shape[0]
    exts = []
    for perm in itertools.permutations(range(n)):
        pos = {slot: t for t, slot in enumerate(perm)}
        if all(pos[a] < pos[b] for a in range(n) for b in range(n) if rel[a, b]):
            exts.append(perm)
    return exts


def growth_prob(rel, s, p_of, birth_order):
    """Sequential-growth probability of the fixed decorated labelled causet
    (rel, indices s) grown in birth_order.  Product over pairs == Bell causality."""
    n = rel.shape[0]
    pos = {slot: t for t, slot in enumerate(birth_order)}
    prob = 1.0
    for a in range(n):
        for b in range(a + 1, n):
            e, l = (a, b) if pos[a] < pos[b] else (b, a)   # earlier, later born
            if rel[e, l]:
                prob *= p_of(s[e], s[l])                   # related: lower born first
            elif rel[l, e]:
                raise AssertionError("birth_order is not a linear extension")
            else:
                prob *= (1.0 - p_of(s[e], s[l]))           # incomparable
    return prob


def covariance_spread(rel, s, p_of):
    """max - min growth probability over all linear extensions.  0 <=> covariant."""
    vals = [growth_prob(rel, s, p_of, pi) for pi in linear_extensions(rel)]
    return max(vals) - min(vals), vals


def matrix_coupling(M):
    """Coupling p(i,j) = M[i,j] from an N x N matrix of index-pair probabilities."""
    return lambda i, j: M[i, j]


def poset_marginal(p_of, s):
    """Full distribution over the 5 unlabelled posets on 3 elements, from
    i.i.d. pre-closure pair inclusion + transitive closure."""
    pairs = [(0, 1), (0, 2), (1, 2)]
    dist = {}
    for bits in itertools.product((0, 1), repeat=3):
        rel = np.zeros((3, 3), dtype=int)
        prob = 1.0
        for (i, j), b in zip(pairs, bits):
            pp = p_of(s[i], s[j])
            rel[i, j] = b
            prob *= pp if b else (1.0 - pp)
        for k in range(3):                                  # transitive closure
            for i in range(3):
                for j in range(3):
                    if rel[i, k] and rel[k, j]:
                        rel[i, j] = 1
        key = (int(rel.sum()),
               tuple(sorted(zip(rel.sum(0).tolist(), rel.sum(1).tolist()))))
        dist[key] = dist.get(key, 0.0) + prob
    return dist


def tv_distance(d1, d2):
    return 0.5 * sum(abs(d1.get(k, 0.0) - d2.get(k, 0.0)) for k in set(d1) | set(d2))


def covariance_constraint_count(N):
    """Covariance imposes p(i,j)=p(j,i): C(N,2) symmetry equations, leaving an
    N(N+1)/2-parameter family of admissible couplings (never empty)."""
    sym_equations = N * (N - 1) // 2
    free_params = N * (N + 1) // 2
    return sym_equations, free_params


def zn_inheritance_associative(N):
    """Child index = (sum of parent indices) mod N: commutative + associative, so
    its causet decoration is path-independent (covariant) for ANY N."""
    return all(((a + b) % N + c) % N == (a + (b + c) % N) % N
               for a in range(N) for b in range(N) for c in range(N))


def admissible_index_cardinalities(n_range):
    """The set of N for which a covariant NON-spectator coupling exists.  A
    symmetric, non-constant N x N coupling is covariant for every N >= 2, so this
    is all of n_range -- the dynamics does not pick a unique N."""
    rng = np.random.default_rng(20260609)
    admissible = []
    for N in n_range:
        M = rng.uniform(0.1, 0.6, size=(N, N))
        M = 0.5 * (M + M.T)                                 # symmetric, non-constant
        p_of = matrix_coupling(M)
        ok = all(covariance_spread(rel,
                                   tuple(int(rng.integers(0, N)) for _ in range(3)),
                                   p_of)[0] < COV_TOL
                 for rel in POSETS.values())
        if ok and not np.allclose(M, M.mean()):
            admissible.append(N)
    return admissible


def main():
    print("=" * 70)
    print("BIG-BETS Bet 2 crux: does growth SEE the internal CHO index?  (EXPLORATORY)")
    print("=" * 70)

    # ---- [A] the arena ----
    print("\n[A] Rideout-Sorkin sequential growth (transitive percolation).")
    exts = linear_extensions(V_POSET)
    print("    V poset (0<1, 0<2, {1,2} incomparable) has linear extensions:", exts)
    print("    Covariance (computable form): all linear extensions of a fixed")
    print("    decorated poset must have EQUAL growth probability.")

    # ---- [B] baseline: index-blind growth is a covariant measure on histories ----
    print("\n[B] Index-blind percolation is covariant -- counting gives a measure")
    print("    on histories (gold-standard criterion A, the thing CHO lacked):")
    blind = lambda i, j: P_DEFAULT
    for name, rel in POSETS.items():
        spread, vals = covariance_spread(rel, (0, 0, 0), blind)
        print("      %-9s covariant=%s  (%d extensions)" % (name, spread < COV_TOL, len(vals)))
    marg = poset_marginal(blind, (0, 0, 0))
    print("    poset marginal sums to %.12f over %d unlabelled posets" % (sum(marg.values()), len(marg)))

    # ---- [C] the crux: covariance constrains the COUPLING, not the cardinality ----
    print("\n[C] Attach an index s_i in {1..N} that COUPLES via p(s_i,s_j).  Ask the axioms:")
    asym = np.array([[0.2, 0.7], [0.1, 0.5]])
    sym = np.array([[0.2, 0.7], [0.7, 0.5]])
    s_diff = (0, 0, 1)                                       # different indices on {1,2}
    spread_a, va = covariance_spread(V_POSET, s_diff, matrix_coupling(asym))
    spread_s, vs = covariance_spread(V_POSET, s_diff, matrix_coupling(sym))
    print("    ASYMMETRIC coupling on the incomparable pair {1,2}:")
    print("      extensions give %s  spread=%.4f  => covariance BROKEN" % ([round(v, 4) for v in va], spread_a))
    print("    SYMMETRIC coupling, same indices:")
    print("      extensions give %s  spread=%.1e => covariance RESTORED" % ([round(v, 4) for v in vs], spread_s))
    print("    => discrete general covariance <=> the index coupling is SYMMETRIC.")

    # ---- [D] N-blindness: the constraint never touches the cardinality ----
    print("\n[D] What covariance says about N (the cardinality):")
    for N in N_RANGE:
        eq, free = covariance_constraint_count(N)
        print("      N=%d: %2d symmetry equations, %2d free coupling params (family never empty)"
              % (N, eq, free))
    admissible = admissible_index_cardinalities(N_RANGE)
    print("    covariant NON-spectator coupling exists for N in", admissible, "=> N=3 NOT singled out.")
    # spectator limit: index-blind marginal is literally N-independent
    rng = np.random.default_rng(7)
    d_ref = poset_marginal(blind, (0, 0, 0))
    max_tv = 0.0
    for N in (1, 2, 3, 4, 5):
        for _ in range(5):
            s = tuple(int(rng.integers(0, N)) for _ in range(3))
            max_tv = max(max_tv, tv_distance(poset_marginal(blind, s), d_ref))
    print("    SPECTATOR limit: index-blind causet marginal TV(N vs N=1) = %.1e for N=1..5" % max_tv)
    print("    Bell causality is automatic (growth prob is a product over pairs) -- also blind to N.")

    # ---- [E] CHO's best shot: a non-trivial inheritance map ----
    print("\n[E] CHO's best shot -- a non-trivial INHERITANCE (child index = product of parents):")
    for N in (2, 3, 4, 5, 6, 7):
        print("      Z/%d inheritance covariant (commutative+associative)? %s"
              % (N, zn_inheritance_associative(N)))
    print("    Covariant+commutative+associative inheritance exists for EVERY N (Z/N).")
    print("    The exceptional rank-3 Albert algebra J3(O) is singled out only by the")
    print("    NON-ASSOCIATIVE octonionic composition -- a kinematic (Hurwitz/Jordan)")
    print("    input, NOT something the order-theoretic growth provides.")

    # ---- [F] verdict ----
    print("\n[F] Verdict")
    print("    (+) growth supplies a covariant, Bell-causal MEASURE on histories (criterion A).")
    print("    (-) it is provably BLIND to the index cardinality: covariance constrains the")
    print("        coupling (symmetric), never N; N=3 stays a kinematic input (G1).")
    print("    Counting gives the FORM (a measure), not the CONTENT (N=3) -- the same boundary")
    print("    the Lambda and gravity probes drew.  Bet-2 crux resolved: NEGATIVE.")
    print("    EXPLORATORY: N=3 not derived from dynamics; NO Bayes credit moves.")

    # ---- stable tripwires (the covariance obstruction + N-blindness + humility) ----
    # The V poset has exactly the two birth orders that make covariance testable:
    assert linear_extensions(V_POSET) == [(0, 1, 2), (0, 2, 1)], "V poset extensions changed"
    # Index-blind growth is covariant on every poset (a genuine measure on histories):
    for rel in POSETS.values():
        assert covariance_spread(rel, (0, 0, 0), blind)[0] < COV_TOL, "blind growth not covariant"
    # The crux: asymmetric coupling BREAKS covariance, symmetric RESTORES it:
    assert spread_a > BREAK_MIN, "asymmetric coupling failed to break covariance"
    assert spread_s < COV_TOL, "symmetric coupling is not covariant"
    # N-blindness: a covariant non-spectator coupling exists for MORE THAN ONE N,
    # so the dynamics cannot be said to select N=3 (humility tripwire):
    assert len(admissible) >= SELECTED_MIN, "growth appears to select a unique N -- recheck"
    assert CHO_GENERATIONS in admissible and (CHO_GENERATIONS - 1) in admissible, \
        "N=3 is not distinguished from its neighbours -- it is not selected"
    # The covariance family is never empty for any tested N:
    for N in N_RANGE:
        eq, free = covariance_constraint_count(N)
        assert free > eq >= 0 and free == N * (N + 1) // 2, "coupling family miscount"
    # Spectator limit is exact:
    assert max_tv < COV_TOL, "index-blind marginal leaked the cardinality N"
    # Inheritance does not force 3 either: Z/N is covariant for a range including and
    # excluding 3, so 3 is not uniquely picked:
    assert all(zn_inheritance_associative(N) for N in (2, 3, 4, 5)), "Z/N inheritance broke"
    # The number we were asked to derive is the kinematic input, not a dynamical output:
    assert CHO_GENERATIONS == JORDAN_RANK == 3, "generation/rank input drifted"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
