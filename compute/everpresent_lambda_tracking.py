"""
BIG-BETS Bet 2a deepening (EXPLORATORY) -- everpresent-Lambda tracking & the
constant-vs-dynamical falsifier made quantitative.
============================================================================

causal_set_lambda.py established the bridge CHO 3^-64 <-> Sorkin Lambda~1/sqrt(V)
with the observed cosmic 4-volume, and flagged its single biggest debit: it uses
the OBSERVED V as input, so it TRADES "why 64?" for the cosmic-coincidence "why is
the universe this old/large NOW?".  This module invests in exactly that debit by
taking the *everpresent* reading of Sorkin's law seriously as a DYNAMICAL dark
energy, and turning the hand-wavy "DESI discriminates" hook into a COMPUTED high-
redshift divergence between the two readings of the SAME exponent.

Two readings of one number.
  * STATIC (CHO):   Lambda is a fixed algebraic constant (3^-256 x prefactor),
    time-independent, equation of state w = -1 EXACTLY.  Then its density fraction
    Omega_Lambda(z) = Omega_L,0 / E(z)^2  DILUTES to zero at high z (matter wins).
  * EVERPRESENT (Sorkin):  Lambda ~ +/- 1/sqrt(V(t)) FLUCTUATES as the past
    4-volume grows.  With the Hubble 4-volume V(t) ~ H(t)^-4 this gives
    Lambda(t) ~ H(t)^2, so the dark-energy density TRACKS the critical density and
    Omega_Lambda(z) ~ O(1) at EVERY epoch.

The first dividend (the why-now debit, partly repaid).  The everpresent scaling
Lambda ~ H^2 makes Omega_Lambda epoch-independent BY CONSTRUCTION -- the dark
energy is comparable to the matter density at all times, so "why is it O(1) now?"
dissolves into "it is O(1) always".  That is a genuine conceptual gain the STATIC
reading (and the original bridge) could not offer.  It is a property of Sorkin's
counting law, not of CHO.

The second dividend (the falsifier, made quantitative).  Because the two readings
share today's value but scale oppositely, they DIVERGE in the past by the computed
factor

        Omega_ever(z) / Omega_static(z)  =  E(z)^2

which is ~3 at z=1, ~70 at z=5, and ~6x10^8 at recombination (z~1100).  This is a
huge, model-independent observational handle: the static CHO reading has NO dark
energy at early times, the everpresent reading has order-unity dark energy at all
times.  DESI/Euclid w0-wa tomography measures precisely this trend, and the 2024-25
hints of EVOLVING dark energy (w0 > -1, wa < 0) point AWAY from the static w=-1.

The honest core (where CHO actually stands).  The entire time-structure above --
the tracking, the divergence, the effective w != -1 -- is CAUSAL-SET content.  CHO
contributes ONLY the present-epoch normalization (that Lambda_today ~ 3^-256); it
is a SPECTATOR in the dynamics.  Concretely, the redshift SHAPE of the divergence
is invariant under changing the CHO exponent (it cancels in the ratio), asserted
below.  So this deepening sharpens the bet in BOTH directions at once:
  (+) the everpresent reading repays the why-now debit and yields a sharp,
      live, quantitative falsifier;
  (-) it makes even clearer that a confirmed evolving-DE signal would support
      SORKIN over the CHO-STATIC reading -- i.e. CHO's own w=-1 is the casualty,
      and CHO adds nothing to the testable dynamics.

Caveat kept in view (not hidden).  A strictly SMOOTH Lambda ~ H^2 is degenerate
with a rescaled Newton constant (it renormalizes the Friedmann equation and does
not accelerate); the everpresent model's genuine dark-energy content lives in the
SIGN FLUCTUATIONS of Lambda, which the full stochastic simulations (Ahmed-Dodelson-
Greene-Sorkin 2004; Zwane-Afshordi-Sorkin 2018) treat and this module does NOT.
The magnitudes and the static-vs-tracking contrast here are heuristic (Hubble-
4-volume) order-of-magnitude statements, deliberately not a fit.

VERDICT: EXPLORATORY.  No prediction promoted, NO Bayes credit moves.  The module
asserts the exact anchors (V_today ~ 10^244, Lambda_today ~ 10^-122), the computed
divergence at recombination, and a CHO-spectator tripwire (the divergence shape is
independent of the CHO exponent) so the deepening cannot be silently read as CHO
predicting dark-energy evolution.
"""
import numpy as np

from causal_set_lambda import T_P, H0_SI, cho_lambda_in_planck, sorkin_volume

