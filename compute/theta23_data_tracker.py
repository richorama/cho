"""
Item 7e -- the append-only data tracker + pre-registered verdict protocol for
sin^2(theta23) = 4/7.
=====================================================================

`theta23_octant_prediction.py` (Item 7) STAKES the bet (4/7, upper octant);
`theta23_experimental_reach.py` (Item 7c) QUANTIFIES the reach and confronts it
with current data. This module supplies the two remaining pieces of the forward
bet's discipline -- the things that make a prediction credible when the data
arrives years later:

  (1) A DATED, APPEND-ONLY LOG of global-fit / experiment snapshots, each scored
      read-only against the frozen Q2 = 4/7 payload. New releases append a new
      dated snapshot; nothing already logged is ever rewritten.

  (2) A PRE-REGISTERED, HASH-LOCKED DECISION RULE: the exact verdict protocol
      (what confirms, what kills, what precision is needed), canonicalised and
      SHA-256-locked so it cannot be silently softened after seeing the data.

The point of pre-registration
-----------------------------
A forward bet is only honest if its falsification criteria are fixed BEFORE the
deciding measurement. The frozen value lives in `prediction_registry.py` (Q2,
hash-locked); this module locks the *decision procedure* around it and tracks the
incoming data without ever touching either.

The pre-registered rule (formalising `theta23_experimental_reach.py`)
---------------------------------------------------------------------
The exact spine is fixed rationals (no fit, no eps0): 4/7 > 1/2 > 3/7, with
gap-to-maximal 1/14 (the octant test) and gap-to-mirror 1/7. Hence:

  * FIVE_SIGMA_OCTANT : a single-measurement precision sigma <= 1/70 (~0.0143)
    separates 4/7 from maximal at >= 5 sigma -> a decisive octant verdict.
  * CONFIRM_UPPER     : a stable upper-octant best fit consistent with 4/7 at the
    measured precision confirms the octant half of the bet.
  * KILL_LOWER        : a stable lower-octant (3/7-side) resolution at >= 5 sigma
    falsifies the prediction.
  * VALUE_KILLED      : a stable upper-octant value far from 4/7 (>= 5 sigma away)
    kills the exact rational while the upper-octant qualitative call survives.

What this module does NOT claim
-------------------------------
* It does not derive the physical N5 map "atmospheric mixing = avoiding/total";
  that bridge stays the open CHO-action obligation. 4/7 is exact GIVEN it.
* It is a tracking/registration DIAGNOSTIC: it promotes no ledger row and does
  not touch the Bayes factor. The forward bet itself is staked in Item 7.
* The logged global-fit anchors are representative NuFIT-class values carried
  read-only from `theta23_experimental_reach.GLOBAL_FITS` (printed, never
  asserted); chi^2 profiles are non-Gaussian, so the Gaussian pulls are rough
  context indicators only. Real future releases append as new dated snapshots.

No numpy / scipy. Standard-library `math`, `fractions`, `hashlib`, `json`, plus
the locked registry and the reach module for the single-source-of-truth spine.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/theta23_data_tracker.py
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math

import prediction_registry
import theta23_experimental_reach as reach


# ---- exact spine, reused from the reach module (single source of truth) ----
SIN2_UPPER = reach.SIN2_UPPER          # 4/7, CHO prediction (upper octant)
SIN2_MAXIMAL = reach.SIN2_MAXIMAL      # 1/2, maximal mixing (octant boundary)
SIN2_MIRROR = reach.SIN2_MIRROR        # 3/7, lower-octant mirror
GAP_MAXIMAL = reach.GAP_MAXIMAL        # 1/14, the octant test
GAP_MIRROR = reach.GAP_MIRROR          # 1/7, the full octant span

# 5-sigma octant verdict precision: sigma = (1/14)/5 = 1/70 ~ 0.0142857.
FIVE_SIGMA_OCTANT_SIGMA = GAP_MAXIMAL / 5      # Fraction(1, 70)
# A value is "consistent with / far from" 4/7 at the n-sigma level by this many
# units of sin^2(theta23) per sigma; the value-kill clause uses 5 sigma.
VALUE_KILL_NSIGMA = 5.0

TOL = 1e-12


# ---------------------------------------------------------------------------
#  Pre-registered, hash-locked decision rule
# ---------------------------------------------------------------------------
# Canonical, sorted-key JSON of this dict is SHA-256-locked below. Editing any
# clause changes the digest and trips the audit -- exactly as for the frozen
# value payloads in prediction_registry.py.
DECISION_RULE = {
    "name": "theta23_octant_verdict_protocol",
    "registered": "2026-06-11",
    "tracks": "prediction_registry Q2 Theta23_octant (sin^2 theta23 = 4/7, upper octant)",
    "exact_spine": {
        "upper_4_7": "4/7",
        "maximal_1_2": "1/2",
        "mirror_3_7": "3/7",
        "gap_to_maximal": "1/14",
        "gap_to_mirror": "1/7",
    },
    "five_sigma_octant_sigma": "1/70",
    "clauses": [
        "FIVE_SIGMA_OCTANT: a single-measurement precision sigma <= 1/70 (~0.0143) "
        "on sin^2 theta23 separates 4/7 from maximal at >= 5 sigma, giving a "
        "decisive octant verdict.",
        "CONFIRM_UPPER: a stable global best fit in the upper octant consistent "
        "with 4/7 at the measured precision confirms the octant half of the bet.",
        "KILL_LOWER: a stable lower-octant (3/7-side) resolution at >= 5 sigma "
        "(sin^2 theta23 < 1/2 robustly across orderings) falsifies the prediction.",
        "VALUE_KILLED_OCTANT_SURVIVES: a stable upper-octant value >= 5 sigma away "
        "from 4/7 kills the exact rational while the upper-octant call survives.",
    ],
    "frozen_payload_ref": "prediction_registry.theta23_octant_values (Q2, hash-locked)",
    "discipline": "Append-only: new data creates a new dated snapshot. This rule "
                  "and the frozen Q2 payload are never overwritten.",
}

# Locked after first computation (see _rule_digest); a mismatch fails the audit.
EXPECTED_RULE_DIGEST = "8c69fd0ffc9d16d66a3e429f1f9d24ac1adc2899bdda475773327847a9b00279"


@dataclass(frozen=True)
class Snapshot:
    """One dated global-fit / experiment release, scored read-only vs 4/7."""
    date: str
    source: str
    fits: tuple  # tuples (label, sin2_bestfit, sigma_lo, sigma_hi, note)
    note: str


# Append-only log. The 2026-06-11 baseline carries the representative NuFIT-class
# anchors from theta23_experimental_reach.GLOBAL_FITS (single source of truth, no
# new unsourced numbers). Real DUNE / Hyper-K / NuFIT releases append BELOW as new
# dated snapshots; existing rows are never edited.
SNAPSHOT_LOG = (
    Snapshot(
        date="2026-06-11",
        source="theta23_experimental_reach.GLOBAL_FITS (NuFIT-class representative)",
        fits=reach.GLOBAL_FITS,
        note="baseline snapshot at registration; octant genuinely open, "
             "NO global min on the 3/7 side currently disfavours 4/7.",
    ),
)


def _canon(obj) -> str:
    """Canonical JSON for hashing: sorted keys, compact separators."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _rule_digest() -> str:
    return hashlib.sha256(_canon(DECISION_RULE).encode("utf-8")).hexdigest()


