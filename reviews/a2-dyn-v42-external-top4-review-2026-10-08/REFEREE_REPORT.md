# External top-four referee report on A2-DYN revision 42

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v42-referee-response-2026-10-08`, `revision/a2-dyn-v42-referee-copy-2026-10-08`  
**Reviewed commit:** `7e155f0fda2a7a5f77a061ed5b54cab5943fb24b`  
**Reviewed repository tree:** `ea873cbae7c0867721bbc1905a03f194002e9d50`  
**Ordinary source payload tree:** `55395ef054227b89bd792c7b4e409cc03e4d8a07`  
**Active manuscript directory:** `papers/A2-DYN-v42-referee-response`  
**Active mathematical source:** ninety-one numbered core modules; revision 42 adds modules 90--91  
**Frozen revision-41 author baseline:** `e8bb719f3100f16cb945ab57c2b3408d19f678dc`  
**Frozen revision-41 ordinary paper tree:** `20e17443eac838e4b1af93dcfb057276540e1340`  
**Controlling report:** `reviews/a2-dyn-v41-external-top4-review-2026-10-08/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `c4b969cb054f3d86db468604b5bc17ba05cf8c44` / `0c1b4cea20c1aabe8a6686812a6df894c59c41db`  
**Date:** 8 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 42 is a genuine theorem-bearing advance. It does not merely restate the fixed-interval arithmetic local law or the exact-event bridge proved in revisions 40--41. It addresses two concrete issues left by the preceding report.

First, it returns to the pointwise raw roof-density problem and treats the regular critical source on the actual return section. It constructs quantitative Morse coordinates on every guarded regular branch below a finite collision cutoff, subtracts two intrinsic right roof jets rather than only the leading jump, sums the resulting residuals in `W^{2,1}`, and obtains an explicit pointwise finite-band inversion error. The construction deliberately keeps the normal initial states and stops the guard at the actual terminal collision.

Second, it refines the arithmetic information in the fixed-radius exact-index interval theorem. It realizes each measurable endpoint phase class as a strong initial source by finite Fourier synthesis of physical peripheral eigenvectors, proves the exact-index conditional law of the initial and terminal phase classes, and couples that finite posterior with the actual-return Gaussian bridge.

I audited the new modules

- `core/90_guarded_morse_extraction.tex`;
- `core/91_arithmetic_endpoint_posteriors.tex`;

as well as their front-matter statements, response, proof ledger, specialist audit map, source manifest, and exact-source qualification record.

Within the scope of that audit, I found no decisive counterexample, Fourier-sign error, collision/return endpoint shift, missing section-normalization factor, incorrect arithmetic residue orientation, or false claim that a finite-cutoff estimate already proves the full raw theorem.

Several parts of the new chain are mathematically well conceived.

1. The critical points are identified by the physical conditions `p=p_m=0`, and the displayed Hessian has the expected positive determinant.
2. The source guard includes the actual terminal collision and no later collision, so the extracted source is tied to the unchanged return event.
3. The normal line `p=0` is not deleted; it is precisely where the regular critical source is analyzed.
4. The second roof jet is chosen so that both the value and first derivative match at the edge, removing the atomic part of the second distributional derivative.
5. The omitted source is retained as an exact nonnegative density rather than declared negligible pointwise.
6. Coincident critical roof values are handled by addition of jets, not by division by their separation.
7. The phase-class indicators are not assumed to be strong multipliers. The manuscript instead constructs the required class sources as finite sums of known strong peripheral vectors.
8. The terminal phase class is `l+r`, with the orientation consistent with the exact iterated phase equation.
9. The phase-posterior denominator reproduces the previously proved arithmetic coefficient.
10. The bridge product statement is restricted to fixed radius and positive arithmetic classes, where its microscopic denominator is actually available.

These are substantive improvements.

The negative recommendation is nevertheless unavoidable. Revision 42 proves a pointwise inversion theorem only for a **finite guarded regular packet**. The full raw density differs from this packet by a nonnegative boundary/singular source `r`. Only the total mass of `r` is controlled; no pointwise bound is proved. In addition, the summed `W^{2,1}` budget grows as

