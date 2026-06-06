"""
Derivation scoreboard: one number that tracks whether the derivation work pays.
==============================================================================

The model-comparison Bayes factor (bayesian_evidence.py) is the project's honest
scoreboard: it charges CHO the full Occam price for every prefactor it CHOOSES
and credits nothing for prefactors it DERIVES. The single question this module
answers is therefore:

    "Has the eps0 = pi/432 derivation program actually moved that number,
     or just added more machinery?"

It does NOT recompute the physics. It reuses two credit-independent facts from
bayesian_evidence.py --

    * the evidence GAIN (how well the fixed predictions match data, corrected
      for the shared-eps0 common mode); this does not depend on what we credit, and
    * the Occam PENALTY = (bits still paid for) * ln 2, which DOES depend on
      which derivation statuses we credit as free --

and sweeps the credit policy from "skeptic credits nothing" up to "program
complete", reading off ln B at each step. Because

    ln B = evidence_gain  -  k_bits * ln 2,

every nat of movement is exactly the description length retired by a derivation.
The credited sets are the SAME status tags audited in model_complexity.py, so the
scoreboard cannot be moved by hand without changing a status there (and its note,
which cites the module that earns it).

Reading guide (Jeffreys): ln B > 0 favours CHO; the sign is the headline.

No scipy. Reuses bayesian_evidence and model_complexity.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/scoreboard.py
"""

import math

from bayesian_evidence import log_bayes_factor, jeffreys
from model_complexity import (
    STRUCTURAL_CHOICES,
    DERIVED,
    GEOMETRIC,
    CHOSEN,
)

GEORGI_JARLSKOG = "Georgi-Jarlskog 8/3 = dim(O)/N_c"


def _discrete_total():
    """All discrete structural bits (nothing credited)."""
    return sum(bits for _l, bits, _s, _n in STRUCTURAL_CHOICES)


def _bits_charged(credited_statuses):
    """Bits still paid for when `credited_statuses` are free."""
    return sum(bits for _l, bits, status, _n in STRUCTURAL_CHOICES
               if status not in credited_statuses)


def _bits_charged_except(free_labels):
    """Bits still paid for when only the named labels are free (historical baseline)."""
    return sum(bits for label, bits, _s, _n in STRUCTURAL_CHOICES
               if label not in free_labels)


def _items(status):
    return [(label, bits, note) for label, bits, s, note in STRUCTURAL_CHOICES
            if s == status]


def ln_b_from_bits(evidence_gain, k_bits):
    """ln B = evidence_gain - k_bits * ln 2 (the only credit-dependent term)."""
    return evidence_gain - k_bits * math.log(2.0)


def scoreboard(F=3.0):
    """Return ln B under a ladder of credit policies at prior width F."""
    # The evidence gain is credit-independent; pull it from any single call.
    base = log_bayes_factor(F, credited=())
    gain = base["corrected"]
    n, n_eff = base["n"], base["n_eff"]

    rows = []

    # 0. Pure skeptic: credit nothing at all.
    k = _bits_charged(())
    rows.append(("skeptic: nothing credited", k, ln_b_from_bits(gain, k)))

    # H. Historical baseline (pre-eps0 program): only Georgi-Jarlskog 8/3 was a
    #    closed result; this reproduces the ~-21 figure the docs quote.
    k = _bits_charged_except({GEORGI_JARLSKOG})
    rows.append(("historical (pre-eps0: 8/3 only)", k, ln_b_from_bits(gain, k)))

    # 1. Closed theorems: every numerically-closed prefactor credited (today's
    #    conservative floor, == bayesian_evidence default).
    k = _bits_charged((DERIVED,))
    rows.append(("closed theorems (today's floor)", k, ln_b_from_bits(gain, k)))

    # 2. + geometric pi/16/27: also credit eps0^2 = pi/432 (number forced by
    #    computed dimensions/holonomy; residual is operator existence/frame).
    k = _bits_charged((DERIVED, GEOMETRIC))
    rows.append(("+ geometric pi/432 (16,27,Berry)", k, ln_b_from_bits(gain, k)))

    # 3. Target: program complete, every structural choice derived.
    k = _bits_charged((DERIVED, GEOMETRIC, CHOSEN))
    rows.append(("target (program complete)", k, ln_b_from_bits(gain, k)))

    return gain, n, n_eff, rows


