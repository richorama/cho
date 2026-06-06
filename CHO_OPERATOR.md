# Candidate CHO Yukawa/Seesaw Operator

Frozen date: 2026-06-06

Purpose: collect the strongest bridge pieces into one explicit candidate operator. This is the next hard target, not a completed theorem. It is designed to make the theory easier to attack: every important flavour bridge now has a concrete operator component whose rank, trace, phase, or perturbation can be checked.

## Composite Operator

The diagnostic script implements the following composite object:

```text
O_CHO = (H_triality, P_sector, W_H, A_gen, Phi_Fano, Y_nu)
```

with components:

```text
H_triality = pi |tau><tau| on A_Weyl x J3(O)
P_sector   = octonion projectors with traces 1, 3, and 8
W_H        = rank-one quaternionic weak/Higgs projector, Tr(W_H)/4 = 1/4
A_gen      = one-step generation adjacency 1 <-> 2 <-> 3
Phi_Fano   = phase from adjacent Fano-line incidence, cos(delta) = 1/3
M_nu       = Y_nu M_R^-1 Y_nu^T, normalized with M_R = I in the diagnostic
```

Run it with:

```bash
python3 compute/cho_bridge_operator.py
```

## What It Actually Derives, Conditionally

The current candidate gives the following if its component projectors are accepted:

```text
epsilon0^2 = Tr(H_triality) / dim(A_Weyl x J3(O)) = pi / (16 * 27)
```

The sector traces give:

```text
up:     Tr(P_up)     = 1  -> m_c/m_t     = 1 * epsilon0^2
down:   Tr(P_down)   = 3  -> m_s/m_b     = 3 * epsilon0^2
lepton: Tr(P_lepton) = 8  -> m_mu/m_tau  = 8 * epsilon0^2
```

The first-generation cascade is implemented as:

```text
m1/m3 = k_f * (m2/m3)^2
```

with shape factors from the composite weak/sector component:

```text
k_up     = (1/4) * 1^2       = 1/4
k_down   = (1/4) * 3^2       = 9/4
k_lepton = (1/4) * (1/pi)    = 1/(4*pi)
```

The CKM phase is derived from adjacent quaternionic subalgebras in the Fano plane:

```text
cos(delta) = dim(shared imaginary line) / dim(Fano line) = 1/3
delta = arccos(1/3).
```

The PMNS component builds an explicit seesaw target:

```text
M_corr = Y_corr Y_corr^T
DeltaM = M_corr - M_TBM
```

where `M_TBM` is fixed by residual TBM reflections and `DeltaM` is the broken-triality perturbation the final CHO operator must generate. The simple cyclic `Z3` action is not yet established for this mass matrix.

## Hard Gap Audit

The strongest objections are tracked in `OPERATOR_GAP_AUDIT.md` and quantified by `compute/operator_gap_audit.py`. In particular:

- adjacent Fano lines give a natural rank-one intersection, but the bridge projector on `A_Weyl x J3(O)` is still not derived;
- the sector projectors remain basis-selected;
- the lepton `1/pi` factor remains an unevaluated coset-average target;
- simple NNI deformation scans at fixed Fano phase do not reconcile corrected CKM magnitudes with the good Jarlskog value;
- the PMNS perturbation is full-rank and reverse-engineered from target angles;
- continuum/RG issues for `alpha`, `sin^2(theta_W)`, `M_W`, and `Lambda` live outside this flavour operator.

## What Is Still Not Proven

This candidate does not yet escape every numerology risk. It removes a lot of freedom by forcing the bridges into one object, but these remain open:

- derive the rank-one transition `|tau><tau|` from the CHO action, not by choosing rank one;
- derive the sector projectors `P_up`, `P_down`, and `P_lepton` from minimal ideals or representation theory;
- derive the lepton `1/pi` average from the coset measure;
- produce one charged-Yukawa diagonalization that gives both the corrected CKM magnitudes and the Fritzsch-level Jarlskog phase placement;
- derive the PMNS `DeltaY` perturbation dynamically, not from the target angles;
- construct separate continuum/RG derivations for `alpha`, `sin^2(theta_W)`, `M_W`, and `Lambda`.

## Why This Helps

Before this step, the bridge pressure points lived in separate notes. Now the bottleneck is sharper:

> Prove that the composite operator above is forced by CHO.

If that proof works, the epsilon trace, sector multiplicities, NNI shape factors, CKM phase, and PMNS perturbation become one construction. If any component fails, the failure mode is localized.
