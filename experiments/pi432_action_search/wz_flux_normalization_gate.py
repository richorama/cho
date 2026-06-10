"""WZ/Schur flux-normalization gate for Phi = pi/432.

This probe isolates the remaining coefficient assumption in the candidate action.
It does not discover a new number; it states the exact conditional derivation:

    minimal WZ/Berry half-flux = pi
    Schur carrier dimension    = 16 * 27 = 432
    flux density Phi           = pi / 432

The hard theorem is still to show that the CHO/Jordan action really normalizes
the WZ term by the full `Delta_9 x J3(O)` carrier, rather than by a chosen trace.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import pi


SPIN9_SPINOR_DIM = 16
J3O_DIM = 27
CARRIER_DIM = SPIN9_SPINOR_DIM * J3O_DIM
SCHUR_WEIGHT = Fraction(1, CARRIER_DIM)
PHI = pi * float(SCHUR_WEIGHT)


@dataclass(frozen=True)
class FluxInput:
    name: str
    value: str
    status: str


INPUTS = (
    FluxInput(
        "minimal OP2 transition WZ/Berry half-flux",
        "pi",
        "geometric input from existing Berry/OP2 probes",
    ),
    FluxInput(
        "Spin(9) spinor carrier",
        str(SPIN9_SPINOR_DIM),
        "Schur irreducible weight 1/16",
    ),
    FluxInput(
        "J3(O) / E6 carrier",
        str(J3O_DIM),
        "Schur/cubic-norm weight 1/27",
    ),
)


def main() -> bool:
    print("=" * 78)
    print("WZ/SCHUR FLUX NORMALIZATION GATE")
    print("=" * 78)

    print("\n[A] Inputs")
    for item in INPUTS:
        print(f"  {item.name}")
        print(f"    value : {item.value}")
        print(f"    status: {item.status}")

    print("\n[B] Exact coefficient")
    print(f"  carrier dimension       : {SPIN9_SPINOR_DIM} * {J3O_DIM} = {CARRIER_DIM}")
    print(f"  Schur carrier weight    : {SCHUR_WEIGHT}")
    print(f"  flux density Phi        : pi * {SCHUR_WEIGHT} = {PHI:.15f}")

    print("\n[C] What remains unproved")
    print("  This is a conditional normalization gate. To graduate, the action must")
    print("  show that the WZ term is averaged over the full Delta_9 x J3(O) carrier")
    print("  by necessity, not by a trace convention chosen after the fact.")

    print("\n[V] Sandbox verdict")
    print("  Phi = pi/432 from WZ/Schur inputs : CONDITIONALLY DERIVED")
    print("  WZ normalization from action      : OPEN")
    print("=" * 78)

    assert CARRIER_DIM == 432
    assert SCHUR_WEIGHT == Fraction(1, 432)
    assert PHI > 0.0
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
