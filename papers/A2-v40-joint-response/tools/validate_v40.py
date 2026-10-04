#!/usr/bin/env python3
"""Qualify two pinned journal documents and retain failed-execution evidence.

Freeze SOURCE_PINS.json only after editing is complete. A development run uses
--allow-dirty and never claims qualification of a Git commit. A publication run
requires --expected-head and verifies the committed bytes, the checkout, the
preserved Git trees, finite diagnostics, and both TeX builds. The two documents
share an isolated auxiliary directory and must reach a stable reference state.
--capture-source records source-only evidence before installing TeX; this mode
does not claim mathematical diagnostics, PDF qualification, or a passed build.
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
PACKAGE = PurePosixPath("papers/A2-v40-joint-response")
WORKFLOW = ".github/workflows/a2-v40-verify.yml"
MANIFEST_NAME = "SOURCE_PINS.json"
SCHEMA = "a2-v40-validation-1"
MANIFEST_SCHEMA = "a2-v40-source-pins-1"
AUTHOR_COMMIT = "f815a7acdb5c03e03b9996fc7052b405db66936d"
REVIEW_COMMIT = "790654161f2f069fb4d1d1ee18bfe86ea5290d74"
JOURNAL_DOCUMENTS = ("main.tex", "companion.tex")
DOCUMENT_ARTIFACTS = {
    "main.tex": "A2-v40-primary.pdf",
    "companion.tex": "A2-v40-companion.pdf",
}
EXTERNAL_DOCUMENTS = {
    "main.tex": [{"source": "companion.tex", "auxiliary": "companion.aux",
                  "prefix": "H-", "citation_mode": "nocite",
                  "pdf": "A2-v40-companion.pdf"}],
    "companion.tex": [{"source": "main.tex", "auxiliary": "main.aux",
                       "prefix": "M-", "citation_mode": "nocite",
                       "pdf": "A2-v40-primary.pdf"}],
}
PRESERVED_TREES = {
    "reviewed_v39": {
        "commit": AUTHOR_COMMIT,
        "path": "papers/A2-v39-response-rigidity",
        "git_tree": "e60aaed448b772942ffd38d556babab35b3c3880",
    },
    "controlling_review": {
        "commit": REVIEW_COMMIT,
        "path": "reviews/a2-v39-external-harsh-top4-rereview-2026-10-04",
        "git_tree": "99a365ce0caa40d473dd89c9e2e4bd8f869796d5",
    },
    "retained_v38": {
        "commit": "a346669928e5147cf2c0ef86c3bc2a455b512d14",
        "path": "papers/A2-v38-finite-field-rigidity",
        "git_tree": "36a5f28721e4aa336dba7a2eb0d07132589cd301",
    },
    "retained_v38_review": {
        "commit": "5dd7a7e346a9d31d7541efe791335d4e965cadb0",
        "path": "reviews/a2-v38-external-harsh-top4-rereview-2026-10-04",
        "git_tree": "91797dde92b95cbaa36d3ef5f543fee025268855",
    },
    "retained_v37": {
        "commit": "02e6a6c799cb00c7dc7304ddfbf7ac885c83ea4d",
        "path": "papers/A2-v37-stationary-rigidity",
        "git_tree": "22519a94ba11210bfd2669998723c88025ecc352",
    },
    "retained_v36": {
        "commit": "2559749a038fd2b5ec46d7cc74fdb4bd844b266a",
        "path": "papers/A2-v36-stationary-boundary",
        "git_tree": "3cc6234334105c6e9be005e19d05df696aa1d923",
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
    "main.tex", "companion.tex", "references.tex", "README.md", "RESPONSE_TO_REFEREES.md",
    "PROOF_LEDGER.md", "HISTORICAL_DERIVATION_AUDIT.md",
    "LITERATURE_AUDIT.md", "SUBMISSION_MAP.md",
    "tools/validate_v40.py", "tools/test_contract_v40.py", "tools/verify_v40.py",
}
GENERATED_TOP_LEVEL = {"build", "verification"}
GENERATED_EVIDENCE = {
    "receipt.json", "artifact-binding.json", "A2-v40-primary.pdf", "A2-v40-companion.pdf",
    "A2-v40-journal-source.zip", "A2-v40-repository-source.zip",
    "final-main.log", "final-main.fls", "final-companion.log", "final-companion.fls",
    "source-pins.json",
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


def source_text(path: Path) -> str:
    """Decode without universal-newline conversion, preserving proof bytes."""
    return path.read_bytes().decode("utf-8")


def tex_document_inputs(paper: Path) -> dict[str, list[str]]:
    """Find each literal source closure; the union must include every TeX file."""
    documents: dict[str, list[str]] = {}
    for document in JOURNAL_DOCUMENTS:
        pending, visited = [document], set()
        while pending:
            name = pending.pop()
            relative = PurePosixPath(name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError("TeX input escapes the journal package: " + name)
            name = relative.as_posix()
            if name in visited:
                continue
            if name in JOURNAL_DOCUMENTS and name != document:
                raise ValueError("journal entry points must not input one another")
            path = paper / name
            if path.is_symlink() or not path.is_file():
                raise ValueError("missing or non-regular TeX input: " + name)
            visited.add(name)
            text = re.sub(r"(?<!\\)%[^\n]*", "", source_text(path))
            for command in re.finditer(r"\\(?:input|include)\s*\{([^}]+)\}", text):
                target = command.group(1).strip()
                if "\\" in target or not target:
                    raise ValueError("non-literal TeX input: " + target)
                if not target.endswith(".tex"):
                    target += ".tex"
                pending.append(target)
        documents[document] = sorted(visited)
    visited = {name for inputs in documents.values() for name in inputs}
    all_tex = {
        p.relative_to(paper).as_posix() for p in paper.rglob("*.tex")
        if p.relative_to(paper).parts[0] not in GENERATED_TOP_LEVEL
    }
    if visited != all_tex:
        raise ValueError("inactive manuscript TeX files: "
                         + ", ".join(sorted(all_tex - visited)))
    return documents


def tex_input_closure(paper: Path) -> list[str]:
    """Return the deduplicated active union, including the shared preamble once."""
    return sorted({name for inputs in tex_document_inputs(paper).values() for name in inputs})


def verify_document_partition(document_inputs: dict[str, list[str]],
                              texts: dict[str, str]) -> dict:
    if set(document_inputs) != set(JOURNAL_DOCUMENTS):
        raise ValueError("incorrect journal document set")
    union = {name for inputs in document_inputs.values() for name in inputs}
    if union != set(texts):
        raise ValueError("document closures differ from the active source union")
    ownership: dict[str, list[str]] = {
        name: [document for document, inputs in document_inputs.items() if name in inputs]
        for name in union
    }
    shared = sorted(name for name, owners in ownership.items() if len(owners) > 1)
    mathematics = re.compile(
        r"\\label\s*\{|\\begin\{(?:proof|theorem|lemma|proposition|corollary|definition)\}")
    for name in shared:
        uncommented = re.sub(r"(?<!\\)%[^\n]*", "", texts[name])
        if mathematics.search(uncommented):
            raise ValueError("labeled mathematics or proofs shared between documents: " + name)
    labels = re.compile(r"\\label\{([^{}]+)\}")
    label_owners: dict[str, list[str]] = {}
    document_counts = {}
    for document, inputs in document_inputs.items():
        text = "\n".join(texts[name] for name in inputs)
        found = labels.findall(text)
        for label in found:
            label_owners.setdefault(label, []).append(document)
        document_counts[document] = {
            "tex_inputs": len(inputs), "labels": len(found),
            "proof_bodies": len(re.findall(r"\\begin\{proof\}", text)),
        }
    duplicate_labels = sorted(label for label, owners in label_owners.items() if len(owners) > 1)
    if duplicate_labels:
        raise ValueError("labels have multiple document owners: " + ", ".join(duplicate_labels))
    return {"shared_label_free_inputs": shared, "documents": document_counts,
            "active_union_files": len(union), "mathematical_inputs_have_one_owner": True}


def verify_external_declarations(paper: Path, document_inputs: dict[str, list[str]]) -> dict:
    """Pin the precise auxiliary imports; they do not expand the source closure."""
    pattern = re.compile(
        r"\\externaldocument\s*\[([^]\n]*)\]\s*\[([^]\n]*)\]"
        r"\s*\{([^}\n]+)\}\s*\[([^]\n]+)\]")
    observed = {}
    for document, inputs in document_inputs.items():
        declarations = []
        for name in inputs:
            text = re.sub(r"(?<!\\)%[^\n]*", "", source_text(paper / name))
            matches = list(pattern.finditer(text))
            if len(matches) != len(re.findall(r"\\externaldocument\b", text)):
                raise ValueError("nonliteral or unsupported external document declaration: " + name)
            for match in matches:
                prefix, citation_mode, stem, pdf = match.groups()
                if name != document:
                    raise ValueError("external document declaration must be in its entry point")
                declarations.append({"source": stem + ".tex", "auxiliary": stem + ".aux",
                                     "prefix": prefix, "citation_mode": citation_mode, "pdf": pdf})
        if declarations != EXTERNAL_DOCUMENTS.get(document):
            raise ValueError("external document declaration differs: " + document)
        observed[document] = declarations
    if set(observed) != set(JOURNAL_DOCUMENTS):
        raise ValueError("incomplete external document declaration set")
    return observed


def manifest_document(actual: dict[str, str], document_inputs: dict[str, list[str]]) -> dict:
    tex_inputs = sorted({name for inputs in document_inputs.values() for name in inputs})
    return {
        "schema": MANIFEST_SCHEMA,
        "repository": "TrillionniumFoundation/theta-theory",
        "paper_directory": str(PACKAGE),
        "journal_documents": list(JOURNAL_DOCUMENTS),
        "document_tex_inputs": document_inputs,
        "external_documents": EXTERNAL_DOCUMENTS,
        "reviewed_author_commit": AUTHOR_COMMIT,
        "controlling_review_commit": REVIEW_COMMIT,
        "preserved_trees": PRESERVED_TREES,
        "workflow": WORKFLOW,
        "source_sha256": actual,
        "tex_inputs": tex_inputs,
        "excluded_generated_paths": ["build/", "verification/", "**/__pycache__/",
                                     "**/*.pyc", "**/*.pyo", MANIFEST_NAME],
        "manifest_binding": "manifest bytes are bound by the Git commit, receipt, and source archive",
        "preservation_contract": "all active v39 labels and every byte-identical v39 proof body remain in the deduplicated active union of the two compiled documents",
        "build_contract": "both documents reach stable shared auxiliary files; actual TeX openings match each source closure; only declared opposite-entry metadata probes accompanied by the pinned auxiliary import are permitted",
        "formal_proof_certificate": False,
        "physical_sensor_executed": False,
    }


def validate_manifest(pins: dict, actual: dict[str, str], document_inputs: dict[str, list[str]]) -> None:
    expected = manifest_document(actual, document_inputs)
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
    """Read the preserved v39 inputs at HEAD; historical commits need not exist."""
    directory = PRESERVED_TREES["reviewed_v39"]["path"]
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


def logged_tex_openings(text: str, paper: Path, candidates: set[str]) -> set[str]:
    """Read TeX's parenthesized input openings, unlike openin/file-name probes."""
    found = set()
    for name in candidates:
        for spelling in (name, "./" + name, str(paper / name)):
            # TeX may hard-wrap a file name at its maximum log line length.
            wrapped = r"(?:\r?\n)?".join(re.escape(char) for char in spelling)
            if re.search(r"\(" + wrapped + r"(?=[\s()\[\\]|$)", text):
                found.add(name)
                break
    return found


