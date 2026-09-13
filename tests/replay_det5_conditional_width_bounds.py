"""Stdlib-only exact input/constant audit for conditional d5 width bounds.

Independently reconstructs full-matrix SMT assertions, binds existing proof
receipts, and checks geometric subdomains. Does not rerun solvers or Ethos.
"""
from fractions import Fraction as Q
from pathlib import Path
import gzip,hashlib,json,re
from copy import deepcopy

ROOT=Path(__file__).resolve().parents[1]
VECTORS={(0,0,1),(0,1,-1),(0,1,0),(1,0,0),(1,0,1),(2,0,1),(3,0,1),(5,0,2),(5,1,1),(5,1,2)}

def need(c,m):
    if not c:raise ValueError(m)
def digest(raw):return hashlib.sha256(raw).hexdigest()
def read(p):return json.loads((ROOT/p).read_text())
def inverse(A):
    n=len(A);M=[[Q(x) for x in r]+[Q(i==j) for j in range(n)] for i,r in enumerate(A)]
    for i in range(n):
        p=next(j for j in range(i,n) if M[j][i]);M[i],M[p]=M[p],M[i];t=M[i][i];M[i]=[x/t for x in M[i]]
        for j in range(n):
            if j!=i:
                t=M[j][i];M[j]=[x-t*y for x,y in zip(M[j],M[i])]
    return [r[n:] for r in M]
def plus(xs):return ['+',*xs]
def times(a,b):return ['*',a,b]

def parse(text):
    tokens=re.findall(r'\(|\)|[^\s()]+',re.sub(r';[^\n]*','',text));at=0
    def one():
        nonlocal at
        t=tokens[at];at+=1
        if t!='(':return t
        out=[]
        while tokens[at]!=')':out.append(one())
        at+=1;return out
    out=[]
    while at<len(tokens):out.append(one())
    return out

def poly(e):
    if not isinstance(e,list):
        try:return {'':Q(e)}
        except (ValueError,TypeError):return {str(e):Q(1)}
    op,*args=e
    if op in ('+','-'):
        out={}
        for i,a in enumerate(args):
            sign=-1 if op=='-' and (len(args)==1 or i>0) else 1
            for n,c in poly(a).items():out[n]=out.get(n,Q(0))+sign*c
        return {n:c for n,c in out.items() if c}
    if op=='*':
        out={'':Q(1)}
        for a in args:
            nxt={}
            for n,c in out.items():
                for m,v in poly(a).items():
                    need(not(n and m),'linear arithmetic only');key=n or m;nxt[key]=nxt.get(key,Q(0))+c*v
            out={n:c for n,c in nxt.items() if c}
        return out
    if op=='/':
        den=poly(args[1]);need(set(den)<={''} and den.get('',0)!=0,'constant divisor')
        return {n:c/den[''] for n,c in poly(args[0]).items()}
    raise ValueError('unsupported polynomial operator '+str(op))

def canon(e):
    if e=='true':return True
    if e=='false':return False
    op,*args=e
    if op in ('or','and'):
        vals=[canon(a) for a in args]
        if (True if op=='or' else False) in vals:return op=='or'
        vals=set(v for v in vals if v is not (False if op=='or' else True))
        return (op,tuple(sorted(vals,key=repr)))
    need(op in ('<','<=','>','>=','='),'comparison operator')
    p=poly(['-',args[0],args[1]])
    if op in ('>','>='):op={'>' : '<','>=':'<='}[op];p={n:-c for n,c in p.items()}
    if not p:return op in ('<=','=')
    items=sorted(p.items());scale=abs(items[0][1])
    if op=='=' and items[0][1]<0:scale=-scale
    return op,tuple((n,c/scale) for n,c in items)

def forms(es):return {x for x in map(canon,es) if x is not True}

