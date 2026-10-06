# Literature audit — Revision 63

This is a targeted author-side comparison, not independent expert clearance or an exhaustive novelty certificate. The complete v62 comparison is retained below and in its immutable source directory.

## New theorem-level comparisons, checked 28 September 2026

| Source | Specific input or conclusion | Relation to the new theorem |
|---|---|---|
| van Erven–Harremoes, IEEE TIT 60 (2014), Theorem 3; arXiv:1206.2459 | Monotonicity of Renyi divergence, including D_1>=D_(1/2) | The affinity inequality is classical. We give its Jensen proof and use it without linearization in a stochastic centroid budget. |
| Pinochet Lobos–Pittet, arXiv:1805.05261v2, Theorems 1.1 and 1.2; expanded 2021 publication | Exact one-step LPS norm and exact reduced-word sphere discrepancy (1+(q-1)b/(q+1))q^(-b/2) | The radial spectral result is classical and stronger than the elementary bound used here. New claims concern error-dependent positive realization under common rows and arbitrary narrow-cut profiles. |
| Parzanchevski–Sarnak, Advances in Mathematics 327 (2018), Section 3, Proposition 3.1; arXiv:1704.02106 | Spectral norm controls almost-covering by arithmetic word sets; navigation of quantum gates | This is a close arithmetic/geometric antecedent. A word-set covering or synthesized unitary is not a compatible positive realization of every input word. We do not deduce an optimal worst-point arithmetic covering radius from our width theorem. |
| Polyanskiy–Wu, IEEE TIT 62 (2016), Proposition 1 | Wasserstein continuity of entropy with Euclidean regularity | This antecedent is already credited in v61/v62. The retained proof treats compact spherical kernels with zeros; the new step keeps block entropy loss at its logarithmic scale. |

Primary URLs consulted: https://arxiv.org/pdf/1206.2459 ; https://arxiv.org/pdf/1805.05261 ; https://arxiv.org/pdf/1704.02106 ; https://ems.press/journals/lem/articles/3007703 . The 2019 preprint numbering, not the expanded journal numbering, is used for the Pinochet Lobos–Pittet theorem citations.

The new chain establishes a uniform subexponential-factor crossover and the limit min(log(2r-1),p*a/2) for spherical Ramanujan alphabets. It is not a new Ramanujan theorem, a new Renyi inequality, an optimal quantum gate synthesis result, or a statement about scalar cut-point recognition. Priority in equivalent positive-realization or automata formalisms remains subject to external review.

## Retained baseline comparison (v62)

# Theorem-level literature audit — Revision 62

Date: 28 September 2026. This is an author-side comparison, not an independent expert priority clearance. The retained v61/v59/v58 audits provide the longer earlier comparisons and remain unchanged. The distinctions below are statements about hypotheses and conclusions, not proof that no equivalent formulation exists elsewhere.

## Primary sources examined for the new arguments

| Source and precise locator | Established result used or compared | Boundary of the present claim |
|---|---|---|
| Grabchak--Sonin, *A Zero-One Law for Markov Chains*, arXiv:2011.04063, Theorem 1 and Section 5.1 | Conditional probabilities of tail events given the current state approach zero or one in a nonhomogeneous Markov chain; the proof relates them to the increasing-past martingale. | The finite-state tail-capacity principle is classical. We restate its emitted-tail version with infinitely many narrow cuts, then use finite-product compactness and a diagnostic cycle to derive an all-error finite-horizon converse. Those reductions, not the zero-one law, are the extension claimed here. |
| Blackwell, *Finite non-homogeneous chains*, Ann. of Math. (2) 46 (1945), 594--599; Cohn, *On the tail sigma-field of the nonhomogeneous Markov chains*, Ann. Math. Statist. 41 (1970), 2175--2176 | Classical finite nonhomogeneous-chain and tail-field structure. Bibliographic and historical attributions are also recorded by Grabchak--Sonin. | We do not claim invention of finite tail atomicity, finite-state martingale convergence, or nonhomogeneous Markov decomposition. The proof needed by the article is supplied in full rather than requiring an unstated imported corollary. |
| Polyanskiy--Wu, *Wasserstein continuity of entropy and outer bounds for interference channels*, arXiv:1504.04419v2, Proposition 1; IEEE Trans. Inform. Theory 62 (2016), 3992--4002 | Quadratic-Wasserstein control of differential entropy under regularity conditions. | The article retains its separately proved compact-support spherical kernel, including zeros and regularization. Orthogonal covariance is elementary. The width statement also requires the actual centroid-flow identity, a full action gap, and the finite-label occupation quantifiers; these are not supplied by entropy continuity alone. |
| Pinochet Lobos--Pittet, *The exact convergence rate in the ergodic theorem of Lubotzky Phillips Sarnak*, arXiv:1805.05261v2, Theorem 1.1 | The classical quaternion set and the precise spherical discrepancy `2 sqrt(p)/(p+1)`. | At p=5 this is the imported full action norm `sqrt(5)/3` for the actual six nonidentity Bloch rotations. We neither prove the automorphic/Deligne input nor infer it from finite harmonics. The new realization theorem removes the idle instruction and tracks vanishing accuracy. |
| Fijalkow--Paperman, *Monadic Second-Order Logic with Arbitrary Monadic Predicates*, arXiv:1709.03117, Theorem 10 in the PDF | A neutral-letter/Crane-Beach collapse for the nonuniform monadic-predicate class; the deterministic argument already preserves the state bound. | State-count preservation alone is not claimed as new. The retained stochastic theorem uses closed numerical error and actual composite rows. The new quantitative occupation argument is not a general neutral-letter collapse: it assumes a full action gap and does not use neutral letters or returns. |

