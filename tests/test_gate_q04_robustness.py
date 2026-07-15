import unittest

from amplitude_bootstrap import robustness_summary
from amplitude_bootstrap.coarse_graining import (
    environment_decoherence_census,
    reduced_dynamics_census,
)
from amplitude_bootstrap.interference import coherence_matches_reversibility
from amplitude_bootstrap.robustness import (
    COARSE_GRAININGS,
    RobustnessRow,
    decoherence_requires_interaction,
    irreversible_but_coherent_count,
    noninteracting_dynamics_is_invariant,
    reversibility_implies_nonclassicality,
)


class GateQ04Robustness(unittest.TestCase):
    """Amplitude Gate Q04: which conclusions survive a second coarse-graining?"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.summary = robustness_summary()

    def test_two_coarse_grainings_are_declared(self) -> None:
        self.assertEqual(COARSE_GRAININGS, (("trace_b", 1), ("trace_a", 0)))

    def test_reduced_autonomy_no_go_is_robust(self) -> None:
        for _, traced in COARSE_GRAININGS:
            census = reduced_dynamics_census(traced)
            self.assertEqual(census.autonomous, 36)
            self.assertEqual(census.autonomous_local, 36)
            self.assertEqual(census.autonomous_entangling, 0)

    def test_noninteracting_dynamics_is_invariant_under_both_maps(self) -> None:
        for _, traced in COARSE_GRAININGS:
            self.assertTrue(noninteracting_dynamics_is_invariant(traced))

    def test_all_decoherence_requires_interaction_under_both_maps(self) -> None:
        for _, traced in COARSE_GRAININGS:
            self.assertTrue(decoherence_requires_interaction(traced))
            for row in environment_decoherence_census(traced):
                self.assertEqual(row.decohering, row.decohering_entangling)

    def test_reversibility_always_implies_nonclassicality(self) -> None:
        for _, traced in COARSE_GRAININGS:
            self.assertTrue(reversibility_implies_nonclassicality(traced))

    def test_exact_equivalence_is_a_trace_b_artefact(self) -> None:
        self.assertTrue(coherence_matches_reversibility(1))
        self.assertFalse(coherence_matches_reversibility(0))
        self.assertEqual(irreversible_but_coherent_count(1), 0)
        self.assertEqual(irreversible_but_coherent_count(0), 108)

    def test_robustness_summary_matches_expected(self) -> None:
        self.assertEqual(
            self.summary,
            (
                RobustnessRow("trace_b", 36, True, True, True, True, 0),
                RobustnessRow("trace_a", 36, True, True, True, False, 108),
            ),
        )


if __name__ == "__main__":
    unittest.main()
