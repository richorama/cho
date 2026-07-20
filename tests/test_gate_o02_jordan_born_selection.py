import unittest
from fractions import Fraction

from jordan_bootstrap.jordan import (
    frame_from_orthogonal,
    identity_matrix,
    is_jordan_frame,
    is_primitive_idempotent,
    jordan_product,
    jordan_state_census,
    outer,
    trace,
    trace_form,
)
from jordan_bootstrap.frame import frames
from jordan_bootstrap.octonion import E, octonion


def _real(x):
    return octonion(x, 0, 0, 0, 0, 0, 0, 0)


class GateO02JordanBornSelection(unittest.TestCase):
    """Octonion premise, Gate O02: Born selection on the exceptional Jordan algebra.

    Rank-one primitive idempotents of h_3(O) are the pure states (OP^2); a Jordan
    frame resolves the identity; the Born rule is the trace form tr(P o Q). The
    trace-form frame total is tr(P) for every frame (Gleason on h_3(O)), and
    non-associativity obstructs statehood: some Hermitian unit-trace rays are not
    idempotent.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = jordan_state_census()

    def test_declared_states_are_primitive_idempotents(self) -> None:
        self.assertEqual(self.census.idempotents_declared, 4)
        self.assertEqual(self.census.idempotents_verified, 4)

    def test_non_associative_rays_are_not_states(self) -> None:
        # Each is Hermitian with unit trace, yet none is idempotent: not a point
        # of OP^2. Non-associativity obstructs statehood -- the octonionic wall.
        self.assertEqual(self.census.nonassociative_declared, 3)
        self.assertEqual(self.census.nonassociative_hermitian_unit_trace, 3)
        self.assertEqual(self.census.nonassociative_idempotent_failures, 3)

    def test_declared_frames_resolve_the_identity(self) -> None:
        self.assertEqual(self.census.frame_count, 2)
        self.assertEqual(self.census.frames_are_resolutions_of_identity, 2)

    def test_trace_form_frame_total_is_tr_P_gleason_on_h3O(self) -> None:
        # sum_i tr(P o Q_i) == tr(P) for every state and every Jordan frame.
        self.assertEqual(self.census.trace_form_frame_checks, 8)
        self.assertEqual(self.census.trace_form_frame_mismatches, 0)

    def test_superposition_state_is_contextual_at_r4(self) -> None:
        self.assertEqual(self.census.contextual_states_r4, 1)

    def test_explicit_jordan_frame_and_born_total(self) -> None:
        frame = frame_from_orthogonal(frames(3)["B"])
        self.assertTrue(is_jordan_frame(frame))
        # A pure state P from a unit real vector; Born total over the frame = 1.
        state = outer((_real(Fraction(3, 5)), _real(Fraction(4, 5)), octonion(0, 0, 0, 0, 0, 0, 0, 0)))
        self.assertTrue(is_primitive_idempotent(state))
        total = sum(
            (trace_form(state, q).coords[0] for q in frame), Fraction(0)
        )
        self.assertEqual(total, Fraction(1))

    def test_diagonal_frame_sums_to_identity(self) -> None:
        frame = frame_from_orthogonal(frames(3)["A"])
        total = frame[0]
        for q in frame[1:]:
            total = tuple(
                tuple(total[i][j] + q[i][j] for j in range(3)) for i in range(3)
            )
        self.assertTrue(
            all(
                total[i][j].coords == identity_matrix()[i][j].coords
                for i in range(3)
                for j in range(3)
            )
        )

    def test_non_associative_ray_fails_idempotency_directly(self) -> None:
        v = (E[1].scaled(Fraction(2, 3)), E[2].scaled(Fraction(2, 3)), E[4].scaled(Fraction(1, 3)))
        p = outer(v)
        self.assertEqual(trace(p).coords[0], Fraction(1))
        self.assertFalse(is_primitive_idempotent(p))


if __name__ == "__main__":
    unittest.main()
