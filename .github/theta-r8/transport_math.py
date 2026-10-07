EDITS = {
'main.tex': ('main.tex', [
(39, 40, r'''A prepared causal experiment acquires a geometry of conditional future responses. We prove a resource transfer theorem combining recursively executable covers with lower bounds at information cuts. A conditional version retains useful geometry even when no global product minorization exists. For a sequential continuation-chart class, the cut width and the optimal finite-state risk are equivalent in order. A noisy regression experiment with a continuous future query realizes a strict separation: online excess is of order $M^{-2/d}$, while terminal checkpoint excess is of order $M^{-2}$ for the same bounded binary task. We also prove a joint acquisition--memory law for nonhomogeneous progressive sensors, allowing smooth and singular factors. An attained erasure defect and a finite-bit implementation give a common resource account. Sparse hidden-state filtering and a submitted nonreset singular supplement verify distinct raw-kernel mechanisms. Theorems concern their stated preparation, strategy and interface classes; they do not assert a universal classification of causal encoders.
'''),
(44, 44, r'''\input{sections/08_continuation}
\input{sections/09_noisy}
'''),
]),
'references.tex': ('references.tex', [
(6, 6, r'''\bibitem{equitz} W. H. R. Equitz and T. M. Cover, \emph{Successive refinement of information}, IEEE Trans. Inform. Theory \textbf{37} (1991), 269--275.
\bibitem{fox} B. Fox, \emph{Discrete optimization via marginal analysis}, Management Sci. \textbf{13} (1966), 210--216.
'''),
(15, 15, r'''\bibitem{orlitsky} A. Orlitsky and J. R. Roche, \emph{Coding for computing}, IEEE Trans. Inform. Theory \textbf{47} (2001), 903--917; conference version, Proc. FOCS (1995), 502--511.
'''),
(16, 17, r'''\bibitem{companion} Q. Qi, \emph{Supplement S to General Theta Foundations I: Acquired Geometry and Causal Resource Transfer}, submitted supplement to this article, 2026, Sections~1--7; supplied in full as part of the same submission, not a separate publication.
'''),
(21, 21, r'''\bibitem{watanabe} S. Watanabe, S. Kuzuoka and V. Y. F. Tan, \emph{Non-asymptotic and second-order achievability bounds for coding with side-information}, IEEE Trans. Inform. Theory \textbf{61} (2015), 1574--1605; accepted author version arXiv:1301.6467v5.
'''),
(22, 22, r'''\bibitem{wynerziv} A. D. Wyner and J. Ziv, \emph{The rate-distortion function for source coding with side information at the decoder}, IEEE Trans. Inform. Theory \textbf{22} (1976), 1--10.
'''),
]),
'sections/01_experiments.tex': ('sections/01_experiments.tex', [
(1, 2, r'''A causal experiment does not present an observer with a parameter manifold. It presents preparations, admissible interventions and reports. Geometry becomes relevant only after specifying which future reports are to be predicted and which information the observer has actually acquired. There is a further obstruction: a small terminal codebook need not be recursively selectable after earlier reports have been discarded. We use \emph{General Theta} for the mathematical program connecting prepared causal kernels, executable future tests, their minimal predictive quotient, resource-certified experiment comparison, acquired geometry and prediction or decision risk. ``Foundations'' refers to this order of construction, not to a claim that all causal encoders have already been classified.
'''),
(3, 4, r'''The central resource transfer theorem, Theorem~\ref{thm:transfer}, has a constructive and a converse side. Physical-law block stability and a relation-preserving global cover construct a legal predictor rounded after every report. In the other direction, the conditional responses to a future suffix form a random element of a separable function space. Quantization of its actual dominated law obstructs every finite retained alphabet crossing the earlier cut. Terminal quantization is the last member of this family, not a replacement for it.
'''),
(5, 6, r'''Theorems~\ref{thm:cutduality} and~\ref{thm:chart} make this converse constructive on a specified class. The first gives an exact one-cut functional-compression problem, two-sided comparison under common-channel domination, and localization over physically supplied side information. The second proves that acquired continuation widths are equivalent in order to a genuinely executable sequential recursion under a positive-mass response chart and a global response modulus. Correlation of acquired reports is allowed. Raw density and regeneration lemmas produce the required common laws rather than postulating a formal reachable set.
'''),
(7, 8, r'''Theorem~\ref{thm:noisy} exhibits why this earlier geometry is necessary. In noisy Gaussian regression, a later noisy observation and a continuous query specify a bounded binary prediction task. The terminal conditional mean is scalar and has checkpoint excess of order $M^{-2}$. Its earlier response-function geometry has dimension $d$ and forces online excess of order $M^{-2/d}$, which a finite recursion attains. Thus a noisy stochastic continuation, not exact random access, separates checkpoint and online exponents in the same scored experiment. The response metric is derived from the raw likelihoods.

A separate difficulty concerns acquisition itself. A lower for one fixed exploration does not determine an optimum over explorations. Theorem~\ref{thm:adaptive} resolves that optimization for progressive binary sensors with independent fair unread tails. Observed bit values do not alter future tail scales; this is the structural reason that a deterministic greedy allocation attains the optimum over all allowed adaptive policies. Arbitrary nonhomogeneous scales permit smooth, singular and mixed product laws without a limiting dimension. Theorem~\ref{thm:joint} combines acquisition, memory, calibration and an attained simulation defect in one task. Theorem~\ref{thm:digital} supplies a finite-bit feasible account, rather than identifying label count with total complexity. Theorem~\ref{thm:brier} gives the sharp state order for ordinary squared filtering loss in sparse Gaussian hidden-state models.

The quantitative completeness theorem applies to the stated sequential-chart class, not to every causal experiment or every intervention design. The general block and cut certificates are not asserted to be universally dual. Conditional projection, functional source coding, quantization, classical allocation and comparison inequalities are explicitly credited in Section~\ref{sec:literature}. Supplement S~\cite{companion} is a submitted part of this same article, supplied in full with the manuscript; it retains the nonreset singular, stopped, calibration, output-grid and typed-interface proofs. It is not an external publication or a repository-only proof premise.
'''),
(14, 15, r'''Here $c$ records nonnegative raw-call, time and other declared resource increments. Positivity means nonnegativity and normalization. Dirac operations, failure symbols and missing reports are allowed. A visible history $h_t$ consists of the preparation report, public exploration coins, and intervening actions, reports and public costs. Private exploration coins that influence later actions remain in the physical/controller state and the actual conditional law unless genuinely reported. Legal action sets have a declared measurable graph. Strategies are parameter-independent Borel kernels on those sets; stopping rules use the visible filtration. They cannot consult future reports or the unknown $\lambda$.
'''),
(18, 19, r'''A predictor retains at most $M$ data labels at each declared cut. Its update uses only its current retained tuple, current action/report and allowed fresh randomness. Any controller, simulator or clock register consulted later is counted separately or included in the label tuple. Temporary workspace must be erased before the next cut; program constants must be known, parameter-independent data with a charged description. A vector output is a write-only stream: previously emitted coordinates are not rereadable workspace. The notation $M$ is an alphabet cardinality, not total arithmetic space. If a public finite phase has $Q$ states, the full serial cardinality is at most $MQ$; a lower bound at a cut uses the \emph{entire} accessible data-dependent tuple. Deterministic time is fixed in the main prediction statements and is not a hidden observation channel.
'''),
(24, 24, r'''
\begin{lemma}[A compact measurable section]\label{lem:selector}
A continuous surjection $e:K\to S$ between compact metrizable spaces has a Borel section.
\end{lemma}
\begin{proof}
For each $n$ fix a finite closed cover $(F_{n,j})_j$ of $K$ by nonempty sets of diameter at most $2^{-n}$. Inductively select the first $j_n$ for which $e^{-1}(s)\cap F_{1,j_1}\cap\cdots\cap F_{n,j_n}$ is nonempty. For a fixed finite index word its compact intersection has closed image under $e$. Each finite-word selection event is therefore Borel, using finite Boolean combinations of those closed images. The selected compact intersections are nested, meet the fiber, and have diameter tending to zero. They have a unique common point in $e^{-1}(s)$. Choosing once a point of each nonempty finite-word intersection gives Borel finite-valued approximants converging to that point. Their pointwise limit is a Borel section.
\end{proof}
'''),
(31, 32, r'''The evaluation map is a continuous surjection from a compact space to a Hausdorff space, hence is perfect. Its product with the report identity is also a quotient map: closedness follows by taking a convergent subnet in the compact belief domain whenever an image net converges. The instrument coordinates and their positive-density ratios therefore descend continuously. The positive-density domain is open in $S\times Y$; no update is defined by division at a null report. For measurability jointly across actions, Lemma~\ref{lem:selector} supplies a Borel section of the compact evaluation map. Composing the assumed joint versions with this section supplies joint Borel versions of all descended kernels. A common jointly Borel null-report extension, when needed on wrong candidates, is additional data.
'''),
]),
'sections/02_transfer.tex': ('sections/02_transfer.tex', [
(4, 5, r'''At a deterministic cut $s\le T$, let $H$ be the actual prefix and $U$ the complete physical pre-decision suffix, including all post-cut public actions, phases, costs and reports. The complete decision history is generated by $(H,U)$. The fixed exploration supplies their joint law $\Lambda(dh,du)$. A dominated continuation certificate consists of a probability measure $\eta$ on the suffix space and a finite measure $\underline\mu$ on prefix histories such that
'''),
(32, 33, r'''At cut $s$ write its retained label as $i(H)$. Give the suffix decoder all of $U$, even when its original online implementation would retain less. Conditional on fixed coins, including all future private decoder coins, composing the finite sequence of later Borel updates gives an output $a_{i(H)}(U)$ for at most $M$ Borel response functions. Here $U$ contains all post-cut public actions, phases, costs and reports, not observation values alone. Projection and \eqref{eq:domination} give
'''),
(72, 72, r'''All certificate measures are unnormalized: scaling $\underline\mu$ scales $q_M(\xi_s)$ by the same factor.
'''),
(81, 81, r'''
The lower can also include every conditional continuation width of Theorem~\ref{thm:cutduality}. On the sequential-chart class of Theorem~\ref{thm:chart}, their supremum and the optimal recursively achievable excess are comparable; outside that class no sufficiency is claimed.
'''),
(109, 110, r'''$W_{CM}\le C' q_M(\nu_T)$, with the same specified full-state cut. A family for which this inequality fails cannot have that claimed online/checkpoint matching, even if its terminal marginal has small covering number. Here $CM$ already denotes the entire data-dependent tuple at that cut. A separately stored phase of $Q$ values must be accounted for as $CMQ$ unless its value is deterministic at that cut; the constant $C$ cannot silently absorb a growing phase.
'''),
(125, 126, r'''Let $e$ be the average posterior bit-classification error. The two inequalities used are
\[
 h_2(e)\ge(1-\log_2M/d)_+,\qquad
 p(1-p)\ge p/2\quad(0\le p\le1/2).
\]
The first is concavity of binary entropy; the second bounds Bernoulli posterior variance by its classification error. Conditional projection proves \eqref{eq:randomaccess}. Zero error forces distinct positive-probability labels for all strings. This is the classical entropy mechanism behind random-access bounds~\cite{nayak}, used here to distinguish two information cuts of a single prediction task, not claimed as a new coding inequality.
'''),
(129, 130, r'''Suppose a finite implementation agrees with a routine satisfying the upper hypotheses until a flagged first failure, and, conditional on the current past and on no earlier flagged failure, its probability of failing at step $t$ is at most $\beta_t$. A repair routine using the same codebook can always be selected on a failure to satisfy the original relation and local-error bound. For a loss in $[0,L_*]$, the actual implementation has risk at most the repaired upper plus $L_*\min(1,\sum_{t\le T}\beta_t)$.
'''),
]),
'sections/03_acquisition.tex': ('sections/03_acquisition.tex', [
(1, 2, r'''The cut argument concerns a fixed exploration. We now optimize acquisition itself. The raw interface in this section is progressive sensing: a call selects a coordinate and reveals its next unread binary digit. Neither a coordinate value nor an infinite tail is supplied as a pre-decision report. This interface is appropriate to a multiresolution measurement, and its restrictions are part of the theorem. Independent fair unread tails make their future variances depend on depth, not on observed bit values. Thus the policy optimization below is not arbitrary observation-dependent experimental design.
'''),
(33, 34, r'''The total order on merged entries is decreasing numerical scale, then increasing coordinate index, then increasing level; it is compatible with each strictly decreasing coordinate list. The sequence is known from the experiment, not estimated from the observed bits.
'''),
(50, 51, r'''At the greedy allocation $k^b$, every coordinate with $k_j^b>0$ has final weighted cylinder length at least $aR_b$. Indeed its last parent was a maximum at an earlier greedy step, hence was at least the eventual maximum $R_b$. In a fixed coordinate all level-$k_j^b$ cylinders have that same length. They have disjoint interiors because each ratio is at most $1/2$; their endpoints have zero fair-product mass. A ball for $\norm{\cdot}_\omega$ of radius $aR_b/4$ has projection length at most $aR_b/2$ in each weighted coordinate. Here physical length is $\ell_{j,k}$, weighted length is $\sqrt{\omega_j}\ell_{j,k}$, and the ball projection diameter is measured in the latter coordinate. It meets at most three of these intervals in each active coordinate. Each product cylinder has mass $2^{-b}$. Consequently
'''),
(54, 55, r'''Coordinates never split contribute just one interval and do not weaken the bound. The product mass is still $2^{-b}$ because $b$ counts the total number of active binary splits.
'''),
(76, 77, r'''Let $\mathcal F_t$ be the sigma field generated by the complete action/report history through call $t$ and an independent seed containing all policy coins. Initially, conditional on the seed, the claim is the product preparation. A selected coordinate is a function of revealed data. Its next unread bit is fair and independent of all other unread bits. Revealing it, or performing an idle, preserves the induction. Conditional means and variances are therefore given by \eqref{eq:actualcenter} and the displayed tail series. Its first term has coefficient $b_{j,k+1}\ge\ell_{j,k}/2$, giving the lower in \eqref{eq:tailvariance}. The whole tail has range of length $\ell_{j,k}$, giving the upper. Each realized allocation has sum at most $n$, so \eqref{eq:minmaxscale} bounds its largest weighted length below by $R_n$. Sum the nonnegative variances and then average. Removing the conditioning on coins proves the claim for randomized policies as well.
'''),
(80, 81, r'''Let $N=n+2\ge2$, $M\ge1$, and $K=\min\{n,\lfloor\log_2M\rfloor\}$. Optimize over all parameter-independent adaptive policies for the raw interface above and all online predictors whose entire data-dependent retained tuple, including any data-dependent acquisition-controller state, has at most $M$ values at every pre-decision cut. Define the analogous checkpoint optimum by allowing the prediction encoder one final access to the complete acquisition history. Then
'''),
(109, 109, r'''For equal weights $\omega_j=1/d$ and constant ratio $r$, write $K=du+v$ with $0\le v<d$. The greedy allocation has $v$ coordinates at depth $u+1$ and the others at depth $u$, so $R_K^2=r^{2u}/d$. Thus the shorthand $R_K^2\asymp r^{2K/d}/d$ includes a factor between $1$ and $r^{-2}$ caused by the remainder.

'''),
(120, 120, r'''\textbf{The virtual exact-bit report must be completed before any progressive command or terminal audit.} All comparisons in this theorem impose that order.
'''),
(139, 139, r'''The common precision $p$ below is charged for each coefficient and each output coordinate. Bit operations use sequential finite tapes, not unit-cost large integers or an uncharged random-access memory.
'''),
]),
'sections/04_filters.tex': ('sections/04_filters.tex', [
(46, 46, r'''For completeness, choosing $K=\lfloor(M/n)^{1/d}\rfloor$ when $M\ge n$ gives $K\ge\tfrac12(M/n)^{1/d}$ and $nK^d\le M$, hence $K^{-1}\le2n^{1/d}M^{-1/d}$. This is the stated all-budget conversion.
'''),
(77, 77, r'''Use the ordinary Euclidean norm inherited from $\R^{d+1}$ on the simplex. Euclidean projection of any forecast onto that closed convex simplex cannot increase its squared loss against a categorical outcome.
'''),
(103, 103, r'''
The density in the lower proof is with respect to the chart $(\pi_1,\ldots,\pi_d)$, with $\pi_{d+1}=1-\sum_{i\le d}\pi_i$; its Euclidean metric is comparable to the full simplex metric. Choosing the clipping failure probability $\zeta=O(M^{-2/d})$ adds at most the bounded-loss constant times $\zeta$ and therefore preserves the displayed excess order.
'''),
]),
'sections/05_composition.tex': ('sections/05_composition.tex', [
(12, 13, r'''Under the upper hypotheses of Theorem~\ref{thm:transfer}, put $\rho=r_M+u$ and $K_\tau=\lceil\tau/m\rceil$. There are explicit finite constants $c,C$, depending only on the block certificate, such that with
'''),
(16, 17, r''' \le C\{\E V_0+\rho^2\E K_\tau\}.
'''),
(18, 19, r'''Consequently $e_0=O(\rho)$ and $\E K_\tau\le L_0$ give
'''),
(38, 40, r'''Multiply the rearranged inequality by the predictable indicator $\one_{\{k<K_\tau\}}$ and sum the finitely many terms. This gives
$(1-\gamma)\E\sum_{k<K_\tau}V_k\le\E V_0+c_0\rho^2\E K_\tau$.
'''),
(48, 49, r''' (C_1c_0/(1-\gamma)+C_2)\rho^2\E K_\tau,
'''),
(54, 55, r'''\begin{lemma}[Measurable maximal report coupling]\label{lem:coupling}
For probability kernels $P_z,Q_z$ on a standard Borel report space, there is a jointly measurable coupling whose disagreement probability is $\norm{P_z-Q_z}_{\TV}$ for every parameter $z$.
\end{lemma}
\begin{proof}
One construction uses nested finite partitions generated by a countable separating algebra. Relative to $R_z=(P_z+Q_z)/2$, their atomwise density ratios are bounded measurable functions. Martingale convergence gives a jointly measurable clipped limsup version $p=dP_z/dR_z$ for each $z$; put $q=2-p$. The common kernel $\mu_z=\min(p,q)R_z$ has mass $c_z$. The coupling
'''),
(60, 60, r'''\end{proof}
'''),
(71, 72, r'''There is one Borel common scored-outcome map and one decision space, with loss in $[0,L_*]$. Uniformly over the common parameters, declared target policies and permitted bounded stops, the joint law of virtual history, permitted public policy coins and scored outcome differs from its target law by at most $\varepsilon$ in total variation. A transducer relying on a real hidden history or unspecified phase is not a finite implementation. Let its state count be $R$, target prediction count $M$, controller count $C_{\rm ctr}$ and phase/clock count $Q$. Workspace, read-only program, precision, raw calls and physical time are separate coordinates. Submitted Supplement S~\cite{companion} gives the fully typed standard Borel transcript construction; these requirements are precisely the ones needed in the following implication.
'''),
(96, 96, r'''
The target class in the exact-bit comparison is all progressive policies with the compulsory early completion order of Theorem~\ref{thm:joint}. In the Gaussian filtering comparison it is the fixed report-adapted physical controller of Theorem~\ref{thm:brier}, with the bounded visible stopping class of Proposition~\ref{prop:stopped} when stopping is used. In Corollary~\ref{cor:noisynumeric} it is the fixed-order regression acquisition and its finite-state prediction class. No implication identifies these different classes.
'''),
]),
'sections/06_literature.tex': ('sections/06_literature.tex', [
(9, 9, r'''
\subsection{Decoder side information and functional source coding}
In the Wyner--Ziv problem~\cite{wynerziv}, the encoder observes a memoryless source block $X^n$, while the decoder additionally observes $Y^n$; the rate--distortion expression minimizes $I(X;W)-I(Y;W)$ over a Markov auxiliary $W-X-Y$ and a decoder reproduction satisfying the distortion constraint. At our cut, $H$ is the encoder observation, $U$ is decoder side information, and $z(H,U)$ is the remote conditional-mean task. These identifications are substantive: fixing a causal cut produces an ordinary side-information coding problem. Formula~\eqref{eq:exactfunctional} is its direct finite-code variational form, not a new source-coding principle. Unlike an asymptotic rate, $M$ bounds the entire retained tuple in one actual experiment, and the task and its Bayes baseline remain fixed through the cut.

Orlitsky and Roche~\cite{orlitsky} study reliable computation of a function of the sender's and receiver's combined data. Their problem is closer than ordinary reconstruction of the sender's source: future reports change the function that the earlier information must support. Our response function $z(h,\cdot)$ records exactly that dependence. The difference is not the observation that functions can be compressed. It is the quantitative use of an actual product sublaw to put all responses in a common $L^2(\eta)$ metric, together with retained submeasure mass and recursively attainable bounds under the stated raw acquisition interface. Zero-error distinguishability and asymptotic functional coding are not being asserted equivalent to squared-distortion Hilbert quantization.

Nor is finite blocklength, by itself, a novelty claim. Watanabe, Kuzuoka and Tan~\cite{watanabe} give nonasymptotic achievability and second-order bounds for side-information problems, including Wyner--Ziv coding. Those bounds concern coding probabilities and rates under their information-spectrum formulation. Here \eqref{eq:cutsandwich} instead compares a hard one-cut cardinality directly with a finite-measure geometric distortion, and \eqref{eq:conditionalcut} localizes when the global reference product fails. Lemma~\ref{lem:minorization} derives the reference from physical report kernels. It does not improve the general finite-block coding bounds of that literature.

The recursively executable conclusion is separate from all these one-cut reductions. Theorem~\ref{thm:chart} explicitly stores quantized incoming coordinates, proves an all-tail moment bound, and gives equivalence of online risk and continuation width on its declared correlated sequential class. Theorem~\ref{thm:noisy} computes a positive-noise, continuous-query example in which the same task has different online and checkpoint exponents. Gaussian conditioning, companding and density quantization are standard tools. The claimed synthesis is the raw-kernel continuation lower together with the legal intermediate-state upper and their common-task separation; no independent priority certification is inferred from this comparison.

\subsection{Allocation and successive refinement}
Incremental allocation for a separable discrete resource constraint has classical marginal-analysis antecedents, including Fox~\cite{fox}. Our merged-list argument is an elementary exchange argument in that tradition. In particular, it does not introduce greedy bit allocation for independent components. The objective in \eqref{eq:minmaxscale} is the largest remaining weighted scale, not an unspecified average-rate Lagrangian. Its value also controls the physical-law small balls and the residual uncertainty under every paid progressive policy. These additional links are what make one scale govern both $N$ and $M$ in \eqref{eq:adaptivelaw}.

Equitz and Cover~\cite{equitz} characterize successive refinement by compatible rate--distortion-optimal reproductions, with the coarse reproduction conditionally generated from the finer one. Their staged code describes a known source block at asymptotic rates. Here each new digit must first be physically acquired, and all already acquired digits count against a hard state cardinality rather than an entropy-coded average rate. Exact prefixes provide an executable refinement mechanism, but we do not deduce that arbitrary sources are successively refinable. Nonhomogeneous coordinate scales and singular factors remove a stationary high-rate formula, not the independence assumption. Observed values cannot change future scale values in this model; an extension to genuinely value-dependent experimental design requires another acquisition converse.
'''),
(24, 25, r'''The new obstruction and the sufficient construction deliberately have different assumptions. Global joint-law domination may have very small mass or fail entirely. Conditional cuts can remain useful, as Example~\ref{ex:diagonal} proves. Theorem~\ref{thm:chart} proves quantitative completeness on its explicit sequential-chart class; passing every available cut test is not proved sufficient outside such a constructively verified class. The profile \eqref{eq:adaptivelaw} is optimized over every adaptive allocation in its raw sensing class, but not over arbitrary interventions, unknown-kernel learning or unbounded stopping. It includes only the stated deterministic phase convention; total persistent state includes any separately stored clock.
'''),
(28, 29, r'''Thus the central connection is mathematical rather than terminological: the prepared kernels determine future tests, their measurable predictive realization and actual acquired laws; compatible finite recursions construct the upper; dominated continuation cuts and acquisition variance supply converses; and typed causal morphisms transfer both at their declared resources. The class equivalence and the noisy separation are proved without an independence or contraction assumption on acquired prefix coordinates, but do not constitute a necessary-and-sufficient classification of every recursive acquired geometry.
'''),
]),
'sections/07_clarifications.tex': ('sections/07_clarifications.tex', [
(2, 3, r'''Submitted Supplement S~\cite{companion}, Section~5, supplied in full and intended to be refereed with this article, supplies a second direct verification of the block hypotheses, distinct from Gaussian filtering. We record its raw data and the exact point of attachment so that its status is not confused with the adaptive progressive-sensor class of Section~\ref{sec:adaptive}.
'''),
]),
}
