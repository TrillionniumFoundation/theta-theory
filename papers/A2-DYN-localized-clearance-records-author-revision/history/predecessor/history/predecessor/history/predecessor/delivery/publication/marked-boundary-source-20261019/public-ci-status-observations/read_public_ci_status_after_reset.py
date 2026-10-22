#!/usr/bin/env python3
"""Read only public, unauthenticated GitHub Actions metadata; preserve raw bytes."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

root = Path('/workspace/scratch/b5cc344d4c8e/iteration-20261019c-recovery/current-ci/independent-public-api-after-reset')
root.mkdir(parents=True, exist_ok=False)
base = 'https://api.github.com/repos/TrillionniumFoundation/theta-theory'
queries = {
    'run': base + '/actions/runs/39281615689',
    'job': base + '/actions/jobs/118156848926',
    'attempt_jobs': base + '/actions/runs/39281615689/attempts/1/jobs?per_page=100',
}

def now():
    return datetime.now(timezone.utc).isoformat()

def read(item):
    name, url = item
    receipt = {'url': url, 'method': 'GET', 'authentication': 'none', 'requested_at': now(), 'transport': 'Python urllib over authorized read-only network exec'}
    try:
        request = Request(url, headers={'User-Agent': 'A2-DYN-author-publication-audit', 'Accept': 'application/vnd.github+json', 'Cache-Control': 'no-cache'})
        try:
            response = urlopen(request, timeout=25)
        except HTTPError as error:
            response = error
        with response:
            payload = response.read()
            receipt.update({'http_status': response.status, 'response_headers': dict(response.headers), 'response_url': response.geturl(), 'response_bytes': len(payload), 'response_sha256': hashlib.sha256(payload).hexdigest()})
        (root / (name + '.response.bin')).write_bytes(payload)
        try:
            parsed = json.loads(payload)
            (root / (name + '.parsed.json')).write_bytes((json.dumps(parsed, indent=2) + '\n').encode())
            receipt['parsed_summary'] = {key: parsed.get(key) for key in ('id', 'head_sha', 'head_branch', 'status', 'conclusion', 'total_count') if key in parsed}
            if isinstance(parsed.get('jobs'), list):
                receipt['parsed_summary']['jobs'] = [{key: row.get(key) for key in ('id', 'head_sha', 'status', 'conclusion', 'started_at', 'completed_at')} for row in parsed['jobs']]
        except (UnicodeDecodeError, json.JSONDecodeError):
            receipt['json_decoded'] = False
    except Exception as error:
        receipt['transport_error'] = {'type': type(error).__name__, 'message': str(error)}
    receipt['observed_at'] = now()
    (root / (name + '.receipt.json')).write_bytes((json.dumps(receipt, indent=2) + '\n').encode())
    return receipt

with ThreadPoolExecutor(max_workers=3) as pool:
    records = list(pool.map(read, queries.items()))
(root / 'ACTUAL_PUBLIC_API_READBACK.json').write_bytes((json.dumps(records, indent=2) + '\n').encode())
print(json.dumps([{key: row[key] for key in ('url', 'http_status', 'parsed_summary', 'transport_error', 'observed_at') if key in row} for row in records], indent=2))
