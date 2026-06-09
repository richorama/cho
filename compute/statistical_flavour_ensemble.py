"""
BIG-BETS Bet 3 (EXPLORATORY) -- stop predicting single Yukawas; predict their
DISTRIBUTION.  Does a CHO-constrained ensemble beat a symmetry-blind one?
=============================================================================

The CHO program is *losing* the one-number coincidence game (scoreboard floor
ln B = -3.2): every CKM/PMNS entry is staked as a single fragile value
(C1: |V_us| = sqrt(7) eps0, C2: |V_cb| = eps0/2, ...).  Bet 3 of BIG_BETS_PLAN.md
proposes the honest fallback: random-matrix theory makes the *distribution* of a
Yukawa ensemble fundamental, turning one brittle coincidence into many correlated,
falsifiable statistical observables.  This module runs the comparison the plan's
kill condition demands -- "if a symmetry-blind ensemble fits as well as the
CHO-constrained one, CHO adds nothing."

The four ensembles (3x3 complex Yukawas; two independent draws per sample, the
up and down sectors, with CKM = U_u^dag U_d read from the left singular vectors):

  A  ANARCHY            i.i.d. complex Ginibre -- all entries O(1), no hierarchy,
                        no texture zeros (the symmetry-BLIND null).
  B  FN HIERARCHY       Froggatt-Nielsen scaling M_ij ~ eps^(q_i+q_j), charges
                        (2,1,0) -- the mass hierarchy ONLY, still no texture zero.
  C  CHO-NNI            FN scaling + the nearest-neighbour-interaction zeros at
                        (1,1),(1,3),(3,1) (the full Fritzsch/NNI texture).
  D  TRIALITY-ONLY      FN scaling + ONLY the (1,3),(3,1) zero -- the single zero
                        triality actually DERIVES (gen1<->gen3 needs two tau steps
                        => doubly suppressed => texture zero, per ckm_from_triality).

What the ensembles say (stable across seeds; see [B]-[E]):

  (+) THE REAL WIN -- distributions kill the symmetry-blind null where the data
      are hierarchical.  Anarchy produces LARGE mixing (median sin^2 ~ 0.3-0.5) and
      essentially NEVER reproduces the tiny quark angles: P(all three CKM moduli as
      small as observed) ~ 0.  Yet the SAME anarchy is perfectly viable for leptons
      (it makes a PMNS-sized theta13 a few % of the time).  The observed quark/lepton
      dichotomy -- "anarchy with structure" -- falls straight out, and it is content
      the single-number predictions never had.  This is the plan's promise delivered.

  (-) THE HONEST NULL -- what beats anarchy is the HIERARCHY, not the CHO texture.
      The famous Gatto-Sartori-Tonin relation |V_us| ~ sqrt(m_d/m_s) (the observed
      coincidence 0.2243 ~ 0.2236) is a CORRELATION between a mixing angle and a mass
      ratio.  Anarchy shows none (corr ~ 0).  But the Froggatt-Nielsen hierarchy
      ALONE (ensemble B, no texture zero) already produces most of it (corr ~ +0.47),
      because in FN both |V_us| and sqrt(m_d/m_s) scale as eps^(q1-q2).  Adding CHO's
      DERIVED triality zero (D) lifts the correlation only marginally (+0.05..0.07).
      The discriminating power is carried by the mass hierarchy -- which is the SAME
      charged input the scoreboard already debits (the eps-ladder / power-of-3
      exponents, F0) -- while the octonionic texture zero is a sub-dominant refinement
      that no symmetry-blind ensemble with the same hierarchy is missing.  And the
      NNI texture is not unique to CHO: every Froggatt-Nielsen model emits it.

Conclusion.  Going to distributions is a genuine methodological win: it converts the
losing one-number game into a many-observable game and decisively falsifies pure
anarchy for quarks.  But it does NOT move CHO credit -- the part that beats the
symmetry-blind baseline is the mass hierarchy (an input the ledger already charges),
and CHO's derived triality texture zero is a measurable but sub-dominant refinement
that does not single out CHO.  Same FORM-not-CONTENT boundary the Lambda, gravity,
and growth-index probes drew, now on the flavour-statistics face.

VERDICT: EXPLORATORY.  The single-value CKM bridges (C1..C4) are untouched and no
Bayes credit moves.  The module asserts the real positive (anarchy killed for
quarks, viable for leptons; the hierarchy carries the GST correlation) AND the
honest-null tripwire (the hierarchy's contribution to the correlation strictly
exceeds the CHO texture zero's, so the texture is not what beats symmetry-blind).
"""
import numpy as np

