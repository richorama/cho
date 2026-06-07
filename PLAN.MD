# Aspirational Theory of Everything Research Plan

> **Scope note (2026-06-06).** The title is
> **aspirational**, not a present-day claim. The framework currently has no dynamical gravity, so the
> defensible present-day description is "an algebraic framework for Standard Model
> parameters from division algebras" (see [README.md](README.md) and
> [CRITICAL_REPAIR_PLAN.md](CRITICAL_REPAIR_PLAN.md) Phase 5). The gravity goals in Phase 3 are a scoped,
> optional research line tracked in [foundations/03_gravity.md](foundations/03_gravity.md);
> the "Theory of Everything" branding is conditional on that line producing a
> metric/curvature sector. Treat Phases 1-2 (Standard Model parameters) as the
> live program and Phase 3 (gravity/cosmology) as exploratory.

## The Problem

Unite quantum mechanics, the Standard Model of particle physics, and general relativity into a single coherent mathematical framework that:

1. Reproduces all known physics (SM particle spectrum, coupling constants, GR in classical limit)
2. Explains currently unexplained observations (dark matter, dark energy, baryon asymmetry, neutrino masses, hierarchy problem)
3. Makes novel testable predictions
4. Is mathematically consistent (finite, anomaly-free, background-independent)

---

## Observational Constraints (Non-Negotiable)

Any candidate theory MUST reproduce or explain:

| Domain | Data |
|--------|------|
| Particle physics | 3 generations of fermions, gauge group SU(3)×SU(2)×U(1), CKM/PMNS mixing matrices, 19+ free parameters of SM |
| Gravity | Einstein field equations in classical limit, gravitational waves (LIGO/Virgo chirp masses), perihelion precession, frame dragging |
| Cosmology | CMB power spectrum (Planck), BAO, accelerating expansion (Λ ≈ 10⁻¹²² in natural units), flat spatial geometry |
| Quantum | Bell inequality violations, entanglement, decoherence, Lamb shift, g-2 of electron/muon |
| Unexplained | Dark matter (~27% energy density), dark energy (~68%), matter-antimatter asymmetry, neutrino oscillations/masses, muon g-2 anomaly |

---

## Core Thesis: Algebraic Emergence from Discrete Causal Information Geometry

**Central idea:** Spacetime, particles, and forces all emerge from a single pre-geometric algebraic structure — a *causal information lattice* equipped with division algebra grading.

This combines three under-explored mathematical directions:

### Pillar 1 — Division Algebras as Origin of Particle Spectrum

The four normed division algebras (ℝ, ℂ, ℍ, 𝕆) have deep unexploited connections to physics:
- ℂ ⊗ ℍ ⊗ 𝕆 has exactly the right algebraic dimension (32 complex = 64 real) to encode one generation of SM fermions + their antiparticles
- The automorphism group of 𝕆 is G₂, which contains SU(3) — color gauge group
- The exceptional Jordan algebra J₃(𝕆) has dimension 27 and its symmetry group is F₄/E₆

**New math needed:** Develop a *graded tensor product* of division algebras with a dynamical norm that generates gauge couplings as algebraic invariants rather than free parameters.

### Pillar 2 — Causal Set + Algebraic Combinatorics

Replace continuous spacetime manifold with a locally-finite partial order (causal set), but enrich each element with division algebra-valued state:
- Each "atom of spacetime" carries an octonionic label
- Causal relations between atoms defined by algebraic compatibility (non-associativity of 𝕆 generates curvature)
- Particle worldlines = chains in the causal set where algebraic labels form coherent subalgebras
- Gauge fields = holonomy of the algebraic grading around closed chains

**New math needed:** *Non-associative causal combinatorics* — a theory of partially ordered sets with non-associative algebraic decorations, where macroscopic geometry emerges statistically.

### Pillar 3 — Information-Theoretic Dynamics

The dynamics (equations of motion) should not be imposed but derived from an information-theoretic principle:
- **Principle:** The universe evolves to maximize the rate of causal information integration (a generalization of Integrated Information Theory to algebraic causal sets)
- This replaces the action principle — the action functional should be *derivable* from the information measure
- Quantum mechanics (superposition, interference) emerges from coarse-graining over consistent causal histories (similar to sum-over-histories but discrete and algebraically constrained)

**New math needed:** An *algebraic information measure* on non-associative causal lattices that reduces to:
- Shannon entropy in classical limit
- von Neumann entropy for quantum subsystems
- Bekenstein-Hawking entropy for causal horizons

---

## Research Phases

### Phase 1: Mathematical Foundations (Months 1–3)

- [ ] **1.1** Construct the algebraic framework
  - Define the octonionic causal lattice formally
  - Prove that SU(3)×SU(2)×U(1) emerges from automorphism structure of ℂ⊗ℍ⊗𝕆 with a specific symmetry-breaking pattern
  - Classify all possible "particle states" as irreducible sub-algebras

- [ ] **1.2** Develop non-associative differential calculus
  - Define discrete derivatives on causal sets with octonionic labels
  - Show curvature emerges from non-associativity (the associator [a,b,c] = (ab)c - a(bc) as torsion/curvature analog)
  - Prove continuum limit recovers Riemannian geometry + gauge connection

- [ ] **1.3** Formulate the information-theoretic action
  - Define causal information integration for algebraic causal sets
  - Derive Euler-Lagrange-like equations from extremizing information measure
  - Show equivalence to Einstein-Hilbert + Yang-Mills + Dirac in appropriate limits

### Phase 2: Particle Physics Derivation (Months 3–6)

