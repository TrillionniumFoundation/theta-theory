# External top-four referee report on A2-DYN revision 38

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v38-referee-response-2026-10-08`, `revision/a2-dyn-v38-referee-copy-2026-10-08`  
**Reviewed commit:** `00f8b9baa95a2fa9d29b1e2e7164dc0f5cb2938e`  
**Reviewed repository tree:** `bb98e86761c9f4aa3b9f471b0461b27d2365129e`  
**Ordinary source payload tree:** `7ddb65e88f9aeb5a7ee5ab9d423e865092eba04a`  
**Active manuscript directory:** `papers/A2-DYN-v38-referee-response`  
**Active mathematical source:** eighty-one numbered core modules; revision 38 adds modules 80--81 and a fourth leading theorem  
**Frozen revision-37 author baseline:** `d039c92d9f957ee180b74c0f3cf4c8bf52b9547c`  
**Frozen revision-37 paper tree:** `606e3db1b2e8dce1fbf9f17d3ef7251ec99d519f`  
**Controlling report:** `reviews/a2-dyn-v37-external-top4-review-2026-10-08/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `08562f799dd967056c81324c55ddcd9b91d79c14` / `ddb96a111b7e39ce7f1b2767668fd86fb17d10c9`  
**Date:** 8 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 38 is a genuine theorem-bearing advance over revision 37. It does not merely repackage the diffusive-window theorem. The new argument uses the fixed small neighborhood of the true occupation frequency already constructed in revision 37 to obtain a four-dimensional absolute inverse estimate at the natural scale `m^(-2)`. From this it proves:

1. an all-target, parameter-uniform concentration upper bound for one exact actual-return index;
2. a Gaussian local theorem for every block of consecutive return indices whose cardinality tends to infinity, however slowly;
3. the correct normalization in the original four-coordinate return covariance `D_R`; and
4. an exact full-occupation-torus identity which separates the proved Gaussian contribution from the still-uncontrolled signed remainder.

I audited the two new modules

- `core/80_four_dimensional_concentration.tex`;
- `core/81_return_resolution_and_complement.tex`;

and their use in the fourth leading theorem. I found no decisive counterexample, Fourier-sign inconsistency, incorrect endpoint count, missing factor of the section mass, covariance-Jacobian error, or illicit substitution of a growing Fourier band into a fixed-band spectral estimate.

The following aspects of the new proof are particularly sound.

- The fixed occupation strip is used exactly within its proved scope. The strip width may shrink when the roof band grows, and no lower bound uniform in that band is assumed.
- The four-dimensional central integral has size `m^(-2)`, as required for two exact lattice displacement coordinates, one exact occupation coordinate and one unscaled roof interval.
- The lower product envelope is not taken to be the product of two possibly negative minorants. The manuscript uses the correct order-preserving combination

  ```text
  q^- p^+ + q^+ p^- - q^+ p^+.
  ```

- The moving-window theorem retains the Gaussian average across the whole occupation block. Its error has the explicit form

  ```text
  epsilon_m(B) + C_J/B + C_J/(sigma_B H),
  ```

  with the band fixed first, the occupation strip fixed second, and the collision count tending to infinity before the final band limit.
- The exact return/occupation disintegration is unchanged: on section-to-section trajectories, `A_m=n` is equivalent to `N_n=m`, with the terminal visit excluded from `[0,m)`.
- The manuscript does not set `H=1` in a theorem whose final error contains `1/H`.

These are substantial improvements. In particular, the new result reaches every diverging return-index width, including logarithmic, iterated-logarithmic or still slower deterministic widths. A fixed diffusive-window weak limit does not imply this moving-window statement.

The negative recommendation is nevertheless forced by the exact endpoint still missing from the paper. Revision 38 proves a natural upper bound for one index, but it does **not** prove the Gaussian asymptotic for one index. Its exact inversion formula leaves a signed integral over the occupation torus outside the controlled strip. The paper explicitly records that the cancellation

```text
m^2 R^q_{n,m,R}(k,t) -> 0
```

is unproved. This is not a cosmetic remainder: it contains all noncentral occupation frequencies needed to distinguish one exact return index from every diverging block.

Furthermore, the roof variable remains tested on a fixed interval. The single-index upper bound is

```text
C (1+|J|) m^(-2),
```

not `C |J| m^(-2)`. It therefore does not imply a pointwise density bound by division by `|J|`. The common raw correction, critical/singular edge contribution and full roof-frequency complement of the four-coordinate return law also remain open.