```text
exp{ C (L+1) log(C/epsilon) }.
```

When the collision cutoff `L` is taken on the scale required to capture a long return, this budget forces an enormous roof-frequency cutoff. The manuscript has no corresponding growing-band operator estimate and no pointwise control of the omitted source. The compatibility of the coefficients of each fixed positive-margin word also does not establish convergence of the infinite common edge correction.

Thus the decisive raw-inversion obstruction has been localized more sharply, but not closed.

There is a second independent issue. The concrete section residues are still not proved to vanish. At fixed radius the exact-index interval main term naturally carries the arithmetic factor `mathfrak a_R`; uniformly in the radius the correct object is the transition kernel `mathcal L_{m,R}`. Revision 42 describes the associated posterior but does not prove that the unmodulated Gaussian theorem is valid for the concrete section.

Finally, a fixed roof interval, an existential slowly shrinking interval, and a finite guarded-packet pointwise inverse are not a pointwise roof-density local limit for the full law. The common correction, the boundary/singular source, the infinite edge sum, and the full high-roof-frequency complement remain open.

At the requested venue level, the article would need either:

- a complete arithmetic raw-density theorem, including the correct residue factor or a proof that it is identically one, together with the full pointwise roof inversion; or
- a substantially more general theorem whose breadth and significance do not depend on the unfinished raw endpoint.

Revision 42 supplies neither yet, although it makes real progress toward the first.

## 2. Frozen source and chronology

Both reviewed author branches resolve to

`7e155f0fda2a7a5f77a061ed5b54cab5943fb24b`.

The repository tree at that commit is

`ea873cbae7c0867721bbc1905a03f194002e9d50`.

The active manuscript is

`papers/A2-DYN-v42-referee-response`.

The source manifest identifies revision 41 as the immediate author baseline. All eighty-nine inherited core modules and all one hundred three inherited Python files are retained byte-for-byte. The bibliography, the inherited mathematical labels, and the compiled A--X synopsis are retained. Revision 42 adds modules 90 and 91 and updates the front matter and source records while preserving the earlier material under provenance.

The branch chronology is correct. The revision begins from the controlling revision-41 review commit and then adds a new author manuscript tree. It is not a review commit relabeled as an author source.

