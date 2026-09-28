# A2 revision 62 — complete review-ready delivery

**Boundary laws and rigidity of periodic dispersing billiards**  
Qian Qi — September 16, 2026

## 1. Frozen submission and branches

| Object | Identity |
|---|---|
| Review-ready branch | `revision/a2-v62-review-ready-2026-09-16` |
| Actual compiled mathematical source | `037c80dc44d8191e6f808591ea0651e813234d06` |
| Compiled manuscript subtree | `160735632f3977d47dcf708fb2292699ab79fafd` |
| Source branch | `revision/a2-v62-finite-experiment-2026-09-16` |
| Verified native-products branch | `revision/a2-v62-native-products-35047150051-1` |
| Native-products head, before this delivery index | `9dc07b142a5aff3ffa8d7de2e3061a61768bf9f0` |
| Native workflow / attempt / artifact | `35047150051` / `1` / `10427846002` |
| Addressed review branch | `review/a2-v61-independent-harsh-top4-2026-09-16` |
| Addressed review head | `9ec2004a18cccc69ed473685bdf94c91f0b25d4d` |
| Previously reviewed mathematical source | `71e0bd6306f54466728c2e6e781bb0f422c5cfb0` |

The review-ready branch descends from the verified native-products head. This final index and verification record do not alter the manuscript subtree, compiled mathematical inputs, or retained PDFs. The latest report, complete sources, response and complete native products are present together. The earlier `A2_REVISION_V62_INDEX.md` is retained as the pre-build source index; this document supplies the completed delivery identities.

## 2. Manuscripts and author response

| Manuscript | Pages | Complete native PDF |
|---|---:|---|
| Principal article | 125 | [rigidity.pdf](deliveries/a2-v62/037c80dc44d8191e6f808591ea0651e813234d06/rigidity.pdf) |
| Full technical manuscript | 300 | [main.pdf](deliveries/a2-v62/037c80dc44d8191e6f808591ea0651e813234d06/main.pdf) |
| Two-collision companion | 7 | [two_collision.pdf](deliveries/a2-v62/037c80dc44d8191e6f808591ea0651e813234d06/two_collision.pdf) |

[Frozen complete source](deliveries/a2-v62/037c80dc44d8191e6f808591ea0651e813234d06/native-source.zip) · [Response to every numbered v61 item](papers/A2-v17-boundary-information-coarsening/RESPONSE_TO_REFEREE_V62.md) · [Cover letter](papers/A2-v17-boundary-information-coarsening/COVER_LETTER_V62.md) · [Historical derivation audit](papers/A2-v17-boundary-information-coarsening/HISTORICAL_DERIVATION_AUDIT_V62.md) · [Dependency ledger](papers/A2-v17-boundary-information-coarsening/journal/DEPENDENCY_LEDGER_V62.md) · [Targeted primary-literature check](papers/A2-v17-boundary-information-coarsening/LITERATURE_CHECK_V62.md).

The directory name `papers/A2-v17-boundary-information-coarsening/` is historical. The active version is 62.

## 3. Mathematical change and direct review route

The new shared proof is [article/23f2_finite_experiment_analytic_inverse_v62.tex](papers/A2-v17-boundary-information-coarsening/article/23f2_finite_experiment_analytic_inverse_v62.tex). Section **13.4**, beginning on principal p. 63, contains five fully proved statements:

| Statement | Principal page | Content |
|---|---:|---|
| Lemma 13.5 | 64 | Uniform finite-to-limit density control, offset continuity, and the actual full-phase acceptance lower bound |
| Theorem 13.6 | 65 | Stability of complete analytic contact germs from finite bridge laws; simultaneous coefficient bounds |
| Theorem 13.7 | 65 | Finite histogram estimator with every raw preparation charged |
| Corollary 13.8 | 67 | Estimated calibration, cell-boundary displacement, amplified timing error, and additive pilot cap |
| Corollary 13.9 | 68 | Complete preparation-budget rate using the retained position pilot; proof ends on p. 69 |

The corresponding full-manuscript section begins on p. 64. The new overview is additive; neither the v61 introduction nor any inherited theorem/proof module is replaced.

For a bounded local analytic class, fixed positive offset, marked channel design and smaller target disc, the exactly calibrated experiment has confidence radius

`C (log(C N/alpha)/N)^[vartheta omega/(4 omega + Gamma)]`

using `2N` independent full-phase preparations, including every rejected attempt. The flight number is even and logarithmic in the budget. The proof fits the cell averages of a realizable limiting law before applying the analytic inverse: finite bridge laws and empirical histograms are not assumed to factor exactly. An outside category remains in the normalization, and measurable approximate selection is proved without a finite computational search claim.

With the existing position-sensor pilot, its compact marked-class hypotheses and an exact clock, a separate conclusion charges the complete onset scan and coordinate calibration. With at most `B` preparations in total, the confidence radius is

`C ([log(C B/alpha)]^2/B)^[vartheta omega/(12 omega + Gamma)]`.

