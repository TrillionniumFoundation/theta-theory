# Independent Proof and Pipeline Audit — General Theta Foundations I, Revision 74 (r48)

**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed exact final head:** `8477a4c44cbed327068ab895c244f2ddfa86e27a`  
**Candidate publication:** `7753a7512c2e8d724fbbff4585017c3dd1b3825b`  
**Qualified native source:** `82f9f5c9868f7ad5847784bf92109f297ae0b876`  
**Revision 73 base:** `ab67d30dc8ad190f1e4cea150a306c8ca3a4dc1f`  
**Prior external report:** v73/r47, `fa857238020a0b5f2befd936b39820a9b426390a`  
**Prior proof/pipeline audit:** `62ffc56f0911b939f3e6b79ae0a5e38563e5a988`  
**Source qualification run:** `37172756259`, success  
**Exact-head read-only run:** `37173200597`, success  
**Audit branch:** `review/general-theta-foundations-i-v74-proof-pipeline-audit-r48-2026-10-04`  
**Date:** 4 October 2026

## Executive classification

| Dimension | Independent audit result |
|---|---|
| Latest revision identity | **Pass.** v74 is the latest completed referee-ready GTF-I object; no v75 branch was found. |
| Exact branch identity | **Pass.** The v74 work and referee-ready branches point to the same exact head, `8477a4c44...`. |
| Source genealogy | **Pass.** Completed v73, v74 native source, candidate publication, and final request form a direct seven-commit chain. |
| Full binary-qubit-ball metric | **Pass with model scope.** No fatal gap found in the radial equality, support-cutoff estimate, angular inheritance, or cancellation-free coupling. |
| Exact one-use norm | **Pass.** The reference-assisted ordered-outcome distance is `|x-y|`. |
| Weighted local covering criterion | **Pass under Ahlfors regularity and small error.** Arbitrary legal lower centres are handled by separation and triangle inequality. |
| Boundary-contact trichotomy | **Pass.** The Stieltjes calculation yields the interior, critical-log, boundary-dominated, and boundary-atom regimes. |
| Disk/ball covering orders | **Pass.** The coordinate disk is critical and the full ball is boundary dominated. |
| Rational joint codec | **Pass for the declared rational target interface.** The algorithm charges visibility and direction in one index and decodes every word legally. |
| Irrational target norm handling | **Pass.** Exact rational comparisons avoid computing the norm or normalized direction. |
| Implementation regression | **Pass as finite evidence.** It does not prove the continuum metric, adaptive supremum, covering theorem, or priority. |
| Source qualification | **Pass.** Run `37172756259` completed successfully. |
| Exact final-head reconstruction | **Pass.** Run `37173200597` reconstructed `8477a4c44...` read-only and rebuilt the journal package. |
| Cryptographic signature | **Open.** The final commit is unsigned and no contrary claim is made. |
| Independent priority clearance | **Not established.** The author audit is targeted and omits the 2009 two-copy adaptive measurement-discrimination paper. |
| Whole Theta A/B/C/D closure | **Open.** All aggregate completion flags remain false. |
| Four-leading-journal threshold | **Not met.** This is an editorial significance conclusion, not a correctness failure. |

The local v74 proof package is coherent. The principal new theorem gives a finite-use operational geometry for one fixed measurement body and converts it into weighted covering laws. This is substantially stronger than v73, but it remains a specialist result and does not close the repository-wide analytic programme.

---

## 1. Frozen object and branch genealogy

The latest completed manuscript branches located were

```text
revision/general-theta-foundations-i-v74-coupled-boundary-geometry-2026-10-04
revision/general-theta-foundations-i-v74-referee-ready-2026-10-04.
```

Both point to

```text
8477a4c44cbed327068ab895c244f2ddfa86e27a.
```

No Revision 75 branch was present in the complete branch survey. Existing external review branches stop at Revision 73/r47 before the present audit.

The exact head has parent candidate publication

```text
7753a7512c2e8d724fbbff4585017c3dd1b3825b
```

and adds only the final exact-head request. The candidate publication is a direct successor of native theorem source

```text
82f9f5c9868f7ad5847784bf92109f297ae0b876.
```

