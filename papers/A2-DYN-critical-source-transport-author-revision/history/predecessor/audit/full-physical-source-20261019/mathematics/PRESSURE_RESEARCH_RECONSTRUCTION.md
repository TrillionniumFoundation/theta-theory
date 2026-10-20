# Author research reconstruction: whole physical-word pressure

## Status

**The uniform whole-word pressure input is not closed by the present candidate.** This is a statement about the completeness of this derivation, not a counterexample to the desired pressure theorem. The proposed route has valid algebraic and geometric components, reconstructed below, but its actual-cell geometry and family-uniform cross-cell conversion have not yet been completed with the required quantifiers.

No native theorem in modules 314–315 needs to change: their full-source roof and mixed singular-multiplier proofs do not use the proposed whole-cell pressure conclusion. The candidate should remain an explicitly identified research record until its remaining geometric assertions are proved. Its conjectural lemmas must not be used as completed inputs elsewhere.

The exact candidate inspected is ../review-ci/WHOLE_PRESSURE_CANDIDATE.tex, **20,822 bytes**, SHA-256 **094c2636e96c8eb8dfe3bdba7fb3005c75603c3e6c16719014649da22906f36f**. It already labels itself an author working draft and makes its final theorem conditional. This reconstruction reads the candidate and the inherited native modules 266, 281–283 and 313; it is not a new referee report.

## The original quantity and the proposed conversion

The target remains exactly

