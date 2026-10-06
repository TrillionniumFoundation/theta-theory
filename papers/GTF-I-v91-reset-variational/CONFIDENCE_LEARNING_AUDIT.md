# All-confidence learning proof audit (v80)

## New statements

Section 62 proves

\[
M_{\rm int}^{\star}(d,N,\delta,\eta)
=\Theta\!\left(N\delta^{-2}
              [d^2+d\log(1/\eta)]\right)
\]

on \(I/4\preceq E\preceq3I/4\), with absolute constants for every \(d,N\ge1\), \(0<\delta\le2^{-13}\), and \(0<\eta\le1/8\). The lower bound allows arbitrary coherent adaptive training and bounded public stopping. The upper bound uses independent one-call Choi preparations with collective processing of completed outputs, so every independent-block cap has the same interior order.

The section also proves the all-confidence full-body one-use operator-norm law, strengthens the full-body block lower bound, adds a full-body upper construction with quadratic dimension dependence and quadratic horizon dependence, and extends the v79 jointly optimal learned fixed-decoder descriptions to all confidence levels. Taking the minimum of the new one-call upper and the retained block upper gives a sharper resource comparison; it does not settle the full-body joint minimax rate or the dimension dependence of boundary entropy.

Stable labels are "thm:interiorconfidence80", "lem:diagonalconfidence80", "lem:binaryconfidenceupper80", "cor:operatorconfidence80", and "cor:interiorconfidencecode80". The one-use operator corollary requires \(0<\epsilon\le2^{-14}\); its upper-only lemma permits \(0<\epsilon\le1\). Coding requires rational \(\delta\).

## Coherent adaptive confidence lower bound

Use \(E_0=I/2\) and \(E_i=I/2+\Delta|i\rangle\langle i|\), where \(\Delta=512\delta/\sqrt N\le1/16\). The retained Bernoulli-product comparison separates each alternative from the null by at least \(4\delta\) in \(d_N\).

For a diagonal effect, insert the common computational-basis measurement before drawing the outcome coin. Keep its basis label \(J\) in an extra register. Discarding \(J\) recovers the original channel exactly, including its retained-reference state; the original controls and final estimate can ignore every extra label. The same augmentation is used under all hypotheses.

For arbitrary *different* current input/reference states \(\rho_0,\rho_i\), common input measurement contracts relative entropy. Adding the conditional Bernoulli bit adds exactly

\[
\Pr_0(J=i)\,
D(\operatorname{Ber}(1/2)\|
  \operatorname{Ber}(1/2+\Delta)).
\]

The Bernoulli divergence is \(-\log(1-4\Delta^2)/2\le3\Delta^2\). This proves the amortized inequality "eq:diagonalchain80" without assuming product inputs, matched current quantum states, or classical memory.

Common controls contract relative entropy. After padding public stopping to the deterministic cap \(M\), the resulting final states obey

\[
D(\Omega_0\|\Omega_i)
\le3\Delta^2\mathbb E_0T_i,
\qquad\sum_i\mathbb E_0T_i=M.
\]

All expectations use the same null experiment. The labels are retained for analysis and need not be disclosed to the original learner. The relative-entropy chain is valid for classical–quantum states with general measurable classical records under the manuscript's standard Borel/separable conventions.

Disjoint success balls yield, for each alternative, a binary test with both errors at most \(\eta\). Its relative entropy is at least

\[
(1-\eta)\log(1/\eta)-\log2
\ge\tfrac12\log(1/\eta).
\]

Summing over coordinates gives the explicit lower bound

\[
M\ge\frac{dN}{6\cdot512^2\delta^2}\log(1/\eta).
\]

The existing \(d^2N\delta^{-2}\) interior lower bound and the inequality \(\max\{a,b\}\ge(a+b)/2\) then give the complete joint lower rate. At \(d=1\) this reduces to the scalar confidence order.

The diagonal classicalisation is credited to Mele–Bittel, Lemma IV.19; their Corollary IV.20 already supplies a related one-use multi-coin lower bound. The source includes the relative-entropy proof to make the coherent-memory and stopping quantifiers explicit.

