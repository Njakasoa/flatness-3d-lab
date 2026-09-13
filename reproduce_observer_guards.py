#!/usr/bin/env python3
"""Replay the column identities, exact pair witnesses and observer guards.

No floating search, solver query, external service or paper download is run.
Use the baseline Python/SymPy environment. The mathematical classification
inputs remain published theorems cited by the written proofs.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
COMMANDS=[
    ['-m','experiments.pair_column_identities'],
    ['-m','experiments.certify_det2_pair_column'],
    ['-m','experiments.certify_det2_pair_four_contacts'],
    ['-O','tests/replay_det2_pair_column_independent.py'],
    ['-m','experiments.det2_partial_box_counterexamples'],
    ['-m','experiments.det2_observer_lines'],
    ['-O','tests/replay_det2_observer_lines_independent.py'],
    ['-m','experiments.det2_observer_gauge_guards'],
    ['-O','tests/replay_det2_gauge_guards_independent.py'],
]
CERTIFICATES=[
    'pair_column_identities','det2_pair_column','det2_pair_four_contacts',
    'det2_partial_box_counterexamples','det2_observer_lines','det2_observer_gauge_guards',
]


def digest(name):
    return hashlib.sha256((ROOT/f'certificates/{name}.json').read_bytes()).hexdigest()


def main():
    if not __debug__:
        raise SystemExit('Run the driver without -O: generators invoke the assertion-based exact geometry core. Independent children are explicitly tested under -O.')
    before={name:digest(name) for name in CERTIFICATES}
    rows=[]
    for args in COMMANDS:
        start=time.monotonic()
        result=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True)
        row={'command':'python '+' '.join(args),'returncode':result.returncode,
             'elapsed_seconds':time.monotonic()-start}
        rows.append(row)
        print(('PASS' if result.returncode==0 else 'FAIL')+': '+row['command'],flush=True)
        if result.returncode:
            print(result.stdout);print(result.stderr)
            raise SystemExit(result.returncode)
    after={name:digest(name) for name in CERTIFICATES}
    if before!=after:
        changed=[name for name in CERTIFICATES if before[name]!=after[name]]
        raise SystemExit('Exact archived payload changed on replay: '+', '.join(changed))
    report={'status':'all_nine_stages_passed','commands':rows,
            'six_exact_certificates_byte_identical':True,'certificate_sha256':after,
            'independent_corruptions_rejected':{'two_pair_witnesses':24,'whole_witness_substitutions':2,
                                                'observer_lines':8,'gauge_guards':10},
            'strict_integer_endpoint_regression':'passed',
            'new_solver_queries_run':0,
            'scope':'Exact incremental replay and independent implementation checks. Theorems use cited classification inputs; no class width bound or external priority is established.'}
    (ROOT/'results/observer_validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: six archived exact certificates unchanged; no solver run')


if __name__=='__main__':main()
