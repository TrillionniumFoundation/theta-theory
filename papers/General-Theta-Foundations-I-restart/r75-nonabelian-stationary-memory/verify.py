#!/usr/bin/env python3
"""Native paired R75 verification with strict Git/source identity.

Strict mode requires --source-commit with the exact 40-hex current Git HEAD.
An uncommitted or standalone source can be compiled with --draft; that mode
never issues a final PASS. All output must be outside the source directory.
"""
from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from seal_source import (BASE_COMMIT, BASE_PATH, BASE_SOURCE_COMMIT, BASE_TREE, BODY_IDENTITIES,
                         COMPANION_PATH, COMPLETE_PRESERVATION, EXPECTED_CURRENT_STATEMENTS,
                         EXPECTED_OLD_STATEMENTS, EXPECTED_PREDECESSOR_FILES, INDEX, MANIFEST, OLD_INDEX,
                         REVIEW_BLOB, REVIEW_COMMIT, REVIEW_PATH, REVIEW_SHA256,
                         ROOT, SUFFIX_IDENTITY, file_identity, git_object, git_tree,
                         pinned_body_checks, read_json, require, sha256,
                         verify_manifest)

INHERITED_DIAGNOSTICS = [("r61", "diagnostics.py")] + [
    (f"r{n}", f"diagnostics_r{n}.py") for n in range(62, 73)
] + [("r73-normal-form", "diagnostics_r73_normal_form.py"),
     ("r73-certificates", "diagnostics_r73_certificates.py"),
     ("r74-contrast", "diagnostics_r74_contrast.py"),
     ("r74-noisy", "diagnostics_r74_noisy.py"),
     ("r74-instruments", "diagnostics_r74_instruments.py"),
     ("r74-quotient-challenge", "challenge_c2_four.py")]
EXPECTED_INHERITED_DIAGNOSTIC_SUITES = 18
# These two R75 scripts are fixed by the final integration plan. Missing files,
# non-PASS reports or incomplete suite execution fail verification.
R75_DIAGNOSTICS: list[tuple[str, str]] = [
    ("r75-nonabelian", "diagnostics_r75_nonabelian.py"),
    ("r75-conditional", "diagnostics_r75_conditional.py")]
EXPECTED_CURRENT_DIAGNOSTIC_SUITES = 20
DIAGNOSTICS = INHERITED_DIAGNOSTICS + R75_DIAGNOSTICS
STATEMENT_PREFIXES = {"thm", "lem", "prop", "cor", "ex"}
STATE: dict = {}


def progress(message: str) -> None:
    STATE["stage"] = message
    print(message, flush=True)


def run(command: list[str], cwd: Path, log: Path, env: dict,
        error_log: Path | None = None) -> None:
    with log.open("wb") as stdout:
        if error_log is None:
            result = subprocess.run(command, cwd=cwd, env=env, stdout=stdout,
                                    stderr=subprocess.STDOUT, check=False)
        else:
            with error_log.open("wb") as stderr:
                result = subprocess.run(command, cwd=cwd, env=env, stdout=stdout,
                                        stderr=stderr, check=False)
    require(result.returncode == 0,
            f"Command exited {result.returncode}: {command}; see {log}"
            + (f" and {error_log}" if error_log else ""))


