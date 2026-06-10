"""Probe 3: Jordan / nonassociative spectral-action route for pi/432.

The finite associative spectral-action heat-kernel route is killed because its
finite moments are rational. This probe asks what a viable replacement must look
like: it must contain an essential period/WZ term, a Schur carrier measure, and an
F4-breaking seed functional.

This is a structural gate, not a derivation.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


@dataclass(frozen=True)
class Term:
    name: str
    supplies_period_pi: bool
    supplies_schur_432: bool
    breaks_f4_for_seed: bool
    killed_as_direct_source: bool
    note: str


TERMS = (
    Term(
        "finite rational spectral moments",
        supplies_period_pi=False,
        supplies_schur_432=False,
        breaks_f4_for_seed=False,
        killed_as_direct_source=True,
        note="killed as a direct source of pi/432: finite moments are rational",
    ),
    Term(
        "Berry/WZ period on OP^2 transition sphere",
        supplies_period_pi=True,
        supplies_schur_432=False,
        breaks_f4_for_seed=False,
        killed_as_direct_source=False,
        note="supplies the bare pi as a period/flux, not as a rational moment",
    ),
    Term(
        "Schur carrier measure Delta_9 x J3(O)",
        supplies_period_pi=False,
        supplies_schur_432=True,
        breaks_f4_for_seed=False,
        killed_as_direct_source=False,
        note="supplies 1/(16*27) once the carrier is selected",
    ),
    Term(
        "F4-breaking Jordan seed functional",
        supplies_period_pi=False,
        supplies_schur_432=False,
        breaks_f4_for_seed=True,
        killed_as_direct_source=False,
        note="must make the seed spectrum stationary rather than spec(A) input",
    ),
)


def viable_templates() -> list[tuple[Term, ...]]:
    templates = []
    live_terms = [term for term in TERMS if not term.killed_as_direct_source]
    for width in range(1, len(live_terms) + 1):
        for combo in combinations(live_terms, width):
            if not any(term.supplies_period_pi for term in combo):
                continue
            if not any(term.supplies_schur_432 for term in combo):
                continue
            if not any(term.breaks_f4_for_seed for term in combo):
                continue
            templates.append(combo)
    return templates


def main() -> bool:
    templates = viable_templates()
    minimal = min(len(template) for template in templates)
    minimal_templates = [template for template in templates if len(template) == minimal]

    print("[A] Associative spectral-action route")
    killed = [term for term in TERMS if term.killed_as_direct_source]
    for term in killed:
        print(f"  killed: {term.name}")
        print(f"    {term.note}")

    print("\n[B] Minimal live nonassociative/Jordan template")
    for template in minimal_templates:
        print("  template:")
        for term in template:
            print(f"    - {term.name}")
            print(f"      {term.note}")

    print("\n[C] Required next theorem")
    print("  Define a Jordan/nonassociative action where the WZ period term is")
    print("  intrinsic, the Schur carrier is selected by the variational problem, and")
    print("  the F4-breaking seed functional has stationary eigenvalues rather than")
    print("  hand-inserted spec(A).")

    print("\n[V] Sandbox verdict")
    print("  rational spectral-action route: KILLED")
    print("  Jordan/WZ/F4-breaking template gate: PASS")
    print("  derivation: OPEN")

    assert templates, "no viable Jordan/nonassociative template found"
    assert minimal == 3, "the minimal viable template should need period, measure, and seed terms"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
