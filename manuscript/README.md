# Kimberling's rational-enumeration conjecture

This note proves that first-occurrence cumulative generation under `x/(1+y)`
enumerates the rationals in `(0,1]` in the order defining OEIS A371279 and
A371280. It gives a denominator bound and determines the position
multiplicities in A371353, including a correction to its prime-occurrence
comment, one displayed entry, and one row label. It proves the exact cumulative
minimum `2^(1-n)` and the first-generation formula for dyadic reciprocals.
The rational-coverage mechanism extends the classical Kepler-tree argument
described by Smolinsky (2016) and Dekking (2017); it is not a new rational tree.
The exact closure problem is BMO 2004/5, Round 1, Problem 5. Saha (2025,
Solution 14) and Grytczuk--Kisielewicz--Przeslawski (2026, Theorem 6.2)
give the earlier denominator-descent argument. The continued-fraction
generation bound applies Dajani--de Lepper--Robinson's Kepler path-length lemma.
The linked closure statements A226080(1), (9), and `(1,z+1,c/z)` for positive
integers `c` are reproved with credit to Kimberling and Moses (2014).

## Contents

- `note.tex`: complete proofs, references, and verification scope.
- `metadata.json`: scientific identity, creators, license, and pinned Lean link.
- `verify.py`: standard-library Python checker using exact rational arithmetic.
- `checks.json`: deterministic output of the checker, including finite ranges.

## Build and check

Use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
python3 verify.py --output reproduced-checks.json
cmp checks.json reproduced-checks.json
```

Alternatively use a standard LaTeX distribution:

```sh
pdflatex -no-shell-escape note.tex
pdflatex -no-shell-escape note.tex
```

The bibliography is included directly in `note.tex`; no BibTeX step is required.
The checker needs Python 3.10 or later and no third-party Python packages.
It constructs cumulative lists through `U6`, compares two implementations of
first-occurrence deletion through `U5`, checks denominator-descent expressions
for all `1 <= p <= q <= 400`, and tests position multiplicities through row 40
for values in `U6` with reduced denominator at most 40. These are finite checks;
the universal claims have written proofs in the note.
Additional checks verify the minima of `U1` through `U6`, dyadic first
generations for exponents 0 through 5, all 21 denominator-bound membership
pairs through `q=6`, 6,400 exact unary-map identities and closure witnesses
with `1 <= p,q <= 40` and `1 <= c <= 4`, and 1,600 witnesses using
`1/z` and `1/(1+z)`.
The continued-fraction digit-sum bound is checked for all 38,178 proper
fractions in `U6`, using their exact first generations.

## Mathematical coverage

The pinned Lean declaration `D5.S3.Arith.CounterSequences.KimberlingA371279.result`
states ordered first-occurrence updating, unique rational occurrence, stable
flattening, injectivity, and reduced-coordinate identities:

https://github.com/the-omega-institute/trureturing/blob/f3466406d8191001830cf15e84db4578d4891435/D5/S3/Arith/CounterSequences/KimberlingA371279.lean

Its cumulative index is zero-based (`cumulative n = U(n+1)`), and its fraction
index is zero-based. The stronger bound `p/q in Uq`, exact minimum and dyadic
first-generation formulas, A371353 multiplicity formula, and unary-closure
corollary are written proofs in this note. The linked private `coverage_q`
declaration has the weaker bound `p/q in U(q+1)`; `Occurs` uses one-based
generation and within-generation coordinates.
The A226080 Fibonacci/Wythoff position formulas concern another enumeration
and are outside its scope.

## Creators and license

1. Haobo Ma — ChronoAI Pte Ltd, Singapore.
2. Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore.

Copyright 2026 Haobo Ma and Wenlin Zhang. Licensed under Creative Commons
Attribution 4.0 International (CC BY 4.0), `cc-by-4.0`.
