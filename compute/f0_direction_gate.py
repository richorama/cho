"""
F0 direction gate: continue closure work, or pivot.

Purpose
-------
User-level confusion often comes from doing mathematically correct work that
still does not change the headline verdict. This module is a governance gate,
not a physics derivation:

1) Read the current F0 contracts from audit_contract.py.
2) Inspect the eps0 structural status in model_complexity.py.
3) Read the Bayes ladder from scoreboard.py.
4) Emit an explicit recommendation:
   - CONTINUE F0 closure only if there is a direct path to changing a live
     F0 contract from OPEN to CLOSED (or to moving eps0^2 from GEOMETRIC to
     DERIVED with a real theorem).
   - Otherwise PIVOT to non-theory-for-theory tracks (falsification / paper /
     prediction discipline).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_direction_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass

from audit_contract import (
    CONTRACTS,
    STATUS_OPEN_BRIDGE,
    STATUS_DERIVED_BRIDGE,
    STATUS_THEOREM,
    VERDICT_OPEN,
    VERDICT_CLOSED,
)
from model_complexity import STRUCTURAL_CHOICES, GEOMETRIC, DERIVED
from scoreboard import scoreboard


@dataclass(frozen=True)
class F0Row:
    artifact: str
    status: str
    verdict: str
    open_bridge_count: int


def _f0_contract_rows():
    rows = []
    for name, c in CONTRACTS.items():
        if "F0" in c.ledger_ids:
            rows.append(F0Row(name, c.status, c.verdict, len(c.open_bridges)))
    rows.sort(key=lambda r: r.artifact)
    return rows


def _eps0_status():
    for label, _bits, status, note in STRUCTURAL_CHOICES:
        if label.startswith("eps0^2 = pi/432"):
            return status, note
    return None, "eps0 row not found"


def _live_f0_bridges():
    items = []
    for name, c in CONTRACTS.items():
        if "F0" in c.ledger_ids and c.open_bridges:
            for b in c.open_bridges:
                items.append((name, b))
    return items


def main() -> bool:
    rows = _f0_contract_rows()
    eps0_status, eps0_note = _eps0_status()

    gain, _n, _n_eff, ladder = scoreboard(F=3.0)
    ln_closed = ladder[2][2]    # closed-theorem floor
    ln_geom = ladder[3][2]      # + geometric pi/432

    n_open = sum(1 for r in rows if r.verdict == VERDICT_OPEN or r.status == STATUS_OPEN_BRIDGE)
    n_closed = sum(1 for r in rows if r.verdict == VERDICT_CLOSED or r.status in (STATUS_DERIVED_BRIDGE, STATUS_THEOREM))

    print("=" * 78)
    print("  F0 DIRECTION GATE")
    print("  Continue seam-closure work, or pivot to falsification/paper work?")
    print("=" * 78)
    print()

    print("  Contract status snapshot (F0 artifacts)")
    print("  " + "-" * 74)
    print(f"  {'artifact':<32} {'status':<14} {'verdict':<10} open_bridges")
    for r in rows:
        print(f"  {r.artifact:<32} {r.status:<14} {r.verdict:<10} {r.open_bridge_count}")
    print()

    print("  Scoreboard context (credit-independent gain shown for orientation)")
    print("  " + "-" * 74)
    print(f"  evidence gain                 : {gain:+.1f} nats")
    print(f"  ln B (closed-theorem floor)   : {ln_closed:+.1f}")
    print(f"  ln B (+ geometric pi/432)     : {ln_geom:+.1f}")
    print(f"  eps0 structural status        : {eps0_status}  ({eps0_note})")
    print()

    live = _live_f0_bridges()
    print("  Live F0 bridges")
    print("  " + "-" * 74)
    for a, b in live:
        print(f"  - {a}: {b}")
    print()

    # Decision rule: if eps0 is still GEOMETRIC and any F0 bridge is open, we
    # continue ONLY if next task directly targets one named open bridge.
    continue_allowed = (eps0_status == GEOMETRIC and n_open > 0)

    print("  DECISION")
    print("  " + "-" * 74)
    if continue_allowed:
        print("  CONTINUE, but only on closure-critical tasks.")
        print("  Guardrail: every next task must map to one live F0 bridge above.")
        print("  If a proposed task does not retire one of them, treat it as theory")
        print("  for theory's sake and reject/pivot.")
        print()
        print("  Recommended immediate targets (in priority order):")
        print("  1. Derive physical transition ray tau from action dynamics.")
        print("  2. Derive admissible epsilon-kernel class from full CHO action.")
        print("  3. Only then revisit eps0 status promotion GEOMETRIC->DERIVED.")
    else:
        print("  PIVOT: F0 closure path is not currently actionable.")
        print("  Recommended non-theory tracks:")
        print("  1. Falsification pressure: neutrino-floor / future tests.")
        print("  2. Submission packaging: paper-quality theorem ledger and claims matrix.")

    print()
    # PASS means decision computed cleanly.
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
