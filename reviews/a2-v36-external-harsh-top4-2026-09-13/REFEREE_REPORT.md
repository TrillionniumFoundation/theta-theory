# Independent harsh referee-style report on A2 v36

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed branch:** `revision/a2-v36-complete-native-delivery-top4-2026-09-13`  
**Immutable reviewed submission:** `0802bfa20533feff55bf5620d39d6399d5e778f5`  
**Submission tree:** `8a3872f8f341644ef206b019f3308ed9babd40ac`  
**Native entry:** `papers/A2-v17-boundary-information-coarsening/main.tex`  
**Review branch:** `review/a2-v36-external-harsh-top4-2026-09-13`  
**Date:** September 13, 2026.

This is an author-requested, AI-assisted independent referee-style assessment against the requested standards of Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, and Acta Mathematica. It is not a commissioned journal report, an editorial decision, or a claim of affiliation with those journals. It does not constitute an additional human referee. Source keys, inspection coverage, execution evidence, and limitations are recorded in [SOURCE_AUDIT.md](SOURCE_AUDIT.md). The locations below refer to source filenames and theorem labels, not pages of an uninspected PDF.

## Recommendation

**Major revision of the assembled submission; no acceptance recommendation in its present state. The v36 mathematical clarification is satisfactory, but the promised complete native delivery has not been demonstrated.**

The revision does not make a new substantial mathematical change. Relative to the exact v35 submission, it adds thirteen explanatory lines to the likelihood-tilting chapter, changes two version-identification lines in the native entry, adds a workflow, and imports the previous referee files. The density expansion, alternative mean, centered fourth-moment estimate, and original-law quadratic-risk argument remain intact. I do not reopen those repairs. [S1–S4]

The central unresolved requirement is still **C2**. The latest workflow on the reviewed SHA failed before any step was executed and has no artifacts. The workflow definition describes a suitable source-first retention procedure, but that description is not execution evidence. In addition, both current README entry points still identify v35 and direct the reader to the previous response and verification ledger. This is a new version-navigation regression, **I1**, rather than an objection to the historically stable directory name. There is also a limited hypothesis-reference error, **E2**, in the single-offset global theorem. [S1, S2, S6, C1]

**No new fatal mathematical counterexample was established in this examination.** In particular, the abstract two-sided moving-ceiling comparison, the analytic finite-signature matching mechanism, and the marked rank-two reconstruction survive the checks described below. This is not a correctness certificate for every input of the assembled article. Nor is absence of a discovered counterexample an acceptance criterion at the requested journal level.

| Identifier | Disposition | Required action or reason |
|---|---|---|
| R1: alternative mean and unbounded quadratic risk | Closed in the re-examined argument | Retain the in-place expansion, centering, and original-law fourth moments |
| V36 dependency clarification | Satisfactory | The three logical roles are now distinguished explicitly |
| Finite likelihood normalization and compact Gaussian passage | Not reopened in the inspected scope | The normalized likelihood coupling and separate continuity/net argument are present |
| Count–endpoint record distinction | Previous disposition not reopened | No new change or counterexample established; this round does not freshly audit the entire count theorem |
| C2: complete native submission and actual verification | **Open; delivery blocker** | Supply actual immutable-source build products, logs, and inspection evidence |
| I1: current version/navigation | **Regressed; correction required** | Align both README entries, current response, and tested-source ledger with the actual submission |
| E2: full-table theorem hypothesis reference | **Correction required; not a counterexample** | Cite or explicitly state the spanning-tree hypothesis of the full periodic rigidity theorem |

The next revision should complete and identify the submission, not manufacture another theorem to compensate for an unexecuted build. No arbitrary deletion, weakening to finite parameter sets, or removal of the established geometric and statistical scope is requested.

## 1. What v36 actually changes

The reviewed commit is dated September 13, 2026, 02:04:07 UTC, or 04:04:07 Europe/Amsterdam. The authenticated comparison with v35 at `1c50ef04fc2863b4744b5312b539cb68265054f3` is four commits ahead and zero behind. It lists exactly seven changed paths and no deleted path. The active mathematical-source changes are confined to `main.tex` and `article/18a2_likelihood_tilting_moments_v34.tex`. The former changes its version comment and PDF subject from 35 to 36; the latter adds the dependency paragraph discussed below. The abstract and direct input sequence are not changed by that comparison. [S1]

