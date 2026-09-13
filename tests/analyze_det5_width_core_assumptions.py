"""Classify source CPC global assumptions by independent input reconstruction.

This read-only proof analysis runs no solver or kernel. Referenced global
assumptions are compared with the separate lexical dependency slice.
"""
import sys,json,gzip,re,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads((ROOT/path).read_text())
def raw(path):return (ROOT/path).read_bytes()
from audit_det5_scaled_pending_transfer_independent import formula
from audit_det5_scaled_frame_independent import canonical,inverse,rat,need,R,TARGET,Q
from itertools import combinations,product
import hashlib
import z3
s=gzip.decompress(raw('certificates/det5_scaled_leaf_contact_width_two.cpc.gz')).decode()
refs=collections.Counter(re.findall(r'@p\d+',s))
defs={m[1]:m[2]for l in s.splitlines()if(m:=re.fullmatch(r'\(define (@t\d+) \(\) (.*)\)',l))}
cache={}
def expandid(m):
 t=m[0]
 if t not in cache:cache[t]=re.sub(r'@t\d+',expandid,defs[t])
 return cache[t]
def smt(expr):
 e=re.sub(r'@t\d+',expandid,expr)
 return re.sub(r'(?<![\w])(-?\d+)/(\d+)(?![\w])',lambda m:'(- (/ '+m[1][1:]+' '+m[2]+'))'if m[1].startswith('-')else'(/ '+m[1]+' '+m[2]+')',e)
decls='\n'.join(l for l in s.splitlines()if l.startswith('(declare-const '))
d=read('results/det5_scaled_pending_transfer.json');row=next(r for r in d['queries']if r['status']=='unsat')
C=next(c for c in read('certificates/nonunimodular_observer_guards.json')['classes']if c['class_index']==5)
S=next(c for c in read('results/two_vector_class_scan.json')['classes']if c['class_index']==5)
expected,F,T,b,lifted,dirs,cuts=formula(C,S,row)
cm={k:{canonical(z3.simplify(c))for c in vv}for k,vv in cuts.items()}

labels={}
def add(label,e):
 key=canonical(z3.simplify(e));labels.setdefault(key,set()).add(label)
for name,es in cuts.items():
 for e in es:add(name,e)
for i,j in product(range(4),repeat=2):
 if i!=j:
  add('F_positive',F[i][j]>0)
  add('F_unit_domain',F[i][j]>=0);add('F_unit_domain',F[i][j]<=1)
for i in range(4):
 add('Y_unit_domain',T[i][1]>=0);add('Y_unit_domain',T[i][1]<=1)
add('Y_target_upper_gap',b<rat(1/TARGET))
add('volume_lower_gap',b>rat(1/R))
P=C['contact_points'];B=inverse([[1]*4]+[[p[k]for p in P]for k in range(3)])
def ell(v,affine=False):return [sum(Q(a)*Q(x)for a,x in zip(r,[int(affine),*v]))for r in B]
old=set(map(tuple,C['primitive_contact_edge_directions']))|{tuple(a['vector'])for a in S['eligible_vectors']}
extra={(1,-1,1),(2,1,1),(3,1,0),(6,1,2),(1,1,0),(2,1,0),(3,1,1),(4,1,1)}
for vs,beta in [(old,Q(37,102)),(old|extra,Q(183,500))]:
 for v in vs:
  c=ell(v);f=[sum(F[i][j]*rat(c[j])for j in range(4))for i in range(4)]
  add('gauge:'+str(beta)+':'+','.join(map(str,v)),z3.Or(*[sum(f[i]for i in range(4)if mask&(1<<i))>rat(beta)for mask in range(1,15)]))
for p in C['guards']:
 c=ell(p,True)
 add('guard:'+','.join(map(str,p)),z3.Or(*[sum(F[i][j]*rat(c[j])for j in range(4))<=0 for i in range(4)]))
