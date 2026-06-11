"""
Item 7d -- which frozen prediction is the sharpest? (registry-derived, checked)
===============================================================================

The program asserts in prose that sin^2(theta23) = 4/7 is "the single sharpest
falsifiable CHO claim". This module turns that EDITORIAL judgement into a
machine-checked FACT derived from the locked prediction registry itself: it
classifies every frozen prediction along objective defensibility axes read off
the registry's OWN frozen strings, scores and ranks them, and ASSERTS that
exactly one entry -- Theta23_octant -- is top-tier (an exact rational AND
independent of the open pi/432 seam). If a future edit adds another "exact"
prediction, makes theta23 lean on eps0, or drops it, the assertion fires.

Defensibility axes (each derived from registry strings, not hand-set verdicts)
------------------------------------------------------------------------------
  * eps0-independent : the formula/inputs do NOT mention epsilon0 / eps0 /
                       pi/432, so the value does not move with the open seam.
  * no dimensionful scale : the formula/inputs carry no measured scale
                       (M_P, v, m_H, Delta m^2, GeV/eV) -- a pure number.
  * exact rational : the formula is a bare small-integer ratio a/b with neither
                       eps0 nor a dimensionful scale -- the strongest tier: no
                       free parameter and no fitted prefactor at all.
  * sharp binary : the kill condition turns on a discrete alternative
                       (octant / mass ordering) -- a clean near-term yes/no.

Score = 3*exact_rational + 2*eps0_independent + 1*sharp_binary (transparent
integer weights; exact_rational dominates because it is the only tier with no
knob whatsoever). The full ranking is printed; only the structural conclusions
are asserted (the anchors/units inside the strings are never asserted).

Why the weights cannot be blamed for the verdict
------------------------------------------------
A skeptic will object that the (3,2,1) weights were chosen to make theta23 win.
They were not, and the module PROVES it: theta23's axis vector is (1,1,1,1) --
it is best-or-equal to every rival on EVERY axis and the unique entry that is an
exact rational -- so it is the unique Pareto-maximal prediction. A Pareto-
maximal element is the sharpest under ANY non-negative weighting with positive
weight on exactness, so the specific integer weights only fix the DISPLAY order;
no weight choice dethrones theta23. (This is the portfolio analogue of
theta23_fano_invariance killing the "did you pick e7?" objection.)

Honest scope
------------
This is a portfolio DIAGNOSTIC over the frozen registry. It crowns the most
defensible prediction; it does NOT make any prediction more true, does not
derive the open N5 physical map, promotes no ledger row, and does not move the
Bayes factor. The frozen registry stays authoritative; this reads it -- and the
locked manifest digest -- read-only.

No numpy / scipy. Standard library (re, fractions) + the locked registry.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/prediction_defensibility.py
"""

from __future__ import annotations

import re
from fractions import Fraction

import prediction_registry


# eps0 / open-seam markers (case-insensitive substring is unambiguous here).
EPS0_TOKENS = ("epsilon0", "eps0", "epsilon_0", "pi/432")

# Dimensionful / measured-scale markers. Matched CASE-SENSITIVELY with word
# boundaries so unit fragments cannot collide with ordinary words (e.g. the
# "eV" unit must not match the "ev" inside "seven").
DIM_RE = re.compile(r"\bGeV\b|\bMeV\b|\bmeV\b|\beV\b|M_P|m_H|Delta m|v\^2|v=|v =")

# A bare small-integer ratio a/b that is NOT glued to a word/decimal (so "pi/24"
# and "M_P/3^9" do not count -- their numerator is not a bare integer).
RATIO_RE = re.compile(r"(?<![\w.])(\d+)\s*/\s*(\d+)(?![\w.])")

# Discrete near-term alternatives that make a prediction a clean yes/no.
BINARY_TOKENS = ("octant", "ordering")

W_EXACT = 3
W_EPS0_INDEP = 2
W_BINARY = 1

TOP_TIER_NAME = "Theta23_octant"


def banner(title: str) -> None:
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


def _entry_text(entry) -> str:
    """All frozen prose for one entry: formula + inputs + kill condition."""
    return " ".join((entry.formula,) + tuple(entry.frozen_inputs)
                    + (entry.kill_condition,))


def _bare_ratio(formula: str):
    """Return the first bare integer ratio in the formula as a Fraction, else None."""
    m = RATIO_RE.search(formula)
    if not m:
        return None
    return Fraction(int(m.group(1)), int(m.group(2)))


def classify(entry) -> dict:
    """Objective defensibility flags + score for one frozen entry."""
    text = _entry_text(entry)
    low = text.lower()
    eps0_dependent = any(tok in low for tok in EPS0_TOKENS)
    has_dim_scale = DIM_RE.search(text) is not None
    ratio = _bare_ratio(entry.formula)
    eps0_independent = not eps0_dependent
    exact_rational = (ratio is not None) and eps0_independent and not has_dim_scale
    sharp_binary = any(tok in low for tok in BINARY_TOKENS)
    score = (W_EXACT * exact_rational
             + W_EPS0_INDEP * eps0_independent
             + W_BINARY * sharp_binary)
    return {
        "name": entry.name,
        "category": entry.category,
        "eps0_independent": eps0_independent,
        "no_dim_scale": not has_dim_scale,
        "exact_rational": exact_rational,
        "ratio": ratio,
        "sharp_binary": sharp_binary,
        "score": score,
    }