It is important not to inflate this increment. The revision inherits the earlier geometric and statistical proofs; it does not newly prove them because their source files are retained. Conversely, unchanged proofs should not be treated as newly defective simply because a review is requested again. The present examination therefore distinguishes direct rechecking, newly extended module coverage, and inherited dispositions.

The manuscript's stable `A2-v17-...` directory is not itself a problem. The actual problem is that the root README and the paper README explicitly say v35, point to the v35 branch, and identify the v33 report as the latest addressed review, despite the v36 entry and imported v35 referee report. A reader following the current entry points is not given an accurate account of the revision now under review. [S2]

## 2. The statistical repair remains mathematically meaningful

### 2.1 Three different arguments, not one interchangeable estimate

The added paragraph correctly separates the one-mark density expansion, likelihood tilting, and integrability of unbounded loss. These are different tasks. Write the successful density as

\[
 f_\theta=a_\theta(w_\theta)_+,
 \qquad \mathsf S=D_\theta\log a_\theta|_0+V/w_0,
 \qquad J=\mathcal J_\Sigma.
\]

With \(\ell_n=\log(1/\delta_n)\), \(q_n=\delta_n\ell_n^{1/4}\), and \(C_n=\{w_0\ge q_n\}\), the in-place proof expands the smooth product before dividing by the reference density:

\[
 \frac{f_{\delta_nh}}{f_0}
 =1+\delta_nh^t\mathsf S
       +O_K\!\left(\delta_n^2(1+w_0^{-1})\right).
\]

In normal coordinates \(s=w_0\), the density-volume factor is of order \(s\), while the score is of order \(1+s^{-1}\). Integrating the remainder against the score therefore costs a logarithm. The resulting mean expansion is

\[
 \mathbb E_{n,h}\Delta_n
 =np_n\delta_n\mathbb E_0[\mathsf S1_{C_n}]
  +np_n\delta_n^2\mathbb E_0[\mathsf S\mathsf S^t1_{C_n}]h
  +O_K(np_n\delta_n^3\log(1/q_n))
 =Jh+o_K(1).
\]

This controls the alternative mean before the fourth-moment estimate is applied. For \(B_n=np_n\delta_n^2\ell_n\to1\), the relevant budgets are

\[
 np_n\delta_nq_n=B_n\ell_n^{-3/4},\qquad
 np_n\delta_n^2\log(1/q_n)
 =B_n\left(1-\frac{\log\ell_n}{4\ell_n}\right),\qquad
 np_n\delta_n^4q_n^{-2}=B_n\ell_n^{-3/2}.
\]

The independent-sum fourth-moment estimate is applied to centered summands, after which the bounded mean is restored. The conclusion is compact-uniform fourth moments under the **original alternatives**, not merely under a censored surrogate. Each excluded observation contributes zero; an excluded observation does not erase the rest of the sample. These are substantive repairs, not cosmetic notation. [S3, S4]

### 2.2 Tilting and quadratic risk

For the censored likelihoods, nonnegativity, weak convergence, and unit means imply uniform integrability through

\[
 \mathbb E(L_n-A)_+=1-\mathbb E(L_n\wedge A).
\]

The limiting Gaussian likelihood is positive and has mean one. Truncated tilting gives the shifted limit; the bound

\[
 P_n(A_n)\le P_n\{L_n\le c\}+c^{-1}Q_n(A_n)
\]

gives reverse contiguity. This avoids assuming the desired alternative limit in order to prove that same limit. Combining the weak limit with the direct fourth-moment bound justifies quadratic-risk convergence. Total-variation comparison alone would not justify that step for an unbounded loss. The fixed Moore–Penrose inverse acts on \(\operatorname{Ran}J\); the proof does not invert information in unidentifiable directions. [S3, S4]

The new dependency paragraph accurately explains this architecture. It does not replace the calculations already present, and it should not be advertised as an additional theorem.

### 2.3 Finite and compact experiments

I also rechecked the finite likelihood lemma and the compact-net argument. Unit means of the limiting likelihood coordinates are essential. They give uniform integrability of the likelihood vector; a coupling with vanishing expected \(\ell^1\) discrepancy can then be disintegrated in both directions. Sufficiency of the likelihood-vector statistic and regular conditional reconstruction on standard Borel spaces provide the original observation-space kernels. The same coupling serves every parameter index. [S3]