Thus revision 38 has crossed from a diffusive return window to arbitrarily fine mesoscopic windows and exact-index concentration, but it has not crossed to the advertised singleton raw mixed-density local limit theorem.

At the requested benchmark, the article would need either:

1. the complete exact-index, pointwise-roof raw-return theorem which continues to organize the manuscript; or
2. a general result of independent scope and breadth whose significance does not depend on that unfinished endpoint.

Revision 38 supplies neither yet, although it materially narrows the first gap.

## 2. Frozen source and chronology

Both reviewed author branches resolve to

`00f8b9baa95a2fa9d29b1e2e7164dc0f5cb2938e`.

The repository tree at that commit is

`bb98e86761c9f4aa3b9f471b0461b27d2365129e`.

The active manuscript is

`papers/A2-DYN-v38-referee-response`.

The source manifest identifies revision 37 as the exact author baseline. All seventy-nine inherited core files and all eighty-seven inherited Python files are retained byte-for-byte. The bibliography, inherited mathematical labels and compiled A--X synopsis are retained. Revision 38 adds the two modules listed above and modifies the front matter by adding Theorem 4 and the corresponding synopsis material. The previous main source is archived under provenance.

The branch history also preserves the revision-37 external report. This is the correct chronology: the author revision begins from the controlling review commit, then adds a new manuscript tree. It is not a review commit relabeled as an author source.

The present review branch begins directly from the reviewed author commit and adds only this report under

`reviews/a2-dyn-v38-external-top4-review-2026-10-08/`.

No author manuscript source, prior review, workflow or unrelated repository path is intentionally modified.

## 3. Qualification evidence and verification boundary

The exact-source qualification workflows completed successfully on both reviewed branches:

- response branch run `37664399588`;
- referee-copy branch run `37664412625`.

The verifier checks, among other things:

- the frozen revision-37 paper identity;
- all eighty-one core inclusions;
- byte identity of the seventy-nine inherited cores and eighty-seven inherited scripts;
- preservation of inherited labels, bibliography and the A--X appendix;
- the exact controlling-report blob and workflow hash;
- the ordinary-source Merkle identity;
- normal/optimized agreement;
- native TeX compilation and theorem-label-based proof-page rendering.

The new finite diagnostics test product-envelope algebra, covariance determinants, half-integer block boundaries, finite occupation Fourier inversions and nonintegral centering phases. Negative controls reject the product of two negative minorants, terminal-visit miscounting, parity-based inference of singleton asymptotics, the substitution `H=1`, and use of an uncontrolled shrinking strip.

These are meaningful source, algebra and regression checks. They do not establish the inherited continuum collision-space estimates, the exact section multiplier, the small-occupation resolvent perturbation, the uniform joint spectral expansion, or the local theorem itself. The manuscript and its validation record state this limitation accurately.

## 4. Scope of this review

I did not attempt to re-prove all eighty-one mathematical modules. The substantive audit concerns:

1. the fixed-strip integral and its coverage;
2. the all-target single-index concentration estimate;
3. the signed product-envelope lower bound;
4. the moving-envelope lemma and its uniformity in the block width;
5. the iterated order of limits;
6. the passage from occupation blocks to actual-return blocks;
7. the original covariance normalization;
8. the exact occupation-torus remainder identity;
9. the distinction between concentration, mesoscopic local limits, exact-index local limits and pointwise roof density;
10. source identity and qualification evidence.

The inherited revision-37 results are treated as the source-pinned baseline: exact section multiplication, the joint near-zero expansion, the fixed displacement--roof band gap for small occupation frequency, strong-space faithfulness, finite-cover mixing, and exact return disintegration. This report does not convert those inherited claims into independent human proof certification.

## 5. The fixed four-dimensional strip

For a fixed roof band `|b| <= B`, revision 37 provides two inputs:

- a joint analytic spectral expansion near `(u,b,v)=0` with uniformly positive covariance `Omega_R`;
- a compact spectral gap for displacement--roof frequencies away from zero, stable under sufficiently small occupation frequency `v`.

Revision 38 chooses `sigma_B` after `B` and splits

```text
T^2 x [-B,B] x [-sigma_B,sigma_B]
```

into a neighborhood of the four-dimensional origin and its complement.

Near zero, the eigenvalue satisfies a Gaussian bound

```text
|lambda_R(u,b,v)|^m <= exp(-c m |(u,b,v)|^2).
```

