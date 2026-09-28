# Independent harsh referee-style report on A2 v22

**Manuscript:** Qian Qi, *Boundary laws, signed contact rigidity, and physical information in dispersing billiards*  
**Review date:** 11 September 2026  
**Requested standard:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the American Mathematical Society*  
**Author revision branch:** `revision/a2-v22-allorder-multichannel-top4-2026-09-11`  
**Immutable revision-branch head reviewed:** `ea97acaa8efb1f4009df5394af58cf9c367a13ab`  
**Canonical manuscript-source commit identified by the revision:** `82a19b18f35fee63819bcc99d530f52adf56c384`  
**Immediate predecessor report:** `reviews/a2-v21-independent-harsh-top4-2026-09-11/REFEREE_REPORT.md`  
**Principal active entry point:** `papers/A2-v17-boundary-information-coarsening/main.tex`

This is an author-requested, AI-assisted independent referee-style assessment. It is not a journal-commissioned report and is not an editorial decision by any journal named above. I reviewed the active v22 theorem chain and the historical dependencies that feed it, rather than treating the response letter or revision manifest as a proof certificate.

## 1. Recommendation to the editor

**Recommendation: reject in the present form at the requested top-four level. A substantially reconstructed version could merit a fresh assessment.**

This recommendation is materially different from the v21 recommendation. V22 has repaired most of the concrete mathematical/formulation defects isolated in the previous report. In particular, I no longer regard the all-order signed-jet calculus, the same-type parity convention, the deterministic-cap quantifiers, the observation-sigma-field hierarchy, or the non-dominated LAN formulation as unresolved in the way they were in v21. The author has done real mathematical work rather than merely rewriting claims.

My negative recommendation now rests primarily on the architecture and significance of the new global conclusion, together with a remaining ambiguity in that theorem and a persistent mismatch between the exact global rigidity statement and the physical statistical experiment.

The central issue is this. The new `finite-channel analytic table rigidity` theorem does produce a table-level statement, but its principal version assumes **registered channels whose contact points and oriented contact frames are already known in one common Euclidean laboratory registration**. Under that hypothesis, the genuinely new work is the one-channel all-order inverse. The passage from a recovered analytic contact germ to the complete connected analytic obstacle is then essentially analytic continuation plus uniqueness for the planar Frenet equations. This is mathematically legitimate, but it does not amount to recovering the global registration from intrinsic billiard data. At the four-journal level, I do not think this corollary by itself supplies the global conceptual leap that the v21 report said was missing.

The manuscript then states a more general version in which the common laboratory registration is forgotten and one initial channel frame is fixed. As written, that statement is not sufficiently defined. There are two possible readings, and neither is satisfactory without revision. If the relative Euclidean placements of all channel frames are still retained, then one has merely retained the common laboratory registration modulo one global Euclidean motion, so the statement adds little. If instead only each channel's intrinsic local frame is retained, then the present definition of a `spanning channel cover`—every obstacle label appears in at least one channel—is insufficient: a cover whose channel-incidence graph has two disconnected components admits independent Euclidean placements of the two components. In that interpretation one does **not** reduce to a single common Euclidean motion. The data and connectivity hypotheses must be made precise.

A second architectural issue remains. The deterministic global theorem is exact, analytic, and all-order: one uses a continuum signed endpoint-support germ, reconstructs every jet, and analytically continues it around a connected obstacle. The physical statistical theorem, by contrast, is explicitly a **fixed finite contact-jet model** in an anchored registered chart, and it deliberately studies an endpoint-output coarsening rather than the complete physical observation. No theorem in v22 lets the jet order grow with the statistical sample, controls analytic continuation from noisy recovered jets, or derives a global table-recovery experiment from the physical model. Thus the new global theorem and the nonregular statistical theorem coexist in the same paper, but they are not yet fused into one global information theorem.

A third issue is the meaning of `physical information`. The v22 formulation is now honest: it says that waiting counts and the richer endpoint-time transcript may contain additional, possibly faster, information, and that no efficiency theorem is claimed for the full raw collision history. I regard this as a correctness improvement, not a defect. But it also makes the top-four limitation sharper. The current information matrix characterizes a deliberately chosen endpoint-output subexperiment. If the paper is to sell a major theorem about physical information, the natural next step is the joint/local limit experiment that includes the success/waiting channel, or else a substantially narrower positioning of the statistical part.