Here `e^(-omega j)` is the relative finite-flight error and `Gamma` bounds the acceptance exponent, enlarged as needed for the pilot. The power 12 comes from the printed pilot cap and displacement tolerance. These are proved upper bounds, not assertions of optimality. The analytic prior, radius loss, local target and observation marks are explicit. Global analytic continuation, incidence matching, lattice reconstruction, finite-dimensional differential results, nuisance windows and the broader acquisition theory retain their original hypotheses and proofs.

The v61 report established no new mandatory core correction. Its significance judgment is engaged by this finite-experiment consequence, not reclassified as a technical error. Neither the new theorem nor a successful build compels a positive general-journal recommendation; the response requests independent mathematical and editorial reassessment.

## 4. Preservation and verification actually performed

All **753** files in the prior frozen source were verified before editing. The new frozen source has **767** files. All inherited paths remain; **750** are byte-identical. The only changed inherited files are `main.tex`, `rigidity.tex`, and the manuscript `README.md`. Their exact originals are archived in `history/v61-review-baseline/`, along with the previous repository README. Every inherited active proof input remains unchanged and in its original relative order. The active input counts are 115 full, 47 principal and one companion, with 126 distinct paths in their union.

Native run `35047150051`, attempt 1, completed both `native` and `publish-verified-products` successfully. The publisher verified indexed products, pushed to a new branch, fetched actual Git objects and checked them again before committing the attestation. The full evidence is in the [delivery directory](deliveries/a2-v62/037c80dc44d8191e6f808591ea0651e813234d06/), including `build-report.json`, manifests, logs, diagnostics, `REPOSITORY_RETENTION.json`, and `COMMITTED_OBJECTS_VERIFIED.json`.

After downloading the native artifact, the author-side delivery check independently verified all 767 frozen file lengths, SHA-256 values and Git blob identities, and 45 build-report evidence entries. All **432** PDF pages match the separately compiled local products in extracted text. PDF byte identity with the local build is not asserted. Native and local v62 diagnostics agree, and normal and optimized Python runs agree.

Finite controls comprise 20 exact binomial-tail cases, 60 Bernstein cases, 12 cell-tube cases and 54 even-schedule cases, plus negative controls for an omitted outside category, mesh-independent displacement and an uncharged pilot. These are finite diagnostic checks, not proofs of the relative determinant limit, the analytic inverse or the statistical theorem.

Actual visual inspection covered principal pp. **1, 2, 9, 10, 63–69**, full technical pp. **1–2**, and companion p. **1**: 14 selected pages. Their native and local 1.3-scale render arrays agree. No clipping or unreadable expression was observed on those pages. This is not all-page visual inspection. Final logs have no overfull-box, undefined-reference/citation or missing-glyph finding; they retain four full-manuscript and one principal underfull-vbox notices, and none in the companion.

[Machine-readable author verification](A2_REVISION_V62_VERIFICATION.json) records the exact coverage. Source preservation, selected finite checks and successful typesetting are not a proof certificate or evidence that the editorial significance question is closed. Historical interfaces examined are listed in the derivation audit; no fresh line-by-line audit of all inherited 420 pages is claimed.

## 5. Product hashes

| Product | Bytes | SHA-256 |
|---|---:|---|
| `rigidity.pdf` | 1138902 | `d328e5217fd7052a42f73016c9cefbd269845497ca50b764e082c26f8006e98f` |
| `main.pdf` | 2193988 | `725f2f9db68bb0bd3c269c53250ad3093add261a7a9cac54efc16d1907c22f3b` |
| `two_collision.pdf` | 333367 | `b9390b0975c41bdef488dade494e9d8f06150e191d563e052ad7b556174e1eb1` |
| Frozen `native-source.zip` | See retained manifest | `3d320058366746fb3b4d9d8dc5e71f01a710737ea8c3e686bfe6687ddcea138f` |
| Downloaded workflow artifact ZIP | 6499817 | `e02c1f9bb6cb60ad1cbd08dfd1923f2e92672d52ab97ec7f2e6d10b6da2710bc` |

The PDF Git blobs are respectively `c7a67f7f2a4a3df9d6fbacd546ee8a2ba0fdb74c`, `f9fffda4f9ac21abc574df81c95347416105e94e`, and `dae9697f40bcac775d7dd6aa26144af0181adc75`.

## 6. Reproduction

In a fresh clone with Python, NumPy, SciPy, SymPy, latexmk, the required TeX Live packages and Poppler installed, reproduce from the actual mathematical source rather than a delivery-index commit:

```sh
git checkout --detach 037c80dc44d8191e6f808591ea0651e813234d06
git fetch --no-tags origin 71e0bd6306f54466728c2e6e781bb0f422c5cfb0
P=papers/A2-v17-boundary-information-coarsening
python3 -B "$P/tools/check_revision_v62.py"
python3 -O -B "$P/tools/check_revision_v62.py"
python3 -B "$P/tools/build_revision_v56.py" --output-dir /tmp/a2-v62-rebuild
```

The historical builder name does not determine the manuscript version: it builds the committed current entries and records their actual source. Its cross-document references require the companion/full/principal build order implemented there. No shell escape is needed. No A1 source, default-branch ref or historical review ref was changed by this revision.
