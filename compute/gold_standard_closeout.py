"""
PROGRAM CLOSEOUT — the gold-standard scorecard, made executable and self-checking.
====================================================================================

Why this module exists
----------------------
`f0_phase1_closeout.py` closed *criterion 1* (the F0 / pi-432 dynamical route):
its three independent converging-negatives (the Phase-1.3 heat-kernel prefactor,
the Phase-1.4 L_X ratios, and the f0_theta_reality_gate topological angle) all
localise the entire F0 gap to ONE missing object -- a derived dynamical action.

This module is the PROGRAM-level analogue. It consolidates the WHOLE seven-point
gold-standard scorecard (ROBUSTNESS_ACTIONS.md) into one executable statement and
*asserts* the honest-null standing position against its source-of-truth modules,
so the Fail-branch position cannot SILENTLY drift into over-claim. It is NOT a new
physics result and NOT another invariance witness; it is the capstone that records
where the internal program terminates and re-checks it every time pytest runs.

What it imports (source of truth, never re-derived here)
--------------------------------------------------------
* `scoreboard.scoreboard()`     -> the single headline number, the ln B credit
  ladder: historical -21.3 -> closed-theorem floor -3.2 (today's EARNED position)
  -> +5.6 if the geometric pi/432 is GRANTED -> +36.2 if the program completes.
  The sign is still NEGATIVE at the earned floor: on earned credit, the numerology
  null still wins today; only GRANTING pi/432 flips the sign, and that credit is
  granted, not earned.
* `audit_contract.CONTRACTS`    -> the rigour census: how many THEOREM vs
  OPEN_BRIDGE artifacts, and a guard that the headline F0 and one-operator
  contracts are still OPEN (not silently promoted).
* `prediction_registry`         -> the frozen forward-prediction manifest digest
  (criterion 4 is PENDING an external clock, not closed by more internal work).
* `f0_phase1_closeout.prefactor_route / ratio_route` -> re-runs the two decisive
  Phase-1 numbers so criterion 1 is re-verified, not merely trusted by label.

The convergence this records
----------------------------
Every INTERNAL criterion collapses onto the same missing object:
  1 (dynamical principle)  ABSENT   -- the derived action (3 converging-negatives)
  3 (one unifying object)  OPEN     -- yukawa_operator_full forces the flavour
                                       STRUCTURE but not the magnitudes/seed; the
                                       deformation nulls localise the failure to
                                       eps0 + Fano phase + the seed = the SAME action
  2 (derived not fitted)   PARTIAL  -- 7 DERIVED vs 9 CHOSEN; the open half is the
                                       seed/exponents the action would fix
The EXTERNAL criteria cannot be closed by more internal work:
  4 (pre-registered hit)   PENDING  -- sin^2 th23 = 4/7 awaits DUNE / Hyper-K
  6 (single UV scale)      FALSIFIED-- two EW boundaries over-determine the scale
  7 (independent reproduction) ABSENT -- self-published; needs external review
So the internal program is COMPLETE in the precise sense that the only remaining
internal lever is the one missing action, and the only remaining external levers
are an experiment (4) and peer acceptance (7). Standing position (the Fail-branch,
now executable): the standalone math (PAPER_JORDAN_THEOREMS.md) + the honest null.

Nothing here is published, so nothing here is permanent. The numbers this module
asserts are today's EARNED position, not sacred constants. The assertions are a
TRIPWIRE, not a cage: they catch *silent* drift -- a refactor that quietly moves a
rung, an unearned promotion -- and force any change to be DELIBERATE. When the
science actually earns a different ladder, you update the constant here, re-verify,
and move on; that is following the evidence, not a violation. This module is a
REPORTER, not a source: it grants no Bayes credit of its own -- credit is earned in
the physics artifacts it reads.

No scipy. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/gold_standard_closeout.py
"""

import audit_contract
import prediction_registry
import scoreboard
from f0_phase1_closeout import prefactor_route, ratio_route


# Today's EARNED headline ladder (ROBUSTNESS_ACTIONS.md; quoted to 0.1 nat).
# A tripwire, not a freeze: when the science moves a rung, update the constant
# deliberately and re-verify -- the assertions below only forbid SILENT drift.
LNB_HISTORICAL = -21.3        # pre-eps0 program (only Georgi-Jarlskog 8/3 closed)
LNB_FLOOR = -3.2              # today's EARNED floor (every closed theorem credited)
LNB_GRANTED = 5.6            # if the geometric pi/432 is GRANTED (not earned)
LNB_TARGET = 36.2            # if the program completes (every choice derived)
LNB_TOL = 0.25               # tolerance: tight enough to catch drift, > float noise


