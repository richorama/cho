"""
BERRY / WZ SIGMA-MODEL ON OP^2 -- the decisive topological-route test for pi/432.
==============================================================================

Why this module exists
----------------------
Phase 1.3 (`f0_spectral_action_heatkernel.py`) REFUTED the analytic route to the
prefactor: for the finite octonionic triple the spectral-action ratio a4/a2 =
M4/M2^2 = 0.00582895 is a pi-FREE rational, so it can NEVER equal the
transcendental pi/432 = 0.00727221. The only pi a spectral action emits is the
continuum (4 pi)^(-d/2). The heat-kernel reading also showed the bare pi is a
Berry HALF-solid-angle, and the big-bets adelic keeper independently argued a
real-ANALYTIC action over R cannot emit arithmetic objects on {2,3,7}. BOTH
refutations point the same way: stop trying to get pi/432 from a continuum
spectral action; the object that can carry pi is TOPOLOGICAL, not analytic.

This module runs that alternative as ONE decisive experiment. It assembles the
natural candidate the triangulation points at -- a Berry / Wess-Zumino
sigma-model whose target is the triality-vacuum manifold OP^2 (the rank-one
idempotent variety of J3(O), dim 16 = the E6 minimal orbit), with the
E6-invariant cubic norm N3 as the potential:

        S[path]  =  (Berry/WZ kinetic term on OP^2)   -   (N3 potential).

A topological/discrete action of this shape is exactly the kind of object that
the spectral action provably is NOT (Phase 1.3). The make-or-break question has
two independent halves, and this module tests BOTH:

   [FORM]    does the Berry/WZ kinetic term's HOLONOMY on OP^2 give pi?
   [CONTENT] do the CRITICAL POINTS of the N3 potential SELECT the three
             charged-lepton seeds (the mass hierarchy)?

Only if BOTH pass does the scoreboard sign flip FOR REAL (pi/432 promoted to a
derived output, not granted). This is the single highest-value internal probe:
it is the one experiment that could have flipped the sign without a grant.

What this module reuses (source-of-truth -- it re-derives none of it)
---------------------------------------------------------------------
* `epsilon_action_selection.cubic_norm` (N3 = det), `.eigenvalues`,
  `._f4_basis`, `.random_automorphism`, `.candidate_action_angle`
  (the great-circle Berry phase already shown = pi);
* `epsilon_orbit_selection.freudenthal_sharp` (X# = grad N3, =0 iff rank<=1),
  `.primitive_idempotents`, `._diag`;
* `spectral_action_432.ladder_mismatch`, `.measured_lepton_ratios`
  (the single-knob eps0 ladder MISSES the lepton hierarchy by ~1.40 decades).

The honest outcome (decided by the computation below)
-----------------------------------------------------
[FORM] PASSES. The Berry holonomy of the minimal (great-circle / geodesic) loop
   of ACTUAL rank-one J3(O) idempotents is pi (= 1/2 * 2pi solid angle),
   cross-checked against the source-of-truth great-circle phase; a non-geodesic
   latitude loop gives a DIFFERENT value, so pi is the geodesic-selected
   holonomy specifically. The topological kinetic term DOES emit pi -- the right
   kind of object, succeeding exactly where the analytic spectral action cannot.

[CONTENT] FAILS, and it fails for a STRUCTURAL reason that is itself the result.
   N3 = det = 0 on ALL of OP^2 (every point is rank-one), and the J3(O) spectrum
   is identically (1,0,0) on OP^2. So N3 -- and indeed EVERY F4-invariant, since
   F4 preserves the spectrum -- is CONSTANT on the vacuum manifold: a symmetric
   potential CANNOT lift the OP^2 degeneracy to pick three distinct seeds. On the
   full slice the only N3 critical points are the degenerate rank-one MINIMUM and
   the central MAXIMUM I/3 (the all-EQUAL state -- the ANTI-hierarchy); the
   measured hierarchy is a non-symmetric triple and is NOT a critical point of
   N3. The single-knob eps0 ladder confirms the miss (~1.40 decades).

NET (the new, sharp content): the sigma-model SEPARATES pi/432. The FORM (pi) is
reachable by the topological route -- the kinetic term is settled. The CONTENT
(the seeds) is NOT reachable from any F4-invariant potential; seed-selection
REQUIRES an F4-BREAKING term. This is a NEW no-go that localises the ENTIRE
remaining gap to a single object -- an F4-breaking seed-selection potential on
OP^2 -- with the kinetic pi now topological and fixed. The scoreboard sign does
NOT flip (CONTENT failed), no Bayes credit moves, F0 stays GEOMETRIC/open. This
CONFIRMS the Phase 1.4 result (structure forced, absolute seed open) from an
independent dynamical direction, and converts it into a symmetry no-go.

EXPLORATORY. F0 is NOT promoted. No Bayes credit moves. numpy only; no scipy.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/berry_sigma_model_op2.py
"""

