# pi/432 Action Search Sandbox

This folder is quarantined from the core audit harness. Nothing here is imported
by `compute/audit.py`, nothing here has an `audit_contract`, and nothing here
moves Bayes credit. The purpose is to search laterally for a real derivation of
`eps0^2 = pi/432` without contaminating the theorem/audit core.

Current target:

```text
derive an F4-breaking dynamical action whose flux gives pi/432
and whose spectrum gives the seed
```

That is stricter than recognizing the number. The durable pieces already point to
`pi/432 = (Berry/WZ pi) * 1/(16*27)`. The missing object is the action principle
that chooses the flux, carrier, and seed spectrum.

## Quarantine Rules

- Do not import these files from core code.
- Do not add these files to `compute/audit.py` until a probe produces a real
  candidate action with explicit assumptions and kill conditions.
- Do not update the scoreboard from these probes.
- Treat every successful exact identity here as a target, not a derivation.

## Already Tried

See [ruled_out_routes.md](ruled_out_routes.md). The short version: heat-kernel
`a4/a2`, finite KO theta, F4-invariant OP^2 potentials, more Schur/trace
witnesses, single-scale RG, and the broad big-bets directions have all failed as
direct derivations.

## Top Three Active Probes

1. `moment_map_orbit_quantization.py`
   - Attack: derive `16*27` as selected quantized carrier data and `pi` as
     minimal Berry/WZ flux via moment-map or symplectic-reduction logic.
   - Acceptance target: an action/reduction that selects the `Delta_9 x J3(O)`
     carrier and level-one flux without inserting them.

2. `anomaly_wz_inflow.py`
   - Attack: treat `pi/432` as a Wess-Zumino/anomaly/inflow coefficient, not as a
     heat-kernel coefficient.
   - Acceptance target: an anomaly polynomial or descent construction whose
     normalized boundary term forces denominator `432` and level `1`.

3. `jordan_nonassoc_spectral_action.py`
   - Attack: replace the killed finite associative spectral-action route with a
     Jordan/nonassociative action that has an essential period/WZ term and an
     F4-breaking seed functional.
   - Acceptance target: a nonassociative/Jordan variational principle where the
     period term supplies `pi`, Schur geometry supplies `1/432`, and the seed
     spectrum is stationary rather than inserted.

## Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/run_top3.py
PYTHONDONTWRITEBYTECODE=1 python3 experiments/pi432_action_search/run_everything.py
```

The runners only check exact arithmetic/structure gates and print next
mathematical requirements. Passing means "still plausible enough to pursue," not
"solved."

## Second-Wave Probes

The broader sweep tries parked radical routes without promoting them:

- `candidate_wz_jordan_entropy_action.py`
- `wz_flux_normalization_gate.py`
- `peirce_gap_derivation.py`
- `entropy_principle_derivation.py`
- `frame_lift_f4_breaking.py`
- `unified_boundary_wz_jordan_action.py`
- `boundary_variation_gate.py`
- `exceptional_cs_higher_gauge.py`
- `freudenthal_unfolding.py`
- `exceptional_harmonic_analysis.py`
- `adelic_variational.py`
- `motivic_period_geometry.py`
- `topological_string_geometry.py`
- `exceptional_matrix_model.py`
- `categorical_state_sum.py`

Standing result today: no solution. The full sweep keeps several routes alive as
action-principle searches, but none derives the `F4`-breaking action or seed
spectrum.

## First Concrete Candidate

`candidate_wz_jordan_entropy_action.py` is the first actual action-functional
attempt. It tests

```text
S_seed(rho) = Tr(rho log rho) + Delta_Phi Tr(rho N)
Delta_Phi  = -1/2 log(Phi)
Phi        = pi/432
N          = diag(0,1,2)
```

The Euler-Lagrange equations output the seed ratios
`(1, sqrt(Phi), Phi)`. This is a conditional candidate mechanism, not a final
derivation. Supporting gates now reduce the assumptions:

- `wz_flux_normalization_gate.py`: `Phi = pi/432` follows conditionally from WZ
  half-flux normalized over the Schur carrier `16*27`.
- `peirce_gap_derivation.py`: rank-3 primitive Peirce grading gives `N=(0,1,2)`,
  and endpoint flux gives `Delta_Phi=-1/2 log(Phi)`.
- `entropy_principle_derivation.py`: relative entropy is the canonical Gibbs
  free-energy form once the seed problem is posed as a large-deviation problem.
- `frame_lift_f4_breaking.py`: the fixed-frame candidate passes the finite S3
  frame-selection shadow, but the full F4 lift is still open.

The remaining theorem is to derive all of these gates from one CHO/Jordan/WZ
action rather than postulating them separately.

`unified_boundary_wz_jordan_action.py` is the current unified candidate. It uses
an ordered orthogonal primitive boundary pair `(P0,P2)` in `OP^2`, completes it
to the Jordan frame `P1=I-P0-P2`, normalizes the minimal WZ half-flux over the
`16*27` carrier, and runs the Gibbs/Peirce seed action on that moving frame. It
checks covariance under random `F4` automorphisms using the existing core F4
machinery. This is the best sandbox answer so far, but it still has to be
derived from full CHO dynamics before touching core claims.

`boundary_variation_gate.py` is the next hinge. It varies the boundary endpoints
on `OP2 x OP2` with the overlap functional `B(P,Q)=Tr(P o Q)`. Gradient descent
forces `B -> 0`, so the endpoints become an orthogonal primitive pair and
complete to a Jordan frame. The result is real progress, but the overlap term is
symmetric: it gives an unordered pair. The WZ orientation/order remains open.
