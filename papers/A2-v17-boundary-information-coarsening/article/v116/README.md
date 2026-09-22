# A2 revision 116 — conductor reduction and primary contact structures

**Manuscript:** *Conductor reduction and primary structures of multiplication failure schemes*.

**Revision branch:** `revision/a2-v116-primary-contact-structure-2026-09-22`.

**Controlling report:** R115, `review/a2-v115-independent-harsh-top4-2026-09-22`, frozen at `1cb4e00c86699247454d21dbec2dcce01a9c6b8b`. The reviewed v115 revision head was `acfd3d57e0053e1b03df53020fd8e79e14599c03`; its mathematical-source commit was `426d112c574f5d3289f6c7d4ecb5f0328ac040b5`.

## Reading copies

- [Geometry article](geometry.pdf), with [LaTeX source](geometry.tex).
- [Complete archival manuscript](paper.pdf), with [LaTeX source](paper.tex).
- [Complete application appendices](applications.pdf), with [LaTeX source](applications.tex).
- [Point-by-point response to R115](RESPONSE_TO_R115.md).
- [Proof audit](PROOF_AUDIT.md), [nearest-source comparison](LITERATURE_AUDIT.md), and [preservation/dependency record](PRESERVATION_AND_DEPENDENCIES.md).

The source and generated reading copies are separate stages of publication. A review should freeze the branch only after the actual PDFs and `evidence/BUILD_RECEIPT.json` are present. That receipt records the mathematical-source commit and hashes the actual PDFs and logs; compilation and finite diagnostics are not proof certification.

## Mathematical changes

The revision pursues R115's Routes A and D through a complete natural family, rather than rebranding the arbitrary-matrix normal form.

For a length-d divisor D, including arbitrary multiplicities, and n >= 2d-1, the inverse-image subseries U of a generating subspace A on D has a multiplication cokernel canonically isomorphic to the finite-contact multiplication cokernel. This is an isomorphism of coherent sheaves on the relative Grassmannian, after arbitrary base change, and transports every Fitting ideal.

For contact pencils, U has codimension d-2. The entire failure scheme is determined in every symmetric degree. Above m >= d-1 its ideal is a power-basis determinant. For D = sum d_i p_i, the exact primary weights are binomial(d_i,2) on ramification divisors and d_i*d_j on pair-identification divisors. All coranks, exact nilpotency indices, successive nilradical quotients, and local weighted-arrangement equations are given. Component descent is determined over every multiplicity stratum.

When D moves without restricting its multiplicities, the total failure divisor is integral. Its normalization is the smooth finite incidence marking a scalar length-two subdivisor. The manuscript supplies an explicit normalization map and a necessary-and-sufficient singular-support test, including contact collisions. A worked example has a smooth total point but a triple nonreduced fixed-divisor fibre.

R115's explicit proof requests for the hyperplane theorem are also addressed: the plane derivative is displayed as a nonzero scalar times diag(m,1,...,1), the residual spans are computed, the confluent length-two Hankel radical is proved, and the equivariant associated-point argument is isolated with exact references.

## Preservation and scope

All 24 immediately reviewed TeX sources are archived byte-for-byte with SHA256 hashes. Seventeen remain byte-identical in active use. All 158 old theorem/lemma/proposition/corollary/proof blocks, 201 labels, and 27 bibliography keys are retained. The original v115 directory and review branch are not edited.

The new contact families are entire generating open relative Grassmannians of subseries containing the conductor W_D. They are not asserted to be the entire unrestricted ambient Grassmannian. The old quadratic excess theorem is not silently promoted to an all-associated-prime theorem; the hyperplane nilpotency bound is not relabelled as its exact primary structure.

The theorem-level comparison with Ballico 1993 remains uncompleted because its theorem pages were not obtained. The accessible Ballico 1996 statements and the Hankel/Fitting/associated-prime sources are compared precisely. Source inaccessibility is not treated as evidence of originality. See `LITERATURE_AUDIT.md` and response items 5 and 14.

## Rebuild

Run `bash build.sh` from this directory or invoke it by absolute path. Python 3 with SymPy, pdfLaTeX with the packages listed in the preambles, and Poppler's `pdfinfo` are required. The build verifies preservation, reruns the inherited v115 finite checks in a temporary copy, runs the new exact diagnostics, compiles all three reading copies, exports cross-references, and generates source-bound receipts. It refuses undefined references, duplicate labels, and overfull or underfull boxes in final logs.

The new diagnostic suite has 272 modular global multiplication/conductor tests, seven symbolic confluent determinant identities, three normalization examples, an exact transverse derivative for the smooth-total/triple-fibre example, and 1,287 colon-exponent tests. These are finite consistency checks supporting reproducibility; the manuscript's universal claims rest on its proofs.
