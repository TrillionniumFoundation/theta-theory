# Response to the A2 v13 referee reports

**Revised manuscript:** Qian Qi, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*, A2 v14, 10 September 2026.

**Primary report:** `reviews/a2-v13-independent-harsh-normal-form-2026-09-10/REFEREE_REPORT.md`, commit `b3f0ad5843782c221651c9189fc156d20865cab1`, reviewing author commit `0e54099f079232df233316ae6fe7986fc51b7ea1`. The analytic benchmark at that review commit is treated as part of R13-1. The earlier same-version report at `f29d8f96e87bf46db2ffbe8217caa09563c5e536` is also addressed below. We do not mistake either author-requested AI-assisted report for an editorial decision.

The revision retains the complete English manuscript and all its auxiliary proofs. It adds a focused forward comparison and an intrinsic geometric characterization of the existing boundary amplitude. It also repairs the abstract's family quantifier without changing the hypotheses or conclusion of the proved finite-family observation theorem. The 218 reviewed formal statement/proof blocks remain byte-identical and active. Their new numbering is caused by inserting Section 8, not by replacing their content.

## R13-1. Analytic normal forms, physical projection, and the smooth contribution

We agree that the nearest forward comparison is the local analytic hyperbolic mechanism. The distinction between selected probabilities and a global marked or Laplace spectrum does not settle that comparison. The revised introduction has a separate subsection on hyperbolic coordinates and the boundary measure; the complete comparison is in `article/16_hyperbolic_coordinates.tex`.

### 1. A complete, explicitly attributed analytic benchmark

Proposition 8.1 (`prop:v14-normal-form`) takes the normal form and the two canonical endpoint charts as hypotheses. Its proof includes the mixed-boundary contraction, the derivative estimates after relative normalization, the physical inverse map on a fixed inner box, and the action limit obtained from first variations. In its notation,

