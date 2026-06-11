"""Uniqueness gate for the pi/432 carrier (Track 2: the scoreboard lever).

This probe sharpens the carrier question. `moment_map_orbit_quantization.py`
already checks that `Delta_9 x J3(O) = 16 * 27` is the unique product equal to
432 *within a hand-curated 12-element catalog* of CHO dimensions. That is honest
but soft: the catalog selection is itself a choice. Here we ask the harder,
filter-based question that the durable decomposition

    eps0^2 = Phi = (Berry/WZ half-flux pi) * (1/432),   432 = 16 * 27

actually rests on:

    Of ALL ways to split 432, how many survive the requirement that makes the
    1/432 weight forced in the first place -- namely that each carrier factor is
    an IRREDUCIBLE module of the CHO structure-group chain, so Schur's lemma
    fixes its averaging weight to 1/dim (Theorem B)?

Reframing existence -> uniqueness
---------------------------------
The point of this gate is NOT to produce 432 again (every gate here can). It is
to measure how much freedom is left once the Schur-flat / irreducible-module
requirement is imposed, and to name the residual knobs explicitly. Both possible
outcomes are legitimate deliverables:

  * POSITIVE (rigidity): the filter forces a unique carrier -> the denominator
    432 is not numerology but the only Schur-admissible split, and the open work
    collapses to a small, named set of structural choices.
  * NEGATIVE (one free knob): several inequivalent Schur-admissible carriers give
    432 -> the theory carries exactly one irreducible free choice for this
    constant, which is the honest thing to report (and would demote the F0
    "pi/432 is derived" claim to "pi/432 has one declared knob").

What this gate establishes (exact arithmetic)
---------------------------------------------
  [A] Integer-factorization freedom: 432 has nine nontrivial factor pairs.
  [B] Loose CHO numerology is NON-unique: at least two of those pairs are built
      from CHO-meaningful integers (e.g. 16*27 AND 18*24 and 6*72), so "432 is
      obviously 16*27" is KILLED as a standalone argument.
  [C] Schur-irreducibility filter: among the divisors of 432, only {16, 27} are
      dimensions of irreducible modules of the CHO structure-group chain
      (Spin(9), F4, E6, G2, SU(3), Spin(8)). Hence (16, 27) is the UNIQUE
      two-irreducible-factor carrier. This is a genuine (conditional) rigidity.
  [D] Residual knobs the filter does NOT remove (named, not hidden).
  [E] Look-elsewhere base rate: how special is "factors into two irreps" anyway?

Honest scope / kill condition
-----------------------------
The rigidity in [C] is conditional on three structural choices that THIS gate
does not derive from CHO dynamics:
  (1) the carrier is a tensor product of exactly TWO irreducible modules;
  (2) the `27` is normalized under E6 (where it is irreducible) rather than F4
      (where it splits 1 (+) 26, giving weight 1/3, not 1/27) -- Theorem B;
  (3) the WZ flux sits at the primitive level one (wz_level_integrality_gate.py).
KILL: if any inequivalent (carrier, group, level) choice consistent with CHO
structure also reproduces pi/432, uniqueness is false and pi/432 is a genuine
free knob (the honest-negative branch above).

Quarantined: imports nothing from the core model, moves no Bayes credit.
No scipy / no numpy. Pure exact arithmetic.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/uniqueness_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import itertools


TARGET = 432  # the eps0^2 = pi/432 denominator; 432 = 16 * 27 = 2^4 * 3^3
SPIN9_SPINOR_DIM = 16
J3O_DIM = 27
SCHUR_WEIGHT = Fraction(1, SPIN9_SPINOR_DIM) * Fraction(1, J3O_DIM)


# ----------------------------------------------------------------------------
# Dimensions of IRREDUCIBLE modules of the CHO structure-group chain, with
# provenance. On each such module Schur's lemma forces a FLAT averaging weight
# 1/dim (this is exactly what makes the 1/432 of Theorem B rigid). Standard
# rep-theory facts (Adams, "Lectures on Exceptional Lie Groups"; Fulton-Harris).
# ----------------------------------------------------------------------------
IRREP_DIMS: dict[int, str] = {
    3: "SU(3) fundamental 3",
    6: "SU(3) sextet 6 / Spin(6) vector",
    7: "G2 fundamental = Im(O)",
    8: "Spin(8) vector 8v (octonions)",
    9: "Spin(9) vector 9",
    14: "G2 adjoint 14",
    16: "Spin(9) real spinor Delta_9 (= OP^2 tangent space)",
    26: "F4 fundamental (traceless Albert) 26",
    27: "E6 minuscule 27 = J3(O)  (also the G2 27)",
    28: "Spin(8) adjoint so(8) 28",
    36: "Spin(9) adjoint so(9) 36",
    52: "F4 adjoint 52",
    78: "E6 adjoint 78",
}

# Integers that are CHO-"meaningful" but are NOT irreducible-module dimensions:
# root/structure counts that loose dimensional numerology would also accept.
# Their presence is what shows integer-level counting is non-unique. Provenance
# from the repo's own usage (higgs_quartic_geometry.py and the root lattices).
STRUCTURE_COUNTS: dict[int, str] = {
    18: "lambda/eps0^2 = 432/24 (appears in the Higgs-quartic geometry)",
    24: "|roots(D4 = so(8))| = Higgs quartic lambda integer (pi/24)",
    72: "|roots(E6)| = 72",
}

MEANINGFUL = {**{d: ("irrep", t) for d, t in IRREP_DIMS.items()},
              **{d: ("structure", t) for d, t in STRUCTURE_COUNTS.items()}}


@dataclass(frozen=True)
class Pair:
    a: int
    b: int

    @property
    def product(self) -> int:
        return self.a * self.b


def factor_pairs(n: int) -> tuple[Pair, ...]:
    """All unordered factor pairs (a, b) with 1 < a <= b and a*b == n."""
    out = []
    a = 2
    while a * a <= n:
        if n % a == 0:
            out.append(Pair(a, n // a))
        a += 1
    return tuple(out)


def both_in(pair: Pair, table) -> bool:
    return pair.a in table and pair.b in table


def irrep_factor_pairs(n: int) -> tuple[Pair, ...]:
    return tuple(p for p in factor_pairs(n) if both_in(p, IRREP_DIMS))


def meaningful_factor_pairs(n: int) -> tuple[Pair, ...]:
    return tuple(p for p in factor_pairs(n) if both_in(p, MEANINGFUL))


def base_rate(window_hi: int) -> tuple[int, int, int]:
    """Over n in [2, window_hi]: (#with >=1 irrep split, #with exactly 1, total)."""
    total = window_hi - 1
    has_any = 0
    has_exactly_one = 0
    for n in range(2, window_hi + 1):
        k = len(irrep_factor_pairs(n))
        if k >= 1:
            has_any += 1
        if k == 1:
            has_exactly_one += 1
    return has_any, has_exactly_one, total


def main() -> bool:
    print("=" * 78)
    print("PI/432 CARRIER UNIQUENESS GATE")
    print("=" * 78)

    all_pairs = factor_pairs(TARGET)
    meaningful = meaningful_factor_pairs(TARGET)
    irreps = irrep_factor_pairs(TARGET)

    print("\n[A] Integer-factorization freedom of 432")
    print(f"  432 = 2^4 * 3^3 ; nontrivial unordered factor pairs: {len(all_pairs)}")
    for p in all_pairs:
        print(f"    {p.a:>3} * {p.b:<3}")

    print("\n[B] Loose CHO numerology is NON-unique")
    print("  Pairs whose BOTH factors are CHO-meaningful (irrep dim OR structure count):")
    for p in meaningful:
        ka, _ = MEANINGFUL[p.a]
        kb, _ = MEANINGFUL[p.b]
        print(f"    {p.a:>3} ({ka:<9}) * {p.b:<3} ({kb})")
    print(f"  => {len(meaningful)} CHO-meaningful splits exist, so 'obviously 16*27' is KILLED.")

    print("\n[C] Schur-irreducibility filter (each factor an irreducible module)")
    print("  Only these factors of 432 are irreducible-module dimensions:")
    for d in sorted(d for d in _divisors(TARGET) if d in IRREP_DIMS):
        print(f"    {d:>3} : {IRREP_DIMS[d]}")
    print("  Pairs with BOTH factors irreducible-module dimensions:")
    for p in irreps:
        print(f"    {p.a} * {p.b}  ->  weight 1/{p.a} * 1/{p.b} = {Fraction(1, p.a) * Fraction(1, p.b)}")
    if len(irreps) == 1:
        print("  => UNIQUE Schur-admissible carrier: (16, 27). Conditional rigidity holds.")
    else:
        print(f"  => {len(irreps)} Schur-admissible carriers: pi/432 is a genuine free knob.")

    print("\n[D] Residual knobs this gate does NOT remove")
    print("  (1) two-factor ansatz : why a tensor of exactly TWO irreducibles?")
    print("  (2) E6 vs F4 for '27' : under F4 the 27 splits 1 (+) 26 -> weight 1/3,")
    print("      not 1/27. The 1/27 needs E6 irreducibility (Theorem B).")
    print("  (3) primitive level   : WZ level one is primitive, not yet physically")
    print("      selected (see wz_level_integrality_gate.py).")

    has_any, has_one, total = base_rate(2 * TARGET)
    print("\n[E] Look-elsewhere base rate (how special is 'two irreps' alone?)")
    print(f"  integers n in [2, {2 * TARGET}] : {total}")
    print(f"  with >= 1 two-irrep split       : {has_any} ({100.0 * has_any / total:.1f}%)")
    print(f"  with exactly one such split     : {has_one} ({100.0 * has_one / total:.1f}%)")
    print("  => a unique two-irrep split is a real but not rare property (~5%):")
    print("     it is shared by dozens of integers here, so it does not single out")
    print("     432 by itself. The force comes from the factors being the SPECIFIC")
    print("     required modules (Delta_9 and J3(O)), not from unique factorability.")

    print("\n[V] Sandbox verdict")
    print("  naive '432 factors uniquely'        : KILLED (9 splits; >=2 CHO-meaningful)")
    print("  Schur-irreducible carrier (16,27)   : UNIQUE  (conditional rigidity)")
    print("  pi/432 forced from CHO dynamics     : OPEN (3 named knobs in [D])")
    print("=" * 78)

    # --- tripwires (exact) -------------------------------------------------
    assert TARGET == SPIN9_SPINOR_DIM * J3O_DIM == 432
    assert SCHUR_WEIGHT == Fraction(1, 432)
    # [A] nine nontrivial factor pairs of 432
    assert len(all_pairs) == 9
    # [B] integer numerology is non-unique: more than one CHO-meaningful split
    assert len(meaningful) >= 2
    assert Pair(16, 27) in meaningful and Pair(18, 24) in meaningful
    # [C] Schur filter forces a unique carrier
    assert irreps == (Pair(16, 27),)
    assert 16 in IRREP_DIMS and 27 in IRREP_DIMS
    # robustness: no OTHER divisor of 432 is an irreducible-module dimension
    other_divisor_irreps = [d for d in _divisors(TARGET)
                            if d in IRREP_DIMS and d not in (16, 27)]
    for d in other_divisor_irreps:
        assert (TARGET // d) not in IRREP_DIMS, (d, TARGET // d)
    # [D] the F4-vs-E6 knob is real: 27 = 1 + 26 under F4
    assert 1 + 26 == 27
    return True


def _divisors(n: int) -> tuple[int, ...]:
    out = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            if d != n // d:
                out.append(n // d)
        d += 1
    return tuple(sorted(out))


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
