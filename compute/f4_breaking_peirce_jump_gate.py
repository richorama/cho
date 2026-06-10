"""
F4-BREAKING PEIRCE-JUMP GATE -- the vacuum-damping jumps are the Peirce modes.
================================================================================

The CHO Lindbladian gate wrote down a concrete generator for the relaxation
channel, with jump operators

    L_k = sqrt(gamma) |p><e_k|     (amplitude damping into the vacuum ray p),

verified on a faithful two-level (qubit) representation. But the "directions
e_k orthogonal to the vacuum" and the choice "damp toward the vacuum ray p"
were written by hand on the qubit. This gate climbs underneath that structure
and shows the jump modes and their target are NOT free: they are the Peirce
decomposition of the exceptional Jordan algebra J3(O) relative to a PRIMITIVE
idempotent.

For an element P of J3(O) the Jordan left-multiplication L_P (X) = P o X is
self-adjoint for the trace form, and the Peirce theorem says that when P is an
idempotent (P o P = P) its spectrum is contained in {0, 1/2, 1}, splitting the
27-dimensional algebra into three trace-orthogonal eigenspaces

    J3(O) = J_1(P)  (+)  J_{1/2}(P)  (+)  J_0(P) .

For a PRIMITIVE (rank-one) idempotent the multiplicities are

    dim J_1 = 1        the vacuum ray  span(P)
    dim J_{1/2} = 16   the coherence / transition modes  ( = dim OP^2 = Delta_9 )
    dim J_0 = 10       the orthogonal population modes  ( the J2(O) block )

with 1 + 16 + 10 = 27. The trace-orthogonal complement of the vacuum ray is
exactly J_{1/2}(P) (+) J_0(P) -- the 26 off-vacuum modes -- so the abstract
"e_k orthogonal to p" of the Lindbladian jump operators are concretely these
Peirce modes: 16 coherences plus 10 populations. The depolarizing-toward-vacuum
channel on J3(O),

    R_r(X) = (1 - r) X + r tr(X) P ,

(the Jordan-algebra image of the Lindbladian C_r) has eigenvalue 1 on the vacuum
ray and (1 - r) on all 26 off-vacuum modes, a UNIQUE steady ray span(P), and a
composing semigroup r(t) = 1 - exp(-gamma t) -- reproducing the Lindbladian's
unique vacuum steady state at the full-Jordan level.

What this proves
----------------
The jump-operator STRUCTURE of the CHO Lindbladian -- amplitude damping of the
orthogonal modes into a unique vacuum ray -- is forced by the Peirce
decomposition of J3(O) at a primitive idempotent. The off-vacuum directions are
canonically the 16-dimensional coherence space J_{1/2}(P) (= dim OP^2) and the
10-dimensional population space J_0(P); the unique vacuum ray is span(P). Only a
PRIMITIVE idempotent gives a one-dimensional vacuum ray: a rank-two idempotent
leaves a 10-dimensional J_1 (no single ray), the identity has no off-vacuum
modes at all, and a non-idempotent target has L-spectrum outside {0,1/2,1} so no
Peirce structure exists. The Peirce projectors are exact (rational structure
constants), idempotent and trace-orthogonal to machine zero.

What this still does not prove
------------------------------
This does not derive the relaxation rate gamma (the timescale) from a CHO action,
and -- crucially -- it does not derive WHY the dynamics selects a PRIMITIVE
idempotent (rather than a rank-two or rank-three idempotent) as the vacuum; that
vacuum selection is the F4-breaking step and stays open. It does not derive the
source overlap d = pi/432. It reduces "why these vacuum-damping jump operators"
to "why a primitive-idempotent vacuum", conditional on the OP^2/Jordan geometry.

No Bayes credit moves.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/f4_breaking_peirce_jump_gate.py
"""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

