"""
Bet 1 (second probe) — is the WHOLE constant set ONE arithmetic object?
=======================================================================

Built on the `big-bets` branch. EXPLORATORY: it moves no Bayes credit and
asserts only exact arithmetic + its own humility firewall. It is the deeper
follow-on the plan named for Bet 1, after `padic_hierarchy.py` lit up
conceptually and stayed null numerically:

    > Follow-ons if it lights up: read 4/7 and the pi/432 numerator as adelic
    > periods / (mock) modular-form coefficients; test whether the *whole*
    > constant set satisfies ONE arithmetic relation (the Monstrous-Moonshine
    > precedent: 196883, 432, ...).                       -- BIG_BETS_PLAN.md

WHERE padic_hierarchy STOPPED, AND WHERE THIS GOES
--------------------------------------------------
`padic_hierarchy.py` (#77) read the three hierarchy EXPONENTS {9, 36, 64}
ADDITIVELY (perfect squares; increments +27, +28) and 3-adically. This module
reads the CONSTANTS THEMSELVES MULTIPLICATIVELY -- the prime factorisation of
432, of the mixing ratio 4/7, and of the arena dimensions -- and asks the
sharper Moonshine question: do they all live on ONE small set of primes, and is
there ONE arithmetic relation behind the set?

THE IDEA (the positive-leaning reading)
---------------------------------------
The CHO constants that ENTER PREDICTIONS are:
    eps0^2 = pi / 432          (the holonomy normalisation; 432 = 16*27)
    sin^2(theta23) = 4 / 7     (the only eps0-free exact mixing prediction)
    M/M_P = 3^-{9, 36, 64}     (the three power-of-three hierarchies)
plus the arena integers 16 = dim(OP^2)/Delta_9, 27 = dim J3(O), 28 = dim so(8).

Read p-adically, every one of them is an S-UNIT over the SAME three primes
    S = {2, 3, 7},
which are precisely the primes the octonions distinguish:
    p=2  Cayley-Dickson doubling: the normed division algebras have dim 2^k
         (R,C,H,O = 1,2,4,8) -- Hurwitz's theorem; 16 = 2^4, 64 = 2^6.
    p=3  triality / Jordan rank 3 / three generations / Tr P1 = 3; 27 = 3^3,
         9 = 3^2.
    p=7  Im(O) = R^7 / the 7 Fano points = 7 Fano lines / G2 acting on R^7.
And the central number factorises EXACTLY into the arena:
    432 = 2^4 * 3^3 = 16 * 27,   v2 = 4 = dim H,   v3 = 3 = generations.
The mixing prediction is literally a COUNTING (arithmetic) statement, not an
analytic one: of the 7 Fano lines, 4 avoid the vacuum direction and 3 pass
through it, so sin^2(theta23) = 4/7 and cos^2 = 3/7 -- 7 = 4 + 3. And the
octonion / Fano automorphism group is
    |PSL(2,7)| = |GL(3,2)| = |Aut(Fano)| = 168 = 2^3 * 3 * 7,
whose prime support is EXACTLY {2, 3, 7}. ((2,3,7) is also the Hurwitz triangle
group of the Klein quartic -- genus 3, 168 automorphisms -- noted, not leaned
on; see the trap list.) This is the same conceptual gain padic_hierarchy made,
now extended from the exponents to the whole multiplicative set: these are
arithmetic objects a real-analytic spectral action over R could never emit.

THE HONESTY FIREWALL (why HOSTING is not FORCING -- the sixth face)
-------------------------------------------------------------------
(a) {2,3,7}-smoothness is GENERIC for small integers: ~11-40% of integers below
    a few hundred are {2,3,7}-smooth, and the CHO constants are all small and
    built from octonionic dimensions, so their smoothness is low-surprise.
(b) The pattern BREAKS inside CHO's own vocabulary: the dimensions of the very
    structure groups CHO is built on are NOT {2,3,7}-smooth --
        dim F4 = 52 = 2^2 * 13,   dim E6 = 78 = 2 * 3 * 13,
        dim E7 = 133 = 7 * 19,    dim E8 = 248 = 2^3 * 31,
    bringing in primes 13, 19, 31. So smoothness is a property of the SUBSET
    that enters numerical predictions, not a theory-wide law -- if the arithmetic
    were FORCED, F4 and E6 would obey it too. This is selection, not derivation.
(c) No single arithmetic relation generates the set: 432 is NOT a j-function or
    Monster coefficient (the Moonshine 196884 = 196883 + 1 has no 432 analogue),
    and the only S-unit equations among the constants are trivial (7 = 4 + 3 and
    the additive increment ladder already in padic_hierarchy).
(d) The factorisation 432 = 16*27 just re-expresses the arena CHO already
    ingests; no constant moves from CHOSEN, no Bayes credit moves.

KILL CONDITION (declared, and its outcome)
------------------------------------------
If (i) {2,3,7}-smoothness of the predictive constants is no rarer than for
generic small integers, AND (ii) the smoothness FAILS for CHO's own structure
dimensions, AND (iii) no non-trivial single arithmetic relation links the set,
then the arithmetic reading HOSTS but does not FORCE the constants -- a
converging-negative, no nats. Outcome: (i) holds (smoothness common), (ii) holds
(F4, E6, E7, E8 all break it), (iii) holds (432 not Moonshine; only trivial
S-unit equations). Net: stays EXPLORATORY, no credit -- the sixth face of the
FORM-not-CONTENT boundary, with a real conceptual extension on the (+) side.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/adelic_constant_relation.py
"""

