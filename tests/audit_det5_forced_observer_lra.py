"""Independent exact audit of two forced-observer SAT inputs and actual bodies.

No solver queries. Reconstructs the matrix model from physical contacts,
then uses only rational arithmetic for the saved bodies and lattice boxes.
"""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from math import ceil,floor,gcd
from pathlib import Path
import json
import re
import sympy as s
import z3
from audit_det5_quadratic_chart_independent import as_z3,forms
from replay_det5_full_gauge_retained_independent import inverse,multiply,dot,need
from replay_det5_conditional_width_bounds import parse,poly

ROOT=Path(__file__).resolve().parents[1]
CONTACTS=((0,0,0),(5,1,2),(0,1,0),(0,0,1))
VECTORS=((0,0,1),(0,1,-1),(0,1,0),(1,0,0),(1,0,1),(2,0,1),
         (3,0,1),(5,0,2),(5,1,1),(5,1,2),(1,-1,1))
GUARDS='certificates/nonunimodular_observer_guards.json'
OUT='results/det5_forced_observer_lra_validation.json'


def sha(path):return sha256((ROOT/path).read_bytes()).hexdigest()
def read(path):return json.loads((ROOT/path).read_text())

def scalar(text):
    value=parse(text);need(len(value)==1,'single rational expression')
    constant=poly(value[0]);need(set(constant)<={''},'rational assignment')
    return constant.get('',Q(0))


def reconstruct(order,guard_points,beta=s.Rational(183,500),facet=None):
    P=s.Matrix([[1]*4]+[[v[k] for v in CONTACTS] for k in range(3)])
    need(abs(P.det())==5,'physical contact determinant')
    inv=P.inv()
    F=s.Matrix(4,4,lambda i,j:0 if i==j else s.Symbol(f'F_{i}_{j}'))
    expected=[as_z3(F[i,j])>0 for i in range(4) for j in range(4) if i!=j]
    expected += [as_z3(sum(F[i,j] for i in range(4)))==1 for j in range(4)]
    for v in VECTORS:
        image=F*inv*s.Matrix([0,*v])
        expected.append(z3.Or(*[as_z3(sum(image[i] for i in range(4) if mask&(1<<i)))>as_z3(beta) for mask in range(1,15)]))
    for point in guard_points:
        image=F*inv*s.Matrix([1,*point])
        expected.append(z3.Or(*[as_z3(value)<=0 for value in image]))
    chosen=(1 if order=='lt' else 2) if facet is None else facet
    for point,index in (((2,1,1),chosen),((3,1,1),0)):
        image=F*inv*s.Matrix([1,*point])
        expected.append(as_z3(image[index])<=0)
    return expected


def complete_directions():
    # Width of the integral contact hull is an integer. If it is <=3, then
    # |b|,|c|,|5a+b+2c|<=3, hence |5a|<=12 and |a|<=2.
    result=[]
    for v in product(range(-2,3),range(-3,4),range(-3,4)):
        if not any(v) or gcd(*v)!=1 or next(x for x in v if x)<0:continue
        heights=[dot(v,p) for p in CONTACTS]
        if max(heights)-min(heights)<=3:result.append(v)
    need(len(result)==15,'complete fifteen primitive contact widths below four')
    return sorted(result)


