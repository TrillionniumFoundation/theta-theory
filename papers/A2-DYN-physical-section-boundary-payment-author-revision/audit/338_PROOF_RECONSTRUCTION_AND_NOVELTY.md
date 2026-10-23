# Native338: author proof reconstruction, scope, and novelty

This note records coauthor mathematical work for the next A2-DYN author revision.
It is not a new referee report and does not represent independent human expert
certification. The native candidate is
`338_original_section_critical_fan_payment.tex`.
No inherited module was edited.

## Proved new statement

At the original radius interval \(R\in[9/20,47/100]\), let
\(\mathcal K^{\mathrm{sec}}_{m,R}\) contain every original-section critical
germ whose actual finite trajectory has positive visited incidences and
strictly positive unvisited clearances. The original return, displacement,
collision and physical roof labels are retained. At criticality
\(p_0=p_m=0\). Its positive all-label fan coefficient satisfies

\[
\sum_{x\in\mathcal K^{\mathrm{sec}}_{m,R}}\sum_\ell
 \mathfrak J(x)\beta_{\ell,y}(x)
 \le 10C_JE\left[
  (C_0H_h+\tfrac12H_v)(m-1)\sigma^{(m-2)/2}
  +2\sigma^{m-1}\right].
\]

The first term is exactly zero at \(m=1\).
Here \(\sigma=47/59\), \(E=47/6\), \(C_0=53/12\),
\(C_J=170/(18c_*)\), and \(H_h,H_v\) are precisely the canonical-source
constants from native324, with the enlarged native284 curve class.

Combine the result with the retained native322 first-witness theorem and the
native323 visited-grazing trace theorem. Every genuine physical-boundary or
original-section-boundary critical fan is then paid by

\[
B_\partial(m)=B_{\rm sec}(m)+C_{\rm pc}m\sigma^{(m-1)/2}.
\]

For every fixed real \(q\ge0\), \(m^qB_\partial(m)\to0\), uniformly in the
original radius family. This includes the original \(m^2\) collision
normalization. No uniform positive clearance guard has been inserted:
all positive clearances, however small, are covered, and exact zero clearances
are separately assigned to the already proved theorem322.

For the existing smooth observation/guard class, signed coefficients are
grouped by the actual same physical roof and exact label before applying the
triangle inequality. Their all-label total variation is at most
\(a_0b_0B_\partial(m)\). Coincident roofs are never treated as distinct.

## Mechanism and nontrivial new step

The existing regular canonical-side estimate controls the overlay of two
families of intervals and has a short-half loss
\(\sigma^{i-1}+\sigma^{m-i-1}\). It deliberately excludes the incoming
critical coefficient at \(p_0=p_m=0\).

For critical points, both endpoint momenta take the same prescribed normal
value. At a fixed original section level, distinct physical source states
cannot lie in a single monotone backward interval, and cannot lie in a single
monotone forward interval. This gives a matching, rather than an arbitrary
interval overlay. Both inverse-derivative sums are bounded by the canonical
constant \(H_h\) or \(H_v\).

The exact two-sided determinant then gives

\[
\sum_x u_x \le
 C_0\sqrt{1-b^2}\,E H_h\,\sigma^{\max(i-1,m-i-1)}
\]

on a horizontal side, and

\[
\sum_x u_x \le
 \tfrac12 E H_v\,\sigma^{\max(i-1,m-i-1)}
\]

on a vertical side. The larger half-length appears because either factor may
be bounded individually while summing the other. No stochastic independence
is asserted. This pays all shallow and deep section indices simultaneously.

The matching is essential: an exact negative control in the diagnostic script
uses one left interval of weight \(1/4\) overlapping sixteen right intervals
of weight \(1/16\). Each family has total weight at most one, but the overlay
product sum is \(1/4\), whereas the false matching bound is \(1/16\).
The new critical-root argument is exactly what excludes this multiplicity.

## Reconstruction checks

| Point | Actual check |
|---|---|
| Physical representatives | Assign all unvisited zero-clearance germs to322 first. A remaining finite path has a genuinely open physical neighborhood with its exact word. Approximate only the null artificial source cuts on the **same original source level**. |
| Original selectors | Representative points need not preserve a side's return label, because the canonical bound is over the complete physical source and is used only as a positive upper bound. The coefficient itself keeps all original labels and sector fractions. |
| Source multiplicity | One normalized collision state at index \(i\) determines its entire regular finite past and future. Translating that disk to the origin does not create lattice or word copies. |
| Both half sums | Distinct limiting source parameters have positive separation in any fixed finite family. Monotone derivative lower bounds contradict convergence of both endpoint momenta to zero if two representatives share either partition interval. |
| Null cuts | Bulk nullness is used only to choose actual regular representatives in an open one-dimensional source interval. It is never used to declare a critical trace zero. |
| Hessian coefficient | Native285 gives \(\sqrt{\det G}/R^2\le170/9\). Thus \(C_J=170/(18c_*)\). The larger eigenvalue bound \(320/9\) is unnecessary because the sum bounds complete \(J\), and sector fractions are at most one. |
| Collision-area factor | Native324 gives \(u=c_i/[A_-A_+(d_-+d_+)]\). There is one \(c_i\) and no additional \(R^{-1}\). The exact polynomial identity is checked separately. |
| Side count | Five rectangles give ten horizontal and ten vertical side occurrences. Coincident levels can only reduce the one-copy count. |
| Moving section | For \(q_R\in[49/100,53/100]\), \(2q/(1+q^2)\) is increasing. The moving horizontal lower level is \(1947599/2480200>1/200\), and the upper level is \(2132809/2561800<5/6\). |
| Endpoint horizontal sides | Every original level has absolute value at least \(1/200\); none can meet a normal endpoint. |
| Endpoint vertical sides | A fixed angle with zero momentum fixes one true state. There is at most one physical germ per side. The two endpoints together have twenty side occurrences, with weight at most \(E\sigma^{m-1}\) each. |
| Reversal | The inverse map has the same absolute lower-left derivative by preservation of \(d\alpha\,dp\). Original section labels are transported; section invariance under reversal is not assumed. |
| Simultaneous boundaries | Visited grazing first uses its proved trace theorem; unvisited tangencies next use the322 first-witness assignment; remaining section sides use338. A corner is counted once. |
| Exact \(m=1\) indexing | There is no interior source and no fractional negative-power contribution. Only the endpoint bound remains. |
| Conditioning | \(c_*^{-1}\) occurs once, in \(C_J\) and inherited \(C_{\rm pc}\). There is no additional conditioning on a section side or source mark. |
| Limits | Work at fixed \(R,m\), approximate finitely many roots, pass the local parameter to zero, exhaust positive finite subsets, then use uniform final constants. No local radius is claimed uniform in \(m\). Original outer limits are untouched. |
| Necessary scope | Strictly interior critical germs, regular constant-roof side atoms, and the complete absolutely continuous roof derivative are outside338. The subsequent coauthor339 treats a separate endpoint-arc stratum. |

