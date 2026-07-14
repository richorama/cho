# Theory Crucible

Created: 2026-07-14

Status: **successor program, exploratory, outside the closed CHO audit**.

## Reversal

The closed program asked whether

```text
C x H x O and J3(O) -> Standard Model structure and constants.
```

The crucible asks instead whether minimally specified dynamics select exceptional
structures from a wider theory space:

```text
selection rule -> stable low-energy structures -> perhaps CHO/J3(O).
```

CHO is one candidate outcome, not a premise. A negative result is allowed to
eliminate it.

## Rules Against Circularity

1. A selection objective may not contain `3`, `4/7`, `pi/432`, a measured mass,
   or an exceptional-group label merely because CHO uses it.
2. Every exceptional candidate must be compared with non-exceptional controls
   carrying the same coarse dimensions, ranks, or spectra where possible.
3. State counts, normalized traces, and symmetry invariants are kinematics until
   an observable map or dynamics is derived.
4. Inputs, outputs, controls, and failure conditions must be printed separately.
5. The old prediction registry is append-only. Crucible results cannot silently
   reinterpret or retune the frozen `sin^2(theta23)=4/7` wager.
6. A new gate enters `compute/audit.py` only after it defines a physical model,
   survives a matched null, and earns a ledger claim. These initial gates do not.

## Initial Question

The first target is the cleanest surviving CHO claim: the Fano-plane value

```text
sin^2(theta23) = 4/7.
```

The old work proved that `4/7` is independent of Fano labels and is the normalized
trace of a rank-four avoidance projector. The crucible asks what part of that
statement is physically distinctive.

### Gate 01: Projector-Rank Null

[`projector_rank_null.py`](projector_rank_null.py) compares the Fano avoidance
projector with Haar-conjugated generic rank-four projectors on `R^7`.

Result:

- Fano incidence canonically identifies four avoiding lines.
- Every rank-four projector in dimension seven has spectrum `{1^4,0^3}` and
  normalized trace `4/7`.
- An isotropic random state has expected weight `4/7` in every such subspace.

Therefore the subspace is Fano-specific, but the spectral number is rank-generic.

### Gate 02: Symmetry-Selection No-Go

[`fano_selection_no_go.py`](fano_selection_no_go.py) constructs all `168`
elements of `GL(3,2)=Aut(Fano)` exactly.

Result:

- Before a vacuum choice, all seven lines form one orbit and an invariant
  diagonal observable has one weight.
- The vacuum stabilizer has order `24` and splits line space into orbits of sizes
  `3` and `4`.
- The invariant observable is therefore
  `a P_through + b P_avoiding`; symmetry does not determine `b-a`.

The geometry creates the alternatives but does not select the upper-octant one.

### Gate 03: Thermal-Selection Tension

[`thermal_selection_tension.py`](thermal_selection_tension.py) gives those two
sectors the minimal stabilizer-invariant Gibbs dynamics. If their energy gap is
`Delta`, then

```text
p_avoiding = 4 exp(-beta Delta) / (3 + 4 exp(-beta Delta)).
```

Result: `p_avoiding=4/7` if and only if `beta Delta=0`. Any finite-temperature
energetic preference moves the result away from the exact state-count ratio.
This is a no-go only for the minimal equilibrium interpretation; coherent,
non-equilibrium, and scattering maps remain open.

### Gate 04: Observable-Map Classification

[`observable_map_gate.py`](observable_map_gate.py) decomposes the seven-line
module under the order-`24` vacuum stabilizer and classifies every linear
equivariant map into the two natural three-dimensional targets. It uses both
exact character inner products and a direct intertwiner null-space calculation.

Result:

- The line module is `2*1 + 2 + 3`.
- The reducible three-line target `1+2` admits three independent intertwiners,
  so symmetry does not determine an observable map.
- The irreducible target `3` admits one intertwiner up to scale, but that map
  removes the uniform avoiding mode. Its pullback projector has rank `3` and
  normalized trace `3/7`, not `4/7`.
- A rank-four projector cannot be the pullback of an isometric map into a
  three-dimensional flavour space.

Thus the unique linear equivariant construction points to the lower mirror, while
the construction capable of more freedom retains explicit knobs.

### Gate 05: Stabilizer-Invariant Unitary Dynamics

[`unitary_dynamics_gate.py`](unitary_dynamics_gate.py) classifies all invariant
Hermitian Hamiltonians on both natural three-flavour targets.

Result:

- On the irreducible `3`, Schur's lemma leaves only a scalar Hamiltonian, hence a
  global phase and no oscillation.
- On `1+2`, the Hamiltonian has one physical energy gap and every distinct-basis
  transition obeys
  `P(i->j)=4/9 sin^2(Delta E t/2)`.
- Its maximum `4/9` is strictly below the frozen `4/7` target.