from epsilon_weyl_isomorphism import jordan_product_tensor
from epsilon_orbit_selection import (
    DIM_DELTA9,
    DIM_J3O,
    DIM_ARENA,
    freudenthal_sharp,
    primitive_idempotents,
)
from f4_breaking_seed_op2 import EPS0_SQ
from f4_breaking_cho_lindbladian_gate import GAMMA


TOL = 1e-9
EXACT_TOL = 1e-11
SPECTRUM_TOL = 1e-7
RANK_TOL = 1e-7
SEMIGROUP_TOL = 1e-12


# --------------------------------------------------------------------------- #
#  J3(O) machinery (convention: epsilon_weyl_isomorphism.jordan_product_tensor) #
#  A J3(O) element is a 27-vector; diagonal reals at indices 0,1,2; identity   #
#  is e0+e1+e2; (X o Y)_k = sum_ij T[k,i,j] X_i Y_j.                            #
# --------------------------------------------------------------------------- #
_T = jordan_product_tensor()
_IDENTITY = np.eye(DIM_J3O)
_TRACE_COVECTOR = np.zeros(DIM_J3O)
_TRACE_COVECTOR[0] = _TRACE_COVECTOR[1] = _TRACE_COVECTOR[2] = 1.0


def _diag(a, b, c):
    v = np.zeros(DIM_J3O)
    v[0], v[1], v[2] = a, b, c
    return v


def jordan_product(x, y):
    return np.einsum("kij,i,j->k", _T, x, y)


def left_multiplication(x):
    """L_X with (L_X)_{k,j} = sum_i T[k,i,j] X_i, so L_X @ Y = X o Y."""
    return np.einsum("kij,i->kj", _T, x)


def trace(x):
    return float(x[0] + x[1] + x[2])


def trace_form_gram():
    """G_{ij} = tr(e_i o e_j) = T[0,i,j] + T[1,i,j] + T[2,i,j], the trace form."""
    return _T[0] + _T[1] + _T[2]


def idempotency_residual(x):
    """|X o X - X|: zero iff X is a Jordan idempotent."""
    return float(np.max(np.abs(jordan_product(x, x) - x)))


def peirce_minimal_residual(left):
    """|L (L - 1/2) (L - 1)|: zero iff L's spectrum is in {0, 1/2, 1}
    (the Peirce theorem for an idempotent), independent of multiplicities."""
    half = 0.5 * _IDENTITY
    return float(np.max(np.abs(left @ (left - half) @ (left - _IDENTITY))))


def peirce_projectors(left):
    """Exact Lagrange-interpolation spectral projectors of L_P for eigenvalues
    {1, 1/2, 0}.  E1 = 2L^2 - L, Eh = 4L - 4L^2, E0 = 2L^2 - 3L + I.  These are
    genuine idempotents summing to I only when L's spectrum is {0, 1/2, 1}."""
    lsq = left @ left
    e1 = 2.0 * lsq - left
    eh = 4.0 * left - 4.0 * lsq
    e0 = 2.0 * lsq - 3.0 * left + _IDENTITY
    return e1, eh, e0


# --------------------------------------------------------------------------- #
#  Rows                                                                         #
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class PeirceRow:
    label: str
    idempotency_residual: float
    peirce_residual: float
    is_idempotent: bool
    dim_j1: int
    dim_jhalf: int
    dim_j0: int
    projector_error: float
    vacuum_is_single_ray: bool
    vacuum_equals_span: bool
    coherence_matches_op2: bool
    sharp_norm: float


@dataclass(frozen=True)
class RelaxationRow:
    time: float
    relaxation_fraction: float
    offvacuum_decay: float
    steady_ray_error: float
    fixes_vacuum_error: float
    offvacuum_mode_count: int


@dataclass(frozen=True)
class PeirceControlRow:
    label: str
    is_idempotent: bool
    dim_j1: int
    vacuum_is_single_ray: bool
    interpretation: str