# --------------------------------------------------------------------------
def scoreboard_ladder():
    """Pull the ln B credit ladder from the source-of-truth scoreboard.

    Returns a dict of the four rungs plus the credit-independent evidence gain."""
    gain, n, n_eff, rows = scoreboard.scoreboard(F=3.0)

    def rung(needle):
        for label, _k, ln_b in rows:
            if needle in label:
                return float(ln_b)
        raise KeyError(needle)

    return {
        "gain": float(gain),
        "n": int(n),
        "n_eff": float(n_eff),
        "historical": rung("historical"),
        "floor": rung("closed theorems"),
        "granted": rung("geometric pi/432"),
        "target": rung("target"),
    }


def contract_census():
    """Status histogram over every contracted artifact (the rigour criterion)."""
    counts = {}
    for c in audit_contract.CONTRACTS.values():
        counts[c.status] = counts.get(c.status, 0) + 1
    return counts


def registry_intact():
    """Is the forward-prediction manifest digest still at its recorded value?"""
    rows = prediction_registry.collect_registry_rows()
    digest = prediction_registry.manifest_digest(rows)
    return digest == prediction_registry.EXPECTED_MANIFEST_DIGEST, digest


def criterion_one_absent():
    """Re-run the two decisive Phase-1 routes; True iff both still need the action."""
    _a4a2, _M2, _M4, _gap, pre_closed = prefactor_route()
    _best, _miss, ratio_open = ratio_route()
    return pre_closed and ratio_open


def one_operator_open():
    """Criterion 3: is the one-operator flavour gate still OPEN (not promoted)?"""
    return (audit_contract.CONTRACTS["yukawa_operator_full"].status
            == audit_contract.STATUS_OPEN_BRIDGE)


# --------------------------------------------------------------------------
# The seven-point scorecard, each row tied to the source that backs it.
# (number, criterion, status, where it is anchored)
# --------------------------------------------------------------------------
SCORECARD = (
    (1, "Dynamical principle (action -> vacuum -> spectrum)", "ABSENT",
     "f0_phase1_closeout: 3 converging-negatives -> one missing derived action"),
    (2, "Parameters derived not fitted", "PARTIAL",
     "scoreboard: 7 DERIVED vs 9 CHOSEN; the open half is the seed/exponents"),
    (3, "One unifying object", "OPEN (bounded)",
     "yukawa_operator_full: structure forced, magnitudes/seed open -> same action"),
    (4, "Confirmed pre-registered prediction", "PENDING",
     "prediction_registry pre-registers sin^2 th23 = 4/7; awaits DUNE / Hyper-K"),
    (5, "Mathematical rigour (theorems)", "PARTIAL",
     "contract census: >=1 THEOREM, many OPEN_BRIDGE; PAPER_JORDAN_THEOREMS.md"),
    (6, "Continuum / UV control (single scale)", "FALSIFIED",
     "rg_scale_derivation: two EW boundaries over-determine the scale; gravity gated"),
    (7, "Independent reproduction / acceptance", "ABSENT",
     "self-published; not closable by internal work -- needs external review"),
)


