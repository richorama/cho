"""
F4-BREAKING ACTION CLOSEOUT — the 17-rung dissipative ladder, consolidated.
===========================================================================

Why this module exists
----------------------
`theory_probation_closeout` named, in writing, the ONE internal route worth more
time: "derive an F4-BREAKING dynamical action whose flux gives pi/432 and whose
spectrum gives the seed." The 17-rung `f4_breaking_*` ladder — from
`f4_breaking_action_origin_gate` through `f4_breaking_cooling_arrow_gate` — IS the
execution of exactly that route, built rung by rung. Its own terminal rung
(`f4_breaking_cooling_arrow_gate`) declares itself "the terminal rung of the
dissipative ladder": the residual that remains is the thermodynamic arrow of time,
not a shallower CHO sub-problem.

This module is the CLOSEOUT of that ladder. Like `f0_sigma_model_closeout` for the
OP^2 sigma-model route and `f0_phase1_closeout` for the spectral-triple route, it is
NOT another derivation attempt — adding an 18th rung to a self-declared-terminal
ladder is precisely the treadmill the standing notes forbid. It is the opposite: a
REPORTER that RECORDS the ladder as a converging-negative so the 17 rungs are never
re-walked, states honestly what the ladder DID earn (a forced dynamical scaffold and
several embedded theorems) and what it did NOT (the value pi/432, the seed
magnitudes), and surfaces the governance consequence the probation closeout
pre-registered.

The convergence (the closeout result)
-------------------------------------
The ladder is the longest single internal push the project has made at F0, and it
reaches the same wall as every other route, from the dynamical side: the VALUE
d = pi/432 is an INPUT at every one of the 17 rungs. The dynamics is built to be
CONSISTENT WITH an assumed d (every rung imports d and shows a forced structure
around it); no rung PRODUCES d. The chain of structural "why"s — why a half-log,
why a Born square, why a calibrated source, why an iid ensemble, why a Lindbladian,
why a Peirce jump structure, why a rank-one vacuum — bottoms out at the cooling
DIRECTION, which the terminal rung relocates to the zero-temperature / arrow-of-time
boundary condition: DEEPER and more general than pi/432, and not CHO-specific.

What the ladder DID earn (real, durable — kept)
-----------------------------------------------
The scaffold is not nothing. Several rungs are genuine theorems independent of the
F0 grant: Spohn's H-theorem (relaxation TO the steady state is automatic), the
J3(O) Peirce decomposition 27 = 1 + 16 + 10 with exact rational idempotents
(`f4_breaking_peirce_jump_gate`), purity strict-convexity forcing rank-one attractors
(`f4_breaking_vacuum_purity_gate`), and the uniqueness of the KL/calibrated-source
stationary point. Given d, the ladder assembles a continuous and largely FORCED
dynamical story from "a density" to "a dissipative dynamics whose unique pure steady
state is the primitive-idempotent vacuum." That structure stands.

What the ladder did NOT earn (the headway gap)
----------------------------------------------
The QUANTITATIVE target never moved. `source_overlap_derived_from_cho` is False at
every rung that records it; the value d = pi/432 stays an untouched input, the seed
MAGNITUDES stay spec(A) input, and the terminal residual is the arrow of time. So
the ladder made real STRUCTURAL headway and ZERO headway on the number that flips
the scoreboard sign.

The governance consequence (pre-registered)
--------------------------------------------
`theory_probation_closeout` pre-registered the rule: "If that cannot be done without
inserting the scale/seed by hand, demote the SM-constant program to beautiful
algebraic numerology with strong structure, not a theory of nature." The 17-rung
ladder is that route pursued to its terminus, and the scale (d = pi/432) and seed
(spec(A)) ARE inserted by hand at every rung. The pre-registered demotion condition
is therefore MET for the internal action-derivation route: the dynamical scaffold is
real and largely forced, but it does not derive the number.

The standing position (bounded, moves no credit)
-------------------------------------------------
The scoreboard sign does NOT flip. pi/432 stays Berry/Schur GEOMETRIC, F0 stays
GEOMETRIC/open, the earned floor stays ln B = -3.2 < 0, the frozen registry is
untouched. The only lever left that can move the bottom line is EXTERNAL — the sharp
falsifiable datum sin^2 theta23 = 4/7 (DUNE / Hyper-K) — plus shipping the standalone
math (PAPER_JORDAN_THEOREMS.md). Another internal pi/432 rung is the losing race.

What it imports (source of truth, never re-derived here)
--------------------------------------------------------
* `audit_contract.CONTRACTS` -> the 17 ladder contracts; this module asserts each is
  STATUS_EXPLORATORY / VERDICT_OPEN and still humble (>=1 open bridge AND >=1 kill
  condition), still names the target pi/432, and still disclaims moving Bayes credit.
* `scoreboard.scoreboard()` -> the headline ln B ladder; this module asserts the
  EARNED floor is still -3.2 < 0, i.e. the whole 17-rung ladder moved no credit.

The assertions are a TRIPWIRE against silent drift, not a cage: they catch a rung
quietly promoted, the floor quietly moved, or the ladder quietly extended (an 18th
rung must be a DELIBERATE re-opening, not a silent one). REPORTER, not a source:
credit is earned in physics artifacts, never granted here.

No scipy. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_action_closeout.py
"""