def expected(C,ext,box,beta):
    P=C['contact_points'];A=inverse([[1]*4]+[[p[k] for p in P] for k in range(3)])
    coords=lambda v,affine=False:[sum(x*y for x,y in zip(r,(int(affine),*v))) for r in A]
    F=[[0 if i==j else f'F_{i}_{j}' for j in range(4)] for i in range(4)]
    free=[i for i in range(4) if i not in ext]
    q=[0 if i==ext[0] else 1 if i==ext[1] else f'q_{i}' for i in range(4)]
    variables={F[i][j] for i in range(4) for j in range(4) if i!=j}|{q[i] for i in free}|{'offset','gap'}|{f'product_{i}_{j}' for i in free for j in range(4) if i!=j}
    e=[['>',F[i][j],0] for i in range(4) for j in range(4) if i!=j]
    e += [['=',plus(F[i][j] for i in range(4)),1] for j in range(4)]
    e += [['>=','offset',0],['<=',plus(['offset','gap']),1],['>','gap',0],['<','gap',Q(5,17)]]
    for v in sorted(VECTORS):
        l=coords(v);values=[plus(times(l[j],F[i][j]) for j in range(4)) for i in range(4)]
        e.append(['or',* [['>',plus(values[i] for i in range(4) if mask&(1<<i)),beta] for mask in range(1,15)]])
    for v in C['guards']:
        l=coords(v,True)
        e.append(['or',*[['<=',plus(times(l[j],F[i][j]) for j in range(4)),0] for i in range(4)]])
    for i,(lo,hi) in zip(free,box):
        lo,hi=Q(lo),Q(hi);e += [['>=',q[i],lo],['<=',q[i],hi]]
        for j in range(4):
            if i==j:continue
            p=f'product_{i}_{j}';f=F[i][j]
            e += [['>=',p,times(lo,f)],['<=',p,times(hi,f)],
                  ['>=',p,plus([q[i],times(hi,f),-hi])],['<=',p,plus([q[i],times(lo,f),-lo])]]
    for j in range(4):
        terms=[F[i][j] if i==ext[1] else f'product_{i}_{j}' for i in range(4) if i!=j and i!=ext[0]]
        rhs='offset' if P[j][1]==0 else plus(['offset','gap'])
        e.append(['=',plus(terms),rhs])
    return variables,e

def audit_row(C,row,ext,box,beta):
    raw=(ROOT/row['input_path']).read_bytes();need(digest(raw)==row['input_sha256'],'input hash')
    commands=parse(raw.decode());declared=set();assertions=[]
    for command in commands:
        if command[0]=='set-logic':need(command==['set-logic','QF_LRA'],'linear logic')
        elif command[0]=='declare-fun':
            need(len(command)==4 and command[2]==[] and command[3]=='Real','real variable declaration');declared.add(command[1])
        elif command[0]=='assert':assertions.append(command[1])
        else:raise ValueError('unexpected SMT command')
    variables,wanted=expected(C,ext,box,beta)
    need(declared==variables and len(declared)==22,'exact 22-variable domain')
    need(forms(assertions)==forms(wanted),'exact independent full-matrix assertion set')
    need(row['status']=='unsat' and row['ethos']['exit_code']==0 and row['ethos']['stdout']=='correct' and row['ethos']['stderr']=='','successful existing proof receipt')
    packed=(ROOT/row['proof_path']).read_bytes();proof=gzip.decompress(packed)
    need(digest(packed)==row['compressed_proof_sha256'] and digest(proof)==row['proof_sha256'],'existing proof hashes')
    return {'input_path':row['input_path'],'input_sha256':digest(raw),'proof_path':row['proof_path'],
            'proof_sha256':digest(proof),'beta':str(beta),'extrema':ext,'box':box,'assertions':len(assertions)}

