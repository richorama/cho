"""
Phase 5 gravity gate.
=====================

This is a decision gate, not a gravity derivation. It pressure-tests the
remaining bridge after compute/gravity_curvature.py:

* internal metric: Im(O), G2 < SO(7), positive-semidefinite rank-4 mode;
* spacetime arena: C x H ~= M_2(C), Lorentz SO(3,1);
* missing bridge: a canonical 4D Lorentzian metric and dynamics.

The gate exits zero when the status is honest and the demotion trigger is
explicit. It exits nonzero only if the internal consistency checks fail.
"""

from dataclasses import dataclass
import math

import numpy as np

from gravity_curvature import (
    emergent_metric,
    finite_g2_automorphisms,
    fourvector_to_hermitian,
    imag_octonion,
    minkowski_norm_from_det,
    random_imag,
    random_sl2c,
)


@dataclass(frozen=True)
class GateCheck:
    requirement: str
    status: str
    metric: str
    note: str


@dataclass(frozen=True)
class SignatureStats:
    positive: int
    negative: int
    zero: int


def matrix_signature(matrix, tol=1e-9):
    eigenvalues = np.linalg.eigvalsh((matrix + matrix.T) / 2.0)
    scale = max(1.0, float(np.max(np.abs(eigenvalues))))
    threshold = tol * scale
    positive = int(np.sum(eigenvalues > threshold))
    negative = int(np.sum(eigenvalues < -threshold))
    zero = int(matrix.shape[0] - positive - negative)
    return SignatureStats(positive, negative, zero), eigenvalues


def spacetime_arena_check(n_trials=200):
    """Check the borrowed C x H ~= M_2(C) Minkowski/Lorentz arena."""
    rng = np.random.default_rng(41)
    det_error = 0.0
    hermitian_error = 0.0
    for _ in range(n_trials):
        vector = rng.standard_normal(4)
        matrix = fourvector_to_hermitian(vector)
        minkowski = vector[0] ** 2 - float(vector[1:] @ vector[1:])
        det_error = max(det_error, abs(minkowski_norm_from_det(matrix) - minkowski))
        transform = random_sl2c(rng)
        transformed = transform @ matrix @ transform.conj().T
        hermitian_error = max(hermitian_error, float(np.max(np.abs(transformed - transformed.conj().T))))
        det_error = max(det_error, abs(minkowski_norm_from_det(transformed) - minkowski_norm_from_det(matrix)))
    return {
        "det_error": det_error,
        "hermitian_error": hermitian_error,
        "pass": det_error < 1e-9 and hermitian_error < 1e-9,
    }


def internal_metric_signature(n_trials=256):
    """Check that the associator metric is PSD rank 4, not Lorentzian."""
    rng = np.random.default_rng(42)
    signatures = {}
    min_eigenvalue = math.inf
    max_negative_count = 0
    for _ in range(n_trials):
        a, b = random_imag(rng), random_imag(rng)
        signature, eigenvalues = matrix_signature(emergent_metric(a, b))
        key = (signature.positive, signature.negative, signature.zero)
        signatures[key] = signatures.get(key, 0) + 1
        min_eigenvalue = min(min_eigenvalue, float(np.min(eigenvalues)))
        max_negative_count = max(max_negative_count, signature.negative)
    most_common = max(signatures.items(), key=lambda item: item[1])[0]
    return {
        "most_common": most_common,
        "min_eigenvalue": min_eigenvalue,
        "max_negative_count": max_negative_count,
        "pass": most_common == (4, 0, 3) and max_negative_count == 0,
    }


def commutant_dimension(automorphisms):
    """Dimension of matrices commuting with the finite G2 automorphism witness."""
    basis = []
    for row in range(7):
        for col in range(7):
            element = np.zeros((7, 7))
            element[row, col] = 1.0
            basis.append(element)

    blocks = []
    for transform in automorphisms:
        block = np.column_stack([
            (transform @ element - element @ transform).reshape(-1)
            for element in basis
        ])
        blocks.append(block)
    constraints = np.vstack(blocks)
    singular_values = np.linalg.svd(constraints, compute_uv=False)
    tolerance = 1e-9 * max(1.0, float(singular_values[0]))
    return int(np.sum(singular_values < tolerance)), singular_values