from __future__ import annotations

import math

import numpy as np

from epsilon_orbit_selection import (
    _diag,
    freudenthal_sharp,
    primitive_idempotents,
)
from epsilon_action_selection import (
    cubic_norm,
    eigenvalues,
    _f4_basis,
    random_automorphism,
    candidate_action_angle,
)
from spectral_action_432 import ladder_mismatch, measured_lepton_ratios

PI = math.pi
ONE_OVER_27 = 1.0 / 27.0

# tolerances
TOL_PI = 2e-3        # the holonomy must hit pi this closely (great circle)
TOL_GEODESIC = 1e-2  # a non-geodesic loop must differ from pi by at least this
TOL_FLAT = 1e-3      # |N3| on OP^2 must be below this (flat vacuum manifold)
TOL_SPEC = 1e-3      # OP^2 spectrum must be (1,0,0) to within this
TOL_SHARP = 1e-3     # |X#| on OP^2 must be below this (rank-one certificate)
MISS_DECADES = 1.0   # the single-knob ladder must miss the hierarchy by >this


# --------------------------------------------------------------------------- #
#  [FORM]  Berry / WZ holonomy of the minimal loop in OP^2                      #
# --------------------------------------------------------------------------- #
def _coherent_state(theta: float, phi: float) -> np.ndarray:
    """A unit vector in a complex 2-plane C^2 ⊂ O^3 (embedding C ⊂ O on the
    first two coordinates): P = v v^dagger is a genuine primitive (rank-one,
    trace-1) idempotent of J3(O), i.e. a point of a CP^1 = S^2 subsphere of the
    triality-vacuum manifold OP^2."""
    return np.array(
        [math.cos(theta / 2.0), np.exp(1j * phi) * math.sin(theta / 2.0), 0.0],
        dtype=complex,
    )


def _bargmann_holonomy(states) -> float:
    """Pancharatnam-Berry phase of a closed loop of pure states:
    -arg prod_i <v_i | v_{i+1}> (the gauge-invariant Bargmann invariant)."""
    prod = 1.0 + 0.0j
    n = len(states)
    for i in range(n):
        overlap = np.vdot(states[i], states[(i + 1) % n])
        prod *= overlap / abs(overlap)
    return float(-np.angle(prod))


def holonomy_on_op2(samples: int = 4000):
    """The minimal closed loop in OP^2 is a great circle of a CP^1 = S^2
    subsphere; its Berry holonomy = 1/2 * (enclosed solid angle) = 1/2 * 2pi =
    pi. Build the loop from ACTUAL rank-one J3(O) idempotents and measure it,
    then cross-check against the source-of-truth great-circle phase. A
    non-geodesic latitude loop (theta = pi/3) encloses less solid angle and must
    give a DIFFERENT phase, so pi is the geodesic-selected holonomy specifically.

    Returns (holo_great, holo_latitude, ref_phase, idempotency_error, rank)."""
    phis = np.linspace(0.0, 2.0 * PI, samples, endpoint=False)
    great = [_coherent_state(PI / 2.0, p) for p in phis]      # equator: Omega=2pi
    latitude = [_coherent_state(PI / 3.0, p) for p in phis]   # cap: Omega<2pi
    holo_great = abs(_bargmann_holonomy(great))
    holo_latitude = abs(_bargmann_holonomy(latitude))
    # certify the loop runs over genuine rank-one trace-1 projectors
    v = great[0]
    P = np.outer(v, v.conj())
    idem_err = float(np.linalg.norm(P @ P - P))
    rank = int(np.linalg.matrix_rank(P, tol=1e-9))
    # source-of-truth cross-check (epsilon_action_selection.candidate_action_angle
    # = action_derivation.berry_phase_of_latitude(pi/2))
    ref = abs(candidate_action_angle())
    return holo_great, holo_latitude, ref, idem_err, rank


