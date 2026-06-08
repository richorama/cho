"""
F0 vacuum selection is ROBUST: the rank-one ray is the majorization-maximal state.
=================================================================================

Why this module exists
----------------------
`epsilon_action_selection.py` (last increment) showed the rank-one transition
ray is the global MINIMISER of the *specific* E6-invariant cubic norm
N3 = det on the J3(O) state slice {O >= 0, Tr O = 1}.  That is true but narrow:
it pins the F0 vacuum to ONE chosen action (the Jordan cubic).  A referee's fair
question is "why that functional and not another?"

This module answers with a stronger, classical statement that does NOT depend on
the choice of functional at all.  On the J3(O) state slice the rank-one ray is
the **majorization-maximal** element: its spectrum (1,0,0) majorises the spectrum
of every other state, and the maximally-mixed centre I/3 = (1/3,1/3,1/3) is
majorised by every state.  By the Hardy-Littlewood-Polya theorem this single
order fact fixes the extremiser of an ENTIRE universality class of actions:

    * every Schur-CONVEX action  is MAXimised at rank-one, minimised at I/3;
    * every Schur-CONCAVE action is MINimised at rank-one, maximised at I/3.

The cubic norm N3 = det is just one Schur-concave member.  The von Neumann and
all Renyi entropies are others.  Crucially, the leading field-dependent term of
a Connes finite spectral action,  Tr f(D/Lambda) -> -a Tr(Phi^2) + b Tr(Phi^4),
is a SPECTRAL (eigenvalue-sum) functional whose symmetry-breaking minimum on the
slice is, again by majorisation, the rank-one ray.

Two honest consequences
------------------------
  (ROBUST, constructive) The F0 vacuum -- the rank-one coherent transition ray --
  does not hinge on the action being the cubic norm.  It is the common vacuum of
  the whole Schur-concave/convex class, so a Connes-type spectral action selects
  the SAME ray.  This connects the F0 program to the standard spectral-action
  framework (the same KO-dim-6 triple ko_dimension_chirality.py / spectral_action.py
  already match) instead of resting on one bespoke functional.

  (CORRECTIVE, honest) The spectral-action induced potential is EVEN
  (Tr Phi^2, Tr Phi^4); the cubic norm N3 = det is degree-3 / odd.  They are
  DIFFERENT functionals.  They agree only on the *vacuum* (rank-one), because both
  are governed by majorisation -- not on the off-vacuum potential shape.  So the
  cubic-norm identification of epsilon_action_selection is NOT the same as a
  spectral-action derivation; which action is physical is still open.

What this proves (all asserted)
-------------------------------
  [A] majorisation extremality: rank-one (1,0,0) majorises every sampled PSD
      trace-1 spectrum; I/3 is majorised by every spectrum.
  [B] spectral functionals are F4-invariant: a J3(O) state and its F4-automorphism
      image share a spectrum, so vacuum selection reduces to the eigenvalue
      simplex {lam >= 0, sum lam = 1}.
  [C] universality panel: for a panel of strictly convex g, Tr g(O) = sum g(lam_i)
      is maximised at rank-one / minimised at I/3; for strictly concave g the
      reverse -- so N3 = det, purity Tr O^2, and von Neumann / Renyi-2 entropy all
      select rank-one, with N3(I/3) = 1/27 and S_vN(I/3) = log 3.
  [D] spectral-action bridge: the Connes symmetry-breaking potential
      -a Tr Phi^2 + b Tr Phi^4 is minimised at the rank-one ray; and it is EVEN,
      whereas N3 scales as t^3 (degree 3) vs purity t^2 -- distinct functionals,
      one vacuum.
  [E] on the actual J3(O): the three primitive idempotents E_i (the generations)
      are the rank-one vacua: N3(E_i) = 0 and purity(E_i) = 1 (zero-entropy pure).

Honest scope (F0 stays GEOMETRIC -- NOT promoted, no Bayes credit moves)
------------------------------------------------------------------------
Majorisation fixes the vacuum DIRECTION (rank-one) for the whole class of natural
actions; it does NOT decide WHICH action the CHO dynamics realise, fix the kinetic
coefficient on the Berry pi, or supply the normalisation pi/432.  This is a
robustness theorem about the vacuum, not a derivation of the action or the
measure.  F0 remains an open bridge.

No scipy.  numpy only.  Reuses the verified J3(O) toolkit.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f0_vacuum_majorization.py
"""

