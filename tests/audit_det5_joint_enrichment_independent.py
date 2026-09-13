"""Incremental exact encoding/frontier audit for the 14- and 18-gauge runs.

Uses previously reviewed reconstruction helpers; imports no experiment.
Z3 only parses expressions. No solver queries or UNSAT proof checks.
"""
from copy import deepcopy
from pathlib import Path
import hashlib,json
import z3
from audit_det5_joint_cover_independent import formula,frontier,compare,need
from audit_height_cover_independent import inverse,expect_rejection

ROOT=Path(__file__).resolve().parents[1]
ORBIT1=((1,-1,1),(2,1,1),(3,1,0),(6,1,2))
ORBIT2=((1,1,0),(2,1,0),(3,1,1),(4,1,1))


def read(path):return json.loads((ROOT/path).read_text())
def digest(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

def strengthened_formula(C,S,row,vectors):
    expected=formula(C,S,row)
    expected += [z3.Real('height_gap')>z3.RealVal('2042829/50000000'),
                 z3.Real('U_gap')>z3.RealVal('2042829/100000000')]
    F=[[z3.RealVal(0) for _ in range(4)] for _ in range(4)]
    for j in range(4):
        ids=[i for i in range(4) if i!=j]
        a,b=[z3.Real(f'f{i}{j}') for i in ids[:2]]
        for i,x in zip(ids,(a,b,1-a-b)):F[i][j]=x
    P=C['contact_points'];T=inverse([[1]*4]+[[p[k] for p in P] for k in range(3)])
    for v in vectors:
        l=[sum(x*y for x,y in zip(r,(0,*v))) for r in T]
        values=[sum(F[i][j]*z3.RealVal(str(l[j])) for j in range(4)) for i in range(4)]
        expected.append(z3.Or(*[sum(values[i] for i in range(4) if mask&(1<<i))>z3.RealVal('183/500') for mask in range(1,15)]))
    return expected


def prefix(child,parent,count):
    need(child['volume_gap_seed']['query_count']==count,'seed query count')
    need(len(parent['queries'])==count,'parent query count')
    need(child['queries'][:count]==parent['queries'],'unchanged inherited query prefix')


def main():
    pinned={
      'tests/audit_det5_joint_round2_independent.py':'8247a3fa1c7f42691101e9a6b466775ef53407e79562975be3f4f81ecfa5035d',
      'results/det5_joint_round2_encoding_validation.json':'91d57a35732afacfa74351dd5d91827a92d0b0047c445dba96bf77dddcf87c15',
      'results/det5_joint_round2.json':'fcfc7eda2099eb72525d382ff82e315f7acd46e0259e05824b58afa8d9a0c56b',
      'tests/audit_det5_joint_cover_independent.py':'bc00ce9350e922532ab99cdd052b8c09c82095160c482cefbb55f5f9ef93e75b',
      'tests/audit_det5_height_independent.py':'c6d1f03facfff8f588dd2bceeb035d290b6203fa3e3fad30348c6d6e57049c4b',
      'tests/audit_height_cover_independent.py':'74b0dec05d07435223b95af6476d2d7651e715b5d681e260b91be076c9789154',
      'results/det5_joint_cover_encoding_validation.json':'ca0f9370e7497e78a450d14286a068b779caf79fd015975afd3ac17500eb6a98'}
    for path,sha in pinned.items():need(digest(path)==sha,'unchanged reviewed dependency: '+path)
    prior=read('results/det5_joint_round2_encoding_validation.json')
    need(prior['status']=='PASS' and prior['prior_encodings_bound']==514 and prior['new_encodings_checked']==322,'previous audit scope')
    oldreceipt=read('results/det5_joint_cover_encoding_validation.json')
    need(oldreceipt['status']=='PASS' and oldreceipt['query_count']==514,'older audited prefix')
    priorinputs=oldreceipt['inputs']+prior['fresh_inputs']
    for entry in priorinputs:need(digest(entry['path'])==entry['sha256'],'previous formula unchanged')
    C=next(c for c in read('certificates/nonunimodular_observer_guards.json')['classes'] if c['class_index']==5)
    S=next(c for c in read('results/two_vector_class_scan.json')['classes'] if c['class_index']==5)
    round2=read('results/det5_joint_round2.json');rootpath='results/det5_joint_enriched_roots.json';roots=read(rootpath)
    enrichedpath='results/det5_joint_enriched_cover.json';shortpath='results/det5_joint_short_gauges.json'
    enriched=read(enrichedpath);short=read(shortpath)
    need(roots['source_path']=='results/det5_joint_round2.json' and roots['source_sha256']==digest(roots['source_path']),'root source binding')
    need(set(map(tuple,roots['extra_gauge_vectors']))==set(ORBIT1),'root added gauge set')
    key=lambda r:(tuple(r['Y_extrema']),tuple(r['U_extrema']))
    openkeys={key(c) for c in round2['charts'] if not c['complete_cover']}
    need(len(roots['queries'])==9 and len({key(r) for r in roots['queries']})==9 and {key(r) for r in roots['queries']}==openkeys,'exactly nine formerly open roots')
    fresh=[]
    def checkrow(row,vectors):
        p=row['path'];need(digest(p)==row['input_sha256'],'fresh input hash')
        compare(strengthened_formula(C,S,row,vectors),list(z3.parse_smt2_file(str(ROOT/p))))
        fresh.append({'path':p,'sha256':digest(p),'additional_gauge_count':len(vectors)})
        if len(fresh)%25==0:print('PASS new enriched encodings: '+str(len(fresh)),flush=True)
    for row in roots['queries']:
        need(row['box']==[['0','1'] for _ in range(4)],'whole root box')
        need(row['status'] in ('sat','unsat','unknown'),'root status label')
        checkrow(row,ORBIT1)
    reports=[]
    for path,data,parent,count,total,vectors in [
            (enrichedpath,enriched,round2,835,849,ORBIT1),
            (shortpath,short,enriched,849,953,ORBIT1+ORBIT2)]:
        prefix(data,parent,count)
        seed=data['volume_gap_seed'];need(digest(seed['path'])==seed['sha256'],'inherited source file hash')
        need(read(seed['path'])==parent,'seed identifies actual parent archive')
        need(len(data['queries'])==total,'frozen archive query count')
        need(set(map(tuple,data['extra_gauge_vectors']))==set(vectors),'archive added gauge set')
        need(data['linear_volume_gap_cuts']['Y']=='2042829/50000000' and data['linear_volume_gap_cuts']['U']=='2042829/100000000','gap metadata')
        for row in data['queries'][count:]:
            need(row['volume_gap_cuts'] is True,'fresh gap marker');checkrow(row,vectors)
        charts=frontier(data,C)
        reports.append({'path':path,'sha256':digest(path),'query_count':total,'inherited_query_count':count,
                        'new_formulas_checked':total-count,'complete_charts_from_archived_labels':sum(c['complete_cover'] for c in charts),
                        'pending_boxes':sum(c['pending_leaves'] for c in charts),'frontier_charts_checked':len(charts)})
    need(short['total_gauge_count']==18 and short['intrinsic_gauge_cutoff']=='6/5','18-gauge metadata')
    row=short['queries'][849];expected=strengthened_formula(C,S,row,ORBIT1+ORBIT2)
    actual=list(z3.parse_smt2_file(str(ROOT/row['path'])))
    mutations=[expect_rejection('missing new orbit inequality',lambda:compare(expected,actual[:-1])),
               expect_rejection('wrong stronger Y gap',lambda:compare(expected,actual+[z3.Real('height_gap')>z3.RealVal('1/10')]))]
    wrong=deepcopy(enriched);wrong['queries'][0]['box'][0][1]='1/2'
    mutations.append(expect_rejection('modified inherited prefix',lambda:prefix(wrong,round2,835)))
    wrong2=deepcopy(short);next(c for c in wrong2['charts'] if c['pending_leaves'])['pending_leaves'].pop()
    mutations.append(expect_rejection('omitted pending box',lambda:frontier(wrong2,C)))
    need(len(fresh)==127,'9 roots plus14 enriched plus104 short-gauge formulas')
    out={'status':'PASS','scope':'Incremental exact assertion reconstruction, immutable prefix/input binding, and all36-chart frontier reconstruction for each continuation. Archived solver status labels are not proved; no class exclusion or UNSAT proof claim.',
         'prior_encoding_files_hash_bound':len(priorinputs),'new_encodings_checked':len(fresh),'new_enriched_roots_checked':9,
         'root_archive':{'path':rootpath,'sha256':digest(rootpath)},'archives':reports,'fresh_inputs':fresh,
         'pinned_review_dependencies':pinned,'rejected_mutations':mutations,'solver_queries_run':0,'unsat_proofs_checked':0}
    (ROOT/'results/det5_joint_enrichment_encoding_validation.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('status','prior_encoding_files_hash_bound','new_encodings_checked','archives','solver_queries_run','unsat_proofs_checked')},indent=2))

if __name__=='__main__':main()
