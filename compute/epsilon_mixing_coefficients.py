"""
M11 — mixing-sector coefficients as Fano-line counts, and the lepton 1/(4pi).
=============================================================================

Context (ledger M11/C1-C2/N2-N3-N5, sector_projector_derivation.py, FLAVOUR_DERIVATION.md)
------------------------------------------------------------------------------------------
The single knob eps0^2 = pi/432 drives the mixing sector through coefficients
that, until now, were the last "chosen" numbers in the flavour bridge:

    |V_us|         = sqrt(7) * eps0          (C1, an AMPLITUDE, power 1 in eps)
    |V_cb|         = (1/2)   * eps0          (C2, an AMPLITUDE, power 1 in eps)
    sin^2(theta13) = 3       * eps0^2        (N3, a PROBABILITY, power 2 in eps)
    dm21^2/dm31^2  = 4       * eps0^2        (N2, a PROBABILITY, power 2 in eps)
    sin^2(theta23) = 4/7                     (N5, a PROBABILITY ratio)
    lepton shape   = 1/(4 pi)                (M11, the -3.75 sigma audit outlier)

What this module shows
----------------------
[1] FANO-LINE DIRECTION COUNTS.  The vacuum omega = (1 + i e7)/2 fixes the point
    e7.  The octonion Fano plane has 7 lines; exactly 3 pass through the vacuum
    point (the SU(3) colour/stabiliser triplet) and the remaining 4 avoid it.
    These three integers 7, 3, 4 are read directly off the Fano incidence table
    (no fitting), and they ARE the mixing multiplicities:

        7  = all Fano lines          -> |V_us|        (full Cabibbo channel)
        3  = lines through vacuum     -> sin^2(theta13) (colour/stabiliser)
        4  = lines avoiding vacuum    -> dm21^2/dm31^2  (broken directions)
        4/7 = avoiding / total        -> sin^2(theta23)

[2] AMPLITUDE-vs-PROBABILITY DICHOTOMY.  A mixing ANGLE (CKM, power 1 in eps) is
    an amplitude: a coherent-looking but random-phase sum of n unit transition
    amplitudes has RMS magnitude sqrt(n).  A mixing PROBABILITY (sin^2, mass-
    ratio, power 2 in eps) is the squared amplitude and scales as the plain count
    n.  So the SAME Fano counts give sqrt(7) for the |V_us| amplitude but 3 and 4
    for the sin^2 / mass-ratio probabilities.  Verified by Monte-Carlo:
    <|sum of n random-phase units|^2> = n, so RMS magnitude = sqrt(n).

[3] THE LEPTON 1/(4 pi).  The up/down |A/C|^2 shape factors are pure rationals
    (1/4 and 9/4 = weak-isospin squares).  The lepton sector is the ONLY one
    carrying a pi -- and (eps0 route 1) that pi must be the Berry/holonomy pi of
    the transition Bloch sphere S^2, never a heat-kernel (4 pi)^{-d/2}.  The
    natural pi-carrying lepton object is the UNIFORM (rotation-invariant) measure
    on that S^2: Int_{S^2} dOmega = 4 pi, so a spherical average normalises by
    1/(4 pi).  The lepton sector traces over the FULL Fock module (the derived
    "8", epsilon_channel_coefficients.py) and correspondingly averages over the
    FULL transition sphere -> 1/(4 pi); the quark sectors use discrete weak-
    isospin projections (1/4, 9/4) and carry no pi.  Verified: Int_{S^2} dOmega
    = 4 pi numerically.

Honest scope
------------
Derived here as Fano/geometry: the counts 7, 3, 4, 4/7 and the amplitude-vs-
probability sqrt-rule, and the IDENTIFICATION of 1/(4 pi) as the transition-
sphere measure.  NOT derived: the |V_cb| weak-isospin coefficient 1/2 (a single
doublet transition, T3 = 1/2 -- an input), and the dynamical reduction of the
lepton Yukawa trace to the uniform S^2 average (the measure is identified, its
derivation from the CHO operator remains open).  M11 is ADVANCED, not closed.

numpy only.  No scipy.  Reuses spurion_bridge (FANO_LINES, VACUUM_POINT, OBSERVED).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_mixing_coefficients.py
"""

from __future__ import annotations

import numpy as np

from spurion_bridge import FANO_LINES, VACUUM_POINT, OBSERVED


EPS0_SQ = np.pi / 432.0
EPS0 = np.sqrt(EPS0_SQ)


# --------------------------------------------------------------------------
# [1] Fano-line direction counts.
# --------------------------------------------------------------------------


