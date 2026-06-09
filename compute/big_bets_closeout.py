"""
BIG-BETS CLOSEOUT — the six exploratory faces, consolidated into one statement.
==============================================================================

Why this module exists
----------------------
After the internal CHO program terminated (`gold_standard_closeout.py`: the
earned ln B floor is -3.2, and the only open INTERNAL lever is one missing
derived dynamical action), the `big-bets` branch ran four ranked outside-the-box
bets from `BIG_BETS_PLAN.md`, across eight EXPLORATORY modules, asking whether
some NEW structure — counting dynamics, entropic gravity, sequential growth,
flavour statistics, positive geometry, or adelic number theory — could supply
what the static algebra could not: a derived measure/action, the coefficient
1/4, the generation count 3, a CHO-specific flavour texture, the exceptional
arena, or the specific constants.

This module is the capstone. Like `gold_standard_closeout.py` for the internal
program, it consolidates the WHOLE big-bets arc into ONE executable, self-checking
statement and ASSERTS the honest standing position against its source-of-truth
contracts, so the result cannot silently drift into over-claim. It is NOT a new
physics result and grants NO Bayes credit; it is a REPORTER that re-checks, every
time pytest runs, that all eight probes are still EXPLORATORY/OPEN and that the
scoreboard floor never moved.

The ONE finding the six faces triangulate
-----------------------------------------
Every bet delivered the SAME two-part result: it SUPPLIED THE FORM the static
algebra lacked (a genuine dynamical/structural principle of the right shape) but
NEVER THE CONTENT (the specific CHO number that would actually move credit).
Six independent structural directions, one boundary. That convergence is itself
the synthesis: it is strong (if negative) evidence that the missing object is
SINGULAR — a derived dynamical action that selects the seed/value — exactly the
object the internal closeout already localised. The big bets do not contradict
that closeout; they CONFIRM it from six new outside directions.

What it imports (source of truth, never re-derived here)
--------------------------------------------------------
* `audit_contract.CONTRACTS` -> the eight big-bets contracts; this module asserts
  every one is STATUS_EXPLORATORY / VERDICT_OPEN and still carries its humility
  (>=1 open bridge AND >=1 kill condition), so none was silently promoted.
* `scoreboard.scoreboard()`  -> the headline ln B ladder; this module asserts the
  EARNED floor is still -3.2 < 0, i.e. the whole big-bets arc moved no credit.

Nothing here is published, so nothing here is permanent. The assertions are a
TRIPWIRE, not a cage: they catch SILENT drift (a probe quietly promoted, the
floor quietly moved) and force any change to be DELIBERATE. This module is a
REPORTER, not a source: credit is earned in physics artifacts, never granted here.

No scipy. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/big_bets_closeout.py
"""

import audit_contract
import scoreboard


# The eight big-bets EXPLORATORY modules, in build order (artifacts #77-#84),
# grouped under the four ranked bets of BIG_BETS_PLAN.md.
BIG_BETS_MODULES = (
    "padic_hierarchy",             # Bet 1, probe 1 (exponents, additive/3-adic)
    "causal_set_lambda",           # Bet 2 (Lambda from Sorkin counting)
    "entropic_gravity_cho",        # Bet 2 (gravity / Newton's G)
    "everpresent_lambda_tracking", # Bet 2a (dynamical dark energy)
    "causal_growth_index",         # Bet 2 crux (does growth force N=3?)
    "statistical_flavour_ensemble",# Bet 3 (flavour distributions)
    "positive_geometry_cluster",   # Bet 4 (amplituhedron / cluster algebra)
    "adelic_constant_relation",    # Bet 1, probe 2 (constants, multiplicative)
)

