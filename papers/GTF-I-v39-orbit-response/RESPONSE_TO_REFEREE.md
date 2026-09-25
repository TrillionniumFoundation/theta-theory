# Response to the twenty-third pipeline-aware referee report

**General Theta Foundations I — Revision 39**  
**Minimal Orbits and the Width of Numerical Experiments**  
25 September 2026

Controlling report: `reviews/general-theta-foundations-i-v38-orbit-entropy-pipeline-harsh-top4-r23-2026-09-25/REFEREE_REPORT.md`, frozen at `5439c0ea2540e3caddbab600cc7a4f8699421439`. Reviewed v38 publication: `8ec190c921656b9869f3520ec9bf7bf754622e97`, native source `e52157d8a7df50e2ca962029e29412e7f62f0ed1`.

The report recognizes the projective theorem and asks for an orbit-level classification rather than repeated spectral calculations. This revision supplies that classification for compact connected orthogonal representations under the same full-gap resource model. It retains the projective theorem at its original signal range and keeps every earlier proof and historical path. It does not treat a change of journal target or deletion of the program title as a mathematical response.

Stable labels below are mapped to actual numbers and pages in `evidence/THEOREM_LOCATIONS.json`. All universal claims have analytic proofs in the article.

## 15.6 / Sections 6, 9 and 10 — an intrinsic orbit classification

**Addressed by a uniform orbit theorem, a matching compiler and a reducible maximum law.**

`thm:uniform-orbits` defines `s(U)=min_unit dim(Gv)` and proves the uniform orbital ball bound `A_U r^s` for a compact connected group with no invariant vectors. The infinitesimal map `X -> dU(X)v` has rank at least s at every unit direction. A finite cover of the compact product `G x sphere` supplies locally co-Lipschitz s-dimensional coordinate slices with bounded Haar density. Integrating the remaining coordinates proves a single uniform constant across singular as well as regular stabilizer types. A minimal orbit supplies the matching local power, so the exponent is not an arbitrary sufficient estimate. The proof does not assume that hidden conditional means stay on the seed orbit or have a fixed spectral type.

`thm:orbit-upper` chooses a minimal orbit of an irreducible representation. Irreducible covariance gives a ball inside its convex hull; a compact smooth orbit net loses only quadratically in its support function. With spacing N^(-1/2), one contracted net hull supports every command row. Expanding the represented scale by the reciprocal contraction makes the expectation evolve exactly. There are O(N^(s/2)) labels, at most d+1 successors per row, common command matrices and a horizon-dependent decoder. Arbitrary unit seeds work for rho<=1/(8d); minimal-orbit seeds retain rho<=1/10.

The inherited representation-valued entropy occupation theorem, reproduced with its complete proof, gives the lower order against all hidden-state machines. Thus `cor:irreducible-width` identifies the order for every nontrivial real irreducible representation satisfying the stated full-gap and calibration conditions, rather than a list of bespoke orbit examples.

`thm:sum-width` gives a further distinction: for spanning seeds in a reducible space, the exponent is half the **maximum** of the minimum orbit dimensions of its nontrivial irreducible constituents. It is not the minimum on the whole sphere, which would be zero after adding a fixed direction, and it is not the dimension of a generic product orbit. The lower proof projects a normalized seed into one constituent while retaining the actual whole-machine hidden register. For the upper proof choose branch i with weight d_i/D, charge its identifier in a disjoint label set, and amplify its conditional initialization by the reciprocal weight. The exact marginal response is the weighted sum. This prices the selector and does not impose an independent joint-output law.

`prop:matrix-orbits` gives the real, complex and quaternionic self-adjoint families. `prop:harmonic-family` gives linear width at every fixed positive spherical-harmonic degree of SO(3), although generic orbits can be larger than the minimizing orbit. `prop:separate-width39` proves that with symmetric basis seeds every internal cut separately has positive minimum D+1; those separate factorizations embed in whole machines with unrestricted other cuts. The growing theorem is therefore a compatibility statement, not a disguised static rank lower bound.

The scope is fixed representation, fixed signal and error, complete numerical words, and a full group norm gap. It is not an all-alphabet theorem or a uniform high-dimensional asymptotic. No compact-group gap is derived from the orbit rank computation alone.

## 15.2 / Section 8 — current quantum-automata comparison

**Addressed by an explicit same-task separation of semantics.**

The main article now cites the revised Chen–Wu April preprint, its Proposition 3.1 and Theorem 3.2, the May simulation paper, and Chen's September symmetry paper. The inspected August revision gives q^2+1 as its universal strict-cutpoint simulation upper bound. The reduction multiplies the signed generalized-automaton value by a positive length-dependent factor; it does not preserve numerical probabilities. The September paper's symmetry and orbit statements are compared under its own strict-cutpoint behavioral equivalence, not relabeled as numerical simulation.

`prop:sign-simulator` proves a stronger operational explanation in the present interface itself. A regular simplex gives D+1 positive command states with mean `(2D)^(-N-1) U_w x` and a common decoder at all lengths. It preserves every cutpoint sign, including ties, but its numerical error approaches a fixed positive quantity. This is explicitly a classical positive-embedding mechanism, not a claim that this conversion is newly invented.

