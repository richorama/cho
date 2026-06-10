"""Second-wave probe: exceptional harmonic-analysis route.

This checks whether the rank-one symmetric-space data of OP2 naturally contain
enough information for pi/432. The cheap answer: they contain the OP2/pi side,
but not the J3(O) 27 or the seed spectrum by themselves.
"""

from __future__ import annotations


ROOT_MULT_ALPHA = 8
ROOT_MULT_2ALPHA = 7
RANK = 1
OP2_DIM = ROOT_MULT_ALPHA + ROOT_MULT_2ALPHA + RANK
RHO = (ROOT_MULT_ALPHA + 2 * ROOT_MULT_2ALPHA) // 2


def main() -> bool:
    print("[A] Compact rank-one OP2 data")
    print(f"  root multiplicities       : m_alpha={ROOT_MULT_ALPHA}, m_2alpha={ROOT_MULT_2ALPHA}")
    print(f"  dimension check           : {ROOT_MULT_ALPHA}+{ROOT_MULT_2ALPHA}+1 = {OP2_DIM}")
    print(f"  rho                       : (m_alpha + 2*m_2alpha)/2 = {RHO}")

    print("\n[B] Cheap gate")
    print("  OP2 harmonic analysis naturally sees the 16-dimensional rank-one")
    print("  geometry and can carry pi through volumes/kernels. It does not by")
    print("  itself see the 27-dimensional J3(O) carrier or the F4-breaking seed.")

    print("\n[C] Required next theorem")
    print("  Couple the OP2 spherical transform to the E6/J3(O) carrier and prove")
    print("  a canonical lowest mode or Plancherel residue selects the seed. Without")
    print("  that coupling, this route is a form-only route.")

    print("\n[V] Sandbox verdict")
    print("  OP2 harmonic data: PASS")
    print("  full pi/432 action: OPEN, lower priority")

    assert OP2_DIM == 16
    assert RHO == 11
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
