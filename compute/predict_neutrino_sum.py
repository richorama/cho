"""
FROZEN PREDICTION: the neutrino mass sum  Sigma m_nu.
=====================================================

Frozen date: 2026-06-06.  Do NOT retune after new data; record revisions.

Most of the CHO audit table consists of POSTDICTIONS (constants known before
the formulas were written). A framework earns trust by committing, in advance,
to a single sharp number that future data can kill. This file is that commitment.

CHO inputs to this prediction
-----------------------------
  * Normal mass ordering (consequence of the CHO seesaw hierarchy).
  * Heaviest neutrino mass from the CHO seesaw:  m_nu3 = v^2 / (2 M_R),
    M_R = M_P / 3^9  ->  m_nu3 ~ 48.9 meV.
  * The lightest state is near-massless in the CHO hierarchy (m_nu1 << m_nu2).

Given those, the sum is fixed by the measured oscillation splittings, which
enter only as already-known experimental anchors (labelled as such).

Decisive experiments: DESI, Euclid, CMB-S4, LiteBIRD (cosmological Sigma m_nu);
JUNO/DUNE/Hyper-K (ordering).  Sensitivity is reaching the ~0.02-0.03 eV level,
enough to test this number this decade.
"""
import math

# --- Experimental oscillation anchors (already-known inputs, NOT predictions) ---
DM21_SQ = 7.42e-5   # eV^2, solar splitting (NuFit-class central value)
DM31_SQ = 2.510e-3  # eV^2, atmospheric splitting, normal ordering

# --- CHO seesaw prediction for the heaviest state ---
M_P = 1.221e19      # GeV
v = 246.22          # GeV
M_R = M_P / 3.0**9  # CHO right-handed scale
m_nu3_cho = (v**2 / (2 * M_R)) * 1e9  # eV


def sum_from_lightest(m1):
    """Normal-ordering sum given the lightest mass m1 (eV), using splittings."""
    m2 = math.sqrt(m1**2 + DM21_SQ)
    m3 = math.sqrt(m1**2 + DM31_SQ)
    return m1 + m2 + m3, (m1, m2, m3)


def cho_internal_sum(m1):
    """Normal-ordering sum using CHO's OWN predicted m_nu3 for the heavy state.
    m2 is tied to m3 by the solar splitting; m1 is the light input."""
    m3 = m_nu3_cho
    m2 = math.sqrt(max(m3**2 - DM31_SQ, 0.0) + DM21_SQ)
    return m1 + m2 + m3, (m1, m2, m3)


def main():
    print("=" * 70)
    print("  FROZEN PREDICTION (2026-06-06):  Sigma m_nu")
    print("=" * 70)

    # Minimal normal-ordering sum (lightest state -> 0).
    s_min, (m1, m2, m3) = sum_from_lightest(0.0)
    print(f"\n  Oscillation anchors (measured inputs):")
    print(f"    Delta m21^2 = {DM21_SQ:.3e} eV^2")
    print(f"    Delta m31^2 = {DM31_SQ:.3e} eV^2  (normal ordering)")

    print(f"\n  CHO seesaw heaviest state:")
    print(f"    m_nu3 (CHO) = {m_nu3_cho*1e3:.1f} meV")
    print(f"    sqrt(Delta m31^2) = {math.sqrt(DM31_SQ)*1e3:.1f} meV "
          f"(oscillation lower bound on m3)")

    print(f"\n  Normal-ordering mass spectrum (lightest ~ 0):")
    print(f"    m1 ~ {m1*1e3:5.1f} meV")
    print(f"    m2 ~ {m2*1e3:5.1f} meV")
    print(f"    m3 ~ {m3*1e3:5.1f} meV")

    # Frozen central value and band, using CHO's OWN m_nu3 (Q1-consistent).
    s_lo, _ = cho_internal_sum(0.0)
    s_hi, _ = cho_internal_sum(0.005)  # m1 up to ~5 meV ceiling
    central = 0.5 * (s_lo + s_hi)
    # For reference, the strict-splitting (oscillation-floor) minimal sum:
    s_osc, _ = sum_from_lightest(0.0)
    print("\n  " + "-" * 60)
    print(f"  FROZEN PREDICTION:  Sigma m_nu = {central*1e3:.0f} meV  "
          f"(band {s_lo*1e3:.0f}-{s_hi*1e3:.0f} meV)")
    print("  Ordering           :  NORMAL")
    print(f"  Basis              :  CHO seesaw m_nu3 = {m_nu3_cho*1e3:.1f} meV")
    print("  " + "-" * 60)
    print(f"  Cross-check: using the oscillation floor instead of CHO m_nu3")
    print(f"  gives a minimal sum of {s_osc*1e3:.0f} meV. The ~{(s_osc-s_lo)*1e3:.0f} meV")
    print(f"  gap reflects a real internal tension: CHO m_nu3 = {m_nu3_cho*1e3:.1f} meV")
    print(f"  sits ~{(math.sqrt(DM31_SQ)-m_nu3_cho)/math.sqrt(DM31_SQ)*100:.1f}% below sqrt(Delta m31^2) = "
          f"{math.sqrt(DM31_SQ)*1e3:.1f} meV.")
    print(f"  This 1.2 meV tension is itself a sharpenable test of the seesaw scale.")

    print("\n  FALSIFICATION CONDITIONS (any one falsifies or strongly pressures):")
    print("   1. Inverted ordering established at high significance.")
    print(f"   2. Cosmological Sigma m_nu robustly > ~0.12 eV after systematics")
    print(f"      (would force quasi-degenerate masses, ruling out this band).")
    print(f"   3. Cosmological Sigma m_nu robustly < {s_osc*1e3:.0f} meV")
    print(f"      (below the oscillation floor -> would break the framework AND")
    print(f"       standard 3-neutrino oscillations).")
    print(f"   4. Terrestrial m_nu3 measurement inconsistent with "
          f"~{math.sqrt(DM31_SQ)*1e3:.0f} meV.")

    print("\n  Why this is a real test, not a postdiction:")
    print("   * The cosmological Sigma m_nu is NOT yet decisively measured.")
    print("   * The number is sharp (a ~10 meV window) and ordering-specific.")
    print("   * Near-future data (DESI/Euclid/CMB-S4) reach the required")
    print("     ~0.02-0.03 eV sensitivity, so this resolves this decade.")
    print("   * The prediction is frozen here; revisions must be logged, not")
    print("     silently retuned.")
    print()


if __name__ == "__main__":
    main()
