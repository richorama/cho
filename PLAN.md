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

Require one microscopic rule to induce compatible effective laws under at least
two non-equivalent blocking families. A rule does not pass merely because one
custom partition makes it lumpable.

Primary output: survivor rarity relative to matched random rules and shuffled
blocking controls.

### Gate 03: Recursive Consistency

Apply blocking repeatedly. Determine whether the induced laws approach a fixed
point, a short cycle, a trivial absorber, or uncontrolled drift.

Primary output: exact finite flow graphs over equivalence classes of update
rules, with basin sizes and surviving parameter counts.

### Gate 04: Records And Influence

Test whether survivors can create persistent, locally readable records while
retaining a bounded influence cone. Constant rules, permutations with no
interaction, and globally mixing rules are explicit controls.

Primary output: a classification of rules supporting both memory and nontrivial
causal interaction.

### Gate 05: Defects And Composition

Introduce localized deviations from a fixed-point background. Ask whether they
persist, move, scatter, and compose without a particle interpretation being
inserted.

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

Implement Gate 02 as a robustness test across inequivalent blocking families.
First quotient partitions by microscopic relabeling and define independence
without inspecting the update rule. Then classify which Gate 01 survivors close
under more than one partition shape and whether their induced coarse laws agree
up to coarse relabeling.

Do not begin Gate 03 until Gate 02 has named tests for partition independence,
matched shuffled controls, survivor rarity, and invariance under relabeling.