def git(*arguments: str) -> str:
    result = subprocess.run(["git", *arguments], cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    require(result.returncode == 0,
            "Git identity check failed: git " + " ".join(arguments) + "; " + result.stderr.strip())
    return result.stdout.strip()


def strict_git_identity(source_commit: str, source_tree: str) -> dict:
    require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
            "Strict --source-commit must be a full 40-hex commit SHA, never a placeholder")
    require(git("cat-file", "-t", source_commit) == "commit", "Declared source object is not a commit")
    require(git("rev-parse", "HEAD") == source_commit,
            "Strict verification requires the actual current Git HEAD to equal --source-commit")
    repository = Path(git("rev-parse", "--show-toplevel")).resolve()
    prefix = ROOT.relative_to(repository).as_posix()
    require(prefix == "papers/General-Theta-Foundations-I-restart/r75-nonabelian-stationary-memory",
            "Unexpected source location in the repository")
    committed_tree = git("rev-parse", source_commit + ":" + prefix)
    require(committed_tree == source_tree,
            "Computed current source tree differs from the tree at the declared Git commit")
    require(git("rev-parse", source_commit + ":" + BASE_PATH) == BASE_TREE,
            "The current commit changed the complete inherited R74 source tree")
    require(git("rev-parse", BASE_SOURCE_COMMIT + ":" + BASE_PATH) == BASE_TREE
            and git("rev-parse", BASE_COMMIT + ":" + BASE_PATH) == BASE_TREE,
            "The fixed R74 source and publication do not share the expected paper tree")
    git("merge-base", "--is-ancestor", BASE_COMMIT, source_commit)
    changed = git("diff", "--no-relative", "--name-only", BASE_COMMIT, source_commit).splitlines()
    require(bool(changed) and all(name.startswith(prefix + "/") for name in changed),
            "The source commit changes files outside the independent R75 source directory")
    # This checks tracked working files when present; sparse omissions are not
    # falsely claimed materialized. The immutable committed R74 tree was checked above.
    git("diff", "--quiet", source_commit, "--", ":(top)" + BASE_PATH)
    raw_tree = subprocess.check_output(
        ["git", "ls-tree", "--full-tree", "-r", "-z", BASE_COMMIT + ":" + BASE_PATH], cwd=ROOT)
    predecessor_files = {}
    for record in raw_tree.split(b"\0"):
        if not record:
            continue
        metadata, path_raw = record.split(b"\t", 1)
        mode, kind, blob = metadata.decode("ascii").split()
        require(kind == "blob", "Unexpected non-blob in the complete R74 source tree")
        path = path_raw.decode("utf-8")
        require(path not in predecessor_files, "Duplicate predecessor source path")
        predecessor_files[path] = {"mode": mode, "git_blob": blob}
    preservation = read_json(COMPLETE_PRESERVATION)
    preserved = {row["predecessor_path"]: row for row in preservation["files"]}
    require(len(predecessor_files) == EXPECTED_PREDECESSOR_FILES
            and set(predecessor_files) == set(preserved),
            "The complete 275-file preservation map differs from the actual R74 Git tree")
    for path, fixed in predecessor_files.items():
        row = preserved[path]
        local = file_identity(ROOT / row["current_preserved_path"])
        require(fixed["git_blob"] == row["git_blob"] == local["git_blob"]
                and fixed["mode"] == local["mode"],
                "Preserved complete-file identity differs from the actual R74 tree: " + path)
    for row in read_json(BODY_IDENTITIES):
        require(git("rev-parse", BASE_COMMIT + ":" + BASE_PATH + "/" + row["path"])
                == row["git_blob"],
                "Retained-body pointer differs from the actual predecessor commit: " + row["path"])
    suffix_record = read_json(SUFFIX_IDENTITY)
    predecessor_supplement = subprocess.check_output(
        ["git", "show", BASE_COMMIT + ":" + BASE_PATH + "/supplement.tex"], cwd=ROOT)
    marker = suffix_record["retained_start_marker"].encode("utf-8")
    require(predecessor_supplement.count(marker) == 1,
            "Predecessor supplement suffix marker missing or ambiguous")
    predecessor_suffix = predecessor_supplement[predecessor_supplement.index(marker):]
    require(len(predecessor_suffix) == suffix_record["suffix_bytes"]
            and sha256(predecessor_suffix) == suffix_record["suffix_sha256"],
            "Retained supplement suffix identity does not match the actual predecessor Git blob")
    old_index_blob = git_object("blob", (ROOT / OLD_INDEX).read_bytes())
    require(git("rev-parse", BASE_COMMIT + ":" + BASE_PATH + "/THEOREM_INDEX.json")
            == old_index_blob, "The inherited index is not the exact R74 index body")
    require(len(INHERITED_DIAGNOSTICS) == EXPECTED_INHERITED_DIAGNOSTIC_SUITES,
            "The fixed inherited 18-suite diagnostic inventory differs")
    for _, filename in INHERITED_DIAGNOSTICS:
        require(git("rev-parse", BASE_COMMIT + ":" + BASE_PATH + "/" + filename)
                == git_object("blob", (ROOT / filename).read_bytes()),
                "Inherited diagnostic source differs from the actual R74 commit: " + filename)
    return {"head": source_commit, "repository": str(repository), "paper_path": prefix,
            "committed_paper_tree": committed_tree, "r74_committed_paper_tree": BASE_TREE,
            "r74_tracked_worktree_unchanged": True,
            "r74_ancestry_verified": True, "r74_complete_preserved_files_verified": len(preserved),
            "predecessor_supplement_suffix_verified": True, "changed_source_paths": len(changed),
            "changed_paths_confined_to_new_source": True,
            "inherited_diagnostic_sources_verified": len(INHERITED_DIAGNOSTICS),
            "source_epoch": int(git("show", "-s", "--format=%ct", source_commit))}


