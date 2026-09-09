# Response to the v32 independent referee report

Controlling report: `reviews/a1-english-v32-harsh-independent-2026-09-08/REFEREE_REPORT.md`
at `60c5b116a2c002dfd8056a351a87d7014d8c78e1`.
Reviewed manuscript: `e712437fe13cf29978715d3f16d825eadb450fea`.
Revision: A1 English v33, September 8, 2026.

The report acknowledges the mathematical repairs in v32 but asks for a
stronger structural contribution, a coherent original-model development,
a precise comparison with finite-approximation results, and an executed
original-model certificate and complete build. We address these requests
by adding same-model theorems, preserving the collision classification
and every inherited proof module, and changing the exposition rather
than presenting the generic controller net as the main contribution.
The numbering below groups the five principal objections; it is not a
claim that the report itself used these labels.

## 1. A chosen relative certificate rate is not an intrinsic exponent

Theorem 11.4, `v33/precision.tex`, now proves the arbitrary-precision
statement. For every s > 2, command radius at most M^(-s), stochastic-row
denominator ceil(M^(s+1)), and objective-enclosure width at most M^(-s)
give absolute width at most C_1 M^(-s). The relative bound first divides
by the **full** c Xi_N(M,a), and only then by its M^(-2) floor.
Thus M^(-1) in the inherited corollary is the case s = 3, not a new
statistical exponent. The complete net cardinality is stated explicitly:

    binom(b+M-1,M-1)^(T M C_delta X) (b+1)^(M sum_t Q_t).

An arbitrary absolute tolerance is also given with its parameter choices.
The collision volumes, exact-collision statements and phase law remain
unchanged. The manuscript now distinguishes statistical resolution,
representation size, coefficient evaluation and exhaustive computation.

## 2. A finite history program alone is not the structural theorem

Section 8, `v33/moment_controllers.tex`, works in the original
prescribed-command experiment with one shared latent variable, M labels
charged after every report, and no persistent public seed or history tape.
It eliminates full-history controller variables rather than merely
listing them on a finite grid.

Lemma 8.1 identifies the compact convex one-state implementability body
and its exact support function. A single failure update must be shared
by all underlying raw cells. Corollary 8.2 proves compulsory positive
row overlap, showing why arbitrary stochastic row matrices would admit
controllers that cannot be implemented in this experiment.

Theorem 8.3 proves both directions of the finite-moment realization:
q_(n,i)(t) = P(S_n=i | t) obeys a closed cell-polynomial recursion, and
every feasible set of one-step coefficients is realized by one common
controller. Conditional-centroid decoding gives an **attained exact
minimum of the maximum of mean checkpoint risks**. Zero state occupancy
is included by a continuous perspective extension. The optimization uses
T M^2 J one-step entries and at most M binom(n+J-1,J-1) formal occupancy
coefficients at time n. Prior-dependent coefficients use cell moments
of degree at most N. No controller variable is indexed by a full history
or a command grid. Evaluating the controller-independent baseline may
still be costly; no efficient global nonconvex solver is asserted.

Theorem 8.6 removes fresh private transition randomization while preserving
the entire mean-risk vector under atomless command laws. The abstract
finite-moment purification argument is classical and explicitly attributed
to Dvoretzky, Wald and Wolfowitz; its application preserves the coupled
failure coefficients, hence every conditional state law. The prior itself
may be singular. Theorem 8.7 gives polyhedral failure regions and command-
independent accepted-report updates for a globally optimal scalarized
risk. It does not infer a convex minimax identity. Theorem 8.8 proves
compact transfer of optimal controller laws through collisions on the
same coefficient domain and connects the exact value to the retained
full collision profile. These are additional original-model structural
claims, not consequences of the regenerative example.

## 3. The comparison must be at theorem and information-resource level

Section 13, `v33/comparison.tex`, compares the precise hypotheses and
conclusions of Saldi--Yuksel--Linder (JMAA 2016, Assumption 3.1 and
Theorem 3.2), their decentralized finite-model paper (arXiv:1511.04657,
Theorems 4, 5 and 11), and Yuksel--Linder (SIAM JCO 2012, Theorems 3.4
and 6.2). `MODEL_AND_COMPARISON_V33.md` provides the corresponding
resource ledger.

