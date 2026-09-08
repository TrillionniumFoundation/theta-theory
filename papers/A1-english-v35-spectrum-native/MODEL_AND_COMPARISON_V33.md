# Information models and finite-approximation comparison — v33

## Model ledger

| Development | Acquisition and memory | Decoder / randomness | Criterion |
|---|---|---|---|
| Main collision law; Section 8 exact moment representation | Shared latent parameter; prescribed independent commands; M labels after every report; time/calibration read-only | Current label and post-compression query only; fresh private transition coins discarded; no persistent public seed | Maximum of unconditional mean checkpoint risks for one common controller; collision theorem also separately treats worst history |
| Section 8 purification | Same model; atomless prescribed command laws | Deterministic replacement preserves each conditional state law and fixed decoder mean-risk vector | Does not preserve the risk at each individual history or a public-seed-indexed decoder |
| Section 8 polyhedral updates | Same original model, including atomic prescribed command laws | Fixed decoder during row replacements, ultimately deterministic transitions | Weighted sum of checkpoint means; not an asserted convex minimax formula |
| Section 10 controlled-command corollary | Same shared latent parameter; next command chosen from retained state before report | No full-history scheduler supplied for free | Extra acquisition decision problem; not assigned the prescribed exploration collision lower bound |
| Companion graph experiments | Independent edge priors, vertex batches and stated boundary charging | Finite visited-set descriptor; any stronger converse oracle is explicit | Tensor query and separately enlarged local-readout query are not conflated |
| Companion regenerative routes/networks | Conditional regeneration at each acquired node/block | Explicit public node/route descriptor and tape-independent seed | Exact flow formula under those hypotheses, not proof of the original shared-latent theorem |
| Companion delayed-use example | Four positive acquisitions; early/jit schedules; block-boundary charging | Two labels, no persistent public coin and no feedback of prior predictions | Exact maximum of two expected risks, not incompatible checkpoint-specific designs |

## Theorem-level comparison used in main Section 13

The cited results are primary sources. Exact bibliographic data and links
are in `v33/references_main.tex`; no new novelty is claimed for classical
purification, convex separation, or finite-controller nonlinear programs.

| Resource / conclusion | Saldi–Yuksel–Linder, JMAA 2016, Assumption 3.1 / Theorem 3.2 | Saldi–Yuksel–Linder, arXiv:1511.04657, Theorems 4, 5, 11 | Yuksel–Linder, SIAM JCO 2012, Theorems 3.4 / 6.2 | Present finite approximation / Section 8 |
|---|---|---|---|---|
| Horizon / objective | Discounted stochastic control | Stated team/decentralized objectives | One stage / finite horizon | Fixed finite horizon; maximum of common checkpoint risks |
| Resource approximated | Action alphabet | Observation/action alphabets under team information structure | Observation channel | Prescribed command likelihoods and one common retained-label controller |
| Feedback information | Model state; belief-state reduction in partially observed application | Each decision maker's specified information | Observation/action history allowed | Previous label, current command/report only |
| Persistent memory bound | Not the same M-label constraint | Not identified simply with finite observations | Not the same M-label constraint | Exactly M persistent labels, read-only clock/calibration |
| Randomization | Not identified with a free persistent public decoder seed here | Information/randomness conventions remain those of each cited model | Channel/policy comparison on admitted observations | Fresh private transition coins; Section 8 removes them under atomless commands |
| Continuity conditions | Weakly continuous kernel, continuous cost and stated weight conditions | Stated continuity, compactness/integrability hypotheses | Total-variation channel convergence, uniform in state for finite horizon; bounded measurable cost | Likelihood positivity and uniform command perturbation; Borel encoding regions need not be continuous |
| Guarantee | Compact-uniform convergence of discounted values | Asymptotically optimal finite approximations/lifted policies | Continuity/convergence of optimal cost | Explicit finite-horizon absolute enclosure; exact finite-moment common-controller formula in the monomial experiment |
| Uniformity | On compact state sets under assumptions | Under stated team hypotheses | Under stated convergence assumptions | Absolute command error uniform in M and calibration; relative bound also uses the independently proved collision profile |
| Effective input | Conditions of the cited approximation theorem | Conditions of the cited approximation theorem | Channel law and convergence | Certified finite moment list for executed numerical enclosures; arbitrary full-support prior alone is not a computability assumption |

The lifted-command proof compares the original model to a cellwise-constant
likelihood on the **same command space**. It does not assert total-variation
convergence of a continuous command law to atomic point masses. Finite
team models already have information constraints; the additional issue
here is preserving factorization through one shared retained label at
all times. Section 8 eliminates controller history variables but does not
claim polynomial-time evaluation of its baseline coefficients or solution
of its nonconvex optimum.
