# R79 publication consistency audit

## Scope and result

This is a final internal author-side consistency check of the assembled publication packet for **General Theta Foundations I**. It is not a new independent referee report, mathematical proof verification, visual reinspection, human expert assessment, or editorial decision. The complete mathematical build was not rerun. No sealed source file or assembled publication file was modified during this check.

**Result: no blocking publication inconsistency found.** The publication integrity verifier completed successfully; source identities, PDF identities, finite-diagnostic totals, statement counts, inheritance/newness wording, visual coverage, local-versus-hosted execution claims, and relative navigation agree at the inspected identities. One small nonblocking evidence-packaging improvement was identified in Section 7 and subsequently completed as recorded in Section 8: preserve the first baseline attempt's underlying diagnostic stderr, in addition to its already deposited failure receipt and outer traceback.

The inspected directory is `papers/General-Theta-Foundations-I-restart/r79-robust-instrument-frontier-publication`. The controlling source commit is **`90cae2f5aca243b39d3a2194a4d6e0696671a101`**. The final identity read for this snapshot was at **2026-10-23 07:47:11 UTC**. The subsequently containing publication commit and its remote readback are separate evidence; this prepublication audit does not claim that a future commit or push has already occurred.

## 1. Inspected controlling files

| File | SHA-256 at the audited snapshot |
|---|---|
| `README.md` | `d658682eab2ab39935fc84aee79e840f5028af295b4def07e29ad13f73a9c547` |
| `PUBLICATION_RECEIPT.json` | `c79f7bc84a8734e1e75d5bc746bd15bb687dfcc33e5642da2d2a09aefddfae74` |
| `BUILD_RECEIPT.json` | `038fd8a00f85f6fa2339a8e9527628563d8d6bde19808a9d9f4e52c953584ba0` |
| `VISUAL_QA.md` | `0aeec4368f955cd09faa50089c7e2c1ae4a6a017a49bdfe8b8d264a8e975ab68` |
| `VALIDATION_CONTENTS.json` | `a76ca0180a0a8ed006a724da432c5349fa13193be363489e321783204b1375dd` |
| `verify_publication.py` | `86f6ece8eb5158c7387a5681a95b279d28455ee2fee5017882f521b40d2e4010` |

The associated source remote readback, prepublication ref comparison, theorem-map check, historical-census receipts, three visual scope notes, render receipt, and relevant archived raw outputs were inspected as supporting evidence. Their inspection was read-only.

## 2. Source and publication identities

The README, publication receipt, strict build receipt, source remote readback, archive manifest, and render receipt consistently identify source commit `90cae2f5aca243b39d3a2194a4d6e0696671a101`. The actual local Git commit object independently confirms its repository root tree `b16569cd3e017713f1c4b62171db46ff6cd1d095` and its R78 parent `e0377beea364e456af2301f5e4fec98fe343cbcb`. Resolving the committed paper subtree yields `582c4a664cb571c63927940ab7ef08be869cf10b`, as recorded in the receipts. Hashing the actual source manifest gives `e603a906514127a45525deef79fc4462d74d7784e57d5f6da0b6af108a3fd1a6`, also matching the packet.

The completed strict receipt records 806 verified source files, the same before/after source tree, unchanged source during execution, and execution after creation of the source commit. Its document and preservation records are identical to the corresponding publication-receipt fields. The source commit's own message correctly defers native execution and PDF publication to a later child commit.

The publication receipt deliberately does not self-embed its future commit SHA. That is appropriate: its containing Git commit and actual remote readback must supply publication identity. The README's description of a later child publication is consistent with the intended assembly sequence, but the final child/remote identity remains a post-assembly check. The current integrity verifier is a receipt-relative content check; the containing Git object supplies the external identity of the receipt itself.

The remote source readback explicitly records an unsigned commit and does not equate content authentication with a cryptographic author signature. The frozen-head comparison records 1,307 original heads unchanged and one new source branch, for 1,308 current heads, at its stated snapshot time. It is not represented as a permanent assertion about all future remote refs.

## 3. Actual integrity execution and raw diagnostic recount

The following command was actually executed from the publication directory:

```text
python3 -B verify_publication.py
```

