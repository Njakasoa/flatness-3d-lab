"""Independent compact polynomial/interval compiler audit, with no solver calls."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from collections import Counter
from functools import lru_cache
import hashlib,json,random,sys,gzip
import sympy as s
import z3
from audit_det5_quadratic_chart_independent import eliminated,as_z3,forms
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from experiments import det5_compact_interval_fiber as tested
from experiments.det5_horizontal_fiber_oracle import compile_fiber
Pp,Qq,C,E,R,U=s.symbols('p q C E r u');SH=(Pp,Qq,C,E,R,U)
T,H,Z=s.symbols('alpha eta rho');FV=(T,H,Z);L=1-Pp*Qq
BETA=s.Rational(183,500);W=s.Rational(17,5);MAX=s.Rational(50000000,2042829)
VECTORS=[(0,0,1),(0,1,-1),(0,1,0),(1,0,0),(1,0,1),(2,0,1),(3,0,1),(5,0,2),(5,1,1),(5,1,2),(1,-1,1)]
CONTACT=s.Matrix([[1,1,1,1],[0,5,0,0],[0,1,1,0],[0,2,0,1]])
J=s.Matrix([[-1,-1,-1],[1,0,0],[0,1,0],[0,0,1]])

def need(v,m):
    if not v:raise ValueError(m)
def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def atom(expr,rel):return (rel,s.expand(expr))
def disj(atoms):return ('or',atoms)

def independent_models():
    Cdata=next(c for c in read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index']==5)
    need(Cdata['contact_points']==[[0,0,0],[5,1,2],[0,1,0],[0,0,1]],'physical contact order')
    need(len(Cdata['guards'])==len(set(map(tuple,Cdata['guards'])))==20,'twenty guards')
    directions=[(0,0,1),(0,1,-1),(0,1,0),(0,1,1),(0,2,-1),(1,-3,-2),(1,-3,-1),(1,-2,-3),(1,-2,-2),(1,-2,-1),(1,-1,-3),(1,-1,-2),(1,-1,-1),(1,0,-3),(1,0,-2)]
    need(list(map(tuple,read('results/det5_complete_geometry_validation.json')['directions']))==directions,'all fifteen directions')
    old=read('results/det5_class5_y_cvc5_validation.json')
    boxes=[r['box'] for r in old['leaves'] if r['extrema']==[0,3]]+[read('results/det5_y_corner_enlarged_3_5.json')['box'],read('results/det5_strong_anchor_rectangle.json')['box']]
    need(len(boxes)==9,'nine prior closed rectangles')
    models={};polynomials=set();identities=0
    for order in ('lt','gt'):
        symbols,F,heights,a,b=eliminated(order)
        x,y,t,c,e,r,u,h=symbols
        sub={x:Pp*(1-Qq)/L,y:(1-Qq)/L,c:C*L/(1-Pp),e:E*L/(1-Qq),r:R,u:U}
        def lift(value):return s.expand(s.cancel(L*Z*value.subs(sub,simultaneous=True).subs({t:T/Z,h:H/Z},simultaneous=True)))
        M=F.applyfunc(lift)
        G=(F*J)[1:4,:];Numerator=CONTACT[1:,:]*J*G.adjugate()
        pairs={}
        for i in range(4):
            for j in range(i):
                ij=s.zeros(4,1);ij[i]=1;ij[j]=-1
                nums=Numerator*ij[1:4,:]
                for k in range(3):pairs[k,i,j]=lift(nums[k])
        D=U*(C+Pp*E)-R*(Qq*C+E)
        oldD=u*((1-x)*c+x*e)-r*((1-y)*c+y*e)
        need(s.cancel(oldD.subs(sub,simultaneous=True)-D)==0,'horizontal determinant unchanged');identities+=1
        for sign in (-1,1):
            rows=[]
            def add(expr,rel,label):rows.append((label,atom(expr,rel)))
            add(L*(H-Z*x.subs(sub)-T*(y-x).subs(sub)-1),'=','height normalization')
            for expr in (Z-W,MAX-Z,T,Z-T,H,Z-H):add(expr,'>','projective bounds')
            for v in (Pp,Qq):add(v,'>=','compact shape');add(1-v,'>','compact shape')
            for v in (C,E,R,U):add(v,'>','compact shape')
            for v in (1-C-E,1-R,1-U):add(v,'>','compact shape')
            delta=s.Rational(49,1500) if order=='lt' else s.Rational(249,1700)
            add(L-delta,'>','analytic height separation')
            add(sign*D-Z/MAX,'>','global volume determinant margin')
            add(C+E-BETA,'>','horizontal Z gauge')
            add(MAX*(1-Pp)-L,'>','global gap compact face margin')
            if sign==1:add((C+Pp*E)*(Qq*C+E)-(3 if order=='lt' else 2)*W/MAX,'>','positive determinant product margin')
            for i in range(4):
                for j in range(4):
                    if i!=j:add(M[i,j],'>','strict facet contact')
            for v in VECTORS:
                image=M*CONTACT.inv()*s.Matrix([0,*v])
                rows.append(('gauge '+str(v),disj([atom(sum(image[i] for i in range(4) if mask&(1<<i))-BETA*L*Z,'>') for mask in range(1,15)])))
            for point in Cdata['guards']:
                image=M*CONTACT.inv()*s.Matrix([1,*point])
                rows.append(('observer '+str(point),disj([atom(value,'<=') for value in image])))
            add(Qq*C+E-(3 if order=='lt' else 2)*U,'>=','simplified first observer')
            for v in directions:
                if v==(0,1,0):continue
                nums=[sum(v[k]*pairs[k,i,j] for k in range(3)) for i in range(4) for j in range(i)]
                rows.append(('width '+str(list(v)),disj([atom(eps*5*n-17*sign*D*L,'>') for n in nums for eps in (-1,1)])))
            hn=[Pp*(1-Qq),1-Qq] if order=='lt' else [1-Qq,Pp*(1-Qq)]
            for box in boxes:
                rows.append(('closed rectangle complement '+str(box),disj([atom(expr,'>') for n,(lo,hi) in zip(hn,box) for expr in (s.Rational(lo)*L-n,n-s.Rational(hi)*L)])))
            models[order,sign]=rows
            actual,meta=tested.exact_model(order,sign)
            need(len(actual)==len(rows),'all labeled rows')
            def compare(expected,node):
                nonlocal identities
                rel,value=expected
                if rel=='or':
                    need(set(node)=={'or'} and len(value)==len(node['or']),'all disjuncts')
                    for a,b in zip(value,node['or']):compare(a,b)
                    return
                need(set(node)=={'relation','coefficients'} and node['relation']==rel and len(node['coefficients'])==4,'exact relation and four coefficients')
                poly=s.Poly(s.cancel(value),*FV)
                need(poly.total_degree()<=1,'independently affine in fiber')
                expected_coeff=[poly.coeff_monomial(m) for m in (1,T,H,Z)]
                for a,b in zip(expected_coeff,node['coefficients']):
                    need(s.expand(a-b)==0,'independent cleared polynomial coefficient');identities+=1
                    s.Poly(a,*SH);polynomials.add(s.expand(a))
            for (label,node),row in zip(rows,actual):
                need(label==row['label'],'exact ordered labels');compare(node,row['formula'])
            for p,digest in meta['sources'].items():need(sha(p)==digest,'source binding')
    return models,polynomials,identities,boxes


@lru_cache(None)
def natural_bounds(expr,box):
    # Independent monotonic monomial bounds on nonnegative shape intervals;
    # no calls to the compiler's iterative interval multiplication.
    lo=hi=Q(0)
    for powers,coefficient in s.Poly(expr,*SH).terms():
        low=Q(1);high=Q(1)
        for (a,b),n in zip(box,powers):low*=a**n;high*=b**n
        c=Q(coefficient)
        lo+=c*(low if c>=0 else high);hi+=c*(high if c>=0 else low)
    return lo,hi


@lru_cache(None)
def fiber_coefficients(value):
    poly=s.Poly(s.cancel(value),*FV)
    return tuple(poly.coeff_monomial(m) for m in (1,T,H,Z))


def outer_expected(node,box,closed=False):
    rel,value=node
    if rel=='or':return z3.Or(*[outer_expected(a,box,closed) for a in value])
    bounds=[natural_bounds(c,box) for c in fiber_coefficients(value)]
    variables=[z3.RealVal(1),*z3.Reals('alpha eta rho')]
    low=sum(z3.RealVal(str(b[0]))*v for b,v in zip(bounds,variables));high=sum(z3.RealVal(str(b[1]))*v for b,v in zip(bounds,variables))
    if closed:rel={'>':'>=','<':'<='}.get(rel,rel)
    return {'>':lambda:high>0,'>=':lambda:high>=0,'<':lambda:low<0,'<=':lambda:low<=0,'=':lambda:z3.And(low<=0,high>=0)}[rel]()


@lru_cache(None)
def rational_terms(expr):
    return tuple((powers,Q(coefficient)) for powers,coefficient in s.Poly(expr,*SH).terms())

def exact_value(expr,point):
    return sum(c*s.prod(v**n for v,n in zip(point,powers)) for powers,c in rational_terms(expr))


def main():
    tested.interval=lru_cache(None)(tested.interval)
    print('Independent symbolic model reconstruction...',flush=True)
    models,polynomials,identities,rectangles=independent_models()
    print('Symbolic coefficients verified; testing interval enclosures...',flush=True)
    rng=random.Random(5092026)
    boxes=[tuple((Q(0),Q(1)) for _ in SH),tuple((Q(1,4),Q(3,4)) for _ in SH)]
    for _ in range(4):
        box=[]
        for v in SH:
            a,b=sorted((rng.randrange(17),rng.randrange(17)));box.append((Q(a,16),Q(b,16)))
        boxes.append(tuple(box))
    # Two rational shapes of opposite determinant signs; all compact parameters
    # interior, C+E<1. Both original height orders are tested at each shape.
    points=[(Q(1,3),Q(1,4),Q(1,5),Q(1,4),Q(1,10),Q(1,2)),
            (Q(1,3),Q(1,4),Q(1,5),Q(1,4),Q(1,2),Q(1,10))]
    boxes.extend(tuple((x,x) for x in point) for point in points)
    enclosure_samples=0;coefficient_enclosures=0;formula_cases=[]
    for box in boxes:
        samples=[tuple(a for a,b in box),tuple(b for a,b in box)]
        samples.extend(tuple(a+(b-a)*Q(rng.randrange(17),16) for a,b in box) for _ in range(4))
        for poly in polynomials:
            bounds=natural_bounds(poly,box);need(bounds==tested.interval(poly,box),'independent entire coefficient interval')
            coefficient_enclosures+=1
            for point in samples:
                value=Q(exact_value(poly,point))
                need(bounds[0]<=value<=bounds[1],'exact rational enclosure fixture');enclosure_samples+=1
        for (order,sign),rows in models.items():
            for closed in (False,True):
                expected=[outer_expected(node,box,closed) for label,node in rows]+[v>=0 for v in z3.Reals('alpha eta rho')]
                variables,actual,meta=tested.compile_box(box,order,sign,closed)
                need([str(v) for v in variables]==['alpha','eta','rho'],'three projective variables')
                need(forms(actual)==forms(expected),'full outer formula and polarity')
                need(len(actual)==len(expected),'full assertion count')
                need(forms(actual)!=forms(expected[:-1]),'missing explicit nonnegative rho rejected')
                formula_cases.append({'order':order,'sign':sign,'closed':closed,'assertions':len(actual)})
    print('Outer interval formulas verified; testing point controls...',flush=True)
    # At point boxes the shared core exactly agrees with the already audited
    # fixed-shape oracle, up to positive multiplication by the fixed L.
    point_checks=[]
    for point in points:
        p,q,c0,e0,r,u=point;ell=1-p*q
        oldshape=(p*(1-q)/ell,(1-q)/ell,c0*ell/(1-p),e0*ell/(1-q),r,u)
        D=u*(c0+p*e0)-r*(q*c0+e0);sign=1 if D>0 else -1
        box=tuple((v,v) for v in point)
        for order in ('lt','gt'):
            _,oldrows,_=compile_fiber(oldshape,order,full_width=True,volume_cuts=True)
            selected=[]
            for label,node in models[order,sign]:
                if label=='height normalization' or label=='strict facet contact' or label.startswith(('gauge ','observer ','width ')):
                    selected.append(outer_expected(node,box))
            # Old core: normalization,12 contacts,11 gauges,20 observers,14 widths.
            eq=oldrows[0];expected=[z3.And(eq.arg(0)<=eq.arg(1),eq.arg(0)>=eq.arg(1)),*oldrows[5:48],*oldrows[56:70]]
            need(forms(selected)==forms(expected),'point core agrees with fixed fiber oracle, all physical directions')
            need(len(selected)==len(expected)==58,'full shared point core')
            point_checks.append({'shape':list(map(str,point)),'order':order,'D':str(D),'shared_assertions':58})
    # Endpoint complements are evaluated independently from true normalized
    # heights, with strict outside polarity, for every inherited rectangle.
    endpoint_checks=[]
    for index,box in enumerate(rectangles):
        q1,q2=Q(box[0][0]),Q(box[1][1])
        if q1==q2:q1,q2=Q(box[0][1]),Q(box[1][0])
        x,y=min(q1,q2),max(q1,q2);p=x/y;q=(1-y)/(1-x)
        point=(p,q,Q(1,5),Q(1,4),Q(1,10),Q(1,2));order='lt' if q1<q2 else 'gt'
        node=models[order,1][-9+index][1]
        expr=outer_expected(node,tuple((v,v) for v in point))
        need(z3.is_false(z3.simplify(expr)),'each closed rectangle retains endpoint')
        endpoint_checks.append(index)
    # Adversarial controls for the specific enclosure choices.
    point=points[0];box=tuple((v,v) for v in point)
    order='lt';sign=1
    expected=[outer_expected(n,box) for _,n in models[order,sign]]
    width_index=next(i for i,(label,_) in enumerate(models[order,sign]) if label.startswith('width '))
    need(forms(expected)!=forms(expected[:width_index]+expected[width_index+1:]),'missing complete-width row rejected')
    p,q,c0,e0,r,u=point;D=u*(c0+p*e0)-r*(q*c0+e0)
    width_node=models[order,sign][width_index][1]
    altered=disj([atom(value+17*sign*(U*(C+Pp*E)-R*(Qq*C+E))*(L-1),rel) for rel,value in width_node[1]])
    need(forms([outer_expected(width_node,box)])!=forms([outer_expected(altered,box)]),'missing L in width denominator rejected')
    idx=next(i for i,(label,_) in enumerate(models['lt',1]) if label=='gauge (1, 0, 0)')
    need(any(s.expand(a[1]-b[1])!=0 for a,b in zip(models['lt',1][idx][1][1],models['gt',1][idx][1][1])),'wrong physical reverse branch coefficient rejected')
    norm=outer_expected(models[order,sign][0][1],box)
    zero=[(v,z3.RealVal(0)) for v in z3.Reals('alpha eta rho')]
    need(z3.is_false(z3.simplify(z3.substitute(norm,*zero))) and z3.is_true(z3.simplify(z3.substitute(z3.Or(*norm.children()),*zero))),'equality OR mutation distinguished')
    # On [0,1], coefficient p lies between 0 and1. At z=-1, 0*z is
    # not a lower bound for p*z at p=1: nonnegative fiber variables matter.
    need(Q(0)*(-1)>Q(1)*(-1),'negative-variable enclosure counterexample')
    # Wrong polarity would discard p=1,z=1 satisfying p*z-1/2>0.
    need(Q(0)-Q(1,2)<0<Q(1)-Q(1,2),'upper-to-lower polarity counterexample')
    archive_checks=[]
    for path in sorted((ROOT/'results').glob('det5_compact_interval_*.json')):
        row=json.loads(path.read_text())
        if not all(k in row for k in ('input_path','box','order','determinant_sign','closed_strict_atoms')):continue
        box=tuple(tuple(map(Q,b)) for b in row['box']);order=row['order'];sign=row['determinant_sign'];closed=row['closed_strict_atoms']
        expected=[outer_expected(node,box,closed) for label,node in models[order,sign]]+[v>=0 for v in z3.Reals('alpha eta rho')]
        actual=list(z3.parse_smt2_file(str(ROOT/row['input_path'])))
        need(row['input_sha256']==sha(row['input_path']),'archived input hash')
        # Serialization may omit an inert trailing true; none are required as premises.
        def nontrivial(xs):return forms([v for v in xs if not z3.is_true(z3.simplify(v))])
        need(nontrivial(actual)==nontrivial(expected),'independent entire archived outer formula')
        entry={'path':str(path.relative_to(ROOT)),'input_sha256':row['input_sha256'],'status_recorded':row['status'],'assertions':len(actual)}
        proofpath=path.with_name(path.stem+'_ethos_validation.json')
        if proofpath.exists():
            from check_det5_fiber_proofs import reference
            from check_height_ethos import ETHOS_REV,CVC5_REV
            proof=json.loads(proofpath.read_text())
            ref,vs,count=reference((ROOT/row['input_path']).read_text())
            need(proof['status']=='PASS' and row['status']=='unsat','checked archived refutation')
            need(proof['input_sha256']==row['input_sha256'],'proof input binding')
            rawproof=gzip.decompress((ROOT/row['proof_path']).read_bytes())
            need(hashlib.sha256(rawproof).hexdigest()==proof['proof_sha256']==row['proof_sha256'],'proof bytes')
            need(proof['reference_sha256']==hashlib.sha256(ref.encode()).hexdigest() and proof['assertions_preserved']==count and set(proof['variables'])==vs,'exact checked reference')
            need(proof['ethos']['exit_code']==0 and proof['ethos']['stdout']=='correct' and not proof['ethos']['stderr'],'external success')
            need(proof['ethos_revision']==ETHOS_REV and proof['cvc5_signature_revision']==CVC5_REV and proof['unrelated_assumption_rejected'],'pinned checker and negative control')
            entry['bound_external_proof_receipt']=str(proofpath.relative_to(ROOT))
        archive_checks.append(entry)
    receipt={'status':'PASS','scope':'Independent algebra, exact interval and Boolean outer-formula audit; no solver calls, no whole-domain exclusion inferred from labels.',
             'symbolic_coefficient_identities':identities,'distinct_coefficient_polynomials':len(polynomials),'coefficient_intervals_checked':coefficient_enclosures,
             'exact_rational_enclosure_samples':enclosure_samples,'outer_formula_cases':formula_cases,'point_oracle_controls':point_checks,
             'strict_rectangle_endpoint_controls':endpoint_checks,'mutation_controls':['missing nonnegative rho','missing width direction','missing L denominator','wrong physical reverse order','equality OR','negative fiber enclosure','reversed polarity'],'archived_inputs':archive_checks,'solver_queries_run':0,'proof_kernel_calls_run':0}
    (ROOT/'results/det5_compact_interval_fiber_validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print('COMPACT_INTERVAL_FIBER_INDEPENDENT=PASS')

if __name__=='__main__':main()
