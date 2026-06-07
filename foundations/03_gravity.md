# The Gravity Sector: Scoped Research Line (Currently Out of Scope)

Created: 2026-06-06 (legacy repair-pass Tier 4, item T4.2)

Status: **research line, not a result.** CHO still has **no dynamical
gravity.** A first *kinematic* brick now exists, however
([`compute/gravity_curvature.py`](../compute/gravity_curvature.py), milestone
M-GRAV below, ledger row GR1): a symmetric, positive-semidefinite, **G₂-covariant
rank-2 metric perturbation** emerges from the octonionic associator with **no
hand-inserted geometric input**. This note states honestly what exists (now a
candidate mechanism *plus* a verified kinematic metric) and what remains (the
load-bearing continuum conjecture, the reduction to 4-d spacetime, and all
dynamics).

**Phase 5 update (2026-06-07):** [`foundations/11_gravity_gate.md`](11_gravity_gate.md)
and [`compute/gravity_gate_audit.py`](../compute/gravity_gate_audit.py) trigger
the down-scope condition. The internal metric is kinematically valid, but no
canonical `G2`-invariant four-plane, Lorentzian signature, field equation, or
Newton constant emerges. Gravity remains out of scope for the present framework
and should be treated as a separate exploratory line.

This note exists so the word "gravity" is backed by an explicit, bounded
research target and by a real computation rather than by the placeholder script
[`compute/graviton.py`](../compute/graviton.py).

---

## 1. What exists today (and its status)

| Ingredient | Where | Status |
|---|---|---|
| Associator as curvature: `Ω(x,y,z) = [φ(x),φ(y),φ(z)]` | `01_algebra.md` §4 | **Definition**, motivated; not yet a metric |
| Curvature decomposition `Ω = Ω_grav + Ω_color + Ω_weak + Ω_em` | `01_algebra.md` §4, Thm 4.1 | **Claim**, not derived; `Ω_grav` = scalar/norm part of the associator |
| Information action `I[C,≺,φ]` and "maximal causal information" | `01_algebra.md` §6 | **Definition + variational principle**, no continuum proof |
| Continuum limit `I → ∫√-g (R/16πG − ¼F² + ψ̄(iD̸−m)ψ − Λ)` | `01_algebra.md` §6, Conj 6.1 | **Conjecture**, unproven — this is the whole game |
| `compute/graviton.py` | repo | **Placeholder**, superseded by `gravity_curvature.py` for the metric brick |
| Emergent metric `g_μν(a,b) = ⟨[e_μ,a,b],[e_ν,a,b]⟩` (Gram of associator) | `compute/gravity_curvature.py` | **Verified kinematic result** (symmetric, PSD, G₂-covariant rank-2; `tr g = 16|a∧b|²`); reduction to spacetime still open |

The honest summary: there is a *candidate* mechanism (non-associativity →
curvature; information action → Einstein–Hilbert in the continuum) but **no
computed metric, no curvature invariant, and no flat-space limit check.**
Conjecture 6.1 is the load-bearing unproven step.

---

## 2. The candidate mechanism (what would have to be true)

Two known ideas are invoked and would need to be made concrete for CHO:

1. **Non-associativity as curvature.** The octonionic associator
   `[a,b,c] = (ab)c − a(bc)` vanishes iff `a,b,c` lie in a common quaternionic
   subalgebra. The proposal (`01_algebra.md` §4) is that its **scalar/norm
   projection** `Ω_grav` plays the role of Riemann curvature on the causal
   lattice, while the imaginary-octonion / quaternion / complex projections give
   the gauge curvatures. For this to be gravity, `Ω_grav` must define a
   **symmetric rank-2 metric perturbation** with the correct continuum
   transformation law — currently unshown.

2. **Thermodynamic / information emergence (Jacobson-style).** Jacobson (1995)
   derived the Einstein equations as an equation of state from `δQ = T δS` across
   local causal horizons. The CHO information action `I` is meant to play the
   role of the entropy functional whose extremization yields the field equations
   in the continuum limit (Conjecture 6.1). Making this rigorous requires a
   controlled coarse-graining of the algebraic causal set with a defined notion
   of horizon area.

---

## 3. Minimal computable deliverable (the actual T4.2 target)

To justify the word "gravity" beyond a placeholder, the smallest honest
milestone is:

> **M-GRAV.** Define the discrete connection/transport on a small algebraic
> causal set, compute **one** curvature invariant from the associator
> projection `Ω_grav`, and exhibit its **flat-space limit** (a configuration
> where `Ω_grav → 0` and transport becomes path-independent).

Concretely, in code this means extending `octonion_toolkit.py` to:

1. build a minimal causal triangle `x ≺ y ≺ z` with octonionic labels;
2. compute `Ω(x,y,z) = [φ(x),φ(y),φ(z)]` and extract the scalar/norm projection
   `Ω_grav`;
3. show that when the three labels lie in a common quaternionic subalgebra
   `Ω_grav = 0` (flat), and that it is nonzero otherwise (curved);
4. check that `Ω_grav` aggregated over a coherent region transforms as a scalar
   curvature density under the `G₂`/Lorentz action, to leading order.

Steps 1–3 are achievable now and would be a genuine first brick. Step 4 is the
hard part and is where the line either progresses or stalls.

### STATUS (actioned, 2026-06-06): M-GRAV met and partly exceeded

