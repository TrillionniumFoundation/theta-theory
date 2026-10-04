#!/usr/bin/env python3
"""Qualify one pinned manuscript; retain evidence even when qualification fails.

Freeze SOURCE_PINS.json only after editing is complete. A development run uses
--allow-dirty and never claims qualification of a Git commit. A publication run
requires --expected-head and verifies the committed bytes, the checkout, the
preserved Git trees, finite diagnostics, and the primary TeX build.
"""
from __future__ import annotations

import argparse
from collections import Counter
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = PurePosixPath("papers/A2-v37-stationary-rigidity")
WORKFLOW = ".github/workflows/a2-v37-verify.yml"
MANIFEST_NAME = "SOURCE_PINS.json"
SCHEMA = "a2-v37-validation-1"
MANIFEST_SCHEMA = "a2-v37-source-pins-1"
AUTHOR_COMMIT = "2559749a038fd2b5ec46d7cc74fdb4bd844b266a"
REVIEW_COMMIT = "3c6b195c183df2c52e58e25cf59f7e3fcba07fc3"
PRESERVED_TREES = {
    "reviewed_v36": {
        "commit": AUTHOR_COMMIT,
        "path": "papers/A2-v36-stationary-boundary",
        "git_tree": "3cc6234334105c6e9be005e19d05df696aa1d923",
    },
    "controlling_review": {
        "commit": REVIEW_COMMIT,
        "path": "reviews/a2-v36-external-harsh-top4-rereview-2026-10-04",
        "git_tree": "525207754a23a6f70f0e7034cc41f13ead111522",
    },
    "retained_v35": {
        "commit": "70c055e1ff090d58ecd61a5644e0fa62a7766f13",
        "path": "papers/A2-v35-self-calibrated-stationary",
        "git_tree": "80780f2590aec6d471985835b1b334774b23675f",
    },
    "retained_v34": {
        "commit": "ed3876b8a82e2c46bc1533457978c15fea1a2114",
        "path": "papers/A2-v34-calibration-experiments",
        "git_tree": "66f504938686e4b4920cdf250a92644bd1eae1d9",
    },
    "retained_v35_review": {
        "commit": "985d798e172d38c0a9df2a068fe414b2fd13bcbc",
        "path": "reviews/a2-v35-external-harsh-top4-rereview-2026-10-04",
        "git_tree": "2abfbf4ce4d99884c0107bf0caabcf5e70608584",
    },
}
REQUIRED_FILES = {
    "main.tex", "references.tex", "README.md", "RESPONSE_TO_REFEREES.md",
    "PROOF_LEDGER.md", "HISTORICAL_DERIVATION_AUDIT.md",
    "LITERATURE_AUDIT.md", "SUBMISSION_MAP.md",
    "tools/validate_v37.py", "tools/test_contract_v37.py", "tools/verify_v37.py",
}
GENERATED_TOP_LEVEL = {"build", "verification"}
GENERATED_EVIDENCE = {
    "receipt.json", "artifact-binding.json", "A2-v37-primary.pdf",
    "A2-v37-journal-source.zip", "A2-v37-repository-source.zip",
    "final-main.log", "final-main.fls", "source-pins.json",
}


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, check=False,
    )
    if result.returncode:
        raise ValueError("Git command failed: " + " ".join(args) + ": "
                         + result.stderr.strip())
    return result.stdout.strip()


def repository_root(paper: Path = ROOT) -> Path:
    repo = Path(git(paper, "rev-parse", "--show-toplevel")).resolve()
    if paper.resolve() != repo / Path(PACKAGE):
        raise ValueError("paper is not at its declared repository path")
    return repo


