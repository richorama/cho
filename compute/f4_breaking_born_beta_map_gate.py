"""
F4-BREAKING BORN BETA-MAP GATE -- density to amplitude to beta.
=================================================================

The level-one carrier gate selected a WZ half-turn density

    d = pi/432.

The remaining scalar obstruction is the map from that selected density to the
Gibbs/seed ratio

    exp(-beta) = eps0,       exp(-2 beta) = d.

This gate tests the next local bridge: the WZ/Schur object is a probability or
flux density, while the F4-breaking spurion spectrum is an amplitude cascade.
Under the Born square map, the grade-one amplitude is

    r = sqrt(d),             beta = -log r,

and the grade-two probability is r^2 = d. This reproduces eps0 exactly.

What is proved here
-------------------
Given (1) the level-one WZ density from `f4_breaking_level_one_carrier_gate.py`
and (2) the already-audited amplitude/probability dichotomy used in the mixing
sector, the half-log beta map is no longer arbitrary: the unique positive
amplitude whose square is the selected density is eps0.

What is not proved here
-----------------------
This is still not the full CHO variational action. It does not derive from first
principles why the F4-breaking height spectrum must use amplitude coefficients,
nor does it derive the beta stationarity equation dynamically. It closes the
local density-to-amplitude map once the Born interpretation is granted.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_born_beta_map_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from f4_breaking_beta_selection_gate import gibbs_ratios
from f4_breaking_level_one_carrier_gate import carrier_selection
from f4_breaking_primitive_level_gate import CARRIER_DIM, PI, half_turn_density
from f4_breaking_seed_op2 import EPS0, EPS0_SQ


TOL = 1e-14
MISS_TOL = 1e-4


@dataclass(frozen=True)
class BornMapRow:
    label: str
    density: float
    amplitude: float
    beta: float | None
    ratio2: float
    target_error: float
    matches_target: bool
    interpretation: str


@dataclass(frozen=True)
class BornSelection:
    selected_density: float
    selected_amplitude: float
    selected_beta: float
    selected_ratios: tuple[float, float, float]
    density_recovered_from_amplitude: float
    born_map_selects_beta: bool
    beta_variational_principle_derived: bool


def beta_from_amplitude(amplitude: float) -> float | None:
    if not (0.0 < amplitude < 1.0):
        return None
    return -math.log(amplitude)


def born_amplitude(density: float) -> float:
    if density < 0.0:
        raise ValueError("density must be non-negative")
    return math.sqrt(density)


def map_rows() -> tuple[BornMapRow, ...]:
    selected = carrier_selection()
    selected_density = selected.selected_density
    candidates = (
        (
            "level-one density as probability",
            selected_density,
            born_amplitude(selected_density),
            "Born: amplitude is sqrt(density)",
        ),
        (
            "level-one density as amplitude",
            selected_density,
            selected_density,
            "wrong: treats a probability as an amplitude",
        ),
        (
            "state count only as probability",
            1.0 / CARRIER_DIM,
            born_amplitude(1.0 / CARRIER_DIM),
            "wrong: omits Berry/WZ pi flux",
        ),
        (
            "level-two density as probability",
            half_turn_density(2.0),
            born_amplitude(half_turn_density(2.0)),
            "wrong carrier: k=2 is a three-state sector",
        ),
    )
    rows = []
    for label, density, amplitude, interpretation in candidates:
        beta = beta_from_amplitude(amplitude)
        ratio2 = amplitude * amplitude
        rows.append(
            BornMapRow(
                label=label,
                density=float(density),
                amplitude=float(amplitude),
                beta=None if beta is None else float(beta),
                ratio2=float(ratio2),
                target_error=abs(ratio2 - EPS0_SQ),
                matches_target=abs(ratio2 - EPS0_SQ) < TOL,
                interpretation=interpretation,
            )
        )
    return tuple(rows)


def born_selection() -> BornSelection:
    selected = carrier_selection()
    density = selected.selected_density
    amplitude = born_amplitude(density)
    beta = beta_from_amplitude(amplitude)
    assert beta is not None
    ratios = gibbs_ratios(beta)
    return BornSelection(
        selected_density=float(density),
        selected_amplitude=float(amplitude),
        selected_beta=float(beta),
        selected_ratios=tuple(float(x) for x in ratios),
        density_recovered_from_amplitude=float(amplitude * amplitude),
        born_map_selects_beta=True,
        beta_variational_principle_derived=False,
    )


def main() -> bool:
    rows = map_rows()
    selection = born_selection()

    print("=" * 78)
    print("F4-BREAKING BORN BETA-MAP GATE")
    print("Does the selected WZ density determine beta by the Born square map?")
    print("=" * 78)

    print("\n[A] Candidate maps from WZ density to the grade-one seed amplitude")
    for row in rows:
        beta_str = "n/a" if row.beta is None else f"{row.beta:.12f}"
        print(
            f"  {row.label:<34} density={row.density:.12f} "
            f"amp={row.amplitude:.12f} beta={beta_str} "
            f"amp^2={row.ratio2:.12f} |.-target|={row.target_error:.3e} "
            f"match={row.matches_target}"
        )
        print(f"      {row.interpretation}")

    print("\n[B] Selected map")
    print(f"  WZ/carrier density d                      : {selection.selected_density:.15f}")
    print(f"  sqrt(d)                                   : {selection.selected_amplitude:.15f}")
    print(f"  eps0                                      : {EPS0:.15f}")
    print(f"  beta=-log(sqrt(d))                       : {selection.selected_beta:.12f}")
    print(f"  target beta=-log(eps0)                   : {-math.log(EPS0):.12f}")
    print(
        "  Gibbs ratios from beta                    : "
        f"({selection.selected_ratios[0]:.9f}, "
        f"{selection.selected_ratios[1]:.9f}, "
        f"{selection.selected_ratios[2]:.9f})"
    )
    print(f"  recovered density amp^2                  : {selection.density_recovered_from_amplitude:.15f}")
    print(f"  pi/432                                    : {PI / CARRIER_DIM:.15f}")

    print("\n[V] Verdict")
    print("  level-one WZ density selected             : YES")
    print("  Born density -> amplitude map gives eps0  : YES")
    print("  beta = -log(eps0) follows from the map    : YES, conditional")
    print("  beta variational principle derived        : NO")
    print("  remaining object                          : derive the Born-amplitude action coupling")
    print("  Bayes/scoreboard credit moved             : NO")
    print("=" * 78)

    matching = [row for row in rows if row.matches_target]
    misses = [row for row in rows if not row.matches_target]
    assert len(matching) == 1
    assert matching[0].label == "level-one density as probability"
    assert all(row.target_error > MISS_TOL for row in misses)
    assert abs(selection.selected_density - EPS0_SQ) < TOL
    assert abs(selection.selected_amplitude - EPS0) < TOL
    assert abs(selection.selected_beta + math.log(EPS0)) < TOL
    assert abs(selection.density_recovered_from_amplitude - selection.selected_density) < TOL
    assert abs(selection.selected_ratios[1] - EPS0) < TOL
    assert abs(selection.selected_ratios[2] - EPS0_SQ) < TOL
    assert selection.born_map_selects_beta
    assert not selection.beta_variational_principle_derived
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)