# pi/432 Option Map

This is the working map after the probation closeout. It separates what has been
tried from what remains plausible. The goal is to avoid repeating dead routes
while keeping enough lateral freedom to find the actual action.

## Already Tried And Ruled Out As Direct Solutions

1. Finite spectral-action heat-kernel coefficient `a4/a2`.
   - Ruled out because the finite moments are exact rationals and cannot equal
     transcendental `pi/432`.

2. KO/topological theta term in the current finite-triple channels.
   - Ruled out because the natural theta data collapse to zero.

3. Any `F4`-invariant potential on `OP2`.
   - Ruled out because `F4` preserves the `J3(O)` spectrum, so all such potentials
     are flat on the rank-one vacuum manifold.

4. Direct cubic norm `N3` on `OP2`.
   - Ruled out because `N3 = 0` on rank-one idempotents.

5. One more Schur / normalized-trace / invariant-average witness.
   - Ruled out as a solution. These explain the `1/(16 x 27)` factor, but do not
     derive the dynamical selection.

6. Single electroweak RG matching scale.
   - Ruled out as a route to the constants: the relevant boundaries require
     incompatible scales.

7. Generic outside big-bet routes.
   - Causal-set counting, entropic gravity, growth dynamics, flavour statistics,
     positive geometry, and adelic patterning supplied form but not CHO content.

## Second-Wave Probes

These are no longer just parked; each has a cheap executable gate in this sandbox.
They remain lower priority than the top three unless they produce an actual action
principle.

- exceptional Chern-Simons / higher gauge theory: `exceptional_cs_higher_gauge.py`;
- Freudenthal cubic universal unfolding: `freudenthal_unfolding.py`;
- exceptional harmonic analysis on `F4/Spin(9)` or `E6` spaces: `exceptional_harmonic_analysis.py`;
- adelic variational principle: `adelic_variational.py`;
- motivic / period geometry: `motivic_period_geometry.py`;
- topological string or enumerative exceptional geometry: `topological_string_geometry.py`;
- exceptional matrix model: `exceptional_matrix_model.py`;
- categorical state-sum / TQFT construction: `categorical_state_sum.py`;
- accept the result as geometric numerology and stop the physics claim.

Current sweep result: no route is solved. The routes that survive all cheap gates
still require an explicit action, descent class, motive, category, matrix saddle,
or unfolding theorem. The top three remain the most concentrated attacks.

## Active Top Three

### 1. Moment-Map / Symplectic Reduction

Best hope: derive the `16 x 27` carrier as quantized orbit data and the bare `pi`
as minimal transition flux, while the same moment map supplies an `F4`-breaking
Hamiltonian whose eigenvalues are not hand-inserted.

Entry probe: `moment_map_orbit_quantization.py`.

### 2. WZ / Anomaly / Inflow

Best hope: derive the action coefficient as a level-one Wess-Zumino or anomaly
inflow term normalized over the `16 x 27` carrier, with the half-turn Berry phase
giving the `pi` numerator.

Entry probe: `anomaly_wz_inflow.py`.

### 3. Jordan / Nonassociative Spectral Action

Best hope: replace the killed associative finite spectral-action coefficient with
a genuinely Jordan/nonassociative action that includes topological flux and cubic
or Peirce dynamics, so the spurion spectrum is generated rather than inserted.

Entry probe: `jordan_nonassoc_spectral_action.py`.

Concrete candidate: `candidate_wz_jordan_entropy_action.py`.
Flux gate: `wz_flux_normalization_gate.py`.
Level/integrality gate: `wz_level_integrality_gate.py`.
Gap derivation gate: `peirce_gap_derivation.py`.
Entropy gate: `entropy_principle_derivation.py`.
Frame lift gate: `frame_lift_f4_breaking.py`.
Unified action candidate: `unified_boundary_wz_jordan_action.py`.
Boundary variation gate: `boundary_variation_gate.py`.
Boundary metric-origin gate: `boundary_metric_origin_gate.py`.
Oriented WZ boundary gate: `oriented_wz_boundary_gate.py`.
WZ chain-origin gate: `wz_chain_origin_gate.py`.
Action-origin unification gate: `action_origin_unification_gate.py`.

This candidate action uses `Phi = pi/432` as a WZ/Schur flux and tests a
Jordan-frame entropy functional

```text
S_seed(rho) = Tr(rho log rho) + Delta_Phi Tr(rho N),
Delta_Phi = -1/2 log(Phi), N = diag(0,1,2).
```