- [ ] **2.1** Derive the particle spectrum
  - Show 3 generations emerge from triality of SO(8) (the rotation group of 𝕆)
  - Compute mass ratios from algebraic invariants (norms, traces of Jordan algebra elements)
  - Derive CKM/PMNS mixing from octonionic multiplication table ambiguities

- [ ] **2.2** Compute coupling constants
  - Derive α_em, α_s, α_w at some scale from algebraic structure constants
  - Show running of couplings (RG flow) emerges from coarse-graining the causal lattice
  - Predict gauge coupling unification scale (or explain why they don't exactly unify)

- [ ] **2.3** Address the hierarchy problem
  - Show the Higgs mass is stabilized by algebraic constraints (the norm in J₃(𝕆) is bounded)
  - Derive Higgs VEV from minimizing information measure over scalar sector
  - Explain why gravity is weak: gravitational DOF = collective/emergent, suppressed by lattice density

### Phase 3: Gravity and Cosmology (Months 6–9)

- [ ] **3.1** Derive general relativity
  - Show Einstein equations emerge as thermodynamic/information equations of state for the causal lattice (extending Jacobson's thermodynamic derivation)
  - Compute quantum corrections (these should be finite by construction — no UV divergences in discrete theory)
  - Address background independence explicitly

- [ ] **3.2** Cosmological predictions
  - Derive cosmological constant from information-theoretic ground state of the lattice
  - Show dark energy = residual information integration of the vacuum lattice
  - Model dark matter as algebraic defects (elements with non-standard subalgebra embedding — "misaligned" octonionic labels that interact gravitationally but not via SM gauge groups)

- [ ] **3.3** Black hole information
  - Show information is preserved in the causal lattice (no information paradox by construction)
  - Derive Bekenstein-Hawking entropy from counting lattice microstates
  - Predict corrections to Hawking radiation spectrum

### Phase 4: Predictions and Tests (Months 9–12)

- [ ] **4.1** Novel predictions
  - Compute proton decay rate (or prove stability) from algebraic selection rules
  - Predict new particles (if any) from unused algebraic representations
  - Derive neutrinoless double beta decay rate from Majorana nature implied by algebra
  - Predict deviations from SM at specific energy scales

- [ ] **4.2** Cosmological signatures
  - Predict specific non-Gaussianities in CMB from discrete causal structure
  - Compute gravitational wave background from phase transitions in algebraic structure
  - Predict modifications to gravitational wave propagation at extreme frequencies

- [ ] **4.3** Consistency checks
  - Verify anomaly cancellation
  - Check unitarity and causality
  - Prove finiteness (no renormalization needed in discrete theory, but must show continuum limit is controlled)

---

## Key Mathematical Tools to Develop

1. **Octonionic Fiber Bundles** — fiber bundles where the fiber is non-associative; need new theory of connections and holonomy
2. **Non-Associative Homological Algebra** — chain complexes over octonions don't work naively; need weakened exactness conditions
3. **Causal Set Spectral Theory** — analog of spectral geometry (à la Connes) for causal sets with algebraic decoration
4. **Information Cohomology** — cohomological formulation of information measures on algebraic lattices
5. **Exceptional Periodicity Arithmetic** — number-theoretic structure of exceptional algebras that may fix coupling constants

---

## Why This Might Work (Where Others Failed)

| Previous approach | Why it stalled | How we differ |
|---|---|---|
| String theory | Too many vacua (10⁵⁰⁰), no unique predictions, requires SUSY (not found) | We derive spectrum algebraically — no landscape, no SUSY required |
| Loop quantum gravity | Gets gravity right but can't naturally include matter/SM | We start from algebra that contains BOTH geometry and matter |
| Noncommutative geometry (Connes) | Beautiful but still mostly continuous, struggles with gravity dynamics | We go fully discrete + non-associative, not just noncommutative |
| Causal set theory | Too sparse — hard to get matter content | We enrich causal sets with algebraic structure that encodes particles |
| Asymptotic safety | May work for gravity but doesn't address why SM has its specific structure | We derive SM structure, not just gravity |

---

## Immediate Next Steps

1. **Write formal definitions** of the octonionic causal lattice (rigorous math, not hand-waving)
2. **Prove the first theorem:** SU(3)×SU(2)×U(1) ⊂ Aut(ℂ⊗ℍ⊗𝕆) with correct representations for one generation
3. **Build computational tools** to enumerate small causal lattices and verify emergence numerically
4. **Literature review checkpoint:** Verify we're not duplicating Furey (2012-2024), Boyle (2020), or Todorov & Dubois-Violette

---

## Success Criteria

The theory succeeds if it can:
- [ ] Derive all 19 free parameters of the SM from a few explicit inputs/bridge assumptions, with no row-by-row fitted low-energy parameters
- [ ] Predict at least one currently unmeasured quantity that is subsequently verified
- [ ] Resolve the cosmological constant problem (predict Λ within an order of magnitude)
- [ ] Be falsifiable — state clearly what observations would rule it out

---

## References and Inspirations

- Furey, C. — Division algebras and the Standard Model (ℂ⊗ℍ⊗𝕆 approach)
- Connes, A. — Noncommutative geometry and SM
- Sorkin, R. — Causal set theory
- Jacobson, T. — Thermodynamic derivation of Einstein equations
- Baez, J. — Octonions and exceptional Lie algebras
- Boyle, L. — Cosmological CPT symmetry and mirror universe
- Tononi, G. — Integrated Information Theory (for information-theoretic dynamics inspiration)
- Wolfram, S. — Computational universe / hypergraphs (for discrete emergence ideas)