The present review branch begins directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v42-external-top4-review-2026-10-08/`.

No author manuscript source, prior review, workflow, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-source qualification workflow completed successfully on the final response branch SHA:

- response branch run `37732355661`.

At the time of this review, the GitHub Actions branch query returned no separate completed run for `revision/a2-dyn-v42-referee-copy-2026-10-08`. The copy branch nevertheless resolves to the identical reviewed SHA. I therefore record one completed qualification run and do not invent a second execution claim.

The verifier checks, among other things:

- the frozen revision-41 source identity;
- all ninety-one core inclusions;
- byte identity of the eighty-nine inherited cores and one hundred three inherited scripts;
- preservation of inherited labels, bibliography, and A--X statements;
- the exact controlling-report blob and workflow hash;
- the ordinary-source Merkle identity;
- normal/optimized diagnostic agreement;
- native TeX compilation and theorem-label-based page rendering.

The new finite diagnostics cover positive symplectic collision products, the critical Hessian formulas, radial two-jet models, phase/residue identities, actual stopping/count conventions, and selected negative controls.

These checks are meaningful source, algebra, and regression evidence. They do not establish:

- the continuum branch regularity estimates;
- the zero-extension argument at all decision boundaries;
- the quantitative Morse coordinates;
- the summed coarea derivative estimates;
- the full anisotropic operator chain inherited from revision 41;
- the phase-posterior local theorem;
- or the missing pointwise raw-density estimates.

The manuscript and its validation record state this boundary accurately.

## 4. Scope of this review

I did not attempt to re-prove all ninety-one modules. The substantive audit concerns the new claims which could change the revision-41 assessment:

1. the characterization and Hessian of guarded regular critical points;
2. the high-order derivative and reciprocal regularity budget;
3. construction of quantitative Morse coordinates;
4. the invariant two-jet edge subtraction;
5. the stopped guard and actual terminal convention;
6. the exact finite-packet decomposition `mu=e+q+r`;
7. the summed coefficient and `W^{2,1}` budget;
8. the pointwise residual inversion and the role of the omitted source;
9. stabilization of the coefficients of a fixed positive-margin word;
10. the strong realization of measurable phase-class sources;
11. the arithmetic class local law and finite posterior;
12. the product of that posterior with the exact-event return bridge;
13. the distinction between fixed-radius arithmetic statements and radius-uniform transition statements;
14. the remaining long-time, boundary, and high-frequency steps;
15. source identity and qualification evidence.

The inherited revision-41 theorems are treated as the source-pinned baseline. This report does not independently recertify the full action-weighted anisotropic-space construction, the full occupation-torus spectrum, or the conditional bridge proof.

## 5. Critical-point geometry

On a regular `m`-collision branch the manuscript writes

```text
D T_R^m = [[A,B],[C,D]].
```

The differential identities are

```text
partial_alpha L_{m,R} = R (p_m A-p),
partial_p     L_{m,R} = R p_m B.
```

Because `B` is nonzero on a regular branch, a critical point has `p_m=0`; the first identity then gives `p=0`. Conversely those two conditions make both derivatives vanish.

At such a point the Hessian is stated as

```text
R [[AC,BC],[BC,BD]].
```

Using `AD-BC=1`, the mixed derivative can be written either as `R(AD-1)` or `RBC`. Its determinant is

```text
R^2 BC.
```

The entries of `(-1)^m D T_R^m` are positive. Hence `AC`, `BC`, and `BD` have the signs required for positive definiteness. The parity signs cancel in the relevant products.

I found the algebra of this Hessian coherent. It is also consistent with the inherited leading edge coefficient. With physical source density `(4 pi c)^{-1}` and

```text
sqrt(det Hessian)=R sqrt(BC),
```

the leading right jump is

```text
1/(2 c R sqrt(BC)).
```

This agrees with the displayed stabilized coefficient.

The assertion of at most one critical point per ordered center word is inherited from the convex endpoint-action argument. In the new module it is used only on a fixed regular physical word; it is not transferred between inducing sections.

## 6. Quantitative guarded regularity

The manuscript introduces the budget

```text
H = exp{ C (L+1) log(C/epsilon) }
```

for all branches of collision length at most `L` which remain inside the enlarged guard region.

The intended mechanism is plausible:

- each one-collision root and reflection map has fixed-order derivatives bounded by a power of `1/epsilon`;
- a repeated chain rule through at most `L+1` maps gives exponential growth in `L log(1/epsilon)`;
- the inverse of `(alpha,p) -> (p,p_m)` is controlled through the nonvanishing derivative `C`;
- a quantitative inverse theorem locates a true zero from a small value of `(p,p_m)`;
- the Hessian has reciprocal lower eigenvalue bounds of the same general size;
- a smaller regularity ball then supports the Morse chart.

The manuscript explicitly avoids replacing this by an unjustified bound whose logarithm grows like `C^L`. This distinction matters later.

This is, however, one of the most specialist parts of the new proof. A full audit should verify:

1. that every guard factor used to select a physical word has the claimed reciprocal margin on the enlarged region;
2. that the derivative induction really retains the stated dependence through order ten;
3. that the lower bound for the derivative of `(p,p_m)` is uniform on the required neighborhood;
4. that the quantitative inverse neighborhood stays inside the same physical word;
5. and that all constants can be absorbed into one exponent without circularly shrinking the neighborhood.

I found no immediate contradiction, but I do not regard the finite diagnostics as a substitute for this continuum verification.

## 7. The explicit Morse chart

With `h=x-x_0`, the manuscript defines

```text
Q(h)=2 integral_0^1 (1-s) Hess L(x_0+s h) ds,
z=Q(h)^{1/2} h.
```

Taylor's formula gives

```text
L(x)-L(x_0)=|z|^2/2.
```

On a sufficiently small ball, `Q(h)` remains symmetric positive definite. The square root is then smooth, and its derivatives can be controlled through the Sylvester equation. At the origin the derivative is the positive square root of the Hessian, so the same quantitative inverse argument gives a coordinate chart.

This construction has two advantages.

- It makes the normalization of the radial variable explicit.
- It avoids an appeal to a nonquantitative Morse lemma whose constants would be unavailable in the later word sum.

The claimed `C^6` chart bounds are compatible with the fixed-order derivative budget, subject again to the specialist checks listed above.

## 8. Why two jets are required

For a smooth source written in Morse coordinates as `g(z) dz`, the roof density at height `s>0` is

```text
F(t_0+s)=integral_0^{2 pi} g(sqrt(2s) n_theta) d theta.
```

Angular integration removes every odd monomial. The right value and first derivative are therefore

```text
a_0 = 2 pi g(0),
a_1 = pi Delta g(0).
```

The manuscript subtracts

```text
1_{s>=0} e^{-s} {a_0+(a_0+a_1)s}.
```

Its right value is `a_0`, and its right derivative is

```text
-a_0+(a_0+a_1)=a_1.
```

Thus the residual and its first derivative match the zero left traces. Its second distributional derivative has no delta mass. This is the correct reason to subtract two jets rather than only the leading edge.

The Fourier transform

```text
e^{i b t_0} [a_0/(1-i b)+(a_0+a_1)/(1-i b)^2]
```

is also correct for the stated Fourier convention.

The chart invariance of the jets follows because they are the right jets of the same local pushforward measure. A cutoff which is one near the minimum changes neither jet.

I found this local calculation sound.

## 9. The stopped source and event identity

For a state whose actual terminal collision count is `m=N_{n,R}`, the guard is

```text
G(x)=product_{j=0}^m chi(T_R^j x).
```

It is set to zero when `N_n>L` or the itinerary is undefined.

Two choices are important.

1. There is no separate factor removing `p=0`.
2. No collision after the actual terminal collision is tested.

The first choice preserves the regular critical source. The second keeps the extracted measure tied to the original return event; it does not impose a future regularity condition unrelated to `J_{n,R}`.

Since `0<=G<=1`, the difference between the original source and the guarded source is positive. The cumulative return tail controls `N_n>L`, while a union bound through the actual stopping time controls guard failure. This gives the stated total mass estimate

```text
C { exp(a n-c_0 L)+(L+1) epsilon^{1/16} }.
```

The endpoint convention is consistent with the earlier half-open occupation convention: the terminal collision is checked for regularity, while the return count itself is still the physical one.

## 10. Partition by words and zero extension

The guarded source is partitioned by center words and section decisions. The manuscript argues that each source piece extends smoothly by zero because, at the first collision or decision where the record changes, a guard factor already vanishes on a two-sided neighborhood.

This is a load-bearing assertion. If correct, it removes boundary terms from the two integrations by parts used on the submersion region.

The proof does not require each word domain to be connected. It only needs:

- a finite number of records through cutoff `L`;
- smoothness on each regular component;
- and zero extension across every boundary relevant to changing that record.

The record count is allowed to be exponential in `L`; it is later absorbed into the same exponential derivative budget.

The exact compatibility of the auxiliary guard zeros with all center and section-decision boundaries deserves expert checking. I found no explicit missing class of decision boundary in the written description, but this point cannot be certified by the finite word models alone.

## 11. Submersion integration by parts

Outside the smaller critical neighborhoods the manuscript has

```text
|grad L_m| >= H^{-1}
```

and uses

```text
V=grad L_m/|grad L_m|^2.
```

For a zero-extended source `b_D`, it writes

```text
D_t (L_m)_*(b_D dx)
  =(L_m)_*(div(b_D V) dx),

