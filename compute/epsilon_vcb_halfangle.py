"""
C2 — the |V_cb| coefficient 1/2 is the SU(2) spinor half-angle.
===============================================================

Context (ledger C2, spurion_bridge.py SectorChannel "CKM |V_cb|", M11)
----------------------------------------------------------------------
M11 derived the mixing MULTIPLICITIES (7, 3, 4, 4/7) as octonion Fano-line
counts and identified the lepton 1/(4 pi) as the transition-sphere measure.  It
left ONE coefficient as an honest input: the 1/2 in

    |V_cb| = (1/2) * eps0        (a single-doublet CKM amplitude, power 1 in eps)

which M11 attributed to "weak isospin T3 = 1/2, an input".  This module removes
that input: the 1/2 is the spin-1/2 HALF-ANGLE of the SU(2) double cover of the
transition Bloch sphere -- the same S^2 whose Berry flux pi sits in eps0.

The claim of this module
------------------------
The spurion history is a rotation by a small angle eps0 on the two-level (qubit)
transition sphere S^2 = SU(2)/U(1).  A transition is read in whichever
representation carries it, and the SU(2) double cover SU(2) -> SO(3) makes the
half-angle explicit:

  [1] SPINOR (fundamental) channel.  A rotation by angle theta about an axis acts
      on the qubit as U(theta) = exp(-i theta n.sigma / 2); its OFF-diagonal
      (transition) amplitude is sin(theta/2) ~ (1/2) theta.  Coefficient = 1/2.
      This is the channel of an INTER-generation transition (vacuum ray <-> the
      orthogonal broken ray -- the two-level Bloch system of R1/R2), so

          |V_cb| = sin(eps0/2) ~ (1/2) eps0.

  [2] VECTOR (adjoint) channel.  The SAME rotation acts on the 7-dimensional
      imaginary-octonion space (where |V_us| lives) at FULL angle: the off-
      diagonal of a vector rotation is sin(theta) ~ theta.  Coefficient = 1.
      Summed coherently over the 7 Fano directions (M11) this is sqrt(7) eps0.

      So the contrast sqrt(7)  vs  1/2  is exactly VECTOR (full angle, 7 dirs)
      vs SPINOR (half angle, one qubit): the 1/2 is the SU(2)->SO(3) double-cover
      factor, not a weak-isospin number put in by hand.

  [3] FINITE-ANGLE AVATAR: tan(pi/8) = sqrt(2) - 1.  The ratio of transition to
      survival amplitude on the Bloch sphere is sin(theta/2)/cos(theta/2) =
      tan(theta/2).  At the octonionic maximal-reflection angle theta = pi/4 (the
      45 degrees between adjacent imaginary-octonion planes) this is
      tan(pi/8) = sqrt(2) - 1.  The small-angle 1/2 and the 45-degree sqrt(2)-1
      are the SAME spinorial half-angle tan(theta/2), linearised vs evaluated at
      the discrete octonionic reflection.

Honest scope
------------
Derived here: the VALUE 1/2 as the spin-1/2 half-angle (and its finite avatar
tan(pi/8) = sqrt(2)-1), and the vector-vs-spinor contrast that distinguishes the
sqrt(7) |V_us| channel from the 1/2 |V_cb| channel.  NOT derived from the CHO
operator: the channel ASSIGNMENT itself -- why |V_cb| is carried by the spinor
(the inter-generation two-level transition) while |V_us| is the Im(O) vector.
That assignment is the remaining input; the coefficient 1/2 is no longer one.

numpy only.  No scipy.  Reuses spurion_bridge (OBSERVED).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_vcb_halfangle.py
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from spurion_bridge import OBSERVED  # noqa: E402


EPS0_SQ = np.pi / 432.0
EPS0 = np.sqrt(EPS0_SQ)

# Pauli matrices.
SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SIGMA_Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)


# --------------------------------------------------------------------------
# [1] Spinor (fundamental) transition amplitude: sin(theta/2) -> coefficient 1/2
# --------------------------------------------------------------------------


def su2_rotation(theta: float, axis: np.ndarray) -> np.ndarray:
    """U(theta) = exp(-i theta n.sigma / 2) in the SU(2) fundamental."""
    n = np.asarray(axis, dtype=float)
    n = n / np.linalg.norm(n)
    generator = n[0] * SIGMA_X + n[1] * SIGMA_Y + n[2] * SIGMA_Z
    # exp(-i theta/2 (n.sigma)) = cos(theta/2) I - i sin(theta/2) (n.sigma).
    return np.cos(theta / 2.0) * np.eye(2) - 1.0j * np.sin(theta / 2.0) * generator


def spinor_halfangle_coefficient() -> dict:
    """Leading coefficient of the spinor transition amplitude vs theta -> 1/2."""
    axis = np.array([0.0, 1.0, 0.0])  # rotation about y: real, |<1|U|0>| = sin(theta/2)
    up = np.array([1.0, 0.0], dtype=complex)
    down = np.array([0.0, 1.0], dtype=complex)
    thetas = np.array([1e-3, 2e-3, 4e-3, 8e-3])
    amps = []
    for th in thetas:
        U = su2_rotation(th, axis)
        amps.append(abs(np.vdot(down, U @ up)))
    amps = np.array(amps)
    # amplitude = sin(theta/2); leading coefficient = amplitude/theta -> 1/2.
    coeff = float(np.mean(amps / thetas))
    exact = abs(np.sin(EPS0 / 2.0) / EPS0)  # exact spinor coefficient at eps0
    return {
        "coefficient": coeff,
        "is_half": abs(coeff - 0.5) < 1e-5,
        "exact_at_eps0": exact,
        "amplitude_is_sin_half": bool(
            np.allclose(amps, np.sin(thetas / 2.0), atol=1e-12)
        ),
    }


# --------------------------------------------------------------------------
# [2] Vector (adjoint) transition amplitude: sin(theta) -> coefficient 1
# --------------------------------------------------------------------------


def so3_rotation_xy(theta: float) -> np.ndarray:
    """A rotation by theta in the x-y plane (vector / adjoint rep)."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def vector_fullangle_coefficient() -> dict:
    """Leading coefficient of the vector transition amplitude vs theta -> 1."""
    e_x = np.array([1.0, 0.0, 0.0])
    e_y = np.array([0.0, 1.0, 0.0])
    thetas = np.array([1e-3, 2e-3, 4e-3, 8e-3])
    amps = []
    for th in thetas:
        R = so3_rotation_xy(th)
        amps.append(abs(e_y @ (R @ e_x)))  # off-diagonal = sin(theta)
    amps = np.array(amps)
    coeff = float(np.mean(amps / thetas))
    return {
        "coefficient": coeff,
        "is_one": abs(coeff - 1.0) < 1e-5,
        "amplitude_is_sin": bool(np.allclose(amps, np.sin(thetas), atol=1e-12)),
    }


