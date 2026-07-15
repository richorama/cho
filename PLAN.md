# Mission: Derive Laws From Observer Consistency

## North Star

Determine whether requiring internal observers to agree across equivalent
representations and resolutions selects a small, nontrivial class of dynamical
laws.

The project does not begin by choosing matter, geometry, amplitudes, or a target
theory. It begins with finite processes and asks which properties survive every
admissible change of description. Anything that depends on microscopic names,
an arbitrary blocking convention, or inaccessible detail is not physical.

The hoped-for conceptual move is an equivalence principle:

> No experiment available inside a process can reveal which equivalent
> microscopic representation or admissible resolution was used to describe it.

The goal is not to reproduce known physics by search. The goal is to discover
whether this principle is restrictive enough to force reusable structure. A
clean no-go theorem is a successful outcome.

## Object Of Study

A microscopic candidate consists of:

- a finite state or process space;
- allowed preparations and operational effects;
- a compositional update rule;
- an explicit notion of locality or permitted interaction, when required;
- one or more independently specified translations to coarser descriptions.

For microscopic evolution `U`, blocking map `B`, and candidate effective
evolution `U_B`, the central diagram is

```text
microscopic state -- U^m --> microscopic state
       | B                         | B
       v                           v
coarse state      -- U_B --> coarse state
```

Observer consistency asks whether the two paths are operationally
indistinguishable:

```text
B U^m  ~=  U_B B.
```

Equality means agreement for every allowed coarse preparation and effect, not
merely similarity of matrix entries. Approximate equality must use a declared
operational distance with no observable-specific fitting.

The fundamental research object is therefore not an individual update table.
It is an equivalence class of processes under representation changes and
coarse-graining.

## Central Conjecture

Repeated observer consistency is rare.

Most microscopic rules will either fail to admit an autonomous coarse law,
depend strongly on the blocking convention, erase all records, propagate
influence without a stable bound, or flow to trivial fixed points. The conjecture
is that rules surviving all of these pressures occupy a small number of
universality classes with emergent structural properties not placed in the
search objective.

This conjecture is false if acceptable behavior is generic, or if almost any
rule can be rescued by choosing a custom coarse-graining map.

## What We Are Trying To Learn

The first question is not whether our universe appears. It is whether a coherent
macroscopic law can exist without being chosen separately at every scale.

Only after that question has a positive answer may we inspect whether survivors
also exhibit unscored properties such as:

- bounded causal influence;
- reversible microscopic dynamics with irreversible effective behavior;
- stable records and transportable defects;
- interference or another nonclassical probability calculus;
- scale-independent propagation laws;
- an effective dimension or metric;
- continuous symmetries emerging from finite rules.

These are holdout diagnostics, not initial optimization targets.

## First Research Campaign: Exact Finite Crucible

Use exhaustive enumeration and exact arithmetic for the smallest nontrivial
systems before introducing stochastic search or large tensor networks.

### Gate 00: Representation Invariance

Status: **implemented and passing**.

Joint relabeling of preparations, updates, and effects must preserve operational
probabilities exactly. Label-sensitive diagnostics must be rejected.

### Gate 01: Exact Coarse-Graining

Status: **implemented and passing**.

Small deterministic and rational stochastic processes are exhaustively paired
with blocking maps chosen independently of their dynamics. The tests classify
when an autonomous effective update exists:

```text
B U^m = U_B B.
```

The deterministic census checks `159659` nontrivial rule/partition pairs through
five states and finds `34311` survivors. The denominator-two stochastic census
checks `130648` pairs through four states and finds `25480` survivors. Constant
and identity blocking are excluded. Every deterministic partition count matches
an independent closed formula.

### Gate 02: Blocking Robustness

Status: **implemented and passing as a no-go**.

One microscopic rule is required to close under every relabeling-equivalent
partition in each shape, with induced laws agreeing up to coarse relabeling.
The weak control, existence of one favorable partition in two shapes, is nearly
generic: `242/256` deterministic four-state rules and `3101/3125` five-state
rules pass. Strong robustness leaves only identity and constant maps (`5` and
`6` rules respectively). Among `10000` denominator-two four-state stochastic
rules, `15` are universally lumpable and only `9` have shape-compatible induced
laws: identity, four resets, and four half-identity/half-reset mixtures.

Therefore arbitrary set partitions are not an admissible universal notion of
resolution for nontrivial dynamics. The result kills the unstructured finite-set
route rather than licensing a custom partition.

### Gate 03: Recursive Consistency

Status: **implemented and passing at Level 2**.

The process space is the 256 elementary cellular automata on periodic binary
rings. Nearest-neighbor locality, pair decimation, and pair parity are declared
before inspecting any rule. Exact one-step blocking leaves only rules `0`, `51`,
`204`, and `255`, reproducing the noninteraction obstruction. Under the natural
factor-two spacetime rescaling `B U^2 = U_B B`, exactly 20 rules close under both
blockings at source sizes `6`, `8`, and held-out size `10`. Both induced flow
edges stay inside the 20-rule family, permitting indefinite recursive blocking.

Eight rules are common fixed points of both flows. Four are interacting: `60`,
`90`, `102`, and `150`. They are precisely additive XOR dynamics within this
fixed-point set. The result establishes a small exact universality class but does
not establish records, defects, nonlinearity, continuum behavior, or physics.

Primary output: exact finite flow graphs over equivalence classes of update
rules, with basin sizes and surviving parameter counts.

### Gate 04: Records And Influence

Status: **implemented with a split result; no Level 3 promotion**.

