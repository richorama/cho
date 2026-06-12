# STATUS — closed

Closed: 2026-06-12 · `master` · HEAD `2f6ff36` · 157 commits (2026-06-03 → 2026-06-12)

This is the single "where it stands" snapshot for the **C⊗H⊗O** framework, written
to close the project cleanly. It is a PROVED-vs-NOT scorecard, not a pitch. If any
public wording is stronger than this file, weaken the wording — do not strengthen
this file. Canonical detail lives in [DERIVATION_LEDGER.md](DERIVATION_LEDGER.md),
[PUBLIC_CLAIMS.md](PUBLIC_CLAIMS.md), and [METHODOLOGY_LIMITS.md](METHODOLOGY_LIMITS.md).

## One-paragraph verdict

C⊗H⊗O is a **few-input algebraic framework for Standard-Model parameter relations
from division algebras** — **not** a completed Theory of Everything. The durable
result is theorem-level mathematics about the exceptional Jordan algebra `J3(O)`
and the gauge/representation layer. The claim that the framework *derives* the
Standard-Model constants is **on probation**: it hinges on one unbuilt object — an
`F4`-breaking dynamical action whose flux gives `pi/432` and whose spectrum gives
the flavour seed. Until that exists, the constant-physics layer is a constrained,
hard-to-vary parametrization with strong structure, not a theory of nature.

## What is PROVED (durable, machine-verified, decoupled from physics)

These survive even if the physics program never closes. See
[PAPER_JORDAN_THEOREMS.md](PAPER_JORDAN_THEOREMS.md) and
[compute/jordan_standalone_theorems.py](compute/jordan_standalone_theorems.py).

- **Theorem A — inner-frame.** The Jordan-frame `S3` acts by **inner**
  automorphisms of the connected `F4 = Aut(J3O)`; the three primitive idempotents
  are F4-congruent `OP^2 = F4/Spin(9)` points (isotropy `36`, tangent `16 = Δ9`,
  real-type commutant `1`). This is categorically unlike the **outer** `Spin(8)`
  triality on the inequivalent `8v, 8s, 8c`, so a Distler–Garibaldi mirror
  obstruction **cannot be posed** — the count-and-chirality route to `N_gen = 3`
  is obstruction-free.
- **Theorem B — Schur weights.** Schur's lemma forces the flat weights `1/16`
  (`Spin(9)` on `Δ9`) and `1/27` (`E6` on the `27`; `F4` alone leaves it reducible
  `1 + 26`), product **`1/432`**.
- **Theorem C — Freudenthal seesaw.** Vieta on the Freudenthal cubic norm gives the
  exact relation `m2·m3 = |N3|/m1`.
- **Theorem D — Cayley–Hamilton.** The degree-3 identity on `J3(O)` underwrites the
  cubic/rank structure used above.
- **Gauge sector (borrowed but rigorous).** The `C⊗H⊗O` one-generation gauge and
  representation layer — electric charge, weak isospin, hypercharge, anomaly
  cancellation — is reproduced and audited
  ([compute/physics_map_audit.py](compute/physics_map_audit.py)). Credit:
  Furey, Dixon, Todorov/Dubois-Violette, Boyle/Krasnov.
- **Derived flavour STRUCTURE (not magnitudes).** Several mixing quantities are
  derived as exact counts/half-angles (Fano-line counts, `SU(2)` half-angles,
  triality `Z3` texture). The overall magnitudes still ride on the open seed.

## What is NOT proved (open bridges)

- **The `pi/432` measure (F0).** `pi`, `16`, `27` are geometrically triangulated and
  the flat weights are Schur-forced, but no `F4`-breaking action has been written
  down that *selects* the normalized-trace measure. This is the Bayes-factor hinge.
- **Yukawa magnitudes / mass spectrum (A3).** A flavour-diagonal element still
  returns only its seeded diagonal; no operator yet produces a hierarchy from
  first principles.
- **Three-generation content map.** Count + chirality are obstruction-free, but the
  fermion-content map onto `T(OP^2)`, the Dirac operator, and the Yukawa spectrum
  remain open.
- **`alpha`, `sin^2(theta_W)`, `M_W` (continuum/RG).** Algebraic boundary terms plus
  underived continuum/RG residuals; no single consistent matching scale yet (S4/S5).
- **Cosmological constant.** The `3^64` and `11/12` screening factors remain proof
  obligations.
- **Gravity — out of scope.** Phase 5 ([foundations/11_gravity_gate.md](foundations/11_gravity_gate.md))
  confirms the internal `G2`-covariant associator metric brick yields no canonical
  4D Lorentzian reduction and no dynamics. Treat as an exploratory side line.

## The one-number bottom line (Bayes scoreboard)

From [compute/scoreboard.py](compute/scoreboard.py) — the model is charged the full
Occam price for every prefactor it *chooses* and credited nothing for those it
*derives*. The verdict hinges on exactly one named claim (`pi/432`):

| credit policy | `ln B` | verdict |
|---|---|---|
| historical (only `8/3` closed) | **−21.3** | null |
| today's closed-theorem floor | **−3.2** | null (model mildly disfavored) |
| + geometric `pi/432` credited | **+5.6** | CHO favoured |
| target (program complete) | **+36.2** | CHO |

Honest reading: **today's earned floor is `ln B = −3.2` — the model is mildly
DISFAVORED on closed results alone.** The internal route to lift it (build the
action that forces `pi/432`) is a *converging-negatives* program: every triangulation
sharpened the seam but none selected the measure. The sign only flips if `pi/432`
is granted.

## The one live external lever

The internal route is closed pending the action. The single sharpest **forward**
bet is on an unmeasured quantity:

- **`sin^2(theta23) = 4/7 = 0.5714`** (upper octant, `theta23 ≈ 49.1°`) —
  [compute/theta23_octant_prediction.py](compute/theta23_octant_prediction.py).
  It is the only mixing number that is exact-rational **and** `eps0`-independent
  (so it stands clear of the `pi/432` seam), and the octant is the Fano
  discriminator (`4` lines avoiding the vacuum vs `3` through it). **KILL:** a stable
  lower-octant resolution (`sin^2 < 1/2`, the `3/7` side). **Reach:** DUNE,
  Hyper-Kamiokande.

## Last research passes

### The "different integer"

A late pass turned the one remaining hard, `pi`-carrying, still-*chosen*
constant that had never been triangulated like `pi/432` was: the Higgs quartic
`lambda = pi/24`. See [compute/higgs_quartic_geometry.py](compute/higgs_quartic_geometry.py).

- **PROVED (exact):** `432 = 18 × 24`, so `lambda = pi/24 = 18·eps0^2`. Given the
  established result that `eps0^2 = pi/432` carries the Berry half-solid-angle `pi`,
  the `pi` in `lambda` is **forced to be the same holonomy** — not an independent
  "D4 root geometry" assumption. The framework therefore has **one** independent
  transcendental in this sector, not two. (Durable gain: one fewer free `pi`.)
- **NOT proved:** the integer `24` is **not uniquely forced** — it has at least three
  distinct framework-dimension origins (`|roots(D4)| = 28−4`, off-diagonal
  `J3(O) = 27−3 = 3·dim O`, `|2T| = 2|A4|`). Exactly like `432`, no `F4`-breaking
  action selects it. **Same FORM-not-CONTENT wall, on a different observable.** No
  new derived bit; `S3` stays the same open obligation as `F0`.

Conclusion: the stone is turned. It yields one structural simplification and
confirms the wall is general (it is not specific to `432`), which is itself useful
evidence about *where* the program is actually stuck.

### Structural line + predictions web (final pass, 2026-06-12)

The last working session ran two arcs to their natural ends; **both are
diagnostic and neither moved the scoreboard** (still `ln B = −3.2`).

- **The `pi/432` structural line** (eight exact, quarantined gates in
  [experiments/pi432_action_search/](experiments/pi432_action_search/)): the
  `F4 → Spin(9)` vacuum is built explicitly (16 Goldstones = one generation,
  `432 = 16 × 27` from the breaking); the numerator `pi` is an exact geometric
  half-turn (`(1+i)^4 = −4 → pi`, Chern number `1`); the `1/16` is Schur-forced
  and the `1/27` needs one extra democracy/traciality principle; that democracy
  and the seed Gibbs cascade collapse to **one** max-entropy (spectral-action)
  principle; and central simplicity of `J3(O)` proves the chiral doubling is
  **forced**, with `pi` shown to be a topological index (not a finite spectral
  moment), so a finite-⊗-continuous product triple is required. Every gate
  converges on the **same one missing object** — a derived `F4`-breaking action —
  so the internal structural line has converged, not closed.
- **The `eps0`-free predictions web** (six `compute/` diagnostics,
  `epsilon_free_mixing_web` … `epsilon_higher_order_split_test`): the one-knob
  `eps0^2 = pi/432` hypothesis holds to `~1–2%`, and its single `~2σ` structured
  residual (amplitudes `~0.8%` low, probabilities `~0.8%` high) is provably **not**
  a wrong `pi/432` (exclusion theorem), **not** the `√n`-vs-`n` bridge rule,
  **not** dominantly RG running, and **not** a single `O(eps0^2)` geometric
  correction — so it deflates toward noise. The web also exposes parameter-free,
  `pi/432`-independent cross-sector relations (`sin^2 θ13 = (3/7)|V_us|^2`, the
  completeness sum rule, `m_s/m_b = sin^2 θ13`) that hold at `~1σ` today.

## How to resume

A broader multi-track resume plan exists: [NEXT_PHASE_PLAN.md](NEXT_PHASE_PLAN.md).
Resume passes through 2026-06-12 executed its diagnostic pieces — a `pi/432`
carrier-uniqueness gate (Track 2), the `theta23` operator-hardening plus a
hash-locked data tracker (Track 3), the eight-gate structural line, and the
`eps0`-free predictions web. **None moved the scoreboard** (still `ln B = −3.2`);
they sharpen seams and tighten discipline, nothing more. The verdict still hinges
on the one item below.

1. The only move that flips the verdict is the one named in
   [compute/f0_sigma_model_closeout.py](compute/f0_sigma_model_closeout.py) and
   [ROBUSTNESS_ACTIONS.md](ROBUSTNESS_ACTIONS.md): **construct the `F4`-breaking
   dynamical action** whose flux gives `pi/432` and whose spectrum gives the seed —
   without hand-inserting the scale or the seed. Everything else is downstream.
2. The standing rule for new attempts
   ([experiments/pi432_action_search/ruled_out_routes.md](experiments/pi432_action_search/ruled_out_routes.md)):
   a new attempt must either **construct the missing `F4`-breaking action** or
   **explain why the target action was formulated incorrectly** — otherwise it is
   probably another witness, not a solution.
3. Run everything: `python3 compute/audit.py` (one artifact:
   `python3 compute/audit.py <name>`); validate the claim contracts with
   `python3 compute/audit_contract.py`; full test suite `python3 -m pytest -q`.

## Reproduce / verify

```bash
python3 compute/audit.py            # full robustness + derivation-frontier suite
python3 compute/audit_contract.py   # every artifact tied to a claim contract
python3 -m pytest -q                # one test per audit artifact
```
