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

`compute/epsilon_action_selection.py` sharpens the FIRST of those open items — the physical transition ray. It shows rank one is not posited but EXTREMAL: the Freudenthal sharp IS the gradient of the `E6`-invariant cubic norm `N3` on `J3(O)` (`X# = grad N3`, finite-difference match `~1e-8`, with `N3 = det`), so the critical locus of `N3` is exactly the rank-one variety `X#=0`. Trace-constrained criticality `X#=lam I` admits ONLY the rank-one (`lam=0`) and central (`lam=c^2`) configurations; on the physical slice `{O>=0, Tr O=1}` AM-GM bounds `N3 in [0, 1/27]`, with the rank-one idempotents the GLOBAL MINIMISERS (`N3=0`, flat exactly along the `f4`-orbit `OP^2` of tangent dim `16`) and `I/3` the unique maximiser (`1/27`). The SAME `N3` whose reduced structure group `E6` Schur-forces the flat `1/27` measure (`epsilon_measure_schur`) thus also selects the ray via its minimisers. This upgrades "rank-one kernel assumed" to "rank-one = minimiser of the invariant cubic potential", but it does NOT close the bridge: deriving that the CHO action's potential IS this `N3`, the kinetic coefficient on the great-circle Berry `pi`, and the full equations of motion all remain open, and F0 is not promoted.

`compute/f0_vacuum_majorization.py` then makes that ray-selection ROBUST to the choice of functional. On the same slice `{O>=0, Tr O=1}` the rank-one ray is the MAJORIZATION-MAXIMAL state: its spectrum `(1,0,0)` majorises every state and the maximally-mixed centre `I/3` is majorised by every state. By Hardy-Littlewood-Polya this single order fixes the extremiser of an entire universality class at once — every Schur-concave action (the cubic norm `N3=det`, the von Neumann and Renyi entropies) is minimised at the rank-one ray, and every Schur-convex action (purity `Tr O^2`, and the leading `-a Tr Phi^2 + b Tr Phi^4` term of a Connes finite spectral action) is extremised there. So the F0 vacuum does not hinge on the action being the specific cubic norm, and a Connes-type spectral action (the same KO-dim-6 triple as `ko_dimension_chirality`/`spectral_action`) lands on the SAME rank-one ray. Honest corrective: the spectral-action potential is EVEN (degrees 2 and 4) while `N3` is degree 3 — different functionals that agree only on the vacuum, by majorisation. This is a robustness theorem about the vacuum direction; it does NOT pick which action CHO realises, fix the kinetic coefficient on the Berry `pi`, or supply the `pi/432` normalisation, and F0 is not promoted.

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

- `compute/epsilon_vcb_halfangle.py` — **the `|V_cb|` `1/2`, derived (C2).** The
  `1/2` in `|V_cb| = (1/2) eps0` is the spin-1/2 HALF-ANGLE of the `SU(2)` double
  cover of the transition Bloch sphere: a single-qubit (inter-generation)
  transition amplitude is `sin(eps0/2) ~ (1/2) eps0` (coefficient `1/2`), while
  the `Im(O)` VECTOR channel of `|V_us|` carries the FULL angle `sin(eps0)`
  (coefficient `1`, summed coherently to `sqrt7`). So `sqrt7` vs `1/2` is exactly
  vector-vs-spinor, and its finite avatar at the octonionic 45-degree reflection
  is `tan(pi/8) = sqrt(2) - 1` (the same `tan(theta/2)` half-angle, verified
  exactly). The `1/2` is no longer a weak-isospin input; the residual is the
  channel ASSIGNMENT (which channel is the spinor).

- `compute/epsilon_a4_two_level.py` — **the two-level symmetry origin (R2),
  derived.** The `U(2) -> SO(3)` symmetry that `epsilon_free_action.py` assumed
  is the `SU(2)` closure of the `A4` flavour group. `A4` is the tetrahedral
  rotation group in `SO(3)` (order 12, classes `1+3+4+4`); its normal Klein
  subgroup `V4` (the three `pi`-rotations) lifts under the double cover
  `SU(2) -> SO(3)` to the qubit Pauli group `Q8 = {+-I, +-i sigma}` (and `A4`
  itself to the binary tetrahedral `2T`). By Burnside the irreducible 2-dim rep of
  `Q8` spans the full matrix algebra `M2(C)`, so the continuous closure is exactly
  `U(2)/su(2)` — the assumed two-level symmetry. And `A4/V4 = Z3` is the
  three-generation grading, so the SAME `A4` symmetry forces both the free action
  (R2) and `N_gen = 3` (cf. R1). R2's residual shrinks to the origin of `A4`
  itself.

**Net effect on the proof obligations below:** the `pi` (obligation 3) is
geometric and action-selected, and its WEIGHT is now forced — the free action +
topological term is the unique two-level-symmetric weight (R2), and that two-level
symmetry is itself the `SU(2)` closure of the `A4` flavour group (`Q8 = ` double
cover of `V4 < A4`, irreducible by Burnside; `A4/V4 = Z3` the generation grading);
the trace space
(obligation 1) is a **product of two geometric dimensions whose 16s are the same
octonionic `Delta_9` subgroup** (isomorphism discharged, the gauge-vs-flavour
seam closed to a frame choice); the rank (obligation 2) is reframed — rank one is
**dual to `N_gen = 3`** (a primitive idempotent), no longer a value chosen to fit
`m_c/m_t`; and the mass-sector **sector coefficients** `(1, 3, 8)` (obligation 5)
are derived as number-operator Fock-grade traces (the lepton `8 = 2^3`), while
the **mixing coefficients** `(7, 3, 4, 4/7)` are derived as Fano-line counts, the
`|V_cb|` `1/2` is derived as the `SU(2)` spinor half-angle (finite avatar
`tan(pi/8) = sqrt(2)-1`), and the lepton `1/(4 pi)` is identified as the
transition-sphere measure (advancing M11). The `27`'s discriminant origin is
closed off as a dead end. What remains for F0 are minimal residuals: vacuum
**purity** (R1), one **frame choice** on the octonion pair (the seam), the origin
of the `A4` flavour symmetry itself (R2), the CKM channel **assignment**, and the
dynamical reduction of the lepton trace to the sphere measure (M11).