\[
P_m(R)=\sum_{w\in\mathcal W_m(R)}
\sup_{x\in[w]_R\cap M_R'}J^sT_R^m(x),
\qquad
\sup_{R\in[9/20,47/100],\,m\ge0}P_m(R)<\infty.
\]

The words contain every actual lifted collision. The stable Jacobian uses Euclidean arclength in the real collision coordinates \((s,\varphi)\), and \(M_R'\) is the set regular in both infinite time directions. There is no probability normalization in this unconditioned positive sum. An arclength sum on one chosen test curve is not this whole-cell supremum sum.

Let \(\mathcal B_n\) denote the proposed connected backward partition, including the current homogeneity strip and all required actual past cuts through time \(-n\). With \(y=T_R^n x\), define

\[
k_n(y)=J^uT_R^{-n}(y),\qquad
r_n(y)=c(T_R^{-n}y)k_n(y),\qquad
A_n(B)=\sup_{B\cap M_R'}r_n,\qquad
S_n=\sum_{B\in\mathcal B_n}A_n(B).
\]

The new route aims to control \(S_n\) by finitely many transverse tests for long cells and a summable succession of short cells. It would avoid a radius-dependent mixing-time argument. Its success requires a precise geometric conversion between those actual planar cells and the curve class already verified in modules 281–283.

## Primary theorem scope checked

The author-hosted primary text of [Baladi–Demers, Thermodynamic formalism for dispersing billiards](https://faculty.fairfield.edu/mdemers/research/2022.09.19.thermo.postultimate.proofed.pdf) was opened and its Lemma 2.2, partition (2.4), and proof (2.5)–(2.8) were read. Lemma 2.2 compares Jacobians on different short homogeneous stable curves inside one specified backward cell; it excludes true singular points. Its statement is for a fixed billiard table. A uniform radius-family constant requires reconstruction of the geometric constants in that proof, especially its two-sided-cell distance estimate. A fixed-table statement alone does not supply that family estimate.

The primary [Demers–Zhang text, A functional analytic approach to perturbations of the Lorentz gas](https://arxiv.org/pdf/1210.1261), Lemma 3.2(b), was also opened and checked. It bounds the sum of contraction suprema in the inverse partition of a stable curve. Its proof identifies the common curve, expansion and distortion data as its inputs. The candidate uses exactly this curve statement through the already completed native application in module 283. Neither its quantifier over curves nor its uniformity over an admissible map family is a theorem about every planar cylinder supremum.

Only these limited facts are taken from the external texts here. The calculations and conditional implications below are reconstructed directly from the current candidate and the stated native physical identities.

## 1. Exact incidence-weighted conversion to physical words

### Proposition 1: the cocycle identity and pressure reduction

Write \(j_n(x)=J^sT_R^n(x)\), \(u_n(x)=J^uT_R^n(x)\), and
\(e(x)=|\sin\angle(E^s(x),E^u(x))|\). The already proved native area identity is

\[
u_n(x)j_n(x)\frac{e(T_R^n x)}{e(x)}
=\frac{c(x)}{c(T_R^n x)},
\qquad e_0\le e\le1,\quad e_0=\frac{2(100/47)}{19^2}.
\]

Since \(k_n(y)=u_n(T_R^{-n}y)^{-1}\), multiplication by the initial incidence gives the exact relation

\[
r_n(y)=c(y)j_n(T_R^{-n}y)\frac{e(y)}{e(T_R^{-n}y)}.
\]

It also gives, for all integers \(l,j\ge0\),

\[
r_{l+j}(y)=r_l(T_R^{-j}y)k_j(y).
\]

The index convention is correct, including the empty cocycle. The terminal incidence \(c(y)\) is a necessary part of this formula.

Assume only that each backward partition cell determines its first \(n\) actual past symbols. The already native one-step inequality \(j_1(y)\le6400c(y)\) implies

\[
j_{n+1}(x)
\le6400c(y)j_n(x)
\le\frac{6400}{e_0}r_n(y),\qquad y=T_R^n x.
\]

For a word of length \(n+1\), choose a sequence of regular points approaching its stable-Jacobian supremum. At its time-\(n\) image, the past cell determines the first \(n\) physical symbols. There are at most \(D\) choices for the final symbol, so no cell receives more than \(D\) distinct selected full words. There are only finitely many physical words at each finite count. Sum the displayed positive inequality for these choices and then take the supremum approximations. This proves

\[
P_{n+1}(R)\le\frac{6400D}{e_0}\,S_n(R).
\]

This reduction is valid without assuming a pressure bound. It shows exactly which weighted planar sum the proposed geometric route must control. Omitting the final incidence would change that required sum and destroy the later homogeneity summation.

## 2. A complete elementary lemma for rectangle restrictions

### Lemma 2: connected monotone bands remain connected after a physical coordinate rectangle cut

Let \(v>0\), \(I\) be an interval, and \(g_-,g_+:I\to\mathbb R\) be nondecreasing \(1/v\)-Lipschitz functions with \(g_-<g_+\). In coordinates

\[
h=\varphi+vs,
\]

let

\[
B=\{(h,s):h\in I,\ g_-(h)<s<g_+(h)\}.
\]

Intersect \(B\) with any open coordinate rectangle
\(s_-<s<s_+\), \(\varphi_-<\varphi<\varphi_+\).
The intersection is empty or a connected band of the same type.

**Proof.** In \((h,s)\), its lower and upper fiber bounds are

\[
\ell(h)=\max\{g_-(h),\,s_-,\,(h-\varphi_+)/v\},
\qquad
u(h)=\min\{g_+(h),\,s_+,\,(h-\varphi_-)/v\}.
\]

Maxima and minima of nondecreasing \(1/v\)-Lipschitz functions have the same properties. Nonemptiness of the fiber is equivalent to every lower candidate being smaller than every upper candidate. The original inequality \(g_-<g_+\) already holds on \(I\). The new conditions reduce to:

\[
g_-<s_+,\quad s_-<g_+,\quad
g_- -h/v<-\varphi_-/v,\quad
g_+ -h/v>-\varphi_+/v,
\]

together with the two constant-rectangle bounds on \(h\) and inequalities depending only on the nonempty side lengths.

The first two conditions define half-intervals because \(g_-\) and \(g_+\) are nondecreasing. The next two also define half-intervals because \(g_\pm(h)-h/v\) are nonincreasing. The linear conditions on \(h\) define intervals. Their intersection with \(I\) is therefore an interval \(I'\), possibly empty. Continuity makes the strict positivity region open relative to \(I\). Over \(I'\) the fiber is precisely \((\ell(h),u(h))\).

The continuous middle graph \((\ell+u)/2\) connects every nonempty fiber to every other one, so the resulting band is connected. This proves the assertion. \(\square\)

This closes the rectangle-connectivity substep in the candidate **once the actual cell has the claimed band description**. It does not prove that description for the full physical backward partition. Arbitrary monotone graphs can cross repeatedly; the argument uses the extreme slopes 0 and \(1/v\) of the added rectangle constraints, not an incorrect claim that two increasing graphs cross at most once.

### Consequence for the claimed short-cell diameter

If an actual band has fiber width at most \(L_n\), then for any two of its points

\[
|s-s'|\le v^{-1}|h-h'|+L_n,\qquad
|\varphi-\varphi'|\le2|h-h'|+vL_n.
\]

Thus its Euclidean diameter is bounded above by

\[
(2+v^{-1})|I|+(1+v)L_n.
\]

If the fiber lies in one true inverse branch, its pullback is a cone-stable curve. The inherited adapted expansion and the bounded angular range give the proposed \(L_n\le C_s\Lambda^{-n}\), with a fixed generous \(C_s\). This implication is valid; the physical hypothesis that every fiber has that single regular inverse branch must still follow from the complete actual-cell description.

## 3. What the planar first-hit calculation does establish

The local first-hit part is more informative than a generic curve-slope argument. It supplies the following exact geometric facts.

Use the real oriented-line variables

\[
\vartheta=s/R+\varphi,\qquad b=-R\sin\varphi.
\]

For a candidate center \(z\), a terminal incidence level or tangency level is a graph

\[
b=z\cdot v_\vartheta^\perp-a,\qquad |a|\le R.
\]

For distinct candidate centers, the difference between two such graphs is
\(d\cdot v_\vartheta^\perp-a'\), where
\(|d|\ge1\) and \(|a'|\le2R_+<1\). Its successive zeros are separated by at least \(2\arccos(2R_+)\). Thus on an angular interval shorter than \(1/10\), any pair has at most one zero. A repeated zero cannot occur because it would require \(|a'|=|d|\). The same-center comparison is constant. Consequently each comparison of a selected upper and lower candidate graph restricts the angular coordinate to an interval or half-interval.

A physical positive-cone boundary of slope \(V\ge0\), expressed as \(b=\beta(\vartheta)\), has

\[
\beta'(\vartheta)=-\frac{RcV}{R^{-1}+V}\in[-Rc,0].
\]

At its intersection with a relevant candidate graph,

\[
\frac{d}{d\vartheta}
(z\cdot v_\vartheta^\perp-a-\beta(\vartheta))
\le-z\cdot v_\vartheta+Rc=-t_z.
\]

For a positive disk-contact foot, the actual exclusion geometry gives
\(t_z\ge\sqrt{1-2R_+}>0\). Hence the comparison crosses in only one direction. This is stronger than mere monotonicity of the individual graphs.

**Conditional connectivity consequence.** Suppose the local source restriction is already known to be bounded by complete graphs of this class and to have connected angular projection, with every relevant candidate foot remaining positive. Restrict to a sufficiently small angular interval so that the above crossing properties hold. Selecting one first-hit center and one target strip imposes finitely many graph upper/lower inequalities. Nonemptiness of the vertical fiber amounts to their pairwise comparisons; these define intervals. The resulting set is a connected band or is empty. This proves at most one connected piece for that center and strip under the stated source geometry.

The inherited strong finite-horizon argument supplies a persistent first strict disk for every limiting outgoing ray, including a ray initially grazing or tangent to earlier disks. Earlier near-tangent alternatives have terminal incidence tending to zero and cannot produce an \(H_0\) piece after the neighborhood is reduced. The strict disk prevents a later disk from becoming the first hit there. These facts support the proposed bound of at most one central \(H_0\) component and a finite number of components per grazing strip.

The missing step is the uniform application of this calculation to **every actual planar backward cell and all the refinement descendants used in renewal**, with the precise boundary and angular-projection properties. Module 282 established the corresponding result for admissible curves. That already completed curve result does not by itself establish this larger planar source class.

If the planar component bound is obtained, the actual adapted contraction already proved in module 282 gives

\[
\sum_{\text{complete children}}\sup J^{u,*}T_R^{-1}
\le\Lambda^{-1}
+\frac{J_f}{a\tau_-(k_0-1)}
=\theta<1.
\]

The grazing contribution includes both signed strips. The norm conversion belongs at the endpoints of a whole chain and costs \(\Gamma\), rather than \(\Gamma^j\). The analytic summation is valid; a curve one-step estimate cannot simply be relabeled as this whole-cell sum.

## 4. The finite transverse tests have the correct incidence payment

### Proposition 3: long-cell payment under a precise geometric comparison

Assume:

1. Every current backward cell has the claimed band description in its actual previous-center chart, and the set of its \(h\)-values is an open interval.
2. The actual cross-cell comparison holds uniformly: inverse Jacobians on short homogeneous stable curves in one backward cell differ by at most \(C_{\rm cell}\), independently of \(R,n\).
3. The inverse curve partition on a test cuts every actual backward boundary distinguishing two assigned cells.

For \(v=95/9\), call a cell long when its \(h=\varphi+vs\) interval has length at least \(\delta>0\). There are at most \(N_f\) actual previous-center charts. Their total \(h\)-range is bounded by \(\pi(1+vR_+)\). In each chart choose a translated grid of mesh \(\delta/3\), with at most

\[
N_h=3+\left\lceil3\pi(1+vR_+)/\delta\right\rceil
\]

relevant levels. Every long open interval meets a level in its interior. Cut the resulting affine stable lines into current homogeneity strips and short admissible curves. Their curvature is zero and their slope belongs to the inherited stable cone. The number of short subdivisions per level and strip is bounded by a fixed \(N_s\).

For each fixed radius, Fubini permits a generic grid translation for which \(M_R'\) has full arclength on every one of the countably many tests. The translation is chosen once for all \(n\). A common translation for all uncountably many radii is unnecessary.

Assign each long cell to its first intersected test and one inverse component there. The hypotheses make this assignment injective among cells sharing a test. At a regular \(y\) in a cell \(B\subset H\), use a short affine curve tangent to the actual stable line at \(y\). Uniform whole-cell comparison and the exact area identity then give

\[
A_n(B)
\le e_0^{-1}C_{\rm cell}(\sup_H c)
\sup_{V}J_VT_R^n.
\]

The already proved curve-growth estimate bounds the sum over inverse components of each test by \(C_g\), including arbitrarily short strip intersections. Finally

\[
C_H:=\sum_{H\in\mathcal H}\sup_H c
\le1+2\sum_{k\ge k_0}k^{-2}<\infty.
\]

It follows that

\[
\sum_{B\text{ long}}A_n(B)
\le e_0^{-1}C_{\rm cell}N_fN_hN_sC_gC_H=:L_*.
\]

This is a correct conditional conversion and it covers every high grazing strip. Dropping \(\sup_H c\) before the strip sum would leave an infinite number of tests without payment. Conversely, imposing a finite strip cutoff or assuming a positive fraction of long cells is not needed in this conversion.

## 5. The renewal algebra is complete under its actual-cell hypotheses

### Proposition 4: last-long-ancestor summation

Assume the long-cell bound \(L_*\), a uniform short-cell one-step adapted sum \(\theta<1\), and closure of the actual refinement class under the rectangle cuts and images used in the candidate. Let \(M_0\) bound the number of initial small rectangles needed for one source chart. Let \(n_0\) be fixed so that every short actual cell with past length at least \(n_0\) has diameter smaller than the one-step geometric scale.

Starting with a short cell, every chain with no later long cell consists entirely of small sources. Positivity, the exact cocycle, and the one-step sum give an adapted \(j\)-step relative sum at most \(\theta^j\). The endpoint conversion gives \(\Gamma\theta^j\) in Euclidean arclength. Starting with a long cell costs at most one initial \(M_0\), since every later original cell on the selected chain is short. The rectangle lemma above justifies connectedness of the initial cut if the band hypothesis holds; the closure hypothesis ensures each later refined component remains in the same admissible planar class.

A finite initial bound is obtained by such a fixed subdivision at every step:

\[
S_l\le K_0^lC_H,\qquad K_0=\max\{1,\Gamma M_0\theta\}.
\]

When an original component meets several refined pieces, its supremum is at most the sum of their suprema. This is a valid positive overcount; no common lower mass or independence is assumed.

At time \(n\ge n_0\), every short cell has either no long ancestor since \(n_0\) or a unique last long ancestor. Its actual past itinerary determines that ancestor. The cocycle then yields

\[
S_n\le L_*+\Gamma\theta^{n-n_0}S_{n_0}
+\Gamma M_0\sum_{j=1}^{n-n_0}\theta^j
\sum_{\substack{B\in\mathcal B_{n-j}\\B\ {\rm long}}}A_{n-j}(B).
\]

Consequently

\[
S_n\le L_*+\Gamma K_0^{n_0}C_H
+\Gamma M_0L_*\frac{\theta}{1-\theta}.
\]

The finitely many smaller \(n\) use the initial budget. Proposition 1 then gives the desired bounded pressure. This implication is exact. Its conditionality lies in the actual planar geometry and cross-cell comparison, not in an unsummed residual at the last-long step.

## 6. Minimal unclosed geometric conversion

### A. Complete actual barriers and every endpoint

The candidate proposes extending each introduced boundary along an older one at its endpoints. A complete proof must establish, for the exact partition, all of the following:

- Every regular arc endpoint lies on a specified older genuine image boundary or the physical cylinder boundary, including simultaneous grazing and homogeneity endpoints.
- Introduction time, with a precise tie convention for genuine and homogeneous cuts, decreases at every extension switch.
- The extension is monotone in the chosen \(h\)-chart, creates no added physical cut, and is valid at the chart boundary selected by the previous-center displacement.
- Countable strip limits introduce no additional regular interior endpoint or omitted open fiber.
- Complementary connected components are exactly the bands used in the tests; the same statement is preserved by the positive refinement images.

Positive slopes alone prove none of these endpoint and global partition assertions. The proposed finite-age continuation is a plausible mechanism, but the current paragraph does not yet supply a full proof for every simultaneous singular endpoint and every resulting physical component. This is the precise source-class question to finish before the local planar calculation can be applied globally.

### B. Uniform two-sided-cell geometry for distortion

The needed assertion is a constant \(C_b\), uniform in the actual radius family, such that for every relevant backward homogeneous cell, every \(u,v\) in its regular closure, and \(0\le i\le n\),

\[
d(T_R^{-i}u,T_R^{-i}v)
\le C_b\bigl(\Lambda^{-i}+\Lambda^{-n+i}\bigr).
\]

The published fixed-table cross-cell lemma uses such a two-sided geometric bound. It is not enough to have bounded distortion along each single curve, nor to assert that cone transversality automatically converts the two intrinsic curve diameters for an arbitrary planar set. A very thin horizontal rectangle, for example, can have short stable- and unstable-cone segments while retaining substantial horizontal diameter. This is only an elementary geometric warning; it is not a claimed physical cell counterexample.

A potentially useful route, discussed with the other author agent, is to pass from a homogeneous cell to its containing **true, unhomogenized two-sided cell**. Only the genuine opposite-cone boundaries remain there; narrow artificial horizontal strips no longer supply the problematic geometry. One must then prove a uniform cone-path/diameter comparison on that true parent cell, with the original singular endpoint and cylinder-boundary conventions. Hyperbolicity would give the two exponential lengths. This route is still a proof obligation, not an established replacement lemma.

A concrete construction to test is the following. Express that true parent between increasing past barriers with slopes in \([a,K]\) and decreasing future barriers with slopes in \([-K,-a]\). At the midpoint of an \(s\)-projection of width \(L\), endpoint feasibility may force opposite-family gaps to have size comparable to \(aL\). A thin same-family band could then be followed by its midpoint cone graph through the wider opposite-family constraints; if neither band is thin, a cone segment should fit directly. Proving a length lower bound \(c(a,K)L\), and the corresponding vertical-diameter bound, would supply the desired conversion. The endpoint feasibility estimates, cylinder caps and complete genuine-barrier extensions still need a full proof; this paragraph records a construction for further work and asserts none of those missing estimates.

Once this estimate is actually obtained, the analytic part of the distortion argument is adequate: the original \(q=2\) strips give the \(1/3\)-Hölder logarithmic incidence comparison, the disk entry formula gives a uniform square-root modulus for the flight, and the native slope transform has contraction at most \(47/48\). The Euclidean endpoint norm factors telescope, and the two-sided exponential sums converge uniformly. It is the physical-cell geometry feeding these sums that remains to be completed.

### C. Planar component theorem and refinement closure

After A, the crossing calculation in Section 3 gives a concrete route to the needed at-most-one central component and finite grazing-component count. A final proof must apply it to the complete actual planar source class uniformly at limiting grazing states and verify that the small-diameter cover has a common Lebesgue number in radius and state. The inherited curve theorem only established this for one admissible graph at a time.

The refinement class must then be stated so that each descendant used in Proposition 4 retains complete positive barriers and a single counted first-hit/homogeneity component. Lemma 2 removes the rectangle-intersection concern under the band hypothesis. It does not replace the missing proof that every forward refined component has the required actual geometry.

## 7. Author integration decision

Preserve the candidate and this reconstruction as a research record. Retain the independently verified propositions and the explicit rectangle proof as useful completed components. Keep A–C as the minimal outstanding geometric conversion for this route, with B especially distinguished from ordinary curve distortion.

There is no justification at this stage for promoting \(Q_*\) to an independently completed radius-uniform theorem, changing the source event, discarding high strips, or treating a finite branch calculation as the full planar pressure proof. There is also no reason to weaken the original pressure objective: the weighted transverse-grid mechanism retains all strips and the exact last incidence, and its renewal conclusion would close the required positive sum if the physical geometric conversion is completed.

No existing article, native proof module, workflow, commit or remote ref was changed by this reconstruction. No sampled trajectories, floating-point plots or CI outcome were used to decide the continuum geometric assertions above.
