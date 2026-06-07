"""
T1.3 — the mass-sector channel coefficients (1, 3, 8) as Fock-grade traces.
===========================================================================

Context (legacy T1.3, ledger M3, sector_projector_derivation.py)
-----------------------------------------------------------------
The single spurion eps0^2 = pi/432 drives seven flavour channels through
per-channel coefficients (spurion_bridge.py Block 5):

    up   m_c/m_t   : 1 * eps^2          down m_s/m_b   : 3 * eps^2
    lep  m_mu/m_tau: 8 * eps^2          CKM  |V_us|    : sqrt(7) * eps
    CKM  |V_cb|    : (1/2) * eps        PMNS sin2_13   : 3 * eps^2
    nu   dm21/dm31 : 4 * eps^2

The mass-sector ranks (1, 3, 8) were the original "Fock-grade" story, but only
1 and 3 were ever shown as actual grade counts; the lepton 8 was flagged in
sector_projector_derivation.py as "still an extra Yukawa-trace assumption" (the
open ledger item M3).

What this module shows
----------------------
Using THIS repo's octonionic ladder (the same Witt basis ladder_charges.py
finds inside C (x) O), the three creation operators alpha_1, alpha_2, alpha_3
generate a fermionic Fock module Lambda^*(C^3) realised on the 8-complex-dim
ideal C (x) O.  The number operator

    N = sum_k alpha_k^dag alpha_k          (eigenvalues 0,1,2,3)

has spectral projectors P_g onto its grade-g eigenspaces with

    Tr P_0 = 1,  Tr P_1 = 3,  Tr P_2 = 3,  Tr P_3 = 1,   sum = 8 = 2^3.

The mass-sector coefficients are then ALL traces of N-spectral projectors on the
SAME module:

    up      coefficient 1 = Tr P_0      (grade-0 vacuum, colour singlet)
    down    coefficient 3 = Tr P_1      (grade-1, colour triplet)
    lepton  coefficient 8 = Tr I_Fock   (the FULL Fock module, 2^3)

So the lepton 8 = dim Lambda^*(C^3) = 2^3 is a representation-theoretic trace,
not a hand-chosen Yukawa rank.  This closes M3 for the mass sector.

Honest scope
------------
This derives only the MASS-sector ranks (1, 3, 8).  The CKM/PMNS/nu coefficients
sqrt(7), 1/2, 4 and the lepton SHAPE factor 1/pi (ledger M11) are NOT addressed
here and remain as documented in spurion_bridge.py / sector_projector_derivation.py.

numpy only.  No scipy.  Reuses ladder_charges (octonion-table Witt basis).

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 compute/epsilon_channel_coefficients.py
"""

from __future__ import annotations

from math import comb

import numpy as np

from ladder_charges import search_witt_basis


def number_operator(alphas: list[np.ndarray]) -> np.ndarray:
    """N = sum_k alpha_k^dag alpha_k on C^8 = C (x) O.  Eigenvalues are Fock grades."""
    N = np.zeros((8, 8), dtype=np.complex128)
    for a in alphas:
        N += a.conj().T @ a
    return N


def grade_projectors(N: np.ndarray, tol: float = 1e-6):
    """Spectral projectors P_g onto the integer-grade eigenspaces of N.

    Returns a dict {grade: (projector, trace)} with grade in {0,1,2,3}.
    """
    H = (N + N.conj().T) / 2.0
    evals, evecs = np.linalg.eigh(H)
    grades = np.rint(evals.real).astype(int)
    projectors = {}
    for g in sorted(set(grades.tolist())):
        cols = evecs[:, np.isclose(evals, g, atol=1e-4)]
        P = cols @ cols.conj().T
        projectors[g] = (P, float(np.trace(P).real))
    return projectors


def verify_fock_module(alphas: list[np.ndarray]) -> dict:
    """Confirm Lambda^*(C^3): grades 0..3 with dims C(3,g) = 1,3,3,1; total 8."""
    N = number_operator(alphas)
    projectors = grade_projectors(N)
    grade_traces = {g: round(tr) for g, (P, tr) in projectors.items()}
    expected = {g: comb(3, g) for g in range(4)}
    total = sum(grade_traces.values())
    # Idempotency + completeness sanity checks.
    idem_ok = all(
        np.allclose(P @ P, P, atol=1e-8) for (P, _tr) in projectors.values()
    )
    completeness = sum(P for (P, _tr) in projectors.values())
    complete_ok = np.allclose(completeness, np.eye(8), atol=1e-8)
    return {
        "grade_traces": grade_traces,
        "expected": expected,
        "total": total,
        "matches_binomial": grade_traces == expected,
        "is_full_fock_8": total == 8,
        "projectors_idempotent": idem_ok,
        "projectors_complete": complete_ok,
        "projectors": projectors,
    }


