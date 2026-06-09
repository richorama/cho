"""
THE SEED, LOCALIZED -- does the framework's OWN F4-breaking object select the
three generation seeds on OP^2?  (the CONTENT half of pi/432, attacked head-on)
==============================================================================

Why this module exists
----------------------
`berry_sigma_model_op2.py` split pi/432 cleanly into a FORM half and a CONTENT
half, and proved a sharp NO-GO for the CONTENT:

    on the triality-vacuum manifold OP^2 = F4/Spin(9) the cubic norm N3 (= det)
    is FLAT (identically 0), and -- since F4 acts transitively -- EVERY
    F4-invariant function is constant there.  So the three generations (the three
    primitive idempotents E1,E2,E3, all F4-equivalent points of OP^2) cannot be
    told apart, let alone given a hierarchy, by ANY F4-invariant potential.
    Seed-selection REQUIRES an F4-BREAKING term.

`berry_pi_intrinsic_op2.py` then hardened the FORM (the pi is a half-turn forced
by generation-orthogonality, intrinsic to OP^2, the SU(2) sign flip).  This
module attacks the CONTENT half the no-go left open: it asks whether the
framework's OWN canonical F4-breaking object -- the triality-breaking vacuum
spurion (rank-one, |tau><tau|, the e7/omega direction of `epsilon_rank_one_kernel`
and `spurion_bridge`) -- is exactly the F4-breaking term the no-go demanded, and
WHAT it selects.

The honest two-sided result
---------------------------
The finding is genuinely two-sided, and both sides are real content.

  POSITIVE (the FORM of seed-selection WORKS; the no-go is EVADED).  A linear
  frame-breaking potential V_A(P) = Tr(P o A) -- the height function of a fixed
  J3(O) element A -- has, on OP^2, critical points EXACTLY at the three primitive
  idempotents E1,E2,E3 of A's eigenframe (the standard Morse theory of height
  functions on a flag manifold: critical points = torus-fixed points).  We verify
  the F4-gradient g_D = Tr((D.P) o A) vanishes (~1e-16) at all three generations
  for a frame-diagonal A, that gradient ASCENT from random points on OP^2 flows
  to the top generation, and -- the control -- that the F4-INVARIANT choice A = I
  is flat (V = Tr P = 1 everywhere, gradient 0), reproducing the no-go.  So the
  three generations ARE the critical set of the canonical frame-breaking
  potential; "which points get selected" is answered, and answered by the SAME
  generation frame the project already owns (`three_generations_frame`), so the
  DIRECTION is frame-canonical, NOT circular: any distinct-spectrum A in that
  frame yields the SAME three critical points (only the values change).

  HONEST OPEN (the seed MAGNITUDES are the spurion spectrum; rank-one forces the
  cascade; the absolute scale stays input).  The critical VALUES are
  V_A(E_i) = a_i = spec(A) -- i.e. the seed magnitudes ARE A's spectrum, which is
  the input, not an output.  And the framework's canonical vacuum spurion is
  RANK-ONE (A = E_tau): its height function lifts EXACTLY ONE level (V(E_tau)=1,
  and the whole OP^1 of idempotents orthogonal to E_tau is a DEGENERATE critical
  manifold at value 0), the geometric form of `spurion_perturbation` FACT 1.  So
  three ISOLATED tiers cannot come from a single rank-one spurion; they require
  CUMULATIVE orders A_eff = E1 + eps0 E2 + eps0^2 E3, whose spectrum (1, eps0,
  eps0^2) reproduces the generation cascade ladder -- and the absolute scale
  eps0^2 = pi/432 (the geometric measure) remains the lone surviving input,
  closing the loop back onto the measure rather than deriving it.

Net effect on the seam (no Bayes credit moves)
----------------------------------------------
This tightens `berry_sigma_model_op2`'s open clause "seed-selection requires an
F4-BREAKING term" into: "the F4-breaking term IS the canonical rank-one vacuum
spurion; it makes the three generations the critical points of its height
function (real, frame-canonical, non-circular in direction); rank-one-ness forces
the three-tier hierarchy to be the cumulative-order cascade; and the lone
surviving input is the absolute spurion scale eps0^2 = pi/432."  The CONTENT half
is therefore LOCALIZED -- to one scalar, the same pi/432 of the measure -- but
NOT closed: the seed magnitudes are still input.  F0 stays GEOMETRIC/open, pi/432
is not promoted, and the scoreboard sign does NOT flip.

What this does NOT do (the honest scope)
----------------------------------------
* It does NOT derive the seed magnitudes.  V_A(E_i) = spec(A) is a tautology: the
  seed is put in as A's spectrum and read back out as the critical values.  The
  module's value is in showing WHERE the input sits (the spurion spectrum) and
  WHY it is forced into cascade form (rank-one-ness), not in removing it.
* It does NOT fix the generation ASSIGNMENT (which idempotent is the heaviest).
  That ordering is the residual S3/Weyl freedom -- the "which channel" input --
  untouched here.
* The "three generations = critical points" fact is the standard Morse theory of
  a height function on the flag manifold OP^2 = F4/Spin(9); it is CITED, not
  re-derived.  The NEW content is the identification of that height function's
  linear term A with the framework's canonical rank-one vacuum spurion, and the
  resulting rank-one => one-level => cascade chain.

numpy only.  No scipy.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_seed_op2.py
"""