Finally, the exact revision still has no successful canonical native build. The recorded workflow failed twice before any runner step executed. That is not evidence of a TeX error, but it means the submission package remains unverified.

My overall view is therefore:

> **V22 is mathematically stronger and substantially cleaner than v21. The determinant-one inverse now looks like a serious theorem rather than an underproved calculation, and the statistical experiment has been put on an honest measure-theoretic footing. But the newly added global theorem relies on an externally registered data architecture and does not yet create a top-four-level global rigidity mechanism; the unregistered extension is under-specified; the global analytic and physical statistical chains are not joined; and the canonical submission build is still uncertified.**

This is not a recommendation to delete the main results or to retreat to a low-order theorem. The right response, if the four-journal target is retained, is to strengthen the global/intrinsic consequence and the relation between the deterministic and statistical parts.

## 2. Scope of this review

I reviewed the v22 active source graph at the immutable revision head above, concentrating on the statements promoted in the title, abstract and introduction. In particular I inspected:

- `papers/A2-v17-boundary-information-coarsening/main.tex`;
- `article/01_introduction_v22.tex`;
- `v4/10_boundary_layers.tex`, including the half-line Green kernel and nonlinear factorization;
- `v6/10_experiment_transfer.tex`, especially the exact coarsened record space of the finite-to-boundary comparison;
- `article/17_adaptive_experiments.tex`, including the success-weighted stopped coupling;
- `article/23a_signed_endpoint_rigidity_v22.tex` in detail;
- `article/23b_multichannel_rigidity_v22.tex` in detail;
- `article/18a_vector_boundary_information_v22.tex` in detail;
- `article/18b0_anchored_realization_v22.tex`;
- `article/18b_raw_physical_multirate_v22.tex` in detail;
- the v22 response letter, manifest and verification record as audit aids rather than mathematical authority;
- the v21 referee report, to distinguish genuinely resolved objections from new ones.

I also spot-checked the current rigidity context against the literature cited by the manuscript and the recent developments most relevant to its significance claims: De Simoi–Kaloshin–Leguil, *Inventiones Mathematicae* 233 (2023), on marked-length spectral determination of analytic chaotic billiards under symmetry/genericity hypotheses; Osterman, *Journal of Modern Dynamics* 19 (2023), on length-spectrum rigidity for open dispersing billiards; and the 2025 Finamore–Leguil preprint on enriched marked-length rigidity for finite-horizon Sinai billiards. I did **not** identify an obvious duplicate of the determinant-one signed-endpoint jet mechanism. My objection below is therefore not a priority or plagiarism objection; it is about what the present data assumptions buy and whether the resulting global theorem clears the requested venue threshold.

As in any report of this scale, I have not machine-reproved every inherited lemma. I traced the active dependencies feeding the v22 headline theorems and rechecked the interfaces at which the earlier versions had failed.

## 3. What v22 genuinely fixes

### 3.1 The all-order signed-jet proof is substantially repaired

This is the most important improvement in v22.

The v21 report did not find an algebraic contradiction in the displayed last-jet block; it objected that the proof did not close the infinite-dimensional/high-order bookkeeping around that block. V22 now supplies the missing architecture.

The weighted half-line inverse is written as an actual operator estimate on

`X_rho = { x : sup rho^{-i}|x_i| < infinity }`

with `e^{-gamma_-} < rho < 1`. The Green kernel estimate is compatible with this weight, the nonlinear Hessian perturbation is stated in operator norm as `O(|u|)`, and a Neumann argument gives a uniform inverse after shrinking the endpoint box. This is the right mechanism for repeated implicit differentiation.

More importantly, v22 no longer claims that the differentiated stationarity equations themselves have the desired graph-jet order. It explicitly acknowledges the one-order shift that motivated C21-M1 and proves the **action** filtration separately. The finite-truncation envelope identity cancels the interior orbit variations and estimates the remaining right-boundary term by an exponentially decaying tail. The subsequent homogeneous-degree lemma proves

`partial_{q_{r,m}} S_b(u) = O(u^m)`.

That is exactly the structural statement needed to show that graph jets of order `m>n` cannot enter `S_b^(n)(0)`, while at `m=n` only the linear half-line orbit contributes at degree `n`.

With this in place, the geometric sums

`1 + 2 sum_{k>=1} e^{-2 n gamma k} = coth(n gamma)`

and

