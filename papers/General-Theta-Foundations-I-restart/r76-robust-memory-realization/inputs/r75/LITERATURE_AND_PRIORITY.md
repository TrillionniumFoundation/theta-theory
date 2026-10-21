# R75 literature, mathematical inheritance, and priority ledger

This ledger concerns the actual R75 author revision of **General Theta Foundations I**. It separates classical inputs, results already proved in earlier revisions, and the present mathematical increment. The complete preceding ledger is preserved at [inputs/r74/LITERATURE_AND_PRIORITY.md](inputs/r74/LITERATURE_AND_PRIORITY.md); the R73 ledger and earlier bibliography remain preserved with their sources. This current entry point does not replace those historical records. The controlling R74 source is commit 29b999abf11c43709e64be58765aa1984d13ac91, with complete publication commit c2c05ee3dccd23588790cd92d2aa2b0b3dac00e0. The selection and preservation records are [SOURCE_PROVENANCE.md](SOURCE_PROVENANCE.md) and [PRESERVATION_MAP.md](PRESERVATION_MAP.md).

“Inspected in R75” means that the specified primary text or publisher record was actually opened during this author pass, on 21 October 2026 UTC. Inherited inspections are identified separately. Reading publisher metadata, contents, or an abstract is not recorded as reading a complete proof. This is an author literature audit, not a new independent referee report, formal verification, human specialist endorsement, or editorial decision.

## 1. Internal priority: inheritance and increment

| Subject | Controlling inherited result | Present use or increment |
|---|---|---|
| Causal experiments, predictive states, compression, finite resources, reset experiments, discrimination, variational and dual principles, spectral geometry, and strategy realization | The complete earlier manuscript and independent companion, retained under the preservation map | These remain part of the paper's research identity and proof record. The present memory results do not settle the larger Theta pipeline. |
| Physical posterior dictionaries and stopped-law simulation | R68: thm:r68-instrument, cor:r68-risk, prop:r68-algebraic, thm:r68-block, thm:r68-noise-exponent | Multiple anchors, sparse branch rows, exact stopped laws, algebraic synthesis, clock accounting, and the physical-dictionary noise exponent are inherited. R74 drafts that rediscovered them remain archived and excluded from the increment. |
| Stochastic eigenvalue regions and phase-sensitive memory | R69: first-sector and worst-phase bounds; R71: arithmetic envelope, irrationality exponents, and badly-approximable criterion | R75 transfers the necessary spectrum and sufficient polygon statements to a complete observed instrument. The scalar spectral and arithmetic results are inherited. |
| Reversible experiments and group actions | R72/R73: common permutation-core normal form, decoder obstruction, module bound, synthesis, and prescribed pure-start accounting | These justify passing from arbitrary exact stochastic controllers to the relevant common-action optimization and remain essential lower-bound authorities. |
| Terminal contrast and normal stabilizers | R74: exact small-positive-contrast module saturation; normal-stabilizer preparation absorption; quotient LP and payoff dual; attained contrast intervals | R75 computes the multiplicity constraints, treats prescribed orbit copies, proves the converse to normal-stabilizer convexity, and solves a nonabelian family at every contrast. |
| Conditional memory with a depolarizing average | R74: a rank-three qubit family with uniformly positive report probabilities with exact root-order q versus counted q+1, or infinite memory | R75 retains that undamped result, proves a general stationary initialization law, and adds a noisy full-instrument construction with matching bounds in specified regimes. |
| Common contraction | R74: a supplied contracting norm and legal decoder ball give an explicit finite positive realization | The certificate remains inherited. The new pure-reset family does not satisfy the R68 every-posterior or fixed-block interior condition. |

The sharp four-period threshold $1/\sqrt3$ was already closed by R69 and R73. It remains closed. Finite-probe certificates, algebraic decidability under their written input assumptions, and the R74 robust payoff witness are also inherited. No existing proof is renamed an R75 discovery merely because it is reorganized.

## 2. Current mathematical assertions and scope

The complete arguments are in the native manuscript; [THEOREM_MAP.md](THEOREM_MAP.md) and [PROOF_AUDIT.md](PROOF_AUDIT.md) record their dependencies. “R75 increment” means new relative to the pinned manuscript history, not certified first publication after an exhaustive worldwide search.