# --- CHO inputs under test (NOT outputs of this statistics) ---
EPS0_SQ = np.pi / 432.0              # ledger F0: triality-breaking parameter pi/(16*27)
EPS0 = np.sqrt(EPS0_SQ)              # ~ 0.0853
FN_CHARGES = (2, 1, 0)              # Froggatt-Nielsen charges -> M_ij ~ eps^(q_i+q_j)

# --- observed flavour data (PDG / NuFIT, mirrored from chi_squared.py) ---
M_D, M_S = 4.67e-3, 93.4e-3         # GeV; sqrt(m_d/m_s) is the GST scale
SQRT_MD_MS = np.sqrt(M_D / M_S)     # ~ 0.2236, the observed |V_us| coincidence
VUS_OBS, VCB_OBS, VUB_OBS = 0.2243, 0.0422, 0.00394
S13_QUARK = VUB_OBS ** 2            # quark "theta13": sin^2 ~ |V_ub|^2 ~ 1.6e-5
S13_LEPTON = 0.02203               # lepton theta13: sin^2 theta_13 (PMNS)
PMNS_SIN2 = (0.307, 0.572, 0.02203)  # (12, 23, 13), large -> anarchy-compatible

# --- ensemble controls (FIXED seed => deterministic asserts) ---
SEED = 1
N_SAMPLES = 6000
ENSEMBLES = ("A", "B", "C", "D")

# --- decision thresholds (set with margin around the seed-stable values) ---
ANARCHY_LARGE_MIN = 0.15           # anarchy median sin^2 theta13 is "large"
QUARK_KILL_MAX = 2e-3              # P(anarchy as small as quark CKM) is ~ 0
LEPTON_VIABLE_MIN = 0.01           # anarchy makes a lepton-sized theta13 >1% of the time
CONTRAST_MIN = 10.0                # lepton-viable / quark-viable fraction ratio
CORR_ZERO_MAX = 0.12               # anarchy GST correlation is ~ 0
CORR_HIER_MIN = 0.30               # FN hierarchy ALONE already correlates
TEXTURE_INCREMENT_MAX = 0.25       # CHO texture zero adds only a small increment
GST_COINCIDENCE_TOL = 0.02         # |sqrt(m_d/m_s) - |V_us|_obs| (the observed relation)


def fn_scale():
    """Froggatt-Nielsen suppression matrix M_ij ~ eps^(q_i + q_j)."""
    q = np.array(FN_CHARGES)
    return EPS0 ** (q[:, None] + q[None, :])


FN = fn_scale()


def draw_yukawa(kind, rng):
    """One 3x3 complex Yukawa from the named ensemble.

    A: anarchy (Ginibre).  B: FN hierarchy.  C: NNI texture zeros (1,1),(1,3),(3,1).
    D: only the triality-derived (1,3),(3,1) zero.
    """
    M = (rng.standard_normal((3, 3)) + 1j * rng.standard_normal((3, 3))) / np.sqrt(2)
    if kind == "A":
        return M
    M = M * FN
    if kind == "C":
        M[0, 0] = 0.0
        M[0, 2] = 0.0
        M[2, 0] = 0.0
    elif kind == "D":
        M[0, 2] = 0.0
        M[2, 0] = 0.0
    return M


def diagonalize(M):
    """Left singular vectors (ascending singular value) and the singular values.
    Singular values are the masses; the left unitary rotates the up/down sector."""
    U, s, _ = np.linalg.svd(M)
    order = np.argsort(s)               # ascending: index 0 = lightest generation
    return U[:, order], s[order]


def ckm_matrix(Mu, Md):
    """W = U_u^dag U_d, the mixing matrix from two sector Yukawas."""
    Uu, _ = diagonalize(Mu)
    Ud, _ = diagonalize(Md)
    return Uu.conj().T @ Ud


def mixing_moduli(W):
    """(|V_us|, |V_cb|, |V_ub|) read at the standard CKM positions."""
    return abs(W[0, 1]), abs(W[1, 2]), abs(W[0, 2])