The mathematical predecessor is completed Revision 73:

```text
ab67d30dc8ad190f1e4cea150a306c8ca3a4dc1f.
```

A direct comparison shows v74 seven commits ahead of v73, with a new isolated revision directory, new build and exact-head workflows, the coupled-geometry section, codec, regression suite, response/audit files, rendered papers, and evidence. Existing historical branches and predecessor paths were not overwritten.

Both r48 review branches were created directly from `8477a4c44...`. Each is intended to contain exactly one report commit and no manuscript-source mutation.

---

## 2. Active proof dependency graph

### 2.1 Inherited v73 equal-visibility angular chain

```text
ordered binary equatorial measurement at public visibility lambda
  + exact one-use effect norm
  -> hybrid N-use upper bound

pair-dependent common extremal programmes
  + product classical fidelity
  -> noisy square-root upper modulus

finite GHZ blocks
  + parity extraction
  + finite Bernoulli majority estimate
  -> matching lower modulus

combine
  -> d_N(theta,phi;lambda)
       comparable to min{1,K_(N,lambda) h(theta,phi)}
```

where

```text
K_(N,lambda)=lambda sqrt(N min{N,(1-lambda^2)^(-1)}).
```

Revision 74 uses this theorem only on a same-radius great-circle comparison.

### 2.2 New v74 radial chain

```text
aligned measurements M_(ru), M_(su)
  -> one fixed projective measurement along u
  + independent Bernoulli flip programme
  -> exact equality with N-fold Bernoulli product distance

smaller success probability q=(1-s)/2
  + block length min{N,floor((2q)^(-1))}
  + no-success event
  -> block probability gap of order k(r-s)

common affine binary processing
  -> opposite symmetric Bernoulli biases

finite Bernoulli majority lemma
  -> lower scale
       min{1, sqrt(N/(1-s^2+1/N))(r-s)}

one-bit coupling + product fidelity
  -> matching upper scale
```

The `1/N` cutoff makes the estimate finite at the projective endpoint.

### 2.3 Coupled radial/angular chain

```text
x=ru, y=sv, r>=s
  + input the +u eigenstate
  -> binomial pair with upper parameter
       q'=(1-s cos h)/2 >= (1-s)/2

monotone likelihood ratio
  -> actual coupled pair dominates aligned radial pair

triangle inequality
  -> same-radius angular distance <= 2 actual distance

radial lower + inherited angular lower
  -> cancellation-free joint lower bound

radial upper + inherited angular upper
  + Euclidean chord/angle inequalities
  -> joint upper bound
```

This yields

```text
d_N(M_x,M_y)
asymp min{1,a_N(min{|x|,|y|}) |x-y|}
```

with absolute constants.

### 2.4 Local weighted geometry

```text
e_N(x)=1-|x|^2+1/N
w_N(x)=sqrt(N/e_N(x))

Euclidean radius t/w_N(x)
  -> relative variation of e_N is O(t)
  -> local comparability of weights

operational distance <= t
  + joint metric lower bound
  -> Euclidean localization at radius O(t/w_N(x))

k-Ahlfors regularity of identifiable X
  -> weighted measure w_N^k mu
       assigns mass Theta(t^k) to small operational balls

maximal separated nets
  -> upper and lower covering numbers
```

No family retraction or common estimator is used.

### 2.5 Boundary contact

```text
weighted covering integral
  = delta^(-k) N^(k/2)
      ∫ (1-|x|^2+1/N)^(-k/2) dmu

boundary-depth distribution F(t)
  + Stieltjes integration by parts
  -> compare ∫ (t+1/N)^(-k/2) dF(t)

F(t) ~ t^alpha
  -> alpha>k/2: interior order
  -> alpha=k/2: logarithmic enhancement
  -> alpha<k/2: boundary-dominated order

F(0)>0
  -> N^k boundary atom order
```

### 2.6 Exact rational joint code