D_t^2 (L_m)_*(b_D dx)
  =(L_m)_*(div(V div(b_D V)) dx).
```

The signs are correct under the stated distributional convention. The zero extensions and local cutoffs eliminate boundary terms. Coarea then converts the right-hand source measures into `L^1` roof densities.

The derivative budget follows from fixed powers of the reciprocal gradient and the branch derivative bounds.

This step is the mechanism that gives `W^{2,1}` regularity away from the critical neighborhoods. It is not a spectral estimate, and it makes no claim about a growing collision cutoff beyond the displayed budget.

## 12. The finite critical packet

The resulting decomposition is

```text
mu_{n,R}=e_{n,R}^{L,epsilon}
          +q_{n,R}^{L,epsilon}
          +r_{n,R}^{L,epsilon}.
```

Here:

- `e` is the finite sum of explicit two-jet edges at all guarded regular critical points;
- `q` is the summed `W^{2,1}` residual;
- `r` is the exact nonnegative omitted source.

The manuscript allows coincident roof values. This is correct: the associated jets are added. No small denominator involving the distance between critical values appears.

The summed estimate is

```text
sum_z (|a_{0,z}|+|a_{1,z}|)
 +sum_ell ||q_ell||_{W^{2,1}}
 <= A_{L,epsilon}
 :=exp{ C (L+1) log(C/epsilon) }.
