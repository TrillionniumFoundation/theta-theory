# Validation, A2 revision 66

## Scope

Validation separates exact source retention, finite mathematical controls, native compilation and visual inspection. None is a formal proof certificate or a journal-placement assessment. The proofs are in the active TeX manuscript; no theorem is supplied only by a checker or response file.

## Source retention and finite controls

Commands, from the repository root:

```sh
python3 -B papers/A2-v17-boundary-information-coarsening/tools/check_revision_v66.py > normal.json
python3 -O -B papers/A2-v17-boundary-information-coarsening/tools/check_revision_v66.py > optimized.json
cmp normal.json optimized.json
```

Local normal and optimized executions emitted identical JSON. All 818 inherited file identities and modes are accounted for: 811 unchanged in place and seven with byte-exact archived originals. All 131 inherited active inputs remain; three new shared inputs give 134 (123 full, 55 principal, one companion). The new proof section contains four statements with four complete proofs; the introductory theorem summarizes them and retained results.

The program checked 220 exact rational Schur identities, 42 exact signed cyclic blocks, 40 exact two-point Lipschitz comparisons, 960 contraction iterates, 40 finite Dirichlet models of length 240, six finite-difference curvature Jacobians, six exact two-contact specializations and a positive-data nonimage control. The largest local floating-point discrepancies were approximately `4.45e-16` for the final curvature iterate, `8.89e-16` for the finite Schur value, and `9.24e-11` for the directional curvature Jacobian. These are finite floating-point controls, not rigorous infinite-chain error bounds. The rational examples test the scalar Jacobi identity, not global geometric realization of arbitrary recurrence coefficients.

## Native build

The unchanged `tools/build_revision_v56.py` freezes the committed Git source, builds `two_collision.tex`, `main.tex` and `rigidity.tex` with fresh auxiliaries and shell escape disabled, checks producer/consumer auxiliary provenance and records source, toolchain, recorder inputs and products. Its inherited finite diagnostics are also run normally and with optimization.

A local fresh build at commit `41494931149165c4327058a7fa0ac6bf04ee37f2` passed for all three entries: principal 149 pages, full technical manuscript 324 pages, companion seven pages. That local commit predates this validation note and the repository delivery files; it is not represented as the remote compiled commit. The native workflow independently rebuilds the final committed source and publishes its actual source identity and evidence.

The checked local final logs contain no undefined-reference/citation, missing-character, overfull-box or LaTeX-error pattern. The full manuscript has four inherited-style underfull vertical-box notices; principal and companion have none. The epstopdf package notes that shell escape is disabled, as required by the build command. One initial overfull new display was split into two aligned lines and the complete manuscripts were rebuilt.

## Visual scope

The principal title/abstract page and new curvature proof pages were rendered at 108 dpi and inspected for clipping and legibility. The final delivery verification specifies exactly which final-source pages were visually inspected and distinguishes this from all-page mechanical reproduction. Rendering every page is not claimed to constitute human visual inspection of every page.

## Remote delivery boundary

The workflow activates only source-pinned framing changes and archives their originals. It does not generate a missing proof. Before compiling it checks the staged manuscript tree against the predetermined complete source tree. Source activation is pushed without force; concurrent branch changes therefore fail rather than being overwritten. Native products and fetched-object attestations go to a new version-scoped revision branch. Completed run, product, source and review-ready identities are recorded only after the corresponding operations succeed.
