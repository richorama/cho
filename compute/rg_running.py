"""
1-Loop RG Running Analysis
============================

CONCLUSION: CHO mass predictions are ratios within a sector (m_c/m_t, m_s/m_b,
m_μ/m_τ). These are RG-invariant at 1-loop because same-sector quarks share
the same anomalous dimension γ_m. The running factors cancel in the ratio.

Mass ratios do NOT need running to a common scale.

What DOES need RG running:
- sin²θ_W: predicted = 1/4 at Λ_QCD, runs to 0.231 at M_Z via SU(2)×U(1) RGE
- α_em: predicted ≈ 1/134 at Λ_QCD, runs to 1/137.036 at low energy

This module provides the running machinery for reference and for the gauge
coupling predictions. Mass ratio predictions require no scale choice.
"""
import numpy as np


# QCD parameters
ALPHA_S_MZ = 0.1179  # αs(M_Z), PDG 2024
M_Z = 91.1876        # GeV

# Quark mass thresholds
M_T_POLE = 172.76    # GeV (pole mass)
M_B_MSBAR = 4.18     # GeV (MS-bar at μ = m_b)
M_C_MSBAR = 1.27     # GeV (MS-bar at μ = m_c)


def beta0(nf):
    """1-loop QCD β-function coefficient."""
    return 11 - 2*nf/3


def gamma0():
    """1-loop quark mass anomalous dimension (universal)."""
    return 4.0  # = 8/(2·1) for QCD


def alpha_s_running(mu, mu_ref, alpha_ref, nf):
    """
    1-loop αs running: αs(μ) from αs(μ_ref).
    αs(μ) = αs(μ₀) / [1 + (β₀/2π) αs(μ₀) ln(μ/μ₀)]
    """
    b0 = beta0(nf)
    return alpha_ref / (1 + (b0/(2*np.pi)) * alpha_ref * np.log(mu/mu_ref))


def mass_running(m_ref, mu_from, mu_to, alpha_from, nf):
    """
    Run mass from μ_from to μ_to at 1-loop.
    m(μ₂)/m(μ₁) = [αs(μ₂)/αs(μ₁)]^(γ₀/β₀)
    """
    alpha_to = alpha_s_running(mu_to, mu_from, alpha_from, nf)
    exponent = gamma0() / beta0(nf)
    return m_ref * (alpha_to / alpha_from)**exponent


