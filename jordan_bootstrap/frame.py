"""Gate O01: frame-function / Born selection with octonionic amplitudes.

The amplitude campaign's Gates Q11/Q12 proved that among the ``r``-norm rules only
``r = 2`` gives a measurement a total independent of the orthonormal frame chosen
to resolve it (Parseval). This gate reruns that exact selection with amplitudes
taken from the octonions ``O`` instead of ``Q(i)``.

A state is a vector ``s`` in ``O**d`` (each coordinate an exact octonion). An
orthonormal frame is an exact rational orthogonal matrix acting on the
coordinates; the ``r``-frame total is ``sum_i |(O s)_i|^r``. For even ``r`` the
weight ``|x|^r = (|x|^2)^{r/2}`` is an exact rational, so every total below is
decidable over the rationals.

Two facts make this a genuine octonionic statement rather than real Parseval in
disguise:

* **Sufficiency (Parseval).** For ``r = 2`` the total is ``sum_i |s_i|^2`` and is
  invariant under every rational orthogonal frame change, exactly, in every
  dimension -- the octonion norm is a positive-definite rational quadratic form.
* **Superposition is essential (the octonionic monomial control).** Multiplying
  every coordinate by a fixed *unit octonion* -- the octonionic echo of the
  monomial phases of ``Q(i)`` -- leaves the whole multiset of weights unchanged
  for *every* ``r`` (Hurwitz, Gate O00), so it can never expose ``r != 2``. Only a
  genuinely superposing rational rotation does, and it selects ``r = 2`` alone,
  reproducing the exact ``3027/625`` and ``5331/625`` witnesses of the complex
  Born-rule theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, Sequence, Tuple

from .octonion import E, ONE, Octonion, octonion

Matrix = Tuple[Tuple[Fraction, ...], ...]
State = Tuple[Octonion, ...]

_3 = Fraction(3, 5)
_4 = Fraction(4, 5)


def _identity(d: int) -> Matrix:
    return tuple(
        tuple(Fraction(1) if i == j else Fraction(0) for j in range(d))
        for i in range(d)
    )


def _pythagorean_split(d: int) -> Matrix:
    """Rotate the coordinates ``(1, 2)`` by the exact Pythagorean angle, fix the rest.

    This is the same complement rotation that powers the complex Born-rule
    theorem's necessity argument, embedded in dimension ``d >= 3``.
    """
    rows = [list(row) for row in _identity(d)]
    rows[1][1], rows[1][2] = _3, _4
    rows[2][1], rows[2][2] = -_4, _3
    return tuple(tuple(r) for r in rows)


def frames(d: int) -> Dict[str, Matrix]:
    """The two declared orthonormal frames for a ``d``-dimensional resolution."""
    return {"A": _identity(d), "B": _pythagorean_split(d)}


def is_orthogonal(matrix: Matrix) -> bool:
    """Exact check that ``matrix`` is orthogonal: rows orthonormal over the rationals."""
    d = len(matrix)
    for i in range(d):
        for j in range(d):
            dot = sum(
                (matrix[i][k] * matrix[j][k] for k in range(d)), Fraction(0)
            )
            if dot != (Fraction(1) if i == j else Fraction(0)):
                return False
    return True


def apply_frame(matrix: Matrix, state: State) -> State:
    """Resolve ``state`` in the frame ``matrix``: ``(O s)_i = sum_j O_ij s_j``."""
    d = len(matrix)
    out = []
    for i in range(d):
        acc = octonion(0, 0, 0, 0, 0, 0, 0, 0)
        for j in range(d):
            acc = acc + state[j].scaled(matrix[i][j])
        out.append(acc)
    return tuple(out)


def weight(x: Octonion, r: int) -> Fraction:
    """Exact effect weight ``|x|^r`` for even ``r`` (``(|x|^2)^{r/2}``)."""
    if r % 2 != 0:
        raise ValueError("exact rational weights require an even exponent r")
    return x.norm2() ** (r // 2)


def frame_total(matrix: Matrix, state: State, r: int) -> Fraction:
    """The ``r``-frame total ``sum_i |(O s)_i|^r`` as an exact rational."""
    return sum((weight(x, r) for x in apply_frame(matrix, state)), Fraction(0))


def unit_octonion_relabel(state: State, unit: Octonion) -> State:
    """Right-multiply every coordinate by a fixed unit octonion (octonionic monomial)."""
    return tuple(s * unit for s in state)


def census_states(d: int) -> Tuple[State, ...]:
    """A frozen family of octonionic states in ``O**d``."""
    def pad(*head: Octonion) -> State:
        tail = tuple(octonion(0, 0, 0, 0, 0, 0, 0, 0) for _ in range(d - len(head)))
        return tuple(head) + tail

    equal_real = pad(ONE, ONE, ONE)               # the (1,1,1) witness state
    equal_imag = pad(E[1], E[1], E[1])            # a genuinely octonionic witness
    mixed = pad(ONE + E[2], ONE + E[2], E[5])     # octonion entries, still witnesses in plane (1,2)
    orthogonal_units = pad(E[3], E[1], E[2])      # distinct units: no r>2 discrepancy
    generic = pad(octonion(1, 2, 3, 4, 5, 6, 7, 8), E[6], ONE)
    return (equal_real, equal_imag, mixed, orthogonal_units, generic)


@dataclass(frozen=True)
class FrameConsistencyCensus:
    """Exact tallies for Gate O01, owned and asserted by the test contract."""

    dimensions: Tuple[int, ...]
    total_states: int
    born_frame_checks: int
    born_frame_mismatches: int          # r = 2 must be invariant everywhere
    contextual_states_r4: int           # states where split A != split B at r = 4
    contextual_states_r6: int           # ditto at r = 6
    unit_relabel_checks: int
    unit_relabel_multiset_mismatches: int  # unit-octonion relabeling must not move any multiset


def _weight_multiset(state: State, r: int) -> Tuple[Fraction, ...]:
    return tuple(sorted(weight(s, r) for s in state))


def frame_consistency_census(
    dimensions: Sequence[int] = (3, 4),
    unit_relabels: Sequence[Octonion] | None = None,
) -> FrameConsistencyCensus:
    """Run the exact frame-consistency selection over the declared octonionic census."""
    if unit_relabels is None:
        unit_relabels = (E[1], E[2], E[4], -E[7])

    total_states = 0
    born_checks = 0
    born_mismatches = 0
    contextual_r4 = 0
    contextual_r6 = 0
    unit_checks = 0
    unit_mismatches = 0

    for d in dimensions:
        frame_map = frames(d)
        for state in census_states(d):
            total_states += 1

            # (1) r = 2 is invariant across every frame (Parseval / Born).
            base2 = frame_total(frame_map["A"], state, 2)
            for name, matrix in frame_map.items():
                born_checks += 1
                if frame_total(matrix, state, 2) != base2:
                    born_mismatches += 1

            # (2) r = 4 and r = 6 can disagree between the two frames (contextual).
            if frame_total(frame_map["A"], state, 4) != frame_total(
                frame_map["B"], state, 4
            ):
                contextual_r4 += 1
            if frame_total(frame_map["A"], state, 6) != frame_total(
                frame_map["B"], state, 6
            ):
                contextual_r6 += 1

            # (3) Octonionic monomial control: unit-octonion relabeling leaves the
            #     multiset of weights unchanged for every r -> never exposes r != 2.
            for unit in unit_relabels:
                relabelled = unit_octonion_relabel(state, unit)
                for r in (2, 4, 6):
                    unit_checks += 1
                    if _weight_multiset(relabelled, r) != _weight_multiset(state, r):
                        unit_mismatches += 1

    return FrameConsistencyCensus(
        dimensions=tuple(dimensions),
        total_states=total_states,
        born_frame_checks=born_checks,
        born_frame_mismatches=born_mismatches,
        contextual_states_r4=contextual_r4,
        contextual_states_r6=contextual_r6,
        unit_relabel_checks=unit_checks,
        unit_relabel_multiset_mismatches=unit_mismatches,
    )


def theorem_witnesses() -> Dict[str, Fraction]:
    """The exact ``(1,1,1)`` frame totals that tie O01 to the complex Born theorem."""
    d = 3
    frame_map = frames(d)
    state = (ONE, ONE, ONE)
    return {
        "r2_split_A": frame_total(frame_map["A"], state, 2),
        "r2_split_B": frame_total(frame_map["B"], state, 2),
        "r4_split_A": frame_total(frame_map["A"], state, 4),
        "r4_split_B": frame_total(frame_map["B"], state, 4),
        "r6_split_A": frame_total(frame_map["A"], state, 6),
        "r6_split_B": frame_total(frame_map["B"], state, 6),
    }
