# General Theta Foundations I — Revision 33

**Compatible Polyhedral Lifts and Quantitative Causal Width**  
Qian Qi · 25 September 2026

Controlling r17 report: `eaa2661530ed473f8b79407eba7a1182c8e0a450`. Reviewed v32 publication: `d38fca741135d147dfdbdbd99cfd9a1a716a88a5`. Native v32 source: `4ccfe985f0507154969b4405e94b99a2c8a451f3`.

Work branch: `revision/general-theta-foundations-i-v33-compatible-lifts-2026-09-25`. The publication workflow creates the separate referee-ready branch only after a successful build. The work branch was created remotely from the review before manuscript publication. No old paper, report, pipeline file or other branch is overwritten.

[English article](paper.pdf) · [Native LaTeX](main.tex) · [Response to r17](RESPONSE_TO_REFEREE.md) · [Small referee package](evidence/REFEREE_PACKAGE.zip) · [Core sources](evidence/CORE_SOURCES.zip) · [Executed build receipt](evidence/BUILD_RECEIPT.json) · [Theorem locations](evidence/THEOREM_LOCATIONS.json)

## Principal results

The paper distinguishes three tasks, not three names for one task. W_N is unrestricted clocked hidden-state width. V_N imposes a predictive vector at each state with a statewise stochastic intertwining identity. A_N is total state count for a clock-free device with one fixed decoder answering a terminating query at every length 0 through N.

For the golden-angle experiment, every hidden-state profile satisfies

```
sum_(t<N) 2^(-3 K_t) <= 320,
max(3, log2(N/320)/3) <= W_N <= V_N <= q_N,
```

where q_N is the first Fibonacci convergent denominator at least max(5,(40N)^(1/3)). For every bounded-type irrational angle, V_N is Theta_alpha(N^(1/3)), with a lower bound against every time-varying vector-state chain and a matching exact resonant-polygon construction. The unrestricted hidden problem still has a logarithmic lower and cube-root upper bound. The subclass theorem is not substituted for the general problem.

Mean support, rather than area, supplies the improved cumulative potential. A convergent with denominator q>=8M gives a one-step gain at least 3a/(4 M^2 q). The exact upper machine exploits a residual rotation angle of order q^(-2), so its radial expansion has logarithm at most 40/q^3. Its command rows may be stationary, but its decoder is horizon-specific.

Every bounded f-facet extension has a normalized f-coordinate simplex-section representation. An affine map positive on that section need not extend to a stochastic map on the ambient simplex. The paper gives the exact linear dual for this extension requirement, an explicit example of optimal uniform extension error 1/4, and an operational equivalence between compatible stochastic lifts and the full hidden-state profile problem. It does not infer that every logarithmic regular-polygon lift works or fails.

For the rational rotation (3+4i)/5, the explicit all-hidden-state bound is

```
N <= 140*2^(2W_N)*5^(8*2^W_N).
```

This is weaker than the bounded-type bound but requires no unproved Diophantine assumption or numerical quantifier elimination. Under the stronger anytime fixed-decoder specification, every infinite-order rotation has N+1 <= A_N <= 3(N+1)+2. Strictly contractive rotations instead admit a fixed finite polygon device, with an explicit bounded-type upper estimate.

Benvenuti–Farina's 1999 fixed-degree/unbounded-order result, their 2003 positive-Hankel/intertwining comparison, Yannakakis, Fiorini–Rothvoss–Tiwary and Vandaele–Gillis–Glineur are discussed explicitly. Static lifts, positive rank and dynamical compatibility are not claimed as new concepts. The inspected original and secondary-to-original author texts are recorded in `LITERATURE_AUDIT.md`; exhaustive independent priority clearance is not claimed.

## Reproduction and preservation

Use Python 3.11+, SymPy 1.14.0 (including mpmath), PyMuPDF 1.26.7, and a TeX installation supplying AMS, Latin Modern, geometry, microtype, booktabs, mathtools, needspace and hyperref.

```sh
python papers/GTF-I-v33-compatible-lifts/verify.py
python -O papers/GTF-I-v33-compatible-lifts/verify.py
python papers/GTF-I-v33-compatible-lifts/build.py
```

The small core archive is independent of the historical volumes: extract it and run `python GTF-I-v33-compatible-lifts/build.py --core-only` from its parent directory. The full source archive has sibling predecessor directories for historical regression and preservation checks. No standalone font files are distributed.

The entire v32 article is copied unchanged to `supporting-results.pdf`. Its cumulative mathematical and development volumes are preserved after the full current article and a divider. Original repository paths remain unchanged. The small referee package excludes these large archives.

The build separates exact rational/algebraic checks from 80-digit floating diagnostics of the explicit polygon rows. Neither is a proof of the continuum bounds. It also runs inherited v24–v32 regressions in normal and optimized Python, new negative controls, three TeX passes and predecessor checks. The actual receipt, not this description, records execution. Atomic irrational rows, program tables, fixed-length queries and the stronger anytime task remain explicit resource distinctions.