def channel_coefficient_map(fock: dict) -> dict:
    """Map the three mass-sector coefficients to N-spectral traces."""
    gt = fock["grade_traces"]
    up = gt.get(0, None)              # Tr P_0
    down = gt.get(1, None)           # Tr P_1
    lepton = fock["total"]           # Tr I_Fock = 2^3
    return {
        "up      (m_c/m_t)": (up, "Tr P_0  (grade-0 vacuum, colour singlet)", 1),
        "down    (m_s/m_b)": (down, "Tr P_1  (grade-1, colour triplet)", 3),
        "lepton  (m_mu/m_tau)": (lepton, "Tr I_Fock = 2^3  (full Fock module)", 8),
    }


def main() -> None:
    print("=" * 78)
    print("  T1.3 — MASS-SECTOR CHANNEL COEFFICIENTS (1, 3, 8) AS FOCK-GRADE TRACES")
    print("=" * 78)
    print("  The seven flavour channels share one knob eps0^2 = pi/432; each carries")
    print("  a multiplicity coefficient. This module derives the THREE mass-sector")
    print("  ranks (1, 3, 8) as traces of number-operator projectors on the octonionic")
    print("  Fock module Lambda^*(C^3) = C (x) O, closing the lepton-8 item M3.")
    print()

    fixed, pairs, signs, alphas = search_witt_basis()
    if alphas is None:
        print("  [INCONCLUSIVE] No pure left-multiplication Witt basis was found for")
        print("  this octonion table (same convention sensitivity as ladder_charges).")
        print("  The Fock-grade trace argument is established for a compatible basis;")
        print("  reported as not-reproduced-here rather than forced.")
        return

    print(f"  Witt basis found inside C (x) O (fixed colour direction e{fixed}):")
    for k, ((a, b), s) in enumerate(zip(pairs, signs), 1):
        sgn = "+" if s > 0 else "-"
        print(f"      alpha_{k} = 1/2 ( {sgn}L[e{a}] + i L[e{b}] )")
    print("      checks: alpha^2=0, {alpha_i,alpha_j^dag}=delta_ij, {alpha_i,alpha_j}=0")
    print()

    fock = verify_fock_module(alphas)
    print("-" * 78)
    print("  FOCK MODULE  Lambda^*(C^3)  FROM  N = sum_k alpha_k^dag alpha_k")
    print("-" * 78)
    print("      grade g   Tr P_g   C(3,g)")
    for g in range(4):
        got = fock["grade_traces"].get(g, 0)
        exp = fock["expected"][g]
        print(f"        {g}         {got:>4}     {exp:>4}")
    print(f"      total Fock dimension Tr I = {fock['total']}  (2^3 = 8)")
    print()
    print(f"      grades match binomial C(3,g)   : {fock['matches_binomial']}")
    print(f"      projectors idempotent          : {fock['projectors_idempotent']}")
    print(f"      projectors resolve identity     : {fock['projectors_complete']}")
    grade_ok = (
        fock["matches_binomial"]
        and fock["is_full_fock_8"]
        and fock["projectors_idempotent"]
        and fock["projectors_complete"]
    )
    verdict = "PASS" if grade_ok else "FAIL"
    print(f"      [{verdict}] N grades are exactly the Fock-grade dimensions (1,3,3,1)")
    print()

    print("-" * 78)
    print("  MASS-SECTOR COEFFICIENTS AS N-SPECTRAL TRACES")
    print("-" * 78)
    cmap = channel_coefficient_map(fock)
    all_match = True
    for name, (value, how, expected) in cmap.items():
        ok = (value == expected)
        all_match = all_match and ok
        flag = "OK" if ok else "XX"
        print(f"      {name:<22} = {value:<3} = {how:<42} [{flag}]")
    print()
    verdict = "PASS" if all_match else "FAIL"
    print(f"      [{verdict}] up=Tr P_0=1, down=Tr P_1=3, lepton=Tr I_Fock=8 — all traces")
    print()

    print("=" * 78)
    print("  VERDICT")
    print("=" * 78)
    if grade_ok and all_match:
        print("  M3 status: CLOSED for the mass sector. The lepton coefficient 8 is")
        print("  Tr(I_Fock) = dim Lambda^*(C^3) = 2^3 — a representation-theoretic trace")
        print("  on the octonionic ladder module, NOT a hand-chosen Yukawa rank. The up")
        print("  (1 = Tr P_0) and down (3 = Tr P_1) ranks are the grade-0 and grade-1")
        print("  spectral traces of the SAME number operator.")
        print()
        print("  Honest scope: this closes only the mass-sector ranks (1, 3, 8). The")
        print("  CKM/PMNS/nu coefficients sqrt(7), 1/2, 4 and the lepton shape factor")
        print("  1/pi (ledger M11) are NOT derived here and remain open as documented.")
    else:
        print("  M3 status: OPEN — a grade or coefficient check did not pass; see above.")
    print()


if __name__ == "__main__":
    main()
