# Literature and theorem audit — Revision 34

This is a targeted primary-source comparison, not an exhaustive independent originality certificate. External papers are cited rather than redistributed. Internal revision manuscripts provide provenance and inherited constructions, not external validation.

## Blackwell comparison and deficiency

**Blackwell (1953), Equivalent Comparisons of Experiments**, Annals of Mathematical Statistics 24, 265–272, DOI 10.1214/aoms/1177729032. The publisher record was checked; the original full-text endpoint was not available as readable text in this session. The finite relation F=ET with row-stochastic T is expressly attributed as Blackwell garbling. It is proved internally with the decision support function, not treated as a new dual.

**Torgersen (1991), Comparison of Statistical Experiments**, Cambridge University Press, Encyclopedia of Mathematics and its Applications 36. Publisher bibliographic data were checked; the whole monograph was not obtained or claimed read. The manuscript fixes one-sided deficiency as min_T max_h TV((ET)_h,F_h), with TV one half of l1. Its finite dual and triangle inequality are proved in full.

**Fritz–Gonda–Perrone–Rischel (2023)**, Representable Markov Categories and Comparison of Statistical Experiments in Categorical Probability, Theoretical Computer Science 961, 113896; arXiv:2010.07416v3. The primary abstract and stated Blackwell–Sherman–Stein lineage were inspected. This is cited as a modern formulation, not a claim that the categorical theorem is newly established here.

**Jencova, arXiv:1512.07016v2**, Comparison of quantum channels and statistical experiments. The classical randomization criterion in its Section 3/Theorem 3 was inspected as a primary-source confirmation of the total-variation normalization. Its quantum extensions are not used by the manuscript's classical proof.

The manuscript's new use is not a novel one-step ordering. It constructs a common-row finite diagram, proves executable error composition, then obtains a lower bound on the total defect of every small diagram of the same rotation experiment from the new hidden-state theorem. Cancellation of intermediate errors is not excluded; the sum is not identified with optimal final error.

## Symmetric and equivariant lifts

**Gouveia–Parrilo–Thomas (2013)**, Lifts of Convex Sets and Cone Factorizations, Mathematics of Operations Research 38, 248–264, DOI 10.1287/moor.1120.0575. Relevant full primary preprint: https://optimization-online.org/wp-content/uploads/2011/11/3249.pdf . Definitions 2.7–2.8 and Theorem 2.9 in that version define symmetric lifts/factorizations and prove their correspondence. The theorem numbers are version-specific, not attached without checking to a different edition. The objects are one convex body, one cone lift and a compatible group homomorphism, unlike a chain of noninvertible stochastic maps between changing sections.

**Fawzi–Saunderson–Parrilo (2017)**, Equivariant Semidefinite Lifts of Regular Polygons, Mathematics of Operations Research 42, 472–494, DOI 10.1287/moor.2016.0813; full arXiv:1409.4379 inspected, particularly the introduction, definitions, table on page 4 and Appendix B. The regular prime-power polygon equivariant-LP lower bound is linear; nonsymmetric LP lifts can be logarithmic; equivariant PSD lifts of regular 2^n-gons have logarithmic constructions. This is not imported as a lower bound for arbitrary time-dependent stochastic diagrams. The paper's permutation action and affine-slice invariance are explicitly contrasted with the present maps.

**Kaibel–Pashkovich–Theis (2012)**, Symmetry Matters for Sizes of Extended Formulations, SIAM Journal on Discrete Mathematics 26, 1361–1382, DOI 10.1137/110839813; arXiv:0911.3712. The primary bibliographic/abstract statement was checked. Its broader symmetry-size phenomenon is cited; no uninspected theorem number is assigned and it is not misidentified as the source of the exact regular-polygon theorem.

Static slack-factorization and regular-polygon extension results of Fiorini–Rothvoss–Tiwary and Vandaele–Gillis–Glineur remain inherited background, with their v33 audit preserved. The present session does not claim to repeat an exhaustive audit of every original source. A small static extension is not enough: a valid initialization, all common stochastic update maps and a bounded decoder are required.

## Positive realization and the finite-time distinction

Benvenuti–Farina, Heller, Vidyasagar and Monras–Winter remain credited for classical positive realization, invariant sets, accessible quotients and spectral obstructions. The inherited v33 audit records the primary portions inspected in that revision. These stationary mechanisms are not claimed as new. The v34 main proof uses no assumption that one stochastic matrix is repeated and no assertion that every hidden basis state has an observable predictive vector.

**Lumbreras–Ma–Thompson–Gu (2026)**, An Irreducible Quantum Advantage in Aligning World Models with Reality, arXiv:2608.19779, submitted 20 August 2026. The full primary PDF was accessed, and Section IV.B (page 8) and the model-definition context were inspected directly. Its stationary Wait–Tick argument explicitly uses the same classical update and peripheral limiting behavior, and then connects that mismatch to decision errors. The present theorem permits arbitrary epoch-dependent matrices and horizon-dependent machines, needs only a final correlation, and gives an explicit finite polynomial bound. No quantum advantage theorem is inferred here.

## Proof ingredients versus asserted contribution

Conditional expectation, Jensen loss, Fourier moments, Fejer positivity, finite convex minimax, TV contraction, continued-fraction approximation and stochastic peripheral spectra are standard mathematical tools. Their short needed forms are proved in the article. The proposed contribution is the common-amplitude harmonic error budget and its finite-hidden-atom use to yield an occupation bound for arbitrary stochastic updates. It produces the bounded-type N^(1/5) lower bound, rational logarithmic lower bound and main-family total-diagram-defect obstruction.

The exact resonant cube-root construction, separate minimum three and anytime spectral comparison are inherited and labelled accordingly. The leading hidden exponent remains unmatched. No complete source survey can be inferred from a bibliography or successful finite tests; mathematical originality and correctness remain open to independent scrutiny.
