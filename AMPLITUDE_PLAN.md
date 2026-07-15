# Mission: Does The Amplitude Premise Buy Selective Power?

## Why This Campaign Exists

The classical observer-consistency campaign is complete and parked at Level 2.
Demanding that microscopic dynamics commute with independently chosen
coarse-graining selected exactly the affine (XOR) cellular automata and nothing
richer: bounded causal transport but no stable records, no defects, and no
nonclassical probability calculus. See [PLAN.md](PLAN.md) for that closeout.

The classical plan authorised exactly one continuation: *change one premise at a
time — stochastic, then generalised-probabilistic, then complex amplitudes — and
rerun the same gates to measure what the new premise buys.* This campaign takes
the amplitude step, under a new constitution
([AMPLITUDE_CONSTITUTION.md](AMPLITUDE_CONSTITUTION.md)).

## The Central Question

Under the amplitude premise, the observer-consistency square is

```text
|state>  -- U^m -->  |state'>
   | B                  | B
   v                    v
coarse   -- U_B -->   coarse'
```

with `B U^m ~= U_B B` meaning equality of Born probabilities for every allowed
coarse preparation and effect. The question is whether this selection, now able to
see phase and superposition, forces a **narrow, nonclassical** class of effective
laws — something the classical crucible provably could not produce.

The pivot succeeds only if the amplitude premise buys selective power. If exact
unitary closure is generic, or collapses back onto classical/affine survivors, or
never exhibits interference in an unselected holdout, the amplitude route is
parked exactly as the classical one was. A clean no-go is still a result.

## Staged Gates

### Gate Q00: Representation Invariance

Status: **implemented and passing (Level 0 software contract).**

Born probabilities must be exactly invariant under the amplitude
representation-change group: the monomial unitaries with fourth-root-of-unity
phases. The census exhaustively checks dimensions two and three over all `261632`
effect/state/unitary triples, finds zero operational mismatches, and confirms
`3136` discrepancies for a deliberately basis-sensitive control diagnostic. The
permutation subgroup reproduces the classical Gate 00 relabeling exactly, so the
premise is a strict extension. Owner: `tests/test_gate_q00_representation_invariance.py`.

### Gate Q01: Exact Unitary Coarse-Graining

Status: **implemented and passing as a no-go (Level 0 contract; no Level 1
promotion).**

The microscopic update is a two-qubit unitary over `Q(i)`; the coarse-graining is
the partial trace over the second qubit. An autonomous effective law exists when a
fixed channel `E` satisfies `Tr_B(U rho U^dagger) = E(Tr_B rho)` for *every* global
state `rho`. Over a declared finite ensemble of `144` unitaries
`(a kron b) . entangler`, exactly `36` admit an autonomous coarse channel: precisely
the non-interacting product unitaries (`entangler = local`). All `108` entangling
members fail, and every survivor reduces to reversible conjugation `E(sigma) = a
sigma a^dagger` with Choi rank one, so no decoherence emerges. Strong reduced
autonomy therefore selects exactly non-coupling dynamics, the amplitude echo of the
classical interaction obstruction. Owner:
`tests/test_gate_q01_reduced_dynamics.py`.

The interesting nonclassical regime — an autonomous *decohering* channel from
reversible microscopic dynamics — is impossible under this strong all-states
condition. It is deferred to Gate Q02, whose weaker premise fixes the environment
state, the standard open-systems coarse-graining where irreversibility can appear.

### Gate Q02: Fixed-Environment Decoherence Channel

Status: **implemented and passing; first genuinely nonclassical emergence.**

Weakening the coarse-graining to a declared environment state `rho_B` and the
open-systems map `rho_A -> Tr_B(U (rho_A kron rho_B) U^dagger)` makes the effective
channel always autonomous, so the question becomes its character. Across the
`144`-unitary ensemble and five exact environments, every induced map is trace
preserving, but reversible microscopic unitaries now produce genuinely *irreversible*
(Choi rank two) effective channels. Decoherence arises exactly from the entangling
members: for every environment the decohering count equals the entangling decohering
count, so no local product unitary ever decoheres. Under a maximally mixed
environment the split is exact — all `36` local unitaries stay reversible and all
`108` entangling unitaries decohere — and the effect is environment dependent (CNOT
decoheres against `|+i>` but stays reversible against its target eigenstate `|+>`).

