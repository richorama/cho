# Approximate Quantum Coarse-Graining

## Status

Active on branch `approximate-quantum-coarse-graining`. This project starts
from a literature gap and a frozen theorem, not from measured constants.

## Question

For a microscopic unitary channel and a CPTP coarse-graining `B`, quantify the
best autonomous effective channel:

```text
delta(U,B) = inf_E || B Ad_U - E B ||_diamond.
```

The objective is a rigorous relation between autonomy failure, interaction and
recoverable hidden correlations. No Standard Model or cosmological
interpretation is in scope.

## Literature boundary

- Operator entanglement of unitaries: Zanardi, *Phys. Rev. A* 63, 012301
  (2001), arXiv:quant-ph/0010074.
- Causal and semicausal operations: Beckman et al., *Phys. Rev. A* 64, 052309
  (2001), arXiv:quant-ph/0102043.
- Information-disturbance and Stinespring continuity: Kretschmann,
  Schlingemann and Werner, *IEEE Trans. Inf. Theory* 54, 1708 (2008),
  arXiv:quant-ph/0605009.
- Approximate operator-algebra QEC: Beny and Oreshkov, *Phys. Rev. Lett.* 104,
  120501 (2010), arXiv:0907.5391.
- Directional signalling and causal influence: Barsse, Perinotti, Tosini and
  Vaglini, *Phys. Rev. Research* 6, 043305 (2024), arXiv:2309.07771.
- Exact SWAP and CNOT signalling, including parallel and asymptotic uses:
  Barsse, Perinotti, Tosini and Vaglini, *Disentangling signalling and causal
  influence* (2025), arXiv:2505.14120.
- Tensor-product-structure distance: Andreadakis and Zanardi, *Quantum* 9,
  1668 (2025), arXiv:2410.02911.
- Exact quantum model reduction: Grigoletto et al., *Quantum* 9, 1814 (2025),
  arXiv:2412.05102.

The forward perturbative estimate
`delta <= 2 t ||H_interaction||` follows from channel contractivity and is not a
new result. Petz recovery and Stinespring continuity do not by themselves give
the sharp channel-intertwining defect considered here.

The quantity `delta_A(U)` is not a new measure: under the diamond norm and after
exchanging the subsystem labels, it is exactly the directional signalling
measure `S(U)` of Barsse et al., including its optimization over arbitrary correlated and
ancilla-extended inputs. The 2024 paper proves `S(CNOT)<=1`; the 2025 follow-up
proves exact CNOT and SWAP values. AQC1 independently reproduces the CNOT value
and extends it to a continuous locally equivalent Ising family. The novelty
claim is therefore the exact family evaluation, not the definition or endpoint.

## Frozen results

### AQC0 -- normalization audit

Let `T = Tr_B`, `M = Tr_B Ad_U`, and let

```text
D_A(U) = min_E_linear ||M - E T||_F^2.
```

For every bipartite unitary on dimensions `d_A x d_B`,

```text
D_A(U) = d_A^2 d_B [1 - Tr(rho_A(U)^2)],
```

where `rho_A(U)` is the `AA'` reduction of the normalized vectorized operator
`|U>/sqrt(d_A d_B)`. Thus the old raw closure defect is exactly a dimension
factor times linear operator entanglement. Its contraction across changing
dimensions cannot by itself establish RG irrelevance.

Proof: `T T^dagger = d_B I`, so least-squares projection gives
`D=||M||_F^2-||M T^dagger||_F^2/d_B`. Unitary conjugation gives
`||M||_F^2=d_A^2 d_B`; realignment of `U` gives
`||M T^dagger||_F^2=d_A^2 d_B^2 Tr(rho_A^2)`.

### AQC1 -- sharp Ising autonomy defect

For two qubits and

```text
U_theta = exp(-i theta Z x Z) = c I - i s Z x Z,
```

the operational autonomy defect under `B=Tr_B` is

```text
delta_A(U_theta) = |sin(2 theta)| = 2 |c s|.
```

An optimal effective channel is the dephasing channel
`E_theta(X)=c^2 X+s^2 Z X Z`. The residual factors as

```text
Tr_B Ad_U - E_theta Tr_B
  = sin(2 theta) L,
L(X) = -(i/2)[Z, Tr_B(Z_B X)],
```

and `||L||_diamond=1`. The upper bound follows because
`X -> Tr_B(Z_B X)` and `K -> -(i/2)[Z,K]` have completely bounded trace norm at
most one. For the lower bound, take the two physical product inputs
`|+><+|_A x |0><0|_B` and `|+><+|_A x |1><1|_B`. They have the same A marginal,
so every candidate effective channel gives them the same simulated output.
Their true A outputs differ by `2cs Y`, with trace norm `4|cs|`; the triangle
inequality forces one simulation error to be at least `2|cs|`. This matches the
upper bound without a reference ancilla. The exact code additionally certifies
the equivalent signed-operator witness and its flagged-state realization.

