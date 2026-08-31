# Round-Nine Independent Referee Report — GPT-5.6 Pro

**Manuscript:** A4 — *Exact History Dynamics, Domain-Safe Memory, and Universal Excess Path Pressure*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round9-referee-positive-closure-11paper-2026-08-31`  
**Payload-host branch head at review lock:** `a8c0c551f5f8614856a9d433e78b2eb92a5dcfa1`  
**Registered round-nine payload SHA-256:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`  
**Reviewed registered source:** `revision/round9-referee-final/A4_PAST_KERNEL_DISTRIBUTIONAL_MEMORY.tex`  
**Reviewed source SHA-256:** `41fb8cf5cd7ba0653b402d17a69c485b89326a0dbf67e7cde88c9bc0d86c755d`  

## Evidence boundary

At the review lock, the branch stored the checksum-pinned round-nine payload while the paper-level `main.tex` files still loaded the round-eight modules; the repository publication workflow was queued. I independently verified the payload hash, unpacked it, and ran the repository materializer successfully, producing byte-identical paper-level `ROUND9_POSITIVE_CLOSURE.tex` files. This report therefore reviews the exact registered round-nine theorem text. It does not treat a queued workflow, a clean build, theorem/proof counts, or an internal hostile-regression script as evidence that the mathematical claims are true.

## Executive assessment

The paper now conditions on a genuine symbolic past rather than on a complete deterministic microscopic history, uses the correct causal sign for the memory transform, and separates instantaneous distributions from a regular memory kernel. These are substantial conceptual repairs.

The probabilistic core, however, contains two elementary algebraic errors. The proposed martingale difference is not a martingale difference, and the statewise normalized Feynman–Kac log transform is not a semigroup. Both errors independently invalidate the quenched rough limit and nonlinear history-pressure theorem. The operator-memory statements also remain conditional on unresolved strip estimates and do not establish a billiard-specific realization.

## Decisive objections

### 1. The alleged martingale difference has nonzero conditional mean

The manuscript defines
\[
 D_{n+1}
 =A(H_n)+\chi(H_{n+1})-\mathsf P\chi(H_n).
\]
Since \(A(H_n)\) is \(\mathcal F_n^-\)-measurable,
\[
 \mathbb E(D_{n+1}\mid\mathcal F_n^-)
 =A(H_n)
 +\mathbb E(\chi(H_{n+1})\mid\mathcal F_n^-)
 -\mathsf P\chi(H_n)
 =A(H_n),
\]
not zero.

The proof simply omits the first term. Unless \(A\equiv0\), Lemma `r9-a4-martingale` is false.

There is also an indexing mismatch. With
\[
 \chi=\sum_{n\ge1}\mathsf P^nA
\]
one has
\[
 (I-\mathsf P)\chi=\mathsf P A,
\]
not \(A\). The displayed telescoping decomposition does not follow.

### 2. The quenched enhanced invariance principle has no martingale foundation

The entire proof of Theorem `r9-a4-quenched` begins by invoking the false decomposition. Conditional bracket convergence, Lindeberg estimates, second-level convergence, and the area anomaly are therefore not established.

Even after correcting the algebra, an annealed spectral gap does not automatically give uniform quenched convergence over compact infinite pasts. One must prove uniform Poisson-solution bounds, conditional bracket convergence, and tightness for the suspension interpolation.

### 3. The normalized Feynman–Kac log transform is not a nonlinear semigroup

The manuscript defines
\[
 \mathcal E_t^VF
 =\log P_t^V(e^F)-\log P_t^V1.
\]
For state-dependent \(P_t^V1\),
\[
 \mathcal E_s^V(\mathcal E_t^VF)
 =
 \log P_s^V\!\left(
 \frac{P_t^V(e^F)}{P_t^V1}
 \right)
 -\log P_s^V1,
\]
which is generally not
\[
 \log P_{s+t}^V(e^F)-\log P_{s+t}^V1.
\]
A linear Feynman–Kac tower does not survive statewise normalization. The correct alternatives are an unnormalized log semigroup, a two-parameter horizon-normalized family, or an eigenfunction Doob transform.

Thus Theorem `r9-a4-pressure` repeats a previously identified algebraic error.

### 4. The weighted Feller theorem lacks a Lyapunov estimate

A Markov semigroup is a contraction in the ordinary sup norm, not automatically in the weighted \(C_0^W\) norm. The proof does not establish
\[
 P_tW\le C_TW
\]
or preservation of vanishing at \(W\)-infinity. On a countable inducing alphabet, compactness of \(W\)-sublevels and continuity of the \(g\)-kernel in the proposed metric also require proof. The stated coupling modulus is asserted rather than derived quantitatively.

### 5. The memory theorem is conditional on an unproved continuous-time resolvent packet

The A2 estimates concern a discrete collision/roof transfer operator. The manuscript uses them as if they gave strip meromorphy and \(M+2\) vertical derivatives for the closed Doob generator \(L\) on \(L^2(\widehat\nu_\Psi)\), for an arbitrary finite-rank projection \(P\). No theorem transfers those estimates to this generator and projection.

The polynomial/regular decomposition is therefore a conditional operator statement, not a proven Sinai-memory theorem.

### 6. The descriptor realization is only an input–output bookkeeping identity

A finite principal part of a matrix meromorphic function has a descriptor realization. This general fact does not identify physical microscopic modes, prove well-posed coupling to the unresolved \(Q\)-dynamics, or yield a Markov/Hamiltonian augmented system. The paper should not advertise it as a model-specific closure.

### 7. The paper remains downstream of A2 and A3

The recurrent Gibbs component, exponential tails, spectral gap, singularity control, and pointed-excursion estimates are all imported from papers whose main theorems remain unproved.

## Minimum viable reconstruction

The authors must first correct the Poisson/martingale algebra and choose a genuine nonlinear semigroup normalization. A separate theorem should then prove quenched suspension homogenization from explicit transfer estimates. The memory material should be stated as an abstract conditional theorem unless the required continuous-time resolvent packet is established.

## Recommendation

**Reject.** Two headline theorems are contradicted by direct conditional-expectation and semigroup calculations. The remaining memory realization is largely an abstract, conditional construction.
