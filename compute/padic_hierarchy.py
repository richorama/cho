"""
Bet 1 — the hierarchy exponents are ARITHMETIC (3-adic), not analytic.
======================================================================

This is the first experiment of BIG_BETS_PLAN.md, built on the `big-bets`
branch. It is EXPLORATORY: it moves no Bayes credit and asserts only exact
arithmetic + its own humility threshold. Its job is to test one sharp idea and
report honestly — most likely a converging-negative, possibly something sharper.

THE IDEA
--------
The CHO program's single biggest unclaimed chunk of description length is the
three mass-hierarchy exponents, each written in the repo as a power of 3:

    M_R (seesaw)        = M_P / 3^9        (dark_sector.py)
    M_W (electroweak)   = M_P / 3^36       (summary_table.py)
    Lambda^1/4 (cosmo)  = (11/12) M_P /(sqrt2 * 3^64)   (cc_prediction.py)

model_complexity.py charges all three as CHOSEN (~15 nats) because the repo's
labels for the exponents are HETEROGENEOUS and post-hoc (36 = |roots+(E6)|,
64 = dim_R(A), 9 = "seesaw"). That heterogeneity is why they were never forced.

This module asks whether a *homogeneous* arithmetic reading is hiding in them.

WHAT IS ACTUALLY TRUE (exact integer facts, asserted below)
-----------------------------------------------------------
  * All three exponents are PERFECT SQUARES:  9 = 3^2,  36 = 6^2,  64 = 8^2.
  * Their consecutive differences are two CONSECUTIVE arena dimensions:
        36 - 9  = 27 = dim J3(O)         (the exceptional Jordan algebra)
        64 - 36 = 28 = dim so(8)         (the triality algebra)
    cc_prediction.py ALREADY notes "64 - 36 = 28 = dim(so(8))"; the new content
    is that 36 - 9 = 27 = dim J3(O) closes the OTHER rung, giving a clean ladder
        9  --(+27 = dim J3(O))-->  36  --(+28 = dim so(8))-->  64.
  * 3-adically the electroweak hierarchy is NOT fine-tuned: |M_W/M_P|_3 = 3^-36
    is an ordinary 3-adic number. The "hierarchy problem" (M_W << M_P by ~10^17)
    is an artefact of the archimedean absolute value |.|_inf. Over Q_3 it is
    unit-scale. Base 3 is independently distinguished in CHO (triality, three
    generations, J3, Tr P1 = 3), so Q_3 is the natural completion to read these in.

WHAT IS NOT CLAIMED (the honesty firewall)
------------------------------------------
The arena-dimension identifications {9, +27, +28} are post-hoc labels, exactly
like the repo's existing ones. This module does NOT promote the exponents from
CHOSEN. It runs a look-elsewhere Monte-Carlo null and reports a discounted
significance that, on the generous side, does NOT cross the promotion bar. The
verdict is EXPLORATORY. The solid, citable gain is the CONCEPTUAL reframing
(hierarchy = archimedean artefact; Q_3 is natural), not the numerology.

KILL CONDITION
--------------
If (i) base-3 gives no cleaner near-integer exponents for the data-anchored
scales than other small bases, AND (ii) the {perfect-square + increments-in-
catalogue} conjunction is not significant against the look-elsewhere null, then
the exponents are genuinely free and we log a converging-negative. (Outcome:
test (i) PASSES for EW only, FAILS for CC; test (ii) is suggestive but below the
bar. Net: stays EXPLORATORY, no credit — recorded as such.)

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/padic_hierarchy.py
"""

import numpy as np

from cc_prediction import M_P  # source-of-truth Planck scale (GeV), = 1.2209e19

# ---------------------------------------------------------------------------
# Data anchors (only two of the three scales are directly observed).
# ---------------------------------------------------------------------------
M_W_OBS = 80.377                 # GeV, PDG W-boson mass (electroweak anchor)
LAMBDA_QUARTER_OBS = 2.24e-12    # GeV, = 2.24e-3 eV, Planck-2018 Lambda^(1/4)
# The seesaw scale M_R is theory-internal (no direct measurement); its exponent
# 9 is taken from dark_sector.py as the stated integer, tested but not anchored.

