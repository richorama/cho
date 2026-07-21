"""Gate O22 -- one generation's Standard-Model multiplets on C (x) H (x) O.

Gate O20 assembled the gauge *algebra* ``su(3) (+) su(2) (+) u(1)`` on ``C (x) H (x)
O`` and Gate O21 proved colour ``su(3)`` is the *forced* number-preserving
symmetry of the ``O`` factor, acting as ``1 (+) 3 (+) 3bar (+) 1``. This gate
completes the picture on the full module: it shows the 32-dimensional space
(``H (x) O`` over ``Q(i)``) decomposes, under the commuting colour ``su(3)`` and
weak ``su(2)``, into exactly the quark/lepton weak-doublet pattern of one
Standard-Model generation -- with each tensor factor's representation content
proven exactly.

Because colour acts on the ``O`` factor and weak on the ``H`` factor (they commute,
Gate O20), the module is the ``su(3) x su(2)`` tensor product of the two factors,
and its multiplet content is the product of theirs. Verified exactly over
``Q(i)``:

1. **The weak content is pure doublets.** The weak quadratic Casimir
   ``sum_i W_i^2 = -3 I`` *uniformly* on the whole space (the value for spin-1/2),
   and the weak generators have trivial common kernel: **no weak singlets**. Every
   state sits in a weak doublet -- the ``H`` factor is ``2 (+) 2``.

2. **The colour content is ``1 (+) 3 (+) 3bar (+) 1``** (Gate O21). On the full
   module the colour generators' common kernel -- the colour-singlet subspace -- has
   dimension ``8``: the two ``O``-factor singlets times the four-dimensional weak
   factor. These are the **leptons**.

3. **The multiplet pattern is one generation.** The 32 states split into
   ``8`` colour-singlet weak-doublet states (**leptons**, ``(1,2)``) and ``24``
   colour-triplet weak-doublet states (**quarks**, ``(3,2) (+) (3bar,2)``). This is
   the Standard Model's central qualitative fact -- quarks are colour-triplet weak
   doublets, leptons are colour-singlet weak doublets -- realised exactly as a
   tensor decomposition of ``C (x) H (x) O``.

Non-claim: this exhibits the quark/lepton weak-doublet **multiplet pattern** of one
generation. As in every ``C (x) H (x) O`` construction it appears *doubled*
(particles and antiparticles both present -- the ``3`` and ``3bar``, the two ``O``
singlets, the two weak doublets); it is *not* the chiral (left-only) content, *not*
the hypercharge assignment that splits the doublets, *not* three generations, and
carries no dynamics. The colour--weak product itself is structural (independent
Cayley-Dickson factors, Gate O20), so this is a forced multiplet *pattern* given
the ``C (x) H (x) O`` construction, not a derivation of that construction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence, Tuple

from amplitude_bootstrap.gaussian import Gaussian

from .standard_model import (
    CMatrix,
    _cmul,
    _cscale,
    _csub,
    _identity,
    colour_generators,
    weak_generators,
)

_ZERO = Gaussian(0, 0)
_MODULE_DIM = 32


def weak_casimir() -> CMatrix:
    """The weak quadratic Casimir ``sum_i W_i^2`` on the 32-dim module."""
    gens = weak_generators()
    total = tuple(tuple(_ZERO for _ in range(_MODULE_DIM)) for _ in range(_MODULE_DIM))
    for g in gens:
        total = tuple(
            tuple(total[i][j] + p for j, p in enumerate(row))
            for i, row in enumerate(_cmul(g, g))
        )
    return total


def weak_casimir_is_uniform_doublet() -> bool:
    """Exact check ``sum_i W_i^2 = -3 I`` -- every state is a spin-1/2 doublet."""
    target = _cscale(_identity(_MODULE_DIM), Gaussian(-3, 0))
    return _csub(weak_casimir(), target) == tuple(
        tuple(_ZERO for _ in range(_MODULE_DIM)) for _ in range(_MODULE_DIM)
    )


def _common_kernel_dimension(mats: Sequence[CMatrix]) -> int:
    """Dimension of the simultaneous kernel of ``mats`` (the singlet subspace)."""
    rows: List[List[Gaussian]] = [list(m[i]) for m in mats for i in range(_MODULE_DIM)]
    if not rows:
        return _MODULE_DIM
    width = len(rows[0])
    pivot = 0
    for col in range(width):
        sel = None
        for r in range(pivot, len(rows)):
            if rows[r][col] != _ZERO:
                sel = r
                break
        if sel is None:
            continue
        rows[pivot], rows[sel] = rows[sel], rows[pivot]
        piv = rows[pivot][col]
        rows[pivot] = [x / piv for x in rows[pivot]]
        for r in range(len(rows)):
            if r != pivot and rows[r][col] != _ZERO:
                f = rows[r][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[pivot])]
        pivot += 1
    return width - pivot


def weak_singlet_dimension() -> int:
    """Dimension of the weak-singlet subspace (``= 0``: no weak singlets)."""
    return _common_kernel_dimension(weak_generators())


def lepton_dimension() -> int:
    """Colour-singlet subspace dimension -- the leptons (``= 8``)."""
    return _common_kernel_dimension(colour_generators())


def quark_dimension() -> int:
    """Colour-triplet subspace dimension -- the quarks (``= 24``)."""
    return _MODULE_DIM - lepton_dimension()


@dataclass(frozen=True)
class GenerationMultipletCensus:
    """Exact ledger of one generation's SM multiplet pattern on C (x) H (x) O."""

    module_dimension: int
    weak_casimir_uniform_doublet: bool
    weak_singlet_dimension: int
    lepton_dimension: int
    quark_dimension: int
    is_one_generation_pattern: bool


def generation_multiplet_census() -> GenerationMultipletCensus:
    """Assemble the exact multiplet-pattern ledger over ``Q(i)``."""
    doublet = weak_casimir_is_uniform_doublet()
    weak_singlets = weak_singlet_dimension()
    leptons = lepton_dimension()
    quarks = quark_dimension()
    return GenerationMultipletCensus(
        module_dimension=_MODULE_DIM,
        weak_casimir_uniform_doublet=doublet,
        weak_singlet_dimension=weak_singlets,
        lepton_dimension=leptons,
        quark_dimension=quarks,
        is_one_generation_pattern=(
            doublet and weak_singlets == 0 and leptons == 8 and quarks == 24
        ),
    )