It exited successfully with `FILE_INTEGRITY_PASS`, checking **21 listed publication files** and **159 archived files**. The verifier checks exact publication inventory, file lengths and SHA-256 hashes, source-commit agreement, required strict-run invariants, PDF identities, archive identity, safe regular archive members, absence of duplicate/unlisted entries, and every archived file hash. It does not run TeX, rerun diagnostic suites, reprove theorems, or query hosted CI. The receipt itself is excluded from its own artifact list to avoid a self-hash cycle; its identity belongs to Git and the table above.

The archived ordinary and optimized JSON outputs were read and compared directly. All **29 pairs are byte-identical**, every ordinary output matches the hash and parsed report in the strict receipt, and each suite's exact/floating counts sum to its total. Recounting once per pair gives:

| Quantity | Recounted value |
|---|---:|
| Diagnostic suites | 29 |
| Byte-identical ordinary/optimized pairs | 29 |
| Exact finite checks | 369,145 |
| Floating finite checks | 12,033 |
| Total finite checks, counted once per suite | 381,178 |
| New `r79-examples` exact checks | 6,740 |
| New `r79-reachable` exact checks | 875 |
| Combined new exact checks | 7,615 |

The older successful R78 receipt reports 373,563 checks; adding 7,615 yields 381,178. The README explicitly states that ordinary/optimized execution is not counted twice.

Four inherited raw reports use the status spelling `passed` rather than `PASS`. The source verifier explicitly accepts both spellings after case normalization, and the build receipt consistently normalizes the suite-level result. These are successful legacy reports, not concealed failures. Their raw outputs remain unchanged in the archive.

The archived current strict `BUILD_RECEIPT.json` is byte-identical to the separately deposited build receipt. The three archived PDF text-extraction files match the text hashes recorded for their documents. The final main, supplement, and companion TeX logs contain no lines reporting overfull boxes, undefined references/citations, multiply defined labels, or duplicate destinations in the checked warning categories. The nine compiler-pass outputs are retained separately from the final logs. These observations confirm the deposited execution evidence; they do not constitute a new build.

## 4. Counts, preservation, and mathematical-attribution wording

The three PDF page counts agree across the README and document receipts: **59 main + 190 supplement + 37 companion = 286 pages**. Their byte identities were authenticated by the publication verifier and agree with the render/visual records.

The statement count is **252 = 240 inherited + 12 additionally indexed statements**. The README expressly says that the twelve include restatements and supporting examples and are not twelve novel theorems. This is consistent with the theorem-map receipt and the source's internal-priority correction.

The preservation summary agrees between build and publication receipts: all **694 predecessor files** are retained, consisting of **628 at the same relative paths + 66 explicitly archived**. Seventy protected mathematical body files, the inherited supplement suffix, and all 34 companion files retain their separate byte-preservation claims. The historical receipts consistently give **7,201 combined text blobs**, **112,371,368 authenticated uncompressed bytes**, **873 distinct head commit payloads**, and the frozen **1,307-head census**. This audit cross-checked those recorded quantities; it did not rerun the complete historical-corpus authentication.

The README identifies same-label regularization and uniform-in-memory primitive stability as the central additional argument. It states the fixed-model, all-initial-state, cost-bound, model-pairing, and small-error requirements. It distinguishes the positive-success Lipschitz corollary from the general support-degenerate modulus and explicitly limits the scalar sharpness assertion. The golden-ratio frontier is presented as an exact special model, with its counted pure initializer and stochastic-update converse, rather than a universal resource law.

The support, cost-potential, dark-subspace, finite-model synthesis, and related verification ingredients are credited as inherited or classical. Nonreset feedback alone is not claimed as new. The four-journal aim and the original scientific identity remain intact, while independent A1/A2 and the larger Theta programme are not declared complete. No inconsistency was found in this attribution wording.

The controlling R65 report is described as applicable but already substantively answered in R66–R78, and as not assessing R79. The absence of a later report is tied to the scoped census and content audit, not merely a version number or branch label. No new independent human endorsement is invented.

## 5. Visual-inspection coverage and its limits

The visual summary agrees with the three author-production scope notes and the render receipt. Recorded thumbnail coverage is all 59 main pages, all 190 supplement pages, and all 37 companion pages. Recorded readable-page inspection covers **18 main + 6 supplement + 4 companion = 28 pages**, including every main page from 9 through 20 in the new proof sequence.