# ---------------------------------------------------------------------------
# The three stated hierarchy exponents (source-of-truth integers).
# ---------------------------------------------------------------------------
# Ordered by descending energy scale (ascending exponent = descending mass).
EXPONENTS = (
    ("M_R (seesaw)",          9,  False),   # (label, exponent, data_anchored?)
    ("M_W (electroweak)",     36, True),
    ("Lambda^1/4 (cosmo)",    64, True),
)

P = 3  # the distinguished prime: triality / three generations / J3 / Tr P1 = 3

# Pre-declared CHO structural-dimension catalogue, fixed BEFORE the increment
# test so the look-elsewhere size is explicit and cannot be tuned afterwards.
# These are dimensions that recur throughout the repo's vocabulary.
CHO_DIMS = (2, 3, 4, 7, 8, 14, 16, 21, 24, 26, 27, 28, 36, 52, 78)
DIM_NAMES = {
    27: "dim J3(O)",
    28: "dim so(8) (triality algebra)",
    16: "chiral spinor Delta_9",
    26: "traceless J3(O)",
    52: "dim F4",
    78: "dim E6",
    14: "dim G2",
}

# Promotion bar: a look-elsewhere-corrected p below this would be "interesting".
# (~3 sigma.) The module asserts the discounted p stays ABOVE it (humility).
PROMOTION_P = 1.0e-3


# ===========================================================================
# 1. Exact arithmetic: perfect squares + the increment ladder
# ===========================================================================
def perfect_square_audit():
    """Each exponent as k^2 (exact integer test)."""
    out = []
    for label, e, anchored in EXPONENTS:
        r = int(round(e ** 0.5))
        out.append((label, e, r, r * r == e, anchored))
    return out


def increment_ladder():
    """Consecutive differences of the exponents and whether each is a CHO dim."""
    es = [e for _l, e, _a in EXPONENTS]
    rungs = []
    for i in range(1, len(es)):
        d = es[i] - es[i - 1]
        rungs.append((es[i - 1], es[i], d, d in CHO_DIMS, DIM_NAMES.get(d, "")))
    return rungs


# ===========================================================================
# 2. The 3-adic reframing of the hierarchy problem
# ===========================================================================
def padic_unit_scale():
    """
    Contrast the archimedean size of each hierarchy with its 3-adic size.

    Each ratio scale/M_P is (by the stated relation) an exact power of 3, so its
    3-adic absolute value is |3^-e|_3 = 3^e (a perfectly ordinary 3-adic number),
    while its archimedean value 3^-e is astronomically small. The hierarchy
    'problem' lives entirely in |.|_inf.
    """
    rows = []
    for label, e, _a in EXPONENTS:
        arch = P ** (-e)            # |scale/M_P|_inf  (tiny: the 'hierarchy')
        padic = float(P ** e)       # |scale/M_P|_3    (= 3^e, unit-ordinary)
        # The adelic product over {inf, 3} of |3^-e| is |3^-e|_inf * |3^-e|_3 = 1,
        # the same product formula that ties the primes to the reals.
        product = arch * padic
        rows.append((label, e, arch, padic, product))
    return rows


# ===========================================================================
# 3. Base-specialness: is 3 the natural base for the DATA-anchored scales?
# ===========================================================================
def base_specialness(ratio, bases=range(2, 13)):
    """
    For an observed ratio scale-separation, log_b(ratio) for each base b and the
    distance of that exponent to the nearest integer. A base in which the ratio
    sits near an exact integer power is 'natural' for that hierarchy.
    """
    out = []
    for b in bases:
        x = np.log(ratio) / np.log(b)
        dist = abs(x - round(x))
        out.append((b, x, dist))
    return out


def _cleanest(rows):
    """(base, exponent, dist) with the smallest distance-to-integer."""
    return min(rows, key=lambda r: r[2])