def verify_recorded_inputs(fls: Path, paper: Path, repo: Path,
                           build: Path, sources: dict[str, str],
                           expected_tex_inputs: list[str] | None = None,
                           external_documents: list[dict] | None = None,
                           tex_log: str | None = None) -> list[str]:
    recorded_tex: set[str] = set()
    recorded_aux: set[str] = set()
    for line in fls.read_text(errors="replace").splitlines():
        if not line.startswith("INPUT "):
            continue
        path = Path(line[6:])
        if not path.is_absolute():
            path = paper / path
        path = path.resolve()
        if path.is_relative_to(build):
            if path.parent == build and path.suffix == ".aux":
                recorded_aux.add(path.name)
            continue
        if path.is_relative_to(repo):
            relative = path.relative_to(repo).as_posix()
            if relative not in sources:
                raise ValueError("TeX read an unpinned repository input: " + relative)
            if path.is_relative_to(paper) and path.suffix == ".tex":
                recorded_tex.add(path.relative_to(paper).as_posix())
    metadata_sources = set()
    for external in external_documents or []:
        source = external["source"]
        if (source not in JOURNAL_DOCUMENTS or source in (expected_tex_inputs or [])
                or external["auxiliary"] != Path(source).stem + ".aux"):
            raise ValueError("invalid external entry-point metadata contract")
        if tex_log is None:
            raise ValueError("external metadata probes require the final TeX log")
        if external["auxiliary"] not in recorded_aux:
            raise ValueError("external auxiliary was not read from the isolated build: "
                             + external["auxiliary"])
        normalized_log = re.sub(r"\s+", " ", tex_log)
        if "IMPORTING LABELS FROM " + external["auxiliary"] not in normalized_log:
            raise ValueError("external auxiliary import is absent from the final TeX log")
        metadata_sources.add(source)
    active_recorded = recorded_tex - metadata_sources
    if expected_tex_inputs is not None and active_recorded != set(expected_tex_inputs):
        missing = sorted(set(expected_tex_inputs) - active_recorded)
        extra = sorted(active_recorded - set(expected_tex_inputs))
        raise ValueError("compiled TeX closure differs: missing=" + repr(missing)
                         + "; extra=" + repr(extra))
    if tex_log is not None:
        typeset = logged_tex_openings(tex_log, paper, recorded_tex)
        if typeset & metadata_sources:
            raise ValueError("external metadata entry point was also typeset: "
                             + ", ".join(sorted(typeset & metadata_sources)))
        if expected_tex_inputs is not None and typeset != set(expected_tex_inputs):
            raise ValueError("actual TeX input openings differ from the declared source closure")
    return sorted(active_recorded)