`2 r_b^n sum_{k>=0} e^{-n gamma(2k+1)} = r_b^n csch(n gamma)`

produce the displayed matrix `M_n`, and `r_0 r_1=1` gives

`det M_n = coth^2(n gamma) - csch^2(n gamma) = 1`.

I therefore do **not** repeat C21-M1 as an unresolved major blocker. There are still places where a final journal version could improve operator-class notation and spell out the parameter dependence of differentiated weighted estimates, but the core missing argument has been supplied.

### 3.2 The physical parity defect is fixed

The same-type physical designs now explicitly require

`j_n in 2 N`.

The text also states what changes for odd flight number. This closes the concrete theorem-statement mismatch identified in v21.

### 3.3 The cap quantifier problem is fixed in the intended local-asymptotic sense

The v22 cap is chosen from the reference success probability before any compact local parameter set is quantified over:

`N_{n,l} = ceil(4 k_{n,l} / p^partial_{n,l}(0))`.

Under `j_n delta_n -> 0`, the same cap sequence is eventually adequate on every fixed compact local set. This is the correct quantifier order for a local asymptotic theory in which the compact radius is fixed before `n -> infinity`, and it is compatible with the subsequent local asymptotic minimax limiting order.

The proof would benefit from a sharper backward citation to the precise uniform success-probability expansion that supplies the smooth prefactor and hyperbolic exponent, but I do not see the old logical defect surviving.

### 3.4 The observation sigma-fields are now honestly separated

The manuscript now distinguishes:

1. the full raw collision history;
2. the per-preparation endpoint/residual-time coarsening plus failure;
3. the stopped endpoint-time acquisition transcript retaining designs, failures and stopping time;
4. the further endpoint-output coarsening used for the Gaussian experiment.

This is consistent with the historical `v6` transfer theorem and the adaptive stopped-policy theorem. The v6 theorem controls a common coarsened endpoint/residual-time record and failure atom; it explicitly does not compare the full growing collision array. The adaptive theorem then propagates that comparison through a policy with a success-weighted budget. V22 now states the same hierarchy rather than calling the coarsened transcript the full raw observation.

I therefore do **not** repeat C21-M4 as a major correctness objection.

### 3.5 The non-dominated statistical architecture is now coherent

The common-collar construction in `18a_vector_boundary_information_v22.tex` is a substantial repair rather than rhetorical relabeling.

The original family is allowed to be non-dominated. The support-exclusive mass is controlled at order `p_n delta_n^2`. A parameter-independent censoring map retains a common collar `w_0 >= q_n`, with

`q_n = delta_n (log(1/delta_n))^(1/4)`,

and sends the discarded successful region to an atom. The censored family is genuinely dominated by the null censored law, and both comparison kernels can be chosen independently of the local parameter. At the critical scale

`n p_n delta_n^2 log(1/delta_n) -> 1`,

the discarded product mass is `o(1)`.

The literal LAN expansion is then asserted only for the dominated representative. Finite local subexperiments, contiguity, testing and minimax consequences are stated separately. Singular information is handled on `Ran(J_Sigma)` with the Moore–Penrose inverse rather than by pretending that the full matrix is invertible.

This is the right conceptual hierarchy. I do not find the v20/v21 finite-sample domination error in the active v22 formulation.

### 3.6 The fixed-window reduction and tangent-level finite design are materially improved

The exact billiard endpoint density is compared with the ideal linearly moving-support family using an explicit support remainder

`r_n = delta_n^2 + delta_n/j_n`

and an `O(delta_n)` amplitude remainder. At `k_n delta_n^2 log(1/delta_n) -> 1`, the Hellinger product error is negligible for every `j_n -> infinity`; the two elementary regimes used in the proof have the correct order.

The positive finite-design lemma now works at the derivative level. A vector in the common kernel of all same-type boundary information forms gives zero first variation of both half-line actions near the contact, and the finite signed-jet tangent isomorphism then forces the finite jet direction to vanish. Compactness of the unit sphere yields a finite positive design. This is the correct replacement for the earlier nonlinear-injectivity shortcut.

These improvements should be preserved.

## 4. Major blocker C22-M1: the new table-rigidity theorem does not yet provide an intrinsic global rigidity mechanism

The new theorem is the main reason v22 differs strategically from v21, so it deserves especially careful scrutiny.

### 4.1 The common-registration theorem is plausible but its global step is largely formal once registration is supplied