# The six FORM-not-CONTENT faces. Each row:
#   (face, the new STRUCTURE supplied = the FORM,
#          the CHO target it could NOT force = the CONTENT,
#          backing modules)
FACES = (
    ("cosmological constant Lambda",
     "Sorkin's causal-set law Lambda ~ 1/sqrt(V): a genuine counting measure on histories",
     "the exponent 64 (consumes the OBSERVED 4-volume as input -- trades 'why 64' for the "
     "cosmic-coincidence 'why now'; base-3 is unforced, base 8 fits the volume better)",
     ("causal_set_lambda", "everpresent_lambda_tracking")),
    ("gravity / Newton's G",
     "Jacobson's dQ=TdS with horizon-cell counting: the area law S ~ A is automatic",
     "the coefficient 1/4 in S = A/4 (matching it only RELOCATES G into a_cell = 4 ln d; "
     "the bit-bookkeeping identity shows the CHO dimension is pure bookkeeping)",
     ("entropic_gravity_cho",)),
    ("generation count N = 3",
     "Rideout-Sorkin sequential growth: a covariant, Bell-causal measure on causets (criterion A met)",
     "the number 3 (a covariant non-spectator coupling exists for every N in 2..6; the "
     "exceptional rank-3 Albert algebra needs NON-ASSOCIATIVE octonionic input -- a "
     "kinematic Hurwitz/Jordan fact, not something the order-theoretic growth provides)",
     ("causal_growth_index",)),
    ("flavour texture",
     "a sharp many-observable DISTRIBUTION that decisively falsifies symmetry-blind anarchy for quarks",
     "a CHO-specific texture (what beats anarchy is the mass HIERARCHY, a charged F0 input; "
     "the triality-derived zero adds < the hierarchy's own contribution to the GST correlation)",
     ("statistical_flavour_ensemble",)),
    ("the exceptional arena",
     "a positive-geometry / cluster skeleton that HOSTS the CHO arena exactly "
     "(D4 -> 16, 28; E6 -> 36, 27; the unique Z/3 centre of E6) -- criterion B passes",
     "the arena itself (the cluster CELL count is never a CHO integer and never 3; the "
     "matches are non-unique and multi-hosted, so the arena is NOT selected; the octonionic "
     "positive geometry is unbuilt)",
     ("positive_geometry_cluster",)),
    ("the constants themselves",
     "an adelic / 3-adic reading: every predictive constant is arithmetic on the octonion "
     "primes {2,3,7} (432 = 2^4*3^3 = 16*27; sin^2 th23 = 4/7 = the Fano split 7 = 4+3)",
     "the specific values ({2,3,7}-smoothness is GENERIC for small integers and BREAKS on "
     "CHO's own dim F4 = 52 = 2^2*13, dim E6 = 78 = 2*3*13; no single Moonshine relation "
     "generates the set)",
     ("padic_hierarchy", "adelic_constant_relation")),
)

# The single most useful KEEPER on the (+) side: a real diagnosis of the failure
# mode, NOT a way through it.
KEEPER = (
    "The arithmetic/adelic reading explains WHY Phase 1 hit its wall: the CHO "
    "constants are number-theoretic objects (S-units on the octonion primes "
    "{2,3,7}; 432 = 16*27), and a real-ANALYTIC spectral action lives over R, "
    "which cannot emit them. A citable diagnosis of the failure -- it reframes "
    "the gap, it does not close it."
)

# No credit moved: today's EARNED scoreboard floor (a tripwire vs SILENT drift,
# not a frozen constant -- when the science earns a different floor, update and
# re-verify deliberately; this only forbids the big-bets arc moving it silently).
LNB_FLOOR = -3.2
LNB_TOL = 0.25


# --------------------------------------------------------------------------
def big_bets_contracts():
    """The (name, AuditContract) pairs for the eight big-bets modules."""
    return [(m, audit_contract.CONTRACTS[m]) for m in BIG_BETS_MODULES]


def all_exploratory_open():
    """True iff every big-bets module is EXPLORATORY/OPEN and still humble.

    'Still humble' = it carries at least one open bridge AND at least one kill
    condition, so a silent promotion (which would strip those) is caught.
    """
    for _name, c in big_bets_contracts():
        if c.status != audit_contract.STATUS_EXPLORATORY:
            return False
        if c.verdict != audit_contract.VERDICT_OPEN:
            return False
        if not c.open_bridges or not c.kill_conditions:
            return False
    return True


def scoreboard_floor():
    """Today's EARNED ln B floor from the source-of-truth scoreboard."""
    _gain, _n, _n_eff, rows = scoreboard.scoreboard(F=3.0)
    for label, _k, ln_b in rows:
        if "closed theorems" in label:
            return float(ln_b)
    raise KeyError("closed-theorem floor row not found in scoreboard")


def faces_cover_every_module():
    """True iff the six faces partition exactly the eight big-bets modules."""
    covered = []
    for _face, _form, _content, mods in FACES:
        covered.extend(mods)
    return sorted(covered) == sorted(BIG_BETS_MODULES) and len(covered) == len(BIG_BETS_MODULES)


