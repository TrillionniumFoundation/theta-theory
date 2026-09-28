# A2 v83 proof and preservation ledger

Base: `b7075ecdeacb42befd55d4c732cbff4706fb4aca`, the latest v82 review head. The previous mathematical manuscript head is `0ae206f918edd06f233e1c6493fb20a598cdda89`. The revision is additive: no historical manuscript or review is edited or removed.

## Principal dependency graph

```text
Projective matrix records
  -> visible rank + joint spectral components (classical mechanism, explicit normalization)
  -> scalar component log ratios
  -> nuisance annihilator contrasts
  -> two known-density interval moments
  -> sharp global q+3 action inverse + q+2 ambiguity
  -> relative coefficients and centered gauge
  -> intrinsic component covering
  -> quantitative overlap matching and exact permutation cocycle
  -> globally glued off-model C^m quotient inverse
  -> canonical graphs and absolute primitives
  -> covered coprime return word
```

## Statements and dependencies

| Label | New contribution or retained ingredient | Essential limits |
|---|---|---|
| `lem:v83-interval` | Global interval-endpoint inverse; necessity of strict monotonicity | Known positive density; intervals, not arbitrary measures |
| `thm:v83-classification` | Invariant iff criterion for codimension-two sampled nuisance spaces | An annihilator kernel is positive on the action interval |
| `thm:v83-scalar` | Sharp q+3 clocks, smooth inverse, q+2 action-changing level set | Distinct deadlines and unequal anchor actions below the first deadline |
| `prop:v83-exponential` | Nonpolynomial application with sharp four clocks and its own spectral proof | Known positive lambda, equally spaced clocks, unknown branch coefficients |
| `lem:v83-components` | Explicit classical spectral recovery in this normalization | Full column rank, independent invariant readouts, distinct joint signatures |
| `thm:v83-main` | Sharp absolute-action observation theorem, full gauge and covering identification | Fixed finite degree, visible rank, unequal anchor; not open-world hidden causes |
| `lem:v83-local` | Quantitative finite charts, anchor threshold, off-model smooth maps | Fixed margins and finite atlas; no additional spatial derivative |
| `lem:v83-match` | Unique noisy overlap matching gives an exact cocycle | Original-space channel gap, errors below one quarter of that gap |
| `thm:v83-global` | Global quotient inverse and pairwise C^m error bound | Fixed visible-rank and covering stratum; arbitrary nearby real data allowed |
| `prop:v83-monodromy` | Positive three-cycle example proving topological distinction | Exact smooth circle example, not a trivialized global labelling |
| `thm:v83-return` | Selective records feed exact covered return-lift reconstruction | Canonical coordinates, deterministic realizability, finite phase cover and collars |
| `thm:v83-unobserved` | Exact localized Hamiltonian ambiguity beyond sampled orbit tubes | Smooth exact lifts and the explicitly unsampled open set; not every billiard class |
| `prop:v83-shear` | Actual three-sheet crossing plus persistence on a neighborhood | Regular compact patches, no fold crossing |
| `prop:v83-one-view` | Exact positive full-rank one-view ambiguity for every deadline | Unknown single channel; extra calibration changes the problem |

The interval criterion is formulated in classical two-function Chebyshev language. Divided differences, latent joint diagonalization, generating-function calculus, contact suspension and Bezout's identity are not claimed as new general theories. Novelty is not certified by the regression script.

## Historical derivations consulted

The controlling v82 report was read in full. The v82 exact selective-detector, local stability, polynomial extension, return reconstruction and physical example were read against it. The v81 blind matrix pencils, component formulas, projective scale recovery and return/experiment hypotheses were consulted. The v80 calibrated action framework and physical retention compensation were inspected. The v79 ambient quotient, nuisance split, conditional minimax action proof, raw-budget geometry and root-free prefix arguments were consulted, together with the v77 finite identifying-atlas/coverage and distance machinery. The v78 native source archive was also obtained from successful run 35222041974, artifact 10504561295, to examine historical source and build provenance. This is not a fresh independent line-by-line certification of every historical appendix.

## Preservation

`rigidity_v83_full.tex` retains `article/v82/principal` and all mathematical inputs in `rigidity_v82.tex`. It adds the new principal article and a note identifying the stronger clock count and the corrected global noisy construction. The old bibliography entries are preserved by the existing wrapper; new entries use distinct V83 keys. Old sufficient clock counts remain valid but are not described as optimal.

The principal entry is a self-contained mathematical article. The expanded entry is the complete retained companion reading edition, not a substitute for the principal entry. Neither root README nor a historical file is rewritten. The build script verifies direct-input preservation when the expanded target is selected and records recursive source hashes for each target actually built.
