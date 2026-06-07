"""
Log-axis look-elsewhere for the CHO power-of-three scale relations.
====================================================================

`compute/look_elsewhere.py` audits the DIMENSIONLESS coefficients (eps0^2,
m_b/m_tau, sqrt(7), ...). It deliberately does NOT include the large-hierarchy
relations

    M_W       = M_P / 3^36
    M_R       = M_P / 3^9            (seesaw scale, from m_nu3)
    Lambda^14 = (11/12) M_P / (sqrt(2) 3^64)

because those are a different kind of claim: a single integer exponent on a
fixed base, multiplied by a small rational/sqrt/pi prefactor, aimed at a target
that lives on a LOGARITHMIC axis spanning ~30-60 e-folds. The right
"hardness-to-vary" question for them is not "is pi/432 the simplest coefficient"
but:

    Given the same small prefactor vocabulary, how much of the log axis is
    ALREADY covered (within the experimental tolerance) by SOME
    (prefactor, integer-exponent) pair no more complex than the CHO choice?

If that coverage fraction is close to 1, then landing on the target is nearly
unavoidable and the agreement is cheap, no matter how "simple" the winning
formula looks in isolation. If it is small, the hit is meaningful.

This module computes, per scale target and for the CHO base b = 3:

  * n_fitters  : how many distinct prefactors (at <= CHO complexity) admit an
                 integer exponent landing the value within tolerance;
  * cho_rank   : the simplicity rank of the CHO prefactor among those fitters;
  * coverage   : the fraction of one exponent window [0, ln b) covered by the
                 <=-CHO-complexity prefactor library at the row tolerance --
                 i.e. the prior probability that a RANDOM target in this band is
                 fit by *something* this simple. THIS is the honest look-elsewhere
                 number for a log-axis hierarchy.

It also sweeps alternative bases (2, e, pi) to show base 3 is not uniquely
forced by the data either.

No scipy; standard library only.
"""
import math
from fractions import Fraction
from itertools import product

PI = math.pi


# --------------------------------------------------------------------------
# Complexity model (shared convention with look_elsewhere.py)
# --------------------------------------------------------------------------
def _bits(n):
    return math.log2(abs(int(n)) + 1)


C_PI = 3.0
C_SQRT = 3.0


def prefactor_complexity(num, den, pi_pow, sqrt_rad):
    c = _bits(num) + _bits(den)
    c += abs(pi_pow) * C_PI
    if sqrt_rad != 1:
        c += C_SQRT + _bits(sqrt_rad)
    return c


def exponent_complexity(n):
    """Description length (bits) of the integer base exponent itself."""
    return _bits(n)


INT_VOCAB = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 16, 24, 27]
PI_POWERS = [-1, 0, 1]
SQRT_RADICANDS = [1, 2, 3, 5, 6, 7]


def _fmt(num, den, pi_pow, sqrt_rad):
    parts = []
    parts.append(f"{num}" if den == 1 else f"{num}/{den}")
    if pi_pow == 1:
        parts.append("pi")
    elif pi_pow == -1:
        parts.append("/pi")
    if sqrt_rad != 1:
        parts.append(f"sqrt({sqrt_rad})")
    s = " * ".join(p for p in parts if not p.startswith("/"))
    for p in parts:
        if p.startswith("/"):
            s += " " + p
    return s


def build_prefactor_library(max_complexity):
    """Simplest representative of each distinct prefactor value, <= max_complexity."""
    best = {}
    for num, den in product(INT_VOCAB, INT_VOCAB):
        frac = Fraction(num, den)
        n, d = frac.numerator, frac.denominator
        for pp in PI_POWERS:
            for rad in SQRT_RADICANDS:
                comp = prefactor_complexity(n, d, pp, rad)
                if comp > max_complexity:
                    continue
                val = (n / d) * (PI ** pp) * math.sqrt(rad)
                if not (val > 0) or not math.isfinite(val):
                    continue
                key = round(val, 12)
                prev = best.get(key)
                if prev is None or comp < prev["complexity"]:
                    best[key] = {
                        "value": val,
                        "complexity": comp,
                        "repr": _fmt(n, d, pp, rad),
                    }
    return sorted(best.values(), key=lambda e: e["complexity"])