## Proof Obligations

1. **Trace space:** prove that the transition trace really runs over `A_Weyl x J3(O)`, not `A_R x J3(O)`, `A_Weyl x Im(J3(O))`, or another nearby space. *(Advanced: the two `16`s are proven the same octonionic `Delta_9` subgroup — isomorphism discharged in `epsilon_weyl_isomorphism.py`, gauge-vs-flavour Spin(9) seam closed to a frame choice in `epsilon_spin9_embedding.py`. The flat `1/16` and `1/27` WEIGHTS are now Schur-forced: `epsilon_measure_schur.py` shows `Spin(9)` acts irreducibly on `Delta_9` (`-> 1/16`) and the full cubic-norm group `E6` acts irreducibly on `J3(O)` (`-> 1/27`; `F4 = Der` alone is reducible, `27 = 1+26`, so `E6` is required). What remains is the PRODUCT identification `Delta_9 (x) J3(O)` itself, not its normalization.)*
2. **Rank:** derive `rank(P_transition) = 1` from triality adjacency plus the normalized action rank penalty, not by choosing the value that fits `m_c/m_t`. *(Reframed in `epsilon_rank_one_kernel.py`: rank one = primitive idempotent = pure single-generation vacuum, dual to `N_gen=3`; residual is vacuum purity.)*
3. **Holonomy:** derive the `pi` factor from the minimal path on `G2/SU(3)` or from the CHO information action. *(Advanced: `pi` is the Berry phase of the action's unique closed geodesic; `epsilon_free_action.py` shows the free-action weight that carries it is the unique two-level-symmetric weight, up to a `theta`-irrelevant scale; and `epsilon_a4_two_level.py` traces that two-level symmetry to the `SU(2)` closure of the `A4` flavour group (`Q8 = ` double cover of `V4 < A4`; `A4/V4 = Z3`).)*
4. **Operator embedding:** construct `P_transition` as a projector or matrix element inside the CHO Yukawa operator.
5. **Sector coupling:** show why the same `epsilon0` feeds charged masses, CKM magnitudes, PMNS corrections, and neutrino splitting. *(Advanced: `epsilon_channel_coefficients.py` derives the mass ranks `(1, 3, 8)` as number-operator Fock-grade traces (closes M3); `epsilon_mixing_coefficients.py` derives the mixing counts `(7, 3, 4, 4/7)` as Fano-line incidences and identifies the lepton `1/(4 pi)` as the transition-sphere measure (advances M11); `epsilon_vcb_halfangle.py` derives the `|V_cb|` coefficient `1/2` as the `SU(2)` spinor half-angle (`tan(pi/8) = sqrt(2)-1`). Open: the CKM channel assignment and the dynamical reduction of the lepton trace to that measure.)*

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

## Topological-Route Test (2026-06-09)

`compute/berry_sigma_model_op2.py` runs the decisive experiment the Phase 1.3
refutation pointed at. Phase 1.3 (`f0_spectral_action_heatkernel.py`) proved the
ANALYTIC route to obligation 3 is closed: the finite spectral-action ratio
`a4/a2 = 0.00582895` is a `pi`-FREE rational, so it can never be `pi/432`; the
only `pi` a spectral action emits is the continuum `(4 pi)^(-d/2)`. The object
that can carry `pi` is therefore TOPOLOGICAL, not analytic. So this module
assembles the natural candidate — a Berry/Wess-Zumino sigma-model on the
triality-vacuum manifold `OP^2` (the rank-one `J3(O)` idempotents, `dim 16` =
the E6 minimal orbit) with the E6-invariant cubic norm `N3` as potential,
`S = (Berry/WZ kinetic) - (N3 potential)` — and tests the two halves that must
BOTH pass for `pi/432` to become a derived OUTPUT rather than a granted value.

- **[FORM, obligation 3] PASSES.** The Berry holonomy of the minimal great-circle
  (geodesic) loop of ACTUAL rank-one `J3(O)` idempotents is `pi`
  (`= 1/2 * 2pi` enclosed solid angle), cross-checked against the source-of-truth
  great-circle phase (`epsilon_action_selection.candidate_action_angle`); a
  non-geodesic latitude loop gives `pi/2`, so `pi` is the geodesic-selected
  holonomy specifically. The topological kinetic term DOES emit `pi` exactly
  where the analytic spectral action provably cannot. The kinetic term is settled.

- **[CONTENT, obligation 4/5 — the seeds] FAILS, structurally.** `N3 = det = 0`
  on ALL of `OP^2` (every point is rank-one; `X# = 0`) and the spectrum is
  identically `(1,0,0)` there, so `N3` — and indeed EVERY `F4`-invariant, since
  `F4` preserves the spectrum — is CONSTANT on the vacuum manifold and cannot
  lift its degeneracy to select three distinct eigenvalue-seeds. The measured
  charged-lepton hierarchy is a non-symmetric triple that is NOT an `N3` critical
  point (the global maximum `1/27` is the all-EQUAL anti-hierarchy), and the
  single-knob `eps0` ladder misses by `~1.40` decades.

**Net.** The sigma-model SEPARATES `pi/432`: the FORM (`pi`) is reachable by the
topological route — the kinetic term is settled — but the CONTENT (the seeds) is
NOT reachable from any `F4`-invariant potential and REQUIRES an `F4`-BREAKING
seed-selection term. This is a NEW symmetry no-go: it localises the entire
remaining gap to one object (an `F4`-breaking seed-selection potential on `OP^2`)
with the kinetic `pi` now topological and fixed. The scoreboard sign does NOT
flip (CONTENT failed): `pi/432` is NOT promoted, no Bayes credit moves, F0 stays
GEOMETRIC/open. This CONFIRMS the Phase 1.4 result (`spectral_action_432`:
structure forced, absolute seed open) from an independent dynamical direction.
EXPLORATORY.

## Intrinsic-Pi Hardening (2026-06-09)

`compute/berry_pi_intrinsic_op2.py` pushes the FORM half above past the slice it
was measured on. The `pi` of the topological-route test was the Berry holonomy of
ONE associative `CP^1 ⊂ OP^2` (a complex 2-plane of `O^3`); the honest next
question — "is the `pi` a feature of that slice, and why is it a half-turn?" — is
settled here without ever evaluating an (ill-defined) octonionic Bargmann product.

- **[A] The half-turn is FORCED by generation-orthogonality.** The transition
  sphere's two antipodal POLES are ORTHOGONAL primitive idempotents `E1, E2` of
  `J3(O)` (`Tr(E1 o E2) = 0` — two of the three generations). The Berry phase
  obeys `gamma(theta) = pi(1 - cos theta)` exactly and rises monotonically to the
  great circle — the unique closed geodesic, the locus EQUIDISTANT from the two
  orthogonal generations — which encloses the hemisphere (`Omega = 2pi`) and gives
  `gamma = pi`. A non-geodesic latitude loop encloses less and gives `< pi`. So
  `pi` is the holonomy that SEPARATES two orthogonal generations, not an input.

- **[B] The `pi` is INTRINSIC to `OP^2` (`F4`-invariant), not a slice artifact.**
  `F4 = Aut(J3(O))` preserves the Jordan product and trace, hence the trace metric
  `Tr(P o Q)` — it is an ISOMETRY of `OP^2` (verified to `~1e-13`). Transporting
  the great-circle loop by a random automorphism (i) keeps it a loop of genuine
  rank-one idempotents (`PoP = P`, `N3 = 0`), (ii) preserves EVERY consecutive
  overlap `Tr(P_i o P_{i+1})` — the full metric data the Berry phase `= 1/2 *`
  (round area) depends on — yet (iii) moves the loop into GENUINELY OCTONIONIC
  directions (the `e2..e7` components, zero on the associative slice, become
  `~0.2`). Since `OP^2 = F4/Spin(9)` is two-point-homogeneous, every geodesic
  2-sphere is an `F4`-image of the base `CP^1` and the isometry-invariant Berry
  phase is the SAME `pi`. The `pi` belongs to `OP^2`, not to the complex slice.

- **[C] The half-turn IS the SU(2) sign flip.** Around the great circle the
  Bargmann product of the transition states is a NEGATIVE real number:
  `e^{i pi} = -1`. The vacuum ray returns to MINUS itself after one loop — the
  spin-1/2 double-cover signature, the same `sqrt`/half-angle structure
  `epsilon_vcb_halfangle.py` reads as `tan(pi/8) = sqrt 2 - 1`.

**Net.** The kinetic `pi` of `pi/432` is now hardened: it is the `F4`-INTRINSIC
holonomy of `OP^2` (not an artifact of the associative slice), it equals `pi`
because the great circle is the geodesic separating two ORTHOGONAL generations,
and it is the SU(2) half-turn (`-1`). The intrinsicness rests on the verified
`F4`-isometry plus the standard isometry-invariance of the half-area Berry phase
on a two-point-homogeneous space — it proves the phase-determining trace data is
`F4`-invariant, NOT a re-evaluated octonionic Bargmann product. This does NOT
touch the CONTENT half: the three seeds stay open (every `F4`-invariant is flat
on `OP^2`, so seed-selection still needs an `F4`-BREAKING term). No Bayes credit
moves, `pi/432` is NOT promoted, F0 stays GEOMETRIC/open. EXPLORATORY.

## Seed Localization — the F4-breaking spurion selects the generations (2026-06-09)

`compute/f4_breaking_seed_op2.py` attacks the CONTENT half the intrinsic-pi
hardening left open. `berry_sigma_model_op2` proved a no-go: every `F4`-invariant
(including `N3 = det`) is flat on `OP^2`, so seed-selection requires an
`F4`-BREAKING term. This module tests whether the framework's OWN canonical
`F4`-breaking object — the rank-one triality-breaking vacuum spurion
`|tau><tau|` (`epsilon_rank_one_kernel`, `spurion_bridge`) — is that term, and
finds a TWO-SIDED result.

- **[POSITIVE — the no-go is EVADED].** The linear frame-breaking height
  `V_A(P) = Tr(P o A)` has, on `OP^2`, critical points EXACTLY at the three
  primitive idempotents `E1, E2, E3` of `A`'s eigenframe (the standard Morse
  theory of a height function on the flag manifold `OP^2 = F4/Spin(9)`: critical
  points = torus-fixed points = the eigenframe idempotents). The `F4`-orbit
  gradient `g_D = Tr((D.P) o A)` vanishes (`~1e-16`) at all three generations for
  a frame-diagonal `A`; gradient ASCENT from random `OP^2` points flows to the
  top generation (overlap `1.0000`); and the `F4`-INVARIANT control `A = I` is
  flat (`V = Tr P = 1`, gradient `~1e-15` — reproducing the no-go). So the three
  generations ARE the critical set of the canonical frame-breaking potential.

