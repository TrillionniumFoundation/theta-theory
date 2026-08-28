#!/usr/bin/env python3
"""Independent, fail-closed attestor for the C30a fresh offline runtime.

This auditor is deliberately independent of every C30 producer and verifier.
It pins the machine interpreter, P0 locks, and sealed wheel; verifies every
wheel RECORD claim and every installed RECORD claim; inventories all files
owned by python-flint; and imports flint only after the byte audit succeeds.

Required invocation::

    fresh-python-flint-0.9.0/bin/python -I -B \
        deliverables/cm2_round306c30a_python_flint_fresh_runtime_attestor.py

Success is exactly one newline-terminated canonical JSON object on stdout.
Failure emits no JSON and exits nonzero.
"""

from __future__ import annotations

import base64
import csv
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
from pathlib import Path, PurePosixPath
from typing import Any, Callable


sys.dont_write_bytecode = True

SCRIPT = Path(__file__).resolve(strict=True)
DELIVERABLES = SCRIPT.parent
WORKSPACE = DELIVERABLES.parent
AUDIT = WORKSPACE / ".cm2-runtime/audit/c30a-p0-closure-verifier-20260807"
FRESH = AUDIT / "fresh-python-flint-0.9.0"
LOCK = DELIVERABLES / "cm2_round306c30a_python_flint_runtime_lock.json"
REQUIREMENTS = DELIVERABLES / "cm2_round306c30a_python_flint_requirements.lock"
WHEEL_DIR = DELIVERABLES / "cm2_round306c30a_runtime"

SCRIPT_REL = "deliverables/cm2_round306c30a_python_flint_fresh_runtime_attestor.py"
FRESH_REL = (
    ".cm2-runtime/audit/c30a-p0-closure-verifier-20260807/"
    "fresh-python-flint-0.9.0"
)
LOCK_REL = "deliverables/cm2_round306c30a_python_flint_runtime_lock.json"
REQUIREMENTS_REL = "deliverables/cm2_round306c30a_python_flint_requirements.lock"
WHEEL_REL_PREFIX = "deliverables/cm2_round306c30a_runtime/"

MACHINE_PYTHON = Path("/usr/bin/python3.12")
MACHINE_PYTHON_SHA256 = (
    "1643dacd9feaedc58f3cc581e4d22577dfe25c09b10282936186ccf0f2e61118"
)
LOCK_SHA256 = (
    "ffe714b67a0aa05d8094033a0d9cc8e10ccafa03157951adf3d64055c98cdc79"
)
REQUIREMENTS_SHA256 = (
    "cd171f53dd8a187b2ef4bd7ad0cc2adbe2082395646c0c57407f4e3514c11f5c"
)
WHEEL_FILENAME = (
    "python_flint-0.9.0-cp310-abi3-manylinux2014_x86_64."
    "manylinux_2_17_x86_64.whl"
)
WHEEL_SHA256 = (
    "376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76"
)
EXPECTED_ENV = {"HOME": "/nonexistent", "LC_ALL": "C.UTF-8", "TZ": "UTC"}

LOCK_KEYS = {
    "abi", "architecture", "environment_relpath", "flint_release",
    "flint_version", "glibc", "implementation", "installer_command",
    "machine_python_sha256", "manylinux_floor", "python_cache_tag",
    "python_flint", "python_version", "schema", "wheel_filename",
    "wheel_sha256",
}


class Reject(RuntimeError):
    """Fail-closed attestation rejection."""


def require(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def object_sha256(value: Any) -> str:
    return sha256(canonical(value))


def relpath(path: Path) -> str:
    resolved = path.resolve(strict=True)
    require(resolved.is_relative_to(WORKSPACE), "path containment")
    return resolved.relative_to(WORKSPACE).as_posix()


def lexical_relpath(path: Path) -> str:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.is_relative_to(WORKSPACE), "lexical path containment")
    return absolute.relative_to(WORKSPACE).as_posix()


