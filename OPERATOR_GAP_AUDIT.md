# Operator Gap Audit

Frozen date: 2026-06-06

Purpose: record what the candidate CHO Yukawa/seesaw operator still does **not** derive. This is the document to read before upgrading any bridge status.

## Summary

The candidate operator in `CHO_OPERATOR.md` is useful because it puts the flavour bridges in one auditable object. It is not yet the missing proof.

Current status by blocker:

| Blocker | Current status | What would close it |
|---|---|---|
| Rank-one transition | Fano incidence gives rank-one local support for every non-identical Fano-line transition. The `21` line pairs form one Fano-automorphism orbit, and the normalized `log cos` action conditionally selects the primitive `A_Weyl x J3(O)` product over larger projectors by a `-1/2 log(rank)` penalty | Derive the physical transition ray, exact trace space, physical vacuum/representative selection, and `pi` holonomy from the CHO action or representation category |
| Sector projectors | Mass-sector ranks `1`, `3`, and `8` are now derived as number-operator Fock traces (`Tr P_0`, `Tr P_1`, `Tr I_Fock`) in `compute/epsilon_channel_coefficients.py` | Derive why the final CHO Yukawa trilinear selects these traces inside one operator, rather than accepting them as separate sector rules |
| Lepton `1/pi` | The `1/(4 pi)` shape is now identified as the uniform transition-sphere measure in `compute/epsilon_mixing_coefficients.py`, but the dynamical reduction of the lepton Yukawa trace to that measure is not proved | Derive the sphere-measure reduction from the CHO Yukawa operator or action, not as a post-hoc normalization |
| CKM reconciliation | `|V_us|` and `|V_cb|` coefficients have count/half-angle derivations, and the Fano phase gives a good `J`; one diagonalized charged-Yukawa matrix still has to produce all magnitudes and `J` together | One charged-Yukawa matrix must give `|V_us|`, `|V_cb|`, `|V_ub|`, and `J` together |
| PMNS perturbation | `DeltaM` is constructed from target angles | Derive `DeltaY` or `DeltaM` from broken triality dynamics |
| Continuum/RG | Not addressed by the flavour operator | Separate continuum/RG derivation for `alpha`, `sin^2(theta_W)`, `M_W`, and `Lambda` |

## Diagnostics

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 compute/operator_gap_audit.py
```

The script prints:

- the Fano intersection rank that partially explains why a rank-one transition is plausible;
- the incidence-action degeneracy, Fano-automorphism orbit check, primitive bridge-rank ladder, and normalized action rank penalty behind that rank-one transition, via `ACTION_PROJECTOR_BRIDGE.md`, `PRIMITIVE_PROJECTOR_BRIDGE.md`, `compute/action_projector_derivation.py`, and `compute/primitive_projector_derivation.py`;
- the Fock-grade orbit count and later number-operator trace result behind sector ranks `1`, `3`, and `8`;
- CKM scans at fixed Fano phase showing that simple NNI diagonal deformations do not reconcile all CKM observables;
- singular values and cyclic-`Z3` residuals for the PMNS perturbation, showing it is a target matrix rather than a dynamically generated perturbation;
- the continuum/RG items outside the current flavour-operator scope.

## Unified Spurion Attempt

`SPURION_BRIDGE.md` and `compute/spurion_bridge.py` take the first four blockers
above (rank-one transition, trace space, vacuum representative, `pi` holonomy) plus
the operator-reuse target and turn them into one parametric spurion
`T_break = theta * |tau><tau|` with explicit `PASS`/`FAIL` checks:

- `pi` holonomy is computed as the great-circle Berry phase `-(1/2) Omega = -pi`;
- the `21`-fold Fano-pair orbit reduces to a single vacuum-stabilizer orbit of
  size `3` once `omega = (1 + i e7)/2` fixes `e7`;
- `A_Weyl x J3(O)` is the unique trace space passing equivariance, Jordan
  closure, and trace-direction tests;
- one knob `epsilon0^2 = pi/432` drives all seven flavour channels at ~`1.5%` RMS.

These are failure-closed numerical checks, not CHO-action theorems. Later epsilon
modules derive the mass-sector rank `8`, identify the lepton `1/(4 pi)` sphere
measure, and derive the `|V_cb|` half-angle. The remaining gap is sharper: one
CHO Yukawa/seesaw operator must dynamically select those pieces and produce CKM,
PMNS, and first-generation factors in one diagonalisation.

## Interpretation

The useful next theoretical move is not another formula. It is either:

1. derive the candidate operator from CHO, or
2. find a contradiction in one of its components and revise the bridge.

The most urgent technical target is the charged-Yukawa matrix: it must preserve the Fano-phase Jarlskog success while also producing the corrected CKM magnitudes, including the half-angle `|V_cb|`. The current simple Fritzsch/NNI deformation scans do not do that as one matrix.
