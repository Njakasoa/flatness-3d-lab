"""New pending joint boxes with proved linear volume-gap cuts.

Every relaxed SAT matrix is also inspected as a possible actual hollow body.
Old archives are immutable and no recorded query is re-run.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import permutations
import argparse,hashlib,json,time
import z3
from experiments.det5_joint_height_interval import make,U
from experiments.det5_height_fiber_witness import inverse
from experiments.contact_contraction_trace_probe import certify

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'results/det5_joint_round2.json'
ARCHIVE=ROOT/'results/det5_joint_volume_gaps.json'
PATH_PREFIX='det5_joint_gap'
Y_GAP=Q(2042829,50000000)
U_GAP=Q(2042829,100000000)


def gap_make(C,S,Yext,Uext,box):
    solver,F,q,r,a,b,offset,gap=make(C,S,Yext,Uext,box)
    solver.add(b>z3.RealVal(str(Y_GAP)),gap>z3.RealVal(str(U_GAP)))
    return solver,F,q,r,a,b,offset,gap


def inspect_matrix(matrix,P):
    try:T=inverse(matrix)
    except ValueError:return {'invertible':False}
    V=[[sum(Q(P[i][k])*T[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
    Y=[v[1] for v in V];H=[sum(u*x for u,x in zip(U,v)) for v in V]
    wy,wu=max(Y)-min(Y),max(H)-min(H)
    ye=[[i,j] for i,j in permutations(range(4),2) if Y[i]==min(Y) and Y[j]==max(Y)]
    ue=[[i,j] for i,j in permutations(range(4),2) if H[i]==min(H) and H[j]==max(H)]
    normalizedY=[(v-min(Y))/wy for v in Y];normalizedU=[(v-min(H))/wu for v in H]
    out={'invertible':True,'Y_width':str(wy),'U_width':str(wu),'Y_extrema':ye,'U_extrema':ue,
         'normalized_Y':list(map(str,normalizedY)),'normalized_U':list(map(str,normalizedU)),
         'actual_gaps_pass':1/wy>Y_GAP and 1/wu>U_GAP,
         'retained_Y_extrema':[e for e in ye if e in ([0,1],[0,3],[1,0])]}
    out['both_wide_retained']=wy>Q(17,5) and wu>Q(17,5) and bool(out['retained_Y_extrema']) and out['actual_gaps_pass']
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--max-new-nodes-per-chart',type=int,default=8)
    args=parser.parse_args();raw=SOURCE.read_bytes();digest=hashlib.sha256(raw).hexdigest()
    C=next(c for c in json.loads((ROOT/'certificates/nonunimodular_observer_guards.json').read_text())['classes'] if c['class_index']==5)
    S=next(c for c in json.loads((ROOT/'results/two_vector_class_scan.json').read_text())['classes'] if c['class_index']==5)
    if ARCHIVE.exists():
        data=json.loads(ARCHIVE.read_text())
        if data['volume_gap_seed']['sha256']!=digest:raise ValueError('seed changed')
        if data.get('retained_witness'):print('Witness already stored; no new query');return
    else:
        data=json.loads(raw)
        data['volume_gap_seed']={'path':str(SOURCE.relative_to(ROOT)),'sha256':digest,'query_count':len(data['queries'])}
        data['linear_volume_gap_cuts']={'Y':str(Y_GAP),'U':str(U_GAP),'proof':'proofs/DET5_VOLUME_GAP_BOUNDS.md'}
    def save():ARCHIVE.write_text(json.dumps(data,indent=2)+'\n')
    for chart in data['charts']:
        calls=0;ye,ue=chart['Y_extrema'],chart['U_extrema']
        while chart['pending_leaves'] and calls<args.max_new_nodes_per_chart:
            pending=chart['pending_leaves'][0];node=pending['node'];box=[[Q(x) for x in p] for p in pending['box']]
            if any(r['Y_extrema']==ye and r['U_extrema']==ue and r['node']==node for r in data['queries']):raise ValueError('Repeated node')
            solver,F,q,r,a,b,o,g=gap_make(C,S,ye,ue,box)
            path=f'results/{PATH_PREFIX}_{ye[0]}_{ye[1]}_{ue[0]}_{ue[1]}_{node}.smt2'
            smt=solver.to_smt2().encode();(ROOT/path).write_bytes(smt)
            start=time.monotonic();status=solver.check()
            row={'Y_extrema':ye,'U_extrema':ue,'node':node,'box':pending['box'],'path':path,
                 'input_sha256':hashlib.sha256(smt).hexdigest(),'status':str(status),'timeout_ms':1000,
                 'elapsed_seconds':time.monotonic()-start,'volume_gap_cuts':True}
            chart['pending_leaves'].pop(0);chart['queries']+=1;calls+=1
            if status==z3.unsat:chart['closed_leaves'].append(node)
            else:
                if status==z3.unknown:row['reason_unknown']=solver.reason_unknown()
                axis=max(range(4),key=lambda i:box[i][1]-box[i][0]);l,h=box[axis];mid=(l+h)/2
                for suffix,pair in [('0',[l,mid]),('1',[mid,h])]:
                    child=[list(p) for p in box];child[axis]=pair
                    chart['pending_leaves'].append({'node':node+suffix,'box':[[str(x) for x in p] for p in child]})
            chart['complete_cover']=not chart['pending_leaves'];data['queries'].append(row)
            if status==z3.sat:
                model=solver.model();val=lambda x:model.eval(x,model_completion=True).as_fraction()
                matrix=[[val(x) for x in line] for line in F]
                row['F']=[[str(x) for x in line] for line in matrix]
                row['relaxed_Y_gap']=str(val(b));row['relaxed_U_gap']=str(val(g))
                save() # Preserve raw assignment before any reconstruction.
                row['actual_matrix']=inspect_matrix(matrix,C['contact_points'])
                if row['actual_matrix']['both_wide_retained']:
                    data['retained_witness']={'path':path,'F':row['F'],'actual':row['actual_matrix']}
                    save()
                    data['retained_witness']['exact_body']=certify(matrix,C['contact_points'])
                    save();print('Retained exact both-wide matrix found: '+path,flush=True)
                    return
            save()
        print(json.dumps({'Y':ye,'U':ue,'queries':chart['queries'],'closed':len(chart['closed_leaves']),
                          'pending':len(chart['pending_leaves']),'complete':chart['complete_cover']}),flush=True)
    if SOURCE.read_bytes()!=raw:raise ValueError('Prior archive modified')


if __name__=='__main__':main()