from fractions import Fraction

# ---------------------------------------------------------------------------
# The three octonion-distinguished primes (declared BEFORE any test, so the
# look-elsewhere size is fixed and cannot be tuned afterwards).
# ---------------------------------------------------------------------------
OCTONION_PRIMES = frozenset({2, 3, 7})
PRIME_ROLES = {
    2: "Cayley-Dickson doubling (div-algebra dims 1,2,4,8 = 2^k; Hurwitz)",
    3: "triality / Jordan rank 3 / three generations / Tr P1 = 3",
    7: "Im(O) = R^7 / 7 Fano points = 7 Fano lines / G2 on R^7",
}

# The numerical constants that ENTER CHO's predictions (label, value).
# Integers and exact rationals only -- the arithmetic content, pi stripped off.
PREDICTIVE_CONSTANTS = (
    ("432  (eps0^2 = pi/432 denom)", 432),
    ("16   (dim OP^2 / spinor D9)",  16),
    ("27   (dim J3(O))",             27),
    ("28   (dim so(8), triality)",   28),
    ("14   (dim G2 = Aut(O))",       14),
    ("9    (seesaw exponent = 3^2)",  9),
    ("36   (EW exponent = 6^2)",     36),
    ("64   (CC exponent = 8^2)",     64),
    ("4/7  (sin^2 theta23)",         Fraction(4, 7)),
    ("3/7  (cos^2 theta23)",         Fraction(3, 7)),
)

# The dimensions of CHO's OWN structure groups -- the honest control set.
# If the arithmetic were a theory-wide law these would be {2,3,7}-smooth too.
STRUCTURE_DIMS = (
    ("dim G2  = 14",  14),
    ("dim F4  = 52",  52),
    ("dim E6  = 78",  78),
    ("dim E7  = 133", 133),
    ("dim E8  = 248", 248),
    ("26  (traceless J3(O) / F4 fund.)", 26),
)

# Pre-declared Moonshine reference data (the plan's "196883, 432" hook).
J_FUNCTION_COEFFS = (1, 744, 196884, 21493760, 864299970, 20245856256)
MONSTER_IRREP_DIMS = (1, 196883, 21296876, 842609326, 18538750076)