```text
rational Cartesian target x
  + Q=sum x_j^2 rational
  -> exact comparison with rational radial layers
       r_i=2(i/B)/(1+(i/B)^2)

maximal coordinate axis
  + exact comparisons of x_l/(sqrt(Q)+|x_j|)
  + sign test before squaring
  -> nearest rational stereographic direction digits

radial layer + chart + digits
  -> one integer payload

rational radius x rational unit direction
  -> legal rational Bloch vector
  -> legal ordered binary measurement

radial fidelity budget + angular v73 budget
  -> total operational error below requested tolerance
```

### 2.7 Inherited structural and earlier quantitative graphs

The complete edition retains:

```text
stationarization under eventual approximate returns
stochastic purification and finite physical actions
repeatable classical-probe causal strong converse
spectral-entropy width laws
return-free/no-idle occupation
exponential accuracy crossover
uniform numerical streaming
positive instrument and Choi streaming
intrinsic/adaptive instrument description entropy
rank-aware preparation codes
coherent and input-dependent instrument families
observable projective readout and uniformly seizable covering transfer
```

None of these inherited chains becomes a new v74 result merely because it is present in the complete edition.

---

## 3. Claim-by-claim status table

| Claim | Main source | Audit result | Principal qualification |
|---|---|---|---|
| Finite-use measurement-ball metric | `sections/50-coupled-boundary-geometry.tex` | No fatal gap found | Ordered unbiased binary qubit measurements only. |
| Exact radial Bernoulli reduction | Lemma `radial74` | Correct | Aligned Bloch directions; fixed projective measurement plus flips. |
| Radial support-cutoff lower bound | Lemma `radial74` | Correct | Uses inherited finite Bernoulli majority lemma. |
| Radial product-fidelity upper bound | Lemma `radial74` | Correct | Constants safe, not optimal. |
| Cancellation-free radial/angular coupling | Theorem `ballmetric74` | Correct | Depends on binomial stochastic ordering and inherited v73 angular theorem. |
| Exact one-use distance `|x-y|` | Theorem `ballmetric74` | Correct | Ordered outcomes and unhalved trace norm. |
| Weighted local covering theorem | Theorem `weightedcover74` | Correct under hypotheses | Compact identifiable `k`-Ahlfors regular target and sufficiently small error. |
| Arbitrary legal lower centres | Theorem `weightedcover74` | Correct | Follows from separated packing and triangle inequality, not retraction. |
| Boundary-contact trichotomy | Corollary `contact74` | Correct | Requires two-sided depth-distribution bounds. |
| Disk covering `N log N delta^-2` | Corollary `jointball74` | Correct | Coordinate disk, fixed dimension, small error. |
| Ball covering `N^2 delta^-3` | Corollary `jointball74` | Correct | Full three-dimensional Bloch ball. |
| Rational joint codec | Theorem `jointcodec74` | No fatal gap found | Rational Cartesian targets; dimensions two and three. |
| Every payload word is legal | `coupled_codec.py` | Correct | Canonical target replay is separate. |
| Capacity upper orders | Theorem `jointcodec74` | Correct | Pseudo-polynomial enumeration; no optimal leading constants. |
| Source/build reproducibility | workflows and receipts | Pass | Not mathematical proof or priority certification. |
| Whole Theta closure | status and ledger | Correctly false | No A/B/C/D aggregate gate is discharged. |

---

## 4. Detailed proof audit: radial geometry

### 4.1 Exact programme equality

For the measurement with Bloch vector `tu`, first measure projectively along `u`, then flip the output with probability `(1-t)/2`. This representation uses one processor independent of `t`; the programme is one classical bit per device use.

For any adaptive tester making at most `N` calls, draw `N` programme bits in advance. Conditioned on the bits, every subsequent tester operation is common under the two target measurements. Trace-norm contraction gives the product-Bernoulli upper bound. Repeated `+u` eigenstate inputs expose the programme bits exactly, proving equality.

This remains valid with a finite reference, adaptive feedback, and bounded public stopping. Unused programme bits are ignored after stopping.

### 4.2 Block selection

Let

```text
p=(1-r)/2,
q=(1-s)/2,
Delta=q-p,
```

with `0<=p<=q<=1/2`. When `Delta=0`, the pair is identical. Otherwise `q>0`.

The block size

```text
k=min{N,floor((2q)^(-1))}
```

