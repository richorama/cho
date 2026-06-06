# Epsilon Bridge Scaffold

Frozen date: 2026-06-06

Purpose: turn the triality-breaking rule

```text
epsilon0^2 = pi / 432 = pi / (16 * 27)
```

from dimensional counting into an explicit bridge target. This note does **not** claim the bridge is proven. It states the minimal operator trace that would prove it and lists the exact missing steps.

## Current Status

The value

```text
epsilon0^2 = pi / 432 = 0.007272205...
```

currently acts as the common small quantity behind:

- second-generation masses: `m_c/m_t`, `m_s/(3 m_b)`, `m_mu/(8 m_tau)`
- CKM magnitudes: `|V_us|^2 / 7`, `(2 |V_cb|)^2`
- neutrino quantities: `sin^2(theta13) / 3`, `(Delta m21^2/Delta m31^2) / 4`

That interlocking role is evidence that the same bridge is being reused. It is not, by itself, a derivation.

## Candidate Operator Statement

Let the triality-breaking trace space be

```text
V_bridge = A_Weyl x J3(O)
dim(V_bridge) = dim_C(A) * dim(J3(O)) = 16 * 27 = 432.
```

The proposed bridge is a normalized trace over this space:

```text
epsilon0^2 = Tr(H_triality) / dim(V_bridge)
```

with

```text
H_triality = pi * P_transition,
rank(P_transition) = 1.
```

Equivalently:

```text
epsilon0^2 = Tr(pi * P_transition) / 432
           = pi * rank(P_transition) / 432
           = pi / 432.
```

The physics content is now explicit:

- `dim_C(A) = 16`: trace over one-generation complex Weyl internal states.
- `dim(J3(O)) = 27`: trace over the exceptional Jordan flavour/eigenvalue space.
- `rank(P_transition) = 1`: a single allowed triality-changing adjacent-generation channel.
- `pi`: a half-turn holonomy on the `G2/SU(3) ~= S6` coset, or equivalently the total angle of the minimal triality-breaking path.

## What This Improves

This replaces the vague sentence "divide by `16 * 27`" with a falsifiable operator claim:

> Find the CHO Yukawa/triality operator whose normalized trace on `A_Weyl x J3(O)` is `pi / 432`.

If a derived operator has rank `r != 1`, a different holonomy than `pi`, or a different trace space than `16 * 27`, the bridge changes numerically and the current mass/mixing relations must be revised.

## Action Projector Diagnostic

The memo `ACTION_PROJECTOR_BRIDGE.md` and script `compute/action_projector_derivation.py` ask how much of the rank-one projector is already forced by Fano incidence. They find:

- every non-identical Fano-line pair has a one-dimensional intersection, so local octonionic transition support is rank one;
- this is incidence-degenerate: there are `21` unordered line pairs with the same rank-one overlap, and the diagnostic shows they form one Fano-automorphism orbit;
- the primitive Weyl and primitive Jordan factors have a conditional normalized-action derivation: larger projectors dilute the transition by `S_link=-1/2 log(rank)`;
- using the full Weyl or full Jordan trace would multiply `epsilon0^2` by `16`, `27`, or `432`.

So the status is sharper but not closed: Fano incidence supplies the local rank-one support, the line-pair degeneracy is symmetry-equivalent, and the normalized information action selects the primitive product once a rank-one transition kernel is present. The CHO action must still derive the physical transition ray, the exact trace space, vacuum/representative selection, and `pi` holonomy.

## Unified Spurion Attempt

`SPURION_BRIDGE.md` and `compute/spurion_bridge.py` collapse the five proof
obligations below into one parametric operator `T_break = theta * |tau><tau|` and
attach a failure-closed `PASS`/`FAIL` check to each. That module derives the `pi`
holonomy as a great-circle Berry phase, reduces the `21`-fold Fano-pair
degeneracy to a single vacuum-stabilizer orbit, selects `A_Weyl x J3(O)` uniquely
by equivariance plus Jordan closure, and verifies one operator drives every
flavour channel at about `1.5%` RMS. It is still a numerical derivation attempt,
not a CHO-action theorem.

## Geometric Triangulation Progress (2026-06-06)

Four experiments (wired into `compute/audit.py`) attack the assembly directly,
on the thesis that `pi/432` must be produced as **one geometric object**, not
three independently-chosen pieces (`pi`, `16`, `27`). They triangulate:

- `compute/epsilon_heat_kernel.py` — **which `pi`?** Builds the algebra-internal
  Dirac operator's heat trace `Tr exp(-t D^2)`. A spectral-action `pi` can only
  enter as `(4 pi)^{-d/2}` (a Gaussian mode factor), never as a bare numerator
  `pi`. The bare `pi` is instead the Berry half-solid-angle `(1/2)(2 pi)`.
  **Heat-kernel origin ruled OUT; geometric/holonomy origin ruled IN.**
  Consequence: the `432` must be a pure **state count**, not a heat-kernel
  field-content coefficient.

- `compute/epsilon_cubic_discriminant.py` — **which `27`?** The universal cubic
  discriminant `Delta = -4 p^3 - 27 q^2` carries a `27`, but a rank-one triality
  breaking gives a double root (`{1, 1, 1+eps}`), so `Delta = 0` and the
  discriminant is blind to it. **The discriminant origin of the `27` is ruled
  out;** the `27` is `dim J3(O)`, a state/trace count.

- `compute/epsilon_state_count.py` — **the `16`, derived.** `16 = dim OP^2 =
  dim(F4) - dim(Spin(9)) = 52 - 36` is reproduced numerically as the dimension
  of the rank-one idempotent manifold of `J3(O)` (the manifold of triality vacua
  `|tau>`), via the nullity of the idempotent-equation Jacobian (`16` at all
  three primitive idempotents). The `16` is now a **geometric dimension**, not
  `dim_C(A_Weyl)` chosen by hand.

- `compute/epsilon_product_space.py` — **is `432` a genuine product?** Stratifies
  `J3(O) = 27 = 1 + 16 + 10` (idempotent direction + vacuum-manifold tangent +
  complement) and shows the geometric `16` is the off-diagonal octonion pair
  **inside** the flavour `27`. The external trace space `A_Weyl x J3(O) = 432`
  is therefore exact **iff** the gauge Weyl generation is isomorphic to the
  vacuum tangent, `A_Weyl ~= T(OP^2)`, as Spin(9) spinors (both are 16-dim
  octonion pairs — necessary condition verified, equality open).

**Net effect on the proof obligations below:** the `pi` (obligation 3) is
geometric and action-selected; the trace space (obligation 1) is reduced from a
free `16 x 27` to a **product of two geometric dimensions** with one named
residual — the single representation isomorphism `A_Weyl ~= T(OP^2)`. The `27`'s
discriminant origin is closed off as a dead end. What remains is obligation 2
(rank-one kernel) and that one isomorphism.

## Proof Obligations

1. **Trace space:** prove that the transition trace really runs over `A_Weyl x J3(O)`, not `A_R x J3(O)`, `A_Weyl x Im(J3(O))`, or another nearby space.
2. **Rank:** derive `rank(P_transition) = 1` from triality adjacency plus the normalized action rank penalty, not by choosing the value that fits `m_c/m_t`.
3. **Holonomy:** derive the `pi` factor from the minimal path on `G2/SU(3)` or from the CHO information action.
4. **Operator embedding:** construct `P_transition` as a projector or matrix element inside the CHO Yukawa operator.
5. **Sector coupling:** show why the same `epsilon0` feeds charged masses, CKM magnitudes, PMNS corrections, and neutrino splitting.

## Failure Modes

This bridge should be revised or downgraded if any of the following happens:

- the natural trace space is not `16 * 27`
- the angular factor is not fixed to `pi`
- more than one adjacent channel contributes at the same order
- the same operator cannot feed both mass ratios and mixing angles
- the proof requires fitting a continuous parameter hidden inside `H_triality`

## Immediate Tests

Run:

```bash
python3 compute/epsilon_bridge.py
python3 compute/action_projector_derivation.py
python3 compute/primitive_projector_derivation.py
```

The scripts print the normalized-trace ansatz, compare it to `m_c/m_t`, show nearby alternatives such as `1/(16*27)`, `2pi/(16*27)`, and `pi/(64*27)`, expose the rank ladder from Fano incidence to the full bridge projector, and show the normalized action penalty that selects the primitive product. Those alternatives are not proofs or disproofs, but they make the bridge pressure points visible.