from __future__ import annotations

import math

import numpy as np

from epsilon_orbit_selection import primitive_idempotents, _diag
from epsilon_action_selection import (
    trace_form,
    cubic_norm,
    _f4_basis,
    random_automorphism,
    _expm,
)
from berry_pi_intrinsic_op2 import _embed

PI = math.pi
EPS0_SQ = PI / 432.0            # the geometric measure (spurion_bridge: eps0^2 = pi/432)
EPS0 = math.sqrt(EPS0_SQ)

# tolerances (loose vs the ~1e-16 actuals -> wide tripwire margin)
TOL_CRIT = 1e-9       # F4-gradient at a generation (critical point)
TOL_EXACT = 1e-9      # critical values = spec(A); cascade ladder = (1,eps0,eps0^2)
TOL_FLAT = 1e-9       # F4-invariant control / degenerate-manifold flatness
TOL_NOGO = 1e-9       # N3 flat on OP^2 (the no-go)
MIN_ATTRACTOR = 0.999  # gradient-flow overlap with the selected generation


# --------------------------------------------------------------------------- #
#  The frame-breaking height function V_A(P) = Tr(P o A) and its F4-gradient    #
# --------------------------------------------------------------------------- #
def _f4():
    """The 52 real derivations spanning the Lie algebra of F4 = Aut(J3(O))."""
    return [np.asarray(D).real for D in _f4_basis()]


def height(P: np.ndarray, A: np.ndarray) -> float:
    """V_A(P) = Tr(P o A), the linear frame-breaking potential on OP^2."""
    return float(trace_form(P, A))


def f4_gradient(P: np.ndarray, A: np.ndarray, f4) -> np.ndarray:
    """Components of grad V_A along the F4-orbit tangent at P.  The flow
    exp(t D) . P has  d/dt V_A = Tr((D.P) o A) = trace_form(D @ P, A), so P is a
    critical point of V_A on OP^2 iff every component vanishes."""
    return np.array([trace_form(D @ P, A) for D in f4])


def gradient_flow(P0: np.ndarray, A: np.ndarray, f4, sign: float = +1.0,
                  steps: int = 1200, dt: float = 0.25) -> np.ndarray:
    """Steepest-ascent (sign=+1) / descent (sign=-1) of V_A along the F4-orbit.
    gen = sum_k g_k D_k is in f4 (a derivation), so exp(dt gen) stays EXACTLY on
    OP^2; d/dt V_A = sum_k g_k^2 >= 0, and the raw (un-normalised) gradient makes
    the step shrink as the critical point is approached -> convergence."""
    P = P0.copy()
    for _ in range(steps):
        g = f4_gradient(P, A, f4)
        if np.linalg.norm(g) < 1e-13:
            break
        gen = sign * sum(gk * D for gk, D in zip(g, f4))
        P = _expm(dt * gen) @ P
    return P