- **[DIRECTION is frame-canonical, NOT circular].** Any distinct-spectrum `A` in
  the SAME (generation) frame yields the SAME three critical points — only the
  VALUES change. The critical SET (the three generations) is fixed by the frame,
  independent of the seed magnitudes: the DIRECTION is canonical, the magnitudes
  are a separate input.

- **[HONEST OPEN — the magnitudes are INPUT].** The critical VALUES are
  `V_A(E_i) = spec(A)`, so the seed MAGNITUDES are the spurion spectrum (a
  tautology: seed in, seed out). And the canonical vacuum spurion is RANK-ONE:
  its height function lifts EXACTLY ONE level (`V(E_tau) = 1`, the whole `OP^1`
  of idempotents orthogonal to `E_tau` degenerate at value `0` — the geometric
  form of `spurion_perturbation` FACT 1). So three ISOLATED tiers require
  CUMULATIVE orders `A = E1 + eps0 E2 + eps0^2 E3`, whose spectrum
  `(1, eps0, eps0^2)` reproduces the generation cascade ladder, leaving the
  absolute scale `eps0^2 = pi/432` (the measure) as the lone surviving input.

**Net.** This tightens `berry_sigma_model_op2`'s open clause "seed-selection
requires an `F4`-BREAKING term" into: "the `F4`-breaking term IS the canonical
rank-one vacuum spurion; it makes the three generations the critical points of
its height function (real, frame-canonical/non-circular DIRECTION); rank-one-ness
forces the three-tier hierarchy to be the cumulative-order cascade; and the lone
surviving input is the absolute scale `eps0^2 = pi/432`." The CONTENT half is
therefore LOCALIZED to one scalar — the same `pi/432` of the measure — but NOT
closed: the seed magnitudes are still input, and the generation ASSIGNMENT is the
residual `S3`/Weyl freedom. No Bayes credit moves, `pi/432` is NOT promoted, F0
stays GEOMETRIC/open. EXPLORATORY.

