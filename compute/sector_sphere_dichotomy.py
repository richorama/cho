"""
Sector sphere-vs-discrete dichotomy: WHY the lepton shape carries pi and the
quark shapes do not.

Motivation
----------
The three first-generation shape factors are an open bridge (ledger M9, M10, M11):

    up      m_u = (1/4)   m_c^2 / m_t       k_u = 1/4
    down    m_d = (9/4)   m_s^2 / m_b       k_d = 9/4
    lepton  m_e = (1/4pi) m_mu^2 / m_tau    k_l = 1/(4 pi)

`lepton_yukawa_action.py` FORCED k_l = 1/(4 pi) as the SU(2)-invariant uniform
average of the rank-one transition projector over the two-level Bloch sphere S^2
(Schur -> I/2, normalized by 1/Vol(S^2) = 1/(4 pi)). Its named open seam was:

    WHY does the lepton channel use the CONTINUOUS-sphere (uniform SU(2)) average
    -- carrying pi -- while the quark sectors use DISCRETE weak-isospin
    projections k_u = 1/4, k_d = 9/4 with NO pi?

This module does not close that selection, but it isolates and verifies the exact
DISCRIMINANT, and ties the quark factors to already-derived numbers.

The discriminant (verified here)
--------------------------------
pi appears in a sector's first-generation shape factor IFF the transition is
averaged over a CONTINUOUS (positive-dimensional) manifold; it is ABSENT
(rational) IFF the average is over a FINITE/DISCRETE set. Concretely:

  [continuous]  A finite irreducible average and a continuous (Lie-group) average
                of a rank-one projector both give I/2 by Schur, but their
                NORMALIZATIONS differ in kind: a FINITE group average is the
                counting-measure mean -> a RATIONAL matrix (no pi); the
                CONTINUOUS S^2 average is the Haar/solid-angle mean -> normalized
                by 1/Vol(S^2) = 1/(4 pi), and Vol(S^2) = 4 pi is transcendental.
                We verify a finite group (Q8 on C^2) averages to EXACTLY I/2
                (rational), while the sphere average is 1/(4 pi).

  [Fock support] The sector's transition support is its Fock grade:
                - up   : the grade-0 vacuum,  Tr P_0 = 1  (colour SINGLET);
                - down : the grade-1 module,  Tr P_1 = 3  (colour TRIPLET, = N_c);
                - lepton: the FULL Fock module Lambda^*(C^3), Tr I = 2^3 = 8.
                A quark projects onto a SINGLE number-operator grade (a discrete
                eigenspace) -> a finite sum -> rational. A lepton is a colour
                SINGLET with no discrete colour fibre, so its transition runs over
                the whole colourless two-level continuum -> the continuous S^2
                average -> pi.

The quark factors as the SAME derived Fock ranks
------------------------------------------------
The quark shape factors are exactly the squares of the half of the derived Fock
grade ranks (the same Tr P_0 = 1, Tr P_1 = 3 that fix the channel coefficients
M1, M2):

    k_u = (Tr P_0 / 2)^2 = (1/2)^2 = 1/4
    k_d = (Tr P_1 / 2)^2 = (3/2)^2 = 9/4 = (1/4) * N_c^2 ,   N_c = Tr P_1 = 3.

This is precisely the "sector-square rule" ledger M10 asks for: k_d = (1/4) N_c^2.
Both quark factors are RATIONAL (discrete). The naive discrete extrapolation to the
full Fock module would give (8/2)^2 = 16; the lepton is instead 1/(4 pi) -- the
continuum REPLACES the discrete value, which is the whole point of the dichotomy.

Honest scope (what this does NOT close)
---------------------------------------
* It does NOT derive WHY the lepton uses the full continuous module while the
  quarks project onto a single Fock grade -- the dynamical SELECTION (colour
  singlet -> continuous, colour non-singlet -> discrete) is still the input. This
  module characterizes the selection's CONSEQUENCE (pi vs rational) and verifies
  it, rather than deriving the selection from the CHO action.
* The (rank/2)^2 quark law is fit on the TWO quark sectors (up, down); it is the
  simplest law reproducing both and tying them to the derived ranks, not a
  multi-sector theorem.
* The ~6% intrinsic m_e residual (M11) is untouched.

F0 is NOT promoted. M9, M10, M11 remain open bridges; this isolates their shared
discriminant and connects the quark factors to the derived Fock ranks.

numpy only. No scipy. Reuses epsilon_channel_coefficients (Fock ranks) and
lepton_yukawa_action (the continuous-sphere average).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/sector_sphere_dichotomy.py
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

import numpy as np

from epsilon_channel_coefficients import verify_fock_module
from ladder_charges import search_witt_basis
from lepton_yukawa_action import invariant_projector_average, solid_angles

PI = np.pi
N_COLOR = 3
TOL = 1e-7
FLAT_TOL = 1e-9


# --------------------------------------------------------------------------- #
#  Fock-grade ranks (the discrete support of each sector)                      #
# --------------------------------------------------------------------------- #
def fock_grade_ranks():
    """Tr P_g for g = 0..3 on the octonionic Fock module Lambda^*(C^3).
    Computed from the C (x) O Witt basis when available; the binomial structure
    C(3,g) = (1,3,3,1) is the stable theorem either way."""
    fixed, pairs, signs, alphas = search_witt_basis()
    if alphas is not None:
        fock = verify_fock_module(alphas)
        ranks = [fock["grade_traces"].get(g, 0) for g in range(4)]
        total = fock["total"]
        source = "C(x)O number-operator Fock-grade traces"
    else:
        ranks = [comb(3, g) for g in range(4)]
        total = sum(ranks)
        source = "binomial structure of Lambda^*(C^3) (Witt basis convention-sensitive)"
    return ranks, total, source


# --------------------------------------------------------------------------- #
#  Quark (discrete) shape factors = (Fock-grade rank / 2)^2                     #
# --------------------------------------------------------------------------- #
def quark_discrete_shape_factors(ranks):
    """k_u = (Tr P_0 / 2)^2 = 1/4 ; k_d = (Tr P_1 / 2)^2 = 9/4 = (1/4) N_c^2.
    Both RATIONAL: a single Fock grade is a discrete (finite-dimensional)
    eigenspace, so its invariant average is a counting mean (no pi)."""
    n_up, n_down = ranks[0], ranks[1]
    k_up = (n_up / 2.0) ** 2
    k_down = (n_down / 2.0) ** 2
    return {
        "k_up": k_up,
        "k_down": k_down,
        "n_up": n_up,
        "n_down": n_down,
        "k_down_as_quarter_Nc2": 0.25 * n_down * n_down,
        "down_rank_is_N_color": n_down == N_COLOR,
    }


# --------------------------------------------------------------------------- #
#  Lepton (continuous) shape factor = 1 / Vol(S^2) = 1/(4 pi)                   #
# --------------------------------------------------------------------------- #
def lepton_continuous_shape_factor():
    """k_l = 1/(4 pi): the continuous (uniform SU(2) / solid-angle) average of the
    rank-one projector over the full colourless two-level Bloch sphere S^2.
    Schur makes the average I/2; the normalization is 1/Vol(S^2), Vol(S^2)=4 pi."""
    A, k_l = invariant_projector_average()
    vol_s2, hemi = solid_angles()
    schur_flatness = float(np.max(np.abs(A - 0.5 * np.eye(2))))
    return {
        "k_l": k_l,
        "vol_s2": vol_s2,
        "hemisphere": hemi,
        "schur_flatness": schur_flatness,
    }


# --------------------------------------------------------------------------- #
#  The pi diagnostic: finite-group average is RATIONAL, sphere average has pi   #
# --------------------------------------------------------------------------- #
def finite_group_average_rational():
    """Average a rank-one projector |v><v| over the finite quaternion group
    Q8 acting irreducibly on C^2.  By Schur it is I/2, and -- being a finite
    counting mean -- it is EXACTLY rational (no pi).  This is the discrete
    counterpart of the continuous sphere average; the contrast (rational vs
    1/(4 pi)) is the entire discriminant."""
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    eye = np.eye(2, dtype=complex)
    Q8 = [eye, -eye, 1j * sx, -1j * sx, 1j * sy, -1j * sy, 1j * sz, -1j * sz]
    v = np.array([1.0 + 0j, 0.0])
    Pv = np.outer(v, v.conj())
    avg = sum(g @ Pv @ g.conj().T for g in Q8) / len(Q8)
    deviation = float(np.max(np.abs(avg - 0.5 * np.eye(2))))
    return avg.real, deviation


def rationality(value, max_den=64):
    """Nearest rational p/q (q <= max_den) and whether it reproduces the value
    exactly (a rational, pi-free quantity) or only approximately (pi-bearing)."""
    fr = Fraction(value).limit_denominator(max_den)
    err = abs(float(fr) - value)
    return fr, err, err < 1e-9


# --------------------------------------------------------------------------- #
#  Driver                                                                      #
# --------------------------------------------------------------------------- #
def main() -> bool:
    ranks, total, source = fock_grade_ranks()
    quark = quark_discrete_shape_factors(ranks)
    lepton = lepton_continuous_shape_factor()
    fin_avg, fin_dev = finite_group_average_rational()

    k_u, k_d, k_l = quark["k_up"], quark["k_down"], lepton["k_l"]

    print("=" * 78)
    print("  SECTOR SPHERE-vs-DISCRETE DICHOTOMY")
    print("  Why the lepton shape carries pi and the quark shapes do not")
    print("=" * 78)
    print()
    print("  Fock-grade ranks (the discrete support of each sector)")
    print("  " + "-" * 74)
    print(f"  Tr P_g (g=0..3) = {ranks}   total = {total} = 2^3   ({source})")
    print(f"  up   = grade 0  : Tr P_0 = {ranks[0]}   colour SINGLET")
    print(f"  down = grade 1  : Tr P_1 = {ranks[1]}   colour TRIPLET (= N_c = {N_COLOR})")
    print(f"  lepton          : full Fock module, Tr I = {total}   colour SINGLET")
    print()
    print("  Quark (discrete) shape factors = (Tr P_grade / 2)^2  -- RATIONAL")
    print("  " + "-" * 74)
    print(f"  k_u = (Tr P_0/2)^2 = ({ranks[0]}/2)^2 = {k_u:.4f}   (= 1/4)")
    print(f"  k_d = (Tr P_1/2)^2 = ({ranks[1]}/2)^2 = {k_d:.4f}   (= 9/4 = (1/4) N_c^2"
          f" = {quark['k_down_as_quarter_Nc2']:.4f})")
    print(f"  -> ledger M10's 'sector-square rule' k_d = (1/4) N_c^2 with N_c = Tr P_1.")
    print()
    print("  Lepton (continuous) shape factor = 1/Vol(S^2) = 1/(4 pi)  -- pi-BEARING")
    print("  " + "-" * 74)
    print(f"  k_l = 1/(4 pi) = {k_l:.8f}   Vol(S^2) = {lepton['vol_s2']:.6f} (= 4 pi)")
    print(f"  Schur flatness |A - I/2| = {lepton['schur_flatness']:.2e}  (uniform average = I/2)")
    print()
    print("  The pi diagnostic: finite average RATIONAL, sphere average has pi")
    print("  " + "-" * 74)
    print(f"  finite Q8 average of |v><v| = {fin_avg.tolist()}")
    print(f"  |Q8 avg - I/2| = {fin_dev:.2e}  -> EXACTLY I/2 (rational, no pi)")
    for name, val in (("k_u", k_u), ("k_d", k_d), ("k_l", k_l)):
        fr, err, is_rat = rationality(val)
        tag = "RATIONAL (discrete)" if is_rat else "NOT rational -> pi-bearing (continuous)"
        print(f"  {name} = {val:.6f}  nearest p/q(<=64) = {str(fr):>6}  err={err:.1e}  {tag}")
    print()
    print("  Discrete extrapolation vs continuum replacement")
    print("  " + "-" * 74)
    print(f"  discrete law at the full Fock module: (Tr I/2)^2 = (8/2)^2 = {(total/2)**2:.0f}")
    print(f"  but the lepton is k_l = 1/(4 pi) = {k_l:.4f}: the colourless CONTINUUM")
    print(f"  replaces the discrete value -- the dichotomy in one line.")
    print()

    checks = {
        "Fock-grade ranks are (1,3,3,1), total 8": ranks == [1, 3, 3, 1] and total == 8,
        "k_u = (Tr P_0/2)^2 = 1/4 exactly": abs(k_u - 0.25) < TOL,
        "k_d = (Tr P_1/2)^2 = 9/4 exactly": abs(k_d - 2.25) < TOL,
        "k_d = (1/4) N_c^2 (the sector-square rule, N_c = Tr P_1 = 3)":
            abs(k_d - 0.25 * N_COLOR * N_COLOR) < TOL and quark["down_rank_is_N_color"],
        "lepton k_l = 1/(4 pi)": abs(k_l - 1.0 / (4.0 * PI)) < TOL,
        "lepton Vol(S^2) = 4 pi": abs(lepton["vol_s2"] - 4.0 * PI) < 1e-6,
        "lepton uniform average is Schur-flat (I/2)": lepton["schur_flatness"] < FLAT_TOL,
        "finite Q8 average is EXACTLY I/2 (rational, no pi)": fin_dev < TOL,
        "k_u, k_d are exact rationals; k_l = 1/(4 pi) is not":
            rationality(k_u)[2] and rationality(k_d)[2] and not rationality(k_l)[2],
    }
    width = max(len(k) for k in checks)
    for name, ok_ in checks.items():
        print(f"  [{'PASS' if ok_ else 'FAIL'}] {name:<{width}}")
    ok = all(checks.values())
    print()
    print("  AUDIT STATUS:", "PASS" if ok else "FAIL",
          "- pi <=> continuous (colourless) ; rational <=> discrete (coloured).")
    print("  BRIDGE STATUS: the M9/M10/M11 shape factors share ONE discriminant")
    print("                 (continuous-sphere/pi for the colour-singlet lepton vs")
    print("                 discrete-Fock-grade/rational for the coloured quarks),")
    print("                 and k_u, k_d = (Tr P_grade/2)^2 are the derived Fock")
    print("                 ranks. STILL OPEN: deriving the colour-singlet ->")
    print("                 continuous selection from CHO dynamics. F0 NOT promoted.")
    print()

    # Stable arithmetic theorems (regression guards):
    assert ranks == [1, 3, 3, 1] and total == 8
    assert abs(k_u - 0.25) < TOL
    assert abs(k_d - 2.25) < TOL
    assert abs(k_d - 0.25 * N_COLOR * N_COLOR) < TOL
    assert quark["down_rank_is_N_color"]
    assert abs(k_l - 1.0 / (4.0 * PI)) < TOL
    assert abs(lepton["vol_s2"] - 4.0 * PI) < 1e-6
    assert lepton["schur_flatness"] < FLAT_TOL
    assert fin_dev < TOL
    assert rationality(k_u)[2] and rationality(k_d)[2]
    assert not rationality(k_l)[2]
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
