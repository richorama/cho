# Spurion Bridge

Frozen date: 2026-06-06

Purpose: collapse five separate open inputs of the epsilon/flavour bridge into one
parametric operator and give each a falsifiable, failure-closed check. This note
describes `compute/spurion_bridge.py`.

The five inputs, previously tracked separately in `EPSILON_BRIDGE.md`,
`ACTION_PROJECTOR_BRIDGE.md`, `PRIMITIVE_PROJECTOR_BRIDGE.md`, and
`OPERATOR_GAP_AUDIT.md`, are:

1. the physical transition ray `|tau>`,
2. the exact trace space `A_Weyl x J3(O)`,
3. the vacuum representative of the Fano-pair orbit,
4. the `pi` holonomy,
5. the reuse of the same operator across masses, CKM, PMNS, and neutrino splitting.

## Single-Spurion Principle

There is exactly one triality-breaking object:

```text
T_break = theta * |tau><tau|   on   A_Weyl x J3(O),   dim = 16 * 27 = 432.
```

There is exactly one knob:

```text
epsilon0^2 = Tr(T_break) / 432 = theta / 432.
```

Every flavour observable must be a normalized trace of `T_break` composed with a
channel projector. If any observable needs a second, independent epsilon, the
reuse test fails loudly. This is the discipline that converts "same number, reused"
into "same operator, projected".

## What The Module Derives

### Block 4 — `pi` holonomy as a Berry phase

The transition kernel `K = |tau><tau|` is rank one. A closed triality-breaking
loop that exchanges the occupied ray with its triality-adjacent partner traces a
loop on the Bloch sphere of that two-level transition. The geometric
(Pancharatnam-Berry) phase of a rank-one projector is

```text
gamma = -(1/2) * Omega,
```

where `Omega` is the enclosed solid angle. The minimal non-contractible loop is a
great circle (the geodesic loop, shortest loop exchanging the two rays). It
encloses a hemisphere, `Omega = 2 pi`, so

```text
theta = |gamma| = pi.
```

The module computes `gamma` numerically from the discretized Bargmann invariant,
so `pi` is measured, not inserted. Sub-great control loops are shown to give
`Omega/2 < pi`, confirming the quantization is specific to the geodesic loop.

### Blocks 1+3 — transition ray and vacuum representative

The Fano automorphism group is `PSL(2,7)`, order `168`. Under the full group the
`21` unordered line pairs form one orbit, which is the residual degeneracy flagged
in `ACTION_PROJECTOR_BRIDGE.md`.

Fixing the vacuum idempotent `omega = (1 + i e7)/2` fixes the point `e7` and
reduces the symmetry to the vacuum stabilizer of order `24`. Under the stabilizer
the `21` pairs split into orbits of sizes `[3, 6, 12]`. The vacuum-transition
class — line pairs whose shared imaginary unit is the vacuum direction `e7` — has
exactly `3` members and is one stabilizer orbit. So the vacuum collapses the
`21`-fold degeneracy to a single physical class, selecting the transition ray up
to the residual `SU(3)` color/Weyl gauge rather than by hand.

### Block 2 — exact trace space

The trace space is selected by requiring all three of:

- the internal factor carries one full complex CHO Weyl generation (`dim_C = 16`),
- the flavour factor is closed under the Jordan product,
- the flavour factor contains the trace/idempotent direction (full `J3(O) = 27`,
  not the traceless `26`).

The module checks the nearby alternatives (`A_real x J3(O)`, `Im(O) x J3(O)`,
`O x J3(O)`, `A_Weyl x J3(O)_traceless`) and shows `A_Weyl x J3(O)` is the unique
candidate passing all three, giving `dim = 432`.

### Block 5 — one operator across all sectors

With `theta = pi` from Block 4, the single knob `epsilon0^2 = pi/432` drives:

| Observable | Channel | Error |
|---|---|---|
| `m_c/m_t` | `1 * eps^2` | ~1% |
| `m_s/m_b` | `3 * eps^2` | ~2% |
| `m_mu/m_tau` | `8 * eps^2` | ~2% |
| `|V_us|` | `sqrt(7) * eps` | <1% |
| `|V_cb|` | `(1/2) * eps` | ~1% |
| `sin^2(theta13)` | `3 * eps^2` | ~1% |
| `Delta m21^2 / Delta m31^2` | `4 * eps^2` | ~1% |

The single-spurion RMS relative error across all seven channels is about `1.5%`,
and no channel needed a second epsilon knob.

## Status

This is a derivation **attempt** with failure-closed reporting, not a set of
theorems. Each block prints `PASS` only when its specific, falsifiable check
succeeds. What remains is to lift each numerical check to a CHO-action statement:

- prove the great-circle loop is the dynamically selected minimal triality path,
  not merely the minimal geometric loop;
- prove the trace-space requirements (complex Weyl generation, Jordan closure,
  trace direction) follow from the CHO Yukawa map rather than being imposed;
- prove the vacuum stabilizer orbit reduction is the physical gauge orbit;
- derive the channel coefficients (`1, 3, 8, sqrt(7), 1/2, 3, 4`) as operator
  traces rather than as the known sector multiplicities.

The value of the spurion structure is that any future contradiction now fails
loudly in one place instead of hiding in five separate notes.

## How To Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 compute/spurion_bridge.py
```
