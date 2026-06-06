# The CHO Spurion Action and the Derivation of ε₀² = π/432

Created: 2026-06-06 (roadmap Tier 1, items T1.0–T1.2)

Status: **candidate action with one partial derivation.** This note writes down
an explicit functional `S` and uses it to upgrade *one* step — the `π` holonomy —
from "minimal geometric loop" to "stationary configuration of `S`." It does **not**
claim `ε₀² = π/432` is now a closed theorem. The honest residuals are listed in §6.

Companion code: [`compute/action_derivation.py`](compute/action_derivation.py).
This note supersedes the weakest sentence of [`SPURION_BRIDGE.md`](SPURION_BRIDGE.md)
Block 4 ("the minimal non-contractible loop is a great circle") by giving the loop a
variational origin.

---

## 1. Why this note exists

The framework's central credibility gap (see [`METHODOLOGY_LIMITS.md`](METHODOLOGY_LIMITS.md),
"Dimensional Counting Warning") is that factors like `π`, `432`, `16`, `27` are only
meaningful if they fall out of an **explicit operator, trace, path integral, or
action** — not if they are assembled from convenient algebraic pieces. Until now the
project had no written-down action at all; `A4` in the
[`DERIVATION_LEDGER.md`](DERIVATION_LEDGER.md) invoked "the CHO lattice/information
action" by name only.

This note writes one down at the minimal level needed to test `ε₀² = π/432`, and
reports honestly which symbols it forces and which it still assumes.

---

## 2. The state space

From [`SPURION_BRIDGE.md`](SPURION_BRIDGE.md) Block 2, the triality-breaking spurion
lives on

$$
\mathcal{H} \;=\; \mathcal{A}_{\mathrm{Weyl}} \otimes J_3(\mathbb{O}),
\qquad \dim_{\mathbb{R}}\mathcal{H} \;=\; 16 \times 27 \;=\; 432 .
$$

The factor `16` is one full complex CHO Weyl generation (`dim_ℂ = 16`); the factor
`27` is the full exceptional Jordan algebra `J₃(𝕆)` (including the trace direction,
not the traceless `26`). The selection of this space by equivariance + Jordan closure +
trace direction is checked arithmetically in `spurion_bridge.py` Block 2. **We take
`dim 𝓗 = 432` as the arena here; deriving it from `S` itself is residual R3 in §6.**

The vacuum is the idempotent
$$
\omega \;=\; \tfrac{1}{2}\bigl(1 + i\,e_7\bigr),
$$
which fixes the imaginary unit `e₇` and leaves an `SU(3)` colour stabilizer
(`01_algebra.md` §2). The single triality-breaking object is the rank-one spurion

$$
T_{\mathrm{break}} \;=\; \theta\,\lvert\tau\rangle\langle\tau\rvert ,
\qquad
\varepsilon_0^2 \;=\; \frac{\operatorname{Tr} T_{\mathrm{break}}}{432} \;=\; \frac{\theta}{432}.
$$

Everything now reduces to one question: **what fixes `θ`?**

---

## 3. The candidate action

Write the rank-one configuration as a unit ray `|γ⟩ ∈ ℂP¹`, the Bloch sphere `S²` of
the two-level `{occupied, broken}` transition subspace selected by the vacuum
stabilizer (`spurion_bridge.py` Blocks 1+3). A triality-breaking history is a closed
path `γ: [0,1] → S²` that exchanges the occupied ray with its triality-adjacent
partner and returns. Define the candidate action as the sum of a **free (kinetic)
term** and a **geometric (Wess–Zumino / Berry) term**:

$$
S[\gamma] \;=\; \underbrace{\frac{1}{2}\int_0^1 \big\langle \dot\gamma,\dot\gamma\big\rangle_{g}\, dt}_{S_{\mathrm{free}}}
\;-\;
\underbrace{\theta \cdot \frac{1}{2\pi}\,\Omega[\gamma]}_{S_{\mathrm{WZ}}},
$$

where `g` is the round (Fubini–Study) metric on `ℂP¹` and `Ω[γ]` is the solid angle
enclosed by `γ`. The Berry phase of a transported rank-one projector is exactly
`γ_Berry = -½ Ω`, so the WZ coefficient `θ` is the holonomy the spurion accumulates.

This is the **free particle on the transition sphere with a topological θ-term** — the
simplest non-trivial action consistent with the rank-one transition structure.

---

