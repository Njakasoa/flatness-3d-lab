"""Classify and optionally externally replay lexical slices of three CPC proofs.

Only existing refutations are used. No SMT solver calls or old archive writes.
"""
from collections import Counter
from pathlib import Path
import argparse
import gzip
import json
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
import replay_det5_conditional_width_bounds as B
from check_height_ethos import emit,real_reference,proof_body,checker,revision,ETHOS_REV,CVC5_REV
from experiments.det5_cpc_dependency_slice import slice_proof

OUTPUT='results/det5_corner_proof_slice.json'
DIR='certificates/det5_corner_slices'


def labels(C):
    out=[f'F_positive:{i},{j}' for i in range(4) for j in range(4) if i!=j]
    out += [f'column_sum:{j}' for j in range(4)]
    out += ['offset_nonnegative','offset_plus_gap_upper_one','gap_positive','gap_upper_5_17']
    out += ['gauge:'+','.join(map(str,v)) for v in sorted(B.VECTORS)]
    out += ['guard:'+','.join(map(str,v)) for v in C['guards']]
    for i in (1,2):
        out += [f'height_lower:{i}',f'height_upper:{i}']
        for j in range(4):
            if i!=j:
                out += [f'product_envelope:{i},{j}:{s}' for s in ('lower_F','upper_F','lower_affine','upper_affine')]
    out += [f'height_contact_equation:{j}' for j in range(4)]
    return out


def expanded_assumptions(cmds):
    env={};stack=[];result={}
    def expand(e):
        if isinstance(e,list):return [expand(x) for x in e]
        return env.get(e,e)
    for index,c in enumerate(cmds):
        if c[0]=='define':
            B.need(c[2]==[],'nullary CPC definitions only')
            env[c[1]]=expand(c[3])
        elif c[0]=='assume':result[index]=expand(c[2])
        elif c[0]=='assume-push':stack.append(env.copy())
        elif c[0]=='step-pop':env=stack.pop()
    B.need(not stack,'balanced lexical definitions')
    return result


