# Targeted primary-source and priority audit — 5 October 2026

This is an author-side audit for R52, not independent human priority clearance. The full earlier literature audit is preserved in `predecessor-v82-audit/LITERATURE_AUDIT.md`. No priority or journal-acceptance claim follows from a successful build or from this file.

## Versioned primary sources

1. Antonio Anna Mele and Lennart Bittel, *Optimal learning of quantum channels in diamond distance*, arXiv:2512.10214v3, 15 June 2026. Primary text: https://arxiv.org/html/2512.10214v3 ; version history: https://arxiv.org/abs/2512.10214 . Theorem III.3, Remark III.4, Corollary III.9 and the binary lower section were checked. The theorem uses halved diamond distance and an explicit lower admissible failure threshold in its simplified high-confidence form. The author's September news reports acceptance by Nature Physics; this revision pins the mathematical arXiv version rather than inventing final publication metadata.
2. Leonardo Zambrano, Sergi Ramos-Calderer and Richard Kueng, *Fast quantum measurement tomography with optimal error bounds*, arXiv:2507.04500v3, 9 July 2026; Quantum 10, 2162 (15 July 2026). Primary text: https://arxiv.org/html/2507.04500v3 ; version history: https://arxiv.org/abs/2507.04500 . The worst-input TV definition and Theorem 2 were checked. Theorem 2 has the exact `8[d²+epsilon(d²+1)/6] epsilon^-2 log(2^(k+1)9^(2d)/eta)` sufficient sample bound for global-design inputs.
3. Satoshi Yoshida, Kazuki Okigami, Pietro M. Posta and Dmitry Grinko, *Optimal learning of covariant quantum states and channels*, arXiv:2609.39280 (30 September 2026), https://arxiv.org/abs/2609.39280 . Its primary abstract was checked as a newly posted adjacent result. It assumes known symmetry and includes gate-efficient constructions in a permutation-covariant setting. We do not infer an arbitrary ordered-POVM learner from that abstract, nor assert that efficient tomography is absent from the literature. A detailed theorem comparison is a concrete further specialist task.

## Main-text quantitative comparisons

`editions/operational-priority83.tex` provides the actual substitutions rather than a generic assertion of difference. A legal measurement estimator with component error epsilon need not be balanced. The affine repair theorem is explicitly applied before the balanced metric upper. It yields future loss at most `8k sqrt(N) epsilon`.

At constant confidence, the general Mele–Bittel theorem with input d, output k and rank at most dk gives a sufficient `O(d²k⁴ N delta^-2)` budget after choosing `epsilon=delta/(8k sqrt(N))`. The binary-component use of its existing primitive gives the paper's different `k³` sufficient bound. No lower-bound or estimator-optimality conclusion is inferred from the coarse general-channel substitution.

For Zambrano–Ramos-Calderer–Kueng, component norm is bounded by their worst-input TV. The same repair gives `O(k² N delta^-2 d²[d+k+log(1/eta)])`. Their nonadaptive single-copy unentangled probe access is stated next to this formula. Their lower-bound class is not substituted for the present coherent adaptive lower.

## Horizontal principle and attribution

The inherited bibliography credits Fujiwara–Imai, Demkowicz-Dobrzański and coauthors, Kurdziałek and coauthors, Yuan–Fung, and Sieniawski–Demkowicz-Dobrzański for channel geometry, horizontal gauges, adaptive channel-extension bounds and finite path comparison. The new proof uses those general methods, together with classical orthogonal projection, quadratic minimization and inverse-order comparison.

The specific identities supplied here are the normalized-tuple covariance `C_E`, its exact binary Sylvester restriction, its projective zero-operator characterization, and the closed-body regularized path/midpoint upper. A targeted search around POVM covariance, normalized horizontal tangents and finite-use discrimination did not settle whether an equivalent formulation is already present in the broader literature. Accordingly the article states and proves the identities without claiming historical firstness. Independent experts should compare them directly with channel-extension and operator covariance formulations, including their singular domains and normalizations.

## Remaining priority questions

The independent brief separates four checkable objects: the full closed-body covariance upper; the finite-angle noise/horizon example; the fixed-k interior learning/description synthesis; and the search-free affine legality map with quantitative error. The last map uses elementary affine correction and inward mixing; its formulas and use are proved here, not promoted as a fundamentally new convex-optimization method. The computational theorem for the rational evaluator is not a claim of efficient optimal adaptive testing.

No human specialist was contacted or supplied an opinion in this revision process. That external step remains uncompleted, while all theorem-level comparisons required by R52 are now in the main article.