def read_regular(
    path: Path, *, maximum: int = 512 * 1024 * 1024, allow_empty: bool = True
) -> bytes:
    """Race-checked read of one non-symlink, single-link regular file."""

    absolute = Path(os.path.abspath(os.fspath(path)))
    before = absolute.lstat()
    require(
        stat.S_ISREG(before.st_mode)
        and not absolute.is_symlink()
        and before.st_nlink == 1
        and (allow_empty or before.st_size > 0)
        and 0 <= before.st_size <= maximum,
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
            and (
                opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns, opened.st_ctime_ns,
            ) == (
                before.st_dev, before.st_ino, before.st_size,
                before.st_mtime_ns, before.st_ctime_ns,
            ),
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
        after = os.fstat(descriptor)
        require(
            (
                after.st_dev, after.st_ino, after.st_size,
                after.st_mtime_ns, after.st_ctime_ns,
            ) == (
                opened.st_dev, opened.st_ino, opened.st_size,
                opened.st_mtime_ns, opened.st_ctime_ns,
            ),
            "changed input:" + os.fspath(path),
        )
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(raw and b"\x00" not in raw, "JSON encoding:" + label)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            require(type(key) is str and key not in value, "JSON duplicate:" + label)
            value[key] = item
        return value

    try:
        value = json.loads(
            raw.decode("utf-8", "strict"), object_pairs_hook=unique,
            parse_float=lambda token: (_ for _ in ()).throw(ValueError(token)),
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    require(type(value) is dict, "JSON object:" + label)
    return value


def safe_member(value: str, label: str) -> str:
    require(
        type(value) is str and value and value.isascii()
        and "\x00" not in value and "\\" not in value
        and not value.startswith("/"),
        "member syntax:" + label,
    )
    stripped = value[:-1] if value.endswith("/") else value
    pure = PurePosixPath(stripped)
    require(
        stripped and not pure.is_absolute()
        and all(part not in {"", ".", ".."} for part in pure.parts)
        and pure.as_posix() == stripped,
        "member canonical:" + label,
    )
    return stripped


def decode_digest(value: str, label: str) -> str:
    require(value.startswith("sha256="), "RECORD algorithm:" + label)
    encoded = value[7:]
    require(encoded and "=" not in encoded and encoded.isascii(),
            "RECORD digest syntax:" + label)
    try:
        digest = base64.b64decode(
            encoded + "=" * (-len(encoded) % 4), altchars=b"-_", validate=True
        )
    except (ValueError, base64.binascii.Error) as error:
        raise Reject("RECORD base64:" + label) from error
    require(
        len(digest) == 32
        and base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii") == encoded,
        "RECORD canonical digest:" + label,
    )
    return encoded


def parse_record(raw: bytes, label: str) -> dict[str, tuple[str | None, int | None]]:
    require(raw and b"\x00" not in raw, "RECORD encoding:" + label)
    try:
        rows = list(csv.reader(io.StringIO(raw.decode("utf-8", "strict"), newline=""),
                               strict=True))
    except (UnicodeDecodeError, csv.Error) as error:
        raise Reject("RECORD parse:" + label) from error
    require(rows and all(len(row) == 3 for row in rows), "RECORD arity:" + label)
    claims: dict[str, tuple[str | None, int | None]] = {}
    for ordinal, row in enumerate(rows):
        path = safe_member(row[0], f"{label}:{ordinal}")
        require(path not in claims, "RECORD duplicate:" + path)
        require(bool(row[1]) == bool(row[2]), "RECORD pair:" + path)
        if row[1]:
            encoded = decode_digest(row[1], path)
            require(row[2].isascii() and row[2].isdecimal(), "RECORD size:" + path)
            size = int(row[2])
            require(size >= 0 and str(size) == row[2], "RECORD canonical size:" + path)
            claims[path] = (encoded, size)
        else:
            claims[path] = (None, None)
    return claims


def verify_record(
    claims: dict[str, tuple[str | None, int | None]],
    contents: dict[str, bytes], *, record_path: str,
    allowed_unhashed: Callable[[str], bool], label: str,
) -> dict[str, Any]:
    require(set(claims) == set(contents), "RECORD/file closure:" + label)
    require(record_path in claims, "RECORD self:" + label)
    hashed = 0
    unhashed: list[str] = []
    for path in sorted(claims):
        digest, size = claims[path]
        raw = contents[path]
        if digest is None:
            require(allowed_unhashed(path), "unexpected unhashed:" + path)
            unhashed.append(path)
            continue
        hashed += 1
        actual = base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).rstrip(b"=").decode("ascii")
        require(actual == digest and len(raw) == size, "RECORD mismatch:" + path)
    return {
        "entry_count": len(claims), "hashed_entry_count": hashed,
        "unhashed_entry_count": len(unhashed), "unhashed_paths": unhashed,
    }


def table(contents: dict[str, bytes]) -> list[dict[str, Any]]:
    return [
        {"path": path, "sha256": sha256(contents[path]), "size": len(contents[path])}
        for path in sorted(contents)
    ]


def validate_locks() -> tuple[dict[str, Any], bytes, bytes]:
    lock_raw = read_regular(LOCK, maximum=64 * 1024, allow_empty=False)
    requirements_raw = read_regular(REQUIREMENTS, maximum=64 * 1024, allow_empty=False)
    require(sha256(lock_raw) == LOCK_SHA256, "runtime lock pin")
    require(sha256(requirements_raw) == REQUIREMENTS_SHA256, "requirements pin")
    lock = strict_json(lock_raw, LOCK_REL)
    require(set(lock) == LOCK_KEYS, "runtime lock exact keys")
    require(
        lock["schema"] == "cm2.round306c30a.python-flint-runtime-lock.v1"
        and lock["machine_python_sha256"] == MACHINE_PYTHON_SHA256
        and lock["wheel_filename"] == WHEEL_FILENAME
        and lock["wheel_sha256"] == WHEEL_SHA256
        and lock["python_version"] == "3.12.3"
        and lock["python_cache_tag"] == "cpython-312"
        and lock["implementation"] == "cpython"
        and lock["architecture"] == "x86_64"
        and lock["python_flint"] == "0.9.0"
        and lock["flint_version"] == "3.6.0"
        and lock["flint_release"] == 30600
        and lock["glibc"] == "2.39"
        and lock["abi"] == "cp310-abi3"
        and lock["manylinux_floor"] == "manylinux_2_17_x86_64",
        "runtime lock values",
    )
    pattern = re.compile(
        rb"python-flint==0\.9\.0 \\\n    --hash=sha256:"
        + WHEEL_SHA256.encode("ascii") + rb"\n\Z"
    )
    require(pattern.fullmatch(requirements_raw) is not None, "requirements exact form")
    return lock, lock_raw, requirements_raw


def audit_wheel() -> tuple[dict[str, Any], dict[str, bytes]]:
    wheel_path = WHEEL_DIR / WHEEL_FILENAME
    raw = read_regular(wheel_path, maximum=256 * 1024 * 1024, allow_empty=False)
    require(sha256(raw) == WHEEL_SHA256, "wheel SHA pin")
    try:
        archive = zipfile.ZipFile(io.BytesIO(raw), "r")
        infos = archive.infolist()
    except (OSError, zipfile.BadZipFile) as error:
        raise Reject("wheel ZIP") from error
    require(0 < len(infos) <= 1000, "wheel member census")
    seen: set[str] = set()
    contents: dict[str, bytes] = {}
    try:
        for info in infos:
            path = safe_member(info.filename, "wheel")
            require(path not in seen, "wheel duplicate:" + path)
            seen.add(path)
            require(not (info.flag_bits & 1), "wheel encryption")
            node_type = stat.S_IFMT(info.external_attr >> 16)
            require(node_type not in {stat.S_IFLNK, stat.S_IFBLK, stat.S_IFCHR,
                                      stat.S_IFIFO, stat.S_IFSOCK},
                    "wheel special node")
            if info.is_dir():
                require(node_type in {0, stat.S_IFDIR}, "wheel directory type")
                continue
            require(node_type in {0, stat.S_IFREG}, "wheel file type")
            member = archive.read(info)
            require(len(member) == info.file_size, "wheel short member")
            contents[path] = member
    finally:
        archive.close()
    dist = "python_flint-0.9.0.dist-info"
    record_path = dist + "/RECORD"
    claims = parse_record(contents[record_path], "wheel")
    verification = verify_record(
        claims, contents, record_path=record_path,
        allowed_unhashed=lambda path: path == record_path, label="wheel",
    )
    wheel_headers = contents[dist + "/WHEEL"].decode("utf-8", "strict")
    tags = sorted(
        line[5:] for line in wheel_headers.splitlines() if line.startswith("Tag: ")
    )
    require(tags == [
        "cp310-abi3-manylinux2014_x86_64",
        "cp310-abi3-manylinux_2_17_x86_64",
    ], "wheel compatibility tags")
    file_table = table(contents)
    return {
        "path": WHEEL_REL_PREFIX + WHEEL_FILENAME,
        "sha256": WHEEL_SHA256,
        "size": len(raw),
        "member_count_including_directories": len(infos),
        "file_count": len(contents),
        "file_table_sha256": object_sha256(file_table),
        "record_raw_sha256": sha256(contents[record_path]),
        "record_verification": verification,
        "compatibility_tags": tags,
    }, contents


def inventory_owned(site: Path) -> dict[str, bytes]:
    contents: dict[str, bytes] = {}
    roots = ("flint", "python_flint.libs", "python_flint-0.9.0.dist-info")
    site_resolved = site.resolve(strict=True)
    for root_name in roots:
        root = site / root_name
        require(root.is_dir() and not root.is_symlink(), "owned root:" + root_name)
        for directory, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
            dirnames.sort()
            directory_path = Path(directory)
            require(directory_path.is_dir() and not directory_path.is_symlink(),
                    "owned directory")
            for name in dirnames:
                child = directory_path / name
                require(child.is_dir() and not child.is_symlink(), "owned child directory")
            for name in sorted(filenames):
                child = directory_path / name
                resolved = child.resolve(strict=True)
                require(resolved.is_relative_to(site_resolved), "owned containment")
                relative = resolved.relative_to(site_resolved).as_posix()
                require(relative not in contents, "owned duplicate")
                contents[relative] = read_regular(child)
    return contents


def runtime_preconditions(lock: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    require(SCRIPT == WORKSPACE / SCRIPT_REL, "auditor canonical location")
    require(FRESH.is_dir() and not FRESH.is_symlink(), "fresh venv root")
    invoked = FRESH / "bin/python"
    require(Path(os.path.abspath(sys.executable)) == invoked, "fresh interpreter invocation")
    require(invoked.is_file() and not invoked.is_symlink(), "copied interpreter type")
    invoked_raw = read_regular(invoked, maximum=128 * 1024 * 1024, allow_empty=False)
    machine_raw = read_regular(MACHINE_PYTHON, maximum=128 * 1024 * 1024, allow_empty=False)
    glibc_conf = os.confstr("CS_GNU_LIBC_VERSION")
    require(type(glibc_conf) is str and glibc_conf.startswith("glibc "), "glibc query")
    version = ".".join(str(item) for item in sys.version_info[:3])
    require(
        os.environ == EXPECTED_ENV
        and sys.flags.isolated == 1
        and sys.flags.ignore_environment == 1
        and sys.flags.dont_write_bytecode == 1
        and sys.flags.no_user_site == 1
        and sys.flags.safe_path is True
        and sys.dont_write_bytecode is True
        and sys.prefix != sys.base_prefix
        and Path(sys.prefix).resolve(strict=True) == FRESH.resolve(strict=True)
        and sys.implementation.name == lock["implementation"]
        and sys.implementation.cache_tag == lock["python_cache_tag"]
        and version == lock["python_version"]
        and platform.machine() == lock["architecture"]
        and glibc_conf.split(" ", 1)[1] == lock["glibc"]
        and sha256(machine_raw) == MACHINE_PYTHON_SHA256
        and sha256(invoked_raw) == MACHINE_PYTHON_SHA256
        and invoked_raw == machine_raw,
        "fresh interpreter/runtime properties",
    )
    pyvenv_raw = read_regular(FRESH / "pyvenv.cfg", maximum=64 * 1024, allow_empty=False)
    pyvenv_text = pyvenv_raw.decode("utf-8", "strict")
    require(
        "include-system-site-packages = false\n" in pyvenv_text
        and "executable = /usr/bin/python3.12\n" in pyvenv_text
        and "--copies" in pyvenv_text,
        "pyvenv creation binding",
    )
    site = FRESH / "lib/python3.12/site-packages"
    require(site.is_dir() and not site.is_symlink(), "fresh site-packages")
    return site, {
        "venv_relpath": FRESH_REL,
        "invoked_executable_relpath": lexical_relpath(invoked),
        "copied_interpreter": True,
        "copied_executable_sha256": sha256(invoked_raw),
        "machine_executable_path": "/usr/bin/python3.12",
        "machine_executable_sha256": sha256(machine_raw),
        "python_version": version,
        "implementation": sys.implementation.name,
        "cache_tag": sys.implementation.cache_tag,
        "architecture": platform.machine(),
        "glibc": glibc_conf.split(" ", 1)[1],
        "flags": {
            "isolated": sys.flags.isolated,
            "ignore_environment": sys.flags.ignore_environment,
            "dont_write_bytecode": sys.flags.dont_write_bytecode,
            "no_user_site": sys.flags.no_user_site,
            "safe_path": sys.flags.safe_path,
        },
        "environment": dict(sorted(os.environ.items())),
        "pyvenv_cfg_sha256": sha256(pyvenv_raw),
    }


def audit_installed(site: Path, wheel_contents: dict[str, bytes]) -> tuple[dict[str, Any], dict[str, bytes]]:
    candidates = sorted(
        item.name for item in site.iterdir()
        if item.name.startswith("python_flint-") and item.name.endswith(".dist-info")
    )
    require(candidates == ["python_flint-0.9.0.dist-info"], "dist-info cardinality")
    contents = inventory_owned(site)
    record_path = "python_flint-0.9.0.dist-info/RECORD"
    claims = parse_record(contents[record_path], "installed")

    def allowed(path: str) -> bool:
        pure = PurePosixPath(path)
        return path == record_path or (
            pure.parts[0] == "flint" and "__pycache__" in pure.parts
            and pure.suffix == ".pyc"
        )

    verification = verify_record(
        claims, contents, record_path=record_path,
        allowed_unhashed=allowed, label="installed",
    )
    for path, raw in wheel_contents.items():
        if path != record_path:
            require(contents.get(path) == raw, "installed/wheel agreement:" + path)
    extras = sorted(set(contents) - set(wheel_contents))
    non_pyc = {path for path in extras if not path.endswith(".pyc")}
    require(non_pyc == {
        "python_flint-0.9.0.dist-info/INSTALLER",
        "python_flint-0.9.0.dist-info/REQUESTED",
    }, "installed non-wheel extras")
    require(contents["python_flint-0.9.0.dist-info/INSTALLER"] == b"pip\n",
            "INSTALLER payload")
    require(contents["python_flint-0.9.0.dist-info/REQUESTED"] == b"",
            "REQUESTED payload")
    file_table = table(contents)
    native = [row for row in file_table if row["path"].endswith(".so") or ".so." in row["path"]]
    require(
        len([row for row in native if row["path"].startswith("flint/")]) == 39
        and len([row for row in native if row["path"].startswith("python_flint.libs/")]) == 3,
        "native file census",
    )
    return {
        "site_packages_relpath": lexical_relpath(site),
        "distribution_name": "python-flint",
        "distribution_version": "0.9.0",
        "record_raw_sha256": sha256(contents[record_path]),
        "record_verification": verification,
        "sealed_wheel_member_match_count": len(wheel_contents) - 1,
        "installed_extra_paths": extras,
        "file_count": len(file_table),
        "file_table_sha256": object_sha256(file_table),
        "file_table": file_table,
        "native_file_count": len(native),
        "native_file_table_sha256": object_sha256(native),
        "native_files": native,
    }, contents


def import_flint(lock: dict[str, Any], site: Path, before: dict[str, bytes]) -> dict[str, Any]:
    require("flint" not in sys.modules, "flint preimport")

    def offline(event: str, args: tuple[Any, ...]) -> None:
        if event.startswith("socket."):
            raise Reject("network audit event:" + event)

    sys.addaudithook(offline)
    module = importlib.import_module("flint")
    expected = (site / "flint/__init__.py").resolve(strict=True)
    require(
        Path(module.__file__).resolve(strict=True) == expected
        and module.__version__ == lock["python_flint"]
        and module.__FLINT_VERSION__ == lock["flint_version"]
        and module.__FLINT_RELEASE__ == lock["flint_release"],
        "imported flint binding",
    )
    after = inventory_owned(site)
    require(after == before, "import-time distribution mutation")
    relative = expected.relative_to(site.resolve(strict=True)).as_posix()
    return {
        "module": "flint", "module_file_relpath": lexical_relpath(expected),
        "module_file_sha256": sha256(before[relative]),
        "python_flint_version": module.__version__,
        "flint_version": module.__FLINT_VERSION__,
        "flint_release": module.__FLINT_RELEASE__,
    }


def build() -> dict[str, Any]:
    lock, lock_raw, requirements_raw = validate_locks()
    site, interpreter = runtime_preconditions(lock)
    wheel, wheel_contents = audit_wheel()
    installed, installed_contents = audit_installed(site, wheel_contents)
    imported = import_flint(lock, site, installed_contents)
    auditor_raw = read_regular(SCRIPT, maximum=4 * 1024 * 1024, allow_empty=False)
    body: dict[str, Any] = {
        "schema": "cm2.round306c30a.python-flint-fresh-runtime-attestation.v1",
        "verdict": "PASS",
        "offline": True,
        "auditor": {"path": SCRIPT_REL, "sha256": sha256(auditor_raw)},
        "trust_roots": {
            "runtime_lock": {"path": LOCK_REL, "sha256": sha256(lock_raw)},
            "requirements_lock": {
                "path": REQUIREMENTS_REL, "sha256": sha256(requirements_raw)
            },
        },
        "interpreter": interpreter,
        "sealed_wheel": wheel,
        "installed_distribution": installed,
        "imported_flint": imported,
    }
    body["attestation_payload_sha256"] = object_sha256(body)
    return body


def main() -> int:
    try:
        require(len(sys.argv) == 1, "no arguments accepted")
        sys.stdout.buffer.write(canonical(build()) + b"\n")
        sys.stdout.buffer.flush()
    except Exception as error:
        print(
            "C30A_FRESH_RUNTIME_ATTESTATION_REJECT:"
            + error.__class__.__name__ + ":" + str(error),
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
