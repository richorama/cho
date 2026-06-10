# Ruled-Out Direct Routes

These routes are preserved in the core repo as null records. They should not be
restarted as direct proof routes unless a new mechanism changes the assumptions.

| Route | Core artifact | Verdict | Why it is ruled out as a direct solution |
|---|---|---|---|
| Finite spectral-action heat-kernel `a4/a2` | `compute/f0_spectral_action_heatkernel.py` | Killed | Finite spectral moments are exact rationals. They cannot equal transcendental `pi/432`. |
| Finite KO/topological theta | `compute/f0_theta_reality_gate.py` | Killed | Natural KO-6 channels give `eta = 0`, mod-2 index `0`, and no Kramers `Z2`; theta is zero. |
| F4-invariant potential on `OP^2` | `compute/berry_sigma_model_op2.py` | Killed | `N3` and every F4-invariant are constant on the rank-one vacuum manifold, so no hierarchy is selected. |
| Direct cubic norm `N3` on `OP^2` | `compute/berry_sigma_model_op2.py` | Killed | `N3 = 0` on rank-one idempotents; the cubic must enter indirectly, off-vacuum, or through an unfolding. |
| Rank-one spurion as completed solution | `compute/f4_breaking_seed_op2.py` | Incomplete | The spurion gives the critical-point direction, but the critical values are `spec(A)` and remain input. |
| More Schur / normalized-trace witnesses | `compute/epsilon_measure_schur.py` and neighbors | Insufficient | They explain `1/16`, `1/27`, and `1/432`, but do not supply the action that chooses the carrier or seed. |
| One-knob `eps0` spectral ladder | `compute/spectral_action_432.py` | Incomplete | The averaging-law spectrum forces structure, but the best one-knob ladder misses the light charged-lepton hierarchy. |
| Single electroweak RG matching scale | `compute/rg_scale_derivation.py` | Killed | The two electroweak boundaries require scales separated by about `1.8e4`. |
| Broad big-bets routes | `compute/big_bets_closeout.py` | Insufficient | Causal sets, entropic gravity, positive geometry, flavour statistics, and adelic patterns supplied form, not CHO content. |
| Look-elsewhere / simplicity ranking | `compute/look_elsewhere.py` | Support only | Shows the constants are hard to vary in the CHO vocabulary; does not dynamically force them. |
| More invariance witnesses | `compute/gold_standard_closeout.py` | Treadmill | The internal program already localizes to one missing action. More witnesses do not move credit. |

Standing rule: a new attempt must either construct the missing F4-breaking action
or explain why the target action has been formulated incorrectly. Otherwise it is
probably another witness, not a solution.