def immutable_write(path,data):
    path=ROOT/path
    if path.exists():B.need(path.read_bytes()==data,'existing slice artifact differs; preserve it')
    else:path.write_bytes(data)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--ethos',type=Path)
    ap.add_argument('--ethos-source',type=Path)
    ap.add_argument('--cvc5-source',type=Path)
    a=ap.parse_args()
    check=any((a.ethos,a.ethos_source,a.cvc5_source))
    if check:
        B.need(all((a.ethos,a.ethos_source,a.cvc5_source)),'all three checker paths required')
        B.need(revision(a.ethos_source)==ETHOS_REV and revision(a.cvc5_source)==CVC5_REV,'pinned checker and signature revisions')
    C=next(c for c in B.read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index']==5)
    sharp=B.read('results/det5_y_corner_gauge_sharp_probe.json')
    rows=[('beta_4_23',next(r for r in sharp['queries'] if r['beta']=='4/23'),sharp['box'],'results/det5_y_corner_gauge_sharp_probe.json')]
    for tag,path in [('lower_2_3','results/det5_y_corner_enlarged.json'),('lower_3_5','results/det5_y_corner_enlarged_3_5.json')]:
        row=B.read(path);rows.append((tag,row,row['box'],path))
    (ROOT/DIR).mkdir(exist_ok=True)
    result={'status':'ANALYZED','scope':'Exact lexical dependency slices and independent classification of original input assertions. Removed-premise conclusions require each slice to pass the external checker against its actual subset reference.',
            'proofs':[],'solver_queries_run':0,'proof_kernel_calls_run':0}
    for tag,row,box,receipt in rows:
        B.audit_row(C,row,[0,3],box,B.Q(row['beta']))
        smt=(ROOT/row['input_path']).read_text()
        source_commands=B.parse(smt)
        assertions=[c[1] for c in source_commands if c[0]=='assert']
        variables,expected=B.expected(C,[0,3],box,B.Q(row['beta']))
        names=labels(C);B.need(len(expected)==len(names)==82,'independent labels cover full source statement')
        groups={}
        for e,name in zip(expected,names):groups.setdefault(B.canon(e),[]).append(name)
        source_forms={B.canon(e):e for e in assertions}
        raw=gzip.decompress((ROOT/row['proof_path']).read_bytes())
        cmds,nodes,used,kept,assumptions=slice_proof(raw)
        expansion=expanded_assumptions(cmds)
        retained=[];unused=[];wanted=set()
        for index,c in assumptions:
            e=expansion[index];key=B.canon(e)
            B.need(key in source_forms and key in groups,'CPC assumption independently matches input')
            info={'id':c[1],'command_index':index,'groups':groups[key],'original_assertion':emit(source_forms[key])}
            (retained if index in used else unused).append(info)
            if index in used:wanted.add(key)
        B.need(len(assumptions)==len(assertions)==82,'all original assertions accounted for')
        subset=[c for c in source_commands if c[0]!='assert' or B.canon(c[1]) in wanted]
        subset_text='\n'.join(emit(c) for c in subset)+'\n'
        sliced='(\n'+'\n'.join(emit(c) for c in kept)+'\n)\n'
        input_path=f'{DIR}/{tag}.smt2';proof_path=f'{DIR}/{tag}.cpc.gz'
        immutable_write(input_path,subset_text.encode())
        immutable_write(proof_path,gzip.compress(sliced.encode(),mtime=0))
        ref,_,vs=real_reference(subset_text)
        body,_=proof_body(sliced.encode(),vs)
        counts=Counter(g.split(':')[0] for r in retained for g in r['groups'])
        all_used={g for r in retained for g in r['groups']}
        info={'tag':tag,'source_receipt':receipt,'source_receipt_sha256':B.digest((ROOT/receipt).read_bytes()),
              'source_input_path':row['input_path'],'source_input_sha256':row['input_sha256'],
              'source_proof_path':row['proof_path'],'source_proof_sha256':row['proof_sha256'],
              'box':box,'beta':row['beta'],'source_commands':len(cmds),'sliced_commands':len(kept),
              'original_assumptions':len(assumptions),'retained_assumptions':len(retained),'omitted_assumptions':len(unused),
              'retained_group_counts':dict(counts),'used_gauges':[g for g in sorted(all_used) if g.startswith('gauge:')],
              'used_guards':[g for g in sorted(all_used) if g.startswith('guard:')],
              'gap_upper_5_17_used':'gap_upper_5_17' in all_used,
              'retained':retained,'omitted':unused,'input_path':input_path,'input_sha256':B.digest(subset_text.encode()),
              'proof_path':proof_path,'proof_sha256':B.digest(sliced.encode()),
              'compressed_proof_sha256':B.digest((ROOT/proof_path).read_bytes()),'reference_sha256':B.digest(ref.encode())}
        if check:
            with tempfile.TemporaryDirectory(prefix='det5-corner-slice-') as temp:
                p=Path(temp)/'proof.cpc';q=Path(temp)/'reference.smt2'
                p.write_text(body);q.write_text(ref)
                checked=checker(a.ethos,a.cvc5_source,p,q)
                B.need(checked['exit_code']==0 and checked['stdout']=='correct' and not checked['stderr'],'slice passes against actual subset input')
            info['ethos']=checked;result['proof_kernel_calls_run']+=1
        result['proofs'].append(info)
        print(json.dumps({k:info[k] for k in ('tag','retained_assumptions','retained_group_counts','used_gauges','used_guards','gap_upper_5_17_used')},indent=2),flush=True)
    if check:
        result['status']='PASS';result['ethos_revision']=ETHOS_REV;result['cvc5_signature_revision']=CVC5_REV
    destination=ROOT/OUTPUT
    if destination.exists() and B.read(OUTPUT).get('status')=='PASS' and not check:
        print('Existing externally checked analysis preserved.')
    else:destination.write_text(json.dumps(result,indent=2)+'\n')


if __name__=='__main__':main()
