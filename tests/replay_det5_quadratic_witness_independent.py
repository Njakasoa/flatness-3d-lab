"""Independent stdlib exact replay of the saved eight-parameter SAT body.

No discovery imports or solver calls. Exhaustive integer boxes certify hollow
geometry and the full difference-body first minimum, including tied extrema.
"""
from fractions import Fraction as Q
from itertools import product
from math import ceil, floor, gcd
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
P=((0,0,0),(5,1,2),(0,1,0),(0,0,1))
VECTORS=((0,0,1),(0,1,-1),(0,1,0),(1,0,0),(1,0,1),(2,0,1),(3,0,1),(5,0,2),(5,1,1),(5,1,2))

def need(ok,msg):
    if not ok: raise ValueError(msg)

def scalar(s):
    tokens=re.findall(r'\(|\)|[^\s()]+',s)
    def read():
        t=tokens.pop(0)
        if t!='(':return Q(t)
        op=tokens.pop(0);a=[]
        while tokens[0]!=')':a.append(read())
        tokens.pop(0)
        if op=='/':return a[0]/a[1]
        if op=='-':return -a[0] if len(a)==1 else a[0]-a[1]
        raise ValueError('nonrational scalar')
    out=read();need(not tokens,'scalar trailing tokens');return out

def inverse(A):
    n=len(A);M=[[Q(v) for v in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(A)]
    for i in range(n):
        k=next((k for k in range(i,n) if M[k][i]),None);need(k is not None,'invertible matrix')
        M[i],M[k]=M[k],M[i];s=M[i][i];M[i]=[v/s for v in M[i]]
        for k in range(n):
            if k!=i:
                s=M[k][i];M[k]=[a-s*b for a,b in zip(M[k],M[i])]
    return [row[n:] for row in M]

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mv(A,v):return [dot(r,v) for r in A]
def canon(v):return any(v) and next(x for x in v if x)>0 and gcd(*v)==1

def main():
    path=ROOT/'results/det5_quadratic_height_chart.json';source=json.loads(path.read_text())
    row=next(r for r in source['queries'] if r['order']=='lt');need(row['status']=='sat','saved rational SAT')
    need(hashlib.sha256((ROOT/row['input_path']).read_bytes()).hexdigest()==row['input_sha256'],'input binding')
    v={k:scalar(s) for k,s in row['assignment'].items()};x,y,t,c,e,r,u,h=(v[k] for k in ('low','high','theta','c','e','r','u','h'))
    d=y-x
    # Reconstruct columns directly from barycentric constraints, independently
    # of the discovery matrix function.
    cols=[(Q(0),1-t+(1-y)*c,t-(1-x)*c,d*c),
          (1-h-(1-y)*r,Q(0),r,h-y*r),
          (1-h-(1-x)*u,u,Q(0),h-x*u),
          (d*e,1-t-y*e,t+x*e,Q(0))]
    F=[list(row) for row in zip(*cols)]
    need(all(sum(col)==1 for col in cols),'stochastic columns')
    need(all(F[i][j]>0 for i in range(4) for j in range(4) if i!=j),'strict facet contacts')
    fi=inverse(F);vertices=[[sum(Q(P[i][k])*fi[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
    for j in range(4):need([sum(F[i][j]*vertices[i][k] for i in range(4)) for k in range(3)]==list(P[j]),'actual contacts')
    affine=inverse([[1]*4]+[[p[k] for p in P] for k in range(3)])
    def coords(z,point=False):return mv(F,mv(affine,[Q(int(point)),*map(Q,z)]))
    def gauge(z):return sum(map(abs,coords(z)))/2
    bbox=[[ceil(min(z[k] for z in vertices)),floor(max(z[k] for z in vertices))] for k in range(3)]
    interior=[];boundary=[];count=0
    for z in product(*(range(lo,hi+1) for lo,hi in bbox)):
        co=coords(z,True);count+=1
        if min(co)>0:interior.append(list(z))
        elif min(co)==0:boundary.append(list(z))
    need(not interior,'actual body hollow')
    heights=[z[1] for z in vertices];width=max(heights)-min(heights);q=[(z-min(heights))/width for z in heights]
    offset=-min(heights)/width;gap=1/width
    need(q==[0,x,y,1] and gap==h-x-t*d and offset==x+t*d,'exact chart restoration')
    need(width>Q(17,5),'actual Y width target')
    mins=[i for i,z in enumerate(q) if z==0];maxs=[i for i,z in enumerate(q) if z==1]
    need(0 in mins and 3 in maxs,'Y[0,3] possibly tied extrema')
    for j in range(4):need(sum(q[i]*F[i][j] for i in range(4))==offset+gap*P[j][1],'height contact identity')
    boxes=row['excluded_rectangles'];outside=[]
    for box in boxes:
        literals=[q[i]<Q(lo) or q[i]>Q(hi) for i,(lo,hi) in zip((1,2),box)]
        need(any(literals),'strict certified complement');outside.append(literals)
    bound_paths=['results/det5_class5_y_cvc5_validation.json','results/det5_y_corner_enlarged_3_5.json']
    old,new=[json.loads((ROOT/p).read_text()) for p in bound_paths]
    need(boxes==[r['box'] for r in old['leaves'] if r['extrema']==[0,3]]+[new['box']],'certified rectangles bound')
    gauges=[{'vector':list(z),'gauge':str(gauge(z))} for z in VECTORS]
    need(sorted(map(tuple,row['gauge_vectors']))==sorted(VECTORS),'ten vector binding')
    need(all(Q(g['gauge'])>Q(37,102) for g in gauges),'ten weak gauges')
    # Every direction of P-width <=3 has |b|,|c|<=3 and |5a+b+2c|<=3,
    # hence |a|<=12/5. A [-3,3]^3 enumeration is exhaustive.
    directions=[]
    for z in product(range(-3,4),repeat=3):
        if canon(z) and max(dot(z,p) for p in P)-min(dot(z,p) for p in P)<=3:directions.append(z)
    need(len(directions)==15,'complete fifteen primitive widths of P below four')
    widths=[{'direction':list(z),'width':str(max(dot(z,p) for p in vertices)-min(dot(z,p) for p in vertices))} for z in directions]
    global_width=min(Q(w['width']) for w in widths);need(global_width<4,'contact-hull lower bound completes global width')
    spans=[max(p[k] for p in vertices)-min(p[k] for p in vertices) for k in range(3)]
    gbounds=list(map(floor,spans));allgauges=[(gauge(z),z) for z in product(*(range(-b,b+1) for b in gbounds)) if canon(z)]
    minimum=min(g for g,z in allgauges);need(minimum<1,'full gauge enumeration complete below one')
    # Any lattice vector of gauge <=1 is in K-K, so each coordinate is
    # bounded by the corresponding span. Nonprimitive vectors cannot improve.
    threshold=Q(17,5)*(1-minimum)-1
    exactpass=threshold<0 or threshold*threshold<Q(4,3)
    output={'status':'PASS','scope':'Exact actual rational hollow body in Y[0,3] with possible tied extrema; no relaxed products, no solver calls. Full lattice width and full first minimum certified by exhaustive finite arguments.',
       'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'input_sha256':row['input_sha256'],
       'certified_rectangle_source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in bound_paths},
       'parameters':{k:str(z) for k,z in v.items()},'F':[[str(z) for z in row] for row in F], 'F_invertible':True,'strict_facet_contacts':True,
       'vertices':[[str(z) for z in row] for row in vertices],'hollow':True,'integer_bbox':bbox,'lattice_points_checked':count,'boundary_points':boundary,
       'Y_normalized_heights':list(map(str,q)),'Y_gap':str(gap),'Y_offset':str(offset),'Y_minimizer_indices':mins,'Y_maximizer_indices':maxs,
       'Y_width':str(width),'Y_width_exceeds_17_5':True,'actual_chart_equals_saved':True,'strict_rectangle_complement_checks':outside,
       'ten_gauges':gauges,'all_ten_exceed_37_102':True,'all_ten_exceed_183_500':all(Q(g['gauge'])>Q(183,500) for g in gauges),
       'fifteen_complete_direction_widths':widths,'global_lattice_width':str(global_width),'width_minimizers_mod_sign':[w['direction'] for w in widths if Q(w['width'])==global_width],
       'full_difference_minimum':str(minimum),'minimum_gauge_vectors_mod_sign':[list(z) for g,z in allgauges if g==minimum],
       'gauge_integer_box_bounds':gbounds,'primitive_gauge_vectors_checked':len(allgauges),'full_minimum_exceeds_37_102':minimum>Q(37,102),
       'full_minimum_exceeds_183_500':minimum>Q(183,500),'full_minimum_exceeds_exact_ACMS_17_5_threshold':exactpass,
       'exact_ACMS_comparison_rational':str(threshold),'exact_ACMS_squared_margin':str(Q(4,3)-threshold*threshold),'solver_queries_run':0}
    out=ROOT/'results/det5_quadratic_witness_validation.json'
    if out.exists():need(json.loads(out.read_text())==output,'receipt unchanged')
    else:out.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:output[k] for k in ('status','hollow','Y_minimizer_indices','Y_maximizer_indices','Y_width','global_lattice_width','full_difference_minimum','minimum_gauge_vectors_mod_sign','full_minimum_exceeds_exact_ACMS_17_5_threshold','primitive_gauge_vectors_checked')},indent=2))

if __name__=='__main__':main()
