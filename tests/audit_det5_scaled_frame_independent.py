"""Independent scaled-frame formula, frontier and rational SAT audit.

No discovery imports or solver queries. Exact rational polynomial comparison
handles degree two. Saved F/T/b assignments are completed by interval sums.
"""
from collections import deque
from copy import deepcopy
from fractions import Fraction as Q
from itertools import combinations,product
from math import gcd
from pathlib import Path
import hashlib,json
import z3
from audit_height_cover_independent import inverse,need,expect_rejection
from audit_det5_height_independent import geometry

ROOT=Path(__file__).resolve().parents[1]
BETA=Q(183,500); TARGET=Q(17,5); R=Q(6,5)/BETA**3
EXTRA={(1,-1,1),(2,1,1),(3,1,0),(6,1,2),(1,1,0),(2,1,0),(3,1,1),(4,1,1)}

def rat(x):return z3.RealVal(str(x))
def read(path):return json.loads((ROOT/path).read_text())
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def dot(a,b):return sum(x*y for x,y in zip(a,b))

def polynomial(e):
    if z3.is_rational_value(e):return {():e.as_fraction()}
    if z3.is_const(e):
        need(e.sort().kind()==z3.Z3_REAL_SORT,'real polynomial variable');return {(str(e),):Q(1)}
    kind=e.decl().kind(); children=e.children()
    if kind in (z3.Z3_OP_ADD,z3.Z3_OP_SUB,z3.Z3_OP_UMINUS):
        out={}
        for i,c in enumerate(children):
            sign=-1 if kind==z3.Z3_OP_UMINUS or kind==z3.Z3_OP_SUB and i else 1
            for m,v in polynomial(c).items():out[m]=out.get(m,Q(0))+sign*v
        return {m:v for m,v in out.items() if v}
    if kind==z3.Z3_OP_MUL:
        out={():Q(1)}
        for c in children:
            nxt={}
            for m,v in out.items():
                for n,w in polynomial(c).items():
                    term=tuple(sorted(m+n));need(len(term)<=2,'polynomial degree at most two')
                    nxt[term]=nxt.get(term,Q(0))+v*w
            out={m:v for m,v in nxt.items() if v}
        return out
    if kind==z3.Z3_OP_POWER:
        need(z3.is_rational_value(children[1]) and children[1].as_fraction()==2,'only square power')
        return polynomial(children[0]*children[0])
    raise AssertionError('unsupported polynomial '+str(e))

def canonical(expression, negated=False):
    if z3.is_true(expression):
        return not negated
    if z3.is_false(expression):
        return negated
    if z3.is_not(expression):
        return canonical(expression.arg(0), not negated)
    if z3.is_and(expression) or z3.is_or(expression):
        conjunction = z3.is_and(expression) ^ negated
        operator = 'and' if conjunction else 'or'
        values = []
        for child in expression.children():
            value = canonical(child, negated)
            if value is conjunction:
                continue
            if value is (not conjunction):
                return not conjunction
            if isinstance(value, tuple) and value[0] == operator:
                values.extend(value[1])
            else:
                values.append(value)
        values = tuple(sorted(set(values), key=repr))
        if not values:
            return conjunction
        return values[0] if len(values) == 1 else (operator, values)
    comparisons = {z3.Z3_OP_LE: '<=', z3.Z3_OP_LT: '<', z3.Z3_OP_GE: '>=',
                   z3.Z3_OP_GT: '>', z3.Z3_OP_EQ: '='}
    need(expression.decl().kind() in comparisons, 'supported Boolean atom')
    comparison = comparisons[expression.decl().kind()]
    coefficients = polynomial(expression.arg(0) - expression.arg(1))
    if negated:
        comparison = {'<=': '>', '<': '>=', '>=': '<', '>': '<=', '=': '!='}[comparison]
    if comparison in ('>', '>='):
        comparison = {'>': '<', '>=': '<='}[comparison]
        coefficients = {name: -c for name, c in coefficients.items()}
    if not coefficients:
        return comparison in ('<=', '=')
    items = sorted(coefficients.items())
    scale = abs(items[0][1])
    if comparison in ('=', '!=') and items[0][1] < 0:
        scale = -scale
    return comparison, tuple((name, c / scale) for name, c in items)


def forms(expressions):
    output = set()
    for expression in expressions:
        value = canonical(z3.simplify(expression))
        if value is not True:
            output.add(value)
    return output



