"""
Item 7f -- N5 operator hardening: sin^2(theta23) = 4/7 as a symmetry-class
invariant of an explicit mixing operator (not a table read-off).
==========================================================================

The open N5 obligation (ledger N5; theta23_fano_invariance.py;
epsilon_mixing_coefficients.py)
-------------------------------------------------------------------------
The sharpest CHO bet is the atmospheric octant

        sin^2(theta23) = (Fano lines avoiding the vacuum) / (all Fano lines) = 4/7.

`theta23_fano_invariance.py` already hardened the VALUE half: the (3 through, 4
avoiding) split is vacuum-independent and convention-independent. But both that
module and `epsilon_mixing_coefficients.py` still obtain 4/7 by COUNTING lines in
the incidence table. The surviving N5 question is whether 4/7 is an OPERATOR fact
-- the spectral content of an actual mixing operator -- or only a tally.

What this module adds
---------------------
It recasts the count as the normalized trace (the spectral mean) of an explicit,
intrinsically-defined operator on Fano line-space, and proves that normalized
trace is an INVARIANT of the operator's symmetry class -- machine-checked over
the entire automorphism group and every vacuum point. Concretely, for a vacuum
point v, the vacuum-avoidance operator on the 7-dimensional line-space is the
orthogonal projector

        P_avoid(v)  =  diag over lines L of [ 1 if v not in L else 0 ],

a rank-4 projector (P^2 = P = P^T) with spectrum {1^4, 0^3}. Then:

  [A] VALUE AS A TRACE.  sin^2(theta23) = Tr P_avoid / Tr I = 4/7 (exact), and
      equivalently 4/7 = 1/2 + (avoiding - through)/(2*total) = 1/2 + 1/14:
      maximal mixing plus the single-line Fano asymmetry. The mirror operator
      P_through is rank 3 -> 3/7 (the lower octant), with 4/7 + 3/7 = 1.

  [B] SPECTRAL, NOT COORDINATE.  P_avoid is a genuine orthogonal projector; its
      normalized trace equals the spectral mean (unit eigenvalues / dimension),
      a basis-free quantity, not a chosen matrix entry.

  [C] SYMMETRY-CLASS INVARIANT (the real operator statement).  Aut(Fano) =
      PSL(2,7) (order 168) acts on line-space by permutation matrices Pi_g, and

            Pi_g . P_avoid(v) . Pi_g^T  =  P_avoid(g(v))      for all g,

      so the seven vacuum operators form a SINGLE conjugacy orbit (the point
      action is transitive). A class invariant -- the normalized trace -- is
      therefore the same 4/7 for every vacuum choice and every octonion
      relabelling. Verified exactly over all 168 group elements x 7 vacua.

  [D] OCTANT + THE OPEN MAP.  Choosing the avoiding (broken) sector over the
      through (stabiliser/colour SU(3)) sector is the octant choice 4/7 vs 3/7;
      it is selected by the physical input "mixing lives in the broken
      directions", motivated but not derived. And the identification

            atmospheric oscillation probability  =  normalized trace of P_avoid

      is the N5 bridge itself. This module makes that map a precise operator
      statement and shows the value is then forced and basis-free; it does NOT
      derive the map from a CHO action. N5 stays the open obligation.

PROVED here (exact, machine-checked):
  - P_avoid(v) is a rank-4 orthogonal projector with spectrum {1^4, 0^3};
  - its normalized trace is 4/7 = 1/2 + 1/14 (maximal + Fano asymmetry);
  - Pi_g P_avoid(v) Pi_g^T = P_avoid(g(v)) for all 168 automorphisms, and the
    point action is transitive, so 4/7 is a single-orbit class invariant;
  - the mirror P_through gives the complementary 3/7, with 4/7 + 3/7 = 1.

NOT proved here (the surviving open obligation):
  - the PHYSICAL map "atmospheric oscillation probability = normalized trace of
    the avoidance projector". Given the map, the value is forced and canonical;
    deriving the map from the CHO action is the open N5 problem.

DIAGNOSTIC hardening: promotes no ledger row, moves no Bayes credit. The frozen
registry (Q2, Theta23_octant) stays authoritative; this reads it back read-only.

numpy (exact integer arithmetic on small matrices) + fractions + spurion_bridge.
No scipy.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/theta23_mixing_operator.py
"""

from __future__ import annotations

from fractions import Fraction

import numpy as np

import prediction_registry
from spurion_bridge import FANO_LINES, VACUUM_POINT, fano_automorphisms


# --------------------------------------------------------------------------
# Shared facts (single source of truth: spurion_bridge Fano data).
# --------------------------------------------------------------------------
LINES = tuple(frozenset(line) for line in FANO_LINES)   # 7 lines on points 1..7
POINTS = tuple(range(1, 8))
TOTAL = len(LINES)                                       # 7
PSL27_ORDER = 168                                        # |Aut(Fano)| = |PSL(2,7)|

