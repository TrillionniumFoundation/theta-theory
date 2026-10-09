# Literature comparison (checked 9 October 2026)

Primary sources checked include arXiv:2301.11244 (Yuksel, v3 dated 18 December 2024), arXiv:2601.03132 (Mintae Kim, 6 January 2026), arXiv:2602.08734 (Hudak et al., 2026), the SIAM article DOI 10.1137/24M1643736, the INFORMS strategic-measure article DOI 10.1287/moor.2022.0188, the JMLR paper 23(11) (2022), and the original Lorden overshoot and Mundhenk small-policy references. Current arXiv identifiers are cited as preprints rather than inferring unverified journal publication. The native bibliography also directly cites the classical measure-theoretic and renewal tools.

| Route | Relevant conclusion | Difference from native R24 |
|---|---|---|
| Witsenhausen static reduction | Independent reference representation of causal control | Reused finite rows still need their product-coordinate continuity; diagonal report law shows the missing condition. |
| Strategic measures / Yu universally measurable policies | Existence, epsilon-optimality and related minimax results under their information hypotheses | Does not itself prove closure/continuity of the fixed-cardinality reused-row subset or this reset-tail uniform bound. |
| Yu–Bertsekas average finite-state approximation | Near optimality over the set of finite-state controllers | Not the same-M robust value and all-Borel lower certificate. |
| Yuksel history-space approach | Discounted/average existence without belief reduction; finite-window approximation | Different policy topology and initialization; R24 charges compulsory observer resets and optimizes a fixed alphabet. |
| Demirci–Kara–Yuksel | Average optimality through nonlinear-filter contraction | R24 return certificate and nonexpansive cycle examples do not require strict filter contraction, but impose the distinct reset protocol. Neither result is asserted to subsume the other. |
| Kara–Yuksel finite windows | Stability-based finite-memory near optimality | Window length is not directly the same as arbitrary M-state compiled memory. |
| Kim 2026 | Policy-conditional Wasserstein comparison on one execution | R24 geometric layer likewise states fixed exploration; general robust average theorem separately optimizes its whole declared class. |
| Hudak et al. / inductive FSC synthesis | Learned/extracted or inductively synthesized evaluated controllers | R24 provides all-Borel lower coverage, but not comparable computational scalability. |
| Mundhenk small policies | Complexity of small-policy optimization | Exhaustive finite enumeration is not an efficient algorithm claim. |
| Renewal reward / Lorden | Classical ratio and overshoot tools | Used explicitly; novelty is not attributed to these standard identities. |

Candidate new contribution: their precise fixed-budget synthesis with actual return-tail uniformity, sharp time and scored-cycle defect moduli, primitive same-M certificates, and occupation geometry with independent hidden/noncommuting verifications. This is not an independent novelty or priority certification, and no named open problem is claimed solved solely by citation absence.