This is the first result the classical campaign provably could not produce:
reversible microscopic dynamics yielding irreversible effective behaviour, selected
by interaction. Paired with Gate Q01 it isolates what the environment premise buys —
decoherence is impossible under global autonomy yet generic under fixed-environment
reduction. Owner: `tests/test_gate_q02_fixed_environment_decoherence.py`.

### Gate Q03: Interference As A Holdout

Status: **implemented and passing; interference equals reversibility.**

Nonclassicality is measured on the frozen channels of Q01 and Q02 and never used
for selection. A configuration-independent witness asks whether a channel transmits
a computational-basis coherence to a nonzero output coherence, something no
classical stochastic channel can do; an exact Mach-Zehnder visibility
`p(both) - p(which-path)` gives the operational picture, with a fully dephasing
control pinned to zero and a reversible control at `-288/625`. Across all `144`
unitaries and five environments the census tracks the Q02 decoherence tally exactly:
non-interacting product unitaries stay nonclassical under every environment, while a
maximally mixed environment leaves every interacting unitary classical.

The sharp result under this coarse-graining is an exact channel-by-channel
equivalence over all `720` cases: an effective channel transmits coherence if and
only if it is reversible (Choi rank one). Under trace-B, decoherence and the loss of
interference are the same phenomenon, and both are induced precisely by interaction.
**Gate Q04 shows this exact equivalence is specific to the trace-B coarse-graining,
not fundamental** — the robust content is the one-way law that reversibility implies
a nonclassical effective law, plus the invariant that interaction is required for any
decoherence. Owner: `tests/test_gate_q03_interference.py`.

### Gate Q04: Robustness Under A Second Coarse-Graining

Status: **implemented and passing; separates robust laws from an artefact.**

Every Q01–Q03 result used one coarse-graining (trace out qubit B). Q04 re-runs the
campaign under a second, inequivalent coarse-graining (trace out qubit A), genuinely
independent because the ensemble is A/B asymmetric. Robust across both maps: only the
`36` non-interacting product unitaries admit an autonomous coarse law; those unitaries
stay reversible and coherence preserving under every environment; all decoherence and
all loss of coherence require interaction; and reversibility always implies a
nonclassical effective law. Not robust: the exact "coherence iff reversible"
equivalence holds only for trace-B — under trace-A there are `108` irreversible
channels that still transmit coherence (partial decoherence). So "decoherence equals
total loss of interference" was a coarse-graining artefact, while "interaction is the
sole source of classicality" is resolution independent. Owner:
`tests/test_gate_q04_robustness.py`.

## What The Amplitude Premise Bought

Across Q01 to Q04 the pivot is decisive where the classical route was silent. The
classical crucible produced bounded transport but never records, defects, or a
nonclassical calculus. The amplitude premise, under an independently declared
environment, produces genuine irreversibility from reversible dynamics; and Q04
certifies the resolution-independent core: **interaction is the sole and necessary
source of decoherence and classicality**, non-interacting dynamics remaining exactly
reversible and nonclassical under two independent coarse-grainings. The exact
interference-equals-reversibility identity, by contrast, is coarse-graining specific.

### Gate Q05: A Different Blocking, And Parameter Contraction

Status: **implemented and passing; supplies a third blocking and a strict parameter
count reduction.**

Q04 used two tensor-factor traces. Level 2 also needs a *structurally* different
blocking and evidence that repeated coarse-graining does not grow the surviving
parameter count. A rotated factorisation conjugates each unitary by a fixed non-local
Clifford `W` (CNOT, self-inverse) before tracing, so autonomy under it is autonomy of
`W U W†` under the plain trace — a genuinely different bipartition. On the fixed
ensemble it keeps `16` survivors versus the `36` of the plain trace, sharing only
`12`, so the two maps are inequivalent rather than relabellings. Every rotated
survivor still induces a reversible, coherence-preserving law: the robust core holds
in the third frame too. Parameter contraction: the `36` non-interacting survivors
`a ⊗ b` all reduce to the environment-free single-qubit conjugation `E(σ) = a σ a†`,
forgetting `b` entirely and collapsing to `6` distinct effective channels. These
channels compose as `conj(a₂ a₁)` and stay Choi rank one, so recursion never grows
the parameter class. Owner: `tests/test_gate_q05_recursion.py`.

