# Internal author proof reconstruction: native 336--337

This document records a second-agent reconstruction of the new author's arguments. It is not an external referee report, independent human expert certification or a claim that the final raw local limit theorem is complete. The review covers `research/336_complete_physical_roof_sbv.tex`, `research/337_complete_marked_roof_jump_spectrum.tex` and the geometric lemma in `research/physical_source_draft.tex`, together with their native 260, 322, 323, 330, 332, 334 and historical 40, 92, 93, 142, 153, 164 dependencies.

## 1. Physical support and the geometric family

The inherited finite-horizon graph gives finitely many genuine center words and exact labels at each fixed (m,R). It retains all visited reflections, the first-hit rule, original section decisions, integer occupation/displacement labels and the physical sum of flight times. Rational normal and Gauss-direction charts preserve semialgebraicity. The arbitrary (C^1) endpoint and trajectory observations are not assumed tame.

One substantive ambiguity was identified and corrected during author reconstruction: all side closures and relative boundaries must be taken **fiberwise at a fixed radius** before constructing the parameterized family. Ambient closure in ((R,r,t)) could otherwise introduce a spurious entire fiber when a sheet exists only for (R>R_0). The revised geometric lemma gives the quantified fiberwise closure, uses semialgebraic projection, and notes that the actual fixed-(R) regular image is open two-dimensional with boundary of dimension at most one. The finite (C^1) decomposition then includes exceptional radius cells without adding a nonphysical source.

The use of Coste's finite and smooth cell decomposition is valid for the constructed semialgebraic family. It yields a finite (N_m) for one fixed collision count, not a bound independent of (m). A regular side with constant Gauss projection has zero angular flux; a side with varying Gauss projection can be parametrized on finitely many graph pieces. Refining by the sign of the roof derivative gives the constant/strictly monotone dichotomy. Critical configurations are separately retained rather than discarded as collision-area-null points.

## 2. Integrable side pushforwards

