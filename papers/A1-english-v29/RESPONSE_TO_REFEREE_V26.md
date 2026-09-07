# Response to the referee on A1 English v25

**Revised manuscript:** *Attainable information, exponent collisions, and adaptive order*, Qian Qi, A1 English v26, 7 September 2026.

**Controlling report:** `review/a1-english-v25-harsh-independent-2026-09-07`, commit `ab0ebddd80f1e46712650eb6730e113e5c66562f`, report blob `ef18197ba6213d92d41ac197bd23aa5f7e5194a9`.

**Reviewed submission:** `8a84075ee518035069d38fd9262bd455aff4ac86`, `papers/A1-english-v25/`.

**Revision:** `revision/a1-english-v26-separator-capacity-2026-09-07`, `papers/A1-english-v26/`. Paths below are relative to this new directory. The complete controlling report and its original diagnostics are retained in `review-basis-v25/`; those prior diagnostics are not represented as newly executed tests.

## 1. Disposition and preservation

We thank the referee for separating correctness, attribution, scope and mathematical significance. The report finds no fatal counterexample or unresolved central gap in the inspected principal route. Its negative venue recommendation is a significance judgment. We do not recast that judgment as a missing-proof checklist, a mathematical impossibility, or an acceptance prediction after corrections.

The revision preserves the scalar collision classification, all integer budgets, both risk criteria, the single causal filter, the qualitative adaptive theorem with its stronger finite-prefix oracle, the original graph-width consequences, and the original star. Their hypotheses and conclusions are not weakened. The direct scalar route and early intersecting-collision example remain in the principal article. The complete companion remains a separately compiled, active volume. No old manuscript or report is deleted or overwritten.

This revision also makes a mathematical addition rather than relying on citation repairs or test counts to answer the significance assessment. It distinguishes the number of complete observation orders from the number of information states visible to a decoder, supplies a quantitative separating-set bound with local constants, and classifies the entire leading memory phase diagram along analytic collision paths. The existing three-edge experiment then exhibits nonconvex optimal memory and an interval-of-resolutions obstruction that endpoint comparison misses.

## 2. E25.1: bibliography correction

The entry keyed `AmarilliGroz2025` in `v25/references.tex` now reads: A. Amarilli and B. Groz, *Cutwidth bounds via vertex partitions*, arXiv:2504.01574v2, 2025. The primary HTML article identifies Antoine Amarilli and Benoît Groz. The incorrect title, incorrect initial, and third author are removed from the revised active bibliography; the historical v25 submission remains unchanged as an archival source.

The reference continues to support only the definition and attribution of cutwidth. It is not presented as a source for our statistical adaptive theorem, and no new priority claim is made. The separate flow certificate explicitly credits L. R. Ford Jr. and D. R. Fulkerson, *Maximal Flow Through a Network*, Canadian Journal of Mathematics 8 (1956), 399–404. The classical flow–cut argument is proved in the text for completeness, not represented as a new graph theorem.

Primary records checked: https://arxiv.org/html/2504.01574v2 and https://doi.org/10.4153/CJM-1956-045-5. These targeted checks do not constitute an exhaustive literature-priority search.

## 3. E25.2: the missing proof ledger

The intended ledger is now actually supplied at **`papers/A1-english-v26/PROOF_LEDGER.md`**. It gives the exact active source and theorem/equation labels for each inherited prerequisite and each new result. It separately records the decoder models, the order of risk quantifiers, the positive-allocation convention and the role of independent seeds. The mathematical proofs themselves remain in TeX; the ledger does not stand in for them.

## 4. E25.3: actual negative controls

`diagnostics.py` evaluates the equally likely loss vectors `(1,0)` and `(0,1)`. It computes the expectation of the maximum and the maximum of the expectations as 1 and 1/2. Reading the same array as controllers versus checkpoints computes `inf max = 1` and `max inf = 0`. Thus the witness constructs both operations rather than merely comparing two constants.

For individual caps, both compared coefficient arrays have total cap three and length four. The valid caps `(1,2)` give the common-index coefficient `A_3=1/4`; moving the extra direction to the wrong component, with caps `(2,1)`, gives `A_3=1/16`. Array-length differences cannot make this control pass.

The new suite additionally compares capped max-product factorization, subset dynamic programming with exhaustive orders on all 74 labelled simple graphs with two to four vertices, exact split-network flow with exhaustive separating sets, a discrete arbitrarily selected-path subprobability, actual completion-report marginalization, all determinant contact orders of the star, and its full phase and regret calculations. It uses exact rational arithmetic and explicit exceptions rather than Python `assert`. Normal Python and `python -O` were executed locally and produced identical JSON: **843 checks passed**. `DIAGNOSTICS.json` records the script hash, category counts and concrete witnesses. These finite tests do not certify the continuum chart, the causal minimax theorem or any journal decision.

## 5. Finite selection: an explicit lemma

`lem:v26-finite-selection` in `v26/selection.tex` isolates the suggested reduction. For a common event of mass beta and small-loss mass bounds `a_i t^(k_i/2)`, it proves

`max_j E L_j >= (1/q) integral [beta - sum_i a_i t^(k_i/2)]_+ dt`.

When all dimensions equal k, this is

`k beta^(1+2/k) (sum_i a_i)^(-2/k) / (q(k+2))`.

The proof explicitly passes from the expectation of a maximum through the sum of losses to the maximum of expectations. This lemma clarifies the original finite-selection contribution; we do not count the clarification alone as a new structural theorem.

## 6. Beyond complete traces: the separator-capacity converse