@dataclass(frozen=True)
class PeirceJumpSelection:
    primitive_dim_j1: int
    primitive_dim_jhalf: int
    primitive_dim_j0: int
    peirce_dim_sum: int
    coherence_op2_dim: int
    arena_dim: int
    offvacuum_mode_count: int
    relaxation_unique_vacuum: bool
    semigroup_error: float
    sharp_norm_vacuum: float
    jump_modes_are_peirce_decomposition: bool
    unique_vacuum_needs_primitive_idempotent: bool
    coherence_dim_matches_op2: bool
    relaxation_rate_derived_from_cho: bool
    vacuum_primitivity_derived_from_cho: bool
    source_overlap_derived_from_cho: bool


# --------------------------------------------------------------------------- #
#  Peirce decomposition of a candidate vacuum idempotent                        #
# --------------------------------------------------------------------------- #
def peirce_decomposition(label, x):
    """Build the Peirce row for a candidate vacuum element x of J3(O)."""
    left = left_multiplication(x)
    idem_res = idempotency_residual(x)
    peirce_res = peirce_minimal_residual(left)
    is_idem = idem_res < TOL and peirce_res < TOL

    e1, eh, e0 = peirce_projectors(left)
    proj_error = max(
        float(np.max(np.abs(e1 @ e1 - e1))),
        float(np.max(np.abs(eh @ eh - eh))),
        float(np.max(np.abs(e0 @ e0 - e0))),
        float(np.max(np.abs(e1 + eh + e0 - _IDENTITY))),
        float(np.max(np.abs(e1 @ eh))),
        float(np.max(np.abs(e1 @ e0))),
        float(np.max(np.abs(eh @ e0))),
    )
    dim_j1 = int(np.linalg.matrix_rank(e1, tol=RANK_TOL))
    dim_jhalf = int(np.linalg.matrix_rank(eh, tol=RANK_TOL))
    dim_j0 = int(np.linalg.matrix_rank(e0, tol=RANK_TOL))

    vacuum_single = is_idem and dim_j1 == 1
    # vacuum ray equals span(x): E1 fixes x and projects rank one
    vacuum_equals_span = bool(np.max(np.abs(e1 @ x - x)) < TOL and dim_j1 == 1)
    coherence_op2 = is_idem and dim_jhalf == DIM_DELTA9
    sharp_norm = float(np.linalg.norm(freudenthal_sharp(x)))

    return PeirceRow(
        label=label,
        idempotency_residual=idem_res,
        peirce_residual=peirce_res,
        is_idempotent=is_idem,
        dim_j1=dim_j1,
        dim_jhalf=dim_jhalf,
        dim_j0=dim_j0,
        projector_error=proj_error,
        vacuum_is_single_ray=vacuum_single,
        vacuum_equals_span=vacuum_equals_span,
        coherence_matches_op2=coherence_op2,
        sharp_norm=sharp_norm,
    )


def vacuum_complement_is_peirce(primitive):
    """Verify the trace-orthogonal complement of the vacuum ray span(P) equals
    J_{1/2}(P) (+) J_0(P): max |<P, off-vacuum basis>| over the trace form."""
    left = left_multiplication(primitive)
    _e1, eh, e0 = peirce_projectors(left)
    gram = trace_form_gram()
    off = np.hstack([eh, e0])
    return float(np.max(np.abs(primitive @ gram @ off)))


# --------------------------------------------------------------------------- #
#  Depolarizing-toward-vacuum relaxation channel on J3(O)                        #
# --------------------------------------------------------------------------- #
def relaxation_channel(primitive, r):
    """R_r(X) = (1 - r) X + r tr(X) P -- the Jordan image of the Lindbladian
    depolarizing channel C_r, acting on the real 27."""
    return (1.0 - r) * _IDENTITY + r * np.outer(primitive, _TRACE_COVECTOR)