def diagnostic_counts(report: dict, name: str) -> tuple[int, int, int]:
    require(str(report.get("status", "")).lower() in {"pass", "passed"},
            f"Diagnostic {name} did not report PASS/passed")
    total = report.get("total_checks")
    require(type(total) is int and total > 0, f"Diagnostic {name} has no positive actual check count")
    groups = report.get("checks_by_group", report.get("groups"))
    require(isinstance(groups, dict) and all(type(v) is int and v >= 0 for v in groups.values())
            and sum(groups.values()) == total, f"Diagnostic {name} has inconsistent grouped counts")
    if "exact_checks" in report:
        exact = report["exact_checks"]
        floating = report.get("floating_checks", report.get("floating_probes"))
    else:
        require(all(k.startswith("exact") or k.startswith("float") for k in groups),
                f"Unclassified exact/floating groups in {name}")
        exact = sum(v for k, v in groups.items() if k.startswith("exact"))
        floating = sum(v for k, v in groups.items() if k.startswith("float"))
    require(type(exact) is int and type(floating) is int and exact >= 0 and floating >= 0
            and exact + floating == total, f"Diagnostic {name} has inconsistent arithmetic counts")
    return total, exact, floating


def run_diagnostics(out: Path, env: dict) -> dict:
    require(len(INHERITED_DIAGNOSTICS) == EXPECTED_INHERITED_DIAGNOSTIC_SUITES,
            "The inherited 18-suite diagnostic inventory differs")
    require(type(EXPECTED_CURRENT_DIAGNOSTIC_SUITES) is int
            and EXPECTED_CURRENT_DIAGNOSTIC_SUITES == 20
            and len(DIAGNOSTICS) == EXPECTED_CURRENT_DIAGNOSTIC_SUITES,
            "The explicit R75 diagnostic inventory and total have not been finalized")
    require(len({name for name, _ in DIAGNOSTICS}) == len(DIAGNOSTICS)
            and len({filename for _, filename in DIAGNOSTICS}) == len(DIAGNOSTICS),
            "Duplicate diagnostic suite or source file")
    records = {}
    for name, filename in DIAGNOSTICS:
        progress("Finite diagnostics: " + name + " (ordinary and optimized)")
        code = (ROOT / filename).read_text(encoding="utf-8")
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(code))),
                "A diagnostic uses assert checks that disappear under -O: " + filename)
        normal, optimized = out / (name + "-normal.json"), out / (name + "-optimized.json")
        normal_error = out / (name + "-normal.stderr.txt")
        optimized_error = out / (name + "-optimized.stderr.txt")
        normal_command = [sys.executable, filename]
        optimized_command = [sys.executable, "-O", filename]
        run(normal_command, ROOT, normal, env, normal_error)
        run(optimized_command, ROOT, optimized, env, optimized_error)
        require(normal.read_bytes() == optimized.read_bytes(),
                "Ordinary/optimized diagnostic output differs: " + name)
        report = json.loads(normal.read_text(encoding="utf-8"))
        total, exact, floating = diagnostic_counts(report, name)
        records[name] = {"script": filename, "script_sha256": sha256((ROOT / filename).read_bytes()),
                         "status": "PASS", "total_checks": total, "exact_checks": exact,
                         "floating_checks": floating, "ordinary_optimized_identity": True,
                         "assert_statements_in_script": 0,
                         "ordinary_stdout": normal.name, "optimized_stdout": optimized.name,
                         "stdout_sha256": sha256(normal.read_bytes()),
                         "ordinary_stderr": normal_error.name, "optimized_stderr": optimized_error.name,
                         "commands": [normal_command, optimized_command], "report": report}
    require(len(records) == EXPECTED_CURRENT_DIAGNOSTIC_SUITES,
            "The complete declared R61–R75 diagnostic suite was not executed")
    return records


