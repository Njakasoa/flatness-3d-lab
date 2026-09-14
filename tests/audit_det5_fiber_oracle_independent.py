"""Independent fixed-shape LRA and fixed-height anchor audit; no solver calls.

Expected formulas come from column elimination and the invariant 3-space
adjugate, not the compiler or its sparse coefficient certificate. The compiler
is imported only as the object of explicit in-memory mutation/flag fixtures.
"""
from fractions import Fraction as Q
from itertools import product
from math import gcd
from pathlib import Path
import hashlib,json,re,sys
import sympy as s
import z3
from audit_det5_quadratic_chart_independent import eliminated,as_z3,forms as raw_forms
import replay_det5_conditional_width_bounds as oldproof
ROOT=Path(__file__).resolve().parents[1]
VECTORS=[(0,0,1),(0,1,-1),(0,1,0),(1,0,0),(1,0,1),(2,0,1),
         (3,0,1),(5,0,2),(5,1,1),(5,1,2),(1,-1,1)]
SHAPE=('low','high','c','e','r','u')
P=s.Matrix([[1,1,1,1],[0,5,0,0],[0,1,1,0],[0,2,0,1]])
PINV=P.inv()
B=s.Matrix([[-1,-1,-1],[1,0,0],[0,1,0],[0,0,1]])

def forms(expressions):
    # Z3 serialization can omit a trailing tautology. Its multiplicity has no semantic effect.
    return raw_forms([v for v in expressions if not z3.is_true(z3.simplify(v))])

def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def need(v,m):
    if not v:raise ValueError(m)

def source_geometry():
    C=next(v for v in read('certificates/nonunimodular_observer_guards.json')['classes'] if v['class_index']==5)
    need(C['contact_points']==[[0,0,0],[5,1,2],[0,1,0],[0,0,1]],'contact geometry')
    need(len(C['guards'])==len(set(map(tuple,C['guards'])))==20,'twenty distinct guards')
    old=read('results/det5_class5_y_cvc5_validation.json')
    leaves=[r for r in old['leaves'] if r['extrema']==[0,3]]+[read('results/det5_y_corner_enlarged_3_5.json')]
    need(len(leaves)==8,'all eight rectangles')
    bindings=[oldproof.audit_row(C,r,[0,3],r['box'],Q(37,102)) for r in leaves]
    boxes=[r['box'] for r in leaves]
    directions=[]
    # Width(P,v)<=3 implies |v_y|,|v_z|<=3 and |5v_x+v_y+2v_z|<=3,
    # hence |v_x|<=12/5, so this box exhausts all relevant directions.
    for v in product(range(-2,3),range(-3,4),range(-3,4)):
        if not any(v) or gcd(*v)!=1 or next(x for x in v if x)<0:continue
        heights=list((s.Matrix([[0,*v]])*P))
        if max(heights)-min(heights)<=3:directions.append(v)
    need(len(directions)==15,'complete fifteen primitive covectors')
    need(directions==list(map(tuple,read('results/det5_complete_geometry_validation.json')['directions'])),'stored direction list')
    return C,boxes,directions,bindings


