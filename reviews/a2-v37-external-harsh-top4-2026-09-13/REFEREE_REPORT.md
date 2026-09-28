# Independent referee report on A2 revision 37

## Submission and recommendation

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 13, 2026  
**Standard applied:** correctness, significance, and presentation expected of a leading general mathematics journal. This is an author-requested AI-assisted referee-style assessment, not a commissioned report or editorial decision of any journal.

| Object | Immutable identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Reviewed revision branch | `revision/a2-v37-referee-closure-native-submission-2026-09-13` |
| Reviewed submission | `6c311aa389e3af833f06f14ae98de7bfc28c1327` |
| Reviewed tree | `c7285e6882fa0b4c09922ca4f4a9c63b402ac1af` |
| Author's mathematical-source commit | `b0c21cd799bbe4d96bab4a7e1e369d5d7152b294` |
| Preceding v36 report | `01e772030042ffde9df125c0d40401aee2aabd17` |
| Submission examined by that preceding report | `0802bfa20533feff55bf5620d39d6399d5e778f5` |
| Native entry | `papers/A2-v17-boundary-information-coarsening/main.tex` |

The stable directory name is not the revision number. The review is frozen at the displayed submission, not at a subsequently moving branch. Sources, coverage qualifications, and reproducibility instructions are in [AUDIT_AND_REPRODUCTION.md](AUDIT_AND_REPRODUCTION.md). Source keys below refer to that ledger.

**Recommendation: MAJOR REVISION; do not regard the current package as demonstrated submission-ready, and do not recommend acceptance at the stated journal level.**

This recommendation has a precise, limited basis. The v37 mathematical repair of E2 is satisfactory; I1 is also repaired. The previously repaired likelihood-normalization, original-alternative moment, and compact-experiment arguments survive the present source examination. I have not established a new fatal mathematical counterexample in the arguments examined here. However, the complete native main remains unbuilt and uninspected in the supplied execution record, and I independently reproduced a weakness in the inherited build driver's ability to certify which input bytes were used. These are not equivalent to a false mathematical theorem. Conversely, correcting a reference and obtaining successful finite diagnostics are not an acceptance certificate for the full article.

The new finding is **R37-V1**, a verification/provenance defect within the still-open C2 delivery requirement. It must not be advertised as a counterexample to billiard rigidity. The report also expands the independent examination of the charged physical pilot and the count–endpoint product argument, rather than merely copying the v36 verdict.

## 1. What changed, and disposition of the previous report

The comparison from the preceding review commit to the reviewed submission is two commits ahead, with 19 changed paths. Among native mathematical sources, `main.tex` changes its two revision identifiers; `article/23f_single_offset_law_inverse_v26.tex` changes the full-table hypotheses and the associated proof. The remaining changes are navigation, preserved historical copies, a workflow, response documents, diagnostics, and companion evidence. There is no basis for describing this increment as a new proof of all the inherited theorems. [S0–S2]

| Item | Present disposition | Reason |
|---|---|---|
| v36 E2: full-table implication | **Closed in the detailed theorem** | The statement now assumes realizability, the required analytic geometry, a common-frame rank-two anchoring pair, and a rooted signature-rigid spanning tree reaching every obstacle orbit. It cites the full periodic-rigidity theorem. |
| v36 I1: current navigation | **Closed** | Both current README entry points identify v37 and the correct response, report, and verification ledger. Historical README copies are preserved. |
| R1: original-alternative mean and fourth moments | **Repair retained; not reopened** | The native vector chapter contains the one-mark expansion and alternative-centering calculation; the supplement supplies direct normalized likelihood tilting and the risk argument. |
| Finite versus compact Le Cam convergence | **Repair retained; not reopened** | The finite likelihood lemma and the uniform-modulus/finite-net argument are separate and have parameter-independent kernels. |
| C2: complete native delivery | **Open; major** | The author explicitly reports no complete-main build or main-PDF inspection. The inspected hosted run has no executed steps and no artifacts. |
| R37-V1: source-identity certification | **New, reproduced verification gap** | The driver can report an original-source hash rather than the hash of the input in its compilation copy; it also accepts an absent recorder. |

