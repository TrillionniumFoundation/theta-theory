# Referee comparison: the smooth-envelope minimax experiment

**Status:** A mathematical comparison derived during the independent A2-v8 review. This is not a result already claimed in the submitted article, not a formal proof certificate, and not an assertion of publication priority. The nuisance alternatives below are not asserted to be realized by exact billiard tables.

**Source:** `papers/A2-v8-relative-boundary-fixed-offset/` at commit `9345433799379d23993a038e213e62b6b0c16e34`. The inputs are the physical support family, the analytic three-amplitude leading inverse, the definition of the smooth envelope in `article/60_smooth_remainders.tex`, and its acquisition theorem. The lower-bound construction is given in full here.

## 1. A fixed experiment and the additional interior condition

Fix an integer $m\ge1$. Let $K$ be a sufficiently small compact physical neighborhood of the circular parameter $\theta_c=(g_c,e)=(1/2,0)$, containing the small circular gap variations and the two-sided splitting paths described below. Write $C_j(\theta)$ for the physical leading count amplitude, $j=1,2,3$. The target is the unordered curvature triple $\kappa(\theta)$ and, for the joint loss, the gap $g$.

Fix $c_*,C_*,d_*>0$ with $c_*<C_*$ and $C_*d_*^2<1$. Consider all triples satisfying

$$
H_j\in C^m([0,d_*]),\quad c_*\le H_j\le C_*,\quad
\|H_j\|_{C^m}\le C_*,\quad H_j(0)=C_j(\theta).
$$

For definiteness, use the norm $\|H\|_{C^m}=\sum_{k=0}^m\|H^{(k)}\|_\infty$. The same proof works for the maximum convention after changing constants. Assume the following **strict interior condition**: there exists $\rho>0$ such that, for all three indices,

$$
c_*+4\rho<C_j(\theta_c)<C_*-4\rho.
\tag{1}
$$

A constant function has $C^m$ norm equal to its value, so (1) is also a norm-budget margin for the constant reference nuisances. This hypothesis can be arranged when choosing an envelope around the reference model, but it does not follow just from the non-strict inequalities defining every possible envelope in the manuscript. All assertions below are conditional on (1).

Let a fixed known interval $[L_0,U_0]$ contain all gaps in $K$, with $0<W=U_0-L_0<d_*/12$. Shrink $K$ so this is possible and so the manuscript's leading inverse and upper theorem apply. All these choices, including $m$, are fixed independently of requested accuracies and confidence.

Each fresh preparation returns only the bit

$$
Y\sim\operatorname{Ber}(p_j(t)),\qquad
p_j(t)=(t-jg)_+^2H_j((t-jg)_+),\quad j\in\{1,2,3\}.
\tag{2}
$$

Queries at nonpositive offsets are deterministic failures. A policy may choose $j,t\ge0$ adaptively from preceding bits and parameter-independent randomization, and may stop at a stopping time $T$. On every history require $t-jg(\theta)\le d_*$ for every $\theta\in K$. The complete observation is the stopped sequence of queries and returned bits, including the common randomization if needed. No lower collision values or positions are available.

Define $\mathcal N_m^{\mathrm{env}}(\varepsilon,\delta,\eta)$ as the infimum of the worst-case expected $T$ over such policies and Borel estimators satisfying, uniformly in $(\theta,H)$,

$$
\Pr\{\operatorname{dist}_{\mathrm{match}}(\widehat\kappa,\kappa(\theta))
\le\varepsilon,\ |\widehat g-g|\le\delta\}\ge1-\eta.
\tag{3}
$$

The output is a pair of target estimates, as in the manuscript's componentwise loss; it is not required to encode a single exactly fitted table. The curvature-only definition omits the gap requirement.

## 2. The comparison theorem

**Theorem.** Under the fixed choices and strict interior condition above, there are positive constants $c,C,\varepsilon_0,\delta_0$ such that, for $0<\varepsilon<\varepsilon_0$, $0<\delta<\delta_0$, and $0<\eta<1/4$,

