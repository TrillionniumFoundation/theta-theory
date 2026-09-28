# Independent referee-style report on A2 revision 38

## Submission, identity, and recommendation

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 13, 2026  
**Standard:** mathematical correctness, significance, and exposition expected of a leading general mathematics journal. This is an author-requested, AI-assisted external-referee-style assessment. It is not a commissioned report or an editorial decision of any journal.

| Object | Frozen identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Reviewed revision | `revision/a2-v38-source-pinned-native-referee-response-2026-09-13` |
| Submission commit | `7b506becac7fc51dc1ea4f5ab407389d1208b07a` |
| Submission tree | `ff91a3fba7ae4ffd7506669198c738805e40cf33` |
| Mathematical-source increment | `c206a27ba01f20f1a21b780e6d71c77a837ef11d` |
| Source and repaired-tools increment | `7d34d96a7c2dd974ab3725e009bbb584d3228114` |
| Preceding referee commit | `377efa79597776e75e3cc1d399c1986edd097aaf` |
| Native main | `papers/A2-v17-boundary-information-coarsening/main.tex` |

The directory name `A2-v17` is not the revision number. This report concerns the displayed immutable submission, not a subsequently moving branch. Source keys, read coverage, execution records, and literature checks are in [AUDIT_AND_REPRODUCTION.md](AUDIT_AND_REPRODUCTION.md).

**Recommendation: MAJOR REVISION. I do not recommend acceptance at the stated journal level, and the package has not demonstrated complete native submission readiness.**

This verdict must not obscure the actual progress. R37-M1 and R37-M2 are repaired in the mathematical article. The source-provenance implementation fixes the reported R37-V1 failure modes, and independently authored negative controls confirm the relevant rejection behavior. The previously corrected original-alternative moment argument is retained. I have not established a new fatal mathematical counterexample in the arguments examined here.

The outstanding complete-main delivery requirement, C2, is nevertheless not satisfied. The author explicitly says so. An inspected companion, a miniature integration fixture, and successful software tests do not constitute the complete article. Nor would a successful compilation, by itself, establish the mathematical significance required for a top general journal. These are distinct standards, and the report treats them separately.

This round expands the mathematical audit beyond the immediate wording changes: it examines the finite Jacobi reduction and relative determinant, nonlinear two-end factorization, smooth finite-jet inverse, finite-signature embedding and noisy matching, and both directions of the moving-ceiling comparison. The positive findings below apply to these inspected arguments, not automatically to every inherited appendix or every downstream theorem.

## 1. Revision delta and disposition of the previous report

The GitHub comparison from the preceding referee commit to this submission is three commits ahead and changes 29 paths. The only modified active mathematical TeX files are `main.tex`, `article/01_introduction_v27.tex`, and `article/18a_vector_boundary_information_v26.tex`. The other changes concern tooling, a workflow, documentation, evidence, or preserved predecessor copies. This is a targeted repair, not a newly established proof of all inherited conclusions. [S00–S03]

| Referee item | Disposition in this review | Basis |
|---|---|---|
| E2: complete periodic placement | **Accepted repair retained** | The detailed single-offset theorem still distinguishes lattice recovery from rooted placement, with realizability and signature-rigid coverage. |
| R37-M1: introductory anchoring hypotheses | **Closed** | The introduction states the common-frame anchoring pair, cites its definition, assumes realizability, and requires a rooted signature-rigid tree reaching every obstacle orbit. The abstract is aligned. |
| R37-M2: short contiguity argument | **Closed** | The native short proof now invokes the independent normalized-likelihood argument and expressly does not assume an alternative central-sequence limit. |
| R37-V1: actual-input identity | **Closed for the reported failure modes within the declared trust boundary** | Actual compilation files are checked against the frozen manifest; recorder, native entry, recursive inputs, and imported auxiliary provenance are mandatory. Independent controls confirm these checks. This is not a full-CLI execution certificate. |
| R1: original-alternative moments | **Repair retained; not reopened** | The native likelihood-tilting supplement supplies the bounded alternative mean and the centered fourth-moment argument under the original laws. |
| Finite versus compact experiments | **Retained; no contrary finding** | The finite likelihood lemma was directly checked. A fresh exhaustive re-audit of the separate compact-experiment and multirate chapters is not claimed. |
| I1: current navigation | **Maintained** | The current root and manuscript entries identify v38 and its response and verification records. |
| C2: complete native article and inspection | **Open; major delivery requirement** | No complete-main build or visual-inspection product is delivered in the stated record. The re-read hosted job has no executed steps and no artifacts. |

