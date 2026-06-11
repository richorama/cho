# The Octonionic Causal Algebra — Formal Definitions

## 1. The Division Algebra Chain

**Definition 1.1 (Normed Division Algebras).** The four normed division algebras over ℝ are:
- ℝ (dim 1) — real numbers
- ℂ (dim 2) — complex numbers  
- ℍ (dim 4) — quaternions (non-commutative)
- 𝕆 (dim 8) — octonions (non-commutative, non-associative)

Each is obtained from the previous via the Cayley-Dickson construction. By Hurwitz's theorem (1898), these are the *only* normed division algebras.

**Definition 1.2 (The Physics Algebra).** Define the *physics algebra*:

$$\mathcal{A} := \mathbb{C} \otimes \mathbb{H} \otimes \mathbb{O}$$

as the tensor product over ℝ. This has real dimension 2 × 4 × 8 = 64.

As a complex algebra (using the ℂ factor), it has complex dimension 32.

**Remark.** One generation of Standard Model fermions has exactly 32 complex degrees of freedom:
- 2 (weak isospin) × 3 (color) × 2 (particle/antiparticle) = 12 for quarks (×2 for up/down type = 24 complex)  
- Wait — let's count carefully:

| Particle | SU(3) | SU(2) | U(1)_Y | Count |
|----------|--------|--------|---------|-------|
| (ν_L, e_L) | 1 | 2 | -1/2 | 2 |
| e_R | 1 | 1 | -1 | 1 |
| (u_L, d_L) | 3 | 2 | 1/6 | 6 |
| u_R | 3 | 1 | 2/3 | 3 |
| d_R | 3 | 1 | -1/3 | 3 |
| + antiparticles | | | | 15 |
| **Total** | | | | **2 × 15 = 30** or **32 with ν_R** |

Including a right-handed neutrino (which neutrino masses suggest exists): **32 complex = 64 real** ✓

This is the first hint that 𝒜 encodes exactly one generation.

---

## 2. Automorphism Structure

**Definition 2.1 (Automorphism Groups).**

- Aut(ℂ) = ℤ₂ (complex conjugation)
- Aut(ℍ) = SO(3) ≅ SU(2)/ℤ₂
- Aut(𝕆) = G₂ (the smallest exceptional Lie group, dim 14)

**Proposition 2.1.** G₂ contains SU(3) as a maximal subgroup:

$$\text{SU}(3) \subset G_2 = \text{Aut}(\mathbb{O})$$

*Proof sketch.* The octonions have basis {1, e₁, e₂, ..., e₇}. The unit element 1 is fixed by all automorphisms. Choosing a preferred imaginary unit (say e₇) breaks G₂ → SU(3), which acts on the 6-dimensional space spanned by {e₁, ..., e₆} preserving e₇ and the multiplication table. □

**Proposition 2.2.** The algebra ℂ ⊗ ℍ has inner automorphisms isomorphic to SU(2) × U(1).

*Proof sketch.* ℂ contributes a U(1) phase rotation. ℍ, being non-commutative, has inner automorphisms by unit quaternions q → uqu⁻¹, which form SU(2). □

**Theorem 2.1 (Gauge Group Embedding).** The Standard Model gauge group embeds in the automorphism structure of 𝒜:

$$\frac{\text{SU}(3) \times \text{SU}(2) \times \text{U}(1)}{\mathbb{Z}_6} \hookrightarrow \text{Aut}(\mathcal{A})$$

where:
- SU(3) arises from Aut(𝕆) after fixing a preferred imaginary octonionic direction
- SU(2) arises from inner automorphisms of ℍ  
- U(1) arises from the ℂ factor

The ℤ₆ quotient matches exactly the SM quotient (the actual gauge group of nature is [SU(3)×SU(2)×U(1)]/ℤ₆, not the covering group).

**Provenance (not a novel CHO result — cite, do not claim).** Everything in §2 — the
SM gauge group as a subgroup of Aut(ℂ⊗ℍ⊗𝕆), the charge spectrum, and the
one-generation minimal-ideal state space (§5, A2/Q1) — is *established prior work* in
the division-algebra Standard Model literature, and peers grant it. It must be cited,
not presented as new:
- C. Furey (2012–2024) — SM gauge representations as minimal left ideals of ℂ⊗𝕆; the ladder-operator derivation of `SU(3)×U(1)` and `SU(2)×U(1)` and the electric-charge spectrum `Q ∈ {0, 1/3, 2/3, 1}` reproduced numerically in `compute/ladder_charges.py`.
- G. M. Dixon (1994–) — SM representation content from `ℝ⊗ℂ⊗ℍ⊗𝕆`.
- I. Todorov & M. Dubois-Violette (2018) — SM gauge group from the automorphism/structure groups of the exceptional Jordan algebra `J₃(𝕆)`.
- L. Boyle & K. Krasnov (2020–) — gauge-group and representation-level results.

