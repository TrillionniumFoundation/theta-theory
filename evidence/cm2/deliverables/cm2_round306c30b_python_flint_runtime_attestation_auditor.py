#!/usr/bin/env python3
"""Fail-closed, offline attestation of the C30b python-flint runtime.

This program is intentionally independent of the C30b producer and verifier.
It treats the pinned P0 runtime lock and requirements lock as trust roots, reads
the sealed wheel, inventories the isolated venv, verifies both wheel and
installed RECORD files entry by entry, and only then imports :mod:`flint`.

Required invocation (``-I`` and ``-B`` are checked, not merely recommended)::

    .cm2-runtime/python-flint-0.9.0/bin/python -I -B \
        deliverables/cm2_round306c30b_python_flint_runtime_attestation_auditor.py \
        --output PATH

Omit ``--output`` (or use ``--output -``) for stdout.  On success the sole
stdout/file payload is one newline-terminated canonical JSON object.  On any
failure, no JSON is emitted and the process exits nonzero.  No network access,
package installer, producer result, or verifier result is used.
"""

from __future__ import annotations

import argparse
import base64
import csv
import email.policy
import hashlib
import importlib
import io
import json
import os
import platform
import re
import stat
import sys
import zipfile
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from typing import Any, Callable


sys.dont_write_bytecode = True

SCRIPT = Path(__file__).resolve(strict=True)
DELIVERABLES = SCRIPT.parent
WORKSPACE = DELIVERABLES.parent

AUDITOR_RELPATH = (
    "deliverables/"
    "cm2_round306c30b_python_flint_runtime_attestation_auditor.py"
)
P0_LOCK_RELPATH = (
    "deliverables/cm2_round306c30a_python_flint_runtime_lock.json"
)
REQUIREMENTS_RELPATH = (
    "deliverables/cm2_round306c30a_python_flint_requirements.lock"
)
SEALED_WHEEL_DIR_RELPATH = "deliverables/cm2_round306c30a_runtime"

# These are independent trust-root pins.  They are not imported from either
# C30b executable and are checked before any field in either file is used.
P0_LOCK_SHA256 = (
    "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79"
)
REQUIREMENTS_SHA256 = (
    "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c"
)

P0_KEYS = {
    "abi",
    "architecture",
    "environment_relpath",
    "flint_release",
    "flint_version",
    "glibc",
    "implementation",
    "installer_command",
    "machine_python_sha256",
    "manylinux_floor",
    "python_cache_tag",
    "python_flint",
    "python_version",
    "schema",
    "wheel_filename",
    "wheel_sha256",
}
EXPECTED_P0_SCHEMA = "cm2.round306c30a.python-flint-runtime-lock.v1"
ATTESTATION_SCHEMA = "cm2.round306c30b.python-flint-runtime-attestation.v1"

SHA256_HEX = re.compile(r"[0-9a-f]{64}\Z")
VERSION = re.compile(r"[0-9]+(?:\.[0-9]+){2}\Z")
WHEEL_FILENAME = re.compile(
    r"python_flint-(?P<version>[0-9]+(?:\.[0-9]+){2})-"
    r"(?P<python>cp[0-9]+)-(?P<abi>abi3)-"
    r"(?P<platform>manylinux2014_x86_64\.manylinux_2_17_x86_64)\.whl\Z"
)


