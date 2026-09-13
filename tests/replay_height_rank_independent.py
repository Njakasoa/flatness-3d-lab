"""Independent rational rank data and directional counterexample replay.

No experiment, solver or geometry-core import. Continuous arguments are in
proofs/HEIGHT_RANK_AND_VOLUME.md; this checks their inputs and identities.
"""
from fractions import Fraction as Q
from itertools import permutations, combinations, product
from copy import deepcopy
from pathlib import Path
import json
from replay_det13_contraction_independent import solve,need
from replay_weighted_trace_independent import determinant,inv,trace

ROOT=Path(__file__).resolve().parents[1]
H=(0,1,1,0)


def rank(data):
    beta=Q(data['beta']);need(beta==Q(37,102),'threshold')
    need(len(data['classes'])==2,'two classes')
    controls=json.loads((ROOT/'results/directional_contraction_probe.json').read_text())
    report=[]
    for C,(idx,d,a) in zip(data['classes'],((6,7,2),(7,8,3))):
        need((C['class_index'],C['determinant'],C['residue'])==(idx,d,a),'class binding')
        P=((0,0,0),(d,1,a),(0,1,0),(0,0,1))
        A=[[Q(1)]*4]+[[Q(p[k]) for p in P] for k in range(3)]
        vectors=list(map(tuple,C['vectors']))
        need(vectors==[(1,0,0),(3,0,1),(2,0,1)],'rank triple')
        need(tuple(y-x for x,y in zip(*vectors[:2]))==vectors[2],'difference relation')
        need(abs(determinant([[Q(v[k]) for k in (0,2)] for v in vectors[:2]]))==1,'horizontal lattice basis')
        rows=[solve(A,[Q(0),*map(Q,v)]) for v in vectors]
        need(rows==[list(map(Q,r)) for r in C['difference_barycentrics']],'independent barycentrics')
        masses=[sum(map(abs,r))/2 for r in rows];M=max(masses);g=2*beta-M
        need(g>0,'strict rank margin')
        fields={'maximum_mass':M,'l1_distance_to_line_lower_bound':g,
                'complementary_minor_absolute_lower_bound':beta*g/4,
                'complementary_minor_absolute_upper_bound':masses[0]*masses[1],
                'determinant_over_height_gap_lower_bound':d*beta*g/4,
                'contact_basis_determinant':Q(1,d),
                'height_gap_volume_lower_bound':beta**3/(6*masses[0]*masses[1])}
        need(list(map(Q,C['positive_masses']))==masses,'masses')
        for name,value in fields.items():need(Q(C[name])==value,'rank constant '+name)
        c=solve(A,[Q(1),Q(0),Q(0),Q(0)]);t=solve(A,[Q(0),Q(0),Q(1),Q(0)])
        need(determinant(list(map(list,zip(rows[0],rows[1],t,c))))==Q(1,d),'basis orientation')
        model=next(r for r in controls['results'] if r['class_index']==idx)
        F=[list(map(Q,r)) for r in model['F']];T=inv(F)
        Y=[sum(Q(H[i])*T[i][j] for i in range(4)) for j in range(4)]
        span=max(Y)-min(Y);b=1/span;offset=-min(Y)/span
        q=[(y-min(Y))/span for y in Y];low=q.index(0);high=q.index(1)
        need(all(sum(F[i][j]*q[i] for i in range(4))==offset+b*H[j] for j in range(4)),'normalized height identity')
        r,s=[[sum(F[i][j]*l[j] for j in range(4)) for i in range(4)] for l in rows[:2]]
        need(all(sum(map(abs,v))/2>beta for v in (r,s,[y-x for x,y in zip(r,s)])),'control rank gauges')
        minors={(i,j):r[i]*s[j]-r[j]*s[i] for i,j in combinations(range(4),2)}
        i,j=[k for k in range(4) if k not in (low,high)];k=abs(minors[i,j])
        need(beta*g/4<=k<=masses[0]*masses[1],'control minor bounds')
        need(abs(determinant(F))==d*b*k,'control determinant-height identity')
        need(sum(map(abs,minors.values()))==k*sum(abs(q[i]-q[j]) for i,j in combinations(range(4),2)),'complementary Plucker factors')
        for factor in (Q(-2),Q(-1,3),Q(0),Q(1,4),Q(1),Q(3,2),Q(4)):
            need(sum(abs(y-factor*x) for x,y in zip(r,s))>=g,'distance-to-line control')
        report.append({'class_index':idx,'rank_gap':str(g),'minor_bounds':[str(beta*g/4),str(masses[0]*masses[1])],
                       'control_Y_width':str(span),'control_detF':str(determinant(F))})
    expected=set(permutations(range(4),2));seen=set()
    for rec in data['universal_determinant_identities']:
        low,high=rec['low'],rec['high'];need((low,high) in expected-seen,'all twelve extrema once');seen.add((low,high))
        i,j=[k for k in range(4) if k not in (low,high)];need(rec['complementary_rows']==[i,j],'complement rows')
        # det R is affine in qi,qj. These three evaluations fix every coefficient.
        for qi,qj in ((0,0),(1,0),(0,1)):
            q=[Q(0)]*4;q[high]=1;q[i]=Q(qi);q[j]=Q(qj)
            R=[[Q(int(h==i)) for h in range(4)],[Q(int(h==j)) for h in range(4)],q,[Q(1)]*4]
            need(determinant(R)==rec['signed_factor'] and abs(rec['signed_factor'])==1,'universal row-transform identity')
    need(seen==expected,'complete extrema signs')
    hx=list(map(tuple,data['hexagon_vertices']))
    need(set(hx)=={(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)},'projected norm hexagon')
    vals=[abs(x[0]*y[1]-x[1]*y[0]) for x,y in product(hx,repeat=2)]
    need(data['hexagon_determinants']==vals and max(vals)==1,'36 bilinear extreme checks')
    return report