## Upper bound and unrestricted confidence

Mele–Bittel, Corollary III.9, supplies a legal operator-norm estimator at error \(u\) and failure \(q\), with \(O(u^{-2}[d^2+d\log(1/q)])\) calls, for \(q>4e^{-4d^2}\). Choose the rational seed \(q_d=2^{-3d}\). Its strict range condition holds even when \(d=1\), and each seed run at accuracy \(\epsilon/3\) costs \(O(d^2\epsilon^{-2})\) calls.

Let \(k\) be the least positive odd integer at least \(2\log_2(1/\eta)/d\). Run the seed procedure independently \(k\) times. Select the first estimate with more than half the estimates within operator distance \(2\epsilon/3\), with a legal fallback if no such index exists. If more than half the seeds are good, every selectable estimate is within \(\epsilon\) of the target. The probability of the contrary event is at most

\[
2^kq_d^{k/2}\le2^{-dk/2}\le\eta.
\]

The resulting cost is \(O(\epsilon^{-2}[d^2+d\log(1/\eta)])\) for every stated confidence, including probabilities below the direct range of the cited corollary. This is a dimension-dependent amplification of the existing estimator, not a new tomography primitive. The selector is Borel by norm continuity and fixed index ties.

For the interior future loss, take \(\epsilon=\delta/(8\sqrt N)\). Weyl's inequality puts both true and estimated effects in \([I/8,7I/8]\) on the good event, and the retained dimension-free interior comparison yields operational error at most \(\delta/2\).

## Two full-body upper constructions

For the complete effect body, use the same all-confidence one-call estimator at \(\epsilon=\delta/(2N)\). The hybrid inequality \(d_N(E,F)\le2N\|E-F\|_{\rm op}\) gives the required loss with \(O(N^2\delta^{-2}[d^2+d\log(1/\eta)])\) calls. Its fresh one-call acquisition is allowed for every independent-block cap.

Together with the retained block learner, "eq:fullbodyconfidenceupper80" states

\[
M_b^\star\le
C N^2\delta^{-2}
\min\left\{d^2+d\log(1/\eta),\,
           \frac{d^4}{b}\log(d/\eta)\right\}.
\]

The common range is \(d\ge2\), \(1\le b\le N\), \(0<\delta\le\min\{2^{-13},\delta_*\}\), and \(0<\eta\le1/8\). Both public every-record budgets are determined before acquisition, so selecting the cheaper construction requires no additional device calls or target-dependent advice. The logarithm in the retained block bound remains \(\log(d/\eta)\), and the factor \(1/b\) applies only to that construction. The lower and upper bounds do not in general match jointly in growing dimension and horizon.

## Learned word and resource boundaries

For the all-confidence code corollary use \(\epsilon=\delta/(64\lceil\sqrt N\rceil)\). Clip the estimated effect into the promised interior. On its good event the clipping displacement is at most \(\epsilon\), so the true-effect error is at most \(2\epsilon\); no operator-Lipschitz clipping assumption is used.

Compose the resulting Borel estimator with the finite v79 dictionary readout. The future error is at most \(\delta/8+5\delta/16=7\delta/16\), and the failure probability remains \(\eta\). The finite index map can be incorporated into the final collective POVM, so the decoder receives no exact-real side information. The query count has the sharp all-confidence rate, and the fixed-length payload remains

\[
d^2\log_2(\sqrt N/\delta)+O(d^2).
\]

The call converse applies to the decoded estimate. Positive success probability for every target forces the deterministic decoder range to cover the interior, giving the v79 bit lower bound. Training calls, trusted quantum preparation, exact classical computation, decoder reconstruction, and transmitted bits remain separate resources. Effective synthesis is not established by this section's Borel readout; the subsequent resource theorem addresses that separate question.

This document audits the written argument. Independent agent review and finite checks do not constitute formal proof certification, independent human priority clearance, or a journal decision.
