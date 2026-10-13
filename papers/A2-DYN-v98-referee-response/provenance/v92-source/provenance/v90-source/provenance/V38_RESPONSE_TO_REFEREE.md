# Response to the external referee: A2-DYN revision 38

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v37-external-top4-review-2026-10-08/REFEREE_REPORT.md`.  
**Report commit / blob:** `08562f799dd967056c81324c55ddcd9b91d79c14` / `ddb96a111b7e39ce7f1b2767668fd86fb17d10c9`.  
**Reviewed author baseline:** `d039c92d9f957ee180b74c0f3cf4c8bf52b9547c`.  
**Frozen complete paper tree:** `606e3db1b2e8dce1fbf9f17d3ef7251ec99d519f`.  
**Revised article:** `papers/A2-DYN-v38-referee-response/main.tex`.

We thank the referee for recognizing the exact section multiplier and return disintegration. The present response addresses the v37 report, rather than the earlier v36 submission aliases. We retain the physical family, actual section, four-coordinate return record, title and full raw-density objective. All seventy-nine inherited core files and eighty-seven inherited Python files remain byte-identical. The former main source is preserved under provenance; all its mathematical labels and the compiled A--X synopsis remain.

## 1. Exact return-index inversion: new concentration and fine-window theorems

The new modules 80 and 81 use the fixed occupation neighborhood already present in Proposition `prop:v37-joint-small-frequency`, rather than only evaluating the operator at `theta/sqrt(m)`. They prove the four-dimensional absolute inverse bound on that fixed strip. Positivity and two interval majorants then yield, for each individual actual return index,

`P{K_n=k, N_n=m, T_n-t in J} <= C(1+|J|) m^(-2)`.

This is an all-target, radius-uniform upper bound at the natural four-coordinate scale. It is not yet the Gaussian asymptotic or a positive lower bound for each individual index.

The stronger local conclusion applies to a block of H consecutive actual return indices. It holds for **every diverging H**, with no polynomial lower-growth restriction. Uniformly when H=o(sqrt(m)) and the block center and other coordinates are central,

`m^2/H sum_{n in block} P{K_n=k, N_n=m, T_n-t in J} = c |J| g_Omega(z,y) + o(1)`.

For diffusive and larger widths the theorem retains the exact Gaussian average across the window. This is not inferred from v37 weak convergence. Lemma `lem:v38-moving-envelope` proves a uniform estimate for the changing Fourier tests. The error ledger is

`epsilon_m(B) + C_J/B + C_J/(sigma_B H)`,

where B is fixed first, sigma_B is then fixed within the valid occupation neighborhood, and only then m tends to infinity. The final limit B to infinity is taken afterwards. This permits even arbitrarily slowly diverging integer widths; no growing-band spectral estimate is inserted.

The two-variable lower envelope is `q^- p^+ + q^+ p^- - q^+ p^+`. The direct product of two minorants would be invalid because both can be negative. The proof includes the pointwise inequality and the precise Fourier normalization.

Theorem 4 states the new results at the front of the article. Corollary `cor:v38-return-normalization` returns the limiting amplitude to the original D_R normalization. It introduces no new covariance, record, return section or conditioning event.

For a single index, Proposition `prop:v38-exact-index-remainder` gives a new exact inverse identity with its proved Gaussian contribution and an explicit signed remainder on the fixed occupation torus outside the controlled strip. For each fixed band-limited roof test, cancellation of this remainder is equivalent to the desired single-index local asymptotic. Corollary `cor:v38-single-index-criterion` specifies sufficient cancellation for sharp roof intervals. **That cancellation is not proved here.** The fixed-strip theorem resolves all diverging widths, but does not authorize setting H=1 in the asymptotic. Its surviving `1/(sigma_B H)` error is displayed rather than concealed.

## 2. Pointwise roof inversion

The original common pointwise correction, full return-frequency complement and pointwise roof-density inversion are retained, not replaced by an interval topology. The new single-index upper bound has `1+|J|`, not a coefficient proportional to |J| at arbitrarily small lengths, so it cannot be used as a density bound by division by |J|. The exact fixed-roof-band remainder does not estimate the far roof frequencies or the extracted critical/singular branch sum. These remain active requirements of the unchanged raw theorem.

## 3. Principal endpoint and manuscript architecture

The four leading theorems distinguish the stationary physical law, compact-family action principle, inherited diffusive return-window law, and new single-index concentration/fine-window law. Each is stated with its actual topology. The short Part II route now points directly to modules 77, 78, 80 and 81. The full original return analysis remains compiled; no valid mathematics is removed or assigned a different topic. The manuscript does not describe a window limit as a singleton Gaussian limit or as the full raw-density theorem.

## 4. Independent specialist verification

An independent human billiards/anisotropic-spaces audit has not been obtained in this author revision. The unchanged continuum input chain still requires that audit. `SPECIALIST_AUDIT_MAP.md` preserves its scope and adds the finite-strip, moving-envelope, product-lower-bound and exact torus-inverse steps. The new proofs do not assert a full occupation-torus Lasota--Yorke estimate, a new singularity partition, or new regularity of a peripheral vector. Their dynamical inputs are the source-pinned v37 results, not the success of the finite checks.

## 5. Theorem-level comparison

The one-dimensional Beurling--Selberg construction is the inherited classical input, with the existing CVExt citation retained. Analytic perturbation and partial Fourier inversion are not claimed as new. The advance over the reviewed article is a uniform four-dimensional local concentration estimate and a moving-test argument valid down to every diverging return-index width. A fixed diffusive-window weak limit does not provide such moving-window control. The exact original-return amplitude and terminal exclusion are maintained through disintegration. The statement is not represented as a universal new local-limit theorem or as proof of historical priority.

## 6. Scope and generality

The fixed-strip deduction uses positivity, a uniformly nondegenerate joint expansion, a compact complement estimate on a sufficiently small occupation strip, and uniform endpoint norms. It does not use special new circle or ellipse geometry after those inputs. The physical verification in this article is for the same genuine circular return section as v37. The inherited ellipse and nonelliptic support-function applications remain in the paper. We do not declare the specific return-section theorem verified for a new independent system without checking its section multiplier and covariance.

## 7. Scope distinctions and event identity

The new selected statement is for nonnegative multiplier-bounded endpoint factors, evaluated at the actual initial state and actual terminal return. A selected lower bound requires a positive product of section means. No arbitrary path-selector Gaussian amplitude is inferred. Neither a physical fixed-count theorem nor a posterior total-variation comparison is substituted for the raw return-density theorem. The actual occupation remains the sum over [0,m), and the half-integer boundaries select exactly H consecutive integers.

## 8. Version identity and reproducibility

The two v38 branches start from the controlling v37 review commit and receive the same theorem-bearing author commit. The active directory, complete ordinary-source Merkle manifest, workflow and copy ref identify that new source. The verifier checks all 81 core inclusions, every inherited core/script byte, all inherited labels, the bibliography and A--X appendix, the archived previous main source, the exact report blob and the workflow hash. Normal and optimized diagnostics must agree. Native typesetting rejects warnings, undefined references, missing glyphs and overfull boxes; page renders are selected from the actual theorem labels.

No new workflow is predeclared successful in this response. The dynamic receipt and the actual completed GitHub run are the execution evidence. Source qualification, finite regression models, mathematical proofs in the article, and independent specialist validation remain distinct.
