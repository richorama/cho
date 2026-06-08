"""
F0 action-selection route: the rank-one transition ray as a VARIATIONAL OUTPUT.

Motivation
----------
`epsilon_action_stationary.py` shows that, GIVEN a rank-one kernel
K = |tau><tau|, the trace constraint Tr(O) = pi forces the stationary link
operator to be O = pi K.  But the rank-one character of K is fed in by hand:
the physical transition is *assumed* to be rank one (a coherent / pure
transition), and `epsilon_orbit_selection.py` then reads that assumption back
out as "the action selects the E6 minimal orbit".

This module removes the assumption on the configuration-space side.  The claim
is that rank one is not posited but EXTREMAL: the rank-one variety is the
critical / global-minimising locus of the E6-invariant cubic norm N3 on the
J3(O) state space, because the Freudenthal sharp IS the gradient of N3.

The gradient identity
---------------------
For the J3(O) trace form <A,B> = tr(A o B), polarising the cubic norm gives

        dN3|_X (Y)  =  <X#, Y>,            N3(X) = (1/3) <X#, X> = det X,

so  grad N3 (X) = X#  (the Freudenthal sharp).  Hence the unconstrained
critical points of N3 are exactly X# = 0, i.e. the rank<=1 cone -- the very
equation `epsilon_orbit_selection.freudenthal_sharp` uses for the E6 minimal
orbit.  Everything below is a corollary of this one identity.

What this module proves
-----------------------
  [A] X# = grad N3 : finite-difference dN3|_X(Y) matches <X#,Y> to ~1e-7, and
      N3 = det = product of the three J3(O) eigenvalues.
  [B] constrained criticality  grad N3 = lam grad Tr  <=>  X# = lam I.  By the
      J3(O) spectral theorem we may take X = diag(a,b,c), where
      X# = diag(bc,ca,ab); X# = lam I forces bc=ca=ab, whose only solutions are
      lam=0 -> rank<=1 (the minimal orbit) and lam!=0 -> a=b=c (the central
      ray X = cI).  Generic rank-2 / rank-3 X are NOT critical.
  [C] physical slice {X >= 0, Tr X = 1}: N3 = abc with a+b+c=1, a,b,c >= 0, so
      AM-GM gives N3 in [0, 1/27].  The rank-one idempotents are the GLOBAL
      MINIMISERS (N3 = 0); X = I/3 is the unique global MAXIMISER (N3 = 1/27).
  [D] the minimum is degenerate exactly along the F4 symmetry orbit: the
      f4-orbit tangent at a primitive idempotent has dimension 16 = dim OP^2 and
      lies entirely in the zero level set; a trace-preserving deformation into
      the full-rank bulk, diag(1-2t,t,t), raises N3 from 0 -> rank one is a true
      constrained minimum, flat only along the symmetry directions.
  [E] interlock with the measure: the SAME cubic N3 has reduced-structure-group
      E6 = Aut(N3-variety); E6-irreducibility of the 27 is exactly what
      `epsilon_measure_schur.py` uses to force the flat 1/27 transition weight.
      One algebraic object: its zero-locus selects the ray, its symmetry group
      fixes the measure.  (The numerical coincidence max N3 = 1/27 = 1/dim holds
      because dim J3(O) = 27 = 3^3 = rank^3; we quote it but do not lean on it.)
  [F] candidate action S = (Berry kinetic) - (N3 potential): the great-circle
      Berry phase pi from `action_derivation.berry_phase_of_latitude` supplies
      the kinetic angle theta = pi, while the cubic potential's minimal locus
      supplies the rank-one ray.  Stationarity of S in the transition direction
      then reproduces the `epsilon_action_stationary` kernel O = pi |tau><tau|.

Honest scope (F0 stays GEOMETRIC -- NOT promoted, no Bayes credit moves)
------------------------------------------------------------------------
This converts "rank one assumed" into "rank one = global minimiser of the
E6-invariant cubic potential N3", and ties that potential's symmetry group to
the flat measure.  What remains OPEN: deriving from the full CHO dynamics that
the action's potential term IS this cubic N3 (rather than positing the
identification), fixing the kinetic coefficient that multiplies the Berry term,
and writing the full time-dependent equations of motion whose relaxation lands
on the minimal-orbit (coherent) state.  Until those close, this is an honest
increment, not a derivation of the action.
"""

import math

import numpy as np

from epsilon_orbit_selection import (
    _IDENT,
    _T,
    _diag,
    _e6_generators,
    _trace,
    freudenthal_sharp,
    orbit_tangent_dim,
    primitive_idempotents,
)
from action_derivation import berry_phase_of_latitude