def direct_fiber(shape,order,beta,full_width,volume_cuts,C,boxes,directions):
    values,F,q,a,b=eliminated(order)
    x,y,t,c,e,r,u,h=values
    shape=tuple(s.Rational(v) for v in shape)
    xv,yv,cv,ev,rv,uv=shape
    need(order in ('lt','gt') and 0<=xv<yv<=1 and min(cv,ev,rv,uv)>0,'admissible shape')
    fixed=dict(zip((x,y,c,e,r,u),shape))
    D=s.factor(uv*((1-xv)*cv+xv*ev)-rv*((1-yv)*cv+yv*ev))
    need(D!=0,'nonsingular horizontal determinant')
    T,H,R=s.symbols('alpha eta rho')
    def scale(expression):
        return s.expand(s.cancel(R*expression.subs(fixed).subs({t:T/R,h:H/R})))
    M=F.applyfunc(scale)
    A,E,Rho=map(as_z3,(T,H,R))
    expected=[E-as_z3(xv)*Rho-as_z3(yv-xv)*A==1,Rho>0,A>0,A<Rho,Rho>z3.RealVal('17/5')]
    expected.extend(as_z3(M[i,j])>0 for i in range(4) for j in range(4) if i!=j)
    for v in VECTORS:
        image=M*PINV*s.Matrix([0,*v])
        expected.append(z3.Or(*[as_z3(sum(image[i] for i in range(4) if mask&(1<<i)))>as_z3(s.Rational(beta))*Rho for mask in range(1,15)]))
    for point in C['guards']:
        image=M*PINV*s.Matrix([1,*point])
        expected.append(z3.Or(*[as_z3(v)<=0 for v in image]))
    for box in boxes:
        actualheights=[xv,yv] if order=='lt' else [yv,xv]
        expected.append(z3.BoolVal(any(value<s.Rational(lo) or value>s.Rational(hi) for value,(lo,hi) in zip(actualheights,box))))
    # Work on invariant U={sum coordinates=0}; no sparse certificate decoding.
    G=(F*B)[1:4,:]
    N=P[1:,:]*B*G.adjugate()
    numerators={}
    for i in range(4):
        for j in range(i):
            pair=s.zeros(4,1);pair[i]=1;pair[j]=-1
            vector=N*pair[1:4,:]
            for k in range(3):numerators[k,i,j]=scale(vector[k])
    if full_width:
        for v in directions:
            if v==(0,1,0):continue
            gaps=[sum(v[k]*numerators[k,i,j] for k in range(3)) for i in range(4) for j in range(i)]
            expected.append(z3.Or(*[cut for g in gaps for cut in (5*as_z3(g)>as_z3(17*abs(D)),-5*as_z3(g)>as_z3(17*abs(D)))]))
    if volume_cuts:
        need(full_width,'volume requires global width target')
        Rmax=s.Rational(6,5)/s.Rational(183,500)**3
        need(Rmax==s.Rational(50000000,2042829),'volume constant')
        expected.extend([Rho<as_z3(Rmax),E>0,E<Rho,Rho<as_z3(Rmax*abs(D))])
    return expected,D,M,numerators


def audit_coefficients(shape,order,D,M,numerators):
    certificate=read('certificates/det5_horizontal_fiber_structure.json')
    need(certificate['horizontal_variables']==list(SHAPE),'coefficient variable order')
    branches=certificate['branches']
    need(len(branches)==2 and {b['order'] for b in branches}=={'lt','gt'},'both unique coefficient branches')
    branch=next(v for v in branches if v['order']==order)
    def decode(terms):
        result=0
        for row in terms:
            powers=row['powers']
            need(len(powers)==6 and all(type(v)==int and v>=0 for v in powers),'all monomial powers')
            result+=s.Rational(row['coefficient'])*s.prod(s.Rational(v)**k for v,k in zip(shape,powers))
        return result
    need(decode(certificate['horizontal_determinant'])==D,'decoded determinant')
    def affine(row):return sum(decode(row[name])*s.Symbol(var) for name,var in [('alpha','alpha'),('eta','eta'),('rho','rho')])
    entries=branch['scaled_F_entries'];pairs=branch['coordinate_pair_numerators']
    need(len(entries)==16 and {(v['row'],v['column']) for v in entries}==set(product(range(4),repeat=2)),'sixteen coefficient entries')
    need(len(pairs)==18 and {(v['coordinate'],*v['vertex_pair']) for v in pairs}==set(numerators),'eighteen coefficient pairs')
    for row in entries:need(s.expand(affine(row)-M[row['row'],row['column']])==0,'matrix coefficient value')
    for row in pairs:need(s.expand(affine(row)-numerators[row['coordinate'],*row['vertex_pair']])==0,'pair coefficient value')