The previous report is evidence of review history, not authority that substitutes for inspecting the current text. Similarly, the author's finite diagnostic runs are not reclassified as runs performed by this referee. [S1, S5, S6, S11]

## 2. Mathematical core: what the present examination supports

### 2.1 The single-offset density inverse is correct at its declared observation level

**Location:** `article/23f_single_offset_law_inverse_v26.tex`, `thm:v26-density-inverse`, `prop:v26-density-stability`, and `cor:v26-finite-flight-inverse`. [S2]

For the interior density

\[
f(u,v)=Z^{-1}B(u)B(v)[d-S(u)-S(v)],
\]

the cancellation is exact:

\[
R_f(u,v)=\frac{d[d-S(u)-S(v)]}{[d-S(u)][d-S(v)]}
       =1-t(u)t(v),\qquad t(u)=\frac{S(u)}{d-S(u)}.
\]

At a fixed nonzero anchor, strict convexity and the anchoring conditions imply \(t(a)>0\). Thus \(\sqrt{1-R_f(a,a)}=t(a)\), the action is \(dT/(1+T)\), and the normalized amplitude follows from the axis ratio. This argument retains the negative and positive transverse coordinates separately. It does not discard odd jets, and it does not require differentiating a pointwise square root at the action minimum.

The stability statement uses an interior \(C^M\) norm, positive density denominators, and a positive lower bound for the fixed anchor. Products, restriction to slices, reciprocals, and the scalar square root are locally Lipschitz under these assumptions. The finite-flight normalization argument also uses an actual positive integral lower bound at fixed offset. The estimate does not claim that total variation controls derivatives, or that the constants are uniform in jet order, in a vanishing anchor, or as the offset tends to zero. Those distinctions are essential and are correctly retained.

The continuous density version is uniquely determined by the law within the specified class. This is not an assumption that a finite statistical sample reveals density point values. The later bounded-test estimator is the appropriate separate statistical implementation. The independent rational checks include 648 signed interior pairs with asymmetric actions and amplitudes; they check the algebra, not realizability of every illustrative functional density. [D1]

### 2.2 The all-order contact inverse is more substantial than the density identity

**Location:** `article/23a_signed_endpoint_rigidity_v27.tex`, from `lem:v22-weighted-inverse` through `prop:v22-tangent-jet-isomorphism`. [S3]

The weighted half-line argument uses a strict margin \(e^{-\gamma_-}<\rho<1\). Its two Green-kernel summations involve respectively \(e^{-\gamma_-}/\rho\) and \(\rho e^{-\gamma_-}\), both below one. The nonlinear Hessian perturbation is small in the same weighted operator norm after reducing a common endpoint interval. Higher fixed-order derivatives use the same inverse, rather than an unexplained new inverse at each order.

The finite-truncation envelope argument cancels all interior orbit variations by stationarity and leaves one right-end term. The stated weighted bounds make that term, including each fixed number of endpoint derivatives, tend to zero geometrically. This is the relevant justification for differentiating the infinite action. Merely writing down an infinite stationary sum would not suffice.

The separate smooth finite-jet factorization lemma matters. Interpolating two anchored graph pairs with matching jets through order \(M\), and using

\[
\partial_t\ell=\frac{h}{\ell}\,[\Delta\psi_r(y)+\Delta\psi_{1-r}(z)],
\]

gives a summable \(O(|u|^{M+1}\rho^{(M+1)i})\) direct variation along the half-line. Integrating the finite identity before taking the truncation limit proves equality of action jets through order \(M\). This addresses smooth remainders and flat perturbations, rather than treating a smooth function as its Taylor series. The functional derivative bounds required for this step are stated; bounded coefficients alone are not used as a substitute.

For the new degree \(n\), the boundary site occurs once and interior sites twice. Consequently the diagonal and off-diagonal coefficients are

