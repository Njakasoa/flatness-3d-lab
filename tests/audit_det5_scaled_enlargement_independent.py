"""Independent larger-box five-width encoding audit; no solver calls.

Imports only independent reconstruction helpers. No SAT-body, UNSAT-proof,
whole-chart, or class-exclusion inference is made from the archived labels.
"""
from copy import deepcopy
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json
import z3
from audit_det5_scaled_pending_transfer_independent import formula
from audit_det5_scaled_frame_independent import reconstruct,canonical,compare,need,expect_rejection

ROOT=Path(__file__).resolve().parents[1]
KEEP={(0,0,1),(0,1,-1),(1,-2,-2)}
BOXES={
    'half_half':[['1/2','1'],['1/2','1'],['1/2','1'],['1/2','1']],
    'three_quarters_zero':[['3/4','1'],['3/4','1'],['0','1'],['0','1']],
    'zero_half':[['0','1'],['0','1'],['1/2','1'],['1/2','1']],
}
ORIGINAL=[['3/4','1'],['3/4','1'],['1/2','1'],['1/2','1']]

def digest(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def read(path):return json.loads((ROOT/path).read_text())
def key(e):return canonical(z3.simplify(e))

def expected(C,S,row):
    full,F,T,b,lifted,dirs,cuts=formula(C,S,row)
    base,*_=reconstruct(C,S,{'kind':'relaxation','Y_extrema':row['Y_extrema']})
    widths={tuple(u):e for u,e in zip(dirs,base[-15:])}
    need(len(widths)==15 and KEEP<=set(widths),'complete width clause binding')
    width_keys={key(e) for e in widths.values()}
    result=[e for e in full if key(e) not in width_keys]+[widths[u] for u in sorted(KEEP)]
    result_keys={key(e) for e in result}
    # The direct normalized Y and U target constraints survive width pruning.
    need(key(b<z3.RealVal('5/17')) in result_keys,'direct Y-width target retained')
    uheights=[sum(u*t for u,t in zip((1,-1,-2),rowt)) for rowt in T]
    span=uheights[row['U_extrema'][1]]-uheights[row['U_extrema'][0]]
    need(key(span>z3.RealVal('17/5')*b) in result_keys,'direct U-width target retained')
    need(all(key(widths[u]) not in result_keys for u in set(widths)-KEEP),'all other disjunctive width clauses removed')
    return result,widths


def main():
    source='results/det5_scaled_box_enlargement.json';raw=(ROOT/source).read_bytes();data=json.loads(raw)
    C=next(c for c in read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index']==5)
    S=next(c for c in read('results/two_vector_class_scan.json')['classes'] if c['class_index']==5)
    need(len(data['queries'])==3 and {r['tag'] for r in data['queries']}==set(BOXES),'exactly three distinct enlarged boxes')
    reports=[];control=None
    for row in data['queries']:
        need(row['Y_extrema']==[0,3] and row['U_extrema']==[0,3],'same actual extrema chart')
        need(row['box']==BOXES[row['tag']],'intended enlarged rectangle')
        contains=all(Q(l)<=Q(ol)<=Q(oh)<=Q(h) for (l,h),(ol,oh) in zip(row['box'],ORIGINAL))
        strict=any(Q(l)<Q(ol) or Q(oh)<Q(h) for (l,h),(ol,oh) in zip(row['box'],ORIGINAL))
        need(contains and strict,'strictly contains original certified box')
        need(set(map(tuple,row['additional_width_directions']))==KEEP and row['retained_Y_U_targets'] is True,'five-width metadata')
        path=row['path'];need(digest(path)==row['input_sha256'],'new archived formula hash')
        actual=list(z3.parse_smt2_file(str(ROOT/path)));wanted,widths=expected(C,S,row);compare(wanted,actual)
        need(row['status'] in ('sat','unknown (TIMEOUT)'),'no enlarged refutation is present')
        reports.append({'tag':row['tag'],'box':row['box'],'path':path,'input_sha256':digest(path),
                        'assertions':len(actual),'recorded_status':row['status'],'strictly_contains_original_box':True})
        if control is None:control=(row,wanted,actual,widths)
    row,wanted,actual,widths=control
    wrong=deepcopy(row);wrong['box'][0][0]='3/4'
    altered,_=expected(C,S,wrong)
    controls=[expect_rejection('changed enlarged height bound',lambda:compare(altered,actual))]
    target=key(widths[(0,0,1)]);without=[e for e in actual if key(e)!=target]
    need(len(without)<len(actual),'mutation removes actual Z width test')
    controls.append(expect_rejection('missing retained Z width test',lambda:compare(wanted,without)))
    controls.append(expect_rejection('unrequested sixth width test',lambda:compare(wanted,actual+[widths[(0,1,1)]])))
    need((ROOT/source).read_bytes()==raw,'enlargement archive remained frozen')
    result={'status':'PASS','scope':'Exact independent reconstruction of three strictly enlarged rectangles with five width targets and unchanged necessary gauge/volume cuts. Archived SAT means outer feasibility only. No solver or proof-kernel calls; no enlarged box or class is excluded.',
            'archive_sha256':hashlib.sha256(raw).hexdigest(),'original_box':ORIGINAL,'Y_extrema':[0,3],'U_extrema':[0,3],
            'five_width_directions':[[0,1,0],[1,-1,-2],*map(list,sorted(KEEP))],
            'new_encodings_checked':3,'inputs':reports,'rejected_mutations':controls,'solver_queries_run':0,'unsat_proofs_checked':0}
    (ROOT/'results/det5_scaled_enlargement_encoding_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','new_encodings_checked','inputs','solver_queries_run','unsat_proofs_checked')},indent=2))

if __name__=='__main__':main()