The direct linear, equivariant, stabilizer-preserving unitary route is therefore
closed. Stabilizer breaking, a nonlinear/density-matrix map, or a different
physical interpretation would be new assumptions requiring matched controls.

### Gate 06: Matched Projective-Plane Census

[`projective_plane_census.py`](projective_plane_census.py) constructs
`PG(2,q)` over the prime fields `q=2,3,5,7`, verifies the incidence axioms, and
compares each plane under the same avoidance-projector observable.

Result:

- Every control has `q^2+q+1` lines, with `q+1` through a point and `q^2`
  avoiding it.
- The generic normalized avoidance trace is `q^2/(q^2+q+1)`.
- Fano `4/7` is exactly the `q=2` member and is selected by minimum size.
- The same split follows from ordinary finite-field projective geometry without
  invoking octonions or exceptional groups.

Thus `4/7` is a minimal-incidence signature, not an exceptional-geometry
discriminator. A successful CHO model must output something that distinguishes
the octonionic realization from the matched `PG(2,2)` incidence structure.

### Gate 07: Signed-Fano Multiplication Census

[`signed_fano_multiplication_census.py`](signed_fano_multiplication_census.py)
enumerates all `2^7=128` orientations of the seven Fano multiplication lines and
tests norm composition and alternativity exactly.

Result: exactly `16` survive both conditions, and those `16` are precisely the
signed-coordinate orbit of the standard octonion table. They are one algebra in
different basis conventions, not sixteen alternatives. Every survivor has `168`
nonzero ordered basis associators, each with squared norm `4`.

### Gate 08: Multiplication Stability

[`multiplication_stability_gate.py`](multiplication_stability_gate.py) allows the
seven line coefficients to vary continuously and defines a neutral squared-defect
loss for norm composition and alternativity.

Result: all `16` octonion coordinate copies are isolated zero-loss points. The
residual Jacobian has full rank `7`, its minimum local curvature is `324`, and all
`112` rejected discrete controls have positive loss. Octonionic multiplication
is therefore robust within the Fano-supported family, conditional on minimizing
this algebraic loss. No physical reason to minimize it has yet been derived.

### Gate 09: Associator Discriminator

[`associator_discriminator_gate.py`](associator_discriminator_gate.py) forms the
transport defect `M_ab(x)=[x,a,b]` and its Gram operator for all `21` imaginary
basis pairs.

Result: every octonion pair has spectrum `(0,0,0,4,4,4,4)`, equivalently
`G^2=4G`, `Tr G=16`, and rank `4`. Across all `128` signed products, exactly the
same `16` octonion coordinate copies reproduce the complete fingerprint.

This is the first crucible discriminator unavailable to incidence-only
`PG(2,2)`: it requires multiplication and genuine nonassociativity. It is a
candidate carrier for physics, not yet a spacetime or flavour observable.

### Gate 10: Associator Quantum Measurements

[`associator_quantum_measurement_gate.py`](associator_quantum_measurement_gate.py)
tests whether the normalized Gram operators `P_ab=G_ab/4` supply incompatible
quantum measurements.

Result: the `21` source pairs collapse to seven rank-four projectors, one per Fano
line. The no-space of each projector is exactly that line. Every distinct pair
has overlap `Tr(PQ)=2`, principal cosines squared `(1,1,0,0)`, and all seven
projectors commute and sum to `4I`. None of the `112` rejected signed products
produces even one valid projector, while generic rank-four controls do not
commute.

The family is uniquely octonionic within the matched census, but all its yes/no
questions can be answered in one common basis. It is therefore a compatible,
classical measurement geometry by itself, not a source of quantum interference.

### Gate 11: Associator Transport Dynamics

[`associator_transport_dynamics_gate.py`](associator_transport_dynamics_gate.py)
returns to the unsquared signed transport operators `M_ab`, whose orientation
information is erased by `M_ab^T M_ab`.

Result: one transport per Fano line gives seven independent skew generators.
Of their `21` pairs, `17` do not commute. Their Lie-algebra dimensions grow as
`7 -> 18 -> 21`, reaching the full rotation algebra `so(7)`. Their exact finite
exponentials are orthogonal evolutions, so suitable ordered sequences can make
any real seven-state rotation.

This restores noncommuting quantum-style kinematics, but not prediction. Generic
skew controls also reach `so(7)`, and the octonions do not yet choose a generator,
duration, ordering, initial state, or physical seven-state carrier.

### Gate 12: Associator Quantum Control

[`associator_quantum_control_gate.py`](associator_quantum_control_gate.py)
combines the seven transports `M_l` with the seven phase generators `iP_l` and
computes their real Lie closure.