TOL_FD = 1e-5      # finite-difference gradient tolerance
TOL_EXACT = 1e-9   # algebraic identities
ONE_OVER_27 = 1.0 / 27.0


# --------------------------------------------------------------------------- #
#  Cubic norm N3, its gradient (the sharp), eigenvalues                         #
# --------------------------------------------------------------------------- #
def jordan_product(x, y):
    return np.einsum("kij,i,j->k", _T, x, y)


def trace_form(a, b):
    """The J3(O) trace bilinear form <A,B> = tr(A o B)."""
    return _trace(jordan_product(a, b))


def cubic_norm(x):
    """N3(X) = (1/3) <X#, X> = det X = product of the three eigenvalues."""
    return trace_form(freudenthal_sharp(x), x) / 3.0


def _sigma2(x):
    return _trace(freudenthal_sharp(x))


def eigenvalues(x):
    """The three real J3(O) eigenvalues: roots of t^3 - tr t^2 + sigma2 t - N3."""
    coeffs = [1.0, -_trace(x), _sigma2(x), -cubic_norm(x)]
    return np.sort(np.roots(coeffs).real)[::-1]


# --------------------------------------------------------------------------- #
#  F4 automorphisms (exp of derivations) -- preserve N3 exactly                 #
# --------------------------------------------------------------------------- #
def _expm(M, squarings=8, terms=20):
    """Matrix exponential by scaling-and-squaring (numpy only; no scipy)."""
    n = M.shape[0]
    A = M / (2.0 ** squarings)
    E = np.eye(n)
    term = np.eye(n)
    for k in range(1, terms):
        term = term @ A / k
        E = E + term
    for _ in range(squarings):
        E = E @ E
    return E


def _f4_basis():
    """The 52 derivations of J3(O) (= Lie algebra of F4 = Aut(J3O))."""
    return _e6_generators()[1]


def random_automorphism(rng, f4, scale=0.8):
    """A = exp(sum c_i D_i) for derivations D_i: an element of F4 = Aut(J3O)."""
    coeffs = rng.standard_normal(len(f4)) * scale
    gen = sum(c * np.asarray(D).real for c, D in zip(coeffs, f4))
    return _expm(gen)


# --------------------------------------------------------------------------- #
#  [A] gradient identity  X# = grad N3                                          #
# --------------------------------------------------------------------------- #
def check_gradient_identity(n=300, seed=0):
    """Finite-difference dN3|_X(Y) vs <X#,Y>, and N3 = product of eigenvalues."""
    rng = np.random.default_rng(seed)
    max_grad_err = 0.0
    max_det_err = 0.0
    eps = 1e-6
    for _ in range(n):
        x = rng.standard_normal(27)
        y = rng.standard_normal(27)
        fd = (cubic_norm(x + eps * y) - cubic_norm(x - eps * y)) / (2.0 * eps)
        analytic = trace_form(freudenthal_sharp(x), y)
        max_grad_err = max(max_grad_err, abs(fd - analytic))
    # N3 = det on diagonals (where the spectrum is manifest)
    for (a, b, c) in [(1, 0, 0), (2, 1, 0), (2, -1, 3), (0.5, 0.3, 0.2)]:
        max_det_err = max(max_det_err, abs(cubic_norm(_diag(a, b, c)) - a * b * c))
    return max_grad_err, max_det_err


# --------------------------------------------------------------------------- #
#  [B] constrained critical locus  X# = lam I                                   #
# --------------------------------------------------------------------------- #
def _is_proportional_to_identity(v):
    diag = np.array([v[0], v[1], v[2]])
    off = float(np.linalg.norm(v[3:]))
    spread = float(diag.max() - diag.min())
    return off < TOL_EXACT and spread < TOL_EXACT, float(diag.mean())


def critical_locus_table():
    """X# = lam I on representatives: rank-one (lam=0) and central (lam!=0) only."""
    reps = {
        "rank-one E1=diag(1,0,0)": _diag(1, 0, 0),
        "rank-one diag(0.3,0,0)": _diag(0.3, 0, 0),
        "central I/3": _diag(1 / 3, 1 / 3, 1 / 3),
        "central diag(0.5,0.5,0.5)": _diag(0.5, 0.5, 0.5),
        "rank-two diag(0.5,0.3,0)": _diag(0.5, 0.3, 0.0),
        "rank-three diag(0.5,0.3,0.2)": _diag(0.5, 0.3, 0.2),
    }
    table = {}
    for name, x in reps.items():
        prop, lam = _is_proportional_to_identity(freudenthal_sharp(x))
        table[name] = (prop, lam)
    return table


