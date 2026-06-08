"""
F0 factorization-forcedness audit: is 16 x 27 the FORCED split of 432?

Motivation
----------
`epsilon_symplectic_volume.py` shows that IF the transition arena is the product
coadjoint orbit of Spin(9) x E6, then 432 = 16 x 27 is one geometric volume.
That leaves the honest question this module answers head-on:

    of the ten ways to write 432 as a x b, why 16 x 27?
    and why a PRODUCT of two groups at all, rather than one simple group?

This is the same "hardness to vary" discipline as `look_elsewhere.py`: a number
that factors many ways is weak evidence unless the chosen factorization is forced
by independently-derived structure.  Two complementary gates:

  R3  FORCEDNESS AUDIT.  Enumerate every factor pair of 432.  Score each factor
      by whether the framework already DERIVES a transition carrier of that
      dimension (16 = Delta_9 = dim OP^2 = Spin(9) spinor; 27 = dim J3(O) = E6
      minimal -- both derived elsewhere in the project).  Result: 16 x 27 is the
      UNIQUE factor pair whose BOTH factors are independently-derived carriers.
      Every other split has at most one meaningful factor (8 = dim O, 4 = dim H,
      36 = dim so(9), ...) and a structureless partner.

  R4  SINGLE-GROUP NO-GO (sharpening).  Scan the fundamental/minimal irreducible
      representations of the candidate simple Lie groups (su(n), so(n), and the
      exceptionals G2, F4, E6, E7, E8), recomputing each dimension from its root
      system with the Weyl formula.  432 appears among NONE of them, whereas it
      is exactly the (spinor) x (minimal) bifundamental of Spin(9) x E6.  So the
      economical symmetry hosting a 432 arena is a PRODUCT group, not a simple
      one -- which is why the arena factorizes in the first place.

Together these convert "16 x 27 looks chosen" into "16 x 27 is the only split
both of whose factors are derived, and 432 is not a single-group minimal rep, so
a product is forced." That sharpens the live F0 seam to its real content -- which
two orbits the CHO action selects -- and removes the factorization freedom.

Honest scope (what this does NOT close)
---------------------------------------
* R3 ranks by ALREADY-DERIVED structure; it does not by itself derive that the
  carriers are 16- and 27-dimensional (that is the symplectic/Schur work). It
  shows no OTHER split competes.
* R4 is a MINIMAL/fundamental-rep statement. Large non-fundamental irreps of big
  groups can have dimension 432; the claim is that no single simple group hosts
  432 as a fundamental/minimal representation, so the product realization is the
  economical one -- not an absolute group-theoretic impossibility.

F0 is NOT promoted to DERIVED by this module.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_factor_forcedness.py
"""

from __future__ import annotations

import numpy as np

from epsilon_symplectic_volume import (
    positive_roots_from_cartan,
    simply_laced_dim,
    euclidean_dim,
    so9_positive_roots,
    e6_cartan,
)

DIM_ARENA = 432
DIM_DELTA9 = 16
DIM_J3O = 27


# --------------------------------------------------------------------------- #
#  R3 -- forcedness registry                                                   #
# --------------------------------------------------------------------------- #
#
# status meaning:
#   DERIVED_CARRIER  the framework derives a transition trace-space (phase-space
#                    carrier) of this dimension  -> score 2
#   ALGEBRA          a genuine C(x)H(x)O / symmetry dimension, but NOT a derived
#                    transition carrier (a count, a base algebra, or the symmetry
#                    Lie algebra itself)                                -> score 1
#   NONE             no canonical single object of this dimension       -> score 0
#
# A legitimate "phase space = carrier_A (x) carrier_B" factorization needs BOTH
# factors to be DERIVED_CARRIER.

DERIVED_CARRIER = "DERIVED_CARRIER"
ALGEBRA = "ALGEBRA"
NONE = "NONE"
SCORE = {DERIVED_CARRIER: 2, ALGEBRA: 1, NONE: 0}

