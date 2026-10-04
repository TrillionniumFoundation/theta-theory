from pathlib import Path
import json
REPO=Path(__file__).resolve().parents[1]
P=REPO/'papers/GTF-I-v78-block-resource-learning';R=REPO/'papers/GTF-I-v79-joint-interior-coding'
(R/'README.md').write_text('''# General Theta Foundations I — Revision 79

Further response to R51, based on the completed v78 source. The focused entry is `quantitative.tex` / `paper.pdf`; `main.tex` / `COMPLETE_REVISION.pdf` preserves the complete mathematical development; `structural.tex` / `STRUCTURAL_PAPER.pdf` remains a separate unchanged companion. All three original mathematical interfaces and every inherited active proof label are retained.

## New mathematics

Section 61 proves explicit dimension-uniform operational covering bounds on `[I/4,3I/4]`, a finite exact rational public dictionary, the randomized expected prefix-length law, and simultaneously query-optimal learning and fixed-decoder transmission in the ideal-control model. The closed-body boundary entropy, fresh-block law, finite controls and all historical sections remain active. Uniform constants in the new interior results do not promote the full-body `d^4` learning factor to an optimal one.

## Reproduction

At the native-source commit run `python build_revision.py --isolated`. At the published direct child run `GITHUB_SHA=$(git rev-parse HEAD) python build_revision.py --verify-published`. The exact source object and every generated PDF/package digest are in `evidence/BUILD_RECEIPT.json` and `evidence/PACKAGE_MANIFEST.json`. A local `--preview` is explicitly unqualified. The minimal `JOURNAL_PACKAGE.zip` rebuilds the focused paper without the repository or historical PDFs. The full `RESEARCH_PACKAGE.zip` retains all native source, the three PDFs and evidence.

`interior_codec.py` is a supplied-rational-matrix reference encoder and decoder. Complete construction can be enormous. Candidate limits raise an incomplete-construction error; prefix audits are not dictionaries. `interior_codec_check.py` includes two complete scalar dictionaries and small matrix kernels, not a physical learning experiment or a high-dimensional theorem-scale enumeration. The 16 inherited finite regression suites are retained and run alongside it, normally and with `python -O`.

## Review and history

R51 reviewed v77, not v78 or v79. Both governing reports are frozen exactly. `RESPONSE_TO_REFEREE.md` gives the current response and the full retained v78 response. `PRESERVATION_MANIFEST.json` binds 360 v78 native files, 745 complete labels, 245 focused labels and 116 structural labels. Changed originals are in `predecessor-v78-audit`. All 61 inherited section files are unchanged. See the generated source check for actual current counts.

Independent human priority review remains outstanding; no authorship signature, external review of this revision, whole-program completion or journal acceptance is claimed. The author-requested general-mathematics-journal objective is retained.
''')
(R/'JOURNAL_README.md').write_text('''# Standalone focused submission — Revision 79

`paper.pdf` is the primary mathematical submission. Its complete active LaTeX source is included. Run `python journal_verify.py` with pdfLaTeX and PyMuPDF 1.26.6 to reconstruct the pages and compare their text and rasters. The manifest gives the exact native-source identity. No other repository file or historical PDF is needed.

The structural companion is separate and the complete research edition is archival. They are available in the research package but are not dependencies of this focused submission. Build reconstruction and finite tests do not certify mathematical correctness, novelty, human authorship or an editorial decision.
''')
new='''# Response to the controlling reports — Revision 79 / R51

## Current object and further substantive response

The immediate baseline is completed v78 `1906166f98f47f4fe387143617948766395ba186` (qualified source `f893d00e51bf008c530de6046b008a3237001f81`). R51 instead reviewed v77 `5650842e0bc89ca6a8b6d6730115784f0d9ecc12`. The external and pipeline report commits remain `96a3666ed516ea12fcdb8ede341b7082e4ff2c78` and `d01b5b4d48955e8c6f0c5592213b8628e12a66dd`. No later report, human opinion, or new review of v78 is invented. The complete reports and their hashes are retained.

We have further strengthened the mathematics in the same paper rather than changing its objective or deleting difficult results. The new active Section 61 contains four theorems, with complete proofs in both mathematical editions:

* `thm:interiorentropy79`: for every `d,N>=1`, `0<delta<=2^-13`, arbitrary legal lower centres and absolute constants, the interior covering number lies between `(sqrt(N)/(2048 delta))^(d^2)` and `(25 sqrt(N)/delta)^(d^2)`. This is joint in dimension, horizon and accuracy, with no hidden `O_d` constant.
* `thm:interiorcodec79`: an explicitly ordered finite rational dictionary, exact two-sided PSD comparisons, equality rejection, certified rounding and `5delta/16` error. The payload is `(d^2/2)log2 N+d^2log2(1/delta)+O(d^2)`, without the entrywise `d^2log d` cost. Enumeration remains a separate, potentially enormous resource.
* `thm:prefixrate79`: with shared and private randomness, per-target failure at most `eta<=1/8`, and seedwise prefix-free one-way messages, the optimal worst-target expected length is `(1-eta)[(d^2/2)log2 N+d^2log2(1/delta)]+O(d^2)`. The converse permits randomized decoding. No abort flag, timing or target-dependent advice is free.
* `thm:interiorlearnedcode79`: one common finite-output learner attains the joint optimal training order `Theta(d^2 N delta^-2)` and deterministic-decoder payload order on the same interior. It credits and reanalyses Mele–Bittel's estimator, uses independent one-call acquisitions, and adds no device call for encoding. The theorem retains that estimator's ideal trusted operations and does not claim efficient physical synthesis.

These are positive additions on a full-dimensional interior; they do not replace the full closed-body theorem or its endpoint logarithms. All 61 inherited section files and all 745/245/116 active predecessor labels remain. The focused article is the journal-facing object; the complete edition retains the historical development.

## Current disposition of the twelve required revisions

| Item | Current response and locator |
|---|---|
| R01 | Focused submission is independently complete; the new journal package includes only its active graph, PDF and verifier. Structural paper separate, complete edition archival. |
| R02 | The human specialist task remains open. The brief now includes the four new theorem objects and standard-method credit; no AI/CI output is counted as human priority clearance. |
| R03 | Headline and all new statements retain ordered binary, memoryless, input-consuming classical output and arbitrary retained external reference. |
| R04 | New Section 61 supplies uniform growing-dimensional entropy and coding, complementing v78's sharp interior learning. The full-body `d^4` upper is still explicitly unmatched. |
| R05 | The direct Mele–Bittel reanalysis in section 60 is retained. The new learned-word theorem connects it to the sharp dimension-uniform description law, with explicit clipping and measurable finite readout. The fresh-block full-body separation in section 58 remains. |
| R06 | Entropy packings and pair witnesses prove converses; the learned-word theorem uses one parameter-independent estimator and one fixed decoder. |
| R07 | All new packing arguments use the actual metric `d_N` or the operator norm. No triangle inequality or exact-optimum interpretation is assigned to `Q_N`. |
| R08 | Calls, trusted measurement operations, dictionary enumeration, workspace, fixed length, expected prefix length, public seeds and nonpublic headers are now distinguished explicitly. |
| R09 | Uniform interior matching range is `d,N>=1`, `delta<=2^-13`; exact codec alone works for rational `0<delta<=1`; prefix risk `0<=eta<=1/8`; learned-word theorem has failure `1/8`. Earlier ranges remain unchanged. |
| R10 | The existing finite trusted-control theorem for the full-body learner remains. The imported query-optimal interior estimator is kept in its ideal trusted-operation model; finite output does not establish efficient gate synthesis. |
| R11 | Every successor source, PDF, standalone package and exact published head is qualified afresh. Source reconstruction, finite regression and continuum proof remain separate. |
| R12 | The entire historical A/B/C/D gate inventory is retained and its five aggregate flags stay false. No local measurement theorem is substituted for those analytic obligations. |

## Detailed comments, pipeline gates and risk status

The complete v78 line-by-line response reproduced below supplies the retained answers D01–D26 and the full M/P/C/V/E submission-gate crosswalk. Those passages are identified as predecessor response, not as new execution claims. Their mathematical locators continue to exist in v79. In particular: D04/D22 gain the dimension-uniform interior description theorem; D17–D20 gain an exact inner dictionary and the separate randomized-prefix converse; D24 is governed by the new current-object receipt, never the inherited runs; D26 continues to leave independent programme flags unchanged. P01 remains external. All source/PDF/CI gate outcomes are execution-dependent and must be read from the matching v79 receipts.

The ten R51 pipeline risks have the following current dispositions. R1 human priority remains open. R2 binary interface breadth is unchanged. R3 growing dimension is strengthened for both learning and descriptions on the stated interior, not solved for the closed body. R4 `Q_N` remains a comparison modulus. R5 exhaustive computational cost remains explicit. R6 new ranges have absolute constants and earlier ranges retain their original caps. R7 trusted tomography synthesis is not hidden in the call budget. R8 finite checks are not proofs. R9 archival volume is not a significance argument. R10 no whole-program closure is claimed.

## Preserved detailed response from v78 (historical text)

The following document is retained verbatim. References to “this revision”, old file counts or earlier runs within this historical block describe v78 only; the current objects and changes are the ones stated above and in the v79 manifests.

---

'''
(R/'RESPONSE_TO_REFEREE.md').write_text(new+(P/'RESPONSE_TO_REFEREE.md').read_text())
hist='''# History and pipeline audit — Revision 79

The immediate source baseline is completed v78 `1906166f98f47f4fe387143617948766395ba186`, not the v77 object that R51 examined. Native source `f893d00e51bf008c530de6046b008a3237001f81` and successful predecessor run 37209850660 identify v78 only. The source/PDF/evidence bundle was exported from that immutable head in run 37210851902; this export is input provenance, not v79 mathematical or build qualification.

Both R51 reports were read, including their proof audits, twelve required revisions, 26 detailed comments, ten risks and submission gates. The historical audit below and frozen pipeline history/ledger were used to trace the paper's development: positive causal experiments, predictive-state compatibility, common-row and reachable-section realization, compact-group thresholds, numerical/instrument precision, full effect geometry, matrix entropy, calibration, exact coding, block resources and interior learning. The present revision preserves this proof spine and does not claim a new independent reproof of every historical lemma.

## New proof dependency graph

`interiormetric78 -> interiorentropy79 -> interiorcodec79 -> prefixrate79`.

`Mele–Bittel III.9 + interiormetric78 + interiorcodec79 -> interiorlearnedcode79`; its call lower bound imports `dimensionlower78`, whose near-fair information lemma and Fano packing remain active. The new entropy proof works directly with operator-norm balls and cancels the unit-ball volume, so no hidden dimension constant enters. The exact codec uses the inherited PSD algorithm, not the matrix midpoint modulus. The randomized lower bound has its own conditional information argument and does not reuse a fixed-decoder cardinality argument outside its scope.

The proof of the learned-word theorem uses spectral clipping with a two-epsilon triangle bound, not an unjustified noncommutative operator-Lipschitz assertion. A Borel finite partition of the final measurement provides a finite classical output without asserting an exact-real side channel or efficient implementation of imported trusted operations.

## Preservation and analytic programme

All 360 predecessor native files are hash-bound. Every changed original is separately archived; all 61 predecessor section files are byte-identical. All 745 complete, 245 focused and 116 structural labels remain active in their respective editions. The old main/focused source files and both old editorial editions remain available. New Section 61 adds four theorem objects and a definition without moving old proofs. The structural source is unchanged.

The independent graph remains `A2 -> A3 -> A4 -> C2 -> D1`, `B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1`, with A1 independent. Unsmoothed local limits, stopped-path entropy recovery, global past kernels, exact-shell conditioning, process CLT/Mosco recovery, nonlinear graph cores, filter QMD/LAN, varying-filtration response and labelled posterior contraction require their own proofs. The measurement description results do not discharge them. The five aggregate flags remain false. This preserves the historical scope instead of changing topics or discarding unresolved content.

## Preserved v78 audit

The complete predecessor audit follows verbatim. Its version-specific statements describe that historical stage, not the current build, source identity or external-review status.

---

'''
(R/'HISTORY_AND_PIPELINE_AUDIT.md').write_text(hist+(P/'HISTORY_AND_PIPELINE_AUDIT.md').read_text())
(R/'PROOF_AUDIT.md').write_text('''# Proof audit — Revision 79

This is an author-side proof check, not an independent external referee opinion. Current new claims are in active Section 61; earlier proof audits remain byte-preserved.

| Obligation | Argument and scope |
|---|---|
| Joint parameter dimension | Hermitian matrices form a real `d^2`-dimensional normed space. Lebesgue volumes scale as radius to `d^2`; the unknown unit-ball volume cancels in both directions. |
| Arbitrary legal covering centres | Interior packing points are pairwise at least `4delta` apart in actual `d_N`; the metric triangle prevents any radius-`delta` ball, including one centred outside the interior, from holding two. |
| Absolute range | With `s=512delta/sqrt(N)` and `delta<=2^-13`, the nonsaturated term of the dimension-free lower comparison gives `4delta`. The packing has at least `4^(d^2)` points. |
| Constructive radius and rounding | `k=ceil(sqrt(N))`, `K=ceil(128dk/delta)` and threshold `t=delta/(16k)`. Certified approximate-input error plus row-sum rounding is at most `2d/K<=delta/(64k)`. Both resulting matrices lie in the expanded fixed interior. |
| Strict selection/equality | Reject when both `tI-H` and `tI+H` are PSD, including zero eigenvalues. Accept only strict norm separation. No floating tolerance or missing singular-pivot branch is used. |
| Cardinality, without coordinate logarithm | Disjoint radius-`t/2` operator balls lie in radius-`3/8+t/2`; size at most `(1+12k/delta)^(d^2)`. Coordinate enumeration affects computation but is not transmitted. |
| Total legal decoder | Reconstruct entire dictionary; use first covering predecessor. All fixed-length indices outside list decode to `I/2`. Malformed length/schema is an input error, not a purported theorem word. |
| Randomized converse | Packing label independent of public seed. Classify from decoded effect, apply conditional Fano, data processing through private decoder randomness, then conditional Kraft bound. Worst-target expected length dominates packing-average length. |
| Randomized upper | Public seed selects empty-only code with probability eta and fixed-length index set otherwise. No target-dependent stopping or uncharged abort bit. Expected length is `(1-eta)B`. |
| Unknown-device common learner | Imported parameter-independent binary estimator returns one legal F. Spectral clipping satisfies distance to true interior E at most twice operator error by Weyl plus triangle; no noncommutative Lipschitz premise. |
| Finite classical readout | Continuous clipping, coordinate rounding with specified ties and finite dictionary selection define a Borel finite partition of the final POVM. Trusted implementation/gate synthesis is not inferred. |
| Two converses not conflated | Query lower from `dimensionlower78`; fixed-decoder payload lower from actual cover. General randomized expected-length lower separately uses Fano–Kraft. |
| Historical results | Every old section and active label retained; global endpoint logarithms and unoptimized full-body dimension factors are untouched. |

`interior_codec_check.py` tests finite exact arithmetic, equality rejection, malformed input, abort-on-incomplete behavior, small matrix grids, two complete scalar dictionaries, replay and all fixed-length words. These tests do not establish the continuum covering, statistical minimax or Fano claims, which are written proofs. No high-dimensional theorem-scale dictionary or physical learner was run.
''')
(R/'LITERATURE_AUDIT.md').write_text('''# Literature audit — Revision 79

The current primary-source comparison was checked against Mele–Bittel, arXiv:2512.10214v3 (15 June 2026), in its primary HTML version. Corollary III.9 and the binary operator-norm identity remain the imported estimator input, as specified in the preserved audit. The new learned-description theorem does not claim that estimator as an invention of this paper.

The new contribution is a dimension-uniform operational description law on the same promised interior, an exact public rational dictionary at that rate, its one-way randomized expected-prefix variant, and joint learning/transmission in the stated ideal-control model. Norm-ball volume comparison, greedy nets, Kraft's inequality, Fano's inequality, public erasure and measurable coarsening are standard mechanisms. The paper proves their specific combination with the dimension-free future-use metric rather than attributing those mechanisms to this revision. No new literature claim that the four theorem objects are globally first is made. The nearest-neighbour priority questions remain in the human specialist brief.

## Complete predecessor theorem-level audit (historical text)

The following is preserved verbatim. Its claims about what was new in v78 and its date-specific checks are records of that stage.

---

'''+(P/'LITERATURE_AUDIT.md').read_text())
(R/'INDEPENDENT_REVIEW_BRIEF.md').write_text('''# Independent human specialist brief — Revision 79

No independent human specialist opinion has been obtained or fabricated. This is an actionable brief for the next referee. The journal objective is unchanged. R51 is the controlling report on v77; the candidate now contains v78 plus the new Section 61.

Please assess the exact relation of the dimension-free interior future-use comparison and near-fair adaptive information lower bound to known measurement tomography. Then examine whether the growing-dimensional covering law with arbitrary legal centres, the public exact rational dictionary without an entrywise `d^2 log d` payload loss, and the combined query-optimal learned words occur under equivalent interfaces in prior work. The randomized prefix result expressly uses classical Fano–Kraft and public-erasure ideas; assess the operational formulation rather than novelty of these ingredients. In particular, check the unknown-parameter-independent finite coarse graining and the distinction between ideal trusted operations and efficient synthesis.

Full-body endpoint entropy, the sharp fixed-dimensional independent-block law and their priority questions remain unchanged. The complete previous brief follows, as history and additional questions, not as evidence that a human review has occurred.

---

'''+(P/'INDEPENDENT_REVIEW_BRIEF.md').read_text())
res=json.loads((P/'RESOURCE_LEDGER.json').read_text());res['revision_79_interior']={'range':'d,N>=1; matching entropy delta<=2^-13; exact supplied-rational codec delta<=1; randomized prefix eta in[0,1/8]; learned word failure1/8','target':'I/4<=E<=3I/4; decoder centres I/8<=C<=7I/8','deterministic_payload':'(d^2/2)log2N+d^2log2(1/delta)+O(d^2), absolute uniform remainder','randomized_expected_payload':'(1-eta) times the same leading expression plus O(d^2); shared target-independent seed, prefix-free messages at each seed','learned_training':'Theta(d^2 N delta^-2), fresh one-call acquisition and collective completed-output processing','post_learning_queries':0,'dictionary_parameters':'k=ceil(sqrt(N));K=ceil(128dk/delta);t=delta/(16k)','enumeration_tuples':'at most (K+1)^d(2K+1)^(d(d-1)); exact PSD comparisons and their arithmetic/workspace separately charged','implementation':'Exact rational supplied-matrix encoder and decoder. Two complete scalar dictionaries; small matrix kernel cases. No physical common learner execution.','trusted_implementation':'Mele–Bittel ideal tomography for joint query rate; finite POVM coarsening does not establish an efficient gate circuit','headers':'d,N,delta,eta public; nonpublic headers, timing and target-dependent advice charged'}
(R/'RESOURCE_LEDGER.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
(R/'RESOURCE_LEDGER.md').write_text('''# Resource ledger — Revision 79

The new `revision_79_interior` entry in `RESOURCE_LEDGER.json` is controlling for Section 61. In particular, worst-record device calls, maximum fresh-block length, trusted tomography operations, exact dictionary enumeration, classical workspace, deterministic index length and randomized expected prefix length are different resources. Public randomness must be independent of the target. The default finite exact codec has no failure or public-randomness requirement. Runtime interruption produces no partial codebook. The learned-word theorem is in the ideal trusted-operation query model, not an efficient synthesis theorem.

The complete predecessor resource ledger is retained below; its version-specific implementation statements refer to v78.

---

'''+(P/'RESOURCE_LEDGER.md').read_text())
(R/'publish_revision.py').write_text('''#!/usr/bin/env python3
"""Emit generated-artifact inventory at the qualified v79 native source."""
from pathlib import Path
import json
from build_revision import ROOT, DOCS, sha, require, git_output, committed_source, check_source

def main():
    checked, inv = check_source(ROOT)
    r = json.loads((ROOT/'evidence/BUILD_RECEIPT.json').read_text())
    head = git_output(ROOT, 'rev-parse', 'HEAD')
    require(r['schema'] == 'gtf79.build/1' and r['qualified_git_source']
            and r['source_commit'] == head and r['isolated_native_rebuild']
            and r['standalone_journal_rebuild'], 'current native build not qualified')
    committed_source(ROOT, head, inv)
    files = {n: sha((ROOT/n).read_bytes()) for n in DOCS.values()}
    for p in sorted((ROOT/'evidence').rglob('*')):
        if p.is_file(): files[p.relative_to(ROOT).as_posix()] = sha(p.read_bytes())
    print(json.dumps({'schema': 'gtf79.publication-plan/1', 'source_commit': head,
                      'publication_parent': head, 'generated_files': files,
                      'documents': r['documents'], 'read_only': True}, indent=2, sort_keys=True))

if __name__ == '__main__': main()
''')
print('metadata ready')
