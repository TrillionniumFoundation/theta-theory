#!/usr/bin/env python3
"""Verify an actual A2-DYN CI ZIP against frozen published bytes and local receipts.

The verifier does not execute archive code or extract archive files. All inputs
are explicit. A successful result refers only to the observed exact run/head.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import zipfile


def require(value, message):
    if not value:
        raise RuntimeError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_object(kind, data):
    return hashlib.sha1(kind.encode() + b" " + str(len(data)).encode()
                        + b"\0" + data).hexdigest()


def utc(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.tzinfo is not None, "Timestamp has an explicit UTC offset")
    return result


def load(path):
    return json.loads(path.read_bytes())


def safe_path(value):
    p = PurePosixPath(value)
    require(value and not p.is_absolute() and ".." not in p.parts
            and "\\" not in value and str(p) == value,
            "Safe normalized relative path: " + value)
    return value


def mathematical_path(value):
    p = PurePosixPath(value)
    return ((len(p.parts) == 1 and p.suffix == ".tex")
            or (len(p.parts) == 2 and p.parts[0] == "core" and p.suffix == ".tex")
            or (len(p.parts) == 2 and p.parts[0] == "tools" and p.suffix == ".py"))


def pdf_pages(data):
    result = subprocess.run(["pdfinfo", "-"], input=data, capture_output=True)
    require(result.returncode == 0, "Independent actual PDF inspection succeeds")
    match = re.search(rb"^Pages:\s+(\d+)\s*$", result.stdout, re.M)
    require(match is not None, "Actual PDF has a readable page count")
    return int(match.group(1))


def file_identity(data):
    return {"bytes": len(data), "sha256": digest(data),
            "git_blob": git_object("blob", data)}


def expected_tree(rows):
    """Reconstruct canonical Git trees from every published expected file row."""
    root = {}
    for row in rows:
        parts = PurePosixPath(safe_path(row["path"])).parts
        node = root
        for part in parts[:-1]:
            require(not isinstance(node.get(part), tuple), "No file/tree path collision")
            node = node.setdefault(part, {})
        require(parts[-1] not in node, "Unique expected file path")
        mode = row["mode"]
        require(mode in ("100644", "100755", "120000"), "Known expected Git blob mode")
        require(re.fullmatch(r"[0-9a-f]{40}", row["sha"]), "Valid expected Git blob")
        node[parts[-1]] = (mode, row["sha"])
    hashes = {}

    def descend(node, prefix):
        entries = []
        for name, entry in node.items():
            if isinstance(entry, dict):
                h = descend(entry, prefix + name + "/")
                entries.append((name + "/", "40000", name, h))
            else:
                entries.append((name, entry[0], name, entry[1]))
        raw = b"".join(mode.encode() + b" " + name.encode() + b"\0"
                       + bytes.fromhex(h)
                       for _, mode, name, h in sorted(entries, key=lambda e: e[0].encode()))
        h = git_object("tree", raw)
        hashes[prefix.rstrip("/")] = h
        return h

    return descend(root, ""), hashes


def normalize_command(argv, article_name):
    """Retain actual program/options while normalizing known execution paths."""
    require(isinstance(argv, list) and argv, "Nonempty actual argv")
    normalized = []
    previous = None
    marker = "/" + article_name + "/"
    for index, value in enumerate(argv):
        require(isinstance(value, str), "Actual argv consists of strings")
        if index == 0:
            executable = Path(value).name
            normalized.append("python" if re.fullmatch(r"python(?:3(?:\.\d+)?)?", executable)
                              else executable)
        elif previous in ("--details", "--output"):
            require(value.endswith(".details.json"), "Recognized mathematical details output")
            normalized.append("<output>/" + Path(value).name)
        elif value.startswith("-output-directory="):
            target = value.split("=", 1)[1]
            require(Path(target).name in ("native", "build"), "Recognized TeX output directory")
            normalized.append("-output-directory=<output>/" + Path(target).name)
        elif marker in value:
            relative = value.split(marker, 1)[1]
            if relative.startswith(("build/current/", "evidence/current-execution/")):
                require(relative.endswith("/native/main.pdf"), "Recognized PDF inspection path")
                normalized.append("<output>/native/main.pdf")
            else:
                normalized.append("<article>/" + relative)
        else:
            require(not value.startswith("/"), "No unrecognized absolute argv path: " + value)
            normalized.append(value)
        previous = value
    return normalized


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--article", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--tested-commit", required=True)
    parser.add_argument("--tested-article-tree", required=True)
    parser.add_argument("--tested-root-tree")
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--expected-identities", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--reference-build", type=Path, required=True,
                        help="Final local mathematical-checks.json/native-typeset.json directory")
    parser.add_argument("--reference-source", type=Path,
                        help="Separate final local source-checks.json, if not in reference-build")
    parser.add_argument("--reference-history", type=Path, required=True,
                        help="Actual final local historical REBUILD_RECEIPT.json")
    parser.add_argument("--observation", type=Path, required=True,
                        help="Fresh purpose-built GitHub run/jobs/artifacts JSON")
    parser.add_argument("--artifact-id", type=int, required=True)
    parser.add_argument("--job-id", type=int, required=True)
    parser.add_argument("--job-log-identity", type=Path, required=True)
    parser.add_argument("--job-log", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    started = datetime.now(timezone.utc).isoformat()
    article = args.article.resolve()
    article_name = article.name
    require((article / "main.tex").is_file(), "Complete article main.tex exists")
    require(re.fullmatch(r"[0-9a-f]{40}", args.tested_commit), "Exact tested commit SHA")
    require(re.fullmatch(r"[0-9a-f]{40}", args.tested_article_tree), "Exact tested article tree")
    expected_doc = load(args.expected_identities)
    expected = {row["path"]: row for row in expected_doc["files"]}
    require(len(expected) == len(expected_doc["files"]), "Unique published identity rows")
    tree, tree_hashes = expected_tree(expected_doc["files"])
    require(tree == expected_doc["article_tree_sha"] == args.tested_article_tree,
            "Complete expected file list reconstructs exact tested article tree")
    for name, h in expected_doc.get("subtree_hashes", {}).items():
        require(tree_hashes[name] == h, "Canonical expected subtree: " + name)

    local_identities = []

    def checked_local(path):
        path = path.resolve()
        require(path.is_relative_to(article), "Local reference lies inside published article")
        relative = path.relative_to(article).as_posix()
        require(relative in expected, "Local reference is in tested expected tree: " + relative)
        data = path.read_bytes()
        identity = file_identity(data)
        e = expected[relative]
        require(identity["bytes"] == e["bytes"] and identity["sha256"] == e["sha256"]
                and identity["git_blob"] == e["sha"],
                "Actual local bytes match exact tested file: " + relative)
        local_identities.append({"path": relative, **identity})
        return data

    manifest_path = args.manifest or article / "SOURCE_MANIFEST.json"
    manifest_data = checked_local(manifest_path)
    manifest = json.loads(manifest_data)
    manifest_rows = manifest["files"]
    require(manifest["source_count"] == len(manifest_rows)
            == len({r["path"] for r in manifest_rows}), "All frozen source rows unique")
    require(sum(r["bytes"] for r in manifest_rows) == manifest["source_bytes"],
            "Frozen source byte total")
    for row in manifest_rows:
        data = checked_local(article / safe_path(row["path"]))
        require(file_identity(data) == {k: row[k] for k in ("bytes", "sha256", "git_blob")},
                "Frozen source record identity: " + row["path"])

    mathematical_rows = [{"path": p, "sha256": expected[p]["sha256"]}
                         for p in sorted(expected) if mathematical_path(p)]
    require(mathematical_rows, "Nonempty native/tool identity set")
    mathematical_sha = digest(json.dumps(mathematical_rows, sort_keys=True).encode())
    for row in mathematical_rows:
        require(digest(checked_local(article / row["path"])) == row["sha256"],
                "Native/tool bytes match tested source: " + row["path"])

    ref_math = json.loads(checked_local(args.reference_build / "mathematical-checks.json"))
    ref_native = json.loads(checked_local(args.reference_build / "native-typeset.json"))
    ref_source = json.loads(checked_local(args.reference_source
                           or args.reference_build / "source-checks.json"))
    ref_history = json.loads(checked_local(args.reference_history))
    for name, receipt in (("math", ref_math), ("native", ref_native), ("source", ref_source)):
        require(receipt["status"] == "passed", "Final local reference passed: " + name)
        require(receipt["mathematical_source"]["files"] == mathematical_rows
                and receipt["mathematical_source"]["sha256"] == mathematical_sha,
                "Final local reference matches complete tested mathematical source: " + name)
    require(not ref_math["failures"] and not ref_native["layout_or_reference_problems"],
            "Final local reference has no mathematical/layout failures")
    require(ref_history["success"] and len(ref_history["commands"]) == 9,
            "Final local historical reference completed all nine commands")
    reference_native_pdf = checked_local(args.reference_build / "native/main.pdf")
    reference_native_aux = checked_local(args.reference_build / "native/main.aux")
    require(digest(reference_native_pdf) == ref_native["pdf_sha256"]
            and len(reference_native_pdf) == ref_native["pdf_bytes"]
            and pdf_pages(reference_native_pdf) == ref_native["pages"],
            "Actual final local PDF identity and pages")
    require(digest(reference_native_aux) == ref_native["aux_sha256"],
            "Actual final local auxiliary-file identity")
    ref_math_tags = {c["tag"]: c for c in ref_math["commands"]}
    require(len(ref_math_tags) == ref_math["commands_expected"]
            == ref_math["commands_completed"] == len(ref_math["commands"]),
            "Final local mathematical command contract is complete")
    ref_pairs = {(c["program"], c["scope"]): c
                 for c in ref_math["normal_optimized_comparisons"]}
    require(len(ref_pairs) == len(ref_math["normal_optimized_comparisons"])
            and all(c["byte_identical"] for c in ref_pairs.values()),
            "Final local normal/optimized contract is complete")

    observation = load(args.observation)
    run = observation["run"]
    require(run["head_sha"] == args.tested_commit and run["path"] == args.workflow
            and run["event"] == "push", "Actual dedicated push run at exact tested head")
    require(run["status"] == "completed" and run["conclusion"] == "success",
            "Actual run completed successfully")
    jobs = observation["jobs"]["jobs"]
    require(len(jobs) == 1 and jobs[0]["id"] == args.job_id
            and jobs[0]["run_id"] == run["id"]
            and jobs[0]["status"] == "completed" and jobs[0]["conclusion"] == "success",
            "Actual dedicated job completed successfully")
    steps = jobs[0]["steps"]
    require(steps and all(s["status"] == "completed" and s["conclusion"] == "success"
                          for s in steps), "Every actual job step completed successfully")
    artifacts = [a for a in observation["artifacts"]["artifacts"]
                 if a["id"] == args.artifact_id]
    require(len(artifacts) == 1, "Unique observed artifact ID")
    artifact = artifacts[0]
    require(not artifact["expired"] and artifact["workflow_run"]["id"] == run["id"]
            and artifact["workflow_run"]["head_sha"] == args.tested_commit,
            "Unexpired artifact belongs to the exact observed run and head")
    archive_data = args.archive.read_bytes()
    archive_sha = digest(archive_data)
    require(len(archive_data) == artifact["size_in_bytes"]
            and artifact["digest"] == "sha256:" + archive_sha,
            "Actual downloaded bytes match advertised artifact size and digest")
    log_identity = load(args.job_log_identity)
    job_log = args.job_log.read_bytes()
    require(log_identity["job_id"] == args.job_id
            and log_identity["exact_returned_utf8_text"]
            and len(job_log) == log_identity["bytes"]
            and digest(job_log) == log_identity["sha256"],
            "Exact purpose-built job-log text and identity, with no appended newline")
    job_log.decode("utf-8")

    with zipfile.ZipFile(args.archive) as archive:
        entries = [entry for entry in archive.infolist() if not entry.is_dir()]
        names = [entry.filename for entry in entries]
        require(len(names) == len(set(names)), "No duplicate ZIP file paths")
        for entry in entries:
            safe_path(entry.filename)
            require(not stat.S_ISLNK(entry.external_attr >> 16), "No ZIP symbolic links")
        file_manifest = [{"path": entry.filename, **file_identity(archive.read(entry.filename))}
                         for entry in entries]
        require(archive.testzip() is None, "Every ZIP member CRC is valid")

        def read(name):
            return archive.read(safe_path(name))

        def json_read(name):
            return json.loads(read(name))

        prefix = "build/current/"
        require(read(prefix + "CI_CHECKOUT_SHA.txt").decode().strip() == args.tested_commit,
                "Actual archived checkout SHA")
        require(read(prefix + "CI_BUILD_OUTCOME.txt").decode().strip() == "success",
                "Actual archived complete build outcome")
        entrypoint_rows = []
        for line in read(prefix + "CI_ENTRYPOINT_SHA256.txt").decode().splitlines():
            h, name = line.split(None, 1)
            name = safe_path(name.lstrip("*"))
            require(h == expected[name]["sha256"], "Actual entrypoint bytes: " + name)
            entrypoint_rows.append({"path": name, "sha256": h})
        required_entrypoints = {"build.sh", "requirements.txt", "ci/" + Path(args.workflow).name}
        require({r["path"] for r in entrypoint_rows} == required_entrypoints
                and len(entrypoint_rows) == 3, "All three exact dedicated entrypoints")

        phase = json_read(prefix + "PHASE_all.json")
        require(phase["status"] == "passed"
                and set(phase["completed"]) == {"source", "math", "typeset"},
                "Actual CI source, math and native phases all completed")
        require(utc(run["run_started_at"]) <= utc(phase["started_utc"])
                <= utc(phase["finished_utc"]) <= utc(run["updated_at"]),
                "Actual complete phase lies within this CI run")
        require(phase["mathematical_source"]["files"] == mathematical_rows
                and phase["mathematical_source"]["sha256"] == mathematical_sha,
                "Actual CI mathematical fingerprint equals complete frozen native/tool source")

        def command_check(command, base, reference):
            data = read(base + safe_path(command["log"]))
            require(command["exit_code"] == 0 and len(data) == command["log_bytes"]
                    and digest(data) == command["log_sha256"]
                    and command["current_mathematical_source_sha256"] == mathematical_sha,
                    "Actual command result, log and source identity: " + command["tag"])
            require(utc(phase["started_utc"]) <= utc(command["started_utc"])
                    <= utc(command["finished_utc"]) <= utc(phase["finished_utc"]),
                    "Actual command belongs to this completed phase: " + command["tag"])
            require(Path(command["cwd"]).name == article_name,
                    "Actual command uses the requested article: " + command["tag"])
            require(normalize_command(command["command"], article_name)
                    == normalize_command(reference["command"], article_name),
                    "Actual program and options match final local contract: " + command["tag"])

        math = json_read(prefix + "mathematical-checks.json")
        require(math["status"] == "passed" and not math["failures"]
                and math["mathematical_source"] == phase["mathematical_source"],
                "Actual mathematical phase completed at the tested source")
        require(math["commands_expected"] == math["commands_completed"]
                == len(math["commands"]) == len(ref_math_tags)
                and {c["tag"] for c in math["commands"]} == set(ref_math_tags),
                "All actual mathematical programs and both interpreter modes are present")
        for command in math["commands"]:
            command_check(command, prefix, ref_math_tags[command["tag"]])
            require(json_read(prefix + command["tag"] + ".command.json") == command,
                    "Individual actual command receipt agrees: " + command["tag"])
        comparisons = math["normal_optimized_comparisons"]
        require(len(comparisons) == len(ref_pairs)
                and {(c["program"], c["scope"]) for c in comparisons} == set(ref_pairs),
                "All final-contract normal/optimized comparisons are present")
        for pair in comparisons:
            require(pair["scope"] in ("stdout", "details"), "Known paired output scope")
            suffix = ".log" if pair["scope"] == "stdout" else ".details.json"
            left = read(prefix + pair["program"] + "-normal" + suffix)
            right = read(prefix + pair["program"] + "-optimized" + suffix)
            require(pair["byte_identical"] and left == right and digest(left) == pair["sha256"],
                    "Actual normal/optimized bytes agree: " + pair["program"] + "/" + pair["scope"])

        source = json_read(prefix + "source-checks.json")
        require(source["status"] == "passed" and source["manifest"]["verified"]
                and not source["unresolved_references"]
                and source["mathematical_source"] == phase["mathematical_source"],
                "Actual complete source and reference gate")
        for key in ("original_reports_verified", "active_complete_core_bodies", "reachable_native_tex"):
            require(source[key] == ref_source[key], "Actual complete source count: " + key)
        for key in ("source_count", "source_bytes"):
            require(source["manifest"][key] == manifest[key] == ref_source["manifest"][key],
                    "Actual frozen manifest total: " + key)
        anchor_keys = [key for key in manifest if key.endswith("anchor_sha256")]
        require(anchor_keys, "Frozen inherited identity anchors are present")
        for key in anchor_keys:
            require(source["manifest"][key] == manifest[key] == ref_source["manifest"][key],
                    "Actual preserved identity anchor: " + key)

        native = json_read(prefix + "native-typeset.json")
        require(native["status"] == "passed" and not native["layout_or_reference_problems"]
                and native["mathematical_source"] == phase["mathematical_source"],
                "Actual native typeset and source identity")
        reference_native_commands = {c["tag"]: c for c in ref_native["commands"]}
        require(len(native["commands"]) == len(reference_native_commands) == 4
                and {c["tag"] for c in native["commands"]} == set(reference_native_commands)
                and sum(Path(c["command"][0]).name == "pdflatex"
                        for c in native["commands"]) == 3,
                "Three actual TeX passes and one PDF inspection")
        for command in native["commands"]:
            command_check(command, prefix + "native/", reference_native_commands[command["tag"]])
        native_pdf = read(prefix + "native/main.pdf")
        native_aux = read(prefix + "native/main.aux")
        require(digest(native_pdf) == native["pdf_sha256"]
                and len(native_pdf) == native["pdf_bytes"]
                and pdf_pages(native_pdf) == native["pages"] == ref_native["pages"],
                "Actual CI PDF identity and final native page count")
        require(digest(native_aux) == native["aux_sha256"] == ref_native["aux_sha256"],
                "Actual CI auxiliary file agrees with receipt and final local references")
        require(native["main_tex_sha256"] == expected["main.tex"]["sha256"],
                "Actual native main source identity")

        fresh = []
        older = []
        for name in names:
            if name.startswith("evidence/current-execution/historical-recovery/") \
                    and name.endswith("/REBUILD_RECEIPT.json"):
                receipt = json_read(name)
                if utc(receipt["started_utc"]) >= utc(phase["finished_utc"]):
                    fresh.append((name, receipt))
                else:
                    older.append({"path": name, "success": receipt["success"],
                                  "started_utc": receipt["started_utc"],
                                  "sha256": digest(read(name))})
        require(len(fresh) == 1, "Exactly one actual post-native historical rebuild from this CI")
        historical_path, history = fresh[0]
        require(history["success"] and len(history["commands"]) == len(ref_history["commands"]) == 9
                and history["source_files_checked"] == ref_history["source_files_checked"] == 390
                and utc(history["started_utc"]) <= utc(history["completed_utc"])
                <= utc(run["updated_at"]),
                "Actual fresh historical nine-command, 390-source rebuild")
        require(history["historical_whole_repository_gate_executed"] is False
                and history["mathematical_proof_certificate"] is False,
                "Historical rebuild retains its actual source/build-only scope")
        historical_prefix = str(PurePosixPath(historical_path).parent) + "/"
        for command, reference in zip(history["commands"], ref_history["commands"]):
            output = read(historical_prefix + Path(command["output"]).name)
            require(command["returncode"] == 0
                    and file_identity(output) == command["output_identity"],
                    "Actual historical command output identity")
            require(normalize_command(command["argv"], article_name)
                    == normalize_command(reference["argv"], article_name),
                    "Actual historical command matches final local rebuild contract")
            require(utc(history["started_utc"]) <= utc(command["started_utc"])
                    <= utc(history["completed_utc"]), "Actual historical command timestamp")
        reference_documents = {d["document"]: d for d in ref_history["documents"]}
        require(set(reference_documents) == {"main", "supplement"}
                and {d["document"] for d in history["documents"]} == set(reference_documents)
                and len(history["documents"]) == 2, "Both complete historical documents")
        documents = []
        for document in history["documents"]:
            name = document["document"]
            data = read("history/historical-v108/build/" + name + ".pdf")
            log = read("history/historical-v108/build/" + name + ".log")
            require(file_identity(data) == {k: document["pdf"][k]
                                           for k in ("bytes", "sha256", "git_blob")}
                    and pdf_pages(data) == document["pages"] == reference_documents[name]["pages"],
                    "Actual historical PDF identity and final page count: " + name)
            require(file_identity(log) == {k: document["log"][k]
                                          for k in ("bytes", "sha256", "git_blob")},
                    "Actual historical final log: " + name)
            for kind, suffix in (("pdf", ".pdf"), ("log", ".log")):
                require(document[kind]["path"].endswith(
                    "/" + article_name + "/history/historical-v108/build/" + name + suffix),
                    "Actual historical product belongs to the requested article: " + name)
            documents.append({"name": name, "pages": document["pages"],
                              "pdf_sha256": digest(data), "diagnostics": document["diagnostics"]})

        post_status = read(prefix + "CI_POST_RUN_STATUS.txt").decode().splitlines()
        allowed = ["papers/" + article_name + "/" + p for p in
                   ("build/", "history/historical-v108/build/",
                    "evidence/current-execution/historical-recovery/")]
        require(all(len(line) >= 4 and any(line[3:].startswith(p) for p in allowed)
                    for line in post_status), "Post-run changes are generated outputs only")
        environment = read(prefix + "CI_ENVIRONMENT.log").decode()
        require(re.match(r"Python 3\.11\.\d+\n", environment), "Actual Python 3.11 environment")
        requirements = checked_local(article / "requirements.txt").decode().splitlines()
        pinned = [line.strip() for line in requirements
                  if re.fullmatch(r"[A-Za-z0-9_.-]+==[^\s;]+", line.strip())]
        require(pinned and all(pin in environment.splitlines() for pin in pinned),
                "Actual environment contains every frozen numerical package pin")

    result = {
        "status": "passed", "verification_started_utc": started,
        "verified_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Actual observed CI artifact, command outputs and exact frozen source identities; no archive code executed",
        "run_id": run["id"], "job_id": args.job_id,
        "exact_head": args.tested_commit, "root_tree_sha": args.tested_root_tree,
        "article_tree_sha": args.tested_article_tree,
        "expected_git_subtrees_reconstructed": len(tree_hashes),
        "run_status": run["status"], "run_conclusion": run["conclusion"],
        "run_updated_utc": run["updated_at"], "actual_job_steps_verified": len(steps),
        "artifact_id": args.artifact_id, "artifact_bytes": len(archive_data),
        "artifact_sha256": archive_sha, "artifact_files": len(entries),
        "mathematical_source_sha256": mathematical_sha,
        "native_tool_inputs_verified_against_tested_head": len(mathematical_rows),
        "frozen_manifest_sha256": digest(manifest_data),
        "frozen_inputs_verified_against_tested_head": manifest["source_count"],
        "frozen_input_bytes": manifest["source_bytes"],
        "entrypoints_verified": entrypoint_rows,
        "phase_started_utc": phase["started_utc"], "phase_finished_utc": phase["finished_utc"],
        "math_commands_verified": len(math["commands"]),
        "normal_optimized_actual_pairs_verified": len(comparisons),
        "original_reports_verified": source["original_reports_verified"],
        "active_core_bodies": source["active_complete_core_bodies"],
        "reachable_native_tex": source["reachable_native_tex"],
        "native_compile_commands_verified": len(native["commands"]),
        "actual_pdflatex_passes": 3, "native_pages": native["pages"],
        "native_pdf_sha256": native["pdf_sha256"], "native_pdf_bytes": len(native_pdf),
        "native_aux_sha256": native["aux_sha256"],
        "native_aux_matches_final_local": True, "native_advisories": native["advisories"],
        "fresh_historical_receipt": historical_path,
        "fresh_historical_commands_verified": len(history["commands"]),
        "fresh_historical_sources_verified": history["source_files_checked"],
        "historical_documents": documents,
        "historical_started_utc": history["started_utc"],
        "historical_completed_utc": history["completed_utc"],
        "earlier_historical_receipts_preserved_separately": older,
        "post_run_changed_paths": post_status, "post_run_changes_only_generated": True,
        "environment": environment, "exact_job_log": log_identity,
        "local_reference_receipts_anchored_in_tested_tree": True,
        "actual_current_ci_success_verified": True,
        "continuum_mathematical_proof_certificate": False,
        "independent_human_specialist_certification": False,
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "CURRENT_CI_ARTIFACT_VERIFICATION.json").write_text(
        json.dumps(result, indent=2) + "\n")
    (args.output_dir / "CURRENT_CI_ARTIFACT_FILE_MANIFEST.json").write_text(
        json.dumps({"artifact_sha256": archive_sha, "files": file_manifest}, indent=2) + "\n")
    (args.output_dir / "ACTUAL_LOCAL_INPUT_IDENTITIES.json").write_text(
        json.dumps({"tested_commit": args.tested_commit, "files": local_identities}, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
