# The Discrete Internal Structure of One Standard-Model Generation from ℂ⊗ℍ⊗𝕆

**A conservative, falsifiable claim**

Richard Astbury
Developed as a human–AI collaboration (with Claude, Anthropic)
Frozen: 2026-06-07

---

## Abstract

We state and defend a deliberately narrow claim about the tensor-product
division algebra **𝒜 = ℂ⊗ℍ⊗𝕆** (64 real dimensions). We do **not** claim a theory
of the Standard Model's continuous parameters, nor a theory of everything. We
claim only that the *discrete internal structure* of one fermion generation —
its electric charges and colour multiplicities, its weak-isospin and hypercharge
assignments, its gauge-anomaly cancellation, its chirality, and the integer
**three** for the family count — is fixed by the algebra and its automorphisms
with no per-observable continuous input. Each component of this claim is backed
by an executable check that returns PASS in a single audit harness
([compute/audit.py](compute/audit.py)) and is pinned to a status ledger
([DERIVATION_LEDGER.md](DERIVATION_LEDGER.md)) with explicit kill conditions.

The algebraic content (minimal left ideals, charge operators, the gauge group)
is **established prior work** (Furey; Dixon; Dubois-Violette; Todorov; Boyle and
Krasnov); we cite it rather than claim it. Our own contribution is twofold: (i) a
**resolution of the three-generations count-and-chirality problem** that evades
the Distler–Garibaldi obstruction by identifying generations with the three
primitive idempotents of a 𝔍₃(𝕆) frame rather than with triality-permuted
representations; and (ii) two **structural theorems on the cross-generation
Yukawa operator** that delimit precisely what the algebra does and does not fix
about flavour. We are explicit throughout that the *continuous* flavour data (the
mass hierarchy and mixing magnitudes) is **not** derived here, and we localise
the single open problem to one scalar function.

---

## 1. Scope and stance

The literature on division-algebra approaches to particle physics contains a
recurring failure mode: a suggestive numerical coincidence is promoted to a
"derivation" without an accounting of how many choices were spent to reach it.
The most prominent cautionary example is the E₈ embedding of Lisi, shown by
Distler and Garibaldi to be obstructed because a single E₈ cannot contain three
generations of the correct chirality. We adopt the opposite stance: we make the
**smallest** claim the algebra actually forces, we attach a falsifiable check to
each piece, and we keep a separate, public account of everything we cannot yet
derive ([METHODOLOGY_LIMITS.md](METHODOLOGY_LIMITS.md),
[PUBLIC_CLAIMS.md](PUBLIC_CLAIMS.md)).

Concretely, this paper claims **A**, and explicitly disclaims **B**:

- **(A) — claimed.** The discrete internal quantum numbers of one generation, the
  family count `N_gen = 3` at the level of *count and chirality*, and the absence
  of a fourth generation, follow from 𝒜 and its automorphism structure.
- **(B) — disclaimed here.** The Yukawa magnitudes (fermion mass ratios), the
  mixing-angle magnitudes, the gauge couplings, the electroweak and Planck-scale
  hierarchies, and gravity are **not** derived in this paper. Where the wider
  project offers candidate bridges for these, they carry open-bridge or
  diagnostic status and are out of scope for the conservative claim.

This division is not rhetorical. It is enforced mechanically: every statement in
§3–§5 corresponds to an audit artifact whose contract
([compute/audit_contract.py](compute/audit_contract.py)) records its ledger
status, and the claim that any item in (B) is derived is registered as a *kill
condition* that would fail the audit.

---

## 2. The algebra and the one-generation module

We take the internal algebra to be 𝒜 = ℂ⊗ℍ⊗𝕆, the tensor product of the complex
numbers, quaternions, and octonions. The construction of a single fermion
generation as a space of minimal left ideals of (the complexification of) this
algebra, and the appearance of the Standard-Model gauge group
`SU(3)_c × SU(2)_L × U(1)_Y` as the subgroup of automorphisms commuting with a
fixed complex structure, are **prior results** of Furey and of Dubois-Violette,
with closely related constructions by Dixon, Todorov, and Boyle–Krasnov. We use
them as the foundation and do not reproduce or reclaim them; see
[COMPARISON.md](COMPARISON.md) for a claim-by-claim grant/dispute matrix against
that literature.