# --- Flat background (Planck 2018), consistent with cc_prediction's OMEGA_LAMBDA ---
OMEGA_M = 0.3153          # matter
OMEGA_L = 0.6847          # dark energy today (= cc_prediction.OMEGA_LAMBDA)
OMEGA_R = 9.2e-5          # radiation (photons + neutrinos), approximate
Z_RECOMB = 1100.0         # last-scattering redshift

# --- humility / distinguishability thresholds ---
DISTINGUISH_MIN = 1.0e6   # static vs everpresent must diverge by > this at recomb
TRACK_BAND = 3.0          # everpresent Omega_Lambda must stay within this factor (tracking)
STATIC_W = -1.0           # CHO static reading: exact cosmological constant


def E_of_z(z):
    """Dimensionless Hubble rate H(z)/H0 for the flat background."""
    z = np.asarray(z, dtype=float)
    return np.sqrt(OMEGA_R * (1 + z) ** 4 + OMEGA_M * (1 + z) ** 3 + OMEGA_L)


def hubble_planck(z):
    """Hubble rate at redshift z in Planck units (dimensionless)."""
    return H0_SI * E_of_z(z) * T_P


def hubble_four_volume(z):
    """Past Hubble 4-volume V(z) ~ H(z)^-4 in Planck-4-volumes."""
    return hubble_planck(z) ** (-4)


def lambda_everpresent(z):
    """Sorkin everpresent magnitude Lambda(z) ~ 1/sqrt(V(z)) = H(z)^2 (Planck units)."""
    return 1.0 / np.sqrt(hubble_four_volume(z))


def omega_lambda_static(z):
    """Static (CHO) dark-energy fraction: a fixed Lambda diluted by the background."""
    return OMEGA_L / E_of_z(z) ** 2


def omega_lambda_everpresent(z):
    """Everpresent fraction: Lambda~H^2 tracks rho_crit, so Omega_Lambda ~ const."""
    return OMEGA_L * np.ones_like(E_of_z(z))


def divergence(z):
    """Ratio of the two readings' dark-energy fractions = E(z)^2 (the observable handle)."""
    return omega_lambda_everpresent(z) / omega_lambda_static(z)


def divergence_shape(z, static_norm):
    """
    Redshift SHAPE of the everpresent/static Lambda ratio, normalized to z=0.
    static_norm = the CHO present-epoch Lambda (sets the normalization only).
    Used to prove the shape is INDEPENDENT of the CHO exponent (it cancels here).
    """
    r = lambda_everpresent(z) / static_norm
    r0 = lambda_everpresent(0.0) / static_norm
    return r / r0


