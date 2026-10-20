# External top-four referee report on A2-DYN revision 59

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v59-referee-response-2026-10-09`, `revision/a2-dyn-v59-referee-copy-2026-10-09`  
**Reviewed commit:** `69ab2afcceff0a8a2892910b335ac180678b5f4b`  
**Reviewed repository tree:** `f4d42e1572e96d848cf0fc120efcb06ff1e11d90`  
**Ordinary source payload tree:** `0093203296288b5168499eef44e64ea979e6b805`  
**Active manuscript directory:** `papers/A2-DYN-v59-referee-response`  
**Active mathematical source:** one hundred twenty-seven numbered core modules; revision 59 retains all one hundred twenty-four revision-58 modules and adds modules 125--127  
**Frozen revision-58 author baseline:** `b9c8e1f15b65e4843d1321f23ed5b816378b855c`  
**Frozen revision-58 complete paper tree:** `e7be5ba545bfc80e08c86e3c596e36b483bbedf7`  
**Controlling external report:** `reviews/a2-dyn-v58-external-top4-review-2026-10-09/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `94c9ef54bd84d9eb04fbd3b4d3431776beab64de` / `d70134c2f027a53d8bde20187a2b3b706011782c`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 59 is a genuine and mathematically substantive advance over revision 58. The preceding report accepted the flat pressure-contact theorem and the canonical common-Gaussian arithmetic reference, but made two criticisms which were particularly relevant to a possible general-theorem route:

1. the scalar root-taking and accretive-Gaussian steps were too compressed for their load-bearing role; and
2. the independent baker realization tested only an exactly Bernoulli finite-support characteristic function and did not produce a continuous density theorem or a positive source-height estimate.

Revision 59 addresses both points directly.

The new source supplies standalone physical root-taking, compact witness-cover and accretive Gaussian lemmas. It then constructs a two-state correlated Markov baker map preserving a nonuniform stationary area measure, equips it with a positive continuous deterministic roof containing an actual stable endpoint coboundary, realizes the relevant spectral branch on an infinite-dimensional Lipschitz space with a contracting quotient, and verifies a nontrivial damped peak by fixed physical witnesses.

For the unperturbed continuous roof, the manuscript proves an exact coarea density formula and the pointwise estimate

\[
 \operatorname*{ess\,sup}_{t\in\mathbb R}
 \left|\sqrt m\,p_m^{\rm M}(t)
 -g_{\sigma^2}\!\left(\frac{t-m\bar\tau}{\sqrt m}\right)\right|
 \le C\frac{\log(2+m)}{\sqrt m},
 \qquad
 \bar\tau=\frac{24}{7},\quad \sigma^2=\frac{204}{343}.
\]

It also proves direct essential-height estimates for three positive boundary sources in that model:

\[
 \sqrt m\left(
 \|p_{m,s}^{\rm vert}\|_\infty+
 \|p_{m,s}^{\rm stab}\|_\infty+
 \|p_{m,s}^{\rm age}\|_\infty\right)
 \le C\left(s+\left(\frac34\right)^{\lfloor m/2\rfloor}\right).
\]

These are true height estimates. They are not inferred from small source mass, weak integrability, local variation, or deletion of an exceptional roof set.

I audited the new modules

- `core/125_pressure_gaussian_details.tex`;
- `core/126_correlated_markov_realization.tex`;
- `core/127_stable_coarea_height.tex`;

together with their use in the new front matter and their dependence on the unchanged revision-58 pressure-contact theorem. I found no decisive counterexample, missing coarea Jacobian, state-normalization error, sign error in the centered drift, variance error, lattice-span obstruction, false independence step, or invalid transfer of a Markov height result to the Lorentz source.

In particular, the following points are internally coherent.

1. The Markov baker preserves the measure with state weights \(\pi=(4/7,3/7)\), not equally weighted area.
2. The coded states are genuinely correlated, with
   \[
   \operatorname{Cov}(I_0,I_r)=\frac{12}{49}\left(\frac5{12}\right)^r.
   \]
3. The roof sum retains the exact stable endpoint difference \(y_m-y_0\).
4. Constants on stable fibres carry the two-by-two matrix pressure, while the quotient contracts in the Lipschitz seminorm.
5. Fixed endpoint tests cancel the stable coboundary at the resonance and give a nonzero physical branch amplitude.
6. The covariance matrix, damping, maximizer and centered-drift coefficients agree with the characteristic polynomial.
7. Summing the exponentially many suffix cylinders does not multiply the lattice local-limit error by their number; their transition weights sum.
8. The exact coarea derivative is \(1-a_w\), uniformly bounded away from zero.
9. The triangular periodization identity produces the unweighted pointwise Gaussian factor exactly.
10. The boundary-source theorem uses positive cylinder upper bounds at depth \(\lfloor m/2\rfloor\), rather than the signed local-limit error.

