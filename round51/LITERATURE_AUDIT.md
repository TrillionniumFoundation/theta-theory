# Primary-literature audit for Round 51

Checked on 5 September 2026. This is a targeted comparison, not an exhaustive priority search. Source-access scope is part of the record.

| Source | Material actually checked | Use in the article |
|---|---|---|
| Mikhaylov and Mikhaylov, *Dynamic inverse problem for Jacobi matrices*, 2019, DOI 10.3934/ipi.2019021; related arXiv:1907.11153v1 | Publisher record and related author moment-problem text | Classical deterministic response/moment reconstruction lineage; no claim of a new inverse spectral principle |
| Goldenshluger, *Nonparametric estimation of transfer functions: Rates of convergence and adaptation*, IEEE TIT 44(2), 1998, 644–658, DOI 10.1109/18.661510 | University of Haifa institutional record and full abstract. A full theorem-level paper was not obtained | Nonparametric FIR estimation with polynomial/exponential response tails is acknowledged. No unverified theorem is invoked as a premise |
| Sarkar, Rakhlin and Dahleh, *Finite Time LTI System Identification*, JMLR 22(26), 2021, 1–61; arXiv:1902.01848v6 | Journal record; author-preprint Assumption 1, Algorithm 1, Theorem 5.1, Proposition 5.1, Corollary 5.1. PDF pages 7,10,12,13 (printed numbering) visually checked | FIR/Hankel estimation is a usable interface. Gaussian input, zero initial state, finite-order constants and norm bounds are distinguished from the present bounded-input experiment. The new paper supplies its own compatible estimator and uniform truncation calculation |
| Agapiou, Stuart and Zhang, arXiv:1210.1563v3, journal DOI 10.1515/jip-2012-0071 | Author abstract and stated commuting Gaussian, linear severely ill-posed scope | Logarithmic rates alone are not claimed as a new phenomenon |
| Yue, Thunberg and Goncalves, arXiv:1605.06973v1 | Author abstract and stated matrix-exponential/system-aliasing problem | The selected small-norm branch is distinguished from a general slow-sampling inverse |
| Teschl, *Jacobi Operators and Completely Integrable Nonlinear Lattices*, 2000 | Bibliographic source retained from the reviewed moment/Gram derivation | Standard orthogonal-polynomial and Weyl reconstruction background; the quantitative calculation needed here is written out in full |

Primary links:

- https://www.aimsciences.org/article/doi/10.3934/ipi.2019021
- https://arxiv.org/html/1907.11153v1
- https://cris.haifa.ac.il/en/publications/nonparametric-estimation-of-transfer-functions-rates-of-convergen/
- https://jmlr.org/papers/v22/19-725.html
- https://arxiv.org/pdf/1902.01848v6
- https://arxiv.org/abs/1210.1563
- https://arxiv.org/abs/1605.06973

The present deterministic FIR transfer applies to **any** estimator with the stated sup-norm response event, regardless of its source. The separate bounded-sign estimator proves such an event under this manuscript's assumptions. This cleanly separates an interface theorem from an unsupported claim that a particular prior theorem applies unchanged, and from the equally unsupported claim that prior response methods cannot be adapted.