## Action-Origin Modulus Gate (2026-06-10)

`compute/f4_breaking_action_origin_gate.py` attacks the exact residual left by
the seed-localization result. The height dynamics does not merely work for the
target spectrum: the whole family

`A(r) = E1 + r E2 + r^2 E3`

has the same generation critical set and the same qualitative ascent dynamics
for a continuum of `r`. Thus the OP2 height action fixes the frame and the
cascade form, but not the modulus `r`; choosing `r = eps0` inserts the scale.

The same obstruction appears in the entropy/free-energy completion. Maximising
entropy with grade energy `(0,1,2)` gives Gibbs ratios

`(1, exp(-beta), exp(-2 beta))`.

Matching the target cascade requires

`beta = -log(eps0) = 0.5 log(432/pi)`,

but `beta` is a continuous Lagrange multiplier, not selected by the current
action.

**Net.** The live bridge is now sharply localized: derive the scalar
`beta = 0.5 log(432/pi)` (equivalently `r = eps0`) from CHO dynamics. The
generation frame, the Berry/WZ `pi`, and the cascade form are narrowed; the
absolute scale `eps0^2 = pi/432` remains open. No Bayes credit moves.

## Beta-Selection Gate (2026-06-10)

`compute/f4_breaking_beta_selection_gate.py` tries the next rung directly. The
conditional identity

`exp(-2 beta) = pi/432`

is exact, but the current machinery does not select it. Entropy constraints fix
`beta` only after a mean grade is supplied; the natural means `1/16`, `1/27`,
`1/8`, `1/7`, and `1/3` miss the target, while the target mean is fitted.
Dimension-only selectors give `1/432`, `1/16`, `1/27`, or `1/7`; the `pi` enters
only if one postulates the flux/state-to-spectrum map. WZ level quantisation
leaves a family `k*pi/432`, so `k=1` is another primitive-sector assumption, not
yet a consequence.

**Net.** The live bridge is now maximally narrow: derive a beta-dependent CHO
variational term whose stationarity equation outputs `beta = 0.5 log(432/pi)`,
including the flux/state map and primitive level selection. Otherwise the scalar
modulus remains inserted. No Bayes credit moves.

## Primitive-Level Gate (2026-06-10)

`compute/f4_breaking_primitive_level_gate.py` isolates the discrete half of the
beta-selection obstruction. For a CP1 WZ disk action

`S_WZ = (k/2) Omega`,

changing the filling by a full sphere shifts the action by `2*pi*k`, so
single-valuedness of `exp(i S_WZ)` forces integer `k`. With Schur carrier weight
`1/432`, the half-turn density is `k*pi/432`; the primitive positive level
`k=1` gives the target exactly.

The honest obstruction is that integrality alone does not pick `k=1`. Positive
admissible levels `k*pi/432 < 1` run from `k=1` through `k=137`. Thus continuous
WZ normalization freedom is killed, but primitive level-one selection is still a
discrete CHO-dynamics obligation.

**Net.** The scalar problem has split cleanly: continuous normalization is no
longer the issue; the remaining issue is a primitive-sector selection rule tying
the WZ level to the F4-breaking seed spectrum. No Bayes credit moves.

## Level-One Carrier Gate (2026-06-10)

`compute/f4_breaking_level_one_carrier_gate.py` adds the two-level carrier that
was missing from the integrality-only test. For `CP^1` with WZ level `k`,
Borel-Weil quantization gives the `SU(2)` spin-`k/2` representation, hence

`dim H_k = k + 1`.

The transition carrier from the `A4 -> Q8 -> M2(C)` audit is a fundamental
two-state system. Matching the WZ-quantized carrier to that qubit selects
`k=1` uniquely: `k=0` is trivial, and `k>1` gives higher-spin sectors with more
than two states. Thus the discrete primitive-level ambiguity is removed once the
two-level carrier is granted.

