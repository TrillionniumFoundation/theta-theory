# Derivation of the equal-prior initial-spectrum formula — Revision 95

The derivation is instantiated by the six named results in Primary Section 21. It is independent of the local-tube approximation estimates.

1. **Operational reduction.** Keep the original equal-prior law and the once-drawn hidden basis. Every legal protocol with retained old dimension two has a dimension-preserving refinement with positive Grams A_yh of rank at most two, sum_h A_yh=rho, and fresh density Grams b_yh. For X=(C tensor D)(I-dS)(C tensor D)^*, equal labels yield alpha tr X_+ and all unequal labels yield alpha tr(-X)_+, where alpha=t^2/[2d^2(d+1)]. The leaf gain is alpha ||X||_1.

2. **Filtering concavity.** The trace norm equals max tr XZ subject to -M<=Z<=M. Mixtures of feasible intervals prove concavity in M. With M=A tensor B and A diagonal, averaging simultaneous diagonal unitaries gives a diagonal fresh B upper. This upper is unconstrained in fresh rank; feasibility is restored by an explicit two-coordinate maximizer.

3. **Exact leaf.** If eigenvalues of normalized A are (1+z)/2,(1-z)/2, write v=1-z^2 and fresh eigenvalues (1+w)/2,(1-w)/2. The 2-by-2 block has nonpositive determinant. Its norm, plus the two negative scalar entries, is F_z(w)=[(d-1)(1+zw)+sqrt((z-w)^2+d^2v(1-w^2))]/2. Introduce C=d(d-2)+(2d-1)v, psi as in the paper, T=2psi-(d-1), and w*=z((d-1)T-1)/C. Expansion gives (T-(d-1)zw)^2-D(w)=C(w-w*)^2. Both the sign of the square-root upper and the feasibility of w* are proved. This gives max F=psi. Rank-one and zero factors are handled without division.

4. **Spectral concavity.** Rationalizing psi reduces differentiation to h(v)=v/(a+b sqrt(c+sv)). Its first derivative is positive and decreases. Thus f(x,1-x)=psi(4x(1-x)) is symmetric strictly concave, including endpoints by continuity.

5. **Exact roof.** The retained v94 spectral-envelope lemma applies with r=2. The least rank-two majorant is (q,1-q), q=max(lambda_max(rho),1/2). Every branch ensemble has mean f at most psi(4q(1-q)); at most d commuting atoms, all of this spectrum, attain it.

6. **Physical converse.** Factor each weighted atom as C_h^*C_h and act on the actual initial purification with V_h=C_h C_0^+. Prepare the explicit fresh factor on a two-dimensional reference and read positive/negative centered spectral projections according to the classical label relation. These operations saturate the leaf and roof simultaneously. Summing d first labels gives P=1/2+t^2 psi/[2d(d+1)].

7. **Qubits and inference.** When d=2 one atom suffices. Put u=sqrt(det rho): psi=1+6u^2/(1+4u), and fresh bias w*=z/(1+2sqrt(1-z^2)). Subtraction from the known rank-two global optimum gives exact spectral loss. Inverting the increasing psi after deducting a calibrated score error bounds lambda_max(rho).

A finite certificate evaluator uses rational square-root enclosures. It does not estimate a physical reset defect, synthesize an unknown eigenbasis or certify a general all-rank equal-prior formula.
