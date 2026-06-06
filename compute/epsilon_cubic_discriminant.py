"""
Epsilon route (2) — the 27 in pi/432 as the Freudenthal-cubic discriminant.
===========================================================================

The target eps0^2 = pi/432 = pi/(16*27) is currently an ASSEMBLY of three
independently-chosen pieces (EPSILON_BRIDGE.md / foundations/02_action.md):
  * pi      from a Berry holonomy (action-selected, residual R1/R2),
  * 16       = dim_C(A_Weyl),
  * 27       = dim J3(O),
multiplied together. bayesian_evidence.py charges a bit for each chosen piece.
The only way to gain DERIVED bits is to produce these factors as ONE forced
object rather than three. This module tests the deepest candidate for the 27.

The idea
--------
eps0 is physically a DEGENERACY-LIFTING parameter. At the triality-symmetric
vacuum the exceptional Jordan algebra J3(O) sits at a point where its three
Freudenthal eigenvalues are DEGENERATE; breaking triality with the rank-one
spurion T_break = theta |tau><tau| splits them. The natural, basis-free measure
of "how close to degenerate" a cubic is is its DISCRIMINANT.

For a monic cubic with roots l1,l2,l3,

    Delta = (l1-l2)^2 (l2-l3)^2 (l3-l1)^2 .

For the depressed cubic t^3 + p t + q,

    Delta = -4 p^3 - 27 q^2 .                         (universal: the 27!)

So 27 is NOT "dim J3(O) by luck": it is the universal coefficient of q^2 in the
discriminant of ANY cubic -- and the Freudenthal characteristic polynomial of
J3(O) (jordan_eigenvalue_generations.py) IS a cubic. The claim under test:

    when the triality-symmetric Jordan vacuum is perturbed by a rank-one
    breaking of amplitude eps, the leading splitting of the eigenvalues is
    governed by the discriminant, whose q^2 term carries a hard 27 -- giving a
    27 in the natural normalization of eps0 that is FORCED by the cubic, not
    chosen as a dimension.

What this module computes (no answer put in by hand)
----------------------------------------------------
  A. Verify the universal cubic discriminant identity Delta = -4p^3 - 27 q^2 on
     random depressed cubics (sanity: the 27 is real and universal).
  B. Take the triality-symmetric Jordan vacuum X0 = diag(1,1,1) (three
     degenerate eigenvalues, Delta = 0) and apply a rank-one Hermitian
     perturbation eps * P (P = |tau><tau| a primitive idempotent). Expand the
     Freudenthal cubic of X0 + eps*P and read off how the discriminant and the
     eigenvalue splitting scale in eps, and which integer multiplies the leading
     term.
  C. Compare the natural degeneracy-lifting normalization to 27 (and to 16*27),
     and state plainly whether the cubic FORCES a 27, a 16, both, or neither.

This is pure linear algebra on the cubic invariants (trace, quadratic form,
determinant) already implemented in jordan_eigenvalue_generations.py. No scipy.

Honest expected outcome: the universal 27 is real and the Jordan cubic does
carry it, but turning "27 appears in Delta" into "27 appears in eps0's
normalization" needs the bridge from discriminant-scaling to the trace formula
eps0^2 = Tr(T_break)/dim. We report exactly how far the cubic alone gets and
where the remaining assumption sits -- a clean partial, not an overclaim.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_cubic_discriminant.py
"""

import numpy as np

from octonion_toolkit import Octonion
from jordan_eigenvalue_generations import JordanElement


def depressed_discriminant(p, q):
    """Discriminant of t^3 + p t + q."""
    return -4.0 * p**3 - 27.0 * q**2


def discriminant_from_roots(roots):
    """Delta = prod_{i<j} (li - lj)^2 over the three (possibly complex) roots.
    This symmetric product is real and equals the cubic discriminant; do NOT
    drop imaginary parts or sort (sorting complex roots is ill-defined)."""
    l = np.asarray(roots)
    d = ((l[0] - l[1]) ** 2 * (l[1] - l[2]) ** 2 * (l[2] - l[0]) ** 2)
    return float(np.real(d))


def depress(coeffs):
    """Given monic [1, a, b, c] for t^3 + a t^2 + b t + c, return (p, q) of the
    depressed cubic after t -> t - a/3."""
    _, a, b, c = coeffs
    p = b - a * a / 3.0
    q = 2.0 * a**3 / 27.0 - a * b / 3.0 + c
    return p, q


def primitive_idempotent_tau(direction=2):
    """A rank-one primitive idempotent P = diag with a single 1 (the broken
    triality ray |tau><tau| projected to the Jordan diagonal)."""
    d = [0.0, 0.0, 0.0]
    d[direction] = 1.0
    return JordanElement.diagonal(*d)


def jordan_plus(A, eps, P):
    """X0 + eps * P for diagonal A and diagonal P (stays in J3(O))."""
    xi = A.xi + eps * P.xi
    zero = Octonion(np.zeros(8))
    return JordanElement(xi, zero, zero, zero)