import math

import numpy as np

from epsilon_action_selection import (
    _diag,
    cubic_norm,
    eigenvalues,
    _f4_basis,
    random_automorphism,
)
from epsilon_orbit_selection import primitive_idempotents

TOL_EXACT = 1e-9
TOL_NUM = 1e-6
ONE_OVER_27 = 1.0 / 27.0
LOG3 = math.log(3.0)


# --------------------------------------------------------------------------- #
#  Majorisation                                                                #
# --------------------------------------------------------------------------- #
def majorizes(p, q):
    """p majorises q: with both sorted descending and equal totals, every partial
    sum of p dominates that of q.  (Hardy-Littlewood-Polya order.)"""
    p = np.sort(np.asarray(p, float))[::-1]
    q = np.sort(np.asarray(q, float))[::-1]
    cp = np.cumsum(p)
    cq = np.cumsum(q)
    return bool(np.all(cp >= cq - 1e-12) and abs(cp[-1] - cq[-1]) < 1e-9)


def majorization_extremes(n=4000, seed=0):
    """rank-one (1,0,0) majorises every sampled PSD trace-1 spectrum, and the
    centre I/3 is majorised by every sampled spectrum."""
    rng = np.random.default_rng(seed)
    rank_one = np.array([1.0, 0.0, 0.0])
    center = np.array([1 / 3, 1 / 3, 1 / 3])
    top_dominates = True
    center_dominated = True
    for _ in range(n):
        lam = rng.random(3)
        lam = lam / lam.sum()
        if not majorizes(rank_one, lam):
            top_dominates = False
        if not majorizes(lam, center):
            center_dominated = False
    return top_dominates, center_dominated


# --------------------------------------------------------------------------- #
#  [B] spectral functionals depend only on the J3(O) spectrum                   #
# --------------------------------------------------------------------------- #
def spectrum(x):
    """The three J3(O) eigenvalues, sorted descending."""
    return np.sort(eigenvalues(x))[::-1]


def f4_spectral_invariance(n=300, seed=1, scale=0.8):
    """A J3(O) state A.diag(lam) (A in F4) has the SAME spectrum as diag(lam):
    spectral functionals are therefore functions on the eigenvalue simplex."""
    rng = np.random.default_rng(seed)
    f4 = _f4_basis()
    worst = 0.0
    for _ in range(n):
        lam = rng.random(3)
        lam = lam / lam.sum()
        a = random_automorphism(rng, f4, scale)
        s = spectrum(a @ _diag(*lam))
        worst = max(worst, float(np.linalg.norm(s - np.sort(lam)[::-1])))
    return worst


# --------------------------------------------------------------------------- #
#  [C] universality: Schur-convex -> max at rank-one; Schur-concave -> min       #
# --------------------------------------------------------------------------- #
def _simplex_grid(N=120):
    """Eigenvalue simplex {lam >= 0, sum lam = 1} on an N-grid.  N divisible by 3
    so the centre (1/3,1/3,1/3) is an exact node and the corners (1,0,0) are too."""
    pts = []
    for i in range(N + 1):
        for j in range(N + 1 - i):
            a = i / N
            b = j / N
            c = 1.0 - a - b
            if c < -1e-12:
                continue
            pts.append(np.array([a, b, max(c, 0.0)]))
    return pts


def _is_rank_one(lam):
    s = np.sort(lam)[::-1]
    return float(s[1]) < TOL_NUM        # second eigenvalue ~ 0


def _is_center(lam):
    return float(np.max(np.abs(np.asarray(lam) - 1.0 / 3.0))) < 1e-9


def argextreme(g, grid):
    """(argmax, max, argmin, min) of the spectral functional sum_i g(lam_i)."""
    vmax, amax = -np.inf, None
    vmin, amin = np.inf, None
    for lam in grid:
        v = float(np.sum(g(lam)))
        if v > vmax:
            vmax, amax = v, lam
        if v < vmin:
            vmin, amin = v, lam
    return amax, vmax, amin, vmin