def banner(title: str) -> None:
    print("=" * 72)
    print(f"  {title}")
    print("=" * 72)


# ---------------------------------------------------------------------------
#  [A]  executable classification of a single fit against the locked rule
# ---------------------------------------------------------------------------
def classify_fit(bestfit: float, sigma_lo: float, sigma_hi: float) -> dict:
    """Map one (best fit, asymmetric sigma) onto the pre-registered clauses.

    Uses the error bar on the side facing the relevant boundary. Returns the
    triggered clause label and the supporting separations. UNRESOLVED whenever
    the fit is within 5 sigma of maximal (the octant is not yet decided)."""
    upper = float(SIN2_UPPER)
    # separation from the maximal boundary, error bar on the side facing 1/2
    sigma_face_max = sigma_lo if bestfit >= 0.5 else sigma_hi
    sep_from_maximal = abs(bestfit - 0.5) / sigma_face_max
    # separation of this fit from the exact 4/7 value
    sigma_face_val = sigma_hi if upper >= bestfit else sigma_lo
    sep_from_value = abs(bestfit - upper) / sigma_face_val

    if sep_from_maximal < VALUE_KILL_NSIGMA:
        clause = "UNRESOLVED"
    elif bestfit < 0.5:
        clause = "KILL_LOWER"
    elif sep_from_value <= VALUE_KILL_NSIGMA:
        clause = "CONFIRM_UPPER"
    else:
        clause = "VALUE_KILLED_OCTANT_SURVIVES"

    return {
        "bestfit": bestfit,
        "sep_from_maximal": sep_from_maximal,
        "sep_from_value": sep_from_value,
        "clause": clause,
    }