# --------------------------------------------------------------------------- #
#  [A] no-go recap: N3 and the F4-invariant A = I are flat on OP^2              #
# --------------------------------------------------------------------------- #
def nogo_recap(f4, seed: int = 0):
    """The cubic norm N3 (= det) and the F4-invariant height A = I are CONSTANT
    on OP^2, so neither can separate the three generations (berry_sigma_model_op2)."""
    E1, E2, E3 = primitive_idempotents()
    I = _diag(1, 1, 1)
    rng = np.random.default_rng(seed)
    n3 = [abs(cubic_norm(E)) for E in (E1, E2, E3)]
    # random OP^2 points (automorphism images of E1) are still N3 = 0, V_I = 1
    pts = [random_automorphism(rng, f4, 0.8) @ E1 for _ in range(8)]
    n3 += [abs(cubic_norm(P)) for P in pts]
    vI = [height(P, I) for P in (E1, E2, E3)] + [height(P, I) for P in pts]
    grad_I = max(float(np.linalg.norm(f4_gradient(P, I, f4))) for P in pts)
    return max(n3), min(vI), max(vI), grad_I


# --------------------------------------------------------------------------- #
#  [B] the three generations ARE the critical points of a frame-breaking V_A   #
# --------------------------------------------------------------------------- #
def generations_are_critical(A: np.ndarray, f4):
    """For frame-diagonal A, the three primitive idempotents are critical points
    of V_A, with critical values = spec(A)."""
    Es = primitive_idempotents()
    grads = [float(np.linalg.norm(f4_gradient(E, A, f4))) for E in Es]
    values = [height(E, A) for E in Es]
    spectrum = [float(A[i]) for i in range(3)]
    return grads, values, spectrum


def flow_selects_top(A: np.ndarray, f4, n_starts: int = 6, seed: int = 100):
    """Gradient ASCENT from random OP^2 points flows to the top generation (the
    idempotent E_k with the largest a_k); returns (selected indices, min overlap)."""
    Es = primitive_idempotents()
    top = int(np.argmax([A[i] for i in range(3)]))
    selected, min_overlap = [], 1.0
    for s in range(n_starts):
        P0 = random_automorphism(np.random.default_rng(seed + s), f4, 1.0) @ Es[0]
        Pf = gradient_flow(P0, A, f4, sign=+1.0)
        overlaps = [height(Pf, E) for E in Es]
        k = int(np.argmax(overlaps))
        selected.append(k)
        min_overlap = min(min_overlap, overlaps[k])
    return selected, top, min_overlap


# --------------------------------------------------------------------------- #
#  [C] the direction is frame-canonical (non-circular)                         #
# --------------------------------------------------------------------------- #
def direction_is_frame_canonical(f4):
    """Two DIFFERENT distinct-spectrum diagonal A in the SAME (generation) frame
    have the SAME three critical points -- only the values change.  So the
    critical SET = the three generations is fixed by the frame, independent of the
    seed magnitudes: the DIRECTION is canonical, the magnitudes are separate."""
    Es = primitive_idempotents()
    A1 = _diag(1.0, 0.6, 0.3)
    A2 = _diag(0.9, 0.2, 0.05)   # different spectrum, same frame
    g1 = max(float(np.linalg.norm(f4_gradient(E, A1, f4))) for E in Es)
    g2 = max(float(np.linalg.norm(f4_gradient(E, A2, f4))) for E in Es)
    v1 = [height(E, A1) for E in Es]
    v2 = [height(E, A2) for E in Es]
    return g1, g2, v1, v2