`cor:semantic-separation` then contrasts this constant sign width with the polynomial numerical width of the same experiment. The exact centered prefix–suffix matrix still has rank at most D, so a prepare–test linear/sign-rank argument alone does not yield growth in N. Horizon-specific redesign is already allowed by the numerical lower theorem. Inverting the attenuation in a decoder need not remain in [-1,1] and is not stochastic post-processing. The proposition counts command labels in reset–command–query syntax, not an unqualified full-language PFA state count.

## 15.3 / Section 9 — quantization and covering

**The classical exponent is separated from the dynamic theorem.**

The article compares the static h-net count and quadratic support loss with Riemannian quantization, orbit convexity and projective covering. It cites Iacobelli's manifold quantization theorem, Barvinok's irreducible second-moment identity and the orbitopes literature. No projective design or moment-matching property is used. The new conclusion is that the sharp all-hidden numerical exponent is determined by a minimum orbit even if the original seed is on a larger orbit, and by the constituent maximum for reducible experiments. Static quantization of a fixed source measure would not provide either the all-epoch entropy constraint or the legal same-row compiler.

The original detailed Grassmann and projective arguments remain in appendices for their explicit constants and rational net coordinates. The new geometric proof does not delete them or claim their orbit-dimension formulas as discoveries.

## 15.4 / Section 11 — LPS operator normalization

**All convention changes are now a self-contained proposition; the requested original theorem-number verification remains explicitly incomplete.**

Appendix `sec:normalization` states the sole external inequality (LPS5) for the unnormalized sum over `1 +/- 2i`, `1 +/- 2j`, `1 +/- 2k`, on the entire mean-zero spherical L2 space. `prop:lps-transfer39` enumerates the norm-five parity representatives, identifies their adjoint rotations and inverse pairs, divides the sum by six, squares the norm bound, and proves the spherical-to-full-SO(3) transfer by the complete harmonic decomposition. It does not infer a gap on the additional half-integer representations of SU(2).

The original LPS publisher records were checked but the full 1986/1987 page images were not obtained. We therefore do not claim an inspected original theorem number. The exact numbered restatement inspected is Pisier's Theorem 3(ii), while Parzanchevski–Sarnak provides the coauthor quaternionic/Hecke account. The existence statement in the restatement alone does not specify arbitrary six matrices; the required representative convention is part of the explicit external assumption (LPS5). This is a genuine remaining source-audit limitation, not a hidden replacement by finite harmonic calculations. The numerical example retains its external dependency; the general conditional full-gap theorem is independent of it.

## 15.5 / full-gap qualifications

Every main headline states the full mean-zero group norm gap. `lem:transfer` is retained; the invariant projection is Haar averaging for the actual representation. A defining-representation gap, irreducibility, density, or a gap on only one quotient is not substituted for the full-group assumption. The special SO(3) transfer works because **all** its irreducibles occur on S2. General-q algebraic expansion remains a deep external qualitative theorem, without an invented numerical constant.

## 15.7 / resource conventions and detailed technical points

The inherited formal machine model is retained unchanged. Available labels, label bits, total program size, random-bit compilation, quantum dimension, autonomous memory and uniform computational space remain different quantities. The machine may be redesigned for N; its decoder may depend on N; tables and arithmetic are free. Only one coordinate query is answered. Randomized constituent selection is charged in the label, and coefficients are reweighted explicitly. Quaternionic Hilbert inner products use Re tr(AB).

The Grassmann graph chart has full measure, not full set coverage. The projective net is not a design. Rational projectors do not imply rational transition rows for arbitrary algebraic commands. Caratheodory controls successor count, not table-construction complexity. The six-gate constant and its large crossover remain conservative inherited certificates. Its exact error range remains in `thm:effective`.

The original projective signal rho<=1/10 is retained in `cor:projective39`; the general all-seed theorem has its separate sufficient inradius range. The calibrated error threshold is not advertised as optimal. Reducible seeds have an explicit activation factor; a component is not used in the converse unless a seed activates it.

## 15.1, 15.8 and 15.9 — title, pipeline and independent review

The program prefix is retained with a precise mathematical subtitle. The main article's conclusion requires no internal A2/B4/C2 labels. The broader orbit theorem, not editorial repositioning, is the response to the request for conceptual scope.

The current frozen Round-Seventeen ledger and the relevant v38 proofs and history records were consulted. Their A2 -> A3 -> A4 -> C2 -> D1 and hard-sphere B2/B1/B3/B4/C1/C2/D1 chains keep their Fourier/LLT, stopped-LDP, global-kernel, graph-core, nonlinear-semigroup, domain and optional-projection gates. No independent analytic gate is declared closed by this finite representation theorem. An expert's independent check of the two external gap applications has not been obtained and is not simulated by internal regression checks.

## Preservation and delivery

The entropy and quantitative all-spectra source modules are byte-identical to v38. The projective proof changes only its cross-reference to the preserved projective corollary; the effective-gate proof gains a pointer to the normalization appendix. Every old substantive proof remains in the current article or unchanged supporting/cumulative volumes. The complete v38 article is byte-identical as `supporting-results.pdf`. All older repository paths and review branches are untouched.

The compact referee package contains the focused article, this response, the literature audit and independent core sources. Large histories are optional repository archives. Executed finite checks and compilation support reproducibility, not universal proof, originality clearance or an editorial outcome. The main new classification and its explicit hypotheses are ready for independent mathematical scrutiny.