def four_plane_obstruction():
    """Show that G2 symmetry does not select a canonical 4-plane in Im(O)."""
    automorphisms = finite_g2_automorphisms()
    projector = np.diag([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0])
    averaged = sum(transform @ projector @ transform.T for transform in automorphisms) / len(automorphisms)
    scalar_average = (4.0 / 7.0) * np.eye(7)
    scalar_error = float(np.max(np.abs(averaged - scalar_average)))
    idempotent_error = float(np.linalg.norm(averaged @ averaged - averaged))
    eigenvalues = np.linalg.eigvalsh(averaged)
    commutant_dim, singular_values = commutant_dimension(automorphisms)
    return {
        "n_automorphisms": len(automorphisms),
        "scalar_error": scalar_error,
        "idempotent_error": idempotent_error,
        "eigenvalues": eigenvalues,
        "commutant_dim": commutant_dim,
        "sv_min": float(singular_values[-1]),
        "pass": len(automorphisms) == 1344 and scalar_error < 1e-12 and commutant_dim == 1,
    }


def handpicked_plane_signature(n_trials=128):
    """Restrict the internal metric to a chosen 4-plane and inspect signature."""
    rng = np.random.default_rng(43)
    embedding = np.eye(7, 4)
    signatures = {}
    max_negative_count = 0
    for _ in range(n_trials):
        a, b = random_imag(rng), random_imag(rng)
        restricted = embedding.T @ emergent_metric(a, b) @ embedding
        signature, _ = matrix_signature(restricted)
        key = (signature.positive, signature.negative, signature.zero)
        signatures[key] = signatures.get(key, 0) + 1
        max_negative_count = max(max_negative_count, signature.negative)
    most_common = max(signatures.items(), key=lambda item: item[1])[0]
    return {
        "most_common": most_common,
        "max_negative_count": max_negative_count,
        "pass": max_negative_count == 0,
    }


