# Round-Nine Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B1 — *Microcanonical Preparation and Exponential-Scale Ensemble Transfer for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round9-referee-positive-closure-11paper-2026-08-31`  
**Payload-host branch head at review lock:** `a8c0c551f5f8614856a9d433e78b2eb92a5dcfa1`  
**Registered round-nine payload SHA-256:** `cf230322211332af59a7883af1b669eeb9b4f7e9f4220fc24712c634bda17716`  
**Reviewed registered source:** `revision/round9-referee-final/B1_FULL_PRESSURE_WEIGHTED_SHELL.tex`  
**Reviewed source SHA-256:** `3598672575c035e84bf3be971a852f6cb0cb7ddff581b295cb76a266d1820593`  

## Evidence boundary

At the review lock, the branch stored the checksum-pinned round-nine payload while the paper-level `main.tex` files still loaded the round-eight modules; the repository publication workflow was queued. I independently verified the payload hash, unpacked it, and ran the repository materializer successfully, producing byte-identical paper-level `ROUND9_POSITIVE_CLOSURE.tex` files. This report therefore reviews the exact registered round-nine theorem text. It does not treat a queued workflow, a clean build, theorem/proof counts, or an internal hostile-regression script as evidence that the mathematical claims are true.

## Executive assessment

The revision keeps the source-dependent saddle, analyzes the full hard-sphere pressure rather than an idealized proxy, and retains the varying likelihood inside a nontrivial shell integral. These are the correct structural responses to earlier objections.

The new proof still lacks a valid high-frequency minorization for the dynamically tilted hard-sphere law, and the shell class is so broad that the coefficient may itself have exponential cost. The claimed local coefficient and the ensuing microcanonical LDP therefore do not follow.

## Major objections

### 1. The connected remainder is not made small by shrinking a source chart

The proof of the covariance lemma says that the Hessian of the connected remainder has norm at most \(c\) “after reducing the common chart once.” Shrinking the neighborhood in \((H,\lambda)\) does not make the value of the connected Hessian at its center small. A quantitative small parameter—short time, density, or \(\varepsilon\)—is required.

The total Hessian is an actual covariance and may be positive for other reasons, but the perturbative proof written in the paper is invalid.

### 2. The conditional good-block construction is not justified for a path/contact tilt

At time zero, hard-core exclusion has finite geometric range. The source-decorated path law does not. A bounded contact/path source weights future trajectories and couples particles from initially separated cells whenever they may collide during the horizon. With unbounded Maxwellian velocities, no fixed enlargement of a spatial cell isolates its future collision cylinder uniformly.

Consequently the conditional law in one cell, given the outside configuration, need not have a uniformly bounded Radon–Nikodym ratio or a source-uniform full-rank minorization. “Reveal alternating cell families” does not restore conditional independence for a global dynamical Feynman–Kac weight.

This is the load-bearing step in the high-frequency theorem.

### 3. The Fourier estimate is not derived from the stated minorization

Even under a valid minorization, the proof must keep track of the number of selected cells, the \(\varepsilon\)-dependent cell size, hard-core compatibility, the lattice coordinate, and the connected source weight. The text supplies no construction showing linearly many disjoint \(n_0\)-particle cells with uniformly positive conditional success probability.

The statement that the conditional specifications “already contain \(R_\varepsilon\)” does not prove a complex-frequency bound for the full characteristic function.

### 4. The coefficient theorem permits shells with exponential cost

The only declared size condition is that \(W_\varepsilon\) be bounded and have diameter \(o(\sqrt{\mu_\varepsilon})\). This permits, for example, a one-dimensional interval of length
\[
 |W_\varepsilon|=e^{-2\mu_\varepsilon}.
\]
The Gaussian integral in Theorem `r9-b1-coefficient` then has logarithm
\[
 -2\mu_\varepsilon+o(\mu_\varepsilon),
\]
not a subexponential logarithm.

Thus the proof of Theorem `r9-b1-main`, which says that the weighted shell integrals have only subexponential logarithms, is false on the stated shell class. At minimum one needs
\[
 \log \operatorname{vol}(W_\varepsilon)=o(\mu_\varepsilon)
\]
together with boundary regularity and a nondegenerate orientation condition.

### 5. Uniform relative asymptotics cannot hold for arbitrary Borel shells

A pointwise density approximation does not yield a relative coefficient for a set whose Gaussian mass is smaller than the Fourier-inversion error. The theorem allows changing, highly irregular, or zero-volume Borel sets and gives no lower bound on the displayed integral. The \(1+o(1)\) claim therefore has no uniform meaning.

### 6. Existence of the exact finite saddle is not proved globally on the target chart

A positive Hessian gives local injectivity and a local inverse. It does not by itself show that every target in the stated compact subset belongs to the finite-volume mean image. One needs a degree/properness argument and uniform control of the gradient on the boundary of a multiplier domain.

### 7. The prepared lower bound is inherited from the unresolved B2 theorem

The final proof invokes a B2 source-tilted recovery law and a balance-preserving approximation. Those are not established independently. B1 cannot supply the initial prepared LDP until the grand-canonical B2 lower-bound machinery exists.

## A direct consistency point

Keeping
\[
 e^{-\lambda^c\cdot\sqrt\mu z}
\]
inside the shell integral is correct. It also shows why a macroscopic-width shell cannot be summarized by a center value. The paper should retain this correction while imposing a shell regime in which a sharp, uniform integral asymptotic can actually be proved.

## Dependency assessment

B1 is between B2-GC and B2-MC. The source-dependent variational formula is now plausible, but the mixed coefficient remains an independent blocker. B2-MC, B4, C1, and D1 cannot treat the shell transfer as closed.

## Required reconstruction

A valid proof needs:

1. a complex-frequency conditional minorization or another Fourier method for the *full* dynamically tilted hard-sphere law;
2. a quantified finite-volume mean-image theorem;
3. a shell class with subexponential volume and regular boundaries;
4. error bounds relative to the actual weighted Gaussian integral; and
5. a noncircular grand-canonical lower-bound input.

## Recommendation

**Reject.** The corrected saddle formula is important, but the exact coefficient theorem is not proved and is false for shells admitted by its present hypotheses.