\[
1+2\sum_{k\ge1}e^{-2n\gamma k}=\coth(n\gamma),
\qquad
2\mathfrak r_b^n\sum_{k\ge0}e^{-n\gamma(2k+1)}
=\mathfrak r_b^n\operatorname{csch}(n\gamma).
\]

The determinant-one identity is therefore supported by the multiplicities, not just asserted. The quadratic inverse and the block-triangular differential then establish the fixed-order local inverse. The independent checks cover 48 geometry/order pairs and explicit finite-sum tails; they do not certify the nonlinear functional-analytic construction. I found no error in the inspected construction or its finite-jet bookkeeping. This is a positive assessment of these arguments, not an infinite-order conditioning theorem. [D1]

### 2.3 The relative-law normalization is not disposable

**Location:** `article/01c_geometric_setup_v18.tex` and `article/15_operator_comparison.tex`. [S9]

The Dirichlet corner-cofactor identity, the dimension-independent trace-log difference estimate, and the normalized Morse-domain integration argument are coherent in the inspected sources. In particular, an entrywise bound without spatial summability would not produce the needed relative determinant limit. The text recognizes this and identifies the separated nonlinear perturbation blocks as the additional input.

The change of variables in the normalized two-dimensional sublevel integral gives the stated fixed-disk factor of two. Evenness in the square-root offset supplies the smooth extension at zero with a higher but finite derivative budget. Geometric derivatives are explicitly centered derivatives at fixed offset, not derivatives at fixed physical observation time. The exponentially small physical flux factor is retained outside the normalized integral.

This review has **not** independently re-established every upstream finite-bridge, differentiated two-block, and strict-margin estimate in the auxiliary sources. They remain necessary dependencies of the principal relative theorem. No finite determinant calculation, including those supplied here, closes that coverage limitation. The report therefore does not certify the entire forward theorem line by line.

## 3. Periodic reconstruction: E2 is genuinely repaired

**Locations:** `thm:v26-single-offset-global` and `article/23d_rank_two_lattice_recovery_v24.tex`, especially `thm:v24-uncalibrated-periodic-rigidity`. [S2, S4]

The corrected argument separates two logically different operations. With the two holonomies expressed in the same starting frame, write \(V=(v_1\ v_2)\) and let \(M\) contain the independent marked deck vectors. Then

\[
L=VM^{-1},\qquad G=M^{-T}V^TVM^{-1}.
\]

Real linear independence is sufficient; unimodularity is not required. These formulas recover the marked lattice realization in the chosen gauge, but do not place an unvisited obstacle. The rooted signature-rigid spanning tree performs that second task. At each transition the uniquely matched framed curve determines the adjacent placement. The explicit spanning assumption ensures that induction reaches all obstacle orbits. Realizability supplies existence and admissibility; it is not derived from the matrix calculation.

Changing the root frame moves the entire reconstruction by one simultaneous element of \(\mathrm{SE}(2)\). Independent motions of separate obstacles are not permitted. A determinant-six exact example and a common-gauge tree example reproduce these algebraic distinctions; a declared fifth vertex not reached by the four-vertex tree is correctly identified as uncovered. They are not tests of analytic signature rigidity or of geometric realizability. [D1]

It would be unfair to continue listing E2 as an unresolved mathematical gap after this repair. It would be equally wrong to infer general periodic rigidity without the incidence and realizability hypotheses. Analytic continuation and unique signature matching remain substantive upstream ingredients; this round did not independently recheck the complete finite-signature stability chapter.

**Minor presentation request R37-M1.** In the introductory `thm:v26-intro-rigidity`, use the exact phrase “rank-two anchoring pair based at one channel frame,” or explicitly point to its definition when summarizing the two cycles. The detailed theorem now states this correctly. This is alignment of the introductory summary with the proved statement, not a reopened E2 counterexample.

## 4. Statistical proofs: separate the likelihood, moment, and compactness steps

