# Primary-source and theorem-level literature audit — fifth revision

Verification date: 22 September 2026. The introduction and bibliography distinguish cited classical machinery from the particular new causal orbit theorem. The checks below are a targeted closest-neighbour comparison, not an exhaustive proof of priority.

## Direct causal coding neighbours

**T. Linder and S. Yüksel (2014), “On Optimal Zero-Delay Coding of Vector Markov Sources.”** IEEE Transactions on Information Theory 60, 5975–5991. DOI: 10.1109/TIT.2014.2346780. Author manuscript: https://arxiv.org/abs/1307.0396; full-text version consulted: https://arxiv.org/html/1307.0396v3 .

The source model permits causal encoders and decoders with transmitted histories and studies controlled quantizer policies on posterior states. Its Walrand–Varaiya-type structure and existence results are not a theorem that a belief-valued stationary policy has a finite persistent value set. We cite the policy structure, not an unrestricted blanket deterministic stationary optimality statement for every vector Markov source.

**R. G. Wood, T. Linder and S. Yüksel (2017), “Optimal Zero Delay Coding of Markov Sources: Stationary and Finite Memory Codes.”** IEEE Transactions on Information Theory 63, 5968–5980. DOI: 10.1109/TIT.2017.2692215. Author manuscript: https://arxiv.org/abs/1606.09135; full text consulted: https://arxiv.org/html/1606.09135v2 .

Theorem 3 is the direct stationary-policy comparison: finite irreducible aperiodic Markov source, arbitrary initial distribution, deterministic stationary optimal policy and finite-horizon comparison. The policy state and per-time transmission alphabet must not be identified with the total number of persistent observer values. The author is Richard G. Wood; the abbreviated author name in the review is corrected bibliographically rather than propagated.

## Functional and spatial quantization

**H. Luschgy and G. Pagès (2004), “Sharp asymptotics of the functional quantization problem for Gaussian processes.”** Annals of Probability 32, 1574–1599. DOI: 10.1214/009117904000000324. Primary author manuscript: https://arxiv.org/abs/math/0410156 .

The comparison concerns Hilbert-space finite-centre quantization and its covariance-eigenvalue-based Gaussian asymptotics. The use of Hilbert quantization or a small-ball lower bound alone is not claimed as a new principle. The fifth revision computes a generally non-Gaussian orbit law from dynamical cylinder data and then proves finite-state causal realizability.

**M. K. Roychowdhury (2014), “Quantization dimension for Gibbs-like measures on cookie-cutter sets.”** Kyoto Journal of Mathematics 54, 239–257. DOI: 10.1215/21562261-2642377. Primary author/institutional publication record: https://scholarworks.utrgv.edu/mss_fac/251/ . Author manuscript record: https://arxiv.org/abs/1207.5842v4 .

The published work relates spatial quantization dimension to thermodynamic temperature/pressure. This is explicitly acknowledged in the introduction. The present comparison is based on the primary publication record and abstract, not a claimed independent line-by-line reproof. The v4 arXiv record is used; withdrawn earlier arXiv versions are not mistaken for the published result. The new orbit calculation adds survival-weighted future distortion and causal closure. Its spatial pressure root is not claimed as a first pressure formula in quantization theory.

## Thermodynamic machinery and tree coding

**R. Bowen, Equilibrium States and the Ergodic Theory of Anosov Diffeomorphisms**, second revised edition, edited by J.-R. Chazottes, Lecture Notes in Mathematics 470, Springer, 2008. DOI: 10.1007/978-3-540-77695-6. Primary publisher record: https://link.springer.com/book/10.1007/978-3-540-77695-6 .

Chapters 1–2 are the source for the finite-alphabet Hölder Gibbs and variational principles used in the proof. These standard principles are displayed with the exact form needed. No countable-state or billiard spectral extension is attributed to them without its hypotheses.

**B. P. Tunstall (1967), Synthesis of noiseless compression codes**, doctoral dissertation, Georgia Institute of Technology.

Variable-to-fixed greedy prefix-tree construction is a classical antecedent, not an invention of the present revision. The thesis metadata were cross-checked in a primary subsequent coding paper: M. Martinez and J. Serra-Sagristà, “Rice-Marlin Codes: Tiny and Efficient Variable-to-Fixed Codes,” https://arxiv.org/html/1811.05756v1 , reference 20. The original thesis was not independently read in this pass. The fifth revision proves its own distortion-tree properties: the priority is mu[w] V_q(w), rather than simply word probability, and the proof establishes both exact suffix closure and comparison to unrestricted causal risk. No claim is made that elementary greedy construction or the full-tree vertex-count identity is novel by itself.

## Resource comparison

| Source/result | Budget | Dynamics/observation | Mathematical role |
|---|---|---|---|
| Linder–Yüksel | Per-time channel symbols, causal policy information | Vector Markov sources | Coding-policy structure/existence on posterior states. |
| Wood–Linder–Yüksel, Theorem 3 | Zero-delay transmitted symbols | Finite irreducible aperiodic Markov source | Deterministic stationary policy optimality, not automatic finite cardinality of every policy state. |
| Luschgy–Pagès | Static N-centre Hilbert code | Gaussian stochastic elements | Functional quantization; no state transition closure. |
| Roychowdhury | Static spatial quantization | Cookie-cutter Gibbs-like measure | Spatial thermodynamic dimension. |
| Tunstall | Fixed dictionary/variable input words | Lossless source coding | Classical greedy prefix-tree antecedent. |
| v5 intrinsic theorem | ALL persistent values M | C^(1+gamma) separated Gibbs repeller with acquisitions | Finite intrinsic risk profile, all-coder lower bound, exact full-tree causal implementation. |
| v5 pressure theorem | Same M | Nonconstant derivative cocycle, nonuniform Gibbs/Markov weights | Maximum of spatial and survival pressures computes exponent and transition. |
| v5 dependent comparison | Same M | Invariant minorized acquisition kernel with hidden persistence; optional noise | Conditional raw-risk lower and exact expected-loss transfer for restarting observers. |

The earlier verified comparisons with data-rate-limited control, dynamical rate distortion/metric mean dimension and invariant minimax theory are retained in the full bibliography and relevant old sections. The closest new comparisons above are made in the new introduction. The exact Gaussian nuisance quotient remains a constrained target-minimax result, not full Blackwell equivalence in the nuisance parameter.

## Priority boundary

The paper supplies self-contained proofs of the cylinder, greedy, orbit, pressure and dependence statements while citing their classical inputs. Whether their combination and consequences meet the requested journal standard is an independent mathematical assessment. Searches and source comparisons identify relevant neighbours; they do not establish exhaustive novelty or journal suitability.
