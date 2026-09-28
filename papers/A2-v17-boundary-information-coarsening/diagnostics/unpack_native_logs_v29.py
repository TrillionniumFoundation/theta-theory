#!/usr/bin/env python3
"""Decode the committed native-companion evidence without executing its content."""
from __future__ import annotations
import argparse
import base64
import lzma
import hashlib
import json
from pathlib import Path


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle",type=Path,default=Path(__file__).with_name("v29-companion-logs.json"))
    parser.add_argument("--output-dir",type=Path,required=True)
    args=parser.parse_args()
    bundle=json.loads(args.bundle.read_text(encoding="utf-8"))
    if bundle.get("format")!="a2-v29-xz-base64-text-evidence-1":
        raise ValueError("Unexpected evidence format")
    out=args.output_dir.resolve()
    out.mkdir(parents=True,exist_ok=True)
    payload=lzma.decompress(base64.b64decode(bundle["xz_base64"],validate=True))
    if len(payload)!=bundle["payload_bytes"] or hashlib.sha256(payload).hexdigest()!=bundle["payload_sha256"]:
        raise ValueError("Payload checksum mismatch")
    texts=json.loads(payload.decode("utf-8"))
    if set(texts)!=set(bundle["files"]):
        raise ValueError("Evidence member mismatch")
    decoded={}
    for name,record in bundle["files"].items():
        if Path(name).name!=name or name in ("", ".", ".."):
            raise ValueError("Nonlocal evidence filename")
        if (out/name).exists():
            raise FileExistsError("Refusing to overwrite "+str(out/name))
        raw=texts[name].encode("utf-8")
        if len(raw)!=record["bytes"] or hashlib.sha256(raw).hexdigest()!=record["sha256"]:
            raise ValueError("Evidence checksum mismatch: "+name)
        raw.decode("utf-8")
        decoded[name]=raw
    for name,raw in decoded.items():
        with (out/name).open("xb") as target:
            target.write(raw)
    print(json.dumps({"status":"verified_and_extracted","files":sorted(decoded)},indent=2))


if __name__=="__main__":
    main()