**Net.** The remaining scalar bridge is now the beta-dependent action map, not
the WZ integer: derive a CHO variational term whose stationarity equation sets
`exp(-2 beta)` equal to the selected density `pi/432`. No Bayes credit moves.

## Born Beta-Map Gate (2026-06-10)

`compute/f4_breaking_born_beta_map_gate.py` tests the local half-log map left by
the carrier gate. The selected WZ object is a probability/flux density

`d = pi/432`.

The spurion cascade, however, is written in amplitude ratios. Under the Born
square map, the grade-one amplitude is `r=sqrt(d)`, so

`beta = -log(r)` and `exp(-2 beta)=d`.

This gives `r=eps0` exactly. The gate checks nearby wrong interpretations and
they miss visibly: treating `d` itself as an amplitude, using state count `1/432`
without Berry `pi`, or using the `k=2` WZ sector.

**Net.** The density-to-amplitude map is no longer the obstruction once the Born
interpretation is granted. The remaining live object is dynamical: derive the
`F4`-breaking action or transfer operator whose stationarity equation makes that
Born map physical rather than assigned. No Bayes credit moves.

## Projective Born Geometry Gate (2026-06-10)

`compute/f4_breaking_born_geometry_gate.py` hardens the granted Born step. In the
rank-one projector geometry of `CP^1` inside `OP^2`,

`Tr(P o Q) = |<psi|phi>|^2`.

Thus the trace overlap is a transition probability, not an amplitude. Realising
the selected density as `Tr(P o Q)=pi/432` forces the local projective amplitude
to be `sqrt(pi/432)=eps0`. The gate also checks that frame probabilities against
the three orthogonal generation idempotents add to one, and that the same trace
probability is preserved after `F4` transport into genuinely octonionic
directions.

**Net.** The square root in the beta-map gate is now projective geometry rather
than an interpretive convention. The remaining live object is still dynamical:
derive why the selected WZ density sources this transition channel, and derive
the beta stationarity equation. No Bayes credit moves.

## Source-Stationarity Gate (2026-06-10)

`compute/f4_breaking_source_stationarity_gate.py` tests the next conditional
rung. Once the selected density is read as the projective probability source,

`d = pi/432`,

and the cascade channel has

`q(beta)=exp(-2 beta)`,

the Bernoulli/KL stationarity equation gives `q=d`. Therefore

`beta = -0.5 log(d) = -log(eps0)`.

The gate checks the selected solution against the projective geometry witness and
rejects nearby wrong couplings: treating `exp(-beta)` itself as probability,
using `1/432` without the Berry `pi`, or using the `k=2` density.

**Net.** Beta is no longer merely assigned once the sourced projective channel is
granted: the stationarity equation selects it. The remaining live object is the
origin of that source-channel coupling in the CHO/F4-breaking action. No Bayes
credit moves.

## Calibrated Source-Action Gate (2026-06-10)

`compute/f4_breaking_calibrated_source_action_gate.py` checks whether the KL/log
source action was a fragile special choice. It was not. The same stationary beta
is selected by several calibrated local source actions on the projective
probability channel: KL/log score, Brier/quadratic score, Hellinger distance, and
logit-quadratic distance.

Each has a strict local minimum at `q=d`; with `q(beta)=exp(-2 beta)` this gives
the same

`beta = -0.5 log(pi/432) = -log(eps0)`.

Improper controls fail: a linear probability reward is not stationary at `q=d`,
and an amplitude-calibrated square loss targets the wrong coordinate. The wrong
source/channel controls from the stationarity gate still miss.

**Net.** The live assumption is no longer the specific KL functional. It is the
broader calibrated source coupling on projective probability. Deriving that
calibration from the CHO/F4-breaking action remains open. No Bayes credit moves.

## Large-Deviation Source Gate (2026-06-10)

`compute/f4_breaking_large_deviation_source_gate.py` tries to explain why the KL
source term appears at all. If the projective transition is sampled as a repeated
two-outcome process and the selected WZ/Born density is the empirical source
frequency, then binomial counting gives

`[-log P(m|q)+log P(m|m/N)]/N = KL(m/N || q)`

exactly at finite `N`. In the large-deviation limit `m/N -> d=pi/432`, this is
the Bernoulli source action used by the stationarity gate. With
`q(beta)=exp(-2 beta)`, stationarity again selects

`beta = -log(eps0)`.

The gate checks finite rational approximants converging to `pi/432`, verifies the
exact counting identity, and reruns the wrong source/channel controls.

**Net.** KL is no longer merely selected from the calibrated class once the
independent projective-transition ensemble is granted: it is the universal
large-deviation rate function. The remaining live object is deriving that
ensemble/source interpretation from the CHO/F4-breaking action. No Bayes credit
moves.

## Maximum-Caliber Ensemble Gate (2026-06-10)

`compute/f4_breaking_maxcal_ensemble_gate.py` asks whether the independent
projective-transition ensemble used by the large-deviation gate can itself be a
least-biased consequence. For binary histories with transition count `K`, Shannon
maximum caliber with only the mean-count constraint gives

`P(history)=exp(-lambda K)/Z`, with `Z=(1+exp(-lambda))^N`.

This factorizes exactly into iid Bernoulli trials. Setting the constrained mean to
the selected WZ/Born density `d=pi/432` gives `q=d`, and the existing source
stationarity rung again gives

`beta = -log(eps0)`.

The gate explicitly enumerates finite binary histories to check factorization,
normalization, marginal independence, and entropy per trial. Same-mean correlated
controls (all-or-none, paired blocks, and finite fixed-count histories) have lower
entropy per trial.

