"""Independent coupled-frame encoding and old-SAT separation audit.

No discovery imports or solver queries. Rebuilds the new clauses atop the
independently reviewed transfer formulation and checks its frozen bindings.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import hashlib,json
import z3
from audit_det5_scaled_pending_transfer_independent import formula as transfer_formula
from audit_det5_scaled_frame_independent import compare,need,expect_rejection,rat,canonical
from replay_det5_coupled_intervals import per_vertex,BMIN,BMAX,R,W

ROOT=Path(__file__).resolve().parents[1]

def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def key(row):return tuple(row['Y_extrema']),tuple(row['U_extrema']),row['node']

def reconstruction(C,S,row,cert):
    base,F,T,b,lifted,dirs,_=transfer_formula(C,S,row)
    groups={'excluded_rectangles':[],'tau_envelopes':[],'static_bounds':[],
            'directional_static_envelopes':[],'directional_perspective_envelopes':[]}
    free=[i for i in range(4) if i not in row['Y_extrema']];excluded=[]
    for leaf in cert['leaves']:
        if leaf['extrema']!=row['Y_extrema']:continue
        groups['excluded_rectangles'].append(z3.Or(*[a for i,(lo,hi) in zip(free,leaf['box']) for a in (T[i][1]<rat(lo),T[i][1]>rat(hi))]))
        excluded.append(leaf['node'])
    tau={}
    for j in range(4):
        ids=[i for i in range(4) if i!=j];tau[j,j]=rat(0)
        a,c=[z3.Real(f'tau{i}_{j}') for i in ids[:2]]
        for i,t in zip(ids,(a,c,b-a-c)):
            tau[i,j]=t;f=F[i][j]
            groups['tau_envelopes'] += [t>=rat(BMIN)*f,t<=rat(BMAX)*f,
                                       t>=b+rat(BMAX)*f-rat(BMAX),t<=b+rat(BMIN)*f-rat(BMIN)]
    products={(i,j,k):(z3.Real(f'w{i}_{j}_{k}') if (i,j,k) in lifted else z3.simplify(F[i][j]*T[i][k]))
              for i in range(4) for j in range(4) for k in range(3)}
    records=[]
    for i in range(4):
        for u in dirs:
            iv=per_vertex(C['contact_points'],row['Y_extrema'],row['U_extrema'],row['box'],i,u)
            lo,hi=iv['implemented_static'];cap=iv['cap'];g=sum(u[k]*T[i][k] for k in range(3))
            records.append({'vertex':i,'direction':list(u),'bounds':[str(lo),str(hi)],'homogeneous_cap':str(cap)})
            groups['static_bounds'] += [g>=rat(lo),g<=rat(hi)]
            for j in range(4):
                if i==j:continue
                f,t=F[i][j],tau[i,j];z=sum(u[k]*products[i,j,k] for k in range(3))
                groups['directional_static_envelopes'] += [z>=rat(lo)*f,z>=g+rat(hi)*f-rat(hi),z<=g+rat(lo)*f-rat(lo),z<=rat(hi)*f]
                groups['directional_perspective_envelopes'] += [z>=-rat(cap)*t,z>=g+rat(cap)*t-rat(cap)*b,z<=g-rat(cap)*t+rat(cap)*b,z<=rat(cap)*t]
    expected=list(base)
    for clauses in groups.values():expected += clauses
    return expected,F,T,b,dirs,groups,excluded,records


def evaluate(clauses,assignment):
    substitutions=[(z3.Real(n),rat(v)) for n,v in assignment.items()]
    values=[z3.simplify(z3.substitute(e,*substitutions)) for e in clauses]
    need(all(z3.is_true(v) or z3.is_false(v) for v in values),'full rational substitution')
    return sum(z3.is_false(v) for v in values)


def main():
    archivepath='results/det5_coupled_scaled_frame.json';raw=(ROOT/archivepath).read_bytes();data=json.loads(raw)
    sourcepath='results/det5_scaled_pending_transfer.json';source=read(sourcepath)
    certpath='results/det5_class5_y_cvc5_validation.json';cert=read(certpath)
    need(sha(sourcepath)==data['source_sha256'],'frozen predecessor archive')
    need(sha(certpath)==data['certified_Y_receipt_sha256'],'frozen certified rectangles')
    oldaudit=read('results/det5_scaled_pending_transfer_validation.json')
    need(oldaudit['status']=='PASS' and oldaudit['archive_sha256']==sha(sourcepath),'previous transfer audit binding')
    priorinputs={r['path']:r['input_sha256'] for r in oldaudit['inputs']}
    for p,h in priorinputs.items():need(sha(p)==h,'unchanged previous input')
    boundaudit=read('results/det5_conditional_width_bounds_validation.json')
    need(boundaudit['status']=='PASS' and boundaudit['old_proof_receipt_sha256']==sha(certpath),'independently audited closed rectangles')
    C=next(c for c in read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index']==5)
    S=next(c for c in read('results/two_vector_class_scan.json')['classes'] if c['class_index']==5)
    old={key(r):r for r in source['queries']};seen=set();inputs=[];control=None
    need(len(data['queries'])==9,'frozen nine new queries')
    for row in data['queries']:
        k=key(row);need(k in old and k not in seen,'unique inherited target');seen.add(k)
        need(row['box']==old[k]['box'] and row['previous_status']==old[k]['status'],'unchanged source domain and label')
        p=row['path'];need(sha(p)==row['input_sha256'],'new input hash')
        expected,F,T,b,dirs,groups,excluded,records=reconstruction(C,S,row,cert)
        actual=list(z3.parse_smt2_file(str(ROOT/p)));compare(expected,actual)
        need(row['excluded_Y_leaves']==excluded and row['intervals']==records,'all interval and exclusion metadata')
        need(row['new_assertions']==sum(map(len,groups.values())),'new clause count')
        need(len(actual)==row['base_assertions']+row['new_assertions'],'complete assertion count')
        need(row['status'] in ('sat','unsat','unknown'),'recognized result label')
        if row['status']=='sat':need(evaluate(actual,row['assignment'])==0,'saved full coupled SAT assignment')
        inputs.append({'path':p,'input_sha256':sha(p),'status':row['status'],'assertions':len(actual),
                       'group_counts':{g:len(v) for g,v in groups.items()}})
        if control is None:control=(row,expected,actual,groups)
    separations=[]
    for oldrow in source['queries']:
        if oldrow['status']!='sat':continue
        _,_,_,_,_,groups,_,_=reconstruction(C,S,oldrow,cert)
        counts={g:evaluate(groups[g],oldrow['assignment']) for g in ('excluded_rectangles','static_bounds','directional_static_envelopes')}
        separations.append({'Y_extrema':oldrow['Y_extrema'],'U_extrema':oldrow['U_extrema'],'node':oldrow['node'],
                            'old_input_path':oldrow['path'],'failed_new_tau_free_assertions':counts,
                            'rejected_by_static_direction_coupling':counts['static_bounds']+counts['directional_static_envelopes']>0})
    row,expected,actual,groups=control
    mutations=[]
    for group in ('excluded_rectangles','tau_envelopes','directional_static_envelopes','directional_perspective_envelopes'):
        candidates=[e for e in groups[group] if canonical(z3.simplify(e)) is not True]
        target=next((e for e in candidates if canonical(z3.simplify(e)) is not False),None)
        if target is None:continue
        mutations.append(expect_rejection('reversed '+group,lambda target=target:compare(expected,actual+[z3.Not(target)])))
    need((ROOT/archivepath).read_bytes()==raw,'coupled archive remained frozen')
    result={'status':'PASS','scope':'Independent full assertion reconstruction, frozen input/rectangle bindings, and exact evaluation of old saved SAT assignments against new tau-free cuts. Archived UNKNOWN/UNSAT labels do not prove exclusion; no solver calls.',
            'archive_sha256':sha(archivepath),'source_sha256':sha(sourcepath),'certified_rectangle_receipt_sha256':sha(certpath),
            'new_inputs_checked':len(inputs),'previous_inputs_hash_bound':len(priorinputs),'inputs':inputs,
            'recorded_status_counts':dict(Counter(r['status'] for r in inputs)),
            'old_SAT_assignments_checked':len(separations),'old_SAT_assignments_rejected_by_static_direction_coupling':sum(r['rejected_by_static_direction_coupling'] for r in separations),
            'old_SAT_separations':separations,'rejected_mutations':mutations,'solver_queries_run':0,'unsat_proofs_checked':0}
    (ROOT/'results/det5_coupled_scaled_encoding_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','new_inputs_checked','recorded_status_counts','old_SAT_assignments_checked','old_SAT_assignments_rejected_by_static_direction_coupling','solver_queries_run')},indent=2))
if __name__=='__main__':main()
