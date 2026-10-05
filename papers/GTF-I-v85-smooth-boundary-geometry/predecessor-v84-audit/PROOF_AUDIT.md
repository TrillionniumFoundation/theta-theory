# Proof audit — Revision 84

This is an author-side mathematical audit. It is not a formal proof-assistant certificate, an independent human opinion, or an inference of theorem correctness from regression tests. Both R53 reports are preserved verbatim. All predecessor mathematical sections are byte-identical.

## Support-kernel theorem

The Hilbert spaces are real Hermitian matrix spaces with trace inner product. `W_E=sum_j P_j H_d P_j` is a real linear **support span**, not an algebra and not generally the scalar span of the effects. The covariance variance identity says that its kernel consists precisely of tuples with `P_j K_j=P_j S_E(K)`. Write `S=B+iA`. Hermitian diagonal support blocks force `P_j A P_j=0`; the remaining blocks give `K_j=B+i[P_j,A]+Z_j` with `Z_j=Q_j Z_j Q_j`. Zero tuple sum fixes B. Conversely `sum E_j(i[P_j,A]+Z_j)=iA`, which proves the proposed parameterization. A common Hermitian X equal to iA must vanish, proving injectivity. The dimension formula includes every zero effect and all support multiplicities. No effect inverse is used.

## Unitary tangent range

For `H_j=i[G,E_j]`, missing-support compressions `Q_j H_j Q_j` vanish. The pairing with the A-part of the kernel is exactly `-2 tr(GA)`; the correction terms `E_j G P_j+P_j G E_j` lie in the support span. Thus H is orthogonal to the complete kernel iff G lies in W. In particular a stationary generator is in W. The spectral tangent formula is a formula for the regularized covariance energy and is not used, on its own, as a lower operational bound.

## Finite-angle operational theorem

The square-root upper integrates the retained complete-body path theorem. The covariance and tangent conjugate together, so the finite pseudoinverse energy is constant along the orbit. The lower repeats a fixed single-component eigenvector probe and uses the finite Bernoulli-product inequality. It holds for all N on a fixed two-sided small-angle interval; constants depend on E,G.

For a generator outside W, its orthogonal residual A is traceless because I is in W. Its positive and negative parts give states with equal compression on every support. Flagged purifications yield a two-dimensional code satisfying all Kraus-product correction identities, including off-diagonal Kraus products within each outcome. Diagonalizing the correction Gram matrix proves a completely positive, trace-preserving recovery on the **actual classical label and retained reference**. The complement of its correctable output space is explicitly assigned a fixed state; this completion is necessary for the derivative argument. The device environment is never made available.

If V_l are Kraus operators of the completed channel T, exact correction gives `V_l J=c_l I` and trace preservation gives `sum conjugate(c_l) V_l=J*`. This proves that the corrected one-use derivative is the logical commutator. Each unitary-channel Taylor remainder is bounded by `2 t² ||G||op²`; adding two gives `4 t² ||G||op²`. Telescoping m channel compositions gives `4 m t² ||G||op²`. The ideal logical-qubit separation is exactly `2 |sin(m t Delta/2)|`. Choosing m below the first oscillation, with the displayed angle cap, gives the positive lower `min(1,N|t|Delta)/(2 pi)`. No asymptotic QFI statement is substituted for this finite trace estimate. No perfect-discrimination assertion is made.

The recovery is common to both hypotheses and designed using the known E,G. It is not a common learner of an unknown POVM. The construction uses a logical qubit between calls and a per-call reference dimension at most 2d. Its gate synthesis and physical execution are not claimed. Ideal trusted controls are an explicit theorem hypothesis.

## Relation to established channel metrology

The Kraus operators `|j><a|sqrt(E_j)` have Hermitian product span exactly W. This identifies the criterion with the established Hamiltonian-not-in-Kraus-span condition. Zhou–Jiang's channel-estimation theorem and the Knill–Laflamme correction criterion are credited at the construction. The support-kernel formula and written finite-angle error ledger are the objects submitted for scrutiny here, not a claim that the metrological dichotomy was discovered in this revision.

## Processing-covariant regularization

For public probabilities w, the added operator is the covariance of the scalar measurement `(w_j I)`. Both the measurement and scalar covariance obey the same Jensen-square inequality under a column-stochastic T. The dual energy is defined on the full tuple space, modulo constant tuples, so `T*L` need not have zero sum. Supremum comparison proves contraction including infinite values and zero output rows. A stochastic left inverse gives equality. The same tau and the transported weights Tw must be used. A fresh uniform output ridge is not substituted. The operational upper follows separately from `B_w <= max(w) Id`; for uniform w the parameter is tau=k/N, not 1/N.

## Exact computation and finite checks

Rational support projections are constructed from independent columns and a positive Gram inverse. Real-coordinate elimination is used only for linear independence; metric projection uses the Hilbert–Schmidt Gram system. Exact rank and PSD predicates replace all floating tolerances. The support certificate identifies a local regime for a specified known orbit and does not compute the adaptive distance or a recovery channel.

`support_check.py` executes 280 positive checks and 18 negative controls. It compares direct covariance nullity against the support formula, checks the unitary-range criterion and commutator pairing, singular/zero/full-rank examples, output refinement and coarse-graining, rational unitary invariance, transported-ridge equality and contraction, and resource/error rejection. A nonprojective d=2,k=4 BB84 example has an exactly computed reference recovery and a rational nonzero-angle unitary. This is a symbolic channel identity, not a physical experiment. All 21 predecessor suites also execute anew in normal and optimized Python. No finite suite proves a continuum theorem, priority, arbitrary gate efficiency, or whole-program completion.

## Conservation and document structure

V83_BASELINE.json pins 495 native files, 856 complete labels, 363 quantitative labels and 116 structural labels. Every predecessor mathematical section remains byte-identical. The shortened primary and its current binary supplement jointly retain all prior quantitative labels; the relocation list is checked and emitted. All previous complete-edition proof sections remain active in the complete edition, and the structural graph remains unchanged. Cross-document references are rebuilt from current TeX auxiliary files, with only actual theorem labels exported; AMS internal layout labels are excluded. Four linked-document compilation rounds and an independent standalone package rebuild qualify the references. No historical PDF is needed.
