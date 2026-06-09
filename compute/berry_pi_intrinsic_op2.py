"""
THE pi, HARDENED -- is the Berry holonomy INTRINSIC to OP^2, and WHY is it a
half-turn?  (the FORM half of pi/432, pushed past the slice it was measured on)
==============================================================================

Why this module exists
----------------------
`berry_sigma_model_op2.py` settled the FORM half of pi/432: the Berry/WZ
holonomy of the minimal great-circle loop on the triality-vacuum manifold OP^2
is pi, where the analytic spectral action provably cannot emit it (Phase 1.3).
But that holonomy was computed on ONE associative slice -- a CP^1 built from a
COMPLEX 2-plane of O^3 -- and its own contract flagged the open seam:

    "settles only the kinetic term ... a CP^1 ⊂ OP^2 built from a complex
     (associative) 2-plane ... pi read as its geodesic-selected Berry phase."

So the honest next question -- "carry on cracking the pi" -- is whether that pi
is a feature of the chosen associative slice or a property of the WHOLE
octonionic OP^2, and WHY it is a half-turn (pi) rather than some other angle.
This module answers both, rigorously and without ever evaluating an
ill-defined octonionic Bargmann product.

The three things proved here (all NEW relative to the existing pi modules)
--------------------------------------------------------------------------
  [A] THE HALF-TURN IS FORCED BY GENERATION-ORTHOGONALITY.  The CP^1 transition
      sphere has, as its two ANTIPODAL POLES, two ORTHOGONAL primitive
      idempotents of J3(O) -- i.e. two of the three generations E1, E2 with
      Tr(E1 o E2) = 0.  The Berry phase as a function of colatitude is exactly
      gamma(theta) = pi (1 - cos theta) (the spin-1/2 half-solid-angle law); the
      great circle theta = pi/2 -- the unique closed geodesic, the locus
      EQUIDISTANT from the two orthogonal generations -- encloses the hemisphere
      Omega = 2pi and gives gamma = pi.  A non-geodesic latitude loop encloses
      less and gives gamma < pi (theta = pi/3 -> pi/2).  So pi is not an input:
      it is the holonomy at the geodesic that separates two orthogonal
      generations.  (Three mutually orthogonal idempotents E1,E2,E3 give three
      such antipodal transition spheres, one per generation pair.)

  [B] THE pi IS INTRINSIC TO OP^2 (F4-invariant), not a slice artifact.  F4 =
      Aut(J3(O)) preserves the Jordan product and trace, hence the trace metric
      Tr(P o Q) -- it is an ISOMETRY of OP^2 (verified to ~1e-13).  Transporting
      the entire great-circle loop by a random automorphism A in F4 (i) keeps it
      a loop of genuine rank-one idempotents (P o P = P, N3 = 0), (ii) preserves
      EVERY consecutive overlap Tr(P_i o P_{i+1}) -- the full metric data the
      Berry phase = (1/2) x (round area) depends on -- yet (iii) moves the loop
      into GENUINELY OCTONIONIC directions (the e2..e7 components, zero on the
      associative slice, become O(1)).  OP^2 = F4/Spin(9) is a rank-one
      (two-point-homogeneous) symmetric space, so every geodesic 2-sphere is an
      F4-image of the base CP^1 and the isometry-invariant Berry phase is the
      SAME pi on all of them.  The pi belongs to OP^2, not to the complex slice.

  [C] THE HALF-TURN IS THE SU(2) SIGN FLIP.  Around the great circle the
      Bargmann product of the transition states is a NEGATIVE real number:
      e^{i pi} = -1.  The vacuum ray returns to MINUS itself after one loop --
      the spin-1/2 double-cover signature, the same sqrt/half-angle structure
      that `epsilon_vcb_halfangle.py` reads as tan(pi/8) = sqrt 2 - 1.

What this does NOT do (the honest scope -- no Bayes credit moves)
----------------------------------------------------------------
This hardens only the FORM (the pi).  It does NOT touch the CONTENT half: the
three seed eigenvalues remain unselected (berry_sigma_model_op2: N3 and every
F4-invariant is flat on OP^2, so seed-selection needs an F4-BREAKING term).  It
moves NO scoreboard credit: the geometric pi/432 reading is the SAME conditional
hypothesis as before, now shown robust to the octonionic directions; pi/432 is
not promoted, F0 stays GEOMETRIC/open.  The intrinsicness of the pi rests on F4
being an isometry (verified here) plus the standard fact that the Berry phase
= (1/2) x area is isometry-invariant on a two-point-homogeneous space (cited,
not re-derived); this module does NOT evaluate an octonionic Bargmann product
(which is non-associative and ill-defined) -- it proves the phase-determining
trace data is F4-invariant.

numpy only.  No scipy.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/berry_pi_intrinsic_op2.py
"""