SIN2_UPPER = Fraction(4, 7)      # avoiding / total  (upper octant, CHO)
SIN2_LOWER = Fraction(3, 7)      # through  / total  (lower mirror)
SIN2_MAXIMAL = Fraction(1, 2)

TOL = 1e-12


# --------------------------------------------------------------------------
# The vacuum-avoidance / vacuum-through operators on line-space.
# --------------------------------------------------------------------------
def avoidance_mask(vacuum: int) -> tuple[int, ...]:
    """1 on lines avoiding the vacuum point, 0 on lines through it."""
    return tuple(1 if vacuum not in line else 0 for line in LINES)


def avoidance_projector(vacuum: int) -> np.ndarray:
    """Rank-4 orthogonal projector onto the vacuum-avoiding lines (integer)."""
    return np.diag(np.array(avoidance_mask(vacuum), dtype=np.int64))


def through_projector(vacuum: int) -> np.ndarray:
    """Rank-3 complementary projector onto the lines through the vacuum."""
    return np.eye(TOTAL, dtype=np.int64) - avoidance_projector(vacuum)


def normalized_trace(projector: np.ndarray) -> Fraction:
    """Exact spectral mean = Tr P / dim, as a Fraction."""
    return Fraction(int(np.trace(projector)), TOTAL)


# --------------------------------------------------------------------------
# Induced action of a point-automorphism on line-space.
# --------------------------------------------------------------------------
def induced_line_permutation(g: dict) -> tuple[int, ...]:
    """A point automorphism g permutes the 7 lines; return that permutation."""
    perm = []
    for line in LINES:
        image = frozenset(g[p] for p in line)
        perm.append(LINES.index(image))
    return tuple(perm)


def permutation_matrix(perm: tuple[int, ...]) -> np.ndarray:
    """7x7 permutation matrix Pi with Pi[perm[i], i] = 1 (column i -> row perm[i])."""
    mat = np.zeros((TOTAL, TOTAL), dtype=np.int64)
    for i, j in enumerate(perm):
        mat[j, i] = 1
    return mat


def point_orbit(automorphisms: list[dict], start: int) -> set:
    """Orbit of a point under the automorphism group (transitivity check)."""
    return {g[start] for g in automorphisms}


