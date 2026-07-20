from fractions import Fraction
import unittest

from jordan_bootstrap.frame import (
    frame_consistency_census,
    frame_total,
    frames,
    is_orthogonal,
    theorem_witnesses,
)
from jordan_bootstrap.octonion import E, ONE


class GateO01FrameConsistency(unittest.TestCase):
    """Octonion premise, Gate O01: only the norm rule is frame-consistent on O^d.

    The octonionic successor to amplitude Gates Q11/Q12. Among the r-norm rules
    only r = 2 (the Born norm) gives a resolution-independent frame total when the
    amplitudes are octonions; r = 4 and r = 6 are contextual, and the octonionic
    'monomial' control (unit-octonion relabeling) never exposes r != 2.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = frame_consistency_census()

    def test_declared_frames_are_exactly_orthogonal(self) -> None:
        for d in (3, 4):
            frame_map = frames(d)
            self.assertTrue(is_orthogonal(frame_map["A"]))
            self.assertTrue(is_orthogonal(frame_map["B"]))

    def test_census_shape(self) -> None:
        self.assertEqual(self.census.dimensions, (3, 4))
        self.assertEqual(self.census.total_states, 10)

    def test_born_rule_is_exactly_frame_invariant(self) -> None:
        # r = 2 (Parseval) is invariant across every declared frame, every state.
        self.assertEqual(self.census.born_frame_checks, 20)
        self.assertEqual(self.census.born_frame_mismatches, 0)

    def test_higher_norms_are_contextual(self) -> None:
        # r = 4 and r = 6 disagree between the two frames for the superposing states.
        self.assertEqual(self.census.contextual_states_r4, 6)
        self.assertEqual(self.census.contextual_states_r6, 6)

    def test_octonion_unit_relabeling_never_exposes_a_higher_norm(self) -> None:
        # The octonionic monomial control: right-multiplying by a unit octonion
        # leaves the whole multiset of weights unchanged for every r.
        self.assertEqual(self.census.unit_relabel_checks, 120)
        self.assertEqual(self.census.unit_relabel_multiset_mismatches, 0)

    def test_witnesses_match_the_complex_born_theorem_exactly(self) -> None:
        # The (1,1,1) state reproduces the exact rationals of BORN_RULE_THEOREM.md,
        # now with octonionic amplitudes rather than Q(i).
        w = theorem_witnesses()
        self.assertEqual(w["r2_split_A"], Fraction(3))
        self.assertEqual(w["r2_split_B"], Fraction(3))
        self.assertEqual(w["r4_split_A"], Fraction(3))
        self.assertEqual(w["r4_split_B"], Fraction(3027, 625))
        self.assertEqual(w["r6_split_A"], Fraction(3))
        self.assertEqual(w["r6_split_B"], Fraction(5331, 625))

    def test_genuinely_octonionic_witness_state(self) -> None:
        # The same discrepancy appears for an imaginary-unit state (e1, e1, e1),
        # so the selection is not a real-amplitude artefact.
        frame_map = frames(3)
        state = (E[1], E[1], E[1])
        self.assertEqual(frame_total(frame_map["A"], state, 2), Fraction(3))
        self.assertEqual(frame_total(frame_map["B"], state, 2), Fraction(3))
        self.assertEqual(frame_total(frame_map["A"], state, 4), Fraction(3))
        self.assertNotEqual(
            frame_total(frame_map["B"], state, 4), Fraction(3)
        )
        self.assertEqual(frame_total(frame_map["B"], state, 4), Fraction(3027, 625))

    def test_orthogonal_unit_state_has_no_discrepancy(self) -> None:
        # A state of three distinct orthonormal units gives frame total = 3 for
        # every r: the rotation preserves each unit weight, so it cannot witness.
        frame_map = frames(3)
        state = (E[3], E[1], E[2])
        for r in (2, 4, 6):
            self.assertEqual(frame_total(frame_map["A"], state, r), Fraction(3))
            self.assertEqual(frame_total(frame_map["B"], state, r), Fraction(3))


if __name__ == "__main__":
    unittest.main()