Our computational toolkit ([compute/octonion_toolkit.py](compute/octonion_toolkit.py))
builds the octonion multiplication table from the Fano plane and provides the
left/right multiplication operators used throughout. All checks below run on this
explicit table; none rely on closed-form identities we have not verified
numerically.

---

## 3. The derived discrete structure of one generation

Each subsection states a claim, the algebraic source, and the executable witness.
All witnesses return PASS.

### 3.1 Electric charge and colour multiplicity

**Claim.** The one-generation electric charges are `{0, 1/3, 2/3, 1}` with colour
multiplicities `(1, 3, 3, 1)`.

**Source.** The ℂ⊗𝕆 number operator built from the octonionic ladder (Furey;
Dubois-Violette). The eigenvalues of the charge operator and the dimensions of
its eigenspaces are read directly off the ladder.

**Witness.** [compute/ladder_charges.py](compute/ladder_charges.py) reproduces the
charges and multiplicities numerically as an *output* of the algebra (ledger
Lever C). This is the standard hypercharge filter and is granted by the prior
literature.

### 3.2 Weak isospin and hypercharge

**Claim.** The weak `SU(2)_L` acts through the ℍ factor, and the
Gell-Mann–Nishijima relation `Y = 2(Q − T₃)` then fixes the full one-generation
hypercharge spectrum.

**Source.** The quaternionic factor supplies the weak doublet structure; combined
with §3.1 it determines `Y` with no free assignment.

**Witness.** [compute/weak_isospin_hypercharge.py](compute/weak_isospin_hypercharge.py)
(ledger Lever D) derives the hypercharges; the chiral doublet/singlet split is
provided by §3.4.

### 3.3 Anomaly cancellation

**Claim.** The one-generation content assembled in §3.1–§3.2 is free of gauge
anomalies.

**Witness.** [compute/physics_map_audit.py](compute/physics_map_audit.py) freezes
the quantum-number map, verifies algebraic `Q`/`T₃`/`Y` consistency, and checks
Standard-Model anomaly cancellation (Phase 1 repair witness). The three-generation
content map and the Yukawa spectrum are left explicitly open.

### 3.4 Chirality without fermion doubling

**Claim.** The internal space carries a chiral structure of **KO-dimension 6** —
the value at which one obtains chirality without a mirror fermion.

**Source.** Building the Clifford algebra `Cl(0,7)` from octonion
left-multiplications, with the real structure given by complex conjugation, the
two real-structure signs come out `(ε, ε″) = (+1, −1)`, i.e. KO-dimension 6 — the
same value Connes' noncommutative-geometry Standard Model requires so that the
order-two axiom removes fermion doubling.

**Witness.** [compute/ko_dimension_chirality.py](compute/ko_dimension_chirality.py)
(ledger Lever B). This is the structural cure for the mirror-pair problem that
otherwise sinks generation claims (see §4).

---

## 4. The family count: three generations, count and chirality

The headline integer of the framework is `N_gen = 3`. We are careful to claim it
at exactly the level it is established — **count and chirality** — and no further.

### 4.1 Why the naive route fails

The intuitive identification "three triality representations = three generations"
is **obstructed**, and we say so first. Our own stress test
([compute/three_generations_nogo_audit.py](compute/three_generations_nogo_audit.py))
reproduces the Distler–Garibaldi failure mode: the three 8-dimensional `Spin(8)`
representations are a vector `8v` and a chirality-mirror pair of spinors
`8s, 8c`. Identifying generations with them would (i) require the outer triality
to map a vector to a spinor, and (ii) hand each generation a mirror partner. This
is the same obstruction that defeats the E₈ proposal, and it downgrades the naive
bridge to conjecture.

### 4.2 The idempotent-frame resolution

The resolution is to identify the three generations **not** with triality-permuted
representations but with the three **primitive idempotents** of a maximal frame of
the exceptional Jordan algebra 𝔍₃(𝕆) — three identical points of the Cayley
plane `OP² = F₄/Spin(9)`. Two independent results support this:

- **Spectral count (Lever A).**
  [compute/jordan_eigenvalue_generations.py](compute/jordan_eigenvalue_generations.py)
  verifies that the Freudenthal characteristic polynomial of a Hermitian 𝔍₃(𝕆)
  element is a cubic with three real roots and three orthogonal primitive
  idempotents resolving the identity (checked on 4000 random samples). "Three" is
  the **rank** of the algebra — the degree of the cubic norm — and is therefore
  immune to the representation-theoretic mirror obstruction entirely.

