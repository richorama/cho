"""
Cosmological Constant Prediction from CHO Framework
====================================================

Derives Lambda^(1/4) from algebraic structure:
  Lambda^(1/4) = C * M_P / (sqrt(2) * 3^64)

where:
  - 64 = dim_R(A) = dim(C⊗H⊗O): all algebraic directions contribute
  - sqrt(2) = sqrt(dim_R(C)): complex normalization (same as m_t = v/sqrt(2))
  - C = 11/12 = 1 - 1/dim(G_SM): gauge screening factor

Key relations:
  - EW hierarchy: M_W = M_P / 3^36    [36 = |Roots+(E6)|]
  - CC hierarchy: Lambda^(1/4) ∝ M_P / 3^64  [64 = dim(A)]
  - Difference: 64 - 36 = 28 = dim(so(8)) = dim(triality algebra)
"""
import numpy as np


# Physical constants
M_P = 1.2209e19        # Full Planck mass (GeV)
M_P_RED = 2.435e18     # Reduced Planck mass (GeV)
H0 = 1.437e-42         # Hubble constant in GeV (67.36 km/s/Mpc)
OMEGA_LAMBDA = 0.6847  # Dark energy fraction (Planck 2018)


def cc_observed():
    """Compute observed Lambda^(1/4) from Planck 2018 cosmological data."""
    rho_crit = 3 * H0**2 * M_P_RED**2
    rho_lambda = OMEGA_LAMBDA * rho_crit
    lambda_fourth = rho_lambda**0.25
    # Uncertainty: delta(H0)/H0 = 0.8%, delta(Omega)/Omega = 1.1%
    rel_err = 0.25 * np.sqrt((0.0073/OMEGA_LAMBDA)**2 + (2*0.54/67.36)**2)
    return lambda_fourth, rel_err


def cc_prediction(include_gauge_screening=True):
    """
    Predict Lambda^(1/4) from CHO algebraic structure.
    
    Formula: Lambda^(1/4) = C * M_P / (sqrt(2) * 3^64)
    
    Arguments for each factor:
    - M_P: natural UV cutoff (full Planck mass, not reduced)
    - 3^64: each of the 64 real dimensions of A = C⊗H⊗O contributes
             a factor 1/3 to the suppression (same mechanism as EW:
             3^36 from the 72 E6 roots, here 3^64 from dim(A))
    - sqrt(2): complex normalization factor sqrt(dim_R(C))
               (same factor that gives m_t = v/sqrt(2))
    - C = 11/12: gauge screening. Of the 12 SM gauge bosons,
                 11 are massive (8g + W± + Z). The massless photon
                 does not contribute to vacuum energy screening.
                 C = N_massive/N_total = 11/12
    """
    dim_A = 64  # dim_R(C⊗H⊗O) = 2 × 4 × 8
    dim_C = 2   # dim_R(C)
    dim_G_SM = 12  # dim(SU(3)×SU(2)×U(1)) = 8+3+1
    
    suppression = np.sqrt(dim_C) * 3.0**dim_A
    
    if include_gauge_screening:
        C = (dim_G_SM - 1.0) / dim_G_SM  # 11/12
    else:
        C = 1.0
    
    pred = C * M_P / suppression
    return pred