### 4.1 The original-alternative risk repair survives scrutiny

**Locations:** `article/18a_vector_boundary_information_v26.tex`, equations `eq:v35-one-mark-expansion`–`eq:v35-centered-fourth`, and `article/18a2_likelihood_tilting_moments_v34.tex`. [S5]

The one-mark expansion is made before dividing by the reference defining function. On the common collar it gives

\[
\frac{f_{\delta h}}{f_0}=1+\delta h^t\mathsf S
             +O_K\bigl(\delta^2(1+w_0^{-1})\bigr).
\]

Integrating against the truncated score yields the bounded alternative mean and its limit \(Jh\). With \(\ell=\log(1/\delta)\), \(q=\delta\ell^{1/4}\), and \(B=np\delta^2\ell\to1\), the critical budgets are

\[
np\delta q=B\ell^{-3/4},\quad
np\delta^2\log(1/q)=B\left(1-\frac{\log\ell}{4\ell}\right),\quad
np\delta^4q^{-2}=B\ell^{-3/2}.
\]

The fourth-moment estimate is applied to summands centered under the same alternative, and the bounded mean is restored afterward. Every excluded observation contributes zero; a censoring event at one coordinate does not erase the entire statistic. This is a direct original-product-law argument.

Separately, unit means and weak likelihood convergence imply uniform integrability through the truncated-expectation identity. Truncated likelihood tilting then gives the shifted Gaussian law, while positivity of the limiting likelihood supplies reverse contiguity. The supplement contains a direct proof, so no circular invocation of an unproved alternative limit is necessary. Combining this weak limit with the original-law fourth moments justifies unbounded quadratic risk. Total variation alone would not do so.

The Moore–Penrose inverse is fixed and acts on the identifiable range. No risk claim for an unidentifiable component is introduced. I do not reopen R1.

**Minor presentation request R37-M2.** The earlier short proof of `lem:v22-contiguity` should explicitly direct the reader to `prop:v34-tilting-moments` for the noncircular reverse-contiguity argument. The required proof is already present. Consolidating the navigation would improve exposition; deleting the moment derivation would not.

### 4.2 Finite likelihood convergence is correctly upgraded to compact experiments

**Locations:** `lem:v33-finite-likelihood` and `article/18a1_compact_experiments_v32.tex`. [S5, S6]

The finite likelihood-vector proof contains the needed normalization, uniform integrability, coupling, and disintegration. A common coupling gives the two deficiencies the bound \(\tfrac12\int|x_i-y_i|\); the unknown parameter index is not an input to either kernel. This remains valid for singular Gaussian information after restriction to its range.

The compact-net lemma is a separate theorem. For a fixed finite net, one kernel controls all parameters through the prelimit and limit continuity moduli. The proof takes the sample-size limit with that net fixed, then refines the net. The moving-support Hellinger estimate supplies the required prelimit modulus, and the Gaussian family supplies the limit modulus. The result concerns the original moving-support family on each fixed compact local set, not an unbounded local parameter space or the full infinite-dimensional analytic class.

These distinctions remove familiar errors in nonregular experiment arguments. They do not by themselves turn a standard compact-net passage into a new statistical principle.

### 4.3 Fresh check of the count–endpoint product and its rates

**Location:** `article/18d_count_endpoint_multirate_v32.tex`. [S7]

The count direction is normalized by \(D_\vartheta\gamma(v_\gamma)=1\), and the slow shape directions lie in its kernel. With \(\eta_n=(j_n\sqrt{k_n})^{-1}\), the Taylor remainder after the leading success-log term is bounded by

\[
C_K(\delta_n+\eta_n+j_n\delta_n^2+j_n\delta_n\eta_n+j_n\eta_n^2).
\]

Multiplication by \(\sqrt{k_n}\) makes each term vanish under the displayed hypotheses. For example, \(\sqrt{k_n}j_n\delta_n^2=(j_n\delta_n)(\sqrt{k_n}\delta_n)\to0\). Thus the slow coordinates do not acquire a hidden count score at the claimed scale.