from __future__ import annotations

import math

import numpy as np

from epsilon_action_selection import (
    trace_form,
    cubic_norm,
    jordan_product,
    _f4_basis,
    random_automorphism,
)
from epsilon_orbit_selection import primitive_idempotents

PI = math.pi

# tolerances (loose vs the ~1e-13..1e-16 actuals -> wide tripwire margin)
TOL_PHASE = 3e-3      # Berry-phase agreement with the pi(1-cos theta) law
TOL_ORTHO = 1e-9      # Tr(E1 o E2) = 0 for orthogonal generations
TOL_ISOMETRY = 1e-9   # F4 preservation of consecutive overlaps
TOL_IDEM = 1e-9       # P o P = P on the transported loop
TOL_RANK = 1e-9       # N3 = 0 on the transported loop
MIN_OCTONIONIC = 0.1  # the transported loop must leave the associative slice


# --------------------------------------------------------------------------- #
#  Complex coherent states on a CP^1 ⊂ OP^2 and their J3(O) embedding          #
# --------------------------------------------------------------------------- #
def _oct(z: complex) -> np.ndarray:
    """A complex number -> 8-vector octonion (e0 = real, e1 = imaginary)."""
    v = np.zeros(8)
    v[0] = z.real
    v[1] = z.imag
    return v


def _embed(psi: np.ndarray) -> np.ndarray:
    """Embed a unit complex 3-vector psi as the rank-one J3(O) projector
    P = psi psi^dagger, in the source-of-truth 27-coordinate convention
    (verified: embed(e_i) = primitive_idempotents()[i], P o P = P, N3(P) = 0,
    Tr(P o Q) = |<psi|phi>|^2)."""
    a, b, c = psi
    xi = np.array([abs(a) ** 2, abs(b) ** 2, abs(c) ** 2])
    z1 = _oct(b * np.conj(c))     # the (1,2) entry
    z2 = _oct(np.conj(a) * c)     # the (2,0) entry = conj of (0,2)
    z3 = _oct(a * np.conj(b))     # the (0,1) entry
    return np.concatenate([xi, z1, z2, z3])


def _coherent(theta: float, phi: float) -> np.ndarray:
    """Unit complex 3-vector on the CP^1 in the (0,1) plane: poles theta=0 -> E1,
    theta=pi -> E2 (two orthogonal primitive idempotents = two generations)."""
    return np.array(
        [math.cos(theta / 2.0), np.exp(1j * phi) * math.sin(theta / 2.0), 0.0],
        dtype=complex,
    )


def _bargmann_phase(psis) -> complex:
    """The (un-normalised) Bargmann product prod_i <psi_i | psi_{i+1}> around a
    closed loop.  Its argument is the gauge-invariant geometric phase; its sign
    (real-negative) is the SU(2) double-cover signature."""
    prod = 1.0 + 0.0j
    n = len(psis)
    for i in range(n):
        prod *= np.vdot(psis[i], psis[(i + 1) % n])
    return prod


def loop_phase_at_latitude(theta: float, n: int = 4000):
    """|Berry phase| of the latitude-theta loop, and the predicted pi(1-cos th)."""
    phis = np.linspace(0.0, 2.0 * PI, n, endpoint=False)
    psis = [_coherent(theta, p) for p in phis]
    phase = abs(float(np.angle(_bargmann_phase(psis))))
    predicted = PI * (1.0 - math.cos(theta))
    return phase, predicted


# --------------------------------------------------------------------------- #
#  [A] the half-turn is forced by generation-orthogonality                     #
# --------------------------------------------------------------------------- #
def orthogonality_origin():
    """The two poles of the transition CP^1 are orthogonal primitive idempotents
    (two generations); the Berry phase obeys gamma(theta) = pi(1 - cos theta);
    the geodesic equator (equidistant from the two orthogonal generations) gives
    pi.  Sampled from a small loop UP TO the equator, so gamma <= pi rises
    monotonically (no 2pi wrap).  Returns
    (pole_overlap, [(theta, phase, predicted)], equator_phase)."""
    E1, E2, E3 = primitive_idempotents()
    north = _embed(_coherent(0.0, 0.0))        # = E1
    south = _embed(_coherent(PI, 0.0))         # = E2 (up to phase)
    pole_overlap = trace_form(north, south)    # = Tr(E1 o E2) = 0 (orthogonal)
    rows = []
    for theta in (PI / 6.0, PI / 4.0, PI / 3.0, PI / 2.0):
        phase, predicted = loop_phase_at_latitude(theta)
        rows.append((theta, phase, predicted))
    equator_phase, _ = loop_phase_at_latitude(PI / 2.0)
    return pole_overlap, rows, equator_phase


