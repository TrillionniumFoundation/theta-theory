#!/usr/bin/env python3
"""Bind the complete declared Round 47 source graph to an existing Git commit.

This is source-integrity and build verification, not formal verification of
mathematics. The TeX reader accepts literal project inputs; a build additionally
checks the engine's recorded repository-local inputs. Artifact-only descendants
are allowed, but neither missing commits nor changed covered bytes are allowed.
"""
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
import tarfile
import tempfile

ROOTS = ("ROUND47_REVISION.tex", "ROUND47_RETAINED_RESULTS.tex")
SUPPORT = (
    "tools/verify_round47.py", "tools/round47_certificates.py",
    "tests/test_round47.py", "AUTHOR_RESPONSE_ROUND46.md",
    "round47/PROOF_LEDGER.json", "round47/README.md",
    ".github/workflows/round47-readonly.yml",
)
MANIFEST = "round47/SOURCE_MANIFEST.json"

class VerificationError(RuntimeError):
    pass


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()


def git(root: Path, *args: str) -> bytes:
    run = subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=30)
    if run.returncode:
        raise VerificationError("Git operation failed: "+" ".join(args)+"\n"+
                                run.stderr.decode("utf-8", errors="replace"))
    return run.stdout


def safe_path(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_./-]+", name):
        raise VerificationError(f"Nonliteral or unsupported source path: {name!r}")
    path = Path(name)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise VerificationError(f"Source path escapes repository: {name}")
    target = root/path
    if target.is_symlink() or not target.resolve().is_relative_to(root.resolve()):
        raise VerificationError(f"Symlink or escaping source path: {name}")
    if not target.is_file():
        raise VerificationError(f"Missing source file: {name}")
    return target


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        for i, char in enumerate(line):
            if char != "%":
                continue
            count, j = 0, i-1
            while j >= 0 and line[j] == "\\":
                count += 1
                j -= 1
            if count % 2 == 0:
                line = line[:i]
                break
        lines.append(line)
    return "\n".join(lines)


def tex_graph(root: Path, roots: tuple[str, ...] = ROOTS) -> set[str]:
    """Literal input/include/bibliography/graphics and local package graph.

    Paths have the TeX build's repository-root working-directory semantics.
    Dynamic filenames and unbraced input syntax are rejected, not ignored.
    """
    visited: set[str] = set()
    todo = list(roots)
    while todo:
        name = todo.pop()
        if name in visited:
            continue
        path = safe_path(root, name)
        visited.add(name)
        if path.suffix not in (".tex", ".sty", ".cls", ".bst"):
            continue
        text = strip_comments(path.read_text(encoding="utf-8"))
        if re.search(r"\\(?:csname|catcode|openin|InputIfFileExists|IfFileExists|includeonly)\b", text):
            raise VerificationError(f"Dynamic TeX input construct outside declared profile: {name}")
        commands = list(re.finditer(r"\\(?:input|include)\b", text))
        inputs = list(re.finditer(r"\\(?:input|include)\s*\{([^{}]+)\}", text))
        if len(commands) != len(inputs):
            raise VerificationError(f"Unbraced or dynamic TeX input: {name}")
        for match in inputs:
            child = match.group(1).strip()
            if not Path(child).suffix:
                child += ".tex"
            safe_path(root, child)
            todo.append(child)
        for match in re.finditer(r"\\bibliography\s*\{([^{}]+)\}", text):
            for child in match.group(1).split(","):
                child = child.strip()
                if not child.endswith(".bib"):
                    child += ".bib"
                safe_path(root, child)
                todo.append(child)
        for match in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\s*\{([^{}]+)\}", text):
            child = match.group(1).strip()
            choices = [child] if Path(child).suffix else [child+s for s in (".pdf", ".png", ".jpg", ".jpeg", ".eps")]
            choices = [p for p in choices if (root/p).is_file()]
            if len(choices) != 1:
                raise VerificationError(f"Missing or ambiguous graphics input: {child}")
            safe_path(root, choices[0])
            todo.append(choices[0])
        for command, suffix in (("usepackage", ".sty"), ("RequirePackage", ".sty"),
                                ("documentclass", ".cls"), ("bibliographystyle", ".bst")):
            pattern = r"\\"+command+r"(?:\[[^\]]*\])?\s*\{([^{}]+)\}"
            for match in re.finditer(pattern, text):
                for package in match.group(1).split(","):
                    child = package.strip()+suffix
                    if (root/child).exists():
                        safe_path(root, child)
                        todo.append(child)
    return visited


