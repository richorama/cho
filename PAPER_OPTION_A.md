# The Discrete Internal Structure of One Standard-Model Generation in ℂ⊗ℍ⊗𝕆

**A conservative, falsifiable claim**

Richard Astbury
Developed with the assistance of AI tools
Frozen: 2026-06-07

---

## Abstract

We state and defend a deliberately narrow claim about the tensor-product
division algebra **𝒜 = ℂ⊗ℍ⊗𝕆** (64 real dimensions). We do **not** claim a theory
of the Standard Model's continuous parameters, nor a theory of everything. We
claim only that the *discrete internal structure* of one fermion generation —
its electric charges and colour multiplicities, its weak-isospin and hypercharge
assignments, its gauge-anomaly cancellation, and its chirality — is determined,
once a complex structure is fixed, by 𝒜 and its automorphisms, with no
per-observable continuous input. The family count **three** enters separately, as
the **rank** of the exceptional Jordan algebra 𝔍₃(𝕆), which we adopt — following
Dubois-Violette–Todorov and Boyle — rather than derive from 𝒜; we are explicit
that connecting the two algebras is an **open bridge**, not a theorem. We are
equally explicit that this is a constrained discrete model space, not a
parameter-free theory: the construction rests on a fixed complex structure and on
the order of seventeen discrete algebraic choices (§6). Each component of this claim is backed
by an executable check that returns PASS in a single audit harness
([compute/audit.py](compute/audit.py)) and is pinned to a status ledger
([DERIVATION_LEDGER.md](DERIVATION_LEDGER.md)) with explicit kill conditions.