The primary arXiv text and theorem locations were consulted. The web PDF screenshot service failed on the attempted pages; this record does not claim successful visual inspection of those external page images. The submission PDFs generated from the present source are rendered and checked independently in the build.

## Quantifier map for the three new theorem packages

**Return-free occupation.** The inherited spherical entropy and transport lemmas already paid for loss of centroid mass. The new step is to retain the deterministic physical action of every filler and use invariance of entropy and transport under that action. The conclusion counts arbitrary positive k-width cuts of a separately redesigned horizon-specific stochastic machine. Full action gap, legal convex output, and all-direction cap hypotheses remain explicit. No return-free general stationarization result is inferred.

**Joint amplitude/accuracy.** The lower proof keeps `1-rho+epsilon` rather than hiding it in a fixed-error constant. The comparison uses the old geometric upper construction at a slightly reduced amplitude. Matching follows for equal least/target orbit dimensions and subexponential inverse slack. Neither classical orbit covering alone nor a one-shot quantization dimension yields the sequential `N/slack` law. Optimal constants and the full exponential crossover remain separate questions.

**Repeatable-process strong converse.** Classical finite-state tail capacity is the key antecedent. The proof first turns it into a *uniform finite witness* against all nonhomogeneous k-label instruments for n distinct iid output laws. It then constructs one response-resetting diagnostic cycle and applies that witness to actual composite instruments between arbitrary narrow cuts. The policies used for the lower bound are deterministic; correctness must hold for all adaptive policies. Initial mixtures may depend on the tested type, but no unrecorded seed may influence subsequent kernels. The finite future-response cardinality is thereby eventually minimal for all TV errors below one, not only below one half.

## Neighboring theorem languages and remaining priority work

The positive/nonnegative realization literature studies invariant cones and finite positive representations; the old manuscript audits distinguish these from independently redesigned clocked tables. Probabilistic/weighted automata and advice automata similarly require checking exact output semantics, positivity, and uniformity before comparing state minima. These distinctions are important but do not by themselves certify novelty.

For controlled hidden-state and predictive-state models, the retained comparison to Singh--James--Rudary distinguishes linear prediction rank from a positive hidden-label cardinality and a whole-transcript approximation. The new tail lemma allows irreversible hidden kernels, but the diagnostic physical experiment still uses repeatable nondisturbing fresh probes. No general HMM/POMDP or repeated quantum-measurement equivalence is asserted.

For quantization, rate-distortion, and finite-memory filtering, the sequential occupation and centroid-loss budget should be compared at theorem level, not dismissed because terminology differs. A static covering number, a filter-stability estimate, or a Shannon-information bound is not automatically the present label-width invariant. Conversely, we do not claim that every equivalent entropy-based converse has been excluded.

Independent experts in positive realization/automata and controlled stochastic processes would still be needed for an external priority opinion. No such expert opinion has been obtained or fabricated by this revision. The manuscripts and response make their precise new-looking combinations available for that conventional evaluation without changing the journal target.