class Reject(RuntimeError):
    """A closed attestation gate rejected the runtime."""


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def object_sha256(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def workspace_relpath(path: Path) -> str:
    resolved = path.resolve(strict=True)
    require(resolved.is_relative_to(WORKSPACE), "path outside workspace")
    return resolved.relative_to(WORKSPACE).as_posix()


def workspace_lexical_relpath(path: Path) -> str:
    """Return a workspace path without following its intentional final symlink."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.is_relative_to(WORKSPACE), "lexical path outside workspace")
    return absolute.relative_to(WORKSPACE).as_posix()


def read_regular(
    path: Path,
    *,
    maximum: int = 512 * 1024 * 1024,
    allow_empty: bool = True,
) -> bytes:
    """Read one non-symlink, single-link regular file with race checks."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    status = absolute.lstat()
    require(
        stat.S_ISREG(status.st_mode)
        and not absolute.is_symlink()
        and status.st_nlink == 1
        and (allow_empty or status.st_size > 0)
        and 0 <= status.st_size <= maximum,
        "regular singleton:" + os.fspath(path),
    )
    descriptor = os.open(
        absolute,
        os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
    )
    try:
        opened = os.fstat(descriptor)
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and (opened.st_dev, opened.st_ino, opened.st_size)
            == (status.st_dev, status.st_ino, status.st_size),
            "opened identity:" + os.fspath(path),
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            block = os.read(descriptor, min(1024 * 1024, remaining))
            require(bool(block), "short read:" + os.fspath(path))
            chunks.append(block)
            remaining -= len(block)
        require(not os.read(descriptor, 1), "growing input:" + os.fspath(path))
        final = os.fstat(descriptor)
        require(
            (final.st_dev, final.st_ino, final.st_size)
            == (opened.st_dev, opened.st_ino, opened.st_size),
            "changed input:" + os.fspath(path),
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def strict_json_object(raw: bytes, label: str) -> dict[str, Any]:
    require(raw and b"\x00" not in raw and not raw.startswith(b"\xef\xbb\xbf"),
            "JSON encoding:" + label)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(type(key) is str and key not in output,
                    "JSON duplicate key:" + label)
            output[key] = value
        return output

    def reject_constant(token: str) -> None:
        raise ValueError(token)

    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=unique,
            parse_constant=reject_constant,
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    require(type(value) is dict, "JSON top-level object:" + label)
    return value


def normalized_distribution_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def metadata_identity(raw: bytes, label: str) -> dict[str, str]:
    require(raw and b"\x00" not in raw, "metadata encoding:" + label)
    try:
        message = BytesParser(policy=email.policy.default).parsebytes(raw)
    except Exception as error:
        raise Reject("metadata parse:" + label) from error
    require(not message.defects, "metadata defects:" + label)
    names = message.get_all("Name", [])
    versions = message.get_all("Version", [])
    require(len(names) == 1 and len(versions) == 1,
            "metadata identity cardinality:" + label)
    name = str(names[0])
    version = str(versions[0])
    require(normalized_distribution_name(name) == "python-flint",
            "metadata distribution name:" + label)
    require(bool(VERSION.fullmatch(version)), "metadata version syntax:" + label)
    return {"name": name, "version": version}


def safe_record_path(value: str, label: str) -> str:
    require(
        type(value) is str
        and value
        and "\x00" not in value
        and "\\" not in value
        and value.isascii()
        and not value.startswith("/"),
        "RECORD path syntax:" + label,
    )
    pure = PurePosixPath(value)
    require(
        not pure.is_absolute()
        and all(part not in {"", ".", ".."} for part in pure.parts)
        and pure.as_posix() == value,
        "RECORD canonical path:" + label,
    )
    return value


def decode_record_digest(value: str, label: str) -> tuple[str, bytes]:
    require(value.startswith("sha256="), "RECORD hash algorithm:" + label)
    encoded = value[len("sha256="):]
    require(encoded and "=" not in encoded and encoded.isascii(),
            "RECORD hash encoding:" + label)
    try:
        decoded = base64.b64decode(
            encoded + "=" * (-len(encoded) % 4),
            altchars=b"-_",
            validate=True,
        )
    except (ValueError, base64.binascii.Error) as error:
        raise Reject("RECORD base64:" + label) from error
    canonical_b64 = base64.urlsafe_b64encode(decoded).rstrip(b"=").decode("ascii")
    require(len(decoded) == 32 and canonical_b64 == encoded,
            "RECORD canonical sha256 base64:" + label)
    return encoded, decoded


def parse_record(raw: bytes, label: str) -> dict[str, tuple[str | None, int | None]]:
    require(raw and b"\x00" not in raw, "RECORD encoding:" + label)
    try:
        text = raw.decode("utf-8", "strict")
        reader = csv.reader(io.StringIO(text, newline=""), strict=True)
        rows = list(reader)
    except (UnicodeDecodeError, csv.Error) as error:
        raise Reject("RECORD CSV:" + label) from error
    require(rows and all(len(row) == 3 for row in rows),
            "RECORD row arity:" + label)
    claims: dict[str, tuple[str | None, int | None]] = {}
    for ordinal, row in enumerate(rows):
        row_label = f"{label}:{ordinal}"
        path = safe_record_path(row[0], row_label)
        require(path not in claims, "RECORD duplicate path:" + row_label)
        encoded_hash, size_text = row[1], row[2]
        require(bool(encoded_hash) == bool(size_text),
                "RECORD hash/size pairing:" + row_label)
        if encoded_hash:
            canonical_b64, _ = decode_record_digest(encoded_hash, row_label)
            require(size_text.isascii() and size_text.isdecimal(),
                    "RECORD size syntax:" + row_label)
            size = int(size_text)
            require(size >= 0 and str(size) == size_text,
                    "RECORD canonical size:" + row_label)
            claims[path] = (canonical_b64, size)
        else:
            claims[path] = (None, None)
    return claims


def verify_record_contents(
    claims: dict[str, tuple[str | None, int | None]],
    contents: dict[str, bytes],
    *,
    record_path: str,
    allowed_unhashed: Callable[[str], bool],
    label: str,
) -> dict[str, Any]:
    require(set(claims) == set(contents), "RECORD/file closure:" + label)
    require(record_path in claims, "RECORD self row:" + label)
    claimed_count = 0
    unclaimed_paths: list[str] = []
    for path in sorted(claims):
        encoded_hash, claimed_size = claims[path]
        raw = contents[path]
        if encoded_hash is None:
            require(allowed_unhashed(path), "unexpected unhashed RECORD row:" + path)
            unclaimed_paths.append(path)
            continue
        claimed_count += 1
        actual_encoded = base64.urlsafe_b64encode(
            hashlib.sha256(raw).digest()
        ).rstrip(b"=").decode("ascii")
        require(actual_encoded == encoded_hash, "RECORD sha256 mismatch:" + path)
        require(len(raw) == claimed_size, "RECORD size mismatch:" + path)
    return {
        "entry_count": len(claims),
        "hashed_entry_count": claimed_count,
        "unhashed_entry_count": len(unclaimed_paths),
        "unhashed_paths": unclaimed_paths,
    }


def file_table(contents: dict[str, bytes]) -> list[dict[str, Any]]:
    return [
        {"path": path, "sha256": sha256_bytes(contents[path]),
         "size": len(contents[path])}
        for path in sorted(contents)
    ]


def validate_p0() -> tuple[dict[str, Any], bytes, bytes]:
    lock_path = WORKSPACE / P0_LOCK_RELPATH
    requirements_path = WORKSPACE / REQUIREMENTS_RELPATH
    lock_raw = read_regular(lock_path, maximum=64 * 1024, allow_empty=False)
    requirements_raw = read_regular(
        requirements_path, maximum=64 * 1024, allow_empty=False
    )
    require(sha256_bytes(lock_raw) == P0_LOCK_SHA256, "P0 lock trust-root pin")
    require(sha256_bytes(requirements_raw) == REQUIREMENTS_SHA256,
            "requirements trust-root pin")

    lock = strict_json_object(lock_raw, P0_LOCK_RELPATH)
    require(set(lock) == P0_KEYS, "P0 lock exact keys")
    string_keys = P0_KEYS - {"flint_release"}
    require(all(type(lock[key]) is str for key in string_keys),
            "P0 lock string field types")
    require(type(lock["flint_release"]) is int and lock["flint_release"] > 0,
            "P0 lock release field type")
    require(lock["schema"] == EXPECTED_P0_SCHEMA, "P0 lock schema")
    require(lock["environment_relpath"] == ".cm2-runtime/python-flint-0.9.0",
            "P0 environment relpath")
    require(lock["implementation"] == "cpython", "P0 implementation")
    require(lock["architecture"] == "x86_64", "P0 architecture")
    require(lock["abi"] == "cp310-abi3", "P0 ABI")
    require(lock["manylinux_floor"] == "manylinux_2_17_x86_64",
            "P0 manylinux floor")
    require(bool(VERSION.fullmatch(lock["python_flint"])),
            "P0 python-flint version syntax")
    require(bool(VERSION.fullmatch(lock["python_version"])),
            "P0 Python version syntax")
    require(bool(VERSION.fullmatch(lock["flint_version"])),
            "P0 FLINT version syntax")
    require(bool(re.fullmatch(r"[0-9]+\.[0-9]+", lock["glibc"])),
            "P0 glibc version syntax")
    require(bool(SHA256_HEX.fullmatch(lock["machine_python_sha256"])),
            "P0 interpreter hash syntax")
    require(bool(SHA256_HEX.fullmatch(lock["wheel_sha256"])),
            "P0 wheel hash syntax")
    wheel_match = WHEEL_FILENAME.fullmatch(lock["wheel_filename"])
    require(wheel_match is not None, "P0 wheel filename")
    require(
        wheel_match.group("version") == lock["python_flint"]
        and f"{wheel_match.group('python')}-{wheel_match.group('abi')}"
        == lock["abi"],
        "P0 wheel filename fields",
    )
    expected_installer = (
        f"{lock['environment_relpath']}/bin/python -m pip install "
        f"--require-hashes -r {REQUIREMENTS_RELPATH}"
    )
    require(lock["installer_command"] == expected_installer,
            "P0 installer command binding")

    pattern = re.compile(
        rb"python-flint==([0-9]+(?:\.[0-9]+){2}) \\\n"
        rb"    --hash=sha256:([0-9a-f]{64})\n\Z"
    )
    requirement_match = pattern.fullmatch(requirements_raw)
    require(requirement_match is not None, "requirements exact syntax")
    require(
        requirement_match.group(1).decode("ascii") == lock["python_flint"]
        and requirement_match.group(2).decode("ascii") == lock["wheel_sha256"],
        "requirements/P0 agreement",
    )
    return lock, lock_raw, requirements_raw


def zip_member_path(name: str) -> str:
    require(
        name
        and "\x00" not in name
        and "\\" not in name
        and name.isascii()
        and not name.startswith("/"),
        "wheel member path syntax",
    )
    value = name[:-1] if name.endswith("/") else name
    pure = PurePosixPath(value)
    require(
        value
        and not pure.is_absolute()
        and all(part not in {"", ".", ".."} for part in pure.parts)
        and pure.as_posix() == value,
        "wheel canonical member path",
    )
    return value


def audit_wheel(lock: dict[str, Any]) -> tuple[dict[str, Any], dict[str, bytes]]:
    wheel_path = WORKSPACE / SEALED_WHEEL_DIR_RELPATH / lock["wheel_filename"]
    wheel_raw = read_regular(wheel_path, maximum=256 * 1024 * 1024,
                             allow_empty=False)
    wheel_sha = sha256_bytes(wheel_raw)
    require(wheel_sha == lock["wheel_sha256"], "sealed wheel/P0 sha256")

    try:
        archive = zipfile.ZipFile(io.BytesIO(wheel_raw), mode="r")
        infos = archive.infolist()
    except (OSError, zipfile.BadZipFile) as error:
        raise Reject("sealed wheel ZIP") from error
    require(0 < len(infos) <= 10_000, "sealed wheel member count")
    require(sum(info.file_size for info in infos) <= 512 * 1024 * 1024,
            "sealed wheel expanded size")
    seen: set[str] = set()
    contents: dict[str, bytes] = {}
    try:
        for info in infos:
            normalized = zip_member_path(info.filename)
            require(normalized not in seen, "sealed wheel duplicate member")
            seen.add(normalized)
            require(not (info.flag_bits & 1), "sealed wheel encrypted member")
            require(
                info.compress_type in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED},
                "sealed wheel compression method",
            )
            unix_type = stat.S_IFMT(info.external_attr >> 16)
            require(unix_type not in {stat.S_IFLNK, stat.S_IFBLK, stat.S_IFCHR,
                                      stat.S_IFIFO, stat.S_IFSOCK},
                    "sealed wheel special member")
            if info.is_dir():
                require(unix_type in {0, stat.S_IFDIR},
                        "sealed wheel directory type")
                continue
            require(unix_type in {0, stat.S_IFREG}, "sealed wheel file type")
            require(info.file_size <= 256 * 1024 * 1024,
                    "sealed wheel member size")
            try:
                raw = archive.read(info)
            except (OSError, EOFError, RuntimeError, zipfile.BadZipFile) as error:
                raise Reject("sealed wheel member read:" + normalized) from error
            require(len(raw) == info.file_size, "sealed wheel member length")
            contents[normalized] = raw
    finally:
        archive.close()

    dist_info = f"python_flint-{lock['python_flint']}.dist-info"
    metadata_path = dist_info + "/METADATA"
    record_path = dist_info + "/RECORD"
    wheel_metadata_path = dist_info + "/WHEEL"
    require(metadata_path in contents and record_path in contents
            and wheel_metadata_path in contents, "sealed wheel dist-info members")
    identity = metadata_identity(contents[metadata_path], "sealed wheel METADATA")
    require(identity["version"] == lock["python_flint"],
            "sealed wheel distribution version")
    claims = parse_record(contents[record_path], "sealed wheel RECORD")
    verification = verify_record_contents(
        claims,
        contents,
        record_path=record_path,
        allowed_unhashed=lambda path: path == record_path,
        label="sealed wheel",
    )
    wheel_file_table = file_table(contents)
    wheel_headers = contents[wheel_metadata_path].decode("utf-8", "strict")
    expected_tags = {
        "cp310-abi3-manylinux_2_17_x86_64",
        "cp310-abi3-manylinux2014_x86_64",
    }
    tags = {
        line[len("Tag: "):]
        for line in wheel_headers.splitlines()
        if line.startswith("Tag: ")
    }
    require(tags == expected_tags, "sealed wheel compatibility tags")
    return {
        "path": workspace_relpath(wheel_path),
        "sha256": wheel_sha,
        "size": len(wheel_raw),
        "distribution_name": identity["name"],
        "distribution_version": identity["version"],
        "compatibility_tags": sorted(tags),
        "record_raw_sha256": sha256_bytes(contents[record_path]),
        "record_verification": verification,
        "file_count": len(wheel_file_table),
        "file_table_sha256": object_sha256(wheel_file_table),
    }, contents


def assert_directory_tree(path: Path, containment_root: Path) -> None:
    """Reject symlinks and special nodes in a distribution-owned tree."""

    require(path.resolve(strict=True).is_relative_to(containment_root.resolve()),
            "owned root containment")
    for directory, dirnames, filenames in os.walk(path, topdown=True,
                                                   followlinks=False):
        directory_path = Path(directory)
        directory_status = directory_path.lstat()
        require(stat.S_ISDIR(directory_status.st_mode)
                and not directory_path.is_symlink(),
                "owned directory type:" + os.fspath(directory_path))
        for name in sorted(dirnames):
            child = directory_path / name
            child_status = child.lstat()
            require(stat.S_ISDIR(child_status.st_mode) and not child.is_symlink(),
                    "owned child directory type:" + os.fspath(child))
        for name in sorted(filenames):
            child = directory_path / name
            child_status = child.lstat()
            require(
                stat.S_ISREG(child_status.st_mode)
                and not child.is_symlink()
                and child_status.st_nlink == 1,
                "owned file type:" + os.fspath(child),
            )


def physical_distribution_contents(
    site_packages: Path,
    owned_roots: tuple[str, ...],
) -> dict[str, bytes]:
    contents: dict[str, bytes] = {}
    site_resolved = site_packages.resolve(strict=True)
    for root_name in owned_roots:
        root = site_packages / root_name
        require(root.exists(), "installed distribution root:" + root_name)
        assert_directory_tree(root, site_packages)
        for directory, dirnames, filenames in os.walk(root, topdown=True,
                                                       followlinks=False):
            dirnames.sort()
            for name in sorted(filenames):
                path = Path(directory) / name
                resolved = path.resolve(strict=True)
                require(resolved.is_relative_to(site_resolved),
                        "installed file containment")
                relative = resolved.relative_to(site_resolved).as_posix()
                require(relative not in contents, "installed duplicate file path")
                contents[relative] = read_regular(path)
    return contents


def runtime_preconditions(lock: dict[str, Any]) -> tuple[Path, Path, dict[str, Any]]:
    environment = WORKSPACE / lock["environment_relpath"]
    require(environment.resolve(strict=True).is_relative_to(WORKSPACE),
            "venv containment")
    require(environment.is_dir() and not environment.is_symlink(), "venv root")
    invoked_python = environment / "bin/python"
    require(os.path.abspath(sys.executable) == os.fspath(invoked_python),
            "auditor invoked by locked venv bin/python")
    resolved_python = invoked_python.resolve(strict=True)
    require(resolved_python.is_file() and not resolved_python.is_symlink(),
            "resolved interpreter regular file")
    interpreter_raw = read_regular(resolved_python, maximum=128 * 1024 * 1024,
                                   allow_empty=False)
    interpreter_sha = sha256_bytes(interpreter_raw)
    version = ".".join(str(value) for value in sys.version_info[:3])
    glibc_conf = os.confstr("CS_GNU_LIBC_VERSION")
    require(type(glibc_conf) is str and glibc_conf.startswith("glibc "),
            "runtime glibc query")
    glibc = glibc_conf.split(" ", 1)[1]
    require(
        sys.flags.isolated == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.dont_write_bytecode is True
        and sys.flags.no_user_site == 1
        and sys.prefix != sys.base_prefix
        and Path(sys.prefix).resolve(strict=True) == environment.resolve(strict=True)
        and sys.implementation.name == lock["implementation"]
        and sys.implementation.cache_tag == lock["python_cache_tag"]
        and version == lock["python_version"]
        and os.uname().machine == lock["architecture"]
        and platform.machine() == lock["architecture"]
        and glibc == lock["glibc"]
        and interpreter_sha == lock["machine_python_sha256"],
        "locked interpreter/runtime properties",
    )
    major_minor = ".".join(lock["python_version"].split(".")[:2])
    site_packages = environment / "lib" / f"python{major_minor}" / "site-packages"
    require(site_packages.is_dir() and not site_packages.is_symlink(),
            "locked site-packages")
    pyvenv_raw = read_regular(environment / "pyvenv.cfg", maximum=64 * 1024,
                              allow_empty=False)
    return environment, site_packages, {
        "venv_relpath": lock["environment_relpath"],
        "invoked_executable_relpath": workspace_lexical_relpath(invoked_python),
        "resolved_executable_path": os.fspath(resolved_python),
        "resolved_executable_sha256": interpreter_sha,
        "resolved_executable_size": len(interpreter_raw),
        "implementation": sys.implementation.name,
        "python_version": version,
        "cache_tag": sys.implementation.cache_tag,
        "architecture": os.uname().machine,
        "glibc": glibc,
        "isolated_flag": sys.flags.isolated,
        "dont_write_bytecode_flag": sys.flags.dont_write_bytecode,
        "no_user_site_flag": sys.flags.no_user_site,
        "pyvenv_cfg_sha256": sha256_bytes(pyvenv_raw),
    }


def audit_installed_distribution(
    lock: dict[str, Any],
    site_packages: Path,
    wheel_contents: dict[str, bytes],
) -> tuple[dict[str, Any], dict[str, bytes], list[dict[str, Any]]]:
    dist_info_name = f"python_flint-{lock['python_flint']}.dist-info"
    candidates = sorted(
        entry.name
        for entry in site_packages.iterdir()
        if entry.name.startswith("python_flint-") and entry.name.endswith(".dist-info")
    )
    require(candidates == [dist_info_name], "installed dist-info cardinality")
    owned_roots = ("flint", "python_flint.libs", dist_info_name)
    contents = physical_distribution_contents(site_packages, owned_roots)
    record_path = dist_info_name + "/RECORD"
    metadata_path = dist_info_name + "/METADATA"
    require(record_path in contents and metadata_path in contents,
            "installed dist-info required files")
    identity = metadata_identity(contents[metadata_path], "installed METADATA")
    require(identity["version"] == lock["python_flint"],
            "installed distribution version")
    claims = parse_record(contents[record_path], "installed RECORD")

    def allowed_unhashed(path: str) -> bool:
        if path == record_path:
            return True
        pure = PurePosixPath(path)
        return (
            pure.parts[0] == "flint"
            and "__pycache__" in pure.parts
            and pure.suffix == ".pyc"
        )

    verification = verify_record_contents(
        claims,
        contents,
        record_path=record_path,
        allowed_unhashed=allowed_unhashed,
        label="installed distribution",
    )

    wheel_record_path = dist_info_name + "/RECORD"
    for path, raw in wheel_contents.items():
        if path != wheel_record_path:
            require(contents.get(path) == raw,
                    "installed/sealed-wheel content agreement:" + path)
    installed_extras = sorted(set(contents) - set(wheel_contents))
    expected_non_pyc_extras = {
        dist_info_name + "/INSTALLER",
        dist_info_name + "/REQUESTED",
    }
    non_pyc_extras = {
        path for path in installed_extras if not path.endswith(".pyc")
    }
    require(non_pyc_extras == expected_non_pyc_extras,
            "installed non-wheel extras")
    require(contents[dist_info_name + "/INSTALLER"] == b"pip\n",
            "installed INSTALLER")
    require(contents[dist_info_name + "/REQUESTED"] == b"",
            "installed REQUESTED")
    for path in installed_extras:
        if path.endswith(".pyc"):
            pure = PurePosixPath(path)
            require(pure.parts[0] == "flint" and "__pycache__" in pure.parts,
                    "installed generated pyc path")

    table = file_table(contents)
    result = {
        "site_packages_relpath": workspace_relpath(site_packages),
        "dist_info_directory": dist_info_name,
        "distribution_name": identity["name"],
        "distribution_version": identity["version"],
        "metadata_sha256": sha256_bytes(contents[metadata_path]),
        "record_raw_sha256": sha256_bytes(contents[record_path]),
        "record_verification": verification,
        "sealed_wheel_member_match_count": len(wheel_contents) - 1,
        "installed_extra_paths": installed_extras,
        "file_count": len(table),
        "file_table_sha256": object_sha256(table),
        "file_table": table,
    }
    return result, contents, table


def audit_native(table: list[dict[str, Any]]) -> dict[str, Any]:
    extension_modules = [
        row for row in table
        if row["path"].startswith("flint/") and row["path"].endswith(".so")
    ]
    bundled_libraries = [
        row for row in table if row["path"].startswith("python_flint.libs/")
    ]
    require(bool(extension_modules) and bool(bundled_libraries),
            "native extension/bundled-library census nonempty")
    require(
        all(".so." in PurePosixPath(row["path"]).name
            for row in bundled_libraries),
        "bundled library filename census",
    )
    all_native = sorted(extension_modules + bundled_libraries,
                        key=lambda row: row["path"])
    require(len({row["path"] for row in all_native}) == len(all_native),
            "native census unique paths")
    return {
        "extension_module_count": len(extension_modules),
        "extension_module_file_table_sha256": object_sha256(extension_modules),
        "extension_modules": extension_modules,
        "bundled_library_count": len(bundled_libraries),
        "bundled_library_file_table_sha256": object_sha256(bundled_libraries),
        "bundled_libraries": bundled_libraries,
        "native_file_count": len(all_native),
        "native_file_table_sha256": object_sha256(all_native),
    }


def import_and_attest_flint(
    lock: dict[str, Any],
    site_packages: Path,
    installed_contents: dict[str, bytes],
) -> dict[str, Any]:
    require("flint" not in sys.modules, "flint not imported before file audit")

    def offline_audit_hook(event: str, args: tuple[Any, ...]) -> None:
        if event.startswith("socket."):
            raise Reject("network event during flint import:" + event)

    sys.addaudithook(offline_audit_hook)
    try:
        module = importlib.import_module("flint")
    except Exception as error:
        raise Reject("flint import") from error
    expected_module = site_packages / "flint" / "__init__.py"
    require(type(module.__file__) is str, "imported flint __file__ type")
    imported_path = Path(module.__file__).resolve(strict=True)
    require(imported_path == expected_module.resolve(strict=True),
            "imported flint module path")
    require(
        type(module.__version__) is str
        and module.__version__ == lock["python_flint"]
        and type(module.__FLINT_VERSION__) is str
        and module.__FLINT_VERSION__ == lock["flint_version"]
        and type(module.__FLINT_RELEASE__) is int
        and module.__FLINT_RELEASE__ == lock["flint_release"],
        "imported flint locked versions",
    )
    relative = imported_path.relative_to(site_packages.resolve(strict=True)).as_posix()
    require(relative in installed_contents, "imported flint in distribution table")
    require(read_regular(imported_path) == installed_contents[relative],
            "imported flint file unchanged")
    return {
        "module": "flint",
        "module_file_relpath": workspace_relpath(imported_path),
        "module_file_sha256": sha256_bytes(installed_contents[relative]),
        "python_flint_version": module.__version__,
        "flint_version": module.__FLINT_VERSION__,
        "flint_release": module.__FLINT_RELEASE__,
    }


def build_attestation() -> dict[str, Any]:
    require(SCRIPT == WORKSPACE / AUDITOR_RELPATH, "auditor canonical location")
    lock, lock_raw, requirements_raw = validate_p0()
    _, site_packages, interpreter = runtime_preconditions(lock)
    wheel, wheel_contents = audit_wheel(lock)
    installed, installed_contents, installed_table = audit_installed_distribution(
        lock, site_packages, wheel_contents
    )
    native = audit_native(installed_table)
    imported = import_and_attest_flint(lock, site_packages, installed_contents)

    # Re-enumerate and rehash after native import.  This both enforces -B in
    # practice and catches any import-time mutation of distribution files.
    dist_info_name = installed["dist_info_directory"]
    post_import_contents = physical_distribution_contents(
        site_packages, ("flint", "python_flint.libs", dist_info_name)
    )
    require(post_import_contents == installed_contents,
            "distribution unchanged by import")

    auditor_raw = read_regular(SCRIPT, maximum=4 * 1024 * 1024,
                               allow_empty=False)
    body: dict[str, Any] = {
        "schema": ATTESTATION_SCHEMA,
        "verdict": "PASS",
        "offline": True,
        "auditor": {
            "path": AUDITOR_RELPATH,
            "sha256": sha256_bytes(auditor_raw),
        },
        "trust_roots": {
            "p0_runtime_lock": {
                "path": P0_LOCK_RELPATH,
                "sha256": sha256_bytes(lock_raw),
                "schema": lock["schema"],
            },
            "requirements_lock": {
                "path": REQUIREMENTS_RELPATH,
                "sha256": sha256_bytes(requirements_raw),
            },
        },
        "sealed_wheel": wheel,
        "interpreter": interpreter,
        "installed_distribution": installed,
        "native_runtime": native,
        "imported_flint": imported,
    }
    body["attestation_payload_sha256"] = object_sha256(body)
    return body


def write_output(raw: bytes, destination: str) -> None:
    payload = raw + b"\n"
    if destination == "-":
        sys.stdout.buffer.write(payload)
        sys.stdout.buffer.flush()
        return
    output_path = Path(destination)
    require(output_path.name not in {"", ".", ".."}, "output path")
    descriptor = os.open(
        output_path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL
        | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    complete = False
    try:
        offset = 0
        while offset < len(payload):
            written = os.write(descriptor, payload[offset:])
            require(written > 0, "output short write")
            offset += written
        os.fsync(descriptor)
        complete = True
    finally:
        os.close(descriptor)
        if not complete:
            try:
                output_path.unlink()
            except OSError:
                pass


def parse_arguments(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit the sealed C30b python-flint runtime offline."
    )
    parser.add_argument(
        "-o", "--output", default="-", metavar="PATH",
        help="exclusive-create PATH, or '-' for stdout (default)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
    try:
        result = build_attestation()
        write_output(canonical(result), arguments.output)
    except Exception as error:
        print(
            "C30B_RUNTIME_ATTESTATION_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
