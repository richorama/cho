"""Gate O15 -- the octonionic dynamics wall, measured exactly.

Every earlier gate lives in *kinematics*: which states, frames, charges and gauge
algebras the division algebras permit. This gate confronts the one thing the
octonions are famous for *breaking* -- **dynamics**.

Ordinary quantum evolution is a one-parameter unitary group ``U(t) = exp(-iHt)``.
Two facts make it work: (i) ``U(t)U(s) = U(t+s)`` closes because a single
generator associates with itself, and (ii) *independent* evolutions compose
through Baker--Campbell--Hausdorff, whose consistency is exactly the **Jacobi
identity** -- i.e. the generators form a *Lie algebra*. Over the octonions this
second pillar collapses, and this gate measures precisely how, keeping every
number an exact rational.

What survives (the flow still runs):

* **Alternativity / power-associativity.** The associator ``[x,y,z]=(xy)z-x(yz)``
  is totally alternating, so a *single* generator integrates to a well-defined,
  norm-preserving one-parameter flow. A lone octonionic "clock" is fine.
* **Moufang identities.** The rigid substitutes for associativity hold exactly on
  every basis triple -- the octonions are not lawless, they are a Moufang loop.
* **Isometry.** Because ``O`` is a normed algebra, ``|ux| = |u||x|`` even without
  associativity, so a discrete flow ``x_{n+1} = u x_n`` by a unit ``u`` preserves
  the norm exactly: evolution is still "unitary-like" (isometric).

What breaks (the wall):

* **Jacobi fails.** The commutator Jacobiator ``J(x,y,z)=[[x,y],z]+cyc`` is
  *nonzero* on ``168`` of the ``343`` imaginary basis triples. The imaginary
  octonions under ``[,]`` are therefore **not a Lie algebra**: there is no
  octonionic unitary group and no ordinary way to compose two independent
  evolutions.
* **The obstruction is exactly the non-associativity.** Not noise:
  ``J(x,y,z) = 6 [x,y,z]`` identically. The failure to compose evolutions *is*
  six times the associator -- one algebraic quantity governs both.
* **Path-ordering defect.** Composing two flow steps two ways,
  ``(uv)x`` vs ``u(vx)``, gives two *different* (both unit-norm) states whose
  difference is exactly the associator ``[u,v,x]``. This is the observable
  dynamical signature of the wall.

What replaces the Lie law:

* **Malcev structure.** The generators do not close into a Lie algebra but they do
  close into a **Malcev algebra**: the Malcev identity
  ``J(x,y,[x,z]) = [J(x,y,z),x]`` holds *exactly* on every one of the ``343``
  imaginary basis triples. Octonionic infinitesimal dynamics is not undefined --
  it is governed by the strictly weaker, non-Lie Malcev law.

Non-claim: this gate does **not** construct an octonionic quantum dynamics or a
new equation of motion. It proves the exact *obstruction* to the usual one (a
machine-checked no-go: Jacobi fails, hence no unitary group) and identifies the
precise algebraic structure any octonionic dynamics must respect (Malcev, not
Lie). It says what survives (isometric single-generator flow, Moufang, Malcev)
and what cannot survive (a Lie algebra of generators), and nothing more.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import List, Tuple

from .octonion import E, Octonion, Rational, octonion

# The seven imaginary basis units e_1..e_7 (e_0 = 1 is the real unit).
IMAGINARY_INDICES: Tuple[int, ...] = tuple(range(1, 8))


def commutator(x: Octonion, y: Octonion) -> Octonion:
    """The additive commutator ``[x, y] = xy - yx``."""
    return x * y - y * x


def associator(x: Octonion, y: Octonion, z: Octonion) -> Octonion:
    """The associator ``[x, y, z] = (xy)z - x(yz)`` -- zero iff the triple associates."""
    return (x * y) * z - x * (y * z)


def jacobiator(x: Octonion, y: Octonion, z: Octonion) -> Octonion:
    """The Jacobiator ``[[x,y],z] + [[y,z],x] + [[z,x],y]`` -- zero iff Jacobi holds."""
    return (
        commutator(commutator(x, y), z)
        + commutator(commutator(y, z), x)
        + commutator(commutator(z, x), y)
    )


def malcev_defect(x: Octonion, y: Octonion, z: Octonion) -> Octonion:
    """``J(x, y, [x, z]) - [J(x, y, z), x]`` -- zero iff the Malcev identity holds here."""
    lhs = jacobiator(x, y, commutator(x, z))
    rhs = commutator(jacobiator(x, y, z), x)
    return lhs - rhs


def is_alternative() -> bool:
    """Exact check that the associator is totally alternating (``O`` is alternative)."""
    for i in range(8):
        for j in range(8):
            if not associator(E[i], E[i], E[j]).is_zero():
                return False
            if not associator(E[i], E[j], E[i]).is_zero():
                return False
            if not associator(E[i], E[j], E[j]).is_zero():
                return False
    return True


def moufang_identities_hold() -> bool:
    """Exact check of the three Moufang identities on every basis triple."""
    for i in range(8):
        for j in range(8):
            for k in range(8):
                x, y, z = E[i], E[j], E[k]
                left = x * (y * (x * z)) == (x * (y * x)) * z
                right = ((z * x) * y) * x == z * (x * (y * x))
                central = (x * y) * (z * x) == x * ((y * z) * x)
                if not (left and right and central):
                    return False
    return True


def jacobi_failure_count() -> Tuple[int, int]:
    """``(fails, total)`` over imaginary basis triples: how many break Jacobi."""
    fails = 0
    total = 0
    for i, j, k in product(IMAGINARY_INDICES, repeat=3):
        total += 1
        if not jacobiator(E[i], E[j], E[k]).is_zero():
            fails += 1
    return fails, total


def jacobiator_equals_six_associator() -> bool:
    """Exact identity ``J(x,y,z) = 6 [x,y,z]`` on every imaginary basis triple."""
    for i, j, k in product(IMAGINARY_INDICES, repeat=3):
        j_ijk = jacobiator(E[i], E[j], E[k])
        a_ijk = associator(E[i], E[j], E[k]).scaled(6)
        if j_ijk != a_ijk:
            return False
    return True


def malcev_identity_holds() -> bool:
    """Exact check that the Malcev identity holds on every imaginary basis triple."""
    for i, j, k in product(IMAGINARY_INDICES, repeat=3):
        if not malcev_defect(E[i], E[j], E[k]).is_zero():
            return False
    return True


def flow_orbit(u: Octonion, x0: Octonion, steps: int) -> List[Octonion]:
    """The discrete single-generator flow ``x_{n+1} = u x_n`` for ``steps`` steps."""
    orbit = [x0]
    x = x0
    for _ in range(steps):
        x = u * x
        orbit.append(x)
    return orbit


def flow_is_isometric(u: Octonion, x0: Octonion, steps: int) -> bool:
    """Exact check that a unit-generator flow preserves the norm at every step."""
    if u.norm2() != 1:
        raise ValueError("flow generator must be a unit octonion")
    n0 = x0.norm2()
    return all(x.norm2() == n0 for x in flow_orbit(u, x0, steps))


def ordering_defect(u: Octonion, v: Octonion, x: Octonion) -> Octonion:
    """Path-ordering defect ``(uv)x - u(vx)`` of composing two flow steps."""
    return (u * v) * x - u * (v * x)


@dataclass(frozen=True)
class DynamicsWallCensus:
    """The exact ledger of what survives and what breaks for octonionic dynamics."""

    alternative: bool
    moufang: bool
    single_generator_flow_isometric: bool
    jacobi_failures: int
    jacobi_triples: int
    is_lie_algebra: bool
    jacobiator_is_six_associator: bool
    ordering_defect_is_associator: bool
    ordering_defect_nonzero: bool
    malcev_identity: bool


# A fixed rational witness pair for the path-ordering defect: two imaginary unit
# octonions built from Pythagorean pairs, acting on an imaginary state.
_U_WITNESS = octonion(0, Fraction(3, 5), Fraction(4, 5), 0, 0, 0, 0, 0)
_V_WITNESS = octonion(0, 0, 0, Fraction(5, 13), Fraction(12, 13), 0, 0, 0)
_X_WITNESS = E[5]


def dynamics_wall_census() -> DynamicsWallCensus:
    """Assemble the exact dynamics-wall ledger over ``Q``."""
    fails, total = jacobi_failure_count()

    defect = ordering_defect(_U_WITNESS, _V_WITNESS, _X_WITNESS)
    defect_is_assoc = defect == associator(_U_WITNESS, _V_WITNESS, _X_WITNESS)

    return DynamicsWallCensus(
        alternative=is_alternative(),
        moufang=moufang_identities_hold(),
        single_generator_flow_isometric=flow_is_isometric(_U_WITNESS, _X_WITNESS, 6),
        jacobi_failures=fails,
        jacobi_triples=total,
        is_lie_algebra=(fails == 0),
        jacobiator_is_six_associator=jacobiator_equals_six_associator(),
        ordering_defect_is_associator=defect_is_assoc,
        ordering_defect_nonzero=not defect.is_zero(),
        malcev_identity=malcev_identity_holds(),
    )