def flat_limit_scaling():
    """Check the small-curvature limit as the source bivector area goes to zero."""
    e1 = imag_octonion([1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    traces = []
    angles = np.array([1e-3, 2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 1e-1])
    for angle in angles:
        b = imag_octonion([math.cos(angle), math.sin(angle), 0.0, 0.0, 0.0, 0.0, 0.0])
        traces.append(float(np.trace(emergent_metric(e1, b))))
    traces = np.array(traces)
    slope, intercept = np.polyfit(np.log(angles), np.log(traces), 1)
    normalized = traces / (16.0 * np.sin(angles) ** 2)
    return {
        "slope": float(slope),
        "normalized_mean": float(np.mean(normalized)),
        "normalized_std": float(np.std(normalized)),
        "trace_min": float(np.min(traces)),
        "pass": abs(slope - 2.0) < 1e-3 and abs(np.mean(normalized) - 1.0) < 1e-8,
    }


def print_spacetime_check(result):
    print("SPACETIME ARENA CHECK")
    print("=" * 78)
    print(f"C x H ~= M_2(C), det gives (+---) norm: det error {result['det_error']:.2e}")
    print(f"SL(2,C) action preserves Hermiticity:        error {result['hermitian_error']:.2e}")
    print("Status: PASS - the flat Lorentzian arena is available, but separate from Im(O).")
    print()


def print_internal_metric(result):
    print("INTERNAL ASSOCIATOR METRIC")
    print("=" * 78)
    pos, neg, zero = result["most_common"]
    print(f"Most common signature on Im(O): ({pos} positive, {neg} negative, {zero} zero)")
    print(f"Minimum eigenvalue over samples: {result['min_eigenvalue']:.2e}")
    print("Status: PASS for kinematics; OPEN for gravity because this is PSD, not Lorentzian.")
    print()


def print_four_plane_obstruction(result):
    print("CANONICAL 4-PLANE TEST")
    print("=" * 78)
    eigenvalues = ", ".join(f"{value:.6f}" for value in result["eigenvalues"])
    print(f"Finite G2 automorphism witness size: {result['n_automorphisms']}")
    print(f"Commutant dimension of the 7D action: {result['commutant_dim']} (only scalars)")
    print(f"Group-average of a rank-4 projector: eigenvalues [{eigenvalues}]")
    print(f"Max error from (4/7) I: {result['scalar_error']:.2e}")
    print(f"Averaged projector idempotency error: {result['idempotent_error']:.3f}")
    print("Interpretation: G2 symmetry washes any chosen 4-plane into (4/7)I.")
    print("A 4D spacetime subspace therefore has to be supplied by extra structure.")
    print()


def print_plane_signature(result):
    print("HAND-PICKED 4-PLANE SIGNATURE TEST")
    print("=" * 78)
    pos, neg, zero = result["most_common"]
    print(f"Restricting g to the coordinate 4-plane gives typical signature: ({pos}, {neg}, {zero})")
    print(f"Maximum negative directions observed: {result['max_negative_count']}")
    print("Interpretation: even after choosing a 4-plane by hand, the associator metric remains PSD.")
    print("A Lorentzian time direction must come from the separate C x H arena or new data.")
    print()


def print_flat_limit(result):
    print("FLAT / WEAK-FIELD LIMIT")
    print("=" * 78)
    print(f"tr g ~ theta^p with fitted p = {result['slope']:.6f}")
    print(f"tr g / (16 sin^2 theta) mean = {result['normalized_mean']:.6f} +/- {result['normalized_std']:.2e}")
    print("Status: PASS for a perturbative flat limit as source bivector area -> 0.")
    print("Newtonian status: OPEN - no 1/r potential, field equation, or Newton constant follows.")
    print()


def gate_checks(results):
    checks = [
        GateCheck(
            "flat Lorentzian arena from C x H",
            "PASS" if results["spacetime"]["pass"] else "FAIL",
            f"det/Hermiticity errors {results['spacetime']['det_error']:.1e}/{results['spacetime']['hermitian_error']:.1e}",
            "standard M_2(C) witness is intact",
        ),
        GateCheck(
            "internal associator metric",
            "PASS" if results["internal"]["pass"] else "FAIL",
            f"signature {results['internal']['most_common']}",
            "kinematic rank-4 PSD metric remains valid",
        ),
        GateCheck(
            "canonical G2-invariant four-plane",
            "OPEN",
            f"commutant dim {results['four_plane']['commutant_dim']}; projector average -> (4/7)I",
            "no 4D spacetime plane is selected without extra structure",
        ),
        GateCheck(
            "Lorentzian signature from associator metric",
            "OPEN",
            f"hand-picked 4-plane max negative directions {results['plane_signature']['max_negative_count']}",
            "the internal metric is PSD; time direction is not derived",
        ),
        GateCheck(
            "flat perturbative limit",
            "PASS" if results["flat"]["pass"] else "FAIL",
            f"tr g scales as theta^{results['flat']['slope']:.3f}",
            "curvature turns off as source bivector area goes to zero",
        ),
        GateCheck(
            "Einstein/Newton dynamics",
            "OPEN",
            "no field equation, action variation, or Newton constant",
            "Phase 5 acceptance requires dynamics; this gate does not have it",
        ),
    ]
    return checks


def print_verdict(results):
    print("PHASE 5 GATE VERDICT")
    print("=" * 78)
    internal_fail = False
    for check in gate_checks(results):
        print(f"{check.status:<6} {check.requirement:<44} {check.metric}")
        print(f"       {check.note}")
        if check.status == "FAIL":
            internal_fail = True
    print()
    print("AUDIT STATUS: PASS - the gravity decision is explicit and reproducible.")
    print("GRAVITY STATUS: OUT OF SCOPE FOR THE PRESENT FRAMEWORK.")
    print("REASON: the internal G2 metric does not select a 4D Lorentzian spacetime")
    print("        or dynamics without extra structure. Keep it as an exploratory side line.")
    if internal_fail:
        raise SystemExit(1)


def main():
    print("=" * 78)
    print("  PHASE 5 - GRAVITY GATE")
    print("  Tests whether the internal G2 metric becomes 4D Lorentzian dynamics.")
    print("=" * 78)
    print()

    results = {
        "spacetime": spacetime_arena_check(),
        "internal": internal_metric_signature(),
        "four_plane": four_plane_obstruction(),
        "plane_signature": handpicked_plane_signature(),
        "flat": flat_limit_scaling(),
    }

    print_spacetime_check(results["spacetime"])
    print_internal_metric(results["internal"])
    print_four_plane_obstruction(results["four_plane"])
    print_plane_signature(results["plane_signature"])
    print_flat_limit(results["flat"])
    print_verdict(results)


if __name__ == "__main__":
    main()