For a (C^1) map (gamma) with derivative nowhere zero on an interval, the derivative has constant sign, so (gamma) is injective. The substitution denominator is (|gamma'|), and the pushed density has (L^1) norm exactly (|b|_1), including complex weights. Exhaustion by compact subintervals is justified by domination with (|b|). No uniform inverse-derivative lower bound at an endpoint is needed.

A constant side produces the atom ((\int b)delta_\tau). Finitely many isolated subdivision points carry zero (b(r),dr) mass. This excludes a singular-continuous pushforward for this finite geometric side family, even with arbitrary integrable nondefinable side weights. It does not exclude an unbounded but integrable density near a turning roof.

## 3. The exact signed coefficients

The signed interface coefficient is the increasing-roof trace difference ((C^+_\ell-C^-_\ell)|d\theta/dr|). This agrees with the distributional derivative of a one-dimensional interval indicator: positive at entrance, negative at exit. The exterior **trace** is zero; the resulting boundary charge generally is not. All artificial seams cancel before taking absolute values. Coincident physical constraints must be assigned to one actual interface with its two true traces. These conventions prevent both hidden collisions and a multiplicity from duplicated descriptions.

The critical coefficient was independently recomputed in quadratic endpoint coordinates. The initial coarea multiplier is (omega/(4\pi c_*)). For (F-t_x=|y|^2/2), the full-circle radial delta integral is (2\pi/\sqrt{\det G_x}). Their product is

\[
\frac{\omega(x)}{2c_*\sqrt{\det G_x}},
\]

which agrees with the draft. Multiplication by the actual angular sector fraction and continuous one-sided weight gives the stated atom. There is exactly one conditioning factor. The positive Hessian makes this an incoming critical charge. Visited-grazing traces use the retained optical zero-trace proof in native 323; they are not set to zero solely because the singular initial set has zero area.

## 4. Complete signed derivative and its budget

Native 332 already constructs the signed distributional derivative by integration by parts with a finite full positive source budget. Its extra observation derivative contains the necessary (1/|\nabla F|) moment and the actual endpoint/phase norms. Thus regular interior differentiation remains absolutely integrable, and Fubini yields an (L^1) roof density. A continuous smooth guard does not insert a jump at a nearest-center switch.

The corrected finite geometric family accounts for every regular boundary and positive-visited critical source. Pushforward of the nonconstant sides is absolutely continuous; constant sides and critical entrances are atomic. For each exact label and physical roof, all contributions are added with signs before taking an absolute value. The total variation equality

\[
\sum_\ell\|Df_\ell\|_{\rm TV}
=\sum_\ell\left(\|d_\ell\|_1+\sum_u|a_\ell(u)|\right)
\]

follows from mutual singularity of the resulting absolutely continuous and atomic measures, also in the complex case. Its upper bound is the inherited all-label budget; no separate per-label constant is summed. Integrating this derivative from a left exterior interval gives the canonical BV representative and the exact signed jump (a_\ell(u)).

These deductions use the native 323/330/332 proof bodies at their stated scope. This reconstruction does not independently certify every historical dynamical input in the entire pipeline.

## 5. Fourier sign and full-torus normalization

With (widehat f(s)=\int e^{ist}f(t),dt), integration by parts gives (widehat{Df}(s)=-iswidehat f(s)). Therefore (-is\mathcal F=\mathcal A+\mathcal G), and (s\mathcal F-i\mathcal A=i\mathcal G), so the draft's sign is correct. At zero frequency the derivative has total mass zero because the density is compactly supported.

The exact integer vector is (ell=(k_1,k_2,n)). Integrating over the entire three-torus with factor ((2\pi)^{-3}) eliminates cross terms between distinct labels, including labels in different arithmetic residue classes. It does not replace their exact laws by a pooled observation. Averaging in roof frequency contributes ((2S)^{-1}), for (S>0). For unequal roofs the remaining scalar integral is exactly (sin(S(u-v))/(S(u-v))).

Consequently the diagonal is (sum_{\ell,u}|a_\ell(u)|^2), where the coefficient at a coincident roof was already combined with signs. Squaring artificial separate sides would give a different, incorrect answer. The finite-frequency error is bounded by the stated sinc cross sum, (2D\sqrt{\mathcal Q_S}) from Cauchy--Schwarz and the residual (mathcal Q_S). The inequalities (|a|_2\le|a|_1\le D) introduce no label count.

The elementary (L^1) approximation proof of Fourier decay applies at each fixed (m,R); the finite label sum then gives the uniformity only in torus frequency. No quantitative rate in (m,R) or roof separation follows. The coalescing-roof example correctly demonstrates the possible noncommutation of frequency and parameter limits. The result is a physical application of an elementary finite-measure Fourier identity, not a new abstract Fourier theorem.

## 6. The normalized necessary condition

At a jump in the interior of the central roof interval, both one-sided BV traces can be approached by Lebesgue points in that same interval. The finite-peak arithmetic reference is continuous in the roof coordinate at fixed discrete label and radius. Subtracting the two trace inequalities gives (m^2|a_\ell(u)|\le2E_m(M)). Multiplying by (|a_\ell(u)|) and using the complete variation budget yields (m^2\sum|a|^2\le2DE_m(M)), with exactly (m^2), not (m^4).

The smooth central cutoff is a new analytical test of the original record, not a change in its conditional law. Its derivative bound (2M_1\|\psi'\|_\infty/\sqrt m) is correct on its support, and the product rule gives the stated absolutely continuous part and jumps (chi a). The same Fourier calculation consequently applies to these cutoff densities. This last step should be described as applying that calculation to the displayed product-rule decomposition, since a label-dependent roof cutoff is not literally one of the original endpoint/phase weights in native 332.

Whenever the cutoff is nonzero its roof lies strictly inside the larger central interval. The bound for (sum|chi a|^2) follows by multiplying the trace inequality by (|a|chi^2). There is no need for a single common exceptional roof set over all radii. The spectral limit remains first at fixed (m,R), before the collision-count supremum and limit.

## 7. Inherited zero-clearance fans

Native 322 already proves the complete zero-clearance positive-visited fan payment, including shallow indices. The new draft uses it, without claiming to prove it anew. A once-only witness assignment can only reduce its positive sum. The union retains all real side sectors and exact labels. A bounded observation contributes at most (A_V); the original guard is at most one.

Summing (\sigma^{\max(j,m-1-j)}) over (j=0,\ldots,m-1) gives the bound (m\sigma^{(m-1)/2}), and the inherited constant already contains the single conditioning factor. For complex coefficient vectors,

\[
\big|\|a\|_2^2-\|a-b\|_2^2\big|
\le2\|a\|_2\|b\|_2+\|b\|_2^2
\le2DB_m+B_m^2.
\]

Thus the claimed transfer to the new signed energy is valid, including all same-roof interference with other sources. It controls neither positive-clearance critical coefficients nor the remaining continuous derivative.

## 8. Historical scope and unresolved proof

The all-660-blob keyword audit is saved in `HISTORICAL_JUMP_FORMULA_SEARCH.json`; relevant antecedents were also read in context. Historical 40/92/93 already give complete finite-count power-logarithm extraction for their subanalytic source class, so their analytic preparation plus BV already excludes a Cantor part there. Native 153 already gives signed radial boundary currents, true one-hot jumps and coincident-interface cancellation in selected charts. Native 164 already constructs the parameterized semialgebraic physical graph. Native 45 and 142 concern different averaged spectral and collar-trace objects. These ancestors must be explicitly credited.

The legitimate new scope is the full current (C^1) endpoint/trajectory and arbitrary original smooth-guard observation class, its exact complete signed physical coefficients, common geometric atom support at fixed count, and the full marked-roof Fourier energy identity with its normalized necessary consequence. No remaining localized shortage, continuous narrow-spike estimate, full raw local theorem, microscopic conditional denominator or long-time inverse Jacobian is proved by this structure alone. The drafts correctly keep those obligations open.

Final small integration checks: state (S>0); say exterior trace rather than exterior boundary coefficient; explicitly credit native 153; describe the central cutoff's Fourier consequence through its displayed product-rule decomposition. These are precision/attribution edits, with the substantive fiberwise closure repair already incorporated.