The compact passage is separate. For a fixed finite net, one comparison kernel has error bounded by its net error plus the two continuity moduli. The nearby parameter is used only in the inequality, not supplied to the kernel. The printed moving-boundary estimate gives

\[
 H^2(P_{n,h}^{\otimes n},P_{n,h'}^{\otimes n})
 \le C_Ks^2(1+\log(1/s)),\qquad s=\|h-h'\|\le1.
\]

The Gaussian modulus is evaluated on the identifiable space. First taking the sample-size limit with a fixed net, then refining the net, is the correct order. This supports the stated compact local conclusion under its hypotheses, not uniform equivalence over an unbounded local space or the entire analytic table class. The physical fixed-window and stopped-transfer dependencies have not all been independently rederived here. [S5]

## 3. The local inverse: where the real mathematical content lies

### 3.1 Weighted stationarity and smooth remainders

The inspected weighted half-line construction uses a genuine operator inverse, not just formal power-series manipulation. Choosing \(e^{-\gamma_-}<\rho<1\) makes the two weighted Green-kernel tails summable. Locality of the nonlinear stationarity equations gives an operator perturbation of order \(|u|\), allowing a uniformly invertible Neumann correction on a sufficiently small common endpoint interval. The finite-truncation envelope argument keeps the right-boundary orbit-variation term until its decay has been shown. It does not simply discard an infinite boundary term. [S7]

The smooth finite-jet factorization is also important. Interpolate two anchored graph pairs with the same jets through order \(M\). Their graph difference is \(O(|y|^{M+1})\); the direct variation of a flight is bounded by the corresponding endpoint powers. Weighted orbit decay makes the envelope sum summable, yielding an action difference of order \(O(|u|^{M+1})\). Thus the finite action jet depends only on the finite graph jet, including independence from smooth flat remainders. Analyticity is needed later to identify boundary images, not to justify this finite-order factorization. [S7]

### 3.2 The last-jet block

The multiplicities in the envelope sum are correct: the boundary site contributes once and interior sites twice. The linear half-line orbit therefore gives

\[
 1+2\sum_{k\ge1}e^{-2n\gamma k}=\coth(n\gamma),
 \qquad
 2\mathfrak r_b^n\sum_{k\ge0}e^{-n\gamma(2k+1)}
 =\mathfrak r_b^n\operatorname{csch}(n\gamma).
\]

Because \(\mathfrak r_0\mathfrak r_1=1\), the resulting two-by-two block has determinant one. Homogeneous isolation explains why its coefficient is independent of the new graph jet. The finite triangular recursion is accordingly credible in the inspected construction. Determinant one is not, by itself, a quantitative infinite-order condition-number bound; the manuscript appropriately states fixed-order compact stability instead. [S7]

The independent diagnostics evaluate ninety blocks and leading-curvature inversions. More substantially, they solve four nonlinear 64-flight stationary bridges for asymmetric polynomial contact graphs, then evaluate the envelope coefficients at opposite small endpoints. The stationarity residual is below \(3.1\times10^{-17}\), and the largest symmetrized coefficient discrepancy from the limiting block is below \(4.8\times10^{-7}\) at endpoint magnitude \(10^{-3}\). This finite calculation checks the signs and multiplicities in a nonlinear example. It does not prove the infinite-half-line theorem. [D1]

### 3.3 One signed law really removes the flux amplitude

For an interior density

\[
 f(u,v)=Z^{-1}B(u)B(v)[d-S(u)-S(v)],
\]

the four-density ratio satisfies

\[
 1-\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}
 =\frac{S(u)}{d-S(u)}\frac{S(v)}{d-S(v)}.
\]

At a fixed nonzero anchor, strict convexity gives a strictly positive scalar factor. Taking its positive square root and using the mixed slice recovers the action on both signed sides. There is no differentiation of a degenerate square root at the origin. The density law determines the continuous density version; the theorem does not pretend that finite samples directly provide its point values. [S6]

The fixed-order stability statement uses an interior \(C^M\) norm, positive density denominators, and a positive anchor margin. It does not infer derivative control from total variation. The unknown amplitude, its normalizer, and the separate onset gap are kept logically distinct. These distinctions should be preserved. The algebraic cancellation alone is elementary; its mathematical significance comes from the nonlinear billiard law and the subsequent all-order alternating-contact inverse, not from the ratio identity in isolation.

## 4. Extended scrutiny of global geometric reconstruction

### 4.1 Analytic matching, symmetry, and existence

Equality of complete oriented curvature signatures implies equality of analytic curvature germs. Analytic continuation and uniqueness of the planar Frenet system then identify the corresponding framed curve images by a proper Euclidean symmetry. This establishes why a circle or a finite rotational symmetry creates a genuine matching ambiguity. The paper does not resolve such ambiguity merely by naming a preferred phase. [S8]

The general periodic gluing space classifies admissible placements; that classification is not itself a uniqueness theorem. The later uniqueness criteria add signature-rigid transitions, lattice anchoring, and propagation through a spanning tree. Existence is supplied by realizability of the input data as a billiard table. I found no circular use of the word “admissible” to prove uniqueness or existence in the inspected statements.

### 4.2 Rank-two holonomy

The telescoping identity

\[
 A_0H_cA_0^{-1}=\tau_{L\eta_c}
\]

forces the cycle holonomy to have identity rotational part and identifies its translation vector. For independent marked deck columns \(M\) and recovered holonomy columns \(V\),

\[
 L=VM^{-1},\qquad G=M^{-T}V^TVM^{-1}.
\]

The deck columns need to be independent over the reals; they need not form a unimodular integer basis. The independent diagnostic deliberately uses determinant six. The lattice metric and scale are recovered only after the geometric congruences are uniquely identified. It would be misleading to present the final matrix multiplication as the difficult rigidity theorem. [S8, D1]

**E2.** In `thm:v26-single-offset-global`, item 3 invokes “the signature-rigid cycle and spanning-tree hypotheses of” `thm:v24-lattice-gram-recovery`. That referenced theorem assumes a rank-two anchoring pair and recovers the lattice; it does not state the spanning-tree hypothesis for recovering every obstacle orbit. The appropriate full-table reference is `thm:v24-uncalibrated-periodic-rigidity`, or the item should explicitly state the needed rooted signature-rigid spanning tree reaching every obstacle orbit. The introduction and the full periodic theorem make the intended condition understandable, so this is a repairable hypothesis-navigation error, not a counterexample to the intended conclusion. [S6, S8]

### 4.3 Finite signatures and noisy matching

The finite-signature argument uses compactness twice for different purposes. Analytic nonconstancy supplies a nonvanishing derivative coordinate at each framed point; a finite subcover gives uniform finite-order immersion. A Taylor bound then gives local separation. For pairs away from the diagonal, absence of nontrivial proper symmetries gives separation by some signature coordinate, and a second finite subcover makes the order and separation uniform. These steps address the failure of a scalar curvature value to be locally injective. [S9]

The noisy matching lemma assumes \(C^2\) closeness of the recovered signature curve, not arbitrary \(C^0\) perturbation. Outside-arc separation localizes every minimizer; inside the arc,

\[
 \frac{d^2}{dx^2}\frac12|\widetilde J(x)-y|^2
 =|\widetilde J'(x)|^2+(\widetilde J(x)-y)\cdot\widetilde J''(x)
\]

is uniformly positive. This proves the missing local uniqueness, rather than inferring it from a remote separation margin. Subsequent point–tangent placement and finite graph composition are stable operations. The separate compact inverse modulus is a non-effective continuity statement. It does not make unrestricted analytic continuation well conditioned or produce an effective reconstruction complexity.

### 4.4 A common orientation is not erased pointwise

The reflection construction transports the lattice orientation character and the entire collection of signed laws together. On gluing representatives it sends \(\iota\) to \(J\iota\), \(A_e\) to \(JA_eJ\), and the curve image to its reflection. The deck incidence equations are preserved by \(J\tau_v=\tau_{Jv}J\); the Gram form is unchanged. This supports the common-orientation quotient in the inspected argument. It does not justify independently folding every endpoint sign, and the manuscript expressly distinguishes those operations. The off-model transported-anchor extension is a separate dependency not independently rederived in this round. [S10]

## 5. The two-sided moving-ceiling theorem is more than point-process convergence

I examined the complete proof of `thm:v24-two-sided-deficiency`, including its reverse kernel. The model assumes a first-order ceiling approximation and uniform trace convergence, but also the essential bulk condition

\[
 \sup_{z\in K}\left\|\rho_{n,z}/\rho_{n,0}-1\right\|_\infty\le C_K/k.
\]

The last condition cannot be inferred from mere trace convergence. It is explicitly present. Under it, the conditional bulk laws have squared Hellinger discrepancy \(O(k^{-2})\); up to \(k\) reconstructed bulk observations therefore cost \(O(k^{-1/2})\) in total variation. [S11]

The reference layer \(|k(w-r)|\le R\) is parameter independent. Its probability is \(O(k^{-1})\), so the binomial-to-Poisson error is \(O(k^{-1})\). Regularity of the endpoint boundary gives a corner strip of endpoint area \(O(k^{-1})\); multiplying by residual thickness \(O(k^{-1})\) gives one-record corner mass \(O(k^{-2})\). This is exactly the order needed before multiplying by the number of observations.

The reverse kernel maps Poisson points back by \(r=w-y/k\), adds reference-bulk observations to reach the fixed sample size, and applies a random permutation. The exceptional rules for a nonpositive reconstructed residual time and for too many Poisson points are specified. Conditional iid structure within the original layer and bulk permits coupling with that reconstruction. No unknown local parameter is used by the kernel. Consequently the bound

\[
 \Delta(\mathsf E_{n,K}^R,\mathsf P_K^R)
 \le C_K(\varepsilon_{n,K}+k^{-1/2})
\]

has a coherent proof under the printed hypotheses. This is stronger than convergence of the extracted point process. It is not a fresh certification here of every physical anchored-model premise to which the theorem is subsequently applied. [S11]

As an independent corner check, the diagnostics use

\[
 q_\theta(u,v,r)=\frac{2}{\pi(1+\theta)^2}
 1_{\{0<r<1+\theta-u^2-v^2\}},\qquad \theta=z/k.
\]

For \(w=1-u^2-v^2\), \(U=-1\), and strip radius \(R\), its exact layer probability is

\[
 p_{k,z}=(1+z/k)^{-2}
 \left[\frac{2(R+z)}k+\frac{z^2-R^2}{k^2}\right].
\]

The limiting intensity mass is \(2(R+z)\). The script evaluates the complete intensity variation, including the exterior corner for positive \(z\), rather than only the total mass. The common conditional bulk is exactly parameter independent in this model. This example checks the bookkeeping and is not claimed to be realized by a billiard channel. [D1]

## 6. Physical reconstruction: the observation model must remain explicit

The examined calibration and estimation construction does not conceal an exact contact chart as an observed statistic. It begins with labelled alternating words, planar endpoint positions, physical times, and failures in a common sensor frame for the two types of each channel. Different channels are not supplied as registered. Independent phase-volume preparations and known class bounds are assumptions of the acquisition model, not conclusions inferred from the data. [S12]

A near-onset grid point has excess between \(h\) and \(2h\), where the success probability has a uniform positive lower bound of order \(h^2e^{-j\gamma_+}\). The finite scan therefore yields a charged cap and contact localization of order \(\sqrt h\). The pilot is run at the already selected final flight number \(J\), which controls \(J|\widehat g-g|\) rather than an error at an earlier smaller flight number. This ordering prevents a hidden amplification of the gap error.

The estimator includes onsets in its minimum-distance criterion. Conditional transverse laws at one offset then supply additional separating tests. Compactness gives finitely many bounded Lipschitz tests and a finite template net. Concentration is applied to the uncapped successful sequence, and cap failure is charged afterwards; conditioning on successful cap completion is not used to assert iid marks. These are the correct measurable and probabilistic distinctions. [S12]

The resulting global consistency is an existence theorem with potentially non-effective libraries and inverse moduli. It does not provide a sharp analytic minimax rate. It also does not establish that the half-line inverse is necessary in the richer noiseless position experiment: the introduction explicitly retains a same-experiment direct graph-sampling benchmark. The distinctive inverse content is the determination from coarsened transverse laws, not merely the restriction to long even flight words. This round did not independently rederive the entire direct-position benchmark or every stopped physical transfer. [S13]

## 7. C2 is not closed by a workflow title

The pinned v36 workflow run is `34732106624`. Its job `103656672543`, named `complete-native`, is reported as failed, with `steps: []`, `runner_id: 0`, and an empty runner name. It started at 02:04:09 UTC and completed at 02:04:12 UTC on September 13. The dedicated artifact query returns `total_count: 0`. [C1]

These observations establish no executed build or retained artifact from that run. They do **not** establish a TeX error, identify the cause of the runner failure, or show that the manuscript is mathematically false. A billing or permissions explanation would be speculation on this evidence. A configured source-archive step that never executes is not a source archive. A commit message promising actual native products does not establish that the products exist.

The inherited `VERIFICATION_V35.md` describes a companion build, finite diagnostics, and an isolated vector-chapter check, while expressly distinguishing them from full-main verification. Those author-reported products were not independently retrieved or rebuilt in this round. No v36 build ledger is added in the seven-path comparison. The native main and companion have not been compiled or PDF-inspected by this referee examination. [S1, S2]

**C2 closure requires an actual delivery, not another declaration:** identify the immutable assembled source; build the unabridged native main and companion with every active input and bibliography; retain commands, tool versions, exit status, complete final logs, and the actual source and PDF products with hashes; inspect the products for unresolved references, missing content, and unreadable formulas or layout; record the scope of that inspection. A successful reproducible local build is sufficient—GitHub Actions is not a journal requirement. Any post-build source changes must be distinguished from the tested SHA and assessed for whether a rebuild is necessary.

A hash without its product, a source-presence counter, another shortened fixture, or an isolated chapter PDF does not meet this requirement. Equally, a successful full build would close a delivery issue, not prove all the mathematics or establish originality. This distinction is not negotiable in either direction.

## 8. Assessment of significance at the requested journal level

The potentially substantial contribution is the nonlinear relative long-bridge law combined with an unsymmetrized all-order two-contact inverse from one positive-offset transverse density per type. That is the appropriate center of the article's significance claim. A determinant identity, a standard compact-net lemma, a finite-template consistency argument, or the general appearance of a Poisson boundary experiment would not separately justify the requested publication level. This is an editorial assessment of the presented contribution, not a priority certificate. [S6, S7, S13]

The introduction's distinction from spectral rigidity is appropriate. The primary-source abstract of De Simoi–Kaloshin–Leguil concerns analytic open billiards with stated symmetry and genericity assumptions, while Finamore–Leguil uses an enriched marked length spectrum for finite-horizon Sinai billiards. The manuscript studies a different observation map with signed laws, onsets, and marked incidence data. No subsumption of those results follows simply from having different symmetry hypotheses. [L1, L2, S13]

Likewise, Meister–Reiß already gives Poisson asymptotic equivalence in a nonregular regression problem. The relevant contribution here must be the billiard-specific construction and the exact comparison of retained observation levels, not a claim to have originated a Gaussian/Poisson contrast. The external literature check in this round is limited to primary-source abstracts and metadata; it is not an exhaustive priority audit or a full rereading of those papers. [L3]

The ambitious theorem network deserves a complete mathematical assessment; however, neither accumulated favorable modular reports nor unchanged source files supply one automatically. The present report does not endorse unconditional submission-readiness at any of the four named venues. It also does not support a categorical dismissal of the core as false, impossible, or merely formal. The correct next step is a complete, accurately identified submission with the substantive mathematical distinctions preserved.

## 9. Required response and final disposition

The author should answer C2 with actual native products and an accurate tested-source ledger, repair both current entry points under I1, and correct the hypothesis reference under E2. Preserve the accepted alternative-law mean and centered moment argument, the finite/compact distinction, the singular identifiable quotient, the stated observation spaces, and all charged preparation conventions. The v36 dependency clarification is accepted; another expansion of the theorem list is not requested.

The attached diagnostics were executed with ordinary Python and `python -O`; both succeeded and produced byte-identical JSON. They cover six finite diagnostic families, including a nonlinear stationary-envelope calculation and explicit moving-ceiling corner accounting. They do not test every manuscript source, establish global realizability of the illustrative density models, or constitute native-build evidence. The exact commands, environment, and hashes are in the source audit.

**Final disposition: major revision of the assembled submission; C2 open; I1 regressed; E2 requires a precise reference repair; R1 and the v36 dependency clarification satisfactory in the inspected scope; no newly established fatal mathematical counterexample; no acceptance recommendation.**