The algebraic content (minimal left ideals, charge operators, the gauge group)
is **established prior work** (Furey; Dixon; Dubois-Violette and Todorov; Boyle);
we cite it rather than claim it. Our own contribution is twofold: (i) a
**resolution of the three-generations count-and-chirality problem** that evades
the Distler–Garibaldi obstruction by identifying generations with the three
primitive idempotents of a 𝔍₃(𝕆) frame rather than with triality-permuted
representations; and (ii) two **elementary lemmas on the cross-generation
Yukawa operator** that delimit precisely what the algebra does and does not fix
about flavour — in particular, that it fixes a mixing **law** but selects no
hierarchy. We are explicit throughout that the *continuous* flavour data (the
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

- **(A) — claimed.** Once a complex structure is fixed, the discrete internal
  quantum numbers of one generation — charges, colour, weak isospin, hypercharge,
  anomaly freedom, and chirality — follow from 𝒜 and its automorphism structure.
  The family count `N_gen = 3`, at the level of *count and chirality*, and —
  conditionally — the absence of a fourth family, follow instead from the rank of
  an *adopted* 𝔍₃(𝕆) frame; connecting that frame to 𝒜 is an open bridge (§4).
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
with closely related constructions by Dixon, Todorov, and Boyle. We use
them as the foundation and do not reproduce or reclaim them; see
[COMPARISON.md](COMPARISON.md) for a claim-by-claim grant/dispute matrix against
that literature. The choice of complex structure is the step that singles out the
Standard-Model gauge subgroup; we adopt Furey's choice and do not here examine
which complex structure is selected, or why.

Our computational toolkit ([compute/octonion_toolkit.py](compute/octonion_toolkit.py))
builds the octonion multiplication table from the Fano plane and provides the
left/right multiplication operators used throughout. All checks below run on this
explicit table; none rely on closed-form identities we have not verified
numerically.

Our own contribution begins only in §4 and §5. The one-generation gauge content
of §3 is inherited from the works above; we include it for completeness and to fix
notation, and we claim no novelty for it.

---

## 3. The derived discrete structure of one generation

Each subsection states a claim, the algebraic source, and the executable witness.
(Terminology, from the project's audit infrastructure: a *witness* is the
executable script that checks a claim; the *ledger* records each claim's status; a
*kill condition* is a pre-registered statement whose truth would falsify a claim; a
*contract* ties a witness to its ledger status; and "Lever A/B/C/D" are internal
labels for four specific one-generation results — the charge ladder, the
KO-dimension-6 chirality, the spectral generation count, and weak isospin and
hypercharge.) All witnesses return PASS. We stress that a witness is a
reproducibility and consistency check on an explicit finite-dimensional
computation — it verifies the stated representations, spectra, and multiplicities
to machine precision and, for the inherited results of this section, reproduces the
prior-work derivations rather than independently *forcing* them — and is not, by
itself, a substitute for proof. The two genuinely novel claims of §5 are
accordingly accompanied by short proofs, not only witnesses.

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

**Two algebras, and the bridge between them.** A point of honesty must come first.
§§2–3 build one generation inside 𝒜 = ℂ⊗ℍ⊗𝕆, whose relevant module is ℂ⊗𝕆 = ℂ⁸
(16 real dimensions). The generation *count* of this section, by contrast, lives
in the exceptional Jordan algebra 𝔍₃(𝕆) (27 real dimensions), which is **not** a
subalgebra or a tensor factor of 𝒜 — indeed 27 ∤ 64. We do not derive 𝔍₃(𝕆) from
𝒜; we adopt it as an additional algebraic structure, following
Dubois-Violette–Todorov and Boyle, motivated by the observation below that the
tangent space at each of its primitive idempotents is a real `Spin(9)` spinor
Δ₉ ≅ ℂ⊗𝕆 — the same 16-dimensional one-generation module. The integer "three" is
therefore the **rank** of 𝔍₃(𝕆); reading it as the Standard-Model family count, and
identifying 𝔍₃(𝕆) with the generation structure of 𝒜, is an **open bridge**, not a
theorem. We flag this prominently because the claim is otherwise easily over-read:
the count follows from positing a rank-three object, and what 𝒜 contributes is the
one-generation module that sits at each idempotent.

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

**Relation to Boyle and Dubois-Violette–Todorov.** The closest prior work places
one generation in (the tangent space of) the complex exceptional Jordan algebra
and relates the *three* generations to `SO(8)` triality: Boyle states exactly
this, and Dubois-Violette–Todorov locate the three families in the three
off-diagonal octonionic directions of 𝔍₃(𝕆). By the analysis above, those are
precisely the objects (`8v, 8s, 8c`; the off-diagonal Peirce slots) on which the
Distler–Garibaldi obstruction bites. Our contribution is narrow and specific: the
*same count* is available *without* triality, from the three *diagonal* primitive
idempotents of a single real 𝔍₃(𝕆) frame, permuted by an *inner* `S₃ < F₄`. We do
not claim a different or better physical generation structure than these works —
only a different, obstruction-free *route to the count*. The price is real, and we
state it: because the three idempotents are `F₄`-equivalent, this structure carries
**no** flavour information beyond the integer three (all flavour must come from the
symmetry-breaking of §5) — arguably weaker, in that respect, than triality routes
in which `8v, 8s, 8c` are at least distinct objects.

### 4.3 No fourth generation

This is the most conditional of our claims, and we flag it as such. Within the
present construction the family count is the **rank** of the Jordan algebra, and
that rank is capped at three for a structural reason: the Hermitian n×n octonionic
matrices Hₙ(𝕆) satisfy the Jordan axioms only for n ≤ 3 (Jordan–von
Neumann–Wigner); there is no exceptional Jordan algebra 𝔍₄(𝕆), and the naive
extension passes to the non-alternative sedenions. A fourth family is therefore
excluded *relative to* the identification of generations with a
primitive-idempotent frame of 𝔍₃(𝕆) (ledger G2). We state it as a conditional
exclusion, not an unconditional no-go: it would not bind if generations were
realised by some construction other than such a frame.

### 4.4 What §4 does **not** claim

We do not claim the **fermion-content map**: the assignment of the 16 real
dimensions of Δ₉ to the 16 Weyl fields of one Standard-Model generation, *with
their correct chiral gauge action*, is not established here. Until that map exists,
the result of this section is a counting statement about the three primitive
idempotents of a 𝔍₃(𝕆) frame — together with the verified fact that their tangent
spaces are three identical real `Spin(9)` spinors — rather than a statement about
three Standard-Model generations. A flavour-diagonal Jordan element still returns
only its seeded diagonal (an honest negative). The count and the chirality *type*
are obstruction-free; the content map and the *magnitudes* that distinguish the
generations are the subject of §5 and remain open.

---

## 5. The cross-generation Yukawa operator: two elementary lemmas

Because the three generations are *identical* points of `OP²`, nothing in §4
distinguishes them — the mass hierarchy and mixing live entirely in the Yukawa
operator. Here we record two **elementary lemmas** that delimit what the algebra
fixes about that operator. Both are immediate from the diagonal action on the
Peirce slots (the proofs are two lines each); we state them carefully because
their *net* content — that the algebra fixes a mixing law but selects no
hierarchy — is the honest boundary of what 𝔍₃(𝕆) contributes to flavour.

### 5.1 Setup

A single algebra-internal Dirac operator on the one-generation module ℂ⊗𝕆 = ℂ⁸
is isospectral and carries **no** forced mass ratio (the elimination argument of
[compute/spectral_action.py](compute/spectral_action.py)); a generation spectrum
must therefore come from a structure that carries the three families, which in the
present setting is the 𝔍₃(𝕆) frame of §4 — with the three generations as its
primitive idempotents, subject to the open bridge flagged there. The natural algebra-internal Yukawa
operators on 𝔍₃(𝕆) are the Jordan **left multiplication** `L_X : Y ↦ X∘Y` and the
canonical Jordan **quadratic representation** `U_X : Y ↦ 2X∘(X∘Y) − (X∘X)∘Y`. We
build both from the explicit 𝔍₃(𝕆) structure tensor.

### 5.2 Lemma 1 — the averaging law (additive mixing)

**Statement.** For `X = diag(a, b, c)`, the spectrum of `L_X` is exactly
`{a, b, c}` together with `{(a+b)/2, (b+c)/2, (c+a)/2}`, the latter each with
multiplicity 8. Every inter-generation level is the **arithmetic mean** of two
generation levels.

**Proof sketch.** In the diagonal frame, 𝔍₃(𝕆) decomposes as the three real
diagonal entries together with the three off-diagonal octonionic slots z₁, z₂, z₃
(each ≅ 𝕆 ≅ ℝ⁸), giving 3 + 24 = 27. For `X = diag(a, b, c)` the Jordan product
`X∘Y = ½(XY + YX)` acts on a diagonal entry yᵢᵢ as multiplication by xᵢ, and on a
slot entry yᵢⱼ (i ≠ j) as `(X∘Y)ᵢⱼ = ½(xᵢ yᵢⱼ + yᵢⱼ xⱼ) = ½(xᵢ + xⱼ) yᵢⱼ`, since
the xᵢ are real and commute with octonions. Hence `L_X` is block-diagonal in this
decomposition, with eigenvalues a, b, c on the diagonal entries and (a+b)/2,
(b+c)/2, (c+a)/2 on the three 8-dimensional slots. The averaging law and the
multiplicities `[1,1,1,8,8,8]` follow. ∎

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

### 5.3 Lemma 2 — multiplicative mixing from the quadratic operator

**Statement.** For `X = diag(a, b, c)`, the spectrum of the canonical quadratic
representation `U_X` is exactly `{a², b², c²}` together with `{ab, bc, ca}`, the
latter each with multiplicity 8. Every inter-generation level is the **geometric
mean** (product) of two generation levels.

**Proof sketch.** Write s = ½(xᵢ + xⱼ) for the scalar by which `X∘(·)` acts on the
slot yᵢⱼ (proof of Lemma 1), and note `X∘X = diag(a², b², c²)` acts there as
t = ½(xᵢ² + xⱼ²). The quadratic representation `U_X Y = 2 X∘(X∘Y) − (X∘X)∘Y` then
acts on yᵢⱼ as `2s² − t = ½(xᵢ + xⱼ)² − ½(xᵢ² + xⱼ²) = xᵢ xⱼ`, and as xᵢ² on the
diagonal entries. The product (geometric-mean) law and the multiplicities
`[1,1,1,8,8,8]` follow. ∎

**Witness.** [compute/spurion_perturbation.py](compute/spurion_perturbation.py)
verifies this over 200 random seeds with residual **exactly 0** and multiplicity
`[1,1,1,8,8,8]`.

**Significance.** Under `U_X`, log-mass is **additive** in the generation
exponents. Multiplicative mixing is the structural prerequisite for any power-law
hierarchy; switching from the linear Yukawa `L_X` to the canonical Jordan
quadratic `U_X` is therefore the algebraic step that *permits* a power-law ladder
at all. We are candid that the *motivation* for preferring `U_X` is
phenomenological — one wants multiplicativity because the observed hierarchy is
roughly power-law; the lemma itself, however, is a fixed property of the operator,
independent of any data. Neither lemma *selects* a hierarchy: the off-diagonal
levels are means or products of (a, b, c), so all hierarchy must be seeded in the
diagonal profile, which the algebra leaves unexplained.

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

The defensible *content* of the ℂ⊗ℍ⊗𝕆 program is sharp and small: the **discrete
internal anatomy of one Standard-Model generation** — charges, colour, weak
isospin, hypercharge, anomaly freedom, and chirality — is determined, once a
complex structure is fixed, by the algebra and its automorphisms; and the family
count `N_gen = 3`, at the level of count and chirality, is the rank of a 𝔍₃(𝕆)
frame whose primitive idempotents are permuted by an inner `S₃`, evading the
Distler–Garibaldi no-go that defeats representation-counting routes. We are
explicit that this last step rests on adopting 𝔍₃(𝕆) (an open 𝒜 → 𝔍₃(𝕆) bridge
and an unestablished fermion-content map) and that the `F₄`-equivalent idempotents
carry no flavour information beyond the integer three.

Our new contribution to the flavour question is honest delimitation rather than
solution: the cross-generation Yukawa obeys an **averaging law** under linear
Jordan multiplication and a **multiplicative-mixing law** under the canonical
quadratic operator, and the rank-one spurion forces any hierarchy to be
cumulative. These results reduce the open flavour problem from "derive the entire
Yukawa spectrum" to "supply a dynamical principle selecting one diagonal seed
profile." That residual is stated plainly as the program's lone high-risk open
item — not papered over with a fit.

We stress, finally, what this paper does **not** establish: a *positive*
evidential case. Scored honestly (§6), the conservative results do not beat an
O(1)-numerology null (`ln B ≈ −3.2`) unless the geometric origin of `π/432` is
granted — which we keep on the disclaimed side (B). The content here is therefore
offered as a precise, falsifiable *delimitation* of what ℂ⊗ℍ⊗𝕆 and 𝔍₃(𝕆) do and
do not fix, not as positive evidence for the framework. We regard that
delimitation as the correct unit of publication: every component is individually
falsifiable, the inherited results are attributed rather than reclaimed, and the
open bridges are named rather than papered over.

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
8. A. G. Lisi, *An Exceptionally Simple Theory of Everything* (2007) — the
   proposal whose obstruction (ref. 7) this paper is built to respect.
9. P. Jordan, J. von Neumann, and E. Wigner, *On an algebraic generalization of
   the quantum mechanical formalism*, Ann. Math. **35** (1934) 29–64 — the
   classification capping Hₙ(𝕆) at n ≤ 3.
