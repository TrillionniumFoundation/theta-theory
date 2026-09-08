# Independent referee report: A2, Round 33

## Recommendation: reject at the requested top-four mathematics-journal standard

**Review date:** September 8, 2026.  
**Reviewer:** GPT-6 Astra Pro, acting as an independent AI-assisted referee at the repository owner's request. This is not a commissioned report or an editorial decision of Annals of Mathematics, Inventiones Mathematicae, the Journal of the American Mathematical Society, or Acta Mathematica.

**Manuscript actually reviewed:** *A2: Arithmetic and Fourier-Inversion Budgets — Round 33 proof reconstruction*.  
**Reviewed revision carrier:** `revision/round53-bound-certificates-energy-robust-posterior-2026-09-05`.  
**Immutable carrier commit:** `7f1bc9a42ba27615aea61afb9a417ef076e2c6e1`.  
**Last change to the active A2 chapter on that lineage:** `7bb555662a572bd400fbfb0d6011a812ad578593`, September 3, 2026, 00:53:57 UTC.  
**Active proof source:** `round33/chapters/A2.tex`, Git blob `2213344f8efa895b4674f818d404c5d4a9af9da1`.  
**Entry chain:** `papers/A2-sinai-homological-pressure/main.tex` → `ROUND33_REVISION.tex` → `../../round33/chapters/A2.tex`.  
**New review branch:** `review/a2-round33-harsh-independent-2026-09-08`.

### Executive assessment

The active chapter contains a valid elementary algebraic-number estimate and a coherent conditional Fourier-inversion argument. I do not identify a fatal counterexample to either of its two labelled statements under their intended fixed-constant hypotheses. The defect decisive for the requested publication level is different: the chapter does not establish the singular mechanical theorem that would turn these estimates into the proposed A2 research contribution, and it does not establish an independently substantial originality case for the replacement abstract results.

This is not an invitation to fix a sign, add a few citations, and declare the original Sinai theorem proved. The unresolved model estimates contain the central mathematics. Conversely, a conditional statement is not false simply because its intended application has not been established. Both distinctions matter in a harsh but mathematically defensible report.

The appropriate recommendation is **rejection of the present A2 as a top-four-journal research submission**, while preserving the corrected arithmetic and inversion lemmas as supporting material. A future paper need not solve the entire eleven-paper programme; it must supply one substantial, precisely delimited new theorem and actually prove the hypotheses on which that theorem depends.

## 1. Version identity is a substantive part of this review

The repository has diverging manuscript lines. The accessible branch search for `a2`, including its continuation, returned the September 8 workstream branch, not an A2-named revision branch. The revision search was also continued to exhaustion. On the most recent numbered programme-revision carrier inspected, the A2 entry still selects Round 33; the carrier's Round 53 number belongs to a later identification manuscript, not to an A2 Round 53 theorem.

The September 8 A1 v36 revision has a different A2 entry, selecting the older Round 17 text and retaining its much stronger raw local-limit abstract. A newer date on an A1 branch does not make that retained A2 text a new revision of A2. The unchanged README title, *Homological Liouville Path Ensembles and Projective Empirical-Process Large Deviations*, likewise cannot override the active TeX entry chain on the reviewed carrier.

There is also genuinely newer A2-related work: `workstreams/2026-09-08-next-step/research/A2_Two_Collision_Response.tex` at `e8d3b658ead4996dabfc9f31a07b812e070f5446`. Its own index calls it a finite-time technical note and explicitly excludes a full-path or long-time theorem. I read that note and review it separately on `review/a2-two-collision-harsh-independent-2026-09-08`. It is neither silently substituted for this revision nor counted as a proof of the original programme.

These observations are source-selection findings, not accusations about author intent. The next author-facing A2 release should contain a single source-pinned submission index explaining which of these objects is being offered for review.

## 2. What the active statements do and do not prove

| Source locator | Mathematical content | Assessment |
|---|---|---|
| `prop:r33-a2-arithmetic` | A polynomial separation estimate for three specified vectors, for continuous frequencies with norm at least one | Coherent; checked independently below |
| Paragraph following the arithmetic proof | Six scalar data require a suitable realization map or explicit reductions | Correct warning; no realization theorem is supplied |
| `thm:r33-a2-integral` | Four assumed characteristic-function bounds imply a negligible noncentral integral | Correct comparison argument under the stated strict exponent budget |
| “What an Edgeworth input must actually say” | An additional central integrable remainder yields a mixed density expansion | Conditional implication, not an established billiard expansion |
| “Explicit nonempty probabilistic benchmark” | Bernoulli lattice increments and independent Gaussian increments realize an elementary test family | Useful non-vacuity example; centering should be made explicit |
| “Mechanical application still to be established” | Stable-curve spaces, periodic data, cancellation, bad-word estimates, and differentiated remainders remain absent | This is the central unresolved research obligation |

A claim ledger should retain these different logical statuses. A passed arithmetic test is not a passed billiard spectral theorem; an integrable envelope is not the construction of the characteristic family to which it is to be applied.

## 3. Independent arithmetic verification

Write

$$\alpha=k-m\sqrt2-n\sqrt3.$$

