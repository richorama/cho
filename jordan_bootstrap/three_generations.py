"""Gate O24 -- three generations as a Jordan frame of J_3(O).

Gate O12 showed the *triality* route to three generations fails: the three
triality-related ``C (x) O`` ladder towers coincide, giving one tower, not three.
This gate implements the alternative that survives -- following Dubois-Violette--
Todorov and Boyle, and the author's own delimitation (Zenodo 21107402):
**identify the three generations with the three primitive idempotents of a Jordan
frame of the exceptional Jordan algebra** ``J = J_3(O)`` (Gate O02's ``h_3(O)``).

A Jordan frame is a resolution of the identity into three orthogonal rank-one
idempotents ``{E_1, E_2, E_3}`` -- the *rank* of ``J_3(O)`` is three, and that is
the family count. Relative to a frame, ``J`` has the **Peirce decomposition**

    J = (J_11 (+) J_22 (+) J_33) (+) (J_12 (+) J_13 (+) J_23),

three one-dimensional diagonal *generation slots* (each ``J_ii = R E_i``) plus
three eight-dimensional octonionic off-diagonal slots -- dimensions
``3 + 3*8 = 27 = dim J_3(O)``. Each ``E_i`` is picked out by the eigenvalue-1 space
of Jordan multiplication ``L_{E_i}``, whose Peirce spectrum is exactly
``{1: 1, 1/2: 16, 0: 10}``.

Exact facts over the rationals:

1. **Family count three.** The frame is exactly three primitive idempotents that
   resolve the identity (``sum_i E_i = I``, ``E_i o E_j = 0`` for ``i != j``): rank
   ``J_3(O) = 3``.
2. **Genuinely three (not one).** The three idempotents are *linearly independent*
   in the 27-dim ``J`` (span dimension ``3``) -- unlike the O12 triality towers,
   which coincided. This is the exact contrast between the two routes.
3. **Peirce decomposition.** The three diagonal generation slots have total
   dimension ``3`` (each ``J_ii = R E_i``); the octonionic off-diagonals total
   ``24``; together ``27``. Each ``L_{E_i}`` has the Peirce spectrum
   ``{1: 1, 1/2: 16, 0: 10}``.

Non-claim: the count three is the *rank* of ``J_3(O)``, **adopted** here following
Boyle / Dubois-Violette--Todorov, **not derived** from ``C (x) H (x) O`` -- the
``C (x) H (x) O`` <-> ``J_3(O)`` bridge is an open problem, not a theorem. The
value of the idempotent identification is structural: because the generations are a
resolution of the identity rather than triality-permuted representations (O12),
this route is *not* subject to the Distler--Garibaldi obstruction at the level of
count and chirality. It fixes neither the mass hierarchy nor the mixing angles
(the algebra fixes a mixing law but selects no hierarchy -- Zenodo 21107402).

This gate is the exact-over-``Q`` count-and-Peirce core of a fuller (numpy-based)
treatment on the repository's ``master`` branch -- ``compute/three_generations_frame.py``
(the inner ``F4`` frame-Weyl ``S3``, ``OP^2 = F4/Spin(9)``, isotropy ``dim 36 =
spin(9)`` and 16-dim real-spinor tangent), ``compute/jordan_eigenvalue_generations.py``
(the Freudenthal-cubic "why three"), and ``compute/three_generations_nogo_audit.py``
(the triality no-go control). Those cover the ``F4/Spin(9)`` and chirality legs this
gate does not; here everything is re-derived exactly over the rationals.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, List, Sequence, Tuple

from .octonion import E, Octonion, octonion
from .jordan import (
    JMat,
    is_jordan_frame,
    jordan_product,
    outer,
)

_ZERO_O = octonion(0, 0, 0, 0, 0, 0, 0, 0)
_ONE_O = octonion(1, 0, 0, 0, 0, 0, 0, 0)
_DIM = 27
_OFF = ((0, 1), (0, 2), (1, 2))


def _unit_vector(i: int) -> Tuple[Octonion, ...]:
    return tuple(_ONE_O if t == i else _ZERO_O for t in range(3))


def standard_generation_frame() -> List[JMat]:
    """The frame of three diagonal primitive idempotents ``E_i = e_i e_i^dagger``."""
    return [outer(_unit_vector(i)) for i in range(3)]


def family_count() -> int:
    """The rank of ``J_3(O)`` -- the number of idempotents in a frame (``= 3``)."""
    return len(standard_generation_frame())


def frame_resolves_identity() -> bool:
    """Exact check the frame is three orthogonal primitive idempotents summing to I."""
    return is_jordan_frame(standard_generation_frame())


def _flatten(a: JMat) -> List[Fraction]:
    """The 27 real coordinates of a Hermitian ``J_3(O)`` element."""
    coords: List[Fraction] = [a[i][i].coords[0] for i in range(3)]
    for (i, j) in _OFF:
        coords.extend(a[i][j].coords)
    return coords


def _rank(rows: Sequence[Sequence[Fraction]]) -> int:
    rows = [list(r) for r in rows]
    if not rows:
        return 0
    width = len(rows[0])
    pivot = 0
    for col in range(width):
        sel = None
        for r in range(pivot, len(rows)):
            if rows[r][col] != 0:
                sel = r
                break
        if sel is None:
            continue
        rows[pivot], rows[sel] = rows[sel], rows[pivot]
        piv = rows[pivot][col]
        rows[pivot] = [x / piv for x in rows[pivot]]
        for r in range(len(rows)):
            if r != pivot and rows[r][col] != 0:
                f = rows[r][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[pivot])]
        pivot += 1
    return pivot


def idempotent_span_dimension() -> int:
    """Linear span of the three frame idempotents in ``J`` (``= 3``: genuinely three)."""
    return _rank([_flatten(p) for p in standard_generation_frame()])


def _hermitian_basis() -> List[JMat]:
    """A basis of the 27-dim real space of Hermitian ``J_3(O)`` matrices."""
    basis: List[JMat] = []
    for i in range(3):
        rows = [[_ZERO_O] * 3 for _ in range(3)]
        rows[i][i] = _ONE_O
        basis.append(tuple(tuple(r) for r in rows))
    for (i, j) in _OFF:
        for k in range(8):
            rows = [[_ZERO_O] * 3 for _ in range(3)]
            rows[i][j] = E[k]
            rows[j][i] = E[k].conjugate()
            basis.append(tuple(tuple(r) for r in rows))
    return basis


def _left_mult_matrix(idem: JMat) -> List[List[Fraction]]:
    """Matrix of Jordan multiplication ``x -> E o x`` in the Hermitian basis."""
    basis = _hermitian_basis()
    cols = [_flatten(jordan_product(idem, b)) for b in basis]
    return [[cols[c][r] for c in range(_DIM)] for r in range(_DIM)]


def peirce_spectrum(idem: JMat) -> Dict[str, int]:
    """Peirce eigenvalue multiplicities of ``L_E`` (``{1: 1, 1/2: 16, 0: 10}``)."""
    mat = _left_mult_matrix(idem)
    out: Dict[str, int] = {}
    for lam, key in ((Fraction(0), "0"), (Fraction(1, 2), "1/2"), (Fraction(1), "1")):
        shifted = [
            [mat[i][j] - (lam if i == j else Fraction(0)) for j in range(_DIM)]
            for i in range(_DIM)
        ]
        out[key] = _DIM - _rank(shifted)
    return out


def generation_slot_dimension() -> int:
    """Total dimension of the three diagonal Peirce (generation) slots (``= 3``)."""
    return sum(peirce_spectrum(e)["1"] for e in standard_generation_frame())


def offdiagonal_dimension() -> int:
    """Total dimension of the octonionic off-diagonal Peirce slots (``= 24``)."""
    return _DIM - generation_slot_dimension()


@dataclass(frozen=True)
class GenerationFrameCensus:
    """Exact ledger: three generations as a Jordan frame of ``J_3(O)``."""

    family_count: int
    frame_resolves_identity: bool
    idempotent_span_dimension: int
    peirce_spectrum: Tuple[Tuple[str, int], ...]
    generation_slot_dimension: int
    offdiagonal_dimension: int
    total_dimension: int
    is_rank_three_frame: bool


def generation_frame_census() -> GenerationFrameCensus:
    """Assemble the exact three-generation frame ledger over the rationals."""
    frame = standard_generation_frame()
    spectrum = peirce_spectrum(frame[0])
    slots = generation_slot_dimension()
    offdiag = offdiagonal_dimension()
    span = idempotent_span_dimension()
    return GenerationFrameCensus(
        family_count=len(frame),
        frame_resolves_identity=frame_resolves_identity(),
        idempotent_span_dimension=span,
        peirce_spectrum=tuple(sorted(spectrum.items())),
        generation_slot_dimension=slots,
        offdiagonal_dimension=offdiag,
        total_dimension=slots + offdiag,
        is_rank_three_frame=(len(frame) == 3 and span == 3 and slots == 3),
    )
