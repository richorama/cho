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
  octonion pairs — necessary condition verified, equality named).

- `compute/epsilon_weyl_isomorphism.py` — **the isomorphism, established.** Builds
  `f4 = Der(J3(O))` (dim `52`) and its primitive-idempotent stabiliser
  `spin(9)` (dim `36`, closed under bracket, Killing form nondegenerate ⇒ the
  simple `so(9)`) entirely from the octonion table. Proves the `F4/Spin(9)`
  isotropy action on `T(OP^2)` is **irreducible of real type** (commutant
  dimension `1`), i.e. the spinor `Delta_9`; and independently builds `Delta_9`
  from an octonionic `Cl(9)` on the octonion pair `O^2` (the gauge `A_Weyl`
  carrier), also irreducible real (commutant `1`). Since **Spin(9) has a unique
  16-dim irrep** (the real spinor), the two `16`s are the *same* representation:
  `A_Weyl ~= T(OP^2) = Delta_9`, ESTABLISHED. The two `so(9)`'s sit as different
  embeddings in `gl(16)` (combined span `51`-dim), so the link is the
  uniqueness theorem rather than a literal identity — leaving one honest seam.

- `compute/epsilon_spin9_embedding.py` — **the seam, closed to a frame.** The
  flavour `so(9)` carries a UNIQUE positive-definite invariant metric `Q`
  (1-dim solution space), so in the `Q`-orthonormal frame the flavour Spin(9) is
  a literal subgroup of `SO(16)`. Its octonionic `Cl(9)` Clifford system is then
  RECOVERED as the 9-dim "vector" eigenspace of the quadratic Casimir on
  symmetric `16x16` matrices (multiplicities come out exactly `1, 9, 126`),
  satisfies `{Gamma_mu, Gamma_nu} = 2 delta` (error `~1e-14`), and its bivectors
  `span{(1/2)Gamma Gamma}` reproduce the flavour `so(9)` **exactly** (combined
  rank `36`, not `51`). So the flavour Spin(9) is the SAME octonionic Cl(9)
  spinor construction as the gauge side, and since `Cl^0(9) ~= R(16)` is simple
  with a unique 16-dim irrep (both commutants `1`), the two are conjugate in
  `O(16)`. The seam shrinks to one frame choice on the octonion pair.

- `compute/epsilon_rank_one_kernel.py` — **R1, reframed.** The rank-one kernel
  `|tau><tau|` is a PRIMITIVE idempotent of `J3(O)`: its spectrum is `(1,0,0)`,
  it is a zero-entropy PURE vacuum, and it is the minimal nonzero idempotent.
  This is the SAME rank-3 spectral fact (three orthogonal primitive idempotents
  resolve the identity) that forces `N_gen = 3` — so "rank one" = "primitive" =
  "one generation" = "pure". A rank-`r` kernel would switch on `r` generations at
  once (`eps0^2 -> r * pi/432`, degenerate, no hierarchy) and the info action
  `S_link = -1/2 log r` is maximised at `r=1`. Rank one is forced up to vacuum
  purity (the breaking selects one ray), the minimal content of a spurion.

- `compute/epsilon_free_action.py` — **R2, reframed (the weight).** The rank-one
  kernel plus its complement is a two-level system whose natural `U(2) -> SO(3)`
  Bloch-sphere symmetry, assumed alone, forces the weight: invariant potentials
  are CONSTANT (transitivity of `SO(3)` on `S^2`; the invariant subspace of
  functions up to quadratic order is exactly 1-dim), the invariant metric is
  ROUND and unique up to scale (`SO(2)` isotropy on the tangent plane is
  irreducible; invariant symmetric 2-tensors are 1-dim), and `theta = pi` is
  INDEPENDENT of that one undetermined scale (the Berry term is topological and
  great circles stay geodesic under rescaling). So the free kinetic action plus
  the topological term is the UNIQUE symmetric weight — a competing potential is
  forbidden. R2 shrinks to the microscopic origin of the two-level symmetry.

- `compute/epsilon_channel_coefficients.py` — **the lepton `8`, derived (M3).**
  Using this repo's octonionic Witt ladder (the same basis `ladder_charges.py`
  finds inside `C (x) O`), the number operator `N = sum_k alpha_k^dag alpha_k`
  has Fock-grade spectral projectors with traces `(1, 3, 3, 1)` on
  `Lambda^*(C^3)`. The three mass-sector coefficients are all `N`-spectral
  traces: `up = Tr P_0 = 1`, `down = Tr P_1 = 3`, `lepton = Tr I_Fock = 2^3 = 8`.
  The lepton `8` is the FULL Fock dimension, not a hand-chosen Yukawa rank —
  closing M3 for the mass sector. The CKM/PMNS/nu coefficients `sqrt7, 1/2, 4`
  and the lepton shape factor `1/pi` (M11) remain open as documented.

