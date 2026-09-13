#!/usr/bin/env python3
"""Check class-4 archived evidence using the Python standard library.

Optional --audit-python runs the existing Z3-based geometry/formula audit;
that audit parses and normalizes formulas but issues no solver queries.
Proof-kernel replay is separate: tests/check_det5_class4_ethos.py.
"""
import argparse
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'tests'))
from check_height_ethos import real_reference, proof_body, need, ETHOS_REV, CVC5_REV


def read(path):
    return json.loads((ROOT / path).read_text())


def sha(payload):
    return hashlib.sha256(payload).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit-python', type=Path,
                        help='Python with z3-solver installed, for independent formula audit')
    args = parser.parse_args()
    manifest = read('certificates/det5_class4_contact_exclusion.json')
    for path, digest in manifest['evidence_sha256'].items():
        need(sha((ROOT / path).read_bytes()) == digest, 'evidence hash: ' + path)
    subprocess.run([sys.executable, 'tests/replay_nonunimodular_guards_independent.py'],
                   cwd=ROOT, check=True)
    if args.audit_python:
        subprocess.run([str(args.audit_python.absolute()), 'tests/audit_det5_height_independent.py'],
                       cwd=ROOT, check=True)
    points = [[0, 0, 0], [5, 1, 1], [0, 1, 0], [0, 0, 1]]
    template = read('certificates/contact_templates.json')
    embeddings = template['embeddings']
    need(len(embeddings) == 63 and [e['class_index'] for e in embeddings] == list(range(63)),
         '63 indexed necessary classes')
    need(embeddings[4]['vertices'] == points == manifest['contact_points'], 'class-4 points')
    excluded = [4, 6, 7, 8, 9]
    survivors = [i for i in range(63) if i not in excluded]
    need(manifest['excluded_full_tetrahedral_classes_at_candidate_width'] == excluded,
         'exclusion dependency set')
    need(manifest['surviving_full_contact_classes_at_width_ge_2_plus_sqrt2'] == survivors,
         'surviving class list')
    need(manifest['surviving_count_at_candidate_width'] == len(survivors) == 58,
         '58 remaining classes')
    need(manifest['surviving_count_above_original_c'] == 62, 'original threshold count')
    need(manifest['upper_bound'] == '17/5' and manifest['class_index'] == 4,
         'restricted class bound')
    prior = read('certificates/height_contact_exclusions.json')
    need(prior['excluded_full_tetrahedral_classes_at_candidate_width'] == [6, 7, 8, 9],
         'prior exclusion dependency')
    need([i for i in survivors if i < 10] == [0, 1, 2, 3, 5], 'five tetrahedral survivors')
    need(sum(len(embeddings[i]['vertices']) > 4 for i in survivors) == 52,
         '52 larger full hulls retained')
    archive = read('results/det5_height_interval.json')
    expected = {(0, 1), (0, 2), (0, 3), (1, 0), (1, 3)}
    charts = [c for c in archive['charts'] if c['class_index'] == 4]
    need(len(charts) == 5 and {tuple(c['extrema']) for c in charts} == expected,
         'five covering charts')
    for chart in charts:
        need(chart['complete_cover'] and not chart['pending_leaves'] and
             chart['closed_leaves'] == ['r'] and chart['queries'] == 1, 'complete root chart')
    queries = [q for q in archive['queries'] if q['class_index'] == 4]
    need(len(queries) == 5 and {tuple(q['extrema']) for q in queries} == expected,
         'five unique discovery roots')
    for query in queries:
        need(query['status'] == 'unsat' and query['node'] == 'r' and
             [[Fraction(x) for x in r] for r in query['box']] == [[0, 1], [0, 1]],
             'full-square root')
    cvc = read('results/det5_class4_cvc5_validation.json')
    ethos = read('results/det5_class4_ethos_validation.json')
    need(cvc['status'] == ethos['status'] == 'PASS' and
         cvc['class_index'] == ethos['class_index'] == 4 and
         cvc['contact_points'] == points and cvc['guard_count'] == 40,
         'completed class-4 receipts')
    need(ethos['checker']['revision'] == ETHOS_REV and
         ethos['cvc5_signature_revision'] == CVC5_REV, 'pinned proof checker and signatures')
    need(ethos['cvc5_receipt_sha256'] == sha((ROOT / 'results/det5_class4_cvc5_validation.json').read_bytes()),
         'Ethos binds cvc5 receipt')
    need(ethos['adapter_sha256'] == sha((ROOT / 'tests/check_height_ethos.py').read_bytes()),
         'reference adapter binding')
    need(len(cvc['leaves']) == len(ethos['leaves']) == ethos['external_correct'] == 5,
         'five externally checked proofs')
    need(len(ethos['controls']) == 4 and all(c['rejected'] for c in ethos['controls']),
         'four rejected corruption controls')
    external = {r['leaf']: r for r in ethos['leaves']}
    seen = set()
    for row in cvc['leaves']:
        pair = tuple(row['extrema'])
        need(pair in expected and pair not in seen and row['class_index'] == 4 and
             row['node'] == 'r', 'unique root proof')
        seen.add(pair)
        tag = f'4_{pair[0]}_{pair[1]}_r'
        checked = external[tag]
        base = ROOT / 'certificates/det5_class4_cvc5' / tag
        smt = base.with_suffix('.smt2').read_bytes()
        packed = base.with_suffix('.cpc.gz').read_bytes()
        raw = gzip.decompress(packed)
        for payload, key in ((smt, 'input_sha256'), (packed, 'compressed_proof_sha256'),
                             (raw, 'proof_sha256')):
            need(sha(payload) == row[key] == checked[key], 'proof/input binding: ' + tag)
        need(row['status'] == 'unsat' and row['internal_proof_check'] and
             row['check_proofs_complete'] and
             not any('TRUST' in r or 'SORRY' in r for r in row['proof_rules']),
             'complete untrusted-rule-free refutation')
        adapted, assertions, variables = real_reference(smt.decode())
        _, counts = proof_body(raw, variables)
        need(sha(adapted.encode()) == checked['reference_sha256'] and
             assertions == checked['assertions'] and counts == checked['proof_commands'],
             'reference and proof framing binding')
        need(checked['reference_binding'] and checked['balanced_scopes'] and
             checked['final_top_level_false'] and checked['exit_code'] == 0 and
             checked['stdout'] == 'correct' and not checked['stderr'], 'archived Ethos result')
    report = {'status': 'PASS', 'class_index': 4, 'bound_proof_inputs': 5,
              'surviving_count_at_candidate_width': 58, 'solver_queries_run': 0,
              'formula_audit_run': bool(args.audit_python),
              'external_proofs_checked_this_run': False,
              'scope': 'Exact guard/count checks and archived proof/input/reference binding. '
                       'CPC framing and hashes are checked; a proof kernel is not run.'}
    (ROOT / 'results/det5_class4_reproduction.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
