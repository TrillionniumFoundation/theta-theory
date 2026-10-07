#!/usr/bin/env python3
"""Manifest-locked standalone TeX build and independent clean reconstruction."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MANIFEST = "SOURCE_MANIFEST.json"
POLICY = json.loads((ROOT / "PUBLICATION_POLICY.json").read_text())
EXCLUDED_ROOT = {MANIFEST, "paper.pdf", "SOURCE_TRANSFER.tar.gz"}
EXCLUDED_DIRS = {"build", "evidence", ".git", "__pycache__"}

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def need(ok: bool, text: str) -> None:
    if not ok:
        raise RuntimeError(text)

def run(args: list[str], cwd: Path, env: dict[str,str] | None=None) -> str:
    p = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"command failed ({p.returncode}): {args}\n{p.stdout[-5000:]}\n{p.stderr[-3000:]}")
    return p.stdout

def files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file()
                  and not any(x in EXCLUDED_DIRS for x in p.relative_to(root).parts[:-1])
                  and p.relative_to(root).as_posix() not in EXCLUDED_ROOT
                  and p.suffix not in {".pyc"})

def make_manifest() -> None:
    entries = {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in files(ROOT)}
    obj = {"schema":"general-theta.restart-r2.source/1", "canonical_sha":POLICY["canonical_sha"],
           "files":entries, "workflow_is_bound_by_git_commit_not_native_inventory":True}
    (ROOT/MANIFEST).write_text(json.dumps(obj,sort_keys=True,indent=2)+"\n")

def audit(root: Path) -> dict:
    obj = json.loads((root/MANIFEST).read_text())
    expected = obj["files"]
    actual = {p.relative_to(root).as_posix(): sha(p.read_bytes()) for p in files(root)}
    need(actual == expected, "source inventory/hash mismatch")
    texfiles = [p for p in files(root) if p.suffix == ".tex"]
    source = "\n".join(p.read_text() for p in texfiles)
    labels = re.findall(r"\\label\{([^}]+)\}",source)
    need(len(labels)==len(set(labels)), "duplicate labels")
    refs = re.findall(r"\\(?:eqref|ref)\{([^}]+)\}",source)
    need(set(refs)<=set(labels), f"unresolved source labels: {set(refs)-set(labels)}")
    bib = re.findall(r"\\bibitem\{([^}]+)\}",source)
    need(len(bib)==len(set(bib)), "duplicate bibliography keys")
    cites = {k.strip() for group in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}",source) for k in group.split(",")}
    need(cites == set(bib), "unused or missing bibliography entry")
    inputs = re.findall(r"\\input\{([^}]+)\}",(root/"main.tex").read_text())
    need(set(inputs)|{"main.tex"} == {p.relative_to(root).as_posix() for p in texfiles}, "native TeX inventory differs from inputs")
    statements = re.findall(r"\\begin\{(?:theorem|proposition|lemma|corollary)\}",source)
    proofs = re.findall(r"\\begin\{proof\}",source)
    need(len(statements)==len(proofs), "statement/proof environment count mismatch")
    ledger = (root/"PROOF_LEDGER.md").read_text()
    theorem_labels = re.findall(r"\\begin\{(?:theorem|proposition|lemma|corollary)\}(?:\[[^\]]*\])?\\label\{([^}]+)\}",source)
    need(len(theorem_labels)==len(statements), "an unlabelled formal statement exists")
    need(all(label in ledger for label in theorem_labels), "proof ledger misses a label")
    normal = run([sys.executable,"verify.py"],root).strip()
    optimized = run([sys.executable,"-O","verify.py"],root).strip()
    need(normal==optimized, "normal and optimized regressions differ")
    regression = json.loads(normal)
    need(regression["status"]=="success" and regression["continuum_proof_by_tests"] is False, "invalid regression receipt")
    return {"source_files":len(expected), "native_tex_files":len(texfiles),
            "labels":len(labels), "formal_statements":len(statements), "proof_environments":len(proofs),
            "bibliography_entries":len(bib), "manifest_sha256":sha((root/MANIFEST).read_bytes()),
            "normal_optimized_identical":True, "regression":regression}

def compile_tex(root: Path, out: Path) -> tuple[str,int]:
    out.mkdir(parents=True,exist_ok=True)
    env = dict(os.environ, SOURCE_DATE_EPOCH="1791295057", FORCE_SOURCE_DATE="1", TZ="UTC")
    for i in range(1,4):
        log = run(["pdflatex","-interaction=nonstopmode","-halt-on-error",f"-output-directory={out}","main.tex"],root,env)
        (out/f"pass-{i}.txt").write_text(log)
    log = (out/"main.log").read_text(errors="replace")
    forbidden = ["Undefined control sequence", "undefined references", "undefined citations", "multiply defined", "Overfull \\"]
    need(not any(term in log for term in forbidden), "TeX final log failed reference/layout audit")
    need(not re.search(r"(?:Reference|Citation) .+ undefined",log), "unresolved TeX reference")
    data = (out/"main.pdf").read_bytes()
    info = run(["pdfinfo",str(out/"main.pdf")],root)
    match = re.search(r"^Pages:\s+(\d+)",info,re.M)
    need(match is not None, "PDF page count unavailable")
    return sha(data), int(match.group(1))

def git_binding(source_sha: str, verify_published: bool) -> dict:
    p = subprocess.run(["git","rev-parse","--show-toplevel"],cwd=ROOT,capture_output=True,text=True)
    if p.returncode:
        need(not verify_published, "published verification requires a Git checkout")
        return {"kind":"local_manifest_copy_not_full_git_checkout", "source_sha":source_sha}
    gitroot = Path(p.stdout.strip())
    head = run(["git","rev-parse","HEAD"],ROOT).strip()
    need(re.fullmatch(r"[0-9a-f]{40}",source_sha) is not None, "exact source SHA required in Git checkout")
    need(ROOT.relative_to(gitroot).as_posix()+"/" == POLICY["paper_prefix"], "unexpected repository paper path")
    need(not run(["git","status","--porcelain"],ROOT).strip(), "source checkout is dirty")
    scope = run(["git","diff","--name-only","--no-renames",POLICY["canonical_sha"],head],ROOT).splitlines()
    need(all(x.startswith(POLICY["paper_prefix"]) or x in POLICY["workflow_paths"] for x in scope), "historical/canonical file changed outside allowlist")
    binding = {"kind":"exact_git_checkout", "head":head, "source_sha":source_sha,
               "canonical_sha":POLICY["canonical_sha"], "scope_preservation_checked":True,
               "changed_paths_from_canonical":scope}
    if verify_published:
        need(run(["git","rev-parse","HEAD^"],ROOT).strip()==source_sha, "artifact is not direct child of declared native source")
        changed = run(["git","diff","--name-only","--no-renames",source_sha,head],ROOT).splitlines()
        allowed = {POLICY["paper_prefix"]+p for p in POLICY["artifact_paths"]}
        need(set(changed)==allowed, "publication changed more or less than the three artifact files")
        creds = subprocess.run(["git","config","--local","--get-regexp",r"^http\..*\.extraheader$"],cwd=ROOT,capture_output=True,text=True)
        need(not creds.stdout.strip(), "checkout retained HTTP credentials")
        binding.update({"read_only_verification":True, "checkout_credentials_removed":True,
                        "artifact_only_diff":changed})
    else:
        need(head==source_sha, "build HEAD differs from native source SHA")
    return binding

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--make-manifest",action="store_true")
    parser.add_argument("--audit-only",action="store_true")
    parser.add_argument("--verify-published",action="store_true")
    parser.add_argument("--source-sha",default="LOCAL_UNPUBLISHED")
    parser.add_argument("--out",type=Path)
    args = parser.parse_args()
    if args.make_manifest:
        make_manifest()
        return
    diagnostics = audit(ROOT)
    if args.audit_only:
        print(json.dumps(diagnostics,sort_keys=True))
        return
    need(args.out is not None, "--out outside source directory is required")
    out = args.out.resolve()
    need(ROOT not in out.parents and out!=ROOT, "build output must be outside source tree")
    out.mkdir(parents=True,exist_ok=True)
    binding = git_binding(args.source_sha,args.verify_published)
    pdfhash,pages = compile_tex(ROOT,out/"typeset")
    with tempfile.TemporaryDirectory(prefix="general-theta-r2-independent-") as temp:
        clean = Path(temp)/"source"
        clean.mkdir()
        for p in files(ROOT)+[ROOT/MANIFEST]:
            dest = clean/p.relative_to(ROOT)
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(p,dest)
        independent_diagnostics = audit(clean)
        second_hash,second_pages = compile_tex(clean,Path(temp)/"typeset")
        need(independent_diagnostics==diagnostics, "independent source replay differs")
        need((second_hash,second_pages)==(pdfhash,pages), "independent PDF differs")
    shutil.copyfile(out/"typeset/main.pdf",out/"paper.pdf")
    receipt = {"schema":"general-theta.restart-r2.build/1", "status":"success",
               "binding":binding, "diagnostics":diagnostics,
               "pdf_sha256":pdfhash,"pdf_pages":pages,"independent_pdf_sha256":second_hash,
               "independent_rebuild":True,"compiler_passes_per_build":3,
               "compiler":run(["pdflatex","--version"],ROOT).splitlines()[0],
               "python":sys.version.split()[0],"continuum_proof_by_replay":False}
    if args.verify_published:
        published = json.loads((ROOT/"evidence/BUILD_RECEIPT.json").read_text())
        need(sha((ROOT/"paper.pdf").read_bytes())==pdfhash==published["pdf_sha256"], "published PDF does not match exact reconstruction")
        need(published["binding"]["source_sha"]==args.source_sha, "published receipt source SHA mismatch")
        need(published["diagnostics"]==diagnostics, "published diagnostics mismatch")
        need(json.loads((ROOT/"evidence/REGRESSION.json").read_text())==diagnostics["regression"], "published regression mismatch")
        receipt["verified_final_head"] = binding["head"]
        receipt["contents_permission"] = "read (separate workflow job)"
        receipt["receipt_not_committed_back_to_verified_head"] = True
    (out/"BUILD_RECEIPT.json").write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
    (out/"REGRESSION.json").write_text(json.dumps(diagnostics["regression"],sort_keys=True,indent=2)+"\n")
    print(json.dumps(receipt,sort_keys=True,indent=2))

if __name__ == "__main__":
    main()
