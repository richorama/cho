# Observer-Consistency Bootstrap

An exploratory attempt to derive physical law from agreement between internal
observers at different microscopic representations and resolutions.

This is a clean project. It assumes no prior algebra, particle content, spacetime
dimension, measured constant, or preferred microscopic labeling.

## Proposed Principle

> No internal experiment can reveal which equivalent microscopic representation
> was used to describe the same physical process.

The longer-term conjecture is stronger: descriptions related by admissible
coarse-graining should predict the same operational probabilities. Laws would
then be fixed points, or short cycles, of changes of description.

## Current Result

Gate 00 establishes representation invariance under relabeling. Gate 01 then
enumerates deterministic processes through five states and denominator-two
stochastic processes through four states under every nontrivial partition.
Exact autonomous coarse laws exist, but most rule/partition pairs fail.

Gate 02 distinguishes finding one favorable partition from surviving every
relabeling-equivalent partition family. The weak condition is nearly generic.
The strong condition leaves only identity/reset dynamics, so arbitrary set
partitions are too strong to support an interacting observer-compatible world.

Gate 03 adds one declared premise: a periodic binary product lattice with
nearest-neighbor elementary cellular-automaton updates. Pair decimation and pair
parity are fixed before inspecting the 256 rules. One-step blocking again leaves
only four noninteracting controls. With the factor-two spacetime rescaling
`B U^2 = U_B B`, exactly 20 rules close under both blockings on rings `6`, `8`,
and held-out size `10`; both induced flows remain in that family. Four interacting
common fixed points survive: rules `60`, `90`, `102`, and `150`. All are additive
XOR rules, so this is a Level 2 finite universality result, not evidence for a
physical theory.

Gate 04 freezes that family and measures single-site interventions without using
them for selection. Eight of the 20 survivors carry a background-independent,
persistent, replicated causal imprint through four steps; none of the other 236
elementary rules does. All four interacting fixed points pass, with influence
inside the exact radius-one light cone. However, exhaustive local decoders over
all unknown backgrounds fail for every fixed point at every time and window
through four steps. The family transports counterfactual influence but has not
produced a passively readable stable record, so it remains below Level 3.

A predeclared weaker observer protocol also fails to rescue the family. A central
three-bit repetition word is embedded in every possible binary background,
evolved for two steps, and decoded by majority over its fixed future light-cone
window. Six of 20 survivors beat chance for both symbols, compared with 88 of
236 controls; none of the four interacting fixed points passes. Encoded recall
is not selected or enriched. Under the project kill conditions, the elementary
cellular-automaton route is therefore parked at Level 2.

Gate 05 changes one premise explicitly by adding a previous-state channel and
the reversible update `(current, previous) -> (f(current) XOR previous, current)`.
All 256 local rules become exactly invertible. A phase-correct trajectory test,
which blocks states sampled at times `0`, `2`, and `4`, selects exactly the 16
affine Boolean rules under both spatial blockings at sizes `6` and `8`; eight are
interacting and rules `60`, `90`, `102`, and `150` remain common fixed points.
The full two-channel state permits radius-one recovery after two steps for every
rule, as required by the local inverse. But the declared record channel is only
a one-step delay and is then masked by the unknown previous bit. Reversibility
preserves recoverability, not a durable autonomous record subsystem.

Gate 06 closes the proof campaign. Boolean algebraic normal form and a symbolic
`GF(2)` identity prove affine sufficiency for every even ring size at least six.
All 240 non-affine rules have replayable size-six decimation conflicts, proving
they cannot satisfy universal-in-size closure. The complete size-six audit of
all 16 pair maps shows that each nonconstant affine map selects the same 16
affine rules, while nonlinear maps leave only constants. Decimation alone
supplies the universal classification, so agreement between two blockings adds
no selection pressure in this model. The theorem and limitations are stated in
[AFFINE_CLASSIFICATION_NOTE.md](AFFINE_CLASSIFICATION_NOTE.md).

Every scientific claim is a named `unittest` contract. Production modules only
compute finite processes and censuses; tests own all expected values, controls,
and promotion criteria. Passing tests establish the stated finite results, not
quantum theory or physics.

The project mission, staged gates, promotion levels, and stop conditions are
defined in [PLAN.md](PLAN.md). Methodological constraints are kept separately in
[RESEARCH_CONSTITUTION.md](RESEARCH_CONSTITUTION.md).

## Run

```bash
python3 run_all.py
python3 -m unittest discover -s tests -v
```

## Promotion Rule

The project advances only when one update family passes all of:

1. representation invariance;
2. agreement under at least two independently defined coarse-graining maps;
3. stable records and finite information propagation;
4. nontrivial interacting defects;
5. holdout observables excluded from the search objective.

Failure, genericity, and dependence on hand-picked blocking rules are reportable
results. No measured physical observable will enter the search objective.