It would be incorrect to keep R37-M1, R37-M2, or the two reproduced R37-V1 behaviors on a list of uncorrected defects. It would be equally incorrect to convert their repair into a blanket certificate of correctness or suitability for a leading journal.

## 2. The nonlinear relative law: substantive fresh examination

### 2.1 Finite geometry and the Jacobi normalization

**Locations:** `lem:g-channels`, `lem:g-jacobi`, `lem:g-relative`, `eq:v3-green`, and `eq:v3-cofactor`. [S04]

The localization argument makes the relevant distinction between the globally shortest channels, which exhaust the sufficiently near-onset complete event, and a specified nonminimal closest chord with positive clearance, for which only its selected local itinerary is covered. The positive-definite closest-pair Hessian and the separated normal collision states supply a flight-number-independent neighborhood. The text does not infer complete-event coverage merely from a local stationary segment.

For the alternating quadratic problem, the change of variables
$$
 y_i=\sigma_i z_i,\qquad \sigma_i=\sqrt{c_{1-(i\bmod2)}}
$$
reduces the interior recurrence to a constant-coefficient recurrence. The effective endpoint Hessian and Green kernel have the required parity factors. The cofactor identity
$$
 -W_{uv}=\frac{\prod_{i=0}^{j-1}(-\ell_{i,uv})}{\det H_{\rm int}}
$$
includes the one-flight case through the empty determinant convention. The sign is consistent with a positive interior Hessian and negative local mixed derivatives.

I checked these formulas independently against finite matrix inversion and Schur complementation for 21 geometry/length combinations, including unequal curvatures and both parities. The largest Green residual was approximately `2.22e-15`; the largest relative twist discrepancy was approximately `7.22e-15`. These computations are useful indexing and normalization controls, not a proof of the nonlinear theorem. [D1]

### 2.2 Why the determinant estimate is genuinely relative

**Locations:** `lem:g-relative`, `lem:v4-halfline`, and `thm:v4-factorization`. [S04–S05]

The finite-dimensional determinant argument uses an entrywise summable perturbation, not a dimension-dependent operator-norm estimate. Tridiagonality and the two endpoint weights give
$$
 \|\Delta H\|_1\le \sum_{i,k}|\Delta H_{ik}|=O(|u|+|v|).
$$
The logarithmic determinant series then retains a trace-class factor in every differentiated term. The weighted Green estimate uses two strict geometric ratios, so fixed parameter derivatives are absorbed without introducing a loss proportional to the number of sites.

The subsequent two-boundary proof contains the additional step that a finite relative bound alone would not provide. It glues a left half-line solution to a reversed right half-line solution, estimates the stationarity residual in the sum norm, and uses uniform diagonal dominance to control the finite stationary correction in that same norm. It then keeps the first and last `floor(j/3)` interior blocks. The discarded perturbation has exponentially small trace norm; the reflected and off-diagonal Green blocks are also exponentially small. The direct-sum logarithm becomes the sum of the two half-line logarithms.

In particular, the proof does not divide an absolute action remainder by the exponentially small reference twist. The use of a slower fixed exponential to absorb each fixed polynomial derivative loss is legitimate. The rate need not be uniform over arbitrary derivative orders with their constants fixed; the manuscript correctly allows the constants to depend on order and higher boundary norms.

As an independent finite control, I solved the stationary equations for asymmetric cubic/quartic local graph pairs, for both starting types and signed endpoints. Against two 64-flight half-line approximations, the normalized log-amplitude factorization errors at 8, 16, and 24 flights were respectively about `5.5e-6`, `1.0e-9`, and `3.2e-13`. The maximum stationary residual was about `1.04e-17`. These are finite local models, not a verification of global periodic realizability or of the infinite-dimensional analytic estimates. [D1]

### 2.3 The offset endpoint and the scope of the derivatives

**Locations:** `thm:v8-main-relative` and the proof of `thm:v4-law`. [S03, S05]

The normalized sublevel integral is compared through a common Morse-domain representation, rather than by formally differentiating a moving sharp boundary at zero. The positive Hessian square root and inverse coordinate map have uniform fixed-order control on the stated compact positive cone. Rescaling to a fixed disk and canceling odd terms explains the finite extra derivative budget for each offset derivative. The quadratic normalization gives the stated value one at zero.