Its integral in four variables is `O(m^(-2))`. The complementary spectral part has exponentially decaying powers on a fixed-volume set.

Away from the displacement--roof origin, the revision-37 compact gap applies after `sigma_B` is chosen below the corresponding occupation radius. The remaining region with small displacement--roof frequency but non-negligible occupation frequency still lies in the fixed joint-analytic neighborhood and is controlled by the same positive covariance.

This covers the entire displayed strip. The proof does not assume any spectral information for `|v| >= sigma_B`, and it does not claim that `sigma_B` stays positive as `B` tends to infinity.

The resulting estimate

```text
integral_strip |Phi_{m,R}| <= C_B m^(-2)
```

has the correct dimension and is sufficient for the subsequent band-limited concentration argument.

I found no gap in this covering argument, subject to the inherited revision-37 joint expansion and compact perturbation theorem.

## 6. Exact Fourier conventions

For compactly supported Fourier tests `q` in the roof coordinate and `p` in the occupation coordinate, the inverse contains

```text
hat q(-b) hat p(-v)
```

and the oscillation

```text
exp(-i[u.k + b(t-m bar_tau_R) + v(ell-mc)]).
```

These signs agree with testing `q(S_m-t)` and `p(A_m-ell)` under the convention

```text
hat q(b)=integral exp(i b s) q(s) ds.
```

The manuscript also keeps the occupation multiplier on the source side and the preceding displacement--roof multiplier on the image side. This preserves the `[0,m)` occupation count. I found no terminal-index shift or sign mismatch in the new inversions.

The estimate

```text
|I_m(q,p)| <= C_B m^(-2) ||q||_1 ||p||_1
```

follows from the strip integral and the elementary bounds on Fourier transforms. It is uniform in every target, not only in the central region.

## 7. Product envelopes

This is a small but load-bearing point.

A Beurling--Selberg minorant of an interval need not be nonnegative. Consequently, the product of two minorants need not lie below the product of the two interval indicators.

The manuscript avoids this error. If

```text
q^- <= f <= q^+,
p^- <= g <= p^+,
```

with `f,g` interval indicators and `q^+,p^+` nonnegative majorants, it proves

```text
q^- p^+ + q^+ p^- - q^+ p^+ <= f g <= q^+ p^+.
```

The lower inequality is obtained by writing the deficit of the upper product and bounding its two positive pieces separately. It survives multiplication by the nonnegative physical endpoint weight.

The corresponding lower limiting mass is `|J|-2 pi/B`, not the product of two lower masses. This is exactly the combination needed in the two-band squeeze.

I found this algebra correct.

## 8. Single-index concentration

For an occupation singleton, integer-valuedness gives

```text
1_{A_m=n}=1_{[-1/2,1/2]}(A_m-n).
```

A positive band-limited majorant of this unit interval and a positive majorant of a roof interval of length at most one can be inserted into the four-dimensional strip inverse. Their `L^1` norms are fixed constants. This gives

```text
P{K_m=k, A_m=n, S_m-t in J} <= C m^(-2)
```

for `|J| <= 1`, uniformly in all targets. Covering a bounded roof interval by at most `|J|+2` unit intervals gives

```text
P{...} <= C(1+|J|)m^(-2).
```

After the exact section-to-section disintegration, the same estimate holds for

```text
nu_R^*{K_{n,R}=k,N_{n,R}=m,T_{n,R}-t in J}.
```

This is a genuine exact-index statement and has the natural four-coordinate scale. It is also correctly described only as an upper bound.

Two limitations are decisive.

First, no matching lower bound is obtained for one index. Second, the additive constant in `1+|J|` prevents the estimate from yielding a density bound as the roof interval shrinks.

The manuscript states both limitations.

## 9. Uniform moving tests

The main advance over revision 37 is not the fixed-strip upper bound alone. It is the uniform treatment of an occupation interval whose width `H=H_m` changes with `m`.

After division by `H`, the Fourier transform of either occupation envelope is bounded by

```text
1 + 2 pi/(sigma H).
```

This bound is uniform in `H >= 1`. In the four-dimensional central rescaling, the spectral error is therefore dominated by one Gaussian `L^1` function independent of the window width. The replacement of the envelope transform by the exact interval transform costs

```text
C/(sigma H).
```

The Gaussian part is not replaced immediately by its value at the block center. The proof retains