# --------------------------------------------------------------------------
# Targets
# --------------------------------------------------------------------------
class ScaleTarget:
    """A hierarchy ratio T = prefactor * base^(-exponent)."""

    def __init__(self, name, ratio, rel_tol, base, cho_prefactor,
                 cho_exponent, cho_pref_repr, cho_pref_complexity):
        self.name = name
        self.ratio = ratio                 # measured dimensionless ratio (<1)
        self.rel_tol = rel_tol             # fractional tolerance counted as a fit
        self.base = base
        self.cho_prefactor = cho_prefactor
        self.cho_exponent = cho_exponent
        self.cho_pref_repr = cho_pref_repr
        self.cho_pref_complexity = cho_pref_complexity

    def cho_complexity(self):
        return self.cho_pref_complexity + exponent_complexity(self.cho_exponent)

    def best_exponent(self, prefactor_value):
        """Integer exponent n minimising |prefactor * b^-n / ratio - 1|."""
        # ratio = p * b^-n  ->  n = log_b(p / ratio)
        n = round(math.log(prefactor_value / self.ratio) / math.log(self.base))
        return int(n)

    def analyze(self, base=None):
        base = self.base if base is None else base
        budget = self.cho_complexity()
        lib = build_prefactor_library(max_complexity=budget)  # prefactor budget
        # Each candidate also pays for its integer exponent; keep total <= CHO total.
        tol = self.rel_tol
        fitters = []
        for e in lib:
            n = round(math.log(e["value"] / self.ratio) / math.log(base))
            n = int(n)
            total_complexity = e["complexity"] + exponent_complexity(n)
            if total_complexity > budget + 1e-9:
                continue
            value = e["value"] * base ** (-n)
            if abs(value / self.ratio - 1.0) <= tol:
                fitters.append({
                    "repr": e["repr"], "exp": n,
                    "complexity": total_complexity, "value": value,
                })
        fitters.sort(key=lambda f: (f["complexity"], abs(f["value"] - self.ratio)))
        cho_rank = None
        for i, f in enumerate(fitters, 1):
            if (abs(f["value"] - self.cho_prefactor * self.base ** (-self.cho_exponent))
                    <= 1e-12 * self.ratio):
                cho_rank = i
                break

        # Coverage of one exponent window by the SAME-budget prefactor library:
        # the prior probability a random target in this decade is fit by
        # something this simple. Fold each prefactor onto [0, ln base) and union
        # the +/- ln(1+tol) intervals it covers.
        window = math.log(base)
        half = math.log(1.0 + tol)
        intervals = []
        for e in lib:
            # An exponent costs <= budget - prefactor_complexity bits; allow any n
            # that keeps the total within budget (the exponent near the target is
            # the binding one, already counted above, so use a generous cap here).
            if e["complexity"] > budget + 1e-9:
                continue
            centre = math.log(e["value"]) % window
            lo, hi = centre - half, centre + half
            # wrap into [0, window)
            for a, b in _wrap_interval(lo, hi, window):
                intervals.append((a, b))
        coverage = _union_length(intervals, window) / window

        return {
            "n_fitters": len(fitters),
            "cho_rank": cho_rank,
            "fitters": fitters,
            "coverage": coverage,
            "budget_bits": budget,
            "lib_size": len(lib),
        }


def _wrap_interval(lo, hi, window):
    """Split [lo, hi] into pieces inside [0, window)."""
    lo %= window
    hi = lo + (hi - lo)
    out = []
    while hi > window:
        out.append((lo, window))
        lo, hi = 0.0, hi - window
    out.append((lo, hi))
    return out


def _union_length(intervals, window):
    if not intervals:
        return 0.0
    ivs = sorted((max(0.0, a), min(window, b)) for a, b in intervals if b > a)
    total = 0.0
    cur_lo, cur_hi = ivs[0]
    for a, b in ivs[1:]:
        if a <= cur_hi:
            cur_hi = max(cur_hi, b)
        else:
            total += cur_hi - cur_lo
            cur_lo, cur_hi = a, b
    total += cur_hi - cur_lo
    return min(total, window)


