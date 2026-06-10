"""
F0 SIGMA-MODEL CLOSEOUT — the OP^2 topological-action route, consolidated.
==========================================================================

Why this module exists
----------------------
The pi/432 (F0) lever — the single internal object that could flip the scoreboard
sign — has now been probed from every internal angle. The Connes spectral-triple
route is closed out by `f0_phase1_closeout` (heat-kernel a4/a2 REFUTED, L_X-spectrum
ratios PARTIAL; both converge on ONE missing dynamical seed-selection action), and
the topological-theta route by `f0_theta_reality_gate` (KO-6 forces theta = 0).

A SEPARATE route — a Berry/Wess-Zumino sigma-model on the triality-vacuum manifold
OP^2 = F4/Spin(9), the "topological not analytic" object that BOTH the heat-kernel
refutation (Phase 1.3) and the adelic keeper (big_bets_closeout) point at — was run
across three EXPLORATORY modules:

  #86 berry_sigma_model_op2  — assembles S = (Berry/WZ kinetic on OP^2) - (N3
       potential). FORM passes: the great-circle holonomy is pi exactly, the right
       kind of object where the analytic spectral action provably emits none.
       CONTENT fails STRUCTURALLY and that failure IS a NEW NO-GO: N3 (and every
       F4-INVARIANT, since F4 preserves the J3(O) spectrum) is CONSTANT on OP^2, so
       no F4-invariant potential can lift the vacuum degeneracy to a hierarchy.
  #87 berry_pi_intrinsic_op2 — hardens the FORM: the pi is F4-INTRINSIC (an
       isometry-invariant Berry holonomy on the two-point-homogeneous OP^2), a
       half-turn that SEPARATES two orthogonal generations — not a slice artefact.
  #88 f4_breaking_seed_op2   — attacks the CONTENT with the framework's OWN
       canonical F4-BREAKING object (the rank-one vacuum spurion). The three
       generations ARE the Morse critical points of the frame-breaking height
       V_A(P) = Tr(P o A); but the critical VALUES are spec(A) — the magnitudes
       stay input, the absolute scale is pi/432.

This module is the CLOSEOUT of that route. Like `f0_phase1_closeout` for the NCG
route and `big_bets_closeout` for the big-bets arc, it is NOT another derivation
attempt — hunting yet another internal derivation of pi/432 is the treadmill the
standing notes warn against. It is the opposite: a REPORTER that RECORDS the
sigma-model route as a converging-negative so the ground is never re-covered, and
states the one genuinely-new SHARPENING the route contributes.

The convergence (the closeout result)
-------------------------------------
The sigma-model route reaches the SAME wall as the spectral-triple route
(f0_phase1_closeout) and the topological-theta route (f0_theta_reality_gate): the
entire remaining F0 gap is ONE missing DYNAMICAL ACTION that must both PRODUCE
pi/432 and SELECT the three seeds. It is the FOURTH independent converging-negative
on that single object — now reached from the dynamical/topological side.

The one new thing this route adds (the SHARPENING)
--------------------------------------------------
It tells you what KIND of action is missing. #86's no-go proves any F4-INVARIANT
action is flat on the vacuum manifold, so the missing action must BREAK F4. #88
then shows the canonical F4-breaking object — the rank-one spurion — supplies the
DIRECTION (the three generations are exactly its frame's Morse critical points)
but NOT the MAGNITUDE (the critical values are its input spectrum; the absolute
scale is pi/432, the lone surviving input). So "need a derived action" sharpens to
"need a derived F4-BREAKING action whose flux is pi/432 and whose spectrum is the
seed" — DIRECTION solved, MAGNITUDE open.

The honest fork outcome (bounded, moves no credit)
--------------------------------------------------
The scoreboard sign does NOT flip: only BOTH halves (FORM and CONTENT) flipping
would, and CONTENT stays open. pi/432 stays Berry/Schur GEOMETRIC, F0 stays
GEOMETRIC/open, the standing null is unchanged. No Bayes credit moves; the ladder
(-21.3 / -3.2 / +5.6 / +36.2) and the frozen registry are untouched. Standing
position: the standalone math (PAPER_JORDAN_THEOREMS.md) + the honest null + the
one live EXTERNAL lever (sin^2 theta23 = 4/7, DUNE / Hyper-K).

What it imports (source of truth, never re-derived here)
--------------------------------------------------------
* `audit_contract.CONTRACTS` -> the three sigma-model contracts AND the four
  converging-negative contracts; this module asserts each sigma-model probe is
  STATUS_EXPLORATORY / VERDICT_OPEN and still humble (>=1 open bridge AND >=1 kill
  condition), and that the four converging-negative routes are all real artifacts.
* `scoreboard.scoreboard()` -> the headline ln B ladder; this module asserts the
  EARNED floor is still -3.2 < 0, i.e. the whole sigma-model route moved no credit.

The assertions are a TRIPWIRE against silent drift, not a cage: they catch a probe
quietly promoted or the floor quietly moved, and force any change to be DELIBERATE.
REPORTER, not a source: credit is earned in physics artifacts, never granted here.

No scipy. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_sigma_model_closeout.py
"""

