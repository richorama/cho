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
- Tensor-product-structure distance: Andreadakis and Zanardi, *Quantum* 9,
  1668 (2025), arXiv:2410.02911.
- Exact quantum model reduction: Grigoletto et al., *Quantum* 9, 1814 (2025),
  arXiv:2412.05102.

The forward perturbative estimate
`delta <= 2 t ||H_interaction||` follows from channel contractivity and is not a
new result. Petz recovery and Stinespring continuity do not by themselves give
the sharp channel-intertwining defect considered here.

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
most one. The lower bound is attained without an ancilla by the trace-norm-one
hidden correlation `Y_A x Z_B / 4`, whose A marginal vanishes while its evolved
A output has trace norm `|sin(2 theta)|`.

## Promotion and kill rules

1. Exact identities must be proved analytically; code supplies finite
   certificates and regression protection.
2. Frobenius norms may diagnose algebra but cannot be advertised as operational.
3. A diamond-norm claim must include a valid upper bound and a matching witness.
4. Known contractivity, continuity or recovery results must be cited rather than
   renamed.
5. Stop if the next result reduces to operator entanglement, a norm
   normalization, or a direct corollary of Stinespring continuity.

## Next theorem

Determine whether AQC1 extends from the Ising family to arbitrary two-qubit
Cartan interactions with a sharp formula or dimension-independent rigidity
bound. This target must be literature-checked separately before implementation.