W={}
for i,j,k in product(range(4),range(4),range(3)):
 f,t=F[i][j],T[i][k]
 if(i,j,k)not in lifted:W[i,j,k]=z3.simplify(f*t);continue
 fl,fh,tl,th=lifted[i,j,k];w=z3.Real(f'w{i}_{j}_{k}');W[i,j,k]=w
 group='Y_base_envelope'if k==1 else 'horizontal_volume_envelope'
 for e in [w>=rat(fl)*t+rat(tl)*f-rat(fl*tl),w>=rat(fh)*t+rat(th)*f-rat(fh*th),w<=rat(fh)*t+rat(tl)*f-rat(fh*tl),w<=rat(fl)*t+rat(th)*f-rat(fl*th)]:add(group,e)
 add('product_t_domain_Y'if k==1 else 'product_t_domain_volume',t>=rat(tl))
 add('product_t_domain_Y'if k==1 else 'product_t_domain_volume',t<=rat(th))
for j in range(1,4):
 for k in range(3):add('reconstruction_'+str(k),sum(W[i,j,k]-W[i,0,k]for i in range(4))==rat(P[j][k]-P[0][k])*b)
for u in [(0,0,1),(0,1,-1),(1,-2,-2)]:
 h=[sum(u[k]*T[i][k]for k in range(3))for i in range(4)]
 add('extra_lower_width:'+','.join(map(str,u)),z3.Or(*[sign*(h[i]-h[j])>rat(TARGET)*b for i,j in combinations(range(4),2)for sign in(-1,1)]))
# Exact input mapping distinguishes arithmetic term definitions from assumptions.
source_assertions=list(z3.parse_smt2_file(str(ROOT/'results/det5_scaled_leaf_contact_width_two.smt2')))
source_forms={canonical(z3.simplify(e))for e in source_assertions}
assumptions=[];heads=collections.Counter(re.findall(r'^\((?:assume|step|assume-push|step-pop)\s+(@p\d+)\b',s,re.M))
for l in s.splitlines():
 if(m:=re.fullmatch(r'\(assume (@p\d+) (.*)\)',l)):
  need(heads[m[1]]==1,'global assumption identifier not shadowed')
  text=smt(m[2]);e=list(z3.parse_smt2_string(decls+'\n(assert '+text+')'))[0]
  key=canonical(z3.simplify(e));need(key in source_forms,'top assumption matches source input')
  assumptions.append({'id':m[1],'referenced_outside_declaration':refs[m[1]]>1,'reference_occurrences':refs[m[1]]-1,'groups':sorted(labels.get(key,set())),'expanded_SMT':text})
used=[a for a in assumptions if a['referenced_outside_declaration']]
need(len(assumptions)==485 and len(used)==69,'global assumption counts')
need(all(a['groups']for a in used),'every referenced assumption independently classified')
slice_record=read('results/det5_cpc_dependency_slice.json')
need(slice_record['source_sha256']==hashlib.sha256(s.encode()).hexdigest(),'lexical slice source binding')
need(set(slice_record['retained_assumptions'])=={a['id']for a in used},'independent reference census equals lexical dependency core')
counts=collections.Counter(label for a in used for label in a['groups'])
record={'status':'PASS','scope':'Independent classification of syntactically referenced original global assumptions. Actual proof pruning requires external proof checking; an inert declaration is not a needed hypothesis.',
 'source_proof_sha256':hashlib.sha256(s.encode()).hexdigest(),'top_global_assumptions':len(assumptions),'referenced_global_assumptions':len(used),'inert_global_assumptions':len(assumptions)-len(used),
 'reference_census_matches_lexical_core':True,'used_group_memberships':dict(sorted(counts.items())),
 'used_assumptions':used,'unused_assumption_ids':[a['id']for a in assumptions if not a['referenced_outside_declaration']],
 'solver_queries_run':0,'proof_kernel_calls_run':0,
 'caveat':'Group memberships overlap: some Y envelope/domain cuts and volume lower-gap bounds have equivalent copies in later transfer groups. Constant R still appears in four horizontal product bounds.'}
(ROOT/'results/det5_width_core_assumption_analysis.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record[k]for k in ('status','referenced_global_assumptions','inert_global_assumptions','used_group_memberships')},indent=2))