# --------------------------------------------------------------------------
# Reporting + tripwires
# --------------------------------------------------------------------------
def main() -> bool:
    print("#" * 72)
    print("#  CHO ITEM 7f -- N5 OPERATOR HARDENING OF sin^2(theta23) = 4/7")
    print("#  4/7 as a symmetry-class invariant of an explicit mixing operator.")
    print("#  Diagnostic: stakes nothing new, promotes no row, moves no Bayes.")
    print("#" * 72)
    print()

    automorphisms = fano_automorphisms()
    P = avoidance_projector(VACUUM_POINT)
    Pthr = through_projector(VACUUM_POINT)
    eigvals = np.linalg.eigvalsh(P.astype(float))
    nt = normalized_trace(P)
    asymmetry = Fraction(int(np.trace(P)) - int(np.trace(Pthr)), 2 * TOTAL)

    # ------------------------------------------------------------------
    print("=" * 72)
    print("  A  VALUE AS A NORMALIZED TRACE (exact)")
    print("=" * 72)
    print(f"  vacuum point e{VACUUM_POINT};  line-space dimension = {TOTAL}")
    print(f"  rank P_avoid (avoiding lines)   : {int(np.trace(P))}")
    print(f"  rank P_through (through lines)  : {int(np.trace(Pthr))}")
    print(f"  sin^2(theta23) = Tr P_avoid/dim : {nt}  = {float(nt):.6f}")
    print(f"  maximal + Fano asymmetry        : 1/2 + {asymmetry} = "
          f"{SIN2_MAXIMAL + asymmetry}")
    print(f"  mirror (through/total)          : {SIN2_LOWER}  -> lower octant")
    print(f"  complementary check 4/7 + 3/7   : {SIN2_UPPER + SIN2_LOWER}")
    print()

    # ------------------------------------------------------------------
    print("=" * 72)
    print("  B  SPECTRAL, NOT COORDINATE")
    print("=" * 72)
    print(f"  P_avoid is an orthogonal projector (P^2 = P = P^T).")
    print(f"  eigenvalues          : {np.round(eigvals, 9).tolist()}")
    print(f"  spectrum multiplicities: 1 x {int(round(eigvals.sum()))}, "
          f"0 x {TOTAL - int(round(eigvals.sum()))}")
    print(f"  normalized trace = spectral mean = {nt} (basis-free).")
    print()

    # ------------------------------------------------------------------
    print("=" * 72)
    print("  C  SYMMETRY-CLASS INVARIANT (the operator statement)")
    print("=" * 72)
    equivariant = True
    trace_invariant = True
    for g in automorphisms:
        perm = induced_line_permutation(g)
        Pi = permutation_matrix(perm)
        conjugate = Pi @ P @ Pi.T
        target = avoidance_projector(g[VACUUM_POINT])
        if not np.array_equal(conjugate, target):
            equivariant = False
        if normalized_trace(conjugate) != nt:
            trace_invariant = False
    orbit = point_orbit(automorphisms, VACUUM_POINT)
    print(f"  |Aut(Fano)| = {len(automorphisms)}  (= |PSL(2,7)| = {PSL27_ORDER})")
    print(f"  Pi_g P_avoid(v) Pi_g^T == P_avoid(g(v)) for all g : {equivariant}")
    print(f"  normalized trace invariant under all g            : {trace_invariant}")
    print(f"  point orbit of e{VACUUM_POINT} under Aut           : {sorted(orbit)}")
    print(f"  action transitive (all 7 vacua one orbit)         : {orbit == set(POINTS)}")
    all_vacua = {normalized_trace(avoidance_projector(v)) for v in POINTS}
    print(f"  normalized trace over ALL vacua                   : {all_vacua} -> single value")
    print()

    # ------------------------------------------------------------------
    print("=" * 72)
    print("  D  OCTANT CHOICE + THE OPEN PHYSICAL MAP")
    print("=" * 72)
    print("  avoiding (broken, rank 4) -> 4/7 UPPER ; through (SU(3) stabiliser,")
    print("  rank 3) -> 3/7 LOWER. CHO takes the broken sector (motivated input,")
    print("  not derived). The map 'oscillation probability = normalized trace of")
    print("  P_avoid' is the N5 bridge: made precise here, still not derived from a")
    print("  CHO action. Given the map + octant, the value is forced and basis-free.")
    print()

    # ------------------------------------------------------------------
    print("=" * 72)
    print("  E  READ-ONLY REGISTRY CROSS-CHECK")
    print("=" * 72)
    payload = prediction_registry.theta23_octant_values()
    value_ok = abs(payload["sin2_theta23"] - float(SIN2_UPPER)) < TOL
    octant_ok = payload["octant"] == "upper"
    print(f"  registry Q2 (Theta23_octant): "
          f"{'LOCKED-MATCH' if (value_ok and octant_ok) else 'DRIFT'}")
    print(f"    payload = {payload}")
    print()

    print("-" * 72)
    print("  Reading guide: this recasts 4/7 from an incidence-table count into the")
    print("  normalized trace of an explicit projector and PROVES that trace is a")
    print("  single-orbit class invariant under the full Fano automorphism group --")
    print("  a basis-free operator fact. The physical identification (the N5 map)")
    print("  stays the open CHO-action obligation; diagnostic, no row promoted.")

    # ---- assert ONLY the exact / structural spine ----------------------------
    # [A] counts and exact value
    assert len(LINES) == 7, "the octonion Fano plane must have 7 lines"
    for v in POINTS:
        assert sum(avoidance_mask(v)) == 4, f"vacuum e{v} must avoid exactly 4 lines"
        assert sum(through_projector(v).diagonal()) == 3, f"vacuum e{v} must lie on 3 lines"
    assert nt == SIN2_UPPER == Fraction(4, 7), "normalized trace must be exactly 4/7"
    assert asymmetry == Fraction(1, 14), "Fano asymmetry must be exactly 1/14"
    assert SIN2_MAXIMAL + asymmetry == SIN2_UPPER, "4/7 = 1/2 + 1/14 must hold"
    assert SIN2_UPPER + SIN2_LOWER == 1, "octant complementarity 4/7 + 3/7 = 1"
    # [B] projector + spectrum
    assert np.array_equal(P @ P, P), "P_avoid must be idempotent (a projector)"
    assert np.array_equal(P.T, P), "P_avoid must be symmetric (orthogonal projector)"
    assert int(round(eigvals.sum())) == 4, "P_avoid must have four unit eigenvalues"
    assert np.allclose(np.sort(eigvals), np.array([0, 0, 0, 1, 1, 1, 1]), atol=1e-9), \
        "spectrum must be {1^4, 0^3}"
    # [C] equivariance, transitivity, single-orbit invariance
    assert len(automorphisms) == PSL27_ORDER, "Aut(Fano) must have order 168"
    assert equivariant, "Pi_g P_avoid(v) Pi_g^T = P_avoid(g(v)) must hold for all g"
    assert trace_invariant, "normalized trace must be invariant under all automorphisms"
    assert orbit == set(POINTS), "the point action must be transitive (single orbit)"
    assert all_vacua == {Fraction(4, 7)}, "every vacuum must give the same 4/7"
    # [E] registry read-only
    assert value_ok and octant_ok, "locked registry Q2 must still read 4/7 / upper"

    print("\n  RESULT: PASS (operator invariant; N5 physical map remains open).")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