def audit_anchor(C,boxes):
    row=read('results/det5_fiber_anchor.json')
    values,F,q,a,b=eliminated('lt')
    x,y,t,c,e,r,u,h=values
    fixed={x:0,y:s.Rational(1,8)}
    X,Y,T,Cc,E,R,U,H=map(as_z3,values)
    expected=[X>=0,Y<=1,X<Y,T>0,T<1,Cc>0,E>0,as_z3(b)>0,as_z3(b)<z3.RealVal('5/17')]
    expected.extend(as_z3(F[i,j])>0 for i in range(4) for j in range(4) if i!=j)
    for v in sorted(VECTORS):
        image=F*PINV*s.Matrix([0,*v])
        if v==(0,0,1):expected.append(as_z3(image[0]+image[2])>z3.RealVal('183/500'))
        else:expected.append(z3.Or(*[as_z3(sum(image[i] for i in range(4) if mask&(1<<i)))>z3.RealVal('183/500') for mask in range(1,15)]))
    for point in C['guards']:
        image=F*PINV*s.Matrix([1,*point])
        expected.append(z3.Or(*[as_z3(v)<=0 for v in image]))
    for box in boxes:
        expected.append(z3.Or(*[cut for i,(lo,hi) in zip((1,2),box) for cut in (as_z3(q[i])<z3.RealVal(lo),as_z3(q[i])>z3.RealVal(hi))]))
    expected=[z3.simplify(z3.substitute(v,(X,z3.RealVal(0)),(Y,z3.RealVal('1/8')))) for v in expected]
    raw=(ROOT/row['input_path']).read_text();actual=list(z3.parse_smt2_string(raw))
    need(row['input_sha256']==sha(row['input_path']),'anchor input hash')
    need(row['fixed_heights']==['0','1/8'] and row['order']=='lt' and row['beta']=='183/500' and row['target']=='17/5','anchor parameters')
    need(row['gauge_vectors']==[list(v) for v in sorted(VECTORS)] and row['excluded_rectangles']==boxes,'anchor all directions and rectangles')
    need(forms(actual)==forms(expected),'entire independent fixed-height formula')
    declarations=re.findall(r'\(declare-fun\s+(\S+)\s+\(\)\s+Real\)',raw)
    need(len(declarations)==6 and set(declarations)=={'theta','c','e','r','u','h'},'six actual anchor variables')
    need(forms(actual)!=forms(expected[:21]+expected[22:]),'missing anchor gauge rejected')
    return {'input_path':row['input_path'],'input_sha256':row['input_sha256'],'assertions':len(actual),'variables':6,'gauges':11,'guards':20,'complements':8,'status_recorded':row['status']}


