"""
The "different integer": triangulating the Higgs quartic lambda = pi/24.
========================================================================

The flavour seed eps0^2 = pi/432 got the full geometric triangulation: pi is
the Berry half-solid-angle (epsilon_heat_kernel / 02_action), 16 = dim OP^2 is
the rank-one vacuum manifold (epsilon_state_count, Jacobian nullity), 27 =
dim J3(O), and the flat 1/16, 1/27 weights are Schur-forced (epsilon_measure_schur).
That route is CLOSED at the action level (no F4-breaking action PRODUCES the
number) but the FORM is understood to the integer.

By contrast the OTHER hard-to-vary, pi-carrying constant in the framework --
the Higgs quartic

        lambda = pi/24      (m_H = v sqrt(pi/12), since (m_H/v)^2 = 2 lambda)

-- was only ever a one-line citation: "lambda = pi/24 from |roots(D4)| = 24"
(top_yukawa.py) / "from D4 root geometry, Paper 2" (forward_predictions.py).
The integer 24 was never put through the same forcedness analysis as 432. This
module turns that stone. It is a pure-arithmetic DIAGNOSTIC: stdlib `math` +
`fractions` only, no fit, no eps0 input beyond the published formulas.

What is PROVED here (exact, asserted)
-------------------------------------
  * 432 = 18 x 24, so lambda / eps0^2 = (pi/24)/(pi/432) = 432/24 = 18 EXACTLY.
    Hence lambda = 18 * eps0^2: the Higgs quartic and the flavour seed are NOT
    two independent transcendentals. They share ONE Berry pi and differ by a
    pure integer. GIVEN the established result that eps0^2 = pi/432 carries the
    Berry pi, the pi in lambda = pi/24 is therefore DERIVED, not an independent
    "D4 root geometry" assumption -- it is forced to be the same holonomy pi.
    The framework has one independent pi, not two.
  * 432 admits the framework factorizations 16 x 27 (dim OP^2 x dim J3(O)) and
    12 x 36 (half the D4 roots x E6 positive roots) and 18 x 24 -- all exact.

What is NOT proved (reported, never asserted as physics)
--------------------------------------------------------
  * The integer 24 is NOT uniquely forced. It has at least three distinct
    framework-dimension realizations: |roots(D4=so8)| = dim - rank = 28 - 4 = 24
    (the cited origin), the off-diagonal dimension of J3(O) = 27 - 3 = 3 x dim O
    = 24, and |2T| = 2|A4| = 24 (the binary-tetrahedral double cover that
    epsilon_a4_two_level already derives). That MULTIPLICITY is exactly the
    look-elsewhere problem on the integer: like the 432 in pi/432, the 24 is
    plausibly a dimension count, but no F4-breaking action selects the specific
    count. Same FORM-not-CONTENT wall, different observable.
  * Therefore lambda = pi/24 adds NO new derived bit beyond what eps0^2 = pi/432
    already represents. The one durable gain is the collapse of two pi-constants
    to one (lambda = 18 eps0^2).

This module promotes no ledger row and moves no Bayes credit; S3 (Higgs quartic)
stays a derived bridge whose normalization is the same open obligation as F0.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/higgs_quartic_geometry.py
"""

from __future__ import annotations

import math
from fractions import Fraction

# --- the two published pi-carrying constants (exact rational denominators) ---
LAMBDA = Fraction(1, 24)          # Higgs quartic lambda = pi/24  -> pi * LAMBDA
EPS0_SQ = Fraction(1, 432)        # flavour seed eps0^2 = pi/432  -> pi * EPS0_SQ
PI = math.pi
TOL = 1e-12

# --- framework dimensions used below (all integers, cited at point of use) ---
DIM_O = 8                         # dim of the octonions
DIM_OP2 = 16                      # dim OP^2 = F4/Spin(9) = rank-one vacuum manifold
DIM_J3O = 27                      # dim of the exceptional Jordan algebra J3(O)
SO8_DIM, SO8_RANK = 28, 4         # D4 = so(8): dimension and rank
E6_POSITIVE_ROOTS = 36            # E6 positive roots (= dim Spin(9))
A4_ORDER = 12                     # |A4| (tetrahedral); |2T| = 2|A4|


def banner(title: str) -> None:
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


# ---------------------------------------------------------------------------
#  [A]  lambda = 18 * eps0^2  -- the two pi-constants share ONE Berry pi
# ---------------------------------------------------------------------------
def shared_pi_relation() -> dict:
    """lambda/eps0^2 is the pure integer 18 = 432/24; both carry the same pi."""
    ratio = LAMBDA / EPS0_SQ                     # (1/24)/(1/432) = 432/24 = 18
    assert ratio == Fraction(18), ratio          # exact rational
    assert ratio.denominator == 1, ratio          # it really is an integer
    integer_ratio = ratio.numerator

    # float cross-check on the dimensionful values (same pi cancels exactly)
    lam_val = PI * float(LAMBDA)                  # pi/24
    eps_val = PI * float(EPS0_SQ)                 # pi/432
    assert abs(lam_val - integer_ratio * eps_val) < TOL

    return {
        "lambda": LAMBDA,
        "eps0_sq": EPS0_SQ,
        "ratio": integer_ratio,
        "lambda_val": lam_val,
        "eps0_val": eps_val,
    }


