# Response to r29 and continuation of the readable v46 manuscript

**General Theta Foundations I — Revision 47**  
**Robust Compatibility of Numerical Word Realizations**  
27 September 2026

The latest review found in the remote inventory is r29, commit `6e8a9504a1a0820e6195317df885d99aed06c878`, reviewing v43 publication `153830f5dc8d13358f9103c307c619076c5ec80c`. It is not a review of v44, v45 or v46. This revision starts from the readable v46 source-review head `d7914880e7df679756c3b6ae86311485ac922f8a`. The previously published v44 article and the complete v46 mathematical sources were inspected. The separate v45 and other work branches are not altered or represented as independently reviewed.

## What is new in this revision

The current response does not count the v44 Hankel normal form or the v46 Gram identity as new again. The new section `two-state-compatibility.tex` proves an exact two-label reduction, a finite sign certificate, an arbitrary-horizon bottleneck obstruction, and complete error frontiers in explicitly specified classes. These are actual optimized worst-word errors, not numerical local minima or sums of local deficiencies. The elementary algebra used in the proofs is identified as such; no claim of first invention of scalar stochastic updates, tensor products or binary elimination is made.

### Exact normal form (`thm:scalar47`)

For every antisymmetric finite binary experiment with paired seeds, two labels at every command cut suffice to optimize over bounded decomposable tensors: one factor per positive seed, command epoch/letter, and query. Every two-state stochastic update is affine in the signed state probability. Taking the odd part in the seed cancels all accumulated offsets. Crucially, this is realizable by deleting the offsets and retaining the slopes; it does not require a free symmetrization coin or a mixture of whole machines. The converse writes the actual normalized stochastic rows. This gives equality of the optimization problems, not just a lower bound from signed rank.

### Balanced certificates (`thm:sign47`)

A set of nonzero target entries in which each factor occurs an even number of times must have nonnegative product for a decomposable real tensor. A negative target product therefore gives an explicit uniform-error lower bound. If all target means belong to `{0,+rho,-rho}`, inconsistent support signs force the exact optimal error `rho/2`; consistent signs give a constructive error at most `rho/4`. Thus strict improvement over the fair-coin error is completely decided by a linear system over F2. Elimination returns a negative balanced certificate of at most `n+N|A|+d+1` entries when inconsistent.

The consistent case is not asserted to have optimum exactly `rho/4`; some such targets are exact. The complexity bound is polynomial in the fully displayed response table, which may be exponential in N. This is not a general efficient optimizer for succinct stochastic automata.

### Two separated bottlenecks (`thm:bottleneck47`)

For four axis seeds and the fixed alphabet consisting of identity and a quarter-turn, any two distinct command cuts with at most two labels force error `rho/2`, even if every intermediate register is arbitrarily large. Fix identity words before and after the interval. Identity versus one quarter-turn inside it gives four nonzero entries with negative product, although every seed, word and query factor occurs twice. Collapsing the intervening computation into an endpoint stochastic kernel is a converse only; no free macro-input or internal reset is introduced. The target has full support at the signal used in the finite frontier.

### Complete actual-error frontiers (`thm:frontier47`, `thm:sparsefront47`)

For one command and `0<rho<=1/6`, the two-cut table is

| Initial / final command width | 1 | 2 | at least 3 |
|---|---:|---:|---:|
| 1 | rho/2 | rho/2 | rho/2 |
| 2 | rho/2 | rho/2 | rho/4 |
| at least 3 | rho/2 | rho/4 | 0 |

All upper witnesses are explicit and rational when rho is rational. At tolerances from `rho/4` to below `rho/2`, the exact feasible region is the upward closure of `(2,3)` and `(3,2)`. Hence separately minimal approximate factorizations cannot simply be combined.

At arbitrary horizon, if each command width is one, two, or at least four, the entire profile optimum is also determined: `rho/2` if a one-label cut occurs or at least two two-label cuts occur; `rho/4` if exactly one two-label cut occurs; zero if all widths are at least four. This theorem is valid for `0<rho<=1`. Its construction tracks four axis states, projects to two diagonal states at the unique bottleneck, then tracks four diagonal states. The excluded width-three profiles are not filled in by inference. The held answer always costs two labels.

A 1-Lipschitz perturbation argument gives the robust separation `rho/2-eta` versus `rho/4+eta`, positive for `eta<rho/8`. Perturbed targets need not remain antisymmetric. Thus this is not a support-zero artifact or an exact-only factorization example.