def actual_body(values,order,guard_points,directions):
    F=[[Q(0) if i==j else values[f'F_{i}_{j}'] for j in range(4)] for i in range(4)]
    need(all(F[i][j]>0 for i in range(4) for j in range(4) if i!=j),'strict contact matrix')
    need(all(sum(F[i][j] for i in range(4))==1 for j in range(4)),'stochastic columns')
    fi=inverse(F)
    vertices=[[sum(Q(CONTACTS[i][k])*fi[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
    for j in range(4):
        need([sum(F[i][j]*vertices[i][k] for i in range(4)) for k in range(3)]==list(CONTACTS[j]),'reconstructed relint facet contacts')
    affine=inverse([[1]*4]+[[p[k] for p in CONTACTS] for k in range(3)])
    def coordinates(v,point=False):return multiply(F,multiply(affine,[Q(int(point)),*v]))
    bbox=[[ceil(min(v[k] for v in vertices)),floor(max(v[k] for v in vertices))] for k in range(3)]
    interior=[];boundary=[];count=0
    for point in product(*(range(lo,hi+1) for lo,hi in bbox)):
        co=coordinates(point,True);count+=1
        if min(co)>0:interior.append(list(point))
        elif min(co)==0:boundary.append(list(point))
    widths=[]
    for direction in directions:
        projected=[dot(direction,v) for v in vertices]
        widths.append({'direction':list(direction),'width':str(max(projected)-min(projected))})
    best=min(Q(v['width']) for v in widths)
    need(best<4,'finite short-contact directions attain full lattice width')
    yh=[v[1] for v in vertices];wy=max(yh)-min(yh);q=[(h-min(yh))/wy for h in yh]
    mins=[i for i,v in enumerate(q) if v==0];maxs=[i for i,v in enumerate(q) if v==1]
    gauges=[{'direction':list(v),'gauge':str(sum(map(abs,coordinates(v)))/2)} for v in VECTORS]
    need(all(Q(g['gauge'])>Q(183,500) for g in gauges),'eleven actual selected gauges')
    guards=[{'point':list(v),'barycentric':list(map(str,coordinates(v,True)))} for v in guard_points]
    need(all(min(map(Q,g['barycentric']))<=0 for g in guards),'twenty actual guard necessities')
    first=1 if order=='lt' else 2
    forced=[{'point':[2,1,1],'facet':first,'value':str(coordinates((2,1,1),True)[first])},
            {'point':[3,1,1],'facet':0,'value':str(coordinates((3,1,1),True)[0])}]
    need(all(Q(v['value'])<=0 for v in forced),'actual forced facets')
    return {'F':[[str(v) for v in row] for row in F],
            'vertices':[[str(v) for v in row] for row in vertices],
            'relative_facet_contacts':True,'hollow':not interior,'integer_bbox':bbox,
            'lattice_points_checked':count,'interior_lattice_points':interior,'boundary_lattice_points':boundary,
            'actual_Y_heights':list(map(str,yh)),'actual_normalized_Y':list(map(str,q)),
            'actual_Y_minimizer_indices':mins,'actual_Y_maximizer_indices':maxs,
            'actual_Y_width':str(wy),'actual_Y_width_exceeds_17_5':wy>Q(17,5),
            'actual_Y_chart_0_3':0 in mins and 3 in maxs,
            'eleven_gauges':gauges,'twenty_guards':guards,'forced_facet_values':forced,
            'fifteen_complete_direction_widths':widths,'full_lattice_width':str(best),
            'minimizing_directions_mod_sign':[v['direction'] for v in widths if Q(v['width'])==best],
            'width_completeness':'All other primitive integral covectors have contact-hull width at least4; inclusion of the contact hull gives body width at least4 in them. The displayed minimum is below4.',
            'qualifying_actual_target_counterexample':not interior and 0 in mins and 3 in maxs and best>Q(17,5)}


def main():
    C=next(c for c in read(GUARDS)['classes'] if c['class_index']==5)
    need(C['contact_points']==list(map(list,CONTACTS)),'guard source contact labels')
    need(len(C['guards'])==len(set(map(tuple,C['guards'])))==20,'twenty unique guard points')
    directions=complete_directions();bodies=[]
    for order in ('lt','gt'):
        path=f'results/det5_forced_observer_lra_{order}.json';row=read(path)
        need(row['status']=='sat' and row['order']==order and row['target']=='17/5' and row['beta']=='183/500','source metadata')
        need(row['gauge_vectors']==list(map(list,VECTORS)),'exact eleven physical gauges')
        need(row['forced_observers']==[{'point':[2,1,1],'facet':1 if order=='lt' else 2},{'point':[3,1,1],'facet':0}],'forced physical observer facets')
        text=(ROOT/row['input_path']).read_text();need(sha(row['input_path'])==row['input_sha256'],'input hash')
        actual=list(z3.parse_smt2_string(text));expected=reconstruct(order,C['guards'])
        names={f'F_{i}_{j}' for i in range(4) for j in range(4) if i!=j}
        declared=re.findall(r'\(declare-fun\s+(\S+)\s+\(\)\s+Real\)',text)
        need(len(declared)==12 and set(declared)==names and set(row['assignment'])==names,'twelve exact matrix variables')
        need(len(actual)==len(expected)==49 and forms(actual)==forms(expected),'independent full49-assertion reconstruction')
        need(forms(actual)!=forms(expected[:-1]),'missing forced facet mutation rejected')
        need(forms(actual)!=forms(reconstruct(order,C['guards'],facet=2 if order=='lt' else 1)),'wrong forced facet mutation rejected')
        need(forms(actual)!=forms(reconstruct(order,C['guards'],beta=s.Rational(37,102))),'weakened gauge mutation rejected')
        values={name:scalar(value) for name,value in row['assignment'].items()}
        bindings=[(z3.Real(name),z3.RealVal(str(value))) for name,value in values.items()]
        need(all(z3.is_true(z3.simplify(z3.substitute(atom,*bindings))) for atom in actual),'all49 saved assertions exactly true')
        body=actual_body(values,order,C['guards'],directions)
        body.update(source_path=path,source_sha256=sha(path),source_order=order,input_path=row['input_path'],input_sha256=row['input_sha256'],
                    assertions_audited=49,assignment_assertions_exactly_true=49,
                    mutation_controls_rejected=['missing forced facet','wrong forced facet','weakened gauge'])
        bodies.append(body)
    result={'status':'PASS','scope':'Independent exact input and rational actual-body audit of two necessary matrix-relaxation SAT assignments. Neither order label is treated as an actual Y chart; no actual large-width existence follows from SAT.',
            'guard_source':{'path':GUARDS,'sha256':sha(GUARDS)},'complete_width_directions':list(map(list,directions)),
            'bodies':bodies,'qualifying_actual_target_counterexamples':sum(v['qualifying_actual_target_counterexample'] for v in bodies),
            'solver_queries_run':0,'new_models_generated':0,'full_lattice_gauge_minimum_computed':False}
    destination=ROOT/OUT
    if destination.exists():need(read(OUT)==result,'existing audit differs; no overwrite')
    else:destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','bodies':[{'order':b['source_order'],'hollow':b['hollow'],'lattice_points_checked':b['lattice_points_checked'],
       'Y_min':b['actual_Y_minimizer_indices'],'Y_max':b['actual_Y_maximizer_indices'],'Y_width':b['actual_Y_width'],
       'full_lattice_width':b['full_lattice_width'],'qualifies':b['qualifying_actual_target_counterexample']} for b in bodies]},indent=2))


if __name__=='__main__':main()
