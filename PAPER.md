# Observer-Consistency Selects The Born Rule

*An exact finite crucible for deriving physical structure from agreement between
internal observers.*

---

## Abstract

We ask whether a single principle — that no internal experiment can reveal which
equivalent microscopic representation or admissible resolution was used to describe a
process — is restrictive enough to force reusable physical structure. We answer it in a
deliberately austere setting: finite-dimensional systems, exact arithmetic, exhaustive
enumeration, and every scientific claim pinned to a named unit test. Two campaigns are
run. The **classical campaign** takes probability distributions and stochastic/reversible
updates; the **amplitude campaign** changes exactly one premise — complex amplitudes over
the Gaussian rationals `Q(i)` — and reruns the identical gates.

The classical campaign is a clean no-go: demanding agreement under independently chosen
coarse-grainings selects exactly the affine (XOR) cellular automata, with bounded causal
transport but no stable records, and it selects them *only* at power-of-two scales. The
amplitude campaign sharpens the picture and delivers one positive theorem. Interaction is
the sole source of decoherence and of classicality; reversible microscopic dynamics can
induce irreversible effective channels; an irreducible complex phase survives nested
coarse-graining while state-independent contextuality does not; and — the central result —
**superposition-driven observer-consistency selects the Born rule uniquely** among the
`r`-norm probability calculi, in Hilbert dimension three and above, both as
non-contextuality and, equivalently and dimension-robustly, as frame-function
consistency. What the amplitude premise does **not** buy is an interacting nonclassical
dynamics: no interacting unitary admits an autonomous coarse law under two independent
blockings. The pivot therefore derives the *probability calculus of quantum theory*, not
its *interacting dynamics* — a clean and, we argue, honest boundary.

All results are reproducible by `python3 run_all.py` (150 tests).

---

## 1. The principle and the method

### 1.1 The equivalence principle

> No experiment available inside a process can reveal which equivalent microscopic
> representation or admissible resolution was used to describe it.

Anything that depends on microscopic names, an arbitrary blocking convention, or
inaccessible detail is, by this definition, not physical. Concretely, for a microscopic
update `U`, a coarse-graining (blocking) map `B`, and a candidate effective update `U_B`,
the central diagram is

```text
microscopic state  -- U^m -->  microscopic state
       | B                            | B
       v                              v
coarse state       -- U_B -->   coarse state
```

and observer-consistency asks that the two paths be operationally indistinguishable,
`B U^m ~= U_B B`, meaning equality of every allowed coarse preparation/effect probability,
not mere similarity of matrix entries.

### 1.2 The method: an exact finite crucible

Four disciplines make the results decidable rather than suggestive.

1. **Exact arithmetic.** Every amplitude is an element of `Q(i)` (a pair of rationals), so
   every Born probability, rank, and channel identity is an exact rational and every
   census is decidable. No claim depends on floating point.
2. **Exhaustive enumeration.** The smallest nontrivial systems are enumerated completely,
   not sampled.
3. **Predeclared gates with matched controls.** Blocking maps, promotion criteria, and
   kill conditions are frozen before inspection. Failure, genericity, and dependence on a
   hand-picked blocking are reportable outcomes.
4. **Claims are unit tests.** Production modules compute finite censuses only; the tests in
   `tests/` own all expected values, controls, and promotion criteria. A passing test
   establishes the stated finite result — and nothing above it.

### 1.3 Promotion ladder

- **Level 0** — software contract (representation changes implemented correctly).
- **Level 1** — an autonomous coarse law exists under an independently chosen blocking.
- **Level 2** — the same effective structure survives multiple blockings with fewer
  parameters.
- **Level 3** — an unselected nonclassical structure survives robustly.
- **Level 4** — comparison with broad physical holdouts (not reached here).

No level licenses claims from a higher level.

---

## 2. The classical campaign: a clean no-go

The classical theory space is finite probability distributions with permutation or
stochastic updates; the representation-change group is the symmetric group of relabelings.

**Gate 00 — representation invariance.** Joint relabeling of preparations, updates, and
effects preserves operational probabilities exactly; label-sensitive diagnostics are
rejected. (`tests/test_gate_00_representation_invariance.py`)