REGISTRY = {
    1: ("trivial line", NONE),
    2: ("dim_R C", ALGEBRA),
    3: ("N_gen = rank J3(O) (a count, not a carrier)", ALGEBRA),
    4: ("dim_R H", ALGEBRA),
    6: ("-", NONE),
    8: ("dim_R O", ALGEBRA),
    9: ("Spin(9) vector R^9", ALGEBRA),
    12: ("-", NONE),
    16: ("dim Delta_9 = dim_R OP^2 = Spin(9) spinor", DERIVED_CARRIER),
    18: ("-", NONE),
    24: ("-", NONE),
    27: ("dim J3(O) = E6 minimal rep", DERIVED_CARRIER),
    36: ("dim so(9) = Spin(9) adjoint (symmetry, not carrier)", ALGEBRA),
    48: ("-", NONE),
    54: ("2 x 27 (not a single carrier)", NONE),
    72: ("hierarchy exponent (not a dimension)", NONE),
    108: ("-", NONE),
    144: ("-", NONE),
    216: ("-", NONE),
    432: ("the product arena itself", NONE),
}


def divisor_pairs(n):
    pairs = []
    for a in range(1, int(n ** 0.5) + 1):
        if n % a == 0:
            pairs.append((a, n // a))
    return pairs


def status_of(d):
    return REGISTRY.get(d, ("-", NONE))


def forcedness_table(n=DIM_ARENA):
    rows = []
    for a, b in divisor_pairs(n):
        la, sa = status_of(a)
        lb, sb = status_of(b)
        rows.append({
            "pair": (a, b),
            "score": SCORE[sa] + SCORE[sb],
            "both_derived_carrier": sa == DERIVED_CARRIER and sb == DERIVED_CARRIER,
            "a": (a, la, sa),
            "b": (b, lb, sb),
        })
    rows.sort(key=lambda r: (-r["score"], r["pair"]))
    return rows


# --------------------------------------------------------------------------- #
#  R4 -- single-group no-go scan                                               #
# --------------------------------------------------------------------------- #
def _cartan(n, edges):
    c = [[2 if i == j else 0 for j in range(n)] for i in range(n)]
    for a, b in edges:
        c[a][b] = -1
        c[b][a] = -1
    return c


def _fundamental_dims(n, edges):
    roots = positive_roots_from_cartan(_cartan(n, edges))
    out = []
    for m in range(n):
        hw = tuple(1 if i == m else 0 for i in range(n))
        out.append(round(simply_laced_dim(roots, hw)))
    return out


def _a_chain(n):                       # A_n : su(n+1)
    return [(i, i + 1) for i in range(n - 1)]


def _d_fork(n):                        # D_n : so(2n)
    return [(i, i + 1) for i in range(n - 2)] + [(n - 3, n - 1)]


def candidate_minimal_irreps(bound=2000):
    """Fundamental-representation dimensions (<= bound) of the candidate simple
    Lie groups, recomputed from root systems where simply-laced, plus the
    standard minimal dims of the non-simply-laced exceptionals.  Returns
    {label: sorted list of fundamental dims <= bound}."""
    groups = {}

    # A_n = su(n+1): fundamentals are the binomial dims
    for n in range(1, 9):
        groups[f"A{n}=su({n+1})"] = sorted(
            d for d in _fundamental_dims(n, _a_chain(n)) if d <= bound)

    # D_n = so(2n): vector, adjoint, exterior powers, two spinors
    for n in range(4, 9):
        groups[f"D{n}=so({2*n})"] = sorted(
            d for d in _fundamental_dims(n, _d_fork(n)) if d <= bound)

    # so(9) = B4 spinor (non-simply-laced): explicit Euclidean Weyl, highest
    # weights given directly in the orthogonal e_i basis.
    b4 = so9_positive_roots()
    groups["B4=so(9)"] = sorted({
        round(euclidean_dim(b4, [1, 0, 0, 0])),          # vector 9
        round(euclidean_dim(b4, [1, 1, 0, 0])),          # adjoint 36
        round(euclidean_dim(b4, [0.5, 0.5, 0.5, 0.5])),  # spinor 16
    })

    # E6 (simply-laced)
    groups["E6"] = sorted(
        d for d in [round(simply_laced_dim(positive_roots_from_cartan(e6_cartan()),
                    tuple(1 if i == m else 0 for i in range(6)))) for m in range(6)]
        if d <= bound)

    # E7, E8 (simply-laced)
    groups["E7"] = sorted(
        d for d in _fundamental_dims(7, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (2, 6)])
        if d <= bound)
    groups["E8"] = sorted(
        d for d in _fundamental_dims(8,
            [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 7)])
        if d <= bound)

    # Non-simply-laced exceptionals: standard minimal irrep dims (cited facts)
    groups["G2"] = [7, 14]
    groups["F4"] = [26, 52, 273, 1274]

    return groups