# --------------------------------------------------------------------------- #
#  [D] the magnitudes are the spurion spectrum; rank-one forces the cascade    #
# --------------------------------------------------------------------------- #
def rank_one_lifts_one_level(f4, seed: int = 7):
    """The canonical vacuum spurion is RANK-ONE, A = E_tau.  Its height function
    lifts exactly ONE level: V(E_tau) = 1, and every idempotent ORTHOGONAL to
    E_tau is degenerate at value 0 (a flat OP^1 critical manifold).  Geometric
    form of spurion_perturbation FACT 1."""
    Es = primitive_idempotents()
    Etau = Es[0]                                   # the rank-one spurion
    diag_vals = [height(E, Etau) for E in Es]      # (1, 0, 0)
    # sample the OP^1 of idempotents orthogonal to E_tau (psi in the e1,e2 plane)
    rng = np.random.default_rng(seed)
    orth_vals = []
    for _ in range(60):
        a, b = rng.standard_normal(2) + 1j * rng.standard_normal(2)
        psi = np.array([0.0, a, b], dtype=complex)
        psi = psi / np.linalg.norm(psi)
        orth_vals.append(height(_embed(psi), Etau))
    n_lifted = int(sum(1 for v in diag_vals if v > 0.5))
    return diag_vals, n_lifted, max(abs(v) for v in orth_vals)


def cascade_three_tiers(f4):
    """A single rank-one spurion lifts one level; three ISOLATED tiers require
    cumulative orders A = E1 + eps0 E2 + eps0^2 E3, whose three critical values
    (1, eps0, eps0^2) reproduce the generation cascade ladder.  The absolute scale
    eps0^2 = pi/432 (the measure) is the lone surviving input."""
    Es = primitive_idempotents()
    A = Es[0] + EPS0 * Es[1] + EPS0_SQ * Es[2]
    grads = [float(np.linalg.norm(f4_gradient(E, A, f4))) for E in Es]
    values = [height(E, A) for E in Es]
    ladder = [1.0, EPS0, EPS0_SQ]
    distinct = len({round(v, 10) for v in values}) == 3
    return grads, values, ladder, distinct


