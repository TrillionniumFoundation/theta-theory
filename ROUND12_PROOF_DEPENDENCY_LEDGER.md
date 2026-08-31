# Round-Twelve proof dependency ledger

## Independent benchmark

`A1` is independent.

## Sinai chain

`A2 parent-fold spectral/LLT -> A3 deterministic-clock renewal LDP -> A4 Harris/rough/memory -> C2 -> D1`.

## Hard-sphere chain

`B2-GC trace/Jacobi pressure -> B1 exact shell transfer -> B2-MC joint LDP -> B3 covariance/process -> B4 action semigroup -> C1/C2 -> D1`.

B1 uses only the grand-canonical part of B2.  B2's microcanonical theorem is formed only after B1.  B3 constructs covariance before action inversion.  B4 never proves an upstream LDP.  D1 contracts already-proved component laws and cannot substitute for them.

## Merge gates

1. Every `main.tex` loads exactly one `ROUND12_POSITIVE_CLOSURE.tex`.
2. Registered source and active module are byte-identical for all eleven papers.
3. Every theorem-like environment has a proof and every local reference resolves.
4. The round-eleven direct counterexamples are replayed by the hostile verifier.
5. All eleven papers clean-build with no undefined references/citations.
6. The exact verified mathematical tree is published atomically after preserving the previous main.
