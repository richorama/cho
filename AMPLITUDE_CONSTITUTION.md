# Amplitude Constitution

This is a **new campaign with an independently motivated premise**, as required by
the classical project's closeout. It reuses the observer-consistency method but
changes exactly one starting object: descriptions are built from **complex
amplitudes** rather than classical bits. Nothing else about the discipline
changes.

## Starting Objects

The theory space contains finite-dimensional complex Hilbert spaces, pure-state
preparations, unitary updates, and projective or POVM effects, with all
amplitudes taken in the Gaussian rationals `Q(i)` so every Born probability is an
exact rational. Spacetime, dimension, particles, gauge groups, a preferred
tensor factorisation, and any target constant are **not** premises.

## The One Premise That Changed

Classical campaign: states were probability distributions, updates were
permutations or stochastic matrices, and the representation-change group was the
symmetric group of relabelings.

Amplitude campaign: states are amplitude vectors, updates are unitaries, and the
representation-change group is the group of **monomial (generalised permutation)
unitaries with fourth-root-of-unity phases**. The permutation subgroup (all
phases equal to one) recovers the classical relabeling group exactly, so this is a
strict, minimal extension rather than a fresh start.

## Observer-Consistency Principle (unchanged)

Two descriptions are physically equivalent when every allowed internal experiment
assigns them the same outcome probabilities after translation. Under the amplitude
premise, translation is conjugation by a representation-change unitary, and the
operational probability is the exact Born rule
`p(effect, state) = |<effect|state>|^2 / (<effect|effect> <state|state>)`.

The research question is whether demanding this consistency under increasingly
strong changes of description — now including phase and superposition — selects a
narrow class of process theories, and specifically whether it forces a
nonclassical probability calculus that the classical campaign could not exhibit.

## Anti-Circularity Rules (inherited verbatim)

1. Do not reward agreement with measured constants during construction.
2. Do not put Lorentz symmetry, three dimensions, a target amplitude field,
   chirality, or a gauge group into the score function.
3. Compare every survivor with dimension- and spectrum-matched controls.
4. Use at least two coarse-graining maps before calling a feature
   resolution-independent.
5. Freeze models before evaluating physical holdouts.
6. Count surviving parameters and report all failed families.
7. Prefer exact finite enumeration before stochastic search. Keep every amplitude
   in `Q(i)`; never let a claim depend on floating point.
8. Encode every scientific claim, control, and promotion condition as a named unit
   test. Production code computes results but never declares them proved.

## What Would Falsify The Point Of This Pivot

The pivot is only worth continuing if the amplitude premise **buys** something the
classical one could not. It is a failure — and a reportable one — if:

- exact coarse-graining closure over unitaries is generic, or is again satisfied
  only by classical-permutation-like (affine) updates;
- the surviving effective calculus is always classical, i.e. never exhibits
  interference in a holdout not used for selection;
- every nonclassical feature requires a bespoke coarse-graining map per rule.

In any of these cases the amplitude premise adds no selective power over the
classical crucible and the campaign is parked, exactly as the classical one was.

## Kill Conditions

Park this campaign if acceptable behaviour is generic among random unitaries, if
each rule needs its own coarse-graining map, if continuous phase knobs survive
without a selection law, or if apparent macroscopic laws change under harmless
re-encodings.