def directional(data):
    bodies=trace(data,True)
    for R in data['results']:
        F=[list(map(Q,r)) for r in R['F']]
        need(R['height_values']==list(H) and R['height_covector']==[0,1,0],'height covector')
        checks={tuple(c['permutation']):c for c in R['matching_checks']}
        derangements={p for p in permutations(range(4)) if all(p[i]!=i for i in range(4))}
        need(set(checks)==derangements and R['derangement_count']==9,'all derangements')
        for p in permutations(range(4)):
            same=[F[p[j]][j]+F[p[k]][k] for j,k in combinations(range(4),2) if H[j]==H[k]]
            cross=[F[p[j]][j]+F[p[k]][k] for j,k in combinations(range(4),2) if H[j]!=H[k]]
            holds=min(same)>1 and min(cross)>=Q(22,17)
            need(not holds,'all 24 sufficient matchings fail')
            if p in checks:
                c=checks[p]
                need(Q(c['minimum_equal_height_sum'])==min(same) and Q(c['minimum_cross_height_sum'])==min(cross),'matching minima')
                need(c['criterion_holds']==holds,'matching conclusion')
    return bodies


def main():
    data=json.loads((ROOT/'certificates/height_rank_certificate.json').read_text())
    models=json.loads((ROOT/'results/directional_contraction_probe.json').read_text())
    result={'status':'PASS','rank':rank(data),'directional_models':directional(models)}
    mutations=[('rank',lambda d:d['classes'][0]['vectors'][2].__setitem__(0,1)),
               ('rank',lambda d:d['classes'][1].__setitem__('maximum_mass','3/7')),
               ('rank',lambda d:d['classes'][0].__setitem__('complementary_minor_absolute_lower_bound','1/10')),
               ('rank',lambda d:d['universal_determinant_identities'][0].__setitem__('signed_factor',-d['universal_determinant_identities'][0]['signed_factor'])),
               ('rank',lambda d:d['universal_determinant_identities'].pop()),
               ('directional',lambda d:d['results'][0]['matching_checks'][0].__setitem__('criterion_holds',True)),
               ('directional',lambda d:d['results'][1]['exact_body']['width']['width'].__setitem__('a','4'))]
    for kind,mutate in mutations:
        damaged=deepcopy(data if kind=='rank' else models);mutate(damaged)
        try:(rank if kind=='rank' else directional)(damaged)
        except (ValueError,KeyError,TypeError,IndexError):continue
        raise ValueError('accepted mutation: '+kind)
    result.update(rejected_mutations=len(mutations),solver_queries_run=0)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