def compare(expected,actual):
    a,b=forms(expected),forms(actual)
    need(a==b,f'assertion mismatch: missing {len(a-b)}, extra {len(b-a)}')

def directions(P):
    out=[]
    for u in product(range(-2,3),range(-3,4),range(-3,4)):
        if not any(u) or gcd(*u)!=1 or next(x for x in u if x)<0:continue
        h=[dot(u,p) for p in P]
        if max(h)-min(h)<=3:out.append(u)
    need(len(out)==15,'complete 15-direction enumeration')
    return out

def reconstruct(C,S,row):
    P=C['contact_points']; inv=inverse([[1]*4]+[[p[k] for p in P] for k in range(3)])
    coords=lambda v,affine=False:[dot(r,(int(affine),*v)) for r in inv]
    box=[[Q(x) for x in p] for p in row.get('box',[['0','1'] for _ in range(8)])]
    F=[[rat(0) for _ in range(4)] for _ in range(4)];ranges={};free=[]
    for j in range(4):
        ids=[i for i in range(4) if i!=j]; f,g=[z3.Real(f'f{i}{j}') for i in ids[:2]]
        for i,e in zip(ids,(f,g,1-f-g)):F[i][j]=e
        free.extend((f,g));ranges[ids[0],j]=box[2*j];ranges[ids[1],j]=box[2*j+1]
        ranges[ids[2],j]=(max(Q(0),1-box[2*j][1]-box[2*j+1][1]),min(Q(1),1-box[2*j][0]-box[2*j+1][0]))
    e=[F[i][j]>0 for i in range(4) for j in range(4) if i!=j]
    old=set(map(tuple,C['primitive_contact_edge_directions']))|{tuple(x['vector']) for x in S['eligible_vectors']}
    need(len(old)==10 and len(old|EXTRA)==18,'old and strengthened gauge counts')
    for vectors,beta in [(old,Q(37,102)),(old|EXTRA,BETA)]:
        for v in sorted(vectors):
            l=coords(v);f=[sum(F[i][j]*rat(l[j]) for j in range(4)) for i in range(4)]
            e.append(z3.Or(*[sum(f[i] for i in range(4) if mask&(1<<i))>rat(beta) for mask in range(1,15)]))
    for p in C['guards']:
        l=coords(p,True);e.append(z3.Or(*[sum(F[i][j]*rat(l[j]) for j in range(4))<=0 for i in range(4)]))
    for f,(lo,hi) in zip(free,box):e.extend((f>=rat(lo),f<=rat(hi)))
    L,H=row['Y_extrema'];b=z3.Real('scaled_b');e.extend((b>rat(1/R),b<rat(1/TARGET)))
    T=[[rat(0) if i==L else rat(1) if i==H and k==1 else z3.Real(f't{i}_{k}') for k in range(3)] for i in range(4)]
    for i in range(4):e.extend((T[i][1]>=0,T[i][1]<=1))
    for i,j in combinations(range(4),2):
        for k,m in ((0,5),(2,2)):
            d=T[i][k]-T[j][k];e.extend((d<rat(m*R)*b,-d<rat(m*R)*b))
    W={};lifted={};envelopes=[]
    for i,j,k in product(range(4),range(4),range(3)):
        f,t=F[i][j],T[i][k]
        if i==j or i==L:W[i,j,k]=rat(0)
        elif k==1 and i==H:W[i,j,k]=f
        elif row['kind']=='exact':W[i,j,k]=f*t
        else:
            fl,fh=ranges[i,j];tl,th=(Q(0),Q(1)) if k==1 else(-Q((5,1,2)[k])*R/TARGET,Q((5,1,2)[k])*R/TARGET)
            w=z3.Real(f'w{i}_{j}_{k}');W[i,j,k]=w;lifted[i,j,k]=(fl,fh,tl,th)
            e.extend((f>=rat(fl),f<=rat(fh),t>=rat(tl),t<=rat(th)))
            inequalities=[w>=rat(fl)*t+rat(tl)*f-rat(fl*tl),w>=rat(fh)*t+rat(th)*f-rat(fh*th),
                          w<=rat(fh)*t+rat(tl)*f-rat(fh*tl),w<=rat(fl)*t+rat(th)*f-rat(fl*th)]
            e+=inequalities;envelopes+=inequalities
    for j in range(1,4):
        for k in range(3):e.append(sum(W[i,j,k]-W[i,0,k] for i in range(4))==rat(P[j][k]-P[0][k])*b)
    ds=directions(P)
    for u in ds:
        h=[sum(u[k]*T[i][k] for k in range(3)) for i in range(4)]
        e.append(z3.Or(*[sgn*(h[i]-h[j])>rat(TARGET)*b for i,j in combinations(range(4),2) for sgn in (-1,1)]))
    if row['kind']=='relaxation':need(len(lifted)==24,'exactly 24 shared product variables')
    return e,F,T,b,lifted,ds,envelopes


