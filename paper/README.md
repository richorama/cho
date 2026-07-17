# Paper sources

`born_rule_theorem.tex` is a self-contained, arXiv-ready LaTeX draft of the
Born-rule selection theorem. It mirrors the prose proof in
[`../BORN_RULE_THEOREM.md`](../BORN_RULE_THEOREM.md); every asserted rational value
is owned by `tests/test_gate_born_rule_theorem.py` (and Q11/Q12).

Build:

```bash
cd paper
pdflatex born_rule_theorem.tex
```

Produces a 4-page PDF. Build artifacts (`*.aux`, `*.log`, `*.out`, `*.pdf`) are
git-ignored.