def verify_source(root: Path, source_sha: str, *, roots: tuple[str, ...] = ROOTS,
                  support: tuple[str, ...] = SUPPORT, manifest_name: str = MANIFEST) -> dict:
    root = root.resolve()
    if not re.fullmatch(r"[0-9a-f]{40}", source_sha):
        raise VerificationError("--source-sha must name a full lowercase Git commit SHA")
    resolved = git(root, "rev-parse", "--verify", source_sha+"^{commit}").decode().strip()
    if resolved != source_sha:
        raise VerificationError("Source argument is not the exact named commit object")
    git(root, "merge-base", "--is-ancestor", source_sha, "HEAD")
    manifest_path = safe_path(root, manifest_name)
    manifest_bytes = manifest_path.read_bytes()
    if git(root, "show", source_sha+":"+manifest_name) != manifest_bytes:
        raise VerificationError("Working manifest differs from the named source commit")
    try:
        manifest = json.loads(manifest_bytes)
    except (ValueError, UnicodeError) as exc:
        raise VerificationError("Invalid source manifest") from exc
    if manifest.get("schema") != 1 or manifest.get("roots") != list(roots):
        raise VerificationError("Manifest schema or mandatory manuscript roots differ")
    if manifest.get("support") != list(support):
        raise VerificationError("Manifest omitted or changed mandatory support files")
    graph = tex_graph(root, roots)
    expected = graph | set(support)
    files = manifest.get("files", {})
    if not isinstance(files, dict) or set(files) != expected:
        raise VerificationError("Manifest does not exactly cover input graph and support: "+
                                repr(sorted(expected.symmetric_difference(set(files)))))
    hashes = {}
    for name in sorted(expected):
        path = safe_path(root, name)
        entry = files[name]
        if not isinstance(entry, dict) or not re.fullmatch(r"[0-9a-f]{40}", entry.get("git_blob", "")):
            raise VerificationError(f"Invalid blob entry: {name}")
        data = path.read_bytes()
        actual = git_blob(data)
        stored = git(root, "rev-parse", source_sha+":"+name).decode().strip()
        if actual != stored or actual != entry["git_blob"]:
            raise VerificationError(f"Source blob mismatch: {name}")
        if git(root, "show", source_sha+":"+name) != data:
            raise VerificationError(f"Source byte mismatch: {name}")
        tree_record = git(root, "ls-tree", source_sha, "--", name).decode()
        if not tree_record.startswith(("100644 ", "100755 ")):
            raise VerificationError(f"Not a regular committed source file: {name}")
        digest = hashlib.sha256(data).hexdigest()
        if "sha256" in entry and entry["sha256"] != digest:
            raise VerificationError(f"SHA256 mismatch: {name}")
        hashes[name] = {"git_blob": actual, "sha256": digest}
    return {"source_bound": True, "source_commit": source_sha,
            "checkout_commit": git(root, "rev-parse", "HEAD").decode().strip(),
            "roots": list(roots), "tex_graph": sorted(graph), "files": hashes,
            "manifest_git_blob": git_blob(manifest_bytes)}


