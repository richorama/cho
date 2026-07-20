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

- **O01** — exact frame-function / Born selection on the exceptional Jordan
  algebra `h_3(O)`: does resolution-agreement still pick the norm rule at the one
  dimension octonions permit?
- **O0x** — the composite-system wall: show tensoring fails and state the sharpened
  no-go for interacting octonionic dynamics.

## Non-claims

This campaign selects (or fails to select) the probability calculus in an exotic
amplitude ring. It does not derive the Standard Model. Suggestive links between
`h_3(O)`, `F4`/`E6`/`E8`, and particle content exist in the literature but remain
numerology-adjacent until dynamics are derived, which this framework structurally
cannot yet do.