import math

import audit_contract
import scoreboard


PI = math.pi
EPS0_SQ = PI / 432.0                       # eps0^2 = pi/432, the lone surviving input

# No credit moved: today's EARNED scoreboard floor (a tripwire vs SILENT drift,
# not a frozen constant -- when the science earns a different floor, update and
# re-verify deliberately; this only forbids the action-derivation ladder moving it).
LNB_FLOOR = -3.2
LNB_TOL = 0.25


# The 17-rung F4-breaking action-derivation ladder, in build order. The hinge that
# localised the target -- f4_breaking_seed_op2 (#88) -- is owned by
# f0_sigma_model_closeout and is NOT re-counted here; this ladder is what was built
# AFTER it, to try to derive the action that #88 localised.
#
# Phase I -- FLUX -> SEED: map the geometric density d=pi/432 to the seed amplitude.
# Phase II -- WHY THE SOURCE: ground the dissipative dynamics that sources d.
LADDER = (
    # ---- Phase I: the Born / beta half-log map (density -> amplitude) ----------
    ("f4_breaking_action_origin_gate",
     "reduce the live bridge to beta = -log(eps0): the seed is a half-log of a density"),
    ("f4_breaking_beta_selection_gate",
     "select exp(-2 beta) = pi/432 as a stationary point rather than impose it"),
    ("f4_breaking_primitive_level_gate",
     "the selected density lives at the primitive (rank-one) idempotent level"),
    ("f4_breaking_level_one_carrier_gate",
     "the two-state CP^1 carrier fixes the WZ level-one density d = pi/432"),
    ("f4_breaking_born_beta_map_gate",
     "Born square map r = sqrt(d): exp(-2 beta) = d exactly (density -> amplitude)"),
    ("f4_breaking_born_geometry_gate",
     "Tr(P o Q) = |<psi|phi>|^2 hardens d as a projective transition probability"),
    # ---- Phase II: why the source -- the dissipative dynamics that emits d ------
    ("f4_breaking_source_stationarity_gate",
     "KL/Bernoulli stationarity has its unique min at q = d -> beta = -log(eps0)"),
    ("f4_breaking_calibrated_source_action_gate",
     "robust across all calibrated source actions (KL / Brier / Hellinger / logit)"),
    ("f4_breaking_large_deviation_source_gate",
     "finite binomial counting gives KL(d_hat || q) as the large-deviation rate"),
    ("f4_breaking_maxcal_ensemble_gate",
     "MaxCal with one mean-count constraint factorizes into iid Bernoulli(d)"),
    ("f4_breaking_binary_projector_history_gate",
     "the primitive question Q generates the {0,1}^N binary history space"),
    ("f4_breaking_repeated_measurement_gate",
     "Born + memoryless re-preparation gives the product Bernoulli(d) measure physically"),
    ("f4_breaking_vacuum_relaxation_gate",
     "a depolarizing-toward-P channel supplies the memorylessness (Born-Markov)"),
    ("f4_breaking_cho_lindbladian_gate",
     "a concrete GKSL generator L(rho) = gamma(Tr(rho)P - rho) realises the relaxation"),
    ("f4_breaking_peirce_jump_gate",
     "the jump structure IS the J3(O) Peirce decomposition 27 = 1 + 16 + 10 (forced, exact)"),
    ("f4_breaking_vacuum_purity_gate",
     "cooling (purity-gradient) + a generic frame-breaking field force the rank-one vacuum"),
    ("f4_breaking_cooling_arrow_gate",
     "the cooling DIRECTION relocates to the zero-temperature / arrow-of-time boundary (TERMINAL)"),
)

# The two phases, as (label, slice) into LADDER, for the report.
PHASE_I = (0, 6)    # FLUX -> SEED (the Born / beta half-log map)
PHASE_II = (6, 17)  # WHY THE SOURCE (the dissipative dynamics)

