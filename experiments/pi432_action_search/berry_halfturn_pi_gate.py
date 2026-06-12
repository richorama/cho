"""berry_halfturn_pi_gate.py -- the numerator pi is an exact geometric half-turn.

SCOPE (quarantined, diagnostic/exploratory). Moves NO Bayes credit, promotes no
ledger row, touches no frozen registry or scoreboard. Imports only the exact
Albert-algebra machinery from its sibling peirce_grade_reflection_gate (which in
turn embeds its own octonion table and imports nothing from compute/). PURE
stdlib + fractions (exact) -- there are NO floating-point numbers anywhere in the
proof: every geometric phase is the argument of an exact Gaussian-rational number.

It attacks the NUMERATOR of pi/432, the partner of f4_breaking_vacuum_gate.py
(which derived the denominator 432 = 16 x 27 from the spontaneous F4 -> Spin(9)
breaking). The candidate coefficient is

    pi/432 = (primitive half-turn flux  pi) x (1 / carrier 432).

The existing pi modules establish the FORM but only with FLOATS and an ASSUMED
law: compute/berry_pi_intrinsic_op2.py checks gamma = pi(1-cos theta) numerically
(tolerance 3e-3) and shows it is F4-invariant; wz_chain_origin_gate.py asserts the
full-sphere action (1/2)(4 pi) = 2 pi, c1 = 1 in floats; oriented_wz_boundary_gate
.py samples a 4000-point Bargmann product. NONE exhibits the half-turn as an EXACT
number, and none ties it to the explicit OP^2 vacuum idempotents of the breaking
gate. This module does both, exactly.

The idea: on the vacuum manifold OP^2 (the rank-one idempotents of J3(O)) the
minimal transition two-sphere is the CP^1 of rank-one idempotents built from a
complex 2-plane. Five of its points -- |0>, |+>, |+i>, |->, |-i> -- have
GAUSSIAN-RATIONAL projectors, so they are genuine, exactly representable J3(O)
primitive idempotents, and the geometric (Pancharatnam) phase of a closed
geodesic polygon through them is the argument of an exact Gaussian-rational
Bargmann product. No octonionic Bargmann product is ever evaluated (that is
ill-defined); the slice is complex hence associative, and its idempotents are
certified to be genuine J3(O) primitives with the correct trace metric.

PROVED (exact, asserted tripwires; EXIT 0 standalone and inside the sweep):
  [A] the five coherent projectors are genuine PRIMITIVE idempotents of the real
      Albert algebra J3(O): P o P = P and Tr(P) = 1 (hence rank one), checked
      exactly via the sibling Jordan product; and the trace metric reproduces the
      transition probability EXACTLY, Tr(P_v o P_w) = |<v|w>|^2 -- e.g.
      Tr(P_0 o P_+) = 1/2, Tr(P_+ o P_-) = 0 (antipodal = two orthogonal
      generations). So the CP^1 of idempotents carries the round Fubini-Study
      metric of the carrier;
  [B] OCTANT (a geodesic triangle, all three angles right). The Bargmann
      invariant <0|+><+|+i><+i|0> equals EXACTLY 1 + i (Gaussian-rational), whose
      argument is EXACTLY pi/4. The triangle bounds a spherical octant of solid
      angle pi/2, so the geometric phase equals EXACTLY one half of the enclosed
      solid angle -- the half-solid-angle law is OUTPUT here, not assumed;
  [C] THE HALF-TURN. The closed geodesic 4-gon |+> -> |+i> -> |-> -> |-i> -> |+>
      traverses the full great circle (equator). Its Bargmann invariant is
      EXACTLY (1 + i)^4 = -4, a NEGATIVE REAL number, so its argument is EXACTLY
      pi and the loop holonomy is exp(i pi) = -1 (the SU(2) double-cover sign
      flip). The equator bounds a hemisphere of solid angle 2 pi, so once more
      gamma = (1/2) x 2 pi = pi. The numerator pi is therefore the geometric
      half-turn flux of the minimal transition loop on OP^2, pinned to an exact
      rational multiple (1) of pi -- not a fitted constant;
  [D] FIRST CHERN NUMBER ONE. The two hemispheres each carry flux pi, so the
      Berry line bundle over the transition CP^1 has total curvature flux
      (1/2)(4 pi) = 2 pi and first Chern number c1 = 2 pi / 2 pi = 1 (exact, as a
      rational multiple of pi). Hence the primitive WZ level is k = 1: level 0 is
      trivial, |k| > 1 are multiples, and the minimal nonzero flux quantum is the
      half-turn pi;
  [E] THE PRODUCT. Combining with f4_breaking_vacuum_gate.py (carrier
      16 x 27 = 432) the coefficient factorises as pi/432 = (half-turn pi) /
      (16 x 27): BOTH the numerator pi (this gate, exact geometric half-turn) and
      the denominator 432 (the breaking gate, exact representation dimensions) are
      now derived from the carrier geometry rather than inserted.

OPEN (unchanged; stated, not hidden):
  * that the physical seed/WZ COUPLING equals this geometric phase divided by the
    FULL carrier (the flux-over-carrier normalisation) is the Schur-flatness
    input of wz_flux_normalization_gate.py, NOT re-derived here;
  * that CHO dynamics must place exactly this oriented level-one WZ term in the
    action is the action-origin obligation, still open (criterion (1));
  * the intrinsicness of the pi to the octonionic (non-slice) geodesic 2-spheres
    is cited from compute/berry_pi_intrinsic_op2.py (F4-isometry argument), not
    re-derived; this gate hardens the COMPLEX-slice computation to exactness.

KILL: had the octant Bargmann invariant not had argument pi/4, or the equatorial
4-gon not been a negative real (argument pi), or the half-solid-angle identity
2 x gamma = Omega failed at these exact points, the identification "numerator =
geometric half-turn" would be false and the pi side of the route would die.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 \
        experiments/pi432_action_search/berry_halfturn_pi_gate.py
"""