**Gate 01 — exact coarse-graining.** Small deterministic and rational stochastic processes
are paired with dynamics-independent blocking maps. The deterministic census checks
`159659` nontrivial rule/partition pairs through five states (`34311` survivors); the
denominator-two stochastic census checks `130648` pairs through four states (`25480`
survivors). Every partition count matches an independent closed formula.
(`tests/test_gate_01_exact_coarse_graining.py`)

**Gate 02 — blocking robustness (no-go).** Requiring one rule to close under *every*
relabeling-equivalent partition leaves only identity/reset dynamics. Arbitrary set
partitions are too strong to support an interacting observer-compatible world.
(`tests/test_gate_02_blocking_robustness.py`)

**Gate 03 — local recursive consistency (Level 2).** On the 256 elementary cellular
automata over periodic binary rings, with pair decimation and pair parity fixed in
advance, the factor-two spacetime rescaling `B U^2 = U_B B` leaves exactly `20` rules that
close under both blockings at sizes `6`, `8`, and held-out `10`. Four interacting common
fixed points survive — rules `60`, `90`, `102`, `150` — all additive XOR rules. This is a
finite universality result, not a physical theory.
(`tests/test_gate_03_local_recursive_consistency.py`)

**Gates 04–05 — records fail.** The surviving family transports counterfactual influence
inside an exact light cone but produces no passively readable stable record, under either a
passive decoder or a predeclared weaker encoded-recall protocol, and the reversible
two-channel lift preserves recoverability rather than a durable record subsystem.
(`tests/test_gate_04_records_and_influence.py`, `tests/test_gate_05_reversible_records.py`)

**Gates 06–08 — the affine classification.** Algebraic normal form over `GF(2)` proves
affine sufficiency; all `240` non-affine rules carry a replayable size-six decimation
conflict, so they cannot close universally in size. Extending through the dyadic hierarchy
and then to all integer scales yields the sharp statement: **universal matched-scale
affine closure holds if and only if the common spatial/temporal scale is a power of two**
(necessity via a hidden shift in rule `60`).
(`tests/test_gate_06_affine_classification.py`, `..._07_dyadic_renormalization.py`,
`..._08_integer_scale_classification.py`)

**Verdict.** The classical crucible is sterile in the sense that matters: it selects only
additive, record-free dynamics. Under the project's own kill conditions the route is
parked at Level 2. Its authorised continuation is to change exactly one premise.

---

## 3. The amplitude campaign

One premise changes: descriptions are built from complex amplitudes in `Q(i)`; updates are
unitaries; the representation-change group is the monomial unitaries with
fourth-root-of-unity phases (whose permutation subgroup recovers the classical relabeling
group exactly). Nothing else about the discipline changes.

### 3.1 Coarse-graining and the origin of classicality

**Q00 — representation invariance.** Born probabilities are exactly invariant under the
monomial group across all `261632` effect/state/unitary triples in dimensions two and
three (`0` operational mismatches; `3136` control discrepancies for a deliberately
basis-sensitive diagnostic). (`tests/test_gate_q00_representation_invariance.py`)

**Q01 — strong reduced autonomy (no-go).** For a two-qubit unitary and the partial trace
over the second qubit, an autonomous channel exists for exactly the `36` non-interacting
product unitaries of the declared `144`-member ensemble; all `108` entangling members fail,
and every survivor is reversible. Decoherence is impossible under all-states autonomy.
(`tests/test_gate_q01_reduced_dynamics.py`)

**Q02 — decoherence from interaction.** Weakening to a fixed environment state makes the
channel always autonomous; reversible microscopic unitaries then produce genuinely
irreversible (Choi rank two) effective channels, exactly for the entangling members. This
is the first result the classical route provably could not produce.
(`tests/test_gate_q02_fixed_environment_decoherence.py`)

**Q03 — interference as a holdout.** Over all `720` channel/environment cases, an effective
channel transmits coherence if and only if it is reversible; under this coarse-graining
decoherence and loss of interference coincide, both induced by interaction.
(`tests/test_gate_q03_interference.py`)

**Q04 — robustness.** Under a second, inequivalent trace, the resolution-independent core
survives — only non-interacting unitaries admit an autonomous law; interaction is the sole
source of decoherence — while the exact "coherence iff reversible" identity is shown to be
specific to the first coarse-graining. (`tests/test_gate_q04_robustness.py`)