def collect_sources(paper: Path, repo: Path) -> dict[str, str]:
    """Hash every source file, including unknown additions, outside evidence."""
    if paper.is_symlink():
        raise ValueError("symlink at paper root")
    paths: list[Path] = []
    for current, directories, names in os.walk(paper, followlinks=False):
        base = Path(current)
        retained = []
        for name in directories:
            child = base / name
            if child.is_symlink():
                raise ValueError("symlink in paper tree: " + str(child))
            if name == "__pycache__":
                continue
            if base == paper and name in GENERATED_TOP_LEVEL:
                continue
            retained.append(name)
        directories[:] = sorted(retained)
        for name in sorted(names):
            path = base / name
            if path.is_symlink() or not path.is_file():
                raise ValueError("non-regular source file: " + str(path))
            if path == paper / MANIFEST_NAME or path.suffix in {".pyc", ".pyo"}:
                continue
            paths.append(path)
    workflow = repo / WORKFLOW
    if workflow.is_symlink() or not workflow.is_file():
        raise ValueError("missing or non-regular qualification workflow")
    paths.append(workflow)
    actual = {p.relative_to(repo).as_posix(): digest(p) for p in sorted(paths)}
    required = {str(PACKAGE / name) for name in REQUIRED_FILES} | {WORKFLOW}
    missing = sorted(required - actual.keys())
    if missing:
        raise ValueError("required sources missing: " + ", ".join(missing))
    return actual


def tex_input_closure(paper: Path) -> list[str]:
    """Require literal, internal, reachable TeX inputs for the journal ZIP."""
    pending = ["main.tex"]
    visited: set[str] = set()
    while pending:
        name = pending.pop()
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("TeX input escapes the primary package: " + name)
        name = relative.as_posix()
        if name in visited:
            continue
        path = paper / name
        if path.is_symlink() or not path.is_file():
            raise ValueError("missing or non-regular TeX input: " + name)
        visited.add(name)
        text = re.sub(r"(?<!\\)%[^\n]*", "", path.read_text(encoding="utf-8"))
        for command in re.finditer(r"\\(?:input|include)\s*\{([^}]+)\}", text):
            target = command.group(1).strip()
            if "\\" in target or not target:
                raise ValueError("non-literal TeX input: " + target)
            if not target.endswith(".tex"):
                target += ".tex"
            pending.append(target)
    all_tex = {
        p.relative_to(paper).as_posix() for p in paper.rglob("*.tex")
        if p.relative_to(paper).parts[0] not in GENERATED_TOP_LEVEL
    }
    if visited != all_tex:
        raise ValueError("inactive manuscript TeX files: "
                         + ", ".join(sorted(all_tex - visited)))
    return sorted(visited)


def manifest_document(actual: dict[str, str], tex_inputs: list[str]) -> dict:
    return {
        "schema": MANIFEST_SCHEMA,
        "repository": "TrillionniumFoundation/theta-theory",
        "paper_directory": str(PACKAGE),
        "journal_documents": ["main.tex"],
        "reviewed_author_commit": AUTHOR_COMMIT,
        "controlling_review_commit": REVIEW_COMMIT,
        "preserved_trees": PRESERVED_TREES,
        "workflow": WORKFLOW,
        "source_sha256": actual,
        "tex_inputs": tex_inputs,
        "excluded_generated_paths": ["build/", "verification/", "**/__pycache__/",
                                     "**/*.pyc", "**/*.pyo", MANIFEST_NAME],
        "manifest_binding": "manifest bytes are bound by the Git commit, receipt, and source archive",
        "preservation_contract": "all active v36 labels and every v36 proof body remain in the active primary",
        "formal_proof_certificate": False,
        "physical_sensor_executed": False,
    }


def validate_manifest(pins: dict, actual: dict[str, str], tex_inputs: list[str]) -> None:
    expected = manifest_document(actual, tex_inputs)
    if not isinstance(pins, dict) or set(pins) != set(expected):
        raise ValueError("incorrect or incomplete manifest fields")
    for name in expected:
        if pins[name] != expected[name]:
            if name == "source_sha256" and isinstance(pins[name], dict):
                frozen = pins[name]
                missing = sorted(frozen.keys() - actual.keys())
                extra = sorted(actual.keys() - frozen.keys())
                changed = sorted(k for k in frozen.keys() & actual.keys()
                                 if frozen[k] != actual[k])
                raise ValueError("source manifest mismatch: missing=" + repr(missing)
                                 + "; extra=" + repr(extra) + "; changed=" + repr(changed))
            raise ValueError("manifest field differs: " + name)


