"""Incremental encoding audit binding the previously audited 514-node prefix.

Freshly reconstructs only new formulas; hashes every prior input and checks
the complete frontier. No solver calls and no UNSAT proof checking.
"""
from pathlib import Path
import hashlib,json
import z3
from audit_det5_joint_cover_independent import frontier,formula,need,compare

ROOT=Path(__file__).resolve().parents[1]
BASE_REV='cb20dfd'


def read(path):return json.loads((ROOT/path).read_text())


def main():
    # The prior turn actually executed this audit successfully. Bind its
    # archived receipt, mathematical reconstructor, and all previous inputs.
    pinned={'tests/audit_det5_joint_cover_independent.py': 'bc00ce9350e922532ab99cdd052b8c09c82095160c482cefbb55f5f9ef93e75b', 'tests/audit_det5_height_independent.py': 'c6d1f03facfff8f588dd2bceeb035d290b6203fa3e3fad30348c6d6e57049c4b', 'tests/audit_height_cover_independent.py': '74b0dec05d07435223b95af6476d2d7651e715b5d681e260b91be076c9789154', 'results/det5_joint_cover_encoding_validation.json': 'ca0f9370e7497e78a450d14286a068b779caf79fd015975afd3ac17500eb6a98', 'results/det5_joint_continuation.json': '45fc8d804742dcaa8d56e1c831f925616c9f58c6a44b40f4fbd1396f974c8a88'}
    for path,digest in pinned.items():
        need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,
             "unchanged prior audit artifact: "+path)
    prior=read('results/det5_joint_cover_encoding_validation.json')
    need(prior['status']=='PASS' and prior['query_count']==514,'audited prefix receipt')
    for entry in prior['inputs']:
        need(hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'],'unchanged prior formula')
    C=next(c for c in read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index']==5)
    S=next(c for c in read('results/two_vector_class_scan.json')['classes'] if c['class_index']==5)
    old=read('results/det5_joint_continuation.json');round2=read('results/det5_joint_round2.json')
    seed=round2['round2_seed'];need(seed['query_count']==514,'round2 seed length')
    need(hashlib.sha256((ROOT/seed['path']).read_bytes()).hexdigest()==seed['sha256'],'round2 seed hash')
    need(round2['queries'][:514]==old['queries'],'unchanged previous query records')
    report=[];fresh=[]
    for row in round2['queries'][514:]:
        p=ROOT/row['path'];compare(formula(C,S,row),list(z3.parse_smt2_file(str(p))))
        fresh.append({'path':row['path'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        if len(fresh)%100==0:print('PASS fresh joint encodings: '+str(len(fresh)),flush=True)
    charts=frontier(round2,C)
    report.append({'archive':'results/det5_joint_round2.json','query_count':len(round2['queries']),
                   'complete_charts':sum(c['complete_cover'] for c in charts),
                   'pending_boxes':sum(c['pending_leaves'] for c in charts)})
    volume=read('results/det5_joint_volume_gaps.json');seed=volume['volume_gap_seed']
    need(hashlib.sha256((ROOT/seed['path']).read_bytes()).hexdigest()==seed['sha256'],'volume seed hash')
    need(volume['queries'][:seed['query_count']]==round2['queries'],'unchanged round2 prefix')
    for row in volume['queries'][seed['query_count']:]:
        expected=formula(C,S,row)
        expected += [z3.Real('height_gap')>z3.RealVal('2042829/50000000'),
                     z3.Real('U_gap')>z3.RealVal('2042829/100000000')]
        p=ROOT/row['path'];compare(expected,list(z3.parse_smt2_file(str(p))))
        need(row['volume_gap_cuts'],'new gap formula marker')
        fresh.append({'path':row['path'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    charts=frontier(volume,C)
    report.append({'archive':'results/det5_joint_volume_gaps.json','query_count':len(volume['queries']),
                   'complete_charts':sum(c['complete_cover'] for c in charts),
                   'pending_boxes':sum(c['pending_leaves'] for c in charts)})
    out={'status':'PASS','bound_prior_revision':BASE_REV,'prior_encodings_bound':514,
         'new_encodings_checked':len(fresh),'archives':report,'fresh_inputs':fresh,
         'solver_queries_run':0,'scope':'Incremental exact formula and complete frontier audit. Neither archived UNSAT labels nor any class exclusion are established.'}
    (ROOT/'results/det5_joint_round2_encoding_validation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','prior_encodings_bound','new_encodings_checked','archives','solver_queries_run')}))


if __name__=='__main__':main()