**Net.** Independence is no longer an independent primitive once binary histories,
MaxCal, and the single mean constraint are granted. The remaining live object is
deriving the MaxCal/path-entropy principle, binary projective path space, and mean
source constraint from the CHO/F4-breaking action. No Bayes credit moves.

## Binary Projector History Gate (2026-06-10)

`compute/f4_breaking_binary_projector_history_gate.py` asks where the binary
history alphabet used by MaxCal comes from. In the `OP^2`/Jordan projector
geometry, a primitive transition question `Q` generates the two effects

`yes = Q`, `no = I-Q`.

These are orthogonal idempotents and sum to the identity. For a rank-one source
state `P`, their probabilities are

`p_yes = Tr(P o Q)`, `p_no = Tr(P o (I-Q)) = 1-p_yes`.

At the selected primitive transition, `p_yes=pi/432`. Repeated readout of this
single primitive question gives histories in `{0,1}^N`, with multiplicities
`C(N,k)`, which is the binary path space used by the MaxCal and large-deviation
gates.

The gate checks the idempotent/orthogonality identities, F4 transport into genuine
octonionic directions, binomial history counting, and wrong binary sources. A
state-count scaled effect has the same superficial normalization but fails the
projective idempotent-event test.

**Net.** The binary alphabet is no longer an arbitrary statistical wrapper once a
primitive projective transition question is granted. The remaining live object is
deriving why CHO/F4-breaking dynamics selects that primitive question, its mean
`d=pi/432`, and the MaxCal/path-entropy action. No Bayes credit moves.

## Repeated-Measurement Gate (2026-06-10)

`compute/f4_breaking_repeated_measurement_gate.py` asks where the *independence*
used by the MaxCal and large-deviation gates comes from, without invoking a
maximum-entropy inference at all. It reads independence straight off the quantum
measurement structure.

Repeated projective measurement of the primitive question `Q` on a **re-prepared**
rank-one source `P` gives, by the Born rule,

`p_yes = Tr(P o Q) = pi/432`

on every trial, *independent of the history*, because re-preparation erases the
post-measurement state. The path measure is therefore the product `Bernoulli(d)`
measure exactly. Enumerating all histories for `N=4,8,12` shows this Born product
equals the MaxCal measure `exp(-lambda K)/Z` and the large-deviation Bernoulli
measure to ~`1e-16`: three independent routes, one measure.

The control is the **persistent** process with no re-preparation. After a `yes`
outcome the post-measurement state is the question ray `Q` itself, and
re-measuring `Q` is certain,

`Tr(Q o Q) = 1`  (quantum-Zeno absorption),

so the persistent outcomes form a correlated two-state Markov chain, not an iid
sequence. A one-parameter family of stationary chains with the *same* marginal `d`
but lag-1 correlation `r in {0, 0.3, 0.6, 0.9, 0.99}` has path-entropy rate that
falls strictly as `r` grows (gaps below `H(d)`: `0 -> 6.9e-3 -> 1.8e-2 -> 3.5e-2
-> 4.2e-2`). The memoryless `r=0` re-prepared process is the unique point that
saturates the iid bound `H(d)` — memorylessness is maximum caliber.

**Net.** Independence is not only a least-biased inference: it is the Born-rule
path measure of a memoryless re-prepared projective measurement, coinciding exactly
with the MaxCal and large-deviation measures, with the persistent (non-re-prepared)
Markov chain and its `Tr(Q o Q)=1` Zeno absorption as the correlated alternative.
This reduces "why MaxCal" to the more physical "why memoryless re-preparation".
The remaining live object is deriving from CHO/F4-breaking dynamics why the
transition process re-prepares (is memoryless) and why the source question `Q` has
mean `d=pi/432`. No Bayes credit moves.

## Vacuum-Relaxation Gate (2026-06-10)

`compute/f4_breaking_vacuum_relaxation_gate.py` asks where the *memorylessness*
used by the repeated-measurement gate comes from. It is not a free assumption: it
is the complete-relaxation limit of a standard open-system dynamics whose stable
fixed point is the vacuum primitive idempotent `P`.

Model the inter-probe dynamics as a depolarizing-toward-`P` channel

`C_r(rho) = r P + (1 - r) rho`,

a trace-preserving map that attracts every state to the vacuum source `P` with
relaxation fraction `r in [0,1]`. From the measured Born overlaps

`Tr(P o Q) = d = pi/432`,  `Tr(Q o Q) = 1`,  `Tr(Q o (I-Q)) = 0`

(the last by Lueders orthogonality, ~`2.6e-17`), the relaxed conditional
yes-probabilities are

`p(yes | prev=yes) = r d + (1-r) = 1 - r(1-d)`,  `p(yes | prev=no) = r d`,

a stationary two-state chain with lag-1 correlation `1-r` and stationary mean `d`
for every `r>0`. At `r=1` (complete vacuum relaxation) the two conditionals
collapse to `d`: the process is memoryless and its path measure is exactly the iid
`Bernoulli(d) = MaxCal = Born` product. At `r=0` (no relaxation) it freezes into
the persistent / quantum-Zeno chain.

The relaxation fraction is fixed by a timescale separation: with
`r = 1 - exp(-Delta_t/tau)` for inter-probe interval `Delta_t` and relaxation time
`tau`, memorylessness is the Born-Markov limit `Delta_t >> tau` (slow probing of a
fast-relaxing source). The path-entropy rate increases monotonically with
`Delta_t/tau` and saturates `H(d)` (gap `3.8e-2 -> 1.8e-5` across the sampled
ratios). A vacuum-specificity control confirms the attractor must be the vacuum
source: full relaxation toward `P` (overlap `d`) gives mean `d`, while relaxing
toward the measured ray `Q` (overlap `1`) or its complement (overlap `0`) gives
the wrong absorbing means `1` and `0`.