These are meaningful achievements. Revision 59 is substantially stronger than the finite-support baker calculation in revision 58 and should not be described as a cosmetic example.

The negative top-four recommendation is nevertheless still forced by the manuscript's principal object and its remaining endpoint. Revision 59 explicitly does **not** prove either of the two Lorentz essential-height estimates. It therefore does not prove the unrestricted two-sided pointwise arithmetic raw-density theorem for the original four-coordinate return record.

The correlated Markov realization identifies one sufficient mechanism for source-height control: a word-uniform coarea derivative together with positive exact-count cylinder bounds. That mechanism is proved for the model. It is not proved for Lorentz incidence or competing-hit clearance, where grazing, singularity proliferation, competing collision roots, image-side marking and preservation of the exact return labels are the central difficulties.

The generality route has improved, but it has not yet reached the requested benchmark. The new system is still an explicitly solvable finite-state Markov additive process with a bounded stable coboundary. Moreover, the moving damped-peak theorem is established for the \(\epsilon\)-family, while the pointwise density and boundary-height theorem is stated only at \(\epsilon=0\). The source is transparent about this separation. It nevertheless means that pressure contact, moving arithmetic type and pointwise height are not yet controlled simultaneously in a genuinely nontrivial family.

At the requested four-journal level, the article would need either

1. completion of the Lorentz incidence and clearance height estimates and hence of the unrestricted pointwise theorem which governs the title and much of the one-hundred-twenty-seven-module architecture; or
2. a substantially broader abstract source-height theorem, verified in multiple systems where the coarea and cylinder hypotheses are themselves nontrivial and not reducible to finite-state Markov coding.

Revision 59 supplies neither endpoint yet. No independent human specialist audit has been obtained.

My mathematical assessment is therefore positive about the new modules and the direction of the program, but negative about readiness for *Annals*, *Acta*, *Inventiones* or *JAMS*.

## 2. Frozen source, chronology and preservation

Both reviewed author branches resolve to

`69ab2afcceff0a8a2892910b335ac180678b5f4b`.

The repository tree is

`f4d42e1572e96d848cf0fc120efcb06ff1e11d90`.

The active article is

`papers/A2-DYN-v59-referee-response`.

The ordinary source payload tree recorded in the manifest is

`0093203296288b5168499eef44e64ea979e6b805`.

The author commit has the revision-58 external-review commit

`94c9ef54bd84d9eb04fbd3b4d3431776beab64de`

as its parent. The chronology is correct: revision 59 begins from the frozen external assessment and preserves the reviewed revision-58 source.

The source manifest records:

- all one hundred twenty-four inherited core modules retained byte-for-byte;
- all one hundred sixty-seven inherited Python files retained byte-for-byte;
- all inherited compiled appendices and mathematical labels retained;
- an append-only bibliography change;
- three new modules, 125--127;
- `physical_root_lemma_proved: true`;
- `accretive_gaussian_details_proved: true`;
- `correlated_markov_pressure_realization_proved: true`;
- `markov_continuous_roof_pointwise_LLT_proved: true`;
- `markov_boundary_essential_height_proved: true`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `unrestricted_same_roof_pair_bridge_proved: false`;
- `forward_essential_likelihood_convergence_proved: false`;
- `arithmetic_factor_identically_one_proved: false`; and
- `independent_human_review: false`.

