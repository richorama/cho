# Operator Gap Audit

Frozen date: 2026-06-06

Purpose: record what the candidate CHO Yukawa/seesaw operator still does **not** derive. This is the document to read before upgrading any bridge status.

## Summary

The candidate operator in `CHO_OPERATOR.md` is useful because it puts the flavour bridges in one auditable object. It is not yet the missing proof.

Current status by blocker:

| Blocker | Current status | What would close it |
|---|---|---|
| Rank-one transition | Fano incidence gives rank-one local support for every non-identical Fano-line transition. The `21` line pairs form one Fano-automorphism orbit, and the normalized `log cos` action conditionally selects the primitive `A_Weyl x J3(O)` product over larger projectors by a `-1/2 log(rank)` penalty | Derive the physical transition ray, exact trace space, physical vacuum/representative selection, and `pi` holonomy from the CHO action or representation category |
| Sector projectors | Ranks `1` and `3` now have a conditional Fock-grade/orbit count from the chosen idempotent `omega=(1+i e7)/2`; rank `8` is still a full-Fock trace assumption | Derive the selected Fock grades from the CHO Yukawa trilinear and prove the charged-lepton trace is the full Fock space |
| Lepton `1/pi` | Still inserted as a coset-average rule; uniform `S6` volume normalization does not give `1/pi` | Compute the relevant `G2/SU(3)` or Yukawa-measure integral and show it reduces to a one-dimensional angle density `1/pi` |
| CKM reconciliation | Fano phase plus Fritzsch texture gives good `J`, while corrected magnitudes require a different projection | One charged-Yukawa matrix must give `|V_us|`, `|V_cb|`, `|V_ub|`, and `J` together |
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
- the Fock-grade orbit count that partially explains sector ranks `1` and `3`, while leaving rank `8` as a full-trace assumption;
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

These are failure-closed numerical checks, not CHO-action theorems; the CKM
magnitude/Jarlskog reconciliation and the lepton `1/pi` and rank-`8` traces
remain open in the rows below.

## Interpretation

The useful next theoretical move is not another formula. It is either:

1. derive the candidate operator from CHO, or
2. find a contradiction in one of its components and revise the bridge.

The most urgent technical target is the charged-Yukawa matrix: it must preserve the Fano-phase Jarlskog success while lowering `|V_cb|` to the corrected magnitude. The current simple Fritzsch/NNI deformation scans do not do that.
