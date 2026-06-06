"""
Hardness-to-vary / look-elsewhere calculator for the CHO framework.
=====================================================================

A numerical agreement is only evidence if FEW comparably-simple alternatives
would have fit the data equally well. This module makes that quantitative.

Method (choice-independent framing)
-----------------------------------
For each CHO constant or per-row coefficient we:

  1. Enumerate a library of "simple" algebraic numbers built from the SAME
     vocabulary CHO uses: small-integer ratios, optional powers of pi, and
     optional single square roots.
  2. Each candidate gets an explicit description-length complexity (in bits).
  3. We find every candidate that reproduces the measured value within the
     experimental tolerance.
  4. We sort the fitters by complexity and report WHERE the CHO choice ranks.

The robust, tuning-independent claim is the RANK:

  * If the CHO formula is the simplest number that fits, that is strong,
    choice-independent evidence the value is "hard to vary".
  * If many strictly-simpler numbers also fit, the agreement is cheap.

We also report a density (#fitters / #candidates at <= CHO complexity) as a
secondary, range-dependent diagnostic, and a combined look-elsewhere figure.

Nothing here uses any low-energy fit beyond the published CHO formulas; it only
audits how special those formulas are inside their own factor vocabulary.
"""
import math
from fractions import Fraction
from itertools import product

PI = math.pi


# --------------------------------------------------------------------------
# Complexity model
# --------------------------------------------------------------------------
def _bits(n):
    """Description length of a positive integer, in bits."""
    n = abs(int(n))
    return math.log2(n + 1)


C_PI = 3.0      # cost (bits) of including one factor of pi
C_SQRT = 3.0    # cost (bits) of including one square root


def candidate_complexity(num, den, pi_pow, sqrt_rad):
    """Description length (bits) of (num/den) * pi**pi_pow * sqrt(sqrt_rad)."""
    c = _bits(num) + _bits(den)
    c += abs(pi_pow) * C_PI
    if sqrt_rad != 1:
        c += C_SQRT + _bits(sqrt_rad)
    return c


# --------------------------------------------------------------------------
# Library generation
# --------------------------------------------------------------------------
# Integer vocabulary that actually appears in the CHO framework.
INT_VOCAB = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 16, 24, 27, 36, 64, 72, 432]
PI_POWERS = [-2, -1, 0, 1, 2]
SQRT_RADICANDS = [1, 2, 3, 5, 6, 7]


def build_library(max_complexity=None):
    """
    Generate a de-duplicated library of simple algebraic numbers.

    Returns a list of dicts: {value, num, den, pi_pow, sqrt_rad, complexity, repr}.
    Keeps, for each numeric value, only the SIMPLEST representation found.
    """
    best = {}  # rounded value -> entry (simplest)
    for num, den in product(INT_VOCAB, INT_VOCAB):
        frac = Fraction(num, den)
        n, d = frac.numerator, frac.denominator
        for pi_pow in PI_POWERS:
            for rad in SQRT_RADICANDS:
                comp = candidate_complexity(n, d, pi_pow, rad)
                if max_complexity is not None and comp > max_complexity:
                    continue
                val = (n / d) * (PI ** pi_pow) * math.sqrt(rad)
                if val <= 0 or not math.isfinite(val):
                    continue
                key = round(val, 12)
                prev = best.get(key)
                if prev is None or comp < prev["complexity"]:
                    best[key] = {
                        "value": val,
                        "num": n,
                        "den": d,
                        "pi_pow": pi_pow,
                        "sqrt_rad": rad,
                        "complexity": comp,
                        "repr": _fmt(n, d, pi_pow, rad),
                    }
    return sorted(best.values(), key=lambda e: e["complexity"])


def _fmt(num, den, pi_pow, sqrt_rad):
    parts = []
    if den == 1:
        parts.append(f"{num}")
    else:
        parts.append(f"{num}/{den}")
    if pi_pow == 1:
        parts.append("pi")
    elif pi_pow == -1:
        parts.append("/pi")
    elif pi_pow == 2:
        parts.append("pi^2")
    elif pi_pow == -2:
        parts.append("/pi^2")
    if sqrt_rad != 1:
        parts.append(f"sqrt({sqrt_rad})")
    s = " * ".join(p for p in parts if not p.startswith("/"))
    for p in parts:
        if p.startswith("/"):
            s += " " + p
    return s