```text
G_{m,H,R}(z,y)
 = H^(-1) integral_{-H/2}^{H/2}
     g_{Omega_R}(z,y+s/sqrt(m)) ds.
```

This makes the statement valid for diffusive and wider windows as well as subdiffusive ones.

For each fixed roof band `B`, the occupation width `sigma` is fixed within the valid strip. The error `epsilon_m(B)` then tends to zero uniformly in `H`. If `H >= h_m` and `h_m -> infinity`, the term `1/(sigma h_m)` also tends to zero. Only after this first limit is taken does the proof let `B` tend to infinity.

This proves the theorem for every diverging width without a polynomial lower-growth condition. The quantifiers are correctly ordered.

I found no hidden growing-band substitution in this argument.

## 10. From occupation blocks to return-index blocks

The half-integer interval

```text
[j-1/2, j+H-1/2]
```

selects exactly the consecutive integers

```text
{j,j+1,...,j+H-1}.
```

On a trajectory beginning and ending in `Y_R^*`, the exact identity

```text
A_{m,R}=n  <=>  N_{n,R}=m
```

holds with occupation counted on `[0,m)`. Additivity identifies the displacement and roof variables as well.

The collision endpoint weight is `eta_R(x) eta_R(T_R^m x)`. Its product of collision means is `c^2`; disintegration from collision measure to the normalized section probability divides by `c`. The resulting amplitude is therefore `c`.

Thus the new actual-return theorem is

```text
(m^2/H) sum_{n in block} P_{n,m,R}(k,t;J)
  = c |J| G_{m,H,R}(z,y) + o(1).
```

For `H=o(sqrt(m))`, the Gaussian average reduces uniformly to `g_{Omega_R}(z,y)`. On central compact sets it gives a positive block denominator of order `H m^(-2)`.

I found the section-mass normalization and block endpoint convention correct.

## 11. Original return covariance

Revision 37 established

```text
Omega_R = c L_R D_R L_R^T,
det L_R = c.
```

Hence

```text
det Omega_R = c^6 det D_R.
```

For a block centered at `ell`, the inverse linear map gives the original centered return coordinates

```text
(k_1,k_2,m-ell/c,t-ell bar_tau_R/c).
```

Since `ell/m=c+O(m^(-1/2))` on the central set, multiplying the collision-clock formula by `ell^2/m^2` converts the limit to

```text
(ell^2/H) sum_{n in block} P_{n,m,R}(k,t;J)
  = |J| g_{D_R}(V_{ell,R}) + o(1).
```

A half-integer block center causes no problem; every summand still has an integer return index.

This normalization is coherent and introduces no new covariance.

## 12. The exact occupation-torus remainder

The most useful conceptual addition of revision 38 is the exact localization of the remaining single-index obstruction.

For a fixed band-limited roof test `q`, full torus orthogonality in the integer occupation count gives an exact integral over `v in [-pi,pi]`. A smooth torus cutoff `chi_B`, supported in the proved small occupation strip and equal to one near zero, splits that integral into:

1. a central strip contribution evaluated by four-dimensional rescaling; and
2. the signed remainder with factor `1-chi_B(v)`.

The central contribution is

```text
c (integral q) g_{Omega_R}(Z) m^(-2) + o(m^(-2)).
```

The remaining expression is explicit and uses only finite powers of the exact one-step multipliers. The manuscript does not assume long-power bounds on the whole torus.

Centering by `mc` does not destroy the identity. Although the centered factors are not individually periodic when `mc` is nonintegral, the inverse oscillation and the characteristic factor multiply to `exp(i v(A_m-n))`, which is periodic.

For each fixed roof test, the exact-index local theorem is therefore equivalent to cancellation of this signed remainder on the normalized scale.

This equivalence is correct. It is not a proof of the cancellation.

## 13. Why fine windows do not imply a singleton asymptotic

The moving-window error contains

```text
C/(sigma H).
```

For every `H_m -> infinity`, this term disappears after fixing the band. For `H=1`, it does not.

This is not merely a defect of the proof's presentation. Averages over every diverging block can be compatible with bounded oscillations at the lattice scale. The exact-index concentration bound controls the amplitude of such oscillations but does not identify their signed limit.

The uncontrolled occupation-torus frequencies are precisely where such lattice-scale oscillation or arithmetic structure would live. They must be analyzed independently.

Revision 38 correctly refuses to infer the singleton theorem from parity-compatible or other mesoscopic averages.