The exact field norm is

$$N_{\mathbb Q(\sqrt2,\sqrt3)/\mathbb Q}(\alpha)
=(k^2+2m^2-3n^2)^2-8k^2m^2.$$

It is an integer and is nonzero whenever $(m,n)\ne(0,0)$. Rational independence of $1,\sqrt2,\sqrt3$ is exactly the point needed here. There are four embeddings, so controlling the other three conjugates produces the exponent three in the manuscript. The diagnostic script verifies the polynomial identity symbolically and checks 880 finite integer triples; those examples are supplementary, not the proof of rational independence or the all-frequency estimate.

One can make the displayed existence constant explicit with crude bounds. Put $r=|b|\ge1$, $H=1+r$, and let $\delta$ be the Euclidean distance to $2\pi\mathbb Z^3$. For a nearest triple and $\delta<1/10$, the three residuals give

$$|\alpha|\le\frac{\sqrt6}{2\pi}\delta.$$

Also

$$|m|,|n|\le\frac{H}{2\pi},\qquad
|k|\le\frac{\sqrt5H}{2\pi}.$$

Every other conjugate has modulus at most

$$\frac{\sqrt5+\sqrt2+\sqrt3}{2\pi}H<H.$$

Thus $1\le |N(\alpha)|\le |\alpha|H^3$ and $\delta\ge (2\pi/\sqrt6)H^{-3}$. The case $m=n=0$ is impossible in this small-distance regime because it would imply $|b|\le\delta$. In the complementary regime $\delta\ge1/10$, the lower bound with constant $c=1/2$ is immediate from $H\ge2$. Consequently the proposition can, for example, be stated with $c=1/2$.

This verification supports the repaired result; it also illustrates the elementary nature of this part of the contribution. The proof does not construct a billiard periodic orbit with these prescribed observables. In particular, three vectors in $\mathbb R^2$ cannot be treated as freely assignable using an unspecified three-scalar parameter family. One must identify the independent constraints and prove the required rank for an actual parameter map.

The non-openness qualification is also correct. Perturbing the first coordinate of $(\sqrt2,\sqrt3)$ to $p/q$ produces an annihilating character $b=(2\pi q,0)$ for the perturbed data. This does not invalidate the estimate at the exact displayed algebraic data; it prevents unrestricted robustness from being inferred from that example.

## 4. Independent Fourier audit

The four regions in the argument have the required sizes. With $\delta_N=N^{-2/5}$, the low-frequency annulus contributes an exponentially small quantity because $N\delta_N^2=N^{1/5}$. A fixed compact annulus has bounded volume. The region $B<|b|\le N^A$ has polynomial volume, so its stretched-exponential bound is integrable with a super-polynomial gain. In the final region,

$$N^v\int_{N^A}^{\infty}r^{d_C-1-M}\,dr
=\frac{N^{v-A(M-d_C)}}{M-d_C}.$$

The strict inequality

$$A(M-d_C)>v+d/2+1$$

is exactly sufficient for the claimed little-oh bound. At equality the envelope calculation would give only the corresponding big-oh order. This is a statement about the budget calculation, not a constructed counterexample within the class of characteristic functions. The diagnostic script checks both exponent relations exactly.

The central rescaling is consistent as well: $t=\sqrt N\,\xi$ transforms $|\xi|\le N^{-2/5}$ into $|t|\le N^{1/10}$ and introduces the factor $N^{-d/2}$. An $o(N^{-1})$ integrated remainder in the scaled variables therefore gives the asserted absolute order. Including the Riesz amplitude in the Edgeworth coefficients is necessary and is correctly acknowledged.

No estimate in this argument establishes that the actual billiard family satisfies the four input bounds or the central remainder hypothesis. In particular, a normalized transfer operator has $L_0^N1=1$; decay for a matched-branch difference or a return-time layer cannot simply be substituted for the full characteristic matrix coefficient. The revised chapter now makes that distinction, and I do not repeat the earlier allegation that it suppresses the central projection.

### Local statement repairs

The following are relatively small compared with the missing application, but should be settled in any formal statement.

First, the Bernoulli/Gaussian formula printed in the benchmark is uncentered. For the centred Bernoulli sum it should contain the phase factor $e^{-iNpu}$. This leaves the modulus unchanged but affects the central expansion, the translated lattice support, and parameter derivatives. The text already warns that centering creates powers of $N$; the benchmark should implement that warning explicitly.

Second, a self-contained mixed inversion theorem should specify the lattice and its covolume, the reference measure for the density, translated lattice cosets after centering, and positive definiteness of the Gaussian covariance. “The corresponding expansion” is not a substitute for the actual normalized conclusion.

Third, the orders of the source derivatives, the parameter set on which constants are uniform, and the signs and fixed nature of $A,M,v,q$ should be explicit. I interpret the present estimate in its conventional asymptotic regime, with $A>0$ and constants independent of $N$. These are statement-precision requests, not evidence that the repaired power counting is false.

## 5. Blocking research obligations

