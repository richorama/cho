# arXiv Submission Guide

## Generated PDFs (all compile cleanly)

| Paper | File | Pages | Category | Cross-list |
|-------|------|-------|----------|------------|
| 1. Three Generations | `three_generations.tex` | 9 | hep-th | math-ph |
| 2. Electroweak Parameters | `electroweak_parameters.tex` | 19 | hep-ph | hep-th, math-ph |
| 3. Cosmological Constant | `cosmological_constant.tex` | 12 | hep-th | astro-ph.CO, hep-ph |

---

## Step-by-Step Submission Instructions

### Prerequisites
1. Create an arXiv account at https://arxiv.org/user/register (if you don't have one)
2. You may need to be "endorsed" for hep-th or hep-ph if you're a first-time submitter. Ask a colleague with arXiv papers in that category, or request auto-endorsement.

### Submission Order
**Paper 1 → wait for arXiv ID → Paper 2 → Paper 3**

Each paper is a single `.tex` file with inline `\thebibliography` (no separate `.bib`). No figures.

---

### Submitting Paper 1

1. Go to https://arxiv.org/submit
2. Choose **New submission**
3. **License**: Select "arXiv.org perpetual, non-exclusive license to distribute"
4. **Primary category**: `hep-th`
5. **Cross-list**: `math-ph`
6. **Upload files**: Upload `three_generations.tex` only (single source file)
7. arXiv will compile it automatically with pdflatex
8. **Metadata**:
   - Title: `Three Generations from Octonion Triality: Three Independent Proofs`
   - Authors: `Richard Astbury`
   - Abstract: Copy from the `\begin{abstract}...\end{abstract}` block in the .tex
   - Comments: `9 pages, no figures. Companion papers: arXiv:XXXX.XXXXX, arXiv:YYYY.YYYYY`
   - MSC-class: `17A75, 81R05, 81V22` (octonions, algebraic QFT, unified field)
9. **Preview** the compiled PDF — verify it matches your local version
10. **Submit**
11. **Note the arXiv ID** (e.g., `2406.XXXXX`) — you'll need this for Papers 2 & 3

---

### Before submitting Paper 2

Update the bibliography entry for Paper 1:

```latex
\bibitem{Paper1}
R.~Astbury, ``Three Generations from Octonion Triality:
Three Independent Proofs,'' arXiv:2406.XXXXX [hep-th] (2026).
```

Do the same in Paper 3's `\bibitem{Paper1}`.

---

### Submitting Paper 2

1. Same process as above
2. **Primary category**: `hep-ph`
3. **Cross-list**: `hep-th`, `math-ph`
4. **Upload**: `electroweak_parameters.tex`
5. **Metadata**:
   - Title: `Electroweak Parameters from C⊗H⊗O: Twenty-Three Low-Energy Relations from Few Inputs`
   - Comments: `19 pages, no figures. Companion to arXiv:2406.XXXXX`
   - MSC-class: `81V22, 17A75, 81T13`
6. **Note the arXiv ID** for Paper 3

---

### Submitting Paper 3

1. Update both `\bibitem{Paper1}` and `\bibitem{Paper2}` with real arXiv IDs
2. **Primary category**: `hep-th`
3. **Cross-list**: `astro-ph.CO`, `hep-ph`
4. **Upload**: `cosmological_constant.tex`
5. **Metadata**:
   - Title: `The Cosmological Constant from C⊗H⊗O: Resolution of the Hierarchy`
   - Comments: `12 pages, no figures. Companion to arXiv:2406.XXXXX and arXiv:2406.YYYYY`
   - MSC-class: `83E30, 17A75, 81T13`

---

## Timing Strategy

- **Day 1 (Sunday evening UTC)**: Submit Paper 1. It will appear in Monday's new listings.
- **Day 8-10**: Once Paper 1 has its ID and is publicly visible, submit Paper 2.
- **Day 15-17**: Submit Paper 3 citing both.

Submitting on Sunday evening (before the 14:00 ET Monday deadline) ensures your paper appears at the **top** of Monday's new listing (earlier submissions are listed first).

---

## Compilation Command (local verification)

```bash
cd papers/
pdflatex -interaction=nonstopmode three_generations.tex
pdflatex -interaction=nonstopmode three_generations.tex  # second pass for refs
pdflatex -interaction=nonstopmode electroweak_parameters.tex
pdflatex -interaction=nonstopmode electroweak_parameters.tex
pdflatex -interaction=nonstopmode cosmological_constant.tex
pdflatex -interaction=nonstopmode cosmological_constant.tex
```

All three compile with zero errors. The only warnings are harmless hyperref PDF-string encoding notices in Paper 3 (math in section titles).

---

## Pre-submission Checklist

- [x] All `\cite` keys resolve to `\bibitem` entries
- [x] No TODO/placeholder text remaining
- [x] Abstracts present in all papers
- [x] Cross-references between papers consistent
- [x] Acknowledgments filled in (Paper 2)
- [x] PDFs compile cleanly (zero errors, zero undefined refs)
- [ ] Update `\bibitem{Paper1}` in Papers 2 & 3 with real arXiv ID after posting
- [ ] Update `\bibitem{Paper2}` in Paper 3 with real arXiv ID after posting
- [ ] Update "Comments" field with final companion arXiv IDs
- [ ] Optional: Add ORCID to author field
