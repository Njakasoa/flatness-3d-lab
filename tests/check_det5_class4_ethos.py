"""Externally check class-4 CPC proofs with reference-bound official Ethos.

Standard library only. Uses the prior validated framing/Real-numeral adapter.
"""
from pathlib import Path
import argparse,gzip,json,subprocess,tempfile
from check_height_ethos import (ROOT,ETHOS_REV,CVC5_REV,need,sha,revision,
                               real_reference,proof_body,checker)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ethos',type=Path,required=True)
    p.add_argument('--ethos-source',type=Path,required=True)
    p.add_argument('--cvc5-source',type=Path,required=True)
    args=p.parse_args()
    args.ethos=args.ethos.resolve();args.ethos_source=args.ethos_source.resolve();args.cvc5_source=args.cvc5_source.resolve()
    need(revision(args.ethos_source)==ETHOS_REV,'pinned Ethos')
    need(revision(args.cvc5_source)==CVC5_REV,'pinned CPC signatures')
    receipt_path=ROOT/'results/det5_class4_cvc5_validation.json'
    receipt=json.loads(receipt_path.read_text())
    need(receipt['status']=='PASS' and receipt['class_index']==4 and len(receipt['leaves'])==5,'five class-4 refutations')
    config=subprocess.run([str(args.ethos),'--show-config'],text=True,capture_output=True,check=True).stdout.strip()
    need('version 0.2.3' in config,'checker version')
    rows=[];controls=[]
    report={'status':'INCOMPLETE','class_index':4,'checker':{'name':'Ethos','version':'0.2.3','revision':ETHOS_REV,
            'binary_sha256':sha(args.ethos.read_bytes()),'configuration':config},
            'cvc5_signature_revision':CVC5_REV,
            'signature_sha256':{str(f.relative_to(args.cvc5_source)):sha(f.read_bytes()) for f in sorted((args.cvc5_source/'proofs/eo').rglob('*.eo'))},
            'cvc5_receipt_sha256':sha(receipt_path.read_bytes()),
            'adapter_sha256':sha((ROOT/'tests/check_height_ethos.py').read_bytes()),
            'leaves':rows,'controls':controls,
            'reference_binding':'Exact assertion-preserving Real numeral rendering; proof declarations validated and removed, proof streamed on stdin after --reference.',
            'trust_boundary':'Ethos C++ kernel and runtime, official pinned CPC signatures, and validated framing/reference adapter. No trust/sorry steps. Geometric necessity and complete height-orbit coverage are audited separately.',
            'scope':'Class 4 only: five full-unit-square root formulas; no conclusion for class 5.'}
    output=ROOT/'results/det5_class4_ethos_validation.json'
    def save():output.write_text(json.dumps(report,indent=2)+'\n')
    tags=set()
    with tempfile.TemporaryDirectory(prefix='flatness-det5-ethos-') as tmp:
        pr=Path(tmp)/'proof.cpc';ref=Path(tmp)/'reference.smt2'
        for leaf in receipt['leaves']:
            ext=leaf['extrema'];tag=f'4_{ext[0]}_{ext[1]}_r'
            need(leaf['class_index']==4 and leaf['node']=='r' and leaf['status']=='unsat' and tag not in tags,'unique class-4 root');tags.add(tag)
            base=ROOT/'certificates/det5_class4_cvc5'/tag
            smt=base.with_suffix('.smt2').read_bytes();packed=base.with_suffix('.cpc.gz').read_bytes();raw=gzip.decompress(packed)
            need(sha(smt)==leaf['input_sha256'] and sha(raw)==leaf['proof_sha256'] and sha(packed)==leaf['compressed_proof_sha256'],'receipt hash binding')
            adapted,assertions,variables=real_reference(smt.decode());body,counts=proof_body(raw,variables)
            ref.write_text(adapted);pr.write_text(body)
            result=checker(args.ethos,args.cvc5_source,pr,ref)
            rows.append({'leaf':tag,'input_sha256':sha(smt),'proof_sha256':sha(raw),'compressed_proof_sha256':sha(packed),
                         'reference_sha256':sha(adapted.encode()),'assertions':assertions,'proof_commands':counts,
                         'reference_binding':True,'balanced_scopes':True,'final_top_level_false':True,**result});save()
            need(result['exit_code']==0 and result['stdout']=='correct' and not result['stderr'],'Ethos failure: '+tag)
            print(json.dumps({'leaf':tag,'ethos':'correct','seconds':result['elapsed_seconds']}),flush=True)
            if len(rows)==1:
                pr.write_text(body+'\n(assume @fresh_unrelated false)\n')
                r=checker(args.ethos,args.cvc5_source,pr,ref)
                need(r['exit_code']!=0 and 'assumption' in (r['stdout']+r['stderr']).lower(),'reference binding negative control')
                controls.append({'name':'fresh unrelated assumption','rejected':True,**r})
                pos=body.rfind(' false :rule ');need(pos>=0,'explicit final false')
                pr.write_text(body[:pos]+body[pos:].replace(' false :rule ',' true :rule ',1))
                r=checker(args.ethos,args.cvc5_source,pr,ref);need(r['exit_code']!=0,'wrong conclusion rejected')
                controls.append({'name':'final false changed to true','rejected':True,**r})
                last=body.rstrip().rfind('\n')
                try:proof_body(('(\n'+'\n'.join('(declare-const '+v+' Real)' for v in sorted(variables))+'\n'+body[:last]+'\n)').encode(),variables)
                except (ValueError,IndexError):controls.append({'name':'missing final refutation','rejected':True,'checker':'local framing guard'})
                else:raise ValueError('missing final conclusion accepted')
                try:real_reference(smt.decode().replace('() Real)','() Int)',1))
                except ValueError:controls.append({'name':'non-Real reference declaration','rejected':True,'checker':'local reference guard'})
                else:raise ValueError('non-Real reference accepted')
                save()
    need(len(rows)==5 and len(controls)==4,'complete verification')
    report['status']='PASS';report['external_correct']=5;save()
    print(json.dumps({'status':'PASS','external_correct':5,'controls_rejected':4}))


if __name__=='__main__':main()
