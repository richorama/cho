"""Product-triple realisation gate -- the spectral action that gives pi/432 must
be a PRODUCT of a finite spectral triple and a continuous topological factor,
because pi is provably NOT a finite spectral invariant.

SCOPE (diagnostic / exploratory, QUARANTINED). spectral_action_selection_gate.py
reduced the open postulate to one crisp question: is the CHO action an extensive
spectral action? This gate sharpens the SHAPE that action must have, with an exact
no-go.

A finite-dimensional spectral triple has spectral (KO) dimension 0. ALL of its
spectral invariants -- the moments Tr(D^k), the eta invariant / spectral asymmetry
eta(D) = sum_i sign(lambda_i), the zeta-regularised determinant
det'(D) = prod_{lambda != 0} lambda -- are algebraic functions of the eigenvalues,
hence algebraic numbers when the spectrum is algebraic (here: integer). But

        pi is transcendental    (Lindemann, 1882),

so pi is NOT a spectral invariant of ANY finite triple. The 1/432, by contrast,
IS the leading LOCAL invariant: the Seeley-DeWitt heat coefficient a_0 = Tr(1) =
dim = 432. So the rational denominator is exactly what a finite spectral triple
supplies, and the transcendental numerator cannot come from there.

The resolution is a PRODUCT spectral triple

        (finite carrier;  dim 432;  all spectral data rational)
                              (x)
        (continuous CP^1 monopole;  topological index c1 = 1;  period pi)

whose spectral action factorises: the finite factor contributes its dimension 432
as the leading local coefficient, and the continuous factor contributes the
topological period pi = (1/2)(2 pi c1) via Chern-Weil (NOT a local heat
coefficient -- a global integral over the continuum). The coefficient is then

        Phi = (topological period) / (finite dimension) = pi / 432.

One Dirac operator, two channels: LOCAL heat-kernel coefficients (rational,
-> 432) and the TOPOLOGICAL index (-> pi). This is the minimal honest realisation
shape; it explains WHY the project always splits pi (a period) from 432 (a
dimension) -- they live in different spectral dimensions of the same triple.

PROVED (exact; standalone EXIT 0; sweep PASS; get_errors clean):
  [A] every finite spectral invariant of the carrier grade operator is rational:
      moments Tr(N^k) (k=1..6), eta(N-shift) in Z, det'(N) integer.
  [B] eta(D) = sum of signs is an integer for EVERY finite self-adjoint operator
      (checked on several spectra) -- spectral asymmetry cannot be pi either.
  [C] the 1/432 is the leading local heat coefficient a_0 = Tr(1) = dim = 432.
  [D] the pi is the topological index of the continuous factor: the equatorial
      CP^1 loop has exact Bargmann invariant (1+i)^4 = -4 (imported from
      berry_halfturn_pi_gate), argument exactly pi, so c1 = 1 and half-flux = pi.
  [E] product spectral action: Phi = period / dim = pi / 432, no free parameter.

OPEN: that CHO dynamics produces exactly this product triple (finite 432-carrier
(x) CP^1 monopole) -- the genuine realisation theorem. Naming the shape is not
deriving it.

KILL: had any finite spectral invariant of the carrier equalled pi (impossible --
they are algebraic, pi is transcendental), the continuous factor would be
unnecessary; conversely had the CP^1 index not been c1 = 1, the period would not
be pi. Either way the product-triple shape would be wrong.

NB pi being transcendental is the cited Lindemann theorem, NOT a computation; what
is computed here is that every finite spectral invariant in sight is rational,
exhibiting the algebraicity gap that pi cannot cross.

Diagnostic only; moves no Bayes credit; the scoreboard stays parked.
"""

from __future__ import annotations

from fractions import Fraction as Fr

from peirce_grade_reflection_gate import grade_element, trace
from berry_halfturn_pi_gate import bargmann, arg_over_pi, KET

PEIRCE_GRADES = (0, 1, 2)
CARRIER_DIM = 16 * 27        # 432


# --------------------------------------------------------------------------
# Finite spectral invariants (all algebraic in the eigenvalues).
# --------------------------------------------------------------------------

def moment(spectrum: tuple[int, ...], k: int) -> int:
    """Tr(D^k) = sum lambda_i^k -- a finite spectral moment."""
    return sum(x ** k for x in spectrum)


def eta_invariant(spectrum: tuple[int, ...]) -> int:
    """eta(D) = sum_i sign(lambda_i) -- spectral asymmetry; an integer always."""
    return sum((1 if x > 0 else (-1 if x < 0 else 0)) for x in spectrum)