# --------------------------------------------------------------------------- #
#  Driver                                                                       #
# --------------------------------------------------------------------------- #
def main() -> bool:
    f4 = _f4()

    print("=" * 78)
    print("  THE SEED, LOCALIZED -- F4-breaking seed-selection on OP^2")
    print("  does the canonical vacuum spurion select the three generations?")
    print("=" * 78)

    # [A] no-go recap -------------------------------------------------------- #
    n3max, vI_min, vI_max, grad_I = nogo_recap(f4)
    print("\n  [A]  NO-GO RECAP (berry_sigma_model_op2): F4-invariants are flat")
    print("  " + "-" * 74)
    print(f"  max |N3| over OP^2 sample (det = cubic norm) : {n3max:.2e}  (flat = 0)")
    print(f"  F4-invariant height A = I : V_I in [{vI_min:.6f}, {vI_max:.6f}] = Tr P = 1")
    print(f"  max |grad V_I| on OP^2                       : {grad_I:.2e}  (no selection)")
    nogo_ok = n3max < TOL_NOGO and abs(vI_min - 1) < TOL_FLAT and abs(vI_max - 1) < TOL_FLAT and grad_I < TOL_FLAT

    # [B] generations = critical points of a frame-breaking V_A -------------- #
    A = _diag(1.0, 0.6, 0.3)
    grads, values, spectrum = generations_are_critical(A, f4)
    selected, top, min_overlap = flow_selects_top(A, f4)
    print("\n  [B]  FRAME-BREAKING V_A(P) = Tr(P o A), A = diag(1.0, 0.6, 0.3)")
    print("  " + "-" * 74)
    for i, (g, v, s) in enumerate(zip(grads, values, spectrum), start=1):
        print(f"  generation E{i}: |grad V_A| = {g:.2e}   V_A(E{i}) = {v:.6f}  (= a_{i} = {s})")
    print(f"  => the three generations ARE the critical points (gradient ~ 0)")
    print(f"  gradient ASCENT from {len(selected)} random OP^2 points -> generation "
          f"E{top+1} (top a_k); min overlap {min_overlap:.4f}")
    crit_ok = max(grads) < TOL_CRIT and max(abs(v - s) for v, s in zip(values, spectrum)) < TOL_EXACT
    flow_ok = all(k == top for k in selected) and min_overlap > MIN_ATTRACTOR

    # [C] direction is frame-canonical (non-circular) ----------------------- #
    g1, g2, v1, v2 = direction_is_frame_canonical(f4)
    print("\n  [C]  DIRECTION IS FRAME-CANONICAL (non-circular)")
    print("  " + "-" * 74)
    print(f"  A  = diag(1.0,0.6,0.3): max|grad at E_i| = {g1:.2e}   values {[round(x,3) for x in v1]}")
    print(f"  A' = diag(0.9,0.2,0.05): max|grad at E_i| = {g2:.2e}   values {[round(x,3) for x in v2]}")
    print(f"  => SAME three critical points (the generation frame); only VALUES differ")
    canonical_ok = g1 < TOL_CRIT and g2 < TOL_CRIT and v1 != v2

    # [D] magnitudes = spurion spectrum; rank-one forces the cascade --------- #
    diag_vals, n_lifted, orth_flat = rank_one_lifts_one_level(f4)
    cgrads, cvalues, ladder, distinct = cascade_three_tiers(f4)
    print("\n  [D]  MAGNITUDES = SPURION SPECTRUM; RANK-ONE FORCES THE CASCADE")
    print("  " + "-" * 74)
    print(f"  rank-one vacuum spurion A = E_tau: V(E_i) = {[round(v,4) for v in diag_vals]}")
    print(f"  levels lifted = {n_lifted}; OP^1 orthogonal to E_tau flat to {orth_flat:.2e}"
          f"  (spurion_perturbation FACT 1)")
    print(f"  cumulative-order A = E1 + eps0 E2 + eps0^2 E3:")
    print(f"     critical values {[round(v,6) for v in cvalues]}")
    print(f"     cascade ladder  {[round(v,6) for v in ladder]}  (1, eps0, eps0^2)")
    print(f"     eps0^2 = pi/432 = {EPS0_SQ:.6f}  (the measure -- the lone surviving input)")
    rank_one_ok = n_lifted == 1 and orth_flat < TOL_FLAT
    cascade_ok = (max(cgrads) < TOL_CRIT and distinct
                  and max(abs(v - l) for v, l in zip(cvalues, ladder)) < TOL_EXACT)

    # [E] verdict ------------------------------------------------------------ #
    form_works = bool(nogo_ok and crit_ok and flow_ok)         # POSITIVE half
    direction_canonical = bool(canonical_ok)                   # non-circular
    content_open = bool(rank_one_ok and cascade_ok)            # HONEST OPEN half
    sign_flips = False                                         # no Bayes credit
    print("\n  [E]  VERDICT")
    print("  " + "-" * 74)
    print(f"  FORM of seed-selection works (3 gens = critical points)  : {form_works}")
    print(f"  direction frame-canonical (non-circular)                 : {direction_canonical}")
    print(f"  CONTENT open (magnitudes = spurion spec; cascade forced) : {content_open}")
    print(f"  scoreboard sign flips                                    : {sign_flips}")
    print("  the F4-breaking term IS the canonical rank-one vacuum spurion; it makes")
    print("  the three generations the critical points (real, non-circular DIRECTION),")
    print("  rank-one-ness forces the cumulative-order cascade, and the lone surviving")
    print("  input is the absolute scale eps0^2 = pi/432.  F0 stays GEOMETRIC/open.")
    print("=" * 78)

    # self-forbidding tripwires (stable theorems only) ----------------------- #
    assert nogo_ok, "no-go recap failed: an F4-invariant is NOT flat on OP^2"
    assert crit_ok, "the three generations are NOT the critical points of V_A"
    assert flow_ok, "gradient ascent does NOT select the top generation"
    assert canonical_ok, "critical set is NOT frame-canonical / not magnitude-free"
    assert rank_one_ok, "rank-one spurion does NOT lift exactly one level"
    assert cascade_ok, "cumulative-order cascade does NOT give the (1,eps0,eps0^2) ladder"
    assert abs(EPS0_SQ - PI / 432.0) < 1e-15, "eps0^2 must equal pi/432 (the measure)"
    # honest-scope tripwires: the magnitudes are INPUT, no credit moves
    assert form_works and direction_canonical, "the POSITIVE half must hold"
    assert content_open, "the CONTENT (magnitude) half must remain OPEN"
    assert not sign_flips, "EXPLORATORY: the scoreboard sign must NOT flip"
    return form_works and direction_canonical and content_open and not sign_flips


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