# --------------------------------------------------------------------------
# [3] Finite-angle avatar: tan(pi/8) = sqrt(2) - 1
# --------------------------------------------------------------------------


def tan_pi_8_identity() -> dict:
    """tan(theta/2) is the transition/survival ratio; at theta=pi/4 it is sqrt(2)-1."""
    half_angle_ratio = np.tan(np.pi / 8.0)        # transition/survival at theta = pi/4
    closed_form = np.sqrt(2.0) - 1.0
    # Linearised: tan(theta/2) ~ theta/2, leading coefficient 1/2 (same as [1]).
    thetas = np.array([1e-3, 2e-3, 4e-3, 8e-3])
    lin_coeff = float(np.mean(np.tan(thetas / 2.0) / thetas))
    return {
        "tan_pi_8": float(half_angle_ratio),
        "sqrt2_minus_1": float(closed_form),
        "identity_ok": abs(half_angle_ratio - closed_form) < 1e-12,
        "linearised_coefficient": lin_coeff,
        "linearised_is_half": abs(lin_coeff - 0.5) < 1e-5,
    }


# --------------------------------------------------------------------------
# Prediction: |V_cb| = (1/2) eps0 vs |V_us| = sqrt(7) eps0
# --------------------------------------------------------------------------


def predictions() -> list:
    rows = []
    v_cb_pred = 0.5 * EPS0
    v_cb_obs = OBSERVED["V_cb"]
    rows.append(("|V_cb| (spinor)", "(1/2) * eps0", v_cb_pred, v_cb_obs,
                 100.0 * (v_cb_pred - v_cb_obs) / v_cb_obs))
    v_us_pred = np.sqrt(7.0) * EPS0
    v_us_obs = OBSERVED["V_us"]
    rows.append(("|V_us| (vector)", "sqrt(7) * eps0", v_us_pred, v_us_obs,
                 100.0 * (v_us_pred - v_us_obs) / v_us_obs))
    return rows


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------


