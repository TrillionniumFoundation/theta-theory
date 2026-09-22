# Literature and priority audit — A2 v119

Audit date: September 22, 2026. The inherited v118 audit is preserved under `inherited-v118/LITERATURE_AUDIT.md`. This file records the additional comparison and the unresolved item; it is not an exhaustive priority certificate.

## 1. E118.1: Ballico 1993 — still open

E. Ballico, *On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces*, Mathematische Nachrichten 163 (1993), 5–13, DOI 10.1002/mana.19931630102.

The publisher's volume-163 table of contents was consulted and confirms the title, author, year and pages. The enabled public full-text route did not provide the article. The DOI PDF route was inaccessible; exact-title and DOI searches did not supply complete theorem text. The manuscript does not infer absence of overlap from this limitation.

Primary record consulted: `https://onlinelibrary.wiley.com/toc/15222616/1993/163/1`.
Attempted full-text route: `https://onlinelibrary.wiley.com/doi/pdf/10.1002/mana.19931630102`.

| Comparison requested by R118 | Evidence actually available | Status |
|---|---|---|
| Failure loci versus Fitting schemes | Bibliographic record only | Theorem-level comparison not completed |
| Fixed versus moving finite contacts | Bibliographic record only | Not completed |
| Higher-order multiplication or osculating failure | Title is not sufficient evidence | Not completed |
| Conductor transport | No theorem text | Not completed |
| Quotient/Hilbert incidences | No theorem text | Not completed |
| Nonreduced scheme structure | No theorem text | Not completed |

A future comparison must use the complete source, identify its exact hypotheses and conclusions, and compare each relevant theorem with the new statements. No row is marked closed on the basis of a title, abstract or inaccessible link.

## 2. Additional primary source actually read: Sidman's regularity paper

J. Sidman, *On the Castelnuovo–Mumford regularity of products of ideal sheaves*, arXiv:math/0110184v2 (2001).

Source: `https://arxiv.org/pdf/math/0110184`.
The parsed full text was available. The web PDF screenshot endpoint failed with a cache-miss response; no successful screenshot is claimed. Theorem statements and the relevant proof paragraphs were read in the text layer.

**Theorem 1.3:** the regularity condition relates the graded ideal to its saturation in degrees at least its regularity, and gives the cohomology vanishing in the corresponding range. This supports both the sheaf-section/ordinary-square distinction and the first-conormal-layer surjection in the new conductor proof.

**Theorem 1.8:** if the projective schemes defined by homogeneous ideals I and J intersect in a finite set of points, reg(IJ) <= reg(I)+reg(J). Applying it to I=J for a zero-dimensional scheme gives reg(I^2) <= 2 reg(I). Its proof specifically addresses saturation of the ordinary product, not just regularity of the product sheaf.

The paragraph following Theorem 1.8 attributes earlier power bounds to Chandler and independently to Geramita–Gimigliano–Pitteloud, and mentions related work of Conca–Herzog. Those historical statements are attributed to Sidman's discussion; the present session does not claim a fresh theorem-by-theorem reading of every one of those sources.

**What is not claimed:** the regularity inequality, the saturation criterion, or the classical cohomology-and-base-change formalism as new results.

**What the revision proves separately:** the kernel equality for each prescribed inverse-image linear series; the canonical global/finite multiplication-cokernel comparison; its relative extension; and its application to the full embedded Fitting family. No theorem-level non-overlap with Ballico 1993 follows from Sidman's article.

## 3. The finite-algebra comparison retained and sharpened

The inherited comparison with Arpin–Bozlee–Herr–Smith, Iovanov–Sistko, Sistko, GLTU, Grinberg and Haiman remains in the manuscript. The new section explicitly separates:

- classical generator/polygenerator minors from the codimension-sensitive ring-level stabilization proof and the specified full codimension-two presentation;
- the classical rank-three algebra/binary-cubic square calculation from its role as an exceptional conductor-incidence fibre;
- the classical two-row Schur basis and contact algebra G_h from the mixed embedded ideal `(F_h,vF_(h-1),bv,b^2u)` and its realization on the full multigenerator failure scheme;
- the representability of Hilbert/Grassmann functors from the proven isomorphism of the corank-one multiplication scheme with their quadratic-generation incidence.

These distinctions explain the logical inputs and the additional assertions. They do not assert exhaustive originality of a codimension bound or of every incidence construction against all existing literature.

## 4. Mathematical scope is not an editorial or priority judgment

The new text supplies full proofs and specifies parameter spaces. It does not claim that all higher-defect primary strata are classified, that a proper incidence is automatically a normalization, or that primary decompositions commute with arbitrary specialization. New results should be judged on those statements and proofs, not on the successful build, diagnostic counts, branch names, or an asserted likelihood of acceptance.