The frozen Gate 03 family is tested under a single-site intervention while every
other microscopic bit ranges over all backgrounds. At size `11` through four
steps, `16/20` survivors have a background-independent response, `14/20` retain
it at every step, and `8/20` replicate it to multiple final sites. The matched
unselected census is `0/236` for all three properties. Rules `60`, `90`, `102`,
and `150` all carry persistent replicated influence within the exact causal cone.

This causal imprint is not silently called a record. A stricter passive decoder
must recover the original source bit from one bounded future window while all
unobserved background bits remain unknown. Exhaustive tests of every time
`1..4` and every window radius up to that time find no decoder for any of the
four interacting fixed points. Scale consistency strongly selects transport,
but this additive family has not demonstrated locally readable memory.

One weaker operational alternative was frozen before evaluation: prepare a
central three-bit repetition word in every possible size-`11` background, evolve
two steps, and majority-decode its fixed seven-site future light-cone window.
Only `6/20` selected rules recall both symbols above chance, versus `88/236`
controls. None of rules `60`, `90`, `102`, or `150` passes. The weaker record
criterion is generic rather than selected and does not rescue the fixed points.

Primary output: a classification of rules supporting both memory and nontrivial
causal interaction.

### Gate 05: Defects And Composition

Status: **reversible premise tested; split result, no Level 3 promotion**.

Each site is enlarged to `(current, previous)` and every elementary local rule is
lifted to `(f(current) XOR previous, current)`. The inverse is exact for all 256
rules. Instantaneous componentwise blocking again leaves only four noninteracting
controls. Because that map is phase-incompatible with factor-two time sampling,
the valid scale test blocks trajectories at times `0`, `2`, and `4` instead.

Exactly 16 rules close under both trajectory blockings at source sizes `6` and
`8`: the complete affine Boolean family. Eight are interacting, and `60`, `90`,
`102`, and `150` remain common fixed points. The full two-channel future state
locally recovers an initial bit after two steps for every rule, which is an exact
inverse identity rather than selection. The ancillary channel itself copies the
current bit for one step, then becomes one-time-padded by the unknown previous
bit. It is not a durable independent record.

Primary output: holdout statistics for lifetimes, propagation, scattering, and
fusion classes.

## Search Discipline

Use hard gates and Pareto fronts rather than one adjustable weighted score.
Every candidate is reported with:

- operational consistency error;
- number and independence of blocking maps passed;
- description length and surviving continuous parameters;
- stability depth under repeated coarse-graining;
- prevalence among matched controls;
- holdout behavior not used for selection.

Do not combine these into a scalar fitness function unless its weights and kill
conditions are frozen before the search. Keep training objectives and holdout
diagnostics in separate files and code paths.

Every statement presented as a project result must correspond to a named
`unittest` method. Tests contain expected census values, matched controls, and
promotion criteria. Package code contains only representations, transformations,
and pure computations. `run_all.py` performs test discovery and nothing else.

## Promotion Levels

### Level 0: Software Contract

Representation changes and operational comparisons are implemented correctly.
Gate 00 reaches this level.

### Level 1: Coarse Law Exists

At least one nontrivial microscopic family induces an autonomous effective law
under independently chosen blocking.

### Level 2: Universality Class

The same effective structure survives multiple blocking schemes and repeated
coarse-graining, with fewer parameters than its microscopic realization.

### Level 3: Observer-Compatible World

A survivor supports bounded influence, stable records, and interacting defects.
These properties must not be direct terms in its construction score.

### Level 4: Physics Candidate

Only after freezing the model may it be compared with broad physical holdouts:
dimensional scaling, dispersion, symmetry, probability structure, and continuum
behavior. Promotion requires several linked outputs, not one numerical match.

No level licenses claims from a higher level.

## What Would Count As A Major Result

Any one of the following would justify a standalone paper and repository:

1. a classification theorem for finite processes admitting observer-independent
   coarse dynamics;
2. a no-go theorem showing that records, bounded influence, and recursive
   consistency cannot coexist under stated assumptions;
3. a rare universality class exhibiting an unscored causal or nonclassical
   structure robustly across blocking maps;
4. a derivation showing that one probability calculus or compositional rule is
   uniquely stable under observer consistency;
5. an emergent invariant, dimension, or propagation law predicted before its
   physical interpretation is assigned.

## Anti-Goals

This project will not:

- search directly for measured constants;
- optimize for a preferred dimension, symmetry group, or particle spectrum;
- name defects after known particles before model freeze;
- treat visual resemblance to spacetime as evidence;
- introduce a bespoke blocking map for each promising rule;
- add algebraic structure solely to rescue a failed gate;
- claim emergence when an output was encoded in the objective.

## Stop And Pivot Rules

Park this route if any of these conclusions survives matched controls:

1. exact or approximate closure is generic among random rules;
2. nontrivial closure requires dynamics-specific blocking maps;
3. multiple reasonable blockings yield incompatible effective laws;
4. recursive consistency selects only identity, constant, or noninteracting
   permutation dynamics;
5. all interesting macroscopic properties require explicit reward terms;
6. parameter freedom grows rather than shrinks under coarse-graining.

If the finite classical process space is decisively sterile, the next pivot is
not arbitrary complexity. Change exactly one premise at a time: stochastic
processes, generalized probabilistic processes, then complex amplitudes. At each
pivot, rerun the same gates and measure what the new premise buys.

## Immediate Objective

Park the elementary-cellular-automaton route at Level 2. Exact scale invariance
selected bounded causal transport but neither worst-case passive records nor a
predeclared encoded statistical memory. Do not tune further encodings, readout
windows, times, blockings, or ECA subsets around the four fixed points.

Do not promote the reversible affine family to Level 3. The next premise, if
tested, must provide a protected record degree of freedom whose write and
transport phases are fixed independently of the local interaction rule. Require
records to remain readable from that subsystem alone for more than one update,
and compare every survivor with the complete matched reversible control family.