### 2.1 Finite groups and the nonnormal boundary

In [sections/42-nonabelian-memory.tex](sections/42-nonabelian-memory.tex), lem:r75-fourier-multiplicity identifies response-module multiplicities with ranks of stacked Fourier blocks and supplies real descent. Schur orthogonality, complete reducibility, and Frobenius reciprocity are classical. Their operational consequence is thm:r75-orbit-multiplicity: for a prescribed orbit $H\backslash G$, the minimum copy count at sufficiently small positive contrast is the largest ceiling of the required irreducible multiplicity divided by $\dim\rho^H$. An absent active type makes every positive contrast impossible for that prescribed orbit. Allowing all orbit types gives an integer multiplicity-cover formulation of the inherited permutation-module bound. This restricted copy count is not automatically the unrestricted core minimum divided by an orbit size.

Theorem thm:r75-normality-convexity proves that a single transitive orbit's binary probability-response set is convex precisely when its stabilizer is normal. For every nonnormal stabilizer, normalized permutation-character return laws give nonconvexity witnesses at every positive contrast, including arbitrarily close to an interior constant table. The theorem supplies a separation margin without claiming its constant optimal. The normal direction is inherited R74 preparation absorption; the converse and quantitative witness are the increment.

### 2.2 Exact nonabelian transition and extremizers

For $n\ge5$, let $\chi_n(g)$ count the fixed points of $g$ in the natural action of $S_n$, and set
$$
 \beta_t(g)=\frac{1-t}{n}+\frac{t}{n}\chi_n(g),\qquad
 b_t(g)=(\beta_t(g),1-\beta_t(g)),\qquad 0\le t\le1.
$$
The current thm:r75-symmetric-return proves the complete transition
$$
 \tau_n=\frac{\sqrt n-1}{\sqrt n+1},\qquad
 \kappa_{S_n}(b_t)=
 \begin{cases}
 n(n-1),&0<t\le\tau_n,\\
 n^2,&\tau_n<t\le1 .
 \end{cases}
$$
The smaller value is attained at the boundary. At $t=0$, the constant response needs one label. At positive contrast the observable group is $S_n$, the residual count is $n!$, and the response-space dimension is $1+(n-1)^2$. The inherited prescribed-start formula adds one counted initial label to either core value. The upper constructions have physical unitary realizations with two command generators. The lower covers every permitted exact stochastic controller through the inherited normal form and the new subgroup/core argument, not just a chosen natural-orbit ansatz.

For $n\ge5$ and $t>0$, the load-bearing new lemma, lem:r75-singular-coefficient, applies to **every** nonnegative singular $n$-by-$n$ matrix $A$ with total entry sum one and
$$
 PAP=\frac{t}{n}P,\qquad P=I-\frac1n\mathbf1\mathbf1^T.
$$
It proves $t\le\tau_n$ and classifies equality, up to simultaneous coordinate permutation:
$$
 A_*=\frac1{n-1}\sum_{i=1}^{n-1}\ell_i^T\ell_i,\qquad
 \ell_i=\left(1-\frac1{\sqrt n}\right)e_i+\frac1{\sqrt n}e_n.
$$
Here the $\ell_i$ are probability rows. The corresponding minimum permutation-core preparations are rigid at the boundary, while admissible orbit weights can vary. This does not classify every stochastic transition realization or assert uniqueness of an entire controller. The additive positivity cost is $n$; its ratio $n/(n-1)$ tends to one. No increasing relative separation or minimum quantum Hilbert-space dimension is claimed.

Earlier research drafts gave a nonsharp low-contrast interval and a full-contrast obstruction. The exact threshold and coefficient extremum supersede that interim status. General high-contrast optimization for arbitrary nonnormal actions remains open.

### 2.3 General stationary initialization law

Theorem thm:r75-stationary-initializer in [sections/43-stationary-initialization.tex](sections/43-stationary-initialization.tex) compares a free initial hidden mixture with a counted pure start for finite-command edge-emitting models. Its hypothesis is predictive stationarity under a full-support average of unobserved commands, imposed on every future response. When terminal readouts are present, their separate identity includes the empty word. A one-label response has both minima one; otherwise
$$
 n_{\rm pure}=n_{\rm mix}+1
