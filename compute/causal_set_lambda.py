"""
BIG-BETS Bet 2 (EXPLORATORY) -- causal-set / counting dynamics x CHO.
=====================================================================

Bet 1 (padic_hierarchy.py) showed the cosmological-constant smallness is an
ARCHIMEDEAN artefact: 3-adically Lambda^(1/4) ~ M_P/3^64 is unit-ordinary, so a
real-analytic spectral action over R could never EMIT it.  That is a diagnosis,
not a mechanism.  Bet 2 supplies the missing KIND of object -- a *dynamics from
counting* -- and asks whether it gives the CC exponent a physical origin instead
of leaving it CHOSEN.

The bridge (this module).  Causal-set theory's one pre-data success is Sorkin's
heuristic

        Lambda  ~  +/- 1 / sqrt(V)          (Planck units, V = #spacetime atoms)

a Poisson fluctuation of the number of causal-set elements in the 4-volume to the
past.  With the observed cosmic 4-volume V ~ 10^244 this predicted Lambda ~ 10^-122
*before* the 1998 supernova data.  CHO independently writes

        Lambda^(1/4)  ~  M_P / 3^64    <=>    Lambda / M_P^4  ~  3^-256 .

Set the two equal:  Sorkin needs  V = Lambda^-2 ~ 3^512 ~ 10^244 -- which IS the
observed 4-volume.  Equivalently

        Lambda^(1/4)  ~  V^(-1/8),    so   64  ~  log_3(V_obs) / 8 .

So the CHO exponent 64 -- the single largest CHOSEN chunk in model_complexity.py
(~13 bits) -- is what Sorkin's counting law predicts, GIVEN base 3 (from triality /
Bet 1) and the observed cosmic volume.  The CC magnitude gains a *statistical-
dynamical* origin (atom-count fluctuation) that the static algebra never had.

What is honestly NEW and what is NOT.
  * The 1/8 power is (1/4 from the fourth root) x (1/2 from Sorkin's sqrt) -- NOT
    dim(O)=8.  The numerical coincidence with dim(O) is quoted, never leaned on.
  * Lambda is NOT exactly 3^-256: the (11/12)/sqrt2 prefactor (the SAME factor that
    makes CC base-3-DIRTY in Bet 1) shifts log_3(Lambda/M_P^4) to -257.6.  Reported.
  * The match recovers 64 only to ~+/-0.5 across 4-volume conventions (Hubble vs
    particle horizon).  Convention-dependent => SUGGESTIVE, not a derivation.
  * It uses the OBSERVED V as input, so it TRADES "why 64?" for "why is the universe
    this old/large now?" (the cosmic-coincidence problem) -- it relocates the
    mystery, it does not abolish it.

The sharp, falsifiable hook (the real payoff).  The two frameworks make INCOMPATIBLE
claims about whether Lambda is constant:
  * CHO  -> Lambda is a FIXED algebraic number (3^-256 x prefactor), time-independent.
  * Sorkin everpresent-Lambda -> Lambda FLUCTUATES as 1/sqrt(V(t)), DYNAMICAL dark
    energy with w(t) != -1.
They agree only at the present epoch.  DESI/Euclid w0-wa measurements discriminate.

VERDICT: EXPLORATORY.  The CC exponent stays CHOSEN, CC1/S1 untouched, NO Bayes
credit moves.  This is a candidate MECHANISM + a falsifier, not a closed derivation.
The module asserts the exact arithmetic AND a humility tripwire (the convention
spread stays wide enough that the bridge cannot be silently promoted to "derived").
"""
import numpy as np

from cc_prediction import M_P, cc_prediction, cc_observed

# --- Base distinguished by CHO triality (lineage: padic_hierarchy.py / Bet 1) ---
P = 3
CC_EXPONENT = 64          # Lambda^(1/4) ~ M_P / 3^64   (model_complexity: CHOSEN)
CC_DENSITY_EXPONENT = 256  # Lambda / M_P^4 ~ 3^-256  (= 4 * 64)

# --- Sorkin causal-set law:  Lambda ~ 1/sqrt(V)  =>  Lambda^(1/4) ~ V^(-1/8) ---
SORKIN_POWER = 0.5        # Lambda ~ V^-SORKIN_POWER
FOURTH_ROOT = 0.25        # Lambda^(1/4) = (Lambda)^FOURTH_ROOT
BRIDGE_POWER = FOURTH_ROOT * SORKIN_POWER   # = 1/8 (NOT dim(O); coincidence only)