- **Frame equivalence and chirality (Lever A + B).**
  [compute/three_generations_frame.py](compute/three_generations_frame.py) builds
  `f₄ = Der(𝔍₃(𝕆))` (dimension 52) and the idempotent stabiliser `spin(9)`
  (dimension 36, semisimple) from the octonion table, and shows the three
  idempotents are permuted by the **inner** frame `S₃ < F₄`. Because `F₄` is
  connected with no outer automorphism, this `S₃` cannot carry a representation to
  an inequivalent one, so Obstruction (i) cannot even be posed. The 16-dimensional
  tangent space at each idempotent is a single **real** `Spin(9)` spinor `Δ₉` (the
  octonionic `Cl(9)` module, commutant dimension 1) — identical to the
  KO-dimension-6 module of §3.4 — so three identical self-conjugate copies share
  one chirality with no mirror partner, and Obstruction (ii) cannot arise either.

The `8v/8s/8c` triple that the no-go attacks is shown (PART D of the same module)
to be the **off-diagonal** Peirce decomposition, a genuinely different object that
does mix chirality — confirming the obstruction is real for the naive route and
absent for the idempotent route.

### 4.3 No fourth generation

The absence of a fourth family is a theorem conditional on the minimal-ideal
construction (ledger G2): a fourth generation would require extending to the
sedenions / 𝔍₄(𝕆), which is obstructed. With the count-and-chirality bridge now
obstruction-free, this inherits no caveat from §4.1.

### 4.4 What §4 does **not** claim