The original proof indexes a small-ball union by complete vertex permutations. But in the original operational decoder model, a fixed visited set S and its M-valued label determine at most M query prediction vectors. Different prefixes that reach S do not supply an additional uncharged decoder input. This permits the selection argument to run on the subset lattice, where every possible observation order is a path.

`thm:v26-network-selection` proves an abstract separating-set bound. Every chosen path meets every separating set, so the probability that all losses are small is at most the sum of node small-ball capacities over any such set. Taking the minimum gives a function H(t); layer-cake integration yields `beta/q integral [1-H(t)]_+ dt`. This argument neither conditions on the chosen path nor assumes regular decision regions. `prop:v26-flow` identifies the finite certificate by vertex splitting and the classical real-capacity flow–cut argument.

`lem:v26-first-block` simultaneously strengthens the common event. Only the first acquired block of each edge is required to lie in its regular command box and have failure reports. Completion reports and commands are unrestricted and integrate to one. The common mass is the product of actual first-block evidences, not the probability of one report word on all raw trials. The lemma tracks upper restricted densities divided by these first-block masses, so the improvement is not obtained by deleting evidence factors.

`thm:v26-separator` then proves the explicit lower bound

`R_av >= beta(a)/(v-1) integral [1-H_G(t;M,a)]_+ dt`.

The node capacities minimize over positive individually capped allocations and retain the acquired determinant product, the local pushforward density and the arbitrary-centre query-recovery norm. The lattice has `2^v-2` internal states; a complete order is not itself a capacity index. `cor:v26-profile-recovery` obtains the original collision profile by using the separating set of all cuts with profile at least Q, with an explicit inequality for a sufficient lower-bound constant.

This quantitative theorem applies to the actual label/visited-set decoder, while allowing the scheduler its full revealed past. It is **not** advertised for the stronger free-order-prefix decoder; the original qualitative theorem for that oracle remains present and unchanged. Local constants and the first-block mass can deteriorate with graph size. Thus no graph-size-uniform gap, polynomial-time layout algorithm, correlated-prior extension or raw-internal-checkpoint theorem is smuggled into the statement.

## 7. Full collision-path phases and a new resolution obstruction

`prop:v26-dynamic` gives an exact subset recursion for the comparison profiles once the real cut costs are supplied. Its `O(v 2^v)` comparison count is separated from the problem of computing arbitrary prior moments or exact minimax constants.

`thm:v26-phases` treats any analytic calibration path in an admitted compact chamber. Pairwise contact orders determine the vanishing order eta_(e,l) of each maximal Vandermonde product. At accuracy `epsilon=theta^(2s)`, the leading edge cost is `w_e(s)=max_l(l s-eta_(e,l))`. The leading optimal memory is the minimum over orders of the maximum cut sum. It is a finite, continuous, nondecreasing piecewise affine function with integral slopes and rational breakpoints. The proof also gives a uniform expansion for the best single-order penalty over a whole interval of s, including orders that may depend on theta.

Minimization over orders can destroy the convexity shared by the scalar costs. For the **same** positive 24-trial experiment already in v25, `cor:v26-starphase` proves the full law

`W(s)=7s` for `0<s<=1`,
`W(s)=10s-3` for `1<=s<=3/2`,
`W(s)=8s` for `3/2<=s<=3`,
`W(s)=9s-3` for `s>=3`.

The slope drops from 10 to 8. On the full interval `1/2<=s<=2`, the best fixed-order regret is `log_2(1/theta)+O(1)`. At just the two endpoints, it is `(1/2)log_2(1/theta)+O(1)`. The intermediate resolution is therefore essential. This is not an alternative proof of the old endpoint calculation; it identifies a different optimization problem and its sharper obstruction, without introducing a formal scale list unconnected to an actual detector.

## 8. Historical comparison and assessment requested

The targeted historical reading used the actual shared-memory v10 commit `da5abea9f40244879115d5fbcfbda375bc9a123e`, Sections 8–9. Its product posterior, tensor recovery, individually capped joint quantization, additive bits and serial/overlap scheduling are inherited work. V25 adds the adaptive common-event comparison and the first ordering transition. V26 adds the visited-set separator certificate, first-block-only event with explicit density accounting, general analytic-path phase law and uniform-resolution regret. These distinctions are recorded rather than counting the same deterministic composition theorem again.

We ask that the new quantitative and phase results be assessed against the pinned v25 submission. The venue significance question remains a matter for renewed independent review; neither an additional theorem nor the repaired bibliography implies acceptance. The response is positive in mathematical content: it preserves the full established classification and supplies further statements and proofs for examination.

## 9. Verification and reading limits of this revision session

The v25 controlling report, complete new v25 graph proofs, its principal entry point and build source, the native v24 construction/build source, and the targeted v10 shared-memory/scheduling derivations were read through authenticated GitHub. The native v24 tree and v25 source objects are reused without transcription. The session did not freshly re-audit every proof in the complete companion or the entire eleven-paper program.

The 843-check suite and its optimized repetition were actually executed. `SESSION_VALIDATION.json` distinguishes these executions and the local typesetting check of the new modules from a full native two-volume build. The delivered `build.py` reconstructs only the original redundant historical audit copies, verifies historical manifests and pinned source blobs, checks complete inherited formal-block preservation and multiplicities, and runs both volumes with the inherited cross-reference-aware builder. A successful full-build receipt is produced only when that command actually completes. No prior build receipt, prior referee test count, or unobserved GitHub Actions run is relabelled as a new success.
