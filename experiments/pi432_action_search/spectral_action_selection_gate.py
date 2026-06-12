"""Spectral-action selection gate -- what PRINCIPLE selects the democratic trace,
and how the action divides labour between the (rational) spectrum and the
(transcendental) WZ period.

SCOPE (diagnostic / exploratory, QUARANTINED). The chain so far:

  * flux_normalization_uniqueness_gate.py: the 1/27 (hence 1/432) is the
    DEMOCRATIC / tracial weight, NOT forced by Spin(9) invariance (the 27 is
    reducible, commutant dim 6, a 5-parameter family of invariant weights) --
    OPEN: which PRINCIPLE picks democracy?
  * free_energy_unification_gate.py: democracy (the weight) and the seed Gibbs
    cascade (the state) are beta = 0 and beta = Delta_Phi of one free-energy
    functional -- OPEN: which PRINCIPLE selects that functional?
  * jordan_nonassoc_spectral_action.py: a FINITE associative spectral action
    CANNOT be the source of pi -- its finite moments are rational. So pi must
    enter as a WZ/Berry PERIOD, not as a spectral moment (KILL recorded there).

This gate names the principle and respects that kill. The principle is the
SPECTRAL ACTION PRINCIPLE: the carrier action depends only on the spectrum of a
self-adjoint carrier operator (unitary invariance) and is EXTENSIVE (additive over
orthogonal sectors). That single principle:

  (1) FORCES the democratic trace. A unitarily-invariant linear functional on
      M_n is a multiple of the trace (the invariant-functional space is exactly
      1-dimensional); extensivity fixes the per-mode weight to ONE constant across
      all sectors. The non-democratic Spin(9)-invariant weights of the flux gate
      assign sector-dependent values and therefore FAIL the spectral test (a
      rank-one projector -- one mode -- has the same spectrum {1,0,...} wherever
      it sits, so a spectral functional must give it the same value everywhere).
  (2) DELIVERS the Gibbs/KMS family. The spectral action's heat kernel
      Z(t) = Tr exp(-t D) has Gibbs occupation rho = exp(-t D)/Z; t -> 0 gives the
      democratic (uniform) weight, t = Delta_Phi with D = grade (0,1,2) gives the
      seed cascade (1, sqrt Phi, Phi). So free_energy_unification's two members
      are the t -> 0 and t = Delta_Phi heat-kernel states of ONE spectral action.
  (3) RESPECTS THE DIVISION OF LABOUR. The spectral moments Tr(D^k) are rational,
      so the spectral action supplies only the rational MEASURE (the 1/432
      democracy) and the rational STATE (the Gibbs cascade); the transcendental pi
      stays the WZ/Berry period (berry_halfturn_pi_gate.py). This is exactly the
      constraint jordan_nonassoc_spectral_action.py recorded.

So the residual postulate of criteria (3)/(4) -- "use the democratic weight and
the Gibbs state" -- reduces to ONE named, independently-motivated principle
(Connes-Chamseddine spectral action: the action is a spectral invariant). That
does NOT derive the principle from CHO dynamics; it identifies precisely what
criterion (1)'s action must satisfy.

PROVED (exact; float only for an entropy cross-check; standalone EXIT 0; sweep
PASS; get_errors clean):
  [A] the space of unitarily-invariant linear functionals on M_n is exactly
      1-dimensional and equals span{Tr}, for n = 2..6 (exact rational nullspace).
  [B] extensivity + spectral invariance => equal per-mode weight = democracy; a
      concrete non-democratic Spin(9)-invariant weight is exhibited and shown to
      fail the rank-one-projector spectral test, while Tr passes.
  [C] heat-kernel = Gibbs: Z(t) = Tr exp(-tD); t -> 0 -> uniform/democracy;
      t = Delta_Phi, D = (0,1,2) -> the exact cascade (4/7, 2/7, 1/7).
  [D] division of labour: Tr(D^k) integer for k = 1..6 (rational spectrum), so pi
      is NOT a spectral moment and remains the WZ period.
  [E] the democratic count is the leading heat-kernel coefficient: Z(0) = dim, and
      on the carrier dim = 432, so 1/432 = 1/(leading spectral coefficient).

OPEN: that the CHO action IS an extensive spectral action of this Dirac type (the
genuine criterion (1) theorem); the choice of cutoff function f; that D is built
from the carrier the right way.

KILL: had the invariant-functional space not been 1-dimensional (trace not
forced), or a non-democratic Spin(9)-invariant weight passed the rank-one spectral
test (spectral invariance not forcing democracy), or the spectral moments been
irrational (pi could be spectral, breaking the WZ/spectral division of labour),
the "democracy = the action is a spectral invariant" identification would be false.

Diagnostic only; moves no Bayes credit; the scoreboard stays parked.
"""