def score_snapshot(snap: Snapshot) -> list:
    rows = []
    for label, bestfit, sig_lo, sig_hi, note in snap.fits:
        verdict = classify_fit(bestfit, sig_lo, sig_hi)
        # reuse the reach module's octant-probability toy for the tension column
        p_upper = reach.octant_upper_probability(bestfit, sig_lo, sig_hi)
        rows.append({"label": label, "note": note, "p_upper": p_upper, **verdict})
    return rows


def overall_status(log=SNAPSHOT_LOG) -> str:
    """Current verdict from the most recent snapshot under the locked rule."""
    latest = log[-1]
    clauses = {row["clause"] for row in score_snapshot(latest)}
    if "KILL_LOWER" in clauses and clauses == {"KILL_LOWER"}:
        return "FALSIFIED (stable lower octant)"
    if "CONFIRM_UPPER" in clauses and "KILL_LOWER" not in clauses:
        return "CONFIRMED (stable upper octant, consistent with 4/7)"
    if clauses == {"VALUE_KILLED_OCTANT_SURVIVES"}:
        return "VALUE FALSIFIED (upper octant, but far from 4/7)"
    return "UNRESOLVED (octant not yet decided at 5 sigma -- awaiting DUNE/Hyper-K)"


# ---------------------------------------------------------------------------
#  [B]  read-only registry cross-check
# ---------------------------------------------------------------------------
def registry_crosscheck() -> dict:
    """Confirm the locked Q2 payload still reads 4/7 / upper (read-only)."""
    payload = prediction_registry.theta23_octant_values()
    return {
        "payload": payload,
        "value_matches": abs(payload["sin2_theta23"] - float(SIN2_UPPER)) < TOL,
        "octant_matches": payload["octant"] == "upper",
    }