satisfies a constant-factor lower comparison with `min{N,q^(-1)}`. The number of complete blocks `m=floor(N/k)` satisfies `m>=N/(2k)`.

The no-success probabilities

```text
e_p=(1-p)^k,
e_q=(1-q)^k
```

have difference at least `k Delta/2`. The use of Bernoulli's inequality is valid because `(k-1)q<=1/2`.

### 4.3 Symmetric-bias processing

The map

```text
z -> b + c z
```

with

```text
c=1/max{e_p+e_q,2-e_p-e_q},
b=(1-c(e_p+e_q))/2
```

is a stochastic binary channel. It sends the two block events to Bernoulli laws with opposite biases. The denominator lies in `[1,2]`, so `c>=1/2`; the chosen `b` lies in `[0,1-c]`.

The inherited majority lemma applied to `m` independent processed blocks gives a lower bound proportional to

```text
min{1, Delta sqrt(N min(N,q^(-1)))}.
```

Using `1-s^2=2q(1+s)` converts this to the stated radial scale. The constants are conservative.

### 4.4 Upper bounds

A coordinatewise coupling of the Bernoulli bits gives a linear bound of order `N(r-s)`. Root-fidelity comparison gives a square-root bound of order

```text
sqrt(N)(r-s)/sqrt(1-s^2)
```

when `s<1`. Taking the better bound is comparable with

```text
a_N(s)(r-s).
```

The proof avoids division by zero at `s=1`; in the ordered case `r>=s` then forces the identical endpoint.

---

## 5. Detailed proof audit: coupled metric

### 5.1 Reduction to radii and angle

By common unitary conjugation, two unit directions can be placed on one great circle. This preserves every reference-assisted adaptive distance. Write

```text
x=ru,
y=sv,
r>=s,
h=angle(u,v).
```

### 5.2 No cancellation in the lower bound

The aligned radial comparison is `(ru,su)`. On input `+u`, the actual pair `(ru,sv)` produces Bernoulli parameters

```text
p=(1-r)/2,
q'=(1-s cos h)/2.
```

Since `q'>=(1-s)/2>=p`, the binomial likelihood ratio is monotone in the count. For the lower-tail event that is optimal against `p`, its probability under the second law changes monotonically with `q'`. Therefore the actual output distance is at least the aligned radial product distance.

This argument is pairwise and nonadaptive, which is sufficient because `d_N` is a supremum over all testers.

### 5.3 Recovering the angular component

Triangle inequality gives

```text
d(M_su,M_sv)
 <= d(M_su,M_ru)+d(M_ru,M_sv)
 <= 2 d(M_ru,M_sv).
```

The inherited v73 equal-visibility theorem gives a lower bound on the left side at scale

```text
s a_N(s) h.
```

Together with the radial lower scale `a_N(s)(r-s)`, this gives the maximum of two lower contributions. Elementary case splitting converts it to a constant times

```text
min{1,a_N(s)[(r-s)+s h]}.
```

Since `|ru-sv|<=(r-s)+s h`, the stated joint lower bound follows.

### 5.4 Joint upper bound

Concatenate the radial path `(ru,su)` with the angular path `(su,sv)`. The radial lemma gives `3a_N(s)(r-s)`. The angular theorem gives at most `sqrt(2)s a_N(s)h`.

The exact identity

```text
|ru-sv|^2=(r-s)^2+4rs sin^2(h/2)
```

implies

```text
r-s<=|ru-sv|,
sh<=(pi/2)|ru-sv|.
```

Therefore the sum is less than `6a_N(s)|ru-sv|`. Truncation at trace distance two gives the final upper statement.

### 5.5 One-use equality

For one call, the positive-outcome effect difference is

```text
(E_x^+-E_y^+)=(x-y)·sigma/2.
```

Its eigenvalues are `±|x-y|/2`. The two ordered classical output blocks of the channel difference have opposite signs, so their total trace norm is `|x-y|`. Reference assistance cannot improve the dual operator-norm value. This fixes all factor-of-two conventions.

---

## 6. Detailed proof audit: weighted covering

### 6.1 Weight comparison

Set

```text
e_N(x)=1-|x|^2+1/N.
```

Because