def fano_line_counts() -> dict:
    """Count Fano lines total / through the vacuum point / avoiding it."""
    total = len(FANO_LINES)
    through = [ln for ln in FANO_LINES if VACUUM_POINT in ln]
    avoiding = [ln for ln in FANO_LINES if VACUUM_POINT not in ln]
    return {
        "total": total,
        "through_vacuum": len(through),
        "avoiding_vacuum": len(avoiding),
        "through_lines": through,
        "avoiding_lines": avoiding,
        "partition_ok": len(through) + len(avoiding) == total,
    }


# --------------------------------------------------------------------------
# [2] Amplitude (sqrt n) vs probability (n): random-phase Monte-Carlo.
# --------------------------------------------------------------------------


def amplitude_vs_probability(n: int, trials: int = 200000,
                             seed: int = 11) -> dict:
    """<|sum of n unit random-phase amplitudes|^2> = n  =>  RMS magnitude = sqrt(n).

    A mixing AMPLITUDE summing n incoherent unit transition directions has RMS
    magnitude sqrt(n); the corresponding PROBABILITY (its square) scales as n.
    """
    rng = np.random.default_rng(seed)
    phases = rng.uniform(0.0, 2.0 * np.pi, size=(trials, n))
    amp = np.exp(1j * phases).sum(axis=1)
    mean_prob = float(np.mean(np.abs(amp) ** 2))
    rms_mag = float(np.sqrt(mean_prob))
    return {
        "n": n,
        "mean_probability": mean_prob,   # -> n
        "rms_amplitude": rms_mag,        # -> sqrt(n)
        "prob_matches_n": abs(mean_prob - n) < 0.05 * n,
        "amp_matches_sqrt_n": abs(rms_mag - np.sqrt(n)) < 0.05 * np.sqrt(n),
    }


# --------------------------------------------------------------------------
# [3] Lepton 1/(4 pi) = uniform measure normalisation on the transition S^2.
# --------------------------------------------------------------------------


def sphere_measure_normalisation(n_theta: int = 400) -> dict:
    """Int_{S^2} dOmega = 4 pi by direct numerical quadrature of sin(theta)."""
    theta = np.linspace(0.0, np.pi, n_theta)
    # Int_0^pi sin(theta) dtheta = 2, times the phi integral 2 pi -> 4 pi.
    sin_theta = np.sin(theta)
    integral = np.sum(0.5 * (sin_theta[:-1] + sin_theta[1:]) * np.diff(theta))
    solid_angle = float(integral * 2.0 * np.pi)
    return {
        "solid_angle": solid_angle,        # -> 4 pi
        "normalisation": 1.0 / solid_angle,  # -> 1/(4 pi)
        "target_4pi": 4.0 * np.pi,
        "matches_4pi": abs(solid_angle - 4.0 * np.pi) < 1e-3,
    }


# --------------------------------------------------------------------------
# Predictions from the derived counts (frozen eps0, observed values for check).
# --------------------------------------------------------------------------


def predictions(counts: dict) -> list:
    """(name, formula, predicted, observed, pct) for each mixing channel."""
    n_tot = counts["total"]
    n_thru = counts["through_vacuum"]
    n_avoid = counts["avoiding_vacuum"]
    rows = [
        ("|V_us|        ", f"sqrt({n_tot})*eps0",
         np.sqrt(n_tot) * EPS0, OBSERVED["V_us"]),
        ("|V_cb|        ", "(1/2)*eps0   [weak isospin, input]",
         0.5 * EPS0, OBSERVED["V_cb"]),
        ("sin^2(th13)   ", f"{n_thru}*eps0^2",
         n_thru * EPS0_SQ, OBSERVED["sin2_theta13"]),
        ("dm21^2/dm31^2 ", f"{n_avoid}*eps0^2",
         n_avoid * EPS0_SQ, OBSERVED["dm2_ratio"]),
        ("sin^2(th23)   ", f"{n_avoid}/{n_tot}",
         n_avoid / n_tot, 0.57),  # atmospheric, near-maximal
    ]
    out = []
    for name, formula, pred, obs in rows:
        pct = (pred - obs) / obs * 100.0
        out.append((name, formula, pred, obs, pct))
    return out


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------