\[
I=st\Delta(I)^n,\qquad
T_n=\frac{\Delta(I)^n}{1-nI\Delta'(I)/\Delta(I)},\qquad
J_n=\left|\frac{T_n}{\det D\Phi_n}\right|.
\]

The last identity is essential. We do not identify the canonical mixed derivative with a physical configuration observation. The normalized factors are inverse projection Jacobians along the invariant axes. The estimates include each fixed mixed parameter derivative only when the functions and charts themselves form the supplied uniformly smooth family stated in the proposition.

The contracting eigenvalue is the two-flight return eigenvalue, `lambda = exp(-2 gamma)`, not the one-flight abbreviation. The billiard specialization uses the stable and unstable slopes `-a_b` and `a_b` and canonicity to obtain the exact identity

\[
J_n(0,0)=\frac{2a_b\lambda^n}{1-\lambda^{2n}}
        =\frac{a_b}{\sinh(2n\gamma)}.
\]

Thus the comparison agrees with the exact Jacobi normalization, not only its leading exponential order. Where both constructions apply, uniqueness of the normalized limit identifies the analytic projection factors with the half-line determinant factors.

The proof and acknowledgment credit the referee's companion derivation. De Simoi--Kaloshin--Leguil is cited for the local analytic normal-form statement it recalls, not for a physical probability theorem that the cited source does not state. The local theorem's hypotheses are explicitly separated from the symmetry assumptions in its global geometric inverse theorem.

### 2. A geometric identification in the actual smooth class

A comparison alone would leave the smooth amplitude's geometric meaning implicit. Theorem 8.2 (`thm:v14-intrinsic-density`) gives that meaning without postulating a smooth two-dimensional normalizing chart.

Let `phi_b` be the first physical hit of the stable half-line, and let `r_b = sqrt(c_b/c_{1-b}) exp(-gamma)`. The theorem proves the exact cocycle

\[
B_{1-b}(\varphi_b(u))\varphi_b'(u)=r_bB_b(u).
\]

The argument is not an appeal to a normal-form existence theorem. First, the half-line tail identity gives its stationary first-hit equation and its positive implicit derivative. Next, exact finite concatenation gives

\[
-W_{j+1,b,12}
 =\frac{-\ell_{b,12}}{\ell_{b,22}+W_{j,1-b,11}}
                          [-W_{j,1-b,12}].
\]

The finite reference ratio converges to `1/r_b`. Dividing by the exact reference twist before passing to the existing relative limit gives the cocycle. This avoids an absolute-error estimate divided by an exponentially small flux.

Consequently,

\[
\zeta_b(u)=\int_0^u B_b(x)\,dx,
\qquad
\zeta_{1-b}\circ\varphi_b=r_b\zeta_b,
\qquad
\zeta_b\circ R_b=\lambda\zeta_b.
\]

The proof establishes uniqueness among normalized differentiable scalar linearizers and proves the fixed-order mixed derivative limits

\[
\lambda^{-n}R_b^n\longrightarrow\zeta_b,
\qquad
\lambda^{-n}(R_b^n)'\longrightarrow B_b
\]

with an exponential margin uniform on the stated compact smooth families. Parameter derivatives of the multiplier introduce polynomial factors in `n`; the proof explicitly absorbs them in a fixed strict exponential margin.

This theorem is downstream of the already proved half-line factorization. It interprets and characterizes that amplitude; it is not presented as a circular replacement proof of relative factorization. The determinant construction remains active and unchanged.

### 3. What the complete invariant measures

Corollary 8.3 (`cor:v14-width`) pushes the measure into the intrinsic coordinate: `B_b(u) du = d zeta_b(u)`. The limiting integral becomes an ordinary sublevel integral for `S_b composed with zeta_b^{-1}`. Its normalized sublevel width is

\[
\mathcal W_b(E)
 =\sqrt{\frac{a_b}{2}}
    \big[\zeta_b(u_{b,+}(E))-\zeta_b(u_{b,-}(E))\big]
 =\int_0^E x^{-1/2}\mathcal V_b(x)\,dx.
\]

The existing Volterra inverse determines this entire normalized width from the even law, not merely its formal Taylor series. The separate curvature scale is unnecessary for the normalized width; it is needed to undo that normalization. For two even contact graphs the two inverse branches are related by reflection. For general contacts the width combines the branches, and we do not infer unrestricted asymmetric graph reconstruction from their difference.

The dependency is explicit: the prior compatibility theorem uses only the half-line representation and Volterra uniqueness, not the new width corollary. The corollary therefore does not introduce a logical cycle.

### 4. Precise overlap and remainder

The analytic benchmark explains relative factorization in its chart class. Physical projection, positive endpoint Hessians, and the existing fixed-domain integration argument connect that calculation to analytic billiard probabilities. An odd-flight analytic comparison can compose one more physical flight. Neither odd parity nor the absence of global finite horizon is claimed as an obstruction to this local analytic mechanism.

The main physical theorem instead starts from arbitrary smooth obstacle graphs with geometric margins. It supplies, rather than assumes, the half-line and finite-bridge contractions, the normalized trace-ideal estimates, and mixed parameter/offset bounds on a common closed onset collar. The conditional chart clause states what a uniform normal-form route would require; we neither assert that such a route is impossible nor claim an exhaustive priority theorem about smooth normal forms.

The revised contribution statement is the joint chain from smooth physical records to a geometrically identified branch measure, its complete normalized stable-action width, the independent-contact inverse and physical finite-jet image, and a charged finite-preparation experiment. A forward normal form by itself reconstructs none of those observation inputs or inverse outputs. The regular parametric finite-family rate and the sufficient full-profile rate retain their stated roles. We do not relabel them as new minimax principles.

This is a focused mathematical response to the closest forward comparison, not an unrelated expansion of the theorem list. Whether the resulting package meets a particular journal's significance threshold remains for the subsequent referee and editors to assess.

## R13-2. The family quantifier in the abstract

The phrase “every fixed finite-dimensional family” has been replaced by:

> Each locally full-rank physical finite-jet family constructed here is observable through positive windows at two flights.

This is the hypothesis actually proved in Theorem 12.3 (`thm:v13-two-flight-observation`), based on Theorem 11.1 (`thm:v12-realization`) and a sufficiently small coordinate neighborhood. The theorem and its proof are unchanged.

The report's distant translating obstacle is a valid reason not to quantify over arbitrary table parameters: the selected local channel experiment need not observe a parameter that changes only a remote obstacle while preserving the free area and the channel. We accept that correction. It does not remove any theorem, proof, physical finite-jet family, or full smooth-profile result from the paper. It makes the abstract accurately describe the demonstrated rank condition rather than promising an unproved global identification property.

## Earlier same-v13 report: C13-1 and C13-2

**C13-1, exact-germ normalization.** Immediately after `eq:v13-finite-law`, the revised two-flight section specifies that the inverse takes normalized germs. A supplied exact unnormalized germ has leading coefficient

\[
\alpha_2=\lim_{d\downarrow0}p_b(d)/d^2
       =[2A\sinh(2\gamma)]^{-1},\qquad
G_b(d)=p_b(d)/(\alpha_2d^2).
\]

This is an exact-data observation, not an uncharged estimate from finitely many bits. The finite-family experiment supplies its fixed free area, whereas the general unknown-normalization experiment retains the separately charged smooth-class pilot. No derivative or zero-offset observation is added to either sampling experiment.

**C13-2, repository navigation.** The repository README on the new revision branch adds the current A2 source and the frozen report pointer while preserving its existing A1/workstream content. The manuscript README gives a compiled reading map, reproduction commands and the distinction between an author revision and a review decision.

## Preservation, build, and verification

All 52 prior active input files remain included; the new section gives 53 active inputs. The 218 reviewed formal statement/proof blocks are preserved byte-for-byte in the active manuscript. The new proposition, theorem, corollary and their proofs bring the active count to 224. Changed front matter and metadata are archived separately under `history/v13-reviewed/`. The new native manuscript tree is built on the complete v13 tree, so inactive historical directories and tools are also retained. The old manuscript and review paths remain unchanged.

The full main manuscript compiles to 129 pages and the unchanged two-collision companion to 7 pages. The companion is built first for external references. The final local log has no undefined references or citations, duplicate-label warnings, or overfull boxes. Underfull spacing notices in inherited material are retained in the logs; they are not silently described as mathematical errors.

Three explicit diagnostic suites were run both ordinarily and with `python -O`, with byte-identical paired JSON outputs: the retained author's v13 suite, the latest independent referee suite, and the new v14 cocycle/source suite. The last uses exact rational arithmetic on specified synthetic pullbacks of quadratic generating actions; it does not pretend those test actions are Euclidean billiard realizations. It checks the nonlinear implicit derivative, first-flight cocycle, two-type return, exact finite normalization, iterate remainders, sublevel pushforward, and negative controls. The final counts and hashes are recorded in `VERIFICATION.json`.

These are algebraic and source checks, not a formal proof certificate. No remote CI run, physical trajectory simulation, exhaustive new audit of every inherited appendix theorem, or optimal full-profile sampling exponent is claimed. The new analytic and smooth arguments are supplied as complete mathematical proofs for the next independent review.