A `registered channel` is defined to include the two participating obstacle labels, the two contact points and the oriented contact frames in one common Euclidean laboratory registration. Equality of the signed endpoint-law germs then recovers the complete analytic graph germs at those already registered contacts.

For a connected real-analytic obstacle, equality of a boundary germ in a fixed point/tangent frame propagates by analytic continuation; equivalently, the analytic curvature functions coincide and the Frenet ODE reconstructs the same boundary image. Applying this once to an incident measured channel for each label determines every obstacle.

I see no obvious mathematical contradiction in this registered statement. The problem is what it demonstrates. The theorem does **not** infer the contact registration, the relative obstacle placement, or the channel network from the endpoint laws. Those geometric frames are part of the data. The new global step is therefore essentially:

`one registered analytic germ per obstacle -> whole connected analytic obstacle`.

That is a valid exact corollary of the local inverse and analyticity, but it is not comparable in difficulty to global marked-length rigidity results in which the global geometry has to be extracted from intrinsically dynamical data. The manuscript is entitled to use a different data set; however, at the requested venue level the strength of the conclusion must be assessed together with how much geometry was supplied in the observation architecture.

### 4.2 The unregistered extension is under-specified and can be false under the natural weak reading

The theorem says, more generally, that if the common laboratory registration is forgotten but one initial oriented contact frame is fixed, the same data determine every obstacle met by the cover up to one common Euclidean motion.

This needs a formal definition of the data after registration is `forgotten`.

- **Strong reading:** all relative Euclidean placements among all channel frames are retained, and only the absolute origin/rotation is forgotten. Then the data are simply the original common registration modulo one common Euclidean motion. The conclusion is essentially built into the retained registration.
- **Weak reading:** each channel carries only its own two local frames and intrinsic endpoint laws, with identifications propagated through shared obstacle labels. Then the present definition of `spanning channel cover` is insufficient. It only requires every obstacle label to occur in at least one edge. If the channel-incidence graph has two connected components, the two components may be placed by independent Euclidean motions while preserving all per-channel intrinsic data. Fixing one frame in one component does not place the other component.

The proof sentence that `where channels share already reconstructed labels, the registrations are compatible by hypothesis` actually highlights the issue: propagation through shared labels requires graph connectivity if no global registration is otherwise retained.

The author should therefore do one of the following:

1. retain the common registration and delete/soften the unregistered extension;
2. define the unregistered channel data precisely and require the channel-incidence graph to be connected, then prove propagation of relative frames across the graph;
3. preferably, show that the required relative registrations themselves are recoverable from an intrinsic observation scheme.

Until this is done, the global theorem has a theorem-statement/data-model ambiguity, not merely an expository blemish.

### 4.3 `Spanning channel cover` is currently a vertex-cover condition, not a connectivity condition

The terminology invites overreading. The definition means only that every obstacle label occurs at an endpoint of at least one measured channel. It does not mean the channel graph is connected or graph-theoretically spanning in the usual sense.

If the common laboratory coordinates remain known, connectivity is unnecessary. If the coordinates are removed and frame placement is to be propagated through shared obstacles, connectivity becomes essential. The paper should use terminology that makes this distinction impossible to miss.

## 5. Major blocker C22-M2: the four-journal significance threshold is still not crossed by the present global consequence

This is not a claim that the paper is uninteresting. It is a venue assessment.

The determinant-one inverse is, in my view, the strongest and most distinctive theorem in the manuscript. It reconstructs all labelled smooth contact jets from two signed same-type endpoint-support laws, without reflection symmetry, equal contacts, or supplied curvatures. That is a meaningful inverse mechanism.

The new table theorem, however, upgrades this to a global statement only after imposing all of the following:

- real-analytic connected obstacle boundaries;
- exact continuum endpoint-law germs for finitely many channels;
- channel labels;
- signed endpoint coordinates;
- channel onsets;
- and, in the clean primary version, absolute contact points and oriented frames in one common laboratory registration.

Thus `finite-channel` does not mean finite scalar data: every selected channel supplies a continuum germ carrying the entire all-order hierarchy. The manuscript itself notes this, and it should continue to do so.