```

This is a useful finite-cutoff theorem. It is substantially stronger than a word-by-word statement with no summability budget.

The edge density need not be nonnegative. That causes no logical problem because positivity is retained by the full identity and by the separate nonnegative source `r`.

## 13. Stabilization of a fixed regular word

For a fixed physical critical word whose complete finite orbit has strictly positive margins from every guard zero, the guard is eventually identically one near the critical point. The local source density is then the physical constant `(4 pi c)^{-1}`.

Consequently the two jets become independent of larger `L` and smaller `epsilon`. The leading coefficient is

```text
1/(2 c R sqrt(B_m C_m)).
```

This is a genuine compatibility result. It means that the finite packets do not assign changing coefficients to one fixed interior word.

The manuscript correctly limits the assertion to positive-margin words. It makes no stabilization claim at a true singular boundary or a redundant guard zero.

Most importantly, stabilization of each fixed word is **not** convergence of the sum over all words as their lengths tend to infinity. The article explicitly preserves this distinction.

## 14. Pointwise inversion of the guarded packet

Because `q_ell` belongs to `W^{2,1}`, integration by parts gives

```text
|hat q_ell(b)| <= |b|^{-2} ||q_ell''||_1.
```

The Fourier transform is integrable, and its inverse is the continuous `W^{2,1}` representative. The tail outside `[-B,B]` is bounded by

```text
A_{L,epsilon}/(pi B).
```

The rational edges are evaluated explicitly before the residual inversion. At a jump the manuscript fixes the right trace. This avoids an ambiguity in the pointwise statement.

For the full raw density the estimate is only

```text
|p_raw-p_packet|
 <= A_{L,epsilon}/(pi B)+r(ell,t)
```

almost everywhere.

The exceptional output set on which `r` exceeds a threshold has counting--Lebesgue measure bounded by the total mass divided by that threshold. This is a correct Markov estimate.

It is not a supremum estimate.

## 15. The decisive boundary-source obstruction

The nonnegative source `r` contains, among other things:

- trajectories near grazing;
- first-hit singularities;
- section-decision boundaries;
- auxiliary guard zeros;
- and the cumulative collision tail.

The manuscript controls only its total output mass.

A density with arbitrarily small total mass may have arbitrarily high narrow spikes. Therefore

```text
||r||_1 small
```

does not imply

```text
sup_{ell,t} r(ell,t) small.
```

This is not a merely technical distinction. The theorem sought in the raw portion is pointwise on microscopic scales. The omitted source could contribute exactly on those scales unless a separate coarea, distortion, or Fourier estimate is proved for it.

Revision 42 is commendably explicit about this limitation. It nevertheless remains a decisive reason that the full theorem is unproved.

## 16. The long-time parameter obstruction

To make the cumulative collision tail small for a return index of size `n`, one must choose `L` at least proportional to `n` with a sufficiently large constant. To make the guard-removal mass small, `epsilon` must also tend to zero.

But the regular-packet derivative budget is

```text
A_{L,epsilon}
 =exp{ C (L+1) log(C/epsilon) }.