```text
|e_N(x)-e_N(y)|<=2|x-y|,
N e_N(x)>=1,
```

points within Euclidean radius `t/w_N(x)` have relative `e_N` variation bounded by a constant multiple of `t`. For sufficiently small absolute `t`, weights at the two points are comparable.

### 6.2 Operational ball inclusions

The joint metric upper bound shows that a Euclidean ball of radius `ct/w_N(x)` lies in the operational radius-`t` ball.

Conversely, if the operational distance is at most `t<1/256`, the metric lower bound forces

```text
|x-y|<=C t/a_N(min{|x|,|y|}).
```

Applying the preceding weight comparison first at the smaller-radius endpoint and then at `x` yields the reverse Euclidean localization. This is the only place where the asymmetric `min` in the metric weight must be handled carefully.

### 6.3 Weighted Ahlfors mass

On each such local Euclidean ball, `w_N` is comparable to its centre value. The Ahlfors bounds therefore give

```text
nu_N(B_dN(x,t))
asymp w_N(x)^k [t/w_N(x)]^k
asymp t^k.
```

The constants are uniform in `N` but depend on the target regularity data and chosen small-error cap.

### 6.4 Upper covering bound

A maximal `delta`-separated set is a radius-`delta` net. The radius-`delta/3` balls around its points are disjoint and each has weighted mass at least a constant times `delta^k`. Hence the number of points is at most

```text
C nu_N(X) delta^(-k).
```

The centres lie in `X`, giving the family-centred upper bound.

### 6.5 Lower covering bound with arbitrary centres

A maximal `3delta`-separated set is a radius-`3delta` net. Its cardinality is at least a constant times `nu_N(X)delta^(-k)` because the covering balls have weighted mass at most `C delta^k`.

No radius-`delta` ball about any centre in any ambient metric space can contain two target points at distance greater than `2delta`. Thus arbitrary legal memoryless centres do not reduce the lower order. No projection or retraction onto `X` is assumed.

---

## 7. Detailed proof audit: contact law

### 7.1 Integral form

The weighted volume is

```text
N^(k/2) ∫ (t+1/N)^(-k/2) dF(t),
```

where `t=1-|x|^2` and `F` is the depth distribution.

### 7.2 Stieltjes integration

When `F(0)=0`, integration by parts gives one bounded endpoint term plus

```text
(k/2) ∫ F(t)(t+1/N)^(-k/2-1) dt.
```

Splitting at `t=1/N` yields:

- bounded integral when `alpha>k/2`;
- logarithm when `alpha=k/2`;
- order `N^(k/2-alpha)` inside the integral when `alpha<k/2`.

Multiplying by the outer `N^(k/2)` gives the displayed regimes.

### 7.3 Boundary atom

At `|x|=1`, `w_N(x)=N`. A boundary atom of mass `F(0)` contributes exactly `N^k F(0)` to the weighted integral. Since `w_N<=N` everywhere, this also controls the total upper order when the atom is positive.

### 7.4 Coordinate balls

Lebesgue measure on the coordinate `d`-ball is `d`-Ahlfors regular. The measure of a boundary layer of support deficit at most `t` is of order `t`, so `alpha=1`.

Consequently:

```text
d=1: alpha>k/2 -> N^(1/2)
d=2: alpha=k/2 -> N log N
d=3: alpha<k/2 -> N^2.
```

All carry the Euclidean accuracy factor `delta^(-d)`.

---

## 8. Detailed audit of the rational codec

### 8.1 Interface

The target schema accepts exactly two or three rational Cartesian Bloch coordinates. It rejects targets outside the closed unit ball and any extra field, including a free visibility header.

The public parameters are dimension, horizon, and requested error. The target radius is part of the payload.

### 8.2 Radial layers

The code discretizes

```text
t=tan(arcsin(r)/2)
```

on the rational grid `i/B`. The decoded radius

```text
r_i=2(i/B)/(1+(i/B)^2)
```

is rational and lies in `[0,1]`.

For rational `Q=r^2`, comparing the target `t` with a rational `v` is equivalent to comparing `Q` with `[2v/(1+v^2)]^2`. Nearest-grid selection, including tie handling, uses exact rational comparisons.