def main():
    print("=" * 78)
    print("  DERIVATION SCOREBOARD — does deriving prefactors move the Bayes factor?")
    print("  ln B = evidence_gain - (bits still paid) * ln 2.  Sign is the headline.")
    print("=" * 78)

    gain, n, n_eff, rows = scoreboard(F=3.0)
    total = _discrete_total()

    print(f"\n  Independent observables N         : {n}")
    print(f"  Effective independent N_eff       : {n_eff:.1f}  (shared-eps0 common mode)")
    print(f"  Evidence gain (credit-independent): {gain:+.1f} nats")
    print(f"  Total discrete structural bits    : {total:.1f}")

    print("\n  CREDIT LADDER (at reference prior F = 3)")
    print("  " + "-" * 72)
    print(f"    {'credit policy':<34}{'bits paid':>10}{'ln B':>9}{'log10 B':>10}  verdict")
    print("  " + "-" * 72)
    skeptic_lnb = rows[0][2]
    for label, k_bits, ln_b in rows:
        side, _ = jeffreys(ln_b)
        flag = "CHO" if ln_b > 0 else "null"
        print(f"    {label:<34}{k_bits:>10.1f}{ln_b:>9.1f}"
              f"{ln_b / math.log(10):>10.1f}  {flag}")
    print("  " + "-" * 72)

    # Find where the sign crosses zero.
    crossing = None
    for i in range(1, len(rows)):
        if rows[i - 1][2] <= 0 < rows[i][2]:
            crossing = rows[i][0]
            break

    hist = rows[1][2]
    floor = rows[2][2]
    geom = rows[3][2]
    target = rows[4][2]

    print("\n  WHAT THE EPS0 PROGRAM ACTUALLY DID")
    print(f"   * Historical (only 8/3 closed)      : ln B = {hist:+.1f}  "
          f"(the '-21' the docs quote)")
    print(f"   * Today's closed-theorem floor       : ln B = {floor:+.1f}  "
          f"(moved {floor - hist:+.1f} nats)")
    print(f"   * Crediting the geometric pi/432     : ln B = {geom:+.1f}  "
          f"(moved {geom - hist:+.1f} nats vs historical)")
    print(f"   * Target if the program completes    : ln B = {target:+.1f}")
    if crossing:
        print(f"   * SIGN FLIPS at: '{crossing}'.")
        print("     => the verdict now HINGES on one named claim: whether pi/432 is")
        print("        geometrically forced (epsilon_state_count / _weyl_isomorphism /")
        print("        _spin9_embedding). That is a sharp, falsifiable seam, not a knob.")
    else:
        if floor > 0:
            print("   * The closed theorems ALONE already flip the verdict positive.")
        else:
            print("   * The verdict stays negative across every credit policy below target;")
            print("     the program has moved the needle but not yet crossed zero.")

    print("\n  ROBUSTNESS — geometric-credit ln B across prior widths F")
    print("  " + "-" * 50)
    print(f"    {'F':>5}{'ln B (closed)':>16}{'ln B (+geom)':>16}")
    for F in (2.0, 3.0, 5.0, 10.0):
        _, _, _, r = scoreboard(F=F)
        print(f"    {F:>5.0f}{r[2][2]:>16.1f}{r[3][2]:>16.1f}")

    print("\n  CREDITED ITEMS (transparency — cannot be moved without editing a status)")
    print("  " + "-" * 72)
    for status, tag in ((DERIVED, "DERIVED (closed)"),
                        (GEOMETRIC, "GEOMETRIC (number forced, seam open)"),
                        (CHOSEN, "CHOSEN (still paid)")):
        items = _items(status)
        bits = sum(b for _l, b, _n in items)
        print(f"    {tag} — {len(items)} items, {bits:.1f} bits:")
        for label, b, note in items:
            print(f"        {label:<36} {b:5.1f}  {note}")
    print()


if __name__ == "__main__":
    main()