For a negative-binomial waiting time stopped at \(k\) successes, the score for \(\log p\) is \((k-pT)/(1-p)\). Its variance and the sign change induced by \(\log p(b)-\log p(0)=-b/\sqrt{k_n}\) agree with the displayed central sequence. The geometric square-root-density path gives

\[
H^2(G_p,G_q)\le\frac{(\log p-\log q)^2}{4(1-p_*)}.
\]

This is a bound for the actual waiting distribution, not an uncontrolled Poisson replacement. The fresh checks use 25 exact-affinity evaluations and 27 finite-difference checks of the negative-binomial likelihood derivatives. [D1]

The independence argument is correctly placed in the uncapped Bernoulli-mark experiment. Caps are subsequently handled by coupling and their small exceptional probability; independence is not asserted after conditioning on completion. Removing the fast shape perturbation from the endpoint factor costs

\[
C_K k_n\eta_n^2\log(e/\eta_n)
 =C_K\frac{1+\log(j_n\sqrt{k_n})}{j_n^2}=o(1).
\]

Product kernels on compact coordinate projections can then be restricted to the original compact set. The separate finite-bridge transfer contributes \(C_Kk_n\tau^{j_n}\). The observed endpoints here are the declared laboratory transverse coordinates, not noiseless normal coordinates or an augmented collision array.

The conditions are compatible: taking \(k_n\) near \(e^{2n}/n\), \(\delta_n=e^{-n}\), and even \(j_n\) of order \(A\log k_n\), with \(A>1/|\log\tau|\), gives the required limits. The included integer-budget diagnostic illustrates one such choice with \(\tau=1/2\). No sharp necessity of these sufficient conditions is claimed.

## 5. Charged calibration and global reconstruction

**Locations:** `article/25a_common_observables_v25.tex` and `article/25b_augmented_global_reconstruction_v26.tex`. [S8]

The physical observation space really includes positions in one sensor frame shared by the two types of a channel. It does not provide inter-channel registration. The subsequent estimated projection is an observable map of the transcript. The true contact frame appears only in the comparison analysis. This is the correct distinction between an unknown coordinate change and a usable statistical kernel.

The capped onset scan does not require a union bound over every grid point. For each channel/type there is a particular grid time with true excess in \([h,2h]\). Failure at that time has probability at most \(\exp(-Np_*)\); any earlier success is already after onset and no later than that time. A union bound over the \(2|E|\) scans is enough. The grid midpoint estimator then satisfies \(j|\widehat g-g|\le h\). The exact finite checks examine 432 two-type success-time combinations, including boundary placements on the grid. They test this arithmetic, not the billiard success-mass lower bound. [D1]

The order of choices in the finite-order estimator is important and correct: choose the finite separators and sample sizes; choose the final even flight number \(J\); only then choose the pilot resolution, with pilot flight number also \(J\). This avoids applying a gap error proved at a smaller flight number to an uncontrolled larger one.

For the post-pilot batches, the proof uses uncapped successful marks to apply concentration, then charges the cap-exhaustion probability. Tests sharing a sample do not need to be independent for the union bound. The template argument explicitly includes gap coordinates, and its \(3c<8c\) margin yields the required finite-data conclusion. The total deterministic budget includes pilot and post-pilot failures.

The increasing-order argument is a compactness-and-diagonalization construction. Its budget-indexed implementation runs the selected stage afresh. Therefore the minimum flight number of that stage's acquired transcript can diverge; no such claim is made for a cumulative archive containing earlier stages. These are appropriate qualifications.

The theorem is non-effective in its separator library and compact inverse moduli. The source already says so. That is not a missing proof of the stated consistency result, but it materially limits what “reconstruction” means here: neither a quantitative analytic minimax rate nor a computationally feasible reconstruction algorithm follows. Moreover, the full position record admits a direct geometric-sampling benchmark. The global consistency statement is therefore not, on its own, evidence that the distributional inverse is necessary in that richer experiment. The manuscript now acknowledges this point; it must continue to do so.