**Net.** Memorylessness has a standard physical origin — complete relaxation of
the probed state back to the vacuum source `P` — and the memoryless ensemble is
the `Delta_t >> tau` Born-Markov limit of that dynamics, agreeing exactly with the
MaxCal and Born product measures. This reduces "why memoryless" to "why fast
vacuum relaxation / timescale separation". The remaining live object is deriving
the relaxation channel, its time `tau`, the probe interval `Delta_t`, the
separation `Delta_t >> tau`, and the source question `Q` (overlap `d=pi/432`) from
CHO/F4-breaking dynamics. No Bayes credit moves.

## CHO Lindbladian Gate (2026-06-10)

`compute/f4_breaking_cho_lindbladian_gate.py` asks where the depolarizing-toward-`P`
relaxation channel of the vacuum-relaxation gate comes from. It is the finite-time
propagator of a concrete generator of dynamics — the first rung in the ladder to
write down an actual Lindbladian rather than measurement statistics.

Take the standard GKSL (Lindblad) dissipator that damps every basis direction into
the vacuum ray `p` (`P=|p><p|`), with jump operators

`L_k = sqrt(gamma) |p><e_k|`  (amplitude damping into the vacuum),

so that

`L(rho) = sum_k ( L_k rho L_k^dag - 1/2 { L_k^dag L_k, rho } ) = gamma ( Tr(rho) P - rho )`.

This is a genuine completely-positive trace-preserving (CPTP) semigroup generator,
verified against random `rho` to ~`2e-16`. Its finite-time propagator is exactly
the depolarizing-toward-`P` channel,

`exp(t L)(rho) = e^{-gamma t} rho + (1 - e^{-gamma t}) P = C_{r(t)}(rho)`,
`r(t) = 1 - exp(-gamma t)`,  `tau = 1/gamma`,

with a UNIQUE steady state `P` (the vacuum primitive idempotent; steady-manifold
dimension `1`, overlap `Tr(P rho_ss)=1`) and spectral gap `gamma`. The dynamics is
verified on a faithful two-level (qubit) representation of the `{P, Q}` effect
statistics, where `|<p|q>|^2 = Tr(P o Q) = d = pi/432` exactly (cross-checked
against the Jordan trace form), and the matrix exponential is computed independently
by scaling-and-squaring Taylor series (no SciPy), so the semigroup match (~`1e-16`)
is a real verification. The channel is CPTP at every time (Choi matrix PSD), and
survival fractions compose, `(1-r(s))(1-r(t)) = 1-r(s+t)`, to ~`1e-17`.

Feeding `r(Delta_t) = 1 - exp(-gamma Delta_t)` into the vacuum-relaxation
conditionals reproduces the mean `d` for every probe interval and the memoryless
Born-Markov limit as `gamma Delta_t -> infinity` (memoryless gap shrinking
`2.7e-2 -> 1.0e-9`). Controls fail cleanly: a unitary-only generator `-i[H,rho]`
does not relax (degenerate steady manifold, zero decay gap), a wrong-target
dissipator relaxes to `Q` (mean `1`), and a dephasing-only dissipator relaxes to a
mixed non-vacuum state (mean `!= d`).

**Net.** The relaxation channel assumed by the vacuum-relaxation gate is the exact
CPTP semigroup of a concrete Lindblad generator whose unique steady state is the
vacuum `P` and whose relaxation is exponential with time `tau = 1/gamma`. This
reduces "why the relaxation channel" to "why this Lindblad jump structure and rate
from CHO dynamics". The remaining live object is deriving the jump operators, the
rate `gamma` (hence `tau`), the probe interval `Delta_t`, and the source question
`Q` (overlap `d=pi/432`) from the CHO/F4-breaking action. No Bayes credit moves.

## Peirce-Jump Gate (2026-06-10)

`compute/f4_breaking_peirce_jump_gate.py` asks where the CHO Lindbladian's
vacuum-damping jump operators come from. The Lindbladian wrote

`L_k = sqrt(gamma) |p><e_k|`   (amplitude damping into the vacuum ray p),

but the directions `e_k` orthogonal to `p`, and the choice to damp toward `p`,
were written by hand on the faithful qubit. This gate climbs underneath and shows
those modes and their target are the Peirce decomposition of the exceptional
Jordan algebra `J3(O)` relative to a PRIMITIVE idempotent.

For an element `P` of `J3(O)` the Jordan left-multiplication `L_P(X) = P o X` is
self-adjoint for the trace form, so its eigenspaces are trace-orthogonal. The
Peirce theorem says that when `P` is an idempotent (`P o P = P`) the spectrum of
`L_P` lies in `{0, 1/2, 1}` -- verified here by the exact minimal polynomial
`|L_P (L_P - 1/2)(L_P - 1)| = 0` (machine zero, rational structure constants) --
splitting the 27-dimensional algebra into

`J3(O) = J_1(P)  (+)  J_{1/2}(P)  (+)  J_0(P)`.

For a PRIMITIVE (rank-one) idempotent the multiplicities are

`dim J_1 = 1`     the vacuum ray `span(P)`,
`dim J_{1/2} = 16` the coherence / transition modes ( = `dim OP^2 = Delta_9` ),
`dim J_0 = 10`    the orthogonal population modes ( the `J2(O)` block ),

with `1 + 16 + 10 = 27`. The Lagrange-interpolation spectral projectors
`E_1 = 2L^2 - L`, `E_{1/2} = 4L - 4L^2`, `E_0 = 2L^2 - 3L + I` are exact
idempotents, mutually orthogonal and summing to the identity to machine zero, and
the trace-orthogonal complement of the vacuum ray is exactly
`J_{1/2}(P) (+) J_0(P)` -- the 26 off-vacuum modes (`<P, off-vacuum> = 0`
exactly). So the abstract `e_k orthogonal to p` of the Lindbladian jump operators
are concretely these Peirce modes: 16 coherences plus 10 populations.

