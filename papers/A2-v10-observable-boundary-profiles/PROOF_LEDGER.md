# A2 v10 proof and preservation ledger

## Source identity

Author baseline: `33ef794a398b23015651482e93be7667c08d6fad`. Controlling review: `b756f4851669e34c7074ba61b5bcf48689756406`. The revision is based on the completed-v9 nonlinear manuscript, not the other v9 initialization.

## Main inherited dependency chain

The physical geometry and observation normalization are in `v3/10_geometry_action.tex` and `v3/20_integration.tex`. Weighted stationary-action localization supplies the summable perturbations used by `v4/10_boundary_layers.tex`; `v5/15_differentiated_operators.tex` supplies fixed-order differentiated determinant control. The scalar operator comparison is retained in Section 8. The relative law, with its closed-collar offset derivatives, feeds the full smooth-profile inverse in Section 9. The endpoint experiment transfer remains in `v6/10_experiment_transfer.tex`.

The finite-dimensional analytic inverse and binary minimax results retain their own physical-family hypotheses. The smooth-envelope minimax result retains the strict interior-slack hypothesis and its separate nuisance observation model. Round 33 Fourier/arithmetic material is retained as historical conditional derivation, not used to replace the local physical proof chain.

## New declarations and proof steps

### Theorem 11.1 — finite-preparation recovery of full profiles

Source: `article/25_profile_acquisition.tex`, label `thm:v10-acquisition`.

Inputs: known gap g, free area A, multiplier parameter gamma, selected facing patches; the common closed collar; the existing bound ||F_j,b-F_bb||C3 <= C0 tau^j and F_j,b <= M; profiles in K_m(B,beta;D), m >= 4, with a C^{m-1,1} bound, positivity and V(0)=1. Quantitative sampling assumptions do not restrict the existing general forward theorem.

Construction: positive-offset grid; exactly normalized empirical Bernoulli proportions; finite preselected dictionary; first minimizer of the broken-C3 interpolation discrepancy. Unsuccessful preparations are charged. The target is the full weighted symmetrized energy profile, not an arbitrary contact graph.

Proof dependencies: Lemmas 11.3–11.4; exact Bernoulli variance and exponential-moment inequality; union bound; the old C3-to-C0 Volterra stability argument. The dictionary bound is a statistical existence construction, with no claimed computational cost.

Main error decomposition: h^(m-3) + tau^j + t h^(-3) + delta. The smooth bridge error is controlled before differentiating interpolation noise and therefore is not h^(-3)-amplified. The odd limiting law is predicted from the two reconstructed profiles, with an explicit bilinear Lipschitz bound.

### Corollary 11.2 — an explicit accuracy budget

Label `cor:v10-budget`.

Set h comparable to epsilon^(1/(m-3)), t=c epsilon h^3 and delta=c epsilon. Choose the least even j with tau^j <= c epsilon. Then exp(j gamma) <= C epsilon^(-gamma/|log tau|). Sum d_k^(-2) over positive nodes, rather than using the worst node for all allocations. The resulting sufficient preparation power is 2+8/(m-3)+gamma/|log tau|, with log(C/(eta epsilon)). No minimax lower bound or equality tau=exp(-gamma) is asserted.

### Lemma 11.3 — positive-node stencil bounds

Label `lem:v10-stencils`.

Fixed m-point interpolation reproduces polynomials. A degree-(m-1) Taylor expansion with a Lipschitz highest derivative gives the approximation error. A quadratic Taylor expansion gives uniform C3 stability. Scaling the Lagrange basis gives h^(-3) amplification only for unrestricted nodal perturbations. The first cell extrapolates a bounded distance from strictly positive nodes; no data at zero are assumed.

### Lemma 11.4 — compact dictionary and inverse estimate

Label `lem:v10-dictionary`.

Arzela–Ascoli and the fundamental theorem of calculus give compactness of K in C^{m-1}. The mass-one simplex map preserves the required bounded regularity. The finite-grid forward image is compact and has a finite delta-net with representatives in K. A finite ordered minimization is Borel measurable. The Abel reduction, normalization at zero and Gronwall give the C3-to-uniform inverse bound at this regularity. Candidate profiles need not be physically realizable billiards; their use is solely regularization of a true physical profile.

## Expository changes without a new theorem

Section 10 adds the closest inverse-problem comparison with explicit functional settings. Section 1 supplies the information table and mathematical dependency narrative. The closing paragraph of Section 9 separates even-law reconstruction from odd-law validation. Part headings and the final comparison organize all retained material without changing its hypotheses or proof text. Historical delivery status is labelled historical in the current manifest and README.

## Preservation and verification

The original 168 formal environments in the active v9 inputs remain byte-identical in order. Their length-prefixed concatenation has SHA-256 `8eaec7e57da29cad14396fec82418ebd413f1359e013086f44929d28d3e77447`. The new total is 176. Existing repository paths and both old review branches remain untouched.

New diagnostics: 179 exact finite algebra checks, 36 ordinary floating-point design-rounding checks and eight source-integrity checks. The inherited 249 and v9 407 checks also pass in normal and optimized modes. These suites overlap. They check finite identities, design algebra and retention, not the truth of all infinite-dimensional analytical hypotheses or the proof of every theorem. The 97-page article and seven-page companion are cleanly reproducible locally; no remote CI or formal proof certification is claimed.
