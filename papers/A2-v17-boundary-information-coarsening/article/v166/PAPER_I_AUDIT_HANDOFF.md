# Paper I — independent proof-audit handoff

This is an audit specification, not a completed external audit. No person or service is represented here as having independently certified Paper I. The full proof and all singular-pencil statements are retained in v166. The new boundary constructions are not used to prove the sharp inverse.

## Locked objects and reading order

The complete predecessor is the v164 reconstruction manuscript at the controlling review ancestry. Its SHA256 is `f267fc7ac13451657712d0ca37ee1145e35a2a0950515926772d290ebe86ed6a`. The corresponding master hash is `92d97cc1d0c97ebc324e12717b8c57fd53450bcd225b3d8eac167bda5a91bae2`. The v166 preservation receipt verifies the unchanged theorem/proof blocks, and the compiled theorem index gives the new page locations.

The auditor should read the following dependencies directly from the complete manuscript, not from a build receipt or a response letter.

1. **Exact first relation and its intrinsic extraction.** Check the equality of homogeneous multiplication ideals and the absence of relations below the stated order. For an ungraded finite algebra, verify that the maximal-ideal filtration intrinsically recovers the degree-d multiplication kernel. Nonlinear changes of generators must contribute only above degree d. The local inverse is `thm:artin-local-inverse-v146`; the finite-neighbourhood statement is `thm:sharp-finite-pencil`.

2. **Determinant recognition and matrix factors.** Check how the determinant reduction of the recovered cone determines the unordered matrix tensor factors, and whether all rank and irreducibility hypotheses used there include every singular pencil. This is a geometric recognition step, not a consequence of counting parameters.

3. **Exclusion of transposition and recovery of the left coefficient line.** In the proof of the unmarked local inverse, the support-rank asymmetry `(1,M)` is used to select the correct side. Audit this assertion in exceptional dimensions and for common-factor and singular pencils. Then check exterior duality and recovery of the original pencil orbit.

4. **Sharpness, length, and embedding dimension.** Verify `d=n^2+2n-4`, the embedding dimension `n^2`, the dimension M of the first relation subspace, and the resulting length formula. Check that all smaller-order algebras are independent of the pencil and that the cited inequivalent examples establish uniform minimality, rather than only a generic lower bound.

5. **Families and nonreduced bases.** Audit `thm:finite-parameter-immersion` at the level of equations on Grassmannian charts. The map that tensors a line with a fixed vector space must be a closed immersion and the coefficient inclusion must have the stated rank on every pencil. Verify arbitrary complex base change, not merely injectivity on closed points or tangent spaces.

6. **Effective groupoids and the exact quotient.** Audit `thm:pencil-stack-equivalence`, including the nonlinear tangent-identity kernel, the ineffective right group, the exact group sequence, and fppf stackification. An equivalence on this effective image is not an equivalence with the full raw Artin-algebra deformation stack. Check the tangent complex and stabilizer dimension separately from the set-theoretic inverse.

7. **Applications and dependency direction.** Paper II starts with a source and pencil and proves the fixed-target boundary statements geometrically. The v166 effective horizontal proposition applies the already established inverse afterward. Confirm that no circular use of the boundary theory enters the sharp-inverse proof, and that completed local statements are not advertised as unrestricted global raw-algebra deformation assertions.

## Expected audit output

An independent report should identify exact theorem labels and counterexamples or proof gaps, distinguish pointwise from family statements, and record the field, rank, and singular-pencil scope actually checked. Any correction should be tracked against the locked source. Passing finite symbolic tests, preserving old text, or producing a clean PDF is not an acceptable substitute for this report.

The separate historical comparison with Ballico 1993 also remains incomplete until the legitimate full text is available. This handoff does not certify priority or the editorial standard of a particular journal.