def cross_labels(build: Path, name: str) -> None:
    lines = (build / (name + ".aux")).read_text(encoding="utf-8").splitlines()
    # AMS tocindent dimensions are not cross-document reference labels.
    kept = [line for line in lines if line.startswith(r"\newlabel{")
            and not line.startswith(r"\newlabel{tocindent")]
    (build / (name + "-refs.aux")).write_text("\n".join(kept) + "\n", encoding="utf-8")


def aux_labels(build: Path, name: str) -> dict[str, tuple[str, str]]:
    text = (build / (name + ".aux")).read_text(encoding="utf-8")
    records = re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}", text)
    result = {}
    for label, number, page in records:
        if label.startswith("tocindent"):
            continue
        require(label not in result, "Duplicate native auxiliary label: " + label)
        result[label] = (number, page)
    return result


def without_comments(text: str) -> str:
    return "\n".join(re.split(r"(?<!\\)%", line, maxsplit=1)[0] for line in text.splitlines())


def active_tex(stem: str) -> list[str]:
    seen, active = set(), []

    def visit(relative: str) -> None:
        if not relative.endswith(".tex"):
            relative += ".tex"
        require(not Path(relative).is_absolute() and ".." not in Path(relative).parts,
                "Unexpected TeX input outside the current source: " + relative)
        if relative in seen:
            return
        path = ROOT / relative
        require(path.is_file(), "Missing active native TeX input: " + relative)
        seen.add(relative)
        active.append(relative)
        text = without_comments(path.read_text(encoding="utf-8"))
        for target in re.findall(r"\\(?:input|include)\{([^}]+)\}", text):
            visit(target)

    visit(stem + ".tex")
    return active


def make_theorem_index(paired: Path) -> dict:
    require(type(EXPECTED_CURRENT_STATEMENTS) is int
            and EXPECTED_CURRENT_STATEMENTS > EXPECTED_OLD_STATEMENTS,
            "The explicit R75 statement count has not been finalized")
    statements, all_labels = [], set()
    old_labels = {row["label"] for row in read_json(OLD_INDEX)["statements"]}
    for document in ("main", "supplement"):
        origins = {}
        for relative in active_tex(document):
            text = without_comments((ROOT / relative).read_text(encoding="utf-8"))
            for label in re.findall(r"\\label\{([^}]+)\}", text):
                if label.split(":", 1)[0] in STATEMENT_PREFIXES:
                    require(label not in origins, "Duplicate statement label in active source: " + label)
                    origins[label] = relative
        resolved = aux_labels(paired, document)
        compiled = {key for key in resolved if key.split(":", 1)[0] in STATEMENT_PREFIXES}
        require(compiled == set(origins), "Active source and compiled statement labels differ in " + document)
        for label, (number, page) in resolved.items():
            if label not in origins:
                continue
            require(label not in all_labels, "Statement occurs in both paired documents: " + label)
            require(bool(number) and page.isdigit(), "Unresolved theorem number/page: " + label)
            all_labels.add(label)
            statements.append({"document": document, "number": number, "page": int(page),
                               "label": label, "source": origins[label],
                               "inherited_from_r74": label in old_labels})
    require(old_labels <= all_labels,
            "Inherited statement labels missing from the compiled pair: " + ", ".join(sorted(old_labels - all_labels)))
    require(len(old_labels) == EXPECTED_OLD_STATEMENTS and len(statements) == EXPECTED_CURRENT_STATEMENTS,
            f"Expected {EXPECTED_OLD_STATEMENTS} retained and {EXPECTED_CURRENT_STATEMENTS} current indexed statements, found {len(old_labels)} and {len(statements)}")
    return {"schema": "theta.r75.compiled-theorem-index.v1",
            "source": "Actual native main.aux and supplement.aux; strict verification compares every source/label/number/page.",
            "indexed_statement_count": len(statements), "inherited_statement_count": len(old_labels),
            "new_statement_count": len(all_labels - old_labels), "statements": statements}


def check_native_log(build: Path, stem: str, document: str) -> None:
    log = (build / (stem + ".log")).read_text(encoding="utf-8", errors="replace")
    forbidden = ("undefined references", "undefined citations", "multiply defined",
                 r"Overfull \hbox", r"Overfull \vbox", "Label(s) may have changed")
    bad = [phrase for phrase in forbidden if phrase in log]
    undefined_details = bool(re.search(r"LaTeX Warning: (?:Reference|Citation).*?undefined", log, re.S))
    require(not bad and not undefined_details,
            "Final native warnings in " + document + ": " + ", ".join(bad)
            + ("; undefined reference/citation" if undefined_details else ""))