# --------------------------------------------------------------------------
# Per-target analysis
# --------------------------------------------------------------------------
class Target:
    """A single dimensionless quantity CHO predicts via one chosen constant."""

    def __init__(self, name, measured, rel_tol, cho_value, cho_repr, cho_complexity):
        self.name = name
        self.measured = measured
        self.rel_tol = rel_tol          # fractional half-width counted as a "fit"
        self.cho_value = cho_value
        self.cho_repr = cho_repr
        self.cho_complexity = cho_complexity

    def analyze(self, library):
        # Widen by a hair so a CHO point sitting exactly on the edge counts.
        tol = self.rel_tol * (1 + 1e-6) + 1e-12
        lo = self.measured * (1 - tol)
        hi = self.measured * (1 + tol)
        # Candidates no more complex than the CHO choice.
        pool = [e for e in library if e["complexity"] <= self.cho_complexity + 1e-9]
        fitters = [e for e in pool if lo <= e["value"] <= hi]
        fitters.sort(key=lambda e: (e["complexity"], abs(e["value"] - self.measured)))
        # Rank of the CHO choice among fitters by simplicity.
        cho_rank = None
        for i, e in enumerate(fitters, 1):
            if abs(e["value"] - self.cho_value) <= 1e-9 * max(1.0, abs(self.cho_value)):
                cho_rank = i
                break
        simpler_fitters = [e for e in fitters
                           if e["complexity"] < self.cho_complexity - 1e-9]
        return {
            "pool": len(pool),
            "fitters": fitters,
            "n_fitters": len(fitters),
            "density": len(fitters) / max(1, len(pool)),
            "cho_rank": cho_rank,
            "n_simpler_fitters": len(simpler_fitters),
        }