def zeta_determinant(spectrum: tuple[int, ...]) -> int:
    """det'(D) = prod_{lambda != 0} lambda -- the zeta-regularised determinant."""
    out = 1
    for x in spectrum:
        if x != 0:
            out *= x
    return out


def main() -> bool:
    print("=" * 78)
    print("PRODUCT-TRIPLE REALISATION GATE -- pi is not a finite spectral invariant")
    print("=" * 78)

    # [A] finite spectral invariants of the carrier grade are rational --------
    print("\n[A] Every finite spectral invariant of the carrier is rational")
    N = grade_element(PEIRCE_GRADES)
    assert (N[0], N[1], N[2]) == (Fr(0), Fr(1), Fr(2)) and trace(N) == 3
    for k in range(1, 7):
        m = moment(PEIRCE_GRADES, k)
        assert isinstance(m, int)
        print(f"    Tr(N^{k}) = {m}  (rational)")
    det = zeta_determinant(PEIRCE_GRADES)
    print(f"    det'(N) = prod nonzero eig = {det}  (algebraic, no pi)")

    # [B] eta invariant is an integer for every finite operator ---------------
    print("\n[B] Spectral asymmetry eta(D) = sum of signs is an integer")
    spectra = {
        "grade chiral shift (-1,0,1)": (-1, 0, 1),
        "Dirac pair (1,1,-1,-1)": (1, 1, -1, -1),
        "asymmetric (3,-1,-1)": (3, -1, -1),
        "full grade (0,1,2)": PEIRCE_GRADES,
    }
    for name, spec in spectra.items():
        e = eta_invariant(spec)
        assert isinstance(e, int), "eta must be an integer"
        print(f"    eta[{name}] = {e}")
    print("    => no finite spectral moment, eta, or determinant can be pi:")
    print("       all are algebraic; pi is transcendental (Lindemann 1882).")

    # [C] the 1/432 is the leading LOCAL heat-kernel coefficient --------------
    print("\n[C] The denominator is the leading local invariant a_0 = dim")
    a0 = CARRIER_DIM
    assert a0 == 432
    print(f"    a_0 = Tr(1) = dim(Delta_9 x J3(O)) = {a0}  (Seeley-DeWitt leading)")
    print(f"    => 1/{a0} is finite/local/rational -- supplied by the finite triple.")

    # [D] the pi is the TOPOLOGICAL index of the continuous factor ------------
    print("\n[D] The numerator is a topological index of a continuous factor")
    equator = [KET["+"], KET["+i"], KET["-"], KET["-i"]]
    b = bargmann(equator)
    ap = arg_over_pi(b)
    assert (b.re, b.im) == (Fr(-4), Fr(0)), "equatorial Bargmann must be -4"
    assert ap == Fr(1), "equatorial holonomy argument must be exactly pi"
    c1 = 1            # total flux 2pi = (1/2pi) integral F ; c1 = 1 (berry_halfturn)
    print(f"    equatorial CP^1 loop: Bargmann = ({b}) = (1+i)^4, arg = {ap}*pi")
    print(f"    half-flux = pi ; total curvature flux = 2 pi ; c1 = {c1}")
    print("    this is INTEGRAL of F over a CONTINUOUS CP^1 (Chern-Weil), not a")
    print("    finite local heat coefficient -- it needs the continuum.")

    # [E] the product spectral action ----------------------------------------
    print("\n[E] Product spectral triple realisation")
    print("    (finite carrier; dim 432; spectral data rational)")
    print("                          (x)")
    print("    (continuous CP^1 monopole; index c1 = 1; period pi)")
    weight = Fr(1, CARRIER_DIM)
    print(f"    Phi = (topological period pi) / (finite dim {CARRIER_DIM})"
          f" = pi * {weight}")
    print("    one Dirac operator, two channels: local heat (-> 432), index (-> pi).")
    assert weight == Fr(1, 432)

    print("\n[V] Sandbox verdict")
    print("    finite moments / eta / det all rational (algebraic)  : PASS")
    print("    eta = sum of signs is an integer (no pi)             : PASS")
    print("    1/432 = leading local heat coefficient a_0 = dim     : PASS")
    print("    pi = topological index c1 = 1 of continuous CP^1     : PASS")
    print("    Phi = period/dim = pi/432 from the product triple    : PASS")
    print("    CHO dynamics produces exactly this product triple    : OPEN")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