$$
c\bigl(\varepsilon^{-(6+6/m)}+\delta^{-2}\bigr)\log(1/\eta)
\le\mathcal N_m^{\mathrm{env}}(\varepsilon,\delta,\eta)
\le C\bigl(\varepsilon^{-(6+6/m)}+\delta^{-2}\bigr)\log(1/\eta).
\tag{4}
$$

The upper bound can be achieved with an all-history bound on the number of preparations. The lower bound allows adaptation and random stopping. For curvature alone, the order is $\varepsilon^{-(6+6/m)}\log(1/\eta)$.

The result concerns the declared three-indicator observation envelope. It does not extend the physical-family lower bound to arbitrary collision observations, and it does not assert that the free nuisance functions are geometrically realizable.

### 2.1 Physical leading alternatives

Use the support family printed in the manuscript and set $R=1/4$, $\alpha=\zeta=0$, $\beta=\pm s$. The gap remains $g_c=1/2$. The two radius multisets are

$$
(R+36s,R-18s,R-18s),\qquad(R-36s,R+18s,R+18s).
$$

The corresponding coefficient triples are

$$
e^\pm=(0,-972s^2,\pm11664s^3).
\tag{5}
$$

For small $s>0$, the sorted reciprocal matching distance is

$$
\operatorname{dist}_{\mathrm{match}}(\kappa^+,\kappa^-)
=\frac{36s}{R^2-324s^2}\asymp s.
\tag{6}
$$

In particular there is a fixed $c_0>0$ giving separation at least $c_0s$. The leading amplitude map is analytic in a full coefficient neighborhood, and the area constraint is the same at the two points in (5). Bounded coefficient derivatives therefore give

$$
|C_j^+(s)-C_j^-(s)|\le M s^3,\qquad j=1,2,3.
\tag{7}
$$

One may also obtain (7) by expanding the explicit sums of $\Phi_j(R+36s)$ and $2\Phi_j(R-18s)$ and using the even area normalizer. The analytic extension justifies the coefficient argument without any separation assumption. All parameters in (5) belong to the one fixed set $K$ for sufficiently small $s$.

### 2.2 A nuisance splice with a fixed norm budget

On $[0,\infty)$ set

$$
\psi(u)=(1-u)_+^{m+1}.
$$

This is $C^m$ on its domain, equals one at zero, and vanishes for $u\ge1$. Its derivatives through order $m$ vanish at the splice point one and have finite bounds depending only on $m$.

Write $\overline C_j=(C_j^++C_j^-)/2$ and $D_j=(C_j^+-C_j^-)/2$. Choose a fixed large constant $L>0$, set

$$
h=L s^{3/m},\qquad
H_j^\pm(d)=\overline C_j\pm D_j\psi(d/h).
\tag{8}
$$

The equality $H_j^\pm(0)=C_j^\pm$ is exact. The perturbation and its derivatives satisfy

$$
\|(H_j^\pm-\overline C_j)^{(k)}\|_\infty
\le M_m s^3h^{-k}
=M_m L^{-k}s^{3(1-k/m)},\quad 0\le k\le m.
\tag{9}
$$

For $k=m$, first make the right side smaller than a prescribed part of $\rho$ by choosing $L$ sufficiently large. For $k<m$, make the finitely many right sides sufficiently small by decreasing $s$. Since $\overline C_j\to C_j(\theta_c)$, (1) then ensures positivity, the pointwise upper bound, and the full $C^m$ norm bound, for both signs and all three indices. Also $h<d_*$ for sufficiently small $s$.

Thus (8) is a pair of admissible nuisance triples in one fixed envelope, not a family of shrinking norm balls. The alternatives may depend on the requested accuracy, as in an ordinary minimax lower bound, but the envelope itself does not.

### 2.3 Every query has little information, including fixed positive offsets

Both alternatives have the same gap, so a common query has the same offset $d=t-jg_c$. At $d\le0$ it gives no information. At $d\ge h$, (8) gives exactly the same probability under both signs.

