import unittest

from amplitude_bootstrap.interaction import (
    BLOCKINGS,
    InteractionCensus,
    interaction_census,
    multi_blocking_interacting_frames,
    non_interacting_survivors_are_nonclassical,
)


class GateQ09Interaction(unittest.TestCase):
    """Amplitude Gate Q09: the make-or-break interaction question.

    Does any interacting two-qubit unitary admit an autonomous coarse law under two
    independent blockings? Enumerating a declared six-blocking family of the fixed Q01
    ensemble answers no: under the two canonical tensor-factor traces the interacting
    survivor count is exactly zero, no interacting unitary is autonomous under more than
    one structurally distinct blocking, and every interacting law that does close is
    reversible. Observer-consistent amplitude dynamics are therefore non-interacting.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = interaction_census()

    def test_ensemble_partition_is_exact(self) -> None:
        self.assertIsInstance(self.census, InteractionCensus)
        self.assertEqual(self.census.ensemble_size, 144)
        self.assertEqual(self.census.interacting_total, 108)
        self.assertEqual(self.census.non_interacting_total, 36)

    def test_declared_family_has_six_independent_blockings(self) -> None:
        self.assertEqual(len(BLOCKINGS), 6)

    def test_no_interacting_unitary_survives_both_canonical_traces(self) -> None:
        # The make-or-break result: trace-A and trace-B agree on 36 non-interacting
        # survivors and zero interacting ones.
        self.assertEqual(self.census.canonical_survivors, 36)
        self.assertEqual(self.census.canonical_interacting, 0)

    def test_interaction_never_survives_two_distinct_blockings(self) -> None:
        # Exactly one interacting member reaches two blockings, and only within the
        # bespoke CNOT/reverse-CNOT frame pair (a single shared entangling resource).
        self.assertEqual(self.census.max_blockings_any_interacting, 2)
        self.assertEqual(self.census.interacting_multi_blocking, 1)
        frames = multi_blocking_interacting_frames()
        self.assertEqual(frames, (("cz", ("cnot", "rcnot")),))

    def test_every_interacting_law_that_closes_is_reversible(self) -> None:
        # Whenever interaction does admit an autonomous law under some cut, that law is
        # effectively non-interacting: reversible, Choi rank one.
        self.assertEqual(self.census.interacting_autonomous_instances, 8)
        self.assertTrue(self.census.all_interacting_laws_reversible)

    def test_non_interacting_dynamics_are_robustly_autonomous(self) -> None:
        # By contrast, every non-interacting unitary is autonomous under at least three
        # of the six blockings.
        self.assertEqual(self.census.min_blockings_any_non_interacting, 3)

    def test_non_interacting_survivors_stay_nonclassical(self) -> None:
        self.assertTrue(non_interacting_survivors_are_nonclassical())


if __name__ == "__main__":
    unittest.main()