def main():
    C,boxes,directions,bindings=source_geometry()
    anchor=audit_anchor(C,boxes)
    sys.path.insert(0,str(ROOT))
    from experiments.det5_horizontal_fiber_oracle import compile_fiber,statement
    reports=[]
    # Two determinant signs, both orders, optional targets, and exact box endpoints.
    fixtures=[(0,s.Rational(1,8),s.Rational(1,10),s.Rational(1,5),s.Rational(1,10),s.Rational(3,20)),
              (0,s.Rational(1,8),s.Rational(1,10),s.Rational(1,5),s.Rational(3,20),s.Rational(1,10)),
              (s.Rational(3,5),1,s.Rational(1,10),s.Rational(1,5),s.Rational(1,10),s.Rational(3,20))]
    for shape,order,flags in product(fixtures,('lt','gt'),((False,False),(True,False),(True,True))):
        full,volume=flags
        expected,D,M,N=direct_fiber(shape,order,'183/500',full,volume,C,boxes,directions)
        variables,rows,meta=compile_fiber(tuple(map(str,shape)),order,full_width=full,volume_cuts=volume)
        need([str(v) for v in variables]==['alpha','eta','rho'],'three projective variables')
        need(forms(rows)==forms(expected),'independent in-memory fiber formula')
        need(forms(z3.parse_smt2_string(statement(rows)))==forms(expected),'serialized fiber formula')
        audit_coefficients(shape,order,D,M,N)
        need(forms(rows)!=forms(expected[1:]),'missing normalization rejected')
        need(forms(rows)!=forms(expected[:17]+expected[18:]),'missing gauge rejected')
        if full:need(forms(rows)!=forms(expected[:56]+expected[57:]),'missing width direction rejected')
        reports.append({'shape':list(map(str,shape)),'order':order,'D':str(D),'full_width':full,'volume_cuts':volume,'assertions':len(rows)})
    boundary_checks=[]
    for index,box in enumerate(boxes):
        q1,q2=s.Rational(box[0][0]),s.Rational(box[1][1])
        if q1==q2:q1,q2=s.Rational(box[0][1]),s.Rational(box[1][0])
        need(q1!=q2,'distinct boundary heights')
        xv,yv=min(q1,q2),max(q1,q2)
        shape=(xv,yv,s.Rational(1,10),s.Rational(1,5),s.Rational(1,10),s.Rational(3,20))
        if shape[5]*((1-xv)*shape[2]+xv*shape[3])-shape[4]*((1-yv)*shape[2]+yv*shape[3])==0:
            shape=(*shape[:5],s.Rational(1,5))
        order='lt' if q1<q2 else 'gt'
        _,rows,_=compile_fiber(tuple(map(str,shape)),order,full_width=False)
        expected_complements=[any(value<s.Rational(lo) or value>s.Rational(hi) for value,(lo,hi) in zip((q1,q2),b)) for b in boxes]
        need([z3.is_true(z3.simplify(v)) for v in rows[-8:]]==expected_complements,'all complements at box boundary')
        need(not expected_complements[index],'closed excluded rectangle includes endpoint')
        wrong=any(value<=s.Rational(lo) or value>=s.Rational(hi) for value,(lo,hi) in zip((q1,q2),box))
        need(wrong,'nonstrict outside mutation rejected')
        boundary_checks.append({'rectangle_index':index,'q1':str(q1),'q2':str(q2),'order':order})
    invalid=[]
    for label,shape,kwargs in [('singular',(0,1,'1/10','1/10','1/10','1/10'),{}),('unordered',(1,0,1,1,1,2),{}),('invalid volume',fixtures[0],{'full_width':False,'volume_cuts':True})]:
        try:compile_fiber(tuple(map(str,shape)),'lt',**kwargs)
        except ValueError:invalid.append(label)
        else:raise ValueError('accepted '+label)
    archivepath='results/det5_fiber_oracle_controls.json'
    archived=[]
    need((ROOT/archivepath).exists(),'required frozen compiler controls')
    if (ROOT/archivepath).exists():
        archive=read(archivepath)
        need(len(archive['controls'])==2 and {r['tag'] for r in archive['controls']}=={'positive','full_target'},'both exact controls')
        for row in archive['controls']:
            shape=tuple(row['shape'][name] for name in SHAPE)
            expected,D,M,N=direct_fiber(shape,row['order'],row['beta'],row['full_width'],row['volume_cuts'],C,boxes,directions)
            raw=(ROOT/row['input_path']).read_text();actual=list(z3.parse_smt2_string(raw))
            need(sha(row['input_path'])==row['input_sha256'],'archived input hash')
            need(forms(actual)==forms(expected),'entire archived fiber formula')
            need(row['D']==str(D),'archived determinant')
            audit_coefficients(shape,row['order'],D,M,N)
            need(row['coefficient_certificate_sha256']==sha('certificates/det5_horizontal_fiber_structure.json'),'coefficient certificate binding')
            need(row['gauge_vectors']==list(map(list,VECTORS)) and row['excluded_rectangles']==boxes,'all metadata directions and rectangles')
            subs=[(z3.Real(name),z3.RealVal(value)) for name,value in row['assignment'].items()]
            need(set(row['assignment'])=={'alpha','eta','rho'},'complete control assignment')
            truth=[z3.is_true(z3.simplify(z3.substitute(expr,*subs))) for expr in actual]
            # Truth list was recorded before serialization, so compare the direct
            # expected rows as well as every serialized assertion independently.
            expected_truth=[z3.is_true(z3.simplify(z3.substitute(expr,*subs))) for expr in expected]
            need(expected_truth==row['assertion_truth'],'exact saved control truth list')
            need(len(expected)==row['assertions'],'control original assertion count')
            need(sum(not b for b in truth)==sum(not b for b in expected_truth),'serialized false assertions')
            archived.append({'input_path':row['input_path'],'input_sha256':row['input_sha256'],'assertions':len(actual),'original_assertions':len(expected),'true_assertions':sum(truth),'false_assertions':sum(not b for b in truth),'tag':row['tag']})
    result={'status':'PASS','scope':'Independent fixed-height anchor and exact fixed-shape LRA compilation audit. Finite fibers do not cover the continuous shape domain. Recorded UNSAT still needs separately bound external proofs.',
            'anchor':anchor,'archived_fibers':archived,'in_memory_fixtures':reports,'complete_width_directions':list(map(list,directions)),
            'rectangle_proof_bindings':bindings,'rectangle_endpoint_checks':boundary_checks,'invalid_inputs_rejected':invalid,
            'mutation_controls':['missing normalization','missing gauge','missing full-width direction','nonstrict outside of closed rectangle'],
            'solver_queries_run':0,'proof_kernel_calls_run':0}
    (ROOT/'results/det5_fiber_oracle_encoding_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print('FIBER_ORACLE_INDEPENDENT=PASS')

if __name__=='__main__':main()