## r29 §11.1 — the finite-type minimum

The sharper minimum and the restriction to sufficiently small auxiliary h are retained verbatim from v44 in `metric-width.tex`. There is an important logical qualification to the report: `L<=min(a,b)` always implies the weaker `L<=b`; an example with `b>1/2` does not refute that weaker inequality. Displaying the minimum is nevertheless clearer and preserves all the information needed in the limit. No false theorem is defended, and no mathematically false admission is used as an author response.

## r29 §11.2 and §§5–6 — realization theory and structural compatibility

The full normalized Hankel characterization and rowwise dual remain in `hankel-compatibility.tex`. The distinction between ordinary signed rank, nonnegative rank, normalized stochastic factors and a common stochastic update is explicit. The v44 universal distortion-rate/enclosure inequality remains in `distortion-rate.tex`; it is one-sided and does not assert duality at the unrestricted hidden optimum.

The new low-width normal form is a genuine equality for its entire stated antisymmetric class. Its robust frontiers exhibit the compatibility information missed by separate cut minima. It does not identify all higher-width positive realizations with rank-one tensors or vector-state polytopes. The complete inherited v46 Gram, moment and rational-grid proofs are retained. Their global optimization clauses are mathematical finite-effectiveness statements, not claimed executions of quantifier elimination.

The literature comparison was revisited in primary material. Benvenuti–Farina's invariant-cone Theorems 2–3 concern positive realization; Balle–Panangaden–Precup's Theorems 2 and 11 separate weighted Hankel rank from their norm-specific approximation; Ohta's finite tensor reductions concern stationary HMM observation laws; Tzeng's polynomial equivalence algorithm concerns a supplied automaton rather than minimum stochastic order. The present finite selected-query, bounded-decoder and worst-word objective is specified explicitly. These distinctions delimit the claim; they are not exhaustive priority clearance.

## r29 §§11.3–11.6 — resources, arithmetic and novelty

The main resource remains nonuniform clocked atomic-row label width. Horizon-specific redesign, row tables and arithmetic are free in that model. The separately charged finite-bit theorem and its original integer-interval compiler are retained, not used to identify clean labels with all machine configurations. Exact rational witnesses in the new finite example do not imply rational exact realizations for every target or a succinct general row table.

The DGLPS and Bugeaud–Laurent comparisons, ordinary/dual exponent conventions, correlated packet words, deterministic remainders, finite rational phase costs and natural logarithms remain in the inherited article. No new Diophantine exponent, Liouville upper limit or broad nongapped noncommutative classification is claimed. The new results are in the low-width structural problem, not a new arithmetic asymptotic theorem. All inherited arithmetic proofs are included rather than removed to make space.

## r29 §11.7 — historical pipeline

The frozen `ROUND17_PROOF_DEPENDENCY_LEDGER.md` was read at the current base. Its independent Fourier/local-limit, stopped-LDP, global-kernel, nonlinear-semigroup, graph-core, filtering and optional-projection gates are not proved by the finite parity or Gram identities. No unrelated A/B/C/D closure is added to the status ledger. The focused article does not use archive length or internal revision count as evidence of significance.

## Delivery and execution scope

The previous v46 workflow `36260243370` is now observed as failed, not queued: its source push was rejected because the remote work branch had advanced. No mathematical build step ran. This revision does not relabel that failure as success or modify that branch. It publishes readable native sources directly on a new v47 branch before building them, and never force-pushes a concurrently changed ref.

`check_compatibility.py` is a new rational verifier for the present proofs. It enumerates 6,561 ternary sign tables, validates constructive parity outputs or negative balanced witnesses, checks the three rational two-cut constructions, checks odd-part identities, and enumerates small instances of the arbitrary-horizon profile construction. It does not compute generic global optima. The original published v44 regression and finite-bit compiler are included separately and retain their provenance. Actual executed counts and results belong to the source-bound build receipt.

Every inherited v46 mathematical module except the title/abstract and introduction is retained byte-for-byte. The predecessor intro is also retained separately. The complete published v44 PDF and its cumulative volumes are preserved as optional archives. All original paths and branches remain unchanged. The compact review package contains the current article, response, audit and standalone source package, not the large archives.

The series title is retained with a precise subject subtitle. A successful build establishes reproducible delivery, not independent proof verification, originality or an editorial outcome. The next referee can focus on `thm:scalar47`, `thm:sign47`, `thm:bottleneck47`, `thm:frontier47` and `thm:sparsefront47` while every older proof remains available.