# ===========================================================================
# 4. Look-elsewhere Monte-Carlo null (prevents overclaiming)
# ===========================================================================
def look_elsewhere_null(n=400_000, seed=20260608):
    """
    How special is the {all perfect squares AND both increments in CHO_DIMS}
    conjunction fired by (9, 36, 64)?

    Null: draw exponent triples consistent with what the data/theory pin down --
    the two data-anchored exponents within +/-2 of their values (the data fix
    them to ~1), the unobserved seesaw exponent uniformly over a wide window.
    Count the conjunction frequency, then discount by the number of pattern
    families one might equally have 'noticed' (a Bonferroni-style look-elsewhere
    factor). Reports a deliberately CONSERVATIVE (large) discounted p.
    """
    rng = np.random.default_rng(seed)
    # windows: seesaw wide & unobserved; the two anchored ones tight (+/-2).
    mr = rng.integers(4, 17, size=n)             # [4, 16]
    mw = rng.integers(34, 39, size=n)            # [34, 38]
    cc = rng.integers(62, 67, size=n)            # [62, 66]

    def is_square(a):
        r = np.round(np.sqrt(a)).astype(int)
        return r * r == a

    all_square = is_square(mr) & is_square(mw) & is_square(cc)

    dimset = set(CHO_DIMS)
    d1 = mw - mr
    d2 = cc - mw
    in_dims = np.array([(a in dimset) and (b in dimset)
                        for a, b in zip(d1.tolist(), d2.tolist())])

    conjunction = all_square & in_dims
    raw_p = float(conjunction.mean())

    # Pattern families we might equally have noticed (declared, for honesty):
    #   perfect squares, increments-in-catalogue, all even, all multiples of 3,
    #   primes, triangular numbers. The conjunction uses 2 of these; the
    #   look-elsewhere factor counts the full menu we searched.
    pattern_families = (
        "perfect squares", "increments in CHO catalogue", "all even",
        "all multiples of 3", "all prime", "triangular numbers",
    )
    lee_factor = len(pattern_families)
    discounted_p = min(1.0, raw_p * lee_factor)
    return {
        "n": n,
        "raw_p": raw_p,
        "lee_factor": lee_factor,
        "pattern_families": pattern_families,
        "discounted_p": discounted_p,
    }


