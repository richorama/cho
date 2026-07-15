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

## First Question

Before defining coarse-graining, Gate 00 tests the exact finite precursor:
representation invariance under relabeling. A preparation, reversible update,
and measurement effect are transformed together. Their observable probability
must remain unchanged. A deliberately label-sensitive diagnostic must fail.

This gate does not derive quantum theory or physics. It establishes the software
contract that later coarse-graining experiments must satisfy.

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