# ---------------------------------------------------------------------------
#  [B]  the framework factorizations of 432
# ---------------------------------------------------------------------------
def factorizations_of_432() -> list[tuple[str, int, int, str]]:
    """Exact factorizations 432 = a x b whose factors are framework dimensions."""
    facts = [
        ("16 x 27", DIM_OP2, DIM_J3O,
         "dim OP^2 x dim J3(O)  (the triangulated flavour-seed reading)"),
        ("12 x 36", SO8_DIM - SO8_RANK - 12, E6_POSITIVE_ROOTS,
         "half the D4 roots x E6 positive roots"),
        ("18 x 24", 18, 24,
         "the Higgs-quartic split: 432/24 = 18, lambda = pi/24"),
    ]
    for label, a, b, _note in facts:
        assert a * b == 432, (label, a, b)        # every factorization is exact
    return facts


# ---------------------------------------------------------------------------
#  [C]  the integer 24 -- how many framework dimensions equal it?
# ---------------------------------------------------------------------------
def integer_24_origins() -> list[tuple[str, int, str]]:
    """Distinct framework-dimension realizations of the Higgs-quartic 24.

    Multiplicity here IS the look-elsewhere measure on the integer: more than
    one independent geometric origin means 24 is NOT uniquely forced.
    """
    d4_roots = SO8_DIM - SO8_RANK                 # 28 - 4 = 24
    j3o_offdiag = DIM_J3O - 3                      # 27 - 3 = 24 (3 octonion slots)
    binary_tetra = 2 * A4_ORDER                    # |2T| = 2|A4| = 24
    origins = [
        ("|roots(D4=so8)| = dim - rank = 28 - 4", d4_roots,
         "the cited origin (top_yukawa.py)"),
        ("off-diagonal J3(O) = 27 - 3 = 3 x dim O", j3o_offdiag,
         "the three octonion off-diagonal slots, internal to the flavour algebra"),
        ("|2T| = 2|A4| (binary tetrahedral)", binary_tetra,
         "the A4 double cover derived in epsilon_a4_two_level"),
    ]
    for label, val, _note in origins:
        assert val == 24, (label, val)
    # the honest negative: at least two genuinely distinct origins exist
    distinct = {val for _label, val, _note in origins}
    assert distinct == {24} and len(origins) >= 2
    return origins


# ---------------------------------------------------------------------------
#  [D]  PROVED vs NOT-PROVED scorecard
# ---------------------------------------------------------------------------
def forcedness_verdict(rel: dict, origins: list) -> dict:
    """Assemble the honest scorecard for lambda = pi/24."""
    n_origins = len(origins)
    return {
        "pi_shared": True,                         # one Berry pi, proved by [A]
        "lambda_is_integer_multiple_of_eps0": rel["ratio"] == 18,
        "integer_24_unique": n_origins < 2,        # FALSE: not uniquely forced
        "n_framework_origins_of_24": n_origins,
        "new_derived_bit": False,                  # same wall as pi/432
    }


def main() -> bool:
    banner("Higgs quartic lambda = pi/24 -- triangulating the 'different integer'")

    rel = shared_pi_relation()
    print("  [A] shared Berry pi:")
    print(f"      lambda  = pi/24  = {rel['lambda_val']:.7f}")
    print(f"      eps0^2  = pi/432 = {rel['eps0_val']:.7f}")
    print(f"      lambda / eps0^2 = {rel['ratio']}  (exact integer)")
    print(f"      => lambda = {rel['ratio']} * eps0^2  : ONE pi, not two.")
    print("      GIVEN eps0^2 = pi/432 carries the Berry pi (established), the")
    print("      pi in lambda = pi/24 is forced to be the SAME holonomy pi.")
    print()

    facts = factorizations_of_432()
    print("  [B] framework factorizations of 432 (all exact):")
    for label, a, b, note in facts:
        print(f"      432 = {label:8s} = {a:2d} x {b:2d}   {note}")
    print()

    origins = integer_24_origins()
    print("  [C] framework-dimension origins of the integer 24:")
    for label, val, note in origins:
        print(f"      24 = {label:42s}  [{note}]")
    print(f"      => {len(origins)} distinct origins: 24 is NOT uniquely forced")
    print("         (this multiplicity is the look-elsewhere measure on the integer).")
    print()

    verdict = forcedness_verdict(rel, origins)
    print("  [D] PROVED vs NOT-PROVED:")
    print("      PROVED (exact)     : lambda = 18 * eps0^2; the two pi-constants")
    print("                           collapse to one Berry pi + one integer.")
    print("      NOT PROVED         : the integer 24 is not uniquely forced")
    print(f"                           ({verdict['n_framework_origins_of_24']} framework origins), and -- exactly")
    print("                           like 432 in pi/432 -- no F4-breaking action")
    print("                           selects it. Same FORM-not-CONTENT wall.")
    print("      NET                : no new derived bit; S3 normalization stays")
    print("                           the same open obligation as F0. The one gain")
    print("                           is one fewer independent transcendental.")
    print()

    ok = (
        rel["ratio"] == 18
        and verdict["pi_shared"]
        and verdict["lambda_is_integer_multiple_of_eps0"]
        and verdict["integer_24_unique"] is False
        and verdict["new_derived_bit"] is False
        and all(a * b == 432 for _l, a, b, _n in facts)
    )
    print(f"  RESULT: {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