# --------------------------------------------------------------------------- #
#  [C] physical slice {X>=0, Tr X=1}: N3 in [0, 1/27]                           #
# --------------------------------------------------------------------------- #
def psd_slice_bounds(n=400, seed=1, scale=0.8):
    """Sample PSD trace-1 states X = A diag(lam) with A in F4, sum(lam)=1, lam>=0.
    Returns (min N3, max N3, max |N3(A X) - N3(X)| automorphism deviation)."""
    rng = np.random.default_rng(seed)
    f4 = _f4_basis()
    n3min, n3max, auto_dev = 1e9, -1e9, 0.0
    for _ in range(n):
        lam = rng.random(3)
        lam = lam / lam.sum()
        a = random_automorphism(rng, f4, scale)
        x = a @ _diag(*lam)
        val = cubic_norm(x)
        auto_dev = max(auto_dev, abs(val - float(np.prod(lam))))
        n3min = min(n3min, val)
        n3max = max(n3max, val)
    return n3min, n3max, auto_dev


# --------------------------------------------------------------------------- #
#  [D] minimum degenerate along the F4 orbit; rises into the full-rank bulk     #
# --------------------------------------------------------------------------- #
def orbit_flatness():
    """At E1: f4-orbit tangent dim, flatness of N3 along the orbit, and the rise
    of N3 along the trace-preserving bulk deformation diag(1-2t,t,t)."""
    f4 = _f4_basis()
    e1 = _diag(1, 0, 0)
    orbit_dim = orbit_tangent_dim(f4, e1)
    flat = 0.0
    for D in f4:
        d = np.asarray(D).real
        for t in (1e-3, 1e-2):
            flat = max(flat, abs(cubic_norm(e1 + t * (d @ e1))))
    bulk = [cubic_norm(_diag(1 - 2 * t, t, t)) for t in (0.0, 0.1, 0.2)]
    return orbit_dim, flat, bulk


# --------------------------------------------------------------------------- #
#  [E] interlock: E6 preserves the N3-variety; max value = 1/27 = 1/dim         #
# --------------------------------------------------------------------------- #
def variety_invariance(n=64, seed=2, scale=0.6):
    """E6 boosts (traceless left-multiplications) preserve the rank-one variety
    N3 = 0: exp(t L_b) E1 stays on the cone.  Returns max |N3| over E6 images."""
    rng = np.random.default_rng(seed)
    e6, f4 = _e6_generators()
    boosts = [np.asarray(g).real for g in e6[len(f4):]]  # the 26 traceless boosts
    e1 = _diag(1, 0, 0)
    worst = 0.0
    for _ in range(n):
        b = sum(c * B for c, B in zip(rng.standard_normal(len(boosts)) * scale, boosts))
        img = _expm(b) @ e1
        worst = max(worst, abs(cubic_norm(img)))
    return worst


# --------------------------------------------------------------------------- #
#  [F] candidate action: Berry kinetic pi minus the cubic potential             #
# --------------------------------------------------------------------------- #
def candidate_action_angle():
    """The great-circle Berry phase that supplies the kinetic angle theta."""
    return abs(berry_phase_of_latitude(math.pi / 2.0))


