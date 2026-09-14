"""Independent exact complement/interval audit of the combined queue; no solvers."""
from copy import deepcopy
from fractions import Fraction as Q
import gzip
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NEW = 'results/det5_combined_residual_queue.json'
OLD = 'results/det5_separated_residual_queue.json'
ANCHOR = 'results/det5_strong_anchor_rectangle.json'
GEOMETRY = 'results/det5_strong_anchor_rectangle_validation.json'
KERNEL = 'results/det5_strong_anchor_rectangle_ethos_validation.json'
OUT = 'results/det5_combined_residual_queue_validation.json'


def read(p): return json.loads((ROOT/p).read_text())
def sha(p): return sha256((ROOT/p).read_bytes()).hexdigest()
def need(v,m):
    if not v: raise AssertionError(m)


def validate(data):
    old,row,geometry,kernel = map(read,(OLD,ANCHOR,GEOMETRY,KERNEL))
    for key,path in [('source_queue',OLD),('new_rectangle_archive',ANCHOR),
                     ('new_rectangle_geometry_audit',GEOMETRY),('new_rectangle_kernel_receipt',KERNEL),
                     ('new_rectangle_proof',row['proof_path'])]:
        need(data[key]=={'path':path,'sha256':sha(path)},'source binding '+key)
    need(row['status']=='unsat' and row['internal_complete_proof_check'],'refutation')
    need(geometry['status']==kernel['status']=='PASS','geometry and kernel PASS')
    need(geometry['source_archive_sha256']==sha(ANCHOR) and geometry['external_proof_receipt_sha256']==sha(KERNEL),'audit bindings')
    need(row['input_sha256']==sha(row['input_path'])==geometry['input_sha256']==kernel['input_sha256'],'input binding')
    need(row['proof_sha256']==sha256(gzip.decompress((ROOT/row['proof_path']).read_bytes())).hexdigest()==geometry['proof_sha256']==kernel['proof_sha256'],'expanded proof binding')
    need(kernel['ethos']['exit_code']==0 and kernel['ethos']['stdout']=='correct' and kernel['ethos']['stderr']=='','kernel success')
    box = [['0','1/256'],['31/256','33/256']]
    need(row['extrema']==[0,3] and row['box']==geometry['box']==box,'closed rectangle')
    need(data['target']==old['target']==row['target']=='17/5' and data['class_index']==5,'true global target')
    need(data['entry_count']==len(data['entries'])==len(old['entries'])==258,'all258 retained')
    need(data['boolean_semantics']==old['boolean_semantics'] and data['coordinate_semantics']==old['coordinate_semantics'],'inherited interpretation')
    expected = [(i,i+1,relation,box[i][endpoint]) for i in range(2) for relation,endpoint in (('<',0),('>',1))]
    amended=[]
    for before,after in zip(old['entries'],data['entries']):
        current=deepcopy(after)
        if before['Y_extrema']==[0,3]:
            clause=current['outside_Y_clauses'].pop()
            need(clause['excluded_closed_Y_box']==box,'exact excluded region')
            need(clause['proof_input_path']==row['input_path'] and clause['proof_receipt_path']==KERNEL and clause['geometry_receipt_path']==GEOMETRY,'clause provenance')
            actual=[(l['free_coordinate'],l['vertex_index'],l['relation'],l['threshold']) for l in clause['literals']]
            need(actual==expected,'full strict complement with exact endpoints')
            amended.append(before['entry_id'])
        need(current==before,'every original entry value and separation constraint preserved')
    need(data['amended_entry_ids']==amended and len(amended)==data['amended_entry_count']==70,'all70 target clauses')
    need(data['unchanged_entry_count']==188 and not data['newly_removed_entries'],'other188 unchanged; no removal')
    # Complete sign-invariant endpoint/open cells for the *new rectangular*
    # complement. This argument does not discretize the quadratic band.
    axes=[]
    for lo,hi in box:
        cuts=sorted({Q(0),Q(1),Q(lo),Q(hi)})
        axes.append(sorted(set(cuts)|{(a+b)/2 for a,b in zip(cuts,cuts[1:])}))
    cells=0
    for point in product(*axes):
        inside=all(Q(lo)<=v<=Q(hi) for v,(lo,hi) in zip(point,box))
        outside=any(point[i]<Q(t) if op=='<' else point[i]>Q(t) for i,_,op,t in expected)
        need(outside==(not inside),'strict complement on every sign-invariant cell')
        cells+=1
    (xl,xh),(yl,yh)=[[Q(v) for v in p] for p in box]
    mingap=yl-xh
    maximum_rhs=Q(49,1500)*yh*(1-xl)
    need(mingap>maximum_rhs and xh<yl,'whole rectangle satisfies prior separated-height lt branch')
    cert=read('results/det5_class5_y_cvc5_validation.json')
    boxes=[r['box'] for r in cert['leaves'] if r['extrema']==[0,3]]
    boxes.append(read('results/det5_y_corner_enlarged_3_5.json')['box'])
    need(len(boxes)==8,'all8 preceding rectangles')
    for previous in boxes:
        need(any(Q(b)<lo or hi<Q(a) for (a,b),(lo,hi) in zip(previous,((xl,xh),(yl,yh)))),'whole anchor outside old closed union')
    containing=[]
    for entry in old['entries']:
        if entry['Y_extrema']!=[0,3]:continue
        if not all(Q(a)<=lo<=hi<=Q(b) for (a,b),(lo,hi) in zip(entry['box'],((xl,xh),(yl,yh)))):continue
        for clause in entry['outside_Y_clauses']:
            need(any(((xl,xh),(yl,yh))[l['free_coordinate']][1]<Q(l['threshold']) if l['relation']=='<' else ((xl,xh),(yl,yh))[l['free_coordinate']][0]>Q(l['threshold']) for l in clause['literals']),'old complement throughout anchor')
        containing.append(entry['entry_id'])
    need(len(containing)==8,'8 previous residual projections contain whole anchor')
    need(data['new_excluded_closed_rectangle']['box']==box and data['new_excluded_closed_rectangle']['Y_extrema']==[0,3],'reported rectangle')
    need(Q(data['new_excluded_closed_rectangle']['area'])==(xh-xl)*(yh-yl)==Q(1,32768),'positive new area')
    return cells,containing,mingap,maximum_rhs


