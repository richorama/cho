"""Action-origin unification gate for the boundary CHO/Jordan/WZ candidate.

The previous sandbox gates closed separate rungs:

* boundary variation forces an unordered orthogonal primitive pair;
* oriented WZ action supplies the boundary sign/order;
* WZ filling independence quantizes the coefficient to integer level;
* Schur carrier normalization gives `pi/432` once the carrier is fixed;
* Peirce grading plus entropy variation gives `(1, sqrt(Phi), Phi)`.

This gate asks the next, stricter question:

    do these ingredients already amount to one derived CHO action?

Answer: no. They assemble into one coherent effective boundary action, but the
origin of the terms is still imported. The point of this file is to make that
boundary precise and regression-guarded.

Schematic effective action tested here
-------------------------------------
For primitive endpoints P,Q in OP2, ordered WZ boundary orientation, integer
level k, completed frame grades N=(0,1,2), and seed probabilities rho,

    S_eff = B(P,Q) + (k/2) Omega(P -> Q)
          + sum_i rho_i log rho_i + Delta sum_i i rho_i,

where B(P,Q)=Tr(P o Q), Delta=-1/2 log(Phi), Phi=pi/(16*27).

The gate verifies that this assembled action reproduces the current sandbox
outputs and then asserts that the origin theorem is still OPEN.

No scipy. Reuses nearby sandbox gates as source-of-truth witnesses.
Run:
    PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/action_origin_unification_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from boundary_variation_gate import f4_basis, flow_trials
from oriented_wz_boundary_gate import oriented_boundary_frame, oriented_wz_action
from unified_boundary_wz_jordan_action import (
    CARRIER_DIM,
    DELTA,
    GRADES,
    PHI,
    free_energy,
    seed_distribution,
    seed_weights,
    stationarity_residuals,
)
from wz_level_integrality_gate import is_single_valued, normalized_density, primitive_level


PI = math.pi
TOL_EXACT = 1e-12
TOL_FLOW = 1e-8


@dataclass(frozen=True)
class OriginRow:
    ingredient: str
    verified_output: str
    residual: float | None
    action_origin_status: str


def boundary_variation_summary() -> tuple[float, float, bool]:
    row = flow_trials(f4_basis(), seeds=(42,))[0]
    completion_residual = max(
        row.completion_idempotent_residual,
        row.completion_trace_residual,
        row.completion_pair_overlap,
    )
    return row.final_overlap, completion_residual, row.monotone


def level_and_flux_summary() -> tuple[int, float, bool, bool]:
    primitive = abs(primitive_level())
    density = normalized_density(primitive)
    integer_ok = is_single_valued(float(primitive))
    noninteger_killed = not is_single_valued(0.5)
    return primitive, density, integer_ok, noninteger_killed


def seed_summary() -> tuple[tuple[float, float, float], tuple[float, float, float], float]:
    rho = seed_distribution()
    residuals = stationarity_residuals(rho)
    ratios = (1.0, rho[1] / rho[0], rho[2] / rho[0])
    stationarity = max(abs(value) for value in residuals)
    return rho, ratios, stationarity


def origin_rows() -> tuple[OriginRow, ...]:
    final_overlap, completion, monotone = boundary_variation_summary()
    frame = oriented_boundary_frame()
    primitive, density, integer_ok, noninteger_killed = level_and_flux_summary()
    rho, ratios, stationarity = seed_summary()
    target = (1.0, math.sqrt(PHI), PHI)
    ratio_residual = max(abs(a - b) for a, b in zip(ratios, target))

    rows = (
        OriginRow(
            "endpoint contrast term B(P,Q)",
            f"orthogonal endpoints, final B={final_overlap:.3e}, monotone={monotone}",
            max(final_overlap, completion),
            "OPEN/NARROWED: overlap is the canonical F4 two-point contrast; derive why CHO dynamics uses it",
        ),
        OriginRow(
            "oriented WZ boundary term",
            f"S_WZ(pi/2,+)={oriented_wz_action(PI / 2.0, +1):.12f}; grades={frame['forward_grades']}",
            abs(oriented_wz_action(PI / 2.0, +1) - PI),
            "OPEN/NARROWED: primitive CP1 WZ chain supplies orientation; derive why CHO dynamics uses it",
        ),
        OriginRow(
            "WZ level/integrality",
            f"integer k={primitive} passes={integer_ok}; k=1/2 killed={noninteger_killed}",
            abs(density - PI / 432.0),
            "OPEN/NARROWED: level one is primitive c1=1 sector; derive why CHO selects it dynamically",
        ),
        OriginRow(
            "Schur carrier normalization",
            f"carrier dim={CARRIER_DIM}; Phi={PHI:.15f}",
            abs(CARRIER_DIM - 432),
            "OPEN: derive the Delta_9 x J3(O) carrier from the action",
        ),
        OriginRow(
            "Peirce entropy/free energy",
            f"grades={GRADES}; ratios=({ratios[0]:.1f}, {ratios[1]:.12f}, {ratios[2]:.12f})",
            max(stationarity, ratio_residual),
            "OPEN: derive the large-deviation/free-energy principle from CHO",
        ),
    )

    # Keep the local variables live in a way that catches accidental import drift.
    assert rho[0] > rho[1] > rho[2]
    return rows


def open_obligations(rows: tuple[OriginRow, ...]) -> tuple[str, ...]:
    return tuple(row.action_origin_status for row in rows if row.action_origin_status.startswith("OPEN"))


def effective_action_value() -> float:
    rho = seed_distribution()
    # At the variational endpoint B=0. The oriented WZ term is topological and
    # the entropy term is evaluated at its stationary distribution.
    boundary_minimum = 0.0
    wz_half_turn = oriented_wz_action(PI / 2.0, +1)
    seed_free_energy = free_energy(rho)
    return boundary_minimum + wz_half_turn + seed_free_energy


def main() -> bool:
    rows = origin_rows()
    obligations = open_obligations(rows)
    weights = seed_weights()
    action_value = effective_action_value()

    print("=" * 78)
    print("ACTION-ORIGIN UNIFICATION GATE")
    print("=" * 78)

    print("\n[A] Assembled effective action")
    print("  S_eff = B(P,Q) + (k/2)Omega(P->Q) + sum rho log rho + Delta sum i rho_i")
    print("  B(P,Q)=Tr(P o Q), k=1, Delta=-1/2 log(Phi), Phi=pi/(16*27)")
    print(f"  carrier dimension       : {CARRIER_DIM}")
    print(f"  Phi                     : {PHI:.15f}")
    print(f"  Delta                   : {DELTA:.15f}")
    print(f"  stationary weights      : {weights}")
    print(f"  schematic S_eff at gate : {action_value:.15f}")

    print("\n[B] Ingredient-origin ledger")
    for row in rows:
        residual = "n/a" if row.residual is None else f"{row.residual:.3e}"
        print(f"  {row.ingredient}")
        print(f"    output   : {row.verified_output}")
        print(f"    residual : {residual}")
        print(f"    status   : {row.action_origin_status}")

    print("\n[C] What this closes")
    print("  The current gates are mutually compatible as one effective boundary")
    print("  CHO/Jordan/WZ free-energy action. Orthogonality, orientation, integer")
    print("  level, carrier density, Peirce grades, and Gibbs ratios all fit together.")

    print("\n[D] What this refuses to overclaim")
    print("  The action-origin theorem is still absent. The assembled functional uses")
    print("  imported terms whose variational consequences are good, but whose CHO")
    print("  origin has not been derived.")
    print(f"  open origin obligations : {len(obligations)}")
    for obligation in obligations:
        print(f"    - {obligation}")

    print("\n[V] Sandbox verdict")
    print("  single effective boundary action assembly : PASS")
    print("  full action-origin derivation             : OPEN")
    print("  next theorem                              : derive the F4-breaking")
    print("                                             oriented level-one boundary")
    print("                                             action from CHO dynamics")
    print("=" * 78)

    assert CARRIER_DIM == 432
    assert abs(PHI - PI / 432.0) < TOL_EXACT
    assert all(row.residual is not None and row.residual < TOL_FLOW for row in rows)
    assert len(obligations) == 5
    assert any("two-point contrast" in obligation for obligation in obligations)
    assert any("primitive CP1 WZ" in obligation for obligation in obligations)
    assert any("primitive c1=1" in obligation for obligation in obligations)
    assert any("carrier" in obligation for obligation in obligations)
    assert any("free-energy" in obligation for obligation in obligations)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)