def mixing_sin2(W):
    """(sin^2 theta12, sin^2 theta23, sin^2 theta13) in the PDG convention."""
    s13 = abs(W[0, 2]) ** 2
    den = max(1.0 - s13, 1e-12)
    s12 = abs(W[0, 1]) ** 2 / den
    s23 = abs(W[1, 2]) ** 2 / den
    return s12, s23, s13


def sample_ensemble(kind, n, rng):
    """Monte-Carlo a CKM ensemble; return arrays of observables."""
    vus = np.empty(n)
    vcb = np.empty(n)
    vub = np.empty(n)
    s12 = np.empty(n)
    s23 = np.empty(n)
    s13 = np.empty(n)
    sqrt_ratio_down = np.empty(n)       # sqrt(m1/m2) of the down sector (GST scale)
    for i in range(n):
        Mu = draw_yukawa(kind, rng)
        Md = draw_yukawa(kind, rng)
        _, sd = diagonalize(Md)
        W = ckm_matrix(Mu, Md)
        vus[i], vcb[i], vub[i] = mixing_moduli(W)
        s12[i], s23[i], s13[i] = mixing_sin2(W)
        sqrt_ratio_down[i] = np.sqrt(sd[0] / sd[1])
    return {
        "vus": vus, "vcb": vcb, "vub": vub,
        "s12": s12, "s23": s23, "s13": s13,
        "sqrt_ratio_down": sqrt_ratio_down,
    }


def gst_correlation(data):
    """Pearson correlation of |V_us| with sqrt(m_d/m_s) across the ensemble."""
    return float(np.corrcoef(data["vus"], data["sqrt_ratio_down"])[0, 1])


def quark_kill_fraction(data):
    """Fraction of draws with ALL three CKM moduli at or below the observed
    (tiny) quark values -- the probability anarchy looks like the quark sector."""
    return float(np.mean((data["vus"] <= VUS_OBS)
                         & (data["vcb"] <= VCB_OBS)
                         & (data["vub"] <= VUB_OBS)))


def s13_tail_fraction(data, threshold):
    """Fraction of draws with sin^2 theta13 at or below a threshold."""
    return float(np.mean(data["s13"] <= threshold))


def run_ensembles(n=N_SAMPLES, seed=SEED):
    rng = np.random.default_rng(seed)
    return {k: sample_ensemble(k, n, rng) for k in ENSEMBLES}