def build_targets():
    """
    Define the CHO targets in dimensionless 'one chosen constant' form.

    For each we record the measured dimensionless value, a tolerance equal to
    the larger of the experimental relative error and the CHO relative error
    (so any competitor at least as good as CHO counts), and the CHO constant
    with its own complexity from the library model.
    """
    def comp(num, den, pi_pow, rad):
        return candidate_complexity(num, den, pi_pow, rad)

    targets = []

    # Master triality-breaking constant: eps0^2 = pi/432, fixed by m_c/m_t.
    mc, mt = 1.270, 172.76
    eps2_meas = mc / mt
    targets.append(Target(
        "eps0^2  (= m_c/m_t)", eps2_meas,
        rel_tol=max(0.02 / 1.270, abs(PI / 432 - eps2_meas) / eps2_meas),
        cho_value=PI / 432, cho_repr="pi/432", cho_complexity=comp(1, 432, 1, 1)))

    # Top Yukawa coefficient analysed in squared form: (m_t/v)^2 = 1/2.
    v = 246.22
    mt_v2 = (172.76 / v) ** 2
    targets.append(Target(
        "(m_t/v)^2", mt_v2,
        rel_tol=max(2 * 0.30 / 172.76, abs(0.5 - mt_v2) / mt_v2),
        cho_value=0.5, cho_repr="1/2", cho_complexity=comp(1, 2, 0, 1)))

    # Higgs coefficient in squared form: (m_H/v)^2 = pi/12.
    mH_v2 = (125.09 / v) ** 2
    targets.append(Target(
        "(m_H/v)^2", mH_v2,
        rel_tol=max(2 * 0.11 / 125.09, abs(PI / 12 - mH_v2) / mH_v2),
        cho_value=PI / 12, cho_repr="pi/12", cho_complexity=comp(1, 12, 1, 1)))

    # Bottom/tau ratio: m_b/m_tau = 7/3.
    targets.append(Target(
        "m_b / m_tau", 4.18 / 1.777,
        rel_tol=max(0.03 / 4.18, abs(7 / 3 - 4.18 / 1.777) / (4.18 / 1.777)),
        cho_value=7 / 3, cho_repr="7/3", cho_complexity=comp(7, 3, 0, 1)))

    # Strange prefactor over eps0^2*m_b: m_s/(eps0^2 m_b) = 3.
    eps2 = PI / 432
    targets.append(Target(
        "m_s / (eps0^2 m_b)", 0.0934 / (eps2 * 4.18),
        rel_tol=0.03, cho_value=3.0, cho_repr="3 (= N_c)",
        cho_complexity=comp(3, 1, 0, 1)))

    # Muon prefactor: m_mu/(eps0^2 m_tau) = 8.
    targets.append(Target(
        "m_mu / (eps0^2 m_tau)", 0.10566 / (eps2 * 1.777),
        rel_tol=0.03, cho_value=8.0, cho_repr="8 (= dim O)",
        cho_complexity=comp(8, 1, 0, 1)))

    # Cabibbo: |V_us| / eps0 = sqrt(7).
    eps0 = math.sqrt(eps2)
    targets.append(Target(
        "|V_us| / eps0", 0.2243 / eps0,
        rel_tol=max(0.0005 / 0.2243, abs(math.sqrt(7) - 0.2243 / eps0) / (0.2243 / eps0)),
        cho_value=math.sqrt(7), cho_repr="sqrt(7)", cho_complexity=comp(1, 1, 0, 7)))

    # CKM 2-3: |V_cb| / eps0 = 1/2.
    targets.append(Target(
        "|V_cb| / eps0", 0.0422 / eps0,
        rel_tol=max(0.0008 / 0.0422, abs(0.5 - 0.0422 / eps0) / (0.0422 / eps0)),
        cho_value=0.5, cho_repr="1/2", cho_complexity=comp(1, 2, 0, 1)))

    # Atmospheric angle: sin^2 th23 = 4/7.
    targets.append(Target(
        "sin^2 th23", 0.572,
        rel_tol=max(0.024 / 0.572, abs(4 / 7 - 0.572) / 0.572),
        cho_value=4 / 7, cho_repr="4/7", cho_complexity=comp(4, 7, 0, 1)))

    # Reactor angle prefactor: sin^2 th13 / eps0^2 = 3.
    targets.append(Target(
        "sin^2 th13 / eps0^2", 0.02203 / eps2,
        rel_tol=max(0.00056 / 0.02203, 0.02),
        cho_value=3.0, cho_repr="3", cho_complexity=comp(3, 1, 0, 1)))

    # Inter-sector ratio m_s m_t/(m_b m_c) = 3.
    targets.append(Target(
        "m_s m_t/(m_b m_c)", 3.04,
        rel_tol=max(0.10 / 3.04, 0.02), cho_value=3.0, cho_repr="3",
        cho_complexity=comp(3, 1, 0, 1)))

    # Georgi-Jarlskog: m_mu m_b/(m_tau m_s) = 8/3.
    targets.append(Target(
        "m_mu m_b/(m_tau m_s)", 2.661,
        rel_tol=max(0.030 / 2.661, abs(8 / 3 - 2.661) / 2.661),
        cho_value=8 / 3, cho_repr="8/3", cho_complexity=comp(8, 3, 0, 1)))

    return targets


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------
def main():
    library = build_library(max_complexity=20.0)
    targets = build_targets()

    print("=" * 78)
    print("  CHO HARDNESS-TO-VARY / LOOK-ELSEWHERE AUDIT")
    print("  Library: (int/int) * pi^p * sqrt(r), vocab", INT_VOCAB[:8], "...")
    print(f"  Total distinct simple numbers generated: {len(library)}")
    print("  Tolerance per row = max(experimental error, CHO error).")
    print("  KEY METRIC: rank of CHO choice among equally/simpler fitters.")
    print("=" * 78)

    header = f"{'Target':<22}{'CHO formula':<14}{'#fit':>5}{'simpler':>8}{'rank':>6}{'density':>9}"
    print(header)
    print("-" * 78)

    flawless = 0
    total = 0
    product_density = 1.0
    for t in targets:
        r = t.analyze(library)
        total += 1
        rank = r["cho_rank"]
        rank_s = "—" if rank is None else str(rank)
        if r["n_simpler_fitters"] == 0:
            flawless += 1
        product_density *= max(r["density"], 1e-6)
        print(f"{t.name:<22}{t.cho_repr:<14}{r['n_fitters']:>5}"
              f"{r['n_simpler_fitters']:>8}{rank_s:>6}{r['density']:>9.3f}")

    print("-" * 78)
    print(f"  Rows where CHO is the SIMPLEST fitter (no simpler alternative): "
          f"{flawless}/{total}")
    print(f"  Combined density (product of per-row fitter densities): "
          f"{product_density:.2e}")
    print()
    print("  Reading guide:")
    print("   * simpler = 0 and rank = 1  -> choice-independent 'hard to vary'.")
    print("   * simpler > 0               -> a strictly simpler number fits too;")
    print("                                  the CHO choice is not forced by data.")
    print("   * high density              -> many cheap alternatives; weak evidence.")
    print()

    # Show the competing fitters for any row where CHO is NOT the simplest.
    print("  Detail for rows with simpler competitors:")
    any_detail = False
    for t in targets:
        r = t.analyze(library)
        if r["n_simpler_fitters"] > 0:
            any_detail = True
            simpler = [e for e in r["fitters"]
                       if e["complexity"] < t.cho_complexity - 1e-9][:4]
            comp_list = ", ".join(f"{e['repr']}={e['value']:.4f}" for e in simpler)
            print(f"   - {t.name}: CHO={t.cho_repr}={t.cho_value:.4f}; "
                  f"simpler fitters: {comp_list}")
    if not any_detail:
        print("   (none — every CHO choice is the simplest number that fits)")
    print()


if __name__ == "__main__":
    main()