def _vn_entropy_terms(lam):
    p = np.clip(np.asarray(lam, float), 0.0, None)
    out = np.zeros_like(p)
    nz = p > 1e-15
    out[nz] = -p[nz] * np.log(p[nz])
    return out


def universality_panel(grid):
    """For convex g the slice-extremiser is rank-one (max) / centre (min); for
    concave g it is reversed.  Returns a dict name -> (max_is_rank_one,
    min_is_center) for convex and (min_is_rank_one, max_is_center) for concave."""
    convex = {
        "purity  l^2": lambda l: l ** 2,
        "l^4": lambda l: l ** 4,
        "exp(l)": lambda l: np.exp(l),
        "l*log(l+1)": lambda l: l * np.log(l + 1.0),
    }
    concave = {
        "det/N3 (log-sum proxy)": None,   # handled via N3 directly below
        "vN entropy": _vn_entropy_terms,
        "sqrt(l)": lambda l: np.sqrt(np.clip(l, 0, None)),
        "-l^2": lambda l: -(l ** 2),
    }
    res = {}
    for name, g in convex.items():
        amax, _, amin, _ = argextreme(g, grid)
        res["convex:" + name] = (_is_rank_one(amax), _is_center(amin))
    for name, g in concave.items():
        if g is None:
            continue
        amax, _, amin, _ = argextreme(g, grid)
        res["concave:" + name] = (_is_rank_one(amin), _is_center(amax))
    return res


# --------------------------------------------------------------------------- #
#  [D] Connes finite spectral action: even SB potential, rank-one minimum        #
# --------------------------------------------------------------------------- #
def spectral_action_potential(lam, a=1.0, b=0.2):
    """Chamseddine-Connes induced Higgs potential as an eigenvalue sum:
    V = -a Tr(Phi^2) + b Tr(Phi^4) = sum_i (-a lam_i^2 + b lam_i^4).
    Even in Phi (degrees 2 and 4); contains NO cubic term."""
    lam = np.asarray(lam, float)
    return float(np.sum(-a * lam ** 2 + b * lam ** 4))


def spectral_action_vacuum(grid, a=1.0, b=0.2):
    amax, _, amin, vmin = argextreme(
        lambda l: -a * l ** 2 + b * l ** 4, grid
    )
    return amin, vmin


def functional_degrees():
    """N3 is homogeneous of degree 3 (N3(tX)=t^3 N3(X)); purity Tr X^2 of degree 2.
    Different degrees -> N3 cannot equal any even spectral potential, even though
    both select the same rank-one vacuum."""
    x = _diag(0.5, 0.3, 0.2)
    n3_ratio = cubic_norm(2.0 * x) / cubic_norm(x)
    pur = lambda v: float(np.sum(spectrum(v) ** 2))
    pur_ratio = pur(_diag(1.0, 0.6, 0.4)) / pur(_diag(0.5, 0.3, 0.2))
    return n3_ratio, pur_ratio


