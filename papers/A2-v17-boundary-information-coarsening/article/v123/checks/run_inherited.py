"""Execute, rather than merely import, the preserved v122 regression entry points."""
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
for name in ('flags_elliptic', 'loewy', 'ramification_intrinsic'):
    path = ROOT / 'checks' / 'inherited' / f'{name}.py'
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f'Cannot import {path}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.run()
    out = ROOT / 'evidence' / f'inherited_{name}.json'
    out.write_text(json.dumps(result, indent=2, default=str) + '\n', encoding='utf-8')
    print(f'PASS {name}: {out.name}', flush=True)