At `theta=pi/4`, this unitary is locally equivalent to CZ and CNOT. Hence AQC1
also gives `S(CNOT)=1` in the convention of Barsse et al. Their 2025 follow-up
proves that endpoint independently, so the endpoint is prior art; the
continuous Ising formula remains the candidate new result.

### AQC2 -- SWAP boundary control

For equal dimensions `d` and the SWAP unitary,

```text
delta_A(SWAP) = 2 (1 - 1/d^2).
```

In particular, two-qubit SWAP has defect `3/2`. The optimal effective channel
is completely depolarizing. Indeed, with that choice the residual is
`(id - Depol) Tr_A`, so channel contractivity and the standard covariant-channel
identity

```text
||id_d - Depol_d||_diamond = 2 (1 - 1/d^2)
```

give the upper bound. Conversely, fixing the A input reduces every candidate
effective channel to a replacement state on the relabelled B output. Unitary
twirling shows that the maximally mixed replacement minimizes its distance
from the identity channel. A maximally entangled B-reference input attains the
same value. This is a known channel-discrimination identity applied as a
boundary control, not a new theorem. Barsse et al. (2025) also derive this exact
SWAP signalling value in arbitrary equal dimension.

### AQC3 -- Cartan symmetry reduction

For

```text
U = exp[-i (alpha XX + beta YY + gamma ZZ)]
```

write `U=sum_mu a_mu sigma_mu x sigma_mu`. Coupling B to the maximally mixed
state gives the admissible Pauli channel

```text
F(X) = sum_mu |a_mu|^2 sigma_mu X sigma_mu.
```

The nonnegative weights sum to one, so `F` is CPTP, and
`Tr_B Ad_U(X x I/2)=F(X)` exactly. This does not yet prove that `F` is the
globally optimal effective channel.

The Cartan unitary commutes with every joint Pauli `P x P`. Consequently both
`N=Tr_B Ad_U` and `T=Tr_B` obey the same covariance,

```text
N Ad_(P x P) = Ad_P N,    T Ad_(P x P) = Ad_P T.
```

For any candidate channel `E`, conjugating `E` by `Ad_P` preserves the diamond
defect. Convexity then shows that its Pauli twirl cannot increase the defect.
Therefore at least one optimal `E` is Pauli diagonal. This is a symmetry
reduction from all qubit CPTP maps to the Pauli-channel tetrahedron, not a
solution of the remaining diamond-norm minimization and not a novelty claim by
itself.

### AQC4 -- partial-SWAP scalar theorem

On the equal-angle Cartan line `alpha=beta=gamma=t`, the identity
`XX+YY+ZZ=2 SWAP-I` makes the channel, up to global phase,

```text
U_phi = cos(phi) I - i sin(phi) SWAP,   phi=2t.
```

Its full `V x V` covariance strengthens AQC3: an optimal effective qubit
channel can be chosen depolarizing,

```text
E_lambda(X)=lambda X+(1-lambda)Tr(X)I/2,  -1/3<=lambda<=1.
```

For fixed `lambda`, put

```text
a=(1-lambda)/3,
B=(1+lambda)^2-4 lambda cos^2(phi).
```

The diamond SDP evaluates exactly to

```text
d_phi(lambda) =
  4a                         if B <= 4a^2,
  B/(sqrt(B)-a)              if B > 4a^2.
```

Proof: average the full linear diamond-SDP feasible tuple
`(rho_0,rho_1,X)`, not the nonlinear trace-norm formula, over `V x V`.
Linearity preserves its objective and produces invariant input densities.
Schur-Weyl duality then gives `rho=x P_-+y P_+`, with `x+3y=1`. In the
singlet/triplet basis, the scaled Choi matrix splits into two equivalent
blocks. Four eigenvalues are `(lambda-1)y/2`; the remaining four are two copies
of

```text
[(1-lambda)y +- sqrt((1-lambda)^2 y^2+3xyB)]/2.
```

Maximizing their trace norm over `x` gives the displayed branches. Thus

```text
delta_A(U_phi)=min_{-1/3<=lambda<=1} d_phi(lambda).
```

This scalar minimization has a closed weak-coupling branch:

```text
0 <= sin(phi) <= 1/3:
lambda_*=1,   delta_A(U_phi)=2 sin(phi).
```

For `1/3<sin(phi)<1`, a minimizer lies in `0<lambda_*<1` and satisfies