# --- Planck-unit conversions (CODATA) for the OBSERVED cosmic 4-volume ---
ELL_P = 1.616255e-35      # Planck length, m
T_P = 5.391247e-44        # Planck time, s
C_LIGHT = 2.99792458e8    # m/s
H0_SI = 67.36e3 / 3.0856775814913673e22   # Hubble, s^-1 (Planck 2018, 67.36 km/s/Mpc)
AGE_S = 13.797e9 * 3.15576e7              # age of universe, s

PROMOTION_SPREAD = 0.30   # humility: convention spread must exceed this (suggestive only)


def cho_lambda_in_planck():
    """CHO Lambda/M_P^4 (predicted & observed) and its base-3 logarithm."""
    lam4_pred = cc_prediction(include_gauge_screening=True)   # GeV
    lam4_obs, rel = cc_observed()                             # GeV
    rho_pred = (lam4_pred / M_P) ** 4   # Lambda/M_P^4, dimensionless
    rho_obs = (lam4_obs / M_P) ** 4
    log3_pred = np.log(rho_pred) / np.log(P)
    log3_obs = np.log(rho_obs) / np.log(P)
    return {
        "lam4_pred": lam4_pred, "lam4_obs": lam4_obs, "rel": rel,
        "rho_pred": rho_pred, "rho_obs": rho_obs,
        "log3_pred": log3_pred, "log3_obs": log3_obs,
    }


def sorkin_volume(rho):
    """Sorkin V = Lambda^-2 (Planck-4-volumes) and its base-3 logarithm."""
    V = rho ** (-1.0 / SORKIN_POWER)   # rho^-2
    return V, np.log(V) / np.log(P), np.log10(V)


def cosmic_four_volume():
    """
    Observed cosmic 4-volume in Planck-4-volumes, several standard conventions.
    All land at ~10^244 -- the number Sorkin needs for Lambda ~ 10^-122.
    Returns list of (name, log10 V, log_3 V).
    """
    R_H = C_LIGHT / H0_SI            # Hubble radius, m
    rows = []
    for name, L3_cells, T_cells in [
        ("Hubble^3 x Hubble-time", (R_H / ELL_P) ** 3, (1.0 / H0_SI) / T_P),
        ("Hubble^3 x age",         (R_H / ELL_P) ** 3, AGE_S / T_P),
        ("particle-horizon^4",     (3.2 * R_H / ELL_P) ** 3, (3.2 * R_H / C_LIGHT) / T_P),
    ]:
        V = L3_cells * T_cells
        log3V = np.log(V) / np.log(P)
        rows.append((name, np.log10(V), log3V))
    return rows


def recovered_cc_exponent(log3V):
    """CC exponent recovered from a 4-volume:  64 ?= log_3(V) * (1/8) * ... .

    Lambda^(1/4) ~ V^(-1/8) and Lambda^(1/4) ~ 3^-n  =>  n = (1/8) log_3(V).
    """
    return BRIDGE_POWER * log3V


def base_specialness(log_value, bases=range(2, 13)):
    """
    HONEST look-elsewhere: base 3 is NOT forced by this match.  For the cosmic
    log-volume, show the distance of log_b(V)/8 to the nearest integer for each
    base -- base 3 is only justified EXTERNALLY (triality / Bet 1), not here.
    log_value is ln(V).  Returns list of (base, value/8, dist-to-int).
    """
    rows = []
    for b in bases:
        x = (log_value / np.log(b)) * BRIDGE_POWER
        rows.append((b, x, abs(x - round(x))))
    return rows


