# Response to the fifteenth pipeline-aware referee report

**General Theta Foundations I — Revision 31**  
**Compatibility of Positive Memory and Online Simplex Synthesis**  
25 September 2026

Controlling report: `reviews/general-theta-foundations-i-v30-streaming-geometry-pipeline-harsh-top4-r15-2026-09-24/REFEREE_REPORT.md`, frozen at `cd793fde91fca07958c6c5bc3989e9c51a17540b`. Reviewed manuscript: v30 at `a4abeb1c5e0323e5850e7f2446bf96fb1f7d4d8a`, native source `24b98c1a87382104d10ebf518ca90bddb35416fc`. The new work branch was established on the remote from the review before publication.

The report distinguishes valid local results from a genuinely new compatibility phenomenon. We address that distinction by giving the explicit full-support obstruction it requests, determining that example's entire two-cut feasible profile set, and placing it next to a canonical no-obstruction theorem at ranks one and two. The online side is strengthened by a universal transfer for every simplex encoder, not one additional Hadamard construction. The classical cube-absorption and recent RAC comparisons are corrected at theorem level.

The native labels below map to the actual compiled numbers and pages in `evidence/THEOREM_LOCATIONS.json`. The proofs are in the article; tests are not offered in place of them.

## 11.1 / Sections 5–6 — classical geometry and recent coding literature

### Cube absorption: static facts are attributed; the online transfer is explicit

Section `sec:critical` introduces the standard absorption index, with homothety about the simplex centroid, and distinguishes that center from an arbitrary origin-centered dilation. It credits the universal factor n, Hadamard equality, axial-diameter lineage and the critical inclusions in dimensions five and nine to Nevskii–Ukhalov and the earlier literature they discuss. Theorem 2 of their paper supplies the centroid alignment at critical absorption. We also derive the barycentric equality identities internally, including uniform barycentric weights at the origin.

The classical dimension-five and dimension-nine matrices are displayed exactly, in the source's [0,1] coordinates. Their centered augmented matrices have determinant magnitudes 32 and 12800, uniform constant inverse rows 1/6 and 1/10, and absolute inverse-column sums one. Thus the finite seed inclusions can be checked directly from the matrices as well as located in the original paper. The dimension-five seed is perfect in that source's terminology; the dimension-nine critical seed is not perfect. The online theorem needs only criticality, not the stronger all-cube-vertices-on-faces property.

`prop:critical-rows` constructs the online process from the inverse of **any** critical simplex. If its barycentric functions are a_s + sum_i b_(s,i) z_i, the local draw is q_i(s|x_i)=|b_(s,i)|+b_(s,i)x_i, and the update retains the current label with probability (t-1)/t or redraws from q_t with probability 1/t. The full state distribution, not merely its average success, equals the required barycentric encoder. In general an individual local draw does not have mean x_i e_i; the proof uses the correct aggregate cancellation, not a false Hadamard orthogonality assumption.

`cor:nonhadamard` consequently proves sharp online peaks six and ten at signals 1/5 and 1/9. `prop:critical-tensor` gives a normalized tensor closure and an explicit growing rational family. We do not claim to have discovered the underlying classical seed inclusions or a new universal nonnegative-rank tensor theorem.

### Kondo et al.: checkpoint cardinality is actually equivalent

We read the full arXiv:2604.21274v3 (16 July 2026), including Theorem 14, Lemma 15, and equations (143)–(149), and inspected the PDF pages containing those statements. The report's question can be answered more definitively than in v30. For a fixed decoder dictionary D in [-1,1]^n, the following are equivalent:

- worst-case success at least (1+eta)/2 for every input and query;
- eta*[-1,1]^n is contained in conv D;
- exact conditional response means eta*x can be achieved by changing only the encoder.

`prop:exactification` gives the direct support-function proof. No extra message, shared random seed or symmetry selector is required. In the source's [0,1] normalization, the directed l-infinity error e corresponds to centered radius eta=1-2e and success p=(1+eta)/2. This factor is retained explicitly.