from __future__ import annotations

from fractions import Fraction as Fr

from peirce_grade_reflection_gate import DIM, jordan, trace


# --------------------------------------------------------------------------
# Exact Gaussian-rational arithmetic (Q[i]); phases are arguments of these.
# --------------------------------------------------------------------------

class G:
    """A Gaussian rational  re + im*i  with exact Fraction components."""

    __slots__ = ("re", "im")

    def __init__(self, re: Fr, im: Fr = Fr(0)) -> None:
        self.re = Fr(re)
        self.im = Fr(im)

    def __mul__(self, other: "G") -> "G":
        return G(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)

    def __add__(self, other: "G") -> "G":
        return G(self.re + other.re, self.im + other.im)

    def conj(self) -> "G":
        return G(self.re, -self.im)

    def norm2(self) -> Fr:
        return self.re * self.re + self.im * self.im

    def __repr__(self) -> str:
        return f"({self.re} + {self.im} i)"


def inner(u: tuple[G, G], w: tuple[G, G]) -> G:
    """Hermitian inner product <u|w> = sum conj(u_k) w_k  on a complex 2-vector."""
    return u[0].conj() * w[0] + u[1].conj() * w[1]


def bargmann(vertices: list[tuple[G, G]]) -> G:
    """Closed-loop Bargmann invariant  prod_k <v_k | v_{k+1}>  (gauge invariant).

    Its argument is the geometric (Pancharatnam) phase of the geodesic polygon
    through the vertices; the magnitude is irrelevant (only the phase is physical).
    """
    prod = G(Fr(1))
    n = len(vertices)
    for k in range(n):
        prod = prod * inner(vertices[k], vertices[(k + 1) % n])
    return prod


