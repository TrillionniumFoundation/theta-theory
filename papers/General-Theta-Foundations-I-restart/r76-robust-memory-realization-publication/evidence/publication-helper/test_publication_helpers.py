#!/usr/bin/env python3
"""Small integrity challenges for the R76 received-byte helper.

Synthetic fixtures exercise transport and rejection mechanisms only. They are
not manuscripts, Git commits, build receipts or evidence of an actual release.
The current real historical corpus is checked separately without copying it.
"""
from __future__ import annotations
import contextlib
import copy
import hashlib
import io
import json
import pathlib
import sys
import tempfile
import warnings
import zipfile

sys.dont_write_bytecode = True
import restore_archives as h


def ident(data: bytes) -> dict:
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def tiny_zip(names: list[tuple[str, bytes]], *, symlink: bool = False) -> bytes:
    stream = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(stream, "w") as archive:
            for name, data in names:
                info = zipfile.ZipInfo(name)
                info.external_attr = ((0o120777 if symlink else 0o100644) << 16)
                archive.writestr(info, data)
    return stream.getvalue()


def main() -> None:
    checks = []

    def positive(name: str, fn) -> None:
        fn()
        checks.append({"name": name, "expected": "accepted", "observed": "accepted"})

    def rejected(name: str, fn, message: str) -> None:
        try:
            fn()
        except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as error:
            h.require(message in str(error), "Wrong rejection in " + name + ": " + str(error))
            checks.append({"name": name, "expected": "rejected", "observed": "rejected",
                           "reason": str(error)})
        else:
            raise RuntimeError("Corruption was accepted: " + name)

    with tempfile.TemporaryDirectory(prefix="r76-helper-fixture-", dir=pathlib.Path(__file__).parent) as work:
        root = pathlib.Path(work)
        (root / "archives").mkdir()
        payloads = {
            "source": tiny_zip([("source/readme.txt", b"synthetic source fixture only\n")]),
            "validation": tiny_zip([("validation/readme.txt", b"synthetic evidence fixture only\n")]),
            "historical": b"synthetic transport bytes, not a complete historical archive\n"}
        filenames = {"source": "General_Theta_Foundations_I_R76_Source.zip",
                     "validation": "General_Theta_Foundations_I_R76_Validation.zip",
                     "historical": "General_Theta_Foundations_I_R76_Historical_Text_Corpus.tar.gz"}
        source_pin, tree_pin = "a" * 40, "b" * 40
        parts = {"schema": "theta.r76.lossless-archive-parts.v1", "source_commit": source_pin,
                 "archives": []}
        files = []
        for role, payload in payloads.items():
            width = max(1, len(payload) // 3)
            part_rows = []
            for i, offset in enumerate(range(0, len(payload), width)):
                data = payload[offset:offset + width]
                name = f"archives/{role}-{i:03d}.part"
                (root / name).write_bytes(data)
                row = {"path": name, **ident(data)}
                part_rows.append(row)
                files.append(row)
            parts["archives"].append({"file": filenames[role], "role": role, **ident(payload),
                                      "format": "ordered raw byte concatenation", "parts": part_rows})

        def write_manifests(parts_value: dict = parts, schema: str = "theta.r76.delivery-manifest.v1") -> None:
            raw = canonical(parts_value)
            (root / "archives/ARCHIVE_PARTS.json").write_bytes(raw)
            delivery = {"schema": schema, "source_commit": source_pin, "source_paper_tree": tree_pin,
                        "manifest_excludes_itself": True,
                        "files": files + [{"path": "archives/ARCHIVE_PARTS.json", **ident(raw)}]}
            (root / "DELIVERY_MANIFEST.json").write_bytes(canonical(delivery))

        write_manifests()

        def transport_roundtrip() -> None:
            _, declared, _ = h.read_delivery(root, source_pin, tree_pin)
            with h.assembled_archives(root, declared) as output:
                h.require(set(output) == set(payloads), "Transport archive roles differ")
                for role, path in output.items():
                    h.require(path.read_bytes() == payloads[role], "Transport reconstruction differs")

        positive("complete ordered three-role transport round trip", transport_roundtrip)
        rejected("wrong independent source pin", lambda: h.read_delivery(root, "c" * 40, tree_pin),
                 "differs from the supplied pin")
        rejected("wrong independent source-tree pin", lambda: h.read_delivery(root, source_pin, "c" * 40),
                 "differs from the supplied pin")
        rejected("non-full independent SHA pin", lambda: h.read_delivery(root, "abc", tree_pin),
                 "full lowercase Git SHA")
        write_manifests(schema="theta.r75.delivery-manifest.v1")
        rejected("old revision cannot be reclassified as R76", lambda: h.read_delivery(root), "exact R76")
        write_manifests()

        first = root / parts["archives"][0]["parts"][0]["path"]
        correct = first.read_bytes()
        first.write_bytes(bytes([correct[0] ^ 1]) + correct[1:])
        rejected("one changed archive byte", lambda: h.read_delivery(root), "mismatch")
        first.write_bytes(correct[:-1])
        rejected("truncated archive part", lambda: h.read_delivery(root), "Wrong byte count")
        first.write_bytes(correct)
        (root / "unmanifested.txt").write_bytes(b"extra")
        rejected("unmanifested publication payload", lambda: h.read_delivery(root), "Unmanifested")
        (root / "unmanifested.txt").unlink()
        altered = copy.deepcopy(parts)
        altered["archives"][0]["parts"][:2] = reversed(altered["archives"][0]["parts"][:2])
        write_manifests(altered)
        rejected("reordered parts with consistent outer manifests", transport_roundtrip,
                 "Reassembled archive mismatch")
        write_manifests()
        positive("restored clean transport fixture", transport_roundtrip)

        rejected("duplicate JSON keys", lambda: h.parse_json(b'{"key":1,"key":2}'), "Duplicate JSON key")
        for unsafe in ("../escape", "/absolute", "a/../b", "a//b", "a\\b", "C:escape", "./a"):
            rejected("unsafe path " + repr(unsafe), lambda value=unsafe: h.relative_name(value), "Unsafe")

        def zip_check(data: bytes) -> None:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                h.zip_inventory(archive)

        positive("ordinary ZIP membership", lambda: zip_check(tiny_zip([("a.txt", b"a")])) )
        rejected("ZIP path traversal", lambda: zip_check(tiny_zip([("../escape", b"a")])), "Unsafe")
        rejected("ZIP symlink payload", lambda: zip_check(tiny_zip([("link", b"target")], symlink=True)), "symlink")
        rejected("duplicate ZIP payload", lambda: zip_check(tiny_zip([("a", b"1"), ("a", b"2")])), "Duplicate ZIP")

        def wrong_zip_payload() -> None:
            with zipfile.ZipFile(io.BytesIO(tiny_zip([("a", b"changed")]))) as archive:
                h.verify_zip_payload(archive, archive.getinfo("a"), ident(b"correct"), "a")

        rejected("ZIP payload differs beneath outer container", wrong_zip_payload, "SHA-256 mismatch")
        rejected("source Git-tree file/directory collision", lambda: h.git_tree({
            "a": {"mode": "100644", "git_blob": "a" * 40},
            "a/b": {"mode": "100644", "git_blob": "b" * 40}}), "File/directory conflict")

        source_manifest = {
            "schema": "theta.r76.exact-source-manifest.v1",
            "predecessor": {"commit": h.BASE_COMMIT, "source_commit": h.BASE_SOURCE_COMMIT,
                            "path": h.BASE_PATH, "git_tree": h.BASE_TREE,
                            "source_manifest_sha256": h.BASE_MANIFEST_SHA256},
            "controlling_report": {"commit": h.REVIEW_COMMIT, "path": h.REVIEW_PATH,
                                   "git_blob": h.REVIEW_BLOB, "sha256": h.REVIEW_SHA256},
            "inherited_statement_count": 209, "current_indexed_statement_count": 220,
            "complete_predecessor_file_count": 386, "files": []}

        def source_header_case(data: dict) -> None:
            path = root / "fixture-source.zip"
            path.write_bytes(tiny_zip([("fixture/SOURCE_MANIFEST.json", canonical(data))]))
            h.verify_source(path, {"file": "fixture.zip"}, {"source_paper_tree": tree_pin}, "r76")

        altered = copy.deepcopy(source_manifest)
        altered["predecessor"]["source_commit"] = "0" * 40
        rejected("wrong controlling R75 source identity", lambda: source_header_case(altered), "controlling complete R75")
        altered = copy.deepcopy(source_manifest)
        altered["controlling_report"]["sha256"] = "0" * 64
        rejected("wrong controlling R65 report identity", lambda: source_header_case(altered), "controlling R65")
        altered = copy.deepcopy(source_manifest)
        altered["current_indexed_statement_count"] = 219
        rejected("incomplete R76 statement-count declaration", lambda: source_header_case(altered), "statement or preservation counts")

    report = {"schema": "theta.r76.publication-helper-component-challenges.v1",
              "status": "PASS", "checks": checks, "check_count": len(checks),
              "scope": "Small synthetic transport and corruption challenges only; not a delivered manuscript or a final release verification.",
              "current_release_verified": False,
              "current_source_commit": None,
              "limits": "No build, mathematical diagnostic, proof checking, human assessment or editorial decision is performed."}
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
