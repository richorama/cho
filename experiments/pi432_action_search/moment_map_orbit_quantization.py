"""Probe 1: moment-map / orbit-quantization route for pi/432.

Question:
    Can the denominator 432 be forced as selected quantized carrier data, while
    the numerator pi is the minimal Berry/WZ half-flux?

This does not derive the action. It checks the exact arithmetic target and states
the next mathematical gate for a real moment-map/symplectic-reduction solution.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import itertools


TARGET_DENOMINATOR = 432
MINIMAL_BERRY_HALF_FLUX = "pi"


@dataclass(frozen=True)
class Dimension:
    label: str
    value: int
    role: str


CATALOG = (
    Dimension("generation count", 3, "rank / frame size"),
    Dimension("Im(O)", 7, "Fano imaginary octonions"),
    Dimension("O", 8, "octonion dimension"),
    Dimension("Spin(9) vector", 9, "vector representation"),
    Dimension("OP^1 tangent complement", 10, "rank-one stratum complement"),
    Dimension("G2", 14, "automorphism dimension"),
    Dimension("Delta_9", 16, "Spin(9) real spinor / OP^2 tangent"),
    Dimension("F4 traceless J3(O)", 26, "traceless Albert module"),
    Dimension("J3(O)", 27, "exceptional Jordan algebra / E6 minuscule"),
    Dimension("E6 positive roots", 36, "positive-root count"),
    Dimension("F4", 52, "group dimension"),
    Dimension("E6", 78, "group dimension"),
)


def factor_pairs(target: int, dims: tuple[Dimension, ...]) -> list[tuple[Dimension, Dimension]]:
    pairs = []
    for left, right in itertools.combinations(dims, 2):
        if left.value * right.value == target:
            pairs.append((left, right))
    return pairs


def coefficient_from_flux_and_carrier(carrier_dim: int) -> Fraction:
    return Fraction(1, carrier_dim)


def main() -> bool:
    pairs = factor_pairs(TARGET_DENOMINATOR, CATALOG)
    expected = {tuple(sorted((left.label, right.label))) for left, right in pairs}
    wanted = tuple(sorted(("Delta_9", "J3(O)")))

    print("[A] Exact carrier arithmetic")
    print(f"  target denominator: {TARGET_DENOMINATOR}")
    for left, right in pairs:
        print(f"  exact pair: {left.label} ({left.value}) * {right.label} ({right.value})")
        print(f"    roles: {left.role}; {right.role}")

    weight = coefficient_from_flux_and_carrier(TARGET_DENOMINATOR)
    print("\n[B] Candidate period/measure form")
    print(f"  minimal Berry/WZ half-flux: {MINIMAL_BERRY_HALF_FLUX}")
    print(f"  carrier weight           : {weight}")
    print("  target coefficient       : pi/432")

    print("\n[C] Required next theorem")
    print("  Construct a moment-map or symplectic-reduction action that selects")
    print("  Delta_9 x J3(O), fixes WZ level 1, and makes the F4-breaking seed")
    print("  spectrum stationary rather than inserted.")

    print("\n[V] Sandbox verdict")
    print("  arithmetic gate: PASS")
    print("  derivation: OPEN")

    assert wanted in expected, "Delta_9 x J3(O) is not an exact 432 factorization"
    assert len(pairs) == 1, "432 is not unique in the current CHO dimension catalog"
    assert weight == Fraction(1, 432)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