## 14. Why fixed roof intervals do not imply the raw density theorem

The new theorem localizes the roof sum to a fixed interval of positive length. The manuscript's original target is pointwise in the continuous roof coordinate.

The exact-index concentration estimate has the form

```text
C(1+|J|)m^(-2).
```

As `|J|` tends to zero, this does not decay proportionally to `|J|`. It therefore cannot be divided by the interval length to produce a local essential-supremum density estimate.

Moreover, the exact fixed-band remainder controls neither:

- the far roof frequencies;
- the common signed raw correction;
- the critical and singular edge contributions;
- the complete return-frequency complement.

These are the same pointwise inversion obligations retained from the earlier raw-return pipeline.

Accordingly, even a future proof of full occupation-torus cancellation for every fixed roof band would still leave the pointwise roof-density theorem to be completed.

## 15. The remaining mathematical obligations

The manuscript's source manifest and proof ledger accurately mark the following as unproved:

1. **Full occupation-torus cancellation.**  
   Prove that the signed remainder outside the fixed small strip is negligible for the actual section endpoints and the required roof tests.

2. **Exact-return-index Gaussian asymptotics.**  
   Upgrade the natural `m^(-2)` upper bound to

   ```text
   m^2 P_{n,m,R}(k,t;J)
     = c |J| g_{Omega_R}(Z) + o(1)
   ```

   for one index.

3. **Pointwise roof inversion.**  
   Pass from fixed intervals to the raw continuous density, with a local norm strong enough to control microscopic conditioning.

4. **Common pointwise return correction.**  
   Estimate the signed correction produced by the critical-edge/residual decomposition.

5. **Full return-frequency complement.**  
   Control all remaining roof and return frequencies, including the singular and peripheral regions required by the original theorem.

6. **Weighted and path-level consequences.**  
   Evaluate the required selected amplitudes and denominators before asserting general microscopic conditional path bridges.

These are central theorem obligations, not editorial details.

## 16. Specialist verification still required

The new modules introduce no new billiard singularity partition, but they depend on the full continuum chain established in revisions 35--37. The highest-priority independent checks remain:

- the five-rectangle section as a bounded multiplier on the same collision spaces;
- source/image chronology and the exact `[0,m)` occupation convention;
- the three action-weighted collision norm inequalities;
- intermediate regularity of every matched connector;
- faithfulness of the strong completion;
- physical representatives of peripheral vectors;
- finite-cover mixing and the phase-rigidity argument;
- parameter-uniform small-occupation resolvent perturbation;
- the joint four-dimensional covariance expansion;
- the fixed-strip covering in revision 38;
- uniformity in `H` of the moving-envelope comparison;
- the full-torus centering and cutoff identity.

I found no fatal defect in the written revision-38 deduction. That conclusion is conditional on the inherited continuum results and is not a substitute for an expert audit by researchers in dispersing billiards and anisotropic transfer operators.

## 17. Significance at the requested benchmark

Revision 38 strengthens the significance case relative to revision 37. The manuscript now contains:

- a parameter-uniform stationary microscopic local theorem;
- a compact-family action principle with ellipse and genuinely nonelliptic applications;
- an exact true-section occupation multiplier;
- a diffusive-window actual-return local theorem;
- an exact-index natural-scale concentration estimate;
- local Gaussian asymptotics for every diverging return-index block;
- an exact formula locating the remaining singleton obstruction.

This is a substantial body of work.

Nevertheless, the strongest new return theorem remains mesoscopic in the return index and interval-valued in the roof coordinate. The original singleton raw-return theorem remains the article's organizing claim, title-level endpoint and principal source of the long critical-edge and inversion architecture.

The completed package is also still tied to finite-horizon periodic dispersing billiards, the existing collision anisotropic framework, a specific genuine section geometry and one lattice model, even though the stationary physical theorem has been generalized to compact obstacle families.

In my judgment, this is not yet a convincing *Annals* / *Acta* / *Inventiones* / *JAMS* submission. The gap is now sharply isolated rather than diffuse, but it is still the gap between mesoscopic resolution and the advertised microscopic raw theorem.

A materially stronger top-four case would result from either:

- proving full occupation-torus cancellation and pointwise roof inversion for the original return record; or
- extracting a general exact-index resolution theorem for a broader class of singular hyperbolic systems, with multiple independent applications and a significance argument not tied to this one unfinished raw theorem.

## 18. Architecture and submission strategy