CHO's own contribution begins *after* this section (the action, mass numbers, mixing
angles, and the physical three-generation identification); the gauge sector is the
shared, well-supported foundation it builds on. See `COMPARISON.md` for the
claim-by-claim grant/dispute matrix.

---

## 3. The Causal Lattice

**Definition 3.1 (Algebraic Causal Set).** An *algebraic causal set* is a triple (C, ≺, φ) where:
- C is a locally finite set (the "atoms of spacetime")
- ≺ is a partial order on C (causal relation): irreflexive, transitive, locally finite
- φ: C → 𝒜 is an *algebraic labeling* assigning to each element a state in 𝒜

**Definition 3.2 (Local Finiteness).** For any x, y ∈ C with x ≺ y, the *causal interval* [x,y] := {z ∈ C : x ≺ z ≺ y} is finite.

**Definition 3.3 (Algebraic Compatibility).** Two elements x ≺ y are *compatible* if their labels satisfy:

$$\| \phi(y) - T_{x \to y}(\phi(x)) \|_{\mathcal{A}} < \epsilon$$

where T_{x→y} is the *algebraic transport operator* (defined below) and ‖·‖_𝒜 is the norm on 𝒜 induced from the division algebra norms.

**Definition 3.4 (Algebraic Transport).** For a chain x₀ ≺ x₁ ≺ ... ≺ xₙ, the transport operator is:

$$T_{x_0 \to x_n} = L_{\phi(x_{n-1})} \circ L_{\phi(x_{n-2})} \circ \cdots \circ L_{\phi(x_0)}$$

where L_a denotes left multiplication by the *unit projection* of a:

$$L_a(b) = \frac{a}{\|a\|} \cdot b$$

**Critical observation:** Because 𝕆 is non-associative, transport around a closed loop does NOT return to the identity:

$$T_{x \to y \to z \to x} \neq \text{id}$$

The *failure of closure* is precisely the **curvature** (both gravitational and gauge).

---

## 4. The Associator as Curvature

**Definition 4.1 (Associator).** For a, b, c ∈ 𝕆, the *associator* is:

$$[a, b, c] := (ab)c - a(bc)$$

The associator vanishes iff a, b, c lie in a common quaternionic subalgebra.

**Proposition 4.1.** The associator is:
- Alternating: [a,b,c] = -[b,a,c] = -[a,c,b]
- Completely antisymmetric in its three arguments (for 𝕆)
- Related to the structure constants of 𝕆 by: [eᵢ, eⱼ, eₖ] = 2fᵢⱼₖ (where fᵢⱼₖ are the octonionic structure constants)

**Definition 4.2 (Lattice Curvature).** For a minimal closed loop (triangle) x ≺ y ≺ z with x ≺ z in the causal set, define the *curvature 3-form*:

$$\Omega(x,y,z) := [\phi(x), \phi(y), \phi(z)] \in \mathcal{A}$$

**Theorem 4.1 (Curvature Decomposition).** The curvature Ω decomposes under the gauge group as:

$$\Omega = \Omega_{\text{grav}} + \Omega_{\text{color}} + \Omega_{\text{weak}} + \Omega_{\text{em}}$$

where:
- Ω_grav lives in the part of the associator corresponding to changes in the ℝ-valued norm (scalar/tensor part)
- Ω_color lives in the SU(3) ⊂ G₂ part (imaginary octonion directions)
- Ω_weak lives in the SU(2) ⊂ Aut(ℍ) part (quaternionic directions)
- Ω_em lives in the U(1) part (complex phase)

*This is the central claim: all four forces are different projections of the same algebraic curvature.*

---

## 5. Particle States

**Definition 5.1 (Particle State).** A *particle* is a chain P = (x₀ ≺ x₁ ≺ ... ≺ xₙ) in C such that the algebraic labels {φ(xᵢ)} all lie in a *coherent subalgebra* of 𝒜.

**Definition 5.2 (Coherent Subalgebra).** A subalgebra S ⊆ 𝒜 is *coherent* if it is closed under the transport operator restricted to the chain:

$$T_{x_i \to x_{i+1}}(S) \subseteq S \quad \forall i$$

**Classification of Coherent Subalgebras of ℂ ⊗ ℍ ⊗ 𝕆:**

