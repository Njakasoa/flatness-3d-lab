"""Independent exact projection audit: physical pieces, sparse rows, strict alternative.

Uses independent strict Fourier-Motzkin elimination as an oracle for the
small rational control systems. No SMT or optimization solver is called.
"""
from fractions import Fraction as Q
from itertools import combinations,product
from pathlib import Path
from copy import deepcopy
import hashlib,json,random,sys
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from experiments import det5_horizontal_projection as tested
p,q,C,E=s.symbols('p q C E');BASE=(p,q,C,E)
a,tau=s.symbols('a tau');L=1-p*q;A=C+p*E;B=q*C+E;S=C+E
alpha=(1-p)*E;y=(1-q)/L;x=p*y
THRESHOLD=s.Rational(183,100);BETA=s.Rational(183,500)
DELTA=s.Rational(17,5)*s.Rational(5,6)*BETA**3
VECTORS=((1,0,0),(2,0,1),(1,0,1),(3,0,1))

def need(v,m):
    if not v:raise ValueError(m)
def read(path):return json.loads((ROOT/path).read_text())
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

def physical_pieces(order):
    k=3 if order=='lt' else 2
    result=[]
    # In physical contact coordinates,5 ell(v)=vx*(e1-e2)+(5vz-2vx)*(e3-e0).
    # The canonical reverse permutation reverses only the first horizontal vector.
    for vx,vy,vz in VECTORS:
        need(vy==0,'horizontal physical vector')
        m=vx if order=='lt' else -vx;n=5*vz-2*vx
        if m<0:m,n=-m,-n  # evenness of the gauge
        c=n+s.Rational(m,k)*a;t=m*tau
        if n>0:
            # Fixed signs give gamma=cA+t+max(c alpha-(1-y)t,0).
            options=[s.expand(c*A+t+c*alpha-(1-y)*t),s.expand(c*A+t)]
        else:
            j=-c
            # Disjoint variable positive parts, by yA>=omega=yA-xB.
            options=[j*B,t-j*(A-B),j*(B+(1-q)*C)-y*t]
            if s.expand(j-(1-a))==0:
                # The other two pieces are <1 on the stated compact domain.
                options=[options[1]]
        result.append(options)
    return result


def expected_rows(order,pattern):
    k=3 if order=='lt' else 2
    v0=a*alpha/k-(1-y)*tau
    rhs=[('a positive',a),('a below one',1-a),('tau positive',tau),
         ('r below one',1-(a*A/k+tau)),('volume determinant margin',B*tau-DELTA),
         ('projected forced observer',L*(alpha+(5-k)*v0)/(5-k)),
         ('Z gauge',S-BETA),('height separation',L-(s.Rational(49,1500) if order=='lt' else s.Rational(249,1700)))]
    options=physical_pieces(order)
    rhs.extend((str(v),L*(opts[i]-THRESHOLD)) for v,opts,i in zip(VECTORS,options,pattern))
    rows=[]
    for label,expr in rhs:
        poly=s.Poly(s.cancel(expr),a,tau)
        need(poly.total_degree()<=1,'all projected atoms affine')
        rows.append((label,tuple(s.expand(poly.coeff_monomial(v)) for v in (a,tau,1))))
    return rows


def decode(terms):
    value=0
    for term in terms:
        powers=term['powers']
        need(len(powers)==4 and all(type(v)==int and v>=0 for v in powers),'four nonnegative monomial exponents')
        value+=s.Rational(term['coefficient'])*s.prod(v**n for v,n in zip(BASE,powers))
    return s.expand(value)


def rational_rows(rows,base):
    sub=dict(zip(BASE,map(s.Rational,base)))
    return [tuple(Q(v.subs(sub)) for v in co) for label,co in rows]