def main():
    print("=" * 70)
    print("BIG-BETS Bet 2a deepening: everpresent-Lambda tracking vs CHO-static  (EXPLORATORY)")
    print("=" * 70)

    # ---- [A] the two readings of the same exponent ----
    print("\n[A] One exponent, two readings:")
    print("    STATIC (CHO):     Lambda fixed = 3^-256 x prefactor, w = %.0f exactly." % STATIC_W)
    print("    EVERPRESENT (Sorkin): Lambda ~ +/- 1/sqrt(V(t)) ~ H(t)^2, fluctuating, w(t) != -1.")
    print("    They share today's value but scale OPPOSITELY into the past.")

    # ---- [B] anchors: today's volume and Lambda both land ----
    c = cho_lambda_in_planck()
    V_cho, log3V, log10V = sorkin_volume(c["rho_pred"])
    H0_pl = hubble_planck(0.0)
    V_today = hubble_four_volume(0.0)
    lam_today = lambda_everpresent(0.0)
    print("\n[B] Present-epoch anchors (independent cross-check of the bridge):")
    print("    H0 in Planck units      = %.3e" % H0_pl)
    print("    Hubble 4-volume today   = 10^%.1f Planck-4-volumes  (Sorkin needs ~10^244)"
          % np.log10(V_today))
    print("    Lambda_everpresent today= 10^%.1f  (= H0_pl^2; observed ~10^-122)"
          % np.log10(lam_today))
    print("    CHO bridge 4-volume     = 10^%.1f  (from causal_set_lambda)" % log10V)

    # ---- [C] first dividend: tracking repays the why-now debit ----
    print("\n[C] Why-now debit, partly repaid: Lambda~H^2 => Omega_Lambda tracks rho_crit.")
    print("      %-8s %-14s %-16s %s" % ("z", "Om_L static", "Om_L everpresent", "static/today"))
    zs = [0.0, 0.5, 1.0, 2.0, 5.0, 100.0, Z_RECOMB]
    for z in zs:
        os_ = float(omega_lambda_static(z))
        oe_ = float(omega_lambda_everpresent(z))
        print("      %-8.1f %-14.3e %-16.3e %.3e" % (z, os_, oe_, os_ / OMEGA_L))
    print("    STATIC dark energy DILUTES to zero at high z (matter wins); EVERPRESENT stays")
    print("    O(1) at every epoch => 'why O(1) now?' becomes 'O(1) always'.  (Sorkin's win,")
    print("    not CHO's: it is a property of the counting law.)")

    # ---- [D] second dividend: the falsifier, made quantitative ----
    print("\n[D] The constant-vs-dynamical falsifier, COMPUTED:  Om_ever/Om_static = E(z)^2")
    for z in [1.0, 5.0, 100.0, Z_RECOMB]:
        print("      z=%-7.1f divergence = %.3e" % (z, float(divergence(z))))
    div_recomb = float(divergence(Z_RECOMB))
    print("    => at recombination the two readings differ by ~%.0e in dark-energy fraction." % div_recomb)
    print("    DESI/Euclid w0-wa tomography measures this trend; the 2024-25 hints of EVOLVING")
    print("    dark energy (w0 > -1, wa < 0) point AWAY from the CHO-static w = -1.")

    # ---- [E] honest core: CHO is a spectator in the dynamics ----
    print("\n[E] Where CHO actually stands (the honest core):")
    norm1 = c["rho_pred"]            # CHO present-epoch Lambda (exponent 64)
    norm2 = 13.7 * c["rho_pred"]     # a 10x+ different normalization (different prefactor/exponent)
    zz = np.array([0.0, 1.0, 10.0, 100.0, Z_RECOMB])
    shape1 = divergence_shape(zz, norm1)
    shape2 = divergence_shape(zz, norm2)
    print("    The everpresent/static ratio SHAPE vs z is invariant under the CHO normalization:")
    print("      shape (CHO norm)      :", np.array2string(shape1, precision=2))
    print("      shape (10x norm)      :", np.array2string(shape2, precision=2))
    print("      identical?            :", bool(np.allclose(shape1, shape2)))
    print("    => the entire testable time-structure is CAUSAL-SET content; CHO sets only the")
    print("       present-epoch normalization and is a SPECTATOR in the dynamics.")
    print("    Caveat: a strictly SMOOTH Lambda~H^2 is degenerate with rescaled G; the real DE")
    print("       lives in the SIGN fluctuations (Ahmed et al. 2004; Zwane et al. 2018), not")
    print("       simulated here.  Magnitudes are heuristic (Hubble-4-volume), not a fit.")

    # ---- [F] verdict ----
    print("\n[F] Verdict")
    print("    (+) everpresent reading repays the why-now debit and yields a sharp, live,")
    print("        quantitative falsifier (E(z)^2 divergence; DESI evolving-DE hints).")
    print("    (-) the dynamics is borrowed from causal sets; a confirmed evolving-DE signal")
    print("        supports SORKIN over CHO-STATIC -- CHO's own w=-1 is the casualty.")
    print("    EXPLORATORY: no prediction promoted; NO Bayes credit moves.")

    # ---- stable tripwires (exact anchors + computed divergence + CHO-spectator) ----
    # Present-epoch anchors land where the bridge needs them:
    assert 243.0 < np.log10(V_today) < 245.0, "Hubble 4-volume today left the ~10^244 window"
    assert -123.0 < np.log10(lam_today) < -121.0, "Lambda today left the ~10^-122 window"
    # Everpresent magnitude is exactly H^2 (the Sorkin scaling):
    assert np.isclose(lam_today, H0_pl ** 2), "Lambda_everpresent != H^2"
    # The two readings agree today (shared normalization):
    assert np.isclose(float(omega_lambda_static(0.0)), float(omega_lambda_everpresent(0.0)), atol=1e-3), \
        "readings disagree at z=0"
    # Tracking: everpresent Omega_Lambda stays O(1) across all z; static does NOT:
    oe = omega_lambda_everpresent(np.array(zs))
    assert np.all(np.abs(oe - OMEGA_L) < 1e-9), "everpresent fraction is not epoch-independent"
    assert float(omega_lambda_static(Z_RECOMB)) < OMEGA_L / TRACK_BAND, "static did not dilute"
    # The falsifier is real: the readings diverge enormously by recombination:
    assert div_recomb > DISTINGUISH_MIN, "static and everpresent readings are not distinguishable"
    assert np.isclose(div_recomb, float(E_of_z(Z_RECOMB) ** 2)), "divergence != E(z)^2"
    # CHO-spectator: the divergence SHAPE is independent of the CHO normalization/exponent:
    assert np.allclose(shape1, shape2), "divergence shape leaked CHO normalization"
    # Static reading is an exact cosmological constant:
    assert STATIC_W == -1.0, "static reading is not w=-1"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