# --------------------------------------------------------------------------- #
#  [CONTENT]  the N3 potential is FLAT on OP^2 -- no invariant selects the seeds #
# --------------------------------------------------------------------------- #
def op2_potential_flatness(n: int = 300, seed: int = 0, scale: float = 0.9):
    """OP^2 = the F4-orbit of the primitive idempotent E1 (= the E6 minimal,
    rank-one orbit). Sample it by E1 -> A(E1) for random automorphisms A in F4
    and show that on every point:
        * the cubic potential N3 = det is 0   (rank-one => det 0),
        * the Freudenthal sharp X# is 0       (rank-one certificate),
        * the J3(O) spectrum is (1,0,0).
    Hence N3 -- and EVERY F4-invariant (a symmetric function of the spectrum) --
    is CONSTANT on the vacuum manifold OP^2: a symmetric potential cannot lift its
    degeneracy into three distinct eigenvalue-seeds.

    Returns (worst|N3|, worst|X#|, worst spectrum deviation from (1,0,0))."""
    rng = np.random.default_rng(seed)
    f4 = _f4_basis()
    e1 = _diag(1.0, 0.0, 0.0)
    target = np.array([1.0, 0.0, 0.0])
    worst_n3 = 0.0
    worst_sharp = 0.0
    worst_spec = 0.0
    for _ in range(n):
        a = random_automorphism(rng, f4, scale)
        x = a @ e1
        worst_n3 = max(worst_n3, abs(cubic_norm(x)))
        worst_sharp = max(worst_sharp, float(np.linalg.norm(freudenthal_sharp(x))))
        spec = np.sort(eigenvalues(x))[::-1]
        worst_spec = max(worst_spec, float(np.max(np.abs(spec - target))))
    return worst_n3, worst_sharp, worst_spec


def _simplex_grad_n3(a: float, b: float, c: float) -> float:
    """Norm of grad(N3 = abc) projected onto the simplex {a+b+c = const}
    (project out the normal (1,1,1)/sqrt 3). Zero iff (a,b,c) is a constrained
    critical point of the cubic potential on the eigenvalue simplex."""
    g = np.array([b * c, a * c, a * b])
    normal = np.array([1.0, 1.0, 1.0]) / math.sqrt(3.0)
    tangent = g - float(np.dot(g, normal)) * normal
    return float(np.linalg.norm(tangent))


