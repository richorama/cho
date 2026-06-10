"""
F4-BREAKING ACTION ORIGIN GATE -- does the seed spectrum become dynamical?
============================================================================

Why this module exists
----------------------
`f4_breaking_seed_op2.py` localized the CONTENT half of pi/432. The linear height

    V_A(P) = Tr(P o A),   P in OP^2 = F4/Spin(9),

has the three generation idempotents as critical points whenever `A` is diagonal
in the generation frame. That evades the `berry_sigma_model_op2.py` no-go, but it
does not derive the seed magnitudes: the critical values are just `spec(A)`.

This gate attacks exactly that remaining point. It asks whether the currently
available OP^2 height dynamics and the natural entropy/free-energy completion can
turn the spectrum of `A` into an output instead of an input.

The answer is a precise negative / localization:

* The height dynamics fixes the FRAME but leaves a continuous modulus. For every
  ratio `r`, the whole family

      A(r) = E1 + r E2 + r^2 E3

  has the same generation critical set and the same qualitative ascent dynamics.
  Only the values change. Thus `r = eps0` is not selected by the OP^2 height
  action; choosing it inserts the scale.
* The entropy/free-energy completion gives the same obstruction in thermodynamic
  language. Maximising entropy with grade energy (0,1,2) gives Gibbs ratios
  `(1, exp(-beta), exp(-2 beta))`. Matching `(1, eps0, eps0^2)` requires
  `beta = -log(eps0) = 0.5 log(432/pi)`, but `beta` is a continuous Lagrange
  multiplier. The variational equation gives the cascade form, not the number.

Net effect
----------
The live bridge is narrowed from "derive the F4-breaking action" to a single
scalar selection problem: derive the inverse-temperature / spurion-spectrum
modulus `beta = 0.5 log(432/pi)` (equivalently `r = eps0`) from CHO dynamics.
Until that happens, pi/432 remains an inserted geometric scale, not an earned
dynamical output. No Bayes credit moves.

No scipy. Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_action_origin_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from epsilon_orbit_selection import primitive_idempotents
from f4_breaking_seed_op2 import (
    EPS0,
    EPS0_SQ,
    _f4,
    flow_selects_top,
    generations_are_critical,
)


PI = math.pi
TOL_CRIT = 1e-9
TOL_VALUE = 1e-10
TOL_GIBBS = 1e-12
MIN_FLOW_OVERLAP = 0.995


@dataclass(frozen=True)
class SpectrumModulusRow:
    label: str
    r: float
    max_grad: float
    values: tuple[float, float, float]
    target_error: float
    structural_pass: bool


@dataclass(frozen=True)
class FlowRow:
    label: str
    r: float
    selected: tuple[int, ...]
    top: int
    min_overlap: float
    flow_pass: bool


@dataclass(frozen=True)
class GibbsRow:
    label: str
    beta: float
    ratios: tuple[float, float, float]
    stationarity_residual: float
    target_error: float


def cumulative_spurion(r: float) -> np.ndarray:
    """A(r) = E1 + r E2 + r^2 E3 in the generation frame."""
    E1, E2, E3 = primitive_idempotents()
    return E1 + r * E2 + (r * r) * E3


def spectrum_modulus_rows(f4) -> tuple[SpectrumModulusRow, ...]:
    """Same critical set for a continuum of spectra A(r)."""
    candidates = (
        ("target eps0", EPS0),
        ("nearby small", 0.05),
        ("decimal", 0.15),
        ("third", 1.0 / 3.0),
        ("half", 0.5),
    )
    rows = []
    for label, r in candidates:
        A = cumulative_spurion(r)
        grads, values, _spectrum = generations_are_critical(A, f4)
        expected = (1.0, r, r * r)
        max_grad = max(grads)
        max_value_error = max(abs(v - e) for v, e in zip(values, expected))
        structural_pass = max_grad < TOL_CRIT and max_value_error < TOL_VALUE
        rows.append(
            SpectrumModulusRow(
                label=label,
                r=float(r),
                max_grad=float(max_grad),
                values=tuple(float(v) for v in values),
                target_error=abs(r * r - EPS0_SQ),
                structural_pass=structural_pass,
            )
        )
    return tuple(rows)


def flow_rows(f4) -> tuple[FlowRow, ...]:
    """Two different spectra have the same qualitative ascent selection."""
    rows = []
    for label, r in (("target eps0", EPS0), ("third", 1.0 / 3.0)):
        A = cumulative_spurion(r)
        selected, top, min_overlap = flow_selects_top(A, f4, n_starts=2, seed=700)
        flow_pass = all(k == top for k in selected) and min_overlap > MIN_FLOW_OVERLAP
        rows.append(
            FlowRow(
                label=label,
                r=float(r),
                selected=tuple(int(k) for k in selected),
                top=int(top),
                min_overlap=float(min_overlap),
                flow_pass=flow_pass,
            )
        )
    return tuple(rows)


def gibbs_ratios(beta: float) -> tuple[float, float, float]:
    """Unnormalised stationary ratios for entropy + beta * grade energy."""
    return (1.0, math.exp(-beta), math.exp(-2.0 * beta))


def gibbs_stationarity_residual(beta: float) -> float:
    """Check log q_i + beta grade_i is constant at the softmax stationary point."""
    grades = np.array([0.0, 1.0, 2.0])
    raw = np.exp(-beta * grades)
    weights = raw / np.sum(raw)
    lhs = np.log(weights) + beta * grades
    return float(np.max(lhs) - np.min(lhs))


def gibbs_rows() -> tuple[GibbsRow, ...]:
    beta_target = -math.log(EPS0)
    candidates = (
        ("target beta", beta_target),
        ("log 2", math.log(2.0)),
        ("log 3", math.log(3.0)),
        ("unit beta", 1.0),
    )
    rows = []
    for label, beta in candidates:
        ratios = gibbs_ratios(beta)
        rows.append(
            GibbsRow(
                label=label,
                beta=float(beta),
                ratios=tuple(float(x) for x in ratios),
                stationarity_residual=gibbs_stationarity_residual(beta),
                target_error=abs(ratios[2] - EPS0_SQ),
            )
        )
    return tuple(rows)


def main() -> bool:
    f4 = _f4()
    spectrum_rows = spectrum_modulus_rows(f4)
    dyn_rows = flow_rows(f4)
    therm_rows = gibbs_rows()
    beta_target = -math.log(EPS0)

    print("=" * 78)
    print("F4-BREAKING ACTION ORIGIN GATE")
    print("Does the OP2 height/free-energy dynamics derive the spurion spectrum?")
    print("=" * 78)

    print("\n[A] Height dynamics fixes the frame, not the spectral modulus")
    print("    A(r) = E1 + r E2 + r^2 E3")
    for row in spectrum_rows:
        print(
            f"  {row.label:<13} r={row.r:.12f} "
            f"max|grad|={row.max_grad:.2e} values="
            f"({row.values[0]:.6f}, {row.values[1]:.6f}, {row.values[2]:.6f}) "
            f"|r^2-eps0^2|={row.target_error:.3e} pass={row.structural_pass}"
        )
    print("  Every listed r has the same generation critical set; only one r equals eps0.")

    print("\n[B] Qualitative ascent dynamics is also modulus-blind")
    for row in dyn_rows:
        selected = ",".join(str(k + 1) for k in row.selected)
        print(
            f"  {row.label:<13} r={row.r:.12f} selected=({selected}) "
            f"top=E{row.top + 1} min_overlap={row.min_overlap:.4f} pass={row.flow_pass}"
        )

    print("\n[C] Entropy/free-energy completion gives a free beta")
    print("    stationary ratios = (1, exp(-beta), exp(-2 beta))")
    for row in therm_rows:
        print(
            f"  {row.label:<13} beta={row.beta:.12f} ratios="
            f"({row.ratios[0]:.6f}, {row.ratios[1]:.6f}, {row.ratios[2]:.6f}) "
            f"stationarity={row.stationarity_residual:.2e} "
            f"|ratio2-eps0^2|={row.target_error:.3e}"
        )
    print(f"  Matching eps0 requires beta = -log(eps0) = {beta_target:.12f}")
    print("  The variational equation gives the Gibbs form, but not this beta value.")

    print("\n[V] Verdict")
    print("  generation frame / critical set        : DERIVED by the height dynamics")
    print("  three-tier cascade form                : NARROWED to one scalar modulus")
    print("  eps0^2 = pi/432 as dynamical output    : OPEN, not derived here")
    print("  missing object                         : action fixing beta or r=eps0")
    print("  Bayes/scoreboard credit moved          : NO")
    print("=" * 78)

    target_rows = [row for row in spectrum_rows if row.label == "target eps0"]
    non_target_rows = [row for row in spectrum_rows if row.label != "target eps0"]
    assert len(target_rows) == 1
    assert all(row.structural_pass for row in spectrum_rows), "some A(r) lost the generation critical set"
    assert target_rows[0].target_error < TOL_VALUE, "the target row must reproduce eps0^2"
    assert all(row.target_error > 1e-3 for row in non_target_rows), "non-target spectra should miss pi/432 visibly"
    assert all(row.flow_pass for row in dyn_rows), "qualitative ascent selection should not depend on r"
    assert all(row.stationarity_residual < TOL_GIBBS for row in therm_rows), "Gibbs stationarity failed"
    assert abs(math.exp(-2.0 * beta_target) - EPS0_SQ) < 1e-15
    # Honest-scope tripwire: this gate narrows the modulus but does not derive it.
    derived_scale = False
    assert not derived_scale, "this gate must not promote eps0^2 to a dynamical output"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)