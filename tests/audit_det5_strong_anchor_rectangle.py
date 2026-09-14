"""Independent full-matrix rectangle and proof-reference audit; no solver calls."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import gzip,hashlib,json,re
import sympy as s
import z3
from audit_det5_quadratic_chart_independent import as_z3,forms
from check_det5_fiber_proofs import reference
from check_height_ethos import sexps,emit,ETHOS_REV,CVC5_REV
ROOT=Path(__file__).resolve().parents[1]
VECTORS=[(0,0,1),(0,1,-1),(0,1,0),(1,0,0),(1,0,1),(2,0,1),(3,0,1),(5,0,2),(5,1,1),(5,1,2),(1,-1,1)]
BOX=[['0','1/256'],['31/256','33/256']]
BETA=s.Rational(183,500)
LOWER=s.Rational(2042829,50000000)

def need(v,m):
    if not v:raise ValueError(m)
def read(p):return json.loads((ROOT/p).read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
def sha(p):return digest((ROOT/p).read_bytes())

def reconstruct(C,box=BOX,beta=BETA,lower=LOWER):
    P=s.Matrix([[1]*4]+[[v[k] for v in C['contact_points']] for k in range(3)])
    inv=P.inv();need(abs(P.det())==5,'contact determinant')
    F=s.Matrix(4,4,lambda i,j:0 if i==j else s.Symbol(f'F_{i}_{j}'))
    q=s.Matrix([0,s.Symbol('q_1'),s.Symbol('q_2'),1])
    offset,gap=z3.Reals('offset gap')
    expected=[as_z3(F[i,j])>0 for i in range(4) for j in range(4) if i!=j]
    expected.extend(as_z3(sum(F[i,j] for i in range(4)))==1 for j in range(4))
    expected.extend([offset>=0,offset+gap<=1,gap>0,gap<z3.RealVal('5/17')])
    for v in VECTORS:
        image=F*inv*s.Matrix([0,*v])
        expected.append(z3.Or(*[as_z3(sum(image[i] for i in range(4) if mask&(1<<i)))>as_z3(beta) for mask in range(1,15)]))
    for v in C['guards']:
        image=F*inv*s.Matrix([1,*v])
        expected.append(z3.Or(*[as_z3(value)<=0 for value in image]))
    for i,(lo,hi) in zip((1,2),box):
        lo,hi=map(s.Rational,(lo,hi));qi=as_z3(q[i])
        expected.extend([qi>=as_z3(lo),qi<=as_z3(hi)])
        for j in range(4):
            if i==j:continue
            p=z3.Real(f'product_{i}_{j}');f=as_z3(F[i,j])
            expected.extend([p>=as_z3(lo)*f,p<=as_z3(hi)*f,p>=qi+as_z3(hi)*f-as_z3(hi),p<=qi+as_z3(lo)*f-as_z3(lo)])
    for j in range(4):
        total=sum(as_z3(F[i,j]) if i==3 else z3.Real(f'product_{i}_{j}') for i in range(4) if i!=j and i!=0)
        expected.append(total==offset+(gap if C['contact_points'][j][1] else 0))
    expected.append(gap>as_z3(lower))
    variables={str(F[i,j]) for i in range(4) for j in range(4) if i!=j}|{'q_1','q_2','offset','gap'}|{f'product_{i}_{j}' for i in(1,2) for j in range(4) if i!=j}
    return variables,expected


def audit_reference(text):
    converted,variables,count=reference(text)
    cmds=sexps(converted)
    # Independently decode the Ethos Real numeral tokens back into standard SMT.
    def standard(node):
        if isinstance(node,str):
            if re.fullmatch(r'[0-9]+/1',node):return node[:-2]
            return node
        return [standard(v) for v in node]
    returned='\n'.join(emit(standard(c)) for c in cmds)
    original=list(z3.parse_smt2_string(text));normalized=list(z3.parse_smt2_string(returned))
    need(count==len(original)==len(normalized),'all reference assertions preserved')
    need(all(forms([a])==forms([b]) for a,b in zip(original,normalized)),'each reference premise independently equivalent')
    need(not any(c[0]=='set-info' for c in cmds),'metadata removed without removing premises')
    return {'reference_sha256':digest(converted.encode()),'assertions':count,'variables':len(variables)}


def main():
    path='results/det5_strong_anchor_rectangle.json';row=read(path)
    C=next(c for c in read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index']==5)
    need(C['contact_points']==[[0,0,0],[5,1,2],[0,1,0],[0,0,1]],'exact contacts')
    need(len(C['guards'])==len(set(map(tuple,C['guards'])))==20,'twenty distinct guards')
    need(row['extrema']==[0,3] and row['box']==BOX and row['beta']=='183/500' and row['target']=='17/5' and row['gap_lower']==str(LOWER),'exact rectangle metadata')
    need(row['gauge_vectors']==list(map(list,VECTORS)),'eleven physical gauges')
    variables,expected=reconstruct(C)
    raw=(ROOT/row['input_path']).read_bytes();need(digest(raw)==row['input_sha256'],'input hash')
    actual=list(z3.parse_smt2_string(raw.decode()))
    declarations=re.findall(r'\(declare-fun\s+(\S+)\s+\(\)\s+Real\)',raw.decode())
    need(len(declarations)==22 and set(declarations)==variables,'exact variable set')
    need(len(actual)==len(expected)==84,'all 84 assertions')
    need(forms(actual)==forms(expected),'entire independently reconstructed linear relaxation')
    need(forms(actual)!=forms(expected[:-1]),'missing global-volume lower gap rejected')
    need(forms(actual)!=forms(reconstruct(C,beta=s.Rational(37,102))[1]),'wrong weaker gauge threshold rejected')
    need(forms(actual)!=forms(expected[:30]+expected[31:]),'missing eleventh physical gauge rejected')
    need(forms(actual)!=forms(reconstruct(C,box=[['0','1/256'],['31/256','1/8']])[1]),'altered rectangle endpoint rejected')
    need(s.Rational(5,6)*BETA**3==LOWER,'volume-to-width lower gap constant')
    need(s.Rational(17,5)*(1-BETA)==s.Rational(5389,2500),'ACMS rational threshold')
    need(s.Rational(4,3)<(s.Rational(5389,2500)-1)**2,'strict radical bound')
    # Closed-interval separation proves the whole rectangle, including endpoints,
    # is disjoint from each earlier certified Y rectangle.
    old=read('results/det5_class5_y_cvc5_validation.json')
    boxes=[r['box'] for r in old['leaves'] if r['extrema']==[0,3]]+[read('results/det5_y_corner_enlarged_3_5.json')['box']]
    need(len(boxes)==8,'eight older excluded boxes')
    separations=[]
    for oldbox in boxes:
        axes=[i for i in range(2) if Q(BOX[i][1])<Q(oldbox[i][0]) or Q(oldbox[i][1])<Q(BOX[i][0])]
        need(bool(axes),'entire new rectangle outside old closed union')
        separations.append({'old_box':oldbox,'strictly_separating_axes':axes})
    Llower=(s.Rational(31,256)-s.Rational(1,256))/s.Rational(33,256)
    need(Llower==s.Rational(10,11) and Llower>s.Rational(49,1500),'outside quantitative diagonal band')
    area=s.Rational(1,256)*s.Rational(2,256);need(area==s.Rational(1,32768),'new exact height area')
    refaudit=audit_reference(raw.decode())
    controls=[]
    for p in ['results/det5_fiber_anchor.smt2','results/det5_fiber_control_full_target.smt2']:
        controls.append({'input_path':p,**audit_reference((ROOT/p).read_text())})
    synthetic='''(set-logic QF_LRA)
(declare-fun x () Real)(declare-fun y () Real)(declare-fun z () Real)
(assert (let ((u (+ x (/ 1 3)))) (let ((ok (> u y))) (or (not ok) (= u z)))))
(assert (let ((x y)) (let ((y z)) (< x y))))
(assert false)
'''
    controls.append({'input_path':'synthetic nested/Boolean/shadowing lets and false',**audit_reference(synthetic)})
    proofpath='results/det5_strong_anchor_rectangle_ethos_validation.json';proof=read(proofpath)
    need(proof['status']=='PASS' and row['status']=='unsat','existing externally checked refutation')
    need(proof['input_sha256']==row['input_sha256'] and proof['proof_sha256']==row['proof_sha256'],'external receipt bound to exact artifacts')
    need(digest(gzip.decompress((ROOT/row['proof_path']).read_bytes()))==row['proof_sha256'],'actual proof payload hash')
    need(proof['reference_sha256']==refaudit['reference_sha256'] and proof['assertions_preserved']==84 and set(proof['variables'])==variables,'exact normalized proof reference')
    need(proof['ethos']=={'exit_code':0,'stdout':'correct','stderr':''} or (proof['ethos']['exit_code']==0 and proof['ethos']['stdout']=='correct' and proof['ethos']['stderr']==''),'external checker success')
    need(proof['ethos_revision']==ETHOS_REV and proof['cvc5_signature_revision']==CVC5_REV and proof['unrelated_assumption_rejected'],'pinned checker and negative control')
    receipt={'status':'PASS','scope':'One continuous Y[0,3] rectangle excluded under hollow global width >17/5, via exact necessary full-matrix relaxation and externally checked refutation. No whole-class or global-bound conclusion.',
             'source_archive_sha256':sha(path),'input_path':row['input_path'],'input_sha256':row['input_sha256'],'proof_path':row['proof_path'],'proof_sha256':row['proof_sha256'],
             'external_proof_receipt_sha256':sha(proofpath),'assertions':84,'variables':22,'gauges':11,'guards':20,'lifted_products':6,'mccormick_inequalities':24,
             'box':BOX,'beta':str(BETA),'gap_lower':str(LOWER),'new_height_area':str(area),'old_union_separations':separations,'analytic_diagonal_L_lower':str(Llower),
             'reference_audit':refaudit,'reference_controls':controls,'mutation_controls':['missing lower gap','weaker beta','missing eleventh gauge','altered height endpoint'],
             'solver_queries_run':0,'proof_kernel_calls_run':0}
    (ROOT/'results/det5_strong_anchor_rectangle_validation.json').write_text(json.dumps(receipt,indent=2)+'\n');print('STRONG_ANCHOR_RECTANGLE_INDEPENDENT=PASS')

if __name__=='__main__':main()