## 4. What the action forces: θ = π (item T1.2)

**Claim.** The closed extremals of `S` are the closed geodesics of `g`, i.e. the great
circles of `S²`, and a great circle encloses a hemisphere `Ω = 2π`, so

$$
\theta \;=\; \lvert\gamma_{\mathrm{Berry}}\rvert \;=\; \tfrac{1}{2}\,\Omega \;=\; \pi .
$$

**Proof / check.** Varying `S_free` gives the geodesic equation; the WZ term is
topological (depends only on the homotopy class of `γ`) and does not enter the local
equation of motion. Hence stationary closed paths are **closed geodesics**. A curve on
`S²` is a geodesic iff its geodesic curvature `κ_g` vanishes, and for a latitude circle
at colatitude `ϑ` one has `κ_g = cot ϑ`, which vanishes **only** at the equator
`ϑ = π/2` — the great circle.

`compute/action_derivation.py` verifies this numerically: it reconstructs `κ_g` from
the discretized curve (matching the analytic `cot ϑ` to ~3 decimals), confirms the
zero crossing sits exactly on the equator, and computes the Berry phase of that
action-selected loop as `|γ| = 3.141593 = π`. The off-equator latitude loops have
`κ_g ≠ 0` and are therefore **not** action-stationary — closing the objection that the
great circle was chosen merely because it is the shortest loop.

**This is the genuine upgrade.** "Shortest loop" was an assumption; "the unique closed
geodesic of the free action `S_free`" is a variational consequence.

---

## 5. The result

With `θ = π` selected by the action and `dim 𝓗 = 432` taken as the arena:

$$
\boxed{\;\varepsilon_0^2 \;=\; \frac{\theta}{432} \;=\; \frac{\pi}{432} \;=\; 0.00727221\;}
$$

This is the single knob that drives all seven flavour channels at ~1.5% RMS in
`spurion_bridge.py` Block 5. The numerical identity `θ/432 = π/432` is confirmed in
`action_derivation.py`.

---

## 6. Honest residuals (what is NOT yet derived)

The action above forces `θ = π` but still **takes three things as inputs**. These are
the proof obligations that keep F0 short of theorem status, and they are tracked in
[`OPERATOR_GAP_AUDIT.md`](OPERATOR_GAP_AUDIT.md) and the ledger.

| ID | Residual input | What would close it |
|---|---|---|
| R1 | The configuration space **is** the rank-one two-level transition sphere `ℂP¹`. | **Reframed (`compute/epsilon_rank_one_kernel.py`).** The rank-one kernel `|τ⟩⟨τ|` is a *primitive idempotent* of `J₃(𝕆)` (spectrum `(1,0,0)`, a zero-entropy pure vacuum) — the same rank-3 spectral fact that forces `N_gen=3`. Rank one = primitive = one generation = pure; a rank-`r` kernel is `r` generations at once (`ε₀²→r·π/432`, no hierarchy). Residual shrinks to vacuum **purity** (the breaking selects one ray). |
| R2 | The weight is the **free** action `S_free` (round metric, no potential). | Derive the kinetic term and the absence of a competing potential from the CHO lattice/information action `A4`. |
| R3 | The trace space has `dim = 432 = 16 × 27`. | **Substantially closed (`epsilon_state_count`/`product_space`/`weyl_isomorphism`/`spin9_embedding`).** `16 = dim OP²` and `27 = dim J₃(𝕆)` are geometric; the gauge `A_Weyl` and flavour `T(OP²)` are the *same* octonionic Spin(9) spinor `Δ₉` (isomorphism discharged, embedding seam closed to one frame choice on the octonion pair). Residual shrinks to that single **frame choice**. |

**Verdict (for the ledger).** F0 moves from *"open bridge / conditional projector
derivation"* to *"action-selected `π` factor; full theorem pending R1–R3."* This is a
real, bounded upgrade — one of the three numerical inputs (`θ`) is now variational —
but it is explicitly **not** a completed derivation of `ε₀² = π/432`. If R1–R3 cannot
be closed, the honest fallback is to demote F0 to *ansatz*, exactly as the roadmap's
T1.0 kill condition requires.

---

## 7. Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python3 compute/action_derivation.py
```

Expected: a geodesic-curvature scan whose only zero is the equator, an
action-selected Berry phase `θ = π`, and `ε₀² = π/432`, with four `PASS` checks and
the three residuals R1–R3 printed as the open work.