## 6. Open major issues

### C2 — Complete native submission evidence is still absent

**Severity:** major delivery/verification issue; no implication that a mathematical theorem is false.  
**Locations:** `VERIFICATION_V37.md`, `RESPONSE_TO_REFEREE_V37.md`, and the hosted run identified below. [S1, C1]

The author reports a seven-page companion build and finite checks, while explicitly stating that the complete native main was not built or PDF-inspected. The actual companion product was described as attached to the preceding revision conversation, not committed as a complete-main product. This reviewer did not retrieve or inspect that attachment and does not promote its hash to independent PDF evidence.

The independently queried hosted run `34735598451`, job `103666347616`, refers to the mathematical-source commit `b0c21cd...`. Its conclusion is failure, its job has an empty step list and no assigned runner, and its artifact collection is empty. The live API reports an empty list; the author's ledger uses a null-like description. The material conclusion is the same: no executed native build is evidenced by this run. The reason for the infrastructure failure was not established. It must not be relabeled a TeX error.

A declaration of 52 direct main inputs or 36 auxiliary-wrapper inputs does not demonstrate a complete recursive checkout, a successful assembled article, or correct typesetting. A companion build is not a build of the main. A workflow file is not an execution record. The author correctly acknowledges these distinctions, but acknowledgment does not close C2.

### R37-V1 — The inherited driver's provenance check is not fail-closed

**Severity:** major for use of this driver as a source-pinned C2 certificate; a verification-tool issue, not a manuscript theorem defect.  
**Location:** `tools/build_submission.py`, `build_entry` recorder-input loop and `main` source-commit handling.  
**Exact driver blob:** `029e9e96537df18a032d36de55e449e262be87c4`. [B1]

For each recorder path inside the temporary compilation tree, the code finds the corresponding relative path but then hashes `SOURCE / rel`, not the candidate path in the compilation tree. There is no equality check between those two byte strings. If the `.fls` recorder is missing, the same function emits an empty input map and can still return `status: passed`. Separately, `git rev-parse HEAD` records a commit when available but does not establish that the source working tree is clean or matches that commit.

These are specific limitations, not speculation about malicious changes. I materialized the fetched driver and checked its Git blob identity before executing three isolated unit fixtures. The unmodified `build_entry` function was exercised with mocked external TeX and `pdfinfo` execution:

| Fixture | Driver result | Recorder evidence |
|---|---|---|
| Original and compilation copy agree | `passed` | Correct source hash, as a control. |
| Original and compilation copy differ | `passed` | Hash of the original source, not the compilation copy. |
| Recorder absent | `passed` | Empty input map. |

In the divergent-copy fixture, the original hash begins `7fbae491...` and the compilation-copy hash begins `a9d80cee...`; the recorded input is the former. Full hashes and outcomes are retained in `evidence/diagnostics.normal.json`. This demonstrates exactly what the metadata routine does and does not enforce. It does **not** demonstrate that the author's actual companion build used altered input. The fixture products are not genuine PDFs; no TeX process or native manuscript build was performed in these tests. [D1]

**Required remedy before relying on a green driver result for C2:** require a recorder and the native entry among recorded inputs; hash the actual compilation inputs; compare their hashes to a frozen source manifest tied to the declared Git tree; reject unexplained mismatches or identify and separately account for generated inputs; establish source cleanliness or provide an explicit content-addressed snapshot; and retain the complete final evidence. Trusted external packaging checks can provide equivalent guarantees, so this report does not mandate a particular software implementation. Merely changing the output status string would not fix the issue.

## 7. Significance and the journal-level threshold

The introduction's comparison with prior work is now materially more careful than a broad assertion of “generalized billiard rigidity.” De Simoi–Kaloshin–Leguil concern analytic open billiards with non-eclipse, symmetry, and genericity assumptions and marked-length data. Finamore–Leguil concern finite-horizon Sinai billiards and an enriched marked length spectrum. These are different observation maps from marked signed conditional channel laws and onsets. This review did not find a proved reduction identifying those data, and it does not claim subsumption in either direction. The manuscript already states that distinction; the cited work is not an omitted-reference finding. [S10, L1, L2]