```

The pointwise Fourier tail is small only when `B` is much larger than this quantity.

The spectral local-limit arguments elsewhere in the paper fix the roof band before taking the collision count to infinity. They do not provide quantitative operator constants on a band growing at the rate forced by `A_{L,epsilon}`.

Thus there is presently no demonstrated choice of

```text
L=L_n,
epsilon=epsilon_n,
B=B_n
```

for which all of the following hold simultaneously at the required local scale:

1. the cumulative tail is negligible;
2. the guard-removal mass is negligible pointwise;
3. the regular-packet Fourier tail is negligible;
4. the fixed-band spectral error remains controlled;
5. and the arithmetic main term is preserved.

This is the central quantitative gap between the new finite-packet theorem and the full raw-density theorem.

## 17. Infinite edge compatibility is still open

For each positive-margin regular word, the coefficients stabilize. This permits a canonical assignment of a pair `(a_0,a_1)` to that word.

The manuscript does not prove:

- absolute summability of these coefficients over all words;
- conditional convergence in a prescribed order;
- convergence in a distribution or function space;
- uniform control in the radius;
- or compatibility with the growing collision and roof-frequency limits.

It also does not prove that boundary words contribute no additional edge terms.

Therefore there is not yet a common infinite correction which can be subtracted from the complete raw law. The source manifest correctly keeps `infinite_critical_jet_sum_convergent` false.

## 18. Strong phase-class sources

Fix a radius and let the finite resonance generator be `q_*`, of order `d`. The measurable class source is

```text
a_l=eta_R 1_{H_R=l}.
```

The phase indicator is not known to be a strong multiplier. The manuscript avoids that assertion.

Instead it uses finite Fourier inversion:

```text
a_l nu
 = (1/d) sum_{j=0}^{d-1}
       omega^{-jl} M_{eta_R}(q_*^j nu).
```

Every `q_*^j nu` is the physical representative of a simple peripheral eigenvector and therefore lies in the strong space. Multiplication by the actual section indicator has already been proved bounded.

Thus `a_l nu` is a legitimate strong source even though multiplication by `a_l` on an arbitrary strong vector is not asserted.

This is a clean functional-analytic device and directly answers a possible objection to conditioning on measurable phase classes.

## 19. The arithmetic class local law

On the exact event, the terminal phase is the initial phase plus the arithmetic residue `r` modulo `d`.

At the `j`th resonance, the source and endpoint coefficient is

```text
w_l omega^{-jl}
  sum_h w_h omega^{jh}.
```

The inverse arithmetic phase contributes `omega^{-jr}`. Finite Fourier orthogonality gives

```text
sum_j omega^{-jr} w_l omega^{-jl}
       sum_h w_h omega^{jh}
 = d w_l w_{l+r}.
```

The orientation `l+r` is correct.

After the section normalization, the class local law is

```text
m^2 nu_R^*(E and H_R=l)
 = (d/c) |J| g_{Omega_R}(Z) w_l w_{l+r}+o_R(1).
```

Summing over `l` gives

```text
(d/c)|J| g_{Omega_R}(Z)
  sum_l w_l w_{l+r},