$$
with the stated infinity convention. Ordinary stationary non-i.i.d. finite-alphabet edge-emitting HMMs are a special case.

The proof eliminates the initial state through equality of its full future-response function with a convex combination of other states. Conversely the extra initializer consumes the first actual command, without an uncounted preliminary sampling operation. Neither irreducibility nor physical density representatives for classical states are required. Cesàro stationarization of a mixed hidden row, when desired, is a standard convention-preserving observation rather than an additional novelty claim.

### 2.4 Noisy full instruments and stopped-law approximation

In [sections/44-noisy-instruments.tex](sections/44-noisy-instruments.tex), retention $0\le\alpha\le1$ extends the R74 qubit instrument:
$$
 \Psi^{\alpha,\theta}_0=\tfrac18[
 \alpha\operatorname{Ad}_{U_\theta}+(1-\alpha)\mathcal D],\qquad
 \Psi_1(X)=\tfrac14\operatorname{tr}(EX)|0\rangle\langle0|,\qquad
 \Psi_2=\mathcal D-\Psi_0-\Psi_1,
$$
where $E=\operatorname{diag}(3/4,1/4)$ and $\mathcal D(X)=\operatorname{tr}(X)I/2$. The proof supplies complete positivity, uniform report floors, exact average depolarization, and one common physical polygon for all three branches. Report one always resets to a pure state, including after every string of ones. Thus neither the every-posterior nor the fixed-block R68 interior condition applies. Stationarity and one-dependence describe a fixed-angle output process; feedback policies can add temporal correlations.

For nonreal retained modes, a productive-cylinder reduction imposes the classical stochastic spectral obstruction on every exact hidden-state model. Together with the polygon construction, it gives exact first-sector counts, boundary zero-report-matrix rigidity, and the optimal simultaneous all-angle count
$$
 K(\alpha)=\max\left\{3,\left\lceil\frac{\pi}{\arccos\alpha}\right\rceil\right\}
 \quad(0<\alpha<1)
$$
with a free mixture, or $K(\alpha)+1$ with a counted pure start. A finite command alphabet already witnesses the worst-phase lower. For another specified alphabet this is an upper, not a statement that every alphabet attains it. At $\alpha=0$, the exact counts are two and three and the Hankel rank is two. The $\alpha=1$ root-order/infinite alternative is inherited R74. Outside the specified sectors, worst-phase family, and endpoints, equality of the full-instrument minimum with an arbitrary scalar eigenvalue minimum is not proved. Boundary rigidity concerns the productive zero-report matrix under the stated similarities, not the other outcome matrices.

The supplementary thm:r75-stopped-approximation gives an additional consequence. For the **same** randomized adaptive command/stopping/terminal-POVM policy, if the undamped target has expected call count at most $B$, retention $1-\epsilon$ gives complete stopped-record total variation at most $\epsilon B/8$. Nontermination is included as a scalar flag. The statement concerns this qubit without an additional entangled quantum register. Choosing $\epsilon=8\delta/B$ gives a counted-pure-label upper $\pi\sqrt{B/\delta}/4+O(1)$ in the nontrivial small-error regime. The cost hypothesis is on the target, not automatically on the approximation; policy memory is separate. This is a constructive upper, not a matching generic approximation lower, an unknown-model identification result, or a general minimax risk/resource frontier.

## 3. Representation and positive-factorization sources

### Serre 1977: classical representation theory

