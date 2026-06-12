"""Free-energy unification gate -- the democratic flux weight and the seed Gibbs
cascade are ONE principle, at two temperatures.

SCOPE (diagnostic / exploratory, QUARANTINED). Three earlier gates left, between
them, TWO apparently-independent "principle-selection" assumptions still open:

  * flux_normalization_uniqueness_gate.py: the WZ flux is averaged with the
    DEMOCRATIC (tracial / maximally-mixed) weight 1/432 -- OPEN: why democracy?
  * seed_spectrum_reduction_gate.py + candidate_wz_jordan_entropy_action.py: the
    seed spectrum is the GIBBS / max-entropy state rho ~ (1, sqrt Phi, Phi)
    -- OPEN: why Gibbs?

This gate shows those are the SAME principle. Both are members of the single
free-energy family

        F_beta(rho) = Tr(rho log rho) + beta * Tr(rho N),   Tr rho = 1,

minimised over states, with N the Peirce-grade Hamiltonian (the genuine grade
element of J3(O), imported from the sibling). The unique minimiser is the Gibbs
state rho*_i proportional to exp(-beta N_i):

  * beta = 0 (infinite temperature, no grade constraint): rho* = uniform = the
    DEMOCRATIC / tracial state -> the 1/n weight of the flux gate.
  * beta = Delta_Phi = -1/2 log Phi, N = (0,1,2): rho* = the CASCADE
    (1, sqrt Phi, Phi) -> the seed spectrum.

So "democracy" and "Gibbs cascade" are the beta = 0 and beta = Delta_Phi members
of ONE variational principle (maximum entropy at a prescribed mean grade). The
two open postulates collapse to one.

The democratic member is moreover singled out intrinsically: it is the UNIQUE
state with trivial modular flow. A state omega(x) = Tr(rho x) is tracial iff rho
is central iff rho ~ I, and then the modular automorphism sigma_t(x) =
rho^{i t} x rho^{-i t} = x is trivial. So democracy = "the no-grade member has no
intrinsic dynamics", while the cascade is the genuine KMS / modular state of the
grade flow at inverse temperature Delta_Phi.

HONESTY NOTE. This unifies the flux gate's *democracy* (its 1/27 = tracial 27)
with the seed *Gibbs* law. It does NOT touch the flux gate's 1/16, which is forced
by Spin(9) IRREDUCIBILITY (Schur), a distinct symmetry input -- we deliberately do
not conflate the Schur weight with this max-entropy story.

PROVED (exact; float only for the entropy cross-checks; standalone EXIT 0; sweep
PASS; get_errors clean):
  [A] unique Gibbs minimiser, via the exact identity F_beta(rho) - F_beta(rho*) =
      D(rho || rho*) >= 0 (Gibbs' inequality), checked on rational competitors.
  [B] beta = 0 member = uniform = the democratic / tracial weight 1/n.
  [C] beta = Delta_Phi, N = (0,1,2), rational instance Phi = 1/4: minimiser =
      (4/7, 2/7, 1/7) proportional to (1, sqrt Phi, Phi); exact stationarity via
      rho_i * (sqrt Phi)^{-grade_i} = const. N is the real J3(O) grade element.
  [D] modular characterisation: the democratic state is the unique central state
      (rho ~ I, [rho, x] = 0 for all x) => trivial modular flow; the cascade is
      non-central (explicit non-vanishing commutator) => nontrivial KMS flow.
  [E] synthesis: flux-democracy and seed-Gibbs are beta = 0 and beta = Delta_Phi
      of one free-energy principle; two open postulates -> one.

OPEN: that CHO dynamics SELECTS this max-entropy / KMS principle (the action's
job, criterion (1)). Reducing two postulates to one is not deriving the postulate
from a microscopic action.

KILL: had the beta = 0 minimiser not been the democratic uniform state, or the
beta = Delta_Phi minimiser not been the seed cascade, or the democratic state not
been the unique central (trivial-modular-flow) one, the unification would be false.

Diagnostic only; moves no Bayes credit; the scoreboard stays parked.
"""

from __future__ import annotations

import math
from fractions import Fraction as Fr

from peirce_grade_reflection_gate import (
    DIM,
    grade_element,
    trace,
)