We do not characterize team theory as ignoring information constraints.
The distinction is the particular requirement that all later decisions
factor through the same retained label. We also do not infer total-
variation convergence by replacing a continuous command law with point
masses. The proof first compares laws on the same command space, replacing
only likelihoods by cellwise-constant likelihoods, and only afterwards
averages within cells. This preserves the domain of Borel transitions.
Finite-controller optimization and finite-action purification are credited
to their classical sources. The new claim is the exact experiment-specific
implementability body, finite-moment recursion and its realization results,
in conjunction with the retained attainable collision geometry.

## 4. Separate protocols without deleting their mathematics

The main article now follows the original experiment from exact attainable
information through collision-uniform compression to exact common-controller
realization, approximation and an evaluated continuous-command instance.
It has 35 pages. The complete companion has 159 pages and retains all
graph, occupation, regenerative, structural, exact-kernel and effective
proofs with their original hypotheses. The graph modules are unchanged;
their batch charging is not used to prove a per-report theorem.

The inherited v32 new-results chapter is split exactly at its delayed-use
section. Concatenating the two new files reproduces all 35,187 original
bytes. The finite compatibility and approximation proofs remain in the
main article; the block-charged delayed-use theorem remains complete in
the companion. Original entrypoints and the entire native v32 source
tree remain available. The editorial consolidation does not remove
collision strata, reduce the horizon, grant an oracle decoder, change the
mean/worst-history quantifiers, or substitute regeneration for a shared
latent parameter. The state-controlled approximation corollary remains
explicitly a separate acquisition decision problem.

## 5. Execute a same-model certificate and build both complete volumes

Section 12 uses uniform prior on [0,1], positive affine detector cells,
the actual continuous command cube [9/20,11/20]^2, N = 2, M = 2, and
a complete two-element attainable failure-factor query basis. Compression
is charged after the acquisition report. There is no persistent public
seed. Theorem 12.1 solves the global problem over **all Borel stochastic
two-label encoders**, not only over a proposed finite set. Its proof bounds
binary explained variance for the full acquired law, retaining the report
evidence and both atoms. The optimal controller and both decoder tables
are explicit.

Corollary 12.2 gives a rational geometric-tail enclosure. The executed
`v33/certify_instance.py` uses Fraction arithmetic and checks not disabled
by Python optimization. Normal execution and `python -O` produced identical
JSON. At K = 5 the exact risk is enclosed by

    L = 18108150189130829 / 12454041600000000000000
    U = 150901251576091 / 103783680000000000000
    U - L = 1 / 136857600000000000000.

The interval width is approximately 7.31e-21. Its upper certificate is
implemented by retaining whether accepted cell 1 was reported. Its lower
coverage is the analytical all-encoder argument in Theorem 12.1, not a
sampling claim. This is an executed continuum-instance certificate; it is
not an execution of the general enormous controller net or a formal proof-
assistant check of the theorem.

`v33/build_revision.py` actually compiled the complete main and companion
volumes in three cross-reference cycles (six successful invocations),
without shell escape. All 79 active TeX sources are hashed in the build
receipt. Final logs have no unresolved references or citations, duplicate
labels, rerun warning or overfull boxes. All 194 pages were visually
inspected at contact-sheet scale, with selected main pages enlarged.
The full logs and PDFs accompany the conversation review package; the
repository contains the build code, source/PDF hash receipt and exact
certificate. This is a local execution record, not a GitHub Actions pass.

## Request for the next review

The next substantive audit should test the necessity and sufficiency of
the common-failure implementability body, the conditional-state factorization
and zero-occupancy limit in Theorem 8.3, the precise mean-risk scope of
purification, and the all-encoder upper-tail argument in Theorem 12.1.
The new claims are offered for independent mathematical scrutiny. Neither
successful compilation nor exact arithmetic establishes journal suitability
or substitutes for that scrutiny.