The four leading theorems now distinguish their topologies more honestly than earlier cumulative synopses. Theorem 4 clearly separates:

- one-index concentration;
- diverging-block Gaussian asymptotics;
- fixed roof intervals;
- the unproved exact-index remainder.

This is good exposition.

The article remains very large and combines several layers:

1. stationary physical local limits;
2. a compact-family geometric action principle;
3. true-section occupation and mesoscopic return resolution;
4. an incomplete pointwise raw-return inversion programme.

For a specialist or high-level dynamics/probability submission, the authors should choose one principal endpoint.

- If the unified paper is retained, complete the exact-index and pointwise-roof theorem.
- If the current results are submitted before that closure, the stationary/action theorem and the return concentration/fine-window theorem should form a self-contained paper, while the unfinished raw-density programme is clearly separated as a sequel or technical companion.

This is not a recommendation to delete valid mathematics. It is a recommendation to align the title, abstract, proof architecture and editorial claim with the strongest theorem actually proved.

## 19. Required changes before another top-four review

A subsequent top-four revision should address the following items.

1. **Control the full occupation torus.**  
   Prove the cancellation of `R^q_{n,m,R}` or derive a full-torus spectral/arithmetic alternative sufficient for the exact return index.

2. **Complete pointwise roof inversion.**  
   The common correction and full roof complement must be controlled in the local norm required by the raw density theorem.

3. **State the exact arithmetic obstruction.**  
   Identify all possible nonzero occupation phases and explain whether their exclusion follows from finite-cover mixing, actual-return arithmetic, or a new induced/renewal argument.

4. **Keep all limit orders explicit.**  
   Any future enlargement of roof or occupation bands must state which constants depend on which band and must not substitute an `m`-dependent band into a fixed-band estimate without a new quantitative theorem.

5. **Preserve the distinction between bounds and asymptotics.**  
   The exact-index upper bound, diverging-window asymptotic, singleton asymptotic and pointwise density theorem must remain separate claims.

6. **Obtain independent specialist review.**  
   The inherited action-weighted and section-multiplier chain and the new fixed-strip deduction require expert verification.

7. **Strengthen the generality and novelty case.**  
   Explain theorem by theorem what is not already organized by existing Lorentz-process, billiard mixing-LLT and suspension local-limit frameworks.

8. **Reduce the submission burden.**  
   Present one unmistakable principal theorem and move historical pipelines, status ledgers and unresolved companion programmes out of the main proof path where possible.

## 20. Technical and presentation comments

1. The dependence `sigma_B=sigma(B)` should remain visible in every theorem or corollary that uses the fixed strip.
2. The phrase “all-target concentration” should always refer to the upper bound, not to a Gaussian approximation.
3. The exact-index criterion should continue to be labeled conditional until the torus remainder is estimated.
4. The interval length in the roof theorem is fixed before the collision limit; any shrinking-interval statement would require new uniformity.
5. The distinction between the Gaussian window average `G_{m,H,R}` and its center value should remain explicit for diffusive or wider windows.
6. The intersection with `[1,m]` in the actual-return block should be retained outside the subdiffusive central regime.
7. Endpoint-selected lower bounds require uniformly positive section means; they do not follow for arbitrary bounded path selectors.
8. The total-variation posterior results from the stationary physical theorem should not be cited as exact-index return-density asymptotics.
9. Qualification runs and finite models should remain separated from proof certification, as they are in the current metadata.
10. The next response should identify its exact author SHA and not use a review commit as a mathematical baseline.

## 21. Final assessment

Revision 38 is a real and important advance.

It proves the natural four-dimensional concentration upper bound for one exact actual-return index and upgrades the return-index local theorem from diffusive windows to every diverging block. The moving-test proof is not a formal consequence of revision 37; the order-preserving two-envelope argument and the uniform `H` analysis are substantive. The original covariance normalization and section endpoints are maintained exactly. I found no decisive error in the new modules.

The paper nevertheless remains short of its stated raw-return endpoint. Exact-index Gaussian cancellation on the full occupation torus is unproved, and pointwise roof inversion still requires the common correction and complete return-frequency complement. The manuscript itself acknowledges these facts.

Subject to independent specialist verification, the completed concentration and fine-window results could support a strong dynamics/probability submission, especially if presented together with the stationary compact-family theorem in a focused architecture.

At the requested four-journal benchmark, however, the central singleton raw theorem remains incomplete and the current breadth/significance case does not compensate for that incompleteness.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
