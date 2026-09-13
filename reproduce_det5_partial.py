#!/usr/bin/env python3
"""Replay partial determinant-five results; never run an SMT search.

Default: exact standard-library arithmetic and archived premise/proof bindings.
--encodings: also reconstruct scaled formulas (requires pinned z3-solver and cvc5 Python packages).
--ethos: freshly check 16 archived CPC refutations; requires pinned Ethos,
cvc5 signatures, z3-solver and cvc5 Python syntax adapters. See
proofs/HEIGHT_ETHOS_REPRODUCTION.md. Existing proof receipts stay unchanged.
"""
from pathlib import Path
import argparse, gzip, json, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--encodings',action='store_true')
    ap.add_argument('--ethos',type=Path)
    ap.add_argument('--ethos-source',type=Path)
    ap.add_argument('--cvc5-source',type=Path)
    ap.add_argument('--output',type=Path,default=ROOT/'results/public_det5_partial_validation.json')
    a=ap.parse_args()
    if a.ethos and not(a.ethos_source and a.cvc5_source):
        ap.error('--ethos requires both source paths')
    commands=['tests/replay_det5_conditional_width_bounds.py',
              'tests/replay_det5_direction_envelopes.py',
              'tests/replay_det5_known_width_obstructions.py']
    if a.encodings:
        commands += ['tests/audit_det5_scaled_frame_independent.py',
                     'tests/audit_det5_scaled_pending_transfer_independent.py',
                     'tests/audit_det5_five_direction_box_independent.py',
                     'tests/audit_det5_scaled_enlargement_independent.py',
                     'tests/analyze_det5_width_core_assumptions.py',
                     'tests/audit_det5_certified_y_overlay.py']
    result={'status':'INCOMPLETE','scope':'Partial height domains only; no new class exclusion or global bound.',
            'solver_queries_run':0,'encodings_requested':a.encodings,'checks':[],
            'external_proof_checks':[]}
    for name in commands:
        proc=subprocess.run([sys.executable,str(ROOT/name)],cwd=ROOT,text=True,capture_output=True)
        result['checks'].append({'path':name,'exit_code':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr})
        a.output.write_text(json.dumps(result,indent=2)+'\n')
        if proc.returncode:
            raise SystemExit(name+' failed:\n'+proc.stdout+proc.stderr)
        print(name+': PASS',flush=True)
    if a.ethos:
        sys.path.insert(0,str(ROOT/'tests'))
        from check_height_ethos import need,sha,proof_body,checker,revision,ETHOS_REV,CVC5_REV
        from check_det5_scaled_leaf_cvc5 import reference
        need(revision(a.ethos_source)==ETHOS_REV and revision(a.cvc5_source)==CVC5_REV,'pinned sources')
        result.update(ethos_revision=ETHOS_REV,cvc5_signature_revision=CVC5_REV)
        read=lambda p:json.loads((ROOT/p).read_text())
        rows=list(read('results/det5_class5_y_cvc5_validation.json')['leaves'])
        for archive in ['results/det5_y_corner_gauge_threshold.json','results/det5_y_corner_gauge_refinement.json']:
            rows += [r for r in read(archive)['queries'] if r['status']=='unsat']
        for receipt in ['results/det5_scaled_width_core_ethos_validation.json','results/det5_sliced_proof_validation.json']:
            rows.append(read(receipt))
        need(len(rows)==16,'expected sixteen new proof payloads')
        with tempfile.TemporaryDirectory(prefix='det5-public-proof-') as tmp:
            p=Path(tmp)/'proof.cpc';q=Path(tmp)/'reference.smt2'
            for row in rows:
                raw=(ROOT/row['input_path']).read_bytes()
                proof=gzip.decompress((ROOT/row['proof_path']).read_bytes())
                need(sha(raw)==row['input_sha256'] and sha(proof)==row['proof_sha256'],'archived payload binding')
                ref,vs=reference(raw.decode());body,_=proof_body(proof,vs)
                need(sha(ref.encode())==row['reference_sha256'],'archived reference binding')
                p.write_text(body);q.write_text(ref)
                checked=checker(a.ethos,a.cvc5_source,p,q)
                need(checked['exit_code']==0 and checked['stdout']=='correct' and not checked['stderr'],'external proof check')
                result['external_proof_checks'].append({'input_path':row['input_path'],'input_sha256':sha(raw),'proof_path':row['proof_path'],'proof_sha256':sha(proof),'reference_sha256':sha(ref.encode()),'ethos':checked})
                a.output.write_text(json.dumps(result,indent=2)+'\n')
                print(row['proof_path']+': Ethos PASS',flush=True)
            p.write_text(body+'\n(assume @fresh_unrelated false)\n')
            bad=checker(a.ethos,a.cvc5_source,p,q)
            need(bad['exit_code']!=0 and 'assumption' in (bad['stdout']+bad['stderr']).lower(),'unreferenced assumption rejected')
            result['unreferenced_assumption_rejected']=True
    result['status']='PASS'
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print('DET5_PARTIAL_PUBLIC_REPLAY=PASS')

if __name__=='__main__':
    main()
