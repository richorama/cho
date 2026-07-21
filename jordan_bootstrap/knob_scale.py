"""Gate O31 -- the knob denominator ``432 = 16 x 27`` as (Weyl count) x (dim J_3(O)).

Gates O28-O30 all *adopted* a single flavour scale ``eps0^2 = pi/432`` and worked in
its ratios so the knob cancelled. This gate takes one honest step *into* the knob:
the integer ``432`` is not free -- it is the product of two dimensions the campaign
has already computed exactly from the algebra,

    432 = 16 x 27 = (one chirality's Weyl-fermion count) x dim J_3(O),

so ``eps0^2 = pi / (16 * 27)``. Porting the master ``compute/mass_relations.py``
derivation ``eps0^2 = pi / (dim_C(A) * dim(J_3(O)))`` behind Zenodo 21107402, but
anchoring the ``16`` to the campaign's *own* chiral count rather than a fuzzy
``dim_C(A)``.

The two factors, from prior gates (exact over Q)
------------------------------------------------
1. **``16`` -- one chirality of one generation.** Gate O25 gauged the weak ``su(2)``
   with the aligned chirality ``gamma_Q`` and split the 32-dim ``H (x) O`` generation
   into a 16-dim left-handed weak **doublet** and a 16-dim right-handed weak
   **singlet**. That ``16`` is exactly one generation's Weyl-fermion count of a single
   chirality (the ``16`` of ``SO(10)``): ``chiral_weyl_count() = left_handed_dimension()``.
2. **``27`` -- the Jordan algebra.** Gate O24 built ``J_3(O)`` as a 27-dim real space
   (``3`` diagonal generation slots + ``24`` octonionic off-diagonal), so
   ``jordan_dimension() = generation_slot_dimension() + offdiagonal_dimension() = 27``.

Their product is the knob denominator used by O28/O29/O30:

    knob_denominator() = 16 * 27 = 432,   and   eps0^2 = pi / 432 ~ 0.007272.

A second exact integer factorisation ``432 = 24 x 18`` records the master's Higgs
route ``eps0^2 = lambda_Higgs / 18 = (pi/24) / 18`` (``lambda_Higgs = pi/24``,
``18 = 2 x 9`` the Higgs doublet times the see-saw exponent). Both factorisations of
the *same* ``432`` are checked here as consistency; only the ``16 x 27`` one is
anchored to computed campaign dimensions.

Non-claim: what is exact here is only the integer identity ``432 = 16 x 27`` with
``16`` and ``27`` the campaign's already-tested chiral Weyl count and ``dim J_3(O)``.
Still **adopted**, not derived: the numerator ``pi`` (a geometric half-rotation /
Berry phase on the ``G_2/SU(3) ~ S^6`` coset, master interpretation), and the very
claim that the flavour scale *is* ``pi`` divided by this product (that ``eps0^2`` has
this form at all, and equals ``m_c/m_t``). Note also that ``432`` has other
factorisations; the ``16 x 27`` reading is *selected* because both factors are
algebra-native dimensions the campaign computes, not because ``432`` forces it. No
new observable and no dynamics follow -- this gate only makes the adopted denominator
structural. Cross-refs master ``compute/mass_relations.py``.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction

from .chiral_projection import left_handed_dimension
from .three_generations import generation_slot_dimension, offdiagonal_dimension

# The adopted knob, as used numerically by Gates O28/O29/O30.
_EPS0_SQ = math.pi / 432.0


# ---------------------------------------------------------------------------
# The two algebra-native factors, imported from prior gates.
# ---------------------------------------------------------------------------


def chiral_weyl_count() -> int:
    """One chirality of one generation = ``16`` (Gate O25's left-handed dimension)."""
    return left_handed_dimension()


def jordan_dimension() -> int:
    """``dim J_3(O) = 27`` = 3 diagonal generation slots + 24 octonionic off-diagonal."""
    return generation_slot_dimension() + offdiagonal_dimension()


# ---------------------------------------------------------------------------
# The knob denominator and its two exact factorisations.
# ---------------------------------------------------------------------------


def knob_denominator() -> int:
    """The denominator of ``eps0^2 = pi/432``, as ``(Weyl count) x (dim J_3(O))``."""
    return chiral_weyl_count() * jordan_dimension()


def denominator_is_432() -> bool:
    """``16 * 27 = 432`` -- the adopted flavour-scale denominator, from computed dims."""
    return knob_denominator() == 432


def higgs_factorisation() -> tuple[int, int]:
    """The master's second reading ``432 = 24 * 18`` (``lambda_Higgs=pi/24``, ``18=2*9``)."""
    return (24, 18)


def factorisations_agree() -> bool:
    """Both exact factorisations multiply to the same ``432``."""
    a, b = higgs_factorisation()
    return a * b == knob_denominator() == 432


def eps0_squared_exact_denominator() -> Fraction:
    """The exact rational ``1/432`` multiplying ``pi`` in ``eps0^2 = pi/432``."""
    return Fraction(1, knob_denominator())


# ---------------------------------------------------------------------------
# Numerical cross-check against the value used by O28/O29/O30.
# ---------------------------------------------------------------------------


def eps0_squared() -> float:
    """``eps0^2 = pi / (16 * 27)`` -- identical to the knob adopted by O28/O29/O30."""
    return math.pi / knob_denominator()


def matches_adopted_scale() -> bool:
    """The reconstructed ``pi/(16*27)`` equals the ``pi/432`` used downstream."""
    return math.isclose(eps0_squared(), _EPS0_SQ, rel_tol=1e-15)


# ---------------------------------------------------------------------------
# Census.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class KnobScaleCensus:
    chiral_weyl_count: int
    jordan_dimension: int
    knob_denominator: int
    denominator_is_432: bool
    higgs_factorisation: tuple[int, int]
    factorisations_agree: bool
    eps0_squared: float
    matches_adopted_scale: bool


def knob_scale_census() -> KnobScaleCensus:
    return KnobScaleCensus(
        chiral_weyl_count=chiral_weyl_count(),
        jordan_dimension=jordan_dimension(),
        knob_denominator=knob_denominator(),
        denominator_is_432=denominator_is_432(),
        higgs_factorisation=higgs_factorisation(),
        factorisations_agree=factorisations_agree(),
        eps0_squared=eps0_squared(),
        matches_adopted_scale=matches_adopted_scale(),
    )


if __name__ == "__main__":
    census = knob_scale_census()
    print("Gate O31 -- knob denominator 432 = 16 x 27")
    print(f"  chiral Weyl count (O25)   = {census.chiral_weyl_count}")
    print(f"  dim J_3(O)        (O24)   = {census.jordan_dimension}")
    print(f"  knob denominator          = {census.knob_denominator} "
          f"(is 432: {census.denominator_is_432})")
    print(f"  Higgs factorisation       = {census.higgs_factorisation[0]} x "
          f"{census.higgs_factorisation[1]} (agrees: {census.factorisations_agree})")
    print(f"  eps0^2 = pi/(16*27)       = {census.eps0_squared:.7f} "
          f"(matches adopted: {census.matches_adopted_scale})")