def main():
    print("=" * 70)
    print("BIG-BETS Bet 3: predict the Yukawa DISTRIBUTION, not single values  (EXPLORATORY)")
    print("=" * 70)

    data = run_ensembles()
    A, B, C, D = (data[k] for k in "ABCD")

    # ---- [A] the arena ----
    print("\n[A] Four 3x3 complex-Yukawa ensembles (CKM = U_u^dag U_d):")
    print("    A anarchy (Ginibre, symmetry-BLIND)   B FN hierarchy eps^(qi+qj), no zeros")
    print("    C NNI texture (1,1),(1,3) zeros        D triality-derived (1,3) zero only")
    print("    eps0=%.4f  sqrt(m_d/m_s)=%.4f  |V_us|_obs=%.4f  (the GST coincidence)"
          % (EPS0, SQRT_MD_MS, VUS_OBS))

    # ---- [B] anarchy is killed for quarks ----
    print("\n[B] Symmetry-blind anarchy vs the hierarchical quark sector:")
    med = lambda d, k: float(np.median(d[k]))
    print("    anarchy median sin^2 (12,23,13) = (%.3f, %.3f, %.3f) -- LARGE mixing"
          % (med(A, "s12"), med(A, "s23"), med(A, "s13")))
    p_quark = quark_kill_fraction(A)
    print("    P(anarchy all CKM moduli <= observed quarks) = %.4g  => anarchy KILLED for quarks"
          % p_quark)

    # ---- [C] yet anarchy is viable for leptons ----
    print("\n[C] The SAME anarchy is viable for the anarchic lepton sector:")
    f_lep = s13_tail_fraction(A, S13_LEPTON)
    f_quark = s13_tail_fraction(A, S13_QUARK)
    print("    P(anarchy sin^2 th13 <= lepton %.3f) = %.4g  (PMNS-sized: a few %%)"
          % (S13_LEPTON, f_lep))
    print("    P(anarchy sin^2 th13 <= quark  %.1e) = %.4g  (quark-sized: ~never)"
          % (S13_QUARK, f_quark))
    print("    => the observed quark/lepton dichotomy ('anarchy with structure') falls out.")

    # ---- [D] the GST correlation: the hierarchy carries it ----
    print("\n[D] The GST correlation corr(|V_us|, sqrt(m_d/m_s)) across each ensemble:")
    cA, cB, cC, cD = (gst_correlation(d) for d in (A, B, C, D))
    print("    A anarchy        corr = %+.3f  (no mixing<->mass correlation)" % cA)
    print("    B FN hierarchy   corr = %+.3f  (the HIERARCHY alone already correlates)" % cB)
    print("    C NNI texture    corr = %+.3f" % cC)
    print("    D triality zero  corr = %+.3f  (CHO's DERIVED zero)" % cD)

    # ---- [E] the honest null: hierarchy >> texture zero ----
    print("\n[E] Decomposing the correlation (the plan's kill condition):")
    hier_increment = cB - cA
    texture_increment = cD - cB
    print("    hierarchy contributes (B - A) = %+.3f" % hier_increment)
    print("    CHO texture zero adds  (D - B) = %+.3f" % texture_increment)
    print("    => the discriminator is the mass HIERARCHY (the charged eps-ladder input, F0),")
    print("       not the octonionic texture; a symmetry-blind ensemble with the same hierarchy")
    print("       is not missing it.  And NNI is emitted by every Froggatt-Nielsen model.")

    # ---- [F] verdict ----
    print("\n[F] Verdict")
    print("    (+) distributions turn the losing one-number game into a many-observable one and")
    print("        DECISIVELY falsify symmetry-blind anarchy for quarks (viable for leptons).")
    print("    (-) what beats anarchy is the mass hierarchy (an input the ledger already charges);")
    print("        CHO's derived triality texture zero is a sub-dominant refinement, not the win.")
    print("    Counting the distribution gives the FORM (a sharp falsification), not the CONTENT")
    print("    (a CHO-specific texture that beats same-hierarchy symmetry-blindness).")
    print("    EXPLORATORY: C1..C4 single-value bridges untouched; NO Bayes credit moves.")

    # ---- stable tripwires (the real positive + the honest null) ----
    # The observed GST coincidence the whole comparison is about:
    assert abs(SQRT_MD_MS - VUS_OBS) < GST_COINCIDENCE_TOL, "GST coincidence drifted"
    # (+) anarchy is LARGE mixing and is decisively excluded for the quark sector:
    assert med(A, "s13") > ANARCHY_LARGE_MIN, "anarchy theta13 is not large -- recheck ensemble"
    assert med(A, "s12") > 0.3 and med(A, "s23") > 0.3, "anarchy 12/23 mixing not large"
    assert p_quark < QUARK_KILL_MAX, "anarchy reproduced the quark sector -- not killed"
    # (+) but the SAME anarchy is viable for the anarchic lepton sector (the dichotomy):
    assert f_lep > LEPTON_VIABLE_MIN, "anarchy cannot reach a lepton-sized theta13"
    assert f_lep > CONTRAST_MIN * f_quark, "quark/lepton anarchy contrast collapsed"
    # (-) anarchy carries NO mixing<->mass correlation, the FN hierarchy ALONE does:
    assert abs(cA) < CORR_ZERO_MAX, "anarchy showed a spurious GST correlation"
    assert cB > CORR_HIER_MIN, "FN hierarchy alone failed to produce the GST correlation"
    # (-) the CHO texture zeros do not REDUCE the correlation, but their increment is small:
    assert cC > cB - 0.05 and cD > cB - 0.05, "texture zero unexpectedly destroyed correlation"
    assert texture_increment < TEXTURE_INCREMENT_MAX, "texture increment unexpectedly large"
    # THE HONEST-NULL TRIPWIRE: the hierarchy's contribution to the correlation strictly
    # exceeds the CHO texture zero's, so the texture is NOT what beats symmetry-blindness:
    assert hier_increment > texture_increment, \
        "CHO texture zero out-discriminates the hierarchy -- re-examine, CHO may add real content"
    # The CHO input under test is the kinematic eps-ladder, not an output of this statistics:
    assert abs(EPS0_SQ - np.pi / 432.0) < 1e-15, "eps0^2 input drifted from pi/432"
    return True


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)