The depolarizing-toward-vacuum channel on `J3(O)`,

`R_r(X) = (1 - r) X + r tr(X) P`,

the Jordan-algebra image of the Lindbladian `C_r`, has eigenvalue 1 on the vacuum
ray and `(1 - r)` on all 26 off-vacuum modes, a UNIQUE steady ray `span(P)`
(exponential relaxation `|R_{r(t)} X - tr(X) P| -> 1.6e-11` at `t = 25`), and an
exact composing semigroup `R_{r(s)} R_{r(t)} = R_{r(s+t)}` with
`r(t) = 1 - exp(-gamma t)` (`~1e-16`) -- reproducing the Lindbladian's unique
vacuum steady state at the full-Jordan level. Controls miss cleanly: a rank-two
idempotent leaves a 10-dimensional `J_1` (no single ray), the identity has
`L_I = I` and no off-vacuum modes, and non-idempotent targets (`diag(2,0,0)`,
`diag(1/2,0,0)`) have `L`-spectrum outside `{0, 1/2, 1}` so no Peirce structure
exists. Only a PRIMITIVE idempotent gives a one-dimensional vacuum ray.

A cross-check ties this dissipative structure to the measure: the arena dimension
`Delta_9 x J3(O) = 16 x 27 = 432` is the denominator of `eps0^2 = pi/432`, and
the coherence space `J_{1/2}(P)` of dimension `16 = dim OP^2` is the SAME
topological manifold whose Berry holonomy supplies the FORM `pi`. The 16-fold
that carries the holonomy `pi` is the 16-fold of coherences that the vacuum
damping kills.

**Net.** The jump-operator STRUCTURE of the CHO Lindbladian -- amplitude damping
of the orthogonal modes into a unique vacuum ray -- is forced by the Peirce
decomposition of `J3(O)` at a primitive idempotent, not chosen by hand. This
reduces "why these vacuum-damping jump operators" to "why a primitive-idempotent
vacuum". The remaining live object is deriving from CHO/F4-breaking dynamics WHY
the vacuum is a primitive (rank-one) idempotent rather than rank-two or rank-three,
together with the rate `gamma` and the source overlap `d = pi/432`. No Bayes
credit moves.

## Vacuum-Purity Gate (2026-06-10)

`compute/f4_breaking_vacuum_purity_gate.py` climbs underneath the Peirce-jump
gate's one residual: that gate derived the vacuum-damping jump STRUCTURE from the
Peirce decomposition of `J3(O)` at a PRIMITIVE idempotent, but had to ASSUME the
vacuum is primitive (only a rank-one idempotent gives a single vacuum ray). This
gate asks whether that primitivity is free or forced.

**Statics (cited, not re-derived).** On the `J3(O)` state slice `{rho >= 0,
Tr rho = 1}` the purity `pi(rho) = Tr(rho o rho)` lies in `[1/3, 1]`, equal to 1
EXACTLY at the primitive idempotents (the pure states = extreme points = `OP^2`,
dim 16) and `1/3` at the maximally mixed centre `I/3`. The rank-one ray is the
majorisation-maximal element (`f0_vacuum_majorization`) and the unique
zero-entropy state (`epsilon_rank_one_kernel`).

**New dynamical content.** Purity is F4-invariant (`pi(g.rho) = pi(rho)` for
`g in F4 = Aut(J3(O))`, verified `~8e-14`): it depends only on the three
Freudenthal eigenvalues, so a COOLING (purity-increasing / entropy-decreasing)
flow reduces EXACTLY to a projected gradient ascent of `pi(lam) = sum lam_i^2` on
the eigenvalue simplex `{lam_i >= 0, sum lam_i = 1}`. There `pi` is strictly
convex (tangent Hessian `= 2 I`), so its only stable attractors are the three
VERTICES — the rank-one primitive idempotents (`pi = 1`). Cooling from random
states drives `pi -> 1` and the top eigenvalue `-> 1` (a rank-one vertex); the
rank-two EDGE midpoints (`pi = 1/2`) are SADDLES and the rank-three CENTRE `I/3`
(`pi = 1/3`) is a REPELLER. Perturb-and-cool confirms it: the rank-one vertex
stays put (moved `0.0`), while the rank-two and rank-three strata flee to a
vertex (moved `0.71`, `0.82`).

**Frame-breaking picks the vertex.** Cooling alone is degenerate over `OP^2`
(every rank-one vertex has `pi = 1`); a generic frame-breaking field
`V_A(P) = Tr(P o A)` then pins the unique top vertex `E1` while purity stays 1
(the height-function selection of `f4_breaking_seed_op2`, overlap `1.0000`). The
F4-invariant control `A = I` is flat (`|grad| ~ 8e-16`, no vertex selected — the
seed-gate no-go), and the HEATING control (purity descent) flows instead to the
maximally mixed `I/3` (the wrong, rank-three vacuum).

**Net.** Conditional on a COOLING (entropy-decreasing) dynamics and a GENERIC
frame-breaking field, the vacuum is FORCED to be a primitive (rank-one)
idempotent: purity's only stable attractors are the rank-one extreme points, and
the higher-rank idempotents are unstable equilibria. This turns the Peirce-jump
assumption into a dynamical consequence of cooling + frame-breaking — the same
two inputs the dissipative ladder and the seed gate already name. Deriving the
cooling direction (the arrow of time), the frame-breaking field `A`, the
generation assignment, and `pi/432` from the CHO action remains open. F0/S1 stay
open; no Bayes credit moves.
