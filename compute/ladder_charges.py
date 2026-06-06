"""
Lever C — electric charges from a number operator (the hypercharge filter).
===========================================================================

The stringent test of any "Standard Model from an algebra" claim is NOT getting
the gauge GROUP (many groups appear); it is reproducing the bizarre fractional
HYPERCHARGES of one generation. Reproducing {0, 1/3, 2/3, 1} with the right
multiplicities is the filter that kills most candidates.

Furey (2014-2018) and Dubois-Violette/Todorov show that in C (x) O the SU(3) of
colour appears as the subgroup of G2 = Aut(O) fixing a complex structure, and
the ELECTRIC CHARGE is, up to a factor 1/3, the number operator of three
fermionic ladder operators built from the octonionic units:

    alpha_k  (k = 1,2,3),    {alpha_i, alpha_j^dag} = delta_ij,   alpha_i^2 = 0

    Q = (1/3) (alpha_1^dag alpha_1 + alpha_2^dag alpha_2 + alpha_3^dag alpha_3).

Acting on the 8-complex-dimensional ideal C (x) O, Q has eigenvalues

    0   (x1)   ->  neutrino / antineutrino   (colour singlet, Q = 0)
    1/3 (x3)   ->  down-type      (colour triplet,  Q = 1/3)
    2/3 (x3)   ->  up-type        (colour triplet,  Q = 2/3)
    1   (x1)   ->  charged lepton (colour singlet,  Q = 1)

i.e. ONE generation of one chirality, with the SM charges and colour
multiplicities falling out of the number operator -- charge quantisation as a
consequence of the algebra, not an input.

What this module does (no charges put in by hand)
-------------------------------------------------
It builds the ladder operators by LEFT-multiplication from this repo's octonion
table, SEARCHES for a Witt basis (three nilpotent, mutually anticommuting
alpha_k with {alpha_i, alpha_j^dag} = delta_ij) compatible with the table, then
forms Q and reads off its eigenvalues. The charges are whatever the number
operator gives; we then check them against {0,1/3,2/3,1} with multiplicities
(1,3,3,1).

No scipy. Uses octonion_toolkit.OCT_MULT and numpy.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/ladder_charges.py
"""

import itertools

import numpy as np

from octonion_toolkit import OCT_MULT


def left_mult_matrix(i):
    """8x8 real matrix of x -> e_i * x."""
    L = np.zeros((8, 8))
    for j in range(8):
        for k in range(8):
            L[k, j] = OCT_MULT[i, j, k]
    return L


L = [left_mult_matrix(i).astype(np.complex128) for i in range(8)]  # L[0]=I


def ladder_from_pairs(pairs, signs):
    """Build three operators alpha_k = (1/2)(s_a L[a] + i L[b]) for (a,b)=pairs[k].

    Left-multiplication realisation of the Witt (raising/lowering) basis. The
    sign s_a in {+1,-1} flips the real part to hit the nilpotent convention.
    """
    alphas = []
    for (a, b), s in zip(pairs, signs):
        alphas.append(0.5 * (s * L[a] + 1j * L[b]))
    return alphas


def anticomm(A, B):
    return A @ B + B @ A


def is_witt_basis(alphas, tol=1e-9):
    """Check nilpotency, mutual anticommutation, and {a_i,a_j^dag}=delta_ij."""
    I = np.eye(8, dtype=np.complex128)
    for a in alphas:
        if np.max(np.abs(a @ a)) > tol:           # alpha^2 = 0
            return False
    for i in range(3):
        for j in range(3):
            ad = alphas[j].conj().T
            ac = anticomm(alphas[i], ad)
            target = I if i == j else np.zeros((8, 8), dtype=np.complex128)
            if np.max(np.abs(ac - target)) > tol:
                return False
    for i in range(3):
        for j in range(i + 1, 3):
            if np.max(np.abs(anticomm(alphas[i], alphas[j]))) > tol:
                return False
    return True


def search_witt_basis():
    """Search index pairings + signs for a valid Witt basis of left-mults.

    The colour SU(3) inside G2 fixes one imaginary direction; the other six
    pair into three ladder operators. We search over disjoint pairings of the
    seven imaginary units (leaving one fixed) and real-part signs.
    """
    units = list(range(1, 8))
    for fixed in units:
        rest = [u for u in units if u != fixed]
        # all ways to split 6 units into 3 unordered disjoint pairs
        for p in _three_pairs(rest):
            for signs in itertools.product((+1, -1), repeat=3):
                alphas = ladder_from_pairs(p, signs)
                if is_witt_basis(alphas):
                    return fixed, p, signs, alphas
    return None, None, None, None