def verify_frontier(data,C):
    _,_,orbits=geometry(C['contact_points']); reps={tuple(min(o)) for o in orbits}
    need(reps=={(0,1),(0,3),(1,0)},'three Y symmetry representatives')
    need(len(data['charts'])==3 and {tuple(c['Y_extrema']) for c in data['charts']}==reps,'three distinct charts')
    exact=[r for r in data['queries'] if r['kind']=='exact']
    need(len(exact)==3 and {tuple(r['Y_extrema']) for r in exact}==reps,'three distinct exact targets')
    allrows=[r for r in data['queries'] if r['kind']=='relaxation']
    need(len(exact)+len(allrows)==len(data['queries']),'no unknown query kind')
    keys=[(tuple(r['Y_extrema']),r['node']) for r in allrows]
    need(len(keys)==len(set(keys)),'no repeated box query')
    results=[]
    for c in data['charts']:
        rows=[r for r in allrows if r['Y_extrema']==c['Y_extrema']]
        queue=deque([{'node':'r','box':[['0','1'] for _ in range(8)]}]);closed=[]
        for r in rows:
            need(bool(queue),'no query beyond complete cover');leaf=queue.popleft()
            need(r['node']==leaf['node'] and r['box']==leaf['box'],'breadth-first exact eight-dimensional box')
            need(r['status'] in ('sat','unsat','unknown'),'recognized relaxation status')
            if r['status']=='unsat':closed.append(leaf)
            else:
                box=[[Q(x) for x in p] for p in leaf['box']]
                axis=max(range(8),key=lambda i:box[i][1]-box[i][0]);need(r['split_axis']==axis,'longest edge split axis')
                lo,hi=box[axis];mid=(lo+hi)/2
                for suffix,iv in [('0',(lo,mid)),('1',(mid,hi))]:
                    child=deepcopy(box);child[axis]=iv
                    queue.append({'node':leaf['node']+suffix,'box':[[str(x) for x in p] for p in child]})
        need(c['closed']==closed and c['pending']==list(queue),'exact closed and pending frontier')
        results.append({'Y_extrema':c['Y_extrema'],'queries':len(rows),'status_closed_leaves':len(closed),'pending_boxes':len(queue)})
    return results