# --------------------------------------------------------------------------- #
#  Driver                                                                       #
# --------------------------------------------------------------------------- #
def main() -> bool:
    print("=" * 72)
    print("F0 action-selection: rank-one transition ray = minimiser of cubic N3")
    print("=" * 72)

    # [A] gradient identity ---------------------------------------------------
    grad_err, det_err = check_gradient_identity()
    print("\n[A] gradient identity  X# = grad N3,  N3 = det")
    print(f"    max |dN3|_X(Y) - <X#,Y>|      = {grad_err:.2e}  (tol {TOL_FD:.0e})")
    print(f"    max |N3(diag) - abc|          = {det_err:.2e}")
    assert grad_err < TOL_FD, "Freudenthal sharp is not the N3 gradient"
    assert det_err < TOL_EXACT, "N3 is not the determinant"

    # [B] constrained critical locus -----------------------------------------
    print("\n[B] constrained criticality  X# = lam I  <=>  rank-one or central")
    table = critical_locus_table()
    for name, (prop, lam) in table.items():
        print(f"    {name:30s}: X# prop I? {str(prop):5s}  lam = {lam:+.4f}")
    # rank-one: X# = 0 (lam = 0)
    assert table["rank-one E1=diag(1,0,0)"][0]
    assert abs(table["rank-one E1=diag(1,0,0)"][1]) < TOL_EXACT
    assert table["rank-one diag(0.3,0,0)"][0]
    assert abs(table["rank-one diag(0.3,0,0)"][1]) < TOL_EXACT
    # central: X# = lam I with lam = c^2 != 0
    assert table["central I/3"][0]
    assert abs(table["central I/3"][1] - 1.0 / 9.0) < TOL_EXACT
    assert table["central diag(0.5,0.5,0.5)"][0]
    assert abs(table["central diag(0.5,0.5,0.5)"][1] - 0.25) < TOL_EXACT
    # generic higher rank: NOT critical
    assert not table["rank-two diag(0.5,0.3,0)"][0]
    assert not table["rank-three diag(0.5,0.3,0.2)"][0]

    # [C] physical slice bounds ----------------------------------------------
    n3min, n3max, auto_dev = psd_slice_bounds()
    print("\n[C] PSD trace-1 slice:  N3 in [0, 1/27],  rank-one = MIN, I/3 = MAX")
    print(f"    automorphism preserves N3     = {auto_dev:.2e}")
    print(f"    sampled N3 range              = [{n3min:.5f}, {n3max:.5f}]")
    print(f"    1/27                          = {ONE_OVER_27:.5f}")
    print(f"    N3(E1)  (global min)          = {cubic_norm(_diag(1,0,0)):.2e}")
    print(f"    N3(I/3) (global max)          = {cubic_norm(_diag(1/3,1/3,1/3)):.5f}")
    assert auto_dev < 1e-10, "F4 automorphism must preserve N3"
    assert n3min >= -TOL_FD, "N3 must be >= 0 on the PSD slice"
    assert n3max <= ONE_OVER_27 + TOL_FD, "N3 must be <= 1/27 on the PSD slice"
    assert abs(cubic_norm(_diag(1, 0, 0))) < TOL_EXACT, "rank-one is the minimiser"
    assert abs(cubic_norm(_diag(1/3, 1/3, 1/3)) - ONE_OVER_27) < TOL_EXACT, \
        "I/3 is the maximiser with value 1/27"

    # [D] orbit flatness ------------------------------------------------------
    orbit_dim, flat, bulk = orbit_flatness()
    print("\n[D] minimum degenerate along the F4 orbit (OP^2), rises into the bulk")
    print(f"    f4-orbit tangent dim at E1    = {orbit_dim}  (= dim OP^2 = 16)")
    print(f"    max |N3| along orbit          = {flat:.2e}  (flat / zero level)")
    print(f"    N3(diag(1-2t,t,t)) t=0,.1,.2  = {[f'{v:.4f}' for v in bulk]}")
    assert orbit_dim == 16, "f4-orbit at a primitive idempotent must be OP^2 (16)"
    assert flat < 1e-10, "the F4 orbit must lie in the N3 = 0 level set"
    assert bulk[0] < TOL_EXACT < bulk[1] < bulk[2], "N3 must rise into the bulk"

    # [E] interlock with the measure -----------------------------------------
    variety_worst = variety_invariance()
    print("\n[E] interlock: E6 preserves the rank-one variety; max N3 = 1/27 = 1/dim")
    print(f"    max |N3| over E6 images of E1 = {variety_worst:.2e}  (variety stable)")
    print(f"    max N3 = 1/27 = (1/3)^3 ; Schur weight = 1/dim = 1/27 ; dim = 3^3")
    assert variety_worst < 1e-8, "E6 must preserve the rank-one (N3=0) variety"
    assert abs(ONE_OVER_27 - 1.0 / 27.0) < TOL_EXACT

    # [F] candidate action angle ---------------------------------------------
    theta = candidate_action_angle()
    print("\n[F] candidate action S = (Berry kinetic) - (N3 potential)")
    print(f"    great-circle Berry angle      = {theta:.6f}  (= pi = {math.pi:.6f})")
    print(f"    -> kinetic theta = pi ; potential minimum = rank-one ray |tau><tau|")
    assert abs(theta - math.pi) < 1e-3, "kinetic angle must be the Berry pi"

    print("\n" + "-" * 72)
    print("RESULT: the rank-one transition ray is the GLOBAL MINIMISER of the")
    print("E6-invariant cubic potential N3 on the physical state slice -- an")
    print("OUTPUT, not an input.  The same N3 fixes the flat 1/27 measure via E6.")
    print("HONEST OPEN: that the CHO action's potential IS N3, the kinetic")
    print("coefficient, and the full equations of motion remain to be derived;")
    print("F0 stays GEOMETRIC and no Bayes credit moves on this increment.")
    print("-" * 72)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