J.-P. Serre, *Linear Representations of Finite Groups*, Graduate Texts in Mathematics **42**, Springer-Verlag, 1977. DOI: [10.1007/978-1-4684-9458-7](https://doi.org/10.1007/978-1-4684-9458-7). [Primary publisher record](https://link.springer.com/book/10.1007/978-1-4684-9458-7).

The publisher record, contents, and chapter records for character theory, induction, and the group algebra were checked in R75; subscription chapter bodies were not accessed. Complete reducibility, Schur orthogonality, group-algebra decomposition, Frobenius reciprocity, $m_\rho(H)=\dim\rho^H$, fixed-point permutation characters, and the natural standard representation of $S_n$ are classical inputs. R75 supplies the operational deductions and a direct real-descent proof. Multiplicity language and noncommutative Fourier rank are not presented as newly invented methods.

### Gouveia–Parrilo–Thomas: symmetric cone factorizations

J. Gouveia, P. A. Parrilo and R. R. Thomas, *Lifts of convex sets and cone factorizations*, Mathematics of Operations Research **38**(2) (2013), 248–264. DOI: [10.1287/moor.1120.0575](https://doi.org/10.1287/moor.1120.0575). [Primary author text](https://arxiv.org/html/1111.3164v2).

Theorems 2.4 and 2.12 were inspected in R74 and rechecked in R75 group research. Cone lifts, slack-operator factorizations, and equivariance are prior theory. A finite response table is not automatically an entire slack operator, and live stochastic labels are not identified with extension complexity. The fixed-orbit convexity criterion and explicit nonabelian memory transition require their own probability and common-action arguments.

### Kaibel–Pashkovich–Theis: symmetry-sensitive size

V. Kaibel, K. Pashkovich and D. O. Theis, *Symmetry matters for sizes of extended formulations*, SIAM Journal on Discrete Mathematics **26**(3) (2012), 1361–1382. DOI: [10.1137/110839813](https://doi.org/10.1137/110839813). [Primary author text](https://arxiv.org/html/0911.3712v3).

Definition 11 and Lemma 12 were inspected in R74 and rechecked in R75. Coordinate-symmetric sections and symmetry's effect on positive representation size precede this paper. R75 does not import an extension-complexity lower as a memory lower; its subgroup/core argument is proved for the declared resource. The inherited key KPT10 refers to the preliminary IPCO 2010 paper, LNCS 6080, 135–148. The full journal article is from 2012.

### Gillis–Glineur: hidden-factor restrictions matter

N. Gillis and F. Glineur, *On the geometric interpretation of the nonnegative rank*, Linear Algebra and its Applications **437**(11) (2012), 2685–2712. DOI: [10.1016/j.laa.2012.06.038](https://doi.org/10.1016/j.laa.2012.06.038). [Primary author text](https://arxiv.org/pdf/1009.0880).

The full preprint's restricted-rank formulation was inspected in R74; its record and abstract were rechecked in R75. Restricting hidden factors to a prescribed visible subspace changes the optimization. R75 distinguishes action-restricted copies from the unrestricted core and proves the reduction for the symmetric-group lower. Arbitrary stochastic hidden states are not assumed physical. The DOI ends in 038; the earlier incorrect 031 suffix remains corrected.

### Bocci–Carlini–Rapallo: perturbation and persistence

C. Bocci, E. Carlini and F. Rapallo, *Perturbation of matrices and nonnegative rank with a view toward statistical models*, SIAM Journal on Matrix Analysis and Applications **32**(4) (2011), 1500–1512. DOI: [10.1137/110825455](https://doi.org/10.1137/110825455). [Primary author text](https://arxiv.org/pdf/1010.3566).

R74 records inspection of Theorem 3.1, Proposition 3.2, and publisher metadata; those sections were not freshly reread for this ledger. Local nondecrease of nonnegative rank and barycentric perturbations are established. The inherited small-contrast argument is not a first discovery that mixing restores positivity. The present singular-coefficient lemma instead states a specific normalized matrix class, sharp extremum, and equality case.

### Fourier rank in other settings

H. Lawrence, K. Georgiev, A. Dienes and B. T. Kiani, *Implicit bias of linear equivariant networks*, ICML 2022, PMLR **162**, 12096–12125. [Primary proceedings record](https://proceedings.mlr.press/v162/lawrence22a.html).

The primary abstract was inspected in R75 group research. It treats low-rank finite-group Fourier coefficients for another optimization problem. This guards against presenting Fourier rank itself as a new general method; an abstract is not used to replace a missing manuscript proof.

### Chee–Le–Ta: support-pattern factor separation

Y. M. Chee, Q.-T. Le and H. Ta, *On the Asymptotic Nonnegative Rank of Matrices and its Applications in Information Theory*, [primary author text, arXiv:2308.07187v3](https://arxiv.org/html/2308.07187v3), revised 29 January 2024.

Theorem 3.9 and Proposition 3.11 were inspected in R75 group research and rechecked by the integrating author agent. They connect nonnegative subrank with induced matchings and separate nonnegative factors by positive diagonal entries with zero cross entries. The R75 boundary-factorization proof uses that elementary support mechanism after determining its extremal coefficient matrix; the mechanism is not claimed as a new lower-bound method. The present increment is the sharp scalar-centered singular-matrix extremum, its coefficient equality case, and the resulting bounded-decoder classification and unrestricted memory law.

## 4. Realization, initialization, and identification

### Heller 1965: original authority and an access limit

A. Heller, *On stochastic processes derived from Markov chains*, Annals of Mathematical Statistics **36**(4) (1965), 1286–1291. DOI: [10.1214/aoms/1177700000](https://doi.org/10.1214/aoms/1177700000). [Primary publisher page](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-36/issue-4/On-Stochastic-Processes-Derived-From-Markov-Chains/10.1214/aoms/1177700000.full).

Heller's positive-realization antecedence is inherited. R74 verified publisher metadata but encountered a security check for the full PDF; a fresh R75 attempt to open the original full-text page failed as well. No fresh proof reading or exact theorem-number comparison is claimed. The current constructions and elimination argument are written out rather than delegated to inaccessible historical text.

### Monras–Winter: 2014 proceedings and expanded 2016 article

A. Monras and A. Winter, *Quantum learning of classical stochastic processes: The completely-positive realization problem*, TQC 2014, LIPIcs **27** (2014), 99–109. DOI: [10.4230/LIPIcs.TQC.2014.99](https://doi.org/10.4230/LIPIcs.TQC.2014.99). [Primary proceedings/PDF](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2014.99). Expanded article: Journal of Mathematical Physics **57** (2016), 015219, DOI [10.1063/1.4936935](https://doi.org/10.1063/1.4936935), [primary author full text, arXiv:1412.3634v1](https://arxiv.org/html/1412.3634v1).

The proceedings PDF's realization discussion and Theorem 6 were inspected in R75 group research. The expanded text was separately inspected for Definitions 1 and 5, Theorem 6, Lemma 7, and Appendix A. Stationary quasi-realizations, invariant polyhedral cones, group-invariance obstructions, and completely positive realizations are prior theory. Exact theorem numbers must refer to the correct version. The stationary elimination theorem works within that framework; the inspected passages do not state its controlled free-mixture/pure-start minimum comparison. This limited comparison is not worldwide priority clearance.

### Huang–Ge–Kakade–Dahleh: generic identification

Q. Huang, R. Ge, S. Kakade and M. Dahleh, *Minimal Realization Problems for Hidden Markov Models*, [primary author text, arXiv:1411.3698v2](https://arxiv.org/html/1411.3698v2), 14 December 2015; original preprint submitted 13 November 2014.

The abstract and Sections I–III, including the general-position hypothesis and quasi-realization formulation, were inspected in R75. Logarithmic-window identification concerns almost all parameter choices in a specified HMM class. Exceptional models and the quasi-HMM/positive-HMM distinction matter. R75's exact response constructions and all-word lower bounds do not identify arbitrary hidden models from data or establish efficient learning in every case. No numerical constant from abbreviated window-length descriptions is needed for this comparison.

### Ohta: tensor compression can stop at a quasi-realization

Y. Ohta, *On the Realization of Hidden Markov Models and Tensor Decomposition*, [primary author full text, arXiv:2008.11487v1](https://arxiv.org/html/2008.11487v1), 26 August 2020.

Sections 2 and 5 were inspected, together with the introductory generic/deterministic-observation distinction. The work treats stationary state-emitting HMMs and reachable/null-space reductions; its conclusion identifies the reduced tensor construction with a minimal quasi-realization. Positivity and the emission convention cannot be omitted in comparing minimum state counts. The new initialization theorem explicitly uses edge-emitting models and full response functions. It does not solve the unrestricted minimum-HMM problem.

### Earlier positive-dimension literature remains inherited

The retained bibliography includes Carlyle–Paz, *Realizations by stochastic finite automata*, JCSS **5** (1971), 26–40, DOI [10.1016/S0022-0000(71)80005-3](https://doi.org/10.1016/S0022-0000(71)80005-3); Benvenuti–Farina, *An example of how positivity may force realizations of “large” dimension*, Systems & Control Letters **36** (1999), 261–266, DOI [10.1016/S0167-6911(98)00098-X](https://doi.org/10.1016/S0167-6911(98)00098-X); and their *A tutorial on the positive realization problem*, IEEE TAC **49** (2004), 651–664, DOI [10.1109/TAC.2004.826715](https://doi.org/10.1109/TAC.2004.826715). These remain historical authorities, not newly claimed R75 full-text inspections. A gap between linear predictive dimension and positive realization size is not a new general phenomenon.

## 5. Conditional phases, noise, and stochastic spectra

### Fanizza–Lumbreras–Winter: phase obstructions and inverse-square-root noise scaling are prior

M. Fanizza, J. Lumbreras and A. Winter, *Quantum theory in finite dimension cannot explain every general process with finite memory*, Communications in Mathematical Physics **405** (2024), article 50. DOI: [10.1007/s00220-023-04913-4](https://doi.org/10.1007/s00220-023-04913-4). [Primary publisher text](https://link.springer.com/article/10.1007/s00220-023-04913-4); [author preprint](https://arxiv.org/pdf/2209.11225).

Section 2.3, Theorem 2, and Section 4.2 were inspected in R75, including cylinder/pole and Perron-normalization arguments. Section 2.3 credits the FRDN phase obstruction and commensurate counts, referring to Fox–Rubin (1968) and Dharmadhikari–Nadkarni (1970); those originals were not freshly read here. Theorem 2 already gives inverse-square-root noise dependence in a worst-phase classical-memory lower for another quantum family. Neither irrational-phase infinite memory nor that exponent is claimed first. The present scope adds matching complete-instrument bounds in specified regimes, a common commanded-angle dictionary, initialization accounting, boundaries, and bounded-target-cost stopped-law approximation. Its scalar sector formula is inherited R69.

### Karpelevič geometry and constructive boundary matrices

The stochastic eigenvalue region is credited to Karpelevič, following Dmitriev–Dynkin. The retained original source is N. Dmitriev and E. Dynkin, *On characteristic roots of stochastic matrices*, Izv. Akad. Nauk SSSR Ser. Mat. **10** (1946), no. 2, 167–184, [primary Math-Net record im3595](https://www.mathnet.ru/eng/im3595). The original Russian proof and Karpelevič's original article were not freshly reread in R75.

C. R. Johnson and P. Paparella, *A matricial view of the Karpelevič theorem*, Linear Algebra and its Applications **520** (2017), 1–15. DOI: [10.1016/j.laa.2017.01.009](https://doi.org/10.1016/j.laa.2017.01.009). [Primary author text](https://arxiv.org/html/1611.06970v2).

The introduction, classical-region description, and constructive-boundary discussion were inspected in R75. The region and arcs between roots of unity are established; this work supplies realizing matrices. R75 uses inherited R69 first-sector geometry after a response-specific productive-core reduction. A scalar mode alone is not assumed to supply a complete positive instrument model.

S. Kirkland and H. Šmigoc, *Stochastic matrices realising the boundary of the Karpelevič region*, Linear Algebra and its Applications **635** (2022), 116–138. DOI: [10.1016/j.laa.2021.11.016](https://doi.org/10.1016/j.laa.2021.11.016). [Primary author PDF](https://arxiv.org/pdf/2110.01040).

The primary PDF's region description and Type 0 Theorem 4.1 were inspected in R75. The Type 0 realization is a lazy directed cycle up to permutation similarity; other boundary types need not have that rigidity. R75 additionally forces a minimal productive zero-report block onto the relevant boundary with spectral radius $1/8$, after which the classical equality structure applies. Lazy-cycle spectral rigidity itself is not a new result here.

### R71 arithmetic is retained

The Diophantine envelope and exponents transferred to the full instrument are already proved in R71, using the same necessary spectrum and sufficient polygon bounds. The retained source A. N. W. Hone and J. L. Varona, *Continued fractions and irrationality exponents for modified Engel and Pierce series*, Monatshefte für Mathematik **190** (2019), 501–516, DOI [10.1007/s00605-018-1244-1](https://doi.org/10.1007/s00605-018-1244-1), [author version arXiv:1810.10127v1](https://arxiv.org/abs/1810.10127v1), records the standard irrationality-exponent identity used there. No fresh full-text reread or new number-theoretic theorem is claimed in this ledger.

### One-dependence alone is not new

A. E. Holroyd and T. M. Liggett, *Finitely dependent coloring*, Forum of Mathematics, Pi **4** (2016), e9. DOI: [10.1017/fmp.2016.7](https://doi.org/10.1017/fmp.2016.7). [Primary author PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/12/4col.pdf).

R74 records inspection of the introduction, Theorem 1, Proposition 3, and Section 5; this is an inherited read. Stationary one-dependent processes without finite hidden-Markov models already exist, with an obstruction credited there to Schramm. The present family is assessed through its simultaneous explicit physical, predictive, probability-floor, and exact-memory properties. No first-existence claim for one-dependent non-HMM processes is made.

## 6. Polyhedral quantum simulation and different resources

### Okay 2026: adaptive polyhedral updates

C. Okay, *Polyhedral classical simulators for quantum computation*, Research in the Mathematical Sciences **13** (2026), article 55. DOI: [10.1007/s40687-026-00626-x](https://doi.org/10.1007/s40687-026-00626-x). [Primary publisher full text](https://link.springer.com/article/10.1007/s40687-026-00626-x).

R74 records inspection of Theorem 16, Lemma 17, Corollary 19, and the publisher's 2 June 2026 publication date; this is retained rather than described as a new read. Preserved polytopes with legal updates and adaptive composition are explicit prior mechanisms. R75 supplies its particular common polygon, exact response-level lower, and initialization/approximation consequences, without claiming invention of adaptive polyhedral simulation.

### Aubrun–Szarek: physical dictionaries are a particular resource

G. Aubrun and S. J. Szarek, *Dvoretzky's theorem and the complexity of entanglement detection*, Discrete Analysis (2017), paper 1, 20 pp. DOI: [10.19086/da.1242](https://doi.org/10.19086/da.1242). [Primary author text](https://arxiv.org/pdf/1510.00578).

R74 records inspection of Section 6 and Proposition 10. Convex approximation of density matrices is established, with stronger dimension dependence than the manuscript's elementary net. R68's exponent concerns a physical dictionary covering a whole shrunken state body. A realization of one response may use nonphysical hidden states, so that dictionary lower cannot replace an unrestricted memory lower. No best-possible dimension claim is made from the elementary construction.

### Fawzi: extension complexity is not live memory

H. Fawzi, *On polyhedral approximations of the positive semidefinite cone*, Mathematics of Operations Research **46**(4) (2021), 1479–1489. DOI: [10.1287/moor.2020.1077](https://doi.org/10.1287/moor.2020.1077). [Primary author text](https://arxiv.org/pdf/1811.09649).

R74 records inspection of Theorems 1 and 2 and related work. Lifted description size, vertex count, universal physical dictionary size, and live stochastic labels are distinct resources. Those extension-complexity lowers are not transferred automatically to this manuscript's memory counts; the latter use explicit operational reductions.

## 7. Search limits and unresolved claims

Additional R75 searches for the singular-coefficient extremum combined nonnegative singular matrices, double centering, scalar compression, rank-one perturbations, permutation characters, and the exact radical threshold. Some hits were adjacent matrix/perturbation literature; other quoted searches returned irrelevant results. No inspected source was verified to contain the same normalized extremum and equality class. This records a limited search, **not exhaustive absence of prior work**. Irrelevant hits are not cited as evidence. Priority of the exact matrix lemma and its operational deductions remains open to specialist correction.

Historical access limits remain visible. The R74 attempt to consult a Gillis monograph passage on rank-one perturbations encountered a large-PDF tool limit and HTTP 503; an author-hosted Vidyasagar survey redirected to an unavailable page. Their detailed hypotheses were not verified by those attempts. Serre's subscription chapter bodies and Heller's original proof were not accessed in R75. Inherited readings are not retroactively promoted to fresh reads.

The present results do not close arbitrary high-contrast nonnormal-action synthesis, every fixed-phase noisy-instrument optimum, approximation memory with matching general lowers, arbitrary unknown-model identification, or the independent A1/A2 and wider Theta objectives. These have distinct questions and quantifiers. The paper retains its Annals of Mathematics, Acta Mathematica, Inventiones Mathematicae, and Journal of the AMS research ambition. Neither a longer bibliography nor finite exact diagnostics establishes an editorial outcome. The new proofs, preserved dependencies, and stated scopes are the material offered for the next independent assessment.