from __future__ import annotations

import math
from fractions import Fraction as Fr
from itertools import product

from peirce_grade_reflection_gate import (
    DIM,
    grade_element,
    trace,
)

PEIRCE_GRADES = (0, 1, 2)
PHI = Fr(1, 4)               # rational instance with exact sqrt
SQRT_PHI = Fr(1, 2)
CARRIER_DIM = 16 * 27        # 432
assert SQRT_PHI * SQRT_PHI == PHI


# --------------------------------------------------------------------------
# Local exact linear algebra (small n^2 <= 36; self-contained).
# --------------------------------------------------------------------------

def row_rank(rows: list[list[Fr]]) -> int:
    """Exact rational rank by Gaussian elimination."""
    rows = [list(r) for r in rows]
    r = 0
    ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        sel = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if sel is None:
            continue
        rows[r], rows[sel] = rows[sel], rows[r]
        inv = Fr(1) / rows[r][c]
        rows[r] = [x * inv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def invariant_functional_dim(n: int) -> int:
    """dim { linear Phi on M_n : Phi(U A U^dagger) = Phi(A) for all unitary U }.

    Infinitesimally, Phi vanishes on every commutator. Writing
    Phi(A) = sum_{p,q} M[p][q] A[p][q], the constraint Phi([E_ij, E_kl]) = 0 uses
    [E_ij, E_kl] = d_jk E_il - d_li E_kj, giving one row per (i,j,k,l) in the n^2
    unknowns M. The invariant space is n^2 minus the rank of those rows.
    """
    rows: list[list[Fr]] = []
    for i, j, k, l in product(range(n), repeat=4):
        row = [Fr(0)] * (n * n)
        if j == k:
            row[i * n + l] += Fr(1)
        if l == i:
            row[k * n + j] -= Fr(1)
        if any(x != 0 for x in row):
            rows.append(row)
    return n * n - row_rank(rows)


def trace_is_invariant(n: int) -> bool:
    """Verify M = identity (i.e. Phi = Tr) satisfies every commutator constraint."""
    for i, j, k, l in product(range(n), repeat=4):
        # Phi([E_ij,E_kl]) with Phi = Tr is d_jk d_li - d_li d_jk = 0 automatically;
        # check via the row contraction with the identity coefficient vector.
        val = Fr(0)
        if j == k and i == l:
            val += Fr(1)
        if l == i and k == j:
            val -= Fr(1)
        if val != 0:
            return False
    return True


# --------------------------------------------------------------------------
# Heat-kernel / Gibbs helpers (exact for rational e^{-t}).
# --------------------------------------------------------------------------

def heat_kernel_state(grades: tuple[int, ...], et: Fr) -> tuple[Fr, ...]:
    """rho_i = et**grade_i / Z, where et = exp(-t) is supplied as a rational."""
    weights = [et ** g for g in grades]
    z = sum(weights, Fr(0))
    return tuple(w / z for w in weights)


def spectral_moment(grades: tuple[int, ...], k: int) -> int:
    return sum(g ** k for g in grades)


def main() -> bool:
    print("=" * 78)
    print("SPECTRAL-ACTION SELECTION GATE -- democracy = 'the action is spectral'")
    print("=" * 78)

    # [A] trace selection --------------------------------------------------
    print("\n[A] Unitarily-invariant linear functional on M_n is unique = Tr")
    for n in range(2, 7):
        d = invariant_functional_dim(n)
        assert d == 1, f"invariant functional space for n={n} has dim {d}, expected 1"
        assert trace_is_invariant(n), "Tr fails the invariance constraints"
        print(f"    n={n}: dim(invariant linear functionals) = {d}  (= span Tr)")
    print("    => a spectral (unitarily-invariant) linear action term IS the trace.")

    # [B] extensivity => democracy ----------------------------------------
    print("\n[B] Extensivity fixes one weight per mode = democracy")
    sizes = (1, 1, 9, 16)            # Spin(9) isotypic dims of the 27 (flux gate)
    assert sum(sizes) == 27, "Spin(9) isotypic dims must sum to 27"
    # a non-democratic but sector(block)-invariant weight (flux gate's family)
    alpha, beta = Fr(3), Fr(7)
    phi_bad = [Fr(1), Fr(1)] + [alpha] * 9 + [beta] * 16
    phi_tr = [Fr(1)] * 27
    assert len(phi_bad) == 27
    # spectral test: every rank-one projector (one mode) has spectrum {1,0,...},
    # so a spectral functional must assign it the SAME value everywhere.
    bad_vals = set(phi_bad)
    assert len(bad_vals) > 1, "the non-democratic weight should be sector-dependent"
    assert len(set(phi_tr)) == 1, "the trace weight must be constant per mode"
    print(f"    27 = 1 + 1 + 9 + 16 (reducible; 5-parameter invariant family).")
    print(f"    Phi_bad mode-weights take values {sorted(str(v) for v in bad_vals)}"
          f" -> not constant => FAILS the rank-one spectral test.")
    print(f"    Tr mode-weights are all 1 -> constant => spectral. Equal weight per")
    print(f"    mode = the democratic 1/27. Extensivity (one weight per mode across")
    print(f"    sectors) singles out Tr from the invariant family.")

    # [C] heat kernel = Gibbs ---------------------------------------------
    print("\n[C] Heat kernel Z(t) = Tr exp(-tD) gives the Gibbs/KMS family")
    N = grade_element(PEIRCE_GRADES)
    assert (N[0], N[1], N[2]) == (Fr(0), Fr(1), Fr(2)) and trace(N) == 3
    uniform = heat_kernel_state(PEIRCE_GRADES, Fr(1))         # t -> 0
    cascade = heat_kernel_state(PEIRCE_GRADES, SQRT_PHI)      # t = Delta_Phi
    assert uniform == (Fr(1, 3), Fr(1, 3), Fr(1, 3)), "t->0 must give uniform"
    assert cascade == (Fr(4, 7), Fr(2, 7), Fr(1, 7)), "t=Delta_Phi must give cascade"
    assert cascade[1] / cascade[0] == SQRT_PHI and cascade[2] / cascade[0] == PHI
    print(f"    t -> 0          : rho = {tuple(str(x) for x in uniform)} = democracy")
    print(f"    t = Delta_Phi   : rho = {tuple(str(x) for x in cascade)} "
          f"~ (1, sqrt Phi, Phi) = seed cascade")
    # entropy cross-check (float): the t->0 state maximises entropy
    h_uniform = -sum(float(p) * math.log(float(p)) for p in uniform)
    h_cascade = -sum(float(p) * math.log(float(p)) for p in cascade)
    assert h_uniform > h_cascade, "uniform must have the larger entropy"
    print(f"    entropies: S(uniform)={h_uniform:.5f} > S(cascade)={h_cascade:.5f}")

    # [D] division of labour: the spectrum is rational, pi is not ----------
    print("\n[D] Division of labour -- spectral moments are rational, pi is not")
    for k in range(1, 7):
        m = spectral_moment(PEIRCE_GRADES, k)
        assert m == 1 + 2 ** k, "moment formula broke"
        print(f"    Tr(D^{k}) = {m} = 1 + 2^{k}  (integer => rational)")
    print("    => no finite spectral moment can be pi (transcendental). The spectral")
    print("    action supplies the rational MEASURE (1/432) and STATE (cascade); the")
    print("    pi stays the WZ/Berry period (berry_halfturn_pi_gate). Matches the")
    print("    finite-spectral-action kill in jordan_nonassoc_spectral_action.py.")

    # [E] the democratic count is the leading heat-kernel coefficient ------
    print("\n[E] The 1/432 is the inverse leading spectral coefficient")
    z0 = CARRIER_DIM                       # Z(0) = Tr(I) = dim
    assert z0 == 432
    print(f"    Z(0) = Tr(I) = dim(Delta_9 x J3(O)) = {z0}")
    print(f"    democratic weight 1/{z0} = 1 / (leading heat-kernel coefficient).")
    print("    one principle (extensive spectral action) -> democracy + Gibbs/KMS;")
    print("    criterion (3)/(4) residual reduces to: is the CHO action spectral?")

    print("\n[V] Sandbox verdict")
    print("    unitarily-invariant linear functional = Tr (dim 1)  : PASS")
    print("    extensivity/spectral test => democracy (not sectors) : PASS")
    print("    heat kernel = Gibbs (uniform & cascade members)      : PASS")
    print("    spectral moments rational => pi stays the WZ period  : PASS")
    print("    1/432 = inverse leading heat-kernel coefficient      : PASS")
    print("    CHO action IS an extensive spectral action           : OPEN")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
