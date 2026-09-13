#!/usr/bin/env python3
"""Verify archived public bytes before rerunning experiments."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def check(manifest):
    failures = []
    for name, item in manifest['files'].items():
        path = ROOT / name
        if not path.is_file():
            failures.append(name + ': missing')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            failures.append(name + ': SHA-256 mismatch')
    return failures

def main():
    failures = check(json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text()))
    if failures:
        raise SystemExit('PUBLIC_SNAPSHOT=FAIL\n' + '\n'.join(failures))
    print('PUBLIC_SNAPSHOT=PASS')

if __name__ == '__main__':
    main()
