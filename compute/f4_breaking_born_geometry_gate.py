"""
F4-BREAKING PROJECTIVE BORN GEOMETRY GATE -- why density squares to amplitude.
=============================================================================

The previous gate, `f4_breaking_born_beta_map_gate.py`, used the Born square map

    density d = pi/432,      amplitude r = sqrt(d),      beta = -log(r).

That closed the local half-log bridge once the amplitude/probability
interpretation was granted. This gate hardens that granted step geometrically.

On the rank-one projector geometry underlying CP^1 ⊂ OP^2,

    P = |psi><psi|,   Q = |phi><phi|,   Tr(P o Q) = |<psi|phi>|^2.

So the trace overlap is a probability density on an orthogonal idempotent frame,
and the projective amplitude is necessarily its square root. The selected
level-one WZ/carrier density d=pi/432 can therefore be realised as a transition
probability whose amplitude is eps0.

What this proves
----------------
Given the OP^2 rank-one projector geometry, the density-to-amplitude square root
is not an arbitrary algebraic trick: it is the projective/Born law for primitive
idempotents, and it is F4-invariant after transporting the CP^1 transition pair
into genuinely octonionic directions.

What this still does not prove
------------------------------
This gate does not derive the CHO action coupling that makes the selected WZ
density enter this projective transition channel. It also does not derive the
beta stationarity equation dynamically. It removes/hardens the local Born
geometry assumption, but the action-coupling bridge remains open.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_born_geometry_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from berry_pi_intrinsic_op2 import _embed
from epsilon_action_selection import (
    cubic_norm,
    jordan_product,
    random_automorphism,
    trace_form,
    _f4_basis,
)
from epsilon_orbit_selection import primitive_idempotents
from f4_breaking_born_beta_map_gate import beta_from_amplitude, born_selection
from f4_breaking_seed_op2 import EPS0, EPS0_SQ


PI = math.pi
TOL_TRACE = 1e-12
TOL_F4 = 1e-9
MISS_TOL = 1e-3
MIN_OCTONIONIC = 0.05


@dataclass(frozen=True)
class ProjectiveBornRow:
    label: str
    amplitude: float
    separation_angle: float
    inner_amplitude: float
    trace_density: float
    sqrt_trace: float
    trace_error: float
    born_error: float


@dataclass(frozen=True)
class FrameProbabilityWitness:
    amplitudes: tuple[float, float, float]
    probabilities: tuple[float, float, float]
    probability_sum: float
    max_component_error: float
    target_probability: float
    target_amplitude: float


@dataclass(frozen=True)
class F4InvarianceWitness:
    base_density: float
    max_density_error: float
    max_idempotent_error: float
    max_rank_error: float
    min_octonionic_support: float


@dataclass(frozen=True)
class InterpretationRow:
    label: str
    amplitude: float
    beta: float | None
    ratio2: float
    target_error: float
    matches_target: bool
    interpretation: str


def coherent_pair(amplitude: float) -> tuple[np.ndarray, np.ndarray]:
    if not (0.0 <= amplitude <= 1.0):
        raise ValueError("amplitude must lie in [0, 1]")
    psi = np.array([1.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j])
    phi = np.array(
        [amplitude + 0.0j, math.sqrt(max(0.0, 1.0 - amplitude * amplitude)) + 0.0j, 0.0 + 0.0j]
    )
    return psi, phi


def transition_projectors(amplitude: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    psi, phi = coherent_pair(amplitude)
    return psi, phi, _embed(psi), _embed(phi)


def octonionic_support(p27: np.ndarray) -> float:
    support = 0.0
    for base in (3, 11, 19):
        support = max(support, float(np.max(np.abs(p27[base + 2: base + 8]))))
    return support


def projective_born_rows() -> tuple[ProjectiveBornRow, ...]:
    candidates = (
        ("target eps0", EPS0),
        ("half amplitude", 0.5),
        ("equal superposition", 1.0 / math.sqrt(2.0)),
        ("third amplitude", 1.0 / 3.0),
        ("near diagonal", 0.9),
    )
    rows = []
    for label, amplitude in candidates:
        psi, phi, P, Q = transition_projectors(amplitude)
        inner_amplitude = abs(np.vdot(psi, phi))
        trace_density = trace_form(P, Q)
        sqrt_trace = math.sqrt(max(0.0, trace_density))
        rows.append(
            ProjectiveBornRow(
                label=label,
                amplitude=float(amplitude),
                separation_angle=float(2.0 * math.acos(amplitude)),
                inner_amplitude=float(inner_amplitude),
                trace_density=float(trace_density),
                sqrt_trace=float(sqrt_trace),
                trace_error=abs(trace_density - inner_amplitude * inner_amplitude),
                born_error=abs(sqrt_trace - inner_amplitude),
            )
        )
    return tuple(rows)


def frame_probability_witness(amplitude: float = EPS0) -> FrameProbabilityWitness:
    _psi, phi, _P, Q = transition_projectors(amplitude)
    frame = primitive_idempotents()
    probabilities = tuple(float(trace_form(Q, E)) for E in frame)
    amplitudes = tuple(float(abs(x)) for x in phi)
    max_component_error = max(abs(p - a * a) for p, a in zip(probabilities, amplitudes))
    return FrameProbabilityWitness(
        amplitudes=amplitudes,
        probabilities=probabilities,
        probability_sum=float(sum(probabilities)),
        max_component_error=float(max_component_error),
        target_probability=float(probabilities[0]),
        target_amplitude=float(amplitudes[0]),
    )


def f4_invariance_witness(amplitude: float = EPS0, n_auto: int = 12, seed: int = 20260610) -> F4InvarianceWitness:
    _psi, _phi, P, Q = transition_projectors(amplitude)
    base_density = trace_form(P, Q)
    rng = np.random.default_rng(seed)
    f4 = _f4_basis()
    max_density_error = 0.0
    max_idempotent_error = 0.0
    max_rank_error = 0.0
    min_octonionic = math.inf
    for _ in range(n_auto):
        A = random_automorphism(rng, f4, 0.9)
        PP = A @ P
        QQ = A @ Q
        max_density_error = max(max_density_error, abs(trace_form(PP, QQ) - base_density))
        for R in (PP, QQ):
            max_idempotent_error = max(max_idempotent_error, float(np.linalg.norm(jordan_product(R, R) - R)))
            max_rank_error = max(max_rank_error, abs(cubic_norm(R)))
        min_octonionic = min(min_octonionic, max(octonionic_support(PP), octonionic_support(QQ)))
    return F4InvarianceWitness(
        base_density=float(base_density),
        max_density_error=float(max_density_error),
        max_idempotent_error=float(max_idempotent_error),
        max_rank_error=float(max_rank_error),
        min_octonionic_support=float(min_octonionic),
    )


def interpretation_rows() -> tuple[InterpretationRow, ...]:
    selected = born_selection()
    density = selected.selected_density
    amplitude = math.sqrt(density)
    theta = 2.0 * math.acos(amplitude)
    candidates = (
        (
            "projector trace as probability",
            amplitude,
            "forced by Tr(P o Q)=|<psi|phi>|^2",
        ),
        (
            "projector trace as amplitude",
            density,
            "wrong: uses the probability itself as the amplitude",
        ),
        (
            "state-count probability",
            math.sqrt(1.0 / 432.0),
            "wrong: omits the Berry/WZ pi in the selected density",
        ),
        (
            "angle fraction as amplitude",
            theta / PI,
            "wrong: projective distance is not the transition amplitude",
        ),
    )
    rows = []
    for label, candidate_amplitude, interpretation in candidates:
        beta = beta_from_amplitude(candidate_amplitude)
        ratio2 = candidate_amplitude * candidate_amplitude
        rows.append(
            InterpretationRow(
                label=label,
                amplitude=float(candidate_amplitude),
                beta=None if beta is None else float(beta),
                ratio2=float(ratio2),
                target_error=abs(ratio2 - EPS0_SQ),
                matches_target=abs(ratio2 - EPS0_SQ) < TOL_TRACE,
                interpretation=interpretation,
            )
        )
    return tuple(rows)


def main() -> bool:
    rows = projective_born_rows()
    frame = frame_probability_witness()
    invariant = f4_invariance_witness()
    interpretations = interpretation_rows()
    selected = born_selection()

    print("=" * 78)
    print("F4-BREAKING PROJECTIVE BORN GEOMETRY GATE")
    print("Does OP2 rank-one geometry force density -> amplitude by a square root?")
    print("=" * 78)

    print("\n[A] Projector trace law on CP^1 inside OP^2")
    for row in rows:
        print(
            f"  {row.label:<19} amp={row.amplitude:.12f} theta={row.separation_angle:.9f} "
            f"Tr(PQ)={row.trace_density:.12f} sqrtTr={row.sqrt_trace:.12f} "
            f"trace_err={row.trace_error:.2e} born_err={row.born_error:.2e}"
        )
    print("  Trace overlap is the transition probability; the amplitude is its square root.")

    print("\n[B] Orthogonal generation frame: trace probabilities add to one")
    print(
        "  amplitudes against (E1,E2,E3)       : "
        f"({frame.amplitudes[0]:.12f}, {frame.amplitudes[1]:.12f}, {frame.amplitudes[2]:.12f})"
    )
    print(
        "  trace probabilities                 : "
        f"({frame.probabilities[0]:.12f}, {frame.probabilities[1]:.12f}, {frame.probabilities[2]:.12f})"
    )
    print(f"  probability sum                     : {frame.probability_sum:.12f}")
    print(f"  max |p_i-|a_i|^2|                  : {frame.max_component_error:.2e}")
    print(f"  target channel probability          : {frame.target_probability:.15f}")
    print(f"  target channel amplitude            : {frame.target_amplitude:.15f}")

    print("\n[C] F4-invariance: the same trace probability survives off the slice")
    print(f"  base density Tr(PQ)                 : {invariant.base_density:.15f}")
    print(f"  max density error after F4 transport: {invariant.max_density_error:.2e}")
    print(f"  max idempotent error after transport: {invariant.max_idempotent_error:.2e}")
    print(f"  max rank/N3 error after transport   : {invariant.max_rank_error:.2e}")
    print(f"  min genuine octonionic support      : {invariant.min_octonionic_support:.6f}")

    print("\n[D] Candidate amplitude readings")
    for row in interpretations:
        beta_str = "n/a" if row.beta is None else f"{row.beta:.12f}"
        print(
            f"  {row.label:<31} amp={row.amplitude:.12f} beta={beta_str} "
            f"amp^2={row.ratio2:.12f} |.-target|={row.target_error:.3e} "
            f"match={row.matches_target}"
        )
        print(f"      {row.interpretation}")

    print("\n[V] Verdict")
    print("  Born square root from projector geometry : YES")
    print("  selected density pi/432 realised as Tr(PQ): YES")
    print("  F4-invariant off the associative slice    : YES")
    print("  CHO action coupling / stationarity derived: NO")
    print("  remaining object                           : derive why WZ density enters this transition channel")
    print("  Bayes/scoreboard credit moved              : NO")
    print("=" * 78)

    target_rows = [row for row in rows if row.label == "target eps0"]
    assert len(target_rows) == 1
    assert all(row.trace_error < TOL_TRACE for row in rows)
    assert all(row.born_error < TOL_TRACE for row in rows)
    assert abs(target_rows[0].trace_density - EPS0_SQ) < TOL_TRACE
    assert abs(frame.probability_sum - 1.0) < TOL_TRACE
    assert frame.max_component_error < TOL_TRACE
    assert abs(frame.target_probability - selected.selected_density) < TOL_TRACE
    assert abs(frame.target_amplitude - EPS0) < TOL_TRACE
    assert abs(invariant.base_density - EPS0_SQ) < TOL_TRACE
    assert invariant.max_density_error < TOL_F4
    assert invariant.max_idempotent_error < TOL_F4
    assert invariant.max_rank_error < TOL_F4
    assert invariant.min_octonionic_support > MIN_OCTONIONIC
    matching = [row for row in interpretations if row.matches_target]
    misses = [row for row in interpretations if not row.matches_target]
    assert len(matching) == 1
    assert matching[0].label == "projector trace as probability"
    assert all(row.target_error > MISS_TOL for row in misses)
    action_coupling_derived = False
    assert not action_coupling_derived
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)