```text
3[lambda_*+1-2cos^2(phi)] [sqrt(B_*)-2(1-lambda_*)/3] = B_*.
```

It reaches `lambda_*=0` and `delta=3/2` at SWAP. A dedicated search covering
partial-SWAP collision models, covariant channel discrimination, and both
Barsse et al. signalling papers found no treatment of the continuous family or
this two-branch formula. AQC4 therefore appears novel, while its covariance
tools and exact SWAP endpoint are prior art.

### AQC5 -- arbitrary-dimensional partial SWAP

For `U_phi=cos(phi)I-i sin(phi)SWAP` on `C^d x C^d`, full `U(d)` covariance
again reduces the effective channel to

```text
E_lambda(X)=lambda X+(1-lambda)Tr(X)I/d,
-1/(d^2-1) <= lambda <= 1.
```

Let `A=1-lambda`,

```text
B=A^2+d^2 lambda sin^2(phi),
H0=d(d^2-3)/(d^2-1),
H1=2/(d^2-1).
```

For an invariant diamond witness, let `u` be its total weight on the symmetric
subspace.  Write

```text
r_- = d(d-1)/2,  r_+ = d(d+1)/2,
rho = x P_- + y P_+,  r_- x+r_+ y=1,
u=r_+ y.
```

The scaled Choi operator has:

```text
-(1-lambda)y/d, multiplicity d(d-1)(d+2)/2,
-(1-lambda)x/d, multiplicity d(d+1)(d-2)/2,
nu_+, nu_-, each with multiplicity d.
```

Putting `P=(d-1)(d+2)/(d+1)`,
`R=(d+1)(d-2)/(d-1)`, the last two roots obey

```text
nu_+ + nu_- = (1-lambda)[P u+R(1-u)]/d^2,
nu_+ nu_- =
  u(1-u){[(1-lambda)^2/d^2] P R
         -[(1+lambda)^2-4lambda cos^2(phi)]}/d^2.
```

Their signs are opposite.  Summing all eigenvalue magnitudes and setting
`t=2u-1` gives

```text
d_{d,phi}(lambda)
 = max_{-1<=t<=1} (1/d) [
     A(H0+H1 t)
     + sqrt(A^2(H0+H1 t)^2+4B(1-t^2))
   ],
```

where `t=2u-1`.  Put

```text
Q=A^2(H0^2-H1^2)+4B,
C=1-A^2 H1^2/(4B),
D=(A H0+sqrt(Q))/C.
```

If `A H1 D<=4B`, the fixed-channel norm is `D/d`; otherwise its maximum is the
endpoint value `2A(H0+H1)/d`.  This recovers AQC4 when `d=2`.

The outer optimization is convex in `lambda`.  Its left derivative at
`lambda=1` is

```text
sin(phi) - (d^2-3)/(d^2-1).
```

Therefore the exact weak branch is

```text
0 <= sin(phi) <= (d^2-3)/(d^2-1):
lambda_*=1,   delta_A(U_phi)=2 sin(phi).
```

At full SWAP, `lambda_*=0` and
`delta_A=2(1-1/d^2)`, reproducing the known endpoint.  Exact qutrit
certificates give threshold `3/4`, weak value `6/5` at
`(cos phi,sin phi)=(4/5,3/5)`, and SWAP value `16/9`.
For `cos(phi)>0`, the derivative at `lambda=0` is
`-2(d^2-1)cos^2(phi)/d^2<0`; convexity therefore excludes negative
`lambda` from the outer optimum.  Dimension-four certificates give threshold
`13/15`, weak value `8/5` at `(3/5,4/5)`, and SWAP value `15/8`.

## Promotion and kill rules

1. Exact identities must be proved analytically; code supplies finite
   certificates and regression protection.
2. Frobenius norms may diagnose algebra but cannot be advertised as operational.
3. A diamond-norm claim must include a valid upper bound and a matching witness.
4. Known contractivity, continuity or recovery results must be cited rather than
   renamed.
5. Stop if the next result reduces to operator entanglement, a norm
   normalization, or a direct corollary of Stinespring continuity.
6. Prior signalling measures must be named as such; "autonomy" is only the
   coarse-graining interpretation of the same optimization.

## Next theorem

Determine whether AQC1 extends from the Ising family to arbitrary two-qubit
Cartan interactions with a sharp formula or dimension-independent rigidity
bound. The Ising and SWAP endpoints are now exact. The Cartan target must allow
ancilla-assisted witnesses: SWAP shows that system-only hidden-correlation
witnesses need not attain the diamond norm. AQC3 reduces the effective-channel
optimization to the Pauli tetrahedron; proving which Pauli channel is optimal
and evaluating its diamond norm remain open away from the equal-angle
partial-SWAP line solved by AQC4.