Likewise, Meister–Reiß supply a pre-existing example of nonregular regression experiments equivalent to Poisson boundary experiments. The presence of a Poisson limit or a Gaussian/Poisson contrast is not by itself a new principle. The manuscript's related-work paragraph already recognizes this. [S10, L3]

The strongest prospective contribution is the combination of the nonlinear relative long-bridge law with the unsymmetrized contact inverse, under the precise observation conventions. The elementary four-density cancellation, the matrix identity for the lattice, the finite-net argument, and compactness-based consistency support that contribution; they should not each be counted as an independent breakthrough. The complete main is the object on which an ultimate significance and exposition judgment must rest. Neither a long sequence of revision numbers nor repeated author-requested referee memoranda supplies that judgment.

I do not recommend removing mathematical scope merely to make the submission look shorter. I do require a navigable final article in which the genuinely new nonlinear input, classical ingredients, observation levels, and conditional global consequences are visibly distinguished. Successful assembly is necessary for that assessment, but is not alone sufficient for acceptance in a leading general journal.

## 8. Executed checks and limits of this report

The companion package contains seven independently authored diagnostic families: six finite mathematical checks and one provenance-fixture family. The finalized program was executed under Python 3.13.5 in ordinary and optimized modes, with exit status zero in both, empty stderr, and byte-identical JSON. The output SHA-256 is

`4c322709006b0b3e626891bd53847cf5f08d9a0a3ca9b3a61b2fc5dd992b6cb1`.

The seventh family's expected outcome is `expected_provenance_weaknesses_reproduced`, not a declaration that the driver is satisfactory. The code uses explicit exceptions rather than assertions that disappear under optimization. The source driver snapshot is retained byte-for-byte as a fixture, not as a modified author build tool. Commands, hashes, and coverage are in the accompanying ledger and `evidence/execution.json`. [D1]

The present local environment did not yield a complete repository checkout. No complete native main, native companion, or actual manuscript PDF was built or inspected by this reviewer. A GitHub read of a TeX source is not visual inspection of its typeset product. Unchanged Poisson-kernel, full signature-stability, and other auxiliary chapters were not all independently re-proved in this round. The coverage ledger makes these limitations explicit rather than silently inheriting a universal correctness certificate from earlier reports.

## 9. Concrete conditions for the next submission

1. **Close C2 with actual products.** Supply the unabridged native main and companion, complete final logs, commands, executable versions, exit statuses, recorder/input manifests, and a retrievable source snapshot tied to a declared commit/tree. Include explicit inspection coverage of the assembled PDFs and resolve missing symbols, unresolved references/citations, and obstructive layout defects. An evidence artifact need not be committed as a binary file if it is reliably retrievable and unambiguously bound to the source.
2. **Close R37-V1 or provide equivalent independent assurance.** Demonstrate that recorded input hashes describe the compilation inputs, not merely another source directory. An absent recorder or unexplained source mismatch must not count as successful source-pinned verification. Include negative controls for these cases.
3. **Preserve the mathematical repairs.** Retain the complete tree and common-frame anchoring hypotheses, the smooth remainder/envelope proof, original-alternative moment estimates, finite-to-compact experiment argument, charged failure budgets, and observation-level distinctions. Align the short introductory and contiguity summaries with the detailed proofs without replacing those proofs with a response document.

The next response should state which of these requirements was actually executed and identify the resulting products. It need not invent a new theorem to compensate for an absent build. On the present evidence, E2 and I1 are closed, R1 and the compact-experiment repair are retained, C2 remains open, and R37-V1 is a reproduced verification gap. **No new fatal mathematical counterexample is established in this report; no blanket mathematical or journal-acceptance certificate is issued.**