def main():
    data=read(NEW)
    cells,containing,mingap,rhs=validate(data)
    rejected=[]
    for mutation in ('nonstrict_complement','changed_old_clause','lost_separation'):
        bad=deepcopy(data)
        entry=next(e for e in bad['entries'] if e['Y_extrema']==[0,3])
        if mutation=='nonstrict_complement':entry['outside_Y_clauses'][-1]['literals'][0]['relation']='<='
        elif mutation=='changed_old_clause':entry['outside_Y_clauses'][0]['literals'][0]['threshold']='-1'
        else:del entry['additional_necessary_constraints']
        try:validate(bad)
        except AssertionError:rejected.append(mutation)
        else:raise AssertionError('mutation accepted')
    out={'status':'PASS','source_queue':{'path':NEW,'sha256':sha(NEW)},'predecessor_queue':{'path':OLD,'sha256':sha(OLD)},
         'entries_retained':258,'entries_with_appended_clause':70,'other_entries_unchanged':188,
         'all_predecessor_values_and_separation_constraints_preserved':True,
         'strict_complement_endpoint_open_cells':cells,'new_rectangle_area':'1/32768',
         'whole_rectangle_minimum_gap':str(mingap),'whole_rectangle_maximum_separation_rhs':str(rhs),
         'previous_residual_entries_containing_whole_rectangle':containing,
         'mutation_controls_rejected':rejected,'solver_queries_run':0,'proof_kernel_calls_run':0,
         'scope':'Exact queue and continuous rectangle integration. Existing externally checked proof and independent geometry receipt are hash-bound, not rerun. No entry nonemptiness, total residual area, or complete coverage assertion.'}
    (ROOT/OUT).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