The derivative of `2 arctan t` is at most two, so nearest radial grid error gives angular-radius error at most `1/B`. The common radial flip programme converts this to operational error at most `sqrt(N)/B`.

### 8.3 Direction charts

The encoder selects a maximal-absolute target coordinate and its sign. The stereographic coordinate has magnitude at most one. The inverse signed-axis chart is rational and has exact unit norm for every integer digit vector in the cube.

To compare

```text
b/(sqrt(Q)+a)
```

with rational `v`, the code first computes the sign of `b-va`. If negative, the comparison is negative. Otherwise it compares `(b-va)^2` with `v^2 Q`. This is logically equivalent and avoids introducing extraneous solutions by squaring a negative quantity.

### 8.4 Union index

The layer starts are cumulative exact integers. Layer zero has one erased word. Every positive layer has

```text
2d(2A_i+1)^(d-1)
```

chart words. The payload is one integer in the full union, not separate uncharged radius and direction fields.

Chart overlap and redundant boundary words are counted in capacity. They affect constants only.

### 8.5 Legal decoding

For every body index in range, decoding produces a rational unit direction and rational radius. The resulting Bloch vector lies in the closed ball.

The positive and negative Choi blocks use the input-first transpose convention. Their determinant is `(1-r_i^2)/4`, and their sum is the identity. `Instrument.validate()` therefore checks an actual legal ordered binary qubit measurement.

### 8.6 Error budget

The radial grid has

```text
B >= 8 sqrt(N)/delta.
```

The angular grid at layer `i` has

```text
A_i >= 8 sqrt(d-1) K_(N,r_i)/delta.
```

Thus the radial and angular operational errors are each at most `delta/8`. Triangle inequality gives at most `delta/4`, which is the conservative certificate stored in the code.

The theorem only needs error at most `delta`; the unused slack absorbs chart and ceiling constants.

### 8.7 Capacity order

For layers bounded away from the sphere, `K_(N,r_i)=O(sqrt(N))`. Near the boundary,

```text
K_(N,r_i)<=C min{N,sqrt(N)B/(j+1)},
```

where `j=B-i`.

For `d=2`, summing `A_i` gives a harmonic series and order

```text
N delta^(-2) log(N+2).
```

For `d=3`, summing `A_i^2` gives a convergent reciprocal-square series and order

```text
N^2 delta^(-3).
```

### 8.8 Computational scope

The layer table contains `O(B)` integers and can be large when `N` or inverse error is numerically large. Ranking and unranking are finite exact algorithms. No polynomial-time or optimal-workspace result in the binary input lengths is proved.

---

## 9. Code and finite-regression audit

### 9.1 Defensive parsing

The codec enforces:

- exact schema keys;
- canonical rational strings;
- dimensions two or three;
- positive integer horizon distinct from Boolean values;
- rational error in `(0,1/4]`;
- canonical lowercase hexadecimal payload;
- exact payload capacity;
- exact header/certificate replay; and
- duplicate-JSON-field rejection.

### 9.2 Cache-key issue

Python Boolean values compare equal to integers in dictionary and cache keys. The public `layers` function validates arguments before calling the cached private function. The regression explicitly populates a colliding integer key and then confirms that a Boolean horizon is still rejected.

### 9.3 New regression suite

The v74 suite records:

```text
2,265 exact assertions
150 binomial cases
450 monotonicity cases
180 algebraic comparisons
60 codec cases
96 legal-word cases
33 named negative controls
```

It checks finite instances of the radial inequalities, monotonicity, processing-kernel legality, exact chart algebra, determinant identities, payload accounting, and target replay.

### 9.4 Evidentiary boundary

The test does not establish:

- the adaptive supremum over all testers;
- the continuum operational metric;
- the Ahlfors covering theorem;
- the Stieltjes contact law;
- imported v73 theorems; or
- novelty and priority.

The scope string states this correctly.

---

## 10. Build and workflow audit

### 10.1 Source qualification

Workflow run `37172756259`, named `GTF-I v74 native-source qualification and publication`, completed successfully. It was triggered by the v74 source-delivery commit and produced the native source and publication objects recorded in the final request.

