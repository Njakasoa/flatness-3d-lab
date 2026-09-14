#!/usr/bin/env python3
"""Replay height separation and linear fibers; no SMT search, archived bytes preserved.

Default requires SymPy and z3-solver. --encodings/--ethos also need cvc5.
--ethos checks two CPC proofs with the pinned external sources.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--encodings', action='store_true')
    ap.add_argument('--ethos', type=Path)
    ap.add_argument('--ethos-source', type=Path)
    ap.add_argument('--cvc5-source', type=Path)
    ap.add_argument('--output', type=Path,
                    default=ROOT/'results/public_det5_fiber_validation.json')
    args = ap.parse_args()
    if any((args.ethos, args.ethos_source, args.cvc5_source)) and not all(
            (args.ethos, args.ethos_source, args.cvc5_source)):
        ap.error('all three external-checker paths are required together')
    commands = [[p] for p in (
        'tests/replay_det5_rational_height_chart_review.py',
        'tests/replay_det5_horizontal_fiber_independent.py',
        'tests/replay_det5_quadratic_witness_independent.py',
        'tests/replay_det5_compact_shape_chart.py',
        'tests/audit_det5_separated_residual_queue.py',
        'tests/audit_det5_combined_residual_queue.py')]
    commands += [['tests/replay_det5_claim0010_review.py', '--skip-primary-text']]
    if args.encodings:
        commands += [[p] for p in (
            'tests/audit_det5_quadratic_chart_independent.py',
            'tests/audit_det5_quadratic_full_width_independent.py',
            'tests/audit_det5_fiber_oracle_independent.py',
            'tests/audit_det5_strong_anchor_rectangle.py')]
    if args.ethos:
        flags = ['--ethos', str(args.ethos.resolve()),
                 '--ethos-source', str(args.ethos_source.resolve()),
                 '--cvc5-source', str(args.cvc5_source.resolve())]
        commands += [['tests/check_det5_fiber_proofs.py', '--archive',
                      'results/'+name+'.json', '--output',
                      'results/'+name+'_ethos_validation.json', *flags]
                     for name in ('det5_fiber_anchor', 'det5_strong_anchor_rectangle')]
    # The original receipts are dependencies of later audits. Restore each
    # command's refreshed reports before starting the next one.
    preserved = {p: p.read_bytes() for folder in ('results', 'certificates')
                 for p in (ROOT/folder).rglob('*') if p.is_file()
                 and p.suffix in ('.json', '.smt2', '.gz')
                 and p.resolve() != args.output.resolve()}
    report = {'status': 'INCOMPLETE', 'solver_queries_run': 0,
              'scope': 'Restricted height bands, exact fibers and a continuous rectangle; no new class exclusion.',
              'encodings_requested': args.encodings,
              'fresh_kernel_checks_requested': bool(args.ethos), 'checks': []}
    for command in commands:
        try:
            proc = subprocess.run([sys.executable, *command], cwd=ROOT,
                                  capture_output=True, text=True)
            refreshed = {str(p.relative_to(ROOT)):
                         hashlib.sha256(p.read_bytes()).hexdigest()
                         for p, original in preserved.items()
                         if p.exists() and p.read_bytes() != original}
            report['checks'].append({
                'check': ' '.join(command[:2] if command[0] == '-m' else command[:1]),
                'exit_code': proc.returncode, 'stdout': proc.stdout,
                'stderr': proc.stderr, 'refreshed_receipt_hashes': refreshed})
        finally:
            for p, original in preserved.items():
                if not p.exists() or p.read_bytes() != original:
                    p.write_bytes(original)
        args.output.write_text(json.dumps(report, indent=2)+'\n')
        if proc.returncode:
            raise SystemExit(proc.stdout + proc.stderr)
        print(report['checks'][-1]['check'] + ': PASS', flush=True)
    report.update(status='PASS', archived_bytes_preserved=True,
                  fresh_kernel_proofs_checked=2 if args.ethos else 0)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('DET5_FIBER_PUBLIC_REPLAY=PASS')


if __name__ == '__main__':
    main()