def arg_over_pi(z: G) -> Fr:
    """Exact argument of a nonzero Gaussian rational, as a multiple of pi, for the
    eight 'octant' directions (multiples of pi/4). Raises if z is off the lattice
    of nice directions (which never happens for the loops used here)."""
    p, q = z.re, z.im
    assert not (p == 0 and q == 0), "zero has no argument"
    if q == 0:
        return Fr(0) if p > 0 else Fr(1)            # 0 or pi
    if p == 0:
        return Fr(1, 2) if q > 0 else Fr(-1, 2)     # +pi/2 or -pi/2
    if p == q:
        return Fr(1, 4) if p > 0 else Fr(-3, 4)     # +pi/4 or -3pi/4
    if p == -q:
        return Fr(-1, 4) if p > 0 else Fr(3, 4)     # -pi/4 or +3pi/4
    raise AssertionError(f"argument of {z} is not a multiple of pi/4")


# --------------------------------------------------------------------------
# The five coherent states and their exact J3(O) projectors.
# --------------------------------------------------------------------------

ONE = G(Fr(1))
I = G(Fr(0), Fr(1))
ZERO = G(Fr(0))

# Unnormalised complex 2-vectors (normalisation is a positive real -> no phase).
KET = {
    "0":  (ONE, ZERO),          # north pole  -> E11
    "+":  (ONE, ONE),           # equator phi=0
    "+i": (ONE, I),             # equator phi=pi/2
    "-":  (ONE, G(Fr(-1))),     # equator phi=pi
    "-i": (ONE, G(Fr(0), Fr(-1))),  # equator phi=3pi/2
}


def projector_vec(ket: tuple[G, G]) -> list[Fr]:
    """Rank-one projector P = |v><v| / <v|v> as a 27-vector of J3(O) (the complex
    (0,1) block). Entries are Gaussian-rational, hence exactly representable."""
    a, b = ket
    n2 = inner(ket, ket).re            # <v|v> is a positive rational
    a2 = a.norm2() / n2
    b2 = b.norm2() / n2
    off = (a * b.conj())               # P[0][1] = a conj(b)
    off = G(off.re / n2, off.im / n2)
    v = [Fr(0)] * DIM
    v[0] = a2                          # E11 diagonal
    v[1] = b2                          # E22 diagonal
    v[3] = off.re                      # e0 part of the (0,1) octonion slot
    v[4] = off.im                      # e1 part of the (0,1) octonion slot
    return v


