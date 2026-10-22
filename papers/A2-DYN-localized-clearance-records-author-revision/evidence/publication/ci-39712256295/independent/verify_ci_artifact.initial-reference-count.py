#!/usr/bin/env python3
"""Independently reconstruct the actual A2-DYN CI artifact without running its gates.

Inputs are read only. No repository checker is imported or executed. Outputs are
written only to the explicitly selected audit directory. This checks identities,
actual execution receipts, stable finite outputs and native document closure;
it does not certify the continuum billiard mathematics or reconstruct missing
historical source bytes. All conditions remain active under Python -O.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import traceback
import zipfile

import pypdf
from pypdf import PdfReader

EXPECTED = {
    "checkout": "9bd4ab343bb8a0f78b6a6380ae1f1e80a976d761",
    "published_article_tree": "1fb3b20b29e3fe447bdae42f0faca0baf4f6b9cc",
    "run": 39712256295,
    "job": 119606068910,
    "artifact_id": 12397079374,
    "archive_bytes": 11054196,
    "archive_sha256": "6ad292d68d0f16743ad222adfd34b6260b67d50d9c2a0205954bc3ed026e2ac0",
    "mathematical_source": "cecca59e06fc83d0e3bab89e41e347b6c831c50dd78e7603d63377ca4be4feb0",
    "manifest_sha256": "5745a5abe9bb95de6dc64d53d28e018549c41f330b2895fb3382d9019bb8ae55",
    "predecessor_commit": "03d651b8709d28d90aa435fc12d608ad9c945e23",
    "predecessor_root_tree": "d65973a6db0eb2c477359d10b43194cc5f99fa2f",
    "predecessor_article_tree": "3010c90e2363dfe1808101a3e992eb02643c28f1",
    "anchor_sha256": "ca3d5e4d2204230a21e3e3e6ed8439d5b79484a38a98ff3ab8456db03394ae6c",
}
CI_ROOT = "/home/runner/work/theta-theory/theta-theory/papers/A2-DYN-localized-clearance-records-author-revision"
RUNTIME_PROGRAMS = {"check_all_offset_boundary", "check_positive_critical_fans"}
NEW_COUNTS = {
    "check_localized_clearance_transport": 1478574,
    "check_all_label_likelihood": 74071,
    "check_marked_weak_operator": 28388,
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_oid(kind, data):
    return hashlib.sha1(kind.encode() + b" " + str(len(data)).encode() + b"\0" + data).hexdigest()


def identity(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha(data), "git_blob": git_oid("blob", data)}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(data):
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()


def timevalue(value):
    return datetime.fromisoformat(value)


class Audit:
    def __init__(self, article, extracted, archive):
        self.article = article.resolve()
        self.extracted = extracted.resolve()
        self.archive = archive.resolve()
        self.current = self.extracted / "current"
        self.historical = self.extracted / "current-history"
        self.local = self.article / "evidence/current-execution"
        self.checks = Counter()
        self.result = {
            "schema": "A2-DYN-independent-actual-CI-artifact-reconstruction-v1",
            "status": "running",
            "scope": "Read-only reconstruction of actual source-bound CI execution and native artifacts",
            "mathematical_proof_certificate": False,
            "independent_human_specialist_reconstruction": False,
            "expected_publication": EXPECTED,
            "input_locations": {"article": str(self.article), "extracted_artifact": str(self.extracted), "archive": str(self.archive)},
            "limitations": [
                "The archive run/job/artifact association and published article-tree identity are supplied from GitHub metadata by the publishing agent; this checker verifies the exact archive digest and embedded checkout SHA, not a remote API response.",
                "The full historical source byte archive and isolated rebuilt historical source are not included in the CI artifact. This checker reconstructs the preserved predecessor Git tree from its anchored path/mode/blob map, rehashes the 69 available inherited active bodies, and verifies the CI source-gate result against committed local evidence; it does not claim a new independent byte rehash of all 5,938 absent historical files.",
                "The historical rebuild checks the original assembler, six pdflatex passes and two pdfinfo calls; the historical repository-wide gate was not executed.",
                "Finite exact/symbolic checks, output agreement, labels and successful CI are auxiliary evidence. They do not prove the raw pointwise LLT, full joint spectral inversion, the remaining normalized shortage or the four-coordinate long-time inverse theorem.",
            ],
        }

    def require(self, condition, group, message):
        self.checks[group] += 1
        if not condition:
            raise RuntimeError(group + ": " + message)

    def check_identity(self, path, claimed, group):
        actual = identity(path)
        for key in ("bytes", "sha256", "git_blob"):
            if key in claimed:
                self.require(actual[key] == claimed[key], group, f"{key} mismatch: {path}")
        return actual

    def archive_check(self):
        print("Reconstructing archive identity and all extracted members", flush=True)
        got = identity(self.archive)
        self.require(got["bytes"] == EXPECTED["archive_bytes"], "archive", "ZIP size differs")
        self.require(got["sha256"] == EXPECTED["archive_sha256"], "archive", "ZIP digest differs from GitHub artifact")
        entries = []
        with zipfile.ZipFile(self.archive) as zipped:
            names = zipped.namelist()
            self.require(len(names) == len(set(names)), "archive", "duplicate ZIP member")
            for item in zipped.infolist():
                name = PurePosixPath(item.filename)
                self.require(not name.is_absolute() and ".." not in name.parts, "archive", "unsafe ZIP member")
                self.require(not item.is_dir(), "archive", "unexpected explicit directory member")
                path = self.extracted / item.filename
                data = zipped.read(item)
                self.require(path.is_file() and not path.is_symlink(), "archive", "missing/nonregular extracted member")
                self.require(path.read_bytes() == data, "archive", "extracted bytes differ: " + item.filename)
                entries.append({"path": item.filename, "bytes": len(data), "sha256": sha(data)})
        actual_names = {p.relative_to(self.extracted).as_posix() for p in self.extracted.rglob("*") if p.is_file()}
        self.require(actual_names == set(names), "archive", "extraction has omitted or extra files")
        self.require(len(entries) == 247, "archive", "unexpected artifact member count")
        self.require((self.current / "CI_CHECKOUT_SHA.txt").read_text().strip() == EXPECTED["checkout"], "checkout", "wrong CI checkout SHA")
        self.require((self.current / "CI_BUILD_OUTCOME.txt").read_text().strip() == "success", "checkout", "CI build outcome not success")
        self.require((self.current / "CI_POST_RUN_STATUS.txt").read_bytes() == b"", "checkout", "CI post-run tracked tree not clean")
        self.result["archive"] = dict(got, members=len(entries), uncompressed_bytes=sum(x["bytes"] for x in entries), entries=entries)

    def source_check(self):
        print("Rehashing all 140 current inputs and the anchored predecessor tree map", flush=True)
        paths = sorted({p.relative_to(self.article).as_posix() for pattern in ("*.tex", "core/*.tex", "tools/*.py", "ci/*.yml") for p in self.article.glob(pattern)} | {"requirements.txt", "build.sh"})
        rows = [{"path": name, "sha256": sha((self.article / name).read_bytes())} for name in paths]
        self.source = {"sha256": sha(json.dumps(rows, sort_keys=True).encode()), "files": rows}
        self.require(self.source["sha256"] == EXPECTED["mathematical_source"], "current_source", "current mathematical source changed")
        manifest_path = self.article / "SOURCE_MANIFEST.json"
        self.require(sha(manifest_path.read_bytes()) == EXPECTED["manifest_sha256"], "current_source", "manifest digest differs")
        manifest = read_json(manifest_path)
        self.require(manifest["schema"] == "a2-dyn-frozen-mathematical-source-v1", "current_source", "wrong manifest schema")
        self.require(manifest["complete_author_parent"] == EXPECTED["predecessor_commit"], "current_source", "wrong source parent")
        self.require(len(manifest["files"]) == len(paths) == 140, "current_source", "wrong current input count")
        self.require({r["path"] for r in manifest["files"]} == set(paths), "current_source", "current input set differs")
        for row in manifest["files"]:
            p = self.article / row["path"]
            self.check_identity(p, row, "current_source")
            mode = "100755" if p.stat().st_mode & 0o111 else "100644"
            self.require(row["mode"] == mode, "current_source", "current file mode differs: " + row["path"])
        self.require(sum(r["bytes"] for r in manifest["files"]) == 1563890, "current_source", "current byte sum differs")
        self.manifest = manifest
        for line in (self.current / "CI_ENTRYPOINT_SHA256.txt").read_text().splitlines():
            digest, name = line.split(None, 1)
            self.require(sha((self.article / name.strip()).read_bytes()) == digest, "current_source", "CI entrypoint digest: " + name)
        workflow = "a2-dyn-localized-clearance-records-20261021.yml"
        root_workflow = self.article.parents[1] / ".github/workflows" / workflow
        self.require(root_workflow.read_bytes() == (self.article / "ci" / workflow).read_bytes(), "current_source", "root workflow mirror differs")
        anchor_path = self.article / "CURRENT_SOURCE_ANCHOR.json"
        self.require(sha(anchor_path.read_bytes()) == EXPECTED["anchor_sha256"], "predecessor_map", "anchor digest differs")
        anchor = read_json(anchor_path)
        for key, expected_key in (("source_commit", "predecessor_commit"), ("source_root_tree", "predecessor_root_tree"), ("source_article_tree", "predecessor_article_tree")):
            self.require(anchor[key] == EXPECTED[expected_key], "predecessor_map", "wrong predecessor identity: " + key)
        old_rows = anchor["files"]
        self.require(len(old_rows) == anchor["file_count"] == 5938, "predecessor_map", "wrong preserved path count")
        self.require(sum(r["bytes"] for r in old_rows) == anchor["bytes"] == 688244624, "predecessor_map", "wrong preserved byte sum")
        tree = {}
        for row in old_rows:
            name = PurePosixPath(row["original_path"])
            self.require(not name.is_absolute() and ".." not in name.parts, "predecessor_map", "unsafe source path")
            self.require(row["path"] == "history/predecessor/" + row["original_path"], "predecessor_map", "wrong archive relocation")
            branch = tree
            for part in name.parts[:-1]:
                branch = branch.setdefault(part, {})
                self.require(isinstance(branch, dict), "predecessor_map", "file/tree conflict")
            self.require(name.name not in branch, "predecessor_map", "duplicate preserved path")
            branch[name.name] = (row["mode"], row["git_blob"])

        def tree_hash(node):
            entries = []
            for name, child in node.items():
                is_dir = isinstance(child, dict)
                mode, oid = ("40000", tree_hash(child)) if is_dir else child
                entries.append((name.encode() + (b"/" if is_dir else b""), mode.encode() + b" " + name.encode() + b"\0" + bytes.fromhex(oid)))
            return git_oid("tree", b"".join(body for _, body in sorted(entries)))

        reconstructed = tree_hash(tree)
        self.require(reconstructed == EXPECTED["predecessor_article_tree"], "predecessor_map", "anchored map does not reconstruct preserved Git tree")
        lookup = {r["original_path"]: r for r in old_rows}
        inherited = {name for name in lookup if name in {"model.tex", "inputs.tex"} or re.fullmatch(r"core/\d+_[^/]+\.tex", name)}
        self.require(inherited == set(anchor["inherited_active_paths"]) and len(inherited) == 69, "predecessor_map", "inherited active set differs")
        for name in sorted(inherited):
            self.check_identity(self.article / name, lookup[name], "inherited_active_bytes")
        source_gate = read_json(self.current / "source-checks.json")
        local_gate = read_json(self.local / "source/source-checks.json")
        self.require(source_gate == local_gate, "source_gate", "CI and committed local source result differ")
        self.require(source_gate["status"] == "passed" and source_gate["mathematical_proof_certificate"] is False, "source_gate", "source result scope/status")
        self.require(source_gate["mathematical_source"] == self.source, "source_gate", "CI source digest rows differ")
        self.require(source_gate["current_source_anchor_sha256"] == EXPECTED["anchor_sha256"], "source_gate", "CI anchor differs")
        self.require(source_gate["original_files_preserved"] == 5938 and source_gate["original_bytes_preserved"] == 688244624, "source_gate", "CI preservation count differs")
        self.source_gate = source_gate
        pub = read_json(self.article / "PUBLICATION_STATUS.json")
        self.require(pub["full_raw_pointwise_llt_complete"] is False and pub["four_coordinate_inversion_complete"] is False and pub["independent_human_specialist_reconstruction_obtained"] is False, "scope", "publication overstates mathematics")
        environment = (self.current / "CI_ENVIRONMENT.log").read_text()
        versions = [line for line in (self.article / "requirements.txt").read_text().splitlines() if line.strip() and not line.startswith("#")]
        for version in versions:
            self.require(version in environment.splitlines(), "environment", "CI package version not pinned: " + version)
        self.phase = read_json(self.current / "PHASE_all.json")
        self.require(self.phase["status"] == "passed" and self.phase["phase"] == "all" and self.phase["continuum_proof_certificate"] is False, "phase", "wrong CI phase result")
        self.require(self.phase["completed"] == ["math", "source", "typeset"] and self.phase["mathematical_source"] == self.source, "phase", "incomplete/source-mismatched phase")
        self.require(timevalue(self.phase["started_utc"]) < timevalue(self.phase["finished_utc"]), "phase", "invalid phase chronology")
        build_lines = [json.loads(line) for line in (self.current / "CI_BUILD.log").read_text().splitlines() if line.strip()]
        self.require(len(build_lines) == 2 and all(r["status"] == "passed" for r in build_lines), "phase", "wrapper build results")
        self.require(build_lines[0]["mathematical_source_sha256"] == self.source["sha256"] and build_lines[0]["phase"] == "all", "phase", "wrapper source identity")
        self.result["source"] = {
            "mathematical_source": self.source,
            "manifest": {"sha256": sha(manifest_path.read_bytes()), "files": 140, "bytes": 1563890},
            "predecessor_map": {"reconstructed_git_tree": reconstructed, "paths": 5938, "recorded_bytes": 688244624, "independently_rehashed_inherited_active_files": 69, "full_archive_bytes_rehashed_now": False},
            "ci_source_gate_equals_committed_local_result": True,
            "ci_environment_log_sha256": sha(environment.encode()),
            "pinned_packages_verified": versions,
            "publication_status_at_source_commit": pub,
        }

    def closure_check(self):
        print("Reconstructing native input closure, all source labels and references", flush=True)
        sources, labels, edges, stack_seen = [], {}, [], set()
        all_text = []
        aliases = {"sctheorem": "theorem", "sclemma": "lemma", "sccorollary": "corollary", "scproposition": "proposition", "scdefinition": "definition", "scremark": "remark", "inputstatement": "input statement"}

        def no_comments(text):
            out = []
            for line in text.splitlines(keepends=True):
                for i, char in enumerate(line):
                    if char == "%":
                        slashes, j = 0, i - 1
                        while j >= 0 and line[j] == "\\":
                            slashes += 1
                            j -= 1
                        if slashes % 2 == 0:
                            end = len(line) - int(line.endswith("\n"))
                            line = line[:i] + " " * (end - i) + line[end:]
                            break
                out.append(line)
            return "".join(out)

        def visit(name):
            self.require(name not in stack_seen, "native_closure", "duplicate input/cycle: " + name)
            stack_seen.add(name)
            p = self.article / name
            self.require(p.is_file() and not p.is_symlink(), "native_closure", "missing/nonregular active TeX: " + name)
            text = no_comments(p.read_text())
            all_text.append(text)
            row = {"path": name, "bytes": p.stat().st_size, "sha256": sha(p.read_bytes()), "label_count": 0}
            sources.append(row)
            environments = []
            for match in re.finditer(r"\\(begin|end|label)\s*\{([^{}]+)\}", text):
                command, value = match.groups()
                if command == "begin":
                    environments.append(value)
                elif command == "end":
                    if environments and environments[-1] == value:
                        environments.pop()
                    else:
                        self.require(value not in environments, "native_closure", "invalid environment nesting: " + name)
                else:
                    self.require(value not in labels, "native_labels", "duplicate label: " + value)
                    environment = aliases.get(environments[-1], environments[-1]) if environments else None
                    labels[value] = {"source_file": name, "source_line": text.count("\n", 0, match.start()) + 1, "source_environment": environment, "source_sha256": row["sha256"]}
                    row["label_count"] += 1
            inputs = list(re.finditer(r"\\(?:input|include)\s*\{([^{}]+)\}", text))
            self.require(len(inputs) == len(re.findall(r"\\(?:input|include)\b", text)), "native_closure", "unparsed/dynamic input in " + name)
            for match in inputs:
                target = match.group(1)
                if not Path(target).suffix:
                    target += ".tex"
                self.require(not PurePosixPath(target).is_absolute() and ".." not in PurePosixPath(target).parts, "native_closure", "escaping input")
                edges.append({"from": name, "line": text.count("\n", 0, match.start()) + 1, "to": target})
                visit(target)

        visit("main.tex")
        core = [row["path"] for row in sources if re.fullmatch(r"core/\d{3}_[^/]+\.tex", row["path"])]
        numbers = [int(PurePosixPath(name).name[:3]) for name in core]
        self.require(len(sources) == 84 and len(labels) == 1125, "native_closure", "native file/label count differs")
        self.require(len(core) == 73 and sorted(numbers) == list(range(260, 333)), "native_closure", "not all core260--332 exactly once")
        self.require(sorted(row["path"] for row in sources) == self.manifest["reachable_tex_files"], "native_closure", "manifest reachable TeX differs")
        self.require(sorted(core) == self.manifest["active_core_files"], "native_closure", "manifest active core differs")
        joined = "\n".join(all_text)
        refs = [target.strip() for match in re.finditer(r"\\(?:eqref|ref|autoref|cref|Cref|pageref)\*?\s*\{([^{}]+)\}", joined) for target in match.group(1).split(",")]
        self.require(not (set(refs) - set(labels)), "native_references", "unresolved reference: " + str(sorted(set(refs) - set(labels))))
        bibliography = set(re.findall(r"\\bibitem(?:\[[^\]]*\])?\s*\{([^{}]+)\}", joined))
        citations = [key.strip() for match in re.finditer(r"\\cite\w*\*?(?:\[[^\]]*\])*\s*\{([^{}]+)\}", joined) for key in match.group(1).split(",")]
        self.require(set(citations) <= bibliography, "native_references", "unresolved bibliography entry")
        closure = self.source_gate["tex_closure"]
        self.require(closure["reachable_tex_files"] == sorted(stack_seen), "native_closure", "CI source closure differs")
        self.require(closure["active_label_count"] == len(labels) and closure["active_reference_count"] == len(refs), "native_references", "CI source label/reference count differs")
        self.require(closure["active_bibliography_keys"] == sorted(bibliography), "native_references", "CI bibliography list differs")
        self.require(closure["input_edges"] == [{"source": e["from"], "target": e["to"]} for e in edges], "native_closure", "CI source edges differ")
        self.sources, self.labels, self.edges = sources, labels, edges
        self.result["native_source_closure"] = {"source_files": len(sources), "active_core_files": len(core), "core_range": [260, 332], "input_order": numbers, "labels": len(labels), "references": len(refs), "bibliography_keys": sorted(bibliography), "closure_sha256": sha(canonical(sources)), "edges_sha256": sha(canonical(edges))}

    def current_receipt(self, receipt, directory, group):
        tag = receipt["tag"]
        self.require(read_json(directory / (tag + ".command.json")) == receipt, group, "embedded/file receipt mismatch: " + tag)
        self.require(receipt["exit_code"] == 0, group, "nonzero exit: " + tag)
        self.require(receipt["cwd"] == CI_ROOT, group, "wrong cwd: " + tag)
        self.require(receipt["current_mathematical_source_sha256"] == self.source["sha256"], group, "wrong command source: " + tag)
        self.require(receipt["log"] == tag + ".log", group, "wrong log name: " + tag)
        actual = identity(directory / receipt["log"])
        self.require(actual["bytes"] == receipt["log_bytes"] and actual["sha256"] == receipt["log_sha256"], group, "raw log digest differs: " + tag)
        start, finish = timevalue(receipt["started_utc"]), timevalue(receipt["finished_utc"])
        self.require(timevalue(self.phase["started_utc"]) <= start <= finish <= timevalue(self.phase["finished_utc"]), group, "receipt chronology outside phase: " + tag)
        self.require(receipt["elapsed_seconds"] >= 0 and abs((finish - start).total_seconds() - receipt["elapsed_seconds"]) < 0.5, group, "duration mismatch: " + tag)

    def math_check(self):
        print("Verifying 74 actual math receipts, 65 CI comparisons and 130 cross-environment outputs", flush=True)
        tree = ast.parse((self.article / "tools/validate_revision.py").read_text())
        assignments = {node.targets[0].id: node.value for node in tree.body if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)}
        programs = ast.literal_eval(assignments["PROGRAMS"])
        output_flags = ast.literal_eval(assignments["OUTPUT_FLAG"])
        details = set(programs[9:])
        self.require(len(programs) == len(set(programs)) == 37 and len(details) == 28, "math_schema", "program/detail count differs")
        self.require(set(NEW_COUNTS) <= set(programs), "math_schema", "new programs omitted")
        math = read_json(self.current / "mathematical-checks.json")
        self.require(math["status"] == "passed" and math["failures"] == [] and math["continuum_proof_certificate"] is False, "math_receipts", "wrong math status/scope")
        self.require(math["commands_completed"] == math["commands_expected"] == len(math["commands"]) == 74, "math_receipts", "math command count differs")
        self.require(math["mathematical_source"] == self.source, "math_receipts", "math source rows differ")
        tags = {p + "-" + mode for p in programs for mode in ("normal", "optimized")}
        self.require({r["tag"] for r in math["commands"]} == tags, "math_receipts", "missing/duplicate command tags")
        self.require({p.stem.removesuffix(".command") for p in self.current.glob("*-normal.command.json")} | {p.stem.removesuffix(".command") for p in self.current.glob("*-optimized.command.json")} == tags, "math_receipts", "artifact receipt set differs")
        for receipt in math["commands"]:
            self.current_receipt(receipt, self.current, "math_receipts")
            program, mode = receipt["tag"].rsplit("-", 1)
            argv = receipt["command"]
            self.require(argv[0] == "/opt/hostedtoolcache/Python/3.12.15/x64/bin/python3", "math_cli", "unexpected CI interpreter")
            expected = [argv[0]] + (["-O"] if mode == "optimized" else []) + ["-B", CI_ROOT + "/tools/" + program + ".py"]
            if program in details:
                output = CI_ROOT + "/build/current/" + receipt["tag"] + ".details.json"
                if program in {"check_all_label_likelihood", "check_marked_weak_operator"}:
                    expected += ["--details", "--output", output]
                else:
                    expected += ["--output" if program in output_flags else "--details", output]
            if program == "check_transversal_capacity":
                expected += ["--source-root", CI_ROOT, "--manuscript", CI_ROOT + "/core/321_all_class_transversal_capacity.tex"]
            if program == "check_positive_critical_fans":
                expected += ["--source", CI_ROOT + "/core/322_positive_critical_marked_source.tex"]
            if program == "verify_localization":
                expected += ["--source-root", CI_ROOT + "/core"]
            self.require(argv == expected, "math_cli", "wrong invocation: " + receipt["tag"])
        comparisons, cross, differences = [], [], []
        for program in programs:
            scopes = [(".log", "stdout")] + ([(".details.json", "details")] if program in details else [])
            for suffix, scope in scopes:
                normal = self.current / (program + "-normal" + suffix)
                optimized = self.current / (program + "-optimized" + suffix)
                method = "byte-identical"
                same = normal.read_bytes() == optimized.read_bytes()
                if program in RUNTIME_PROGRAMS:
                    left, right = read_json(normal), read_json(optimized)
                    self.require(left.get("optimized") is False and right.get("optimized") is True, "math_comparisons", "runtime optimization flag wrong")
                    for obj in (left, right):
                        for key in ("executed_utc", "optimized"):
                            obj.pop(key, None)
                    same = left == right
                    method = "identical mathematical JSON; runtime timestamp and optimization flag excluded"
                self.require(same, "math_comparisons", "normal/-O mismatch: " + program + "/" + scope)
                comparisons.append({"program": program, "scope": scope, "comparison": method, "match": same, "sha256": sha(normal.read_bytes())})
                for mode in ("normal", "optimized"):
                    name = program + "-" + mode + suffix
                    ci_path, local_path = self.current / name, self.local / "math" / name
                    ci_id, local_id = identity(ci_path), identity(local_path)
                    same_bytes = ci_path.read_bytes() == local_path.read_bytes()
                    row = {"file": name, "ci": ci_id, "committed_local": local_id, "byte_identical": same_bytes, "allowed_changed_fields": []}
                    if not same_bytes:
                        self.require(program in RUNTIME_PROGRAMS, "cross_environment", "unexplained changed output: " + name)
                        ci_data, local_data = read_json(ci_path), read_json(local_path)
                        self.require(ci_data.keys() == local_data.keys(), "cross_environment", "JSON key set differs: " + name)
                        changed = sorted(k for k in ci_data if ci_data[k] != local_data[k])
                        allowed = ["executed_utc", "python"] + (["source"] if program == "check_positive_critical_fans" else [])
                        self.require(changed == sorted(allowed), "cross_environment", "unapproved field changes: " + name + " " + str(changed))
                        for key in changed:
                            row["allowed_changed_fields"].append({"json_pointer": "/" + key, "committed_local_value": local_data[key], "ci_value": ci_data[key]})
                        self.require(str(ci_data["python"]).startswith("3.12.15 ") and str(local_data["python"]).startswith("3.12.14 "), "cross_environment", "unexpected interpreter metadata")
                        self.require(timevalue(ci_data["executed_utc"]) > timevalue(local_data["executed_utc"]), "cross_environment", "execution timestamps inconsistent")
                        if program == "check_positive_critical_fans":
                            rel = "/core/322_positive_critical_marked_source.tex"
                            self.require(ci_data["source"] == CI_ROOT + rel and local_data["source"] == str(self.article) + rel, "cross_environment", "source relocation is not the identical bound input")
                        for key in allowed:
                            ci_data.pop(key)
                            local_data.pop(key)
                        self.require(ci_data == local_data, "cross_environment", "stable mathematical JSON differs: " + name)
                        row["stable_json_sha256"] = sha(canonical(ci_data))
                        differences.append(row)
                    row["stable_output_matches"] = True
                    cross.append(row)
        self.require(comparisons == math["normal_optimized_comparisons"], "math_comparisons", "stored CI comparison report differs from reconstruction")
        self.require(len(comparisons) == 65 and len(cross) == 130 and len(differences) == 8, "math_comparisons", "comparison count differs")
        counts = {}
        for program, expected_count in NEW_COUNTS.items():
            data = read_json(self.current / (program + "-normal.details.json"))
            count = data.get("total_checks", data.get("check_count"))
            self.require(data["status"] == "passed" and count == expected_count, "new_checks", "new exact checker count/status differs")
            counts[program] = count
            if "source_binding" in data:
                binding = data["source_binding"]
                self.require(binding["predecessor_commit"] == EXPECTED["predecessor_commit"] and binding["predecessor_article_tree"] == EXPECTED["predecessor_article_tree"], "new_checks", "new checker predecessor binding")
                for name, claimed in binding["sources"].items():
                    relative = name if "/" in name or name in {"inputs.tex", "model.tex"} else ("tools/" if name.endswith(".py") else "core/") + name
                    self.check_identity(self.article / relative, claimed, "new_checks")
            else:
                for name, digest in data["source_sha256"].items():
                    self.require(sha((self.article / name).read_bytes()) == digest, "new_checks", "geometry checker source binding: " + name)
        self.result["mathematical_execution"] = {"programs": programs, "actual_commands": 74, "all_command_logs_rehashed": True, "all_command_argv_reconstructed": True, "ci_normal_optimized_comparisons": comparisons, "ci_comparison_count": 65, "ci_strict_byte_comparisons": sum(c["comparison"] == "byte-identical" for c in comparisons), "ci_runtime_field_only_comparisons": sum(c["comparison"] != "byte-identical" for c in comparisons), "cross_environment_file_count": 130, "cross_environment_byte_identical": sum(c["byte_identical"] for c in cross), "cross_environment_disclosed_difference_count": len(differences), "cross_environment_files": cross, "cross_environment_differences": differences, "new_exact_finite_check_counts": counts, "continuum_proof_certificate": False}

    @staticmethod
    def braced(text, pos):
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos >= len(text) or text[pos] != "{":
            raise RuntimeError("Expected a braced auxiliary group")
        begin, depth = pos + 1, 1
        pos += 1
        while pos < len(text):
            char = text[pos]
            if char == "\\":
                pos += 2
                continue
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[begin:pos], pos + 1
            pos += 1
        raise RuntimeError("Unclosed auxiliary group")

    def pdf_pair(self, ci_path, local_path, expected_pages, group):
        ci, local = PdfReader(ci_path), PdfReader(local_path)
        self.require(len(ci.pages) == len(local.pages) == expected_pages, group, "actual PDF page count differs")
        text_hashes, stream_hashes, stream_different = [], [], []
        for number, (a, b) in enumerate(zip(ci.pages, local.pages), 1):
            a_text, b_text = a.extract_text(), b.extract_text()
            self.require(a_text == b_text, group, f"actual PDF extracted text differs on page {number}")
            self.require(list(a.mediabox) == list(b.mediabox) and list(a.cropbox) == list(b.cropbox), group, f"PDF page boxes differ on page {number}")
            text_hashes.append(sha(a_text.encode()))
            a_stream, b_stream = a.get_contents().get_data(), b.get_contents().get_data()
            stream_hashes.append({"page": number, "ci_sha256": sha(a_stream), "local_sha256": sha(b_stream)})
            if a_stream != b_stream:
                stream_different.append(number)
        metadata_diff = {key: {"ci": str(ci.metadata.get(key)), "committed_local": str(local.metadata.get(key))} for key in sorted(set(ci.metadata) | set(local.metadata)) if ci.metadata.get(key) != local.metadata.get(key)}
        return ci, {"ci": identity(ci_path), "committed_local": identity(local_path), "pages": expected_pages, "all_page_text_exactly_equal": True, "all_page_boxes_equal": True, "text_page_hashes": text_hashes, "text_page_hash_list_sha256": sha(canonical(text_hashes)), "page_content_streams": stream_hashes, "content_stream_different_pages": stream_different, "metadata_differences": metadata_diff, "binary_identical": ci_path.read_bytes() == local_path.read_bytes(), "pdf_reader": "pypdf " + pypdf.__version__}

    def log_problems(self, text):
        checks = {"undefined_reference": r"LaTeX Warning:.*undefined|Reference .+ undefined|Citation .+ undefined", "multiply_defined": r"multiply defined", "overfull_box": r"Overfull \\[hv]box", "missing_character": r"Missing character:", "tex_error": r"^!"}
        return {key: re.findall(pattern, text, re.M) for key, pattern in checks.items() if re.search(pattern, text, re.M)}

    def native_check(self):
        print("Reading actual current PDF, all 1,125 destinations and 255 local/CI page pairs", flush=True)
        typeset = read_json(self.current / "native-typeset.json")
        native = self.current / "native"
        self.require(typeset["status"] == "passed" and typeset["mathematical_proof_certificate"] is False, "native_build", "wrong typeset status/scope")
        self.require(typeset["mathematical_source"] == self.source and typeset["pages"] == 255, "native_build", "typeset source/page mismatch")
        self.require(typeset["pdf_sha256"] == sha((native / "main.pdf").read_bytes()) and typeset["pdf_bytes"] == (native / "main.pdf").stat().st_size, "native_build", "CI native PDF identity")
        self.require(typeset["main_tex_sha256"] == sha((self.article / "main.tex").read_bytes()) and typeset["aux_sha256"] == sha((native / "main.aux").read_bytes()), "native_build", "CI main/aux identity")
        self.require(len(typeset["commands"]) == 4, "native_build", "wrong compile receipt count")
        for i, receipt in enumerate(typeset["commands"]):
            self.current_receipt(receipt, native, "native_receipts")
            if i < 3:
                expected = ["pdflatex", "-recorder", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-output-directory=" + CI_ROOT + "/build/current/native", "main.tex"]
                self.require(receipt["tag"] == "pdflatex-pass" + str(i + 1) and receipt["command"] == expected, "native_receipts", "wrong pdflatex invocation")
                self.require(re.search(r"Output written on .*?\(255 pages, \d+ bytes\)", (native / receipt["log"]).read_text(), re.S) is not None, "native_receipts", "compile stdout missing 255-page success")
            else:
                self.require(receipt["command"] == ["pdfinfo", CI_ROOT + "/build/current/native/main.pdf"], "native_receipts", "wrong pdfinfo argv")
                self.require(re.search(r"^Pages:\s+255\s*$", (native / receipt["log"]).read_text(), re.M) is not None, "native_receipts", "pdfinfo missing255")
        proof_receipt = read_json(self.current / "proof-navigation.command.json")
        self.current_receipt(proof_receipt, self.current, "native_receipts")
        self.require(proof_receipt["command"][1:] == ["-B", CI_ROOT + "/tools/build_proof_index.py", "--aux", CI_ROOT + "/build/current/native/main.aux", "--pdf", CI_ROOT + "/build/current/native/main.pdf", "--index", CI_ROOT + "/build/current/PROOF_INDEX.json", "--navigation", CI_ROOT + "/build/current/PROOF_NAVIGATION.md"], "native_receipts", "wrong navigation invocation")
        recorder = set()
        for line in (native / "main.fls").read_text().splitlines():
            if not line.startswith("INPUT "):
                continue
            value = line[6:]
            if value.startswith(CI_ROOT + "/"):
                value = value[len(CI_ROOT) + 1:]
            elif value.startswith("/"):
                continue
            value = str(PurePosixPath(value))
            if value.endswith(".tex") and not value.startswith(("history/", "build/", "evidence/")):
                recorder.add(value)
        self.require(recorder == {r["path"] for r in self.sources}, "native_recorder", "actual fls closure differs")
        self.require(sorted(recorder) == typeset["actual_recorder_native_tex"] and typeset["actual_recorder_matches_declared_closure"] is True, "native_recorder", "stored recorder result differs")
        final_log = (native / "main.log").read_text()
        self.require(not self.log_problems(final_log) and typeset["layout_or_reference_problems"] == [], "native_log", "final native log has diagnostic failures")
        advisories = re.findall(r"Package amsmath Warning:[^\n]*", final_log)
        self.require(advisories == typeset["advisories"], "native_log", "advisories not accurately retained")
        aux, metadata = {}, []
        for lineno, line in enumerate((native / "main.aux").read_text().splitlines(), 1):
            if not line.startswith("\\newlabel"):
                continue
            name, pos = self.braced(line, len("\\newlabel"))
            payload, pos = self.braced(line, pos)
            if name.startswith("tocindent"):
                metadata.append(name)
                continue
            self.require(name not in aux, "aux_labels", "duplicate aux label: " + name)
            fields, pos = [], 0
            while pos < len(payload):
                field, pos = self.braced(payload, pos)
                fields.append(field)
            self.require(len(fields) == 5, "aux_labels", "malformed aux reference")
            aux[name] = {"number": fields[0], "auxiliary_page_label": fields[1], "title_tex": fields[2], "pdf_anchor": fields[3], "aux_line": lineno}
        self.require(set(aux) == set(self.labels) and len(aux) == 1125 and len(metadata) == 5, "aux_labels", "source/aux bijection failed")
        local_native = self.local / "typeset/native/main.pdf"
        local_typeset = read_json(self.local / "typeset/native-typeset.json")
        self.require(identity(local_native)["sha256"] == local_typeset["pdf_sha256"], "local_evidence", "committed local native PDF receipt differs")
        pdf, pair = self.pdf_pair(native / "main.pdf", local_native, 255, "native_pdf")
        self.require((native / "main.aux").read_bytes() == (self.local / "typeset/native/main.aux").read_bytes(), "native_pdf", "local/CI aux not byte identical")
        index = read_json(self.current / "PROOF_INDEX.json")
        local_index = read_json(self.local / "typeset/PROOF_INDEX.json")
        self.require(index["input_closure"] == self.sources and index["input_edges"] == self.edges, "proof_index", "proof index source closure differs")
        self.require(index["schema"] == "A2-DYN-current-native-proof-navigation-v3", "proof_index", "wrong index schema")
        for key in set(index) - {"evidence"}:
            self.require(index[key] == local_index[key], "proof_index", "local/CI proof navigation differs: " + key)
        self.require(index["evidence"]["pdf"]["sha256"] == pair["ci"]["sha256"] and index["evidence"]["auxiliary"]["sha256"] == typeset["aux_sha256"], "proof_index", "index artifact identities")
        self.require(index["evidence"]["generator"]["sha256"] == sha((self.article / "tools/build_proof_index.py").read_bytes()), "proof_index", "index generator source identity")
        named = pdf.named_destinations
        page_labels = pdf.page_labels
        offsets, seen = [], set()
        for item in index["labels"]:
            name = item["label"]
            self.require(name not in seen and name in aux and name in self.labels, "proof_index", "index label omitted/duplicated")
            seen.add(name)
            for key, value in self.labels[name].items():
                self.require(item[key] == value, "proof_index", "source field differs: " + name + "/" + key)
            for key, value in aux[name].items():
                self.require(item[key] == value, "proof_index", "aux field differs: " + name + "/" + key)
            self.require(item["pdf_anchor"] in named, "pdf_destinations", "missing actual PDF destination: " + name)
            page = pdf.get_destination_page_number(named[item["pdf_anchor"]]) + 1
            self.require(page == item["pdf_page"] and page_labels[page - 1] == item["pdf_page_label"], "pdf_destinations", "actual destination page differs: " + name)
            if item["auxiliary_page_label"] != item["pdf_page_label"]:
                heading = item["kind"].capitalize() + " " + item["number"]
                self.require(heading in pdf.pages[page - 1].extract_text(), "pdf_destinations", "offset heading not on actual PDF page")
                offsets.append({"label": name, "number": item["number"], "auxiliary_page_label": item["auxiliary_page_label"], "actual_pdf_page": page, "printed_pdf_page_label": item["pdf_page_label"], "actual_heading_text_verified": heading})
        self.require(seen == set(self.labels), "proof_index", "index label set differs")
        self.require(offsets == index["validation"]["auxiliary_page_offsets"] and len(offsets) == 7, "pdf_destinations", "actual offset list differs")
        new_files = {r["path"] for r in self.sources if re.fullmatch(r"core/(?:327|328|329|330|331|332)_[^/]+\.tex", r["path"])}
        self.require(len(new_files) == 6 and sum(r["label_count"] for r in self.sources if r["path"] in new_files) == 94, "proof_index", "new body/label count differs")
        self.result["native_build"] = {"pages": 255, "pdflatex_passes": 3, "pdfinfo_commands": 1, "navigation_commands": 1, "actual_recorder_exact_closure": True, "source_aux_pdf_bijection_labels": 1125, "active_core_bodies": 73, "new_core_bodies": 6, "new_labels": 94, "aux_sha256": typeset["aux_sha256"], "local_aux_byte_identical": True, "index_stable_fields_equal_local": True, "actual_pdf_page_offsets": offsets, "legacy_amsmath_advisories": advisories, "pdf_comparison": pair}

    def historical_check(self):
        print("Verifying original historical assembler, six TeX passes, raw logs and 26/883 PDF page pairs", flush=True)
        summary = read_json(self.historical / "REBUILD_SUMMARY.json")
        receipts = list((self.historical / "execution").glob("*/REBUILD_RECEIPT.json"))
        self.require(len(receipts) == 1, "historical", "historical receipt is missing/ambiguous")
        receipt_path = receipts[0]
        receipt = read_json(receipt_path)
        local_receipts = list((self.local / "historical/execution").glob("*/REBUILD_RECEIPT.json"))
        self.require(len(local_receipts) == 1, "historical", "committed local historical receipt missing/ambiguous")
        local_receipt = read_json(local_receipts[0])
        self.require(summary["exit_code"] == 0 and summary["continuum_proof_certificate"] is False and summary["historical_repository_wide_gate_executed"] is False, "historical", "historical wrapper status/scope")
        self.require(receipt["success"] is True and receipt["historical_whole_repository_gate_executed"] is False and receipt["mathematical_proof_certificate"] is False, "historical", "historical receipt status/scope")
        self.require(timevalue(self.phase["finished_utc"]) <= timevalue(summary["started_utc"]) <= timevalue(receipt["started_utc"]) <= timevalue(receipt["completed_utc"]) <= timevalue(summary["finished_utc"]), "historical", "historical rebuild chronology inconsistent")
        self.require(receipt["source_files_checked"] == local_receipt["source_files_checked"] == 390, "historical", "historical source file count differs")
        self.require(receipt["generated_supplement_source"] == local_receipt["generated_supplement_source"], "historical", "historical generated source identity differs")
        self.check_identity(self.historical / "rebuild.stdout.log", summary["log"], "historical_logs")
        wrapper = read_json(self.historical / "rebuild.stdout.log")
        self.require(wrapper["success"] is True and wrapper["documents"] == receipt["documents"], "historical_logs", "wrapper stdout inconsistent with actual receipt")
        self.require(PurePosixPath(wrapper["receipt"]).name == receipt_path.name and PurePosixPath(wrapper["receipt"]).parent.name == receipt_path.parent.name, "historical_logs", "wrapper points to wrong receipt")
        self.require(len(receipt["commands"]) == 9, "historical_commands", "wrong historical command count")
        sequence = [("assembler", None)] + [("pdflatex", "supplement")] * 3 + [("pdflatex", "main")] * 3 + [("pdfinfo", "main"), ("pdfinfo", "supplement")]
        previous_start = timevalue(receipt["started_utc"])
        command_ids = []
        for row, (kind, document) in zip(receipt["commands"], sequence):
            self.require(row["returncode"] == 0, "historical_commands", "nonzero historical command")
            start = timevalue(row["started_utc"])
            self.require(previous_start <= start <= timevalue(receipt["completed_utc"]) and row["elapsed_seconds"] >= 0, "historical_commands", "historical command chronology")
            previous_start = start
            log = receipt_path.parent / PurePosixPath(row["output"]).name
            command_ids.append({"file": log.name, **self.check_identity(log, row["output_identity"], "historical_logs")})
            argv = row["argv"]
            if kind == "assembler":
                self.require(argv == ["/opt/hostedtoolcache/Python/3.12.15/x64/bin/python3", "tools/assemble_v105.py"], "historical_commands", "wrong historical assembler invocation")
            elif kind == "pdflatex":
                self.require(argv == ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-output-directory=build", document + ".tex"], "historical_commands", "wrong historical pdflatex invocation")
                pages = 26 if document == "main" else 883
                self.require(re.search(r"Output written on build/" + document + r"\.pdf \(" + str(pages) + r" pages, \d+ bytes\)", log.read_text()) is not None, "historical_logs", "historical success/page count not in raw stdout")
            else:
                self.require(argv == ["pdfinfo", receipt["cwd"] + "/build/" + document + ".pdf"], "historical_commands", "wrong historical pdfinfo invocation")
                pages = 26 if document == "main" else 883
                self.require(re.search(r"^Pages:\s+" + str(pages) + r"\s*$", log.read_text(), re.M) is not None, "historical_logs", "historical pdfinfo page count differs")
        docs = []
        local_summary = read_json(self.local / "historical/REBUILD_SUMMARY.json")
        for item, local_item in zip(receipt["documents"], local_receipt["documents"]):
            document = item["document"]
            self.require(document == local_item["document"] and item["pages"] == local_item["pages"], "historical", "historical document map differs")
            pages = 26 if document == "main" else 883
            ci_pdf = self.historical / ("historical-" + document + ".pdf")
            local_pdf = self.article / "delivery" / ("historical-" + document + ".pdf")
            self.check_identity(ci_pdf, item["pdf"], "historical_documents")
            self.check_identity(local_pdf, local_item["pdf"], "historical_documents")
            matching = [r for r in summary["documents"] if PurePosixPath(r["path"]).name == ci_pdf.name]
            self.require(len(matching) == 1, "historical_documents", "wrapper document map")
            self.check_identity(ci_pdf, matching[0], "historical_documents")
            log = receipt_path.parent / (document + ".final.log")
            self.check_identity(log, item["log"], "historical_documents")
            log_text = log.read_text()
            self.require(not self.log_problems(log_text), "historical_logs", "historical final log has failure diagnostics")
            self.require(re.search(r"Output written on build/" + document + r"\.pdf \(" + str(pages) + r" pages, \d+ bytes\)", log_text) is not None, "historical_logs", "historical final log page count")
            self.require(re.findall(r"Package amsmath Warning:[^\n]*", log_text) == item["diagnostics"] == local_item["diagnostics"], "historical_logs", "historical advisory mismatch")
            _, pair = self.pdf_pair(ci_pdf, local_pdf, pages, "historical_pdf")
            docs.append({"document": document, "pages": pages, "raw_final_log": identity(log), "advisories": item["diagnostics"], "pdf_comparison": pair})
            print(f"Historical {document}: verified all {pages} actual local/CI PDF page pairs", flush=True)
        self.result["historical_build"] = {"actual_commands": 9, "assembler_commands": 1, "pdflatex_passes": 6, "pdfinfo_commands": 2, "source_files_checked_by_ci_rebuild": 390, "generated_supplement_source_identity_equal_local": receipt["generated_supplement_source"], "generated_supplement_source_bytes_independently_available": False, "historical_repository_wide_gate_executed": False, "raw_command_logs": command_ids, "documents": docs, "ci_receipt_sha256": identity(receipt_path)["sha256"], "committed_local_receipt_sha256": identity(local_receipts[0])["sha256"]}

    def run(self):
        for method in (self.archive_check, self.source_check, self.closure_check, self.math_check, self.native_check, self.historical_check):
            method()
        self.result["status"] = "passed_with_explicit_scope"
        self.result["checks_by_group"] = dict(sorted(self.checks.items()))
        self.result["total_explicit_conditions"] = sum(self.checks.values())
        self.result["checker"] = {"file": Path(__file__).name, **identity(Path(__file__))}
        return self.result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--article-root", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    permitted = Path(__file__).resolve().parent
    if output.parent != permitted:
        raise RuntimeError("Result output must remain in this independent audit directory")
    audit = Audit(args.article_root, args.artifact_root, args.archive)
    try:
        result = audit.run()
        code = 0
    except Exception as exc:
        traceback.print_exc()
        result = audit.result
        result.update(status="failed", error=str(exc), checks_by_group=dict(sorted(audit.checks.items())), total_explicit_conditions=sum(audit.checks.values()), checker={"file": Path(__file__).name, **identity(Path(__file__))})
        code = 1
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "result": str(output), "total_explicit_conditions": result["total_explicit_conditions"], "mathematical_proof_certificate": False}, sort_keys=True), flush=True)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
