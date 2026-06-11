"""peirce_grade_reflection_gate.py -- why the seed grade vector is (0,1,2).

SCOPE (quarantined, diagnostic/exploratory). Moves NO Bayes credit, promotes no
ledger row, touches no frozen registry or scoreboard. Embeds its own octonion
table and imports nothing from compute/. Pure stdlib + fractions (exact).

It attacks the seed-spectrum criterion (4) of the graduation rule. The candidate
seed law

    rho_i / rho_0 = (1, sqrt(Phi), Phi),     Phi = pi / 432,

is the Gibbs minimiser of

    S[rho] = sum_i rho_i log rho_i + Delta * sum_i rho_i d_i,   sum_i rho_i = 1,

with grade vector d = (0, 1, 2) and Delta = -1/2 log(Phi).

peirce_gap_derivation.py already observed that rank(J3(O)) = 3 forces THREE
levels and called (0, 1, 2) "canonical", but it left dangling WHY consecutive
(0, 1, 2) rather than another primitive triple such as (0, 1, 3): it explicitly
enumerates the non-consecutive primitive gradings as un-excluded alternatives,
and it checks the Gibbs law only numerically.

This module closes that gap on the ACTUAL Albert algebra, exactly (Fractions).

PROVED (exact, asserted tripwires; EXIT 0 standalone and inside the sweep):
  [A] the embedded octonions are a valid composition algebra: e_a^2 = -1,
      alternative ((aa)b = a(ab)), and norm-multiplicative N(uv) = N(u) N(v);
  [B] J3(O) is built explicitly (27-dim Albert algebra) with the Jordan product
      X o Y = 1/2 (XY + YX); the diagonal frame (E11, E22, E33) is a complete,
      orthogonal, idempotent system, each idempotent of trace 1, with Jordan unit
      E11 + E22 + E33;
  [C] the Peirce decomposition is exact: every one of the 27 natural basis
      vectors is a simultaneous eigenvector of (L_E11, L_E22, L_E33); the diagonal
      pieces J_ii are 1-dim (eigen-pattern a delta) and the off-diagonal pieces
      J_ij are 8-dim (eigen-pattern 1/2 on i,j) -- the (1, 8) Peirce pattern that
      certifies the frame is PRIMITIVE;
  [D] the grade operator L_N with N = 0 E11 + 1 E22 + 2 E33 is diagonal with
      spectrum {0^1, (1/2)^8, 1^9, (3/2)^8, 2^1}: the diagonal idempotents sit at
      the INTEGER levels 0, 1, 2 while the octonionic Peirce spaces J_ij sit at
      the HALF levels 1/2, 1, 3/2 (the WZ "half-flux" appearing intrinsically);
  [E] FORCING. The boundary reversal sigma -- swap the two ordered endpoints
      E11 <-> E33 and fix the midpoint E22 -- is a genuine Jordan automorphism of
      J3(O), and it sends the grade element N to its reverse. Hence the grade
      operator transforms L_N -> L_{sigma N}, and

          L_N + L_{sigma N} = 2 * Id    (verified EXACTLY)

      holds iff the grades are equally spaced (d_0 + d_2 = 2 d_1). Enumerating the
      primitive rank-3 gradings, (0, 1, 2) is the UNIQUE reversal-covariant one --
      every non-consecutive primitive triple ((0,1,3), (0,2,3), ...) FAILS. So
      (0, 1, 2) is FORCED by the reversal symmetry, not merely "canonical";
  [F] the exact Gibbs minimiser is rho_i proportional to exp(-Delta d_i); the
      geometric-mean seed law rho_1^2 = rho_0 rho_2 is EQUIVALENT to equal spacing
      (2 d_1 - d_0 - d_2 = 0) and therefore holds for EVERY Delta -- a falsifiable
      prediction that is INDEPENDENT of the value of Phi (it survives even if
      pi/432 is wrong). Specialising exp(-Delta) = sqrt(Phi) reproduces
      (1, sqrt(Phi), Phi).

OPEN (unchanged; stated, not hidden):
  * Phi = pi/432 itself is NOT derived here (that is the separate pi/432 claim);
  * that the entropy functional and the locking exp(-Delta) = sqrt(Phi) are
    forced rather than postulated is NOT shown;
  * the full quantised action from CHO dynamics is NOT derived.

KILL: had L_N + L_{sigma N} failed to be a multiple of Id for (0, 1, 2), or had
any non-consecutive primitive triple passed reversal-covariance, the (0, 1, 2)
grade -- and with it the geometric-mean seed law -- would be an unforced ansatz.

Run:
    PYTHONDONTWRITEBYTECODE=1 python3 \
        experiments/pi432_action_search/peirce_grade_reflection_gate.py
"""

