# Author-side reconstruction of the written native 323

Inspected source: `papers/A2-DYN-physical-roof-variation-author-revision/core/323_complete_physical_roof_variation.tex`.

Final source SHA-256 inspected and used by both recorded diagnostic commands:

`36eae03703168ed37d571a94bd8faf35398415163eaeb49d3b2d73c5b44bbdd8`.

The complete written proof agrees with `UNIFORM_ROOF_BV_RECONSTRUCTION.md`. Its unweighted derivative constant is derived before the guard derivative; the conditional normalization occurs exactly once. Its four cap integrals are each exactly pi/2. The critical fan coefficient has the correct normalized angular change of variables and is not counted twice. Its finite-count analytic slicing, maximal physical interval completion and zero visited-grazing traces give the stated complete directional variation budget. The Fourier and translation corollary is restricted to the proved BV majorants; arbitrary exact-event/Borel restrictions receive density domination only. No weighted-insertion L-infinity conclusion or normalized raw local limit is inferred.

Two requested proof refinements are present in this exact source:

1. The charge assignment treats visited-grazing limits first, then critical limits, then active unvisited constraints before cap constraints. Thus residual cap arcs are actual regular roots to which native 284 applies.
2. Before invoking native 285, the source states that the cap and visited-incidence tests are strict at a positive-visited critical germ; every active boundary is an unvisited clearance with its already proved nonzero differential. This meets that theorem's actual stated hypothesis, beyond merely asserting an analytic angular limit.

The uniqueness paragraph for a fixed-word limiting critical configuration is valid. Apply the two support inequalities to two candidates by continuity. Their normal endpoints and equal zero gradients force their respective endpoint contacts to coincide. The common initial normal ray then fixes the designated next entry/tangent root uniquely; induction fixes all designated contacts. Equivalently, compactness and local positive-Hessian gradient inverses would suffice for the finite-count argument.

No missing positive boundary contribution or contrary example was found for the theorem with its written scope. This is a coauthor proof reconstruction, not a journal review or an independent human-expert certification. It uses the inherited native physical curve-growth and momentum-kernel theorems with their stated hypotheses; their full earlier proofs were not all reconstructed again in this assignment.

## Actual auxiliary diagnostic

Program: `check_complete_roof_variation.py`.

Program SHA-256:

`070c3d8d03a3933d3050659f32547b358519a3b4dcb6ce7b87df814a151a5668`.

The CLI is `python check_complete_roof_variation.py --source SOURCE323 --details OUTPUT`. When installed under the article's `tools/`, the default source resolves to `../core/323_complete_physical_roof_variation.tex`. It raises explicit exceptions on failures and does not rely on Python assertion statements.

Both normal and `-O` runs completed with exit code zero. Each completed **10,148** exact checks: 13 symbolic optical/coarea identities; 5,904 checks on 972 rational positive-Hessian/radius/direction cases; 14 cap and normalization checks; 258 full marked-boundary geometric checks; 2,547 exact quadratic-profile checks; and 1,412 scope-counterexample checks. The mathematical JSON and details are byte-identical in the two modes. Their SHA-256 is `78ebbc24c4fb8ae3467bfd21c05a223bb6a6d410668b6c03ab5dfd79de244612`.

The quadratic examples are explicitly defined analytic roofs on closed elliptic sectors/annuli with constant or smooth polynomial radial weights. They verify actual analytic pushforward and boundary identities for those functions; they are not claimed to be billiard-orbit realizations or a replacement physical model. Cases include a critical disk, a shifted critical ellipse, a noncritical annulus, smooth linear and quadratic radial weights, disconnected domains, an artificial radial split whose signed seam contributions cancel, and two sources meeting at a common roof value.

The exact counterexamples retained in the output are:

- `f_m=1_[0,m^{-4}]`: mass `m^{-4}`, height one and total variation two. Its normalized mass tends to zero while `m^2` times its height diverges. Uniform height and even uniform BV do not pay the required normalized selected-source height.
- `H=1_union_{n>=1}(4^{-n},2*4^{-n})` restricted from `p=1_[0,1]`: selected mass `1/3`, height one, and variation at least `2N` for every `N`, hence infinite. A Borel restriction does not inherit BV.
- The constant quadratic critical disk has zero interior variation, one outgoing boundary unit and one incoming critical unit. Omitting the critical unit produces the false half-variation height bound `1<=1/2`.

`execution/EXECUTION_SUMMARY.json` records exact commands, generated command IDs, timestamps, exit codes, output byte counts and hashes, interpreter path, and source/program immutability during the run. `execution/TOOL_EXECUTION_RECEIPT.json` records the corresponding executor chunk/session IDs. `development-normal.*` preserves the preceding successful development run separately. Runtime metadata is kept outside the deterministic mathematical output.

The script is finite auxiliary evidence. It does not prove analytic physical-chart completeness, the inherited curve-growth chain, continuous singular-stratum exhaustion, or the full raw pointwise local limit theorem.