# --------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("PROGRAM CLOSEOUT: the gold-standard scorecard, made executable")
    print("=" * 78)

    # ---- [1] the single headline number: the Bayes credit ladder --------
    L = scoreboard_ladder()
    print("\n[1] THE HEADLINE NUMBER -- ln B credit ladder (prior F = 3)")
    print(f"    evidence gain (credit-independent) : {L['gain']:+.1f} nats")
    print(f"    independent observables N / N_eff  : {L['n']} / {L['n_eff']:.1f}")
    print(f"    historical (pre-eps0, 8/3 only)    : ln B = {L['historical']:+.1f}")
    print(f"    closed-theorem floor (EARNED today): ln B = {L['floor']:+.1f}")
    print(f"    + geometric pi/432 (GRANTED)       : ln B = {L['granted']:+.1f}")
    print(f"    target (program complete)          : ln B = {L['target']:+.1f}")
    print("    the sign flips ONLY when pi/432 is GRANTED -- on earned credit the")
    print("    numerology null still wins; that is the honest standing position.")

    # ---- [2] the seven-point scorecard ----------------------------------
    census = contract_census()
    n_theorem = census.get(audit_contract.STATUS_THEOREM, 0)
    n_open = census.get(audit_contract.STATUS_OPEN_BRIDGE, 0)
    reg_ok, digest = registry_intact()
    print("\n[2] THE SEVEN-POINT GOLD-STANDARD SCORECARD")
    for num, crit, status, anchor in SCORECARD:
        print(f"    {num}. {crit:<46} {status:<14}")
        print(f"       <- {anchor}")
    print(f"\n    rigour census: {n_theorem} THEOREM, {n_open} OPEN_BRIDGE,"
          f" {len(audit_contract.CONTRACTS)} contracted total")
    print(f"    pre-registered prediction digest   : "
          f"{'MATCH' if reg_ok else 'CHANGED'} ({digest[:16]})")

    # ---- [3] the convergence --------------------------------------------
    c1_absent = criterion_one_absent()
    c3_open = one_operator_open()
    print("\n[3] CONVERGENCE -- the internal program terminates on one object")
    print("    Criteria 1, 3 and the open half of 2 are not independent jobs: each")
    print("    localises to the SAME missing derived dynamical action (the seed-")
    print("    selection / vacuum principle). The three converging-negatives plus the")
    print("    one-operator gate all land there. The external criteria (4, 7) and the")
    print("    falsified single scale (6) are not closable by more internal work.")
    print(f"    criterion 1 re-verified ABSENT (both routes need it): {c1_absent}")
    print(f"    criterion 3 one-operator still OPEN (not promoted)  : {c3_open}")

    # ---- [4] standing position ------------------------------------------
    print("\n[4] STANDING POSITION (the Fail-branch, now executable)")
    print("    Ship the standalone math (PAPER_JORDAN_THEOREMS.md) + the honest null.")
    print("    This capstone is a REPORTER, not a source: it grants no Bayes credit of")
    print("    its own. Its checks only forbid SILENT drift -- when the science earns a")
    print("    different ladder, update it deliberately and re-verify. The only open")
    print("    INTERNAL lever is the one derived action; the only open EXTERNAL levers")
    print("    are DUNE (criterion 4) and peer review (7).")
    print("=" * 78)

    # ---- tripwire assertions (audit.py ignores the return value) --------
    # These forbid SILENT drift only. When the science earns a different ladder,
    # update the constant deliberately and re-verify -- that is not a violation.
    # [1] the headline ladder still matches today's earned rungs ...
    assert abs(L["historical"] - LNB_HISTORICAL) < LNB_TOL, "historical ln B drifted"
    assert abs(L["floor"] - LNB_FLOOR) < LNB_TOL, "closed-theorem floor ln B drifted"
    assert abs(L["granted"] - LNB_GRANTED) < LNB_TOL, "granted pi/432 ln B drifted"
    assert abs(L["target"] - LNB_TARGET) < LNB_TOL, "target ln B drifted"
    # ... and strictly monotone, with the sign flip located at the pi/432 grant:
    assert L["historical"] < L["floor"] < 0.0 < L["granted"] < L["target"], \
        "the credit ladder lost its order / sign-flip location"
    # honesty guard: today's EARNED position is still null-favoured (floor < 0).
    assert L["floor"] < 0.0, "the earned floor went positive without earning it"
    # [2] rigour floor + the pre-registered forward predictions still match:
    assert n_theorem >= 1, "the THEOREM-status floor was lost"
    assert reg_ok, "prediction registry digest changed -- re-confirm it was intentional"
    # headline hinges must not be silently promoted off OPEN_BRIDGE:
    assert c3_open, "criterion 3 (one operator) was promoted off OPEN_BRIDGE"
    assert (audit_contract.CONTRACTS["f0_phase1_closeout"].status
            == audit_contract.STATUS_OPEN_BRIDGE), \
        "criterion 1 closeout was promoted off OPEN_BRIDGE"
    # [3] criterion 1 is re-verified ABSENT from the genuine routes:
    assert c1_absent, "criterion 1 is no longer ABSENT (both routes would need the action)"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
