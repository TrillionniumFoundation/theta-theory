# A2 v46 preservation and dependencies

Baseline mathematical source: `2f064b86b4e071d24ad671f4dc652d7de32a56a4`. Latest review inherited from `0614a20bbba6312830b5523b806ddc726a6333f1`.

The baseline manifest has 98 main inputs and one complete companion input. The new main has 100 inputs. Of the 99 distinct baseline active files, 95 are byte-identical. The four edited active originals are copied verbatim under `history/v45-review-baseline/`, together with the baseline manifest and identity ledger.

The four edits are: main metadata, abstract and two additional inputs; one introductory image-stability qualifier pointing to the new theorem; the exact P1 backtrack correction; and one added bibliography entry. All original references remain. The main retains the exact inherited input order after the two new modules are removed from that list. The companion is untouched.

All 226 inherited theorem/lemma/proposition/corollary/definition environments, 22 remarks and 466 matched mathematical environment blocks remain active. Proof-block comparison permits only the stated P1 substitution. Seven theorem-style environments are added. No historical branch, earlier manuscript, report, native delivery, A1 workstream or other programme paper is deleted or reduced.

The original root and paper navigation are preserved in the baseline directory. New navigation is confined to new revision branches. The full mathematical dependency and inspection scope appears in `HISTORICAL_DERIVATION_AUDIT_V46.md`; the exact executable check is `tools/check_revision_v46.py`. Source preservation and successful compilation are not mathematical certification.