## Actual inherited hypotheses

Native338 uses the source-and-branch theorem324, not merely the endpoint
momentum kernel284. That theorem uses the fixed enlarged class

\[
\mathcal W_R^u(\widehat B_{\rm cv}),\qquad
\widehat B_{\rm cv}\ge\max\{B_{\rm cv},K_{\rm mom},2C_*\},
\]

and **its own** \(\widehat k_0,\widehat\ell_*,\widehat C_g\).
The native281–283 proofs verify the physical curve, one-step expansion and
distortion requirements used in the qualified Demers–Zhang curve-sum lemma.
Native338 neither replaces those proof bodies nor certifies them through
the finite diagnostics. Independent specialist reconstruction remains a
separate evidence question.

Native326's physical-word pressure theorem is not an input here.
Native263's persistent-guard source reduction and its normalized remaining
source are also not inputs. Native338 does not imply their residual height
has vanished. The full raw pointwise LLT and four-coordinate local inverse
remain open at the existing minimal closing conditions.

## Historical novelty evidence

The diagnostic searched every one of the660 distinct preserved native TeX
blobs in `history/ALL_660_NATIVE_SOURCE_OBJECTS.tar.gz`; the archive hash,
all source hashes, matching titles and contexts are recorded in the JSON.
The final search found22 candidates containing the relevant critical,
original-section and exponential-weight language. It is a reproducible text
audit, not a formal semantic equivalence test.

The close preceding proof bodies were read:

- Native285 gives the complete unscaled critical-sector coefficient sum.
  It does not prove exponential section-critical payment.
- Native322, blob `73ab008db1b1d10fdb2f470ed4e7ed8ee68c9014`,
  pays zero-clearance marked critical fans, including simultaneous section
  contacts with such a designated unvisited mark.
- Archived alternate322, blob
  `cc6ceae6e0e12bd9206c0bfe8dcb85e6a281bc55`, explicitly leaves
  “separate section-only or pairing boundary measures” and the shallow
  same-roof source shortage outside its conclusion.
- Native324 gives complete regular punctured canonical-side charges. Its
  text explicitly states that no critical incoming fan at \(P=0\) is
  assigned zero mass by those regular statements.
- Native275's one-sided critical roof theorem supplies the actual sector
  coefficient and reversing-orbit interpretation; it does not supply the
  normalized section-source sum proved here.

The novelty is the canonical-section critical normal-root matching and its
complete normalized geometric consequence. The inherited zero-clearance
argument, existing source growth, pressure theorem, SBV decomposition and
raw-limit closing conditions are not re-presented as discoveries.

## Execution

Command:

`python research-physical/verify_section_critical_payment.py`

Result: PASS, using only Python's standard library.

The script checks exact rational constants and moving-level inequalities,
a sparse symbolic determinant identity, all32640 pairs
\(2\le m\le256,\ 1\le i<m\), exact geometric-series formulas, the \(m=1\)
case, the generic-overlay negative control, and the660-blob archival scan.
The finite exponent checks supplement the proof; the proof of the limit is
the analytic inequality

\[
(q+1)\log m-\frac{m-2}{2}\log(59/47)\longrightarrow-\infty.
\]

The all-count index sum also has the optional exact bound

\[
\sum_{i=1}^{m-1}\sigma^{\max(i-1,m-i-1)}
 \le \frac{1+\sigma}{1-\sigma}\sigma^{(m-2)/2}
 =\frac{53}{6}\sigma^{(m-2)/2}.
\]

The native statement retains the simpler \((m-1)\) bound to keep its counting
transparent. This elementary sharpening is not treated as another research
contribution.

## Discarded proof route

An earlier scratch argument attempted to put section-critical germs with
simultaneous unvisited tangencies on common displaced section levels
\(p_i=b\pm r\) or \(\alpha_i=a\pm r\), using positive physical cones.
That stronger direct statement would require a separate simultaneous-side
representativity argument. It is unnecessary here and is not relied upon.
The final proof assigns that entire zero-clearance stratum to the existing322
theorem first and works only on actual open regular physical neighborhoods.
This preserves every such trajectory while removing the additional local
representativity issue.

