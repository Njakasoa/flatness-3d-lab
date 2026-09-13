#!/usr/bin/env python3
"""Replay exact height-cover evidence; optional external Ethos proof checking.

Default mode checks data, encodings and artifact binding without solver calls.
Supply all three external paths to recheck the CPC proofs with Ethos. Solver
regeneration is separate: tests/replay_height_cover_cvc5.py.
"""
import argparse,gzip,hashlib,json,subprocess,sys,time
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ethos',type=Path);p.add_argument('--ethos-source',type=Path);p.add_argument('--cvc5-source',type=Path)
    args=p.parse_args();paths=[args.ethos,args.ethos_source,args.cvc5_source]
    if any(paths) and not all(paths):p.error('Supply --ethos, --ethos-source and --cvc5-source together')
    commands=[['-O','tests/replay_height_rank_independent.py'],
              ['tests/audit_height_encodings.py'],['tests/audit_height_cover_independent.py']]
    if all(paths):commands.append(['tests/check_height_ethos.py','--ethos',str(args.ethos),
                                  '--ethos-source',str(args.ethos_source),'--cvc5-source',str(args.cvc5_source)])
    stages=[]
    for command in commands:
        start=time.monotonic();r=subprocess.run([sys.executable,*command],cwd=ROOT,text=True,capture_output=True)
        if r.returncode:
            print(r.stdout,r.stderr);raise SystemExit(r.returncode)
        stages.append({'command':'python '+' '.join(command),'returncode':0,'elapsed_seconds':time.monotonic()-start})
        print('PASS: '+' '.join(command[:2]),flush=True)
    # Bind every exported proof to both its independent input and receipt.
    sys.path.insert(0,str(ROOT/'tests'))
    from replay_height_cover_cvc5 import statement,cover,Q
    cover_data=json.loads((ROOT/'results/height_interval_relaxation.json').read_text())
    leaves,_=cover(cover_data)
    records=json.loads((ROOT/'results/height_cover_cvc5_validation.json').read_text())
    if records['status']!='PASS' or len(records['leaves'])!=62:raise ValueError('incomplete cvc5 evidence')
    G=json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())
    H=json.loads((ROOT/'results/contact_height_charts.json').read_text());checked=[]
    for leaf,r in zip(leaves,records['leaves']):
        idx=leaf['class_index'];ext=leaf['extrema'];node=leaf['node']
        if (r['class_index'],r['extrema'],r['node'])!=(idx,ext,node):raise ValueError('proof leaf binding')
        C=next(c for c in G['classes'] if c['class_index']==idx)
        vectors=next(c for c in H['classes'] if c['class_index']==idx)['gauge_vectors']
        generated=statement(C,vectors,ext,[[Q(x) for x in pair] for pair in leaf['box']]).encode()
        tag=f'{idx}_{ext[0]}_{ext[1]}_{node}';base=ROOT/'certificates/height_cover_cvc5'
        archived=(base/(tag+'.smt2')).read_bytes();packed=(base/(tag+'.cpc.gz')).read_bytes();proof=gzip.decompress(packed)
        if archived!=generated:raise ValueError('independent input byte mismatch')
        for payload,key in ((archived,'input_sha256'),(packed,'compressed_proof_sha256'),(proof,'proof_sha256')):
            if hashlib.sha256(payload).hexdigest()!=r[key]:raise ValueError('payload hash mismatch')
        if r['status']!='unsat' or not r['internal_proof_check'] or not r['check_proofs_complete']:raise ValueError('cvc5 proof status')
        if any('TRUST' in rule for rule in r['proof_rules']):raise ValueError('trusted proof rule')
        checked.append(tag)
    report={'status':'PASS','stages':stages,'bound_proof_inputs':len(checked),'solver_queries_run':0,
            'external_proofs_checked_this_run':bool(all(paths)),
            'scope':'Exact cover/encoding and proof-payload binding replay. Without external paths, archived CPC proofs are hashed, not rechecked by a proof kernel; use the Ethos command to perform that check.'}
    (ROOT/'results/height_cover_reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: all62 independent inputs and compressed proof payloads bound; zero solver queries')


if __name__=='__main__':main()