import math

import audit_contract
import scoreboard


PI = math.pi
EPS0_SQ = PI / 432.0                       # eps0^2 = pi/432, the lone surviving input

# No credit moved: today's EARNED scoreboard floor (a tripwire vs SILENT drift,
# not a frozen constant -- when the science earns a different floor, update and
# re-verify deliberately; this only forbids the sigma-model route moving it).
LNB_FLOOR = -3.2
LNB_TOL = 0.25


# The three OP^2 sigma-model EXPLORATORY modules, in build order (artifacts #86-#88).
SIGMA_MODEL_MODULES = (
    "berry_sigma_model_op2",   # #86 FORM passes (pi), CONTENT no-go (F4-invariant flat)
    "berry_pi_intrinsic_op2",  # #87 FORM hardened (pi is F4-intrinsic, a half-turn)
    "f4_breaking_seed_op2",    # #88 F4-breaking: generations = Morse critical points
)

# The FOUR independent converging-negatives on the ONE missing dynamical action.
# Each row: (route, source-of-truth contract, what that route found).
CONVERGING_NEGATIVES = (
    ("prefactor (heat-kernel a4/a2)", "f0_spectral_action_heatkernel",
     "the finite spectral action's a4/a2 = 0.00582895 is a pi-FREE rational, so it "
     "can never equal the transcendental pi/432 -- pi/432 is NOT an analytic output"),
    ("ratios (L_X spectrum)", "spectral_action_432",
     "the octonionic averaging-law spectrum forces the mass STRUCTURE but the best "
     "single-knob eps0 ladder misses the absolute charged-lepton hierarchy by ~1.40 decades"),
    ("topological theta", "f0_theta_reality_gate",
     "the KO-6 / real-structure data force theta = 0 (eta = 0, mod-2 index 0, no "
     "Kramers Z2), so no topological theta-term carries the constant either"),
    ("sigma-model on OP^2 (this route)", "f4_breaking_seed_op2",
     "the Berry/WZ holonomy EMITS pi, but every F4-INVARIANT potential is FLAT on the "
     "vacuum manifold OP^2 -- the seed half needs an F4-BREAKING selector"),
)

# The sigma-model route's one genuinely-new SHARPENING of the missing object.
SHARPENING = (
    "FORM (the pi): SETTLED topologically -- the minimal great-circle Berry/WZ "
    "holonomy on OP^2 is pi exactly, and it is F4-INTRINSIC (isometry-invariant on "
    "the two-point-homogeneous OP^2), a half-turn separating two orthogonal "
    "generations, NOT an artefact of the associative slice.",
    "NO-GO: no F4-INVARIANT potential can select a hierarchical seed -- N3 and "
    "every F4-invariant is constant on the rank-one vacuum manifold -- so the "
    "missing action must BREAK F4.",
    "DIRECTION (solved): the canonical F4-breaking object, the rank-one vacuum "
    "spurion A, makes the three generations EXACTLY the Morse critical points of "
    "the frame-breaking height V_A(P) = Tr(P o A); the direction is "
    "frame-canonical, not circular.",
    "MAGNITUDE (open): the critical VALUES are spec(A) -- the seed magnitudes stay "
    "input and the absolute scale is pi/432, the lone surviving input; the "
    "scoreboard sign does NOT flip.",
)


# --------------------------------------------------------------------------
def sigma_model_contracts():
    """The (name, AuditContract) pairs for the three OP^2 sigma-model modules."""
    return [(m, audit_contract.CONTRACTS[m]) for m in SIGMA_MODEL_MODULES]


def all_exploratory_open():
    """True iff every sigma-model module is EXPLORATORY/OPEN and still humble.

    'Still humble' = it carries at least one open bridge AND at least one kill
    condition, so a silent promotion (which would strip those) is caught.
    """
    for _name, c in sigma_model_contracts():
        if c.status != audit_contract.STATUS_EXPLORATORY:
            return False
        if c.verdict != audit_contract.VERDICT_OPEN:
            return False
        if not c.open_bridges or not c.kill_conditions:
            return False
    return True


def converging_negatives_are_real():
    """True iff all four converging-negative routes name real audited contracts."""
    return all(name in audit_contract.CONTRACTS for _route, name, _found in CONVERGING_NEGATIVES)


def scoreboard_floor():
    """Today's EARNED ln B floor from the source-of-truth scoreboard."""
    _gain, _n, _n_eff, rows = scoreboard.scoreboard(F=3.0)
    for label, _k, ln_b in rows:
        if "closed theorems" in label:
            return float(ln_b)
    raise KeyError("closed-theorem floor row not found in scoreboard")


