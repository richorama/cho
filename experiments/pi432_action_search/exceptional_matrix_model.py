"""Second-wave probe: exceptional matrix-model route."""

from __future__ import annotations

from dataclasses import dataclass



@dataclass(frozen=True)
class PotentialClass:
    name: str
    f4_invariant: bool
    has_external_source: bool
    verdict: str


CLASSES = (
    PotentialClass(
        "pure trace/Jordan invariant potential",
        f4_invariant=True,
        has_external_source=False,
        verdict="killed on OP2: invariant potentials are flat on the rank-one orbit",
    ),
    PotentialClass(
        "source-deformed matrix model Tr(P o A)",
        f4_invariant=False,
        has_external_source=True,
        verdict="gets direction but imports A and its spectrum",
    ),
    PotentialClass(
        "dynamical auxiliary-field matrix model",
        f4_invariant=False,
        has_external_source=False,
        verdict="live only if integrating out the auxiliary field derives A and pi/432",
    ),
)


def main() -> bool:
    print("[A] Matrix-model classes")
    for item in CLASSES:
        print(f"  {item.name}")
        print(f"    F4 invariant     : {item.f4_invariant}")
        print(f"    external source  : {item.has_external_source}")
        print(f"    verdict          : {item.verdict}")

    print("\n[B] Required next theorem")
    print("  Build a J3(O)/Freudenthal matrix integral where the saddle generates")
    print("  the F4-breaking auxiliary field and its eigenvalues. If the model needs")
    print("  A as a source, it is just the existing spurion route in disguise.")

    print("\n[V] Sandbox verdict")
    print("  pure invariant matrix model: KILLED")
    print("  auxiliary-field matrix model: OPEN")

    assert any(not item.f4_invariant and not item.has_external_source for item in CLASSES)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