from __future__ import annotations

from fractions import Fraction as Fr
import math


# --------------------------------------------------------------------------
# [A] Octonions  (embedded; same Fano convention as compute/octonion_toolkit)
# --------------------------------------------------------------------------

FANO_TRIPLES = ((1, 2, 3), (1, 4, 5), (1, 7, 6), (2, 4, 6),
                (2, 5, 7), (3, 4, 7), (3, 6, 5))


def _build_oct_table() -> dict[tuple[int, int], tuple[int, int]]:
    """basis product table: (a, b) -> (index c, sign s) meaning e_a e_b = s e_c."""
    prod: dict[tuple[int, int], tuple[int, int]] = {}
    for a in range(8):
        prod[(0, a)] = (a, 1)
        prod[(a, 0)] = (a, 1)
    for a in range(1, 8):
        prod[(a, a)] = (0, -1)
    for x, y, z in FANO_TRIPLES:
        for p, q, r in ((x, y, z), (y, z, x), (z, x, y)):
            prod[(p, q)] = (r, 1)
            prod[(q, p)] = (r, -1)
    return prod


_OCT = _build_oct_table()


def oct_mult(u: list[Fr], v: list[Fr]) -> list[Fr]:
    res = [Fr(0)] * 8
    for a in range(8):
        ua = u[a]
        if ua == 0:
            continue
        for b in range(8):
            vb = v[b]
            if vb == 0:
                continue
            c, s = _OCT[(a, b)]
            term = ua * vb
            res[c] += term if s > 0 else -term
    return res


def oct_conj(u: list[Fr]) -> list[Fr]:
    return [u[0]] + [-x for x in u[1:]]


def oct_norm2(u: list[Fr]) -> Fr:
    return sum((x * x for x in u), Fr(0))


def e_unit(i: int) -> list[Fr]:
    u = [Fr(0)] * 8
    u[i] = Fr(1)
    return u


def check_octonions() -> None:
    one = e_unit(0)
    # e_a^2 = -1 for imaginary units
    for a in range(1, 8):
        ea = e_unit(a)
        assert oct_mult(ea, ea) == [Fr(-1)] + [Fr(0)] * 7, f"e_{a}^2 != -1"
    # alternative law (aa)b == a(ab) on basis units
    for a in range(8):
        for b in range(8):
            ea, eb = e_unit(a), e_unit(b)
            lhs = oct_mult(oct_mult(ea, ea), eb)
            rhs = oct_mult(ea, oct_mult(ea, eb))
            assert lhs == rhs, f"alternativity fails at ({a},{b})"
    # composition / norm multiplicativity on rational test vectors
    u = [Fr(1), Fr(-2), Fr(3), Fr(0), Fr(1, 2), Fr(0), Fr(-1), Fr(2)]
    v = [Fr(0), Fr(1), Fr(1), Fr(-1), Fr(2), Fr(3), Fr(0), Fr(1, 3)]
    assert oct_norm2(oct_mult(u, v)) == oct_norm2(u) * oct_norm2(v), "norm not multiplicative"
    assert oct_mult(u, one) == u and oct_mult(one, u) == u, "1 not octonion unit"


