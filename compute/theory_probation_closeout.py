"""
THEORY PROBATION CLOSEOUT - durable math kept, physics claim on probation.
============================================================================

This is a governance reporter, not a derivation. It records the current scientific
decision after the theorem-level math survived and the Standard-Model-constant
program failed to earn its dynamical action.

Durable core (keep and polish)
------------------------------
The math that survives independently of the physics claim is the durable core:

* `PAPER_JORDAN_THEOREMS.md` / `jordan_standalone_theorems`: the decoupled J3(O)
  theorem package.
* `three_generations_frame`: the J3(O) idempotent-frame / OP^2 count-and-chirality
  result.
* `epsilon_measure_schur`: Schur-forced weights 1/16 and 1/27.
* `generation_cascade`: the Freudenthal cubic / Vieta seesaw structure.
* `berry_sigma_model_op2`, `berry_pi_intrinsic_op2`, `f4_breaking_seed_op2`:
  OP^2 / Berry geometry and the F4-breaking direction result.

Physics claim (probation)
-------------------------
The SM-constant program is on probation. The only internal route worth more time is
the route named by `f0_sigma_model_closeout.py`:

    derive an F4-breaking dynamical action whose flux gives pi/432 and whose
    spectrum gives the seed.

If that action cannot be derived without inserting the scale/seed by hand, the
program should be demoted to beautiful algebraic numerology with strong structure,
not described as a theory of nature.

Inactive proof routes
---------------------
The negative artifacts are preserved as guardrails, but they are no longer active
proof routes: heat-kernel a4/a2, topological theta, single RG matching scale, big
bets / outside routes, and additional invariance or normalized-trace witnesses.

No scipy. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/theory_probation_closeout.py
"""

from __future__ import annotations

from dataclasses import dataclass

import audit_contract
import scoreboard


LNB_FLOOR = -3.2
LNB_TOL = 0.25


@dataclass(frozen=True)
class CoreItem:
    name: str
    artifact: str
    keep_reason: str


@dataclass(frozen=True)
class InactiveRoute:
    name: str
    artifact: str
    reason_inactive: str


DURABLE_CORE = (
    CoreItem(
        "standalone J3(O) theorem package",
        "jordan_standalone_theorems",
        "decoupled pure math: inner frame S3, Schur weights, Freudenthal seesaw",
    ),
    CoreItem(
        "J3(O) idempotent-frame generations",
        "three_generations_frame",
        "count-and-chirality route via three F4-equivalent OP^2 idempotents",
    ),
    CoreItem(
        "Schur weights 1/16 and 1/27",
        "epsilon_measure_schur",
        "irreducibility forces the flat measure weights; F4 control stays honest",
    ),
    CoreItem(
        "Freudenthal cubic seesaw",
        "generation_cascade",
        "Vieta turns the cubic norm into the light-pair seesaw relation",
    ),
    CoreItem(
        "OP^2 / Berry geometry",
        "berry_sigma_model_op2",
        "topological kinetic pi survives while the seed-selection no-go stays explicit",
    ),
    CoreItem(
        "intrinsic OP^2 Berry pi",
        "berry_pi_intrinsic_op2",
        "the pi is F4-intrinsic and tied to orthogonal idempotents, not a slice artifact",
    ),
    CoreItem(
        "F4-breaking seed direction",
        "f4_breaking_seed_op2",
        "the rank-one spurion gives the critical-point direction, but not magnitudes",
    ),
)


INACTIVE_ROUTES = (
    InactiveRoute(
        "heat-kernel a4/a2 route",
        "f0_spectral_action_heatkernel",
        "finite spectral moments are rational and miss pi/432 structurally",
    ),
    InactiveRoute(
        "topological theta route",
        "f0_theta_reality_gate",
        "KO-6 data force theta = 0 in the natural finite-triple channels",
    ),
    InactiveRoute(
        "single RG matching scale",
        "rg_scale_derivation",
        "the two electroweak boundaries require scales separated by about 1.8e4",
    ),
    InactiveRoute(
        "outside big-bets routes",
        "big_bets_closeout",
        "six external directions supply FORM but not CHO CONTENT; no credit moved",
    ),
    InactiveRoute(
        "more internal invariance witnesses",
        "gold_standard_closeout",
        "the internal program already localises to one missing action; more witnesses are the treadmill",
    ),
)