# ===========================================================================
def main():
    print("=" * 76)
    print("  BET 1 — ARE THE HIERARCHY EXPONENTS ARITHMETIC (3-adic), NOT ANALYTIC?")
    print("  EXPLORATORY. No Bayes credit. Asserts exact arithmetic + its own humility.")
    print("=" * 76)

    # ---- 1. perfect squares + increment ladder ----
    print("\n  [1] EXACT ARITHMETIC OF THE THREE STATED EXPONENTS")
    print("  " + "-" * 66)
    sq = perfect_square_audit()
    for label, e, r, ok, anchored in sq:
        tag = "data-anchored" if anchored else "theory-internal"
        print(f"    {label:<22} exponent {e:>3} = {r}^2  [{'OK' if ok else 'NO'}]  ({tag})")
    print("\n    increment ladder (consecutive differences):")
    for lo, hi, d, indims, name in increment_ladder():
        mark = f"= {name}" if name else ("in catalogue" if indims else "NOT in catalogue")
        print(f"        {lo:>3} --(+{d:>2})--> {hi:<3}   +{d} {mark}")
    print("    => homogeneous reading:  9  --(+27=dim J3(O))-->  36"
          "  --(+28=dim so(8))-->  64")
    print("       (the repo's labels were heterogeneous: |roots+E6|, dim A, 'seesaw')")

    # ---- 2. the 3-adic reframing ----
    print("\n  [2] 3-ADIC RE-FRAMING: THE HIERARCHY IS AN ARCHIMEDEAN ARTEFACT")
    print("  " + "-" * 66)
    print(f"    {'scale':<22}{'|.|_inf (the hierarchy)':>26}{'|.|_3':>10}{'product':>9}")
    for label, e, arch, padic, product in padic_unit_scale():
        print(f"    {label:<22}{arch:>26.3e}{padic:>10.3g}{product:>9.2f}")
    print("    => over Q_3 each ratio is unit-ordinary (|.|_3 = 3^e); the ~1e-17")
    print("       smallness lives ONLY in |.|_inf. Adelic product |x|_inf*|x|_3 = 1.")

    # ---- 3. base-specialness on the data-anchored scales ----
    print("\n  [3] IS 3 THE NATURAL BASE? (distance of log_b(ratio) to nearest integer)")
    print("  " + "-" * 66)
    ew_ratio = M_P / M_W_OBS
    cc_ratio = M_P / LAMBDA_QUARTER_OBS
    for name, ratio in (("electroweak  M_P/M_W", ew_ratio),
                        ("cosmological M_P/Lambda^1/4", cc_ratio)):
        rows = base_specialness(ratio)
        b, x, dist = _cleanest(rows)
        print(f"    {name}:  ratio = {ratio:.3e}")
        # show a few informative bases
        for bb, xx, dd in rows:
            if bb in (2, 3, 6, 8, 9, 10):
                flag = "  <== cleanest" if bb == b else ""
                print(f"        base {bb:>2}:  log = {xx:7.3f}   dist-to-int = {dd:5.3f}{flag}")
        print()
    print("    => EW sits within ~0.02 of an exact power of 3 (and of 9 = 3^2);")
    print("       non-power-of-3 bases are not clean. CC needs the sqrt2*12/11")
    print("       prefactor (dist ~0.40 raw) -- HONESTLY, only EW is base-3-clean.")

    # ---- 4. look-elsewhere null ----
    print("\n  [4] LOOK-ELSEWHERE NULL (does the pattern survive a multiplicity penalty?)")
    print("  " + "-" * 66)
    lee = look_elsewhere_null()
    print(f"    Monte-Carlo draws                 : {lee['n']:,}")
    print(f"    raw P(all squares & both incr in catalogue): {lee['raw_p']:.5f}")
    print(f"    pattern families searched (LEE)   : {lee['lee_factor']}  "
          f"{lee['pattern_families']}")
    print(f"    look-elsewhere-corrected p        : {lee['discounted_p']:.4f}")
    print(f"    promotion bar                     : {PROMOTION_P:.4f}")
    verdict = "BELOW bar (would be interesting)" if lee["discounted_p"] < PROMOTION_P \
        else "ABOVE bar -> SUGGESTIVE ONLY, not promotable"
    print(f"    => {verdict}")

    # ---- standing position ----
    print("\n  [5] STANDING POSITION (honest)")
    print("  " + "-" * 66)
    print("    * SOLID (conceptual): the EW hierarchy is not fine-tuned 3-adically;")
    print("      the puzzle is archimedean, and base 3 is independently distinguished")
    print("      in CHO. This reframes WHY the real-analytic spectral action (Phase 1)")
    print("      could never emit these scales -- it lives over R, not Q_3.")
    print("    * SUGGESTIVE (structural): the exponents form a homogeneous ladder")
    print("      9 -->+27=dim J3(O)--> 36 -->+28=dim so(8)--> 64, cleaner than the")
    print("      repo's heterogeneous labels -- but below the look-elsewhere bar.")
    print("    * NOT CLAIMED: the exponents stay CHOSEN. No Bayes credit moves.")
    print("    * NEXT (if pursued): read 4/7 and the pi in pi/432 as adelic periods /")
    print("      (mock) modular-form coefficients; seek ONE arithmetic relation over")
    print("      the whole constant set. See BIG_BETS_PLAN.md, Bet 1 follow-ons.")

    # ---- assertions: exact arithmetic (stable tripwires) + humility ----
    # Perfect squares and the increment ladder are immutable integer facts.
    assert all(ok for _l, _e, _r, ok, _a in sq), "an exponent is not a perfect square"
    es = [e for _l, e, _a in EXPONENTS]
    assert es == [9, 36, 64], "stated exponents changed -- re-confirm source-of-truth"
    assert es[1] - es[0] == 27, "EW-seesaw increment is not 27 = dim J3(O)"
    assert es[2] - es[1] == 28, "CC-EW increment is not 28 = dim so(8)"
    assert 27 in CHO_DIMS and 28 in CHO_DIMS, "increments left the declared catalogue"
    # 3-adic: each ratio is an exact power of 3, so the adelic 2-place product is 1.
    for _label, _e, arch, padic, product in padic_unit_scale():
        assert abs(product - 1.0) < 1e-9, "adelic product |x|_inf*|x|_3 != 1"
    # Base-3 cleanliness of the electroweak hierarchy (data-anchored, stable).
    ew_rows = base_specialness(M_P / M_W_OBS)
    ew_base3 = next(d for b, _x, d in ew_rows if b == 3)
    assert ew_base3 < 0.05, "EW hierarchy no longer within 0.05 of a power of 3"
    # HUMILITY TRIPWIRE: the look-elsewhere-corrected p must stay above the
    # promotion bar. This module forbids itself from silently becoming a 'result'.
    lee_check = look_elsewhere_null()
    assert lee_check["discounted_p"] > PROMOTION_P, (
        "discounted p crossed the promotion bar -- this would be a real finding; "
        "do NOT auto-promote: re-derive, widen the look-elsewhere menu, and move "
        "credit deliberately on the scoreboard, never here")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