The render receipt contains 42 PNG identities: 13 contact sheets and 29 individual page renders. Main page 24 was rendered but was not recorded as viewed. `VISUAL_QA.md` explicitly excludes that extra render from the inspected-page count. Thus 29 generated individual images are not misreported as 29 inspected pages.

The PNG working files are not deposited, and the summary says so. The exact PDF identities, original render script, render receipt, and scope notes are deposited. The script's original local B/O paths are explained, with the change needed to reproduce rendering from the publication directory; byte-identical PNG output on a different software stack is not promised.

The claims are limited to actual prior author-side image inspection at the stated scales. This consistency audit did not reopen the images. Neither the visual summary nor this audit claims that every glyph was read at detail scale, or that clickable PDF links, accessibility, print output, mathematical correctness, priority, or external expert approval were verified.

## 6. Navigation, evidence categories, and reproduction

All **26 Markdown relative links** found in the assembled publication Markdown files resolve to existing targets. This includes the three PDFs, publication records, visual scope records, and sibling source guides, response, priority/proof/dependency maps, and preservation records. The check is filesystem target resolution; it is not a test of every PDF hyperlink or a new request to every external website.

The README correctly instructs a full mathematical reproduction to check out the exact source commit and use a fresh external output directory. It explicitly warns that the source-only strict diff gate should not be run at the later publication HEAD and mislabeled as the source build. The simpler publication verifier is accurately described as a file-integrity check.

The source-specific GitHub Actions readback records zero runs. The packet therefore claims the completed strict local build and does not claim successful hosted CI. It separately identifies ordinary written proofs, finite exact/floating diagnostics, source authentication, native compilation, visual production checks, unexecuted general quantifier elimination, absent proof-assistant certification, absent new independent human refereeing, and absent editorial decision. The remote push is not inferred from local assembly. These boundaries are consistent throughout the inspected files.

## 7. Nonblocking raw-failure packaging observation

At this snapshot the validation archive separates its contents into **2 first-baseline-attempt files**, **1 subsequent successful-baseline receipt**, and **156 current strict-build files**. The first attempt is explicitly `FAILED`, the later R78 baseline is explicitly strict `PASS`, and the current R79 execution has its own strict `PASS` receipt. No failed or earlier execution is substituted for the current run.

The first-attempt archive contains `BUILD_FAILURE.json` and the outer `process.stdout.txt` traceback. That traceback points to the underlying diagnostic stderr but does not itself display the missing package. The original local file still exists at:

`/workspace/scratch/b8655e579b01/r78_baseline_build/r61-normal.stderr.txt`

It was read during this consistency check and ends with:

```text
ModuleNotFoundError: No module named 'sympy'
```

**Recommended small packaging improvement before final sealing:** include that original stderr under `baseline-first-attempt/`, then regenerate the archive hash, member manifest, publication receipt, and integrity result. This would make the README's stated missing-dependency cause independently recoverable from the deposited packet. It requires no source change and no mathematical rebuild. The absence of that one inner stderr at the inspected snapshot does not invalidate the separately authenticated successful strict run, the diagnostic totals, the PDFs, or the preservation evidence.

If this audit note is itself added to the publication, its artifact inventory and integrity-check count must likewise be regenerated. The exact 21-file/159-member result and hashes above identify the packet actually inspected here, not a subsequently enlarged packet. The final containing Git commit and remote readback should identify whichever complete packet is ultimately deposited.

## 8. Packaging follow-up: missing-dependency trace deposited

Before this audit note was finalized, the author added the original 263-byte `baseline-first-attempt/r61-normal.stderr.txt` and its original zero-byte `baseline-first-attempt/r61-normal.json` stdout to the archive. A read-only inspection of the updated archive confirms **161 members**, **596,764 bytes**, and SHA-256 **`530dfa27e6357df7759be2850f8a586474c7ae32d0200c66ad039e1accf37535`**. The archived stderr contains the actual `ModuleNotFoundError` for `sympy` quoted above. The packaging observation is therefore resolved.

The original **21-file/159-member** full integrity result in Section 3 explicitly predates these two raw-evidence additions. This follow-up authenticated the updated archive and the added contents only. The author will regenerate the publication artifact inventory after adding this audit note and run the final publication integrity check against that complete final packet; its actual final file/member counts belong to that execution record. No mathematical source was changed, and no mathematical rebuild was performed or required by this evidence-only addition.