The geometric derivatives are explicitly channel-centered derivatives with `t = j g(xi) + d`. They are not fixed-physical-time derivatives. That convention is mathematically essential, not dispensable notation.

I found no failure in this inspected relative-law mechanism. I have not independently reconstructed every suspension/flux, regular terminal-level, and other auxiliary dependency from first principles in this round. The finite computations cannot remove that stated coverage boundary.

## 3. The signed inverse: correct algebra supported by a nontrivial envelope argument

**Locations:** `thm:v26-density-inverse`, `prop:v26-density-stability`, `lem:v27-smooth-jet-factorization`, and `prop:v22-last-jet-block`. [S06–S07]

For the interior density
$$
 f(u,v)=Z^{-1}B(u)B(v)[d-S(u)-S(v)],
$$
the four-density ratio gives exactly
$$
 1-\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}
 =t(u)t(v),\qquad t(u)=\frac{S(u)}{d-S(u)}.
$$
Strict convexity makes the fixed nonzero anchor positive. Thus the action and normalized amplitude are recovered without supplying the flux amplitude. Negative and positive coordinates remain distinct. The continuous-density representative is justified within the model class; the manuscript does not assume that an individual statistical sample reveals pointwise density values.

The local stability result uses an interior `C^M` norm, positive density denominators, and a nonvanishing anchor. It does not infer derivative control from total variation or uniform conditioning as the anchor or offset tends to zero. The exact cancellation was independently checked on 121 signed rational endpoint pairs. [D1]

The contact inverse contains a more substantial argument than this algebra. Differentiating a finite action truncation cancels all interior orbit variations by stationarity and leaves a terminal term with a summable exponential bound. For two smooth graph pairs with equal jets through order `M`, interpolation gives the direct flight variation
$$
 \partial_t\ell=\frac{h}{\ell}
       [\Delta\psi_r(y)+\Delta\psi_{1-r}(z)].
$$
Integrating the finite identity before sending the truncation to infinity yields an action difference of order `|u|^{M+1}`. This establishes finite-jet factorization in the presence of genuine smooth remainders and flat perturbations. Finite lists of Taylor coefficients alone are not used as functional remainder bounds.

At the first occurrence of degree `n`, the boundary site is counted once and each interior site twice. The coefficients are therefore
$$
 1+2\sum_{k\ge1}e^{-2n\gamma k}=\coth(n\gamma),\qquad
 2\mathfrak r_b^n\sum_{k\ge0}e^{-n\gamma(2k+1)}
 =\mathfrak r_b^n\operatorname{csch}(n\gamma).
$$
The determinant-one identity follows with the correct multiplicities. It is the leading smooth inverse and the block-triangular finite recursion together that justify fixed-order invertibility. Determinant one alone would not prove an infinite-order inverse theorem, and the manuscript does not make that inference.

The independent controls include 12 jet blocks and finite cubic-envelope variations of the actual local flight-length function. They support the displayed algebra and finite bookkeeping, not the general analytic theorem. Exact reconstruction of connected boundary images still requires analyticity; equality of smooth jets does not determine a smooth obstacle away from its contact.

## 4. Finite signatures and periodic placement: a new audit, not an inherited endorsement

**Locations:** `thm:v25-finite-signature-embedding`, `lem:v25-noisy-signature-match`, `lem:v24-gluing-persistence`, and the detailed single-offset composition. [S08, S06]

The finite-signature chapter separates three issues that must not be conflated: exact analytic uniqueness, unique noisy finite-signature matching, and a non-effective compact inverse modulus.

For a transition obstacle, the assumed unique complete oriented signature match excludes a nonidentity orientation-preserving symmetry. In particular, its curvature is not constant. At every normalized arclength point, some derivative of the finite curvature-signature vector therefore has to be nonzero; otherwise analytic continuation would make the curvature constant. Compactness of the declared class, together with the finite obstacle list, gives a uniformly finite order and a positive derivative lower bound. A uniform second-derivative bound yields a short-arc lower separation estimate. A second compactness argument separates pairs outside that arc by finitely many signature coordinates.

This is a valid finite-subcover argument under the assumptions actually imposed. A mere common holomorphic strip bound, allowing the class to approach a symmetric limit outside the signature-rigid class, would not supply the same positive margins. The manuscript instead assumes a closed compact class of the prescribed realizations. I do not identify an omitted hypothesis here.

The noisy matching lemma also provides the missing local argument rather than relying only on outside-arc separation. For
$$
 F(x)=\tfrac12|\widetilde J(x)-y|^2,
 \qquad
 F''(x)=|\widetilde J'(x)|^2+
          (\widetilde J(x)-y)\cdot\widetilde J''(x),