Lemma 15 of the source already makes the cube-containment passage. We therefore do **not** maintain that exact conditional equality, on its own, gives a stricter checkpoint cardinality problem or a new entropy exponent. The previous exact codebook proof remains a valid proof, but its static objective is now correctly identified with that literature. The source's finite simplex-code optimum overlaps the previous Hadamard checkpoint case. The entropy exponent and logarithmic communication overhead remain attributed to Ambainis–Nayak–Ta-Shma–Vazirani.

The online cost of computing a new exactifying encoder is not controlled by that checkpoint equivalence. Our new additive/affine transfer supplies such a bound under a structural condition and for every simplex dictionary. This is the precise place where the current result adds execution content.

## 11.2 — entropy novelty and exactification

The entropy formula is not used as new novelty evidence. The prior fixed-signal, block-streaming and approximation theorems remain in the unchanged v30 supporting article with their proofs. The present text explicitly states that the O_eta(sqrt(n log n)) excess is an upper construction with no claimed matching second-order lower bound. The exactification proposition is attributed to the inspected RAC geometry; the new work addresses compatible execution rather than renaming the exponent.

## 11.3 / Section 4 — an actual compatibility obstruction

**The requested example is provided with full support and an exact feasible-profile theorem.**

`thm:obstruction` specifies a channel on three successive input symbols: x in {-1,1}^2, a command j in {1,...,5}, and a binary query k. At the two internal cuts every past input and every past random choice must pass through the retained register. The five two-dimensional decoder means are

```
(h,h), (h,-h), (-h,0), (-h/2,h*x1/4), (-h/2,h*x2/4),
9/10 <= h <= 1.
```

Each individual cut has normalized rank and least state count three. Yet no machine has three states at both cuts. The entire feasible profile region is the upward closure of `(3,4)` and `(4,3)`. Both machines are explicitly constructed by common stochastic rows, so the minimum peak is four.

The obstruction is not based on an assumption that internal states are residuals. Rank saturation at the first cut forces its three future arrays into the affine plane of the four actual first-cut rows. Their free coordinates must enclose a square. The three decoder states at the next cut must enclose the first three prescribed points; a forced-triangle lemma restricts their section at first coordinate -h/2. Every shifted first-cut generator has to belong to this **same** decoder triangle. The resulting strip is too narrow for a three-point enclosure of the first-cut square.

The numerical constants are analytic: with delta=1-h, the strip bound is

```
beta(delta)=1/4+delta/(2*(1-delta))+delta/(2-3*delta) < h/2.
```

At delta=1/10 the strict margin is 131/1530. For h<1 the required conditional probabilities all have full support; at h=9/10 they lie in [1/20,19/20]. Thus this is not solely a support-boundary example, and it does not rest on a zero-probability residual trick.

**A canonical no-obstruction class explains the rank boundary.**

`prop:slice-shift` proves that `L_t=aff(R_t) intersect P_t` is automatically closed under positive normalized shifts. This follows by taking an affine combination of complete residuals before restriction and normalization; positivity comes from membership in the causal polytope, not from the affine coefficients. If L_t is a simplex at every cut, its vertices realize all rank minima simultaneously (`thm:slice`). In particular, cut ranks at most two always yield points or intervals and have no compatibility obstruction. The full-support example at rank three is therefore sharp in maximum cut rank.

These slices are fixed polytopes of the specified response array, recognized by linear equations, inequalities and vertex enumeration. The criterion is not defined by existence of unknown common transition coefficients. The underlying invariant-cone/residual construction is classical and is credited; the new explicit incompatible profile supplies the phenomenon the report said the normal-form theorem lacked. We do not call the simplex-slice criterion necessary for every positive realization or claim a succinct polynomial algorithm.

## 11.4 — a structural online theorem and non-Hadamard critical encoders

