"""
Action-level derivation of the triality-breaking holonomy theta = pi.
=====================================================================

This module supports `foundations/02_action.md` (legacy repair-pass item T1.0-T1.2). It
turns the weakest step of `spurion_bridge.py` -- "the great circle is the
minimal GEOMETRIC loop, so theta = pi" -- into a stronger statement: the great
circle is the loop selected by a written-down free-particle (geodesic) action on
the transition two-level sphere, and that selection is what fixes theta = pi.

Why this matters
----------------
`spurion_bridge.py` Block 4 computes the Berry phase pi by *choosing* the
great-circle loop because it is the shortest non-contractible loop. A skeptic
correctly objects that "shortest geometric loop" is an assumption, not a
dynamical principle. This module removes that objection one level: it defines

    S_free[gamma] = (1/2) * integral |gamma'(t)|_g^2 dt           (free particle)

on the unit transition sphere with the round (Fubini-Study) metric g, and shows
the CLOSED extremals of S_free are exactly the great circles, because a curve is
an extremal of S_free iff it is a geodesic iff its geodesic curvature vanishes.

The honest residual: this replaces "minimal geometric loop" with "closed
geodesic of the natural free action on the transition sphere." It does NOT yet
derive, from a spacetime/lattice CHO action, that (a) the relevant configuration
space is this rank-one two-level sphere and (b) the free action is the correct
weight. Those remain inputs, tracked in OPERATOR_GAP_AUDIT.md and 02_action.md.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/action_derivation.py
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


BRIDGE_DIM = 16 * 27  # A_Weyl x J3(O) = 432, the exact trace space


# --------------------------------------------------------------------------
# Geometry of the transition two-level sphere
# --------------------------------------------------------------------------
#
# A rank-one transition kernel K = |tau><tau| lives in CP^1, the Bloch sphere of
# the two-level {occupied, broken} subspace. We use the unit 2-sphere with the
# round metric (the Fubini-Study metric on CP^1 is the round metric of radius
# 1/2; the factor only rescales the action uniformly and does not move the
# extremals). A latitude loop at colatitude theta encloses solid angle
# Omega(theta) = 2 pi (1 - cos theta) toward the north pole.


def latitude_loop(colatitude: float, samples: int = 4000) -> np.ndarray:
    """Cartesian points of a latitude circle at given colatitude on S^2."""
    phis = np.linspace(0.0, 2.0 * np.pi, samples, endpoint=False)
    sin_t = np.sin(colatitude)
    cos_t = np.cos(colatitude)
    return np.stack(
        [sin_t * np.cos(phis), sin_t * np.sin(phis), np.full_like(phis, cos_t)],
        axis=1,
    )


def solid_angle_of_latitude(colatitude: float) -> float:
    """Solid angle enclosed toward the north pole by a latitude circle."""
    return 2.0 * np.pi * (1.0 - np.cos(colatitude))


def geodesic_curvature_of_latitude(colatitude: float) -> float:
    """Exact geodesic curvature of a latitude circle on the unit sphere.

    For a circle of colatitude theta on S^2 the geodesic curvature is
    kappa_g = cot(theta). It vanishes only on the equator (theta = pi/2),
    which is the great circle. This is the analytic check; the numerical
    routine below reproduces it from the discretized curve.
    """
    return 1.0 / np.tan(colatitude)


def numerical_geodesic_curvature(loop: np.ndarray) -> float:
    """Mean geodesic curvature of a closed loop on the unit sphere.

    Computed intrinsically: at each vertex, kappa_g is the component of the
    curve's acceleration tangent to the sphere but normal to the velocity,
    divided by speed squared. Returned as the RMS over the loop, so a closed
    geodesic (great circle) returns ~0 and any latitude returns |cot theta|.
    """
    count = len(loop)
    # Arc-length spacing (uniform parameter -> uniform spacing on a circle).
    velocity = np.gradient(loop, axis=0)
    speed = np.linalg.norm(velocity, axis=1, keepdims=True)
    unit_tangent = velocity / speed
    accel = np.gradient(unit_tangent, axis=0)

    kappas = np.empty(count)
    for i in range(count):
        point = loop[i]
        normal = point / np.linalg.norm(point)          # outward sphere normal
        tangent = unit_tangent[i]
        # in-surface normal direction (binormal within the tangent plane)
        side = np.cross(normal, tangent)
        side /= np.linalg.norm(side)
        # kappa_g = (dT/ds) . side, with dT/ds = (dT/di)/(ds/di) = accel/speed.
        kappas[i] = float(np.dot(accel[i], side) / speed[i, 0])
    return float(np.sqrt(np.mean(np.square(kappas))))


@dataclass(frozen=True)
class GeodesicScan:
    colatitudes: np.ndarray
    geodesic_curvatures: np.ndarray
    solid_angles: np.ndarray
    great_circle_index: int


def scan_closed_geodesics(samples: int = 25) -> GeodesicScan:
    """Scan latitude loops; the closed geodesic is the curvature zero crossing."""
    colats = np.linspace(0.15 * np.pi, 0.85 * np.pi, samples)
    kappas = np.array([numerical_geodesic_curvature(latitude_loop(t)) for t in colats])
    omegas = np.array([solid_angle_of_latitude(t) for t in colats])
    great_idx = int(np.argmin(np.abs(colats - np.pi / 2.0)))
    return GeodesicScan(colats, kappas, omegas, great_idx)


# --------------------------------------------------------------------------
# Berry phase of the action-selected loop
# --------------------------------------------------------------------------


def bloch_spinor(colatitude: float, phi: float) -> np.ndarray:
    return np.array(
        [np.cos(colatitude / 2.0), np.exp(1j * phi) * np.sin(colatitude / 2.0)],
        dtype=complex,
    )


def berry_phase_of_latitude(colatitude: float, samples: int = 4000) -> float:
    """Pancharatnam-Berry phase = -(1/2) * enclosed solid angle, via Bargmann."""
    phis = np.linspace(0.0, 2.0 * np.pi, samples, endpoint=False)
    states = [bloch_spinor(colatitude, p) for p in phis]
    product = 1.0 + 0.0j
    for i in range(samples):
        overlap = np.vdot(states[i], states[(i + 1) % samples])
        product *= overlap / abs(overlap)
    return float(-np.angle(product))


@dataclass(frozen=True)
class ActionResult:
    great_circle_curvature: float
    nongeodesic_curvature: float
    selected_solid_angle: float
    theta: float
    eps0_sq: float
    geodesic_selected: bool
    theta_is_pi: bool


def derive_theta_from_action() -> ActionResult:
    scan = scan_closed_geodesics()

    # The free action's closed extremal is the curve with vanishing geodesic
    # curvature: the great circle (equator). Confirm it is the unique zero.
    great_kappa = numerical_geodesic_curvature(latitude_loop(np.pi / 2.0))
    off_kappa = numerical_geodesic_curvature(latitude_loop(np.pi / 3.0))
    geodesic_selected = bool(great_kappa < 1e-2 and off_kappa > 1e-1)

    # The selected closed geodesic encloses a hemisphere: Omega = 2 pi.
    selected_omega = solid_angle_of_latitude(np.pi / 2.0)
    # Berry phase of the action-selected loop fixes theta.
    theta = abs(berry_phase_of_latitude(np.pi / 2.0))
    theta_is_pi = bool(abs(theta - np.pi) < 1e-3)

    eps0_sq = theta / BRIDGE_DIM
    return ActionResult(
        great_circle_curvature=great_kappa,
        nongeodesic_curvature=off_kappa,
        selected_solid_angle=selected_omega,
        theta=theta,
        eps0_sq=eps0_sq,
        geodesic_selected=geodesic_selected,
        theta_is_pi=theta_is_pi,
    )


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------


def main() -> None:
    print("=" * 78)
    print("  ACTION-LEVEL DERIVATION OF theta = pi  (legacy T1.0-T1.2)")
    print("=" * 78)
    print()
    print("Candidate free-particle action on the transition sphere S^2:")
    print("    S_free[gamma] = (1/2) * integral |gamma'(t)|^2 dt")
    print("Its closed extremals are the closed geodesics = great circles.")
    print("The triality-breaking loop is therefore NOT chosen as 'shortest loop';")
    print("it is the stationary configuration of a written-down action.")
    print()

    scan = scan_closed_geodesics()
    print("Geodesic-curvature scan over latitude loops (kappa_g = 0 <=> geodesic):")
    print(f"  {'colatitude/deg':>14} {'kappa_g(num)':>13} {'kappa_g(exact)':>15} {'Omega/2pi':>10}")
    print("  " + "-" * 56)
    for colat, kappa, omega in zip(scan.colatitudes, scan.geodesic_curvatures, scan.solid_angles):
        exact = geodesic_curvature_of_latitude(colat)
        marker = "  <- closed geodesic" if abs(colat - np.pi / 2.0) < 1e-6 else ""
        print(
            f"  {np.degrees(colat):>14.1f} {kappa:>13.4f} {exact:>15.4f} "
            f"{omega / (2.0 * np.pi):>10.4f}{marker}"
        )
    print()

    result = derive_theta_from_action()
    print("Action-selected loop (the closed geodesic, equator):")
    print(f"  geodesic curvature (great circle) = {result.great_circle_curvature:.4e}  (target 0)")
    print(f"  geodesic curvature (60 deg loop)  = {result.nongeodesic_curvature:.4e}  (nonzero)")
    print(f"  enclosed solid angle Omega        = {result.selected_solid_angle:.6f}  (= 2 pi)")
    print(f"  Berry phase |gamma| = Omega/2     = {result.theta:.6f}  (pi = {np.pi:.6f})")
    print()
    print("Consequence for the single knob:")
    print(f"  epsilon0^2 = theta / dim(A_Weyl x J3(O)) = {result.theta:.6f} / {BRIDGE_DIM}")
    print(f"             = {result.eps0_sq:.8f}")
    print(f"  pi / 432   = {np.pi / 432.0:.8f}")
    print()

    checks = [
        ("free action selects the closed geodesic (great circle)", result.geodesic_selected),
        ("selected loop encloses Omega = 2 pi (hemisphere)",
         abs(result.selected_solid_angle - 2.0 * np.pi) < 1e-9),
        ("action-selected Berry phase gives theta = pi", result.theta_is_pi),
        ("epsilon0^2 = pi/432 follows from theta and the 432 trace space",
         abs(result.eps0_sq - np.pi / 432.0) < 1e-9),
    ]
    print("FAILURE-CLOSED CHECKS")
    print("-" * 78)
    for label, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    print()

    all_pass = all(ok for _, ok in checks)
    if all_pass:
        print("VERDICT: the pi factor is now selected by a written-down free action on")
        print("the transition sphere, upgrading 'minimal geometric loop' (spurion_bridge")
        print("Block 4) to 'closed geodesic of S_free'. This is a genuine, if partial,")
        print("action-level derivation.")
    else:
        print("VERDICT: at least one check failed; theta = pi is NOT action-selected here.")
    print()
    print("HONEST RESIDUAL (still open, tracked in 02_action.md / OPERATOR_GAP_AUDIT.md):")
    print("  * that the configuration space IS the rank-one two-level transition sphere")
    print("    must come from the CHO Yukawa map, not be assumed;")
    print("  * that S_free (free particle) is the correct weight must follow from the")
    print("    CHO lattice/information action, not be posited;")
    print("  * the 432 = 16*27 trace space is justified in spurion_bridge.py Block 2 by")
    print("    equivariance + Jordan closure, which is itself not yet an action theorem.")
    print("  Until those close, F0 status is 'action-derived pi factor, full theorem")
    print("  pending' -- an upgrade over 'open bridge', not a completed proof.")


if __name__ == "__main__":
    main()