$$
the stated `C^2` control makes the second derivative uniformly positive on a sufficiently short target arc. Global separation confines every minimizer to that arc; strict convexity gives uniqueness. A `C^0` perturbation alone is not claimed to give a unique nearest point. The local Lipschitz statement uses the corresponding `C^1` control when comparing the critical-point equations.

For periodic reconstruction, the detailed composition correctly keeps metric recovery and placement separate. In the common starting frame,
$$
 L=VM^{-1},\qquad G=M^{-T}V^TVM^{-1}.
$$
Independent marked deck directions are sufficient; unimodularity is not needed. These formulas do not place an unvisited obstacle. The rooted signature-rigid spanning tree, reaching every obstacle orbit, supplies that induction. Realizability supplies existence and admissibility. The introductory theorem now states the same structure.

The resulting compact inverse modulus is a continuity conclusion on the prescribed compact class. It is not a quantitative analytic continuation algorithm, a minimax rate, or a polynomial-time reconstruction guarantee. Those stronger statements should not be attributed to this theorem in a cover letter or subsequent summary.

## 5. Statistical arguments and the retained observation levels

### 5.1 The likelihood repair is noncircular

**Locations:** `lem:v22-contiguity`, `lem:v33-finite-likelihood`, and `prop:v34-tilting-moments`. [S09–S10]

The revised short proof now follows a valid dependency order. Null LAN gives a strictly positive limiting likelihood of mean one. Unit prelimit means and convergence of bounded truncations yield uniform integrability. This gives forward contiguity. For reverse contiguity, the direct inequality
$$
 P_n(A_n)\le P_n\{L_n\le c\}+c^{-1}Q_n(A_n)
$$
and positivity of the null-law limiting likelihood suffice. No alternative central-sequence limit is assumed to prove the contiguity needed for that same limit. The detailed supplement actually contains this argument.

The finite likelihood-vector lemma separately supplies a common coupling and disintegrations, with both deficiencies bounded by the appropriate coordinatewise `L^1` coupling error. The unknown parameter index is not an input to either kernel. This direct check supports the finite-experiment step; it is not a replacement for the later uniform-modulus argument on compact parameter sets.

The original-law fourth-moment calculation is also retained. With `ell = log(1/delta)`, `q = delta ell^(1/4)`, and `np delta^2 ell` tending to one, the mean and moment budgets are
$$
 np\delta q=O(\ell^{-3/4}),\qquad
 np\delta^2\log(1/q)=O(1),\qquad
 np\delta^4q^{-2}=O(\ell^{-3/2}).
$$
The independent summands are centered under the same alternative, and their bounded mean is restored afterward. Every excluded observation contributes zero; one exclusion does not erase the whole sample. Weak likelihood tilting and this original-law fourth-moment bound then justify compact-local quadratic risk on the identifiable range. Total variation alone would not justify that unbounded-loss conclusion. R1 is not reopened.

### 5.2 Both Poisson comparison directions have been examined

**Location:** `article/18c1_endpoint_time_deficiency_v25.tex`, especially `lem:v24-layer-bulk-bounds` and `thm:v24-two-sided-deficiency`. [S11]

The chapter assumes more than convergence of the ceiling trace. On the common bulk it explicitly requires a relative density perturbation of order `1/k`. Conditional bulk normalization then gives squared Hellinger error of order `1/k^2`; after `k` records its total-variation cost is of order `1/sqrt(k)`. A bare `o(1)` trace estimate would not justify this conclusion. The text identifies the extra hypothesis and explains its use in the anchored fixed-window application.

The reference layer and its change of coordinates depend only on the reference model. Its mass is `O(1/k)`, so binomial-to-Poisson comparison has cost `O(1/k)`. The corner where the moving ceiling meets `r=0` is handled separately: the endpoint strip has area `O(1/k)` and the residual interval has length `O(1/k)`, giving one-record mass `O(1/k^2)` and sample cost `O(1/k)`.

The reverse kernel reconstructs the layer coordinates, adds reference-bulk records, and uniformly permutes the result. It is defined even for too many Poisson points or a reconstructed nonpositive residual time, and those exceptions are bounded. Thus this is an actual two-sided comparison, not merely convergence of an extracted point process. The ancillary tail interpretation is also stated on fixed compact local parameter sets.