# --------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("F0 SIGMA-MODEL CLOSEOUT: the OP^2 topological-action route, consolidated")
    print("=" * 78)

    # ---- [A] the route --------------------------------------------------
    print("\n[A] THE ROUTE -- a Berry/WZ sigma-model on OP^2 = F4/Spin(9), 3 modules")
    print("    #86 berry_sigma_model_op2  : FORM passes (holonomy = pi); CONTENT no-go")
    print("                                 (N3 and every F4-invariant flat on OP^2)")
    print("    #87 berry_pi_intrinsic_op2 : FORM hardened (pi is F4-intrinsic, a half-turn")
    print("                                 separating two orthogonal generations)")
    print("    #88 f4_breaking_seed_op2   : F4-breaking spurion -> generations = Morse")
    print("                                 critical points; values = spec(A) (input)")

    # ---- [B] the four converging-negatives ------------------------------
    print("\n[B] FOUR INDEPENDENT CONVERGING-NEGATIVES on ONE missing dynamical action")
    for route, src, found in CONVERGING_NEGATIVES:
        print(f"\n    {route}")
        print(f"      <- {src}")
        for line in _wrap(found, 70):
            print(f"      {line}")
    print("\n    All four localise the ENTIRE remaining F0 gap to the SAME single object:")
    print("    a DERIVED dynamical action that must (i) produce pi/432 and (ii) select")
    print("    the three seeds. The sigma-model is the FOURTH such route -- now from the")
    print("    dynamical/topological side -- confirming f0_phase1_closeout.")

    # ---- [C] the sharpening ---------------------------------------------
    print("\n[C] THE ONE NEW THING THIS ROUTE ADDS -- what KIND of action is missing")
    for item in SHARPENING:
        for j, line in enumerate(_wrap(item, 70)):
            print(f"    {'- ' if j == 0 else '  '}{line}")
    print("\n    'need a derived action' sharpens to 'need a derived F4-BREAKING action")
    print("    whose flux is pi/432 and whose spectrum is the seed': DIRECTION solved")
    print("    (generations = critical points), MAGNITUDE open (absolute scale pi/432).")

    # ---- [D] tamper-evident standing position ---------------------------
    expl_open = all_exploratory_open()
    cn_real = converging_negatives_are_real()
    floor = scoreboard_floor()
    n_modules = len(SIGMA_MODEL_MODULES)
    print("\n[D] STANDING POSITION (tamper-evident)")
    print(f"    all {n_modules} sigma-model probes still EXPLORATORY/OPEN (and humble): {expl_open}")
    print(f"    the four converging-negative routes are all real artifacts  : {cn_real}")
    print(f"    EARNED scoreboard floor (this route moved no credit)        : ln B = {floor:+.1f}")
    print(f"    the floor is still negative (the null still wins)           : {floor < 0.0}")
    print(f"    the lone surviving input (absolute scale)                   : eps0^2 = pi/432 = {EPS0_SQ:.6f}")

    print("\n    Verdict: the OP^2 sigma-model route is an HONEST CONVERGING-NEGATIVE.")
    print("    The FORM (pi) is settled topologically and shown F4-intrinsic; the CONTENT")
    print("    (the seeds) is localised to one missing F4-BREAKING action that supplies the")
    print("    magnitude (= pi/432) the direction cannot. No constant promoted, no Bayes")
    print("    credit moved. Further internal derivations of pi/432 are the treadmill; the")
    print("    only levers that can move the bottom line remain a derived F4-breaking action")
    print("    (internal) and the external datum sin^2 theta23 = 4/7 (DUNE / Hyper-K).")
    print("=" * 78)

    # ---- tripwire assertions (forbid SILENT drift only) -----------------
    # [1] every sigma-model module exists, is EXPLORATORY/OPEN, and stays humble.
    names = {n for n, _c in sigma_model_contracts()}
    assert names == set(SIGMA_MODEL_MODULES), "a sigma-model module is missing from CONTRACTS"
    assert len(SIGMA_MODEL_MODULES) == 3, "the sigma-model module count changed -- re-confirm the arc"
    assert expl_open, (
        "a sigma-model probe is no longer EXPLORATORY/OPEN-and-humble -- if one was "
        "genuinely promoted, move its credit deliberately on the scoreboard and update "
        "this reporter; do NOT let it drift silently")
    # [2] the convergence is over FOUR real, independent routes (none silently dropped).
    assert len(CONVERGING_NEGATIVES) == 4, "the converging-negative count changed -- re-confirm the convergence"
    assert cn_real, "a converging-negative route no longer names a real audited contract"
    # [3] the sharpening keeps both halves: FORM settled, CONTENT (magnitude) still open.
    assert len(SHARPENING) == 4, "the sharpening lost a clause -- FORM/no-go/direction/magnitude"
    assert EPS0_SQ > 0.0, "the lone surviving input eps0^2 = pi/432 must stay the open scalar"
    # [4] the whole route moved NO credit: the earned floor is unchanged and < 0.
    assert abs(floor - LNB_FLOOR) < LNB_TOL, (
        "the scoreboard floor moved -- the sigma-model route must not change earned credit; "
        "if the science earned a new floor, update LNB_FLOOR deliberately and re-verify")
    assert floor < 0.0, "the earned floor went non-negative without being earned"
    # [5] this reporter must itself stay EXPLORATORY (it grants no credit).
    assert (audit_contract.CONTRACTS["f0_sigma_model_closeout"].status
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