For $0<d<h$,

$$
|p_j^+(d)-p_j^-(d)|
=d^2|C_j^+-C_j^-|\psi(d/h)\le M d^2s^3.
$$

Moreover $p_j^-(d)\ge c_*d^2$ and $1-p_j^-(d)\ge 1-C_*d_*^2>0$. The Bernoulli inequality obtained from $\log x\le x-1$ gives

$$
D_{\mathrm{KL}}(\operatorname{Ber}(p_j^+)\Vert\operatorname{Ber}(p_j^-))
\le\frac{(p_j^+-p_j^-)^2}{p_j^-(1-p_j^-)}
\le C d^2s^6\mathbf 1_{\{0<d<h\}}
\le C h^2s^6=C L^2s^{6+6/m}.
\tag{10}
$$

The constants are independent of the query location. No shrinking-offset restriction has been imposed on the policy: the adversarial nuisance pair itself makes every larger offset uninformative.

### 2.4 Stopping and the confidence logarithm

Condition on a common finite history and the parameter-independent random seed. The next query or stop decision is the same under both hypotheses. Applying the chain rule to the first $M$ transcript positions, padded after stopping, and using (10), gives

$$
D_{\mathrm{KL}}(\mathsf P_+^{[M]}\Vert\mathsf P_-^{[M]})
\le C s^{6+6/m}\mathbb E_+(T\wedge M).
$$

Relative entropy on the increasing transcript sigma-fields converges to that of the full transcript. Monotone convergence on the right therefore gives, whenever $\mathbb E_+T<\infty$,

$$
D_{\mathrm{KL}}(\mathsf P_+\Vert\mathsf P_-)
\le C s^{6+6/m}\mathbb E_+T.
\tag{11}
$$

A policy with infinite worst-case expected cost already satisfies the lower bound. This argument does not assume a deterministic budget or a deterministic design.

Choose $s=L_0'\varepsilon$ with a fixed sufficiently large $L_0'$ so that (6) exceeds $2\varepsilon$. An estimator satisfying the curvature part of (3) produces, by nearest-alternative classification, a test with both errors at most $\eta$. Binary data processing yields

$$
D_{\mathrm{KL}}(\mathsf P_+\Vert\mathsf P_-)
\ge (1-2\eta)\log\frac{1-\eta}{\eta}
\ge\frac14\log(1/\eta),\quad 0<\eta<1/4.
\tag{12}
$$

Combining (11) and (12) proves the curvature lower bound in (4). The same pair proves it for curvature-only loss, even if the exact common gap is supplied.

### 2.5 A gap lower bound within the same envelope

For the second pair, use circular leading parameters $(g_c,0)$ and $(g_c+\Delta,0)$ and take **constant** nuisance functions

$$
H_{j,0}(d)=C_j(g_c,0),\qquad
H_{j,\Delta}(d)=C_j(g_c+\Delta,0).
$$

They belong to the same envelope for small $\Delta$ by (1) and continuity. They are envelope laws; exact geometric realization at positive offset is not needed.

At a common query put $d=t-jg_c$ and $z=j\Delta$. Then

$$
p_0=d_+^2C_j(g_c,0),\qquad
p_\Delta=(d-z)_+^2C_j(g_c+\Delta,0).
$$

If $d\le0$, both vanish. For $0<d\le z$, $p_\Delta=0$ and $|p_\Delta-p_0|\le Cd\Delta$. For $d>z$, expand the difference of squares and use the bounded derivative of $C_j(g,0)$ to obtain the same bound, uniformly for the three indices and the fixed collar. Also $p_0\ge cd^2$ and $1-p_0$ stays bounded away from zero. Consequently

$$
D_{\mathrm{KL}}(\operatorname{Ber}(p_\Delta)\Vert\operatorname{Ber}(p_0))
\le C\Delta^2.
\tag{13}
$$