```

which is exactly the previously proved arithmetic main term

```text
c |J| mathfrak a_R g_{Omega_R}.
```

I found the normalization consistent.

If either relevant phase class has zero section mass, the subevent is exactly null by the phase relation and invariance, not merely asymptotically small.

## 20. The finite endpoint posterior

On a positive arithmetic residue class, division by the preceding denominator gives the limiting endpoint law

```text
pi_{R,r}(l,l')
 =1_{l'=l+r}
   w_l w_{l+r}/sum_h w_h w_{h+r}.
```

This is invariant under simultaneous relabeling of the phase classes.

The total-variation convergence is finite-dimensional and fixed-radius. The manuscript does not claim a globally continuous labeling of the phase classes through radius-dependent changes of the resonance group.

This scope is appropriate.

The result supplies a useful interpretation of the arithmetic coefficient: it is not merely a scalar correction, but the total mass of a finite endpoint matching law.

## 21. Product with the actual-return bridge

The manuscript inserts the strong class source into the pinned characteristic calculation from revision 41.

At fixed radius:

- every surviving resonance has the same Gaussian curvature `Omega_R`;
- the tied block perturbations have zero weighted sum;
- the branch drift and mixed Fourier/bridge terms cancel;
- and only the class residue coefficient changes.

The unnormalized fourth-moment estimate remains valid after restricting to one initial class because its integrand is nonnegative and the event has only been reduced. The class local law provides a positive denominator of order `m^{-2}` on every positive pair.

The pathwise occupation-clock identity and covariance transformation are unchanged on the subevent. Therefore the limiting product law

```text
pi_{R,r} tensor Law(B_{D_R})
```

is plausible and internally consistent.

I found no arithmetic dependence left in the centered bridge factor at fixed radius.

The theorem is correctly limited to:

- a fixed radius;
- a positive arithmetic class;
- the original exact displacement and collision-count constraints;
- and a fixed positive roof interval.

It is not a pointwise roof-conditioned bridge and is not asserted uniform through changes in the phase group.

## 22. What the posterior theorem does not prove

The phase posterior does not show that the phase masses are uniform.

In particular, it does not prove

```text
w_l=c/d
```

or the vanishing of every nontrivial section residue.

Consequently it does not remove the arithmetic factor from the exact-index main term. Indeed it makes the possible nonuniformity more explicit.

A fixed finite packet average removes the nonzero aliases, but that packet is a different union of exact events. It cannot replace an arbitrary preassigned singleton in the statement of a raw local theorem.

Before another top-four review, the authors should either:

- prove the zero-residue condition for the concrete moving section; or
- formulate the final singleton theorem with the arithmetic factor and the radius-uniform transition kernel as part of the main result.

## 23. The remaining pointwise roof problem

Even after adopting the correct arithmetic main term, the following are still required:

1. pointwise control of the singular/decision-boundary source;
2. a convergent common critical correction or another global treatment of all critical words;
3. quantitative control of the complete high-roof-frequency complement;
4. compatibility of that control with the fixed-count full occupation-torus spectrum;
5. a pointwise density statement, not only fixed intervals or one existential shrinking sequence;
6. and the corresponding weighted/selected statements claimed in the inherited raw pipeline.

Revision 42 advances item 2 for finite guarded packets and gives a useful decomposition for item 1. It does not finish either item.

The source manifest therefore correctly keeps the flags for the full raw LLT, the common pointwise correction, the full complement, and the pointwise roof-density theorem false.

## 24. Top-four significance

The manuscript now contains several substantial completed results:

- a parameter-uniform stationary microscopic local law;
- a compact-family action principle with noncircular applications;
- exact actual-return window and mesoscopic local laws;
- a fixed-radius exact-index arithmetic interval law;
- a radius-uniform spectral transition formula;
- an exact-event Gaussian return bridge;
- a fixed finite-packet uniform local law;
- an endpoint phase posterior;
- and a finite guarded critical-packet pointwise inversion theorem.

Subject to independent specialist verification, a focused subset of these results could support a strong dynamics/probability submission.

The present article, however, remains organized around a more ambitious raw pointwise theorem which is not proved. Its size and cumulative architecture amplify rather than reduce this issue. A top-four submission should have one unmistakable principal endpoint whose proof is complete and whose novelty is placed clearly against the existing Lorentz-process and suspension-flow literature.

At present:

- the raw endpoint is incomplete;
- the arithmetic main term is not yet settled in the concrete family;
- the generality case remains tied to a highly specialized mechanical construction;
- and the load-bearing continuum estimates have not received independent specialist audit.

I therefore do not view revision 42 as ready for *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 25. Architecture and presentation

The revision is more honest than several earlier versions about the distinction between finite packets and the full law. The abstract now states that the omitted source still requires pointwise control.

Nevertheless, the main article still combines:

1. stationary physical local limits;
2. the compact-family action principle;
3. exact-index arithmetic interval laws;
4. conditional path bridges;
5. finite phase posteriors;
6. guarded critical extraction;
7. and an unfinished global raw-density programme.

For a specialist submission before full raw closure, the completed results should be reorganized around one principal theorem. The historical pipeline, status ledgers, and unresolved global programme should not dominate the proof path.

This is not a recommendation to delete valid mathematics. It is a recommendation to separate proved theorems from research contracts and to align the title and editorial claim with the strongest completed result.

## 26. Required changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

1. **Control the omitted source pointwise.**  
   Replace the `L^1` boundary-source estimate by a local supremum, a suitable Fourier norm, or another estimate strong enough for the microscopic density theorem.

2. **Close the long-time parameter ledger.**  
   Give explicit sequences `L_n`, `epsilon_n`, and `B_n` and prove that every error tends to zero at the claimed local scale.

3. **Prove a growing-band theorem if needed.**  
   The fixed-band spectral estimates cannot simply be evaluated at the enormous bandwidth forced by the finite-packet derivative budget.

4. **Establish the infinite correction.**  
   Prove convergence of the two-jet edge series, or replace it by a global construction with the required pointwise control.

5. **Resolve the arithmetic main term.**  
   Either prove all nontrivial section residues vanish for the concrete family or state the final theorem with `mathfrak a_R` and `mathcal L_{m,R}`.

6. **Complete the full roof-frequency complement.**  
   Include the critical, singular, and decision-boundary contributions at every relevant frequency.

7. **Obtain independent specialist review.**  
   The guarded branch estimates, full occupation-torus anisotropic inequalities, holonomy argument, resonant stationary phase, and bridge tightness all require expert verification.

8. **Strengthen the novelty case.**  
   Explain theorem by theorem which conclusions are not already consequences of existing billiard local-limit, mixing-LLT, and suspension-flow frameworks.

9. **Reduce the submission burden.**  
   Present one complete principal theorem and move unresolved companion material out of the central route unless it is closed.

## 27. Technical comments

1. Keep the distinction between `B_m,C_m` as derivative entries and every unrelated use of the letter `B` for a roof-frequency band visible.
2. State the coordinate density `(4 pi c)^{-1}` whenever the stabilized critical coefficient is used outside module 90.
3. Retain the right-trace convention at an edge in every pointwise formulation.
4. Do not call the Markov exceptional-set estimate a uniform pointwise estimate.
5. Keep the condition `n<=L` explicit in all finite-packet applications.
6. Do not replace `A_{L,epsilon}` by a polynomial in `n` without a new theorem.
7. The compatibility theorem applies only to positive-margin words; boundary words require separate treatment.
8. The first-decision zero-extension proof should list every auxiliary guard factor that can define a source boundary.
9. Preserve the distinction between a strong class source and a bounded class multiplier.
10. Keep the posterior statement fixed-radius unless a continuous phase-class bundle is constructed.
11. Class pairs of zero weight are exactly null and should not be assigned conditional bridge laws.
12. The finite-packet local law is not a singleton result.
13. A slowly shrinking interval selected by diagonalization is not a prescribed density scale.
14. The arithmetic factor should remain in any candidate pointwise density main term unless the zero-residue criterion is proved.
15. Source qualification and finite models should remain separated from continuum proof certification.

## 28. Final assessment

Revision 42 is a serious and constructive response to the preceding report.

It retains the regular critical source instead of deleting the normal line, constructs intrinsic two-jet edge corrections, proves a summed finite-cutoff `W^{2,1}` residual estimate, and gives a genuine pointwise inverse for the extracted guarded packet. It also gives a clean strong-space realization of measurable phase classes, an exact-index arithmetic endpoint posterior, and an asymptotic product with the actual-return Gaussian bridge.

I found no decisive error in these new modules within the scope of this review.

The paper nevertheless remains short of the theorem which governs its title and raw-inversion architecture. The omitted boundary/singular source has only a mass estimate; the finite-packet derivative budget is incompatible with the presently available fixed-band spectral control at long times; the infinite critical correction is not shown to converge; the full roof-frequency complement is open; and the concrete arithmetic residues are not proved trivial.

Subject to independent specialist verification, the completed interval, bridge, posterior, stationary, and finite-packet results could form a strong focused paper. They do not yet constitute a complete top-four raw local inversion theorem.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
