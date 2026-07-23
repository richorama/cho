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
ancilla-extended inputs. Their CNOT analysis proves `S(CNOT) <= 1`; AQC1 makes
that bound sharp and extends it to a continuous locally equivalent Ising
family. The novelty claim is therefore the exact family evaluation, not the
definition of the measure.

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
most one. The induced-norm lower bound uses the trace-norm-one signed operator
`W=Y_A x Z_B / 4`, whose A marginal vanishes while its evolved A output has
trace norm `|sin(2 theta)|`. Since `W` is not positive, it is not itself a
physical state. An operational diamond-norm witness is obtained from its
positive and negative parts using a one-qubit classical flag:

```text
rho_RAB = |0><0| x W_+ + |1><1| x W_-.
```

This is a normalized state, and block additivity plus the triangle inequality
gives an output trace norm at least that of `L(W)`; the upper bound makes the
inequality sharp.

At `theta=pi/4`, this unitary is locally equivalent to CZ and CNOT. Hence AQC1
also proves `S(CNOT)=1` in the convention of Barsse et al., closing their
published upper bound. This endpoint was not a new measure or a new
no-signalling criterion.

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
boundary control, not a new theorem.

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
witnesses need not attain the diamond norm.