def build_targets():
    M_P = 1.221e19      # GeV
    v = 246.22          # GeV

    def pc(num, den, pp, rad):
        return prefactor_complexity(num, den, pp, rad)

    targets = []

    # M_W / M_P = 3^-36, prefactor 1. Experimental M_W known precisely, but the
    # honest tolerance is the CHO derived-term error (~1.2%).
    M_W = 80.377
    targets.append(ScaleTarget(
        "M_W / M_P  (=3^-36)", M_W / M_P, rel_tol=0.013, base=3,
        cho_prefactor=1.0, cho_exponent=36,
        cho_pref_repr="1", cho_pref_complexity=pc(1, 1, 0, 1)))

    # M_R / M_P = 3^-9, prefactor 1. M_R is INFERRED from m_nu3 (seesaw), not
    # measured, so the band is wider (~few %); anchor it to the oscillation
    # floor m_nu3 >= sqrt(Delta m31^2) = 50.1 meV -> M_R = v^2/(2 m_nu3).
    m_nu3_floor = 50.1e-12          # GeV
    M_R = v**2 / (2 * m_nu3_floor)  # GeV
    targets.append(ScaleTarget(
        "M_R / M_P  (=3^-9)", M_R / M_P, rel_tol=0.05, base=3,
        cho_prefactor=1.0, cho_exponent=9,
        cho_pref_repr="1", cho_pref_complexity=pc(1, 1, 0, 1)))

    # Lambda^(1/4) / M_P = (11/12)/sqrt(2) * 3^-64. CC range 2.24-2.33 meV ~ +/-2%.
    Lambda14 = 2.285e-12            # GeV (mid of 2.24-2.33 meV)
    targets.append(ScaleTarget(
        "Lambda^(1/4)/M_P (=3^-64)", Lambda14 / M_P, rel_tol=0.025, base=3,
        cho_prefactor=(11.0 / 12.0) / math.sqrt(2.0), cho_exponent=64,
        cho_pref_repr="(11/12)/sqrt(2)",
        cho_pref_complexity=pc(11, 12, 0, 2)))

    return targets


def main():
    print("=" * 78)
    print("  CHO SCALE-RELATION LOOK-ELSEWHERE  (log-axis hierarchy audit)")
    print("  Question: with the same simple prefactor vocabulary, how much of")
    print("  the log axis is ALREADY covered by some (prefactor, exponent) pair")
    print("  no more complex than the CHO choice? High coverage = cheap hit.")
    print("=" * 78)

    targets = build_targets()
    header = (f"{'Target':<26}{'CHO':<18}{'#fit':>5}{'rank':>5}"
              f"{'budget':>8}{'coverage':>10}")
    print(header)
    print("-" * 78)
    coverages = []
    for t in targets:
        r = t.analyze()
        rank = "-" if r["cho_rank"] is None else str(r["cho_rank"])
        cho_formula = f"{t.cho_pref_repr}*3^-{t.cho_exponent}"
        coverages.append(r["coverage"])
        print(f"{t.name:<26}{cho_formula:<18}{r['n_fitters']:>5}{rank:>5}"
              f"{r['budget_bits']:>8.1f}{r['coverage']*100:>9.1f}%")
    print("-" * 78)

    print("\n  Base sensitivity (is base 3 forced by the data?):")
    print(f"  {'Target':<26}{'b=2':>8}{'b=3':>8}{'b=e':>8}{'b=pi':>8}"
          "   (coverage %)")
    for t in targets:
        cells = []
        for b in (2, 3, math.e, PI):
            cells.append(t.analyze(base=b)["coverage"] * 100)
        print(f"  {t.name:<26}" + "".join(f"{c:>8.1f}" for c in cells))

    mean_cov = sum(coverages) / len(coverages)
    print("\n  Reading guide:")
    print("   * coverage ~ 1   -> on a log axis spanning tens of e-folds, a simple")
    print("     prefactor x integer-exponent hits this target almost surely; the")
    print("     agreement is CHEAP and the integer exponent is the only real claim.")
    print("   * coverage << 1  -> the simple-formula hit is genuinely constrained.")
    print(f"   * mean coverage over the three scale rows: {mean_cov*100:.1f}%.")
    print("   * HONEST VERDICT: the power-of-three scale relations are far less")
    print("     hard-to-vary than the dimensionless coefficients in")
    print("     look_elsewhere.py. Their content is the INTEGER EXPONENT")
    print("     (36, 9, 64) plus an O(1) prefactor, not a forced number. The CC")
    print("     row (prefactor 11/12 / sqrt(2)) is the weakest: a free O(1)")
    print("     prefactor covers most of the axis by itself.")
    print()


if __name__ == "__main__":
    main()