# ---------------------------------------------------------------------------
#  Reporting + tripwires
# ---------------------------------------------------------------------------
def main() -> bool:
    print("#" * 72)
    print("#  CHO ITEM 7e -- sin^2(theta23)=4/7 DATA TRACKER + LOCKED VERDICT RULE")
    print("#  Append-only data log + pre-registered, hash-locked decision protocol.")
    print("#  Diagnostic: stakes nothing new, promotes no row, moves no Bayes.")
    print("#" * 72)
    print()

    rule_digest = _rule_digest()

    # ------------------------------------------------------------------
    banner("A  PRE-REGISTERED DECISION RULE (hash-locked)")
    print(f"  name       : {DECISION_RULE['name']}")
    print(f"  registered : {DECISION_RULE['registered']}")
    print(f"  tracks     : {DECISION_RULE['tracks']}")
    print(f"  5-sigma octant precision : sigma <= 1/70 = {float(FIVE_SIGMA_OCTANT_SIGMA):.4f}")
    print("  clauses:")
    for clause in DECISION_RULE["clauses"]:
        tag = clause.split(":", 1)[0]
        print(f"    - {tag}")
    lock = "LOCKED-MATCH" if rule_digest == EXPECTED_RULE_DIGEST else "UNLOCKED/DRIFT"
    print(f"  rule SHA-256 : {rule_digest}")
    print(f"  lock status  : {lock}")
    print()

    # ------------------------------------------------------------------
    banner("B  APPEND-ONLY SNAPSHOT LOG (scored read-only vs 4/7)")
    for snap in SNAPSHOT_LOG:
        print(f"  [{snap.date}] {snap.source}")
        print(f"     note: {snap.note}")
        print("     fit              best fit   sep(1/2)   sep(4/7)   clause")
        print("     " + "-" * 64)
        for row in score_snapshot(snap):
            print(f"     {row['label']}  {row['bestfit']:.3f}     "
                  f"{row['sep_from_maximal']:5.2f} s    {row['sep_from_value']:5.2f} s    "
                  f"{row['clause']}")
        print()

    # ------------------------------------------------------------------
    banner("C  CURRENT OVERALL STATUS (under the locked rule)")
    status = overall_status()
    print(f"  {status}")
    print("  Honest read: today's fits sit within ~2-3 sigma of maximal, so no")
    print("  clause fires yet. The octant is genuinely open; DUNE / Hyper-K at")
    print(f"  sigma <= {float(FIVE_SIGMA_OCTANT_SIGMA):.4f} would deliver a 5-sigma octant verdict.")
    print()

    # ------------------------------------------------------------------
    banner("D  LOCKED-REGISTRY CROSS-CHECK (read-only)")
    reg = registry_crosscheck()
    state = "LOCKED-MATCH" if (reg["value_matches"] and reg["octant_matches"]) else "DRIFT"
    print(f"  registry Q2 (Theta23_octant) cross-check: {state}")
    print(f"    payload = {reg['payload']}")
    print()

    print("-" * 72)
    print("  Reading guide: this is the forward bet's DISCIPLINE -- a dated,")
    print("  append-only data log plus a hash-locked verdict rule, both wrapped")
    print("  around the frozen Q2 value without touching it. Tracking/registration")
    print("  DIAGNOSTIC: stakes nothing new, promotes no ledger row, moves no Bayes.")

    # ---- assert ONLY the exact / structural spine + the locks ----------------
    # exact spine (mirrors theta23_experimental_reach, kept in lockstep)
    assert SIN2_UPPER > SIN2_MAXIMAL > SIN2_MIRROR, "ordering 4/7 > 1/2 > 3/7 must hold"
    assert SIN2_UPPER + SIN2_MIRROR == 1, "octant mirror complementarity 4/7 + 3/7 = 1"
    assert GAP_MAXIMAL == Fraction(1, 14), "gap to maximal must be exactly 1/14"
    assert GAP_MIRROR == Fraction(1, 7), "gap to mirror must be exactly 1/7"
    assert FIVE_SIGMA_OCTANT_SIGMA == Fraction(1, 70), "5-sigma octant precision = (1/14)/5 = 1/70"
    # the locked decision rule must match its registered digest
    assert rule_digest == EXPECTED_RULE_DIGEST, (
        f"decision-rule drift: expected {EXPECTED_RULE_DIGEST}, got {rule_digest}")
    # classification boundaries behave as registered
    assert classify_fit(0.50, 0.02, 0.02)["clause"] == "UNRESOLVED", \
        "a fit at maximal must be UNRESOLVED"
    assert classify_fit(0.40, 0.01, 0.01)["clause"] == "KILL_LOWER", \
        "a 10-sigma lower-octant fit must trigger KILL_LOWER"
    assert classify_fit(float(SIN2_UPPER), 0.01, 0.01)["clause"] == "CONFIRM_UPPER", \
        "a precise fit sitting on 4/7 must trigger CONFIRM_UPPER"
    assert classify_fit(0.75, 0.01, 0.01)["clause"] == "VALUE_KILLED_OCTANT_SURVIVES", \
        "a precise far-upper fit must kill the value but keep the octant"
    # the current data must NOT yet decide the bet (honest live tension)
    assert overall_status().startswith("UNRESOLVED"), \
        "current representative data must remain UNRESOLVED under the rule"
    # the frozen registry payload still reads 4/7 / upper (read-only)
    assert reg["value_matches"] and reg["octant_matches"], \
        "locked registry Q2 payload must still read 4/7 / upper"

    print("\n  RESULT: PASS (tracker registered; diagnostic, no row promoted).")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