def _three_pairs(items):
    """Yield all partitions of a 6-element list into three unordered pairs."""
    if not items:
        yield []
        return
    first = items[0]
    for i in range(1, len(items)):
        pair = (first, items[i])
        rest = items[1:i] + items[i + 1:]
        for sub in _three_pairs(rest):
            yield [pair] + sub


def charge_operator(alphas):
    """Q = (1/3) sum_k alpha_k^dag alpha_k."""
    Q = np.zeros((8, 8), dtype=np.complex128)
    for a in alphas:
        Q += a.conj().T @ a
    return Q / 3.0


def main():
    print("=" * 78)
    print("  LEVER C — ELECTRIC CHARGE FROM A NUMBER OPERATOR")
    print("  The hypercharge filter: does C (x) O give {0, 1/3, 2/3, 1}?")
    print("=" * 78)

    fixed, pairs, signs, alphas = search_witt_basis()

    if alphas is None:
        print("\n  No exact Witt basis of pure left-multiplications was found for")
        print("  this octonion table by the (pair, sign) search. The left-action")
        print("  realisation is convention-sensitive; the result is reported as")
        print("  inconclusive rather than forced. (The Furey/Dubois-Violette")
        print("  charge result is established in the literature for a compatible")
        print("  basis; this module could not reproduce it purely numerically here.)")
        print()
        return

    print(f"\n  Found a valid Witt basis (left-multiplication realisation):")
    print(f"      fixed colour direction  e{fixed}")
    for k, ((a, b), s) in enumerate(zip(pairs, signs), 1):
        sgn = "+" if s > 0 else "-"
        print(f"      alpha_{k} = 1/2 ( {sgn}L[e{a}] + i L[e{b}] )")
    print("      checks: alpha^2 = 0, {alpha_i, alpha_j^dag} = delta_ij,")
    print("              {alpha_i, alpha_j} = 0   -> all PASS")

    Q = charge_operator(alphas)
    # Q is Hermitian; eigenvalues are the electric charges on C^8.
    eig = np.linalg.eigvalsh((Q + Q.conj().T) / 2.0)
    eig = np.round(eig, 6)

    # Tally multiplicities.
    vals, counts = np.unique(np.round(eig, 3), return_counts=True)
    print("\n  Electric-charge spectrum of Q = (1/3) sum alpha_k^dag alpha_k:")
    print(f"      eigenvalues : {', '.join(f'{v:+.3f}' for v in eig)}")
    print("      multiplicities:")
    for v, c in zip(vals, counts):
        print(f"        Q = {v:+.3f}  x {c}")

    # Compare to the SM one-generation pattern {0(x1), 1/3(x3), 2/3(x3), 1(x1)}.
    target = {0.0: 1, 1 / 3: 3, 2 / 3: 3, 1.0: 1}
    got = {round(float(v), 3): int(c) for v, c in zip(vals, counts)}
    # Allow an overall sign convention (particle vs antiparticle ideal).
    got_abs = {}
    for v, c in got.items():
        got_abs[abs(v)] = got_abs.get(abs(v), 0) + c
    target_round = {round(k, 3): v for k, v in target.items()}
    match = all(
        got_abs.get(round(k, 3), 0) == v for k, v in target_round.items()
    ) and sum(got_abs.values()) == 8

    print("\n  " + "-" * 74)
    print("  RESULT")
    if match:
        print("   * The number operator reproduces the SM one-generation charges")
        print("     {0, 1/3, 2/3, 1} with multiplicities (1, 3, 3, 1) -- a colour")
        print("     singlet (neutrino), a triplet (down-type, 1/3), a triplet")
        print("     (up-type, 2/3) and a singlet (charged lepton, 1).")
        print("   * Charge QUANTISATION in thirds and the correct colour multiplets")
        print("     are OUTPUTS of the octonionic algebra, not inputs. This is the")
        print("     stringent hypercharge filter that most 'SM from X' attempts fail,")
        print("     here passed for C (x) O (Furey / Dubois-Violette).")
    else:
        print("   * The spectrum did NOT match {0,1/3,2/3,1} x (1,3,3,1) on this")
        print("     construction; reported honestly. The charge result is basis-")
        print("     dependent and this particular left-multiplication realisation")
        print("     did not reproduce it.")

    print("\n  SCOPE / KILL CONDITION (recorded)")
    print("   * This gives ONE generation, ONE chirality, and the ELECTRIC charge")
    print("     (= number operator). The full hypercharge Y and weak isospin still")
    print("     require the C (x) H factor (SU(2) from the quaternions); that")
    print("     embedding is the next derivation target.")
    print("   * KILL: if extending to the C (x) H (x) O whole algebra forces extra")
    print("     unwanted charged states (the usual GUT problem) or spoils the")
    print("     (1,3,3,1) pattern, the clean embedding claim fails.")
    print()


if __name__ == "__main__":
    main()
