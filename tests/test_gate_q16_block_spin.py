import unittest
from fractions import Fraction

from amplitude_bootstrap.approximate_closure import closure_defect
from amplitude_bootstrap.block_spin import (
    ISOMETRIES,
    _CROT,
    block_spin_census,
    block_spin_summary,
    is_isometry,
    single_block_defect,
)
from amplitude_bootstrap.coarse_graining import _CNOT, _CZ


class GateQ16BlockSpin(unittest.TestCase):
    """Amplitude Gate Q16: isometric block-spin does not rescue interaction either.

    Gate Q15 blamed interaction-irrelevance on the dimensional dilution of a bare
    decimation (partial trace). This gate replaces the trace by an isometric block-spin
    ``B_w(O) = w^dagger O w`` that merges two qubits into one effective qubit through an
    isometry ``w`` (``w^dagger w = I``). Two facts emerge. First, block-spin is a
    genuinely different coarse-graining: on the computational-basis isometries ``CZ`` is
    exactly autonomous (defect 0) where decimation leaves defect 4. Second, interaction is
    still universally irrelevant: over the declared isometry family and every coupling the
    two-level flow strictly contracts (worst ratio below one), so no isometry makes any
    coupling marginal or relevant. The non-interacting fixed point survives a second,
    inequivalent, dimension-reducing coarse-graining.
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls.census = block_spin_census()
        cls.summary = block_spin_summary()

    # --- The declared blocking maps are genuine isometries. --------------------

    def test_isometry_family_is_the_declared_six(self) -> None:
        self.assertEqual(len(ISOMETRIES), 6)
        self.assertEqual(
            tuple(name for name, _ in ISOMETRIES),
            ("keep", "ghz", "sym", "bell", "phase", "gen"),
        )

    def test_every_declared_map_is_an_isometry(self) -> None:
        self.assertTrue(self.summary.all_isometries_valid)
        self.assertTrue(all(is_isometry(w) for _, w in ISOMETRIES))

    # --- Block-spin is inequivalent to decimation. -----------------------------

    def test_cz_is_autonomous_under_the_aligned_isometries(self) -> None:
        aligned = dict(ISOMETRIES)
        for name in ("keep", "ghz", "sym", "bell", "phase"):
            self.assertEqual(single_block_defect(_CZ, aligned[name]), Fraction(0))

    def test_a_generic_isometry_reintroduces_a_cz_defect(self) -> None:
        gen = dict(ISOMETRIES)["gen"]
        self.assertEqual(single_block_defect(_CZ, gen), Fraction(1108224, 390625))

    def test_decimation_leaves_cz_a_positive_defect(self) -> None:
        # The partial-trace defect of Gate Q13; a single block-spin can beat it.
        self.assertEqual(closure_defect(_CZ), Fraction(4))
        self.assertTrue(self.summary.cz_autonomous_under_some_block_spin)
        self.assertTrue(self.summary.block_spin_differs_from_decimation)

    # --- Exact single-block defects (the test owns the values). ----------------

    def test_single_block_defects_are_exact(self) -> None:
        table = dict(ISOMETRIES)
        self.assertEqual(single_block_defect(_CNOT, table["keep"]), Fraction(3))
        self.assertEqual(single_block_defect(_CNOT, table["ghz"]), Fraction(3))
        self.assertEqual(single_block_defect(_CNOT, table["bell"]), Fraction(3))
        self.assertEqual(
            single_block_defect(_CNOT, table["sym"]), Fraction(1064064, 390625)
        )
        self.assertEqual(
            single_block_defect(_CNOT, table["phase"]), Fraction(1064064, 390625)
        )
        self.assertEqual(single_block_defect(_CROT, table["keep"]), Fraction(819, 625))
        self.assertEqual(
            single_block_defect(_CROT, table["gen"]), Fraction(6868224, 9765625)
        )

    # --- The central verdict: still no escape. ---------------------------------

    def test_every_pair_is_irrelevant_or_fixed(self) -> None:
        self.assertTrue(self.summary.all_irrelevant)
        self.assertTrue(
            all(
                row.classification in ("irrelevant", "fixed_point")
                for row in self.census
            )
        )

    def test_no_relevant_or_marginal_pair_exists(self) -> None:
        self.assertEqual(self.summary.relevant_or_marginal, 0)

    def test_flow_strictly_contracts_across_the_whole_sweep(self) -> None:
        self.assertEqual(
            self.summary.worst_ratio,
            Fraction(5215972980711164182368, 46456577684866181640625),
        )
        self.assertLess(self.summary.worst_ratio, Fraction(1))


if __name__ == "__main__":
    unittest.main()