def complete_saved_assignment(row,C,actual,F,T,b,lifted,ds):
    fm=[list(map(Q,r)) for r in row['F']];tm=[list(map(Q,r)) for r in row['T']];bm=Q(row['b'])
    substitutions=[]
    for j in range(4):
        for i in [i for i in range(4) if i!=j][:2]:substitutions.append((z3.Real(f'f{i}{j}'),rat(fm[i][j])))
    for i,k in product(range(4),range(3)):
        if z3.is_const(T[i][k]) and not z3.is_rational_value(T[i][k]):substitutions.append((T[i][k],rat(tm[i][k])))
    substitutions.append((b,rat(bm)))
    for i,j in product(range(4),repeat=2):
        need(z3.simplify(z3.substitute(F[i][j],*substitutions)).as_fraction()==fm[i][j],'saved full F binding')
    for i,k in product(range(4),range(3)):
        need(z3.simplify(z3.substitute(T[i][k],*substitutions)).as_fraction()==tm[i][k],'saved normalized T binding')
    bounds={};assignment={};P=C['contact_points']
    for i,j,k in product(range(4),range(4),range(3)):
        if (i,j,k) not in lifted:bounds[i,j,k]=(fm[i][j]*tm[i][k],)*2
        else:
            fl,fh,tl,th=lifted[i,j,k];f,t=fm[i][j],tm[i][k]
            lo=max(fl*t+tl*f-fl*tl,fh*t+th*f-fh*th)
            hi=min(fh*t+tl*f-fh*tl,fl*t+th*f-fl*th)
            need(lo<=hi,'nonempty McCormick product interval');bounds[i,j,k]=(lo,hi)
    for k in range(3):
        col=[(sum(bounds[i,j,k][0] for i in range(4)),sum(bounds[i,j,k][1] for i in range(4))) for j in range(4)]
        lo=max(col[j][0]-bm*(P[j][k]-P[0][k]) for j in range(4))
        hi=min(col[j][1]-bm*(P[j][k]-P[0][k]) for j in range(4))
        need(lo<=hi,'joint contact column-sum interval is nonempty')
        for j in range(4):
            slack=lo+bm*(P[j][k]-P[0][k])-col[j][0]
            for i in range(4):
                lower,upper=bounds[i,j,k];part=min(slack,upper-lower);slack-=part
                if (i,j,k) in lifted:assignment[f'w{i}_{j}_{k}']=lower+part
            need(slack==0,'rational column slack fully distributed')
    substitutions += [(z3.Real(name),rat(value)) for name,value in assignment.items()]
    for expression in actual:need(z3.is_true(z3.simplify(z3.substitute(expression,*substitutions))),'completed rational assignment satisfies every archived assertion')
    contact_residual=max(abs(sum(fm[i][j]*tm[i][k]-fm[i][0]*tm[i][k] for i in range(4))-bm*(P[j][k]-P[0][k])) for j in range(1,4) for k in range(3))
    archived=row['actual_F']
    try:fi=inverse(fm)
    except (StopIteration,ZeroDivisionError):
        need(not archived['invertible'],'actual singular F binding');actual_body={'invertible':False}
    else:
        V=[[sum(Q(P[i][k])*fi[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
        widths=[(max(dot(u,v) for v in V)-min(dot(u,v) for v in V),u) for u in ds]
        minimum=min(w for w,u in widths);minimizers=[u for w,u in widths if w==minimum]
        need(archived['invertible'] and Q(archived['minimum_of_complete_15'])==minimum,'actual F width binding')
        need(tuple(archived['minimizing_list_direction']) in minimizers,'actual minimizing direction binding')
        need(archived['all_15_above_target']==(minimum>TARGET),'actual F target status binding')
        actual_body={'invertible':True,'minimum_of_complete_15':str(minimum),'minimizing_directions':[list(u) for u in minimizers]}
    return {'path':row['path'],'rational_completion':[{'variable':n,'value':str(v)} for n,v in sorted(assignment.items())],
            'exact_contact_residual':str(contact_residual),'exact_contact_equations_hold':contact_residual==0,'actual_F':actual_body,
            'archived_maximum_product_residual_scope':'Original solver w values were not saved; this audit constructs a different certified completion and does not bind that original residual.'}


def pinned_exact_regression(data,C,S):
    source='results/det5_joint_short_gauges.json'
    pin=read(source)['retained_witness'];fm=[list(map(Q,r)) for r in pin['F']]
    P=C['contact_points'];fi=inverse(fm)
    V=[[sum(Q(P[i][k])*fi[i][j] for i in range(4)) for k in range(3)] for j in range(4)]
    L,H=1,0;lo=min(v[1] for v in V);hi=max(v[1] for v in V);bm=1/(hi-lo)
    need(V[L][1]==lo and V[H][1]==hi,'pinned actual Y extrema')
    tm=[[bm*(v[k]-V[L][k]) for k in range(3)] for v in V]
    row=next(r for r in data['queries'] if r['kind']=='exact' and r['Y_extrema']==[L,H])
    expected,F,T,b,lifted,ds,_=reconstruct(C,S,row)
    actual=list(z3.parse_smt2_file(str(ROOT/row['path'])))
    subs=[(b,rat(bm))]
    for j in range(4):
        for i in [i for i in range(4) if i!=j][:2]:subs.append((z3.Real(f'f{i}{j}'),rat(fm[i][j])))
    for i,k in product(range(4),range(3)):
        if z3.is_const(T[i][k]) and not z3.is_rational_value(T[i][k]):subs.append((T[i][k],rat(tm[i][k])))
    bad=[];good=0
    for e in actual:
        value=z3.simplify(z3.substitute(e,*subs))
        need(z3.is_true(value) or z3.is_false(value),'pinned substitution eliminates every variable')
        if z3.is_false(value):bad.append(e)
        else:good+=1
    failing=[];badwidth=[]
    for u,clause in zip(ds,expected[-15:]):
        heights=[dot(u,v) for v in V];width=max(heights)-min(heights)
        if width<=TARGET:
            failing.append({'direction':list(u),'width':str(width)});badwidth.append(clause)
    need(bool(failing),'pinned body has failed complete-width tests')
    need(forms(bad)==forms(badwidth),'exactly failed width clauses reject the pinned body')
    need(all(z3.is_true(z3.simplify(z3.substitute(e,*subs))) for e in expected[:-15]),'all non-width exact constraints pass pinned body')
    return {'source_path':source,'source_sha256':sha(source),'Y_extrema':[L,H],
            'b':str(bm),'T':[[str(x) for x in r] for r in tm],
            'actual_assertions_true':good,'actual_assertions_false':len(bad),
            'all_non_width_assertions_true':True,'false_assertions_are_exactly_failed_width_tests':True,
            'failed_width_tests':failing}


def main():
    path='results/det5_scaled_width_frame.json';raw=(ROOT/path).read_bytes();data=json.loads(raw)
    C=next(c for c in read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index']==5)
    S=next(c for c in read('results/two_vector_class_scan.json')['classes'] if c['class_index']==5)
    need(len(data['queries'])==30,'frozen three exact plus27 relaxation queries')
    need(Q(data['R'])==R and list(map(Q,data['gap_bounds']))==[1/R,1/TARGET],'exact model constant metadata')
    front=verify_frontier(data,C);inputs=[];sat=[];control=None
    for number,row in enumerate(data['queries']):
        p=row['path'];need(sha(p)==row['input_sha256'],'archived input hash')
        expected,F,T,b,lifted,ds,envelopes=reconstruct(C,S,row)
        actual=list(z3.parse_smt2_file(str(ROOT/p)));compare(expected,actual)
        polynomials=[polynomial(e.arg(0)-e.arg(1)) for e in expected if z3.is_eq(e)]
        need(max((len(m) for p in polynomials for m in p),default=0)<= (2 if row['kind']=='exact' else 1),'declared reconstruction degree')
        inputs.append({'path':p,'sha256':sha(p),'kind':row['kind']})
        if row['kind']=='relaxation' and row['status']=='sat':
            sat.append(complete_saved_assignment(row,C,actual,F,T,b,lifted,ds))
            if control is None:control=(row,expected,actual,F,T,b,lifted,ds,envelopes)
        elif row['kind']=='exact':need(row['status']=='unknown','no unchecked exact SAT assignment')
        if (number+1)%10==0:print('PASS scaled formulas: '+str(number+1),flush=True)
    need(len(sat)==19,'nineteen archived rational SAT relaxations')
    row,expected,actual,F,T,b,lifted,ds,envelopes=control
    bad=deepcopy(data);bad['charts'][0]['pending'].pop()
    controls=[expect_rejection('missing pending box',lambda:verify_frontier(bad,C)),
              expect_rejection('missing complete width inequality',lambda:compare(expected,actual[:-1]))]
    ekey=canonical(z3.simplify(envelopes[0]));without=[e for e in actual if canonical(z3.simplify(e))!=ekey]
    need(len(without)<len(actual),'envelope corruption actually changes formula')
    controls.append(expect_rejection('missing shared product envelope',lambda:compare(expected,without)))
    wrong=deepcopy(row);wrong['b']='1'
    controls.append(expect_rejection('corrupt saved gap',lambda:complete_saved_assignment(wrong,C,actual,F,T,b,lifted,ds)))
    pinned=pinned_exact_regression(data,C,S)
    need((ROOT/path).read_bytes()==raw,'archive remained frozen during audit')
    out={'status':'PASS','scope':'Exact degree-two/linear assertion reconstruction and full finite frontier audit. Nineteen rational saved F/T/b assignments are independently completed and satisfy every LRA assertion. No solver queries, UNSAT proof checks or class exclusion.',
         'archive':{'path':path,'sha256':hashlib.sha256(raw).hexdigest()},'query_count':30,'exact_formulas_checked':3,'linear_relaxations_checked':27,
         'shared_products_per_relaxation':24,'rational_SAT_completions_checked':len(sat),'charts':front,'inputs':inputs,'sat_assignments':sat,
         'pinned_exact_regression':pinned,'rejected_mutations':controls,'solver_queries_run':0,'unsat_proofs_checked':0}
    (ROOT/'results/det5_scaled_frame_encoding_validation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','query_count','rational_SAT_completions_checked','charts','solver_queries_run','unsat_proofs_checked')},indent=2))

if __name__=='__main__':main()