[`compute/gravity_curvature.py`](../compute/gravity_curvature.py) implements a
*stronger* version of this milestone. The key move is that the associator
`[a,b,c]` is totally **antisymmetric**, so it cannot directly be a symmetric
metric; instead the module pulls the octonion inner product back through the
associator **map**. Fixing two "matter" labels `a,b`, the transport defect is the
linear operator `M_{a,b}(x) = [x,a,b]` on `Im(𝕆)`, and the emergent metric is its
**Gram matrix**

$$ g_{\mu\nu}(a,b) \;=\; \big\langle\, [e_\mu,a,b],\,[e_\nu,a,b] \,\big\rangle
   \;=\; \sum_k [e_\mu,a,b]_k\,[e_\nu,a,b]_k . $$

Verified numerically (each is a `PASS` line in the module):

1. **Symmetric, positive-semidefinite** by construction — a genuine metric
   perturbation, not just a curvature scalar.
2. **Curvature is transverse:** `Re[a,b,c] = 0` (no scalar/trace part), and
   `S = |[a,b,c]|² = 0` iff the three labels share a quaternionic (associative)
   subalgebra (Artin), `> 0` otherwise — the original flat/curved test.
3. **Step 4 — the transformation law — is met (internally):**
   `g(Ra,Rb) = R·g(a,b)·Rᵀ` *exactly* on all **1344 finite signed-permutation
   automorphisms** of `𝕆`. So `g` is a genuine **rank-2 tensor under the
   structure group `G₂ ⊂ SO(7)`**, with **no independent geometric input
   inserted by hand** (this is what the kill condition demanded).
4. **Clean scalar curvature density:**
   `tr g = 16·(|a|²|b|² − ⟨a,b⟩²) = 16·|a∧b|²` — an area law whose constant is
   the *same* `16 = dim 𝕆ℙ²` that fixes `ε₀² = π/432`.
5. **Graviton-like mode:** by alternativity `g` annihilates its source labels
   (`g·a = g·b = 0`), so the perturbation is **transverse** to the source
   bivector `a∧b`; `g` has rank `4`, and its 3-dim null space is exactly the
   associative subalgebra `span{a, b, Im(ab)}` — the flat directions, Artin made
   geometric.

The module also includes the **spacetime arena** side (the part this note's §2
did not address): `ℂ⊗ℍ ≅ M₂(ℂ)`, whose Hermitian elements are Minkowski
`ℝ^{3,1}` (`det = ` the `(+---)` norm) with `SL(2,ℂ)` acting as the Lorentz group
`SO(3,1)`.

What is **still open** (step 4's truly hard part, untouched): the metric lives on
the 7-dim *internal* `Im(𝕆)` with structure group `G₂ ⊂ SO(7)`. Reducing it to a
**4-dim spacetime** metric with Lorentz `SO(3,1)` signature — i.e. joining the
`ℂ⊗ℍ` arena to the `𝕆` curvature, fixing which 4 of the 7 internal directions
become spacetime — is **not** done, and is the remaining content of
Conjecture 6.1. There is also still **no dynamics** (no field equation, no Newton
constant).

---

## 4. Kill condition (when to stop and down-scope permanently)

> If no symmetric rank-2 metric (or a scalar curvature with the correct
> transformation law) emerges from `Ω_grav` **without inserting an independent
> geometric input by hand**, then gravity is **out of scope**: adopt the
> down-scoped branding (README.md option (a)) permanently, retitle PLAN.MD, and
> label `compute/graviton.py` as a non-derivation.

**Update (2026-06-06):** the *internal* half of this condition is now **passed** —
`gravity_curvature.py` produces a symmetric rank-2 tensor that transforms
correctly (`g(Ra,Rb)=R g Rᵀ`) under the structure group `G₂`, with no
hand-inserted geometric input. The kill condition therefore **sharpens** to its
remaining half:

> If the internal `Im(𝕆)` metric (structure group `G₂ ⊂ SO(7)`) cannot be
> reduced to a **4-dim Lorentzian** spacetime metric (structure group `SO(3,1)`)
> — joining the `ℂ⊗ℍ` arena to the `𝕆` curvature — without inserting an
> independent geometric input by hand, then gravity stays out of scope.

This is the honest fallback. CHO's defensible contribution does not depend on
gravity; the Standard Model parameter program (Tiers 1–3) stands on its own. The
gravity line is **optional and exploratory**, to be pursued only if resourced.

---

## 5. A caution surfaced by the generation audit

`01_algebra.md` §7 assigns the three fermion generations to the triality reps
`{8v, 8s, 8c}` — one vector and two spinors. `compute/three_generations_nogo_audit.py`
shows this exact assignment faces a vector-vs-spinor and a
chirality obstruction. Any gravity construction that *also* wants `8v` to be the
spacetime vector (the natural reading of "8v = the octonions = `Ω_grav`'s arena")
would then be in direct competition with the generation assignment for the same
rep. **This tension must be resolved before either the gravity line or the
three-generations theorem can be called settled.** It is the single sharpest
internal consistency question linking Tiers 3 and 4.

---

## 6. References

- T. Jacobson, *Thermodynamics of spacetime: the Einstein equation of state* (1995).
- R. D. Sorkin, causal set program (locally finite partial orders as spacetime).
- J. Baez, *The Octonions* (2002), §4 (triality, `8v/8s/8c`).
- `foundations/01_algebra.md` §4, §6, §7 (the CHO-specific definitions and conjecture).