def strict_fm(rows):
    """Eliminate a, then tau with exact strict lower/upper comparisons."""
    rows=[tuple(map(Q,row)) for row in rows]
    unary=[(b,c) for aa,b,c in rows if aa==0]
    positive=[r for r in rows if r[0]>0];negative=[r for r in rows if r[0]<0]
    for pa,pb,pc in positive:
        for na,nb,nc in negative:
            unary.append((-na*pb+pa*nb,-na*pc+pa*nc))
    lower=[];upper=[]
    for b,c in unary:
        if b==0:
            if c<=0:return False
        elif b>0:lower.append(-c/b)
        else:upper.append(-c/b)
    return not(lower and upper) or max(lower)<min(upper)


def verify_circuit(rows,cert):
    ids=cert['support'];weights=list(map(Q,cert['weights']))
    need(1<=len(ids)<=3 and len(set(ids))==len(ids)==len(weights),'small distinct support')
    need(all(type(i)==int and 0<=i<len(rows) for i in ids),'support indices')
    need(min(weights)>=0 and sum(weights)==1,'exact normalized nonnegative weights')
    total=[sum(w*Q(rows[i][j]) for i,w in zip(ids,weights)) for j in range(3)]
    need(total[:2]==[0,0] and total[2]<=0,'exact strict Farkas identity')
    need(total[2]==Q(cert['weighted_constant']),'weighted constant value')
    return len(ids)


def verify_witness(rows,point):
    point=tuple(map(Q,point))
    values=[Q(row[0])*point[0]+Q(row[1])*point[1]+Q(row[2]) for row in rows]
    need(min(values)>0,'strict exact witness')
    return min(values)


def kernel_case(rows,bounded=True):
    # Keep integer inputs for selected controls: public helpers must preserve
    # exactness when their caller supplies integers as well as Fractions.
    expected=strict_fm(rows)
    cert=tested.strict_farkas(rows)
    if expected:need(cert is None,'no false strict circuit')
    else:need(cert is not None,'complete support-three alternative');verify_circuit(rows,cert)
    if bounded:
        witness=tested.interior_witness(rows)
        if expected:need(witness is not None,'bounded feasible witness');verify_witness(rows,witness)
        else:need(witness is None,'no boundary-only strict witness')
    return expected