def portfolio() -> list:
    """Classify every frozen entry, ranked by defensibility score (desc)."""
    rows = [classify(e) for e in prediction_registry.FROZEN_ENTRIES]
    rows.sort(key=lambda r: (-r["score"], r["name"]))
    return rows


# The defensibility axes as an ordered boolean vector (exact_rational at index 2).
AXES = ("eps0_independent", "no_dim_scale", "exact_rational", "sharp_binary")


def _axis_vector(row) -> tuple:
    return tuple(bool(row[a]) for a in AXES)


def dominates(a: tuple, b: tuple) -> bool:
    """Pareto: a >= b on every axis and strictly > on at least one."""
    return all(x >= y for x, y in zip(a, b)) and any(x > y for x, y in zip(a, b))


def pareto_analysis(rows) -> dict:
    """Pareto structure of the defensibility axes.

    If one prediction is >= every rival on every axis (strictly > on at least
    one), it is the sharpest under ANY non-negative axis weighting -- so the
    headline verdict does not depend on the chosen integer weights, only the
    DISPLAY order does. This is the weight-independence guarantee.
    """
    vectors = {r["name"]: _axis_vector(r) for r in rows}
    maximal = [
        name for name, vec in vectors.items()
        if not any(dominates(other, vec)
                   for o_name, other in vectors.items() if o_name != name)
    ]
    top_vec = vectors[TOP_TIER_NAME]
    dominated = [
        name for name, vec in vectors.items()
        if name != TOP_TIER_NAME and dominates(top_vec, vec)
    ]
    return {
        "vectors": vectors,
        "maximal": maximal,
        "top_dominates": dominated,
        "top_is_unique_maximal": maximal == [TOP_TIER_NAME],
        "top_dominates_all": len(dominated) == len(vectors) - 1,
    }


def registry_integrity() -> dict:
    """Read-only: confirm the locked manifest digest still matches."""
    rows = prediction_registry.collect_registry_rows()
    manifest = prediction_registry.manifest_digest(rows)
    return {
        "manifest": manifest,
        "matches": manifest == prediction_registry.EXPECTED_MANIFEST_DIGEST,
    }


def _flag(b: bool) -> str:
    return "yes" if b else " . "