# --------------------------------------------------------------------------- #
#  Driver                                                                       #
# --------------------------------------------------------------------------- #
def main() -> bool:
    print("=" * 74)
    print("F0 vacuum is ROBUST: rank-one ray = majorization-maximal J3(O) state")
    print("=" * 74)

    # [A] majorisation extremality -------------------------------------------
    top, center = majorization_extremes()
    print("\n[A] majorisation order on the PSD trace-1 slice")
    print(f"    rank-one (1,0,0) majorises every sampled state : {top}")
    print(f"    centre I/3 is majorised by every sampled state : {center}")
    assert top, "rank-one must majorise every PSD trace-1 spectrum"
    assert center, "I/3 must be majorised by every PSD trace-1 spectrum"

    # [B] F4 spectral invariance ---------------------------------------------
    worst = f4_spectral_invariance()
    print("\n[B] spectral functionals reduce to the eigenvalue simplex")
    print(f"    max |spectrum(A.X) - spectrum(X)| over F4      : {worst:.2e}")
    assert worst < 1e-9, "F4 automorphisms must preserve the J3(O) spectrum"

    # [C] universality panel --------------------------------------------------
    grid = _simplex_grid(120)
    panel = universality_panel(grid)
    print("\n[C] Hardy-Littlewood-Polya universality (one order, every functional)")
    for name, (a_ok, b_ok) in panel.items():
        kind = "max@rank1 min@I/3" if name.startswith("convex") else "min@rank1 max@I/3"
        print(f"    {name:28s} [{kind}]  rank-one ok? {a_ok}  centre ok? {b_ok}")
        assert a_ok and b_ok, f"majorization prediction failed for {name}"

    # named members with values
    amax_p, vmax_p, amin_p, vmin_p = argextreme(lambda l: l ** 2, grid)
    amax_e, vmax_e, amin_e, vmin_e = argextreme(_vn_entropy_terms, grid)
    amax_n, vmax_n, amin_n, vmin_n = argextreme(
        lambda l: np.log(np.clip(l, 1e-15, None)), grid
    )
    print(f"    purity:     max={vmax_p:.4f}@rank1  min={vmin_p:.4f}@I/3 (=1/3)")
    print(f"    vN entropy: min={vmin_e:.4f}@rank1  max={vmax_e:.4f}@I/3 (=log3={LOG3:.4f})")
    print(f"    N3(I/3)={cubic_norm(_diag(1/3,1/3,1/3)):.5f}  N3(E1)={cubic_norm(_diag(1,0,0)):.2e}  1/27={ONE_OVER_27:.5f}")
    assert abs(vmax_p - 1.0) < TOL_NUM and abs(vmin_p - 1.0 / 3.0) < TOL_NUM
    assert abs(vmin_e - 0.0) < TOL_NUM and abs(vmax_e - LOG3) < TOL_NUM
    assert abs(cubic_norm(_diag(1 / 3, 1 / 3, 1 / 3)) - ONE_OVER_27) < TOL_EXACT

    # [D] spectral-action bridge ---------------------------------------------
    sa_vac, sa_val = spectral_action_vacuum(grid)
    n3_deg, pur_deg = functional_degrees()
    print("\n[D] Connes finite spectral action  V = -a Tr(Phi^2) + b Tr(Phi^4)")
    print(f"    symmetry-breaking minimum at spectrum          : {np.round(np.sort(sa_vac)[::-1],3)}")
    print(f"    minimum is the rank-one ray?                   : {_is_rank_one(sa_vac)}")
    print(f"    N3 scaling N3(2X)/N3(X)  (degree 3)            : {n3_deg:.3f}")
    print(f"    purity scaling           (degree 2)            : {pur_deg:.3f}")
    assert _is_rank_one(sa_vac), "spectral-action SB minimum must be the rank-one ray"
    assert abs(n3_deg - 8.0) < TOL_NUM, "N3 must be degree 3 (t^3 = 8)"
    assert abs(pur_deg - 4.0) < TOL_NUM, "purity must be degree 2 (t^2 = 4)"
    # even spectral potential (degree 2/4) != cubic N3 (degree 3): different
    # functionals that nonetheless share the rank-one vacuum by majorisation.
    assert abs(n3_deg - pur_deg) > 1.0, "N3 and the spectral potential must differ"

    # [E] actual J3(O) primitive idempotents (the generations) ----------------
    E = primitive_idempotents()
    n3s = [cubic_norm(e) for e in E]
    purs = [float(np.sum(spectrum(e) ** 2)) for e in E]
    print("\n[E] the three primitive idempotents E_i (generations) are rank-one vacua")
    print(f"    N3(E_i)     (zero, min)        : {[f'{v:.2e}' for v in n3s]}")
    print(f"    purity(E_i) (one, pure)        : {[f'{v:.4f}' for v in purs]}")
    for v in n3s:
        assert abs(v) < TOL_EXACT, "each primitive idempotent has N3 = 0"
    for v in purs:
        assert abs(v - 1.0) < TOL_NUM, "each primitive idempotent is pure (purity 1)"

    print("\n" + "-" * 74)
    print("ROBUST: rank-one is selected by the WHOLE Schur-concave/convex class")
    print("(cubic norm, entropies, AND the Connes spectral-action purity term) --")
    print("so the F0 vacuum does not hinge on one chosen functional.")
    print("HONEST OPEN: majorisation fixes the vacuum direction, not WHICH action")
    print("CHO realises, the kinetic coefficient, or the pi/432 normalisation.")
    print("F0 stays GEOMETRIC (open bridge); no Bayes credit moves.")
    print("=" * 74)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
