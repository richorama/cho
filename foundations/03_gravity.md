# The Gravity Sector: Scoped Research Line (Currently Out of Scope)

Created: 2026-06-06 (roadmap Tier 4, item T4.2)

Status: **research line, not a result.** CHO currently has **no dynamical
gravity.** This note states honestly what exists (a candidate mechanism and a
conjecture), what a minimal computable deliverable would be, and the kill
condition that would make the down-scoped branding (README.md, "an algebraic
framework for Standard Model parameters") permanent.

This note exists so the word "gravity" — and by extension "Theory of Everything"
in [PLAN.MD](../PLAN.MD) — is backed by an explicit, bounded research target
rather than by the placeholder script [`compute/graviton.py`](../compute/graviton.py).

---

## 1. What exists today (and its status)

| Ingredient | Where | Status |
|---|---|---|
| Associator as curvature: `Ω(x,y,z) = [φ(x),φ(y),φ(z)]` | `01_algebra.md` §4 | **Definition**, motivated; not yet a metric |
| Curvature decomposition `Ω = Ω_grav + Ω_color + Ω_weak + Ω_em` | `01_algebra.md` §4, Thm 4.1 | **Claim**, not derived; `Ω_grav` = scalar/norm part of the associator |
| Information action `I[C,≺,φ]` and "maximal causal information" | `01_algebra.md` §6 | **Definition + variational principle**, no continuum proof |
| Continuum limit `I → ∫√-g (R/16πG − ¼F² + ψ̄(iD̸−m)ψ − Λ)` | `01_algebra.md` §6, Conj 6.1 | **Conjecture**, unproven — this is the whole game |
| `compute/graviton.py` | repo | **Placeholder**, not a derivation of graviton dynamics |

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

---

## 4. Kill condition (when to stop and down-scope permanently)

> If no symmetric rank-2 metric (or a scalar curvature with the correct
> transformation law) emerges from `Ω_grav` **without inserting an independent
> geometric input by hand**, then gravity is **out of scope**: adopt the
> down-scoped branding (README.md option (a)) permanently, retitle PLAN.MD, and
> label `compute/graviton.py` as a non-derivation.

This is the honest fallback. CHO's defensible contribution does not depend on
gravity; the Standard Model parameter program (Tiers 1–3) stands on its own. The
gravity line is **optional and exploratory**, to be pursued only if resourced.

---

## 5. A caution surfaced by the generation audit

`01_algebra.md` §7 assigns the three fermion generations to the triality reps
`{8v, 8s, 8c}` — one vector and two spinors. `compute/three_generations_nogo_audit.py`
(roadmap T3.2) shows this exact assignment faces a vector-vs-spinor and a
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