# What the ladder DID earn: structural results that stand without the F0 grant.
EARNED_STRUCTURE = (
    "Spohn's H-theorem: relaxation TO the steady state is automatic for every bath "
    "temperature (relative entropy monotone non-increasing) -- a general theorem, "
    "earned by f4_breaking_cooling_arrow_gate.",
    "The J3(O) Peirce decomposition 27 = 1 + 16 + 10 relative to a primitive "
    "idempotent, with EXACT rational projectors (error 0): the jump structure is "
    "FORCED by the Jordan geometry, not chosen -- f4_breaking_peirce_jump_gate.",
    "Purity Tr(rho o rho) is strictly convex on the eigenvalue simplex, so a cooling "
    "flow has ONLY rank-one attractors (rank-two saddles, centre a repeller): the "
    "rank-one vacuum is dynamically forced -- f4_breaking_vacuum_purity_gate.",
    "The KL / calibrated-source stationary point q = d is unique and robust across "
    "the whole calibrated class (KL/Brier/Hellinger/logit) -- f4_breaking_source_"
    "stationarity_gate / f4_breaking_calibrated_source_action_gate.",
)

# What the ladder did NOT earn: the quantitative target never moved.
UNEARNED_VALUE = (
    "The VALUE d = pi/432 is an INPUT at every one of the 17 rungs "
    "(source_overlap_derived_from_cho = False everywhere): the dynamics is built to "
    "be CONSISTENT WITH an assumed d, it never PRODUCES d.",
    "The seed MAGNITUDES stay spec(A) input -- the frame-breaking field's spectrum "
    "is assigned, not derived (cited open from f4_breaking_seed_op2).",
    "The terminal residual is the cooling DIRECTION = the thermodynamic arrow of "
    "time: DEEPER and more general than pi/432, universal physics, not CHO-specific. "
    "The CHO algebra is time-symmetric; the reverse generator cools to the anti-vacuum.",
)


# --------------------------------------------------------------------------
def ladder_contracts():
    """The (name, AuditContract) pairs for the 17 ladder rungs, in build order."""
    return [(m, audit_contract.CONTRACTS[m]) for m, _role in LADDER]


def _contract_text(c):
    """All human-readable text of a contract, concatenated (for keyword tripwires)."""
    parts = [c.public_claim_policy]
    parts.extend(c.assumptions)
    parts.extend(c.open_bridges)
    parts.extend(c.kill_conditions)
    return " ".join(parts)


def all_exploratory_open():
    """True iff every ladder rung is EXPLORATORY/OPEN and still humble.

    'Still humble' = it carries at least one open bridge AND at least one kill
    condition, so a silent promotion (which would strip those) is caught.
    """
    for _name, c in ladder_contracts():
        if c.status != audit_contract.STATUS_EXPLORATORY:
            return False
        if c.verdict != audit_contract.VERDICT_OPEN:
            return False
        if not c.open_bridges or not c.kill_conditions:
            return False
    return True


def value_stayed_input():
    """True iff every rung still NAMES the target pi/432 and still DISCLAIMS credit.

    This is the source-of-truth tripwire for the headway claim: each rung references
    the value d = pi/432 it is built around AND each still says it must not move
    Bayes credit. A rung silently promoted to 'derive pi/432' would have to drop the
    disclaimer; this catches it.
    """
    for _name, c in ladder_contracts():
        text = _contract_text(c).lower()
        if "pi/432" not in text:
            return False
        if "bayes" not in text and "credit" not in text:
            return False
    return True


def scoreboard_floor():
    """Today's EARNED ln B floor from the source-of-truth scoreboard."""
    _gain, _n, _n_eff, rows = scoreboard.scoreboard(F=3.0)
    for label, _k, ln_b in rows:
        if "closed theorems" in label:
            return float(ln_b)
    raise KeyError("closed-theorem floor row not found in scoreboard")


def _wrap(text, width):
    """Tiny word-wrapper (no textwrap import needed); yields lines <= width."""
    words, line = text.split(), ""
    for w in words:
        if len(line) + len(w) + (1 if line else 0) > width:
            yield line
            line = w
        else:
            line = f"{line} {w}" if line else w
    if line:
        yield line