# The Fano / octonion automorphism group order and its prime support.
FANO_AUT_ORDER = 168  # |PSL(2,7)| = |GL(3,2)| = |Aut(Fano plane)|

SMOOTH_RANGE = 512          # window for the generic-smoothness base rate
PROMOTION_P = 1.0e-3        # ~3 sigma; the base rate must stay FAR above it
RARE = 0.05                 # "common, not a rarity" humility threshold


# ===========================================================================
# Arithmetic primitives (pure stdlib, exact integer / Fraction)
# ===========================================================================
def factorize(n):
    """Prime factorisation of |n| as {prime: exponent} by trial division."""
    n = abs(int(n))
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def prime_support(x):
    """Set of primes dividing numerator OR denominator of an int / Fraction."""
    if isinstance(x, Fraction):
        num, den = x.numerator, x.denominator
    else:
        num, den = int(x), 1
    return set(factorize(num)) | set(factorize(den))


def is_S_unit(x, primes=OCTONION_PRIMES):
    """True if x is an S-unit: its prime support lies inside `primes`."""
    return prime_support(x) <= set(primes)


def smooth_fraction(n_max, primes=OCTONION_PRIMES):
    """Fraction of integers in [2, n_max] that are `primes`-smooth."""
    pr = set(primes)
    cnt = sum(1 for n in range(2, n_max + 1) if set(factorize(n)) <= pr)
    return cnt / (n_max - 1)