- `compute/epsilon_mixing_coefficients.py` — **the mixing counts (M11),
  advanced.** The mixing multiplicities are Fano-line counts read off the
  octonion incidence table with the vacuum `omega = (1 + i e7)/2` fixing the
  point `e7`: `7` = all Fano lines (`= dim Im(O)`), `3` = lines THROUGH the
  vacuum (the SU(3) colour/stabiliser triplet), `4 = 7 - 3` = lines AVOIDING it
  (the broken directions). These give `|V_us| ~ sqrt7 eps0` (an amplitude, so
  `sqrt` of the count), `sin^2 th13 ~ 3 eps0^2`, `dm21^2/dm31^2 ~ 4 eps0^2`
  (probabilities, so the plain count), and `sin^2 th23 = 4/7` — all within `~1.4%`.
  The amplitude-vs-probability `sqrt`-rule is Monte-Carlo verified (RMS of an
  `n`-direction random-phase sum is `sqrt n`). The lepton `1/(4 pi)` shape factor
  is IDENTIFIED as the uniform measure on the transition Bloch sphere `S^2`
  (`Int dOmega = 4 pi`), the unique `pi`-carrying partner of the full-Fock lepton
  trace. Honest residuals: the `|V_cb|` coefficient `1/2` (weak isospin `T3`) is
  an input, and the dynamical reduction of the lepton trace to the sphere average
  is identified but not derived.

**Net effect on the proof obligations below:** the `pi` (obligation 3) is
geometric and action-selected, and its WEIGHT is now forced — the free action +
topological term is the unique two-level-symmetric weight (R2); the trace space
(obligation 1) is a **product of two geometric dimensions whose 16s are the same
octonionic `Delta_9` subgroup** (isomorphism discharged, the gauge-vs-flavour
seam closed to a frame choice); the rank (obligation 2) is reframed — rank one is
**dual to `N_gen = 3`** (a primitive idempotent), no longer a value chosen to fit
`m_c/m_t`; and the mass-sector **sector coefficients** `(1, 3, 8)` (obligation 5)
are derived as number-operator Fock-grade traces (the lepton `8 = 2^3`), while
the **mixing coefficients** `(7, 3, 4, 4/7)` are derived as Fano-line counts and
the lepton `1/(4 pi)` is identified as the transition-sphere measure (advancing
M11). The `27`'s discriminant origin is closed off as a dead end. What remains
for F0 are minimal residuals: vacuum **purity** (R1), one **frame choice** on the
octonion pair (the seam), the microscopic **origin** of the two-level symmetry
(R2), the `|V_cb|` weak-isospin `1/2`, and the dynamical reduction of the lepton
trace to the sphere measure (M11).

## Proof Obligations

1. **Trace space:** prove that the transition trace really runs over `A_Weyl x J3(O)`, not `A_R x J3(O)`, `A_Weyl x Im(J3(O))`, or another nearby space. *(Advanced: the two `16`s are proven the same octonionic `Delta_9` subgroup — isomorphism discharged in `epsilon_weyl_isomorphism.py`, gauge-vs-flavour Spin(9) seam closed to a frame choice in `epsilon_spin9_embedding.py`.)*
2. **Rank:** derive `rank(P_transition) = 1` from triality adjacency plus the normalized action rank penalty, not by choosing the value that fits `m_c/m_t`. *(Reframed in `epsilon_rank_one_kernel.py`: rank one = primitive idempotent = pure single-generation vacuum, dual to `N_gen=3`; residual is vacuum purity.)*
3. **Holonomy:** derive the `pi` factor from the minimal path on `G2/SU(3)` or from the CHO information action. *(Advanced: `pi` is the Berry phase of the action's unique closed geodesic, and `epsilon_free_action.py` shows the free-action weight that carries it is the unique two-level-symmetric weight, up to a `theta`-irrelevant scale.)*
4. **Operator embedding:** construct `P_transition` as a projector or matrix element inside the CHO Yukawa operator.
5. **Sector coupling:** show why the same `epsilon0` feeds charged masses, CKM magnitudes, PMNS corrections, and neutrino splitting. *(Advanced: `epsilon_channel_coefficients.py` derives the mass ranks `(1, 3, 8)` as number-operator Fock-grade traces (closes M3); `epsilon_mixing_coefficients.py` derives the mixing counts `(7, 3, 4, 4/7)` as Fano-line incidences and identifies the lepton `1/(4 pi)` as the transition-sphere measure (advances M11). Open: the `|V_cb|` weak-isospin `1/2` and the dynamical reduction of the lepton trace to that measure.)*

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