We do not claim the fermion-content map onto the tangent spinor, nor the Yukawa
spectrum. A flavour-diagonal Jordan element still returns only its seeded diagonal
(Lever A's honest negative). The count and the chirality are obstruction-free; the
*magnitudes* that distinguish the generations are the subject of §5 and remain
open.

---

## 5. The cross-generation Yukawa operator: two structural theorems

Because the three generations are *identical* points of `OP²`, nothing in §4
distinguishes them — the mass hierarchy and mixing live entirely in the Yukawa
operator. Here we contribute two **theorems** that delimit what the algebra fixes
about that operator, and we are explicit that neither closes the magnitude
problem.

### 5.1 Setup

Following the elimination argument of
[compute/spectral_action.py](compute/spectral_action.py) — a single
algebra-internal Dirac operator on the one-generation module ℂ⊗𝕆 = ℂ⁸ is
isospectral and carries **no** forced mass ratio — any algebra-internal generation
spectrum must come from the 27-dimensional 𝔍₃(𝕆) factor, with the three
generations as its primitive idempotents. The natural algebra-internal Yukawa
operators on 𝔍₃(𝕆) are the Jordan **left multiplication** `L_X : Y ↦ X∘Y` and the
canonical Jordan **quadratic representation** `U_X : Y ↦ 2X∘(X∘Y) − (X∘X)∘Y`. We
build both from the explicit 𝔍₃(𝕆) structure tensor.

### 5.2 Theorem 1 — the averaging law (additive mixing)

**Statement.** For `X = diag(a, b, c)`, the spectrum of `L_X` is exactly
`{a, b, c}` together with `{(a+b)/2, (b+c)/2, (c+a)/2}`, the latter each with
multiplicity 8. Every inter-generation level is the **arithmetic mean** of two
generation levels.

**Witness.** [compute/spectral_action_432.py](compute/spectral_action_432.py)
verifies this over 200 random seeds with residual `~10⁻⁷` and the multiplicity
pattern `[1,1,1,8,8,8]`. This is three parameter-free relations among the 27
eigenvalues (`constants_out = 3`), holding for **all** `X`.

**Consequence.** The single existing triality-breaking spurion `ε₀² = π/432`
breaks the inner `S₃` and reduces the generation freedom from three eigenvalues to
**one** scale. But because `L_X` mixing is *additive* (arithmetic means), a
one-knob `ε₀` ladder cannot reproduce a steep multiplicative hierarchy: it misses
the charged-lepton spectrum by ≈ 1.4 decades on the lightest state. The open
problem is thereby **localised to one scalar seed function** — the profile of the
three diagonal eigenvalues — with the mixing law itself derived.

### 5.3 Theorem 2 — multiplicative mixing from the quadratic operator

**Statement.** For `X = diag(a, b, c)`, the spectrum of the canonical quadratic
representation `U_X` is exactly `{a², b², c²}` together with `{ab, bc, ca}`, the
latter each with multiplicity 8. Every inter-generation level is the **geometric
mean** (product) of two generation levels.

**Witness.** [compute/spurion_perturbation.py](compute/spurion_perturbation.py)
verifies this over 200 random seeds with residual **exactly 0** and multiplicity
`[1,1,1,8,8,8]`.

**Significance.** Under `U_X`, log-mass is **additive** in the generation
exponents. Multiplicative mixing is the structural prerequisite for any power-law
hierarchy; switching from the linear Yukawa `L_X` to the canonical Jordan
quadratic `U_X` is therefore the algebraic step that *permits* a power-law ladder
at all. This is a statement about the operator, not a fit to data.

### 5.4 A companion structural fact, and an honest boundary

Two further observations sharpen — but do **not** close — the magnitude problem:

- **Rank-one bottleneck.** The project's single spurion is rank one,
  `T_break = θ|τ⟩⟨τ|`. A rank-one perturbation of a degenerate level lifts exactly
  one eigenvalue at first order (verified numerically in
  [compute/spurion_perturbation.py](compute/spurion_perturbation.py)). Hence a
  three-tier hierarchy cannot arise from one first-order insertion; the tiers must
  appear at cumulative orders `ε₀¹, ε₀², …`.

- **An exponent pattern, reported with its look-elsewhere cost.** In the *forced*
  base `ε₀ = √(π/432)`, the scheme-clean charged-lepton masses sit at exponents
  close to the triangular numbers `(0, 1, 3)` — i.e. log-mass quadratic in
  generation index — fitting to 0.33 decades, and that triangular triple is the
  only one of 28 integer triples that fits within 0.4 decades
  ([compute/epsilon_generation_ladder.py](compute/epsilon_generation_ladder.py)).
  We **do not** promote this to a law: it is **not universal** across the up and
  down quark sectors, and the quark exponents carry MS̄/scale caveats
  ([compute/mass_ratio_rg_audit.py](compute/mass_ratio_rg_audit.py)). It is a
  measured target for a future dynamical principle, not a derivation.

The honest boundary of this paper is exactly here: §5 fixes the *mixing law* and
the *operator class*, and localises the residue to one diagonal seed profile. The
**dynamical selection** of that profile is not supplied by the algebra and is the
single genuinely open research item. We state it as such rather than fitting it.

---

## 6. Honest statistical assessment

A discrete-structure claim must be defended against the charge that integers are
cheap. We therefore report the project's adversarial diagnostics rather than
suppress them.

- **Parameter count (MDL).** The framework carries roughly 17 discrete structural
  choices plus one continuous input (the Planck mass), not zero
  ([compute/model_complexity.py](compute/model_complexity.py)). The data-compression
  ratio is marginal today (`R ≈ 1.19`).

- **Goodness-of-fit on independent observables.** Once dependent rows are removed
  and a stated theory floor is applied, the independent set is statistically
  consistent (reduced `χ² ≈ 0.92`), with the first-generation electron mass a
  visible outlier ([compute/independent_observables.py](compute/independent_observables.py),
  [compute/covariance_gof.py](compute/covariance_gof.py)). The 22 nominal rows
  collapse to `N_eff ≈ 10` effective observables under the shared-`ε₀` common
  mode — we do not count them as 22 independent successes.

- **Model-comparison Bayes factor.** Crediting only the numerically-closed
  discrete results (the conservative floor of this paper), the Bayes factor
  against an O(1)-numerology null is approximately `ln B ≈ −3`; it becomes `+6`
  only if the geometric origin of `π/432` is granted
  ([compute/bayesian_evidence.py](compute/bayesian_evidence.py),
  [compute/scoreboard.py](compute/scoreboard.py)). The verdict therefore hinges on
  a single named seam, which we keep on the disclaimed side (B). The conservative
  paper does **not** rely on `ln B > 0`.

- **Look-elsewhere on scale relations.** The power-of-three scale hits
  (`M_W, M_R, Λ`) are *cheap*: a simple prefactor times an integer exponent
  already covers ≈ 93% of one exponent window
  ([compute/scale_look_elsewhere.py](compute/scale_look_elsewhere.py)). These are
  explicitly **not** part of claim (A).

The conservative claim survives all of these because it rests on **discrete**,
structure-level results (charges, multiplicities, anomaly cancellation,
KO-dimension, the rank-three count) whose evidential weight does not depend on the
continuous-parameter accounting that the diagnostics (correctly) discount.

---

## 7. What this paper does not claim

For the avoidance of doubt, and as a matter of audit policy, the following are
**not** claimed here and are registered as kill conditions in the contract:

1. The fermion mass ratios / Yukawa eigenvalue magnitudes are not derived (§5.4).
2. The mixing-angle magnitudes are not derived; the integer multiplicities
   `√7, ½, 3, 4` and `4/7` in the wider project are open bridges, not closed.
3. `ε₀² = π/432` is not claimed as geometrically forced; it is an open bridge.
4. The gauge couplings and the electroweak / Planck-scale hierarchies are not
   derived; the relevant rows carry continuum/RG-matching gaps obtained partly by
   inverse running.
5. Gravity is out of scope: the internal metric brick yields no canonical 4D
   Lorentzian reduction or dynamics
   ([compute/gravity_gate_audit.py](compute/gravity_gate_audit.py)).

---

## 8. Conclusion

The defensible result of the ℂ⊗ℍ⊗𝕆 program is sharp and small: the **discrete
internal anatomy of one Standard-Model generation** — charges, colour, weak
isospin, hypercharge, anomaly freedom, and chirality — together with the family
count `N_gen = 3` at the level of count and chirality and the exclusion of a
fourth family, is fixed by the algebra and its automorphisms. The
three-generations result is made obstruction-free by identifying generations with
the primitive idempotents of a 𝔍₃(𝕆) frame, evading the Distler–Garibaldi
no-go that defeats representation-counting routes.

Our new contribution to the flavour question is honest delimitation rather than
solution: the cross-generation Yukawa obeys a derived **averaging law** under
linear Jordan multiplication and a derived **multiplicative-mixing law** under the
canonical quadratic operator, and the rank-one spurion forces any hierarchy to be
cumulative. These results reduce the open flavour problem from "derive the entire
Yukawa spectrum" to "supply a dynamical principle selecting one diagonal seed
profile." That residual is stated plainly as the program's lone high-risk open
item — not papered over with a fit.

We regard this conservative claim as the correct unit of publication: every
component is individually falsifiable, mechanically audited, and free of the
overreach that has historically discredited algebraic approaches to the Standard
Model.

---

## Reproducibility

All claims are checked by a single harness:

```
PYTHONDONTWRITEBYTECODE=1 python3 compute/audit.py          # run every artifact
PYTHONDONTWRITEBYTECODE=1 python3 compute/audit.py <name>   # run one
PYTHONDONTWRITEBYTECODE=1 python3 compute/audit_contract.py # validate contracts
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests
```

Status of every claim is pinned in [DERIVATION_LEDGER.md](DERIVATION_LEDGER.md);
public-claim policy is in [PUBLIC_CLAIMS.md](PUBLIC_CLAIMS.md); caveats are in
[METHODOLOGY_LIMITS.md](METHODOLOGY_LIMITS.md). Numerical inputs use NumPy only.

## References (prior work cited, not claimed)

1. C. Furey, *Standard model physics from an algebra?*, PhD thesis (2015), and
   subsequent papers on ℂ⊗ℍ⊗𝕆 minimal ideals and `SU(3)×SU(2)×U(1)`.
2. G. M. Dixon, *Division Algebras: Octonions, Quaternions, Complex Numbers and
   the Algebraic Design of Physics* (1994).
3. M. Dubois-Violette, *Exceptional quantum geometry and particle physics* (2016);
   M. Dubois-Violette and I. Todorov, papers on 𝔍₃(𝕆) and the Standard Model.
4. J. C. Baez and J. Huerta, *The algebra of grand unified theories* (2010).
5. L. Boyle and K. Krasnov, work on octonionic and `Spin` structures for the
   Standard Model.
6. A. Connes, *Noncommutative geometry and the Standard Model with neutrino
   mixing* (2006); Chamseddine–Connes spectral action and KO-dimension 6.
7. J. Distler and S. Garibaldi, *There is no "Theory of Everything" inside E₈*
   (2010) — the no-go benchmark this paper is built to respect.