Result: transports alone close as `7 -> 18 -> 21 = so(7)`, while projector
phases remain a seven-dimensional commuting algebra. Together they close as
`14 -> 35 -> 49 = u(7)`, permitting arbitrary unitary evolution on seven complex
amplitudes. Across all `128` signed Fano products, exactly the `16` octonion
coordinate copies supply a fully quantum-admissible package. Spectrum-matched
generic controls also reach `u(7)`, so universality is capability rather than an
octonion discriminator by itself.

### Gate 13: Octonion-Symmetry Hamiltonian Selection

[`octonion_symmetry_hamiltonian_gate.py`](octonion_symmetry_hamiltonian_gate.py)
classifies Hamiltonians invariant under the exact `1344`-element signed
automorphism witness, then under stabilizers of an unoriented or oriented vacuum.

Result: the invariant matrix dimensions are `1 -> 2 -> 3`. Full symmetry allows
only `H=aI`, an unobservable global phase. An unoriented vacuum permits
`H=aI+bP_v`, one sector gap but no transfer. An oriented vacuum additionally
derives multiplication by the vacuum, `J_v^2=-(I-P_v)`, and permits
`H=aI+bP_v+c iJ_v`. The spectrum of `iJ_v` is `(-1,-1,-1,0,1,1,1)`.

The exact `1+3+3` structure is a candidate clue, not a generation or flavour
identification. After removing the global phase, two physical coefficients remain
free. The decisive symmetry trial therefore does not select a unique dynamics.

## Current Scorecard

### Proved

- The `3+4` Fano split is exact and canonical after choosing a vacuum point.
- `4/7` as a normalized projector trace is not specific to Fano geometry.
- Fano symmetry alone cannot choose through versus avoiding.
- Minimal equilibrium sector selection cannot nontrivially select and retain
  exactly `4/7` at the same time.
- Linear equivariance gives either three map parameters or one map whose canonical
  projector trace is `3/7`.
- Stabilizer-invariant three-flavour unitary dynamics gives either no oscillation
  or transition probability at most `4/9`, never `4/7`.
- The projective-plane control family reproduces the split generically, with
  `4/7` selected only by choosing the minimum nontrivial plane `PG(2,2)`.
- Norm composition and alternativity select one octonion multiplication class
  from the `128` signed Fano products, and that class is locally isolated.
- The associator Gram spectrum uniquely distinguishes that class from every
  matched signed-Fano control.
- The Gram projectors form seven uniquely octonionic but mutually compatible
  rank-four measurements with a common basis.
- The signed associator transports are noncommuting and generate the full
  `21`-dimensional rotation algebra `so(7)`.
- The transports and projector phases jointly generate all of `u(7)`; exactly
  the octonion copies provide the valid combined package in the signed census.
- Full octonion symmetry forces a scalar Hamiltonian. One oriented vacuum
  canonically produces a `1+3+3` spectral split through `iJ_v`.

### Not Proved

- A physical map outside the now-closed direct linear equivariant route.
- A PMNS operator or oscillation Hamiltonian derived from the geometry.
- A dynamics that selects the avoiding sector and outputs `4/7` coherently.
- Any comparative emergence of CHO or `J3(O)` from a wider theory space.
- A physical interpretation of the now-derived associator structures.
- A law selecting one Hamiltonian, state, duration, or ordered transport path
  from the fully controllable `SO(7)` family.
- Values for the two physical coefficients surviving oriented-vacuum symmetry,
  or a reason to identify the resulting triplets with observed particles.

## Graduation Test

The Fano neutrino route advances only if one explicit model produces a unitary
three-flavour evolution operator from pre-oscillation inputs and satisfies all of:

1. the avoiding/through assignment is an output;
2. `4/7` is not inserted as a rank ratio or fit target;
3. matched rank-four non-Fano controls do not produce the same result;
4. the remaining PMNS observables and unitarity are simultaneously coherent;
5. the model states a kill condition against oscillation data.

The direct linear, equivariant, stabilizer-preserving unitary route has failed
criteria 1-4 and is closed. The broader physical N5 map remains open only to
models with additional structure. The finite-geometry theorem and frozen
experimental prediction remain preserved as a historical wager.

## Next Stages

1. **Expanded matched census:** compare Euclidean Jordan, matrix, Clifford, and
  incidence candidates under objectives that do not name exceptional groups.
2. **Independent vacuum-dynamics requirement:** the symmetry-selection route is
  stopped unless a wider candidate supplies a vacuum orientation and fixes both
  surviving Hamiltonian coefficients without measured inputs.
3. **Carrier-map gate, conditional:** test whether a selected evolution can enter
  a causal observable without identifying internal directions with spacetime or
  flavour by hand.
4. **Holdout gate:** score only observables excluded from model construction.

## Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/theory_crucible/run_all.py
```

The runner fails on the first broken assertion and prints no CHO audit verdict.