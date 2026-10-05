# A2-DYN v6: fixed sources, literature import and validation

## Controlling review and manuscript

The latest located A2-DYN external report is `reviews/a2-dyn-v4-external-top4-review-2026-10-05/REFEREE_REPORT.md`, blob `1af8fb198d0361782cdca21f1d91a81d48ec1300`, at review head `a81eb226c013ca062a6901bb472a90668de29eec`. The complete report, its source audit and literature audit were read. The review branch tree is `8d0d6e95d93c26cf227d92e093191b1351483abb`.

The reviewed author SHA is `f0c2f6c9044a9e76e487329dbf7791f865ee7b8c`; its active core tree is `37509bf72fe8b9e28a7831b2b87fb56a5cff9913`. The latest v5-named remote branch was an exact alias of this v4 source. The earlier mathematical checkpoint is `12a7c04eaf9754de356a69dfc1ec4ae09ba605b8`. The dynamics lineage includes v3 at `55ab80ed1a4f11b58ce9a88c365b0cea2e2ce191` and v1 at `36f1365041de95ca478739a1e2984734c72f95aa`.

The A2-GEOM v43 baseline `4557df22f5c72bc80943690ecd6c2e39de3734ab` remains separate. Its review is not used as an A2-DYN acceptance or proof assessment.

## Recovered unpublished v5 source

The accessible Library artifact `A2-DYN-v5-delivery.zip` supplied the derivation at `papers/A2-DYN-v5-periodic-coercivity/`. It was not assumed to be a remote revision merely because its filename says v5. The inherited mathematical files were compared with the actual v4 Git blobs. The complete new periodic-coercivity source was reread, its proofs checked author-side and its finite diagnostic rerun.

The recovered `core/14_periodic_coercivity.tex` has Git blob `78732b7d250de8a97389e1016a61f1b8e5d2054c` and is retained exactly in the new article. Its eight proofs are distinguished from the 37 reviewed proofs and the 13 new v6 proofs. The active reviewed introduction and all twelve retained files are byte-matched by `tools/audit_source.py`.

## Primary literature checked for the new import

Demers–Zhang, *A functional analytic approach to perturbations of the Lorentz gas*, CMP 324 (2013), 767–830, arXiv:1210.1261, DOI 10.1007/s00220-013-1820-0, was checked at the theorem level: Section 3.3 for the spaces; Theorem 2.1(3) for the complementary power bound; Theorems 2.2, 2.5 and 2.6 for the unforced spectral and geometric perturbation setting; and Remark 2.7(b) for changes of boundary length. The latter theorem page was also inspected visually. The underlying collision spectral source is Demers–Zhang, J. Mod. Dyn. 5 (2011), 665–709, DOI 10.3934/jmd.2011.5.665.

Lemma 14.1 verifies the geometry and coordinates rather than silently changing the reflection law: a common boundary parametrization, positive separation, bounded curvature/C3 norms, uniform horizon and, when needed, a rectangular two-scatterer cover. Its smooth-multiplier estimate is proved from the test-curve norms. Proposition 14.2 derives the needed uniform tilted estimate; the local large-deviation theorem is not applied outside its stated deviation range.

The Szász–Varjú displacement LLT and Dolgopyat–Nándori suspension LCLT remain comparison results, not substitutes for the present raw density. General Livsic regularity is not imported without checking its hypotheses. This audit makes no exhaustive literature-priority claim.

## New source identity and validation scope

Mathematical checkpoint: `65551575d46469c3b47c7bf53ff63d787be02085`. New core tree: `4a5568bd65a67bf1fcdebf33bba37d5cea83fb18`. This tree was computed from local Git object encodings and matched the successful GitHub tree write. The main source blob is `66ceeb2d0e43088267e07f15031a5c14ad92f780`. The tools tree is `5de90eb3373cd643d5e56848855a503d4d519a98`, likewise matched independently.

The local native build passed with 44 pages, 58 active proof bodies, 173 labels and no final TeX warnings, unresolved references, overfull or underfull boxes. All pages were rendered and visually inspected. The actual TeX recorder input set matched the audited 21 mathematical inputs. The local PDF SHA-256 is `ab36fd163a20d292fdd1e5cc14f1c03a6731d21ea2238685a38dc6b463c0b8b8`; later builds may differ in PDF metadata, so source hashes and event SHA are recorded separately.

Normal and optimized executions agreed for the source audit and all six diagnostic scripts. The new v6 finite suite records 962 checks. The recovered v5 suite uses 90 decimal digits for 30 sampled minima, 24 adjacent comparisons and 18 frequency selections. The retained v1/v2 suites and winding/excursion certificates were also rerun. These computations do not prove a continuum spectral theorem, a global raw LLT, or the result of an independent human review.

All new manuscript and support files are confined to `papers/A2-DYN-v6-referee-response/`, with one dedicated qualification workflow. Old source, old reports, other papers and the main branch are unchanged. The build receipt records whether it came from a clean exact event checkout; local qualification is not represented as a GitHub Actions result. The final remote run must be checked at its actual head SHA.