# --------------------------------------------------------------------------
# [B] Albert algebra J3(O): 27 real coords = 3 diagonal + 3 octonion slots
#     coords:  0,1,2 = a1,a2,a3 ;  3..10 = x12 ; 11..18 = x13 ; 19..26 = x23
# --------------------------------------------------------------------------

DIM = 27
SLOTS = {(0, 1): 3, (0, 2): 11, (1, 2): 19}  # upper-triangle octonion offsets


def vec_to_mat(v: list[Fr]) -> list[list[list[Fr]]]:
    """27-vector -> 3x3 octonion-Hermitian matrix (full, lower = conj of upper)."""
    mat = [[[Fr(0)] * 8 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        mat[i][i] = [v[i]] + [Fr(0)] * 7
    for (i, j), off in SLOTS.items():
        xij = list(v[off:off + 8])
        mat[i][j] = xij
        mat[j][i] = oct_conj(xij)
    return mat


def mat_to_vec(mat: list[list[list[Fr]]]) -> list[Fr]:
    """Hermitian 3x3 octonion matrix -> 27-vector (asserts Hermiticity)."""
    v = [Fr(0)] * DIM
    for i in range(3):
        diag = mat[i][i]
        assert all(c == 0 for c in diag[1:]), "diagonal entry not real"
        v[i] = diag[0]
    for (i, j), off in SLOTS.items():
        xij, xji = mat[i][j], mat[j][i]
        assert oct_conj(xij) == xji, "matrix not Hermitian"
        for k in range(8):
            v[off + k] = xij[k]
    return v


def matmul(a: list[list[list[Fr]]], b: list[list[list[Fr]]]) -> list[list[list[Fr]]]:
    """ordinary (nonassociative) 3x3 matrix product over octonion entries."""
    out = [[[Fr(0)] * 8 for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for k in range(3):
            acc = [Fr(0)] * 8
            for j in range(3):
                prod = oct_mult(a[i][j], b[j][k])
                for t in range(8):
                    acc[t] += prod[t]
            out[i][k] = acc
    return out


def jordan(u: list[Fr], v: list[Fr]) -> list[Fr]:
    """Jordan product u o v = 1/2 (uv + vu)."""
    x, y = vec_to_mat(u), vec_to_mat(v)
    xy, yx = matmul(x, y), matmul(y, x)
    half = Fr(1, 2)
    summ = [[[half * (xy[i][j][t] + yx[i][j][t]) for t in range(8)]
             for j in range(3)] for i in range(3)]
    return mat_to_vec(summ)


def basis(k: int) -> list[Fr]:
    v = [Fr(0)] * DIM
    v[k] = Fr(1)
    return v


def scal(c: Fr, v: list[Fr]) -> list[Fr]:
    return [c * x for x in v]


def add(u: list[Fr], v: list[Fr]) -> list[Fr]:
    return [a + b for a, b in zip(u, v)]


UNIT = add(add(basis(0), basis(1)), basis(2))  # Jordan identity = E11 + E22 + E33


def frame_idempotent(i: int) -> list[Fr]:
    return basis(i)  # E_ii


def trace(v: list[Fr]) -> Fr:
    return v[0] + v[1] + v[2]


def check_frame() -> None:
    e = [frame_idempotent(i) for i in range(3)]
    for i in range(3):
        assert jordan(e[i], e[i]) == e[i], f"E{i}{i} not idempotent"
        assert trace(e[i]) == 1, f"trace(E{i}{i}) != 1"
    for i in range(3):
        for j in range(3):
            if i != j:
                assert jordan(e[i], e[j]) == [Fr(0)] * DIM, f"E{i},E{j} not orthogonal"
    assert add(add(e[0], e[1]), e[2]) == UNIT, "frame not complete"
    # Jordan unit acts as identity
    for k in range(DIM):
        assert jordan(UNIT, basis(k)) == basis(k), "unit not identity"


# --------------------------------------------------------------------------
# [C]/[D] Peirce decomposition and the grade operator
# --------------------------------------------------------------------------

def slot_of(k: int) -> tuple[int, int] | None:
    """which Peirce piece basis index k belongs to: None for diagonal i==k."""
    if k < 3:
        return None
    for (i, j), off in SLOTS.items():
        if off <= k < off + 8:
            return (i, j)
    raise AssertionError("bad index")


def peirce_eigs(k: int) -> tuple[Fr, Fr, Fr]:
    """predicted (L_E0, L_E1, L_E2) eigenvalues on natural basis vector k."""
    s = slot_of(k)
    if s is None:               # diagonal idempotent E_kk
        return tuple(Fr(1) if i == k else Fr(0) for i in range(3))  # type: ignore
    i, j = s                    # off-diagonal J_ij
    half = Fr(1, 2)
    return tuple(half if t in (i, j) else Fr(0) for t in range(3))  # type: ignore


def grade_element(d: tuple[int, int, int]) -> list[Fr]:
    """N = d0 E11 + d1 E22 + d2 E33."""
    v = [Fr(0)] * DIM
    v[0], v[1], v[2] = Fr(d[0]), Fr(d[1]), Fr(d[2])
    return v


def grade_eig(d: tuple[int, int, int], k: int) -> Fr:
    """predicted L_N eigenvalue on basis k for N built from grades d."""
    e0, e1, e2 = peirce_eigs(k)
    return d[0] * e0 + d[1] * e1 + d[2] * e2


def verify_peirce_and_grade(d: tuple[int, int, int]) -> dict[Fr, int]:
    """assert every basis vector is the predicted simultaneous eigenvector;
    return the L_N spectrum as {eigenvalue: multiplicity}."""
    e = [frame_idempotent(i) for i in range(3)]
    n = grade_element(d)
    mult: dict[Fr, int] = {}
    for k in range(DIM):
        bk = basis(k)
        pe = peirce_eigs(k)
        for i in range(3):
            assert jordan(e[i], bk) == scal(pe[i], bk), f"L_E{i} not diagonal at {k}"
        lam = grade_eig(d, k)
        assert jordan(n, bk) == scal(lam, bk), f"L_N not diagonal at {k}"
        mult[lam] = mult.get(lam, 0) + 1
    return mult


# --------------------------------------------------------------------------
# [E] Boundary reversal sigma  (swap endpoints E11 <-> E33, fix E22)
# --------------------------------------------------------------------------

PERM = {0: 2, 1: 1, 2: 0}


def sigma_vec(v: list[Fr]) -> list[Fr]:
    mat = vec_to_mat(v)
    swapped = [[mat[PERM[i]][PERM[j]] for j in range(3)] for i in range(3)]
    return mat_to_vec(swapped)


def check_sigma_is_automorphism() -> None:
    # sigma(X o Y) == sigma(X) o sigma(Y) on every basis pair (o is symmetric)
    for i in range(DIM):
        bi = basis(i)
        sbi = sigma_vec(bi)
        for j in range(i, DIM):
            bj = basis(j)
            lhs = sigma_vec(jordan(bi, bj))
            rhs = jordan(sbi, sigma_vec(bj))
            assert lhs == rhs, f"sigma not a Jordan automorphism at ({i},{j})"
    # sigma swaps the ordered endpoints and fixes the midpoint
    assert sigma_vec(frame_idempotent(0)) == frame_idempotent(2)
    assert sigma_vec(frame_idempotent(2)) == frame_idempotent(0)
    assert sigma_vec(frame_idempotent(1)) == frame_idempotent(1)
    assert sigma_vec(UNIT) == UNIT


def reverse(d: tuple[int, int, int]) -> tuple[int, int, int]:
    return (d[2], d[1], d[0])


def reversal_covariant(d: tuple[int, int, int]) -> bool:
    """L_N + L_{sigma N} proportional to Id  <=>  d + reverse(d) constant."""
    s = tuple(a + b for a, b in zip(d, reverse(d)))
    return s[0] == s[1] == s[2]


def operator_sum_is_scalar(d: tuple[int, int, int]) -> tuple[bool, Fr | None]:
    """build L_N + L_{sigma N} on the algebra and test it equals c * Id exactly."""
    n, sn = grade_element(d), grade_element(reverse(d))
    c0 = None
    for k in range(DIM):
        bk = basis(k)
        image = add(jordan(n, bk), jordan(sn, bk))
        # must be a scalar multiple of bk with the SAME scalar for all k
        coeff = grade_eig(d, k) + grade_eig(reverse(d), k)
        assert image == scal(coeff, bk), "operator sum not diagonal"
        if c0 is None:
            c0 = coeff
        elif coeff != c0:
            return (False, None)
    return (True, c0)


def primitive_rank3_gradings(max_grade: int = 5) -> list[tuple[int, int, int]]:
    """shifted (0,b,c) with distinct levels and gcd of pairwise gaps == 1."""
    out = []
    for b in range(1, max_grade + 1):
        for c in range(b + 1, max_grade + 1):
            diffs = [b, c, c - b]
            g = diffs[0]
            for x in diffs[1:]:
                g = math.gcd(g, x)
            if g == 1:
                out.append((0, b, c))
    return out


# --------------------------------------------------------------------------
# [F] Gibbs minimiser and the Phi-independent seed law
# --------------------------------------------------------------------------

def spacing_defect(d: tuple[int, int, int]) -> int:
    """2 d1 - d0 - d2 ; zero iff equally spaced iff rho_1^2 = rho_0 rho_2."""
    return 2 * d[1] - d[0] - d[2]


def gibbs_distribution(d: tuple[int, int, int], delta: float) -> tuple[float, float, float]:
    w = [math.exp(-delta * g) for g in d]
    z = sum(w)
    return tuple(x / z for x in w)  # type: ignore


def main() -> bool:
    print("=" * 78)
    print("PEIRCE-GRADE REFLECTION GATE  --  why the seed grade vector is (0,1,2)")
    print("=" * 78)

    # [A]
    check_octonions()
    print("\n[A] Octonions")
    print("  e_a^2 = -1, alternative, norm-multiplicative : OK")

    # [B]
    check_frame()
    print("\n[B] Albert algebra J3(O) and the diagonal frame")
    print(f"  dimension                                    : {DIM}")
    print("  (E11,E22,E33) complete orthogonal idempotents, trace 1, unit sum : OK")

    # [C] + [D]
    grades = (0, 1, 2)
    spectrum = verify_peirce_and_grade(grades)
    spec_sorted = sorted(spectrum.items(), key=lambda kv: kv[0])
    print("\n[C] Peirce decomposition (simultaneous L_E_ii eigenbasis)")
    print("  diagonal pieces J_ii : dim 1 each   (eigen-pattern delta)")
    print("  off-diagonal J_ij    : dim 8 each   (eigen-pattern 1/2 on i,j)")
    print("  (1,8) pattern certifies the frame is PRIMITIVE")
    print("\n[D] Grade operator L_N, N = 0 E11 + 1 E22 + 2 E33")
    print("  spectrum {eigenvalue: multiplicity}:")
    for lam, m in spec_sorted:
        tag = "  <- integer level (idempotent)" if lam.denominator == 1 and m == 1 else ""
        if lam.denominator == 2:
            tag = "  <- HALF level (octonionic Peirce space J_ij)"
        print(f"    {str(lam):>4} : {m}{tag}")
    assert spectrum == {Fr(0): 1, Fr(1, 2): 8, Fr(1): 9, Fr(3, 2): 8, Fr(2): 1}
    assert sum(spectrum.values()) == DIM

    # [E]
    check_sigma_is_automorphism()
    ok_012, c_012 = operator_sum_is_scalar((0, 1, 2))
    print("\n[E] Boundary reversal sigma (swap endpoints E11<->E33, fix E22)")
    print("  sigma is a Jordan automorphism of J3(O)      : OK")
    print("  sigma sends grade element N to its reverse   : OK")
    print(f"  L_N + L_(sigma N) = c * Id for (0,1,2)        : {ok_012}, c = {c_012}")
    assert ok_012 and c_012 == Fr(2), "reversal identity L_N + L_sigmaN = 2 Id failed"

    primitives = primitive_rank3_gradings()
    passing = [d for d in primitives if reversal_covariant(d)]
    print("\n  primitive rank-3 gradings vs reversal-covariance:")
    for d in primitives:
        cov = reversal_covariant(d)
        consec = (d == (0, 1, 2))
        flag = "reversal-COVARIANT" if cov else "fails reversal"
        extra = "  (consecutive)" if consec else ""
        # cross-check: the algebra-level operator test agrees with the arithmetic test
        ok_op, _ = operator_sum_is_scalar(d)
        assert ok_op == cov, f"operator test disagrees with arithmetic test at {d}"
        print(f"    {d}: {flag}{extra}")
    print(f"  reversal-covariant primitive gradings        : {passing}")
    assert passing == [(0, 1, 2)], "(0,1,2) is NOT the unique reversal-covariant primitive grading"

    # [F]
    print("\n[F] Gibbs minimiser and the Phi-independent seed law")
    print("  stationary point of S[rho] = sum rho log rho + Delta sum rho d :")
    print("      rho_i  proportional to  exp(-Delta d_i)")
    print("  geometric-mean law rho_1^2 = rho_0 rho_2  <=>  2 d_1 - d_0 - d_2 = 0")
    for d in [(0, 1, 2), (0, 1, 3), (0, 2, 3)]:
        print(f"    d={d}: spacing defect 2 d1 - d0 - d2 = {spacing_defect(d)}"
              f"  -> geometric-mean law {'HOLDS' if spacing_defect(d) == 0 else 'fails'}")
    assert spacing_defect((0, 1, 2)) == 0
    assert all(spacing_defect(d) != 0 for d in primitives if d != (0, 1, 2))

    # numeric specialisation exp(-Delta) = sqrt(Phi), Phi = pi/432
    phi = math.pi / 432.0
    delta = -0.5 * math.log(phi)
    rho = gibbs_distribution((0, 1, 2), delta)
    r1, r2 = rho[1] / rho[0], rho[2] / rho[0]
    target = (1.0, math.sqrt(phi), phi)
    gm_residual = abs(rho[1] * rho[1] - rho[0] * rho[2])
    print("\n  numeric specialisation exp(-Delta) = sqrt(Phi), Phi = pi/432:")
    print(f"    Phi                       : {phi:.15f}")
    print(f"    Delta = -1/2 log(Phi)     : {delta:.15f}")
    print(f"    rho_1/rho_0  vs sqrt(Phi) : {r1:.15f}  vs {target[1]:.15f}")
    print(f"    rho_2/rho_0  vs Phi       : {r2:.15f}  vs {target[2]:.15f}")
    print(f"    geometric-mean residual rho_1^2 - rho_0 rho_2 : {gm_residual:.3e}")
    assert abs(r1 - math.sqrt(phi)) < 1e-15
    assert abs(r2 - phi) < 1e-15
    assert gm_residual < 1e-18

    print("\n[V] Sandbox verdict")
    print("  grade vector (0,1,2)            : FORCED by boundary-reversal covariance")
    print("                                    (unique among primitive rank-3 gradings)")
    print("  octonionic Peirce spaces J_ij   : sit at the HALF levels 1/2, 1, 3/2")
    print("  geometric-mean seed law         : rho_1^2 = rho_0 rho_2  (Phi-INDEPENDENT,")
    print("                                    falsifiable; survives even if pi/432 wrong)")
    print("  Phi = pi/432 and exp(-Delta)=sqrt(Phi) forced : OPEN (separate claim)")
    print("  full action from CHO dynamics                 : OPEN")
    print("=" * 78)
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