**All static simplex encoders, not only the known orthogonal examples, admit an online implementation of the same peak.**

`thm:additive` begins with an arbitrary additive stochastic encoder on a finite Cartesian input set. Taking coordinatewise minima decomposes it as a fixed nonnegative base plus local nonnegative terms of input-independent total masses. A weighted replacement process computes the mixture with exactly the same label set. The construction does not retain the index of the selected local term. It works in every externally prescribed order.

If a family of additive terminal channels of affine dimension r-1 has a checkpoint factorization through r generators, those generators are affinely independent. The unique barycentric encoder is additive and therefore online with r states (`cor:additive-rank`). In particular,

```
K_n(eta)=n+1 iff W_n^fo(eta)=n+1 iff W_n^ad(eta)=n+1
```

for every n and eta>0 (`thm:all-simplices`). This rules out a checkpoint-versus-streaming gap at the minimal-rank alphabet for the entire binary-query family. It does not claim equality for arbitrary larger dictionaries, nor simultaneous t+1 optimality at all earlier cuts. The adaptive minimum agrees because the checkpoint lower bound applies to every acquisition method and a fixed-order encoder already attains it.

The general formula applies directly to all critical non-Hadamard inclusions. Five- and nine-dimensional rational rows and a tensor-generated family are supplied. This pursues one of the specific advances proposed in §11.4 and provides a general transfer, rather than merely a further isolated state count. A general second-order interior-signal theorem, computationally optimal exponential codebook or fully adaptive physical collision scheduler is not claimed.

The finite-coin proposition additionally charges phase, old label, current input and rejection prefix. For rational row denominators at most D, T stages and input alphabet bound d, the stated implementation uses at most 2(T+1)md*2^ceil(log2 D) states, with fewer than 2 ceil(log2 D) fair bits per stage on average. No unbounded trial counter is hidden. The result is a different cost ledger, not a claim that sampling preserves the exact atomic state optimum.

## 11.5 — internal automaton conventions

Definition `def:automaton` specifies initial probabilities, labelled transition matrices, stopping probabilities, row normalization, almost-sure termination and removal of unreachable states. All state languages are normalized. The text also gives the exact continuation-mass transformation for a representation initially using finite subprobability state languages, deleting zero-mass states without adding labels.

The inherited finite-language residual/positive separation is then stated and proved in this internal model (`prop:language`). Its phase and generated-query buffer are counted. It is retained for conceptual comparison, not advertised as a newly discovered historical exponential succinctness separation. The incomplete original 2002 full-chapter/Heller/Norberg priority audit is not misreported as complete.

## 11.6, editorial points and the program pipeline

The canonical title retains General Theta Foundations I and identifies the new concrete theorem spine: compatibility of positive memory and online simplex synthesis. The abstract states the atomic stochastic-row model. No claim of journal acceptance or repository-wide analytic closure is used to support the mathematics.

The focused article contains self-contained proofs of the new canonical-slice theorem, quantitative incompatibility theorem, additive synthesis and critical-simplex transfer. The v30 article is preserved byte-for-byte as `supporting-results.pdf`; the cumulative mathematical and historical volumes append their unchanged predecessors. Old physical, saddle, entropy, calibration, revelation, autonomous and pipeline derivations remain at their original repository paths. No theorem has been removed to conceal an objection.

The frozen Round-Seventeen dependency ledger and the v29/v30 derivation chains were consulted. The historical A2/A3/A4 and B2/B1/B3/B4/C1/C2/D1 gates are not asserted to follow from finite query-channel synthesis. This revision establishes an actual finite-memory incompatibility theorem and a universal affine online transfer; it does not fabricate an independent analytic consumer in another branch. All changes are additions on this new branch only.

Every new result is supplied as an analytic proof. Exact rational and symbolic regressions, negative controls, preservation hashes and compilation are recorded separately as reproducibility evidence and not as proof, priority or editorial certification.
