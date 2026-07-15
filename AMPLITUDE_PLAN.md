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

### Gate Q02: Coarse-Graining Robustness (next)

Require one unitary to close under at least two inequivalent amplitude
coarse-graining channels, with induced laws agreeing up to a coarse basis change.
Measure whether robustness is generic (kill condition) or selective.

### Gate Q02: Fixed-Environment Decoherence Channel (next)

Status: **specified, not yet implemented.**

Weaken the coarse-graining: fix a declared environment state `rho_B` and reduce by
`rho_A -> Tr_B(U (rho_A kron rho_B) U^dagger)`. This is the standard open-systems
map and always yields an autonomous channel, so the question shifts from existence
to *character*: which unitaries induce a genuinely decohering (Choi rank > 1)
effective channel, how that depends on `rho_B`, and whether the induced calculus is
still classically simulable. This is the second, inequivalent coarse-graining
required before any resolution-independence claim.

### Gate Q03: Interference As A Holdout (next)

The decisive test of the pivot. Freeze the survivors of Q01/Q02, then measure — as
a holdout never used for selection — whether the induced effective calculus is
genuinely nonclassical: a two-path recombination whose coarse probabilities cannot
be reproduced by any classical stochastic model on the coarse states. If survivors
are always classically simulable, the amplitude premise bought nothing and the
campaign parks.

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