### 3.2 Recursion, phase, and contextuality

**Q05–Q06 — spatial recursion and contraction.** A rotated (CNOT) bipartition gives a
third, structurally different blocking; a genuine nested spatial coarse-graining of a
three-qubit chain contracts survivors `81 → 54 → 27` and distinct effective channels
`81 → 18 → 3`, with each blocking discarding exactly the dynamics coupling across the newly
erased boundary and `0` interacting members reaching the bottom.
(`tests/test_gate_q05_recursion.py`, `tests/test_gate_q06_spatial.py`)

**Q07 — an irreducible complex phase survives (Level 3).** A channel is real-realisable iff
its exact superoperator over `Q(i)` has zero imaginary part, a real-basis invariant. The
phase gate `S` induces a genuinely complex channel that survives the three-qubit recursion
and the rotated blocking, though it was never selected for.
(`tests/test_gate_q07_phase.py`)

**Q08 — contextuality is destroyed (Level 3, opposite fate).** The Peres–Mermin square is
an exact state-independent Kochen–Specker contradiction over `Q(i)` (`0` of `512`
assignments consistent), but coarse-graining sends seven of its nine observables to zero
and leaves a noncontextual single qubit. Contextuality is a fine-grained resource the
recursion erases — the mirror of the surviving complex phase.
(`tests/test_gate_q08_contextuality.py`)

### 3.3 The interaction no-go, dimension robustness, and the Born rule

**Q09 — is any interacting law observer-consistent? (make-or-break).** Over a declared
family of six independent blockings — the two canonical tensor-factor traces and four
Clifford-rotated bipartitions (`cnot`, `rcnot`, `swap`, `cz`) — the two canonical traces
agree on exactly `36` survivors, all non-interacting and `0` interacting. No interacting
unitary is autonomous under more than one structurally distinct blocking: the single member
reaching two (the `CZ` gate) closes only within the bespoke `cnot`/`rcnot` frame pair, and
every interacting law that does close under any single cut is reversible, while every
non-interacting unitary is robustly autonomous under at least three blockings.
**Observer-consistent amplitude dynamics are non-interacting.**
(`tests/test_gate_q09_interaction.py`)

**Q10 — dimension robustness.** Rerunning the nested recursion on a four-qubit chain
contracts survivors `64 → 48 → 32 → 16` (each blocking removing exactly the coupling across
the newly erased boundary), with `0` interacting members reaching the bottom, all
bottom-level channels reversible, distinct channels contracting `24 → 8 → 2`, and the
complex phase surviving. The interaction-filtering and phase-survival results are not
small-chain artefacts. (`tests/test_gate_q10_dimension.py`)

**Q11 / Q12 — the Born rule is selected.** See Section 4.

---

## 4. Central theorem: the Born rule from observer-consistency

Consider the family of `r`-norm outcome rules for a complete measurement `{e_k}` on a
state `s`,

```text
q_r(k) = |<e_k|s>|^r / sum_j |<e_j|s>|^r,      r = 2, 4, 6, ...
```

with `r = 2` the Born rule. Writing `r = 2p` keeps every quantity an exact rational over
`Q(i)`: the weight of an effect is `t_k = |<e_k^|s>|^2` and the rule uses `t_k^p`.

**Observer-consistency demand.** An outcome direction shared by two complete measurements
must be assigned the same probability (no internal observer can tell which surrounding
measurement was used); equivalently, the total weight of a complete measurement must be
independent of the orthonormal frame the observer chose.

**Theorem (exact, finite).** Among the `r`-norm rules, `r = 2` is the unique exponent that
is observer-consistent, and this holds in every Hilbert dimension at least three.

The theorem is established by two independent exact censuses, plus two controls that fix
its scope:

- **Non-contextuality (Q11, dimension three).** Embedding a shared effect in two
  orthonormal bases and comparing `q_r`, Born gives `0` contextual discrepancies while
  `r = 4` and `r = 6` give `24` each over the two declared superposing bases.
  (`tests/test_gate_q11_born_selection.py`)