def auxiliary_state(build: Path) -> dict[str, str]:
    state = {}
    for document in JOURNAL_DOCUMENTS:
        stem = Path(document).stem
        for suffix in (".aux", ".toc", ".out", ".lof", ".lot"):
            path = build / (stem + suffix)
            if path.is_file():
                state[path.name] = digest(path)
    return state


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
        "scope": ("pinned source capture only; no mathematical diagnostics or PDF qualification"
                  if args.capture_source else
                  "current finite diagnostics, both journal builds, and preserved Git tree identities"),
        "journal_documents": list(JOURNAL_DOCUMENTS),
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
        document_inputs = tex_document_inputs(ROOT)
        tex_inputs = sorted({name for inputs in document_inputs.values() for name in inputs})
        record["external_documents"] = verify_external_declarations(ROOT, document_inputs)
        validate_manifest(pins, before, document_inputs)
        manifest_hash = digest_bytes(pins_data)
        record["source_manifest_sha256"] = manifest_hash
        record["source_sha256"] = before
        record["preserved_git_trees"] = verify_preserved_trees(repo)
        active_text = {name: source_text(ROOT / name) for name in tex_inputs}
        record["document_partition"] = verify_document_partition(document_inputs, active_text)
        record["active_content_preservation"] = verify_preservation(
            read_reviewed_inputs(repo), active_text)
        if not args.allow_dirty:
            verify_committed_bytes(repo, before, manifest_hash)
        (out / "source-pins.json").write_bytes(pins_data)
        journal_members = {name: (str(PACKAGE / name), before[str(PACKAGE / name)])
                           for name in tex_inputs}
        source_members = {name: (name, sha) for name, sha in before.items()}
        source_members[str(PACKAGE / MANIFEST_NAME)] = (str(PACKAGE / MANIFEST_NAME), manifest_hash)
        deterministic_zip(out / "A2-v40-journal-source.zip", repo, journal_members)
        deterministic_zip(out / "A2-v40-repository-source.zip", repo, source_members)
        record["journal_members"] = sorted(journal_members)
        record["document_tex_inputs"] = document_inputs
        record["repository_source_members"] = sorted(source_members)
        record["source_captured"] = True
        if args.capture_source:
            if before != collect_sources(ROOT, repo) or pins_data != pins_path.read_bytes():
                raise RuntimeError("source files changed during source capture")
            if head != git(repo, "rev-parse", "HEAD"):
                raise RuntimeError("Git HEAD changed during source capture")
            if not args.allow_dirty:
                validate_head_binding(args.expected_head, head,
                                      git(repo, "status", "--porcelain", "--untracked-files=no"), False)
                verify_committed_bytes(repo, before, manifest_hash)
            record["source_unchanged"] = True
            record["status"] = "source_captured"
            return 0
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

        for script, label in [("tools/verify_v40.py", "mathematical-diagnostics"),
                              ("tools/test_contract_v40.py", "validation-contract")]:
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
        previous_texinputs = os.environ.get("TEXINPUTS", "")
        command_env["TEXINPUTS"] = (str(build) + os.pathsep + previous_texinputs
                                    + ("" if previous_texinputs.endswith(os.pathsep) else os.pathsep))
        previous = auxiliary_state(build)
        stable = False
        record["cross_document_build_rounds"] = []
        for iteration in range(1, 7):
            for document in JOURNAL_DOCUMENTS:
                stem = Path(document).stem
                run(["latexmk", "-g", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                     "-file-line-error", "-latexoption=-no-shell-escape",
                     "-outdir=" + str(build), document],
                    stem + "-build-round-" + str(iteration), timeout=600)
            current = auxiliary_state(build)
            if not all(Path(document).stem + ".aux" in current for document in JOURNAL_DOCUMENTS):
                raise RuntimeError("both documents must produce an auxiliary file")
            record["cross_document_build_rounds"].append(
                {"round": iteration, "auxiliary_sha256": current})
            if current == previous:
                stable = True
                break
            previous = current
        if not stable:
            raise RuntimeError("cross-document references did not reach a stable auxiliary state")
        record["cross_document_auxiliaries_stable"] = True
        for document in JOURNAL_DOCUMENTS:
            stem = Path(document).stem
            log, pdf, fls = (build / (stem + suffix) for suffix in (".log", ".pdf", ".fls"))
            final_log = log.read_text(errors="replace")
            warnings = inspect_tex_log(final_log)
            info = run(["pdfinfo", str(pdf)], stem + "-pdfinfo")
            pages = re.search(r"^Pages:\s+(\d+)\s*$", info, re.M)
            if not pages or int(pages.group(1)) < 1:
                raise RuntimeError("PDF inspection did not return a positive page count: " + document)
            recorded = verify_recorded_inputs(
                fls, ROOT, repo, build, before, document_inputs[document],
                external_documents=record["external_documents"][document], tex_log=final_log)
            record["documents"].append({
                "source": document, "artifact": DOCUMENT_ARTIFACTS[document],
                "pages": int(pages.group(1)), "pdf_sha256": digest(pdf),
                "final_tex_log_sha256": digest(log), "final_tex_diagnostics": warnings,
                "recorded_tex_inputs": recorded,
                "recorded_input_closure_matches": True,
                "actual_tex_openings_match": True,
                "external_auxiliary_imports_verified": record["external_documents"][document],
            })
            if warnings:
                raise RuntimeError("final TeX log contains diagnostics: " + document)
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
                for document in JOURNAL_DOCUMENTS:
                    stem = Path(document).stem
                    for source, target in [(stem + ".log", "final-" + stem + ".log"),
                                           (stem + ".fls", "final-" + stem + ".fls"),
                                           (stem + ".pdf", DOCUMENT_ARTIFACTS[document])]:
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
    parser.add_argument("--capture-source", action="store_true",
                        help="capture source-only evidence without running diagnostics or TeX")
    parser.add_argument("--output-dir", help="generated evidence directory; default verification/current")
    args = parser.parse_args()
    if args.capture_source and args.freeze_manifest:
        parser.error("source capture cannot be combined with manifest freezing")
    if args.freeze_manifest:
        repo = repository_root()
        verify_preserved_trees(repo)
        actual, documents = collect_sources(ROOT, repo), tex_document_inputs(ROOT)
        verify_external_declarations(ROOT, documents)
        inputs = sorted({name for closure in documents.values() for name in closure})
        active_text = {name: source_text(ROOT / name) for name in inputs}
        verify_document_partition(documents, active_text)
        preservation = verify_preservation(read_reviewed_inputs(repo), active_text)
        destination = ROOT / MANIFEST_NAME
        if destination.is_symlink():
            raise ValueError("symlink source manifest")
        destination.write_text(canonical_json(manifest_document(actual, documents)), encoding="utf-8")
        print(json.dumps({"schema": MANIFEST_SCHEMA, "status": "frozen",
                          "source_files": len(actual), "tex_inputs": len(inputs),
                          "journal_documents": list(JOURNAL_DOCUMENTS),
                          "active_content_preservation": preservation,
                          "manifest_sha256": digest(destination),
                          "qualification_performed": False}, sort_keys=True))
        return 0
    return qualify(args)


if __name__ == "__main__":
    raise SystemExit(main())