I found no error in this inspected kernel construction. An independent normalized radial control checks the layer/corner mass budget; it is explicitly not asserted to be billiard-realizable. The abstract comparison theorem should not be read as automatically verifying every physical multi-parameter application or every multirate design in chapters not exhaustively rechecked here.

### 5.3 Physical calibration does not turn the intrinsic inverse into an equivalence theorem

**Location:** the charged scan and calibration theorem in `article/25a_common_observables_v25.tex`, together with the introductory comparison. [S12, S02]

The pilot uses planar positions, not only scalar transverse laws. Both types share a sensor frame within a channel; distinct channels remain unregistered. The near-onset success lower bound is used at a grid point known in the analysis to lie in the required collar. The proof does not require that lower bound at arbitrary late scan times, and a finite run of failures is not treated as proof of zero success probability. The deterministic cap charges all preparations.

Choosing the pilot flight number to equal the final selected flight number controls the correct error `J |g_hat-g|`. The post-pilot scalar test criterion is a genuinely coarser statistic, but the total acquisition protocol remains richer than the intrinsic law-valued datum. The text now states that distinction and includes a direct-position benchmark in the same long-even-flight experiment. These qualifications are essential to the significance claim.

## 6. Source provenance: the reported defects are fixed, but C2 is not

**Locations:** `tools/source_provenance.py`, `tools/build_submission.py`, and the author verification ledger. [S13–S15]

The new implementation freezes Git-object bytes, records commit/tree identities, excludes explicitly listed prior root products, and verifies the compilation copies against the manifest. After compilation, it requires a nonempty recorder, the correct working directory, the native entry, and every recursive static input. It rejects unexplained local inputs. Imported companion auxiliary data are distinguished from source and tied to their producer; their actual bytes and occurrence in the consumer recorder are checked.

The driver source invokes these checks before issuing a successful product status. The trust boundary is explicitly Git and the installed toolchain, not a hostile compiler or a transient change-and-restore attack. Inventing an adversarial scenario outside that boundary would not establish that the reported ordinary provenance defect persists.

For this review I materialized the exact provenance module and checked both its Git blob and SHA-256 identities. Independently authored tests used real temporary files, not a mocked successful TeX process. All 23 controls behaved as required, including rejection of divergent compilation bytes, absent or empty recorders, absent native/recursive entries, unapproved inputs, symlinks, and corrupted or unrecorded imported auxiliary data. Matching inputs and properly accounted-for auxiliary data were accepted. [D1]

**This is narrower than a complete execution of the new CLI.** I did not independently run the author's 41-test program, build either native manuscript, or re-create its miniature TeX integration. Those are author-reported executions in the ledger, not executions by this referee. The independent tests and the inspected driver integration support closure of the specific R37-V1 failure modes, not universal software attestation.

The remaining evidence is as follows:

| Product or execution | What the present record supports |
|---|---|
| Author's miniature TeX integration | Explicitly a fixture, not the A2 main; not independently executed in this review. |
| Author's seven-page companion | Source/PDF identities and inspection are reported in the ledger; the raw previous-conversation attachment was not independently retrieved and inspected here. |
| Hosted run `34743133630`, job `103686134246` | Independently re-read: completed with failure, empty step list, runner ID zero; artifact endpoint returns zero artifacts. |
| Complete native main | Author explicitly reports no build and no PDF inspection; no complete-main execution product is established here. |

The hosted metadata do not identify the underlying failure cause and do not record a TeX command. Calling this a TeX compilation failure would be inaccurate. Likewise, companion summaries without a retrievable product are not an independent companion inspection.

**C2 remains open.** A durable evidence location may be a repository attachment, a retained release artifact, or another retrievable source-bound package; committing every binary to Git is not mandatory. A reference to an attachment in a previous conversation is not, by itself, a durable retrieval route for a new external referee. This is part of the existing delivery requirement, not a new counterexample to billiard rigidity.

## 7. Significance and exposition at the requested journal level

The manuscript's strongest prospective contribution is the nonlinear relative long-bridge law combined with the unsymmetrized, all-order alternating-contact inverse under its precise observation map. The elementary four-density cancellation is useful and exact, but is not by itself the main depth. Nor are `L = V M^{-1}`, a finite-subcover argument, the compact-injection inverse modulus, or a Gaussian/Poisson contrast independently sufficient reasons for publication at the requested level.