def hierarchy_comparison():
    """Compare EW and CC hierarchies side by side."""
    print("UNIFIED HIERARCHY STRUCTURE")
    print("=" * 60)
    print()
    
    # EW hierarchy
    M_W_pred = M_P / 3.0**36
    M_W_obs = 80.377  # GeV
    print(f"EW Hierarchy:")
    print(f"  Formula: M_W = M_P / 3^36")
    print(f"  Exponent: 36 = |positive roots of E6| = 72/2")
    print(f"  Predicted: {M_W_pred:.1f} GeV")
    print(f"  Observed:  {M_W_obs:.3f} GeV")
    print(f"  Error:     {(M_W_pred - M_W_obs)/M_W_obs * 100:+.1f}%")
    print()
    
    # CC hierarchy
    pred = cc_prediction(include_gauge_screening=True)
    obs, rel_err = cc_observed()
    err = (pred - obs) / obs * 100
    print(f"CC Hierarchy:")
    print(f"  Formula: Lambda^(1/4) = (11/12) * M_P / (sqrt(2) * 3^64)")
    print(f"  Exponent: 64 = dim_R(A) = dim(C⊗H⊗O)")
    print(f"  Predicted: {pred*1e12:.3f} meV")
    print(f"  Observed:  {obs*1e12:.3f} ± {obs*rel_err*1e12:.3f} meV")
    print(f"  Error:     {err:+.2f}%")
    print(f"  Sigma:     {abs(err)/(rel_err*100):.1f}σ")
    print()
    
    # Structure
    print(f"Structural Relations:")
    print(f"  EW exponent:  36 (E6 roots → gauge/Yukawa sector)")
    print(f"  CC exponent:  64 (full algebra → all vacuum modes)")
    print(f"  Difference:   {64-36} = dim(so(8)) = triality algebra")
    print(f"  Ratio:        64/36 = 16/9")
    print()
    
    # Full CC hierarchy
    lambda4 = (pred)**4
    mp4 = M_P**4
    print(f"  Lambda/M_P^4 = {lambda4/mp4:.2e}")
    print(f"  3^(-256) = {3.0**(-256):.2e}")
    print(f"  (256 = 4 × 64 = 4 × dim(A))")
    print()
    
    # Higgs quartic connection
    lambda_higgs = np.pi / 24
    m_H = 246.22 * np.sqrt(2 * lambda_higgs)
    print(f"Higgs Quartic Connection:")
    print(f"  lambda = pi/24 = pi/|D_4| (from D_4 root system)")
    print(f"  m_H = v*sqrt(pi/12) = {m_H:.2f} GeV (obs: 125.09)")
    print(f"  24 = |D_4 roots| = 3 × dim(O)")


def cc_sensitivity():
    """Show sensitivity to input parameters."""
    print("\nSENSITIVITY ANALYSIS")
    print("=" * 60)
    
    obs, rel_err = cc_observed()
    
    # Vary M_P within its uncertainty
    print(f"\nObserved: {obs*1e12:.4f} ± {obs*rel_err*1e12:.4f} meV")
    print(f"(Uncertainty dominated by H_0 measurement: ±0.5%)")
    print()
    
    # Different screening factors
    print("Screening factor candidates:")
    candidates = [
        ("No screening (C=1)", 1.0),
        ("C = 11/12 (massive gauge bosons)", 11.0/12),
        ("C = cos(pi/8)", np.cos(np.pi/8)),
        ("C = sqrt(5/6)", np.sqrt(5.0/6)),
    ]
    for name, C in candidates:
        pred = C * M_P / (np.sqrt(2) * 3.0**64)
        err = (pred - obs) / obs * 100
        sigma = abs(err) / (rel_err * 100)
        print(f"  {name:40s}: {pred*1e12:.3f} meV ({err:+.2f}%, {sigma:.1f}σ)")
    
    print()
    print("Note: With Hubble tension (H0=73 km/s/Mpc → SH0ES),")
    H0_local = 73.0 * 1e3 / (3.086e22) * 6.582e-16 / 1e9  # GeV
    # Lambda^(1/4) scales as H0^(1/2)
    obs_local = obs * (73.0/67.36)**0.5
    pred_1112 = (11.0/12) * M_P / (np.sqrt(2) * 3.0**64)
    err_local = (pred_1112 - obs_local) / obs_local * 100
    print(f"  Observed would be: {obs_local*1e12:.3f} meV")
    print(f"  Our prediction:   {pred_1112*1e12:.3f} meV ({err_local:+.1f}%)")
    print(f"  → Prediction sits between CMB and local H_0 values!")


if __name__ == "__main__":
    hierarchy_comparison()
    cc_sensitivity()
