"""
Distler-Garibaldi-style no-go stress test of N_gen = 3  (roadmap T3.2).
=======================================================================

`three_generations.py` argues N_gen = 3 from three legs. Leg 2 -- "SO(8)
triality gives three inequivalent 8-dim reps, hence three generations" -- is the
physically load-bearing one, and it is exactly the kind of algebraic
generation-counting that Distler & Garibaldi (2009) demolished for Lisi's E8.
Their no-go did not dispute that E8 contains SM-looking reps; it proved the
*chirality/embedding* step fails (the construction forces mirror, vector-like
partners rather than three chiral generations).

This module tries to break CHO's Leg 2 the same way. It separates what is
genuinely PROVEN (rep counting) from the physical BRIDGE (the identification of
those reps with three chiral fermion generations), and reports honestly whether
the bridge survives.

What is proven (and verified here)
----------------------------------
  * The D4 Dynkin diagram automorphism group is S3 (order 6), permuting the
    three OUTER nodes and fixing the central node -> exactly three inequivalent
    8-dim irreps of SO(8): the vector 8v and the two spinors 8s, 8c.

What is an unproven bridge (the no-go target)
---------------------------------------------
  * Of the three triality reps, ONE is a vector (8v) and TWO are spinors
    (8s, 8c). Identifying all three as three fermion generations of the SAME
    character requires triality to map vector <-> spinor, which is not a Lorentz
    or gauge symmetry of any field theory.
  * The two spinors 8s and 8c are OPPOSITE-CHIRALITY Weyl spinors (swapped by the
    Z2 in S3). Reading them as two generations therefore pairs a generation with
    a MIRROR (vector-like) generation -- the precise E8 failure mode.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/three_generations_nogo_audit.py
"""

from __future__ import annotations

from itertools import permutations


# --------------------------------------------------------------------------
# D4 Dynkin diagram and its triality automorphism group
# --------------------------------------------------------------------------
# D4 nodes: 1, 2, 3, 4 with node 2 central, connected to the three outer nodes
# 1, 3, 4. The three 8-dim reps sit on the three outer nodes:
#   node 1 -> 8v (vector), node 3 -> 8s (spinor), node 4 -> 8c (co-spinor).
# Edges (undirected):
D4_EDGES = frozenset({frozenset({2, 1}), frozenset({2, 3}), frozenset({2, 4})})
D4_NODES = (1, 2, 3, 4)
OUTER_NODES = (1, 3, 4)
CENTRAL_NODE = 2

# Rep carried by each outer node, with spin character.
REP_OF_NODE = {
    1: ("8v", "vector"),
    3: ("8s", "spinor"),
    4: ("8c", "spinor"),
}


def graph_automorphisms(nodes, edges):
    """All node permutations preserving the edge set."""
    autos = []
    for perm in permutations(nodes):
        mapping = dict(zip(nodes, perm))
        mapped = frozenset(frozenset(mapping[n] for n in e) for e in edges)
        if mapped == edges:
            autos.append(mapping)
    return autos


def verify_triality():
    autos = graph_automorphisms(D4_NODES, D4_EDGES)
    order = len(autos)
    # The central node must be fixed by every automorphism (unique degree-3 node).
    central_fixed = all(a[CENTRAL_NODE] == CENTRAL_NODE for a in autos)
    # Outer nodes are permuted; collect the induced permutations of {1,3,4}.
    outer_perms = {tuple(a[n] for n in OUTER_NODES) for a in autos}
    is_s3 = (order == 6) and central_fixed and (len(outer_perms) == 6)
    return autos, order, central_fixed, is_s3


# --------------------------------------------------------------------------
# The chirality / vector-vs-spinor obstruction
# --------------------------------------------------------------------------


def classify_reps():
    """Return the spin character of the three triality reps."""
    return {REP_OF_NODE[n][0]: REP_OF_NODE[n][1] for n in OUTER_NODES}


def chirality_conjugate_pair(autos):
    """Identify the Z2 in S3 that swaps the two spinors (chirality flip).

    The element that fixes 8v (node 1) and swaps 8s<->8c (nodes 3,4) is the
    parity/chirality conjugation. Its existence shows 8s and 8c are an
    opposite-chirality (mirror) pair, not two independent same-chirality gens.
    """
    for a in autos:
        if a[1] == 1 and a[3] == 4 and a[4] == 3:
            return True
    return False