This is Level 2 for the non-interacting family: one effective structure (reversible
single-qubit conjugation) survives three independent blockings with strictly fewer
parameters and is closed under composition. Honest caveat: this is a two-qubit
system, so "recursive" here means time-composition, not spatial recursion; a genuine
spatial-recursion gate would need larger systems and is left for future work.

### Gate Q06: Genuine Spatial Recursion On A Three-Qubit Chain

Status: **implemented and passing; delivers the nested spatial blocking Q05 deferred.**

Q06 removes the two-qubit caveat. Three qubits `A-B-C` are coarse-grained by tracing
qubit `C` to a two-qubit effective channel on `A-B`, and that channel is coarse-grained
*again* by tracing qubit `B` to a one-qubit channel on `A`. The reduction is defined for
any completely-positive map, so the second level genuinely acts on the channel produced
by the first — nested spatial blocking, not repeated time-composition. From `81`
ensemble members (three single-qubit gates per site, three entangler layers): the first
blocking keeps `54` (non-interacting products and `A-B` interactions, since tracing `C`
respects those boundaries) and discards every `B-C` interaction; the second blocking
keeps only the `27` fully non-interacting products, discarding every `A-B` interaction
too. So each nested blocking removes exactly the dynamics coupling across the newly
erased boundary, and `0` interacting members reach the bottom. Every bottom-level channel
is reversible (Choi rank one). Parameter contraction is monotone: distinct effective
channels shrink `81 → 18 → 3` as the traced factors are forgotten in turn (`c`, then
`b`), leaving the single surviving factor `a`. Owner: `tests/test_gate_q06_spatial.py`.

This is Level 2 proper: one effective structure (reversible single-qubit conjugation)
survives a genuine nested spatial coarse-graining with strictly and monotonically fewer
parameters at each level. Honest caveat: the surviving family is the non-interacting one,
exactly as in the classical campaign's additive Level-2 survivors — the amplitude premise
sharpens *why* interaction is filtered (it couples across the erased boundary) but does
not yet manufacture a nonclassical structure that survives recursively. That is the
Level-3 question.

### Gate Q07: An Irreducible Complex Phase Survives The Recursion

Status: **implemented and passing; the first Level-3 evidence.**

Q06 left the Level-3 question open: does *any* unselected nonclassical structure survive
the recursion that filters out interaction? Q07 answers yes, for the irreducible complex
phase. A channel is realisable with real amplitudes exactly when its exact superoperator
over Q(i) has zero imaginary part, and that property is invariant under every real change
of basis (conjugation by a real matrix sends the imaginary part to `R B R⁻¹`, zero only
if `B` is). So a nonzero imaginary entry is a basis-independent witness that the `i` is
irreducible — no real recombination or real coarse-graining can launder it away. Every
real-orthogonal gate (`I, X, Z, R, XR`) yields a real channel; the phase gate `S`
yields a genuinely complex one. Because `S` is a legal non-interacting factor, the
complex phase survives the three-qubit recursion to the bottom: of the `3` distinct
bottom channels exactly `1` is genuinely complex (`10` of `18` at the intermediate
level), and it also survives the rotated blocking (`3` distinct complex survivors).
Owner: `tests/test_gate_q07_phase.py`.

The contrast with Q06 is the whole point: recursion drives interacting survivors to
`0` but leaves the complex phase untouched, and that phase was never rewarded by any
objective. An unselected nonclassical structure surviving multiple independent blockings
robustly is the definition of Level 3. Honest scope: this establishes that complex
amplitudes are irreducible resolution-independent content — a genuine departure from
real-amplitude dynamics — not that a specific interference pattern, contextual set, or
gauge structure emerges. Those remain sharper Level-3 targets for larger systems.

## Promotion Levels

Identical ladder to the classical campaign. Level 0 is the software contract
(Gate Q00 reaches it). Level 1 requires an autonomous coarse law to exist under
independently chosen amplitude blocking. Level 2 requires the same effective
structure to survive multiple blocking channels with fewer parameters. Level 3
requires an unselected nonclassical structure (interference, contextuality, or
irreducible complex phase) to survive robustly. No level licenses claims above it.

## Anti-Goals

This campaign will not search for measured constants, will not put a target
symmetry group or dimension into the objective, will not name survivors after
known particles, and will not introduce a bespoke coarse-graining channel per
promising unitary. Emergence is only claimed for structure absent from the
objective.

## Run

```bash
python3 run_all.py
python3 -m unittest discover -s tests -v
```
