# External final top-four referee report on A2 v43

**Manuscript:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v43-journal-package-2026-10-04`  
**Equivalent referee-copy alias:** `revision/a2-v43-referee-copy-2026-10-04`  
**Reviewed commit:** `4557df22f5c72bc80943690ecd6c2e39de3734ab`  
**Reviewed repository tree:** `39b947dbdf40a7019b0c31c1aca8d83372f661cc`  
**Controlling preceding report:** `74787c9c353b72983fe1bb43af467e31d3eb0f2a`  
**Reviewed v42 author source:** `fffc85d4da8c8ee6369833369d564b1cffabc63d`  
**Manuscript directory:** `papers/A2-v43-journal-package`  
**Date:** 4 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision, formal proof certificate, apparatus validation, or independent human specialist report.

## 1. Recommendation

**Recommendation: accept. I request no further author-side mathematical or presentational revision.**

The editor should nevertheless complete the independent human specialist confirmation already identified in the v42 report before final publication. That is an editorial verification step, not an additional theorem or manuscript change, and the present AI-assisted report does not purport to satisfy it.

The controlling v42 report gave a minor-revision recommendation and stated that acceptance would be appropriate once four author-side corrections were made and the editor obtained an independent specialist check of five delicate proof tracks. Version 43 closes all four author-side requests. It promotes the signed-record moment-acquisition bound consistently, removes journal-facing version ambiguity, separates exact and finite data models and norms, and freezes the article/companion interface as one exact-SHA package. The authors also state, correctly and prominently, that no independent human specialist review has been performed.

I found no mathematical regression in the transition from v42 to v43. The exact two-field theorem and its singular-support and nonsmooth-curvature foundations are byte-identical to the reviewed v42 source. All 113 v42 proof bodies and all 467 v42 labels remain active. The default finite-law budget is presented first, the larger all-node acquisition remains available as a retained alternative, and the dependency graph is noncircular. The exact-source workflow successfully builds and qualifies both the 47-page article and the 86-page companion from the reviewed commit.

The favorable mathematical assessment of v42 therefore stands. The principal result is sufficiently economical and broad for the requested benchmark: two fixed opposite whole-plane collision fields at one positive command length identify an arbitrary locally finite separated configuration of strictly convex planar obstacles and an arbitrary compact launch probability, including atomic and singular laws, up to the unavoidable common translation. The proof uses a collision-specific support cancellation and a signed surface-area Jordan decomposition, not merely generic deconvolution. The full law, complete ambiguity, all finite-length responses, and full translation-period group follow. The finite theory, while intentionally nonsharp, demonstrates implementability and now has a clearly stated default moment-acquisition mechanism.

## 2. Frozen source and review scope

The author and referee-copy branches resolve to the same commit

`4557df22f5c72bc80943690ecd6c2e39de3734ab`

with repository tree

`39b947dbdf40a7019b0c31c1aca8d83372f661cc`.

The commit descends directly from the final v42 review head

`74787c9c353b72983fe1bb43af467e31d3eb0f2a`,

which reviewed v42 author commit

`fffc85d4da8c8ee6369833369d564b1cffabc63d`.

No A2 revision branch later than v43 existed when this report was frozen. The present review branch starts directly from the v43 author head and adds files only under

`reviews/a2-v43-external-top4-final-rereview-2026-10-04/`.

No manuscript source, author revision branch, workflow, prior report, retained paper, or unrelated path is modified.

The journal submission is a paired package:

1. a 47-page primary article containing the exact two-field theorem, finite geometry and law recovery, prediction results, continuum foundations, the finite-detail appendices, and the protected signed-record acquisition theorem;
2. an 86-page technical companion containing the earlier localized, stationary, calibration, period-recognition, directional-germ, and benchmark results.

The exact theorem is self-contained in the primary. The finite interface with the companion is explicit and frozen.

## 3. Closure of the v42 minor-revision requests

### 3.1 The best moment-acquisition statement is now the default

The v42 report asked that the protected signed-record bound replace the older all-node construction as the default current statement, without deleting the latter.

Version 43 does this consistently. The abstract states that, conditional on a protected complete component, all moments through degree `n` at tolerance `tau` are acquired with

\[
 C\tau^{-2}\log\frac{C(n+1)}{\delta}
\]

attempted bits using shared signed two-bit records. The introduction, finite-law theorem, resource summary, proof ledger, and response to referees all present

\[
 N\le N_{\rm geom}(c a_m,\delta/2)
       +C a_m^{-2}\log\frac{Cm}{\delta}
\]

as the default joint budget. The larger bound

\[
 N\le N_{\rm geom}(c a_m,\delta/2)
       +C m^2a_m^{-4}\log\frac{Cm}{a_m\delta}
\]

is explicitly labelled the retained deterministic all-node alternative.

The proof architecture is sound. The retained proof establishes the common positive-factor reconstruction and the deterministic alternative. The protected linear-moment theorem supplies a different moment input, and a subsequent corollary combines that input with the already established common factor. The improved bound is not used as a premise for itself.

### 3.2 Journal-facing front matter is current and unambiguous

The unprefixed `PROOF_LEDGER.md`, `LITERATURE_AUDIT.md`, `RESPONSE_TO_REFEREES.md`, `SUBMISSION_MAP.md`, and `SOURCE_AUDIT.md` all describe v43. Superseded v41 and v42 front matter is retained under explicit provenance paths and excluded from the journal-facing archive.

There is one current proof/dependency ledger and one current literature audit. The latter rechecks the version-sensitive unknown-noise erratum and the accepted Bernoulli manuscript numbering without upgrading any priority claim. I found no stale journal-facing version designation.

### 3.3 Exact and finite statements are visually separated

The revised abstract uses separate exact and finite paragraphs. The introduction contains an explicit data/hypothesis/conclusion table distinguishing:

- two exact whole-plane spatial fields from finitely sampled bits;
- exact identification of an arbitrary compact probability from finite `W_1` recovery under quantitative geometry;
- local spatial `L^1` response prediction from uniform prediction under a known `BV` density bound;
- exact period recovery without a periodicity premise from uniform finite period decisions using a positive whole-patch margin.

The finite-configuration alternative is separately stated under a complete protected-aperture assumption and does not invoke a period margin. Exact Fourier uniqueness is not represented as finite stable division through transform zeros. These distinctions are now sufficiently prominent.

### 3.4 The article/companion interface is frozen as one package

`JOURNAL_INTERFACE.json` pins the exact-section files, the finite supplement interface, cross-document label owners, the article and companion PDF names, and an acyclic dependency graph. The primary exact theorem has no mathematical dependency on the companion. The finite theorem imports a finite list of explicitly restated auxiliary results through the frozen interface.

The journal archive contains both PDFs and the complete current source closures. Historical front matter and qualification tools are excluded from the journal-facing archive. The standalone build does not patch or transform manuscript sources. The exact-SHA workflow checks duplicate labels, stale ledgers, missing companion files, changed proof bodies, a regressed default exponent, merged data models, circular dependencies, and fabricated human-review claims.

### 3.5 Independent specialist confirmation remains an editorial item

The manuscript does not claim that the requested independent human specialist check has occurred. `SPECIALIST_REVIEW_BRIEF.md` begins with “Status: not performed” and identifies the five requested tracks:

1. singular-law supports and almost-everywhere representatives;
2. nonsmooth support-measure atoms and Jordan decomposition;
3. finite tangential geometry and signed chord extraction;
4. protected first-exit signed records and arbitrary-law quadrature;
5. positive factor fitting and transportation conditioning.

This is the correct status. It does not justify a further author revision. I recommend that the editor commission or document that check before issuing final acceptance. The present report is not a substitute for it.

## 4. Mathematical regression audit

The v43 changes are principally statement promotion, organization, source packaging, and literature clarification. The load-bearing exact sources

- `core/21_two_field_rigidity.tex`;
- `core/24_measure_support.tex`;
- `core/25_nonsmooth_curvature.tex`;
- `core/29_supplement_interface.tex`

remain frozen at the reviewed v42 content hashes. Every v42 proof body is retained byte-for-byte.

I rechecked the parts most exposed to the v43 presentation changes.

### 4.1 Protected first-exit identity

For a recovered expanded component `P`, the outer rational polygon `Q` satisfies

\[
 P\subset Q\subset P+\rho\overline B,
 \qquad \rho+t<g.
\]

The first arithmetic-progression exit from `Q` lies outside `P`, within `rho+t` of `P`, and therefore in no other expanded component. Telescoping the physical endpoint increments gives the exact linear occupation identity used by the signed-record estimator. The stopping index is determined from rational polygon membership, not from observed bits.

### 4.2 Signed two-bit records

Each block selects a grid point `X` and an index `L`, obtains two fresh independent collision bits, and records

\[
 Z=K\mathbf1_{\{L<m_Q(X)\}}(Y_--Y_+).
\]

Conditional expectation over the bits and the uniform index gives the desired occupation value. Negative records are essential and are not clipped. Every block costs two attempted bits, including inactive indices, misses, and solid starts. The same records are reweighted for all requested moments, so the observation count is not multiplied by the number of monomials.

### 4.3 Positive factor fitting and noncircular dependency

The moment stage estimates the occupation-factor moments. Geometry supplies a rational approximation of the uniform-obstacle factor. The positive finite programme fits a probability measure, and the triangular moment comparison plus polynomial approximation yields `W_1` control. The default signed-record acquisition and the all-node acquisition feed the same factor mechanism. The dependency graph recorded in the package is acyclic.

I found no sign, index, conditioning, or resource-accounting regression in these passages.

## 5. Mathematical and editorial significance

I retain the v42 significance assessment. The exact theorem is not merely a repackaging of a passive deconvolution result. The data are two ordered collision fields generated by opposite commands. A finite endpoint identity recovers occupation. Three matched supports cancel the unknown footprint and leave the obstacle support minus a contact chord. The signed surface-area measure then separates a nonatomic strictly convex obstacle contribution from two negative chord atoms. This recovers geometry before Fourier uniqueness is used to identify the arbitrary compact launch probability.

The command alphabet is finite and fixed. The law may be atomic, singular continuous, or lower-dimensional. The obstacle family may be infinite and need not be periodic. The ambiguity is completely classified. This combination is sufficiently economical, general, and collision-specific for publication-level consideration at the requested journals.

The finite law theorem remains a sufficient rather than minimax construction, and its exponentially small moment tolerance makes the uniform joint bound exponential. That limitation is stated correctly and does not diminish the exact theorem carrying the editorial decision.

## 6. Literature positioning

The current literature audit gives theorem-level comparisons to planar covariogram uniqueness and factorization, blind-probe morphology, compact deconvolution, unknown-noise identification, signed support measures, and transportation from moments. It correctly distinguishes those data models and ambiguity classes from the ordered collision fields here.

The version-sensitive checks are responsible. The Gassiat--Le Corff--Lehericy erratum is described as affecting a quantitative contrast argument and associated rate conditions, not as invalidating the exact identification comparison. The accepted Bernoulli manuscript is cited with its accepted-version numbering. No new exhaustive priority claim is made.

I found no literature issue requiring another author revision.

## 7. Source qualification and independent diagnostics

The exact-head workflow is:

- run ID: `37210951299`;
- workflow: `A2 v43 exact-source article and companion qualification`;
- head SHA: `4557df22f5c72bc80943690ecd6c2e39de3734ab`;
- status: `completed`;
- conclusion: `success`.

Exact checkout, pre-install source capture, environment installation, source/proof preservation, normal and optimized diagnostics, both PDF builds, interface stabilization, and evidence archiving all succeeded.

The uploaded artifact is:

- artifact ID: `11306587365`;
- digest: `sha256:3170908bc2be6eed37007e5b128d2d2a65def8e8f2eaa107a28d4d834992f22e`.

The receipt records:

- exact commit qualified: true;
- primary: 47 pages, SHA-256 `fdce6a7fa0c37e8c9b0840180071a26ecabfa03a6c558c2d9e98e759b82d6909`;
- companion: 86 pages, SHA-256 `02d6cf960d9d13ec5ae4d4cf239c37ab41d114e6ab4b9dce96fb4a43c0d90d8d`;
- frozen journal package: 61 members, SHA-256 `d7e59b52aadafe74f4a27daf5b31e8dc0db1ad8a7bfbd9c951558238d26a5fba`;
- 469 active labels, 116 formal result blocks, and 113 proof bodies;
- all 467 v42 labels retained and all 113 v42 proof bodies byte-identical;
- 661,187 retained v41 finite checks and 73,933 retained v42 checks;
- 17 v43 negative contract tests, all passed;
- no final TeX findings;
- formal proof certificate: false;
- physical sensor executed: false;
- independent human specialist review: false.

The accompanying `verify_review.py` imports no author code and uses only the Python standard library. Ordinary and optimized executions are byte-identical at SHA-256

`1af7568f3e209fba4c16c683cd3e72b7cea6d56b35b8018270966ad946b9da1b`.

It records 140,888 successful checks of finite exact models for:

- the pointwise endpoint identity and finite prefix inverse;
- prefix stability under forcing perturbations;
- protected first exits and telescoping;
- signed two-bit unbiasedness, including negative active records;
- shared-record moment scaling;
- triangular factor-moment recovery and factorial conditioning;
- the default-versus-all-node resource hierarchy;
- acyclicity of the finite-law dependency graph.

These checks are supporting finite evidence only. They are not continuum proof certification, a TeX build, a physical sensor test, a human specialist report, or a journal decision.

## 8. Final verdict

**Author-side response to the v42 minor revision:** complete.

**Mathematical regression review:** no fatal counterexample or new gap found; the reviewed exact proofs and all reviewed proof bodies are preserved.

**Journal package:** exact-SHA qualified, paired article and companion frozen, current front matter unambiguous, and the default finite budget consistently promoted.

**Remaining process item:** the editor should obtain the already requested independent human specialist confirmation of the five load-bearing proof tracks. No further author-side revision is requested for that purpose.

**Recommendation: accept at the Annals / Acta / Inventiones / JAMS benchmark, subject only to the editor's independent specialist verification before final publication.**