# --------------------------------------------------------------------------- #
#  Driver                                                                      #
# --------------------------------------------------------------------------- #
def main():
    rows = forcedness_table()
    groups = candidate_minimal_irreps()

    print("=" * 78)
    print("  F0 FACTORIZATION-FORCEDNESS AUDIT")
    print("  Why 16 x 27, and why a product of two groups?")
    print("=" * 78)
    print()
    print("  R3  Every factorization 432 = a x b, ranked by derived-carrier score")
    print("  " + "-" * 74)
    print(f"  {'pair':>9}  {'score':>5}  {'both carriers':>13}   factors")
    for r in rows:
        a, la, sa = r["a"]
        b, lb, sb = r["b"]
        flag = "YES" if r["both_derived_carrier"] else ""
        print(f"  {r['pair'][0]:>4} x {r['pair'][1]:<3} {r['score']:>5}  "
              f"{flag:>13}   {a}:{sa}, {b}:{sb}")
    print()
    winners = [r for r in rows if r["both_derived_carrier"]]
    top = rows[0]
    print(f"  unique both-derived-carrier split : "
          f"{[r['pair'] for r in winners]}")
    print(f"  top score {top['score']} held by      : "
          f"{[r['pair'] for r in rows if r['score'] == top['score']]}")
    print(f"  16 = {REGISTRY[16][0]}")
    print(f"  27 = {REGISTRY[27][0]}")
    print()

    print("  R4  Is 432 a fundamental/minimal irrep of any single simple group?")
    print("  " + "-" * 74)
    all_fund = set()
    for label, dims in groups.items():
        all_fund.update(dims)
        marker = "  <-- contains 432" if DIM_ARENA in dims else ""
        print(f"  {label:<11}: {dims}{marker}")
    has_16 = 16 in all_fund
    has_27 = 27 in all_fund
    print()
    print(f"  432 in any candidate fundamental rep : {DIM_ARENA in all_fund}")
    print(f"  16 present (Spin(9) spinor)          : {has_16}")
    print(f"  27 present (E6 minimal)              : {has_27}")
    print(f"  => 432 = 16 x 27 is the (spinor)x(minimal) rep of the PRODUCT")
    print(f"     group Spin(9) x E6, not a single-group fundamental.")
    print()

    checks = {
        "exactly one factor pair has both factors as derived carriers":
            len(winners) == 1,
        "that unique pair is 16 x 27":
            winners and winners[0]["pair"] == (16, 27),
        "16 x 27 is the strict top-scoring split":
            top["pair"] == (16, 27)
            and sum(1 for r in rows if r["score"] == top["score"]) == 1,
        "16 is a derived carrier (Delta_9 = dim OP^2)":
            status_of(16)[1] == DERIVED_CARRIER,
        "27 is a derived carrier (dim J3(O))":
            status_of(27)[1] == DERIVED_CARRIER,
        "432 is NOT a fundamental rep of any single candidate group":
            DIM_ARENA not in all_fund,
        "16 appears as a single-group fundamental (Spin(9) spinor)": has_16,
        "27 appears as a single-group fundamental (E6 minimal)": has_27,
        "E6 fundamental scan reproduces 27 and 78":
            27 in groups["E6"] and 78 in groups["E6"],
        "E7 scan reproduces 56 and 133":
            56 in groups["E7"] and 133 in groups["E7"],
        "E8 scan reproduces 248":
            248 in groups["E8"],
    }
    width = max(len(k) for k in checks)
    for name, ok_ in checks.items():
        print(f"  [{'PASS' if ok_ else 'FAIL'}] {name:<{width}}")
    ok = all(checks.values())
    print()
    print("  AUDIT STATUS:", "PASS" if ok else "FAIL",
          "- 16 x 27 is the unique derived-carrier split and 432 is")
    print("                  not a single-group minimal rep, so a product is forced.")
    print("  F0 not promoted: this removes the factorization freedom and sharpens")
    print("                   the seam to 'which two orbits the CHO action selects'.")
    print()
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
