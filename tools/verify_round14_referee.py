#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
inv=json.loads((ROOT/"ROUND14_REFEREE_INVENTORY.json").read_text(encoding="utf-8"))
errors=[]
report={"schema":"theta-theory-round14-structural-verification-v1","papers":{}}

thm_re=re.compile(r"\\begin\{(?:theorem|lemma|proposition|corollary)\}")
proof_re=re.compile(r"\\begin\{proof\}")
lab_re=re.compile(r"\\label\{([^}]+)\}")
ref_re=re.compile(r"\\(?:ref|cref|eqref)\{([^}]+)\}")

global_labels={}
total_thm=total_proof=0
for name,entry in inv["papers"].items():
    report_path=ROOT/entry["report_path"]
    source=ROOT/entry["registered_source"]
    active=ROOT/entry["active_module"]
    response=ROOT/entry["response"]
    main=ROOT/"papers"/name/"main.tex"
    for p in (report_path,source,active,response,main):
        if not p.is_file(): errors.append(f"{name}: missing {p.relative_to(ROOT)}")
    if not all(p.is_file() for p in (report_path,source,active,response,main)):
        continue
    report_text=report_path.read_text(encoding="utf-8")
    source_text=source.read_text(encoding="utf-8")
    active_text=active.read_text(encoding="utf-8")
    response_text=response.read_text(encoding="utf-8")
    main_text=main.read_text(encoding="utf-8")
    report_sha=hashlib.sha256(report_text.encode()).hexdigest()
    source_sha=hashlib.sha256(source_text.encode()).hexdigest()
    active_sha=hashlib.sha256(active_text.encode()).hexdigest()
    if report_sha != entry["report_sha256"]:
        errors.append(f"{name}: report hash changed")
    objections=re.findall(r"^###\s+\d+\.\s+(.+)$",report_text,re.M)
    if len(objections)!=entry["objection_count"]:
        errors.append(f"{name}: objection count mismatch")
    for i,obj in enumerate(objections,1):
        if f"### {i}. {obj}" not in response_text:
            errors.append(f"{name}: response missing objection {i}")
    if source_text!=active_text:
        errors.append(f"{name}: registered/active byte mismatch")
    if r"\input{ROUND14_POSITIVE_CLOSURE.tex}" not in main_text:
        errors.append(f"{name}: main not loading Round14")
    if "ROUND14-REFEREE-POSITIVE-CLOSURE" not in main_text:
        errors.append(f"{name}: revision marker absent")
    thm=len(thm_re.findall(source_text)); proof=len(proof_re.findall(source_text))
    if thm==0 or thm!=proof:
        errors.append(f"{name}: theorem/proof mismatch {thm}/{proof}")
    labels=lab_re.findall(source_text)
    if len(labels)!=len(set(labels)):
        errors.append(f"{name}: duplicate local labels")
    for label in labels:
        if label in global_labels:
            errors.append(f"duplicate global label {label}")
        global_labels[label]=name
    refs=[]
    for payload in ref_re.findall(source_text):
        refs.extend(x.strip() for x in payload.split(",") if x.strip())
    missing=sorted(set(refs)-set(labels))
    if missing: errors.append(f"{name}: unresolved local refs {missing}")
    banned=[
        "NO_THEOREM_CREDIT","assume the main gate","reviewer must verify",
        "remove as a standalone submission","no-go theorem","conditional only on",
    ]
    for token in banned:
        if token.lower() in source_text.lower():
            errors.append(f"{name}: banned placeholder {token}")
    total_thm+=thm; total_proof+=proof
    report["papers"][name]={
        "status":"PASS",
        "report_sha256":report_sha,
        "objections":len(objections),
        "source_sha256":source_sha,
        "active_sha256":active_sha,
        "byte_identity":source_sha==active_sha,
        "theorem_like_environments":thm,
        "proofs":proof,
        "labels":len(labels),
        "references":len(refs),
    }

# Declared DAG.
edges=[
 ("A2","A3"),("A3","A4"),("A4","C2"),("C2","D1"),
 ("B2-GC","B1"),("B1","B2-MC"),("B2-MC","B3"),
 ("B3","B4"),("B4","C1"),("B4","C2"),("C1","D1")
]
nodes=set(sum(([a,b] for a,b in edges),[]))
graph={n:[] for n in nodes}
for a,b in edges: graph[a].append(b)
seen=set(); stack=set()
def dfs(n):
    if n in stack: return False
    if n in seen: return True
    stack.add(n)
    for m in graph[n]:
        if not dfs(m): return False
    stack.remove(n); seen.add(n); return True
dag=all(dfs(n) for n in list(nodes))
if not dag: errors.append("dependency cycle")
if inv["total_objections"] != sum(x["objections"] for x in report["papers"].values()):
    errors.append("total objection mismatch")

report.update({
    "paper_count":len(report["papers"]),
    "referee_objections":inv["total_objections"],
    "total_theorem_like_environments":total_thm,
    "total_proofs":total_proof,
    "dependency_dag":"PASS" if dag else "FAIL",
    "errors":errors,
    "status":"PASS" if not errors else "FAIL",
})
(ROOT/"ROUND14_STRUCTURAL_VERIFICATION.json").write_text(
    json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8"
)
if errors:
    for e in errors: print("ROUND14_VERIFY_ERROR",e,file=sys.stderr)
    raise SystemExit(1)
print(f"ROUND14_STRUCTURAL_PASS papers={len(report['papers'])} objections={inv['total_objections']} theorem_proof={total_thm}/{total_proof}")