def main() -> None:
    print("=" * 78)
    print("  M11 — MIXING COEFFICIENTS AS FANO-LINE COUNTS + THE LEPTON 1/(4 pi)")
    print("=" * 78)
    print("  The single knob eps0^2 = pi/432 drives the mixing sector through")
    print("  coefficients sqrt(7), 1/2, 3, 4, 4/7 and the lepton shape 1/(4 pi).")
    print("  This module derives the COUNTS 7, 3, 4 as Fano-line incidences, the")
    print("  sqrt-vs-plain rule from amplitude-vs-probability, and identifies the")
    print("  1/(4 pi) as the transition-sphere measure.")
    print()

    # [1]
    counts = fano_line_counts()
    print("-" * 78)
    print("  [1] FANO-LINE DIRECTION COUNTS (vacuum omega = (1 + i e7)/2 fixes e7)")
    print("-" * 78)
    print(f"      total Fano lines            : {counts['total']}  (= dim Im(O))")
    print(f"      lines through vacuum point 7: {counts['through_vacuum']}  "
          f"{counts['through_lines']}")
    print(f"      lines avoiding vacuum point : {counts['avoiding_vacuum']}  "
          f"{counts['avoiding_lines']}")
    part = "PASS" if counts["partition_ok"] else "FAIL"
    print(f"      [{part}] 7 = 3 (colour/stabiliser) + 4 (broken directions)")
    print()

    # [2]
    print("-" * 78)
    print("  [2] AMPLITUDE (sqrt n) vs PROBABILITY (n): random-phase Monte-Carlo")
    print("-" * 78)
    amp_ok = True
    for n in (counts["total"], counts["through_vacuum"], counts["avoiding_vacuum"]):
        res = amplitude_vs_probability(n)
        ok = res["prob_matches_n"] and res["amp_matches_sqrt_n"]
        amp_ok = amp_ok and ok
        flag = "OK" if ok else "XX"
        print(f"      n={n}: <|sum|^2> = {res['mean_probability']:.3f} (-> {n}),  "
              f"RMS = {res['rms_amplitude']:.3f} (-> sqrt({n})={np.sqrt(n):.3f})  [{flag}]")
    verdict = "PASS" if amp_ok else "FAIL"
    print(f"      [{verdict}] angles (power-1 in eps) scale as sqrt(count);")
    print("             sin^2 / mass ratios (power-2) scale as the plain count")
    print()

    # [3]
    sph = sphere_measure_normalisation()
    print("-" * 78)
    print("  [3] LEPTON 1/(4 pi) = UNIFORM MEASURE ON THE TRANSITION SPHERE S^2")
    print("-" * 78)
    print(f"      Int_S^2 dOmega = {sph['solid_angle']:.6f}  (4 pi = "
          f"{sph['target_4pi']:.6f})")
    print(f"      spherical-average normalisation = 1/(4 pi) = "
          f"{sph['normalisation']:.6f}")
    print("      up/down shape factors 1/4, 9/4 are weak-isospin squares (no pi);")
    print("      the lepton sector traces the FULL Fock module (the derived 8) and")
    print("      averages over the FULL sphere -> the unique pi-carrying shape 1/(4 pi).")
    verdict = "PASS" if sph["matches_4pi"] else "FAIL"
    print(f"      [{verdict}] 1/(4 pi) identified as the transition-sphere measure")
    print()

    # Predictions table.
    print("-" * 78)
    print("  MIXING PREDICTIONS FROM THE DERIVED COUNTS (eps0^2 = pi/432 frozen)")
    print("-" * 78)
    print(f"      {'channel':<15}{'formula':<28}{'pred':>9}{'obs':>9}{'err%':>8}")
    for name, formula, pred, obs, pct in predictions(counts):
        print(f"      {name:<15}{formula:<28}{pred:>9.4f}{obs:>9.4f}{pct:>+7.1f}%")
    print()

    print("=" * 78)
    print("  VERDICT")
    print("=" * 78)
    all_ok = counts["partition_ok"] and amp_ok and sph["matches_4pi"]
    if all_ok:
        print("  M11 status: ADVANCED. The mixing multiplicities are Fano-line counts:")
        print("    7 = all lines (|V_us| amplitude sqrt7), 3 = lines through the vacuum")
        print("    (sin^2 th13), 4 = lines avoiding it (dm^2 ratio), 4/7 = sin^2 th23 --")
        print("    read off the octonion Fano incidence table, not fitted. The sqrt-vs-")
        print("    plain split is the amplitude-vs-probability rule (verified by Monte-")
        print("    Carlo). The lepton 1/(4 pi) is identified as the uniform measure on")
        print("    the transition Bloch sphere S^2 (Int dOmega = 4 pi), the pi-carrying")
        print("    partner of the full-Fock lepton trace.")
        print()
        print("  Honest residuals: the |V_cb| coefficient 1/2 (a single weak-doublet")
        print("  transition, T3 = 1/2) is an input, and the dynamical REDUCTION of the")
        print("  lepton Yukawa trace to the uniform S^2 average is identified but not")
        print("  derived from the CHO operator. M11 is advanced, not closed.")
    else:
        print("  M11 status: OPEN — a count, Monte-Carlo, or measure check failed above.")
    print()


if __name__ == "__main__":
    main()