def run_all_to_2GeV():
    """Run all quark masses to μ = 2 GeV and compare with CHO predictions."""
    
    print()
    print("=" * 75)
    print("  1-LOOP QCD RUNNING: ALL MASSES AT μ = 2 GeV")
    print("=" * 75)
    
    # Step 1: Run αs from M_Z down through thresholds
    # M_Z → m_b (nf=5)
    alpha_mb = alpha_s_running(M_B_MSBAR, M_Z, ALPHA_S_MZ, nf=5)
    # m_b → m_c (nf=4)  [b quark decouples below m_b]
    alpha_mc = alpha_s_running(M_C_MSBAR, M_B_MSBAR, alpha_mb, nf=4)
    # m_c → 2 GeV (nf=4) [we're above m_c so still nf=4... actually m_c=1.27 < 2 GeV]
    # Wait: μ=2 GeV is above m_c=1.27, so nf=4 at μ=2
    alpha_2 = alpha_s_running(2.0, M_C_MSBAR, alpha_mc, nf=4)
    
    print(f"\n  αs running (1-loop):")
    print(f"    αs(M_Z = 91.2 GeV) = {ALPHA_S_MZ:.4f}")
    print(f"    αs(m_b = 4.18 GeV) = {alpha_mb:.4f}")
    print(f"    αs(m_c = 1.27 GeV) = {alpha_mc:.4f}")
    print(f"    αs(2 GeV)          = {alpha_2:.4f}")
    
    # Step 2: Run each mass to μ = 2 GeV
    # Top quark: pole mass → MS-bar at m_t, then run down
    # Approximate: m_t(m_t) ≈ m_t_pole × (1 - 4αs(m_t)/(3π))
    alpha_mt = alpha_s_running(M_T_POLE, M_Z, ALPHA_S_MZ, nf=6)
    m_t_msbar_mt = M_T_POLE * (1 - 4*alpha_mt/(3*np.pi))
    
    # Run m_t from m_t down to m_b (nf=5)
    alpha_mt_5 = alpha_s_running(M_T_POLE, M_Z, ALPHA_S_MZ, nf=5)
    m_t_at_mb = mass_running(m_t_msbar_mt, M_T_POLE, M_B_MSBAR, alpha_mt_5, nf=5)
    # Run from m_b to 2 GeV (nf=4)
    m_t_at_2 = mass_running(m_t_at_mb, M_B_MSBAR, 2.0, alpha_mb, nf=4)
    
    # Bottom quark: MS-bar at m_b, run to 2 GeV (nf=4)
    m_b_at_2 = mass_running(M_B_MSBAR, M_B_MSBAR, 2.0, alpha_mb, nf=4)
    
    # Charm quark: MS-bar at m_c, run to 2 GeV (nf=4)
    m_c_at_2 = mass_running(M_C_MSBAR, M_C_MSBAR, 2.0, alpha_mc, nf=4)
    
    # Light quarks: already given at μ = 2 GeV (PDG convention)
    m_s_at_2 = 0.0934  # GeV
    m_u_at_2 = 2.16e-3  # GeV
    m_d_at_2 = 4.67e-3  # GeV
    
    print(f"\n  Quark masses at μ = 2 GeV (MS-bar, 1-loop):")
    print(f"    m_t(2 GeV) = {m_t_at_2:.1f} GeV")
    print(f"    m_b(2 GeV) = {m_b_at_2*1e3:.0f} MeV")
    print(f"    m_c(2 GeV) = {m_c_at_2*1e3:.0f} MeV")
    print(f"    m_s(2 GeV) = {m_s_at_2*1e3:.1f} MeV")
    print(f"    m_d(2 GeV) = {m_d_at_2*1e3:.2f} MeV")
    print(f"    m_u(2 GeV) = {m_u_at_2*1e3:.2f} MeV")
    
    # Step 3: Check CHO predictions using masses at common scale
    print(f"\n  CHO PREDICTIONS vs EXPERIMENT (all at μ = 2 GeV):")
    print(f"  {'Ratio':<30} {'CHO':>8} {'Obs(2GeV)':>10} {'Error':>7}")
    print(f"  {'-'*60}")
    
    # ε₀² predictions
    eps0_sq = np.pi / 432
    
    # m_c/m_t at 2 GeV = ε₀²  (should be same as at any other scale — RG invariant!)
    ratio_ct = m_c_at_2 / m_t_at_2
    print(f"  {'m_c/m_t = ε₀²':<30} {eps0_sq:>8.6f} {ratio_ct:>10.6f} "
          f"{(eps0_sq - ratio_ct)/ratio_ct*100:>+6.1f}%")
    
    # m_s/m_b = 3ε₀²
    ratio_sb = m_s_at_2 / m_b_at_2
    pred_sb = 3 * eps0_sq
    print(f"  {'m_s/m_b = 3ε₀²':<30} {pred_sb:>8.6f} {ratio_sb:>10.6f} "
          f"{(pred_sb - ratio_sb)/ratio_sb*100:>+6.1f}%")
    
    # Cross-sector ratios (RG-invariant by construction)
    R1 = (m_s_at_2 * m_t_at_2) / (m_b_at_2 * m_c_at_2)
    print(f"  {'m_s·m_t/(m_b·m_c) = 3':<30} {'3.000':>8} {R1:>10.3f} "
          f"{(3.0 - R1)/R1*100:>+6.1f}%")
    
    # First-gen ratios at 2 GeV
    ratio_u = m_u_at_2 * m_t_at_2 / m_c_at_2**2
    print(f"  {'m_u·m_t/m_c² = 1/4':<30} {'0.2500':>8} {ratio_u:>10.4f} "
          f"{(0.25 - ratio_u)/ratio_u*100:>+6.1f}%")
    
    ratio_d = m_d_at_2 * m_b_at_2 / m_s_at_2**2
    print(f"  {'m_d·m_b/m_s² = 9/4':<30} {'2.2500':>8} {ratio_d:>10.4f} "
          f"{(2.25 - ratio_d)/ratio_d*100:>+6.1f}%")
    
    print(f"\n  NOTE: Mass RATIOS within the same sector are RG-invariant at")
    print(f"  1-loop (same anomalous dimension cancels). This is why our")
    print(f"  predictions work without specifying a renormalization scale.")
    print(f"  The inter-sector ratios (involving leptons) are exactly RG-invariant")
    print(f"  since lepton masses don't run under QCD.")
    
    # Step 4: What DOES depend on scale?
    print(f"\n  SCALE-DEPENDENT QUANTITIES:")
    print(f"  ───────────────────────────")
    print(f"  These predictions implicitly assume a scale:")
    print(f"")
    print(f"  • sin²θ_W = 1/4: at Λ_QCD ~ 0.3 GeV (lattice scale)")
    print(f"  • α⁻¹ = 128π/3: at same confinement scale")
    print(f"  • m_t = v/√2: pole mass (scale-independent by definition)")
    print(f"  • m_H = v√(π/12): pole mass (scale-independent)")
    print(f"")
    print(f"  The fermion mass formulas (ε₀², 3ε₀², 8ε₀², 1/4, 9/4, 1/4π)")
    print(f"  predict RATIOS, which are RG-invariant. No scale choice needed.")
    
    return {
        'm_t_2GeV': m_t_at_2,
        'm_b_2GeV': m_b_at_2,
        'm_c_2GeV': m_c_at_2,
        'alpha_s_2GeV': alpha_2,
    }


if __name__ == "__main__":
    run_all_to_2GeV()
