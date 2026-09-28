# Independent referee-style report on A2 revision 43

**Manuscript:** *Boundary laws, intrinsic periodic rigidity, and global physical reconstruction in dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 14, 2026  
**Standard requested:** a highest-level general mathematics journal. This is an author-requested, AI-assisted independent assessment, not a commissioned report or a decision of any journal.

| Object examined | Frozen identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Source branch | `revision/a2-v43-complete-native-delivery-2026-09-14` |
| Source commit | `22d9b930a426cdb2c62984a5a3e5875e95e05e79` |
| Native-products branch | `revision/a2-v43-native-products-34813913830-1` |
| Products commit | `edd95683ee57965ff8cd82cee1462a478d06ae39` |
| Addressed v42 report | `19935273acf323a3f8971d7f5029b8670ec1bd58` |
| Actual products examined | Complete native main, 222 pages; companion, 7 pages |

Source references S01–S18 and primary literature references L1–L4 are defined in [AUDIT_AND_REPRODUCTION.md](AUDIT_AND_REPRODUCTION.md). Page numbers refer to the downloaded native main, not an earlier revision. The historical directory name `A2-v17` is not a version identifier.

## Recommendation and principal findings

**MAJOR REVISION. I do not recommend acceptance of this submission at the requested journal level.** The reason is no longer the absence of a compiled article. The full native source and both PDFs were obtained, their source/product identities checked, and both native entries independently compiled. Treating this revision as another failed or unexecuted build would be factually wrong. [S01]

The fresh mathematical examination below did **not** establish a fatal counterexample to the inspected central theorems. This is a bounded finding, not a certification of all theorems in the 222-page submission. The report distinguishes an actual distribution of work: fresh proof scrutiny, independent finite diagnostics, inherited results not rederived here, and editorial judgment.

The central inverse mechanism is credible and merits serious consideration. Nevertheless, a substantial technical composition and a successful delivery do not, by themselves, establish the exceptional mathematical significance required by the requested journals. That reservation remains after crediting the current introduction's much improved distinctions between observations, classical inputs and new mechanisms. It must not be disguised as a nonexistent proof error. [S02]

There are also two concrete, readily repairable delivery/documentation defects: the products receipt asserts Git retention of files that the commit does not contain, and both current README entries still advertise v42 and its unsuccessful delivery checkpoint. Neither defect refutes the mathematical results. [S16]

| Previous issue or current finding | Disposition |
|---|---|
| No complete source-matched native main/companion | **Closed as a build and present-access objection.** Both products exist and independently rebuild. |
| Rendered-product examination | **Performed with stated coverage:** 33 main pages and all 7 companion pages; not an all-page visual certificate. |
| Common-frame anchoring and rerooting | **Repair retained and now also explicit in Theorem 15.4.** No new registration hypothesis is requested. |
| Smooth finite-jet factorization | **Withstands the fresh envelope/remainder examination below.** |
| Claimed permanent Git retention | **R43-D1 open:** 13 promised native files are absent from the products commit. |
| Current revision navigation | **R43-D2 open:** current entries still identify v42. |
| Exceptional general-journal significance | **Not established by this assessment.** Separate editorial reservation R43-S1. |

## 1. The mathematical contribution being evaluated

The most substantial proposed chain is

$$
\text{relative nonlinear long-bridge asymptotics}
\longrightarrow \text{intrinsic signed endpoint laws}
\longrightarrow \text{both complete contact jets}
\longrightarrow \text{analytic boundary images and marked periodic placement}.
$$

The first arrow requires control relative to an exponentially small endpoint twist, not merely an absolute action approximation. The second concerns laws after genuine deletion of geometric information, not a collection of noiseless graph ordinates. The analytic and marked geometric hypotheses enter the third and fourth arrows in different ways. The physical preparation theorem is an additional realization of the declared observations, with pilots, failures and stopping costs accounted for. [S02–S15]

These distinctions are already present in the current introduction and proof-architecture section. I do not ask the author to add a novelty paragraph that already exists, or to relabel elementary consequences as deep theorems. Nor should the abstract be strengthened to an unmarked inverse problem: obstacle labels, deck labels, selected channel incidence and prescribed gates remain part of the experiment.

## 2. Fresh examination of the relative forward law

The local Euclidean flight generating function has the form

$$
\ell_b(y,z)=\sqrt{(g+\psi_b(y)+\psi_{1-b}(z))^2+(z-y)^2}.
$$

The positive gap, curvature and clearance assumptions supply a uniform contact collar and an alternating itinerary. The selected nonminimal-channel statement is a statement about the selected event; it must not be confused with a decomposition of every collision-count event. The inspected geometric discussion makes that restriction explicit. [S03]