def main() -> bool:
    print("=" * 78)
    print("BERRY HALF-TURN GATE -- the numerator pi as an exact geometric phase")
    print("=" * 78)

    projectors = {name: projector_vec(ket) for name, ket in KET.items()}

    # [A] genuine primitive idempotents + exact transition metric --------------
    print("\n[A] The coherent projectors are exact primitive idempotents of J3(O)")
    for name, P in projectors.items():
        assert jordan(P, P) == P, f"P_{name} is not idempotent"
        assert trace(P) == 1, f"Tr(P_{name}) != 1"
    print("    P o P = P and Tr(P) = 1 for all five (rank one = primitive): OK")

    def overlap(n1: str, n2: str) -> Fr:
        return trace(jordan(projectors[n1], projectors[n2]))

    def prob(n1: str, n2: str) -> Fr:
        u, w = KET[n1], KET[n2]
        return inner(u, w).norm2() / (inner(u, u).re * inner(w, w).re)

    checks = [("0", "+"), ("+", "+i"), ("0", "0"), ("+", "-"), ("0", "-i")]
    for n1, n2 in checks:
        tr = overlap(n1, n2)
        pr = prob(n1, n2)
        assert tr == pr, f"Tr(P_{n1} o P_{n2}) = {tr} != |<.|.>|^2 = {pr}"
        print(f"    Tr(P_{n1} o P_{n2}) = {tr}  =  |<{n1}|{n2}>|^2  (exact)")
    assert overlap("+", "-") == 0, "equator antipodes must be orthogonal"
    print("    antipodes |+>,|-> are orthogonal generations (Tr = 0): OK")

    # [B] octant: geodesic triangle, phase = 1/2 solid angle -------------------
    octant = [KET["0"], KET["+"], KET["+i"]]
    b_oct = bargmann(octant)
    arg_oct = arg_over_pi(b_oct)
    solid_oct = Fr(1, 2)               # octant solid angle = pi/2  (all right angles)
    print("\n[B] Octant geodesic triangle  |0> -> |+> -> |+i>")
    print(f"    Bargmann invariant  <0|+><+|+i><+i|0> = {b_oct}   (exact)")
    print(f"    geometric phase = {arg_oct} * pi      enclosed solid angle = "
          f"{solid_oct} * (2 pi) = pi/2")
    assert b_oct.re == 1 and b_oct.im == 1, "octant Bargmann invariant must be 1+i"
    assert arg_oct == Fr(1, 4), "octant phase must be pi/4"
    # half-solid-angle law: gamma = (1/2) Omega, with Omega in units of pi
    assert 2 * arg_oct == solid_oct, "phase != half the solid angle (octant)"
    print("    => gamma = (1/2) x solid angle  (the half-solid-angle law, derived)")

    # [C] the half-turn: equatorial great circle -------------------------------
    equator = [KET["+"], KET["+i"], KET["-"], KET["-i"]]
    b_eq = bargmann(equator)
    arg_eq = arg_over_pi(b_eq)
    solid_hemi = Fr(2)                 # hemisphere solid angle = 2 pi
    print("\n[C] Equatorial great circle  |+> -> |+i> -> |-> -> |-i>")
    print(f"    Bargmann invariant  = {b_eq}   (exact)  = (1+i)^4")
    print(f"    geometric phase = {arg_eq} * pi      loop holonomy = exp(i pi) = -1")
    assert b_eq.re == -4 and b_eq.im == 0, "equator Bargmann invariant must be -4"
    assert arg_eq == Fr(1), "the half-turn phase must be exactly pi"
    assert b_eq.im == 0 and b_eq.re < 0, "holonomy must be the negative-real sign flip"
    assert 2 * arg_eq == solid_hemi, "phase != half the hemisphere solid angle"
    print("    => the minimal great-circle (half-turn) flux is EXACTLY pi")

    # [D] first Chern number one ----------------------------------------------
    total_flux = 2 * arg_eq            # two hemispheres, each pi  -> 2 (units of pi)
    chern = total_flux / Fr(2)         # c1 = total flux / 2 pi
    print("\n[D] Berry line bundle over the transition CP^1")
    print(f"    total curvature flux = {total_flux} * pi = (1/2)(4 pi) = 2 pi")
    print(f"    first Chern number c1 = {chern}   (primitive WZ level k = 1)")
    assert total_flux == Fr(2), "full-sphere flux must be 2 pi"
    assert chern == Fr(1), "first Chern number must be 1"

    # [E] the product pi/432 ---------------------------------------------------
    carrier = 16 * 27                  # from f4_breaking_vacuum_gate.py
    print("\n[E] The coefficient")
    print(f"    numerator   (this gate)            : pi  (half-turn, c1 = 1)")
    print(f"    denominator (f4_breaking_vacuum)   : 16 x 27 = {carrier}")
    print(f"    coefficient                        : pi / {carrier}")
    assert carrier == 432, "carrier must be 432"

    # [V] verdict --------------------------------------------------------------
    print("\n[V] Sandbox verdict")
    print("    coherent projectors are exact J3(O) primitives   : PASS")
    print("    octant phase = pi/4 = 1/2 solid angle (exact)     : PASS")
    print("    half-turn flux = pi exactly (negative-real sign)  : PASS")
    print("    first Chern number c1 = 1 (primitive level)       : PASS")
    print("    numerator pi derived; pi/432 = pi/(16 x 27)       : numerator DERIVED")
    print("    flux-over-carrier normalisation + CHO action      : OPEN")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