# --------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("F4-BREAKING ACTION CLOSEOUT: the 17-rung dissipative ladder, consolidated")
    print("=" * 78)

    # ---- [A] the ladder -------------------------------------------------
    print("\n[A] THE LADDER -- the only active internal route (theory_probation_closeout),")
    print("    executed across 17 rungs from action_origin to the TERMINAL cooling_arrow")
    print("\n    Phase I -- FLUX -> SEED (the Born / beta half-log map):")
    for i in range(*PHASE_I):
        name, role = LADDER[i]
        print(f"      {i + 1:2}. {name}")
        for line in _wrap(role, 66):
            print(f"          {line}")
    print("\n    Phase II -- WHY THE SOURCE (the dissipative dynamics that emits d):")
    for i in range(*PHASE_II):
        name, role = LADDER[i]
        print(f"      {i + 1:2}. {name}")
        for line in _wrap(role, 66):
            print(f"          {line}")

    # ---- [B] what the ladder DID earn -----------------------------------
    print("\n[B] WHAT THE LADDER DID EARN (real, durable -- kept)")
    for item in EARNED_STRUCTURE:
        print()
        for line in _wrap(item, 72):
            print(f"    {line}")

    # ---- [C] what the ladder did NOT earn (the headway gap) -------------
    print("\n[C] WHAT THE LADDER DID NOT EARN (the headway gap)")
    for item in UNEARNED_VALUE:
        print()
        for line in _wrap(item, 72):
            print(f"    {line}")

    # ---- [D] the governance consequence ---------------------------------
    print("\n[D] GOVERNANCE CONSEQUENCE (pre-registered by theory_probation_closeout)")
    for line in _wrap(
        "Rule pre-registered: 'If [the F4-breaking action] cannot be done without "
        "inserting the scale/seed by hand, demote the SM-constant program to "
        "beautiful algebraic numerology with strong structure, not a theory of "
        "nature.' The 17-rung ladder is that route pursued to its terminus; the "
        "scale (d = pi/432) and seed (spec(A)) ARE inserted by hand at every rung. "
        "The demotion condition is MET for the internal action-derivation route: the "
        "dynamical scaffold is real and largely forced, but it does not derive the "
        "number.", 72):
        print(f"    {line}")

    # ---- [E] standing position ------------------------------------------
    floor = scoreboard_floor()
    print("\n[E] STANDING POSITION (the sign does NOT flip)")
    print(f"    eps0^2 = pi/432 = {EPS0_SQ:.8f}  -- stays Berry/Schur GEOMETRIC, the lone input")
    print(f"    earned scoreboard floor: ln B = {floor:+.2f}  (< 0: NULL still wins)")
    for line in _wrap(
        "Only live lever that can move the bottom line is EXTERNAL: sin^2 theta23 = "
        "4/7 (DUNE / Hyper-K), plus shipping the standalone math "
        "(PAPER_JORDAN_THEOREMS.md). Another internal pi/432 rung is the losing race.",
        72):
        print(f"    {line}")

    # ---- [V] verdict ----------------------------------------------------
    print("\n[V] Verdict")
    print(f"  ladder rungs consolidated (action_origin -> cooling_arrow)  : {len(LADDER)}")
    print("  every rung EXPLORATORY/OPEN and still humble                : YES")
    print("  forced dynamical scaffold + embedded theorems earned        : YES")
    print("  the VALUE pi/432 derived from CHO dynamics (any rung)       : NO")
    print("  the seed magnitudes derived (stay spec(A) input)            : NO")
    print("  residual is DEEPER than pi/432 (the arrow of time)          : YES")
    print("  pre-registered demotion condition met for this route        : YES")
    print("  Bayes/scoreboard credit moved                               : NO")
    print("=" * 78)

    # ---- tripwire assertions (catch SILENT drift; not a cage) -----------
    contracts = ladder_contracts()

    # the ladder is exactly the 17 self-declared rungs: an 18th must be DELIBERATE
    assert len(LADDER) == 17, "ladder length changed -- re-opening must be deliberate"
    assert len({m for m, _r in LADDER}) == 17, "duplicate rung in the ladder"
    assert LADDER[-1][0] == "f4_breaking_cooling_arrow_gate", "terminal rung changed"
    assert LADDER[0][0] == "f4_breaking_action_origin_gate", "first rung changed"
    assert all(name in audit_contract.CONTRACTS for name, _c in contracts)

    # every rung still EXPLORATORY/OPEN and humble (no silent promotion)
    assert all_exploratory_open(), "a ladder rung left EXPLORATORY/OPEN-and-humble"

    # the value stayed input: every rung names pi/432 AND disclaims moving credit
    assert value_stayed_input(), "a rung dropped the pi/432 target or the credit disclaimer"

    # all 17 carry the F0 lever (the route is genuinely the F0 push)
    for _name, c in contracts:
        assert "F0" in c.ledger_ids, "a ladder rung is not charged against F0"

    # no credit moved: the earned floor is still negative and near -3.2
    floor = scoreboard_floor()
    assert floor < 0.0, "earned floor went non-negative without a derivation"
    assert abs(floor - LNB_FLOOR) <= LNB_TOL, (
        f"earned floor {floor:+.3f} drifted from {LNB_FLOOR:+.2f} (re-verify deliberately)"
    )

    # the lone input is exactly pi/432
    assert abs(EPS0_SQ - PI / 432.0) < 1e-15
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