def relaxation_rows(primitive, gamma, times):
    """For each elapsed time t the propagator R_{r(t)} with r(t)=1-exp(-gamma t):
    its off-vacuum modes decay by (1-r), it fixes the vacuum, and it relaxes a
    generic trace-one state toward tr(X) P = P."""
    rng = np.random.default_rng(0)
    probe = primitive + 0.7 * rng.standard_normal(DIM_J3O)
    probe = probe / trace(probe)  # trace-one probe
    rows = []
    for t in times:
        r = 1.0 - math.exp(-gamma * t)
        channel = relaxation_channel(primitive, r)
        relaxed = channel @ probe
        steady_err = float(np.max(np.abs(relaxed - trace(probe) * primitive)))
        fixes_err = float(np.max(np.abs(channel @ primitive - primitive)))
        eigvals = np.sort(np.linalg.eigvals(channel).real)
        offcount = int(np.sum(np.abs(eigvals - (1.0 - r)) < SPECTRUM_TOL))
        rows.append(
            RelaxationRow(
                time=t,
                relaxation_fraction=r,
                offvacuum_decay=1.0 - r,
                steady_ray_error=steady_err,
                fixes_vacuum_error=fixes_err,
                offvacuum_mode_count=offcount,
            )
        )
    return rows


def semigroup_residual(primitive, gamma, s, t):
    """|R_{r(s)} R_{r(t)} - R_{r(s+t)}|: the channel is a one-parameter semigroup
    with r(t)=1-exp(-gamma t)."""
    rs = 1.0 - math.exp(-gamma * s)
    rt = 1.0 - math.exp(-gamma * t)
    rst = 1.0 - math.exp(-gamma * (s + t))
    composed = relaxation_channel(primitive, rs) @ relaxation_channel(primitive, rt)
    direct = relaxation_channel(primitive, rst)
    return float(np.max(np.abs(composed - direct)))


# --------------------------------------------------------------------------- #
#  Controls: only a PRIMITIVE idempotent gives a single vacuum ray              #
# --------------------------------------------------------------------------- #
def peirce_control_rows():
    controls = [
        (
            "rank-2 idempotent diag(1,1,0)",
            _diag(1, 1, 0),
            "rank-two idempotent: J1 is the 10-dim J2(O) block, not a single vacuum ray",
        ),
        (
            "identity diag(1,1,1)",
            _diag(1, 1, 1),
            "rank-three identity: L_I=I, J1 is all of J3(O), no off-vacuum modes to damp",
        ),
        (
            "non-idempotent diag(2,0,0)",
            _diag(2, 0, 0),
            "non-idempotent: L spectrum {0,1,2} not {0,1/2,1}, no Peirce structure",
        ),
        (
            "rank-1 non-idempotent diag(1/2,0,0)",
            _diag(0.5, 0.0, 0.0),
            "rank-one but not idempotent: L spectrum {0,1/4,1/2}, idempotency P o P = P required",
        ),
    ]
    rows = []
    for label, x, interp in controls:
        row = peirce_decomposition(label, x)
        rows.append(
            PeirceControlRow(
                label=label,
                is_idempotent=row.is_idempotent,
                dim_j1=row.dim_j1,
                vacuum_is_single_ray=row.vacuum_is_single_ray,
                interpretation=interp,
            )
        )
    return rows


# --------------------------------------------------------------------------- #
#  Selection                                                                    #
# --------------------------------------------------------------------------- #
def peirce_jump_selection():
    primitive = primitive_idempotents()[0]
    row = peirce_decomposition("primitive E1 = diag(1,0,0)", primitive)
    semigroup_err = semigroup_residual(primitive, GAMMA, 0.4, 0.9)
    rows = relaxation_rows(primitive, GAMMA, (25.0,))
    unique_vacuum = bool(rows[0].steady_ray_error < TOL and row.vacuum_is_single_ray)

    return PeirceJumpSelection(
        primitive_dim_j1=row.dim_j1,
        primitive_dim_jhalf=row.dim_jhalf,
        primitive_dim_j0=row.dim_j0,
        peirce_dim_sum=row.dim_j1 + row.dim_jhalf + row.dim_j0,
        coherence_op2_dim=DIM_DELTA9,
        arena_dim=DIM_ARENA,
        offvacuum_mode_count=row.dim_jhalf + row.dim_j0,
        relaxation_unique_vacuum=unique_vacuum,
        semigroup_error=semigroup_err,
        sharp_norm_vacuum=row.sharp_norm,
        jump_modes_are_peirce_decomposition=bool(
            row.vacuum_equals_span and row.coherence_matches_op2
        ),
        unique_vacuum_needs_primitive_idempotent=True,
        coherence_dim_matches_op2=row.coherence_matches_op2,
        relaxation_rate_derived_from_cho=False,
        vacuum_primitivity_derived_from_cho=False,
        source_overlap_derived_from_cho=False,
    )