# --------------------------------------------------------------------------- #
#  [B] the pi is INTRINSIC to OP^2: F4 is an isometry that octonionises the loop #
# --------------------------------------------------------------------------- #
def _octonionic_support(p27: np.ndarray) -> float:
    """Largest GENUINELY-octonionic component (e2..e7 of each off-diagonal
    octonion) of a 27-vector.  Zero on the complex (associative) slice; O(1)
    once F4 has rotated the loop into the octonionic directions."""
    worst = 0.0
    for base in (3, 11, 19):                   # the three octonion blocks
        worst = max(worst, float(np.max(np.abs(p27[base + 2: base + 8]))))
    return worst


def f4_intrinsic(n_loop: int = 24, n_auto: int = 100, seed: int = 0):
    """Transport the equatorial great-circle loop by random F4 automorphisms.
    The Berry phase = (1/2) x (round area) depends only on the loop's metric
    data {Tr(P_i o P_j)}; F4 preserves all of it (isometry) while moving the
    loop OFF the associative slice into octonionic directions.  By two-point
    homogeneity of OP^2 the phase is therefore the SAME pi on every geodesic
    2-sphere.

    Returns (worst_overlap_dev, worst_idem, worst_rank, min_octonionic_support).
    """
    phis = np.linspace(0.0, 2.0 * PI, n_loop, endpoint=False)
    base = [_embed(_coherent(PI / 2.0, p)) for p in phis]
    base_overlaps = [trace_form(base[i], base[(i + 1) % n_loop])
                     for i in range(n_loop)]
    rng = np.random.default_rng(seed)
    f4 = _f4_basis()
    worst_dev = 0.0
    worst_idem = 0.0
    worst_rank = 0.0
    min_oct = math.inf
    for _ in range(n_auto):
        A = random_automorphism(rng, f4, 0.9)
        img = [A @ P for P in base]
        loop_oct = 0.0
        for i in range(n_loop):
            ov = trace_form(img[i], img[(i + 1) % n_loop])
            worst_dev = max(worst_dev, abs(ov - base_overlaps[i]))
            worst_idem = max(worst_idem,
                             float(np.linalg.norm(jordan_product(img[i], img[i])
                                                  - img[i])))
            worst_rank = max(worst_rank, abs(cubic_norm(img[i])))
            loop_oct = max(loop_oct, _octonionic_support(img[i]))
        min_oct = min(min_oct, loop_oct)
    return worst_dev, worst_idem, worst_rank, min_oct


# --------------------------------------------------------------------------- #
#  [C] the half-turn is the SU(2) sign flip                                     #
# --------------------------------------------------------------------------- #
def half_turn_sign(n: int = 4000):
    """Around the great circle the Bargmann product is a NEGATIVE real number:
    e^{i pi} = -1, the spin-1/2 double-cover signature (the vacuum ray returns
    to minus itself).  Returns (real_part, imag_part)."""
    phis = np.linspace(0.0, 2.0 * PI, n, endpoint=False)
    psis = [_coherent(PI / 2.0, p) for p in phis]
    prod = _bargmann_phase(psis)
    # normalise to unit modulus (only the phase carries the geometry)
    prod /= abs(prod)
    return float(prod.real), float(prod.imag)


# --------------------------------------------------------------------------- #
#  Driver                                                                       #
# --------------------------------------------------------------------------- #
def _fmt(x: float, p: int = 6) -> str:
    return f"{x:.{p}f}"


