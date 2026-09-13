# Independent formula certification for contact class 4

The contact tetrahedron is
`conv((0,0,0), (5,1,1), (0,1,0), (0,0,1))`.
Only class 4 is covered by this certificate campaign. In particular, none of
these refutations certifies the other determinant-five class, class 5.

The five representative ordered height extrema are `(0,1)`, `(0,2)`, `(0,3)`,
`(1,0)`, and `(1,3)`. Each query covers the entire closed square `[0,1]^2`
of the two remaining normalized heights. No subdivision is used.

The independent encoder in
[replay_height_cover_cvc5.py](../tests/replay_height_cover_cvc5.py) reconstructs
barycentric coordinates by Fraction Gaussian elimination. It uses twelve
off-diagonal entries of the stochastic matrix, two free heights, an offset,
a positive gap less than `5/17`, and six McCormick product variables: 22 Real
variables in total. It imposes the 40 guard exclusions and seven integer
gauge inequalities obtained from the six primitive contact edges and the
short vector `(1,0,0)`. It imports no discovery experiment or Z3 encoder.

The dedicated runner
[replay_det5_class4_cvc5.py](../tests/replay_det5_class4_cvc5.py) checks that
the archived five roots cover complete unit squares, constructs the five
formulas afresh, and requests complete internally checked cvc5 proofs.
The exported SMT statements and compressed CPC proofs are in
`certificates/det5_class4_cvc5/`. Their hashes are bound in
[the cvc5 receipt](../results/det5_class4_cvc5_validation.json).

The external checker
[check_det5_class4_ethos.py](../tests/check_det5_class4_ethos.py) uses the
validated adapter from
[check_height_ethos.py](../tests/check_height_ethos.py).
It checks official pinned source revisions, all input/proof hashes,
declarations, scope balance and final top-level `false`. The reference
adapter converts only assertion numeral tokens into Real literals and
preserves all assertions and operators. Duplicate proof declarations are
validated and removed. Crucially, the proof is streamed on stdin *after*
the `--reference` input has been supplied, retaining assumption binding.
No trusted or sorry steps are accepted.

Four negative controls test an unrelated global assumption, a mutated final
conclusion, a missing final refutation, and a non-Real declaration. The first
two reach Ethos; the last two exercise local framing/reference guards.
Results and the checker/signature hashes are recorded in
[the Ethos receipt](../results/det5_class4_ethos_validation.json).

Reproduce the new campaign with:

```sh
.venv/bin/python tests/replay_det5_class4_cvc5.py
python3 tests/check_det5_class4_ethos.py \
  --ethos /tmp/flatness-ethos/build/src/ethos \
  --ethos-source /tmp/flatness-ethos \
  --cvc5-source /tmp/flatness-cvc5-signatures
```

Upstream build instructions and the trusted computing boundary are described
in [HEIGHT_ETHOS_REPRODUCTION.md](HEIGHT_ETHOS_REPRODUCTION.md).
These checks establish the five encoded linear formulas' inconsistency.
The geometric implication from hollow tetrahedra, the gauge threshold,
the guard construction, and the height-orbit reduction need their separate
mathematical audit. Neither a general containing-polytope bound nor the
global flatness conjecture follows from the formula checks alone.