ACTIVE_ROUTE = (
    "derive an F4-breaking dynamical action whose flux gives pi/432 and whose "
    "spectrum gives the seed"
)

DEMOTION_IF_FAILS = (
    "beautiful algebraic numerology with strong structure, not a theory of nature"
)


def _contract(name: str) -> audit_contract.AuditContract:
    return audit_contract.CONTRACTS[name]


def contracts_present(names: tuple[str, ...]) -> bool:
    return all(name in audit_contract.CONTRACTS for name in names)


def scoreboard_floor() -> float:
    """Today's EARNED ln B floor from the source-of-truth scoreboard."""
    _gain, _n, _n_eff, rows = scoreboard.scoreboard(F=3.0)
    for label, _k, ln_b in rows:
        if "closed theorems" in label:
            return float(ln_b)
    raise KeyError("closed-theorem floor row not found in scoreboard")


def durable_core_present() -> bool:
    return contracts_present(tuple(item.artifact for item in DURABLE_CORE))


def inactive_routes_guarded() -> bool:
    for route in INACTIVE_ROUTES:
        c = _contract(route.artifact)
        if c.status not in {
            audit_contract.STATUS_OPEN_BRIDGE,
            audit_contract.STATUS_EXPLORATORY,
        }:
            return False
        if not c.kill_conditions:
            return False
    return True


def active_route_on_probation() -> bool:
    c = _contract("f0_sigma_model_closeout")
    text = " ".join((c.public_claim_policy, *c.open_bridges, *c.kill_conditions))
    return (
        c.status == audit_contract.STATUS_EXPLORATORY
        and c.verdict == audit_contract.VERDICT_OPEN
        and "F4-BREAKING" in text
        and "pi/432" in text
        and "spectrum" in text
    )


def _print_rows(title: str, rows) -> None:
    print(f"\n{title}")
    for row in rows:
        print(f"  - {row.name}")
        print(f"    artifact : {row.artifact}")
        field = getattr(row, "keep_reason", None) or getattr(row, "reason_inactive")
        print(f"    reason   : {field}")


def main() -> bool:
    print("=" * 78)
    print("THEORY PROBATION CLOSEOUT: durable math kept, physics claim on probation")
    print("=" * 78)

    _print_rows("[A] DURABLE CORE -- keep and polish", DURABLE_CORE)
    _print_rows("[B] INACTIVE PROOF ROUTES -- preserve as null records, stop pursuing", INACTIVE_ROUTES)

    print("\n[C] ONLY LIVE INTERNAL ROUTE")
    print(f"  {ACTIVE_ROUTE}")
    print("  Acceptance requires a real dynamical action, not another witness: the")
    print("  action must supply the F4-breaking term, output the flux pi/432, and")
    print("  produce the seed spectrum without inserting those magnitudes by hand.")

    print("\n[D] DEMOTION RULE")
    print(f"  If that route fails: {DEMOTION_IF_FAILS}.")

    floor = scoreboard_floor()
    print("\n[E] STANDING SCOREBOARD")
    print(f"  earned floor: ln B = {floor:+.1f}")
    print(f"  null still wins on earned credit: {floor < 0.0}")
    print("  This reporter grants no credit; it only guards the probation decision.")

    core_ok = durable_core_present()
    inactive_ok = inactive_routes_guarded()
    active_ok = active_route_on_probation()
    own = _contract("theory_probation_closeout")

    print("\n[V] TRIPWIRES")
    print(f"  durable core contracts present         : {core_ok}")
    print(f"  inactive routes still guarded          : {inactive_ok}")
    print(f"  active F4-breaking route on probation  : {active_ok}")
    print(f"  own contract is diagnostic             : {own.status == audit_contract.STATUS_DIAGNOSTIC}")
    print("=" * 78)

    assert core_ok, "a durable-core contract is missing"
    assert inactive_ok, "an inactive route was silently promoted or lost kill conditions"
    assert active_ok, "the live F4-breaking action route is no longer explicit"
    assert abs(floor - LNB_FLOOR) < LNB_TOL, "closed-theorem floor ln B drifted"
    assert floor < 0.0, "earned floor is no longer negative; update probation deliberately"
    assert own.status == audit_contract.STATUS_DIAGNOSTIC
    assert own.verdict == audit_contract.VERDICT_DIAGNOSTIC
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)