"""Multi-factor carrier gate (Track 2): is the pi/432 carrier forced to TWO factors?

This probe attacks residual knob (1) that `uniqueness_gate.py` named but did NOT
remove.  That gate proved:

    among the DIVISORS of 432, only {16, 27} are irreducible-module dimensions,
    so (16, 27) is the UNIQUE *two*-irreducible-factor carrier of eps0^2 = pi/432.

But it flagged, honestly, that the result is conditional on a *two-factor ansatz*:
"why a tensor of exactly TWO irreducibles?"  If the carrier were allowed three or
more irreducible factors, is 16 * 27 still forced?  This gate answers that exactly.

The question
------------
Enumerate EVERY multiplicative decomposition

    432 = d_1 * d_2 * ... * d_k        (k >= 1, each d_i > 1)

in which every factor d_i is an irreducible-module dimension of the CHO
structure-group chain (the same IRREP_DIMS the uniqueness gate uses, imported here
so there is one source of truth).  Then ask whether k = 2 is forced.

What this gate establishes (exact integer arithmetic)
-----------------------------------------------------
  [A] The complete list: 432 has exactly FIVE irrep-dimension decompositions --
      one with k=2, two with k=3, two with k=4 (none with k=1 or k>=5).
  [B] So "exactly two factors" is NOT forced by irreducibility alone: there are
      genuine 3- and 4-factor carriers (e.g. 3*9*16 and 6*8*9). Knob (1) is REAL.
  [C] BUT the exceptional Jordan factor 27 = J3(O) is RIGIDLY two-factor: of all
      five decompositions, 27 appears in exactly ONE -- the carrier (16, 27).
      Every other decomposition either avoids 27 or shatters it into 3*3*3.
      (The spinor 16, by contrast, is flexible: it sits in three of the five.)
      Hence requiring J3(O) to enter AS the irreducible 27 forces two factors.
  [D] Why the dim-27 look-alike is not Schur-equivalent: 3 (x) 3 (x) 3 has the
      right dimension (27) but is REDUCIBLE as an SU(3) module,
          3 (x) 3 (x) 3 = 10 (+) 8 (+) 8 (+) 1   (Fulton-Harris),
      so Schur's lemma gives BLOCK weights (1/10, 1/8, 1/8, 1) on it, never the
      flat 1/27 that the irreducible 27 carries (Theorem B). The flat-1/27 weight
      -- the very thing that fixes the 1/432 of eps0^2 -- singles out the
      irreducible 27 over its tensor-cube look-alike.
  [E] Consequence: knob (1) is NOT independent. Requiring "the 27 is the
      E6-irreducible J3(O)" (knob 2) AUTOMATICALLY forces the two-factor carrier
      (knob 1). A supporting exact fact points the same way: the F4 alternative
      dimension 26 does not even divide 432 (432 / 26 is not an integer), so no
      multiplicative carrier of 432 can be built from the F4-irreducible 26 --
      only the E6 reading (27) can. The uniqueness gate's THREE named residual
      knobs therefore collapse to TWO independent structural choices.

Honest scope / what this does NOT do
------------------------------------
This sharpens the rigidity; it does not manufacture a positive.  It does NOT
derive that the carrier must contain J3(O) (that identification is Theorem B's
domain = knob 2), nor does it select the WZ level (knob 3), nor derive pi/432
from a CHO action.  So it moves NO Bayes credit and does NOT flip the scoreboard;
it only shows the residual freedom in the pi/432 denominator is smaller, and more
structurally concentrated, than the uniqueness gate left it: two knobs, not three,
and both are facts about how the 27 enters, not free integers.

KILL: if some inequivalent k>=3 carrier built from irreducible factors ALSO
contained the irreducible 27 (so 27 were not rigidly two-factor), knob (1) would
survive as independent and this collapse would be false.

Quarantined: imports only the irrep table from uniqueness_gate (same sandbox),
nothing from the core model, moves no Bayes credit. No scipy / no numpy. Pure
exact integer / Fraction arithmetic.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/multi_factor_carrier_gate.py
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction

from uniqueness_gate import IRREP_DIMS, TARGET


# Irreducible-module dimensions that DIVIDE 432 -- the only ones that can appear
# as a factor in a multiplicative decomposition of 432.
IRREP_DIVISORS: tuple[int, ...] = tuple(sorted(d for d in IRREP_DIMS if TARGET % d == 0))

CARRIER = (16, 27)                 # spinor Delta_9 (x) Jordan J3(O)
JORDAN_DIM = 27                    # E6-minuscule J3(O); irreducible => flat 1/27 (Theorem B)
SPINOR_DIM = 16                    # Spin(9) real spinor Delta_9 = OP^2 tangent
F4_FUNDAMENTAL = 26                # traceless Albert algebra; the F4 reading of the 27-space

# SU(3) Clebsch-Gordan for the fundamental cube (Fulton-Harris, "Representation
# Theory"): 3 (x) 3 = 6 (+) 3bar; then (6 (+) 3bar) (x) 3 = 10 (+) 8 (+) 8 (+) 1.
# The dim-27 tensor cube is REDUCIBLE; this is its irreducible content.
SU3_CUBE_BRANCHING = (10, 8, 8, 1)   # dims sum to 27, four irreducible blocks


def irrep_decompositions(n: int, factors: tuple[int, ...], min_factor: int = 2) -> list[tuple[int, ...]]:
    """All non-decreasing multisets drawn from `factors` (each > 1) with product n.

    Each multiset is generated exactly once (factors kept non-decreasing via
    `min_factor`). The length-1 decomposition (n,) is included iff n itself is an
    allowed factor.
    """
    out: list[tuple[int, ...]] = []
    for f in factors:
        if f < min_factor:
            continue
        if f == n:
            out.append((f,))
        elif n % f == 0 and f < n:
            for tail in irrep_decompositions(n // f, factors, f):
                out.append((f,) + tail)
    return out


def schur_weight(decomp: tuple[int, ...]) -> Fraction:
    """Flat Schur averaging weight of a tensor product of irreducibles = prod 1/d_i."""
    w = Fraction(1, 1)
    for d in decomp:
        w *= Fraction(1, d)
    return w


def main() -> bool:
    ok = True

    print("=" * 78)
    print("MULTI-FACTOR CARRIER GATE: is pi/432 forced to TWO irreducible factors?")
    print("=" * 78)
    print(f"  target 432 = {TARGET};  irreducible-module dims dividing it:")
    print(f"    {IRREP_DIVISORS}")
    print(f"    ({', '.join(f'{d}={IRREP_DIMS[d]}' for d in IRREP_DIVISORS)})")

    decomps = irrep_decompositions(TARGET, IRREP_DIVISORS, 2)
    by_k: dict[int, list[tuple[int, ...]]] = {}
    for d in decomps:
        by_k.setdefault(len(d), []).append(d)

    # ---- [A] the complete list -------------------------------------------
    print("\n[A] Every irrep-dimension decomposition of 432")
    for k in sorted(by_k):
        for d in sorted(by_k[k]):
            print(f"    k={k}: {' * '.join(map(str, d)):<16} weight = prod 1/d_i = {schur_weight(d)}")
    print(f"  total decompositions: {len(decomps)}  (by k: "
          f"{ {k: len(v) for k, v in sorted(by_k.items())} })")

    # ---- [B] two-factor is not forced by irreducibility alone ------------
    two_factor = sorted(by_k.get(2, []))
    multi_factor = [d for d in decomps if len(d) >= 3]
    print("\n[B] Is k=2 forced by 'every factor irreducible' alone?")
    print(f"  k=2 carriers .............. {two_factor}")
    print(f"  k>=3 carriers ............. {sorted(multi_factor)}")
    print(f"  => NO: {len(multi_factor)} carriers with 3+ irreducible factors exist,")
    print(f"     so 'exactly two factors' is a genuine ansatz (knob 1 is real).")

    # ---- [C] the 27 is rigidly two-factor --------------------------------
    contain_27 = sorted(d for d in decomps if JORDAN_DIM in d)
    contain_16 = sorted(d for d in decomps if SPINOR_DIM in d)
    print("\n[C] But the exceptional Jordan factor 27 = J3(O) is RIGIDLY two-factor")
    print(f"  decompositions containing the irreducible 27 : {contain_27}")
    print(f"  decompositions containing the spinor 16 ..... : {contain_16}")
    print(f"  => 27 occurs in exactly {len(contain_27)} decomposition (the carrier); "
          f"16 occurs in {len(contain_16)}.")
    print(f"  Requiring J3(O) to enter AS the irreducible 27 => the carrier is (16, 27).")

    # ---- [D] the dim-27 look-alike is reducible --------------------------
    cube_sum = sum(SU3_CUBE_BRANCHING)
    print("\n[D] Why 3*3*3 (same dim 27) is not a Schur-equivalent substitute")
    print(f"  3 (x) 3 (x) 3 = {' (+) '.join(map(str, SU3_CUBE_BRANCHING))}  "
          f"(dims sum to {cube_sum}); REDUCIBLE.")
    print(f"  irreducible 27 -> flat Schur weight 1/27 (Theorem B).")
    print(f"  reducible 3^(x)3 -> block weights {tuple(f'1/{b}' for b in SU3_CUBE_BRANCHING)}, "
          f"never a single 1/27.")
    print(f"  The flat 1/27 (which fixes the 1/432) singles out the irreducible 27.")

    # ---- [E] the knob collapse -------------------------------------------
    f4_divides = (TARGET % F4_FUNDAMENTAL == 0)
    print("\n[E] Consequence: knob (1) collapses into knob (2)")
    print(f"  'the 27 is the E6-irreducible J3(O)' (knob 2) ALREADY forces two factors (knob 1).")
    print(f"  Supporting exact fact: the F4 alternative dim 26 divides 432? {f4_divides} "
          f"(432/26 = {TARGET / F4_FUNDAMENTAL:.3f}).")
    print(f"  So no multiplicative carrier of 432 can use the F4-irreducible 26; only E6's 27.")
    print(f"  => the uniqueness gate's THREE residual knobs reduce to TWO independent ones:")
    print(f"     (2') the 27 enters as the E6-irreducible J3(O)  [now also forces the two-factor shape],")
    print(f"     (3)  the WZ flux sits at the primitive level one (wz_level_integrality_gate.py).")

    # ---- [V] verdict ------------------------------------------------------
    print("\n[V] Sandbox verdict")
    print("  two-factor forced by irreducibility alone : NO (5 carriers; k=2,3,4)")
    print("  two-factor forced GIVEN '27 irreducible'  : YES (27 is rigidly two-factor)")
    print("  net effect on the pi/432 residual freedom : 3 named knobs -> 2 (knob 1 in knob 2)")
    print("  pi/432 forced from CHO dynamics           : still OPEN (no dynamics derived here)")
    print("=" * 78)

    # --- tripwires (exact) -------------------------------------------------
    assert SPINOR_DIM * JORDAN_DIM == TARGET == 432
    assert set(IRREP_DIVISORS) == {3, 6, 8, 9, 16, 27, 36}
    # [A] exactly five decompositions, distributed 1/2/2 across k = 2/3/4
    assert len(decomps) == 5
    assert {k: len(v) for k, v in by_k.items()} == {2: 1, 3: 2, 4: 2}
    assert 1 not in by_k and not any(k >= 5 for k in by_k)
    # [B] k=2 unique carrier, but 3+ factor carriers also exist (knob 1 real)
    assert two_factor == [(16, 27)]
    assert (3, 9, 16) in decomps and (6, 8, 9) in decomps
    assert (3, 3, 3, 16) in decomps and (3, 3, 6, 8) in decomps
    assert len(multi_factor) == 4
    # [C] the irreducible 27 is rigidly two-factor; the 16 is not
    assert contain_27 == [(16, 27)]
    assert len(contain_16) == 3
    # every decomposition has the SAME flat weight 1/432 (dim identity), so the
    # weight cannot distinguish them -- only irreducibility of the FACTOR can:
    assert all(schur_weight(d) == Fraction(1, 432) for d in decomps)
    # [D] the dim-27 look-alike really is reducible into >1 block, none of dim 27
    assert cube_sum == JORDAN_DIM
    assert len(SU3_CUBE_BRANCHING) > 1 and JORDAN_DIM not in SU3_CUBE_BRANCHING
    # [E] the F4 reading cannot even multiplicatively reach 432
    assert TARGET % F4_FUNDAMENTAL != 0
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
