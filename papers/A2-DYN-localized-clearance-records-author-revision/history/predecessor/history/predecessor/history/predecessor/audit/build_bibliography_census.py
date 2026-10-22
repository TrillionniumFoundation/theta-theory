#!/usr/bin/env python3
"""Record bibliography source identities and explicit verification scope."""
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
if (BASE.parent / "history/historical-v108").is_dir():
    # Portable invocation from the delivered native article's audit directory.
    ROOT = article = BASE.parent
    bases = [article / "history/historical-v108", article / "history/numbered-variants",
             article / "history/historical-manuscript-variants", article]
else:
    ROOT = BASE.parent
    article = ROOT / "theta-theory/papers/A2-DYN-global-minimizer-localization-author-revision"
    bases = [ROOT / "audit-source/historical-native", ROOT / "audit-source/native-variants", article]
content_map = {}
for base in bases:
    for path in base.rglob("*"):
        if not path.is_file() or path.suffix not in (".tex", ".txt"):
            continue
        relative = str(path.relative_to(ROOT))
        if base == article and path.relative_to(article).parts[0] in ("history", "audit"):
            continue
        raw = path.read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        if sha not in content_map:
            content_map[sha] = {"sha256": sha, "bytes": len(raw), "paths": [], "text": raw.decode(errors="replace")}
        content_map[sha]["paths"].append(relative)
entries = defaultdict(list)
citations = defaultdict(list)
for sha, obj in content_map.items():
    # Preserve line numbers while discarding TeX comments for citation navigation.
    tex = re.sub(r"(?<!\\)%[^\n]*", "", obj["text"])
    for match in re.finditer(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}([\s\S]*?)(?=\\bibitem|\\end\{thebibliography\}|\Z)", tex):
        entry = re.sub(r"\s+", " ", match[2]).strip()
        entries[match[1]].append({"entry": entry, "source_sha256": sha, "source_paths": obj["paths"], "line": tex.count("\n", 0, match.start())+1})
    for match in re.finditer(r"\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}", tex):
        for key in match[1].split(","):
            citations[key.strip()].append({
                "source_sha256": sha, "source_paths": obj["paths"],
                "line": tex.count("\n", 0, match.start())+1,
                "citation_command": match[0],
                "local_source_context": tex[max(0,match.start()-260):min(len(tex),match.end()+400)]
            })
aliases = {"DZUniform":"DZ", "DNFlow":"DN"}
internal = {"A2G","Q108","Q109","Q110","Q111","Q114"}
fresh = {
 "DZ": {"status":"fresh_primary_theorem_object_check", "primary_url":"https://arxiv.org/pdf/1210.1261", "checked":"Lemma 3.2(b), H2-H4, Theorems 2.2-2.6 and Remark 2.7(b)", "scope":"Native 281-283 curve-growth match checked; not a certification of all physical-cylinder pressure or all strong/weak operator uses."},
 "BDPressure":{"status":"fresh_primary_theorem_object_check", "primary_url":"https://arxiv.org/pdf/2009.10936", "checked":"Section 1.1 stronger horizon convention, pressure-gap interval, Theorems 1.1-1.2 and Corollary 1.5", "scope":"Native 287/294 satisfy no-all-tangent geometry. Full partition-object adaptation and radius-uniform pressure input remain separate."},
 "DN":{"status":"fresh_primary_theorem_object_check", "primary_url":"https://arxiv.org/pdf/1710.08568", "checked":"Definition 2.2, Remark 2.5 and Proposition 6.3", "scope":"Tested flow/local-limit hypotheses and arithmetic cases checked. Does not supply raw roof essential height or arbitrary microscopic conditioning."}
}
defined_key_count=len(entries)
cited_key_count=len(citations)
undefined_keys=sorted(set(citations)-set(entries))
allkeys=sorted(set(entries)|set(citations))
records=[]
for key in allkeys:
    work=aliases.get(key,key)
    if key in internal:
        verification={"status":"repository_native_source_reference", "scope":"Source identity/preservation reference, not an external mathematical theorem or external journal endorsement."}
    elif work in fresh:
        verification=fresh[work]
    elif key=="BVNotes":
        verification={"status":"background_only_not_new_theorem_input", "scope":"Convex-duality lecture notes are background; all new variational arguments are native proofs. No fresh theorem-level recertification of the notes is claimed."}
    else:
        verification={"status":"retained_historical_import_not_freshly_primary_recertified", "scope":"Source text and citation contexts are recovered. Historical author checks are retained, but this iteration has not independently reread every cited primary theorem and reconstructed all its applications."}
    records.append({"key":key,"canonical_work_key":work,"classification":"repository_native" if key in internal else "external", "definition_variants":entries[key], "citation_occurrences":citations[key], "verification":verification})
externalworks=sorted({x["canonical_work_key"] for x in records if x["classification"]=="external"})
result={
 "purpose":"Full recovered bibliography census with explicit primary theorem-check statuses, not complete historical import certification",
 "date":"2026-10-18",
 "scanned_roots":[str(p.relative_to(ROOT)) for p in bases],
 "distinct_source_contents":len(content_map),
 "definition_key_count":defined_key_count,
 "cited_key_count":cited_key_count,
 "external_distinct_works":len(externalworks),
 "repository_native_keys":sorted(internal),
 "undefined_citation_keys":undefined_keys,
 "fresh_primary_work_keys":sorted(fresh),
 "new_native_304_309_external_theorem_inputs":"none; modules 306 and 309 normalized conclusions use the explicitly retained native pressure and pairing inputs",
 "source_manifest":[{k:v for k,v in obj.items() if k!="text"} for obj in content_map.values()],
 "records":records
}
out=BASE/"HISTORICAL_BIBLIOGRAPHY_CENSUS.json"
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:result[k] for k in ["distinct_source_contents","definition_key_count","cited_key_count","external_distinct_works","undefined_citation_keys","fresh_primary_work_keys"]},indent=2))

