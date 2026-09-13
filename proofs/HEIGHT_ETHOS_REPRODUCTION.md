# External checking of the height-cover CPC refutations

The checker consumes the 62 existing `.cpc.gz` certificates and their exact
`.smt2` inputs. It does not regenerate proofs or invoke a satisfiability solver.
Its receipt is [height_ethos_validation.json](../results/height_ethos_validation.json).
The separate encoding and dyadic-cover audits establish that these inputs cover
the intended geometric cases; Ethos establishes their refutations relative to
the pinned CPC rule signature.

## Official tools and exact revisions

- [Ethos](https://github.com/cvc5/ethos), version 0.2.3, commit
  `221641668d75eaffd308e0511d63962cea937110`.
- [cvc5](https://github.com/cvc5/cvc5), tag `cvc5-1.3.4`, commit
  `f3b21c4483d3b88dc63cb7cd3e5eb092eee5e341`; use its `proofs/eo` signatures.
  This release's [official installation helper](https://github.com/cvc5/cvc5/blob/cvc5-1.3.4/contrib/get-ethos-checker)
  pins the Ethos revision above.
- Initial build: GNU C++ 13.3.0, CMake 4.4.3, Ubuntu GMP development package
  `2:6.3.0+dfsg-2ubuntu6.1`. All 174 upstream Ethos tests passed.
  No third-party source is vendored into this research repository.

Example setup, with CMake and GMP development files already available:

```sh
git clone https://github.com/cvc5/ethos.git /tmp/flatness-ethos
git -C /tmp/flatness-ethos checkout 221641668d75eaffd308e0511d63962cea937110
git clone --depth 1 --branch cvc5-1.3.4 https://github.com/cvc5/cvc5.git /tmp/flatness-cvc5-signatures
cmake -S /tmp/flatness-ethos -B /tmp/flatness-ethos/build -DCMAKE_BUILD_TYPE=Release
cmake --build /tmp/flatness-ethos/build -j 2
ctest --test-dir /tmp/flatness-ethos/build --output-on-failure -j 2
```

In the original environment GMP headers were absent. The official Ubuntu
`libgmp-dev` and `libgmpxx4ldbl` packages were downloaded with `apt download` and
extracted using `dpkg-deb -x` into `/tmp/flatness-gmp`, without system installation.
The build used these additional CMake options:

```sh
-DGMP_INCLUDE_DIR=/tmp/flatness-gmp/usr/include/x86_64-linux-gnu
-DGMP_LIBRARIES=/tmp/flatness-gmp/usr/lib/x86_64-linux-gnu/libgmp.a
-DCMAKE_CXX_FLAGS=-I/tmp/flatness-gmp/usr/include
```

Run from the research repository:

```sh
python3 tests/check_height_ethos.py \
  --ethos /tmp/flatness-ethos/build/src/ethos \
  --ethos-source /tmp/flatness-ethos \
  --cvc5-source /tmp/flatness-cvc5-signatures
```

The script checks both Git revisions and rejects modified tracked source files.
It records the executable hash, every Eunoia source hash, the cvc5 receipt hash,
and each original input, uncompressed/compressed proof and adapted reference
hash. `--output PATH` selects an alternative receipt. Python's standard library
is sufficient for this stage.

## Proof-input binding and adapter

The [Ethos manual](https://github.com/cvc5/ethos/blob/221641668d75eaffd308e0511d63962cea937110/user_manual.md)
describes reference assertions, the `correct`/`incomplete` distinction, and the
need to check that a desired conclusion was actually proved. The adapter adds
that framing check, because a well-typed unfinished proof can also be reported
as `correct` by Ethos.

The original files declare only nullary Real variables and use QF_LRA. The
reference adapter parses that restricted grammar and replaces each numeral
`n` occurring in an assertion with the exact rational literal `n/1`. Every
operator, variable, assertion and its order is preserved. This resolves the
CPC signature's distinction between Int and Real syntax without algebraic
simplification. Using `--normalize-num` globally is incorrect here: indices in
CPC proof-rule arguments must retain their integer types.

The proof adapter removes its single outer list and the verified duplicate
Real declarations, which must match the reference's 22 variables exactly.
Every remaining proof command is preserved. Removing duplicate declarations
is necessary because a second declaration introduces a fresh symbol in Ethos.
The proof permits only declarations, nullary abbreviations, assumptions and
proof steps; it cannot introduce new rules or signatures. Global assumptions
must be outside local scopes. Push/pop scopes must balance and the last command
must be an explicit top-level proof step concluding `false`.

**For this pinned Ethos revision, stream the adapted proof on standard input.**
The effective invocation is:

```sh
ethos \
  --include=CVC5/proofs/eo/cpc/Cpc.eo \
  --include=CVC5/proofs/eo/cpc/expert/CpcExpert.eo \
  --reference=adapted-reference.smt2 < adapted-proof.cpc
```

Passing a proof filename after `--reference` does not provide the intended
binding: `State::includeFile` in this revision sets `d_hasReference` to the
current file's reference flag, thereby disabling it when opening a proof file.
Streaming avoids that path. No upstream source was patched. A negative control
adds `(assume @fresh_unrelated false)` and requires Ethos to reject it explicitly
as absent from the reference assertions. This detects the misleading filename
invocation even if its proof checking returns `correct`.

Three further controls change the final conclusion from `false` to `true`
(Ethos must reject the rule application), omit the final refutation (the framing
guard must reject it), and change a reference declaration from Real to Int
(the reference adapter must reject it).

## Scope of the certificate

A PASS requires all 62 leaves to return exit status zero and exactly `correct`,
without stderr, as well as all four negative controls. Trust/sorry rules are
rejected locally; Ethos also reports incomplete if a used rule is marked
`:sorry`. The certificate is therefore an external rule check with no such
proof holes, including actual assumption binding and a closed final refutation.

The trusted computing base remains the Ethos C++ kernel, its compiler/runtime
and GMP, the official CPC Eunoia rule definitions, and this small adapter.
The soundness of the entire CPC signature has not been formalized in a separate
proof assistant. This stage does not independently prove the mathematical
soundness of the geometry-to-SMT reduction, the covering argument, or the global
flatness conjecture. Those claims require their corresponding evidence.
