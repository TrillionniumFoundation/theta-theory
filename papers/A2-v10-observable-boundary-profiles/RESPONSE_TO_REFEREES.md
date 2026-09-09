# Response to the completed-v9 referee report

**Manuscript:** *Relative boundary laws and inverse experiments in dispersing billiards*, Qian Qi.  
**Revision:** v10, September 10, 2026.  
**Controlling report:** `reviews/a2-v9-nonlinear-compatibility-harsh-2026-09-10/REFEREE_REPORT.md`, commit `b756f4851669e34c7074ba61b5bcf48689756406`.  
**Reviewed author source:** `33ef794a398b23015651482e93be7667c08d6fad`.

The response concerns the completed nonlinear-boundary v9, not the separate initialization at `12a3f50e143cc4951d8e9bea888206d965b90e51`. The report's positive findings about the physical relative law, nonlinear compatibility, full smooth-profile inverse and envelope comparison are retained as the starting point. We do not treat the editorial significance reservation as a newly discovered contradiction, nor regard further revision as an acceptance decision.

## E1. The invariant, its significance and an additional observable consequence

**Revision locations:** Section 1; Theorem 11.1 and Corollary 11.2; the end of Section 22. Sources `article/01_introduction.tex`, `article/25_profile_acquisition.tex`, `article/72_observable_comparison.tex`.

The introduction now identifies the main invariant as a normalized weighted pushforward of the one-sided stationary action and determinant amplitude into energy coordinates. The physical relative theorem places this full-function object, rather than only the gap and linear multiplier, in a scalar collision experiment. It also specifies exactly what information is lost by the two-branch symmetrization. Classical Schur, Abel and Volterra arguments are not presented as new mechanisms.

The additional result is not another rank-one reformulation. Theorem 11.1 constructs a measurable regularized estimator of both full profiles from finitely many independent physical preparations that return a selected-event bit. Its hypothesis is the existing relative closed-collar C3 bound, with uniform smoothness and positivity constants on the profile class. The gap, area, multiplier and facing patch labels are supplied. Both orientations are observed at one chosen even flight number on a grid of positive offsets. All failures are recorded and charged.

For a grid spacing h, even flight number j, scalar accuracy t, dictionary tolerance delta, and a bounded C^{m-1,1} profile class with m >= 4, the theorem gives, with confidence 1-eta,

    max_b ||Vhat_b - V_b||_infinity
       <= C (h^(m-3) + tau^j + t h^(-3) + delta).

The proof distinguishes a C3 bridge error from unrestricted scalar noise: stable interpolation does not multiply the former by h^(-3). The first cell uses positive nodes and controlled extrapolation to zero, so no onset value is silently supplied as a noisy observation. The finite-dictionary minimum-distance estimator is measurable by an explicit tie rule. Compactness provides the dictionary; computation and dictionary cardinality are not included in the preparation count.

The per-node allocation is derived from the exact physical Bernoulli variance and an exponential-moment inequality. Summing the nonuniform allocation, rather than charging every node at the smallest offset's cost, gives

    N_total <= C epsilon^[-2-8/(m-3)-gamma/|log tau|]
                    log[C/(eta epsilon)].

This is a sufficient upper bound, not an optimality assertion. The factor depending on gamma/|log tau| explicitly pays for increasing the bridge length to suppress bias. No identity between tau and exp(-gamma) is assumed. The predicted odd limiting law follows from the two recovered profiles; it is not needed to construct them.

The new theorem responds directly to the report's Section 7.3: the limiting profile is no longer treated as an exactly and freely observed function. We credit that variance observation. The physical forward theorem, regularization, binary concentration and bridge-length choice are separate proof steps. This makes a concrete case for the invariant's experimental content without changing to the unrelated four-window experiment. We do not assert that this advance compels a particular venue decision.

## E2. The closest deautoconvolution comparison

**Revision locations:** Section 10, `article/22_deautoconvolution.tex`; bibliography entries Dai–Lamm and Hofmann–Werner–Deng; `LITERATURE_VERIFICATION.md`.

The focused comparison records five distinctions: the kernel class, available collar, origin normalization, observation topology and dynamical origin. Here k(x)=x^(-1/2)V(x) is locally integrable but not square integrable at zero. The observed scalar law includes residual-time integration, and differentiating d^2 F twice gives the finite-collar autoconvolution. The fixed leading singularity normalizes the Abel reduction; the inverse bound uses a C3 law norm.