The recent billiard-rigidity literature provides a useful benchmark, even though the data sets are different. De Simoi–Kaloshin–Leguil obtain global table determination from marked length spectral data under their analytic/symmetry/genericity hypotheses; Osterman obtains global/local consequences from marked length data in open dispersing billiards; Finamore–Leguil's enriched marked-length work obtains a global isometry statement for finite-horizon Sinai billiards from an intrinsically dynamical data set. I do not infer from these papers that the present endpoint theorem is known or redundant. I infer that a top-four global rigidity claim must make clear what global geometry is reconstructed **rather than supplied as registration data**.

At present the new theorem does not answer the strongest natural question suggested by the paper:

> Can the boundary-law data themselves recover the relative placement and full table, up to the unavoidable single Euclidean motion, without giving one absolute contact frame per measured channel in advance?

A positive theorem of that form would change my significance assessment substantially. Other possible routes include a smooth (not merely analytic) global rigidity/stability result, a universality theorem showing the determinant-one mechanism in a wider class of hyperbolic variational systems, or a complete physical local experiment that captures the currently omitted information channel.

Without such a strengthening, I would regard v22 as potentially a strong specialist paper after technical cleanup, but not yet as an Annals/Acta/Inventiones/JAMS paper.

## 6. Major blocker C22-M3: the exact global analytic theorem and the physical statistical theorem remain logically disconnected

The introduction presents two chains:

`relative boundary law -> all-order contact inverse -> analytic table rigidity`

and

`fixed laboratory endpoint law -> dominated representative -> Gaussian endpoint experiment`.

This is an honest presentation; the paper no longer falsely claims that the statistical theorem itself is global. But that honesty reveals a structural gap.

The table-rigidity theorem uses **every** contact jet and exact analytic continuation. The physical statistical theorem fixes a finite jet order `M` and then constructs a finite design with positive-definite information on that finite-dimensional model. The design is explicitly allowed to depend on `M` and on the reference geometry. There is no result controlling:

- a sequence `M=M_n -> infinity`;
- conditioning of the determinant-one recursion as `M` grows;
- statistical estimation of an analytic norm rather than a fixed finite jet;
- propagation of noisy local jets by analytic continuation;
- global table loss or uncertainty;
- or the cost/information tradeoff required to recover more and more jet orders.

This is not a hidden correctness error: the current theorem carefully avoids those claims. But it means the analytic global theorem cannot presently be used as the conceptual payoff of the physical information theorem. They share the half-line action, but they live at different inferential levels.

For a top-four revision, the author should either bridge these levels or reposition the paper so that they are clearly separate applications of the boundary law rather than components of one global statistical rigidity theorem.

A genuinely strong bridge would be, for example, an analytic-class theorem with quantitative coefficient bounds that permits `M_n` to grow, combines the finite-jet information matrices with a regularization scheme, and yields a nontrivial global reconstruction/stability statement. I do not insist on this exact route, but the present exact/noisy gap is too large for the current top-four narrative.

## 7. Major blocker C22-M4: the physical information theorem is intentionally a subexperiment, and the paper should either complete it or narrow the headline claim

V22 correctly states that the endpoint-output information matrix is **not** an efficiency bound for the richer stopped endpoint-time transcript and still less for the full raw collision history. It also observes that the success probability contains the hyperbolic factor and that waiting counts may carry additional and possibly faster information in directions changing the exponent.

This is a strength of the revision as mathematics. But from the perspective of the title and four-journal significance, the current result is therefore a theorem about a selected endpoint-output information channel, not the physical information of the acquisition process as a whole.

There are two defensible paths.

### Path A: complete the physical local experiment

Retain the waiting/success-count channel jointly with the endpoint law, determine its local scaling relative to the `delta_n` endpoint scale, and identify the joint asymptotic experiment. This may be genuinely multirate: the hyperbolic exponent enters the rare-event success probability through `exp(-j gamma)`, whereas the moving support produces logarithmic boundary information. If these channels interact nontrivially, the complete theorem could be substantially stronger than the endpoint result and might itself provide the conceptual gain the paper needs.

### Path B: narrow the claims

If the endpoint-output channel is the intended final object, the title, abstract and significance discussion should consistently say so. `Physical endpoint information` or an equivalent formulation would be more accurate than language that can be read as characterizing all physical information.

At a specialist-journal level Path B may be entirely reasonable. At the requested four-journal level I would encourage Path A.

## 8. Major blocker C22-M5: there is still no successful canonical native build

The v22 verification record is admirably explicit: workflow run `34595965653` and its explicit rerun both failed before any runner step executed, with `steps = null`. Hence there is no evidence of an executed LaTeX failure, but there is also no successful exact-head build certificate.