# --------------------------------------------------------------------------- #
#  Driver                                                                       #
# --------------------------------------------------------------------------- #
def main() -> bool:
    primitive = primitive_idempotents()[0]
    row = peirce_decomposition("primitive E1 = diag(1,0,0)", primitive)
    complement_err = vacuum_complement_is_peirce(primitive)
    relax = relaxation_rows(primitive, GAMMA, (0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 25.0))
    semigroup_err = semigroup_residual(primitive, GAMMA, 0.4, 0.9)
    controls = peirce_control_rows()
    selection = peirce_jump_selection()

    print("=" * 78)
    print("  F4-BREAKING PEIRCE-JUMP GATE")
    print("  Are the Lindbladian vacuum-damping jumps the Peirce modes of J3(O)?")
    print("=" * 78)

    print("\n[A] Peirce decomposition of J3(O) at the primitive idempotent P")
    print(f"  idempotency residual |P o P - P|          : {row.idempotency_residual:.2e}")
    print(f"  Peirce residual |L(L-1/2)(L-1)|           : {row.peirce_residual:.2e}")
    print(f"  projector idempotent/orthogonal/sum error : {row.projector_error:.2e}")
    print(f"  dim J_1(P)  (vacuum ray)                  : {row.dim_j1}")
    print(f"  dim J_1/2(P) (coherence modes)            : {row.dim_jhalf}")
    print(f"  dim J_0(P)  (population modes)            : {row.dim_j0}")
    print(f"  sum of Peirce dimensions                 : {row.dim_j1 + row.dim_jhalf + row.dim_j0} (= dim J3(O) = {DIM_J3O})")
    print(f"  |P#| Freudenthal sharp (rank-one test)    : {row.sharp_norm:.2e} (rank one)")

    print("\n[B] The off-vacuum jump modes are the Peirce complement")
    print(f"  vacuum ray equals span(P)                 : {row.vacuum_equals_span}")
    print(f"  coherence dim = dim OP^2 = Delta_9        : {row.dim_jhalf} == {DIM_DELTA9}  ({row.coherence_matches_op2})")
    print(f"  off-vacuum modes  16 + 10                 : {row.dim_jhalf + row.dim_j0}")
    print(f"  trace-orthogonal <P, J_1/2 (+) J_0>       : {complement_err:.2e} (vacuum complement = Peirce off-modes)")
    print(f"  arena dim Delta_9 x J3(O) = 16 x 27       : {DIM_ARENA} (denominator of eps0^2 = pi/432 = {EPS0_SQ:.6f})")

    print("\n[C] Depolarizing-toward-vacuum channel R_r(X)=(1-r)X + r tr(X) P")
    for r in relax:
        print(
            f"  t={r.time:<5} r={r.relaxation_fraction:.12f} decay={r.offvacuum_decay:.12f} "
            f"off-modes={r.offvacuum_mode_count} fix_vac={r.fixes_vacuum_error:.1e} "
            f"steady|R X - tr(X)P|={r.steady_ray_error:.2e}"
        )
    print(f"  semigroup |R_r(s) R_r(t) - R_r(s+t)|      : {semigroup_err:.2e}")
    print("  unique steady ray span(P); 26 off-vacuum modes decay; gap -> memoryless.")

    print("\n[D] Controls (only a PRIMITIVE idempotent gives a single vacuum ray)")
    print(
        f"  {'primitive E1 = diag(1,0,0)':<34} idemp={row.is_idempotent} "
        f"dim_J1={row.dim_j1} single_ray={row.vacuum_is_single_ray}"
    )
    print("      the rank-one vacuum ray + 16 coherence + 10 population: amplitude damping into P")
    for c in controls:
        print(
            f"  {c.label:<34} idemp={c.is_idempotent} dim_J1={c.dim_j1} "
            f"single_ray={c.vacuum_is_single_ray}"
        )
        print(f"      {c.interpretation}")

    print("\n[V] Verdict")
    print("  jump modes = Peirce J_1/2 (+) J_0 of J3(O)  : YES")
    print("  vacuum ray = span(P), single primitive ray  : YES")
    print("  coherence dim = dim OP^2 = 16               : YES")
    print("  relaxation channel = Lindbladian C_r on J(O) : YES")
    print("  rate gamma from CHO action                  : NO")
    print("  primitive-idempotent vacuum from CHO action  : NO")
    print("  source overlap d = pi/432 from CHO action    : NO")
    print("  Bayes/scoreboard credit moved               : NO")
    print("=" * 78)

    # [A] exact Peirce decomposition at the primitive idempotent
    assert row.is_idempotent
    assert row.idempotency_residual < EXACT_TOL
    assert row.peirce_residual < EXACT_TOL
    assert row.projector_error < EXACT_TOL
    assert row.dim_j1 == 1
    assert row.dim_jhalf == DIM_DELTA9 == 16
    assert row.dim_j0 == 10
    assert row.dim_j1 + row.dim_jhalf + row.dim_j0 == DIM_J3O == 27
    assert row.sharp_norm < TOL  # primitive idempotent is rank one

    # [B] off-vacuum modes are the trace-orthogonal Peirce complement
    assert row.vacuum_equals_span
    assert row.coherence_matches_op2
    assert complement_err < EXACT_TOL
    assert DIM_ARENA == DIM_DELTA9 * DIM_J3O == 432

    # [C] relaxation channel: unique vacuum ray, 26 off-modes decay, semigroup
    for r in relax:
        assert r.fixes_vacuum_error < EXACT_TOL
        assert r.offvacuum_mode_count == row.dim_jhalf + row.dim_j0 == 26
        assert abs(r.offvacuum_decay - (1.0 - r.relaxation_fraction)) < TOL
    steady = [r.steady_ray_error for r in relax]
    assert all(steady[i] > steady[i + 1] for i in range(len(steady) - 1))
    # relaxation is exactly exponential: steady error = off-vacuum decay x const
    constants = [r.steady_ray_error / r.offvacuum_decay for r in relax]
    assert max(constants) - min(constants) < TOL
    assert steady[-1] < TOL  # large t reaches the vacuum ray
    assert semigroup_err < SEMIGROUP_TOL

    # [D] only the primitive idempotent is a single-ray vacuum; controls miss
    single_ray = [c for c in controls if c.vacuum_is_single_ray]
    assert len(single_ray) == 0
    rank2 = [c for c in controls if "rank-2" in c.label][0]
    assert rank2.is_idempotent and rank2.dim_j1 == 10
    identity = [c for c in controls if "identity" in c.label][0]
    assert identity.dim_j1 == DIM_J3O
    nonidem = [c for c in controls if "non-idempotent diag(2,0,0)" in c.label][0]
    assert not nonidem.is_idempotent
    rank1_nonidem = [c for c in controls if "rank-1 non-idempotent" in c.label][0]
    assert not rank1_nonidem.is_idempotent

    # honesty flags
    assert selection.relaxation_unique_vacuum
    assert selection.jump_modes_are_peirce_decomposition
    assert selection.coherence_dim_matches_op2
    assert selection.peirce_dim_sum == 27
    assert not selection.relaxation_rate_derived_from_cho
    assert not selection.vacuum_primitivity_derived_from_cho
    assert not selection.source_overlap_derived_from_cho
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
