"""Probe 2: anomaly / WZ / inflow route for pi/432.

The finite KO-theta route is killed. This probe is different: it asks whether a
boundary Wess-Zumino or anomaly-inflow normalization has exact channels whose
denominator is 432 and whose level can be 1.

Passing this file does not prove an anomaly. It identifies exact channels worth
trying to realize as a descent/anomaly-polynomial calculation.
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools


TARGET_DENOMINATOR = 432


@dataclass(frozen=True)
class Factor:
    label: str
    value: int
    kind: str


FACTORS = (
    Factor("dim H", 4, "division-algebra dimension"),
    Factor("rank F4", 4, "rank"),
    Factor("hvee Spin(9)", 7, "dual Coxeter number"),
    Factor("dim O", 8, "division-algebra dimension"),
    Factor("hvee F4", 9, "dual Coxeter number"),
    Factor("hvee E6", 12, "dual Coxeter number"),
    Factor("dim Delta_9", 16, "carrier dimension"),
    Factor("dim J3(O)", 27, "carrier dimension"),
    Factor("dim F4", 52, "group dimension"),
    Factor("dim E6", 78, "group dimension"),
)


def exact_channels(max_width: int = 3) -> list[tuple[Factor, ...]]:
    found = []
    for width in range(2, max_width + 1):
        for combo in itertools.combinations(FACTORS, width):
            product = 1
            for factor in combo:
                product *= factor.value
            if product == TARGET_DENOMINATOR:
                found.append(combo)
    return found


def labels(combo: tuple[Factor, ...]) -> tuple[str, ...]:
    return tuple(factor.label for factor in combo)


def main() -> bool:
    channels = exact_channels()
    label_sets = {labels(combo) for combo in channels}

    print("[A] Killed route explicitly excluded")
    print("  finite KO theta: killed in core; do not restart it here")
    print("  this probe: WZ/anomaly/inflow normalization, a broader topological route")

    print("\n[B] Exact denominator channels")
    for combo in channels:
        product = 1
        for factor in combo:
            product *= factor.value
        joined = " * ".join(f"{factor.label}={factor.value}" for factor in combo)
        kinds = "; ".join(f"{factor.label}: {factor.kind}" for factor in combo)
        print(f"  {joined} -> {product}")
        print(f"    {kinds}")

    print("\n[C] Required next theorem")
    print("  Build a genuine descent/inflow calculation selecting one exact channel")
    print("  with integer level 1. Without the anomaly polynomial or boundary WZ term,")
    print("  these are only arithmetic targets.")

    print("\n[V] Sandbox verdict")
    print("  exact-channel gate: PASS")
    print("  anomaly derivation: OPEN")

    assert ("dim Delta_9", "dim J3(O)") in label_sets
    assert ("dim H", "hvee F4", "hvee E6") in label_sets
    assert channels, "no exact WZ/anomaly denominator channels found"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