The scope flags are accurate. The new Markov density theorem is explicitly restricted to the unperturbed roof \(\tau_0\), and the Markov boundary heights are not represented as Lorentz source heights.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v59-external-top4-review-2026-10-09/`.

No author manuscript source, prior review, workflow, historical manuscript or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-SHA qualification workflows completed successfully on both reviewed author refs:

- response branch run `37935957580`;
- referee-copy branch run `37935977060`.

The runs bind the source archive, finite diagnostics, native build and theorem-page renders to the reviewed SHA.

According to the validation record, the verifier checks

- the frozen revision-58 complete paper tree;
- the controlling revision-58 report blob;
- one hundred twenty-four unchanged inherited core files;
- one hundred sixty-seven unchanged inherited Python files;
- all one hundred twenty-seven core inclusions;
- all inherited mathematical labels and compiled appendices;
- thirteen provenance copies;
- the append-only bibliography;
- the ordinary Git payload identity;
- the read-only workflow hash;
- agreement of ordinary and optimized finite diagnostics;
- native TeX compilation; and
- theorem-label-based rendering.

The new finite diagnostics check detailed balance, stationary probabilities, pressure derivatives, damped-peak coefficients, stable-cylinder partitions, coarea normalization, triangle periodization and the Hermitian inverse identity. Negative controls retain an i.i.d. variance, an omitted coarea Jacobian and an unconjugated inverse formula as failures.

These are useful source, algebra and bookkeeping checks. They do not certify

- the inherited Lorentz occupation operator on anisotropic spaces;
- physical peripheral representations and branch visibility;
- resonant Hessian contact through arithmetic transitions;
- the Lorentz first-physical-defect decomposition;
- incidence and clearance multiplier geometry;
- complete local raw variation;
- the graph-coupled return clock;
- the Markov quotient spectral argument in the continuum Lipschitz space;
- the stable-cylinder approximation;
- or either Lorentz essential-height estimate.

The manuscript and its validation files state these limitations correctly.

## 4. Scope of this review

I did not attempt to re-prove all one hundred twenty-seven core modules. The substantive audit concentrates on the new modules and the inherited inputs immediately used by them:

1. the physical root-taking lemma;
2. the compact witness-cover argument;
3. the Hermitian accretive Gaussian identity and derivatives;
4. preservation and symbolic dynamics of the two-state Markov baker;
5. the nonindependence calculation;
6. positivity and telescoping of the continuous roof;
7. the infinite-dimensional conditional-expectation operator;
8. the stable-fibre quotient contraction and block resolvent;
9. the fixed physical witness at the nonzero resonance;
10. the matrix pressure covariance;
11. the real maximizer, damping and centered-drift coefficients;
12. the exact-state Markov lattice local limit;
13. the terminal-state stable-cylinder estimate;
14. the exact coarea density formula;
15. the uniform pointwise roof LLT;
16. the endpoint-weighted overlap factor;
17. the three positive boundary-source height bounds;
18. the separation between the perturbed pressure theorem and the unperturbed density theorem;
19. source preservation and qualification evidence;
20. the relation of the model mechanism to the missing Lorentz heights; and
21. top-four significance and architecture.

The inherited revision-58 and earlier Lorentz continuum chain is treated as a source-pinned baseline, not as independently certified mathematics.

## 5. The physical root-taking lemma

Module 125 isolates the scalar step which was compressed in revision 58.

For a centered bounded observable \(X\), the original probability gives

\[
 1\le \int e^{-t\cdot S_mX}\,d\nu
 \le C_0e^{m\mathscr P(t)}.
\]

The lower bound follows from Jensen. Taking logarithms and roots gives
\(\mathscr P(t)\ge0\).

A visible physical branch is written as

\[
 I_m(z)=A(z)e^{m\psi(z)}+E_m(z),
 \qquad |A(z)|\ge a_*>0,
 \qquad |E_m(z)|\le C_1\rho^m.
\]

Physical domination and the reverse triangle inequality yield

\[
 a_*e^{m\operatorname{Re}\psi(z)}
 \le C e^{m\mathscr P(t)}+C_1\rho^m.
\]

The amplitude lower bound is used before roots are taken. Since
\(\mathscr P(t)\ge0\) and \(\rho<1\), the root limsup gives

\[
 \operatorname{Re}\psi(a_0+it)\le\mathscr P(t).
\]

This is correct. It does not use an order relation on an anisotropic Banach space.

The finite witness-cover lemma is also correct. A finite subcover of the compact zero-damping locus supplies common amplitude, remainder and tilt constants, while the damping has a positive minimum on the complementary compact set. No global continuous choice of endpoint tests is required.

This resolves a genuine exposition and logical-boundary issue from the revision-58 report.

## 6. The accretive Gaussian lemma

For complex symmetric \(H\) with positive Hermitian real part, the identity

\[
 \operatorname{Re}(H^{-1})
 =(H^*)^{-1}(\operatorname{Re}H)H^{-1}
\]

is the correct formula. It gives a positive lower bound for
\(\operatorname{Re}(H^{-1})\) on a compact accretive family.

The accretive symmetric domain is convex and contains no singular matrix. The determinant therefore has a single logarithm branch fixed by continuation from real positive matrices. The manuscript then uses

\[
 \nabla_ZG_H=-H^{-1}ZG_H
\]

and

\[
 D_HG_H[E]
 =\frac12G_H
 \left\{Z^{\mathsf T}H^{-1}EH^{-1}Z
       -\operatorname{tr}(H^{-1}E)\right\}.
\]

These formulas are correct. Uniform inverse and determinant bounds, followed by absorption of polynomial factors into a weaker Gaussian, give the stated derivative estimate.

The explicit choice

\[
 \delta_m=\min\{\delta_0/2,m^{-1/2}\}
\]

correctly closes the free-\(\delta\) estimate from revision 58 without inserting a growing Fourier band into a fixed-band spectral theorem.

## 7. The correlated Markov baker

The transition matrix and stationary weights are

\[
 P=\begin{pmatrix}3/4&1/4\\1/3&2/3\end{pmatrix},
 \qquad \pi=(4/7,3/7).
\]

Detailed balance holds:

\[
 \pi_iP_{ij}=\pi_jP_{ji}.
\]

On the strip corresponding to \(i\to j\), the map expands \(x\) by
\(P_{ij}^{-1}\) and contracts \(y\) by \(P_{ji}\). Its Jacobian is
\(P_{ji}/P_{ij}\), and detailed balance converts the source state weight
\(\pi_i\) to the target state weight \(\pi_j\). Thus the map preserves
the stated \(\pi\)-weighted area measure.

The incoming images partition each target square horizontally. The map is invertible modulo the finitely many vertical and horizontal boundary lines.

The second eigenvalue of \(P\) is \(5/12\). Since
\(\operatorname{Var}_\pi(I_0)=12/49\),

\[
 \operatorname{Cov}_\mu(I_0,I_r)
 =\frac{12}{49}\left(\frac5{12}\right)^r.
\]

The symbols are therefore not independent. The text correctly avoids claiming that the system lacks a measure-theoretic Bernoulli model.

This is a legitimate correlated singular realization.

## 8. The continuous roof and the physical operator

The roof is

\[
 \tau_\epsilon
 =3+\xi_\epsilon(i,j)+y\circ F-y,
 \qquad
 \xi_\epsilon(i,j)=j+\epsilon ij.
\]

For \(|\epsilon|<1/4\), it is positive. On each regular strip it is affine in the stable coordinate with nonzero derivative.

The sum telescopes exactly:

\[
 S_m\tau_\epsilon
 =m(3+\bar\xi_\epsilon)
 +\sum_{r=0}^{m-1}
   \bigl(\xi_\epsilon(I_r,I_{r+1})-\bar\xi_\epsilon\bigr)
 +y_m-y_0.
\]

No independent smoothing variable is present.

The operator

\[
 (\mathcal P_{\epsilon,z}h)_i(y)
 =\sum_jP_{ij}e^{iz(\xi_\epsilon(i,j)-\bar\xi_\epsilon)}
 h_j(b_{ji}+P_{ji}y)
\]

acts on pairs of Lipschitz functions, and

\[
 \mathcal Q_{\epsilon,z}
 =M_{e^{-izy}}\mathcal P_{\epsilon,z}M_{e^{izy}}
\]

incorporates the stable coboundary.

The scalar pairing identity with bounded initial tests and Lipschitz terminal tests is exact.

The subspace of functions constant on each stable fibre is invariant and carries the two-by-two matrix

\[
 D_\epsilon(z)_{ij}
 =P_{ij}e^{iz(\xi_\epsilon(i,j)-\bar\xi_\epsilon)}.
\]

On the quotient, the Lipschitz seminorm contracts by at most

\[
 \rho_0e^{C|\operatorname{Im}z|},
 \qquad \rho_0=3/4.
\]

Choosing the complex neighborhood so this number is below one gives a uniform quotient spectral-radius bound. Splitting a function into its values at \(y=0\) and the vanishing remainder produces an upper-triangular block operator. The block resolvent then identifies the spectrum outside the quotient disk with that of \(D_\epsilon(z)\).

This argument is plausible and internally consistent. A final specialist audit should still check the bounded block projection, the quotient norm and the uniformity of the conjugating multipliers on the chosen complex neighborhoods, but I do not find a contradiction in the printed proof.

At \((\epsilon,z)=(0,2\pi)\), the fixed tests

\[
 a(i,y)=e^{2\pi iy},
 \qquad d(i,y)=e^{-2\pi iy}
\]

cancel the endpoint coboundary and give the exact pairing
\(e^{-6\pi im/7}\). The leading amplitude is therefore one and remains bounded away from zero on a smaller neighborhood. These witnesses are physical and fixed; they are not selected after the imaginary tilt.

## 9. Pressure covariance and the moving peak

The matrix pressure is obtained from the Perron root of

\[
 \begin{pmatrix}
 3/4&(1/4)e^s\\
 1/3&(2/3)e^{s+t}
 \end{pmatrix}.
\]

Its logarithm \(C(s,t)\) satisfies

\[
 DC(0,0)=\left(\frac37,\frac27\right),
\]

and

\[
 D^2C(0,0)
 =\frac1{343}
 \begin{pmatrix}204&192\\192&198\end{pmatrix}.
\]

The determinant is \(72/2401>0\).

For the reward \(j+\epsilon ij\), the variance is

\[
 \sigma_\epsilon^2
 =\frac{204+384\epsilon+198\epsilon^2}{343}.
\]

The bounded stable coboundary does not change the asymptotic variance of the roof sum.

The exact identity at \(\epsilon=0\),

\[
 D_0(2\pi+w)=e^{-6\pi i/7}D_0(w),
\]

gives second-order pressure contact at the resonance.

The expansion printed in the article is

\[
 a_\epsilon
 =2\pi-\frac{32\pi}{17}\epsilon+O(\epsilon^2),
\]

\[
 \kappa_\epsilon
 =\frac{12\pi^2}{119}\epsilon^2+O(\epsilon^3),
\]

\[
 v_\epsilon
 =-\frac{3456\pi^2}{99127}\epsilon^2+O(\epsilon^3).
\]

The quadratic minimization and the listed third derivatives of \(C\) give these coefficients. The sign convention is consistent with
\(D_z\psi_\epsilon(a_\epsilon)=iv_\epsilon\).

Consequently \(v_\epsilon^2=o(\kappa_\epsilon)\), while
\(\kappa_\epsilon>0\) for sufficiently small nonzero \(\epsilon\).

This is a nontrivial correlated continuous-roof verification of the pressure-contact theorem.

## 10. The exact-state lattice local limit

For

\[
 A_m=\sum_{r=1}^m I_r,
\]

the manuscript proves, for fixed initial and terminal states,

\[
 \left|\sqrt m\,\Pr_i(A_m=k,I_m=j)
 -\pi_jg_{\sigma^2}\!\left(\frac{k-3m/7}{\sqrt m}\right)\right|
 \le Cm^{-1/2}.
\]

The Fourier matrix is \(P_{ij}e^{izj}\).

There is no nonzero peripheral frequency. Equality in the triangle inequality forces all transition phases to agree with the eigen-equation; the \(00\) loop fixes the eigenvalue and the \(11\) loop then forces \(e^{iz}=1\).

Near zero, the eigenvalue logarithm has the correct variance and a bounded cubic remainder. The projection entry is \(\pi_j+O(|z|)\). Integrating the projection and cubic errors gives a raw error of order \(m^{-1}\), hence an order \(m^{-1/2}\) error after multiplication by \(\sqrt m\). Compact frequencies away from zero are exponentially small.

The estimate is uniform in the lattice label because the Fourier inversion phase has modulus one.

I find this argument sound.

## 11. Stable cylinders

For a fixed terminal state, the last \(L\) transitions partition the stable unit interval into cylinders whose lengths are products of reverse transition probabilities and are at most \(\rho_0^L\).

Detailed balance gives

\[
 \pi_i\prod_{\rm suffix}P_{i_ri_{r+1}}
 =\pi_j|I_w|.
\]

The exact-count probability of a suffix is a prefix exact-state probability times the forward suffix weight.

The manuscript correctly observes that summing the local-limit error over exponentially many suffixes does not multiply the error by their number. The sum of the corresponding transition weights is uniformly bounded.

Changing the prefix Gaussian to the full-\(m\) Gaussian costs
\(C(1+L)/\sqrt m\), uniformly in the label. An arbitrary interval is approximated from inside and outside by complete stable cylinders, with only finitely many boundary cylinders and total boundary length \(O(\rho_0^L)\).

The resulting estimate

\[
 \left|\sqrt m\,\mu\{A_m=k,b_m\in J\}
 -g_{\sigma^2}\!\left(\frac{k-3m/7}{\sqrt m}\right)
  |J\cap[0,1]|\right|
 \le C\left(\frac{1+L}{\sqrt m}+\rho_0^L\right)
\]

is consistent. The positive upper bound uses the exact-state upper estimate and does not rely on cancellation in the local-limit error.

This positive upper estimate is the load-bearing input for the later height theorem.

## 12. Exact coarea and the pointwise density theorem

On a complete word \(w\),

\[
 y_m=b_w+a_wy_0,
 \qquad 0<a_w\le\rho_0^m.
\]

At \(\epsilon=0\),

\[
 S_m\tau_0
 =3m+A_m+b_w-(1-a_w)y_0.
\]

Conditional on the word, \(y_0\) is uniform. The exact density is therefore

\[
 p_m^{\rm M}(t)
 =\sum_w\frac{w_\mu}{1-a_w}
 \mathbf 1_{[b_w+a_w-1,b_w]}
       (t-3m-A_m(w)).
\]

The derivative \(1-a_w\) is uniformly bounded below. No word is removed near a cut.

For a fixed count \(k\), put \(\delta=t-3m-k\). The contribution is trapped between stable-cylinder probabilities for

\[
 [\delta,\delta+1-\rho_0^m]
 \quad\text{and}\quad
 [\delta,\delta+1].
\]

Choose

\[
 L=\left\lceil\frac{\log m}{2\log(4/3)}\right\rceil.
\]

Then \(\rho_0^L\le m^{-1/2}\), and the cylinder estimate yields the triangular factor

\[
 g_{\sigma^2}\!\left(\frac{k-3m/7}{\sqrt m}\right)
 (1-|\delta|)_+
\]

with error \(O(\log m/\sqrt m)\) on the \(\sqrt m\)-normalized density.

At any roof value, at most three integer labels contribute. Their Gaussian arguments differ from the physical roof coordinate by \(O(m^{-1/2})\), and

\[
 \sum_{k\in\mathbb Z}(1-|r-k|)_+=1.
\]

This proves the stated uniform essential-supremum local limit.

The proof is direct. It does not differentiate a weak limit or a fixed-window theorem.

The weighted endpoint theorem is also correctly more arithmetic than a product-of-means formula. The one-periodic factor

\[
 \Theta_{f,d}(r)
 =\sum_{k\in\mathbb Z}
 \int_{[0,1]\cap[r-k,r-k+1]}
 f(v-r+k)d(v)\,dv
\]

comes from the actual stable overlap. It equals one only for \(f=d=1\).

## 13. Direct positive boundary-source heights

The vertical source is supported near the forward cuts in the \(x\)-coordinate. A union of forward cylinders of depth \(L=\lfloor m/2\rfloor\) covers it from outside with total stationary mass

\[
 O(s+\rho_0^L).
\]

For each prefix cylinder, the remaining exact-count probability is
\(O(m^{-1/2})\). The coarea density on each complete word is uniformly bounded, and a fixed roof value uses at most three count labels. Summing positive prefix weights proves the vertical-source estimate.

For terminal stable strips, the coarea point satisfies

\[
 |y_m-b_m|\le\rho_0^m.
\]

Enlarging the finitely many target intervals by this amount and applying the positive stable-cylinder upper bound gives the terminal estimate.

For initial-age strips, the exact coarea relation converts
\(y_0<s\) and \(y_0>1-s\) into stable-endpoint intervals of length
\(O(s+\rho_0^m)\). The same positive upper bound applies.

Thus

\[
 \sqrt m\left(
 \|p_{m,s}^{\rm vert}\|_\infty+
 \|p_{m,s}^{\rm stab}\|_\infty+
 \|p_{m,s}^{\rm age}\|_\infty\right)
 \le C(s+\rho_0^{\lfloor m/2\rfloor}).
\]

The proof controls essential height directly. It does not infer it from source mass.

This is the most important new mathematical contribution of revision 59 beyond the scalar pressure theorem.

## 14. What revision 59 closes

Relative to revision 58, the manuscript closes the following issues.

- The physical root-taking step is now a standalone lemma with the nonzero amplitude and exponential remainder visible before roots are taken.
- The compact witness-cover argument is explicit.
- The accretive Gaussian inverse identity, determinant branch and derivatives are explicit.
- The free covariance-splitting parameter has an explicit diagonal.
- The independent realization now has correlated symbols.
- The operator has a genuine infinite-dimensional stable-fibre quotient.
- The roof is continuous along regular stable fibres and has a true deterministic endpoint coboundary.
- Fixed physical witnesses see the nonzero resonance.
- A nontrivial damped peak is computed in the correlated family.
- An exact continuous-roof coarea density is evaluated.
- A pointwise roof local limit with an explicit rate is proved.
- Three actual positive boundary-source heights are proved without deleting a roof set.
- The endpoint-weighted arithmetic overlap is retained rather than replaced by a product of means.

These are real advances.

## 15. What revision 59 does not close

The original Lorentz endpoint remains unchanged.

The manuscript does not prove

\[
 \lim_{B\to\infty}\limsup_{m\to\infty}
 \sup_{R,n,k}
 \operatorname*{ess\,sup}_{u\ {\rm central}}
 m^2b^{\varepsilon(B),{\rm inc},1}_{n,k,m,R}(u)=0
\]

or the analogous estimate for the complete competing-hit clearance source.

It therefore does not prove

- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- the full pointwise roof-density LLT for the original return record;
- unrestricted same-roof collision and return bridges;
- forward essential likelihood convergence;
- the unrestricted pointwise roof-conditioned path theorem;
- the strong critical \(L^{145/144}\) endpoint;
- an identically-one arithmetic factor; or
- an independent proof certificate.

The source manifest and publication-status file record these limitations accurately.

## 16. Why the Markov height theorem does not transfer automatically

The model proof relies on two features:

1. on every word, the continuous roof has a coarea derivative
   \[
   1-a_w\ge1-\rho_0
   \]
   independent of the word length and of the boundary source; and
2. exact-count probabilities remain uniformly bounded after conditioning on cylinders of depth up to \(m/2\).

Neither statement is presently available for the Lorentz incidence and clearance sources at the exact original labels.

In the Lorentz problem:

- grazing can make physical coordinate derivatives degenerate;
- competing-hit clearance is read at the next collision;
- singularity cuts proliferate under iteration;
- the positive first-defect source carries image-side marks;
- exact return and occupation labels must be preserved;
- multiple physical roots can exchange order; and
- one may not continue an orbit across a seam merely to obtain a nearby regular word.

The Markov theorem is therefore a useful sufficient-mechanism example, not a proof by analogy.

## 17. Generality and significance

Revision 59 responds positively to the revision-58 request for an additional system with a genuine continuous density consequence. The new example is correlated, singular, deterministic, infinite-dimensional at the operator level and includes direct positive source heights.

This materially strengthens the generality case.

It still falls short of a four-journal general theorem for three reasons.

First, the pointwise theorem is at \(\epsilon=0\), where the nonzero damped peak has returned to an exact resonance. The perturbed \(\epsilon\)-family verifies pressure contact, but the manuscript does not prove a uniform perturbed pointwise density or height theorem. Thus moving arithmetic peaks and pointwise coarea control are not yet combined in one nontrivial family.

Second, the roof is an explicitly solvable finite-state additive reward plus a bounded stable coboundary. The decisive coarea derivative and cylinder structure are transparent. This does not independently test the nonuniform physical roots, grazing and competing-hit geometry which make the Lorentz height problem difficult.

Third, the manuscript has not abstracted the coarea/cylinder mechanism into a theorem with verifiable hypotheses and multiple realizations. The source contains a model proof, not yet a reusable source-height theory for singular hyperbolic systems.

The new material is strong specialist mathematics. It does not yet establish the independent breadth expected for a positive top-four recommendation.

## 18. Architecture and editorial significance

The direct reading route is helpful, and the new front matter accurately separates

- the canonical integrated Lorentz theorem;
- the abstract pressure-contact principle;
- the correlated Markov pointwise theorem; and
- the still-open Lorentz pointwise endpoint.

Nevertheless, the article contains one hundred twenty-seven numbered modules, more than sixteen hundred inherited mathematical labels and a long historical dependency chain.

The title continues to emphasize raw local inversion in the triangular Lorentz gas, while the unrestricted Lorentz pointwise theorem remains unproved. The second complete pointwise theorem belongs to a different Markov model.

There are now at least three plausible papers inside the archive:

1. flat pressure contact and canonical arithmetic Gaussian references;
2. the correlated Markov-baker continuous-roof and boundary-height theorem; and
3. the Lorentz pointwise raw-inversion program.

Keeping all three in one manuscript is understandable for research continuity. It is not an effective four-journal submission architecture.

A positive top-four submission should present one completed principal theorem with the shortest complete proof route.

## 19. Independent specialist verification

No independent human specialist audit has been obtained.

For modules 125--127, the highest-priority checks are:

1. the lower amplitude bound before the root limsup;
2. the finite witness cover near every zero-damping branch;
3. the centered logarithm convention;
4. the Hermitian identity for \(\operatorname{Re}(H^{-1})\);
5. the determinant square-root branch;
6. preservation of the \(\pi\)-weighted area measure;
7. the block decomposition of the Lipschitz operator;
8. quotient contraction and the common resolvent contour;
9. the fixed physical witness pair at \(2\pi\);
10. the pressure covariance and third derivatives;
11. the maximizer, damping and drift coefficients;
12. absence of a nonzero lattice peripheral frequency;
13. terminal-state normalization in the lattice LLT;
14. detailed-balance conversion from suffix weights to stable-cylinder lengths;
15. summation of the local-limit error over cylinder collections;
16. the exact coarea interval and derivative;
17. the triangular periodization;
18. the bounded-variation passage for endpoint weights;
19. the forward-cylinder cover of the vertical source;
20. the positive cylinder upper bound in the stable and age sources; and
21. the strict separation of the \(\epsilon\)-family pressure theorem from the \(\epsilon=0\) density theorem.

The inherited Lorentz audit obligations remain:

- the actual section occupation multiplier;
- full occupation-torus spectral power bounds;
- physical peripheral representations;
- branch visibility through arithmetic transitions;
- critical-collar and first-defect geometry;
- incidence and next-collision clearance sources;
- complete local raw variation;
- positive path remainder;
- graph-coupled clock transfer; and
- the two missing essential-height estimates.

Source qualification and finite symbolic checks do not replace this audit.

## 20. Required mathematical changes before another top-four review

### 20.1 Prove the Lorentz incidence height

Establish the uniform central-scale essential-height estimate for the complete incidence source on the original exact labels, without deleting an exceptional roof set and without replacing the physical word.

### 20.2 Prove the Lorentz clearance height

Establish the corresponding estimate for the full competing-hit clearance source, respecting the next-collision convention and without continuing a trajectory across a physical seam.

### 20.3 Complete the unrestricted pointwise theorem

Combine the two positive-height estimates with the retained positive raw-error representation and the canonical arithmetic reference.

Keep the finite arithmetic factor unless the concrete residue criterion is proved separately.

### 20.4 Deduce unrestricted same-roof consequences

Only after the pointwise source estimates are available should the manuscript promote the record-mean bridge and likelihood statements to unrestricted same-roof bridge and forward essential-likelihood conclusions.

### 20.5 If breadth is the chosen route, abstract the source-height mechanism

Formulate a reusable theorem whose hypotheses include

- a wordwise coarea derivative bounded away from zero;
- positive exact-count cylinder estimates at mesoscopic depth;
- endpoint/cut source covers with controlled cylinder mass;
- compatibility with arithmetic labels; and
- parameter-uniformity.

Verify it in more than one genuinely different system.

### 20.6 Combine moving contact and pointwise density in one family

A stronger second realization would prove the pointwise density and source-height theorem uniformly for nonzero \(\epsilon\), so that the moving damped peak and the density inversion coexist in the same nontrivial family.

### 20.7 Obtain independent specialist review

The Lorentz occupation spectrum and physical source geometry require experts in dispersing billiards and anisotropic transfer operators. The Markov coarea/cylinder proof should also receive an independent probability/dynamical-systems audit.

### 20.8 Reduce the journal proof burden

Present the shortest complete route to one principal endpoint. Keep provenance, validation ledgers and historical theorem hierarchies in the repository or a technical supplement.

### 20.9 Sharpen the literature comparison

Explain theorem by theorem what is new beyond finite-state Markov additive density theory, classical lattice local limits, Lorentz-process LLTs, billiard endpoint LLTs and suspension-flow local central limits.

## 21. Technical and presentation comments

1. Keep the \(\pi\)-weighted area measure explicit whenever the baker map is described as measure preserving.
2. State that detailed balance, rather than equal strip areas, supplies invariance.
3. Keep the coded-state correlation statement separate from Bernoulli-isomorphism questions.
4. Keep the roof positivity range and the nonzero stable derivative visible.
5. In the block-resolvent proof, state the bounded projection defining the constant-fibre block.
6. Record the quotient norm and the uniform multiplier bounds for the conjugation by \(e^{izy}\).
7. Keep the physical witness functions fixed throughout the complex neighborhood.
8. Keep the centered logarithm adjacent to the drift sign.
9. State that the covariance belongs to the symbolic reward and is unchanged by the bounded endpoint coboundary.
10. Preserve the distinction between the \(\epsilon\)-family contact theorem and the \(\epsilon=0\) density theorem.
11. Do not advertise a perturbed pointwise density theorem.
12. In the lattice LLT, retain the terminal-state factor \(\pi_j\).
13. Keep the self-loop aperiodicity argument visible.
14. In the cylinder lemma, display why transition weights, rather than cylinder count, sum the local-limit error.
15. Keep \(L\le m/2\) explicit.
16. Distinguish the full-word endpoint \(b_m\) from the endpoint of a suffix cylinder.
17. Keep the lower and upper interval inclusions in the coarea proof.
18. Retain the coarea denominator \(1-a_w\).
19. Keep the triangular partition-of-unity identity adjacent to the unweighted theorem.
20. Do not replace the endpoint factor \(\Theta_{f,d}\) by a product of means.
21. State that the weighted theorem covers the stated Lipschitz endpoint class, not arbitrary path selectors.
22. Keep the vertical, stable and age sources distinct.
23. In the vertical estimate, state that the residual exact-count bound is applied after fixing the prefix.
24. In the stable estimate, retain the enlargement by \(\rho_0^m\).
25. In the age estimate, retain both one-sided interval formulas.
26. Keep essential supremum, source mass and exceptional-set length as separate notions.
27. Do not transfer the Markov source-height conclusion to Lorentz incidence or clearance.
28. Keep the Lorentz pointwise status flags false.
29. Keep arithmetic zero classes in the canonical reference.
30. Retain the signed arithmetic coefficient until the positive part is explicitly normalized.
31. Keep probability total variation equal to one half of variation mass.
32. Keep the graph-coupled collision and return bridges nonindependent.
33. Preserve the complete output event in postselection.
34. Exclude path-reading selectors from the record-only contraction theorem.
35. Keep exact-source qualification separate from proof certification.
36. Consider extracting modules 125--127 as a separate, self-contained Markov/additive paper.
37. Consider moving extensive source-manifest and validation discussion outside the main journal narrative.

## 22. Final assessment

Revision 59 is a serious and mathematically coherent response to the revision-58 report.

It makes the pressure-contact theorem independently readable, replaces the finite-support baker illustration by a correlated continuous-roof singular realization, proves a pointwise density LLT by exact coarea, and obtains direct positive boundary-source height estimates.

The state normalization, correlation, pressure covariance, damped-peak coefficients, lattice LLT, stable-cylinder weights, coarea Jacobian, triangle periodization and height bounds are mutually consistent. I found no decisive error in modules 125--127.

The new example is substantially more relevant to the Lorentz obstruction than the revision-58 finite-digit example. It demonstrates that pressure contact, a continuous roof, singular cuts, exact density inversion and positive height estimates can coexist in a deterministic correlated system.

It does not, however, prove the two required Lorentz height estimates. Nor does it yet produce a general source-height theorem with genuinely difficult multiple realizations. The pointwise Markov theorem is restricted to the unperturbed roof, while the moving damped-peak theorem is verified on the perturbed family.

The original unrestricted pointwise Lorentz theorem, unrestricted same-roof bridges and forward essential likelihood therefore remain open. The article also remains extraordinarily large and dependent on an inherited continuum pipeline which has not received independent specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

The new Markov-baker theorem could support a focused specialist or high-level dynamics/probability paper. The canonical integrated Lorentz theorem likewise has independent value. A future top-four submission should return only after the Lorentz incidence and clearance heights are closed, or after a genuinely reusable source-height theory is extracted and independently verified across substantially different systems.
