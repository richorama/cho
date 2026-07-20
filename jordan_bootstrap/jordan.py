"""Gate O02: Born selection on the exceptional Jordan algebra h_3(O).

Gate O01 selected the norm rule for octonion *coordinate vectors*. This gate
moves to the honest home of octonionic quantum states: the exceptional Jordan
algebra ``J = h_3(O)`` of 3x3 Hermitian octonionic matrices under the Jordan
product ``A o B = (AB + BA)/2``. Its rank-one primitive idempotents (``P o P = P``,
``tr P = 1``) are the pure states -- the octonionic projective plane ``OP^2`` -- and
a *Jordan frame* is a resolution of the identity into three orthogonal primitive
idempotents. The Born rule is the trace form ``prob(P, Q) = tr(P o Q)``.

Everything is exact over the rationals. Two results are genuinely Jordan-algebraic
rather than inherited from O01:

* **Gleason on h_3(O).** For any state ``P`` the trace-form frame total
  ``sum_i tr(P o Q_i)`` equals ``tr(P)`` for *every* Jordan frame ``{Q_i}``, because
  the frame resolves the identity -- the exact octonionic analogue of Parseval,
  giving a frame-independent Born total.
* **Non-associativity obstructs statehood.** A rational unit vector whose three
  octonion entries do *not* lie in a common associative (quaternionic) subalgebra
  gives an outer product that is Hermitian and unit-trace yet is *not* idempotent,
  so it is not a point of ``OP^2``. Not every octonionic ray is a state -- the first
  honest wall the octonions raise.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Sequence, Tuple

from .octonion import Octonion, octonion
from .frame import frames, weight

JMat = Tuple[Tuple[Octonion, ...], ...]
Vector = Tuple[Octonion, ...]

_ZERO_O = octonion(0, 0, 0, 0, 0, 0, 0, 0)


def _real(x) -> Octonion:
    """A real octonion carrying the rational scalar ``x`` in its e_0 slot."""
    return octonion(x, 0, 0, 0, 0, 0, 0, 0)


_ONE_O = _real(1)


def _zeros() -> JMat:
    return tuple(tuple(_ZERO_O for _ in range(3)) for _ in range(3))


def _matmul(a: JMat, b: JMat) -> JMat:
    return tuple(
        tuple(
            sum((a[i][k] * b[k][j] for k in range(3)), _ZERO_O) for j in range(3)
        )
        for i in range(3)
    )


def _add(a: JMat, b: JMat) -> JMat:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(3)) for i in range(3))


def _scale(a: JMat, factor: Fraction) -> JMat:
    return tuple(tuple(a[i][j].scaled(factor) for j in range(3)) for i in range(3))


def jordan_product(a: JMat, b: JMat) -> JMat:
    """The Jordan product ``(AB + BA)/2`` of two 3x3 octonionic matrices."""
    return _scale(_add(_matmul(a, b), _matmul(b, a)), Fraction(1, 2))


def equal(a: JMat, b: JMat) -> bool:
    return all(a[i][j].coords == b[i][j].coords for i in range(3) for j in range(3))


def trace(a: JMat) -> Octonion:
    """Trace ``sum_i A_ii`` (a real octonion for Hermitian ``A``)."""
    return sum((a[i][i] for i in range(3)), _ZERO_O)


def is_hermitian(a: JMat) -> bool:
    return all(
        a[i][j].coords == a[j][i].conjugate().coords
        for i in range(3)
        for j in range(3)
    )


def outer(v: Vector) -> JMat:
    """The rank-one Hermitian matrix ``P_ij = v_i conj(v_j)``."""
    return tuple(tuple(v[i] * v[j].conjugate() for j in range(3)) for i in range(3))


def is_primitive_idempotent(p: JMat) -> bool:
    """Exact test ``P o P == P`` and ``tr P == 1`` (a pure state / point of OP^2)."""
    return equal(jordan_product(p, p), p) and trace(p).coords == _ONE_O.coords


def identity_matrix() -> JMat:
    rows = []
    for i in range(3):
        rows.append(tuple(_ONE_O if i == j else _ZERO_O for j in range(3)))
    return tuple(rows)


def frame_from_orthogonal(matrix) -> Tuple[JMat, ...]:
    """Turn a rational orthogonal 3x3 matrix into a Jordan frame of idempotents.

    Row ``i`` is a real unit vector ``q_i`` in ``O^3``; ``Q_i = outer(q_i)`` is a
    primitive idempotent and the three of them resolve the identity.
    """
    frame = []
    for i in range(3):
        q = tuple(_real(matrix[i][j]) for j in range(3))
        frame.append(outer(q))
    return tuple(frame)


def is_jordan_frame(frame: Sequence[JMat]) -> bool:
    """Exact check: each idempotent, pairwise Jordan-orthogonal, summing to identity."""
    for p in frame:
        if not is_primitive_idempotent(p):
            return False
    for i in range(len(frame)):
        for j in range(i + 1, len(frame)):
            if not equal(jordan_product(frame[i], frame[j]), _zeros()):
                return False
    total = _zeros()
    for p in frame:
        total = _add(total, p)
    return equal(total, identity_matrix())


def trace_form(a: JMat, b: JMat) -> Octonion:
    """The Born trace form ``tr(A o B)``."""
    return trace(jordan_product(a, b))


# --- state census -----------------------------------------------------------

def _associative_states() -> Tuple[JMat, ...]:
    """Genuine pure states: outer products of quaternionic rational unit vectors."""
    from .octonion import E

    vs = [
        (_ONE_O, _ZERO_O, _ZERO_O),
        (_real(Fraction(3, 5)), _real(Fraction(4, 5)), _ZERO_O),
        (E[1].scaled(Fraction(3, 5)), _ZERO_O, E[2].scaled(Fraction(4, 5))),
        (
            _real(Fraction(2, 3)),
            E[1].scaled(Fraction(2, 3)),
            E[2].scaled(Fraction(1, 3)),
        ),  # entries in span{1,e1,e2,e3} = a quaternion subalgebra
    ]
    return tuple(outer(v) for v in vs)


def _nonassociative_vectors() -> Tuple[Vector, ...]:
    """Unit vectors whose entries span a non-associative octonion triple."""
    from .octonion import E

    return (
        (E[1].scaled(Fraction(2, 3)), E[2].scaled(Fraction(2, 3)), E[4].scaled(Fraction(1, 3))),
        (E[3].scaled(Fraction(2, 3)), E[4].scaled(Fraction(2, 3)), E[6].scaled(Fraction(1, 3))),
        (E[2].scaled(Fraction(2, 7)), E[3].scaled(Fraction(3, 7)), E[5].scaled(Fraction(6, 7))),
    )


@dataclass(frozen=True)
class JordanStateCensus:
    idempotents_verified: int
    idempotents_declared: int
    nonassociative_declared: int
    nonassociative_hermitian_unit_trace: int
    nonassociative_idempotent_failures: int
    frame_count: int
    frames_are_resolutions_of_identity: int
    trace_form_frame_checks: int
    trace_form_frame_mismatches: int
    contextual_states_r4: int


def jordan_state_census() -> JordanStateCensus:
    """Exact tallies for Gate O02, owned and asserted by the test contract."""
    states = _associative_states()
    idem_ok = sum(1 for p in states if is_primitive_idempotent(p))

    nonassoc = _nonassociative_vectors()
    herm_unit = 0
    idem_fail = 0
    for v in nonassoc:
        p = outer(v)
        if is_hermitian(p) and trace(p).coords == _ONE_O.coords:
            herm_unit += 1
        if not is_primitive_idempotent(p):
            idem_fail += 1

    frame_matrices = frames(3)
    built = [frame_from_orthogonal(frame_matrices[name]) for name in ("A", "B")]
    resolutions = sum(1 for f in built if is_jordan_frame(f))

    # Gleason on h_3(O): the trace-form frame total equals tr(P), every frame.
    checks = 0
    mismatches = 0
    for p in states:
        tr_p = trace(p)
        for f in built:
            checks += 1
            total = _ZERO_O
            for q in f:
                total = total + trace_form(p, q)
            if total.coords != tr_p.coords:
                mismatches += 1

    # Necessity tie-in: an r=4 analog on the (1,1,1) superposition state is
    # contextual (the frame total stops equalling tr P), reproducing O01.
    from .octonion import ONE

    contextual = 0
    super_state = (ONE, ONE, ONE)
    for f_name in ("A", "B"):
        matrix = frame_matrices[f_name]
        rows = [tuple(_real(matrix[i][j]) for j in range(3)) for i in range(3)]
        total_r4 = sum(
            (
                weight(
                    sum((r[k].conjugate() * super_state[k] for k in range(3)), _ZERO_O),
                    4,
                )
                for r in rows
            ),
            Fraction(0),
        )
        if total_r4 != Fraction(3):
            contextual += 1

    return JordanStateCensus(
        idempotents_verified=idem_ok,
        idempotents_declared=len(states),
        nonassociative_declared=len(nonassoc),
        nonassociative_hermitian_unit_trace=herm_unit,
        nonassociative_idempotent_failures=idem_fail,
        frame_count=len(built),
        frames_are_resolutions_of_identity=resolutions,
        trace_form_frame_checks=checks,
        trace_form_frame_mismatches=mismatches,
        contextual_states_r4=contextual,
    )