def main():
    path='certificates/det5_horizontal_projection.json';cert=read(path)
    need(cert['base_parameters']==list(map(str,BASE)) and cert['eliminated_variables']==['a','tau'],'parameter order')
    need(cert['coefficient_order']==['a','tau','constant'] and cert['all_rows_strict_positive'],'strict coefficient convention')
    need(cert['base_domain']==['0<=p<1','0<=q<1','C>0','E>0','C+E<1'],'base domain')
    need(cert['threshold']=='183/500' and cert['global_width_target']=='17/5','global target metadata')
    need(set(cert['orders'])=={'lt','gt'},'both original orders')
    need(DELTA==s.Rational(34728093,250000000),'volume determinant constant')
    for source,digest in cert['sources'].items():need(sha(source)==digest,'source proof binding')
    allrows={};identities=0
    for order in ('lt','gt'):
        options=physical_pieces(order)
        patterns=list(product(*(range(len(v)) for v in options)))
        need(len(patterns)==12,'exact twelve branches')
        stored=cert['orders'][order]
        need(len(stored)==12 and [tuple(v['pattern']) for v in stored]==patterns,'complete unique branch patterns')
        for branch,pattern in zip(stored,patterns):
            expected=expected_rows(order,pattern);allrows[order,pattern]=expected
            need(len(branch['rows'])==12,'all twelve branch inequalities')
            for saved,(label,co) in zip(branch['rows'],expected):
                need(saved['label']==label and len(saved['coefficients'])==3,'row labels and coefficient coverage')
                for terms,wanted in zip(saved['coefficients'],co):
                    need(s.expand(decode(terms)-wanted)==0,'independent physical polynomial coefficient');identities+=1
            generated=tested.coefficient_rows(order,pattern)
            need(all(r['label']==label and all(s.expand(c-w)==0 for c,w in zip(r['coefficients'],co)) for r,(label,co) in zip(generated,expected)),'generator matches independently reconstructed rows')
    controls_path='results/det5_horizontal_projection_controls.json';controls=read(controls_path)
    need(controls['certificate_sha256']==sha(path),'frozen coefficient certificate binding')
    need(len(controls['controls'])==10,'ten archived base controls')
    wanted_bases=[('1/4','1/4','1/4','1/4'),('1/8','1/2','1/8','3/4'),('0','1/2','1/10','4/5'),('1/3','1/3','2/5','1/2'),('1/2','1/2','1/4','1/3')]
    need([(tuple(v['base']),v['order']) for v in controls['controls']]==[(b,o) for b in wanted_bases for o in ('lt','gt')],'exact control coverage')
    outcome_counts={'feasible':0,'infeasible':0};support_counts={1:0,2:0,3:0};checked_controls=[]
    for control in controls['controls']:
        base=tuple(map(Q,control['base']));order=control['order']
        need(0<=base[0]<1 and 0<=base[1]<1 and base[2]>0 and base[3]>0 and base[2]+base[3]<1,'admissible control base')
        patterns=[tuple(v['pattern']) for v in cert['orders'][order]]
        need(len(control['branches'])==12 and [tuple(r['pattern']) for r in control['branches']]==patterns,'all archived branch controls')
        statuses=[]
        for branch,pattern in zip(control['branches'],patterns):
            rows=rational_rows(allrows[order,pattern],base);feasible=strict_fm(rows)
            need((branch['status']=='feasible')==feasible,'independent strict Fourier-Motzkin classification')
            statuses.append(branch['status']);outcome_counts[branch['status']]+=1
            if feasible:
                slack=verify_witness(rows,(branch['a'],branch['tau']))
                need(slack==Q(branch['minimum_strict_slack']),'exact saved minimum slack')
            else:support_counts[verify_circuit(rows,branch['certificate'])]+=1
        need(control['status']==('feasible' if 'feasible' in statuses else 'infeasible'),'aggregate base classification')
        checked_controls.append({'base':control['base'],'order':order,'status':control['status'],'branches':12})
    probe_path='results/det5_horizontal_projection_base_probe.json'
    probe=read(probe_path);need(len(probe['controls'])==22,'twenty-two frozen additional bases')
    candidates=[]
    for pp,qq,cc,ee in product(map(Q,['0','1/4','1/2','3/4']),map(Q,['0','1/4','1/2','3/4']),map(Q,['1/16','1/8','1/4','3/8']),map(Q,['1/2','5/8','3/4','7/8'])):
        aa=cc+pp*ee;bb=qq*cc+ee;ss=cc+ee;ll=1-pp*qq
        if ss>=1 or ll*ee<=2*Q(183,500)*qq:continue
        if not(bb>Q(183,200) or bb-aa>Q(83,200)):continue
        candidates.append((pp,qq,cc,ee))
    need([(tuple(map(Q,v['base'])),v['order']) for v in probe['controls']]==[(b,'lt') for b in candidates[:22]],'complete initial selected-grid prefix')
    probe_counts={'feasible':0,'infeasible':0};probe_found=[]
    for control in probe['controls']:
        base=tuple(map(Q,control['base']));order=control['order'];patterns=[tuple(v['pattern']) for v in cert['orders'][order]]
        need(len(control['branches'])==12 and [tuple(v['pattern']) for v in control['branches']]==patterns,'all additional twelve branches')
        any_feasible=False
        for branch,pattern in zip(control['branches'],patterns):
            rows=rational_rows(allrows[order,pattern],base);feasible=strict_fm(rows)
            need((branch['status']=='feasible')==feasible,'additional independent Fourier-Motzkin classification')
            any_feasible |= feasible;probe_counts[branch['status']]+=1
            if feasible:need(verify_witness(rows,(branch['a'],branch['tau']))==Q(branch['minimum_strict_slack']),'additional exact witness and slack')
            else:verify_circuit(rows,branch['certificate'])
        need(control['status']==('feasible' if any_feasible else 'infeasible'),'additional aggregate status')
        if not any_feasible:probe_found.append({'order':order,'base':control['base']})
    need(len(probe_found)==4 and probe_found==probe['new_infeasible_after_cuts'],'four exact additional point obstructions')
    unit=[(1,0,0),(-1,0,1),(0,1,0),(0,-1,1)]
    named=[('unit square',unit,True),('zero atom',unit+[(0,0,0)],True),('negative constant',unit+[(0,0,-1)],True),('positive constant',unit+[(0,0,3)],True),
           ('closed segment only',unit+[(-1,0,0)],True),('closed point only',unit+[(-1,0,0),(0,-1,0)],True),
           ('integer nonterminating pair',[(2,0,0),(-1,0,0)],False),('parallel feasible',[(2,0,1),(3,0,-1)],False),
           ('positive cofactor triangle',[(1,0,0),(0,1,0),(-1,-1,0)],False),('negative cofactor triangle',[(0,1,0),(1,0,0),(-1,-1,0)],False),
           ('rank-two zero-cofactor triple',[(1,0,0),(-1,0,0),(0,1,1)],False),('negative-constant triangle',[(1,0,-1),(0,1,-1),(-1,-1,1)],False)]
    named_reports=[{'name':name,'strict_feasible':kernel_case(rows,bounded)} for name,rows,bounded in named]
    rng=random.Random(533102026);random_count=160
    for _ in range(random_count):
        rows=[tuple(map(Q,r)) for r in unit]+[tuple(Q(rng.randrange(-3,4)) for _ in range(3)) for j in range(rng.randrange(1,6))]
        kernel_case(rows,True)
    # This fixture checks that the a=1 endpoint
    # can move inward while every other original inequality stays strict.
    endpoint_rows=[(1,0,0),(0,1,0),(-Q(1,4),-1,1),(1,-1,Q(1,2))]
    endpoint=(Q(1),Q(1,4));verify_witness(endpoint_rows,endpoint)
    epsilon=min([Q(1,2)]+[(aa*endpoint[0]+bb*endpoint[1]+cc)/(2*aa) for aa,bb,cc in endpoint_rows if aa>0])
    moved=(1-epsilon,endpoint[1]);verify_witness(endpoint_rows+[(-1,0,1)],moved)
    # Literal certificate corruption must be rejected by the independent verifier.
    pair=tested.strict_farkas([(Q(2),Q(0),Q(0)),(Q(-1),Q(0),Q(0))])
    bad=deepcopy(pair);bad['weights'][0]=str(Q(bad['weights'][0])+Q(1,10))
    rejected=False
    try:verify_circuit([(Q(2),Q(0),Q(0)),(Q(-1),Q(0),Q(0))],bad)
    except ValueError:rejected=True
    need(rejected,'mutated weight rejected')
    result={'status':'PASS','scope':'Independent strict projection coefficient and exact-control audit. Four-dimensional continuous feasibility remains unresolved; no solver calls.',
            'certificate_sha256':sha(path),'control_archive_sha256':sha(controls_path),'symbolic_coefficient_identities':identities,'branches_per_order':12,'strict_rows_per_branch':12,
            'controls':checked_controls,'archived_branch_outcomes':outcome_counts,'additional_probe_sha256':sha(probe_path),'additional_probe_bases':22,'additional_probe_branch_outcomes':probe_counts,'additional_point_obstructions':probe_found,'infeasibility_support_sizes':support_counts,'named_degenerate_kernel_controls':named_reports,
            'random_bounded_kernel_controls':random_count,'a_equals_one_strictification_fixture':{'epsilon':str(epsilon),'moved_point':list(map(str,moved))},'mutated_weight_rejected':True,
            'solver_queries_run':0,'optimization_solver_calls_run':0}
    (ROOT/'results/det5_horizontal_projection_validation.json').write_text(json.dumps(result,indent=2)+'\n');print('HORIZONTAL_PROJECTION_INDEPENDENT=PASS')

if __name__=='__main__':main()