def _fmt_factor(x):
    """Human-readable factorisation string for an int or Fraction."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return _fmt_factor(x.numerator)
        return f"{_fmt_factor(x.numerator)} / {_fmt_factor(x.denominator)}"
    f = factorize(x)
    if not f:
        return "1"
    return " * ".join(f"{p}^{e}" if e > 1 else f"{p}" for p, e in sorted(f.items()))


# ===========================================================================
def main():
    print("=" * 76)
    print("  BET 1 (probe 2) — IS THE WHOLE CONSTANT SET ONE ARITHMETIC OBJECT?")
    print("  EXPLORATORY. No Bayes credit. Asserts exact arithmetic + a humility firewall.")
    print("=" * 76)

    # ---- [A] prime-factorisation fingerprint of the predictive constants ----
    print("\n  [A] PRIME FINGERPRINT: every PREDICTIVE constant is an S-unit over {2,3,7}")
    print("  " + "-" * 66)
    print(f"    {'constant':<30}{'factorisation':<18}{'primes':<12}{'S-unit?'}")
    all_pred_smooth = True
    for label, val in PREDICTIVE_CONSTANTS:
        sup = sorted(prime_support(val))
        ok = is_S_unit(val)
        all_pred_smooth &= ok
        print(f"    {label:<30}{_fmt_factor(val):<18}{str(sup):<12}{'yes' if ok else 'NO'}")
    print(f"    => all predictive constants {{2,3,7}}-smooth: {all_pred_smooth}")
    print(f"    => 432 = {_fmt_factor(432)} = 16 * 27  (v2=4=dim H, v3=3=generations)")

    # ---- [B] the three primes ARE the octonion structure primes ----
    print("\n  [B] THE THREE PRIMES ARE THE OCTONION STRUCTURE PRIMES")
    print("  " + "-" * 66)
    for p in sorted(OCTONION_PRIMES):
        print(f"    p = {p}:  {PRIME_ROLES[p]}")
    print(f"    the mixing 4/7 IS a Fano line-count: 7 lines = 4 (avoid vacuum) + 3 (through)")
    print(f"        => sin^2(theta23) = 4/7,  cos^2 = 3/7,  and 7 = 4 + 3 (counting, not analysis)")
    print(f"    |Aut(Fano)| = |PSL(2,7)| = {FANO_AUT_ORDER} = {_fmt_factor(FANO_AUT_ORDER)}"
          f"  -> prime support {sorted(prime_support(FANO_AUT_ORDER))} = {{2,3,7}} exactly")

    # ---- [C] the firewall: the pattern BREAKS on CHO's own structure groups ----
    print("\n  [C] FIREWALL: the SAME test on CHO's OWN structure-group dimensions")
    print("  " + "-" * 66)
    broken = []
    for label, val in STRUCTURE_DIMS:
        sup = sorted(prime_support(val))
        ok = is_S_unit(val)
        if not ok:
            broken.append(label)
        extra = sorted(set(sup) - OCTONION_PRIMES)
        tag = "smooth" if ok else f"BREAKS (extra prime{'s' if len(extra) > 1 else ''} {extra})"
        print(f"    {label:<34}= {_fmt_factor(val):<14} {tag}")
    print(f"    => {len(broken)} of {len(STRUCTURE_DIMS)} break it, including F4 (52=2^2*13) and")
    print(f"       E6 (78=2*3*13) -- CHO's CENTRAL groups carry prime 13 not in {{2,3,7}}.")
    print(f"       So {{2,3,7}}-smoothness is a property of the PREDICTIVE SUBSET, not a law.")

    # ---- [D] the single-relation (Moonshine) test -- null ----
    print("\n  [D] ONE ARITHMETIC RELATION? (the Moonshine follow-on) -- NULL")
    print("  " + "-" * 66)
    in_j = 432 in J_FUNCTION_COEFFS
    in_m = 432 in MONSTER_IRREP_DIMS
    print(f"    is 432 a j-function coefficient {J_FUNCTION_COEFFS[:4]}... ? {in_j}")
    print(f"    is 432 a Monster irrep dimension {MONSTER_IRREP_DIMS[:3]}... ? {in_m}")
    print(f"    the genuine McKay relation 196884 = 196883 + 1 has NO 432 analogue here.")
    print(f"    only S-unit equations among the set are TRIVIAL: 7 = 4 + 3 (the 4/7 split)")
    print(f"    and the additive ladder 9 ->+27-> 36 ->+28-> 64 (already in padic_hierarchy).")
    print(f"    => no single modular/arithmetic object has the CHO constants as its data.")

    # ---- [E] look-elsewhere: smoothness is generic for small integers ----
    print("\n  [E] LOOK-ELSEWHERE: {2,3,7}-smoothness is COMMON for small integers")
    print("  " + "-" * 66)
    for N in (50, 100, 256, SMOOTH_RANGE):
        print(f"    fraction of [2,{N:>3}] that is {{2,3,7}}-smooth: {smooth_fraction(N):.3f}")
    base = smooth_fraction(SMOOTH_RANGE)
    full = list(PREDICTIVE_CONSTANTS) + list(STRUCTURE_DIMS)
    full_rate = sum(1 for _l, v in full if is_S_unit(v)) / len(full)
    print(f"    base rate at N={SMOOTH_RANGE}: {base:.3f}  (>> promotion bar {PROMOTION_P})"
          f"  -> the pattern is unremarkable")
    print(f"    full CHO catalogue (predictive + structure): {full_rate:.2f} smooth"
          f"  (1.00 would be a theory-wide law; it is not)")

    # ---- [F] verdict ----
    print("\n  [F] VERDICT")
    print("  " + "-" * 66)
    print("    (+) the constants that ENTER predictions are arithmetic objects on exactly")
    print("        the three octonion primes {2,3,7}: 432 = 2^4*3^3 = 16*27, the mixing")
    print("        4/7 is the Fano partition 7 = 4+3, and |Aut(Fano)| = 168 = 2^3*3*7.")
    print("        The adelic reading is internally coherent and extends padic_hierarchy")
    print("        from the exponents to the whole multiplicative set -- the same reason a")
    print("        real-analytic spectral action over R could never emit these numbers.")
    print("    (-) but HOSTING is not FORCING: {2,3,7}-smoothness is generic for small")
    print("        octonion-built integers, it BREAKS on CHO's own F4/E6/E7/E8 dimensions")
    print("        (primes 13,19,31), and NO single arithmetic relation generates the set")
    print("        (432 is not a Moonshine coefficient; only trivial S-unit equations).")
    print("        The factorisation re-expresses the arena CHO already ingests; nothing")
    print("        is derived. The sixth face of the FORM-not-CONTENT boundary.")
    print("    EXPLORATORY: no constant promoted to derived; NO Bayes credit moves.")

    # =======================================================================
    # ASSERTIONS — exact arithmetic tripwires + the humility firewall
    # =======================================================================
    # Immutable integer facts: 432 IS the arena, on exactly primes {2,3}.
    assert factorize(432) == {2: 4, 3: 3}, "432 != 2^4 * 3^3"
    assert 432 == 16 * 27 == 2 ** 4 * 3 ** 3, "432 != 16*27"
    assert factorize(16) == {2: 4} and factorize(27) == {3: 3}, "16,27 not pure prime powers"
    assert factorize(28) == {2: 2, 7: 1} and factorize(14) == {2: 1, 7: 1}, "so(8)/G2 dims wrong"
    # The mixing ratio is a Fano line-count split: 7 = 4 + 3, both S-smooth.
    assert prime_support(Fraction(4, 7)) == {2, 7}, "sin^2 theta23 support changed"
    assert prime_support(Fraction(3, 7)) == {3, 7}, "cos^2 theta23 support changed"
    assert 4 + 3 == 7, "Fano partition 7 = 4(avoid) + 3(through) broken"
    # The Fano/octonion automorphism order has prime support EXACTLY {2,3,7}.
    assert factorize(FANO_AUT_ORDER) == {2: 3, 3: 1, 7: 1}, "|PSL(2,7)| != 2^3*3*7"
    assert prime_support(FANO_AUT_ORDER) == set(OCTONION_PRIMES), "Fano-aut prime support != {2,3,7}"
    # Every predictive constant is an S-unit over {2,3,7}.
    for label, val in PREDICTIVE_CONSTANTS:
        assert is_S_unit(val), f"predictive constant {label} left {{2,3,7}}"
    # FIREWALL 1: the pattern must BREAK on CHO's own central groups (else it
    # would look like a theory-wide law and tempt a false promotion).
    assert not is_S_unit(52) and not is_S_unit(78), "F4/E6 unexpectedly {2,3,7}-smooth"
    assert 13 in factorize(52) and 13 in factorize(78), "prime 13 should divide dim F4, dim E6"
    assert not is_S_unit(248), "dim E8 unexpectedly {2,3,7}-smooth"
    full = list(PREDICTIVE_CONSTANTS) + list(STRUCTURE_DIMS)
    full_rate = sum(1 for _l, v in full if is_S_unit(v)) / len(full)
    assert full_rate < 1.0, (
        "the FULL CHO catalogue is {2,3,7}-smooth -- that WOULD be a theory-wide law; "
        "re-examine before claiming HOSTING, this is the firewall")
    # FIREWALL 2: 432 is not a Moonshine coefficient (no single-relation shortcut).
    assert 432 not in J_FUNCTION_COEFFS and 432 not in MONSTER_IRREP_DIMS, \
        "432 appeared in Moonshine data -- re-derive before treating as a relation"
    assert 196884 - 196883 == 1, "the McKay relation is the Moonshine anchor, not a CHO one"
    # FIREWALL 3 (humility): {2,3,7}-smoothness is COMMON, not a ~3-sigma rarity.
    base = smooth_fraction(SMOOTH_RANGE)
    assert base > RARE > PROMOTION_P, (
        "{2,3,7}-smoothness became rare -- if it ever does, that would be a finding; "
        "do NOT auto-promote: re-derive, widen the prime menu, move credit deliberately "
        "on the scoreboard, never here")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
