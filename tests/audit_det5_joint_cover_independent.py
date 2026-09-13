"""Independent exact joint-height frontier and linear-encoding audit.

No experiment imports or solver queries. Checks every box and assertion;
does not prove the archived UNSAT labels. Seed archives remain immutable.
"""
from collections import deque
from copy import deepcopy
from fractions import Fraction as Q
from itertools import permutations
from pathlib import Path
import hashlib, json
import z3
from audit_height_cover_independent import need,expected_assertions,compare,expect_rejection
from audit_det5_height_independent import geometry

ROOT=Path(__file__).resolve().parents[1]


def frontier(data,C):
    _,_,orbits=geometry(C['contact_points'])
    reps={tuple(orb[0]) for orb in orbits}
    expected={(y,u) for y in reps for u in permutations(range(4),2)}
    keys=[(tuple(c['Y_extrema']),tuple(c['U_extrema'])) for c in data['charts']]
    need(len(keys)==len(set(keys))==36 and set(keys)==expected,'all 36 joint charts')
    querykeys=[(tuple(r['Y_extrema']),tuple(r['U_extrema']),r['node']) for r in data['queries']]
    need(len(querykeys)==len(set(querykeys)),'no repeated query')
    need(all((y,u) in expected for y,u,_ in querykeys),'no foreign chart')
    result=[]
    for chart in data['charts']:
        key=(chart['Y_extrema'],chart['U_extrema'])
        rows=[r for r in data['queries'] if (r['Y_extrema'],r['U_extrema'])==key]
        queue=deque([('r',[[Q(0),Q(1)] for _ in range(4)])]);closed=[]
        for row in rows:
            need(bool(queue),'no query below closed cover')
            node,box=queue.popleft()
            need(row['node']==node and [[Q(x) for x in p] for p in row['box']]==box,'exact breadth-first closed box')
            need(row['status'] in ('sat','unsat','unknown'),'known status label')
            if row['status']=='unsat':closed.append(node)
            else:
                axis=max(range(4),key=lambda i:box[i][1]-box[i][0]);l,h=box[axis];mid=(l+h)/2
                for suffix,pair in [('0',[l,mid]),('1',[mid,h])]:
                    child=deepcopy(box);child[axis]=pair;queue.append((node+suffix,child))
        pending=[{'node':n,'box':[[str(x) for x in p] for p in b]} for n,b in queue]
        need(chart['queries']==len(rows),'chart query count')
        need(chart['closed_leaves']==closed and chart['pending_leaves']==pending,'exact closed and pending frontier')
        need(chart['complete_cover']==(not pending),'honest completion status')
        result.append({'Y_extrema':key[0],'U_extrema':key[1],'closed_leaves':len(closed),'pending_leaves':len(pending),'complete_cover':not pending})
    return result


def formula(C,S,row):
    yext,uext=row['Y_extrema'],row['U_extrema']
    box=[[Q(x) for x in p] for p in row['box']]
    expected,gauges,_=expected_assertions(C,S,yext,box[:2])
    # All contact barycentric coefficients have denominator dividing five;
    # hence 37/102 occurs here only as the gauge comparison threshold.
    expected += [z3.substitute(g,(z3.RealVal('37/102'),z3.RealVal('183/500'))) for g in gauges]
    F=[[z3.RealVal(0) for _ in range(4)] for _ in range(4)]
    for j in range(4):
        ids=[i for i in range(4) if i!=j];a,b=[z3.Real(f'f{i}{j}') for i in ids[:2]]
        for i,x in zip(ids,(a,b,1-a-b)):F[i][j]=x
    r=[z3.RealVal(0) if i==uext[0] else z3.RealVal(1) if i==uext[1] else z3.Real(f'Uq{i}') for i in range(4)]
    offset,gap=z3.Reals('U_offset U_gap')
    expected += [offset>=0,offset+2*gap<=1,gap>0,gap<z3.RealVal('5/17')]
    products={}
    for i,(lo,hi) in zip([i for i in range(4) if i not in uext],box[2:]):
        l,h=z3.RealVal(str(lo)),z3.RealVal(str(hi));expected += [r[i]>=l,r[i]<=h]
        for j in range(4):
            if i==j:continue
            p=z3.Real(f'U_product_{i}_{j}');f=F[i][j];products[i,j]=p
            expected += [p>=l*f,p<=h*f,p>=r[i]+h*f-h,p<=r[i]+l*f-l]
    heights=[2,2,1,0]
    for j in range(4):
        expected.append(sum(products.get((i,j),r[i]*F[i][j]) for i in range(4))==offset+gap*heights[j])
    return expected


def main():
    data=json.loads((ROOT/'results/det5_joint_continuation.json').read_text())
    C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes'] if c['class_index']==5)
    S=next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes'] if c['class_index']==5)
    seed=data['continuation_seed'];raw=(ROOT/seed['path']).read_bytes();old=json.loads(raw)
    need(hashlib.sha256(raw).hexdigest()==seed['sha256'],'frozen seed hash')
    need(data['queries'][:seed['query_count']]==old['queries'],'old queries preserved byte-equivalent as records')
    charts=frontier(data,C);inputs=[]
    for number,row in enumerate(data['queries']):
        p=ROOT/row['path'];compare(formula(C,S,row),list(z3.parse_smt2_file(str(p))))
        inputs.append({'path':row['path'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        if (number+1)%100==0:print('PASS exact joint encodings: '+str(number+1),flush=True)
    wrong=deepcopy(data);wrong['queries'][0]['box'][0][1]='1/2'
    mutations=[expect_rejection('gap in root box',lambda:frontier(wrong,C))]
    wrong2=deepcopy(data);next(c for c in wrong2['charts'] if not c['complete_cover'])['complete_cover']=True
    mutations.append(expect_rejection('partial chart labelled complete',lambda:frontier(wrong2,C)))
    row=data['queries'][0];expected=formula(C,S,row);actual=list(z3.parse_smt2_file(str(ROOT/row['path'])))
    offset,gap=z3.Reals('U_offset U_gap')
    mutations.append(expect_rejection('overrestrictive offset cap',lambda:compare(expected,actual+[offset+3*gap<=1])))
    mutations.append(expect_rejection('missing U contact identity',lambda:compare(expected,actual[:-1])))
    out={'status':'PASS','query_count':len(inputs),'new_query_count':len(inputs)-seed['query_count'],
         'complete_charts':sum(c['complete_cover'] for c in charts),
         'pending_boxes':sum(c['pending_leaves'] for c in charts),
         'charts':charts,'inputs':inputs,'mutations':mutations,'solver_queries_run':0,
         'scope':'Exact encoding and closed-box frontier audit. Archived UNSAT statuses are not independently proof-checked here; no whole-class exclusion follows from a partial cover.'}
    (ROOT/'results/det5_joint_cover_encoding_validation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','query_count','new_query_count','complete_charts','pending_boxes','solver_queries_run')}))


if __name__=='__main__':main()