The related-work paragraph appropriately distinguishes its data from marked length spectra. The primary abstracts checked for De Simoi–Kaloshin–Leguil concern analytic open billiards with symmetry/genericity hypotheses; Finamore–Leguil concern finite-horizon Sinai billiards and enriched marked-length data. The present result assumes signed channel laws, onsets, marked deck labels, and specified signature-rigid incidence structure. No reduction between these observation maps was established in this review. I therefore neither claim subsumption nor allege that the manuscript has omitted those already-cited works. [L1–L2, S02]

Meister–Reiss provide an earlier nonregular-regression/Poisson-boundary equivalence. The existence of a Poisson boundary experiment is not, in isolation, a new statistical principle. The paper already acknowledges this. My literature check is limited to those primary records and the manuscript's comparison; it is not an exhaustive priority investigation. [L3, S02]

For a leading general journal, the complete article must make the genuinely new nonlinear mechanism readily distinguishable from the supporting standard arguments, the conditional global consequences, and the distinct statistical observations. A large number of theorem labels, appendices, revisions, or author-requested referee reports is not evidence of significance. Conversely, arbitrary deletion of difficult mathematics would not improve the argument. The required remedy is a coherent hierarchy and a verifiable complete article, not an artificial contraction of its mathematical scope.

**Minor presentation request R38-P1.** The compiled auxiliary section `article/65_envelope_minimax.tex` opens with development-history narration about a referee memorandum. Its mathematical model is explicitly an envelope with physical leading parameters, not a claim that all spliced nuisances are billiard-realizable; that distinction is good. Retain the proof and that distinction, but move developmental narration to the appropriate acknowledgement or external provenance record while preserving any necessary scholarly attribution. A submission appendix should read as mathematics rather than as a continuing response log. This is an editorial request, not a new mathematical obstruction. [S16]

## 8. Independently executed checks and limits

The accompanying program contains four finite mathematical families and one provenance family with 23 controls. It was executed with Python 3.13.5 and NumPy 2.3.5, once normally and once under `-O`, with `OPENBLAS_NUM_THREADS=1`. Both executions returned zero, stderr was empty, and the JSON outputs were byte-identical. The output SHA-256 is

`fb558b857dc429d77b349d8018cead07d218a599649f8986126d5ef86967abce`.

The code uses explicit exceptions rather than optimization-disabled assertions. The finite mathematical families concern quadratic Jacobi identities, nonlinear finite local-flight factorization/envelopes, exact signed-density/finite-jet algebra, and a normalized radial layer/corner control. Tolerances and actual errors are in the code and outputs. Floating-point residuals close to machine precision are measured diagnostic quantities, not rigorous interval bounds. [D1]

No complete repository checkout was materialized locally for this review. No native main, native companion, or actual manuscript PDF was compiled or visually inspected by this reviewer. The source review is not a substitute for typeset inspection. The common-orientation quotient, every multirate application, all Abel and count-only arguments, and the complete 36-input auxiliary compendium have not all been independently re-proved in this round. The audit ledger makes read coverage explicit.

## 9. Requirements for a further submission

1. **Close C2 with actual complete products.** Supply the unabridged native main and companion, source-bound logs, commands, executable versions, return codes, recorder/input manifests, and a durable source/PDF retrieval route. Include explicit visual-inspection coverage of the assembled documents and remedy unresolved references, missing symbols, duplicate labels/destinations, or obstructive layout defects. Neither a fixture nor a workflow configuration substitutes for execution.
2. **Preserve the mathematical repairs and their exact scope.** Retain the common-frame anchoring and rooted coverage, the functional smooth-remainder/envelope proof, the original-law mean and moment estimates, the separate compact-experiment argument, and charged observable calibration. Do not silently replace the intrinsic transverse-law datum by ambient position sampling or the physical model by an unrestricted nuisance envelope.
3. **Present the complete mathematical contribution as a finished article.** Make the principal nonlinear estimates and their dependency chain central, distinguish classical supporting facts and conditional consequences, and keep revision-management material outside the theorem–proof narrative. Address R38-P1 without deleting its proof or misrepresenting its model. A top-journal significance claim must rest on the mathematics and comparison of observation maps, not on the fact that earlier objections have been answered.

The recommendation is not a demand for a new theorem to compensate for missing build evidence. It is also not a declaration that the principal mathematical program has failed. The precise disposition is: the two v37 mathematical-presentation requests are closed; the reproduced provenance failure modes are repaired and independently tested; C2 remains open; no new fatal mathematical counterexample has been established within the stated audit coverage; and no acceptance or universal-correctness certificate is issued.
