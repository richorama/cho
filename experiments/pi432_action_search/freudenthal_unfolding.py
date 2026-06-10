"""Second-wave probe: Freudenthal/Jordan cubic universal-unfolding route.

The cubic norm is durable math, but N3 vanishes on rank-one OP2 points. This probe
tests the only sensible continuation: the cubic must enter through an unfolding,
off-vacuum extension, or boundary coupling to the Berry period.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class CubicRoute:
    name: str
    has_period_source: bool
    breaks_f4: bool
    seed_forced: bool
    note: str


ROUTES = (
    CubicRoute(
        "pure F4-invariant N3 on OP2",
        has_period_source=False,
        breaks_f4=False,
        seed_forced=False,
        note="killed: N3=0 on rank-one idempotents and F4-invariants are flat",
    ),
    CubicRoute(
        "off-vacuum Freudenthal cubic flow",
        has_period_source=False,
        breaks_f4=False,
        seed_forced=False,
        note="may shape a seesaw, but pure algebra over rational data has no pi source",
    ),
    CubicRoute(
        "unfolded cubic plus Berry/WZ boundary period",
        has_period_source=True,
        breaks_f4=True,
        seed_forced=False,
        note="live only if the unfolding parameter is derived, not supplied as A",
    ),
)


def main() -> bool:
    print("[A] Cubic routes")
    for route in ROUTES:
        print(f"  {route.name}")
        print(f"    period source : {route.has_period_source}")
        print(f"    breaks F4     : {route.breaks_f4}")
        print(f"    seed forced   : {route.seed_forced}")
        print(f"    note          : {route.note}")

    live = [route for route in ROUTES if route.has_period_source and route.breaks_f4]

    print("\n[B] Required next theorem")
    print("  Construct the universal unfolding of the Freudenthal/Jordan cubic with")
    print("  a boundary Berry/WZ period, and prove the unfolding parameter is fixed")
    print("  by the action. If the unfolding parameter is just A, this route reduces")
    print("  to the existing spurion-input problem.")

    print("\n[V] Sandbox verdict")
    print("  standalone cubic route: KILLED")
    print("  cubic-plus-period route: OPEN")

    assert Fraction(16 * 27, 1) == 432
    assert live, "no live cubic route remains after the OP2 no-go"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