Its Euler-Lagrange equations output the unnormalized seed spectrum
`(1, sqrt(Phi), Phi)`. The Peirce gap probe conditionally derives
`N=(0,1,2)` and `Delta_Phi=-1/2 log(Phi)` from rank-3 primitive grading plus
endpoint flux. The entropy gate derives the Gibbs form from a large-deviation
principle, and the frame-lift gate checks the finite S3 shadow of F4 breaking. It
is therefore the strongest concrete candidate so far, but it remains conditional
until one CHO/WZ/Jordan action derives the flux normalization, entropy principle,
and full F4 frame lift together.

`wz_level_integrality_gate.py` sharpens the flux side: for `S_WZ=(k/2)Omega`,
changing the disk filling by a full sphere shifts the action by `2*pi*k`, so
single-valuedness forces integer `k`. The primitive nonzero level gives the
half-turn `pi`, and Schur normalization gives `pi/432`. This kills the continuous
coefficient but does not derive the oriented WZ term, the carrier, or the choice
of primitive level from CHO dynamics.

`uniqueness_gate.py` sharpens the carrier side, reframing existence as
uniqueness. It does not produce 432 again; it measures how much freedom survives
the Schur-flat requirement. Exact divisor arithmetic shows: (i) 432 has nine
nontrivial factor pairs and at least three are CHO-meaningful (e.g. `16*27`,
`18*24`, `6*72`), so naive integer numerology is non-unique and KILLED; but
(ii) among the divisors of 432, only `16` and `27` are dimensions of irreducible
modules of the CHO structure-group chain, so `(16, 27)` is the UNIQUE
two-irreducible-factor carrier. This is a genuine conditional rigidity. It is
conditional on three named knobs the gate does not derive: the two-factor
ansatz, E6-vs-F4 normalization of the `27` (under F4 it splits `1 + 26`, weight
`1/3` not `1/27`), and primitive WZ level one. KILL: any inequivalent CHO-
consistent `(carrier, group, level)` that also gives `pi/432` would make it a
genuine free knob.

`unified_boundary_wz_jordan_action.py` now provides that single effective action
candidate at the sandbox level. It is F4-covariant because the ordered boundary
pair and its completed Jordan frame are transported by `F4`; it breaks `F4` only
through boundary data. It still remains below theorem status because the boundary
free-energy action itself has not been derived from full CHO dynamics.

`boundary_variation_gate.py` attacks the first missing input. On `OP2 x OP2`, the
endpoint-overlap functional `B(P,Q)=Tr(P o Q)` has gradient descent to `B=0`, so
it variationally forces an orthogonal primitive endpoint pair and hence a Jordan
frame completion. This removes the need to impose orthogonality by hand. It does
not derive the ordering: `B(P,Q)=B(Q,P)`, so the WZ orientation remains the live
boundary-data gap.

`boundary_metric_origin_gate.py` narrows the origin of that overlap term. It
checks that `Tr(P o Q)` is the rank-one transition probability, equals
`cos^2(theta/2)` on the boundary `CP1`, and is preserved by `F4`; therefore it is
the canonical invariant two-point contrast on `OP2`. This still does not derive
the boundary action coefficient or explain why CHO dynamics chooses the linear
monotone, but it removes the sense that the overlap cost is an arbitrary scalar.

`oriented_wz_boundary_gate.py` narrows that gap. It distinguishes the oriented WZ
action `+pi(1-cos theta)` from the reversed action `-pi(1-cos theta)`. At the
great-circle half-turn the unit holonomies coincide because `exp(i*pi)=exp(-i*pi)`,
so the orientation cannot be read from U(1) alone; it must be carried by the
oriented WZ chain/action. Conditional on that oriented boundary, grade order is
fixed as `(0,1,2)` and reverses to `(2,1,0)` under boundary reversal. The remaining
frontier is deriving this oriented boundary term from the CHO action.

`wz_chain_origin_gate.py` narrows the WZ origin. The primitive Berry/WZ curvature
on the transition `CP1` has full-sphere action `2*pi`, hence first Chern number
`1`; level one is the primitive nontrivial integral WZ chain, level zero is
trivial, and higher levels are multiples. This connects orientation and
integrality, but the microscopic CHO action still has to supply this boundary
chain.

`action_origin_unification_gate.py` is the current anti-treadmill check. It
assembles the overlap boundary term, oriented WZ term, integer level, Schur
carrier, Peirce grades, and entropy variation into one effective boundary action
and verifies that the outputs cohere. It also machine-checks the honest negative:
the metric origin of the overlap and the primitive WZ chain are narrowed, but the
full CHO-derived action is still open.

## Graduation Rule

A track may affect core code only after it supplies all of the following:

1. an explicit action functional;
2. a derivation of the `F4`-breaking term;
3. flux `pi/432` without hand-normalizing the coefficient;
4. a seed spectrum or hierarchy without inserting `spec(A)`;
5. a kill condition that would falsify the route.