def main() -> None:
    print("=" * 78)
    print("  C2 — |V_cb| coefficient 1/2 = the SU(2) spinor half-angle")
    print("=" * 78)
    print(f"  eps0 = sqrt(pi/432) = {EPS0:.7f}")
    print()

    spn = spinor_halfangle_coefficient()
    print("-" * 78)
    print("  [1] SPINOR (fundamental) transition amplitude = sin(theta/2)")
    print("-" * 78)
    print(f"      leading coefficient (amp/theta)  = {spn['coefficient']:.6f}  (-> 1/2)")
    print(f"      |<down|U(eps0)|up>| / eps0        = {spn['exact_at_eps0']:.6f}")
    print("      a single-qubit (inter-generation) transition carries the HALF angle")
    s1 = spn["is_half"] and spn["amplitude_is_sin_half"]
    print(f"      [{'PASS' if s1 else 'FAIL'}] spinor coefficient is 1/2")
    print()

    vec = vector_fullangle_coefficient()
    print("-" * 78)
    print("  [2] VECTOR (adjoint) transition amplitude = sin(theta)")
    print("-" * 78)
    print(f"      leading coefficient (amp/theta)  = {vec['coefficient']:.6f}  (-> 1)")
    print("      the Im(O) channel of |V_us| carries the FULL angle (coherent sqrt(7))")
    s2 = vec["is_one"] and vec["amplitude_is_sin"]
    print(f"      [{'PASS' if s2 else 'FAIL'}] vector coefficient is 1, so 1/2 = "
          "double-cover half-angle")
    print()

    tan = tan_pi_8_identity()
    print("-" * 78)
    print("  [3] FINITE-ANGLE AVATAR: tan(pi/8) = sqrt(2) - 1")
    print("-" * 78)
    print(f"      tan(pi/8)        = {tan['tan_pi_8']:.7f}")
    print(f"      sqrt(2) - 1      = {tan['sqrt2_minus_1']:.7f}")
    print(f"      tan(theta/2) leading coefficient = {tan['linearised_coefficient']:.6f}"
          "  (-> 1/2)")
    print("      transition/survival = tan(theta/2): 1/2 (small angle) and sqrt(2)-1")
    print("      (at the octonionic 45 deg reflection) are the SAME half-angle")
    s3 = tan["identity_ok"] and tan["linearised_is_half"]
    print(f"      [{'PASS' if s3 else 'FAIL'}] tan(pi/8) = sqrt(2)-1, linearises to 1/2")
    print()

    print("-" * 78)
    print("  PREDICTION (eps0^2 = pi/432 frozen)")
    print("-" * 78)
    print(f"      {'channel':<18}{'formula':<18}{'pred':>9}{'obs':>9}{'err%':>8}")
    pred_ok = True
    for name, formula, pred, obs, pct in predictions():
        print(f"      {name:<18}{formula:<18}{pred:>9.4f}{obs:>9.4f}{pct:>+7.1f}%")
        pred_ok = pred_ok and abs(pct) < 3.0
    print()

    print("=" * 78)
    print("  VERDICT")
    print("=" * 78)
    if s1 and s2 and s3 and pred_ok:
        print("  C2 status: DERIVED. The 1/2 in |V_cb| = (1/2) eps0 is the spin-1/2")
        print("  half-angle of the SU(2) double cover of the transition Bloch sphere:")
        print("  a single-qubit (inter-generation) transition amplitude is sin(eps0/2)")
        print("  ~ (1/2) eps0, while the Im(O) VECTOR channel of |V_us| carries the full")
        print("  angle sin(eps0) summed coherently to sqrt(7). The contrast sqrt(7) vs")
        print("  1/2 is vector-vs-spinor; its finite avatar at the octonionic 45 deg")
        print("  reflection is tan(pi/8) = sqrt(2)-1. The 1/2 is no longer a weak-isospin")
        print("  input.")
        print()
        print("  Honest residual: the channel ASSIGNMENT (|V_cb| = spinor inter-gen")
        print("  transition, |V_us| = Im(O) vector) follows the two-level/Im(O) split")
        print("  but its derivation from the CHO Yukawa operator is still open. The")
        print("  VALUE 1/2 is derived; which channel is spinor is the remaining input.")
    else:
        print("  C2 status: OPEN — a half-angle, vector, identity, or prediction check")
        print("  failed above.")
    print()


if __name__ == "__main__":
    main()
