"""Second-wave probe: exceptional Chern-Simons / higher-gauge route.

This route asks whether pi/432 can be a quantized topological-action coefficient
coming from exceptional group data rather than a finite spectral moment.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations


TARGET = 432


@dataclass(frozen=True)
class Datum:
    label: str
    value: int
    kind: str


DATA = (
    Datum("rank F4", 4, "rank"),
    Datum("dim H", 4, "division algebra dimension"),
    Datum("hvee Spin9", 7, "dual Coxeter number"),
    Datum("dim O", 8, "division algebra dimension"),
    Datum("hvee F4", 9, "dual Coxeter number"),
    Datum("hvee E6", 12, "dual Coxeter number"),
    Datum("dim Delta9", 16, "carrier dimension"),
    Datum("dim J3O", 27, "carrier dimension"),
    Datum("dim F4", 52, "group dimension"),
    Datum("dim E6", 78, "group dimension"),
)


def product(combo: tuple[Datum, ...]) -> int:
    out = 1
    for item in combo:
        out *= item.value
    return out


def exact_channels() -> list[tuple[Datum, ...]]:
    hits = []
    for width in (2, 3):
        for combo in combinations(DATA, width):
            if product(combo) == TARGET:
                hits.append(combo)
    return hits


def main() -> bool:
    channels = exact_channels()
    print("[A] Exceptional topological coefficient channels")
    for combo in channels:
        pieces = " * ".join(f"{item.label}={item.value}" for item in combo)
        kinds = "; ".join(f"{item.label}: {item.kind}" for item in combo)
        print(f"  {pieces} -> {product(combo)}")
        print(f"    {kinds}")

    print("\n[B] What would solve it")
    print("  Find an actual exceptional Chern-Simons / higher-gauge action whose")
    print("  quantized level is 1 and whose normalization selects one of these 432")
    print("  channels. Then show its boundary variation generates the F4-breaking")
    print("  seed term rather than taking the seed as a source.")

    print("\n[V] Sandbox verdict")
    print("  exact exceptional channels: PASS")
    print("  actual topological action: OPEN")

    assert Fraction(1, TARGET) == Fraction(1, 432)
    assert channels, "no exact exceptional 432 channels found"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