The direction is higher gap to lower gap, including the interval with $p_\Delta=0$. The same stopped chain rule gives a transcript bound $C\Delta^2\mathbb E_\Delta T$. Set $\Delta=3\delta$ and classify by the estimated gap. Equation (12) gives the gap lower bound $c\delta^{-2}\log(1/\eta)$.

The two pairs prove two worst-case lower bounds, which combine using $\max(u,v)\ge(u+v)/2$. This proves the lower half of (4).

### 2.6 The upper bound and its information requirements

The manuscript's `thm:v8-nuisance` gives, for fixed $m$, gap error at most $C_mh^{m+1}$ and curvature error at most $C_mh^{m/3}$ with all-history preparation bound

$$
C_mh^{-(2m+2)}\log(C_m/\eta).
$$

Its procedure acquires the initial bracket from the fixed interval and has no success-dependent waiting time. Its pilot and final programmed times remain admissible for every possible gap in that interval, even after a failed search. Thus it belongs to the experiment defined in Section 1, not just to a correct-search conditional version of it.

Choose a sufficiently small fixed constant $c_m$ and set

$$
h=c_m\min\{\varepsilon^{3/m},\delta^{1/(m+1)}\}.
$$

For small enough accuracies, $h$ lies in the theorem's range and both error requirements in (3) hold. Its cost is bounded by a constant times

$$
\max\{\varepsilon^{-(6+6/m)},\delta^{-2}\}\log(1/\eta)
\le(\varepsilon^{-(6+6/m)}+\delta^{-2})\log(1/\eta).
$$

The constants are fixed because $m$, the envelope, the leading inverse neighborhood, and the initial interval are fixed. This proves the upper half of (4). Omitting the gap constraint and taking $h=c_m\varepsilon^{3/m}$ gives the curvature-only upper bound. Together with Section 2.4 it establishes the asserted curvature-only order.

## 3. Exact equality on any finite positive-offset design

Fix any finite list of windows whose offsets at $g_c$ are all strictly positive, and let $d_{\min}$ be the smallest such offset. Choose the splitting parameter $s>0$ sufficiently small that the two parameters lie in $K$ and $h=L s^{3/m}<d_{\min}$. For every one of those windows, (8) gives

$$
H_j^+(d)=H_j^-(d),\qquad p_j^+(d)=p_j^-(d).
$$

Therefore all products of observations from those windows agree exactly under the two alternatives, regardless of the number of repetitions or adaptation among that finite set of windows. Yet (6) gives two different curvature targets. No estimator using only that design can be uniformly consistent on the whole envelope. For any tolerance below half this fixed pair's separation, the corresponding two-hypothesis error sum is at least one.

This includes the four fixed positive-offset windows of the exact-family theorem when evaluated at their reference gap. It does not include designs which introduce new offsets tending to onset as accuracy improves. Such designs are precisely how the upper bound avoids this obstruction.

## 4. Interpretation and boundaries

In the exact analytic family, fixed positive-offset probabilities retain the full known nonlinear relation to the four local coefficient coordinates. The manuscript proves joint order $(\varepsilon^{-6}+\delta^{-2})\log(1/\eta)$ there. In the smooth envelope, the nuisance splice can erase the cubic curvature signal outside a layer of width $\varepsilon^{3/m}$. Within that layer, the success probability contributes the additional factor $\varepsilon^{6/m}$ to the information cost. Equation (10), rather than a design restriction alone, is the reason for the slower rate.

At the particular joint target $\delta=\varepsilon^{3+3/m}$, the two experiments have the same preparation power, because the timing requirement already costs $\varepsilon^{-(6+6/m)}$. For curvature alone, or a sufficiently loose timing target, they differ. This makes the comparison depend on both the information model and the loss, as it should.

The proof does not assert a uniform $m\to\infty$ limit, analytic-nuisance optimality, unrestricted-count optimality, or geometric realization of the cutoff alternatives. Strict interior slack in the nuisance bounds is essential to the construction as stated. A boundary-degenerate envelope requires its own analysis. These qualifications are part of the theorem, not optional interpretive footnotes.