This is not a mathematical reason to reject a theorem. It is nevertheless a submission-readiness blocker. Before another referee round the author should produce, from the exact revision source:

- a successful clean native build;
- no unresolved references or citations;
- the built PDF and source hash;
- and preferably a reproducible minimal build command independent of repository history.

The report should not be marked `submission ready` until that exists.

## 9. Secondary mathematical and expository comments

These are not the primary basis of the recommendation, but they should be addressed in a serious revision.

### 9.1 State the data model for table rigidity before the theorem, not inside explanatory prose

For each channel, specify exactly which objects are observed and which are externally registered: labels, contact points, tangent orientations, relative frame transforms, onset time, endpoint coordinate units, and the germ parameter `d`. Then define equivalence of two data sets. The present phrase `same spanning channel cover in one common laboratory registration` carries too much hidden structure.

### 9.2 Separate `absolute registration`, `registration modulo E(2)`, and `intrinsic per-channel data`

These are three different inverse problems. The current theorem moves between them too quickly. The group action should be explicit.

### 9.3 If an unregistered theorem is retained, use a connected channel graph and prove the placement induction

A graph-theoretic formulation would make the missing geometry transparent. Vertices are obstacle labels; measured channels are edges. If shared obstacles identify local frames, explain precisely how an edge incident to an already placed vertex places its other endpoint and why cycle compatibility follows from the data.

### 9.4 The cap lemma should cite the exact success-law estimate used to obtain the ratio `1+o(1)`

The proof currently says, in effect, `this is the uniform threshold law and smooth parameter dependence of its prefactor`. Given how important the cap quantifier was in the previous round, the final version should point to the precise proposition/equation that yields the decomposition with a parameter-uniform prefactor after extracting `exp(-j gamma)`.

### 9.5 Give one explicit compatible asymptotic choice of `(delta_n,j_n,k_n)`

The conditions

`k_n delta_n^2 log(1/delta_n) -> 1`,

`j_n delta_n -> 0`,

and

`k_n tau^{j_n} -> 0`

are compatible, but a one-line example would help the reader see the nonempty regime immediately. For instance, an even `j_n` proportional to a sufficiently large multiple of `log(1/delta_n)` satisfies the last condition while remaining `o(1/delta_n)`.

### 9.6 Clarify the sense in which the finite signed-jet inverse is quantitatively stable

For fixed `M` the compact-uniform lower singular-value bound is useful. The paper should say explicitly that no uniform-in-`M` conditioning is claimed. This matters because the analytic global theorem uses all orders whereas the statistical theorem fixes `M`.

### 9.7 The phrase `finite data architecture` should not suggest finitely many real numbers

There are finitely many channels, but each channel supplies a continuum endpoint-law germ. The corollary already gestures at this; the terminology should remain explicit everywhere the global theorem is advertised.

### 9.8 The analytic-continuation step deserves a clean standalone lemma

A short lemma for connected embedded real-analytic planar curves—equality of a registered nonempty boundary germ implies equality of the complete connected boundary image—would make the table theorem cleaner and prevent the global argument from being hidden in prose.

### 9.9 The manuscript remains structurally overgrown

The active source combines historical modules from several generations of the project, auxiliary inverse transforms, statistical regularization results, physical transfer machinery, and the new all-order/table-rigidity material. Much of this may be mathematically useful, but a top-four submission should read as one deliberate paper rather than a repository history.

I am **not** recommending arbitrary deletion of results. I am recommending a stronger theorem hierarchy: place every lemma under a named headline theorem, move genuinely auxiliary material to appendices, remove version-history language from the mathematical narrative, and make the logical dependency graph visible from the introduction and section openings.

### 9.10 The acknowledgments/history apparatus should not substitute for proof provenance

The acknowledgments currently list many AI-assisted independent memoranda. Transparency is good, but the paper itself must remain self-contained and conventionally citable. Referee-history documents should not be needed to understand why a theorem is true or which assumptions are active.

## 10. What I would require before another top-four assessment

I would not ask the author to downscale the all-order inverse. I would ask for the following stronger revision program.

### R22-1. Replace the present global corollary by a genuinely intrinsic or precisely registered global theorem

At minimum, repair the data-model ambiguity and the unregistered statement. For a materially stronger result, recover relative channel placement from the observed data rather than supplying all contact frames in a common Euclidean registration.