def main() -> bool:
    print("#" * 72)
    print("#  CHO ITEM 7d -- DEFENSIBILITY RANKING OF THE FROZEN PREDICTIONS")
    print("#  Machine-checks the editorial claim 'theta23 = 4/7 is THE sharpest'")
    print("#  against the locked registry. Diagnostic: promotes nothing, no Bayes.")
    print("#" * 72)
    print()

    rows = portfolio()

    # ------------------------------------------------------------------
    banner("A  DEFENSIBILITY AXES PER FROZEN PREDICTION (from registry strings)")
    print("    prediction          eps0-indep  no-scale  exact-ratio  binary  score")
    print("    " + "-" * 68)
    for r in rows:
        ratio = f" ({r['ratio']})" if r["ratio"] is not None else ""
        print(f"    {r['name']:<18}    {_flag(r['eps0_independent'])}       "
              f"{_flag(r['no_dim_scale'])}      {_flag(r['exact_rational'])}{ratio:<6}"
              f"   {_flag(r['sharp_binary'])}     {r['score']}")
    print()

    # ------------------------------------------------------------------
    banner("B  THE RANKING")
    for i, r in enumerate(rows, 1):
        tier = "TOP TIER" if r["exact_rational"] else "         "
        print(f"    {i}. {r['name']:<18} score {r['score']}   {tier}")
    winner = rows[0]
    exact_rows = [r for r in rows if r["exact_rational"]]
    print()
    print(f"  Sharpest frozen prediction: {winner['name']} (score {winner['score']}).")
    print(f"  Exact eps0-independent rationals in the whole registry: "
          f"{len(exact_rows)} ({', '.join(r['name'] for r in exact_rows)}).")
    print()

    # ------------------------------------------------------------------
    pareto = pareto_analysis(rows)
    banner("B'  WEIGHT-INDEPENDENCE -- theta23 is the unique Pareto-optimal bet")
    print("    prediction          (eps0-indep, no-scale, exact, binary)")
    print("    " + "-" * 58)
    for r in rows:
        vec = pareto["vectors"][r["name"]]
        flags = ", ".join("1" if v else "0" for v in vec)
        print(f"    {r['name']:<18}    ({flags})")
    print()
    print(f"  Pareto-maximal (no rival wins on every axis): "
          f"{', '.join(pareto['maximal'])}")
    print(f"  {TOP_TIER_NAME} dominates (>= on every axis, > on >=1): "
          f"{', '.join(pareto['top_dominates'])}")
    print("  => theta23 is best-or-equal on EVERY axis and the only exact rational,")
    print("     so it is sharpest under ANY non-negative weighting. The (3,2,1)")
    print("     weights only fix the display order -- they cannot manufacture the")
    print("     verdict (no weight choice dethrones it). Same spirit as proving the")
    print("     4/7 is a Fano invariant: remove the 'you chose it' objection.")
    print()

    # ------------------------------------------------------------------
    banner("C  HONEST READ")
    print("  Only theta23 = 4/7 is an EXACT rational that is also independent of the")
    print("  open pi/432 seam: no free parameter, no fitted prefactor, no measured")
    print("  scale. Sigma_m_nu is eps0-independent but a dimensionful BAND (seesaw")
    print("  scale), not a bare ratio; P2_m_betabeta leans on the open eps0 seam;")
    print("  P1 / P3 carry measured mass scales. So the program's prose claim that")
    print("  the octant is THE single sharpest bet is not editorial -- it is forced")
    print("  by the registry's own structure, and (section B') weight-independent.")
    print("  (The N5 physical map stays the open obligation; this ranks")
    print("  defensibility, it does not derive that map.)")
    print()

    # ------------------------------------------------------------------
    banner("D  LOCKED-REGISTRY INTEGRITY (read-only)")
    integ = registry_integrity()
    print(f"  manifest digest {'MATCH' if integ['matches'] else 'DRIFT'}: "
          f"{integ['manifest'][:32]}...")
    theta_payload = prediction_registry.theta23_octant_values()
    print(f"  Theta23_octant value payload: sin^2 = {theta_payload['sin2_theta23']:.6f}"
          f" ({Fraction(4, 7)}), octant = {theta_payload['octant']}")
    print()

    print("-" * 72)
    print("  Reading guide: this is a portfolio DIAGNOSTIC. It crowns the most")
    print("  defensible frozen prediction from the registry's own structure; it")
    print("  makes no prediction more true, promotes no ledger row, and does not")
    print("  move the Bayes factor. The frozen registry stays authoritative.")

    # ---- assert ONLY the structural conclusions (not the string anchors) ----
    # exactly one exact-rational entry, and it is the theta23 octant
    assert len(exact_rows) == 1, \
        f"expected exactly one exact eps0-independent rational, found {len(exact_rows)}"
    assert exact_rows[0]["name"] == TOP_TIER_NAME, \
        f"the unique exact rational must be {TOP_TIER_NAME}, got {exact_rows[0]['name']}"

    # the bare ratio parsed from the registry formula must be exactly 4/7 and
    # must equal the computed value payload (string <-> value cross-check)
    assert exact_rows[0]["ratio"] == Fraction(4, 7), \
        "the theta23 registry formula must read the bare ratio 4/7"
    assert abs(theta_payload["sin2_theta23"] - 4.0 / 7.0) < 1e-12, \
        "theta23 value payload must equal 4/7"

    # theta23 must be the STRICT unique top scorer
    assert winner["name"] == TOP_TIER_NAME, "theta23 must rank first"
    others = [r["score"] for r in rows if r["name"] != TOP_TIER_NAME]
    assert all(winner["score"] > s for s in others), \
        "theta23 must STRICTLY out-score every other frozen prediction"
    assert winner["score"] == W_EXACT + W_EPS0_INDEP + W_BINARY, \
        "theta23 must score on all three axes (exact + eps0-indep + binary)"

    # every prediction that leans on the open seam must be flagged not-eps0-indep,
    # and no eps0-dependent prediction may be exact
    for r in rows:
        if not r["eps0_independent"]:
            assert not r["exact_rational"], \
                f"{r['name']} depends on eps0 yet was scored exact -- impossible"

    # WEIGHT-INDEPENDENCE: theta23 is the UNIQUE Pareto-optimal prediction -- it
    # dominates every rival on every axis (>=) and strictly on the exact-rational
    # axis, so no non-negative weighting (with positive weight on exactness) can
    # dethrone it. The (3,2,1) weights are display-only; this is the portfolio
    # analogue of the 4/7 Fano-invariance proof (kills "you chose the weights").
    assert pareto["top_is_unique_maximal"], \
        "theta23 must be the UNIQUE Pareto-maximal prediction"
    assert pareto["top_dominates_all"], \
        "theta23 must Pareto-dominate every other frozen prediction"
    top_vec = pareto["vectors"][TOP_TIER_NAME]
    assert all(top_vec), "theta23 must score on ALL four defensibility axes"
    exact_idx = AXES.index("exact_rational")
    for name, vec in pareto["vectors"].items():
        if name == TOP_TIER_NAME:
            continue
        assert all(t >= o for t, o in zip(top_vec, vec)), \
            f"theta23 must be >= {name} on every defensibility axis (Pareto)"
        assert top_vec[exact_idx] and not vec[exact_idx], \
            f"theta23 must be the only exact rational vs {name}"

    # locked registry integrity (read-only)
    assert integ["matches"], "locked prediction-registry manifest digest must still match"

    print("\n  RESULT: PASS (ranking machine-checked; diagnostic, no row promoted).")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