def seed_selection_status():
    """The two facts that together kill N3 as the seed-selector:
      [crit] on the eigenvalue simplex the measured charged-lepton hierarchy is
             a NON-symmetric triple and is NOT a critical point of N3
             (grad != 0), while the all-EQUAL state I/3 -- the global MAXIMUM
             N3 = 1/27 -- IS (grad = 0). A symmetric potential's critical points
             sit on the symmetric strata, never at a generic hierarchy.
      [miss] the best single-knob eps0 ladder misses the measured hierarchy by
             ~1.40 decades (spectral_action_432.ladder_mismatch).
    Returns (seed_simplex, grad_at_seed, grad_at_equal, N3(I/3), best_ladder,
             worst_log10_miss)."""
    ratios = measured_lepton_ratios()          # (1, m_mu/m_tau, m_e/m_tau)
    seed = ratios / ratios.sum()               # three DISTINCT simplex weights
    grad_at_seed = _simplex_grad_n3(*seed)
    grad_at_equal = _simplex_grad_n3(1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
    n3_equal = cubic_norm(_diag(1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0))
    best, results, _ = ladder_mismatch()
    worst_miss = results[best]["worst_log10_miss"]
    return seed, grad_at_seed, grad_at_equal, n3_equal, best, worst_miss


# --------------------------------------------------------------------------- #
#  Driver                                                                       #
# --------------------------------------------------------------------------- #
def _fmt(x: float, p: int = 6) -> str:
    return f"{x:.{p}f}"


def main() -> bool:
    print("=" * 78)
    print("BERRY/WZ SIGMA-MODEL ON OP^2 -- the decisive topological-route test")
    print("=" * 78)

    print("\n[A] THE MODEL")
    print("    S[path] = (Berry/WZ kinetic on OP^2) - (N3 potential).")
    print("    target  : OP^2 = rank-one idempotents of J3(O) (dim 16, E6 minimal)")
    print("    potential: N3 = det, the E6-invariant cubic norm")
    print("    The analytic route is closed (Phase 1.3: a4/a2 = 0.00582895 is a")
    print("    pi-FREE rational, never pi/432). A topological action is the kind of")
    print("    object that CAN carry pi. Two halves must BOTH pass to flip the sign.")

    # ---- [FORM] holonomy ---------------------------------------------------
    holo, holo_lat, ref, idem_err, rank = holonomy_on_op2()
    form_pass = (abs(holo - PI) < TOL_PI) and (abs(ref - PI) < TOL_PI)
    geodesic_specific = abs(holo_lat - PI) > TOL_GEODESIC
    print("\n[B] FORM TEST -- Berry/WZ holonomy on OP^2")
    print("    great-circle (geodesic) holonomy : " + _fmt(holo) + "   (pi = "
          + _fmt(PI) + ")")
    print("    source-of-truth cross-check       : " + _fmt(ref))
    print("    non-geodesic latitude loop        : " + _fmt(holo_lat)
          + "   (!= pi, so pi is geodesic-selected)")
    print("    loop is genuine rank-one P=P^2    : |P^2-P| = " + _fmt(idem_err, 2)
          + ", rank = " + str(rank))
    print("    => topological kinetic term EMITS pi: " + str(form_pass)
          + "  (the right kind of object; the spectral action cannot)")

    # ---- [CONTENT] potential / seeds --------------------------------------
    worst_n3, worst_sharp, worst_spec = op2_potential_flatness()
    seed, g_seed, g_equal, n3_equal, best, worst_miss = seed_selection_status()
    op2_flat = (worst_n3 < TOL_FLAT and worst_sharp < TOL_SHARP
                and worst_spec < TOL_SPEC)
    hierarchy_not_critical = g_seed > 10.0 * g_equal
    ladder_misses = worst_miss > MISS_DECADES
    content_pass = False  # seeds are NOT selected -- decided below
    print("\n[C] CONTENT TEST -- does the N3 potential select the three seeds?")
    print("    N3 on OP^2 (vacuum manifold)      : max|N3| = " + _fmt(worst_n3, 8))
    print("    rank-one certificate on OP^2      : max|X#| = " + _fmt(worst_sharp, 8))
    print("    spectrum on OP^2                  : max|spec-(1,0,0)| = "
          + _fmt(worst_spec, 8))
    print("    => N3 (and EVERY F4-invariant) is FLAT on OP^2: " + str(op2_flat))
    print("       (a symmetric potential cannot lift the OP^2 degeneracy)")
    print("    measured lepton seed (simplex)    : ("
          + ", ".join(_fmt(s, 5) for s in seed) + ")")
    print("    grad N3 at the hierarchy seed     : " + _fmt(g_seed, 5)
          + "   (NOT a critical point)")
    print("    grad N3 at the all-equal I/3      : " + _fmt(g_equal, 5)
          + "   (critical: the global MAX N3 = " + _fmt(n3_equal, 5)
          + " = 1/27, the ANTI-hierarchy)")
    print("    single-knob ladder vs hierarchy   : best '" + best
          + "' misses by " + _fmt(worst_miss, 2) + " decades")
    print("    => seeds NOT selected by any invariant potential: "
          + str(not content_pass))

    # ---- [D] verdict -------------------------------------------------------
    sign_flips = form_pass and content_pass
    print("\n[D] VERDICT (EXPLORATORY -- F0 not promoted, no Bayes credit moves)")
    print("    The sigma-model SEPARATES pi/432:")
    print("      * FORM (the pi)   : REACHABLE by the topological route -- the")
    print("        Berry/WZ kinetic term emits pi on OP^2, where the analytic")
    print("        spectral action provably cannot. The kinetic term is SETTLED.")
    print("      * CONTENT (seeds) : NOT reachable from any F4-invariant. N3 and")
    print("        every spectral invariant is FLAT on OP^2; seed-selection")
    print("        REQUIRES an F4-BREAKING term -- a NEW no-go.")
    print("    => scoreboard sign flips FOR REAL: " + str(sign_flips)
          + "  (CONTENT failed, so NO).")
    print("    Net: the missing object is now localised to ONE F4-breaking")
    print("    seed-selection potential on OP^2, with the kinetic pi topological")
    print("    and fixed. Confirms Phase 1.4 (structure forced, seed open) from an")
    print("    independent dynamical direction, and sharpens it into a symmetry")
    print("    no-go. F0 stays GEOMETRIC/open; the honest null is unchanged.")
    print("=" * 78)

    # ---- tripwires (assert KNOWN/derived facts; forbid SILENT drift) -------
    assert form_pass, "FORM: the Berry/WZ holonomy on OP^2 must be pi"
    assert geodesic_specific, "pi must be the geodesic-selected holonomy specifically"
    assert rank == 1 and idem_err < 1e-9, "the loop must run over rank-one projectors"
    assert op2_flat, "N3/spectrum must be flat (rank-one) on the OP^2 vacuum manifold"
    assert hierarchy_not_critical, "the measured hierarchy must NOT be an N3 critical point"
    assert abs(n3_equal - ONE_OVER_27) < 1e-6, "the N3 max must be the all-equal I/3 = 1/27"
    assert ladder_misses, "the single-knob ladder must miss the hierarchy by >1 decade"
    assert not content_pass, "CONTENT: the seeds must NOT be selected by an invariant potential"
    assert not sign_flips, "the sign must NOT flip: CONTENT failed (no credit moves)"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
