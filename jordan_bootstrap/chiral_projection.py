"""Gate O25 -- discharging the vector-like wall: chirality from one KO-6 idempotent.

Gate O23 hit an honest wall. It built a handedness projector ``P = (1/2)(I + i R_1)``
from a quaternion *right* multiplication, showed it commutes with the whole gauge
algebra and splits the 32-dim generation into two 16-dim halves -- but the weak
Casimir was ``-3 I`` *uniformly*, so **both** halves were weak doublets. The
construction was exactly **vector-like**, and O23 flagged an "extra by-hand
ingredient" as the missing piece.

This gate supplies that ingredient *explicitly and exactly over* ``Q(i)``, and shows
it is a *single* object, not eight per-field choices. The diagnosis of O23 is that
its projector sat on the **wrong leg** (the ``H`` factor, a spectator that commutes
with everything) and was applied to the *module* rather than built into the
*generators*. The fix, following the master-branch program (``foundations/06`` and
``compute/chiral_projector.py`` behind Zenodo 21107402), uses the aligned
**KO-dimension-6 chirality** on the ``O`` leg:

    gamma_Q = i * L_{e_1} L_{e_2} ... L_{e_6},

the ordered product of the *six* charge-carrying octonion left-multiplications,
**dropping the colour-fixing axis** ``e_7``. Exactly over ``Q(i)``:

* ``gamma_Q^2 = I`` and ``tr gamma_Q = 0`` -- a genuine chirality, eigenvalues
  ``+-1`` with 4-dim ``+`` and 4-dim ``-`` eigenspaces on the 8-dim ``O`` leg.
* ``[N, gamma_Q] = 0`` -- because ``e_7`` is dropped, the chirality **commutes with
  the charge operator** ``N`` (the naive full 6-fold product using all axes would
  not). This *alignment* is what lets the projector be gauge-compatible.

The **left projector** ``P_L = (1/2)(I + gamma_Q)`` is idempotent (``P_L^2 = P_L``),
and the physically **gauged** weak generators put it *inside* each generator, on the
``O`` leg:

    G_a = W_a (x) P_L      (a = 1, 2, 3).

The decisive exact facts:

1. **The projected generators still close as ``su(2)``.** ``[G_1, G_2] = 2 G_3``
   cyclically -- because ``P_L^2 = P_L`` (idempotency, not commutativity, rides
   through the bracket): ``[W_a (x) P_L, W_b (x) P_L] = [W_a, W_b] (x) P_L``.
2. **The gauged Casimir is chiral.** ``sum_a G_a^2 = (-3 I_H) (x) P_L`` exactly.
   On the ``gamma_Q = +1`` sector (16-dim) the Casimir is ``-3`` -- a weak
   **doublet**; on the ``gamma_Q = -1`` sector (16-dim) it is ``0`` -- a weak
   **singlet**. Left-handed doublets, right-handed singlets: the Standard-Model
   chiral pattern, from **one** idempotent.
3. **Contrast with the vector-like wall.** The *ungauged* weak Casimir
   ``sum_a W_a^2 = -3 I`` is ``-3`` on *both* ``gamma_Q`` sectors: applied to the
   module (O23's spectator) it can only ever give doublet ``+`` doublet. Gauging --
   folding ``P_L`` into the generators -- is exactly what breaks the ``L``/``R``
   symmetry.

(The campaign normalises weak isospin by ``[W_i, W_j] = 2 W_k`` with Casimir
``-3 I``; the master branch uses ``[T_a, T_b] = i eps_abc T_c`` with Casimir
``(3/4) I``. These are the same ``su(2)`` in different normalisations; the doublet
vs. singlet *split* is normalisation-independent.)

Non-claim: this is an *adopted* ingredient, not a forced one. The choice of the
aligned KO-6 chirality ``gamma_Q`` (equivalently, which sector is called
"left-handed") is a convention inherited from the Furey/Dixon and master-branch
program (Lever B), not something ``C (x) H (x) O`` selects on its own. What this
gate *does* establish exactly is that **a single KO-dimension-6 idempotent**, once
adopted, converts the O23 vector-like content into the genuinely chiral
doublet-left / singlet-right Standard-Model pattern -- replacing the informal
"extra by-hand ingredient" with one explicit, exactly-checkable object. The Yukawa
spectrum, the Higgs, and three generations remain outside this gate.

See also (master branch, behind Zenodo 21107402): ``foundations/06_chiral_idempotent.md``
and ``compute/chiral_projector.py``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Tuple

from amplitude_bootstrap.gaussian import Gaussian

from .fermion_charges import clifford_generators, number_operator
from .standard_model import (
    CMatrix,
    _cmul,
    _commutator,
    _cscale,
    _identity,
    _kron,
    weak_generators,
)

_ZERO = Gaussian(0, 0)
_ONE = Gaussian(1, 0)
_I = Gaussian(0, 1)
_TWO = Gaussian(2, 0)
_HALF = Gaussian(Fraction(1, 2), 0)

_DIM_O = 8
_DIM_H = 4
_MODULE = _DIM_H * _DIM_O  # 32


def _cadd(a: CMatrix, b: CMatrix) -> CMatrix:
    return tuple(
        tuple(a[i][j] + b[i][j] for j in range(len(a[0]))) for i in range(len(a))
    )


def _trace(a: CMatrix) -> Gaussian:
    return sum((a[i][i] for i in range(len(a))), _ZERO)


def _matrix_rank(a: CMatrix) -> int:
    """Exact row rank over ``Q(i)`` of a single square matrix (field elimination)."""
    rows = [list(r) for r in a]
    n = len(rows[0]) if rows else 0
    pivot = 0
    for col in range(n):
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
                rows[r] = [x - f * y for x, y in zip(rows[r], rows[pivot])]
        pivot += 1
    return pivot


def _nullity(a: CMatrix) -> int:
    return len(a) - _matrix_rank(a)


def aligned_chirality() -> CMatrix:
    """The KO-6 chirality ``gamma_Q = i * L_{e_1} ... L_{e_6}`` on the 8-dim ``O`` leg.

    The ordered product runs over the *six* charge-carrying imaginary octonion
    left-multiplications, dropping the colour-fixing axis ``e_7``.
    """
    lefts = clifford_generators()  # L_{e_1} .. L_{e_7}
    product = _identity(_DIM_O)
    for k in range(6):  # e_1 .. e_6, dropping e_7
        product = _cmul(product, lefts[k])
    return _cscale(product, _I)


def left_projector() -> CMatrix:
    """The left-handed idempotent ``P_L = (1/2)(I + gamma_Q)`` on the ``O`` leg."""
    return _cscale(_cadd(_identity(_DIM_O), aligned_chirality()), _HALF)


def right_projector() -> CMatrix:
    """The right-handed idempotent ``P_R = (1/2)(I - gamma_Q)`` on the ``O`` leg."""
    gamma = aligned_chirality()
    return _cscale(_cadd(_identity(_DIM_O), _cscale(gamma, Gaussian(-1, 0))), _HALF)


def chirality_is_involution() -> bool:
    """Exact check ``gamma_Q^2 = I`` (a genuine chirality)."""
    gamma = aligned_chirality()
    return _cmul(gamma, gamma) == _identity(_DIM_O)


def chirality_is_traceless() -> bool:
    """Exact check ``tr gamma_Q = 0`` (balanced ``+-1`` eigenspaces)."""
    return _trace(aligned_chirality()) == _ZERO


def chirality_eigendimensions() -> Tuple[int, int]:
    """Dimensions of the ``gamma_Q = +1`` and ``gamma_Q = -1`` eigenspaces on ``O``."""
    gamma = aligned_chirality()
    ident = _identity(_DIM_O)
    plus = _nullity(_cadd(gamma, _cscale(ident, Gaussian(-1, 0))))
    minus = _nullity(_cadd(gamma, ident))
    return (plus, minus)


def chirality_commutes_with_charge() -> bool:
    """Exact check ``[N, gamma_Q] = 0`` -- the alignment condition (drop ``e_7``)."""
    gamma = aligned_chirality()
    n = number_operator()
    comm = _commutator(n, gamma)
    return all(x == _ZERO for row in comm for x in row)


def projector_is_idempotent() -> bool:
    """Exact check ``P_L^2 = P_L``."""
    p = left_projector()
    return _cmul(p, p) == p


def gauged_generators() -> List[CMatrix]:
    """The chirally-gauged weak generators ``G_a = W_a (x) P_L`` (32x32)."""
    w = [_weak_quaternion(k) for k in (1, 2, 3)]
    p = left_projector()
    return [_kron(wa, p) for wa in w]


def _weak_quaternion(k: int) -> CMatrix:
    """The bare weak generator ``W_k`` on the ``H`` leg (4x4), from O13/O20."""
    from .weak_isospin import _complexify, quaternion_left_mult

    return _complexify(quaternion_left_mult(k))


def gauged_su2_relations() -> bool:
    """Exact check ``[G_1, G_2] = 2 G_3`` cyclically (survives because ``P_L^2=P_L``)."""
    g = gauged_generators()
    return (
        _commutator(g[0], g[1]) == _cscale(g[2], _TWO)
        and _commutator(g[1], g[2]) == _cscale(g[0], _TWO)
        and _commutator(g[2], g[0]) == _cscale(g[1], _TWO)
    )


def gauged_casimir() -> CMatrix:
    """The gauged weak Casimir ``sum_a G_a^2`` (32x32)."""
    g = gauged_generators()
    total = tuple(tuple(_ZERO for _ in range(_MODULE)) for _ in range(_MODULE))
    for ga in g:
        total = _cadd(total, _cmul(ga, ga))
    return total


def casimir_equals_projector_form() -> bool:
    """Exact check ``sum_a G_a^2 = (-3 I_H) (x) P_L`` -- the chiral Casimir."""
    target = _kron(_cscale(_identity(_DIM_H), Gaussian(-3, 0)), left_projector())
    return gauged_casimir() == target


def left_handed_dimension() -> int:
    """Dimension of the weak-doublet (Casimir ``-3``) left-handed sector."""
    cas = gauged_casimir()
    ident = _identity(_MODULE)
    return _nullity(_cadd(cas, _cscale(ident, Gaussian(3, 0))))


def right_handed_dimension() -> int:
    """Dimension of the weak-singlet (Casimir ``0``) right-handed sector."""
    return _nullity(gauged_casimir())


def is_chiral() -> bool:
    """The reconciliation: a 16-dim weak-doublet ``L`` and 16-dim weak-singlet ``R``.

    Genuinely chiral (inequivalent weak reps on the two halves) -- discharging the
    O23 vector-like wall.
    """
    return left_handed_dimension() == 16 and right_handed_dimension() == 16


def ungauged_casimir_is_vector_like() -> bool:
    """Contrast: bare weak Casimir ``sum_a W_a^2 = -3 I`` -- ``-3`` on *both* sectors.

    This is O23's spectator failure: applied to the module (not folded into the
    generators) the weak Casimir is uniform, so both chirality halves are doublets.
    """
    w = weak_generators()
    total = tuple(tuple(_ZERO for _ in range(_MODULE)) for _ in range(_MODULE))
    for wa in w:
        total = _cadd(total, _cmul(wa, wa))
    target = _cscale(_identity(_MODULE), Gaussian(-3, 0))
    return total == target


@dataclass(frozen=True)
class ChiralProjectionCensus:
    """Exact ledger of the O25 chiral reconciliation over ``Q(i)``."""

    chirality_involution: bool
    chirality_traceless: bool
    eigendimensions: Tuple[int, int]
    commutes_with_charge: bool
    projector_idempotent: bool
    gauged_su2: bool
    casimir_chiral: bool
    left_dimension: int
    right_dimension: int
    is_chiral: bool
    ungauged_vector_like: bool


def chiral_projection_census() -> ChiralProjectionCensus:
    """Assemble the exact O25 ledger."""
    return ChiralProjectionCensus(
        chirality_involution=chirality_is_involution(),
        chirality_traceless=chirality_is_traceless(),
        eigendimensions=chirality_eigendimensions(),
        commutes_with_charge=chirality_commutes_with_charge(),
        projector_idempotent=projector_is_idempotent(),
        gauged_su2=gauged_su2_relations(),
        casimir_chiral=casimir_equals_projector_form(),
        left_dimension=left_handed_dimension(),
        right_dimension=right_handed_dimension(),
        is_chiral=is_chiral(),
        ungauged_vector_like=ungauged_casimir_is_vector_like(),
    )