- **Frame-function consistency (Q12, dimensions three and four).** The Born frame sum
  equals `<s|s>` for every basis (Parseval), giving `0` inconsistent states, while `r = 4`
  and `r = 6` are frame-dependent for essentially every state (`26/26` in dimension three,
  `78/80` in dimension four). (`tests/test_gate_q12_frame_consistency.py`)
- **Control 1 — superposition is necessary.** A classical relabeling (a permutation of
  outcomes) exposes *nothing* for any exponent: it is genuine superposition that does the
  selecting. This is exactly the extra content the amplitude premise adds over the
  classical relabeling group.
- **Control 2 — dimension is necessary.** In a qubit the complement of a shared effect is
  forced, so every exponent is consistent; the selection requires dimension `>= 3`,
  recovering Gleason's threshold by finite enumeration rather than by assuming his theorem.

The significance is that the selection is *not* imported Gleason machinery: the
consistency demand is the project's own coarse-graining/resolution-agreement principle, and
the derivation is finite, exact, and driven by superposition — the single premise that
distinguishes the amplitude campaign from the classical one.

---

## 5. What the amplitude premise did and did not buy

| Question | Classical crucible | Amplitude premise |
|---|---|---|
| Autonomous coarse law exists | affine (XOR) only | non-interacting products only |
| Reversible microscopic → irreversible effective | no | **yes** (Q02), from interaction |
| Interaction observer-consistent under 2 blockings | no | **no** (Q09) |
| Stable passive records | no | not exhibited |
| Nonclassical calculus in a holdout | no | **yes**: irreducible complex phase (Q07/Q10) |
| Fine-grained contextuality | n/a | present but coarse-grained away (Q08) |
| Probability rule selected | n/a | **Born rule, uniquely** (Q11/Q12) |

The honest summary: the amplitude premise buys the **probability calculus** of quantum
theory — the Born rule as a resolution-agreement theorem, an irreducible complex phase, and
decoherence as the signature of interaction — but it does **not** buy an interacting
nonclassical *dynamics* that survives independent coarse-grainings. Observer-consistent
amplitude worlds are non-interacting, exactly as the classical ones were. The nonclassical
content that survives the recursion always rides on non-interacting dynamics.

---

## 6. Scope, non-claims, and limitations

- No measured constant, symmetry group, spacetime dimension, or particle spectrum was ever
  in a search objective. No survivor is named after a physical object.
- Results are finite and exact. "Level 3" means an unselected nonclassical structure
  survives multiple declared blockings; it does **not** mean a specific interference
  pattern, gauge structure, or continuum limit emerges. Those remain Level-4 targets and
  are not claimed.
- The Born theorem is proved over `Q(i)` for the enumerated exact bases in dimensions three
  and four, and for the `r = 2p` (even-`r`) family; it is consistent with, and gives a
  finite constructive witness for, the classical Gleason statement, but a fully general
  continuous-amplitude proof is outside this crucible.
- The interaction no-go (Q09) is an exact statement about the declared `144`-unitary
  ensemble and six-blocking family; it is decisive for that crucible and is the amplitude
  echo of the classical interaction obstruction, not a universal impossibility proof over
  all conceivable coarse-grainings.

---

## 7. Reproducibility

```bash
python3 run_all.py                         # discovers and runs all 150 gate tests
python3 -m unittest discover -s tests -v   # equivalent, verbose
```

Every claim in this paper corresponds to a named `unittest` method in `tests/`. The
production packages `observer_bootstrap/` (classical) and `amplitude_bootstrap/`
(amplitude) contain only exact representations and pure censuses; they declare nothing
proved. The governing documents are [PLAN.md](PLAN.md),
[RESEARCH_CONSTITUTION.md](RESEARCH_CONSTITUTION.md), and
[AMPLITUDE_CONSTITUTION.md](AMPLITUDE_CONSTITUTION.md); the supporting classical theorems
are in [AFFINE_CLASSIFICATION_NOTE.md](AFFINE_CLASSIFICATION_NOTE.md),
[DYADIC_RENORMALIZATION.md](DYADIC_RENORMALIZATION.md), and
[INTEGER_SCALE_CLASSIFICATION.md](INTEGER_SCALE_CLASSIFICATION.md); the amplitude gate
narrative is in [AMPLITUDE_PLAN.md](AMPLITUDE_PLAN.md).
