OPERATIONAL = r'''
\begin{lemma}[Affine witnesses and executable tests]\label{lem:operational_tests}
On a compact predictive carrier $K$, the uniform closure of the linear span of the constant and the determining affine test coordinates is $\aff(K)$. A finite expression $c_0+\sum_{i=1}^m c_i f_i$ can be realized as the expectation of a signed bounded score by randomly selecting one of the executable tests $f_i$, provided they share a legal continuation budget. The score bound and test-selection cost must be included. A uniform limit is not thereby one finite-cost experiment, and a maximum of affine expectations is not generally an executable single-test expectation.

In the local allocation inequality, uniform approximation of every affine component within $\epsilon$ changes the difference of its two sides by at most $2\epsilon$. In the simultaneous inequality this bound is $2n\epsilon$. Thus every strict finite-coordinate dual violation is preserved by sufficiently accurate finite test-span approximation, without identifying a convex dual function with one physical continuation.
\end{lemma}
\begin{proof}
Let $W$ be the uniform closure of the stated span. If a continuous affine $f$ were not in $W$, Hahn--Banach and the representation of continuous linear functionals on $C(K)$ would give a finite signed measure $\mu$ annihilating $W$ but not $f$. Since constants lie in $W$, its positive and negative parts have equal mass. If that mass is positive, their normalized probabilities have equal determining coordinates and therefore the same barycenter. Affinity gives equal integrals of $f$, a contradiction. Zero mass is immediate. Uniform limits of affine functions are affine, proving equality.

For a finite expression put $C=\sum_i|c_i|$. If $C>0$, choose $i$ with probability $|c_i|/C$, execute its test, and score $c_0+C\operatorname{sgn}(c_i)T_i$, where $T_i$ is the actual test outcome with conditional expectation $f_i$. For normalized $|f_i|\le1$ the score has absolute value at most $|c_0|+C$. The required physical budget is the common allowed budget, with its selector and programme costs, not an assertion that arbitrary collections of differently typed tests have one cheap execution. If $C=0$ only the constant is needed.

The maximum of finitely many functions is 1-Lipschitz in their uniform component norm. The two local measures have mass one. In the simultaneous expression, the left total occupancy mass is $n$, while $\sum_{z,a}\eta_{z,a}(\mathcal Y_a)=n$ and the Radon--Nikodym phase weights sum to one. Applying the same bound on each side gives $2n\epsilon$.
\end{proof}
'''
FINITE_EXAMPLE = r'''
\subsection{Finite matrices and a sharp programme-reuse threshold}
For finite reports, write $\mathbf f_t(q)$ for the constant and a finite affine coordinate basis, when the carrier is finite-dimensional. Given the proposed occupancies, predictive states and action rows, put
\[
 A_{t,z,a,y}=p_{t,z}\alpha_z(a)J_t(q_{t,z},a)(y)
              \mathbf f_{t+1}(F_t(q_{t,z},a,y)),\qquad
 b_{t,j}=p_{t+1,j}\mathbf f_{t+1}(q_{t+1,j}).
\]
Then the simultaneous allocation is precisely the finite feasibility system
\begin{equation}\label{eq:finite_matrix}
 \sum_{z,a,y}A_{t,z,a,y}k_{z,a,y,j}=b_{t,j},\qquad
 k_{z,a,y,j}\ge0,\qquad\sum_jk_{z,a,y,j}=1.
\end{equation}
It is a linear system for a \emph{fixed proposal}; optimizing the occupancies and action rows is not generally one linear programme. Finite-dimensional linear-programming duality gives the finite version of \eqref{eq:simdual}. Each report row occurs once, even if used at several phases. With finite raw states, retaining the unnormalized physical occupancy vectors instead yields polynomial recursions in the controller rows, directly connecting this formulation with finite-state-controller parameter synthesis\cite{junges}.

A small complete experiment shows both nontrivial feasible reuse and a sharp risk threshold. There are four paid calls and action types \emph{sense} and \emph{respond}. At calls one and three only sense is legal; its binary reports have respective laws $(3/4,1/4)$ and $(1/4,3/4)$. At calls two and four only responses $0,1$ are legal. Call two returns a deterministic \emph{return} marker and call four a deterministic \emph{finish} marker. A hidden scoring register records whether the first response was $0$ and the second response was $1$. After the observer has halted, a fixed audit scores the average of the two errors; the scoring register and audit outcome are never readable before the decision. The audit adds one physical scoring call if included in acquisition totals, not one more controller transition. This is an ordinary positive finite kernel after adjoining the phase and score to the hidden state.

\begin{theorem}[A finite sharp reuse frontier]\label{thm:finite_reuse}
For this prepared four-call experiment, with one autonomous programme and the entire label set counted,
\begin{equation}\label{eq:finite_reuse}
 R_{\aut}(4,M)=
 \begin{cases}
 +\infty,&M<3,\\
 1/2,&M=3,\\
 1/4,&M=4,\\
 0,&M\ge5.
 \end{cases}
\end{equation}
An external observer with one label at every phase has risk zero. The internally timed thresholds do not follow from a clock-neutral-report theorem: the return and finish markers have different phase supports.
\end{theorem}
\begin{proof}
First suppose one sense location is reused. If $a,b$ are the probabilities that its report rule ultimately selects response zero on reports zero and one, the two phase probabilities are
\[
 u=(3a+b)/4,\qquad v=(a+3b)/4.
\]
Every $(u,v)\in[0,1]^2$ is separately phasewise feasible. One common row exists exactly on the nontrivial parallelogram
\begin{equation}\label{eq:reuse_polytope}
 0\le3u-v\le2,\qquad0\le3v-u\le2,
 \qquad a=(3u-v)/2,\quad b=(3v-u)/2.
\end{equation}
These are the finite simultaneous constraints. In particular $u-v\le1/2$, so the average error $(1-u+v)/2$ is at least $1/4$. The common deterministic row $a=1,b=0$ attains it. For an interior feasible example, $a=3/4,b=1/4$ gives $(u,v)=(5/8,3/8)$; the displayed inverse recovers the same randomized row at both phases.

Labels reached at sense and response cuts cannot coincide: their stationary action distributions would have to be supported in two disjoint legal action sets. A stopping label is different from both. Thus at least three labels are necessary. With exactly three, there is one response label, whose fixed response distribution is the same at both scored calls; its average error is $1/2$. A chain using the markers to return to the sense label and then halt attains it.

With four labels, if there is only one response label its average error is still $1/2$. Otherwise there is exactly one sense label and at most two response labels. Any randomization at the response labels can be composed with the sense row to give the common binary probabilities $a,b$ above, so the same $1/4$ lower applies to \emph{all} randomized programmes. Attain it with labels $s,r_0,r_1,d$: sense at $s$, send report $y$ to $r_y$, respond $j$ at $r_j$, send return to $s$ and finish to the stopping label $d$. These are phase-independent rules.

With five labels, use two sense locations $s_0,s_1$, two response locations and one halt location. Initially sense at $s_0$ and send either report to $r_0$; return goes to $s_1$, whose reports both go to $r_1$; finish goes to halt. The risk is zero. The external observer knows the stage and can choose the correct response without retaining the reports, also at zero risk. No unscored internal memory has been used.
\end{proof}
'''
OBSTRUCTION_NOTE=r'''
\begin{remark}[Why compactness supplies no enumeration rate]\label{rem:obstruction_rate}
Consider a fair hidden bit, a constant report, one acquisition and two allowed terminal labels, under binary error loss. The acquired predictive law is $\delta_{1/2}$ and the true risk is $1/2$. The proposed retained law $(\delta_0+\delta_1)/2$ has the same barycenter and risk zero. It passes every affine inequality but fails the convex-order condition. A countable dense convex-test enumeration may start with any prescribed finite number of affine functions. The corresponding finite relaxation therefore remains at zero for an arbitrarily long initial segment. Density and compactness alone give no bound on that index. This example concerns the supplied enumeration, not a lower bound for every algorithm. The effective theorem obtains its quantitative certificate from additional instrument and computation data, not by reinterpreting topological compactness as an effective modulus.
\end{remark}
'''