def validate_head_binding(expected: str | None, actual: str, dirty: str,
                          allow_dirty: bool) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", actual):
        raise ValueError("invalid actual Git commit")
    if allow_dirty:
        if expected is not None:
            raise ValueError("development mode cannot claim an expected commit")
        return "development_source_content"
    if not expected or not re.fullmatch(r"[0-9a-f]{40}", expected):
        raise ValueError("an exact 40-character expected Git commit is required")
    if expected != actual:
        raise ValueError("expected and actual Git commits differ")
    if dirty:
        raise ValueError("tracked checkout is not clean")
    return "exact_expected_checkout"


def verify_preserved_trees(repo: Path) -> dict[str, str]:
    observed = {}
    for name, pin in PRESERVED_TREES.items():
        tree = git(repo, "rev-parse", "HEAD:" + pin["path"])
        if tree != pin["git_tree"]:
            raise ValueError("preserved Git tree differs: " + name)
        if git(repo, "diff", "--name-only", "HEAD", "--", pin["path"]):
            raise ValueError("preserved checkout source changed: " + name)
        observed[name] = tree
    return observed


def verify_committed_bytes(repo: Path, source_hashes: dict[str, str],
                           manifest_hash: str) -> None:
    expected = {**source_hashes, str(PACKAGE / MANIFEST_NAME): manifest_hash}
    for path, sha in expected.items():
        result = subprocess.run(
            ["git", "-C", str(repo), "show", "HEAD:" + path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if result.returncode or digest_bytes(result.stdout) != sha:
            raise ValueError("source is absent from, or differs from, HEAD: " + path)


def read_reviewed_inputs(repo: Path) -> dict[str, str]:
    """Read the preserved v36 inputs at HEAD; historical commits need not exist."""
    directory = PRESERVED_TREES["reviewed_v36"]["path"]
    pending, inputs = ["main.tex"], {}
    while pending:
        name = pending.pop()
        if name in inputs:
            continue
        relative = PurePosixPath(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError("reviewed TeX input escapes its package")
        result = subprocess.run(
            ["git", "-C", str(repo), "show", "HEAD:" + directory + "/" + name],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        )
        if result.returncode:
            raise ValueError("reviewed TeX input unavailable at HEAD: " + name)
        text = result.stdout.decode("utf-8")
        inputs[name] = text
        uncommented = re.sub(r"(?<!\\)%[^\n]*", "", text)
        for match in re.finditer(r"\\(?:input|include)\s*\{([^}]+)\}", uncommented):
            target = match.group(1).strip()
            if "\\" in target or not target:
                raise ValueError("non-literal reviewed TeX input")
            pending.append(target if target.endswith(".tex") else target + ".tex")
    return inputs


def verify_preservation(reviewed: dict[str, str], current: dict[str, str]) -> dict:
    old_text, new_text = "\n".join(reviewed.values()), "\n".join(current.values())
    labels = re.compile(r"\\label\{([^{}]+)\}")
    old_labels, new_labels = Counter(labels.findall(old_text)), Counter(labels.findall(new_text))
    missing_labels = old_labels - new_labels
    if missing_labels:
        raise ValueError("reviewed labels removed: " + ", ".join(sorted(missing_labels)))
    duplicates = sorted(label for label, count in new_labels.items() if count > 1)
    if duplicates:
        raise ValueError("duplicate current labels: " + ", ".join(duplicates))
    proofs = re.compile(r"\\begin\{proof\}(?:\[[^\]]*\])?(.*?)\\end\{proof\}", re.S)
    old_proofs, new_proofs = Counter(proofs.findall(old_text)), Counter(proofs.findall(new_text))
    missing_proofs = old_proofs - new_proofs
    if missing_proofs:
        raise ValueError(str(sum(missing_proofs.values())) + " reviewed proof bodies changed or removed")
    if not old_labels or not old_proofs:
        raise ValueError("reviewed source has no auditable labels or proof bodies")
    formal = re.compile(r"\\begin\{(?:theorem|lemma|proposition|corollary)\}")
    return {
        "reviewed_labels": sum(old_labels.values()), "current_labels": sum(new_labels.values()),
        "all_reviewed_labels_retained": True,
        "reviewed_proof_bodies": sum(old_proofs.values()),
        "current_proof_bodies": sum(new_proofs.values()),
        "reviewed_proof_bodies_byte_identical": True,
        "reviewed_formal_blocks": len(formal.findall(old_text)),
        "current_formal_blocks": len(formal.findall(new_text)),
    }


def deterministic_zip(destination: Path, repo: Path,
                      members: dict[str, tuple[str, str]]) -> None:
    """members maps archive names to (repository path, expected SHA-256)."""
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for archive_name, (source_name, expected) in sorted(members.items()):
            name = PurePosixPath(archive_name)
            if name.is_absolute() or ".." in name.parts:
                raise ValueError("unsafe source archive member")
            data = (repo / source_name).read_bytes()
            if digest_bytes(data) != expected:
                raise ValueError("source changed before packaging: " + source_name)
            entry = zipfile.ZipInfo(name.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)


def inspect_tex_log(text: str) -> list[str]:
    return re.findall(r"^.*(?:Warning|Overfull|Underfull|undefined|^!).*$", text, re.M)


def verify_recorded_inputs(fls: Path, paper: Path, repo: Path,
                           build: Path, sources: dict[str, str]) -> None:
    for line in fls.read_text(errors="replace").splitlines():
        if not line.startswith("INPUT "):
            continue
        path = Path(line[6:])
        if not path.is_absolute():
            path = paper / path
        path = path.resolve()
        if path.is_relative_to(build):
            continue
        if path.is_relative_to(repo):
            relative = path.relative_to(repo).as_posix()
            if relative not in sources:
                raise ValueError("TeX read an unpinned repository input: " + relative)


def prepare_evidence_directory(out: Path) -> None:
    if out.is_symlink():
        raise ValueError("symlink evidence directory")
    out.mkdir(parents=True, exist_ok=True)
    for path in out.iterdir():
        if path.is_symlink() or not path.is_file():
            raise ValueError("unexpected entry in evidence directory: " + path.name)
        if path.name not in GENERATED_EVIDENCE and not path.name.endswith(".log"):
            raise ValueError("evidence directory contains an unrecognized file: " + path.name)
    for path in out.iterdir():
        path.unlink()


def qualify(args: argparse.Namespace) -> int:
    out = Path(args.output_dir).resolve() if args.output_dir else ROOT / "verification/current"
    record = {
        "schema": SCHEMA, "status": "running",
        "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source_commit": None, "expected_head": args.expected_head,
        "execution_kind": "development_source_content" if args.allow_dirty else "exact_expected_checkout",
        "exact_commit_qualified": False,
        "github_sha": os.environ.get("GITHUB_SHA"),
        "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        "platform": platform.platform(), "python": sys.version,
        "commands": [], "diagnostics": [], "documents": [],
        "formal_proof_certificate": False, "physical_sensor_executed": False,
        "scope": "current finite diagnostics, current primary build, and preserved Git tree identities",
    }
    build: Path | None = None
    evidence_ready = False
    try:
        prepare_evidence_directory(out)
        evidence_ready = True
        repo = repository_root()
        head = git(repo, "rev-parse", "HEAD")
        record["source_commit"] = head
        tracked_status = git(repo, "status", "--porcelain", "--untracked-files=no")
        record["tracked_status_at_start"] = tracked_status
        record["execution_kind"] = validate_head_binding(
            args.expected_head, head, tracked_status, args.allow_dirty)
        if record["github_sha"] and record["github_sha"] != head:
            raise ValueError("GitHub trigger differs from checkout")
        pins_path = ROOT / MANIFEST_NAME
        if pins_path.is_symlink() or not pins_path.is_file():
            raise ValueError("missing or non-regular source manifest")
        pins_data = pins_path.read_bytes()
        pins = json.loads(pins_data)
        before = collect_sources(ROOT, repo)
        tex_inputs = tex_input_closure(ROOT)
        validate_manifest(pins, before, tex_inputs)
        manifest_hash = digest_bytes(pins_data)
        record["source_manifest_sha256"] = manifest_hash
        record["source_sha256"] = before
        record["preserved_git_trees"] = verify_preserved_trees(repo)
        record["active_content_preservation"] = verify_preservation(
            read_reviewed_inputs(repo),
            {name: (ROOT / name).read_text(encoding="utf-8") for name in tex_inputs})
        if not args.allow_dirty:
            verify_committed_bytes(repo, before, manifest_hash)
        (out / "source-pins.json").write_bytes(pins_data)
        journal_members = {name: (str(PACKAGE / name), before[str(PACKAGE / name)])
                           for name in tex_inputs}
        source_members = {name: (name, sha) for name, sha in before.items()}
        source_members[str(PACKAGE / MANIFEST_NAME)] = (str(PACKAGE / MANIFEST_NAME), manifest_hash)
        deterministic_zip(out / "A2-v37-journal-source.zip", repo, journal_members)
        deterministic_zip(out / "A2-v37-repository-source.zip", repo, source_members)
        record["journal_members"] = sorted(journal_members)
        record["repository_source_members"] = sorted(source_members)
        source_epoch = git(repo, "show", "-s", "--format=%ct", "HEAD")
        command_env = {
            **os.environ, "PYTHONDONTWRITEBYTECODE": "1", "TERM": "dumb",
            "LC_ALL": "C", "TZ": "UTC", "SOURCE_DATE_EPOCH": source_epoch,
            "FORCE_SOURCE_DATE": "1",
        }
        record["source_date_epoch"] = int(source_epoch)

        def run(argv: list[str], label: str, timeout: int = 180) -> str:
            command = {"argv": argv, "cwd": str(PACKAGE), "log": label + ".log"}
            record["commands"].append(command)
            log = out / command["log"]
            try:
                result = subprocess.run(
                    argv, cwd=ROOT, env=command_env, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True, errors="replace",
                    check=False, timeout=timeout,
                )
                command["exit_code"] = result.returncode
                log.write_text(result.stdout, encoding="utf-8")
            except (OSError, subprocess.TimeoutExpired) as exc:
                command["exit_code"] = None
                partial = getattr(exc, "stdout", None) or ""
                if isinstance(partial, bytes):
                    partial = partial.decode("utf-8", errors="replace")
                log.write_text(partial + "\n" + str(exc) + "\n", encoding="utf-8")
                command["sha256"] = digest(log)
                raise RuntimeError(label + ": " + str(exc)) from exc
            command["sha256"] = digest(log)
            if result.returncode:
                raise RuntimeError(label + ": exit " + str(result.returncode))
            return result.stdout

        for script, label in [("tools/verify_v37.py", "mathematical-diagnostics"),
                              ("tools/test_contract_v37.py", "validation-contract")]:
            normal = run([sys.executable, script], label + "-normal")
            optimized = run([sys.executable, "-O", script], label + "-optimized")
            if normal != optimized:
                raise RuntimeError("ordinary and optimized diagnostics differ: " + script)
            result = json.loads(normal)
            if not isinstance(result, dict) or result.get("status") != "passed":
                raise RuntimeError("diagnostic output does not report success: " + script)
            record["diagnostics"].append({"script": script,
                                          "normal_optimized_identical": True,
                                          "result": result})
        run(["pdflatex", "--version"], "tex-version")
        run(["latexmk", "-v"], "latexmk-version")
        (ROOT / "build").mkdir(exist_ok=True)
        build = Path(tempfile.mkdtemp(prefix="qualification-", dir=ROOT / "build"))
        run(["latexmk", "-g", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
             "-file-line-error", "-latexoption=-no-shell-escape",
             "-outdir=" + str(build), "main.tex"], "primary-build", timeout=600)
        log, pdf, fls = build / "main.log", build / "main.pdf", build / "main.fls"
        warnings = inspect_tex_log(log.read_text(errors="replace"))
        info = run(["pdfinfo", str(pdf)], "primary-pdfinfo")
        pages = re.search(r"^Pages:\s+(\d+)\s*$", info, re.M)
        if not pages or int(pages.group(1)) < 1:
            raise RuntimeError("PDF inspection did not return a positive page count")
        record["documents"].append({
            "source": "main.tex", "pages": int(pages.group(1)),
            "pdf_sha256": digest(pdf), "final_tex_log_sha256": digest(log),
            "final_tex_diagnostics": warnings,
        })
        if warnings:
            raise RuntimeError("final TeX log contains diagnostics")
        verify_recorded_inputs(fls, ROOT, repo, build, before)
        if before != collect_sources(ROOT, repo) or pins_data != pins_path.read_bytes():
            raise RuntimeError("source files changed during qualification")
        if head != git(repo, "rev-parse", "HEAD"):
            raise RuntimeError("Git HEAD changed during qualification")
        if record["preserved_git_trees"] != verify_preserved_trees(repo):
            raise RuntimeError("preserved source trees changed during qualification")
        if not args.allow_dirty:
            validate_head_binding(args.expected_head, head,
                                  git(repo, "status", "--porcelain", "--untracked-files=no"), False)
            verify_committed_bytes(repo, before, manifest_hash)
        record["source_unchanged"] = True
        record["exact_commit_qualified"] = not args.allow_dirty
        record["status"] = "passed"
    except Exception as exc:
        record["status"] = "failed"
        record["error"] = type(exc).__name__ + ": " + str(exc)
    finally:
        record["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        if evidence_ready:
            if build is not None:
                for source, target in [("main.log", "final-main.log"),
                                       ("main.fls", "final-main.fls"),
                                       ("main.pdf", "A2-v37-primary.pdf")]:
                    if (build / source).is_file():
                        shutil.copyfile(build / source, out / target)
            record["artifact_sha256"] = {
                path.name: digest(path) for path in sorted(out.iterdir()) if path.is_file()
            }
            (out / "receipt.json").write_text(canonical_json(record), encoding="utf-8")
        print(canonical_json(record), end="")
    return 0 if record["status"] == "passed" else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--freeze-manifest", action="store_true")
    mode.add_argument("--expected-head", metavar="FULL_GIT_SHA")
    mode.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--output-dir", help="generated evidence directory; default verification/current")
    args = parser.parse_args()
    if args.freeze_manifest:
        repo = repository_root()
        verify_preserved_trees(repo)
        actual, inputs = collect_sources(ROOT, repo), tex_input_closure(ROOT)
        destination = ROOT / MANIFEST_NAME
        if destination.is_symlink():
            raise ValueError("symlink source manifest")
        destination.write_text(canonical_json(manifest_document(actual, inputs)), encoding="utf-8")
        print(json.dumps({"schema": MANIFEST_SCHEMA, "status": "frozen",
                          "source_files": len(actual), "tex_inputs": len(inputs),
                          "manifest_sha256": digest(destination),
                          "qualification_performed": False}, sort_keys=True))
        return 0
    return qualify(args)


if __name__ == "__main__":
    raise SystemExit(main())