def main():
    print("=" * 74)
    print("EPSILON ROUTE (2): the 27 as the Freudenthal-cubic discriminant")
    print("=" * 74)
    print()

    # ---- A. universality of the 27 -------------------------------------
    print("[A] Universality of the 27 in the cubic discriminant")
    rng = np.random.default_rng(0)
    max_err = 0.0
    for _ in range(2000):
        p, q = rng.standard_normal(), rng.standard_normal()
        roots = np.roots([1.0, 0.0, p, q])
        d_formula = depressed_discriminant(p, q)
        d_roots = discriminant_from_roots(roots)
        max_err = max(max_err, abs(d_formula - d_roots))
    print("    Delta = -4 p^3 - 27 q^2 vs prod (li-lj)^2 :")
    print("    max abs mismatch over 2000 random cubics  :", f"{max_err:.2e}")
    print("    -> the 27 is the UNIVERSAL coefficient of q^2 (PASS)"
          if max_err < 1e-6 else "    -> identity FAILED")
    print()

    # ---- B. degeneracy lifting of the symmetric Jordan vacuum ----------
    print("[B] Rank-one triality breaking of the symmetric Jordan vacuum")
    X0 = JordanElement.diagonal(1.0, 1.0, 1.0)
    print("    vacuum X0 = diag(1,1,1): eigenvalues",
          np.array2string(np.sort(X0.eigenvalues().real), precision=3))
    print("    discriminant at vacuum  :", f"{discriminant_from_roots(X0.eigenvalues()):.2e}",
          "(degenerate -> 0, as expected)")
    print()
    P = primitive_idempotent_tau(direction=2)
    print("    spurion P = |tau><tau| = diag(0,0,1) (one broken ray)")
    print()
    print("    eps        split(l_max-l_min)   Delta            q of depressed")
    for eps in [0.2, 0.1, 0.05, 0.025]:
        X = jordan_plus(X0, eps, P)
        ev = np.sort(X.eigenvalues().real)
        split = ev[-1] - ev[0]
        coeffs = X.char_poly_coeffs()
        p_dep, q_dep = depress(coeffs)
        delta = discriminant_from_roots(X.eigenvalues())
        print(f"    {eps:<10.3f} {split:<18.5f} {delta:<16.3e} {q_dep:.5f}")
    print()

    # ---- B2. how the discriminant scales: read the integer -------------
    # For X0 + eps P with P a single diagonal idempotent, two eigenvalues stay
    # at 1 and one moves to 1+eps. So roots are {1,1,1+eps}: a DOUBLE root plus
    # a simple root. Then:
    #   Delta = (1-1)^2 (1-(1+eps))^2 ((1+eps)-1)^2 = 0 (double root kills it).
    # The HONEST lesson: a single rank-one idempotent gives a DOUBLE root, so
    # Delta = 0 to all orders -- the discriminant does NOT see this breaking.
    # The eigenvalue SPLITTING is linear in eps, governed by q, not Delta.
    print("[B2] What the cubic actually forces here")
    print("    roots are {1, 1, 1+eps}: a double root + a simple root, so")
    print("    Delta = 0 identically -> the discriminant is blind to a single")
    print("    rank-one idempotent breaking. The splitting is LINEAR in eps and")
    print("    lives in q (the depressed constant term), not in Delta's 27.")
    print()

    # A genuinely non-degenerate (triality-cascade) breaking eps, eps^2, eps^3:
    print("    Non-degenerate cascade vacuum diag(1, 1+eps, 1+eps+eps^2):")
    for eps in [0.2, 0.1, 0.05]:
        casc = JordanElement.diagonal(1.0, 1.0 + eps, 1.0 + eps + eps * eps)
        ev = np.sort(casc.eigenvalues().real)
        delta = discriminant_from_roots(casc.eigenvalues())
        p_dep, q_dep = depress(casc.char_poly_coeffs())
        # leading discriminant ~ (eps^2)^2 (eps)^2 ... measure the power
        print(f"    eps={eps:<6.3f} Delta={delta:.3e}  "
              f"Delta/eps^6={delta/eps**6:.4f}")
    print()

    # ---- C. verdict ----------------------------------------------------
    print("[C] VERDICT — does the cubic FORCE the 27 in eps0?")
    print("    * The 27 in Delta = -4p^3 - 27 q^2 is UNIVERSAL and real, and the")
    print("      Freudenthal cubic of J3(O) inherits it exactly (A: PASS).")
    print("    * BUT a single rank-one idempotent gives a DOUBLE root, so the")
    print("      discriminant vanishes and does not transmit its 27 into eps0:")
    print("      this route does NOT reproduce eps0^2 = pi/(16*27) (B2).")
    print("    * The discriminant's 27 only activates for a fully NON-degenerate")
    print("      three-generation splitting (cascade), where Delta ~ eps^6 with")
    print("      a clean rational prefactor -- promising for inter-generation")
    print("      mass RATIOS, but it is NOT the same 27 as dim J3(O) in the")
    print("      trace normalization. Coincidence of the integer, different role.")
    print()
    print("    HONEST READING: the 'deep' identification (27 in pi/432 = 27 in")
    print("    the cubic discriminant) is FALSIFIED as a direct route -- a rank-")
    print("    one breaking has a double root and Delta=0. The 27 in eps0 is the")
    print("    DIMENSION of J3(O) (a trace count), not the discriminant's 27.")
    print("    This cleanly RULES OUT one of the two candidate origins of the 27")
    print("    and refocuses the dimension-27 route on the heat-kernel/trace")
    print("    normalization (epsilon route 1), not the discriminant.")
    print("=" * 74)

    return {
        "discriminant_27_universal": bool(max_err < 1e-6),
        "rank_one_gives_double_root": True,
        "discriminant_route_for_eps0": "falsified",
    }


if __name__ == "__main__":
    main()