def compile_documents(out: Path, env: dict) -> tuple[list[dict], dict]:
    paired, companion = out / "paired", out / "companion"
    paired.mkdir()
    companion.mkdir()
    pair_env = dict(env, TEXINPUTS=str(paired) + os.pathsep + env.get("TEXINPUTS", ""))
    commands = {}
    for pass_number in range(1, 4):
        for stem in ("main", "supplement"):
            progress(f"Native paired LaTeX: {stem}, pass {pass_number}/3")
            command = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
                       "-no-shell-escape", "-recorder", f"-output-directory={paired}", stem + ".tex"]
            run(command, ROOT, paired / f"{stem}-pass-{pass_number}.txt", pair_env)
            cross_labels(paired, stem)
            commands[stem] = command
    companion_command = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
                         "-no-shell-escape", "-recorder", f"-output-directory={companion}", "main.tex"]
    for pass_number in range(1, 4):
        progress(f"Native retained R58 LaTeX: pass {pass_number}/3")
        run(companion_command, ROOT / COMPANION_PATH, companion / f"pass-{pass_number}.txt", env)

    index = make_theorem_index(paired)
    (out / INDEX).write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    documents = []
    definitions = [
        ("manuscript", paired, "main", "General_Theta_Foundations_I_R75.pdf", commands["main"]),
        ("supplement", paired, "supplement", "General_Theta_Foundations_I_R75_Supplement.pdf", commands["supplement"]),
        ("companion", companion, "main", "General_Theta_Foundations_I_R75_Retained_Companion_R58.pdf", companion_command)]
    for name, build, stem, filename, command in definitions:
        check_native_log(build, stem, name)
        pdf = out / filename
        shutil.copyfile(build / (stem + ".pdf"), pdf)
        text_path = out / (Path(filename).stem + ".txt")
        run(["pdftotext", "-layout", str(pdf), str(text_path)], ROOT,
            build / (stem + "-pdftotext.txt"), env)
        info_path = build / (stem + "-pdfinfo.txt")
        run(["pdfinfo", str(pdf)], ROOT, info_path, env)
        info = info_path.read_text(encoding="utf-8", errors="replace")
        found = re.search(r"^Pages:\s+(\d+)", info, re.M)
        require(found is not None and int(found.group(1)) > 0, "Cannot read PDF page count: " + filename)
        documents.append({"document": name, "file": filename, "pages": int(found.group(1)),
                          "sha256": sha256(pdf.read_bytes()), "bytes": pdf.stat().st_size,
                          "text_file": text_path.name, "text_sha256": sha256(text_path.read_bytes()),
                          "passes": 3, "command": command, "shell_escape": False,
                          "final_overfull_or_undefined_warnings": False})
    return documents, index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path, help="fresh output directory outside this source")
    parser.add_argument("--source-commit", help="full 40-hex Git HEAD; mandatory for strict final verification")
    parser.add_argument("--draft", action="store_true", help="compile an unsealed source without a final PASS")
    parser.add_argument("--skip-diagnostics", action="store_true", help="draft compile only; prohibited in strict mode")
    args = parser.parse_args()
    require(not args.skip_diagnostics or args.draft, "--skip-diagnostics is permitted only with --draft")
    require(not (args.draft and args.source_commit), "Draft mode cannot claim an exact source-commit verification")
    require(args.draft or (args.source_commit and re.fullmatch(r"[0-9a-fA-F]{40}", args.source_commit)),
            "Strict mode requires --source-commit with a full 40-hex SHA")
    out = args.out.resolve()
    require(out != ROOT and ROOT not in out.parents, "Build output must be outside the immutable source")
    require(not out.exists() or (out.is_dir() and not any(out.iterdir())),
            "Build output must be fresh/empty; preserve earlier failed runs under their own paths")
    out.mkdir(parents=True, exist_ok=True)
    STATE.update({"out": str(out), "mode": "draft" if args.draft else "strict",
                  "declared_source_commit": args.source_commit, "started_utc": dt.datetime.now(dt.timezone.utc).isoformat()})
    for tool in ("pdflatex", "pdftotext", "pdfinfo"):
        require(shutil.which(tool) is not None, "Missing native executable: " + tool)

    progress("Checking current source and pinned inherited mathematical bodies")
    if args.draft:
        manifest, retention = None, pinned_body_checks()
    else:
        manifest, retention = verify_manifest()
    before = git_tree()
    identity = None
    if not args.draft:
        progress("Binding the exact current Git HEAD and preserved R74 tree")
        identity = strict_git_identity(args.source_commit.lower(), before)
    source_epoch = identity["source_epoch"] if identity else 1792540800
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1",
               PYTHONDONTWRITEBYTECODE="1", SOURCE_DATE_EPOCH=str(source_epoch), TZ="UTC")
    diagnostics = {} if args.skip_diagnostics else run_diagnostics(out, env)
    documents, index = compile_documents(out, env)
    matched_index = (ROOT / INDEX).is_file() and read_json(INDEX) == index
    if not args.draft:
        require(matched_index, "The sealed theorem index does not match the actual paired label/number/page map")
        verify_manifest()
    after = git_tree()
    if not args.draft:
        require(before == after, "The source mutated during strict verification")
        require(git("rev-parse", "HEAD") == args.source_commit.lower(), "Git HEAD changed during verification")
    progress("Writing the actual execution receipt")
    total = sum(row["total_checks"] for row in diagnostics.values())
    exact = sum(row["exact_checks"] for row in diagnostics.values())
    floating = sum(row["floating_checks"] for row in diagnostics.values())
    receipt = {"schema": "theta.r75.native-verification.v1",
               "status": "DRAFT_COMPILE_COMPLETE" if args.draft else "PASS",
               "mode": "draft" if args.draft else "strict", "started_utc": STATE["started_utc"],
               "completed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
               "declared_source_commit": args.source_commit.lower() if args.source_commit else None,
               "source_commit_verified": not args.draft, "git_identity": identity,
               "source_git_tree_before": before, "source_git_tree_after": after,
               "source_unchanged_during_build": before == after,
               "source_manifest_sha256": sha256((ROOT / MANIFEST).read_bytes()) if manifest else None,
               "source_files_verified": len(manifest["files"]) + 1 if manifest else None,
               "retention": retention,
               "controlling_report": {"commit": REVIEW_COMMIT, "path": REVIEW_PATH,
                                      "git_blob": REVIEW_BLOB, "sha256": REVIEW_SHA256,
                                      "local_body_verified": True},
               "documents": documents, "diagnostics": diagnostics,
               "diagnostic_suite_count": len(diagnostics), "diagnostics_skipped": args.skip_diagnostics,
               "ordinary_optimized_identity": True if diagnostics else None,
               "total_checks": total, "exact_finite_checks": exact, "floating_finite_checks": floating,
               "compiled_statement_count": len(index["statements"]),
               "inherited_statement_count": EXPECTED_OLD_STATEMENTS,
               "sealed_theorem_index_matched": bool(matched_index),
               "generated_theorem_index_sha256": sha256((out / INDEX).read_bytes()),
               "python": sys.version, "python_executable": sys.executable,
               "platform": platform.platform(), "source_date_epoch": source_epoch,
               "pdflatex": subprocess.check_output(["pdflatex", "--version"], text=True).splitlines()[0],
               "visual_pdf_review": "Separate rendered-page inspection is recorded in the publication evidence, not inferred by this script.",
               "limitations": [
                   "Native compilation and finite exact/floating diagnostics do not prove continuum theorems or mathematical novelty.",
                   "This is not a proof-assistant verification, independent human referee assessment, or editorial decision.",
                   "General real quantifier elimination is proved available but was not executed by these diagnostics.",
                   "A local strict PASS is not a hosted CI result or a remote-publication receipt.",
                   "Draft mode never authenticates a committed manuscript, may skip diagnostics, and never reports a final PASS."]}
    (out / "BUILD_RECEIPT.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "documents": documents,
                      "checks": total, "exact_checks": exact, "floating_probes": floating,
                      "compiled_statement_count": len(index["statements"]),
                      "source_git_tree": after, "receipt": str(out / "BUILD_RECEIPT.json")}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        if "out" in STATE:
            failure = {"schema": "theta.r75.native-build-failure.v1", "status": "FAILED",
                       **STATE, "failed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                       "error": str(exc), "error_type": type(exc).__name__,
                       "limitation": "A failed or partial attempt is not a verification pass."}
            (Path(STATE["out"]) / "BUILD_FAILURE.json").write_text(
                json.dumps(failure, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        raise