For a finite stationary bridge the tridiagonal Schur-complement/cofactor formula expresses its negative mixed endpoint derivative as the product of the edge twists divided by the interior Hessian determinant. Since the reference mixed derivative decreases exponentially with the number of flights, an absolute remainder estimate would be insufficient. The manuscript instead controls the logarithm of the relative determinant. The sum of absolute Hessian-perturbation entries is bounded independently of bridge length, giving the required trace-norm bound. Small operator norm then permits the logarithmic determinant series. This is the appropriate relative mechanism. [S03, S05]

The half-line comparison also has substance beyond a formal limiting argument. Weighted orbit bounds make the residual of the two glued half-lines summable, of order a polynomial in the flight number times an exponential. Symmetry and diagonal dominance transfer the inverse-Hessian bound to the sum norm. In the determinant comparison, retained endpoint blocks are separated by a middle region; tails, reflected Green terms and the off-diagonal interaction are estimated before taking logarithms. In particular,

$$
|\operatorname{tr}(T^m-(T')^m)|
\le m q^{m-1}\|T-T'\|_1,\qquad \|T\|,\|T'\|\le q<1,
$$

provides dimension-independent summability. At every prescribed finite differentiated order, a slightly slower exponential absorbs the polynomial factors. I found no justified basis for reopening the earlier objection about dividing an uncontrolled absolute error by an exponentially small twist.

The integration step changes variables from the stationary endpoint action to a common disk by a parameter-dependent Morse map. Odd terms integrate to zero, and finite additional endpoint derivatives control the right derivatives in the offset at zero. This is materially different from differentiating the moving indicator formally. The flux normalization and the exclusion of roof truncation use the gap restriction on the offset. Parameter derivatives are taken in the channel-centred parametrization, not at a fixed physical time while silently allowing the gap to move. [S04]

These findings concern the inspected contact-collar arguments and their composition. They are not a proof of every historical count-law application in the auxiliary compendium.

## 3. The all-order inverse: where the real difficulty lies

### 3.1 Smooth remainders are treated before finite jet coordinates

Theorem 12.1 depends on a filtration statement that cannot follow merely from the nonzero determinant of a displayed two-by-two matrix. A derivative of a stationarity equation can expose apparently higher graph derivatives. The manuscript therefore needs to prove that finite action jets factor through finite graph jets. Lemmas 12.3 and 12.4 now provide that argument. [S06; pp. 48–50]

For a finite action truncation, interior orbit variations cancel by stationarity. The terminal boundary term is a product of two exponentially decaying quantities and tends to zero, including at each fixed differentiated order under the stated smooth bounds. For two graph pairs agreeing through order M, interpolate their actual smooth graphs on a common local interval. The direct variation of one flight is

$$
\partial_t\ell_{r,t}(y,z)
=\frac{h_{r,t}(y,z)}{\ell_{r,t}(y,z)}
\{\Delta\psi_r(y)+\Delta\psi_{1-r}(z)\}.
$$

Equal finite jets give a remainder of order M+1. Along the weighted orbit this is bounded by a summable multiple of

$$
|u|^{M+1}\rho^{(M+1)i}.
$$

Integrating the exact finite envelope identity in the interpolation parameter and then passing to the truncation limit yields

$$
|S_b^{[1]}(u)-S_b^{[0]}(u)|
\le \frac{C_M}{1-\rho^{M+1}}|u|^{M+1}.
$$

This deals with smooth functional remainders, including flat variations, rather than only polynomial coefficients. The interpolation is local and does not assume that every intermediate graph pair is a globally realized periodic table. Uniformity requires functional smoothness bounds on a common interval; bounded finite coefficients alone are not substituted for those bounds.

### 3.2 The triangular block is an inverse, not an infinite-order conditioning certificate

At the first occurrence of an order-n graph jet, only the linear half-line orbit contributes. The starting contact appears once and each interior contact twice. The relevant sums are

$$
1+2\sum_{k\ge1}e^{-2n\gamma k}=\coth(n\gamma),\qquad
2\mathfrak r_b^n\sum_{k\ge0}e^{-n\gamma(2k+1)}
=\mathfrak r_b^n\operatorname{csch}(n\gamma).
$$

Together with $\mathfrak r_0\mathfrak r_1=1$, these give the claimed determinant-one block. Once the smooth filtration has been established, the finite block-lower-triangular inverse follows. The corresponding constants are local and depend on the prescribed finite order and geometric class. Nothing here supplies an unrestricted, uniformly conditioned infinite-jet inverse. The current text respects that distinction. Analyticity is used subsequently to determine boundary images, not to replace the smooth remainder proof. [S06]

### 3.3 The single-offset density formula uses a nondegenerate scalar anchor

On the positive interior square, write

$$
f(u,v)=Z^{-1}B(u)B(v)\{d-S(u)-S(v)\},\qquad
R(u,v)=\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}.
$$

Then $1-R(u,v)=t(u)t(v)$, where $t=S/(d-S)$. For a fixed nonzero anchor a, strict convexity gives t(a)>0 and

$$
t(u)=\frac{1-R(u,a)}{\sqrt{1-R(a,a)}},\qquad
S(u)=\frac{dt(u)}{1+t(u)}.
$$

The amplitude is recovered up to its irrelevant normalization. This calculation works for non-even actions and unknown nonconstant amplitudes. Crucially, the square root is taken at one positive scalar anchor, not differentiated pointwise through a double zero at the origin. [S07; Theorem 13.1, p. 53]

An exact law in the stated class determines its continuous interior density. That fact does not make a density value a single sample observation. The stated stability is in an interior C^M topology, with positive density and anchor margins; it is not a claim that total variation controls arbitrary jets. The finite-flight corollary treats normalization on the entire box using the Lipschitz property of the positive part, then differentiates only in the positive interior. The estimated constant and linear action terms are removed before applying the anchored inverse. I found no new defect in these steps.

## 4. Global geometry and the common-frame issue

Equality of complete oriented curvature signatures on an analytic closed strictly convex curve characterizes its proper Euclidean symmetry orbits. The proof combines analytic continuation of arclength curvature with uniqueness of the Frenet system. In particular, uniqueness at one point rules out every nontrivial proper symmetry, and gives uniqueness at all points. [S08]

This is exactly what makes the rerooting lemma work. Along the reversed path, each new parent was already an old parent, except for the chosen new root, where signature uniqueness is supplied by the anchoring hypothesis. It would not justify rerooting at an arbitrary symmetric leaf. The actual lemma does not claim that. [S09]

The detailed single-offset proof and the v43 version of Theorem 15.4 now perform the complete composition in one frame. After fixing the common starting frame of the rank-two anchoring cycles, reroot at an incident obstacle, recover the two translation holonomies, and set

$$
L=VM^{-1},\qquad L^TL=M^{-T}V^TVM^{-1}.
$$

All subsequent deck corrections and obstacle placements use this same lattice realization. Aligning two admissible realizations at the starting frame gives equal lattice matrices and then equal child placements inductively. Realizability supplies existence and geometric admissibility; it is not a conclusion for arbitrary noisy gluing data. The formerly abbreviated proof now cites the rerooting lemma explicitly. The common-frame objection should remain closed. [S07, S10; pp. 54–55, 68]

The stability chapter also distinguishes two arguments that must not be conflated. Finite signatures are locally embedded using nonvanishing signature derivatives and compactness, with a separate global separation argument. A C^2-nearby signature curve has a unique local nearest match because

$$
\frac{d^2}{dx^2}\frac12|\widetilde J(x)-y|^2
=|\widetilde J'(x)|^2+(\widetilde J(x)-y)\cdot\widetilde J''(x)
$$

is positive on a small arc, while the outside gap excludes other minimizers. Mere C^0 closeness would not suffice. Separately, exact injectivity on a compact analytic class gives a generally non-effective inverse modulus. The geometric series tail in the jet-product metric is not a quantitative analytic-continuation rate. These limitations are stated, not hidden. [S11; Theorems 16.1, 16.2 and 16.4]

## 5. Fresh scrutiny of the statistical and physical composition

### 5.1 What was freshly checked in the Gaussian comparison

The compact-parameter upgrade in Theorem 27.2 was examined anew. One comparison kernel is chosen for an entire finite parameter net. Its error outside the net is bounded by the prelimit and limit total-variation moduli; the unknown parameter is not supplied to a nearest-net-point kernel. The moving-support Hellinger estimate gives a product modulus bounded by a constant times

$$
s\sqrt{1+\log(1/s)},\qquad s=\|h-h'\|,
$$

which tends to zero. Gaussian continuity is taken on the identifiable subspace, so a singular information matrix is not improperly inverted. This is a valid finite-to-compact mechanism, conditional on the finite-experiment convergence established elsewhere. [S12]

This review does not rederive every preceding LAN, common-collar, alternative-moment, quadratic-loss or Poisson-kernel theorem. Favorable findings in the v42 report about those dependencies are historical evidence, not fresh certification by this report. In particular, no claim of complete two-sided physical Poisson verification is made here. [S17]

### 5.2 The pilot pays for its precision at the final flight number

The physical acquisition theorem uses common observable planar records in each channel frame; different channels need not be preregistered. Channel labels, deck labels and gates are supplied. For an onset scan with mesh h at flight number j, the success lower bound on a witness interval is of order $h^2e^{-j\gamma_{\max}}$. A first observed success therefore localizes the onset within an interval of length 2h with the stated high probability, after a finite preparation cap. [S13]

The important composition detail is that the final flight number J is chosen before the pilot, and the pilot is run at that same J. Thus the error bound controls $J|\widehat g-g|$, rather than estimating g at a fixed small flight number and multiplying its error by an uncontrolled later J. Endpoint localization estimates the channel normal and tangent with error of order square root h, using the positive gap margin. The ensuing bounded-test bias has the declared contributions from chart error, offset error and the exponential bridge error. The ideal centred chart is used in the proof, not handed to the observer as an oracle.

### 5.3 The global estimator is an existence theorem with charged costs

On the compact class, pairs of tables separated in the target finite-data metric are separated by some gap or bounded Lipschitz law test. A finite subcover gives a finite list of tests and a positive separation margin. A finite template library then turns their estimates into a table-valued estimator. The source accounts for pilot failure, bounded-test concentration and preparation-cap failure separately. It uses the iid sequence of uncapped successes and then charges the exceptional cap event; it does not assert iid sampling after conditioning on a cap-dependent success event. [S14]

Theorem 39.3 also handles its diverging minimum flight number correctly. For budget N it runs the selected stage afresh, rather than accumulating all previous stages, which would retain short flights forever. Its library, inverse modulus and preparation caps may be non-effective. No polynomial-time implementation, sharp analytic minimax rate or cheap rare-event complexity is proved or claimed. The recovered object includes the Euclidean lattice. [S14; p. 141]

The finite-rank analytic variation construction was also inspected: support-function variations fix the contact position and normal at the selected angles while prescribed higher jets vary through a triangular map. Compactness and the positive curvature/contact-separation margins enter the bounded right inverse. This is a finite-rank construction, not an assertion that an arbitrary compact parameter set is a smooth manifold. [S15]

These are genuine safeguards. They should not be deleted to make the statement look broader. The separate direct-position benchmark, however, remains a serious significance comparison: noiseless geometric ordinates can carry information not present in the coarsened transverse laws. Restricting flights to be long does not by itself exclude that benchmark. The introduction correctly acknowledges this. [S02]

## 6. Independently executed diagnostics

The accompanying [implementation](independent_checks.py) and [results](RESULTS.json) are new for this report. They do not import manuscript implementations and make no network calls. Both ordinary Python and optimized Python executions passed and produced byte-identical JSON. Explicit runtime checks are used rather than assertions that disappear under optimization. [S18]

| Diagnostic | Recorded outcome | Evidentiary scope |
|---|---|---|
| Rational four-density identity | 1,083 exact pair identities; 171 action/amplitude recoveries | Non-even action, unknown amplitude, three offsets and three anchors; interior algebra only |
| Nonlinear finite bridges | 96 stationary solves; maximum stationarity residual 1.53e-16 | Actual Euclidean flight lengths with asymmetric cubic and quartic perturbations |
| Independent twist computations | Maximum relative cofactor/Schur discrepancy 1.61e-14 | Finite positive Hessians over six bridge lengths |
| Endpoint factorization | Largest tested log-factorization defect at 48 flights: 1.42e-14 | Four endpoint/start configurations; no uniform theorem inferred |
| Sixth-order jet isolation | 32 stationary solves; maximum smallest-endpoint coefficient error 3.97e-5 | Symmetrized finite stationary envelope, 60 flights, both varied contact types |
| Git-retention negative control | Plain directory add omits all 13 ignored native files; explicit force-add retains them | A temporary local repository, not a change to the author's repository |

The finite bridges are nonlinear stationary-action calculations, not a numerical restatement of the determinant-one matrix. Conversely, none of these finite tests proves an infinite-dimensional implicit-function theorem, all differentiated tail estimates, arbitrary smooth-remainder factorization or analytic continuation. The negative Git control is evidence about the delivery workflow, not a mathematical counterexample.

## 7. Literature and the requested significance threshold

The current version-sensitive Florio–Leguil comparison is correct. Their v5 notice removes the earlier geometric spectral-rigidity assertion after an error in Proposition 3.1, while retaining a smooth-conjugacy conclusion. The manuscript uses the retained conclusion. This correction should not be repeatedly reopened. [S02; L1]

De Simoi–Kaloshin–Leguil address analytic open billiards under symmetry and genericity assumptions. Finamore–Leguil formulate their finite-horizon Sinai rigidity result for an enriched marked length spectrum. Neither observation map is simply the present collection of signed channel laws, onsets and marked incidence data. The manuscript appropriately does not claim an unproved reduction between these experiments. This check neither establishes a priority refutation nor proves superiority of the present data. [L2–L3]

Meister–Reiß already obtain Poisson boundary experiments from nonregular regression. Thus a contrast between Gaussian and Poisson limits cannot, by itself, be the new general principle. The substantive additional work must lie in the billiard-specific nonlinear laws, the precise coarsening map and the actual comparison kernels. The manuscript cites and acknowledges this background. [S02; L4]

**R43-S1 — major editorial reservation.** The introduction now assigns the difficult and elementary parts of the argument more accurately. Even so, I am not persuaded that the combination, in its present presentation, establishes exceptional breadth or depth for a highest-level general mathematics journal. The rank-one cancellation, compact inverse modulus and final lattice matrix formula are useful but not individually compelling grounds for such placement. The physical consistency theorem is carefully formulated but non-effective and must be judged against the richer direct-position benchmark. A preservation count, page count or succession of favorable local checks cannot settle this question.

A useful substantive improvement would be a fully worked nonsymmetric periodic example or family that exhibits the measured channels, the two independent deck cycles, the signature-rigid spanning structure and the clearance conditions together. An abstract polynomial density check is not such a geometric realization. The inspected argument does not provide a worked demonstration at that level of integration. This request concerns intelligibility and significance: it is **not** a claim that the theorem's realizable class is empty, a newly imposed hypothesis, or a demand for a universal channel-discovery algorithm. The author may address the editorial reservation through a different comparably concrete demonstration of the central mechanism's reach.

The priority examination here is bounded to the named primary sources, not an exhaustive literature certification. The lack of a fatal counterexample in this review is likewise not an acceptance argument.

## 8. Concrete outstanding corrections

### R43-D1 — the repository-retention receipt is not a receipt for the committed tree

The downloaded Actions artifact contains both PDFs and their raw auxiliary/log files. Its build is real. But the products commit does not contain 13 files listed by `REPOSITORY_RETENTION.json`, including `main.pdf`, `two_collision.pdf`, both raw `.log` files and both `.fls` recorders. An authenticated fetch of the advertised `main.pdf` path at the product SHA returns 404; the source-to-product commit comparison contains no such paths. [S16]

The mechanism is directly visible. The root ignore file excludes `.pdf`, `.aux`, `.log`, `.fls`, `.out`, `.toc` and `.fdb_latexmk`. The retention workflow copies the files and writes the receipt, then runs an ordinary directory-level `git add -- ...`, without force-addition or a delivery-subtree exception. Filesystem verification before staging does not establish Git-object retention. The independent local control reproduces all 13 omissions. [S16, S18]

Correct the receipt and retain the promised products through a durable, retrievable archive or a narrowly scoped Git inclusion rule. Verify committed objects or the permanent archive after publication, rather than certifying the pre-staging directory. The existing artifact is accessible but records an expiry of December 13, 2026. The previous referee explicitly permitted an artifact or release package; committing every binary to Git is not a new requirement of this review. **The missing-Git-files finding must not be rewritten as absence of a native PDF or as compiler failure.**

### R43-D2 — current navigation still points to the earlier failed checkpoint

At the v43 source and products commits, the repository and paper README files still identify v42, its earlier author branch and its open failed-build ledger. Preserve that earlier ledger as historical evidence, but make the current entry identify the actual v43 source, build run, products location and scoped visual coverage. This is a current-navigation correction, not a reason to invalidate the mathematical revisions that v42 already made. [S16]

### Final disposition

The native-build portion of the former C2 hold is resolved. A complete, presently retrievable article exists and was independently rebuilt. The lasting-retention claim and current navigation need correction; the visual conclusion is limited to the recorded sample. No new fatal mathematical counterexample was established within the fresh coverage specified here.

**The recommendation nevertheless remains major revision, with no acceptance recommendation at the requested journal level.** The principal remaining reservation is the significance and integrated exposition of the mathematical contribution, not an invented failure of a repaired proof. Correction of delivery bookkeeping alone would not settle that reservation. No deletion of essential arguments, abandonment of the programme, arbitrary contraction of scope, or additional inter-channel registration assumption is requested. A further submission should be evaluated on the mathematics and demonstrated reach of its central observation-specific inverse mechanism, not on its revision number.