Dai–Lamm are credited for causal local regularization of nonlinear inverse autoconvolution. Hofmann–Werner–Deng are credited for the L2 uniqueness and ill-posedness framework, including the significance of origin support in their limited-data setting. We neither invoke their detailed theorems outside their hypotheses nor use their L2 ill-posedness to contradict the different topology here. The new finite-dictionary estimator is established in the manuscript, not attributed as an application of an uninspected theorem from those papers.

The verification log identifies the primary records inspected. Dai–Lamm's publisher abstract and bibliographic record were accessible; a full-text inspection of that paper is not claimed. The cited Hofmann–Werner–Deng version is explicitly the inspected arXiv v1. This is a focused comparison, not an exhaustive priority determination.

## E3. The observation models and their information sets

**Revision locations:** Section 1 information table and following explanation; Section 11's opening, hypotheses and concluding interpretation.

The table lists observed data, supplied information, recovered object and norm or loss. It separates the following settings without transferring assumptions between them.

The long-bridge deterministic inverse observes the two normalized oriented even laws in a differentiated norm. The new acquisition theorem instead observes their finite physical binary reports and adds a quantitative smoothness class for regularization. Both require the same calibration and labels. The new theorem makes no derivative observations and targets the uniform norm of the full weighted profiles.

The exact analytic physical-family result observes four unlabelled fixed-window means. Its inverse concerns an unknown gap and coalescing curvature coordinates. Its bounded-flight joint minimax loss is not the profile loss, and it is not evidence that the normalizers and labels supplied in the long-bridge theorem have been removed there.

The positive Cm remainder envelope observes binary reports with unknown nuisance functions and requires the printed strict interior margin. Its minimax alternatives are not asserted to be exact finite-offset billiard probabilities. Its different smoothness-dependent cost is not a lower bound for the general physical profile experiment.

All individual earlier theorems and their necessary qualifications remain intact. Section 11 adds an observation theorem in the same labelled long-bridge model, rather than using a theorem from another model to claim profile acquisition.

## E4. Organization, preservation and reconstruction versus validation

**Revision locations:** main article Parts I–III; Section 1 dependency narrative; the final paragraph of Section 9; current README and `history/README.md`.

Part I treats the relative physical law and scalar boundary invariant. Part II treats profile observation and endpoint experiments. Part III treats finite-dimensional inverse experiments. The original complete appendices remain after the main argument. The dependency narrative uses mathematical subjects rather than revision numbers; the source directories retain historical names to preserve provenance.

All 168 completed-v9 formal statement and proof environments have been checked byte for byte, and all original active inputs remain active in their original order. The eight added formal environments are the four new declarations and their proofs. This is a retention check, not proof certification. The companion source remains identical and independently builds to the same seven-page PDF.

The final paragraph of Section 9 now says that the two oriented even subsequences suffice for profile reconstruction and odd-law prediction. Observations of the odd subsequence are for direct compatibility validation, not a third reconstruction datum. The distinction is also repeated in the new theorem's interpretation.

Historical v8 and v9 delivery sentences are not silently rewritten. The current entry points and source pins describe this revision; the old records remain attributed to their dates and source states. The new branch adds native manuscript sources without changing an existing author or referee path. The parent retains the complete original v9 lossless publication.

## Verification and boundaries

The completed-v9 packet was authenticated by matching its manifest digest to the GitHub review's record and checking all 118 manifest entries. The active mathematical changes were then made in a separate copy. The local clean build produces a 97-page main article and a seven-page companion, with no unresolved references or overfull boxes. The current verification summary records the PDF hashes and nonsuppressed warnings.

The inherited 249-check suite, v9 407-check suite and new 223-check suite pass in normal and optimized Python with identical per-suite outputs. They overlap and include source-integrity checks. They are not 879 independent mathematical proof obligations; no count of checks substitutes for the written proofs. No formal proof assistant, exact nonlinear finite-offset probability oracle, physical simulation, remote CI success or journal acceptance is claimed.

The remaining assessment of exceptional importance belongs to a subsequent independent review. This revision responds with a new full-profile observation theorem and a more precise account of its invariant, information and cost, while preserving the general nonlinear mathematics previously reviewed.