A credible theorem could use a connected measured-channel graph, one fixed initial frame, and data that determine the relative transform across each edge. The proof should show that the entire table is then determined up to one global Euclidean motion. Even better would be a formulation in terms of an intrinsic billiard observation scheme with no external contact-frame registration.

### R22-2. Decide whether the endpoint-output theorem is a component of a complete physical experiment or an intentionally partial channel

If the four-journal target is retained, I strongly encourage a joint asymptotic analysis of endpoint observations and success/waiting counts. The manuscript itself identifies this as a potentially faster information channel, so ignoring it leaves an obvious next theorem on the table.

If that theorem is not pursued, narrow the title and headline claims so the reader cannot mistake the endpoint matrix for complete physical information.

### R22-3. Bridge finite-jet statistics to analytic/global recovery, or stop using the global analytic theorem to elevate the statistical claim

A quantitative analytic-class theory with growing jet order and global loss would be a substantial result. If it is out of scope, the manuscript should present the deterministic global theorem and finite-dimensional statistical theorem as two separate consequences of the boundary law, without implying that the physical experiment reconstructs the analytic table.

### R22-4. Preserve the v22 repairs

Do not regress on:

- the weighted all-order inverse/envelope proof;
- the even-flight same-type convention;
- the reference-based deterministic caps;
- the exact observation-sigma-field hierarchy;
- the non-dominated/common-collar distinction;
- the identifiable-subspace formulation for singular information;
- the fixed laboratory-coordinate model;
- and the explicit statement that waiting counts are not ancillary by decree.

These are genuine gains.

### R22-5. Produce a successful canonical build

A fresh review should be based on an immutable source head with a successful clean PDF build and diagnostics.

### R22-6. Reorganize the manuscript around the strongest theorem chain

The paper needs to feel like a theorem-driven research article rather than an accumulation of revision-era modules. This is especially important if the target remains one of the four journals named above.

## 11. Bottom-line assessment of the headline claims

For clarity, my present referee judgments are:

- **Nonlinear two-boundary relative law:** no new v22 objection; I regard the inherited theorem as a legitimate foundation for this round.
- **All-order signed endpoint rigidity / determinant-one blocks:** **substantially repaired and mathematically credible in v22**. I do not find the previous proof-closure objection still decisive.
- **Finite signed-jet tangent isomorphism:** credible once the all-order filtration is accepted; the finite-dimensional lower singular-value statement is correctly only compact/fixed-order.
- **Non-dominated vector boundary Gaussian limit:** the measure-theoretic architecture is now coherent; the previous false finite-sample likelihood issue is not present in the active formulation.
- **Fixed-window multirate endpoint experiment:** internally consistent at the declared endpoint-output level; parity, caps and laboratory coordinates have been repaired.
- **Stopped finite-to-boundary transfer:** correctly limited to the endpoint/residual-time coarsened transcript; the historical adaptive theorem supports the success-weighted `k_n tau^{j_n}` bound.
- **Finite-channel analytic table rigidity in common registration:** mathematically plausible, but too dependent on supplied global registration to furnish the desired top-four conceptual consequence by itself.
- **Unregistered table-rigidity extension:** under-specified; depending on what registration data remain, it is either essentially the registered theorem modulo one motion or needs additional connectivity/placement hypotheses.
- **Complete physical information claim:** not proved, and v22 appropriately no longer says it is; waiting counts/full histories remain outside the efficiency theorem.
- **Submission readiness:** not yet achieved because the exact-head native build has not executed successfully.

## 12. Final recommendation

**Reject in the present form at Annals/Acta/Inventiones/JAMS standard, with encouragement to resubmit a substantially strengthened and reorganized version for a fresh assessment.**

The reason is no longer that the manuscript is riddled with the same local proof defects as earlier revisions. V22 has solved most of those. The reason is that, once the local defects are repaired, the four-journal question becomes sharper: what is the genuinely global/intrinsic theorem, and what is the complete physical information theorem?

The determinant-one signed inverse is strong enough to justify continuing the project. The next revision should build **outward** from it rather than weaken it: recover or eliminate the external registration, connect the channel network intrinsically, or complete the physical multirate experiment (and ideally connect finite-jet statistical information to global analytic recovery). If one of those directions succeeds at theorem level, the paper's venue profile could change materially.

Until then, I would not recommend acceptance at the requested top-four level.