### 10.2 Exact final-head reconstruction

Workflow run `37173200597` has

```text
head_sha = 8477a4c44cbed327068ab895c244f2ddfa86e27a
conclusion = success.
```

Its steps successfully:

1. installed fixed dependencies;
2. checked out the exact final object without retained credentials;
3. trusted only the container checkout;
4. rebuilt sources, all pages, and all tests read-only;
5. independently rebuilt the minimal journal source package; and
6. uploaded an external exact-head attestation.

This is stronger provenance than a builder that only verifies a parent and then writes an unchecked successor.

### 10.3 Build receipt

The committed receipt records:

```text
quantitative paper: 46 pages
structural paper:   41 pages
complete edition:  146 pages
isolated rebuild:  true
LaTeX diagnostics: none recorded
normal/optimized:  identical
predecessor files: 222
preserved labels:  502
active labels:     522
```

All inherited exact suites and the new v74 suite are included.

### 10.4 Signature status

The final commit reports GitHub verification reason `unsigned`. The external workflow attests exact bytes and reproducibility, not human authorship. No release signature should be inferred.

---

## 11. Literature and priority audit

### 11.1 Existing comparison

The focused package now cites and distinguishes:

- Sedlák--Ziman on noisy single-shot qubit measurement discrimination with unequal noise levels;
- Puchała--Pawela--Krawiec--Kukulski on single-shot projective measurement distance;
- the later multiple-shot projective-measurement theorem;
- classical channel simulation in noisy metrology;
- environment-programme and seizing frameworks;
- adaptive channel discrimination;
- state population compression;
- supplied-description coding versus unknown-channel learning; and
- mathematical descriptions versus physical classical simulation.

### 11.2 Missing direct two-use reference

J. Fiurášek and M. Mičuda, *Optimal two-copy discrimination of quantum measurements*, **Physical Review A 80** (2009), 042312, arXiv:0909.2940, explicitly studies two uses of projective single-qubit measurements. It compares fixed probes, adaptive probes, entangled probes, and feed-forward; it finds strict improvements and, in part of the parameter range, perfect discrimination.

This is not equivalent to v74:

- it is projective rather than the full noisy ball;
- it treats two uses rather than uniform arbitrary `N`;
- it optimizes binary discrimination rather than family covering;
- it has no Ahlfors/contact theorem; and
- it has no rational joint code.

It is nevertheless a direct antecedent for the adaptive tester interface and should be included in the theorem-level priority discussion.

### 11.3 Priority classification

The strongest plausible new assembly is:

```text
radial exact programme equality
+ finite rare-event support cutoff
+ equal-visibility entangled angular modulus
+ cancellation-free coupling
-> all-pair finite-use ball metric
-> weighted regular-family covering
-> boundary-contact trichotomy
-> exact rational charged joint code.
```

An independent expert should determine whether equivalent weighted-volume or critical-log statements already appear in quantum local asymptotic geometry, singular statistical-model entropy, or measurement-discrimination literature.

The author-side audit is not sufficient to close that question.

---

## 12. Repository-wide pipeline assessment

The frozen independent analytic graph remains

```text
A2 -> A3 -> A4 -> C2 -> D1
B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1
A1 independent.
```

Open obligations include:

- raw unsmoothed local limits;
- predictable stopped-path entropy and large deviations;
- a global past kernel;
- exact canonical coefficients and shell conditioning;
- process CLT and Mosco recovery;
- nonlinear Nisio resolvents and graph cores;
- filtering/QMD/LAN;
- changing-filtration response; and
- labelled posterior contraction.

The v74 finite-use metric theorem does not prove any of these objects. Its bounded public stopping is part of an adaptive tester, not a stopped-path LDP. Its local boundary weight is not a global past kernel or a Mosco form. Its pairwise testing is not filtering/LAN.

Accordingly, the following remain false:

```text
historical_A2_replacement
B4_aggregate
C2_aggregate
eleven_paper_aggregate
whole_Theta_program.
```

This separation is correctly represented in `PROOF_STATUS.json`.

---

## 13. Risk register

### R1 — Independent priority risk: high

