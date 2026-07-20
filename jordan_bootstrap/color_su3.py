"""Gate O10 -- color SU(3) as the octonionic complex-structure stabiliser.

Every earlier octonion gate stayed inside a *fixed* octonion algebra. This gate
asks what continuous symmetries the octonions have at all, and finds the first
place where the exceptional algebra reaches back toward particle physics.

A *derivation* of the octonions is a linear map ``D`` obeying the Leibniz rule
``D(x y) = D(x) y + x D(y)``. The derivations form a Lie algebra under the
commutator bracket, and a classical theorem (Cartan 1914) identifies it with the
14-dimensional exceptional Lie algebra ``g2`` -- i.e. ``Aut(O) = G2``. We do not
assume this: we *solve the linear Leibniz system exactly over the rationals* and
count the null space (``= 14``).

Then we pick one imaginary unit ``u`` and keep only the derivations that fix it,
``D(u) = 0``. This is one linear condition per output coordinate; exact
elimination shows the surviving algebra is exactly **8-dimensional**. We prove it
is the compact simple Lie algebra ``su(3)`` -- the colour gauge algebra of the
strong force -- by three exact certificates:

* it is closed under the bracket (a genuine subalgebra);
* its Killing form ``K(X, Y) = tr(ad_X ad_Y)`` is non-degenerate (semisimple)
  and negative definite (compact real form);
* dimension ``8`` cannot be written as a sum of smaller compact-simple
  dimensions (the only ones below 8 are ``su(2) = 3``, and ``3 + 3 = 6``,
  ``3 + 3 + 3 = 9``), so a semisimple algebra of dimension 8 is *simple*, hence
  the unique 8-dimensional compact simple algebra ``A2 = su(3)``.

Finally the physics reading, which drops out for free from the Leibniz rule.
Because ``D(u) = 0``, every fixing derivation commutes with left multiplication
``L_u`` (``D(u x) = D(u) x + u D(x) = u D(x)``), and octonionic alternativity
gives ``L_u^2 = -I``. So ``L_u`` is an exact complex structure ``J`` on the
six-dimensional space of imaginaries orthogonal to ``u``: those six real
directions become ``C^3``, ``su(3)`` acts on them complex-linearly, and the fixed
direction ``u`` is a colourless singlet. This is Gunaydin-Gursey (1973) colour
``SU(3)`` -- a quark triplet ``3``, an antiquark ``3bar``, and a lepton-like
singlet ``1`` -- extracted here as an exact rational census, not a numerical
approximation.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import List, Sequence, Tuple

from .octonion import E, ONE, Octonion, octonion

Matrix = Tuple[Tuple[Fraction, ...], ...]

# -- exact rational linear algebra (dependency free) ------------------------


def _rref(rows: List[List[Fraction]]) -> Tuple[List[List[Fraction]], List[int]]:
    """Reduced row echelon form over Q; returns the matrix and pivot columns."""
    mat = [list(r) for r in rows]
    if not mat:
        return mat, []
    cols = len(mat[0])
    pivots: List[int] = []
    pivot_row = 0
    for col in range(cols):
        sel = None
        for r in range(pivot_row, len(mat)):
            if mat[r][col] != 0:
                sel = r
                break
        if sel is None:
            continue
        mat[pivot_row], mat[sel] = mat[sel], mat[pivot_row]
        piv = mat[pivot_row][col]
        mat[pivot_row] = [v / piv for v in mat[pivot_row]]
        for r in range(len(mat)):
            if r != pivot_row and mat[r][col] != 0:
                f = mat[r][col]
                mat[r] = [a - f * b for a, b in zip(mat[r], mat[pivot_row])]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == len(mat):
            break
    return mat, pivots


def _null_space(rows: List[List[Fraction]], width: int) -> List[List[Fraction]]:
    """Exact basis of ``{x : rows @ x = 0}`` as a list of rational vectors."""
    if not rows:
        return [[Fraction(1) if i == j else Fraction(0) for i in range(width)]
                for j in range(width)]
    mat, pivots = _rref(rows)
    pivot_set = set(pivots)
    free = [c for c in range(width) if c not in pivot_set]
    basis: List[List[Fraction]] = []
    for f in free:
        vec = [Fraction(0)] * width
        vec[f] = Fraction(1)
        for i, pc in enumerate(pivots):
            vec[pc] = -mat[i][f]
        basis.append(vec)
    return basis


def _matmul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return tuple(
        tuple(sum((a[i][k] * b[k][j] for k in range(n)), Fraction(0))
              for j in range(n))
        for i in range(n)
    )


def _trace(a: Matrix) -> Fraction:
    return sum((a[i][i] for i in range(len(a))), Fraction(0))


def _negative_definite(sym: Matrix) -> bool:
    """Exact test that a symmetric rational matrix is negative definite.

    Runs symmetric (LDL^T) elimination and checks every pivot is < 0, which is
    Sylvester's law of inertia applied exactly over the rationals.
    """
    n = len(sym)
    m = [[sym[i][j] for j in range(n)] for i in range(n)]
    for k in range(n):
        piv = m[k][k]
        if piv >= 0:
            return False
        for i in range(k + 1, n):
            if m[i][k] == 0:
                continue
            f = m[i][k] / piv
            for j in range(k, n):
                m[i][j] = m[i][j] - f * m[k][j]
    return True


# -- octonion structure as rational matrices --------------------------------


def _column(op: Sequence[Octonion]) -> Matrix:
    """Assemble the 8x8 rational matrix whose column ``j`` is ``op[j]``."""
    return tuple(
        tuple(op[j].coords[i] for j in range(8)) for i in range(8)
    )


def _apply(mat: Matrix, x: Octonion) -> Octonion:
    coords = tuple(
        sum((mat[i][j] * x.coords[j] for j in range(8)), Fraction(0))
        for i in range(8)
    )
    return Octonion(coords)


def left_mult_matrix(u: Octonion) -> Matrix:
    """Matrix of left multiplication ``x |-> u x`` in the basis ``e_0..e_7``."""
    return _column([u * E[j] for j in range(8)])


def _leibniz_residual_rows() -> List[List[Fraction]]:
    """Rows of the linear system encoding ``D(e_j e_k) = D(e_j)e_k + e_j D(e_k)``.

    Unknowns are the 64 entries ``M[i][j]`` (flattened as ``i*8 + j``), where
    ``D(e_j) = sum_i M[i][j] e_i``. The residual is linear in ``M`` so each
    unknown's contribution is read off by probing a unit matrix entry.
    """
    products = [[E[j] * E[k] for k in range(8)] for j in range(8)]
    rows: List[List[Fraction]] = []
    # One equation per (j, k, output-component p): 8*8*8 = 512 rows.
    for j in range(8):
        for k in range(8):
            for p in range(8):
                row = [Fraction(0)] * 64
                # term1: D(e_j e_k) = sum_m c_m e_m  ->  sum_m c_m M[p][m]
                ejek = products[j][k].coords
                for m in range(8):
                    if ejek[m] != 0:
                        row[p * 8 + m] += ejek[m]
                # term2: -D(e_j) e_k = -sum_i M[i][j] (e_i e_k)
                for i in range(8):
                    coeff = products[i][k].coords[p]
                    if coeff != 0:
                        row[i * 8 + j] -= coeff
                # term3: -e_j D(e_k) = -sum_i M[i][k] (e_j e_i)
                for i in range(8):
                    coeff = products[j][i].coords[p]
                    if coeff != 0:
                        row[i * 8 + k] -= coeff
                rows.append(row)
    return rows


def _vec_to_matrix(vec: Sequence[Fraction]) -> Matrix:
    return tuple(tuple(vec[i * 8 + j] for j in range(8)) for i in range(8))


def derivation_algebra() -> List[Matrix]:
    """Exact basis of the derivation algebra of the octonions (= g2)."""
    rows = _leibniz_residual_rows()
    basis_vecs = _null_space(rows, 64)
    return [_vec_to_matrix(v) for v in basis_vecs]


def is_derivation(mat: Matrix) -> bool:
    """Check the Leibniz rule ``D(e_j e_k) = D(e_j)e_k + e_j D(e_k)`` exactly."""
    for j in range(8):
        for k in range(8):
            lhs = _apply(mat, E[j] * E[k])
            rhs = _apply(mat, E[j]) * E[k] + E[j] * _apply(mat, E[k])
            if lhs.coords != rhs.coords:
                return False
    return True


def _bracket(a: Matrix, b: Matrix) -> Matrix:
    ab = _matmul(a, b)
    ba = _matmul(b, a)
    return tuple(tuple(ab[i][j] - ba[i][j] for j in range(8)) for i in range(8))


def _coordinates_in(basis: List[Matrix], mat: Matrix) -> List[Fraction]:
    """Express ``mat`` in ``basis`` by exact least-squares-free elimination.

    Solves ``sum_a c_a B_a = mat`` for the coordinates ``c_a`` (unique because the
    basis is independent). Returns the coordinate vector.
    """
    dim = len(basis)
    # Build a (64 x dim) system A c = target and reduce.
    aug = []
    for i in range(8):
        for j in range(8):
            row = [basis[a][i][j] for a in range(dim)] + [mat[i][j]]
            aug.append(row)
    reduced, pivots = _rref(aug)
    coords = [Fraction(0)] * dim
    for r, pc in enumerate(pivots):
        if pc < dim:
            coords[pc] = reduced[r][dim]
    return coords


def _killing_form(basis: List[Matrix]) -> Matrix:
    """Killing form ``K_ab = tr(ad_a ad_b)`` of a Lie algebra given by a basis."""
    dim = len(basis)
    # Structure constants f^c_{ab}: [B_a, B_b] = sum_c f^c_ab B_c.
    struct = [[_coordinates_in(basis, _bracket(basis[a], basis[b]))
               for b in range(dim)] for a in range(dim)]
    # ad_a as a dim x dim matrix: (ad_a)_{c,b} = f^c_{ab}.
    ad = [tuple(tuple(struct[a][b][c] for b in range(dim)) for c in range(dim))
          for a in range(dim)]
    return tuple(
        tuple(_trace(_matmul(ad[a], ad[b])) for b in range(dim))
        for a in range(dim)
    )


def stabiliser_subalgebra(basis: List[Matrix], u: Octonion) -> List[Matrix]:
    """Derivations in ``basis`` that also fix ``u`` (i.e. ``D(u) = 0``)."""
    dim = len(basis)
    # For each output component, D(u) = sum_a c_a (B_a u) = 0 gives one row.
    images = [_apply(b, u) for b in basis]
    rows = [[images[a].coords[p] for a in range(dim)] for p in range(8)]
    sols = _null_space(rows, dim)
    out: List[Matrix] = []
    for sol in sols:
        combo = tuple(
            tuple(sum((sol[a] * basis[a][i][j] for a in range(dim)), Fraction(0))
                  for j in range(8))
            for i in range(8)
        )
        out.append(combo)
    return out


def _is_bracket_closed(basis: List[Matrix]) -> bool:
    """Every bracket of basis elements re-expands in the basis (subalgebra)."""
    dim = len(basis)
    for a in range(dim):
        for b in range(a + 1, dim):
            br = _bracket(basis[a], basis[b])
            coords = _coordinates_in(basis, br)
            recon = tuple(
                tuple(sum((coords[c] * basis[c][i][j] for c in range(dim)),
                          Fraction(0)) for j in range(8))
                for i in range(8)
            )
            if recon != br:
                return False
    return True


def _commutes_with(mat: Matrix, other: Matrix) -> bool:
    return _matmul(mat, other) == _matmul(other, mat)


@dataclass(frozen=True)
class ColorSU3Census:
    """Frozen exact certificate that octonionic symmetry contains colour su(3)."""

    derivation_dimension: int
    all_basis_are_derivations: bool
    g2_bracket_closed: bool
    g2_killing_nondegenerate: bool
    g2_killing_negative_definite: bool
    stabiliser_dimension: int
    stabiliser_bracket_closed: bool
    stabiliser_killing_nondegenerate: bool
    stabiliser_killing_negative_definite: bool
    dimension_forbids_semisimple_split: bool
    complex_structure_squares_to_minus_one: bool
    stabiliser_commutes_with_complex_structure: bool
    fixed_direction_is_singlet: bool


def _det(mat: Matrix) -> Fraction:
    n = len(mat)
    m = [[mat[i][j] for j in range(n)] for i in range(n)]
    det = Fraction(1)
    for col in range(n):
        piv = None
        for r in range(col, n):
            if m[r][col] != 0:
                piv = r
                break
        if piv is None:
            return Fraction(0)
        if piv != col:
            m[col], m[piv] = m[piv], m[col]
            det = -det
        det *= m[col][col]
        inv = m[col][col]
        for r in range(col + 1, n):
            if m[r][col] != 0:
                f = m[r][col] / inv
                m[r] = [m[r][j] - f * m[col][j] for j in range(n)]
    return det


def _sum_of_su2_dims_hits(target: int) -> bool:
    """True if ``target`` is a positive sum of copies of 3 (the only compact
    simple dimension below 8). Used to certify an 8-dim semisimple algebra can
    only be simple."""
    return target % 3 == 0 and target // 3 >= 1


def color_su3_census(u_index: int = 7) -> ColorSU3Census:
    """Build the full exact certificate; ``u = e_{u_index}`` is the fixed axis."""
    g2 = derivation_algebra()
    u = E[u_index]

    g2_killing = _killing_form(g2)
    stab = stabiliser_subalgebra(g2, u)
    stab_killing = _killing_form(stab)

    # Complex structure J = L_u on the octonions; alternativity => J^2 = -I.
    j = left_mult_matrix(u)
    j2 = _matmul(j, j)
    neg_identity = tuple(
        tuple(Fraction(-1) if i == k else Fraction(0) for k in range(8))
        for i in range(8)
    )

    return ColorSU3Census(
        derivation_dimension=len(g2),
        all_basis_are_derivations=all(is_derivation(b) for b in g2),
        g2_bracket_closed=_is_bracket_closed(g2),
        g2_killing_nondegenerate=_det(g2_killing) != 0,
        g2_killing_negative_definite=_negative_definite(g2_killing),
        stabiliser_dimension=len(stab),
        stabiliser_bracket_closed=_is_bracket_closed(stab),
        stabiliser_killing_nondegenerate=_det(stab_killing) != 0,
        stabiliser_killing_negative_definite=_negative_definite(stab_killing),
        dimension_forbids_semisimple_split=(
            len(stab) == 8 and not _sum_of_su2_dims_hits(8)
        ),
        complex_structure_squares_to_minus_one=(j2 == neg_identity),
        stabiliser_commutes_with_complex_structure=all(
            _commutes_with(d, j) for d in stab
        ),
        fixed_direction_is_singlet=all(
            _apply(d, u).is_zero() for d in stab
        ),
    )
