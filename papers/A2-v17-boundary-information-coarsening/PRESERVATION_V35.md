# A2 v35 preservation and provenance

The source base is the complete v34 tree `014fd9acaf5f6b1af376ce3bb7802f500bc88ec4` at `127f9334f15c5fb12307bd691973d1eb44e499e8`. The latest addressed review is `d51c06689ba540711b2f890beb35eb235dba13e4`, reviewing v33 `b577cffcb3ca5597cb4905269bea9de3bd4ead38`. Its report and three reproducibility files are incorporated by their existing blobs, without altering the review branch.

Only the local risk-proof paragraph is mathematically expanded. The other change to an active TeX entry is the revision identity in `main.tex`. The original abstract, all eight theorem/lemma statements in the changed chapter, all 52 direct inputs in their original order, and the 36-input auxiliary compendium are preserved. No existing repository file is deleted. All other inherited manuscript sources are reused from the base tree, including the v34 likelihood-tilting supplement and the complete native companion.

| Preserved source | Exact Git blob | Archive path |
|---|---|---|
| v34 main | `4aa56cd663a522dad0d628db2c6928fa45fc865a` | `history/v34/main.tex` |
| v34 vector chapter | `c036b730155d55420b92980a20abd40812ba7811` | `history/v34/article/18a_vector_boundary_information_v26.tex` |
| Prior repository README | `f971281eac847ad2078bd8122672b95bd43707f1` | root `README_PRE_V35.md` |
| Prior paper README | `a5dc1d9bef6bf3e49ae57e771b0c7ffc10b49c30` | paper `README_PRE_V35.md` |
| Unchanged auxiliary compendium | `a596f344cd660eeaacc8e4e3eb21a0cb39610a9e` | active original path |
| Unchanged native companion | `df44402b17031525c087d39dfedf8dac3ada611d` | `two_collision.tex` |
| Unchanged v34 supplement | `a8658275503f4eed5ebbae675710e4a8392a39a5` | active original path |

The revised vector blob is `8ff3ce7334954d6544555e9867a12fa805ca5ea0`. The revised main blob is `d21ea5c3c3926890505a8e44683b8e5de91e9d8b`. `tools/check_revision_v35.py` checks source identities and statement preservation explicitly in ordinary and optimized Python.

The historical path `A2-v17-boundary-information-coarsening` is retained for relative-path stability; it is not the revision number of the active manuscript. The actual README and PDF metadata now identify v35. The statistical A1 and separate dynamical/mechanical workstreams remain untouched. No merge to `main`, branch-protection change, membership change, or alteration of prior review records is part of this revision.