# --------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("BIG-BETS CLOSEOUT: the six exploratory faces, consolidated")
    print("=" * 78)

    # ---- [A] the arc ----------------------------------------------------
    print("\n[A] THE ARC -- 4 ranked bets, 8 EXPLORATORY modules, 6 faces")
    print("    Bet 1 (arithmetic/adelic) : padic_hierarchy, adelic_constant_relation")
    print("    Bet 2 (counting dynamics) : causal_set_lambda, entropic_gravity_cho,")
    print("                                everpresent_lambda_tracking, causal_growth_index")
    print("    Bet 3 (flavour statistics): statistical_flavour_ensemble")
    print("    Bet 4 (positive geometry) : positive_geometry_cluster")

    # ---- [B] the six faces ----------------------------------------------
    print("\n[B] THE SIX FACES -- each supplied the FORM, none forced the CONTENT")
    for face, form, content, mods in FACES:
        print(f"\n    {face}")
        print(f"      FORM    (+): {form}")
        print(f"      CONTENT (-): {content}")
        print(f"      <- {', '.join(mods)}")

    # ---- [C] the convergence --------------------------------------------
    print("\n[C] CONVERGENCE -- six directions, one boundary, one missing object")
    print("    Counting (Lambda, gravity), growth (N=3), distributions (texture),")
    print("    positive geometry (arena) and arithmetic (constants) each deliver a")
    print("    structure of the RIGHT SHAPE -- a measure, an area law, a covariant")
    print("    growth law, a sharp falsifier, an exact host, an adelic reframing --")
    print("    yet none forces the specific CHO value. The FORM is reachable from many")
    print("    outside directions; the CONTENT is not reachable from any of them.")
    print("    This CONFIRMS the internal closeout from six new directions: the lone")
    print("    missing object is SINGULAR -- a derived dynamical action that selects")
    print("    the seed/value -- not a different gap per sector.")

    # ---- [D] tamper-evident standing position ---------------------------
    expl_open = all_exploratory_open()
    floor = scoreboard_floor()
    cover = faces_cover_every_module()
    n_modules = len(BIG_BETS_MODULES)
    print("\n[D] STANDING POSITION (tamper-evident)")
    print(f"    all {n_modules} probes still EXPLORATORY / OPEN (and still humble): {expl_open}")
    print(f"    the six faces cover exactly those {n_modules} modules            : {cover}")
    print(f"    EARNED scoreboard floor (whole arc moved no credit)  : ln B = {floor:+.1f}")
    print(f"    the floor is still negative (the null still wins)    : {floor < 0.0}")

    # ---- [E] the keeper -------------------------------------------------
    print("\n[E] THE ONE KEEPER (a diagnosis, not a derivation)")
    for line in _wrap(KEEPER, 72):
        print(f"    {line}")
    print("\n    Verdict: the big-bets arc is a HONEST NULL with a keeper framing.")
    print("    No constant promoted, no Bayes credit moved; the standalone math plus")
    print("    the honest null is unchanged. Further probes would re-read the same six")
    print("    faces; the only levers that can move the bottom line remain a derived")
    print("    action (internal) and an experiment / peer review (external).")
    print("=" * 78)

    # ---- tripwire assertions (forbid SILENT drift only) -----------------
    # [1] every big-bets module exists, is EXPLORATORY/OPEN, and stays humble.
    names = {n for n, _c in big_bets_contracts()}
    assert names == set(BIG_BETS_MODULES), "a big-bets module is missing from CONTRACTS"
    assert len(BIG_BETS_MODULES) == 8, "the big-bets module count changed -- re-confirm the arc"
    assert expl_open, (
        "a big-bets probe is no longer EXPLORATORY/OPEN-and-humble -- if one was "
        "genuinely promoted, move its credit deliberately on the scoreboard and update "
        "this reporter; do NOT let it drift silently")
    # [2] the six faces partition exactly the eight modules (no probe unaccounted).
    assert len(FACES) == 6, "the face count changed -- the synthesis is six faces"
    assert cover, "the six faces no longer cover exactly the eight big-bets modules"
    # [3] the whole arc moved NO credit: the earned floor is unchanged and < 0.
    assert abs(floor - LNB_FLOOR) < LNB_TOL, (
        "the scoreboard floor moved -- the big-bets arc must not change earned credit; "
        "if the science earned a new floor, update LNB_FLOOR deliberately and re-verify")
    assert floor < 0.0, "the earned floor went non-negative without being earned"
    # [4] this reporter must itself stay EXPLORATORY (it grants no credit).
    assert (audit_contract.CONTRACTS["big_bets_closeout"].status
            == audit_contract.STATUS_EXPLORATORY), \
        "the closeout reporter must stay EXPLORATORY -- it grants no Bayes credit"
    return True


def _wrap(text, width):
    """Tiny word-wrapper (no textwrap dependency needed)."""
    words, line, out = text.split(), "", []
    for w in words:
        if line and len(line) + 1 + len(w) > width:
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    if line:
        out.append(line)
    return out


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