The author comparison is careful but incomplete. Measurement-discrimination and singular statistical-geometry literatures need external specialist review.

### R2 — Model-breadth risk: high for a general journal

The new theorem is confined to ordered unbiased binary qubit measurements.

### R3 — Small-error risk: moderate

The operational metric is global, but the covering law is local. Large-error family multiplicity is not classified.

### R4 — Regularity risk: moderate

The weighted criterion assumes Ahlfors regularity. Singular nonregular identifiable sets may exhibit different behaviour.

### R5 — Constant/sharpness risk: moderate

The comparison constants are safe rather than optimal. There is no exact adaptive distance formula away from inherited special cases.

### R6 — Pairwise-versus-estimation risk: moderate

Pair-dependent tests suffice for packing but do not give one global estimator or identification protocol.

### R7 — Resource-interpretation risk: controlled but persistent

Payload length, encoder workspace, query learning, and physical simulation are distinct. Summary language must not merge them.

### R8 — Implementation-complexity risk: low to moderate

The codec is exact and finite but pseudo-polynomial in numerical grids.

### R9 — Provenance risk: low

The exact final SHA has a successful read-only reconstruction. Human author signing remains absent.

### R10 — Whole-program overclaim risk: controlled

All aggregate flags remain false, but future summaries must preserve that fact.

---

## 14. Specialist-release acceptance gates

### Mathematical gates

- retain the complete radial equality and support-cutoff proof;
- retain the monotonicity argument preventing radial/angular cancellation;
- state the ordered-outcome and unhalved-distance conventions prominently;
- state the Ahlfors and small-error hypotheses in every covering theorem;
- distinguish pair-dependent tests from common estimators;
- retain arbitrary legal centres in the lower covering definition;
- keep the disk critical logarithm derivation explicit; and
- keep the exact sign-before-square comparison in the codec proof.

### Literature gates

- add Fiurášek--Mičuda 2009 to the focused bibliography;
- compare its two-use adaptive, entangled, and feed-forward strategies with the present arbitrary-`N` metric;
- obtain external review from a measurement-discrimination specialist;
- compare the weighted contact law with singular quantum statistical-model entropy; and
- avoid novelty claims for programme contraction, binomial testing, Stieltjes integration, or stereographic charts individually.

### Reproducibility gates

- preserve the exact-head workflow result and artifact digest;
- publish a durable signed release if authorship identity is important;
- keep the source-bound journal package independent of historical PDFs;
- retain normal/optimized regression parity; and
- keep finite-test scope statements visible.

### Editorial gates

- submit the 46-page quantitative paper separately;
- treat the 146-page complete edition as archival;
- describe the structural companion as inherited in this revision;
- compress repository genealogy in the journal-facing introduction; and
- position the paper around the ball metric, weighted covering theorem, contact law, and exact codec.

---

## 15. Final audit verdict

### Local mathematics

**Pass with explicit model and regularity qualifications.** No fatal gap was found in the new v74 theorem chain.

### Implementation

**Pass for the declared exact rational interface.** The codec and finite tests match the written construction.

### Reproducibility

**Pass.** Source qualification and exact final-head read-only reconstruction both succeeded.

### Priority

**Open.** A direct 2009 adaptive two-use antecedent is missing, and no independent expert clearance has been obtained.

### General-journal significance

**Not met.** The theorem is sharp and useful but specialized to one fixed qubit measurement body and local regular-family covering.

### Repository-wide programme

**Open.** No A/B/C/D aggregate gate is closed.

### Overall classification

```text
latest completed revision:       v74
exact reviewed head:             8477a4c44cbed327068ab895c244f2ddfa86e27a
joint ball metric:               PASS WITH MODEL SCOPE
weighted covering:               PASS WITH AHLFORS/SMALL-ERROR SCOPE
contact trichotomy:              PASS
rational joint codec:            PASS
source qualification:            PASS
exact-head reconstruction:       PASS
independent priority:            OPEN
cryptographic signature:         OPEN
whole Theta programme:           OPEN
four-leading-journal threshold:  NOT MET
```

Revision 74 should be regarded as a strong specialist-level contribution, not as a closure of general quantum instrument boundary geometry or of the broader Theta research programme.