def check_recorded_inputs(root: Path, fls: Path, covered: set[str], build_dir: Path) -> None:
    root, build_dir = root.resolve(), build_dir.resolve()
    if not fls.is_file():
        raise VerificationError("TeX recorder output missing")
    for line in fls.read_text(errors="replace").splitlines():
        if not line.startswith("INPUT "):
            continue
        path = Path(line[6:])
        if not path.is_absolute():
            path = root/path
        path = path.resolve()
        if path.is_relative_to(build_dir):
            continue  # Fresh engine-generated auxiliaries only.
        if path.is_relative_to(root) and path.relative_to(root).as_posix() not in covered:
            raise VerificationError("Undeclared recorded local TeX input: "+str(path))


def build_documents(root: Path, covered: set[str]) -> dict:
    if not shutil.which("pdflatex"):
        raise VerificationError("pdflatex is not installed")
    outputs = {}
    with tempfile.TemporaryDirectory(prefix="round47-tex-") as temporary:
        source_root = Path(temporary)/"source"
        build_dir = Path(temporary)/"build"
        source_root.mkdir()
        build_dir.mkdir()
        # Copy only already verified inputs. Old auxiliaries and untracked
        # local packages in the working checkout cannot contaminate this build.
        for name in sorted(covered):
            original = safe_path(root, name)
            destination = source_root/name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(original, destination)
        for source in ROOTS:
            stem = Path(source).stem
            for pass_no in range(1, 4):
                cmd = ["pdflatex", "-no-shell-escape", "-halt-on-error",
                       "-interaction=nonstopmode", "-recorder",
                       "-output-directory", str(build_dir), source]
                run = subprocess.run(cmd, cwd=source_root, capture_output=True, timeout=180)
                log_path = root/f"{stem}_BUILD_{pass_no}.log"
                log_path.write_bytes(run.stdout+run.stderr)
                if run.returncode:
                    raise VerificationError(f"TeX failed for {source}; see {log_path.name}")
            engine_log = (build_dir/f"{stem}.log").read_text(errors="replace")
            if re.search(r"Overfull \\[hv]box|undefined references|Reference .* undefined|Citation .* undefined", engine_log):
                raise VerificationError(f"Unresolved references or overflow in {source}")
            check_recorded_inputs(source_root, build_dir/f"{stem}.fls", covered, build_dir)
            pdf = build_dir/f"{stem}.pdf"
            shutil.copy2(pdf, root/pdf.name)
            shutil.copy2(build_dir/f"{stem}.log", root/f"{stem}.log")
            outputs[source] = {"pdf": pdf.name, "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                               "passes": 3, "recorded_inputs_checked": True,
                               "isolated_verified_source_copy": True}
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--build", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    report: dict = {"schema": 1, "status": "failed", "formal_proof_verification": False}
    try:
        report.update(verify_source(root, args.source_sha))
        run = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests",
                              "-p", "test_round47.py", "-v"], cwd=root, capture_output=True, timeout=180)
        (root/"ROUND47_TESTS.log").write_bytes(run.stdout+run.stderr)
        if run.returncode:
            raise VerificationError("Round 47 regression tests failed")
        report["regression_tests"] = {"passed": True, "log": "ROUND47_TESTS.log"}
        if args.build:
            report["build"] = build_documents(root, set(report["files"]))
        report["status"] = "passed"
    except (VerificationError, OSError, subprocess.TimeoutExpired) as exc:
        report["error"] = str(exc)
    result_path = root/"ROUND47_VERIFICATION.json"
    temporary = result_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True)+"\n")
    os.replace(temporary, result_path)
    if report["status"] == "passed" and args.build:
        members = set(report["files"]) | {MANIFEST, result_path.name, "ROUND47_TESTS.log"}
        members.update(item["pdf"] for item in report["build"].values())
        with tarfile.open(root/"ROUND47_REVIEW_BUNDLE.tar.gz", "w:gz") as archive:
            for name in sorted(members):
                archive.add(root/name, arcname=name, recursive=False)
    print(json.dumps({k: report[k] for k in ("status", "source_commit", "error") if k in report}))
    return 0 if report["status"] == "passed" else 1

if __name__ == "__main__":
    raise SystemExit(main())
