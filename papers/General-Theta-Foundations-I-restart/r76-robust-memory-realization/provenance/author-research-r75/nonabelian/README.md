# R75 nonabelian mathematics — integration packet

The authoritative proposed native section is `42-nonabelian-memory.tex`. It contains the arbitrary-group Fourier/multiplicity synthesis, exact normality/convexity boundary with a quantitative margin, full-contrast rigidity, and the all-`n` exact two-level symmetric-group law. Its transition is now proved to be `tau_n=(sqrt(n)-1)/(sqrt(n)+1)`. A sharp singular-coefficient lemma gives the entire equality class, and the main theorem classifies minimum permutation-core factorizations at that threshold, including nonuniform weights.

`42-orbit-multiplicity.tex` and `43-symmetric-return-law.tex` are earlier split development drafts retained only as research history; they should not both be included with the combined section. `development/42-nonabelian-memory-before-closed-threshold.tex` preserves the immediately preceding two-level proof before the threshold was closed. The active section retains its rational subinterval decoder and full-contrast return-law proof.

`bibliography-r75-nonabelian.tex` adds the classical Serre reference. All other external background authorities already occur in the inherited bibliography. `LITERATURE_AND_PRIORITY_R75_NONABELIAN.md` records what was actually consulted and the scope of the proposed increment.

Run the canonical finite diagnostic with:

```sh
python diagnostics_r75_nonabelian.py --output diagnostics_r75_nonabelian.json
python -O diagnostics_r75_nonabelian.py --output diagnostics_r75_nonabelian_optimized.json
```

These commands require SymPy 1.14.0. In the shared revision workspace the pinned interpreter is `/workspace/scratch/f856e3d63ac5/r75-venv/bin/python`. The ordinary and optimized executions completed with 95,999 exact checks and zero floating checks; `DIAGNOSTIC_VALIDATION.json` pins the corresponding source, script and report hashes.

If the script is moved into the manuscript root it automatically finds `sections/42-nonabelian-memory.tex`; `--source PATH` selects another location. Both executions must produce byte-identical reports. The report pins the exact source and script SHA-256 values. It has no runtime timestamp or optimization-dependent checks. Every check is an ordinary conditional that raises on failure, so Python optimization cannot remove any checks.

The earlier `nonabelian_exact_diagnostics.py` and `nonabelian_exact_results.json` are superseded development artifacts; the canonical script/report above control current validation.

## Scope of the numerical work

The canonical report checks rational/integer identities on all elements of `S3`, `S4`, `S5`, `S6`; full residual ranks and counts through `S5`; every subgroup of `S3`; explicit controllers and a finite margin grid; nonconstant extra sign-orbit contributions that cancel to a constant and are absorbed; a three-output example in which each individual Fourier block has rank one but the correct vertical stack has rank two; and all natural-orbit partitions for `5 <= n <= 30`.

The threshold closure adds 111 exact algebraic and symbolic checks: the lower-bound algebra, radical coefficient/equality matrices for `n=5,6,9,16`, the full `S5` and `S6` response tables and four specified elements for `S9` and `S16`, uniform and nonuniform legal weights, a decoder-violation negative control, and nonsymmetric singular matrices covered by the relaxed lemma. Matrix identities and full response tables are each counted as one check. The diagnostic does not enumerate all subgroups of the larger symmetric groups or all stochastic realizations. Its symbolic simplification is not proof-assistant verification; the universal assertions rely on the written mathematical proofs.

The common-action factorization uses row transition matrices `P_g P_h = P_gh`; the prepared quantum realization uses `U_g = P_g^T tensor I`. The pure-start formula is inherited and is applied only with the computed observable group and residual cardinality.

Only this research directory was edited by the nonabelian subtask. Source integration, the full manuscript/supplement build, controlling referee response, branch commit and GitHub push remain with the root revision task.