def main() -> bool:
    print("=" * 78)
    print("THE pi, HARDENED -- intrinsic to OP^2, and a half-turn from")
    print("generation-orthogonality (the FORM half of pi/432, pushed off-slice)")
    print("=" * 78)

    # ---- [A] orthogonality origin -----------------------------------------
    pole_overlap, rows, equator_phase = orthogonality_origin()
    # robust to phase sign/wrap: compare on the unit circle (chord distance)
    law_ok = all(abs(complex(math.cos(ph), math.sin(ph))
                     - complex(math.cos(pr), math.sin(pr))) < TOL_PHASE
                 for _, ph, pr in rows)
    monotone = all(rows[i][1] < rows[i + 1][1] for i in range(len(rows) - 1))
    equator_pi = abs(equator_phase - PI) < TOL_PHASE
    print("\n[A] THE HALF-TURN IS FORCED BY GENERATION-ORTHOGONALITY")
    print("    transition-sphere poles = two primitive idempotents E1, E2")
    print("    pole overlap Tr(E1 o E2)          : " + _fmt(pole_overlap, 9)
          + "   (= 0: orthogonal generations)")
    print("    Berry phase law gamma = pi(1 - cos theta):")
    for theta, phase, predicted in rows:
        tag = "  <- great circle (geodesic)" if abs(theta - PI / 2) < 1e-9 else ""
        print("      theta = " + _fmt(theta, 4) + " : gamma = " + _fmt(phase, 5)
              + "   predicted " + _fmt(predicted, 5) + tag)
    print("    equator (equidistant from the two orthogonal generations): "
          + "gamma = " + _fmt(equator_phase, 6) + " = pi: " + str(equator_pi))

    # ---- [B] intrinsic via F4 isometry ------------------------------------
    worst_dev, worst_idem, worst_rank, min_oct = f4_intrinsic()
    isometry_ok = worst_dev < TOL_ISOMETRY
    still_op2 = worst_idem < TOL_IDEM and worst_rank < TOL_RANK
    octonionised = min_oct > MIN_OCTONIONIC
    intrinsic = isometry_ok and still_op2 and octonionised
    print("\n[B] THE pi IS INTRINSIC TO OP^2 (F4-invariant, not a slice artifact)")
    print("    F4 preserves every loop overlap   : worst dev = "
          + _fmt(worst_dev, 2) + "   (isometry: " + str(isometry_ok) + ")")
    print("    transported loop stays rank-one    : |PoP-P| = "
          + _fmt(worst_idem, 2) + ", |N3| = " + _fmt(worst_rank, 2))
    print("    loop leaves the associative slice  : min octonionic support = "
          + _fmt(min_oct, 4) + "   (> " + str(MIN_OCTONIONIC) + ": "
          + str(octonionised) + ")")
    print("    => same metric data on a genuinely octonionic 2-sphere, so the")
    print("       isometry-invariant Berry phase = (1/2)x area is the SAME pi:")
    print("       pi is intrinsic to OP^2: " + str(intrinsic))

    # ---- [C] the SU(2) sign flip ------------------------------------------
    re, im = half_turn_sign()
    sign_flip = (re < -0.999) and (abs(im) < 1e-3)
    print("\n[C] THE HALF-TURN IS THE SU(2) SIGN FLIP")
    print("    great-circle Bargmann product      : " + _fmt(re, 6) + " + "
          + _fmt(im, 6) + " i   (= -1 = e^{i pi})")
    print("    the vacuum ray returns to MINUS itself: " + str(sign_flip)
          + "  (spin-1/2 double cover; cf. epsilon_vcb_halfangle tan(pi/8))")

    # ---- [D] verdict -------------------------------------------------------
    print("\n[D] VERDICT (EXPLORATORY -- FORM hardened, CONTENT still open)")
    print("    The pi is no longer tied to the associative slice it was measured")
    print("    on: it is the F4-INTRINSIC holonomy of OP^2, equal to pi because")
    print("    the great circle is the geodesic separating two ORTHOGONAL")
    print("    generations, and it is the SU(2) half-turn (-1). The kinetic term")
    print("    of pi/432 is now hardened against the octonionic directions.")
    print("    UNCHANGED: the CONTENT half (the three seeds) stays open -- N3 and")
    print("    every F4-invariant is flat on OP^2 (berry_sigma_model_op2), so")
    print("    seed-selection still needs an F4-BREAKING term. No Bayes credit")
    print("    moves; pi/432 is NOT promoted; F0 stays GEOMETRIC/open.")
    print("=" * 78)

    # ---- tripwires (assert the hardened facts; forbid SILENT drift) --------
    assert abs(pole_overlap) < TOL_ORTHO, "the CP^1 poles must be orthogonal generations"
    assert law_ok, "the Berry phase must follow gamma = pi(1 - cos theta)"
    assert monotone, "gamma must rise monotonically to pi as the loop grows to the geodesic"
    assert equator_pi, "the geodesic equator holonomy must be pi"
    assert isometry_ok, "F4 must preserve the loop overlaps (isometry of OP^2)"
    assert still_op2, "the F4-transported loop must stay rank-one idempotents"
    assert octonionised, "the transported loop must leave the associative slice"
    assert intrinsic, "the pi must be intrinsic to OP^2, not a slice artifact"
    assert sign_flip, "the great-circle holonomy must be the -1 SU(2) sign flip"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