def main():
    C=next(c for c in read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index']==5)
    oldpath='results/det5_class5_y_cvc5_validation.json';old=read(oldpath)
    need(old['status']=='PASS' and len(old['leaves'])==12 and set(map(tuple,old['gauge_vectors']))==VECTORS,'twelve proved ten-gauge rectangles')
    need(digest((ROOT/old['source_path']).read_bytes())==old['source_sha256'],'frozen source archive')
    audits=[];whole=[];pieces=[]
    for row in old['leaves']:
        ext=row['extrema'];box=row['box'];audits.append(audit_row(C,row,ext,box,Q(37,102)))
        (xl,xh),(yl,yh)=[[Q(x) for x in p] for p in box]
        cap=max(abs(xl-yh),abs(xh-yl)) if ext==[0,1] else 1-min(xl,yl)
        if cap<=Q(5,17):whole.append({'extrema':ext,'node':row['node'],'box':box,'strict_gap_upper_bound':str(cap)})
        if ext==[0,1]:pieces.append({'extrema':ext,'node':row['node'],'box':box,'additional_condition':'abs(q2-q3)<=5/17'})
        elif max(xl,Q(12,17))<=xh and max(yl,Q(12,17))<=yh:
            pieces.append({'extrema':ext,'node':row['node'],'box':[[str(max(xl,Q(12,17))),str(xh)],[str(max(yl,Q(12,17))),str(yh)]],'additional_condition':'none'})
    need({(tuple(r['extrema']),r['node']) for r in whole}=={((0,1),'r00000'),((0,1),'r00110'),((0,3),'r1111')},'three whole automatic-width rectangles')
    need(len(pieces)==7,'seven stronger-bound certified pieces')
    cornerpath='results/det5_y_corner_gauge_threshold.json';corner=read(cornerpath)
    need(corner['extrema']==[0,3] and corner['box']==[['3/4','1']]*2,'corner data')
    for row in corner['queries']:
        if row['status']=='unsat':audits.append(audit_row(C,row,[0,3],corner['box'],Q(row['beta'])))
    refinementpath='results/det5_y_corner_gauge_refinement.json';refinement=read(refinementpath)
    need(refinement['extrema']==[0,3] and refinement['box']==[['3/4','1']]*2 and set(map(tuple,refinement['gauge_vectors']))==VECTORS,'refined corner metadata')
    refined=next(r for r in refinement['queries'] if r['status']=='unsat' and Q(r['beta'])==Q(3,10))
    audits.append(audit_row(C,refined,[0,3],refinement['box'],Q(3,10)))
    control=next(r for r in corner['queries'] if r['status']=='unsat')
    beta=Q(control['beta']);mutations=[]
    wrong_status=deepcopy(control);wrong_status['status']='sat'
    wrong_hash=deepcopy(control);wrong_hash['proof_sha256']='0'*64
    cases=[('residual stronger gauge',lambda:audit_row(C,control,[0,3],corner['box'],Q(37,102))),
           ('overrestricted corner endpoint',lambda:audit_row(C,control,[0,3],[['4/5','1'],['3/4','1']],beta)),
           ('altered proof hash',lambda:audit_row(C,wrong_hash,[0,3],corner['box'],beta)),
           ('unsuccessful proof receipt',lambda:audit_row(C,wrong_status,[0,3],corner['box'],beta))]
    for name,action in cases:
        try:action()
        except ValueError:mutations.append(name)
        else:raise ValueError('accepted mutation: '+name)
    coefficient=1/(1-Q(37,102));need(coefficient==Q(102,65),'general ACMS coefficient')
    need(Q(11,7)-coefficient==Q(1,455),'strict improvement on original reduction coefficient')
    need(Q(4,3)<Q(7,6)**2 and coefficient*Q(13,6)==Q(17,5),'general bound strictly below17/5')
    need(1/(1-Q(1,3))==Q(3,2),'one-third corner coefficient')
    need(1/(1-Q(3,10))==Q(10,7),'three-tenths corner coefficient')
    need(Q(3,2)-Q(10,7)==Q(1,14),'refined corner improves one-third result')
    need(tuple(Q(10,7)*x for x in (Q(1),Q(2,3)))==(Q(10,7),Q(20,21)),'refined exact coefficients in Q(sqrt3)')
    # 3/2*(1+2/sqrt3)=3/2+sqrt3, since 3/sqrt3=sqrt3.
    need(tuple(Q(3,2)*x for x in (Q(1),Q(2,3)))==(Q(3,2),Q(1)),'exact coefficients in Q(sqrt3)')
    result={'status':'PASS','scope':'Independent stdlib full-matrix input reconstruction and existing proof-hash/receipt binding; exact geometric thresholds and ACMS constants. No solver or Ethos reruns. Conditional subdomains only, no whole class exclusion.',
            'old_proof_receipt_sha256':digest((ROOT/oldpath).read_bytes()),'corner_proof_receipt_sha256':digest((ROOT/cornerpath).read_bytes()),'refined_corner_receipt_sha256':digest((ROOT/refinementpath).read_bytes()),
            'inputs_checked':audits,'general_bound':'(102/65)*(1+2/sqrt(3))','coefficient_margin_below_11_over_7':'1/455',
            'automatic_width_whole_rectangles':whole,'general_bound_pieces':pieces,
            'verified_corner_bound_at_one_third':'3/2+sqrt(3)','verified_corner_bound':'(10/7)*(1+2/sqrt(3))','verified_corner_beta':'3/10','rejected_mutations':mutations,'solver_queries_run':0,'proof_kernel_reruns':0}
    (ROOT/'results/det5_conditional_width_bounds_validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','general_bound','automatic_width_whole_rectangles','verified_corner_bound','solver_queries_run')},indent=2))
if __name__=='__main__':main()
