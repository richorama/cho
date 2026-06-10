"""Second-wave probe: adelic variational-principle route.

The prior adelic route was only pattern recognition. This probe asks what would
be needed for a real adelic action: the real place must supply pi, finite places
must supply 2^4*3^3, and a product/action principle must force the combination.
"""

from __future__ import annotations

from collections import Counter


TARGET = 432


def prime_factors(n: int) -> Counter[int]:
    factors: Counter[int] = Counter()
    candidate = 2
    while candidate * candidate <= n:
        while n % candidate == 0:
            factors[candidate] += 1
            n //= candidate
        candidate += 1
    if n > 1:
        factors[n] += 1
    return factors


def main() -> bool:
    factors = prime_factors(TARGET)
    support = tuple(sorted(factors))
    print("[A] Finite-place target")
    print(f"  432 factors : {dict(factors)}")
    print(f"  support     : {support}")
    print("  reading     : 2^4 from quaternion/doubling side, 3^3 from triality/rank-3 side")

    print("\n[B] Real-place target")
    print("  archimedean period must supply pi, not a rational spectral moment")

    print("\n[C] Required next theorem")
    print("  Define an adelic action whose Euler product or product formula gives")
    print("  real period pi times finite measure 1/(2^4*3^3). The old prime-pattern")
    print("  observation is not enough; this needs a variational principle and a seed")
    print("  spectrum.")

    print("\n[V] Sandbox verdict")
    print("  arithmetic support: PASS")
    print("  adelic action: OPEN")

    assert TARGET == 2**4 * 3**3
    assert support == (2, 3)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
