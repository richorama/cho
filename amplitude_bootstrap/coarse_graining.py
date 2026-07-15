"""Exact amplitude coarse-graining: autonomous reduced dynamics under partial trace.

Gate Q01 asks the amplitude version of the classical coarse-graining question. A
two-qubit unitary ``U`` is the microscopic update. The coarse-graining ``B`` is the
partial trace over the second qubit, the canonical "throw away resolution" map. An
autonomous effective law exists when there is a fixed channel ``E`` on the first
qubit with

    Tr_B(U rho U^dagger) = E(Tr_B rho)   for every global state rho.

This is the density-matrix analogue of the classical ``B U = U_B B`` census, and it
is decided exactly over Q(i). When ``E`` exists we also classify it as reversible
(unitary, Choi rank one) or genuinely decohering (Choi rank at least two), an
irreversibility holdout that is never used for selection.
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, NamedTuple, Optional, Tuple

from .gaussian import ONE, ZERO, Gaussian
from .linalg import Matrix, dagger, identity, kron, matmul, rank, solve_columns

# --- Fixed two-qubit layout: qubit A is the coarse system, qubit B the environment.
_FINE = 4
_COARSE = 2


def _basis_operator(dimension: int, row: int, col: int) -> Matrix:
    return tuple(
        tuple(
            ONE if (r == row and c == col) else ZERO
            for c in range(dimension)
        )
        for r in range(dimension)
    )


def partial_trace_b(operator: Matrix) -> Matrix:
    """Trace out the second qubit of a two-qubit operator, index ``i = 2a + b``."""
    result = [[ZERO, ZERO], [ZERO, ZERO]]
    for a in range(_COARSE):
        for a_prime in range(_COARSE):
            total = ZERO
            for b in range(_COARSE):
                total = total + operator[2 * a + b][2 * a_prime + b]
            result[a][a_prime] = total
    return tuple(tuple(row) for row in result)


def partial_trace(operator: Matrix, traced: int) -> Matrix:
    """Trace out one qubit of a two-qubit operator.

    ``traced == 1`` removes the second factor (keep qubit A); ``traced == 0`` removes
    the first factor (keep qubit B). Fine index is ``i = 2 * a + b``.
    """
    result = [[ZERO, ZERO], [ZERO, ZERO]]
    for keep in range(_COARSE):
        for keep_prime in range(_COARSE):
            total = ZERO
            for gone in range(_COARSE):
                if traced == 1:
                    row, col = 2 * keep + gone, 2 * keep_prime + gone
                else:
                    row, col = 2 * gone + keep, 2 * gone + keep_prime
                total = total + operator[row][col]
            result[keep][keep_prime] = total
    return tuple(tuple(row) for row in result)


def _vec(operator: Matrix) -> Tuple[Gaussian, ...]:
    return tuple(value for row in operator for value in row)


def _superoperator(images: List[Matrix]) -> Matrix:
    """Assemble a coarse-by-fine matrix from the images of the fine basis operators."""
    columns = [_vec(image) for image in images]
    coarse_dim = len(columns[0])
    return tuple(
        tuple(columns[fine][coarse] for fine in range(len(columns)))
        for coarse in range(coarse_dim)
    )


def _fine_basis_images(transform) -> List[Matrix]:
    images = []
    for i in range(_FINE):
        for j in range(_FINE):
            images.append(transform(_basis_operator(_FINE, i, j)))
    return images


def reduced_channel(unitary: Matrix, traced: int = 1) -> Optional[Matrix]:
    """Return the autonomous coarse channel ``E`` as a 4x4 vec-matrix, or None.

    ``E`` acts on row-major vectorised 2x2 operators. It exists exactly when the
    reduced dynamics factors through the partial trace for every global operator.
    ``traced`` selects the coarse-graining: trace out qubit B (default) or A.
    """
    unitary_dagger = dagger(unitary)

    def trace(operator: Matrix) -> Matrix:
        return partial_trace(operator, traced)

    def evolve_then_trace(operator: Matrix) -> Matrix:
        return trace(matmul(matmul(unitary, operator), unitary_dagger))

    evolved = _superoperator(_fine_basis_images(evolve_then_trace))
    traced_super = _superoperator(_fine_basis_images(trace))

    # Solve E @ traced = evolved for the 4x4 channel matrix E, exactly.
    solution = solve_columns(_transpose(traced_super), _transpose(evolved))
    if solution is None:
        return None
    return _transpose(solution)


def _transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[r][c] for r in range(len(matrix)))
        for c in range(len(matrix[0]))
    )


def _apply_channel(channel: Matrix, operator: Matrix) -> Matrix:
    image = matmul(channel, tuple((value,) for value in _vec(operator)))
    flat = [row[0] for row in image]
    return ((flat[0], flat[1]), (flat[2], flat[3]))


def choi_rank(channel: Matrix) -> int:
    """Exact Choi-matrix rank; one iff the channel is a reversible unitary."""
    blocks = [[None] * _COARSE for _ in range(_COARSE)]
    for i in range(_COARSE):
        for j in range(_COARSE):
            blocks[i][j] = _apply_channel(channel, _basis_operator(_COARSE, i, j))
    choi = [[ZERO] * (_COARSE * _COARSE) for _ in range(_COARSE * _COARSE)]
    for i in range(_COARSE):
        for j in range(_COARSE):
            image = blocks[i][j]
            for p in range(_COARSE):
                for q in range(_COARSE):
                    choi[i * _COARSE + p][j * _COARSE + q] = image[p][q]
    return rank(tuple(tuple(row) for row in choi))


# --- The declared, finite, exactly-unitary two-qubit ensemble over Q(i). ------

def _g(real: int, imag: int = 0) -> Gaussian:
    return Gaussian(Fraction(real), Fraction(imag))


_I2: Matrix = ((ONE, ZERO), (ZERO, ONE))
_X: Matrix = ((ZERO, ONE), (ONE, ZERO))
_S: Matrix = ((ONE, ZERO), (ZERO, _g(0, 1)))
_Z: Matrix = ((ONE, ZERO), (ZERO, _g(-1)))
# Exact Pythagorean rotation: rational, genuinely superposing, unitary.
_R: Matrix = (
    (Gaussian(Fraction(3, 5)), Gaussian(Fraction(-4, 5))),
    (Gaussian(Fraction(4, 5)), Gaussian(Fraction(3, 5))),
)

ONE_QUBIT_GATES: Tuple[Matrix, ...] = (_I2, _X, _S, _Z, _R, matmul(_X, _R))

_CZ: Matrix = tuple(
    tuple(_g(-1) if (r == 3 and c == 3) else (ONE if r == c else ZERO) for c in range(4))
    for r in range(4)
)
# CNOT with qubit A as control: |a, b> -> |a, b xor a>.
_CNOT_PERM = (0, 1, 3, 2)
_CNOT: Matrix = tuple(
    tuple(ONE if c == _CNOT_PERM[r] else ZERO for c in range(4)) for r in range(4)
)
_SWAP_PERM = (0, 2, 1, 3)
_SWAP: Matrix = tuple(
    tuple(ONE if c == _SWAP_PERM[r] else ZERO for c in range(4)) for r in range(4)
)
_I4: Matrix = identity(4)

ENTANGLERS: Tuple[Tuple[str, Matrix], ...] = (
    ("local", _I4),
    ("cz", _CZ),
    ("cnot", _CNOT),
    ("swap", _SWAP),
)


def ensemble() -> List[Tuple[str, Matrix]]:
    """Every ``(local_a kron local_b) @ entangler`` unitary, with an entangler tag."""
    members = []
    for a in ONE_QUBIT_GATES:
        for b in ONE_QUBIT_GATES:
            local = kron(a, b)
            for tag, entangler in ENTANGLERS:
                members.append((tag, matmul(local, entangler)))
    return members


class ReducedCensus(NamedTuple):
    ensemble_size: int
    autonomous: int
    reversible: int
    decohering: int
    autonomous_local: int
    autonomous_entangling: int
    entangling_total: int


def reduced_dynamics_census(traced: int = 1) -> ReducedCensus:
    """Classify the ensemble by existence and reversibility of the coarse channel."""
    ensemble_size = 0
    autonomous = 0
    reversible = 0
    decohering = 0
    autonomous_local = 0
    autonomous_entangling = 0
    entangling_total = 0

    for tag, unitary in ensemble():
        ensemble_size += 1
        is_entangling = tag != "local"
        if is_entangling:
            entangling_total += 1
        channel = reduced_channel(unitary, traced)
        if channel is None:
            continue
        autonomous += 1
        if is_entangling:
            autonomous_entangling += 1
        else:
            autonomous_local += 1
        if choi_rank(channel) == 1:
            reversible += 1
        else:
            decohering += 1

    return ReducedCensus(
        ensemble_size=ensemble_size,
        autonomous=autonomous,
        reversible=reversible,
        decohering=decohering,
        autonomous_local=autonomous_local,
        autonomous_entangling=autonomous_entangling,
        entangling_total=entangling_total,
    )


# --- Gate Q02: fixed-environment coarse-graining and emergent decoherence. ----

def _density(entries: Tuple[Tuple[Gaussian, ...], ...]) -> Matrix:
    return tuple(tuple(row) for row in entries)


_HALF = Fraction(1, 2)

# Declared environment states, all exact density matrices over Q(i).
ENVIRONMENTS: Tuple[Tuple[str, Matrix], ...] = (
    ("zero", ((ONE, ZERO), (ZERO, ZERO))),
    ("one", ((ZERO, ZERO), (ZERO, ONE))),
    ("plus", ((Gaussian(_HALF), Gaussian(_HALF)), (Gaussian(_HALF), Gaussian(_HALF)))),
    (
        "plus_i",
        (
            (Gaussian(_HALF), Gaussian(Fraction(0), -_HALF)),
            (Gaussian(Fraction(0), _HALF), Gaussian(_HALF)),
        ),
    ),
    ("mixed", ((Gaussian(_HALF), ZERO), (ZERO, Gaussian(_HALF)))),
)


def fixed_environment_channel(
    unitary: Matrix, environment: Matrix, traced: int = 1
) -> Matrix:
    """The open-systems channel ``rho_S -> Tr_env(U (rho_S kron rho_env) U^dagger)``.

    ``traced`` selects the environment qubit: with ``traced == 1`` the system is
    qubit A and the environment is qubit B (default); with ``traced == 0`` the roles
    swap. Returns the 4x4 vec-matrix of an always-autonomous channel on the system.
    """
    unitary_dagger = dagger(unitary)
    images = []
    for i in range(_COARSE):
        for j in range(_COARSE):
            system = _basis_operator(_COARSE, i, j)
            if traced == 1:
                joint = kron(system, environment)
            else:
                joint = kron(environment, system)
            evolved = matmul(matmul(unitary, joint), unitary_dagger)
            images.append(partial_trace(evolved, traced))
    return _superoperator(images)


def channel_preserves_trace(channel: Matrix) -> bool:
    """Exact trace-preservation check for a qubit channel in vec form."""
    for i in range(_COARSE):
        for j in range(_COARSE):
            image = _apply_channel(channel, _basis_operator(_COARSE, i, j))
            trace = image[0][0] + image[1][1]
            expected = ONE if i == j else ZERO
            if trace != expected:
                return False
    return True


class DecoherenceRow(NamedTuple):
    environment: str
    reversible: int
    decohering: int
    decohering_entangling: int
    trace_preserving: int


def environment_decoherence_census(traced: int = 1) -> Tuple[DecoherenceRow, ...]:
    """Per-environment tally of reversible vs genuinely decohering channels."""
    members = ensemble()
    rows = []
    for name, environment in ENVIRONMENTS:
        reversible = 0
        decohering = 0
        decohering_entangling = 0
        trace_preserving = 0
        for tag, unitary in members:
            channel = fixed_environment_channel(unitary, environment, traced)
            if channel_preserves_trace(channel):
                trace_preserving += 1
            if choi_rank(channel) == 1:
                reversible += 1
            else:
                decohering += 1
                if tag != "local":
                    decohering_entangling += 1
        rows.append(
            DecoherenceRow(
                environment=name,
                reversible=reversible,
                decohering=decohering,
                decohering_entangling=decohering_entangling,
                trace_preserving=trace_preserving,
            )
        )
    return tuple(rows)


def local_channels_are_environment_independent(unitary_a: Matrix) -> bool:
    """A local ``a kron b`` channel equals ``a(.)a^dagger`` for every environment."""
    reference = None
    for _, environment in ENVIRONMENTS:
        channel = fixed_environment_channel(kron(unitary_a, _I2), environment)
        if reference is None:
            reference = channel
        elif channel != reference:
            return False
    return True
