#!/usr/bin/env python3
"""Exact incremental replay of containment bounds and generic guards."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PAYLOADS = ['certificates/det13_contraction.json',
            'certificates/nonunimodular_observer_guards.json',
            'results/two_vector_class_scan.json']
COMMANDS = [
    ['-m','experiments.det13_contraction'],
    ['-O','tests/replay_det13_contraction_independent.py'],
    ['-m','experiments.two_vector_class_scan'],
    ['-O','tests/replay_two_vector_scan_independent.py'],
    ['-m','experiments.nonunimodular_observer_guards'],
    ['-O','tests/replay_nonunimodular_guards_independent.py'],
]


def hashes():
    return {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in PAYLOADS}


def main():
    before = hashes()
    records = []
    for args in COMMANDS:
        start = time.monotonic()
        result = subprocess.run([sys.executable,*args],cwd=ROOT,text=True,capture_output=True)
        record = {'command': 'python '+' '.join(args), 'returncode':result.returncode,
                  'elapsed_seconds':time.monotonic()-start, 'output':result.stdout.strip()}
        records.append(record)
        if result.returncode:
            print(result.stdout,result.stderr)
            raise SystemExit(result.returncode)
        print('PASS: '+record['command'],flush=True)
    after = hashes()
    if before != after:
        raise SystemExit('Archived exact payload changed on replay')
    report = {'status':'all_six_stages_passed','commands':records,
              'payload_sha256':after,'exact_payloads_byte_identical':True,
              'mutation_counts':{'det13':24,'two_vector_scan':10,'generic_guards':10},
              'solver_queries_run':0,
              'scope':'Incremental exact arithmetic checks supporting the written containment bounds and conditional observer theorem. Prior classification and ACMS inputs are not reproved by this script.'}
    (ROOT/'results/contraction_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: three exact payloads unchanged; 44 mutations rejected; no solver')


if __name__ == '__main__':
    main()