def main():
    print("=" * 78)
    print("  NO-GO STRESS TEST OF N_gen = 3  (Distler-Garibaldi-style, T3.2)")
    print("=" * 78)

    autos, order, central_fixed, is_s3 = verify_triality()

    print("\n  PART A -- what is genuinely PROVEN (rep counting)")
    print("  " + "-" * 60)
    print(f"  D4 Dynkin automorphism group order      = {order}  (expect 6 = |S3|)")
    print(f"  central node fixed by all automorphisms = {central_fixed}")
    print(f"  three outer nodes fully permuted (S3)   = {len(autos) == 6}")
    print(f"  => exactly three inequivalent 8-dim SO(8) reps: 8v, 8s, 8c")
    leg2_counting = is_s3
    print(f"  [{'PASS' if leg2_counting else 'FAIL'}] triality rep-counting leg is SOUND")

    print("\n  PART B -- the physical BRIDGE the no-go attacks")
    print("  " + "-" * 60)
    spin = classify_reps()
    for rep in ("8v", "8s", "8c"):
        print(f"    {rep}: {spin[rep]}")
    n_vectors = sum(1 for v in spin.values() if v == "vector")
    n_spinors = sum(1 for v in spin.values() if v == "spinor")
    print(f"    -> {n_vectors} vector + {n_spinors} spinors among the 3 triality reps")

    mixes_spin = n_vectors >= 1 and n_spinors >= 1
    print()
    print("  Obstruction 1 (vector vs spinor):")
    print("    Identifying all three reps as fermion generations of the same")
    print("    character requires triality to map vector <-> spinor. That is")
    print("    NOT a Lorentz or gauge symmetry of any field theory.")
    print(f"    triality mixes vector and spinor reps = {mixes_spin}")

    chiral_pair = chirality_conjugate_pair(autos)
    print()
    print("  Obstruction 2 (chirality / mirror partners):")
    print("    The Z2 in S3 fixing 8v and swapping 8s<->8c is the chirality")
    print("    conjugation: 8s and 8c are OPPOSITE-chirality Weyl spinors.")
    print("    Reading them as two generations pairs a generation with a MIRROR")
    print("    (vector-like) generation -- the exact E8 failure mode.")
    print(f"    chirality-conjugation element exists   = {chiral_pair}")

    print("\n  VERDICT")
    print("  " + "-" * 60)
    bridge_broken = mixes_spin and chiral_pair
    if leg2_counting and bridge_broken:
        print("  [PROVEN ] three inequivalent 8-dim reps exist (rep counting).")
        print("  [OPEN   ] the identification '3 reps = 3 chiral generations' does")
        print("           NOT survive first-principles scrutiny: triality mixes a")
        print("           vector with two opposite-chirality spinors. Without a")
        print("           derivation of bridge A3 that (a) selects only fermionic")
        print("           reps and (b) avoids the mirror pairing, G1/G2 are at")
        print("           CONJECTURE level on this axis, not THEOREM.")
        print()
        print("  Honest consequence for the ledger:")
        print("   * keep N_gen = 3 as 'theorem conditional on A2-A3', and flag in")
        print("     DERIVATION_LEDGER G1/G2 that the triality->generation bridge")
        print("     faces the vector-vs-spinor and chirality obstructions above;")
        print("   * this does NOT falsify CHO -- it precisely locates the single")
        print("     most important proof obligation (A3) and shows the headline")
        print("     'theorem' is conditional, exactly as honesty requires.")
    else:
        print("  The no-go test did not reproduce the expected obstruction; review")
        print("  the rep assignments before claiming Leg 2 is either safe or broken.")
    print()
    print("  NOTE: this is the SAME class of argument that broke Lisi's E8")
    print("  (Distler-Garibaldi 2009). Surviving it would make N_gen = 3 CHO's")
    print("  strongest rigorous result; as it stands, the bridge is open.")
    print()


if __name__ == "__main__":
    main()
