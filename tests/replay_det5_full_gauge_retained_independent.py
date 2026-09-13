"""Independent full-gauge rational body and retained-chart replay, using only stdlib.

No imports from discovery, geometry core, other validators, or solvers.
"""
from fractions import Fraction as Q
from itertools import product, permutations
from math import ceil, floor, gcd
from pathlib import Path
from copy import deepcopy
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]

def need(condition,message):
    if not condition: raise ValueError(message)

def inverse(A):
    n=len(A); M=[[Q(x) for x in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(A)]
    for i in range(n):
        p=next((j for j in range(i,n) if M[j][i]),None)
        need(p is not None,'invertible matrix')
        M[i],M[p]=M[p],M[i]; scale=M[i][i];M[i]=[x/scale for x in M[i]]
        for j in range(n):
            if j!=i:
                scale=M[j][i];M[j]=[x-scale*y for x,y in zip(M[j],M[i])]
    return [r[n:] for r in M]

def determinant3(A):
    return sum(A[0][i]*(A[1][(i+1)%3]*A[2][(i+2)%3]-A[1][(i+2)%3]*A[2][(i+1)%3]) for i in range(3))

def multiply(A,v):return [sum(x*y for x,y in zip(r,v)) for r in A]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def qvalue(x):
    need(Q(x['b'])==0,'rational scalar binding');return Q(x['a'])
def canon(v):return any(v) and next(x for x in v if x)>0 and gcd(*v)==1

def replay(witness,frontier):
    F=[list(map(Q,r)) for r in witness['F']]; beta=Q(183,500)
    need(len(F)==4 and all(len(r)==4 for r in F),'matrix dimensions')
    need(all(F[i][i]==0 for i in range(4)),'facet diagonal')
    need(all(F[i][j]>0 for i in range(4) for j in range(4) if i!=j),'relative facet interiors')
    need(all(sum(F[i][j] for i in range(4))==1 for j in range(4)),'stochastic columns')
    P=((0,0,0),(5,1,2),(0,1,0),(0,0,1)); Fi=inverse(F)
    V=[[sum(Q(P[i][k])*Fi[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
    archived=witness['exact_body']
    need(V==[[qvalue(x) for x in r] for r in archived['vertices']],'vertex binding')
    affine_inverse=inverse([[1]*4]+[[p[k] for p in P] for k in range(3)])
    def coords(v,affine=False):return multiply(F,multiply(affine_inverse,[Q(int(affine)),*map(Q,v)]))
    bbox=[(ceil(min(v[k] for v in V)),floor(max(v[k] for v in V))) for k in range(3)]
    count=0; boundary=[]
    for z in product(*(range(l,h+1) for l,h in bbox)):
        c=coords(z,True);count+=1;need(min(c)<=0,'hollow body')
        if min(c)==0:boundary.append(list(z))
    need(boundary==archived['hollow']['boundary_points'],'complete boundary binding')
    D=[[V[i][k]-V[0][k] for k in range(3)] for i in range(1,4)]
    volume=abs(determinant3(D))/6
    need(volume==qvalue(archived['volume']) and volume<beta**-3,'exact volume cut')
    spans=[max(v[k] for v in V)-min(v[k] for v in V) for k in range(3)]
    W=min(spans); Di=inverse(D)
    limits=[floor(W*sum(map(abs,row))) for row in Di]
    widths=[]
    for u in product(*(range(-b,b+1) for b in limits)):
        if canon(u):
            values=[dot(u,v) for v in V];widths.append((max(values)-min(values),u))
    best=min(w for w,u in widths); minimizing=[list(u) for w,u in widths if w==best]
    need(best==qvalue(archived['width']['width']),'global width binding')
    need(minimizing==archived['width']['minimizing_directions_mod_sign'],'minimizing directions')
    # Every vector with gauge <=1 belongs to K-K, hence lies in this finite box.
    gbounds=list(map(floor,spans)); gauges=[]
    for z in product(*(range(-b,b+1) for b in gbounds)):
        if canon(z):gauges.append((sum(map(abs,coords(z)))/2,z))
    minimum=min(g for g,z in gauges)
    need(minimum<1,'complete K-K box contains the minimum')
    minvec=[list(z) for g,z in gauges if g==minimum]
    # Intrinsic mass <=6/5 implies v in (6/5)(P-P), hence this exhaustive box.
    intrinsic_bounds=[6,1,2]
    finite=sorted(v for v in product(*(range(-b,b+1) for b in intrinsic_bounds))
                  if canon(v) and sum(map(abs,multiply(affine_inverse,[0,*v])))/2<=Q(6,5))
    need(len(finite)==18 and frontier['total_gauge_count']==18,'eighteen intrinsic short gauges')
    extras=set(map(tuple,frontier['extra_gauge_vectors']))
    need(len(extras)==8 and extras<=set(finite),'eight additional gauges belong to the complete eighteen')
    values={','.join(map(str,v)):str(sum(map(abs,coords(v)))/2) for v in finite}
    need(all(Q(g)>beta for g in values.values()),'all eighteen finite gauges')
    need(minimum==Q(211637,541875) and minvec==[[2,1,0]],'independent full minimum regression')
    # sqrt(4/3) > (17/5)*(1-minimum)-1 is the exact ACMS threshold check.
    threshold=Q(17,5)*(1-minimum)-1
    exact_acms=threshold<0 or threshold*threshold<Q(4,3)
    need(exact_acms,'every nonzero lattice gauge exceeds exact ACMS target threshold')
    need(volume*minimum**3<1,'stronger actual-minimum volume cut')
    directions=[];free=[]
    for name,u,ext,H,bound in [('Y',(0,1,0),[1,0],[0,1,1,0],Q(2042829,50000000)),
                              ('U',(1,-1,-2),[1,3],[2,2,1,0],Q(2042829,100000000))]:
        heights=[dot(u,v) for v in V];low=min(heights);width=max(heights)-low;gap=1/width
        q=[(h-low)*gap for h in heights]
        offset=(min(dot(u,p) for p in P)-low)*gap
        need(width>Q(17,5) and gap>bound,'two actual widths and volume-derived gaps')
        need(q[ext[0]]==0 and q[ext[1]]==1,'actual retained extrema')
        need([q.index(0),q.index(1)]==ext,'unique actual extrema')
        need(q==list(map(Q,witness['actual']['normalized_'+name])),'normalized height binding')
        need(width==Q(witness['actual'][name+'_width']),'directional width binding')
        need(all(sum(F[i][j]*q[i] for i in range(4))==offset+gap*H[j] for j in range(4)),'full bilinear height identities')
        need(offset>=0 and offset+max(H)*gap<=1,'shifted height range')
        free += [q[i] for i in range(4) if i not in ext]
        directions.append({'direction':name,'extrema':ext,'width':str(width),'gap':str(gap),'offset':str(offset),'normalized_heights':list(map(str,q))})
    chart=next(c for c in frontier['charts'] if c['Y_extrema']==[1,0] and c['U_extrema']==[1,3])
    contains=lambda box:all(Q(l)<=x<=Q(h) for x,(l,h) in zip(free,box))
    pending=[p for p in chart['pending_leaves'] if contains(p['box'])]
    need(pending and not chart['complete_cover'],'exact witness remains in pending frontier')
    # Closed leaves are bound to their archived query boxes.
    closed=[r for r in frontier['queries'] if r['Y_extrema']==[1,0] and r['U_extrema']==[1,3] and r['node'] in chart['closed_leaves']]
    need(len(closed)==len(chart['closed_leaves']),'every closed leaf has an archived query')
    need(not any(contains(r['box']) for r in closed),'witness does not inhabit a closed leaf')
    return {'vertices':[[str(x) for x in v] for v in V],'volume':str(volume),'hollow_box':bbox,
            'lattice_points_checked':count,'boundary_points':boundary,'lattice_width':str(best),
            'minimizing_directions':minimizing,'width_search_bounds':limits,'primitive_width_directions_checked':len(widths),
            'full_difference_minimum':str(minimum),'minimum_gauge_vectors':minvec,'gauge_search_bounds':gbounds,
            'primitive_gauge_vectors_checked':len(gauges),'passes_exact_ACMS_threshold':exact_acms,
            'finite_gauges':values,'intrinsic_cutoff':'6/5','intrinsic_search_bounds':intrinsic_bounds,'exact_ACMS_squared_margin':str(Q(4,3)-threshold*threshold),'volume_times_full_minimum_cubed':str(volume*minimum**3),'directional_charts':directions,'actual_free_heights':list(map(str,free)),
            'frontier_queries':len(frontier['queries']),'containing_pending_leaves':pending,'containing_closed_leaves':0}

def main():
    source=ROOT/'results/det5_joint_short_gauges.json';front=source
    witness=json.loads(source.read_text())['retained_witness'];frontier=json.loads(front.read_text())
    result=replay(witness,frontier)
    for mutation in ('matrix','width','normalized_height','pending_box','boundary','volume'):
        w,f=deepcopy(witness),deepcopy(frontier)
        if mutation=='matrix':w['F'][0][1]='0'
        elif mutation=='width':w['exact_body']['width']['width']['a']='4'
        elif mutation=='normalized_height':w['actual']['normalized_U'][0]='0'
        elif mutation=='boundary':w['exact_body']['hollow']['boundary_points']=[]
        elif mutation=='volume':w['exact_body']['volume']['a']='100'
        else:
            c=next(c for c in f['charts'] if c['Y_extrema']==[1,0] and c['U_extrema']==[1,3]);c['pending_leaves']=[]
        try:replay(w,f)
        except ValueError:continue
        raise ValueError('accepted mutation '+mutation)
    record={'status':'PASS','scope':'Actual hollow rational body occupies a retained normalized Y/U chart, exceeds the exact ACMS target threshold for every nonzero lattice gauge, and satisfies volume cuts. It disproves infeasibility of Y/U-only plus these global-gauge and volume necessities, but has small global lattice width and does not challenge the flatness conjecture.',
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'frontier_sha256':hashlib.sha256(front.read_bytes()).hexdigest(),
            'solver_queries_run':0,'rejected_mutations':6,'witness':result}
    (ROOT/'results/det5_full_gauge_retained_validation.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))
if __name__=='__main__':main()