PEIRCE_GRADES = (0, 1, 2)
PHI = Fr(1, 4)               # rational instance: a perfect-square flux so sqrt is exact
SQRT_PHI = Fr(1, 2)          # sqrt(1/4); the Gibbs ratio r = exp(-Delta_Phi) = sqrt(Phi)
assert SQRT_PHI * SQRT_PHI == PHI


# --------------------------------------------------------------------------
# States and the free-energy functional.
# --------------------------------------------------------------------------

def gibbs_state(grades: tuple[int, ...], ratio: Fr) -> tuple[Fr, ...]:
    """Exact Gibbs state rho_i proportional to ratio**grade_i (ratio rational)."""
    weights = [ratio ** g for g in grades]
    z = sum(weights, Fr(0))
    return tuple(w / z for w in weights)


def uniform_state(n: int) -> tuple[Fr, ...]:
    return tuple(Fr(1, n) for _ in range(n))


def free_energy(rho: tuple[Fr, ...], grades: tuple[int, ...], beta: float) -> float:
    """F_beta(rho) = sum rho_i ln rho_i + beta sum rho_i grade_i  (float)."""
    s = 0.0
    for p, g in zip(rho, grades):
        pf = float(p)
        s += pf * math.log(pf) + beta * pf * g
    return s


def rel_entropy(p: tuple[Fr, ...], q: tuple[Fr, ...]) -> float:
    """D(p || q) = sum p_i ln(p_i / q_i)  (float)."""
    return sum(float(pi) * math.log(float(pi) / float(qi)) for pi, qi in zip(p, q))


# --------------------------------------------------------------------------
# 3x3 matrix helpers (exact) for the modular-flow characterisation.
# --------------------------------------------------------------------------

def diag(p: tuple[Fr, ...]) -> list[list[Fr]]:
    n = len(p)
    return [[p[i] if i == j else Fr(0) for j in range(n)] for i in range(n)]


def commutator3(A: list[list[Fr]], B: list[list[Fr]]) -> list[list[Fr]]:
    n = len(A)
    AB = [[sum((A[i][k] * B[k][j] for k in range(n)), Fr(0)) for j in range(n)]
          for i in range(n)]
    BA = [[sum((B[i][k] * A[k][j] for k in range(n)), Fr(0)) for j in range(n)]
          for i in range(n)]
    return [[AB[i][j] - BA[i][j] for j in range(n)] for i in range(n)]


def is_zero(M: list[list[Fr]]) -> bool:
    return all(x == 0 for row in M for x in row)