def main():
    print("=" * 70)
    print("BIG-BETS Bet 2: causal-set Lambda ~ 1/sqrt(V) vs CHO 3^64  (EXPLORATORY)")
    print("=" * 70)

    # ---- [A] CHO Lambda in Planck units ----
    c = cho_lambda_in_planck()
    print("\n[A] CHO cosmological constant (source: cc_prediction.py)")
    print("    Lambda^(1/4): pred %.4e GeV, obs %.4e GeV (%.1f%%)"
          % (c["lam4_pred"], c["lam4_obs"], 100 * (c["lam4_pred"] - c["lam4_obs"]) / c["lam4_obs"]))
    print("    Lambda/M_P^4: pred %.3e (log10 %.2f), obs %.3e (log10 %.2f)"
          % (c["rho_pred"], np.log10(c["rho_pred"]), c["rho_obs"], np.log10(c["rho_obs"])))
    print("    log_3(Lambda/M_P^4) pred = %.2f   (bare target -256; offset = prefactor)"
          % c["log3_pred"])
    print("    HONEST: 3^-256 = %.3e is base-3 only to ~10%% -- the (11/12)/sqrt2"
          % (P ** (-CC_DENSITY_EXPONENT)))
    print("            prefactor (same CC contamination as Bet 1) shifts it to 3^-257.6.")

    # ---- [B] Sorkin volume vs observed cosmic 4-volume ----
    V_pred, log3V_pred, log10V_pred = sorkin_volume(c["rho_pred"])
    print("\n[B] Sorkin: Lambda ~ 1/sqrt(V)  =>  V = Lambda^-2")
    print("    from CHO Lambda:   V = 10^%.1f = 3^%.1f" % (log10V_pred, log3V_pred))
    print("    bare 3^512:        V = 10^%.1f   (512 = 2 x 256 = 8 x 64)"
          % (CC_DENSITY_EXPONENT * 2 * np.log10(P)))
    print("    observed cosmic 4-volume (independent of Lambda):")
    vol_rows = cosmic_four_volume()
    for name, log10V, log3V in vol_rows:
        print("      %-26s 10^%.1f = 3^%.1f" % (name, log10V, log3V))

    # ---- [C] the bridge: 64 = (1/8) log_3(V) ----
    print("\n[C] Bridge:  Lambda^(1/4) ~ V^(-1/8),  so  64 ?= (1/8) log_3(V)")
    print("    1/8 = (1/4 fourth-root) x (1/2 Sorkin) = %.4f   (NOT dim(O); coincidence)"
          % BRIDGE_POWER)
    recs = []
    for name, log10V, log3V in vol_rows:
        n = recovered_cc_exponent(log3V)
        recs.append(n)
        print("      %-26s recovered exponent = %.2f   (CHO uses 64)" % (name, n))
    n_from_cho = recovered_cc_exponent(log3V_pred)
    spread = max(recs) - min(recs)
    print("    from CHO's own Lambda: %.2f ; convention spread = %.2f" % (n_from_cho, spread))
    print("    => CC exponent reframed as a VOLUME-FLUCTUATION scale, not a free integer.")

    # ---- [D] the sharp falsifier: constant (CHO) vs dynamical (Sorkin) ----
    print("\n[D] Falsifiable hook: is Lambda constant or dynamical?")
    print("    CHO    -> Lambda FIXED (3^-256 x prefactor), time-independent, w = -1.")
    print("    Sorkin -> Lambda ~ 1/sqrt(V(t)), DYNAMICAL, everpresent, w(t) != -1.")
    print("    They agree ONLY at the present epoch.  DESI/Euclid w0-wa discriminate.")
    print("    KILL: if dark energy is confirmed an exact constant (w=-1), the causal-set")
    print("          everpresent reading dies and V~3^512 reverts to a 'why-now' coincidence.")

    # ---- [E] honesty / look-elsewhere ----
    print("\n[E] Look-elsewhere & humility")
    bs = base_specialness(np.log(V_pred))
    clean = min(bs, key=lambda r: r[2])
    b3 = [r for r in bs if r[0] == P][0]
    print("    nearest-integer distance of (1/8)log_b(V) by base:")
    print("      base 3: value %.2f dist %.3f ;  cleanest base %d: value %.2f dist %.3f"
          % (b3[1], b3[2], clean[0], clean[1], clean[2]))
    print("    => base 3 is NOT forced by the volume match; its only warrant is EXTERNAL")
    print("       (triality / Bet 1).  The bridge uses observed V as INPUT (why-now trade).")
    print("    VERDICT: EXPLORATORY -- candidate dynamical MECHANISM for the CC magnitude")
    print("       + a constant-vs-dynamical falsifier.  Exponent stays CHOSEN; CC1/S1")
    print("       untouched; NO Bayes credit moves.")

    # ---- stable tripwires (exact arithmetic + humility) ----
    # CHO Lambda is NOT exactly 3^-256 (prefactor contamination, honest):
    assert abs(c["log3_pred"] + CC_DENSITY_EXPONENT) > 0.5, "prefactor offset vanished?"
    # Sorkin round-trip: sqrt(V) * Lambda = 1 exactly:
    assert abs(np.sqrt(V_pred) * c["rho_pred"] - 1.0) < 1e-9, "Sorkin V != Lambda^-2"
    # The bridge recovers 64 to within 1 from CHO's own Lambda:
    assert abs(n_from_cho - CC_EXPONENT) < 1.0, "bridge does not recover 64"
    # Observed cosmic 4-volume sits in the ~10^244 window for every convention:
    for name, log10V, log3V in vol_rows:
        assert 240.0 < log10V < 248.0, "4-volume outside ~10^244: %s" % name
    # The 1/8 power is exactly (1/4)x(1/2):
    assert abs(BRIDGE_POWER - 0.125) < 1e-12, "bridge power != 1/8"
    # HUMILITY: convention spread stays wide => suggestive, cannot be silently promoted:
    assert spread > PROMOTION_SPREAD, "spread collapsed -- re-examine before promoting"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
