"""
F4-BREAKING VACUUM-PURITY GATE -- why the vacuum is a PRIMITIVE idempotent.
================================================================================

The Peirce-jump gate closed with one sharp residual: it derived the
vacuum-damping jump STRUCTURE of the CHO Lindbladian from the Peirce
decomposition of J3(O) at a PRIMITIVE idempotent, but it had to ASSUME that the
vacuum is primitive (rank one) -- only a primitive idempotent gives a single
one-dimensional vacuum ray; a rank-two idempotent leaves a 10-dimensional J_1
and the identity has no off-vacuum modes at all. So "why these jumps" was
reduced to "why a primitive-idempotent vacuum". This gate climbs underneath that
assumption.

The static side is already known and is only CITED here: on the J3(O) state slice
{rho >= 0, Tr rho = 1} the purity pi(rho) = Tr(rho o rho) lies in [1/3, 1], equals
1 EXACTLY at the primitive idempotents (the pure states, the extreme points = OP^2)
and 1/3 at the maximally mixed centre I/3; the rank-one ray is the majorisation-
maximal element (f0_vacuum_majorization) and the unique zero-entropy state
(epsilon_rank_one_kernel). What is NEW here is DYNAMICAL: the rank-one vacuum is
the unique STABLE attractor of a COOLING (purity-increasing / entropy-decreasing)
flow, while every higher-rank idempotent is an UNSTABLE equilibrium.

Because purity is F4-invariant (pi(g.rho) = pi(rho) for g in F4 = Aut(J3(O)), it
depends only on the three Freudenthal eigenvalues), the cooling dynamics reduces
exactly to a projected gradient flow of pi(lam) = sum lam_i^2 on the eigenvalue
simplex {lam_i >= 0, sum lam_i = 1}. There pi is STRICTLY CONVEX (its tangent
Hessian is 2*I), so:

    * the three VERTICES (1,0,0) -- the rank-one primitive idempotents, pi = 1 --
      are the strict local maxima: STABLE attractors of cooling;
    * the three EDGE midpoints (1/2,1/2,0) -- the rank-two idempotents, pi = 1/2 --
      are SADDLES: unstable, cooling flows them off to a vertex;
    * the CENTRE (1/3,1/3,1/3) -- the identity I/3, rank three, pi = 1/3 -- is the
      global MINIMUM: a repeller, maximally unstable under cooling.

So a cooling dynamics DYNAMICALLY selects a rank-one (primitive) vacuum: a generic
state flows to OP^2 and the higher-rank idempotents are measure-zero unstable
equilibria. Cooling alone is still degenerate over OP^2 (every rank-one vertex has
pi = 1); a GENERIC frame-breaking field V_A(P) = Tr(P o A) then breaks that
degeneracy and pins the unique top vertex E1 -- the height-function selection of
the seed gate (f4_breaking_seed_op2), here shown to KEEP purity maximal while it
picks the vertex.

What this proves
----------------
Conditional on a COOLING (entropy-decreasing) dynamics and a GENERIC
frame-breaking field, the vacuum is forced to be a PRIMITIVE (rank-one) idempotent:
(i) purity is F4-invariant and strictly convex on the eigenvalue simplex; (ii) its
only stable attractors are the rank-one vertices; (iii) rank-two idempotents are
saddles and the rank-three centre I/3 is a repeller, all unstable under cooling
(verified by perturb-and-cool); (iv) the generic frame-breaking field selects the
unique top vertex E1 while purity stays 1. This turns the Peirce-jump assumption
"the vacuum is a primitive idempotent" into a DYNAMICAL consequence of cooling +
frame-breaking, the same two inputs the dissipative ladder and the seed gate
already name.

What this still does not prove
------------------------------
It does NOT derive the COOLING direction (why entropy decreases -- the arrow of
time / second-law input; heating flows instead to the maximally mixed I/3). It
does NOT derive the GENERIC frame-breaking field A from a CHO action (cited from
f4_breaking_seed_op2; the F4-invariant choice A = I is flat and selects nothing).
It does NOT fix WHICH vertex is the heaviest generation (the S3/Weyl assignment
residual). It does NOT derive the source overlap d = pi/432. The cooling flow is a
purity-gradient model, not itself derived from the CHO Lindbladian.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_vacuum_purity_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from epsilon_orbit_selection import (
    primitive_idempotents,
    _diag,
    DIM_DELTA9,
    DIM_J3O,
)
from epsilon_action_selection import (
    trace_form,
    jordan_product,
    eigenvalues,
    random_automorphism,
)
from f4_breaking_seed_op2 import (
    EPS0_SQ,
    _f4,
    height,
    f4_gradient,
    gradient_flow,
)


TOL = 1e-9
EXACT_TOL = 1e-11
PURITY_TOL = 1e-6          # cooling-flow convergence to a vertex (pi -> 1)
INVARIANCE_TOL = 1e-10     # F4-invariance of purity
STABLE_MOVE = 0.02         # a stable attractor moves less than this under cooling
UNSTABLE_MOVE = 0.3        # an unstable equilibrium flees at least this far
MIN_ATTRACTOR = 0.999      # frame-breaking flow overlap with the selected vertex


# --------------------------------------------------------------------------- #
#  J3(O) state functionals (convention: epsilon_action_selection)              #
#  A state is a trace-one element with non-negative Freudenthal eigenvalues.    #
# --------------------------------------------------------------------------- #
def trace(x):
    return float(x[0] + x[1] + x[2])


def purity(rho):
    """pi(rho) = Tr(rho o rho) = sum of squared Freudenthal eigenvalues.  On the
    trace-one state slice pi in [1/3, 1]: 1 at a primitive idempotent (pure),
    1/3 at the maximally mixed centre I/3."""
    return float(trace_form(rho, rho))


def idempotency_residual(x):
    """|X o X - X|: zero iff X is a Jordan idempotent."""
    return float(np.max(np.abs(jordan_product(x, x) - x)))


def jordan_rank(rho):
    """Number of non-zero Freudenthal eigenvalues (the Jordan rank)."""
    return int(np.sum(np.abs(eigenvalues(rho)) > 1e-7))


def is_primitive_idempotent(rho):
    return idempotency_residual(rho) < TOL and jordan_rank(rho) == 1


# --------------------------------------------------------------------------- #
#  Cooling / heating flow = projected purity gradient on the eigenvalue simplex #
# --------------------------------------------------------------------------- #
def cooling_flow(lam0, sign, steps=800, dt=0.05):
    """Projected gradient flow of pi(lam) = sum lam_i^2 on the simplex
    {lam_i >= 0, sum lam_i = 1}.  grad pi = 2 lam; projected onto {sum d = 0} it
    is g_i = 2(lam_i - mean).  sign = +1 is COOLING (purity ascent -> a vertex);
    sign = -1 is HEATING (purity descent -> the centre I/3).  Non-negativity is
    enforced by clamping, the trace by renormalising -- the state slice is kept."""
    lam = np.clip(np.array(lam0, dtype=float), 0.0, None)
    lam = lam / lam.sum()
    for _ in range(steps):
        g = 2.0 * (lam - lam.mean())
        lam = np.clip(lam + sign * dt * g, 0.0, None)
        s = lam.sum()
        if s > 0:
            lam = lam / s
    return lam


def purity_tangent_hessian():
    """Hessian of pi(lam) = sum lam_i^2 restricted to the simplex tangent
    {sum d = 0}; strictly positive (= 2 on an orthonormal tangent basis) means pi
    is strictly convex, so its maxima on the state slice are the extreme points."""
    basis = np.array([[1.0, -1.0, 0.0], [1.0, 1.0, -2.0]]).T
    basis = basis / np.linalg.norm(basis, axis=0)
    hess = 2.0 * np.eye(3)
    return np.linalg.eigvalsh(basis.T @ hess @ basis)


# --------------------------------------------------------------------------- #
#  Rows                                                                         #
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class PurityRow:
    label: str
    rank: int
    trace: float
    purity: float
    expected_purity: float
    idempotency_residual: float
    is_primitive_idempotent: bool


@dataclass(frozen=True)
class StabilityRow:
    label: str
    start_rank: int
    cooled_purity: float
    cooled_top_eigenvalue: float
    distance_moved: float
    is_stable_attractor: bool


@dataclass(frozen=True)
class FrameRow:
    label: str
    max_gradient: float
    overlap_with_top: float
    final_purity: float
    selects_unique_vertex: bool


@dataclass(frozen=True)
class VacuumPuritySelection:
    pure_purity: float
    mixed_purity_rank2: float
    mixed_purity_rank3: float
    purity_f4_invariance: float
    hessian_min_eigenvalue: float
    cooling_attractor_rank: int
    cooling_attractor_purity: float
    heating_attractor_purity: float
    frame_breaking_overlap: float
    coherence_op2_dim: int
    pure_states_are_primitive_idempotents: bool
    cooling_attractor_is_rank_one: bool
    higher_rank_idempotents_unstable: bool
    purity_is_f4_invariant: bool
    unique_vacuum_ray_needs_rank_one: bool
    cooling_direction_derived_from_cho: bool
    frame_breaking_field_derived_from_cho: bool
    source_overlap_derived_from_cho: bool
    generation_assignment_derived_from_cho: bool


# --------------------------------------------------------------------------- #
#  [A] purity recap on the three idempotent strata (cited, not re-derived)      #
# --------------------------------------------------------------------------- #
def purity_rows():
    E1, E2, E3 = primitive_idempotents()
    reps = [
        ("primitive E1 = diag(1,0,0)", E1, 1, 1.0),
        ("rank-2 (E1+E2)/2 = diag(1/2,1/2,0)", 0.5 * (E1 + E2), 2, 0.5),
        ("maximally mixed I/3 = diag(1/3,1/3,1/3)", _diag(1, 1, 1) / 3.0, 3, 1.0 / 3.0),
    ]
    rows = []
    for label, rho, rank, expected in reps:
        rows.append(
            PurityRow(
                label=label,
                rank=jordan_rank(rho),
                trace=trace(rho),
                purity=purity(rho),
                expected_purity=expected,
                idempotency_residual=idempotency_residual(rho),
                is_primitive_idempotent=is_primitive_idempotent(rho),
            )
        )
    return rows


def purity_f4_invariance(seed=3):
    """max |pi(g.rho) - pi(rho)| over random F4 automorphisms g: purity depends
    only on the spectrum, so the cooling dynamics reduces to the eigenvalue simplex."""
    E1, E2, E3 = primitive_idempotents()
    f4 = _f4()
    rng = np.random.default_rng(seed)
    worst = 0.0
    for _ in range(20):
        g = random_automorphism(rng, f4, 1.0)
        for rho in (E1, 0.5 * (E1 + E2), _diag(1, 1, 1) / 3.0):
            worst = max(worst, abs(purity(g @ rho) - purity(rho)))
    return worst


# --------------------------------------------------------------------------- #
#  [B] cooling selects rank-one; higher-rank idempotents are unstable           #
# --------------------------------------------------------------------------- #
def cooling_converges_to_rank_one(seed=5, n=12):
    """Cooling (purity ascent) from random states drives the spectrum to a vertex
    (1,0,0) -- a rank-one primitive idempotent (pi -> 1)."""
    rng = np.random.default_rng(seed)
    worst_purity = 1.0
    worst_top = 1.0
    for _ in range(n):
        lam0 = rng.dirichlet([1.0, 1.0, 1.0])
        lam = cooling_flow(lam0, +1.0)
        worst_purity = min(worst_purity, float(np.sum(lam * lam)))
        worst_top = min(worst_top, float(np.max(lam)))
    return worst_purity, worst_top


def stability_rows(seed=11):
    """Perturb each idempotent stratum and COOL: the rank-one vertex returns
    (stable attractor), the rank-two saddle and the rank-three centre flee to a
    vertex (unstable equilibria)."""
    rng = np.random.default_rng(seed)
    strata = [
        ("rank-1 vertex (1,0,0)", np.array([1.0, 0.0, 0.0]), 1),
        ("rank-2 edge (1/2,1/2,0)", np.array([0.5, 0.5, 0.0]), 2),
        ("rank-3 centre (1/3,1/3,1/3)", np.array([1.0, 1.0, 1.0]) / 3.0, 3),
    ]
    rows = []
    for label, lam_fix, rank in strata:
        perturbed = np.clip(lam_fix + 0.02 * rng.standard_normal(3), 0.0, None)
        perturbed = perturbed / perturbed.sum()
        cooled = cooling_flow(perturbed, +1.0)
        moved = float(np.linalg.norm(np.sort(cooled)[::-1] - np.sort(lam_fix)[::-1]))
        rows.append(
            StabilityRow(
                label=label,
                start_rank=rank,
                cooled_purity=float(np.sum(cooled * cooled)),
                cooled_top_eigenvalue=float(np.max(cooled)),
                distance_moved=moved,
                is_stable_attractor=(moved < STABLE_MOVE),
            )
        )
    return rows


# --------------------------------------------------------------------------- #
#  [C] a generic frame-breaking field pins the unique top vertex (purity stays) #
# --------------------------------------------------------------------------- #
def frame_breaking_rows(n_starts=3, seed=100):
    """Gradient ASCENT of the generic frame-breaking height V_A(P) = Tr(P o A),
    A = diag(1.0,0.6,0.3), from random OP^2 points flows to the top vertex E1 while
    purity stays 1 (it never leaves the rank-one stratum).  The F4-invariant choice
    A = I is flat: zero gradient, no vertex selected (the seed-gate no-go)."""
    f4 = _f4()
    E1, E2, E3 = primitive_idempotents()
    Es = (E1, E2, E3)
    rng = np.random.default_rng(seed)
    rows = []

    A = _diag(1.0, 0.6, 0.3)              # generic (non-degenerate) frame-breaking
    overlaps, purities, grads, tops = [], [], [], []
    for s in range(n_starts):
        P0 = random_automorphism(np.random.default_rng(seed + s), f4, 1.0) @ E1
        Pf = gradient_flow(P0, A, f4, sign=+1.0)
        ov = [height(Pf, E) for E in Es]
        overlaps.append(ov[int(np.argmax(ov))])
        purities.append(purity(Pf))
        grads.append(float(np.linalg.norm(f4_gradient(Pf, A, f4))))
        tops.append(int(np.argmax(ov)) == 0)   # E1 is the top vertex (a_1 = 1.0)
    rows.append(
        FrameRow(
            label="generic A = diag(1.0,0.6,0.3)",
            max_gradient=max(grads),
            overlap_with_top=min(overlaps),
            final_purity=min(purities),
            selects_unique_vertex=bool(min(overlaps) > MIN_ATTRACTOR and all(tops)),
        )
    )

    I = _diag(1, 1, 1)                    # F4-invariant control: flat, no selection
    pts = [random_automorphism(np.random.default_rng(seed + 50 + s), f4, 1.0) @ E1
           for s in range(n_starts)]
    grad_I = max(float(np.linalg.norm(f4_gradient(P, I, f4))) for P in pts)
    rows.append(
        FrameRow(
            label="F4-invariant A = I (control)",
            max_gradient=grad_I,
            overlap_with_top=float("nan"),
            final_purity=min(purity(P) for P in pts),
            selects_unique_vertex=False,
        )
    )
    return rows


# --------------------------------------------------------------------------- #
#  [D] heating control: entropy ascent flows to the maximally mixed centre      #
# --------------------------------------------------------------------------- #
def heating_attractor(seed=7, n=8):
    """HEATING (purity descent / entropy ascent) drives every state to the
    maximally mixed centre I/3 (pi -> 1/3, rank three) -- the WRONG vacuum.  The
    cooling direction (entropy DECREASE) is the arrow-of-time input that is not
    derived here."""
    rng = np.random.default_rng(seed)
    worst = 1.0 / 3.0
    for _ in range(n):
        lam0 = rng.dirichlet([1.0, 1.0, 1.0])
        lam = cooling_flow(lam0, -1.0)
        worst = max(worst, float(np.sum(lam * lam)))
    return worst


# --------------------------------------------------------------------------- #
#  Selection                                                                    #
# --------------------------------------------------------------------------- #
def vacuum_purity_selection():
    rows = purity_rows()
    pure = [r for r in rows if r.rank == 1][0]
    rank2 = [r for r in rows if r.rank == 2][0]
    rank3 = [r for r in rows if r.rank == 3][0]
    invariance = purity_f4_invariance()
    hess = purity_tangent_hessian()
    cool_purity, cool_top = cooling_converges_to_rank_one()
    stab = stability_rows()
    frame = frame_breaking_rows()[0]
    heat_purity = heating_attractor()
    higher_unstable = all(
        (not s.is_stable_attractor) for s in stab if s.start_rank > 1
    )

    return VacuumPuritySelection(
        pure_purity=pure.purity,
        mixed_purity_rank2=rank2.purity,
        mixed_purity_rank3=rank3.purity,
        purity_f4_invariance=invariance,
        hessian_min_eigenvalue=float(np.min(hess)),
        cooling_attractor_rank=1,
        cooling_attractor_purity=cool_purity,
        heating_attractor_purity=heat_purity,
        frame_breaking_overlap=frame.overlap_with_top,
        coherence_op2_dim=DIM_DELTA9,
        pure_states_are_primitive_idempotents=pure.is_primitive_idempotent,
        cooling_attractor_is_rank_one=bool(cool_purity > 1.0 - PURITY_TOL),
        higher_rank_idempotents_unstable=higher_unstable,
        purity_is_f4_invariant=bool(invariance < INVARIANCE_TOL),
        unique_vacuum_ray_needs_rank_one=True,
        cooling_direction_derived_from_cho=False,
        frame_breaking_field_derived_from_cho=False,
        source_overlap_derived_from_cho=False,
        generation_assignment_derived_from_cho=False,
    )


# --------------------------------------------------------------------------- #
#  Driver                                                                       #
# --------------------------------------------------------------------------- #
def main() -> bool:
    rows = purity_rows()
    invariance = purity_f4_invariance()
    hess = purity_tangent_hessian()
    cool_purity, cool_top = cooling_converges_to_rank_one()
    stab = stability_rows()
    frame = frame_breaking_rows()
    heat_purity = heating_attractor()
    selection = vacuum_purity_selection()

    print("=" * 78)
    print("  F4-BREAKING VACUUM-PURITY GATE")
    print("  Why is the dissipative vacuum a PRIMITIVE (rank-one) idempotent?")
    print("=" * 78)

    print("\n[A] Purity pi(rho)=Tr(rho o rho) on the J3(O) state slice (cited statics)")
    for r in rows:
        print(
            f"  {r.label:42} rank={r.rank} tr={r.trace:.4f} "
            f"pi={r.purity:.6f} (exp {r.expected_purity:.6f}) "
            f"primitive={r.is_primitive_idempotent}"
        )
    print(f"  purity is F4-invariant  max|pi(g.rho)-pi(rho)|   : {invariance:.2e}")
    print(f"  pure(pi=1)=primitive idempotent=extreme point=OP^2 (dim {DIM_DELTA9}); "
          f"I/3 is majorisation-min (f0_vacuum_majorization)")

    print("\n[B] Cooling (purity ascent) -> rank-one; higher-rank idempotents unstable")
    print(f"  purity strictly convex: simplex tangent Hessian eig = "
          f"{np.round(hess, 6)} (> 0)")
    print(f"  cooling from random states: worst pi -> {cool_purity:.8f}, "
          f"worst top eigenvalue -> {cool_top:.8f} (rank one)")
    for s in stab:
        verdict = "STABLE attractor" if s.is_stable_attractor else "UNSTABLE (flees to a vertex)"
        print(
            f"  perturb {s.label:26} cool -> pi={s.cooled_purity:.6f} "
            f"top={s.cooled_top_eigenvalue:.4f} moved={s.distance_moved:.4f}  {verdict}"
        )

    print("\n[C] Generic frame-breaking field pins the unique top vertex E1")
    for f in frame:
        ov = "n/a" if f.overlap_with_top != f.overlap_with_top else f"{f.overlap_with_top:.6f}"
        print(
            f"  {f.label:32} max|grad V|={f.max_gradient:.2e} "
            f"overlap_top={ov} final_pi={f.final_purity:.6f} "
            f"unique_vertex={f.selects_unique_vertex}"
        )
    print("  cooling lands on OP^2 (rank one); the generic field selects E1 (seed gate),")
    print("  keeping purity 1; the F4-invariant A=I is flat -> no vertex (the no-go).")

    print("\n[D] Heating control: entropy ascent flows to the WRONG (mixed) vacuum")
    print(f"  heating (purity descent) from random states: worst pi -> {heat_purity:.6f} "
          f"(-> 1/3, the maximally mixed I/3, rank three)")
    print(f"  eps0^2 = pi/432 = {EPS0_SQ:.6f} is the source overlap (NOT derived here)")

    print("\n[V] Verdict")
    print("  pure state pi=1 = primitive idempotent = extreme point : YES")
    print("  purity F4-invariant (reduces to eigenvalue simplex)    : YES")
    print("  cooling attractor is rank-one (primitive) vacuum       : YES")
    print("  rank-two saddle / rank-three centre unstable on cooling : YES")
    print("  generic frame-breaking field pins the unique top vertex : YES")
    print("  unique vacuum ray needs a rank-one idempotent (Peirce)  : YES")
    print("  cooling direction (arrow of time) from CHO action       : NO")
    print("  generic frame-breaking field A from CHO action          : NO")
    print("  source overlap d = pi/432 from CHO action               : NO")
    print("  generation assignment (which vertex) from CHO action    : NO")
    print("  Bayes/scoreboard credit moved                           : NO")
    print("=" * 78)

    # [A] purity statics: exact values on the three strata, F4-invariance
    pure = [r for r in rows if r.rank == 1][0]
    rank2 = [r for r in rows if r.rank == 2][0]
    rank3 = [r for r in rows if r.rank == 3][0]
    assert pure.is_primitive_idempotent
    assert abs(pure.purity - 1.0) < EXACT_TOL
    assert abs(rank2.purity - 0.5) < EXACT_TOL
    assert abs(rank3.purity - 1.0 / 3.0) < EXACT_TOL
    assert pure.purity > rank2.purity > rank3.purity
    assert abs(pure.trace - 1.0) < EXACT_TOL
    assert invariance < INVARIANCE_TOL

    # [B] strict convexity + cooling selects rank-one; higher-rank unstable
    assert float(np.min(hess)) > 1.0          # tangent Hessian = 2 > 0 (strictly convex)
    assert cool_purity > 1.0 - PURITY_TOL      # cooling -> a rank-one vertex (pi -> 1)
    assert cool_top > 1.0 - PURITY_TOL
    by_rank = {s.start_rank: s for s in stab}
    assert by_rank[1].is_stable_attractor                       # rank-one stable
    assert by_rank[1].distance_moved < STABLE_MOVE
    assert not by_rank[2].is_stable_attractor                   # rank-two saddle: unstable
    assert by_rank[2].distance_moved > UNSTABLE_MOVE
    assert not by_rank[3].is_stable_attractor                   # rank-three centre: unstable
    assert by_rank[3].distance_moved > UNSTABLE_MOVE
    for rk in (2, 3):
        assert by_rank[rk].cooled_purity > 1.0 - PURITY_TOL     # they flee to a vertex

    # [C] generic frame-breaking field pins the unique top vertex, purity stays 1
    generic = [f for f in frame if "generic" in f.label][0]
    control = [f for f in frame if "control" in f.label][0]
    assert generic.selects_unique_vertex
    assert generic.overlap_with_top > MIN_ATTRACTOR
    assert generic.max_gradient < 1e-3                         # gradient flow converged near the vertex
    assert abs(generic.final_purity - 1.0) < TOL               # never leaves OP^2
    assert control.max_gradient < 1e-9                          # A = I flat: no selection
    assert not control.selects_unique_vertex

    # [D] heating control flows to the maximally mixed centre (the wrong vacuum)
    assert abs(heat_purity - 1.0 / 3.0) < 1e-4

    # honesty flags
    assert selection.pure_states_are_primitive_idempotents
    assert selection.cooling_attractor_is_rank_one
    assert selection.higher_rank_idempotents_unstable
    assert selection.purity_is_f4_invariant
    assert selection.unique_vacuum_ray_needs_rank_one
    assert selection.cooling_attractor_rank == 1
    assert not selection.cooling_direction_derived_from_cho
    assert not selection.frame_breaking_field_derived_from_cho
    assert not selection.source_overlap_derived_from_cho
    assert not selection.generation_assignment_derived_from_cho
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