**A2-R1 — No established model-level root theorem.** The original homology/return/roof programme needs a specified mechanical family and a theorem about that family. The current source explicitly leaves the difficult mechanical inputs unproved. The replacement title is more accurate, but a title change does not discharge those obligations.

**A2-R2 — Arithmetic is not realization or dynamical cancellation.** The algebraic example establishes separation for chosen vectors. It supplies neither a periodic-data realization map nor uniform returned non-integrability. These tasks cannot be closed by a numerical certificate of the displayed radicals.

**A2-R3 — Operator estimates and derivatives remain unconstructed.** The actual stable-curve spaces, source-dependent multiplication operators, singularity transport, uniform return and bad-word bounds, and the relevant matrix coefficients must be defined and estimated. Declaring a function to obey a four-region budget moves the main proof into hypotheses.

**A2-R4 — The raw mixed density/Edgeworth conclusion remains conditional.** A central spectral expansion with an integrated, source-differentiated remainder must be proved on those spaces, together with the required lattice and covariance properties. Neither a central limit theorem nor continuity of a perturbed spectral projection automatically provides this package.

**A2-R5 — Independent significance is not demonstrated.** The active arithmetic proof is a field-norm argument and the Fourier theorem integrates explicitly assumed envelopes. I find no demonstrated new phenomenon, decisive improvement, or model application that elevates this combination to the requested journal level. This is an assessment of the submitted contribution, not a claim to have proved that every possible refinement is already in the literature.

The previous Round 34 report at `9f5276233b63218a0d89df6611381975dc873232`, Section 4.2, already distinguished the sound arithmetic/inversion lemmas from the absent model theorem. My independent checks support that distinction. The carrier's later commits do not constitute an A2 response to it: the active chapter's last-change commit remains the Round 33 commit given above.

## 6. Why the September 8 collision note does not close these items

The newer note establishes finite-time count probabilities using

$$J(R)=\int(T-\tau_R)_+\,d\nu,\qquad T=0.11.$$

The window is below twice the minimum inter-obstacle gap. Its count law consequently depends on the one-roof marginal and the stationary intensity, not on iterates of the collision map in a long characteristic family. The proof of smoothness is localized to uniformly transverse short flights and a regular terminal level.

These are real mechanical calculations. They do not supply the periodic-data realization, differentiated transfer-operator bounds, or central remainder required in this chapter. The newer note says so itself. It would be unfair to accuse that note of claiming the full result; it would be equally incorrect to certify the full result by citing the note.

The separate report contains an exact pair of stationary suspensions with identical two-event-window laws but different three-event probabilities at a longer window, as well as an onset calculation showing why fixed-window smoothness cannot automatically be extended through all collision thresholds. These are logical scope tests, not counterexamples to the new note's printed Lorentz-gas theorem.

## 7. Literature positioning

Three primary sources were checked for their actual stated scope.

Demers and Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, arXiv:1210.1261, develops transfer-operator methods for perturbations, including movements and deformations of scatterers, and proves continuity of spectral data. It is relevant context for the missing construction; its stated continuity result is not the source-differentiated raw Edgeworth theorem sought here. [Primary source](https://arxiv.org/abs/1210.1261).

Demers, Melbourne and Nicol, *Martingale approximations and anisotropic Banach spaces with an application to the time-one map of a Lorentz gas*, arXiv:1901.00131, establishes martingale approximation and statistical limit laws for Hölder observables. Its scope must not be relabelled as the stronger mixed density theorem. [Primary source](https://arxiv.org/abs/1901.00131).

Marklof, *Entry and return times for semi-flows*, arXiv:1605.02715, explains the stationary point-process and Palm framework relevant to the newer collision-count identity, including non-ergodic settings. That framework does not itself provide parameter differentiation for long billiard histories. [Primary source](https://arxiv.org/abs/1605.02715).

This is a targeted comparison, not an exhaustive priority certification. The next submission needs a theorem-by-theorem comparison of its genuinely new result with the closest applicable primary results.

## 8. Re-review requirements and execution record

A serious re-review should receive a single source-pinned A2 submission, a precise principal theorem, and a dependency table distinguishing proved inputs from conditional implications. If the intended theorem is the original singular mechanical local-limit result, its actual spaces, realization, cancellation, and integrated remainder must be supplied. If a different substantial theorem is proposed, it must stand on its own significance; another elementary benchmark is not enough.

The companion `diagnostics.py` was written independently for this review. It imports no repository code and makes no network calls. Its 31 named checks passed under normal Python and under `python -O`; the resulting JSON files were byte-identical. The exact checks include the algebraic norm identity, exponent budgets, and 333 direct suspension-length comparisons. The floating checks use a new oriented-line quadrature and separately compute the bulk and level contributions to the newer note's second derivative.

These diagnostics are not a formal proof certificate. I did not replay the author's complete test suite, rebuild the manuscripts, inspect their PDF pages, run remote CI, or certify literature priority. The frozen TeX sources and the relevant historical report were read through the connected repository. No mathematical source, existing branch, review, permission, or protection rule is changed by this report.

**Final disposition:** the repaired auxiliary mathematics should be retained. A completed, original A2 contribution of the requested publication significance has not been established by the reviewed revision. **Reject at the requested top-four standard.**