def main() -> bool:
    print("=" * 78)
    print("FREE-ENERGY UNIFICATION GATE -- democracy and Gibbs are one principle")
    print("=" * 78)

    beta_phi = -0.5 * math.log(float(PHI))     # Delta_Phi = -1/2 log Phi

    # [A] unique Gibbs minimiser ------------------------------------------
    print("\n[A] One functional  F_beta(rho) = Tr(rho log rho) + beta Tr(rho N)")
    rho_star = gibbs_state(PEIRCE_GRADES, SQRT_PHI)
    competitors = [
        uniform_state(3),
        (Fr(2, 5), Fr(2, 5), Fr(1, 5)),
        (Fr(1, 2), Fr(1, 4), Fr(1, 4)),
    ]
    print("    Gibbs' inequality  F_beta(rho) - F_beta(rho*) = D(rho || rho*) >= 0:")
    f_star = free_energy(rho_star, PEIRCE_GRADES, beta_phi)
    for q in competitors:
        lhs = free_energy(q, PEIRCE_GRADES, beta_phi) - f_star
        rhs = rel_entropy(q, rho_star)
        assert abs(lhs - rhs) < 1e-12, "free-energy / relative-entropy identity broke"
        assert lhs > -1e-15, "Gibbs state is not the minimiser"
        print(f"      q={tuple(str(x) for x in q)}: "
              f"DeltaF={lhs:.6f}  D={rhs:.6f}  (equal, >= 0)")
    print("    => the Gibbs state rho*_i ~ exp(-beta N_i) is the UNIQUE minimiser.")

    # [B] beta = 0 member = democracy -------------------------------------
    print("\n[B] beta = 0 member (infinite temperature, no grade constraint)")
    rho0 = gibbs_state(PEIRCE_GRADES, Fr(1))   # ratio exp(0) = 1
    assert rho0 == uniform_state(3), "beta=0 Gibbs state must be uniform"
    f0_star = free_energy(uniform_state(3), PEIRCE_GRADES, 0.0)
    for q in competitors[1:]:
        lhs = free_energy(q, PEIRCE_GRADES, 0.0) - f0_star
        rhs = rel_entropy(q, uniform_state(3))
        assert abs(lhs - rhs) < 1e-12 and lhs > -1e-15
    print(f"    rho*(beta=0) = {tuple(str(x) for x in rho0)} = uniform")
    print("    = the DEMOCRATIC / tracial weight 1/n  (flux_normalization gate's 1/27).")

    # [C] beta = Delta_Phi member = the seed cascade ----------------------
    print("\n[C] beta = Delta_Phi member, N = (0,1,2)  (the real J3(O) grade element)")
    N = grade_element(PEIRCE_GRADES)
    assert (N[0], N[1], N[2]) == (Fr(0), Fr(1), Fr(2)), "N diagonal must be (0,1,2)"
    assert all(N[k] == 0 for k in range(3, DIM)), "grade element must be diagonal"
    assert trace(N) == 3, "Tr N = 0+1+2 = 3"
    cascade = rho_star
    # exact stationarity: rho_i * (sqrt Phi)^{-grade_i} all equal (= 1/Z)
    plateau = {cascade[i] / (SQRT_PHI ** g) for i, g in enumerate(PEIRCE_GRADES)}
    assert len(plateau) == 1, "Gibbs stationarity rho_i ~ (sqrt Phi)^grade broke"
    assert cascade == (Fr(4, 7), Fr(2, 7), Fr(1, 7)), "cascade must be (4/7,2/7,1/7)"
    # the ratios are exactly (1, sqrt Phi, Phi)
    assert cascade[1] / cascade[0] == SQRT_PHI and cascade[2] / cascade[0] == PHI
    print(f"    N diagonal = (0,1,2); Tr N = {trace(N)}")
    print(f"    rho*(Delta_Phi) = {tuple(str(x) for x in cascade)} "
          f"~ (1, sqrt Phi, Phi)  (exact, Phi=1/4)")
    print("    = the seed cascade (seed_spectrum_reduction / candidate action gate).")

    # [D] modular characterisation of democracy ---------------------------
    print("\n[D] Modular flow: democracy = the unique state with trivial dynamics")
    # generating off-diagonal elements of M_3
    gens = []
    for (a, b) in ((0, 1), (1, 2), (0, 2)):
        X = [[Fr(0)] * 3 for _ in range(3)]
        X[a][b] = Fr(1)
        gens.append(X)
    rho_dem = diag(uniform_state(3))
    rho_cas = diag(cascade)
    assert all(is_zero(commutator3(rho_dem, X)) for X in gens), \
        "uniform state must be central (commute with all generators)"
    assert any(not is_zero(commutator3(rho_cas, X)) for X in gens), \
        "cascade must be non-central"
    # modular Hamiltonian K = -log rho is scalar (~ I) iff the rho_i are all equal
    assert len(set(uniform_state(3))) == 1, "democratic K = -log rho must be scalar"
    assert len(set(cascade)) == 3, "cascade K = -log rho must be non-scalar"
    print("    [rho_dem, X] = 0 for all generators X  => central => trivial flow")
    print("    [rho_cas, X] != 0 for some X           => non-central => KMS flow")
    print("    tracial state <=> central rho <=> rho ~ I  (the democratic member).")

    # [E] synthesis -------------------------------------------------------
    print("\n[E] Synthesis")
    print("    flux democracy (1/n)   = beta -> 0      member  (max entropy)")
    print("    seed Gibbs cascade     = beta = Delta_Phi member (grade KMS state)")
    print("    one functional F_beta, one principle: max entropy at fixed mean grade.")
    print("    => two open 'principle' postulates collapse to ONE.")
    print("    (NB the flux gate's 1/16 is Schur/irreducibility, a SEPARATE input.)")

    print("\n[V] Sandbox verdict")
    print("    Gibbs state is the unique free-energy minimiser     : PASS")
    print("    beta=0 member = democratic / tracial weight 1/n     : PASS")
    print("    beta=Delta_Phi member = seed cascade (1,sqrtPhi,Phi): PASS")
    print("    democracy = unique central (trivial-modular) state  : PASS")
    print("    democracy + Gibbs unified into one principle        : PASS")
    print("    CHO dynamics selects that principle (criterion 1)   : OPEN")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
