# The Octonion Campaign

*Observer-consistency on the last normed division algebra.*

The classical campaign used bits; the amplitude campaign changed exactly one
premise to complex amplitudes over the Gaussian rationals `Q(i)`. This campaign
changes exactly one premise again and takes the final rung of the Cayley-Dickson
ladder `R -> C -> H -> O`: amplitudes become **octonions** over the rationals.

## Why octonions, and why this is the last stop

Each doubling of the ladder loses one property — ordering (`R->C`), commutativity
(`C->H`), then **associativity** (`H->O`). **Hurwitz's theorem (1898)** says
`R, C, H, O` are the *only* normed division algebras: the norm form
`|x|^2 = x conj(x)` is multiplicative exactly up to the octonions and fails at the
next doubling (the sedenions, which have zero divisors). So the Born norm — the
project's `r = 2` invariant — is precisely the composition-algebra norm, and there
are exactly four amplitude worlds that can carry it.

Two structural facts frame the campaign:

- **Gleason's floor meets the octonion ceiling at 3.** The Born-selection theorem
  needs Hilbert dimension `d >= 3`; octonionic quantum mechanics *only* exists up
  to `d = 3`, the exceptional Jordan algebra `h_3(O)`. The window is a single
  dimension wide.
- **Composite systems are expected to fail harder**, sharpening the amplitude
  campaign's honest boundary that observer-consistency buys the probability
  calculus but not interacting dynamics.

## Method (unchanged)

Exact rational arithmetic, exhaustive finite census, predeclared gates with
matched controls, and every scientific claim pinned to a named `unittest`. The
Cayley-Dickson ladder *is* the code: a level-`k` number is a flat tuple of `2**k`
rationals (`jordan_bootstrap/octonion.py`).

## Gate O00 — representation invariance (implemented, passing)

The octonionic successor to amplitude Gate Q00. Representation changes are exact
rational **unit octonions**; the invariant they must preserve is the Born norm
`|x|^2`.

- **240** exactly-representable unit octonions are declared and frozen: the 16
  signed axes `+-e_k` (the octonionic "monomial" subgroup — signed relabeling)
  and 224 genuine two-axis superpositions built from the exact Pythagorean pair
  `(3/5, 4/5)` (the octonionic echo of the amplitude campaign's `(3,4,5)`
  rotations). The size `240` is a coincidence of the construction, **not** the E8
  root system (whose unit octonions are irrational).
- **Norm invariance is exact:** over 4800 checks, unit-octonion multiplication
  moves no Born norm (`0` mismatches), and the unit set is closed under
  multiplication (57600 checks, `0` non-units) — the exact echo of Hurwitz
  multiplicativity.
- **Controls bite:** every non-unit scaling is rejected (60/60), the algebra is
  genuinely non-associative (168 basis triples fail associativity), the
  quaternion sub-level still associates, every nonzero octonion has an exact
  two-sided inverse, and the ladder's kill condition is exhibited — one doubling
  past the octonions the norm identity breaks, `(e_1+e_10)(e_4+e_15)` giving norm
  `8 != 4`.

Contract: `tests/test_gate_o00_representation_invariance.py`. Package:
`jordan_bootstrap/`.

## Next gates (planned)

- **O01** — exact frame-function / Born selection on octonionic amplitudes:
  *implemented, passing* (see below).
- **O0x** — the composite-system wall: show tensoring fails and state the sharpened
  no-go for interacting octonionic dynamics.

## Gate O01 — frame-function / Born selection (implemented, passing)

The octonionic successor to amplitude Gates Q11/Q12. A state is a vector in
`O**d`; an orthonormal frame is an exact rational orthogonal matrix acting on the
coordinates; the `r`-frame total is `sum_i |(O s)_i|^r`, an exact rational for even
`r`. The question: which `r` gives a total independent of the frame?

- **Only `r = 2` survives.** Over the declared census (10 states across `d = 3, 4`)
  the Born total is exactly frame-invariant (`0 / 20` mismatches — Parseval for the
  octonion norm), while `r = 4` and `r = 6` are contextual (`6 / 10` states
  disagree between the two frames).
- **It reproduces the complex Born theorem exactly.** The `(1,1,1)` witness state
  gives frame totals `3` (both frames) at `r = 2`, but `3` vs **`3027/625`** at
  `r = 4` and `3` vs **`5331/625`** at `r = 6` — the identical rationals of
  `BORN_RULE_THEOREM.md`, now with octonionic amplitudes. The same discrepancy
  appears for the imaginary-unit state `(e_1, e_1, e_1)`, so the selection is not a
  real-amplitude artefact.
- **Superposition is essential (octonionic monomial control).** Right-multiplying
  every coordinate by a fixed *unit octonion* leaves the whole multiset of weights
  unchanged for every `r` (`0 / 120` mismatches, Hurwitz / Gate O00), so the
  octonionic relabeling group can never expose `r != 2`. Only a genuinely
  superposing rational rotation does.

Contract: `tests/test_gate_o01_frame_consistency.py`.

## Next gates (planned, continued)

- **O02** — Born selection on the exceptional Jordan algebra `h_3(O)`:
  *implemented, passing* (see below).
- **O0x** — the composite-system wall and the interacting-dynamics no-go.

## Gate O02 — Born selection on h_3(O) (implemented, passing)

Gate O01 selected the norm rule for octonion coordinate vectors; this gate moves
to the honest home of octonionic quantum states: the exceptional Jordan algebra
`h_3(O)` of 3x3 Hermitian octonionic matrices under `A o B = (AB + BA)/2`. Its
rank-one primitive idempotents (`P o P = P`, `tr P = 1`) are the pure states --
the octonionic projective plane `OP^2` -- and a Jordan frame resolves the
identity into three orthogonal idempotents. The Born rule is the trace form
`tr(P o Q)`.

Two genuinely Jordan-algebraic results, both exact:

- **Gleason on `h_3(O)`.** For every declared state and every Jordan frame the
  trace-form total `sum_i tr(P o Q_i)` equals `tr(P)` (`0 / 8` mismatches) -- the
  frame resolves the identity, so the Born total is frame-independent. The two
  declared frames are verified exact resolutions of the identity (`2 / 2`).
- **Non-associativity obstructs statehood.** Three declared rational unit vectors
  whose octonion entries span a non-associative triple give outer products that
  are Hermitian and unit-trace yet are **not** idempotent (`3 / 3` fail), so they
  are not points of `OP^2`. Not every octonionic ray is a state -- the first
  honest wall the octonions raise, and it appears already at the level of what
  counts as a pure state. The four quaternionic (associative) unit vectors, by
  contrast, all give genuine primitive idempotents (`4 / 4`).

The `(1,1,1)` superposition remains contextual at `r = 4` inside the idempotent
picture, tying O02 back to O01 and the complex Born theorem.

Contract: `tests/test_gate_o02_jordan_born_selection.py`.

## Next gates (planned, continued)

- **O0x** — the composite-system wall: tensoring `h_3(O)` fails, sharpening the
  amplitude campaign's no-go for interacting octonionic dynamics.

## Non-claims

This campaign selects (or fails to select) the probability calculus in an exotic
amplitude ring. It does not derive the Standard Model. Suggestive links between
`h_3(O)`, `F4`/`E6`/`E8`, and particle content exist in the literature but remain
numerology-adjacent until dynamics are derived, which this framework structurally
cannot yet do.