| Subalgebra | Real dim | Particle interpretation |
|------------|----------|------------------------|
| ℂ ⊗ 1 ⊗ 1 | 2 | Neutrino (colorless, weak singlet, has U(1) charge) |
| ℂ ⊗ ℍ ⊗ 1 | 8 | Lepton doublet (has weak charge, no color) |
| ℂ ⊗ 1 ⊗ ℍ_sub | 8 | Colored singlet (subset of octonionic directions) |
| ℂ ⊗ ℍ ⊗ ℍ_sub | 32 | Quark doublet (weak + color) |
| 1 ⊗ 1 ⊗ 1 | 1 | Graviton/scalar (pure real, no internal quantum numbers) |

Here ℍ_sub denotes a quaternionic subalgebra of 𝕆 (there are 480 such subalgebras, related by G₂ transformations — they form the 3-dimensional color representations).

---

## 6. Dynamics: The Information Action

**Definition 6.1 (Causal Information).** For an algebraic causal set (C, ≺, φ), define the *causal information functional*:

$$\mathcal{I}[C, \prec, \phi] := \sum_{\text{links } x \prec y} \log \frac{\|\phi(x)\| \cdot \|\phi(y)\|}{\|\phi(x) \cdot \phi(y) - \phi(y) \cdot \phi(x)\| + \epsilon}$$

This measures how much *non-commutativity* (= information content = interaction) exists across each causal link.

**Definition 6.2 (The Principle of Maximal Causal Information).** The physical configuration is the one that extremizes 𝒫:

$$\delta \mathcal{I} = 0$$

subject to:
- Fixed boundary conditions (initial/final algebraic states)
- Local finiteness constraint (bounded density)
- Norm conservation along worldlines (unitarity)

**Conjecture 6.1.** In the continuum limit (causal set density → ∞), the information action reduces to:

$$\mathcal{I} \to \int d^4x \sqrt{-g} \left[ \frac{R}{16\pi G} - \frac{1}{4} F_{\mu\nu}^a F^{a\mu\nu} + \bar{\psi}(i\gamma^\mu D_\mu - m)\psi - \Lambda \right]$$

i.e., the full Standard Model + GR Lagrangian, with coupling constants determined by the algebraic structure constants of 𝒜.

---

## 7. Three Generations from Triality

**Definition 7.1 (Triality).** The Lie algebra so(8) has a unique outer automorphism group S₃ (symmetric group on 3 elements) called *triality*, which permutes the three 8-dimensional representations:
- 8_v (vector)
- 8_s (positive spinor)  
- 8_c (negative spinor)

**Proposition 7.1.** The octonions are the vector representation 8_v of Spin(8). The two spinor representations correspond to:
- 8_s = left-multiplications by unit octonions
- 8_c = right-multiplications by unit octonions

**Conjecture 7.1 (Three Generations).** The three generations of fermions correspond to the three representations related by triality:

| Generation | Triality sector | Mass hierarchy origin |
|------------|----------------|----------------------|
| 1st (e, ν_e, u, d) | 8_v (vector) | Lowest norm — direct algebraic |
| 2nd (μ, ν_μ, c, s) | 8_s (left spinor) | Middle norm — one triality rotation |
| 3rd (τ, ν_τ, t, b) | 8_c (right spinor) | Highest norm — two triality rotations |

The mass hierarchy (mₜ/mᵤ ~ 10⁵) would emerge from the *breaking of triality symmetry* by the specific octonionic multiplication table (which distinguishes left from right multiplication).

> **Status update — superseded as the generation map.** Identifying the generations with the triality reps `{8_v, 8_s, 8_c}` above faces two Distler–Garibaldi-style obstructions: triality mixes the vector `8_v` with the spinors, and `8_s, 8_c` are opposite-chirality mirror partners (`compute/three_generations_nogo_audit.py`). The **count** (three) and **chirality** are instead recovered obstruction-free by an *inner*-automorphism route — the three generations are the three primitive idempotents of a `J₃(𝕆)` Jordan frame, permuted by an `S₃ ⊂ F₄`, each with a `16`-dimensional tangent equal to one real `Spin(9)` spinor `Δ₉` (Theorem A of `PAPER_JORDAN_THEOREMS.md`; `compute/three_generations_frame.py`). The map from idempotents to fermion content/masses remains open (ledger A3).

---

## Open Questions for Phase 1

1. Is the information action well-defined (bounded below, convergent sums)?
2. Does the continuum limit exist and if so, what controls it?
3. How exactly does the ℤ₆ quotient emerge from the algebraic structure?
4. Can we compute anything in closed form for small causal sets (3-5 elements)?
5. What fixes the overall scale (Planck length ↔ lattice spacing)?
